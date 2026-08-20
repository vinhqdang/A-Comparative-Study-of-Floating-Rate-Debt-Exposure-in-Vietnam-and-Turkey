"""
Build harmonised firm-year panels for a cross-country sample spanning the full
range of 2021-2024 monetary tightening doses, from Türkiye's 33.5 percentage
points down to Thailand's 2.0.

Design mirrors src/tr_yf.py: statements from Yahoo Finance, ticker universe
enumerated via TradingView's screener (which is not geo-blocked, unlike
Is Yatirim), non-financial firms only. Vietnam and Turkey retain their
existing, independently validated panels (vnfinancialdata / Is Yatirim); this
module supplies the additional six.
"""
from __future__ import annotations
import concurrent.futures as cf, pathlib, sys, time, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT/"data"/"processed"
RAW = ROOT/"data"/"raw"/"multi"; RAW.mkdir(parents=True, exist_ok=True)

# (TradingView market, Yahoo suffix, BIS/ISO code, tightening dose in pp 2021-peak)
COUNTRIES = [
    ("hungary",       ".BD", "HU", 10.60),
    ("chile",         ".SN", "CL",  7.25),
    ("brazil",        ".SA", "BR",  5.75),
    ("mexico",        ".MX", "MX",  5.75),
    ("poland",        ".WA", "PL",  5.00),
    ("israel",        ".TA", "IL",  4.65),
    ("korea",         ".KS", "KR",  2.50),
    ("thailand",      ".BK", "TH",  2.00),
]

BS_MAP = {"Total Assets":"total_assets","Current Assets":"current_assets",
          "Cash And Cash Equivalents":"cash","Current Liabilities":"current_liabilities",
          "Stockholders Equity":"equity","Current Debt":"st_debt",
          "Long Term Debt":"lt_debt","Total Debt":"total_debt_reported",
          "Retained Earnings":"retained_earnings"}
IS_MAP = {"Total Revenue":"revenue","EBIT":"ebit","EBITDA":"ebitda",
          "Interest Expense":"interest_expense","Pretax Income":"pretax_income",
          "Net Income":"net_income"}


def _universe(market: str, cap: int = 800) -> list[str]:
    from tradingview_screener import Query, col
    n, df = (Query().set_markets(market)
             .select("name","sector","market_cap_basic")
             .limit(cap).get_scanner_data())
    df = df[~df["sector"].isin(["Finance"])] if "sector" in df else df
    df = df.sort_values("market_cap_basic", ascending=False)
    return df["name"].dropna().tolist()


def _one(ticker: str, suffix: str):
    import yfinance as yf
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
            for col_, val in bs.loc[label].items():
                rows.setdefault(col_.year, {})[name] = val
    if fin is not None and not fin.empty:
        for label, name in IS_MAP.items():
            if label in fin.index:
                for col_, val in fin.loc[label].items():
                    rows.setdefault(col_.year, {})[name] = val
    out = []
    for year, vals in rows.items():
        vals.update(ticker=ticker, year=year)
        out.append(vals)
    return out


def derive(df: pd.DataFrame, iso: str) -> pd.DataFrame:
    df = df.sort_values(["ticker","year"]).copy()
    df["total_debt"] = df[["st_debt","lt_debt"]].sum(axis=1, min_count=1)
    df["total_debt"] = df["total_debt"].fillna(df.get("total_debt_reported"))
    df["total_liabilities"] = df["total_assets"] - df["equity"]
    g = df.groupby("ticker", sort=False)
    df["total_debt_lag"] = g["total_debt"].shift(1)
    df["debt_to_assets"] = df["total_debt"]/df["total_assets"]
    df["st_debt_share"] = df["st_debt"]/df["total_debt"]
    avg_debt = df[["total_debt","total_debt_lag"]].mean(axis=1)
    df["implied_rate"] = df["interest_expense"].abs()/avg_debt
    df["icr"] = df["ebit"]/df["interest_expense"].abs()
    df["roa"] = df["ebit"]/df["total_assets"]
    df["ebit_margin"] = df["ebit"]/df["revenue"]
    df["debt_growth"] = np.log(df["total_debt"].where(df["total_debt"]>0)).groupby(df["ticker"]).diff() \
        if False else g["total_debt"].transform(lambda s: np.log(s.where(s>0)).diff())
    x1=(df.current_assets-df.current_liabilities)/df.total_assets
    x2=df.retained_earnings/df.total_assets; x3=df.ebit/df.total_assets
    x4=df.equity/df.total_liabilities
    df["altman_z"]=3.25+6.56*x1+3.26*x2+6.72*x3+1.05*x4
    df["country"]=iso; df["source"]="yahoo"
    return df


def fetch_country(market, suffix, iso, workers=8):
    cache = RAW/f"{iso}.csv"
    if cache.exists():
        print(f"[{iso}] cached", flush=True)
        return pd.read_csv(cache)
    tickers = _universe(market)
    print(f"[{iso}] {len(tickers)} tickers from {market}", flush=True)
    records = []
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(_one, t, suffix) for t in tickers]
        for i, f in enumerate(cf.as_completed(futs), 1):
            records.extend(f.result())
            if i % 200 == 0:
                print(f"  [{iso}] {i}/{len(tickers)}", flush=True)
    raw = pd.DataFrame(records)
    raw.to_csv(cache, index=False)
    return raw


def main():
    frames = []
    for market, suffix, iso, dose in COUNTRIES:
        raw = fetch_country(market, suffix, iso)
        if raw.empty:
            print(f"[{iso}] EMPTY"); continue
        panel = derive(raw, iso)
        panel["dose_pp"] = dose
        frames.append(panel)
        print(f"[{iso}] -> {len(panel):,} firm-years, {panel.ticker.nunique()} firms", flush=True)

    full = pd.concat(frames, ignore_index=True)
    path = OUT/"multi_panel.csv"
    full.to_csv(path, index=False)
    print(f"\nwrote {path}  total rows={len(full):,}")
    print(full.groupby("country").ticker.nunique().to_string())


if __name__ == "__main__":
    main()
