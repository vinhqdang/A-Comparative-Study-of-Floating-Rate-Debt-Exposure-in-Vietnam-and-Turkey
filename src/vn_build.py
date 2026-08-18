"""
Build the Vietnamese firm-year panel from the vnfinancialdata Hugging Face
dataset (thanhnp-uel/vietnam-listed-companies-financial-statements, v1.0.0).

Output: data/processed/vn_panel.csv  (one row per ticker-year)

Variables are chosen to be constructible from the Turkish (BIST) side as well,
so that the two panels can be stacked into a harmonised cross-country panel.
"""

from __future__ import annotations

import pathlib

import pandas as pd
import vnfinancialdata as v

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

EXCHANGES = ["HSX", "HNX"]

# ---------------------------------------------------------------------------
# Item map: canonical name -> (statement, item_code)
# Financial-sector items are deliberately excluded; banks/brokers/insurers are
# dropped from the estimation sample (their liability structure is not
# comparable to that of non-financial borrowers).
# ---------------------------------------------------------------------------
ITEMS = {
    # Balance sheet
    "total_assets":        ("balance_sheet", "bs_tong_tai_san"),
    "current_assets":      ("balance_sheet", "bs_tai_san_ngan_han"),
    "cash":                ("balance_sheet", "bs_tien"),
    "total_liabilities":   ("balance_sheet", "bs_no_phai_tra"),
    "current_liabilities": ("balance_sheet", "bs_no_ngan_han"),
    "lt_liabilities":      ("balance_sheet", "bs_no_dai_han"),
    "equity":              ("balance_sheet", "bs_von_chu_so_huu_4d280b22"),
    "st_debt":             ("balance_sheet", "bs_vay_ngan_han"),
    "lt_debt":             ("balance_sheet", "bs_vay_dai_han"),
    "retained_earnings":   ("balance_sheet", "bs_lai_chua_phan_phoi"),
    # Income statement
    "revenue":             ("income_statement", "is_doanh_so_thuan"),
    "ebit":                ("income_statement", "is_ebit"),
    "ebitda":              ("income_statement", "is_ebitda"),
    "pretax_income":       ("income_statement", "is_lai_lo_rong_truoc_thue"),
    "net_income":          ("income_statement", "is_lai_lo_thuan_sau_thue"),
    "interest_expense":    ("income_statement", "is_trong_do_chi_phi_lai_vay"),
    # Cash flow
    "depreciation":        ("cash_flow", "cf_khau_hao_tscd"),
}


def _long_to_wide() -> pd.DataFrame:
    """Pull every needed item code and pivot to one row per ticker-year."""
    wanted: dict[str, list[str]] = {}
    for _, (stmt, code) in ITEMS.items():
        wanted.setdefault(stmt, []).append(code)

    pieces = []
    for stmt, codes in wanted.items():
        for ex in EXCHANGES:
            df = v.load(exchange=ex, statement=stmt, item_code=codes)
            pieces.append(df[["ticker", "year", "exchange", "item_code", "value"]])

    long = pd.concat(pieces, ignore_index=True)

    # A handful of (ticker, year, item_code) triples repeat across source
    # sheets; keep the last non-null observation.
    long = long.dropna(subset=["value"])
    long = long.drop_duplicates(subset=["ticker", "year", "item_code"], keep="last")

    wide = long.pivot_table(
        index=["ticker", "year", "exchange"],
        columns="item_code",
        values="value",
        aggfunc="last",
    ).reset_index()

    rename = {code: name for name, (_, code) in ITEMS.items()}
    wide = wide.rename(columns=rename)

    for name in ITEMS:
        if name not in wide.columns:
            wide[name] = pd.NA

    wide.columns.name = None
    return wide


def _derive(df: pd.DataFrame) -> pd.DataFrame:
    """Construct the exposure, leverage and distress variables."""
    df = df.sort_values(["ticker", "year"]).copy()

    df["total_debt"] = df[["st_debt", "lt_debt"]].sum(axis=1, min_count=1)

    g = df.groupby("ticker", sort=False)
    df["total_debt_lag"] = g["total_debt"].shift(1)
    df["total_assets_lag"] = g["total_assets"].shift(1)

    # --- Debt structure -----------------------------------------------------
    df["debt_to_assets"] = df["total_debt"] / df["total_assets"]
    df["leverage"] = df["total_liabilities"] / df["total_assets"]
    df["st_debt_share"] = df["st_debt"] / df["total_debt"]

    # --- Implied cost of debt: the repricing signal -------------------------
    # Average of beginning- and end-of-year debt in the denominator, so the
    # ratio is not mechanically driven by within-year borrowing.
    avg_debt = df[["total_debt", "total_debt_lag"]].mean(axis=1)
    df["implied_rate"] = df["interest_expense"].abs() / avg_debt

    # --- Distress / servicing capacity --------------------------------------
    df["icr"] = df["ebit"] / df["interest_expense"].abs()
    df["roa"] = df["ebit"] / df["total_assets"]
    df["cash_ratio"] = df["cash"] / df["current_liabilities"]
    df["current_ratio"] = df["current_assets"] / df["current_liabilities"]

    # Altman Z''-score for emerging markets (Altman, 2005):
    #   Z'' = 3.25 + 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
    x1 = (df["current_assets"] - df["current_liabilities"]) / df["total_assets"]
    x2 = df["retained_earnings"] / df["total_assets"]
    x3 = df["ebit"] / df["total_assets"]
    x4 = df["equity"] / df["total_liabilities"]
    df["altman_z"] = 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4

    return df


def main() -> None:
    wide = _long_to_wide()
    panel = _derive(wide)
    panel["country"] = "VN"

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "vn_panel.csv"
    panel.to_csv(path, index=False)

    print(f"wrote {path}  rows={len(panel):,}  firms={panel.ticker.nunique()}")
    print(f"years {int(panel.year.min())}-{int(panel.year.max())}")
    cov = panel[panel.year.between(2011, 2025)]
    key = ["total_assets", "total_debt", "interest_expense", "ebit", "equity"]
    print("\nnon-missing coverage, 2011-2025:")
    print((cov[key].notna().mean() * 100).round(1).to_string())


if __name__ == "__main__":
    main()
