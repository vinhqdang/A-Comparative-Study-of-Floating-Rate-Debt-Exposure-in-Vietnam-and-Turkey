"""
Fetch annual financial statements for every BIST-listed company.

Source
------
İş Yatırım's public `MaliTablo` endpoint, which returns the balance sheet,
income statement, cash-flow statement and a block of supplementary items
(export sales, net FX position, financial expenses, D&A) in a single call,
with bilingual TR/EN item labels.

Two practical notes drive the design:

1. One request accepts four independent (year, period) pairs.  Asking for
   period 12 of four consecutive years therefore returns four *annual*
   observations per call, cutting the request count by a factor of four.

2. isyatirim.com.tr refuses connections from most non-Turkish egress IPs
   (TCP timeout, not an HTTP error).  Requests are therefore routed through
   r.jina.ai, which reaches the host.  Set FETCH_DIRECT=1 when running from
   an IP that can reach the origin, which is faster and has no third party
   in the path.

Responses are cached one file per (ticker, year-block), so the job is
resumable and re-running it costs nothing for work already done.
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import pathlib
import re
import sys
import time

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "tr"

ORIGIN = (
    "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/"
    "Data.aspx/MaliTablo"
)

# 2010-2025 in blocks of four; the panel is trimmed to 2011+ downstream to
# match the Vietnamese sample.
YEAR_BLOCKS = [(2010, 2013), (2014, 2017), (2018, 2021), (2022, 2025)]

DIRECT = os.environ.get("FETCH_DIRECT") == "1"
WORKERS = int(os.environ.get("FETCH_WORKERS", "6"))
RETRIES = 3


def _url(ticker: str, y0: int) -> str:
    years = "".join(
        f"&year{i}={y0 + i - 1}&period{i}=12" for i in (1, 2, 3, 4)
    )
    return f"{ORIGIN}?companyCode={ticker}&exchange=TRY&financialGroup=XI_29{years}"


def _fetch_one(ticker: str, y0: int) -> str | None:
    """Return the raw JSON payload for one ticker / year-block, or None."""
    out = RAW / f"{ticker}_{y0}.json"
    if out.exists():
        return "cached"

    origin = _url(ticker, y0)
    url = origin if DIRECT else "https://r.jina.ai/" + origin

    for attempt in range(RETRIES):
        try:
            r = requests.get(url, timeout=90)
            if r.status_code == 200 and '"ok":true' in r.text:
                # The proxy wraps the payload in markdown; recover the JSON.
                m = re.search(r'\{"ok":.*\}', r.text, re.S)
                if m:
                    payload = json.loads(m.group(0))
                    out.write_text(
                        json.dumps(payload, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    return "ok"
        except Exception:
            pass
        time.sleep(2 * (attempt + 1))

    return None


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)

    import borsapy as bp

    tickers = sorted(bp.companies()["ticker"].dropna().unique().tolist())
    jobs = [(t, y0) for t in tickers for y0, _ in YEAR_BLOCKS]
    todo = [j for j in jobs if not (RAW / f"{j[0]}_{j[1]}.json").exists()]

    print(f"{len(tickers)} tickers | {len(jobs)} jobs | {len(todo)} outstanding",
          flush=True)

    done = fail = 0
    t0 = time.time()

    with cf.ThreadPoolExecutor(WORKERS) as ex:
        futs = {ex.submit(_fetch_one, t, y): (t, y) for t, y in todo}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            if fut.result():
                done += 1
            else:
                fail += 1
            if i % 100 == 0:
                el = time.time() - t0
                rate = i / el
                eta = (len(todo) - i) / rate / 60 if rate else 0
                print(f"  {i}/{len(todo)}  ok={done} fail={fail} "
                      f"{rate:.1f}/s  eta {eta:.0f}m", flush=True)

    print(f"finished: ok={done} fail={fail} "
          f"files={len(list(RAW.glob('*.json')))} "
          f"elapsed={(time.time() - t0) / 60:.1f}m", flush=True)


if __name__ == "__main__":
    sys.exit(main())
