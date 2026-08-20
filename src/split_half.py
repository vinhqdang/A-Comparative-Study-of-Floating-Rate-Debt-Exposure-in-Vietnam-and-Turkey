"""
Split-half reliability and variance decomposition of estimated repricing
exposure (Propositions 2, 6 and Corollary 1 of the manuscript).

Reuses exposure.py's macro_frame()/firm_frame() and the same 2012-2022
estimation window, EST_WINDOW, and trimming convention (clip at the 2nd/98th
country percentile before standardising). For each firm, the window's
diff-year observations are split at the median available year into two
contiguous, non-overlapping halves; theta (beta_rate) and gamma (beta_fx)
are re-estimated independently on each half. Short-term debt share and
export share -- included as a benchmark of traits that are NOT
regression-estimated -- are split the same way and averaged within each half.

The split-half correlation across firms between the two halves' estimates
is the reliability ratio lambda under Proposition 2's model (an unbiased
true score observed with independent noise in each half, so two
independently-drawn halves correlate at exactly lambda, with no
Spearman-Brown step-up: the manuscript is explicit that the correlation
*is* the estimate, not a half-length proxy for it).

The variance decomposition additionally estimates each firm's classical
sampling variance of beta_rate from its own full-window OLS covariance
matrix, so the naive "how much of the dispersion looks like it could be
sampling noise" reliability can be contrasted with the split-half number
that Proposition 2 says is the right one.
"""
from __future__ import annotations

import pathlib
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RES = ROOT / "results"
RES.mkdir(exist_ok=True)

import sys
sys.path.insert(0, str(ROOT / "src"))
from exposure import EST_WINDOW, macro_frame  # noqa: E402

MIN_OBS_HALF = 3


def _trait_frame() -> pd.DataFrame:
    """Firm-year short-term debt share and export share, for the two traits
    carried alongside the regression-estimated measures as a stable-trait
    benchmark."""
    vn = pd.read_csv(PROC / "vn_panel.csv").assign(country="VN")
    tr = pd.read_csv(PROC / "tr_panel.csv").assign(country="TR")
    cols = ["country", "ticker", "year", "st_debt_share", "export_share"]
    for df in (vn, tr):
        if "export_share" not in df.columns:
            df["export_share"] = np.nan
    d = pd.concat([vn.reindex(columns=cols), tr.reindex(columns=cols)], ignore_index=True)
    d["st_debt_share"] = d.st_debt_share.where(d.st_debt_share.between(0, 1))
    d["firm"] = d.country + "_" + d.ticker.astype(str)
    return d


def _firm_years() -> pd.DataFrame:
    """Firm-year implied-rate diffs merged with macro diffs and traits,
    restricted to EST_WINDOW -- the same universe exposure.estimate() uses."""
    vn = pd.read_csv(PROC / "vn_panel.csv").assign(country="VN")
    tr = pd.read_csv(PROC / "tr_panel.csv").assign(country="TR")
    cols = ["country", "ticker", "year", "implied_rate", "total_debt"]
    df = pd.concat([vn.reindex(columns=cols), tr.reindex(columns=cols)], ignore_index=True)
    df = df[df.total_debt.notna() & (df.total_debt > 0)]
    df["implied_rate"] = df.implied_rate.where(df.implied_rate.between(0, 1))
    df["firm"] = df.country + "_" + df.ticker.astype(str)
    df = df.sort_values(["firm", "year"])
    df["d_ir"] = df.groupby("firm")["implied_rate"].diff()

    macro = macro_frame()
    d = df.merge(macro, on=["country", "year"], how="inner")
    d = d[d.year.between(*EST_WINDOW)].dropna(subset=["d_ir", "d_rate", "d_lnfx"])

    traits = _trait_frame()
    d = d.merge(traits[["firm", "year", "st_debt_share", "export_share"]],
                on=["firm", "year"], how="left")
    return d


