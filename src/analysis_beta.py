"""
The paper's primary test: do firms whose borrowing costs actually reprice with
policy suffer larger deterioration in default risk once policy tightens?

Exposure is the repricing beta from src/exposure.py, estimated over 2012-2022
and standardised within country, so it is pre-determined and measured from
revealed behaviour rather than from a balance-sheet ratio.

Two specifications:

  DiD          Y_it = b * (beta_z x post_t) + firm FE + year FE
  Event study  Y_it = sum_k b_k * (beta_z x 1[year = k]) + firm FE + year FE

The event study is the one that matters. It shows whether high-beta firms were
already drifting apart before 2023, which is the assumption the whole design
rests on and which the previous specification could not test.
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

WINDOW = (2018, 2025)
BASE_YEAR = 2022          # omitted category in the event study
OUTCOMES = ["icr", "altman_z", "roa", "implied_rate"]


def _winsor(s):
    return s.clip(s.quantile(0.01), s.quantile(0.99)) if s.notna().sum() > 20 else s


def build() -> pd.DataFrame:
    vn = pd.read_csv(PROC / "vn_panel.csv").assign(country="VN")
    frames = [vn]
    tr_path = PROC / "tr_panel.csv"
    if tr_path.exists():
        tr = pd.read_csv(tr_path).assign(country="TR")
        frames.append(tr)

    cols = ["country", "ticker", "year", "icr", "altman_z", "roa",
            "implied_rate", "total_debt", "total_assets"]
    df = pd.concat([f.reindex(columns=cols) for f in frames], ignore_index=True)

    df = df[df.year.between(*WINDOW)]
    df = df[df.total_debt.notna() & (df.total_debt > 0)
            & df.total_assets.gt(0)]
    df["icr"] = df["icr"].where(df["icr"].between(-50, 100))
    df["implied_rate"] = df["implied_rate"].where(df["implied_rate"].between(0, 1))
    df["firm"] = df["country"] + "_" + df["ticker"].astype(str)

    for c in OUTCOMES:
        df[c] = df.groupby(["country", "year"])[c].transform(_winsor)

    exp = pd.read_csv(PROC / "exposure_betas.csv")[
        ["firm", "beta_rate_z", "beta_fx_z", "n_obs"]]
    df = df.merge(exp, on="firm", how="inner")
    df["post"] = (df.year >= 2023).astype(int)
    return df


def did(df: pd.DataFrame, country: str) -> pd.DataFrame:
    d0 = df[df.country == country]
    rows = []
    for y in OUTCOMES:
        d = d0.dropna(subset=[y, "beta_rate_z"]).copy()
        if d.firm.nunique() < 30:
            continue
        d["treat"] = d["beta_rate_z"] * d["post"]
        d = d.set_index(["firm", "year"])
        try:
            r = PanelOLS(d[y], d[["treat"]], entity_effects=True,
                         time_effects=True, drop_absorbed=True
                         ).fit(cov_type="clustered", cluster_entity=True)
        except Exception:
            continue
        rows.append({"country": country, "outcome": y, "n": int(r.nobs),
                     "firms": d.index.get_level_values(0).nunique(),
                     "coef": round(float(r.params["treat"]), 4),
                     "se": round(float(r.std_errors["treat"]), 4),
                     "p": round(float(r.pvalues["treat"]), 4)})
    return pd.DataFrame(rows)


def event_study(df: pd.DataFrame, country: str, y: str) -> pd.DataFrame:
    d = df[(df.country == country)].dropna(subset=[y, "beta_rate_z"]).copy()
    years = sorted(d.year.unique())
    cols = []
    for yr in years:
        if yr == BASE_YEAR:
            continue
        name = f"b_{yr}"
        d[name] = d["beta_rate_z"] * (d.year == yr).astype(int)
        cols.append(name)
    if not cols or d.firm.nunique() < 30:
        return pd.DataFrame()

    dd = d.set_index(["firm", "year"])
    try:
        r = PanelOLS(dd[y], dd[cols], entity_effects=True, time_effects=True,
                     drop_absorbed=True).fit(cov_type="clustered",
                                             cluster_entity=True)
    except Exception:
        return pd.DataFrame()

    out = []
    for c in cols:
        if c in r.params.index:
            out.append({"year": int(c.split("_")[1]),
                        "coef": round(float(r.params[c]), 4),
                        "se": round(float(r.std_errors[c]), 4),
                        "p": round(float(r.pvalues[c]), 4)})
    out.append({"year": BASE_YEAR, "coef": 0.0, "se": 0.0, "p": np.nan})
    return pd.DataFrame(out).sort_values("year")


def main() -> None:
    df = build()
    RES.mkdir(exist_ok=True)

    print("=== sample ===")
    print(df.groupby(["country", "year"]).firm.nunique().to_string())

    all_did = []
    for c in sorted(df.country.unique()):
        res = did(df, c)
        if not res.empty:
            all_did.append(res)

    if all_did:
        tab = pd.concat(all_did, ignore_index=True)
        tab.to_csv(RES / "did_beta.csv", index=False)
        print("\n=== PRIMARY: repricing beta x post "
              "(firm FE + year FE, clustered by firm) ===")
        print(tab.to_string(index=False))

    for c in sorted(df.country.unique()):
        for y in ("icr", "altman_z"):
            ev = event_study(df, c, y)
            if ev.empty:
                continue
            ev.to_csv(RES / f"event_{c}_{y}.csv", index=False)
            print(f"\n=== EVENT STUDY {c} / {y}  (base {BASE_YEAR}) ===")
            for _, r in ev.iterrows():
                star = "" if pd.isna(r.p) else (
                    "***" if r.p < .01 else "**" if r.p < .05
                    else "*" if r.p < .1 else "")
                bar = "" if r.year == BASE_YEAR else f"  {r.coef:+.3f} ({r.se:.3f}){star}"
                mark = " <- treatment" if r.year == 2023 else ""
                print(f"  {int(r.year)}{bar}{mark}")


if __name__ == "__main__":
    main()
