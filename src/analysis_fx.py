"""
Test the balance-sheet channel the data can actually measure.

The repricing beta failed validation (see results/interim-findings.md): it is
not a stable firm trait. Balance-sheet characteristics are -- FX exposure
persists at 0.52 across 2018-2022 and export share at 0.84 -- so exposure
defined on them is measured, not estimated.

This matters theoretically as well as practically. Türkiye's corporate sector
carries substantial unhedged FX liabilities; Vietnam's does not. If the binding
constraint under tightening is currency mismatch rather than contractual
repricing, then FX exposure is the treatment and Vietnam is the counterfactual
where the channel is absent by construction.

Two outcomes are examined deliberately:
  * price  -- the implied borrowing rate;
  * quantity -- debt growth and leverage.
If banks ration credit rather than reprice it, the channel shows up in
quantities while leaving interest cost flat. That would explain the earlier
null on price without implying the absence of transmission.
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

WINDOW = (2017, 2025)
BASE = 2022
PRE = [2021, 2022]


def _w(s):
    return s.clip(s.quantile(.01), s.quantile(.99)) if s.notna().sum() > 20 else s


def build() -> pd.DataFrame:
    tr = pd.read_csv(PROC / "tr_panel.csv").assign(country="TR")
    tr["fx_exposure"] = (tr.net_fx_position / tr.total_assets)
    tr["export_share"] = tr.export_share.where(lambda s: s.between(0, 1))

    df = tr[tr.year.between(*WINDOW)].copy()
    df = df[df.total_debt.gt(0) & df.total_assets.gt(0)]
    df["fx_exposure"] = df.fx_exposure.where(lambda s: s.between(-2, 2))
    df["implied_rate"] = df.implied_rate.where(lambda s: s.between(0, 3))
    df["icr"] = df.icr.where(lambda s: s.between(-50, 100))
    df["firm"] = df.ticker

    # Quantity outcomes.
    df = df.sort_values(["firm", "year"])
    df["debt_growth"] = df.groupby("firm")["total_debt"].pct_change()
    df["debt_growth"] = df.debt_growth.where(lambda s: s.between(-1, 5))
    df["log_debt"] = np.log(df.total_debt)

    for c in ["icr", "altman_z", "implied_rate", "debt_growth",
              "debt_to_assets", "roa"]:
        df[c] = df.groupby("year")[c].transform(_w)

    # Pre-determined exposure: negative net FX position means FX liabilities
    # exceed FX assets, so flip the sign to make "more exposed" the higher value.
    pre = df[df.year.isin(PRE)].groupby("firm").agg(
        fx=("fx_exposure", "mean"), exp_sh=("export_share", "mean"))
    pre["fx_liab"] = -pre["fx"]
    for c in ("fx_liab", "exp_sh"):
        pre[c + "_z"] = (pre[c] - pre[c].mean()) / pre[c].std()

    df = df.merge(pre[["fx_liab_z", "exp_sh_z"]], on="firm", how="inner")
    df["post"] = (df.year >= 2023).astype(int)
    return df.dropna(subset=["fx_liab_z"])


def did(df, y, expo):
    d = df.dropna(subset=[y, expo]).copy()
    if d.firm.nunique() < 40:
        return None
    d["treat"] = d[expo] * d["post"]
    d = d.set_index(["firm", "year"])
    try:
        r = PanelOLS(d[y], d[["treat"]], entity_effects=True, time_effects=True,
                     drop_absorbed=True).fit(cov_type="clustered",
                                             cluster_entity=True)
    except Exception:
        return None
    return {"outcome": y, "exposure": expo, "n": int(r.nobs),
            "firms": d.index.get_level_values(0).nunique(),
            "coef": round(float(r.params["treat"]), 4),
            "se": round(float(r.std_errors["treat"]), 4),
            "p": round(float(r.pvalues["treat"]), 4)}


def event(df, y, expo):
    d = df.dropna(subset=[y, expo]).copy()
    cols = []
    for yr in sorted(d.year.unique()):
        if yr == BASE:
            continue
        d[f"e{yr}"] = d[expo] * (d.year == yr)
        cols.append(f"e{yr}")
    dd = d.set_index(["firm", "year"])
    try:
        r = PanelOLS(dd[y], dd[cols], entity_effects=True, time_effects=True,
                     drop_absorbed=True).fit(cov_type="clustered",
                                             cluster_entity=True)
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame([
        {"year": int(c[1:]), "coef": round(float(r.params[c]), 4),
         "se": round(float(r.std_errors[c]), 4),
         "p": round(float(r.pvalues[c]), 4)}
        for c in cols if c in r.params.index]).sort_values("year")


def main() -> None:
    df = build()
    RES.mkdir(exist_ok=True)
    print(f"TR sample: {df.firm.nunique()} firms, {len(df):,} obs, "
          f"{int(df.year.min())}-{int(df.year.max())}")
    print("\npre-period FX liability exposure (share of assets, +ve = net FX debt):")
    print((-df.groupby("firm").fx_liab_z.first()).describe().round(3).to_string())

    rows = []
    for expo in ("fx_liab_z", "exp_sh_z"):
        for y in ("implied_rate", "icr", "altman_z", "debt_growth",
                  "debt_to_assets", "roa"):
            r = did(df, y, expo)
            if r:
                rows.append(r)
    tab = pd.DataFrame(rows)
    tab.to_csv(RES / "did_fx.csv", index=False)
    print("\n=== TÜRKİYE: exposure x post (firm FE + year FE, clustered) ===")
    print(tab.to_string(index=False))

    for y in ("debt_growth", "altman_z"):
        ev = event(df, y, "fx_liab_z")
        if ev.empty:
            continue
        print(f"\n=== EVENT STUDY: FX exposure -> {y} (base {BASE}) ===")
        for _, r in ev.iterrows():
            s = "***" if r.p < .01 else "**" if r.p < .05 else "*" if r.p < .1 else ""
            mark = "  <- treatment" if r.year == 2023 else ""
            print(f"  {int(r.year)}  {r.coef:+.4f} ({r.se:.4f}){s}{mark}")


if __name__ == "__main__":
    main()
