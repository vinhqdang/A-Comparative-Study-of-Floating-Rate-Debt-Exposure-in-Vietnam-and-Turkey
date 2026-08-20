"""
Cross-validate each country panel against an independent Yahoo Finance pull.

The Vietnamese and Turkish panels are built from national sources
(vnfinancialdata / Hugging Face, and Is Yatirim).  Yahoo Finance is an
independent third party with its own normalisation of the same filings, so
agreement between them is evidence that our item mapping is right, and
disagreement localises exactly which construct is defined differently.

That second case is the useful one: the Turkish interest-expense comparison is
how we discovered that Is Yatirim's `4BB` Financial Expenses bundles FX
revaluation losses and cannot be used as an interest measure.
"""

from __future__ import annotations

import pathlib
import sys
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from tr_yf import derive, fetch  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

FIELDS = ["total_assets", "equity", "total_debt", "revenue",
          "ebit", "interest_expense"]


def compare(national: pd.DataFrame, yahoo: pd.DataFrame, label: str) -> pd.DataFrame:
    m = national.merge(yahoo, on=["ticker", "year"], suffixes=("_nat", "_yh"))
    rows = []
    for f in FIELDS:
        a, b = m.get(f"{f}_nat"), m.get(f"{f}_yh")
        if a is None or b is None:
            continue
        # Interest expense uses opposite sign conventions across sources
        # (one reports it as a negative flow, the other positive); comparing
        # magnitudes is the meaningful test, so take absolute values only here.
        if f == "interest_expense":
            a, b = a.abs(), b.abs()
        ok = a.notna() & b.notna() & (a != 0) & (b != 0)
        if ok.sum() < 5:
            continue
        rel = (b[ok] - a[ok]) / a[ok].abs()
        rows.append({
            "field": f,
            "n": int(ok.sum()),
            "corr": round(float(np.corrcoef(a[ok], b[ok])[0, 1]), 4),
            "median_rel_diff": round(float(rel.median()), 4),
            "within_2pct": round(float((rel.abs() < 0.02).mean()), 3),
        })
    out = pd.DataFrame(rows)
    print(f"\n=== {label}  (overlap: {len(m)} firm-years, "
          f"{m.ticker.nunique()} firms) ===")
    print(out.to_string(index=False))
    return out


def main() -> None:
    # --- Vietnam -----------------------------------------------------------
    vn = pd.read_csv(OUT / "vn_panel.csv")
    # Non-financial firms only: banks and brokers use a different template.
    nf = vn[vn.st_debt.notna() & vn.current_assets.notna()]
    sample = (nf[nf.year == 2023]
              .nlargest(180, "total_assets")["ticker"].tolist())
    print(f"Vietnam: pulling {len(sample)} tickers from Yahoo", flush=True)
    vn_yh = derive(fetch(sample, ".VN"), "VN")
    vn_yh.to_csv(OUT / "vn_panel_yahoo.csv", index=False)
    vn_cmp = compare(vn, vn_yh, "VIETNAM: vnfinancialdata vs Yahoo")

    # --- Turkiye -----------------------------------------------------------
    tr_path = OUT / "tr_panel.csv"
    if tr_path.exists():
        tr = pd.read_csv(tr_path)
        tr_yh = pd.read_csv(OUT / "tr_panel_yahoo.csv")
        tr_cmp = compare(tr, tr_yh, "TURKIYE: Is Yatirim vs Yahoo")
    else:
        tr_cmp = pd.DataFrame()

    rep = OUT / "validation_report.csv"
    pd.concat(
        [vn_cmp.assign(country="VN"), tr_cmp.assign(country="TR")],
        ignore_index=True,
    ).to_csv(rep, index=False)
    print(f"\nwrote {rep}")


if __name__ == "__main__":
    main()
