"""
Cross-country test of the dose-response prediction: does the exposure gradient
(or its absence) scale with tightening severity across a 10-country sample
spanning Türkiye's 33.5 percentage points down to Thailand's 2.0?

This extends src/analysis_flow.py's two-country design to N countries. The
identification logic is unchanged: flow outcomes only, exposure measured
pre-treatment, firm and country-year fixed effects. What is new is a
triple-difference in continuous dose rather than a binary country indicator,
and a first-stage check of whether the VALIDATED PRICE measure (not the
exposure proxy) itself scales with dose -- which is the aggregate,
non-firm-level claim this paper can actually support.
"""
from __future__ import annotations
import pathlib, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from linearmodels.panel import PanelOLS

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC = ROOT/"data"/"processed"; RES = ROOT/"results"; RES.mkdir(exist_ok=True)

# Five-country sample: the two decade-long anchors plus the three
# additional markets with the largest, most reliable firm counts among
# the seven fetched after the desk rejection (Brazil, Chile, Hungary and
# Mexico dropped -- the latter two for having fewer firms, 23 and 19,
# than the 83-firm Turkish sample already shown to produce a false
# positive; Brazil and Chile dropped to hold the set to five).
#
# Dose = policy (or, for Vietnam, lending) rate at end-2021 to the TRUE
# maximum reached at any point 2022 onward -- not the year-end value in
# whichever year that maximum happened to occur. This distinction bound
# TR: BIS monthly data shows CBRT held 50.0% from March through November
# 2024, cut to 47.5% only in December; a year-end-only series (which an
# earlier version of this script used) silently reports the December
# figure and mislabels it "the peak," understating the true dose by
# nearly 3pp. Verified against BIS WS_CBPOL monthly series for TR/PL/IL/
# KR (2021-2025) and the World Bank lending-rate annual series for VN
# (no BIS policy-rate series exists for Vietnam). PL/IL/KR's true peaks
# happen to coincide with a year-end reading, so only TR and VN's values
# changed from an earlier, year-end-only computation of this table.
#   TR: 14.00 (2021-12) -> 50.00 (2024-03, held through 2024-11) = 36.00
#   VN: 7.811 (2021)    -> 9.323 (2023, WB series ends there)     = 1.51
#   PL: 1.75  (2021-12) -> 6.75  (2022-09)                        = 5.00
#   IL: 0.10  (2021-12) -> 4.75  (2023-05)                        = 4.65
#   KR: 1.00  (2021-12) -> 3.50  (2023-01)                        = 2.50
DOSE = {"TR":36.00, "VN":1.51, "PL":5.00, "IL":4.65, "KR":2.50}


def _w(s):
    return s.clip(s.quantile(.02), s.quantile(.98)) if s.notna().sum() > 20 else s


def load_all() -> pd.DataFrame:
    vn = pd.read_csv(PROC/"vn_panel.csv"); vn["country"]="VN"
    tr = pd.read_csv(PROC/"tr_panel_yahoo.csv"); tr["country"]="TR"
    multi_path = PROC/"multi_panel.csv"
    frames = [vn, tr]
    if multi_path.exists():
        frames.append(pd.read_csv(multi_path))
    cols = ["country","ticker","year","total_assets","total_debt","st_debt",
            "equity","interest_expense","ebit","icr","implied_rate","roa",
            "debt_to_assets","st_debt_share","revenue","ebit_margin","debt_growth"]
    df = pd.concat([f.reindex(columns=cols) for f in frames], ignore_index=True)
    df = df[df.year.between(2021,2025)]
    df = df[df.total_debt.gt(0) & df.total_assets.gt(0)]
    # Recompute uniformly: some sources carry a partial column, which would
    # otherwise skip recomputation for the rest under a global isna-all check.
    df["ebit_margin"] = df.ebit/df.revenue
    df["implied_rate"] = df.implied_rate.where(lambda s: s.between(0,3))
    df["icr"] = df.icr.where(lambda s: s.between(-50,100))
    df["ebit_margin"] = df.ebit_margin.where(lambda s: s.between(-2,2))
    df["st_debt_share"] = df.st_debt_share.where(lambda s: s.between(0,1))
    for c in ["implied_rate","icr","ebit_margin","debt_growth"]:
        df[c] = df.groupby(["country","year"])[c].transform(_w)
    df["dose"] = df.country.map(DOSE)
    df["firm"] = df.country+"_"+df.ticker.astype(str)
    df["post"] = (df.year>=2023).astype(int)
    return df.dropna(subset=["dose"])


