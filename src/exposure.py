"""
Estimate revealed repricing exposure: how strongly each firm's own realised
cost of debt moves with the policy rate.

For every firm, over a window that ends before treatment:

    d(implied rate)_it = a_i + b_i * d(rate)_t + g_i * d(ln FX)_t + e_it

    implied rate_it = |interest expense_it| / average debt_it

b_i is the repricing beta -- the object the design calls for. It measures
exposure from behaviour rather than from a balance-sheet ratio, which matters
because the short-maturity share turned out to proxy credit quality as much as
repricing risk (see results/interim-findings.md).

g_i is carried alongside deliberately rather than as a nuisance control. In
Türkiye a large share of movement in realised borrowing cost comes from
currency revaluation on FX debt, not from the policy rate. Estimating the two
jointly separates the repricing channel from the FX-mismatch channel instead of
letting them contaminate one another.

The estimation window ends in 2022 and treatment begins in 2023, so exposure is
strictly pre-determined.
"""

from __future__ import annotations

import pathlib
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

EST_WINDOW = (2012, 2022)
MIN_OBS = 6


def fx_series() -> pd.DataFrame:
    """Annual FX rates from Yahoo Finance.

    Yahoo's VND=X series carries a single corrupted observation at end-2016
    (2.33 instead of approximately 22,000 -- evidently a bad tick, since VND
    was flat at roughly 22,000-22,400 through 2015-2017 and the Turkish lira
    series over the same window has no comparable discontinuity). A value
    implausible relative to both neighbouring years is replaced by linear
    interpolation rather than silently propagated into a log-difference,
    which would otherwise produce a spurious +-900% swing in the FX beta
    regression for one year and its reversal the next.
    """
    import yfinance as yf
    out = []
    for pair, country in (("VND=X", "VN"), ("TRY=X", "TR")):
        h = yf.Ticker(pair).history(start="2009-01-01", interval="1mo")
        a = h["Close"].resample("YE").last()
        a.index = a.index.year
        a = a.sort_index()
        for yr in a.index[1:-1]:
            prev, cur, nxt = a.loc[yr - 1], a.loc[yr], a.loc[yr + 1]
            if cur < 0.5 * min(prev, nxt) or cur > 2.0 * max(prev, nxt):
                a.loc[yr] = (prev + nxt) / 2
        out.append(pd.DataFrame({"country": country,
                                 "year": a.index,
                                 "fx": a.values}))
    return pd.concat(out, ignore_index=True)


def macro_frame() -> pd.DataFrame:
    """Country-year rate and FX, first-differenced."""
    m = pd.read_csv(PROC / "macro_rates.csv")
    # Türkiye uses the BIS policy rate; Vietnam has no BIS entry, so the World
    # Bank average lending rate is the only annual series available.
    m["rate"] = np.where(m.country == "TR",
                         m["policy_rate_eop"], m["lending_rate"])
    m = m[["country", "year", "rate"]].dropna()

    m = m.merge(fx_series(), on=["country", "year"], how="left")
    m = m.sort_values(["country", "year"])
    m["d_rate"] = m.groupby("country")["rate"].diff()
    m["d_lnfx"] = m.groupby("country")["fx"].transform(lambda s: np.log(s).diff())
    return m


def firm_frame() -> pd.DataFrame:
    vn = pd.read_csv(PROC / "vn_panel.csv").assign(country="VN")
    frames = [vn[["country", "ticker", "year", "implied_rate", "total_debt"]]]

    tr_path = PROC / "tr_panel.csv"          # İş Yatırım: the long history
    if tr_path.exists():
        tr = pd.read_csv(tr_path).assign(country="TR")
        frames.append(tr[["country", "ticker", "year",
                          "implied_rate", "total_debt"]])

    df = pd.concat(frames, ignore_index=True)
    df = df[df.total_debt.notna() & (df.total_debt > 0)]
    df["implied_rate"] = df["implied_rate"].where(df["implied_rate"].between(0, 1))
    df["firm"] = df["country"] + "_" + df["ticker"].astype(str)
    df = df.sort_values(["firm", "year"])
    df["d_ir"] = df.groupby("firm")["implied_rate"].diff()
    return df


def estimate() -> pd.DataFrame:
    macro = macro_frame()
    firms = firm_frame()

    d = firms.merge(macro, on=["country", "year"], how="inner")
    d = d[d.year.between(*EST_WINDOW)].dropna(subset=["d_ir", "d_rate", "d_lnfx"])

    rows = []
    for firm, g in d.groupby("firm"):
        if len(g) < MIN_OBS:
            continue
        X = np.column_stack([np.ones(len(g)), g["d_rate"], g["d_lnfx"]])
        y = g["d_ir"].to_numpy()
        try:
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        except Exception:
            continue
        fit = X @ coef
        ss_res = float(((y - fit) ** 2).sum())
        ss_tot = float(((y - y.mean()) ** 2).sum())
        rows.append({
            "firm": firm,
            "country": g["country"].iat[0],
            "ticker": g["ticker"].iat[0],
            "n_obs": len(g),
            "beta_rate": float(coef[1]),
            "beta_fx": float(coef[2]),
            "r2": 1 - ss_res / ss_tot if ss_tot > 0 else np.nan,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    # Trim the tails before standardising: per-firm betas from short series
    # have fat tails that would otherwise dominate the standardisation.
    for c in ("beta_rate", "beta_fx"):
        out[c] = out.groupby("country")[c].transform(
            lambda s: s.clip(s.quantile(0.02), s.quantile(0.98)))
        out[c + "_z"] = out.groupby("country")[c].transform(
            lambda s: (s - s.mean()) / s.std())
    return out


def main() -> None:
    exp = estimate()
    if exp.empty:
        print("no firms met the minimum-observation requirement")
        return

    path = PROC / "exposure_betas.csv"
    exp.to_csv(path, index=False)
    print(f"wrote {path}\n")
    print("=== estimated betas ===")
    print(exp.groupby("country").agg(
        firms=("firm", "size"),
        median_obs=("n_obs", "median"),
        beta_rate_mean=("beta_rate", "mean"),
        beta_rate_sd=("beta_rate", "std"),
        beta_fx_mean=("beta_fx", "mean"),
        median_r2=("r2", "median"),
    ).round(4).to_string())

    print("\n=== beta_rate distribution ===")
    print(exp.groupby("country")["beta_rate"]
          .describe(percentiles=[.1, .25, .5, .75, .9]).round(4).to_string())

    share = exp.assign(pos=exp.beta_rate > 0).groupby("country")["pos"].mean()
    print("\nshare of firms with positive repricing beta:")
    print(share.round(3).to_string())


if __name__ == "__main__":
    main()
