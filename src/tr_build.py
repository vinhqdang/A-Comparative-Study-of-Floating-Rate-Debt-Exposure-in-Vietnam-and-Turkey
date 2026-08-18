"""
Build the Turkish firm-year panel from cached İş Yatırım responses.

Output: data/processed/tr_panel.csv, using the same column names as
data/processed/vn_panel.csv so the two stack directly.
"""

from __future__ import annotations

import json
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "tr"
OUT = ROOT / "data" / "processed"

# İş Yatırım XI_29 item codes -> harmonised names.
CODES = {
    "1BL":  "total_assets",
    "1A":   "current_assets",
    "1AA":  "cash",
    "2A":   "current_liabilities",
    "2B":   "lt_liabilities",
    "2N":   "equity",
    "2AA":  "st_debt",          # Short-Term Financial Loans
    "2BA":  "lt_debt",          # Long-Term Financial Loans
    "2OCE": "retained_earnings",
    "3C":   "revenue",
    "3DF":  "ebit",             # Operating profit
    "3I":   "pretax_income",
    "3L":   "net_income",
    "4BB":  "interest_expense",  # Financial expenses
    "4B":   "depreciation",
    "4BD":  "export_sales",     # Türkiye only
    "4BE":  "net_fx_position",  # Türkiye only
}


def _read_all() -> pd.DataFrame:
    rows = []
    for path in sorted(RAW.glob("*.json")):
        ticker, y0 = path.stem.rsplit("_", 1)
        y0 = int(y0)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        for item in payload.get("value", []):
            name = CODES.get(item.get("itemCode"))
            if name is None:
                continue
            for i in range(1, 5):
                raw = item.get(f"value{i}")
                if raw in (None, "", "0"):
                    val = 0.0 if raw == "0" else None
                else:
                    try:
                        val = float(raw)
                    except (TypeError, ValueError):
                        val = None
                if val is not None:
                    rows.append((ticker, y0 + i - 1, name, val))

    long = pd.DataFrame(rows, columns=["ticker", "year", "field", "value"])
    if long.empty:
        return long

    long = long.drop_duplicates(subset=["ticker", "year", "field"], keep="last")
    wide = long.pivot(index=["ticker", "year"], columns="field",
                      values="value").reset_index()
    wide.columns.name = None

    for name in CODES.values():
        if name not in wide.columns:
            wide[name] = pd.NA
    return wide


def _derive(df: pd.DataFrame) -> pd.DataFrame:
    """Mirror of src/vn_build.py:_derive, so both panels carry the same fields."""
    df = df.sort_values(["ticker", "year"]).copy()

    df["total_liabilities"] = df[["current_liabilities", "lt_liabilities"]].sum(
        axis=1, min_count=1)
    df["total_debt"] = df[["st_debt", "lt_debt"]].sum(axis=1, min_count=1)

    g = df.groupby("ticker", sort=False)
    df["total_debt_lag"] = g["total_debt"].shift(1)
    df["total_assets_lag"] = g["total_assets"].shift(1)

    df["debt_to_assets"] = df["total_debt"] / df["total_assets"]
    df["leverage"] = df["total_liabilities"] / df["total_assets"]
    df["st_debt_share"] = df["st_debt"] / df["total_debt"]

    avg_debt = df[["total_debt", "total_debt_lag"]].mean(axis=1)
    df["implied_rate"] = df["interest_expense"].abs() / avg_debt

    df["icr"] = df["ebit"] / df["interest_expense"].abs()
    df["roa"] = df["ebit"] / df["total_assets"]
    df["cash_ratio"] = df["cash"] / df["current_liabilities"]
    df["current_ratio"] = df["current_assets"] / df["current_liabilities"]

    x1 = (df["current_assets"] - df["current_liabilities"]) / df["total_assets"]
    x2 = df["retained_earnings"] / df["total_assets"]
    x3 = df["ebit"] / df["total_assets"]
    x4 = df["equity"] / df["total_liabilities"]
    df["altman_z"] = 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4

    # Türkiye-only channels, used for the heterogeneity analysis.
    df["export_share"] = df["export_sales"] / df["revenue"]
    df["fx_exposure"] = df["net_fx_position"] / df["total_assets"]

    df["country"] = "TR"
    return df


def main() -> None:
    wide = _read_all()
    if wide.empty:
        print("no cached responses yet")
        return

    panel = _derive(wide)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "tr_panel.csv"
    panel.to_csv(path, index=False)

    print(f"wrote {path}  rows={len(panel):,}  firms={panel.ticker.nunique()}")
    print(f"years {int(panel.year.min())}-{int(panel.year.max())}")
    key = ["total_assets", "total_debt", "interest_expense", "ebit", "equity"]
    sub = panel[panel.year.between(2011, 2025)]
    print("\nnon-missing coverage, 2011-2025:")
    print((sub[key].notna().mean() * 100).round(1).to_string())


if __name__ == "__main__":
    main()
