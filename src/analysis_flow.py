"""
Main specification: monetary tightening and corporate distress, restricted to
outcomes that survive Turkish inflation accounting.

Why the restriction
-------------------
TMS-29 restates non-monetary stocks (fixed assets, inventory, equity) by an
index tied to each asset's vintage, while monetary items (debt, cash) are
already in period-end purchasing power. Because vintage differs across firms,
the restatement effect on any stock-based ratio is *heterogeneous across
firms* and lands on 2022-23 -- exactly the treatment date. It therefore enters
as an exposure-by-post interaction and fixed effects cannot absorb it. Turkish
median leverage falls from 0.226 in 2019 to 0.100 in 2024 on this mechanism
alone.

Income-statement items are restated to period-end purchasing power by a common
CPI factor, so a ratio of two flows is approximately unaffected, and a common
multiplicative factor is absorbed by year effects. The outcomes here are
therefore all flow-based:

    implied rate    interest expense / average debt   (monetary / monetary)
    interest cover  EBIT / interest expense           (flow / flow)
    EBIT margin     EBIT / revenue                    (flow / flow)
    debt growth     d log(total debt)                 (common inflation in year FE)

Deliberately excluded: Altman Z'', debt-to-assets, equity ratios, ROA -- every
one of them stock-based.

Source choice
-------------
Turkish flows come from Yahoo, not İş Yatırım, because `4BB` bundles FX
revaluation into financial expense. Using it while treating FX exposure as the
regressor would be circular. Turkish *exposure* is taken from İş Yatırım at
2021, before restatement, since balance-sheet characteristics are what that
source measures well.
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

EXPO_YEAR = 2021          # pre-treatment and pre-restatement
BASE = 2022               # omitted year in the event study
WINDOW = (2021, 2025)
LONG_WINDOW = (2015, 2025)   # for outcomes that do not use interest expense

OUTCOMES = ["implied_rate", "icr", "ebit_margin", "debt_growth"]


def _w(s):
    return s.clip(s.quantile(.02), s.quantile(.98)) if s.notna().sum() > 20 else s


def _flows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["ticker", "year"]).copy()
    df["ebit_margin"] = (df["ebit"] / df["revenue"]).where(
        lambda s: s.between(-2, 2))
    df["debt_growth"] = df.groupby("ticker")["total_debt"].transform(
        lambda s: np.log(s.where(s > 0)).diff())
    df["implied_rate"] = df["implied_rate"].where(lambda s: s.between(0, 3))
    df["icr"] = df["icr"].where(lambda s: s.between(-50, 100))
    return df


def build() -> pd.DataFrame:
    # ---- Türkiye: flows from Yahoo, exposure from İş Yatırım ---------------
    tr = _flows(pd.read_csv(PROC / "tr_panel_yahoo.csv"))
    tr["country"] = "TR"

    iy = pd.read_csv(PROC / "tr_panel.csv")
    iy = iy[iy.year == EXPO_YEAR].copy()
    iy["fx_liab"] = -(iy.net_fx_position / iy.total_assets)
    iy["st_share"] = iy.st_debt_share
    tr_exp = iy[["ticker", "fx_liab", "st_share"]]
    tr = tr.merge(tr_exp, on="ticker", how="inner")

    # ---- Vietnam ----------------------------------------------------------
    vn = _flows(pd.read_csv(PROC / "vn_panel.csv"))
    vn["country"] = "VN"
    vexp = vn[vn.year == EXPO_YEAR][["ticker", "st_debt_share"]].rename(
        columns={"st_debt_share": "st_share"})
    vn = vn.merge(vexp, on="ticker", how="inner")
    vn["fx_liab"] = np.nan

    # EBIT margin and debt growth need no interest figure, so the FX bundling
    # in `4BB` is irrelevant for them and the İş Yatırım history can be used
    # instead -- buying a real pre-period and a testable event study.
    iy_long = _flows(pd.read_csv(PROC / "tr_panel.csv"))
    iy_long["country"] = "TR"
    iy_long = iy_long.merge(tr_exp, on="ticker", how="inner")
    iy_long["implied_rate"] = np.nan      # contaminated: 4BB bundles FX losses
    iy_long["icr"] = np.nan
    iy_long = iy_long[iy_long.year.between(*LONG_WINDOW)]

    cols = ["country", "ticker", "year", "st_share", "fx_liab"] + OUTCOMES
    tr_short = tr.reindex(columns=cols)
    tr_short = tr_short[tr_short.year.between(*WINDOW)]

    # Interest-based outcomes from Yahoo; the other two from the long history.
    tr_long = iy_long.reindex(columns=cols)
    tr_all = (pd.concat([tr_short, tr_long], ignore_index=True)
              .groupby(["country", "ticker", "year"], as_index=False)
              .agg({c: "first" for c in
                    ["st_share", "fx_liab"] + OUTCOMES}))

    vn_all = vn.reindex(columns=cols)
    vn_all = vn_all[vn_all.year.between(*LONG_WINDOW)]

    df = pd.concat([tr_all, vn_all], ignore_index=True)

    df["st_share"] = df.st_share.where(lambda s: s.between(0, 1))
    df["fx_liab"] = df.fx_liab.where(lambda s: s.between(-2, 2))

    for c in OUTCOMES:
        df[c] = df.groupby(["country", "year"])[c].transform(_w)

    # Standardise exposure within country: coefficients are per SD.
    for c in ("st_share", "fx_liab"):
        df[c + "_z"] = df.groupby("country")[c].transform(
            lambda s: (s - s.mean()) / s.std())

    df["firm"] = df.country + "_" + df.ticker.astype(str)
    df["post"] = (df.year >= 2023).astype(int)
    return df


def did(df, country, y, expo):
    d = df[df.country == country].dropna(subset=[y, expo]).copy()
    if d.firm.nunique() < 40:
        return None
    d["treat"] = d[expo] * d["post"]
    d = d.set_index(["firm", "year"])
    try:
        r = PanelOLS(d[y], d[["treat"]], entity_effects=True,
                     time_effects=True, drop_absorbed=True
                     ).fit(cov_type="clustered", cluster_entity=True)
    except Exception:
        return None
    return {"country": country, "exposure": expo, "outcome": y,
            "n": int(r.nobs), "firms": d.index.get_level_values(0).nunique(),
            "coef": round(float(r.params["treat"]), 4),
            "se": round(float(r.std_errors["treat"]), 4),
            "p": round(float(r.pvalues["treat"]), 4)}


def event(df, country, y, expo):
    d = df[df.country == country].dropna(subset=[y, expo]).copy()
    cols = []
    for yr in sorted(d.year.unique()):
        if yr == BASE:
            continue
        d[f"e{yr}"] = d[expo] * (d.year == yr)
        cols.append(f"e{yr}")
    if not cols:
        return pd.DataFrame()
    dd = d.set_index(["firm", "year"])
    try:
        r = PanelOLS(dd[y], dd[cols], entity_effects=True, time_effects=True,
                     drop_absorbed=True).fit(cov_type="clustered",
                                             cluster_entity=True)
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame([{"year": int(c[1:]),
                          "coef": round(float(r.params[c]), 4),
                          "se": round(float(r.std_errors[c]), 4),
                          "p": round(float(r.pvalues[c]), 4)}
                         for c in cols if c in r.params.index]).sort_values("year")


def main() -> None:
    df = build()
    RES.mkdir(exist_ok=True)

    print("=== sample (firms per country-year) ===")
    print(df.groupby(["country", "year"]).firm.nunique().to_string())

    rows = []
    for c in ("TR", "VN"):
        for expo in ("st_share_z", "fx_liab_z"):
            if df[df.country == c][expo].notna().sum() < 50:
                continue
            for y in OUTCOMES:
                r = did(df, c, y, expo)
                if r:
                    rows.append(r)

    tab = pd.DataFrame(rows)
    tab.to_csv(RES / "did_flow.csv", index=False)
    print("\n=== MAIN: exposure x post, flow outcomes "
          "(firm FE + year FE, clustered by firm) ===")
    print(tab.to_string(index=False))

    for c, expo in (("TR", "fx_liab_z"), ("TR", "st_share_z"),
                    ("VN", "st_share_z")):
        for y in ("ebit_margin", "debt_growth"):
            ev = event(df, c, y, expo)
            if ev.empty:
                continue
            print(f"\n=== EVENT STUDY {c} / {expo} -> {y} (base {BASE}) ===")
            for _, r in ev.iterrows():
                s = ("***" if r.p < .01 else "**" if r.p < .05
                     else "*" if r.p < .1 else "")
                mark = "  <- treatment" if r.year == 2023 else ""
                print(f"  {int(r.year)}  {r.coef:+.4f} ({r.se:.4f}){s}{mark}")
    print(f"\nwrote {RES / 'did_flow.csv'}")


if __name__ == "__main__":
    main()