def aggregate_dose_response(df):
    """The paper's supportable claim: aggregate pass-through scales with dose."""
    rows=[]
    for c,g in df.groupby("country"):
        pre = g[g.year==2022].implied_rate.median()
        post = g[g.year.isin([2023,2024])].implied_rate.median()
        icr_pre = g[g.year==2022].icr.median()
        icr_post = g[g.year.isin([2023,2024])].icr.median()
        rows.append({"country":c, "dose_pp":DOSE[c], "n_firms":g.ticker.nunique(),
                     "rate_pre":pre, "rate_post":post,
                     "rate_change_pp":None if pre is None or post is None else round((post-pre)*100,2),
                     "icr_pre":icr_pre, "icr_post":icr_post})
    out = pd.DataFrame(rows).sort_values("dose_pp", ascending=False)
    out.to_csv(RES/"dose_response.csv", index=False)
    print("=== Aggregate dose-response across countries ===")
    print(out.to_string(index=False))
    ok = out.dropna(subset=["rate_change_pp"])
    if len(ok) >= 4:
        corr = np.corrcoef(ok.dose_pp, ok.rate_change_pp)[0,1]
        print(f"\ncorr(policy dose, change in implied rate) = {corr:.3f}  (n={len(ok)})")
    return out


def exposure_gradient(df, expo="st_debt_share"):
    """Does the (already-shown-unreliable) exposure gradient scale with dose?
    Included for completeness / referee anticipation, not as a load-bearing
    result -- see the split-half reliability findings."""
    pre = df[df.year==2021].groupby("firm")[expo].mean().rename("expo")
    d = df.merge(pre, on="firm", how="inner")
    d["expo_z"] = d.groupby("country")["expo"].transform(lambda s:(s-s.mean())/s.std())
    d["dose_z"] = (d.dose-d.dose.mean())/d.dose.std()
    d["treat"] = d.expo_z*d.post
    d["treat_dose"] = d.expo_z*d.post*d.dose_z
    # PanelOLS requires a numeric time index; encode country-year as an
    # integer so "time effects" become country-by-year effects.
    country_code = d.country.astype("category").cat.codes
    d["tvar"] = d.year*100 + country_code
    rows=[]
    for y in ("icr","ebit_margin","implied_rate"):
        s = d.dropna(subset=[y,"treat","treat_dose"]).set_index(["firm","tvar"])
        if s.index.get_level_values(0).nunique() < 60: continue
        try:
            r = PanelOLS(s[y], s[["treat","treat_dose"]], entity_effects=True,
                        time_effects=True, drop_absorbed=True
                        ).fit(cov_type="clustered", cluster_entity=True)
        except Exception:
            continue
        rows.append({"outcome":y, "n":int(r.nobs),
                     "firms":s.index.get_level_values(0).nunique(),
                     "treat_coef":round(float(r.params["treat"]),4),
                     "treat_p":round(float(r.pvalues["treat"]),4),
                     "treat_dose_coef":round(float(r.params["treat_dose"]),4),
                     "treat_dose_p":round(float(r.pvalues["treat_dose"]),4)})
    out = pd.DataFrame(rows)
    out.to_csv(RES/"dose_exposure_gradient.csv", index=False)
    print("\n=== Exposure x dose triple interaction (all countries pooled) ===")
    print(out.to_string(index=False))
    return out


def main():
    df = load_all()
    print(f"Countries: {sorted(df.country.unique())}")
    print(f"Total: {df.firm.nunique()} firms, {len(df):,} firm-years\n")
    aggregate_dose_response(df)
    exposure_gradient(df)


if __name__ == "__main__":
    main()