def _ols_beta_rate(g: pd.DataFrame):
    """Fit d_ir on [1, d_rate, d_lnfx]; return (beta_rate, beta_fx, r2,
    sampling variance of beta_rate) or None if under-identified."""
    if len(g) < 3:
        return None
    X = np.column_stack([np.ones(len(g)), g["d_rate"], g["d_lnfx"]])
    y = g["d_ir"].to_numpy()
    try:
        xtx_inv = np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        return None
    coef = xtx_inv @ X.T @ y
    fit = X @ coef
    resid = y - fit
    dof = len(g) - X.shape[1]
    ss_res = float((resid ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    sigma2 = ss_res / dof if dof > 0 else np.nan
    var_rate = sigma2 * xtx_inv[1, 1] if dof > 0 else np.nan
    return {"beta_rate": float(coef[1]), "beta_fx": float(coef[2]),
            "r2": r2, "var_rate": var_rate, "n": len(g)}


def full_window_estimates(d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for firm, g in d.groupby("firm"):
        fit = _ols_beta_rate(g)
        if fit is None or fit["n"] < 6:
            continue
        fit["firm"] = firm
        fit["country"] = g["country"].iat[0]
        rows.append(fit)
    return pd.DataFrame(rows)


def _one_split(d: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """One random partition of each firm's own available diff-years into two
    groups of equal size (the odd one out, when the year count is odd, falls
    in the second group); regression measures re-estimated on each half,
    trait measures averaged on each half."""
    rows = []
    for firm, g in d.groupby("firm"):
        years = np.sort(g.year.unique())
        if len(years) < 2 * MIN_OBS_HALF:
            continue
        shuffled = rng.permutation(years)
        half = len(years) // 2
        set1 = set(shuffled[:half])
        h1 = g[g.year.isin(set1)]
        h2 = g[~g.year.isin(set1)]
        if len(h1) < MIN_OBS_HALF or len(h2) < MIN_OBS_HALF:
            continue
        f1, f2 = _ols_beta_rate(h1), _ols_beta_rate(h2)
        if f1 is None or f2 is None:
            continue
        rows.append({
            "firm": firm, "country": g["country"].iat[0],
            "theta_1": f1["beta_rate"], "theta_2": f2["beta_rate"],
            "gamma_1": f1["beta_fx"], "gamma_2": f2["beta_fx"],
            "r2_1": f1["r2"], "r2_2": f2["r2"], "n_1": f1["n"], "n_2": f2["n"],
            "st_1": h1.st_debt_share.mean(), "st_2": h2.st_debt_share.mean(),
            "exp_1": h1.export_share.mean(), "exp_2": h2.export_share.mean(),
        })
    return pd.DataFrame(rows)


N_SPLITS = 200


def split_half_estimates(d: pd.DataFrame, seed: int = 0) -> pd.DataFrame:
    """Average split-half estimates over N_SPLITS random half/half
    partitions of each firm's years (Cronbach-style averaging over splits),
    rather than reporting a single arbitrary partition, since a lone split
    is itself a noisy draw of the very quantity Proposition~2 says is
    unreliable. Returns one row per (split, firm); downstream correlations
    are computed per split and then averaged across splits."""
    rng = np.random.default_rng(seed)
    frames = []
    for i in range(N_SPLITS):
        s = _one_split(d, rng)
        if not s.empty:
            s["split"] = i
            frames.append(s)
    return pd.concat(frames, ignore_index=True)


def _clip(s: pd.Series) -> pd.Series:
    """Winsorise at the 2nd/98th percentile, matching exposure.py's own
    convention. Each side of a split-half pair is clipped against its own
    quantiles rather than a quantile pooled across both halves, so an
    outlier estimate on one half cannot be carried over to distort the
    other half's clipping threshold."""
    return s.clip(s.quantile(0.02), s.quantile(0.98)) if s.notna().sum() > 20 else s


def _split_corr(g: pd.DataFrame, c1: str, c2: str) -> float:
    """Correlation for one split (one country, one split index)."""
    s1, s2 = g[c1], g[c2]
    m = s1.notna() & s2.notna()
    if m.sum() < 5:
        return np.nan
    s1c, s2c = _clip(s1[m]), _clip(s2[m])
    if s1c.std() == 0 or s2c.std() == 0:
        return np.nan
    return float(np.corrcoef(s1c, s2c)[0, 1])


def _corr(df, c1, c2, by):
    """Mean correlation across the N_SPLITS random partitions, per
    country -- the average-split-half reliability estimate."""
    out = {}
    for country, g in by.items():
        per_split = g.groupby("split").apply(lambda s: _split_corr(s, c1, c2))
        out[country] = float(per_split.mean(skipna=True))
    return out


def split_half_table(sp: pd.DataFrame) -> pd.DataFrame:
    by = {c: g for c, g in sp.groupby("country")}
    rows = {
        "Repricing sensitivity theta": _corr(sp, "theta_1", "theta_2", by),
        "FX sensitivity gamma": _corr(sp, "gamma_1", "gamma_2", by),
        "Short-term debt share": _corr(sp, "st_1", "st_2", by),
        "Export share": _corr(sp, "exp_1", "exp_2", by),
    }
    out = pd.DataFrame(rows).T
    out.to_csv(RES / "split_half_reliability.csv")
    return out


def decomposition_table(full: pd.DataFrame, sp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for country in ("VN", "TR"):
        f = full[full.country == country]
        theta = _clip(f.beta_rate)
        var_total = float(theta.var(ddof=1))
        sampling = float(f.var_rate.dropna().median())
        reliab_sampling = 1 - sampling / var_total if var_total > 0 else np.nan

        s = sp[sp.country == country]
        rho = _corr(sp, "theta_1", "theta_2", {country: s})[country]
        permanent = max(0.0, rho) * var_total
        transitory = var_total - permanent
        rows.append({
            "country": country, "var_total": var_total,
            "sampling_component": sampling,
            "reliability_sampling_alone": reliab_sampling,
            "split_half_correlation": rho,
            "permanent_component": permanent,
            "transitory_component": transitory,
            "transitory_share": transitory / var_total if var_total > 0 else np.nan,
        })
    out = pd.DataFrame(rows).set_index("country")
    out.to_csv(RES / "variance_decomposition.csv")
    return out


def main():
    d = _firm_years()
    full = full_window_estimates(d)
    sp = split_half_estimates(d)

    print("=== Table: split-half reliability of candidate exposure measures ===")
    print(split_half_table(sp).round(3).to_string())

    print("\n=== Table: variance decomposition of estimated repricing sensitivities ===")
    print(decomposition_table(full, sp).T.round(6).to_string())

    print("\n=== Full-window median in-sample R2 (2012-2022) ===")
    print(full.groupby("country").r2.median().round(3).to_string())

    print("\n=== Split-half-window median in-sample R2 ===")
    r2s = pd.concat([sp[["country", "r2_1"]].rename(columns={"r2_1": "r2"}),
                      sp[["country", "r2_2"]].rename(columns={"r2_2": "r2"})])
    print(r2s.groupby("country").r2.median().round(3).to_string())
    print(f"\nnull benchmark k/(T-1), k=2, median half-length "
          f"T={int(pd.concat([sp.n_1, sp.n_2]).median())}: "
          f"{2/(pd.concat([sp.n_1, sp.n_2]).median()-1):.3f}")


if __name__ == "__main__":
    main()
