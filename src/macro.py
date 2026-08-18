"""
Assemble annual macro-financial series for Vietnam and Türkiye.

Sources, in order of preference:
  * BIS WS_CBPOL - central bank policy rates, monthly end-of-period.
    Authoritative and machine-readable, but covers 38 economies and
    Vietnam is NOT among them.
  * World Bank FR.INR.LEND - average bank lending rate. Available for
    Vietnam 2010-2023; the Türkiye series is empty.

The two countries therefore cannot be put on an identical rate definition
from a single source. That matters less than it looks: the estimating
equation carries country-by-year fixed effects, which absorb any
country-level rate series entirely. These series are used for descriptive
validation of the implied-rate measure and for the pass-through window,
not as a regressor.
"""

from __future__ import annotations

import io
import pathlib

import pandas as pd
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

BIS = ("https://stats.bis.org/api/v1/data/WS_CBPOL/M.{iso}/all"
       "?format=csv&startPeriod=2010")
WB = ("https://api.worldbank.org/v2/country/{iso}/indicator/FR.INR.LEND"
      "?format=json&per_page=300&date=2010:2025")


def bis_policy(iso: str) -> pd.DataFrame:
    """Annual (December) policy rate from BIS."""
    r = requests.get(BIS.format(iso=iso), timeout=60)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.text))
    d = d[["TIME_PERIOD", "OBS_VALUE"]].dropna()
    d["year"] = d["TIME_PERIOD"].str[:4].astype(int)
    d["month"] = d["TIME_PERIOD"].str[5:7].astype(int)

    dec = (d[d.month == 12].set_index("year")["OBS_VALUE"]
           .rename("policy_rate_eop"))
    avg = d.groupby("year")["OBS_VALUE"].mean().rename("policy_rate_avg")
    return pd.concat([dec, avg], axis=1).reset_index()


def wb_lending(iso: str) -> pd.DataFrame:
    r = requests.get(WB.format(iso=iso), timeout=60)
    r.raise_for_status()
    payload = r.json()
    if len(payload) < 2 or payload[1] is None:
        return pd.DataFrame(columns=["year", "lending_rate"])
    rows = [(int(x["date"]), x["value"]) for x in payload[1]
            if x["value"] is not None]
    return pd.DataFrame(rows, columns=["year", "lending_rate"]).sort_values("year")


def main() -> None:
    frames = []

    tr = bis_policy("TR").assign(country="TR")
    tr = tr.merge(wb_lending("tur"), on="year", how="left")
    frames.append(tr)

    # Vietnam is absent from BIS; the lending rate is the only machine-readable
    # annual series, and it ends in 2023.
    vn = wb_lending("vnm").assign(country="VN")
    vn["policy_rate_eop"] = pd.NA
    vn["policy_rate_avg"] = pd.NA
    frames.append(vn)

    macro = pd.concat(frames, ignore_index=True)
    macro = macro[["country", "year", "policy_rate_eop", "policy_rate_avg",
                   "lending_rate"]].sort_values(["country", "year"])

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "macro_rates.csv"
    macro.to_csv(path, index=False)
    print(f"wrote {path}")
    print(macro.to_string(index=False))


if __name__ == "__main__":
    main()
