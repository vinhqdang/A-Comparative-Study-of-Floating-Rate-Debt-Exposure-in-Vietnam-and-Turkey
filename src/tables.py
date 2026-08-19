"""
Produce the descriptive and robustness exhibits for the manuscript.

Everything written to results/tables/ as CSV and echoed to stdout so the
numbers in the paper can be traced to a single reproducible run.
"""
from __future__ import annotations
import pathlib, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from linearmodels.panel import PanelOLS

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC, OUT = ROOT/"data"/"processed", ROOT/"results"/"tables"
OUT.mkdir(parents=True, exist_ok=True)

def w(s, lo=.01, hi=.99):
    return s.clip(s.quantile(lo), s.quantile(hi)) if s.notna().sum()>20 else s

def load():
    vn = pd.read_csv(PROC/"vn_panel.csv"); vn["country"]="VN"
    tr = pd.read_csv(PROC/"tr_panel.csv"); tr["country"]="TR"
    trY = pd.read_csv(PROC/"tr_panel_yahoo.csv"); trY["country"]="TR"
    return vn, tr, trY

def tbl_descriptives(vn, tr):
    rows=[]
    for lab, d in (("VN", vn), ("TR", tr)):
        d = d[d.year.between(2015,2025) & d.total_debt.gt(0) & d.total_assets.gt(0)].copy()
        d["st_debt_share"]=d.st_debt_share.where(lambda s:s.between(0,1))
        d["debt_to_assets"]=d.debt_to_assets.where(lambda s:s.between(0,2))
        d["implied_rate"]=d.implied_rate.where(lambda s:s.between(0,1))
        d["icr"]=d.icr.where(lambda s:s.between(-50,100))
        for v in ["total_assets","debt_to_assets","st_debt_share","implied_rate","icr","roa"]:
            if v not in d: continue
            s=w(d[v].dropna())
            if v=="total_assets": s=np.log(s[s>0])
            rows.append({"country":lab,"variable":("log_assets" if v=="total_assets" else v),
                         "n":len(s),"mean":round(s.mean(),3),"sd":round(s.std(),3),
                         "p25":round(s.quantile(.25),3),"median":round(s.median(),3),
                         "p75":round(s.quantile(.75),3)})
    t=pd.DataFrame(rows); t.to_csv(OUT/"t1_descriptives.csv",index=False)
    print("\n### Table: descriptive statistics, 2015-2025\n"); print(t.to_string(index=False))
    return t

def tbl_coverage(vn, tr):
    rows=[]
    for lab,d in (("VN",vn),("TR",tr)):
        for y in range(2015,2026):
            s=d[d.year==y]
            rows.append({"country":lab,"year":y,"firms":s.ticker.nunique(),
                         "with_debt":int((s.total_debt>0).sum())})
    t=pd.DataFrame(rows).pivot(index="year",columns="country",values="firms")
    t.to_csv(OUT/"t2_coverage.csv")
    print("\n### Table: firms per year\n"); print(t.to_string())
    return t

def tbl_placebo(vn, trY):
    """Assign a fake treatment year well before the real one. A design that is
    working should return nothing here."""
    rows=[]
    for lab, d, expo_src in (("VN", vn, vn), ("TR", trY, pd.read_csv(PROC/"tr_panel.csv"))):
        d=d[d.year.between(2015,2021)].copy()      # window ends before real treatment
        d["icr"]=d.icr.where(lambda s:s.between(-50,100))
        d["ebit_margin"]=(d.ebit/d.revenue).where(lambda s:s.between(-2,2))
        e=expo_src[expo_src.year==2016][["ticker","st_debt_share"]].rename(
            columns={"st_debt_share":"expo"})
        e["expo"]=e.expo.where(lambda s:s.between(0,1))
        d=d.merge(e,on="ticker",how="inner").dropna(subset=["expo"])
        d["expo_z"]=(d.expo-d.expo.mean())/d.expo.std()
        d["post"]=(d.year>=2018).astype(int)       # placebo treatment
        for y in ("icr","ebit_margin"):
            s=d.dropna(subset=[y,"expo_z"]).copy()
            if s.ticker.nunique()<40: continue
            s["treat"]=s.expo_z*s.post
            s=s.set_index(["ticker","year"])
            try:
                r=PanelOLS(s[y],s[["treat"]],entity_effects=True,time_effects=True,
                           drop_absorbed=True).fit(cov_type="clustered",cluster_entity=True)
                rows.append({"country":lab,"outcome":y,"placebo_year":2018,
                             "n":int(r.nobs),"coef":round(float(r.params["treat"]),4),
                             "se":round(float(r.std_errors["treat"]),4),
                             "p":round(float(r.pvalues["treat"]),4)})
            except Exception: pass
    t=pd.DataFrame(rows); t.to_csv(OUT/"t3_placebo.csv",index=False)
    print("\n### Table: placebo treatment at 2018\n"); print(t.to_string(index=False))
    return t

def tbl_reliability_grid(vn, tr):
    """Split-half reliability of measured characteristics, several horizons."""
    rows=[]
    for lab,d in (("VN",vn),("TR",tr)):
        d=d.copy()
        d["st"]=d.st_debt_share.where(lambda s:s.between(0,1))
        d["lev"]=d.debt_to_assets.where(lambda s:s.between(0,2))
        for v,name in (("st","short-term debt share"),("lev","debt to assets")):
            p=d.pivot_table(index="ticker",columns="year",values=v)
            for a,b in ((2016,2019),(2016,2022),(2019,2022)):
                if {a,b}<=set(p.columns):
                    s=p[[a,b]].dropna()
                    if len(s)>40:
                        rows.append({"country":lab,"measure":name,"years":f"{a}-{b}",
                                     "n":len(s),"corr":round(float(np.corrcoef(s[a],s[b])[0,1]),3)})
    t=pd.DataFrame(rows); t.to_csv(OUT/"t4_reliability.csv",index=False)
    print("\n### Table: persistence of measured characteristics\n"); print(t.to_string(index=False))
    return t

def main():
    vn, tr, trY = load()
    tbl_coverage(vn, tr); tbl_descriptives(vn, tr)
    tbl_reliability_grid(vn, tr); tbl_placebo(vn, trY)
    print(f"\nwrote exhibits to {OUT}")

if __name__ == "__main__":
    main()
