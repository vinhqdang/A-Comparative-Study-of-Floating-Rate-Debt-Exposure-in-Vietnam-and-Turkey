"""Event-study and validation figures for the manuscript."""
from __future__ import annotations
import pathlib, sys, warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG = ROOT/"paper"/"tex"/"figs"; FIG.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT/"src"))
from analysis_flow import build, event   # noqa: E402

plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False,
                     "figure.dpi":200,"savefig.bbox":"tight"})

def panel(ax, ev, title):
    ev = pd.concat([ev, pd.DataFrame([{"year":2022,"coef":0.0,"se":0.0}])]).sort_values("year")
    ax.axhline(0, color="0.6", lw=.8)
    ax.axvline(2022.5, color="0.3", lw=.9, ls="--")
    ax.errorbar(ev.year, ev.coef, yerr=1.96*ev.se, fmt="o-", ms=3.5, lw=1.1,
                capsize=2.5, color="#1f4e79", ecolor="#7ba7d1")
    ax.fill_between(ev.year, ev.coef-1.96*ev.se, ev.coef+1.96*ev.se, alpha=.10, color="#1f4e79")
    ax.set_title(title, fontsize=8.5)
    ax.set_xlabel("Year"); ax.set_ylabel("Coefficient")

def main():
    df = build()
    specs = [("TR","st_share_z","debt_growth","Türkiye: short-maturity share on debt growth"),
             ("TR","fx_liab_z","ebit_margin","Türkiye: FX exposure on EBIT margin"),
             ("VN","st_share_z","ebit_margin","Vietnam: short-maturity share on EBIT margin"),
             ("VN","st_share_z","debt_growth","Vietnam: short-maturity share on debt growth")]
    fig, axes = plt.subplots(2,2, figsize=(7.4,5.2))
    for ax,(c,e,y,t) in zip(axes.ravel(), specs):
        ev = event(df, c, y, e)
        if ev.empty: ax.set_visible(False); continue
        panel(ax, ev, t)
    fig.tight_layout(); fig.savefig(FIG/"event_studies.pdf")
    print("wrote", FIG/"event_studies.pdf")

    macro = pd.read_csv(ROOT/"data"/"processed"/"macro_rates.csv")
    vn = pd.read_csv(ROOT/"data"/"processed"/"vn_panel.csv")
    tr = pd.read_csv(ROOT/"data"/"processed"/"tr_panel_yahoo.csv")
    fig, axes = plt.subplots(1,2, figsize=(7.4,2.8))
    v = vn[vn.implied_rate.between(0,1) & vn.year.between(2011,2025)]
    vm = v.groupby("year").implied_rate.median()*100
    mv = macro[macro.country=="VN"].set_index("year").lending_rate.dropna()
    axes[0].plot(vm.index, vm.values, "o-", ms=3, lw=1.2, color="#1f4e79", label="Implied cost")
    axes[0].plot(mv.index, mv.values, "s--", ms=3, lw=1.0, color="#c0504d", label="Lending rate")
    axes[0].set_title("Vietnam", fontsize=9); axes[0].legend(frameon=False, fontsize=7.5)
    t = tr[tr.implied_rate.between(0,3) & tr.year.between(2021,2025)]
    tm = t.groupby("year").implied_rate.median()*100
    mt = macro[macro.country=="TR"].set_index("year").policy_rate_eop
    mt = mt[(mt.index>=2021)&(mt.index<=2025)]
    axes[1].plot(tm.index, tm.values, "o-", ms=3, lw=1.2, color="#1f4e79", label="Implied cost")
    axes[1].plot(mt.index, mt.values, "s--", ms=3, lw=1.0, color="#c0504d", label="CBRT policy")
    axes[1].set_title("Türkiye", fontsize=9); axes[1].legend(frameon=False, fontsize=7.5)
    for ax in axes: ax.set_xlabel("Year"); ax.set_ylabel("Percent")
    fig.tight_layout(); fig.savefig(FIG/"validation.pdf")
    print("wrote", FIG/"validation.pdf")

if __name__ == "__main__":
    main()
