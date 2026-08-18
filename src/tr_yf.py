"""
Build a Turkish firm-year panel from Yahoo Finance.

This is the second, independent source for the Turkish side. It is fast
(~2 minutes for the whole exchange) and needs no proxy, but Yahoo only
retains four to five annual periods, so it covers roughly 2021-2025.

Its two jobs:

1. Provide the Turkish panel over the difference-in-differences window
   around the June 2023 policy shift, which is the identification window.
2. Cross-validate the İş Yatırım parse in src/tr_build.py.  Two independent
   sources agreeing on the same firm-years is a materially stronger basis
   for a published panel than either alone.

Long pre-trends (2010-2020) and the Türkiye-specific items -- export sales,
net FX position -- come only from İş Yatırım, so the two sources are
complements, not substitutes.
"""

from __future__ import annotations

import concurrent.futures as cf
import pathlib
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import yfinance as yf

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

# Yahoo's normalised labels -> harmonised names.
BS_MAP = {
    "Total Assets":              "total_assets",
    "Current Assets":            "current_assets",
    "Cash And Cash Equivalents": "cash",
    "Current Liabilities":       "current_liabilities",
    "Stockholders Equity":       "equity",
    "Current Debt":              "st_debt",
    "Long Term Debt":            "lt_debt",
    "Total Debt":                "total_debt_reported",
    "Retained Earnings":         "retained_earnings",
}
IS_MAP = {
    "Total Revenue":    "revenue",
    "EBIT":             "ebit",
    "EBITDA":           "ebitda",
    "Interest Expense": "interest_expense",
    "Pretax Income":    "pretax_income",
    "Net Income":       "net_income",
}


def _one(ticker: str, suffix: str) -> list[dict]:
    try:
        tk = yf.Ticker(f"{ticker}{suffix}")
        bs, fin = tk.balance_sheet, tk.financials
    except Exception:
        return []
    if bs is None or bs.empty:
        return []

    rows: dict[int, dict] = {}
    for label, name in BS_MAP.items():
        if label in bs.index:
            for col, val in bs.loc[label].items():
                rows.setdefault(col.year, {})[name] = val
    if fin is not None and not fin.empty:
        for label, name in IS_MAP.items():
            if label in fin.index:
                for col, val in fin.loc[label].items():
                    rows.setdefault(col.year, {})[name] = val

    out = []
    for year, vals in rows.items():
        vals.update(ticker=ticker, year=year)
        out.append(vals)
    return out


def fetch(tickers: list[str], suffix: str, workers: int = 8) -> pd.DataFrame:
    records: list[dict] = []
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(_one, t, suffix) for t in tickers]
        for i, f in enumerate(cf.as_completed(futs), 1):
            records.extend(f.result())
            if i % 200 == 0:
                print(f"  {i}/{len(tickers)}", flush=True)
    return pd.DataFrame(records)


def derive(df: pd.DataFrame, country: str) -> pd.DataFrame:
    df = df.sort_values(["ticker", "year"]).copy()

    df["total_debt"] = df[["st_debt", "lt_debt"]].sum(axis=1, min_count=1)
    df["total_debt"] = df["total_debt"].fillna(df.get("total_debt_reported"))
    df["total_liabilities"] = df["total_assets"] - df["equity"]

    g = df.groupby("ticker", sort=False)
    df["total_debt_lag"] = g["total_debt"].shift(1)

    df["debt_to_assets"] = df["total_debt"] / df["total_assets"]
    df["leverage"] = df["total_liabilities"] / df["total_assets"]
    df["st_debt_share"] = df["st_debt"] / df["total_debt"]

    avg_debt = df[["total_debt", "total_debt_lag"]].mean(axis=1)
    df["implied_rate"] = df["interest_expense"].abs() / avg_debt

    df["icr"] = df["ebit"] / df["interest_expense"].abs()
    df["roa"] = df["ebit"] / df["total_assets"]
    df["current_ratio"] = df["current_assets"] / df["current_liabilities"]

    x1 = (df["current_assets"] - df["current_liabilities"]) / df["total_assets"]
    x2 = df["retained_earnings"] / df["total_assets"]
    x3 = df["ebit"] / df["total_assets"]
    x4 = df["equity"] / df["total_liabilities"]
    df["altman_z"] = 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4

    df["country"] = country
    df["source"] = "yahoo"
    return df


def main() -> None:
    import borsapy as bp

    tickers = sorted(bp.companies()["ticker"].dropna().unique().tolist())
    print(f"fetching {len(tickers)} BIST tickers from Yahoo", flush=True)

    raw = fetch(tickers, ".IS")
    panel = derive(raw, "TR")

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "tr_panel_yahoo.csv"
    panel.to_csv(path, index=False)

    print(f"\nwrote {path}  rows={len(panel):,}  firms={panel.ticker.nunique()}")
    print(f"years {int(panel.year.min())}-{int(panel.year.max())}")
    key = ["total_assets", "total_debt", "interest_expense", "ebit", "equity"]
    print("\nnon-missing coverage:")
    print((panel[key].notna().mean() * 100).round(1).to_string())
    print("\nfirms per year:")
    print(panel.groupby("year").ticker.nunique().to_string())


if __name__ == "__main__":
    main()
