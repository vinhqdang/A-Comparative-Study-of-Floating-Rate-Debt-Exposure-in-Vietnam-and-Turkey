"""
Estimate whether firms with more repricing-exposed debt saw their default risk
deteriorate more once policy tightened, and whether that gradient is steeper in
Türkiye's extreme tightening than in Vietnam's mild one.

Sample construction
-------------------
Vietnam comes from vnfinancialdata and Türkiye from Yahoo Finance. That is a
deliberate choice, not a convenience: the validation exercise in
src/validate.py shows Vietnamese interest expense from vnfinancialdata
reconciles with Yahoo almost exactly (corr 0.991, median difference 0.00%),
while İş Yatırım's `4BB` runs about three times Yahoo's interest expense
because it bundles FX revaluation losses. Using vnfinancialdata for Vietnam
and Yahoo for Türkiye therefore puts both countries on the same construct.

Design
------
Exposure is measured in the pre-period only (2021-2022 average), so it cannot
respond to the treatment. Because it is time-invariant it is absorbed by firm
fixed effects; the interaction with Post is what identifies the effect.

    Y_it = b * (Exposure_i x Post_t) + firm FE + year FE + e_it        [by country]
    Y_it = b * (Exp x Post) + g * (Exp x Post x TR) + firm FE + country-year FE

Standard errors are clustered by firm.
"""

from __future__ import annotations

import pathlib
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RES = ROOT / "results"

PRE = [2021, 2022]
POST_FROM = 2023
WINDOW = (2021, 2025)

OUTCOMES = ["icr", "altman_z", "implied_rate", "roa"]


def _winsor(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    if s.notna().sum() < 20:
        return s
    return s.clip(s.quantile(lo), s.quantile(hi))


def load_panels() -> pd.DataFrame:
    vn = pd.read_csv(PROC / "vn_panel.csv")
    vn["country"] = "VN"
    tr = pd.read_csv(PROC / "tr_panel_yahoo.csv")
    tr["country"] = "TR"

    keep = ["ticker", "year", "country", "total_assets", "total_debt",
            "st_debt", "equity", "interest_expense", "ebit", "icr",
            "altman_z", "implied_rate", "roa", "debt_to_assets",
            "st_debt_share", "current_ratio"]
    for d in (vn, tr):
        for c in keep:
            if c not in d.columns:
                d[c] = np.nan

    df = pd.concat([vn[keep], tr[keep]], ignore_index=True)
    df = df[df.year.between(*WINDOW)]

    # Non-financial firms with real debt: the channel is undefined otherwise,
    # and banks/insurers use incomparable statement templates.
    df = df[df.total_debt.notna() & (df.total_debt > 0)
            & df.total_assets.notna() & (df.total_assets > 0)]

    # Bound ratios at economically meaningful values before winsorising.
    df["implied_rate"] = df["implied_rate"].where(df["implied_rate"].between(0, 3))
    df["st_debt_share"] = df["st_debt_share"].where(df["st_debt_share"].between(0, 1))
    df["icr"] = df["icr"].where(df["icr"].between(-50, 100))
    df["debt_to_assets"] = df["debt_to_assets"].where(df["debt_to_assets"].between(0, 2))

    for col in OUTCOMES + ["debt_to_assets", "st_debt_share"]:
        df[col] = df.groupby(["country", "year"])[col].transform(_winsor)

    df["firm"] = df["country"] + "_" + df["ticker"].astype(str)
    df["post"] = (df.year >= POST_FROM).astype(int)
    df["is_tr"] = (df.country == "TR").astype(int)
    return df


def add_exposure(df: pd.DataFrame) -> pd.DataFrame:
    """Pre-period exposure, standardised within country so the two coefficients
    are on a comparable scale (one standard deviation of exposure)."""
    pre = df[df.year.isin(PRE)]
    exp = (pre.groupby(["country", "firm"])[["st_debt_share", "debt_to_assets"]]
           .mean()
           .rename(columns={"st_debt_share": "exp_stshare",
                            "debt_to_assets": "exp_lev"})
           .reset_index())

    for c in ("exp_stshare", "exp_lev"):
        exp[c + "_z"] = exp.groupby("country")[c].transform(
            lambda s: (s - s.mean()) / s.std())

    df = df.merge(exp.drop(columns=["country"]), on="firm", how="inner")
    return df.dropna(subset=["exp_stshare_z"])


def run(df: pd.DataFrame, y: str, expo: str, subset: str | None) -> dict | None:
    d = df if subset is None else df[df.country == subset]
    d = d.dropna(subset=[y, expo]).copy()
    if d.firm.nunique() < 30:
        return None

    d["treat"] = d[expo] * d["post"]
    if subset is None:
        d["treat_tr"] = d["treat"] * d["is_tr"]
        # PanelOLS requires a numeric time index; encode country-year as an
        # integer so "time effects" become country-by-year effects.
        d["tvar"] = d["year"] * 10 + d["is_tr"]
        exog = ["treat", "treat_tr"]
    else:
        d["tvar"] = d["year"]
        exog = ["treat"]

    d = d.set_index(["firm", "tvar"])
    try:
        m = PanelOLS(d[y], d[exog], entity_effects=True, time_effects=True,
                     drop_absorbed=True)
        r = m.fit(cov_type="clustered", cluster_entity=True)
    except Exception:
        return None

    out = {"outcome": y, "exposure": expo,
           "sample": subset or "pooled",
           "n": int(r.nobs), "firms": int(d.index.get_level_values(0).nunique())}
    for k in exog:
        if k in r.params.index:
            out[f"{k}_coef"] = round(float(r.params[k]), 4)
            out[f"{k}_se"] = round(float(r.std_errors[k]), 4)
            out[f"{k}_p"] = round(float(r.pvalues[k]), 4)
    return out


def main() -> None:
    df = add_exposure(load_panels())
    RES.mkdir(exist_ok=True)

    print("=== sample ===")
    print(df.groupby(["country", "year"]).firm.nunique().to_string())
    print(f"\nfirms: {df.firm.nunique()}  obs: {len(df):,}")

    print("\n=== pre-period exposure (2021-22 mean) ===")
    print(df.groupby("country")[["exp_stshare", "exp_lev"]]
          .agg(["mean", "std"]).round(3).to_string())

    rows = []
    for expo in ("exp_stshare_z", "exp_lev_z"):
        for y in OUTCOMES:
            for sub in ("VN", "TR", None):
                r = run(df, y, expo, sub)
                if r:
                    rows.append(r)

    res = pd.DataFrame(rows)
    res.to_csv(RES / "did_estimates.csv", index=False)

    print("\n=== DiD: exposure x post, by country "
          "(firm FE + year FE, clustered by firm) ===")
    show = res[res["sample"] != "pooled"][
        ["exposure", "outcome", "sample", "n", "firms",
         "treat_coef", "treat_se", "treat_p"]]
    print(show.to_string(index=False))

    print("\n=== Triple difference (pooled, firm FE + country-year FE) ===")
    tri = res[res["sample"] == "pooled"][
        ["exposure", "outcome", "n", "firms",
         "treat_coef", "treat_p", "treat_tr_coef", "treat_tr_p"]]
    print(tri.to_string(index=False))
    print(f"\nwrote {RES / 'did_estimates.csv'}")


if __name__ == "__main__":
    main()
