"""
Download Eurostat CN8 trade data for gallium and germanium (separated)
=====================================================================
Dataset: DS-045409 (EU trade since 1988 by HS2-4-6 and CN8)
CN8 codes:
  81129289 = unwrought gallium; gallium powders
  81129295 = unwrought germanium; germanium powders
  81129281 = unwrought indium; indium powders (placebo within bundle)
  81129291 = unwrought vanadium; vanadium powders (placebo within bundle)

Monthly data, EU27 imports from all partners + China specifically.
Period: 2019-01 to 2024-12.

API: Eurostat Comext SDMX 2.1
https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/

Dimension structure: freq.reporter.partner.product.flow.indicators
  freq = M (monthly)
  reporter = EU27 country codes (see below)
  partner = CN (China) or WORLD
  product = CN8 code (e.g., 81129289)
  flow = 1 (imports)
  indicators = VALUE_IN_EUROS

No registration required. No strict rate limits (use 1-2 sec intervals).
"""

import requests
import pandas as pd
import time
import json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "03_data" / "raw"
EUROSTAT_DIR = DATA_DIR / "eurostat_cn8"
EUROSTAT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://commission.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409"

EU27_2020 = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "EL", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
]

CN8_CODES = {
    "81129289": "Unwrought gallium; gallium powders",
    "81129295": "Unwrought germanium; germanium powders",
    "81129281": "Unwrought indium; indium powders",
    "81129291": "Unwrought vanadium; vanadium powders",
}

PARTNERS = {
    "CN": "China",
    "WORLD": "All partners",
}

FLOW_IMPORTS = "1"
START = "2019-01"
END = "2024-12"


def build_url(reporter, partner, product, flow=FLOW_IMPORTS,
              indicator="VALUE_IN_EUROS", start=START, end=END):
    freq = "M"
    key = f"{freq}.{reporter}.{partner}.{product}.{flow}.{indicator}"
    params = {
        "startPeriod": start,
        "endPeriod": end,
        "format": "sdmx-json",
    }
    return f"{BASE_URL}/{key}", params


def fetch_sdmx_json(url, params, retries=3, delay=2):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://commission.europa.eu/eurostat",
    })
    # Warm up session with homepage visit
    try:
        session.get("https://commission.europa.eu/eurostat_en", timeout=15)
    except Exception:
        pass
    time.sleep(1)

    for attempt in range(retries):
        try:
            resp = session.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                ct = resp.headers.get("content-type", "")
                if "json" not in ct.lower() and resp.text.strip().startswith("<"):
                    print(f"    Got HTML instead of JSON (WAF block). Retrying...")
                    time.sleep(delay * 3)
                    continue
                return resp.json()
            elif resp.status_code == 429:
                wait = delay * (attempt + 3)
                print(f"    Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code == 404:
                print(f"    404 — no data for this combination")
                return None
            else:
                print(f"    HTTP {resp.status_code}: {resp.text[:200]}")
                time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"    Request error: {e}")
            time.sleep(delay)
    return None


def parse_sdmx_series(data):
    if data is None:
        return pd.DataFrame()

    try:
        structure = data.get("structure", {})
        series_list = (
            structure.get("attributes", {})
            .get("series", {})
            .get("dataStructure", {})
        )

        observations_key = None
        for k in data.get("data", {}).get("dataSets", [{}])[0].get("observations", {}):
            observations_key = k
            break

        ds = data.get("data", {}).get("dataSets", [{}])[0]
        series = ds.get("series", {})
        time_periods = structure.get("dimensions", {}).get("observation", [])
        period_dim = None
        for d in time_periods:
            if d.get("role") == "time" or d.get("id") == "TIME_PERIOD":
                period_dim = d
                break

        if not period_dim:
            for d in time_periods:
                if "values" in d and len(d["values"]) > 12:
                    period_dim = d
                    break

        if not period_dim:
            print("    Could not find time dimension in structure")
            return pd.DataFrame()

        periods = [v["id"] if "id" in v else str(v) for v in period_dim.get("values", [])]

        rows = []
        for series_key, series_data in series.items():
            obs = series_data.get("observations", {})
            for obs_idx, val in obs.items():
                if val is not None:
                    try:
                        p = periods[int(obs_idx)]
                    except (IndexError, ValueError):
                        p = f"unknown_{obs_idx}"
                    rows.append({"period": p, "value": float(val)})

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"    Parse error: {e}")
        return pd.DataFrame()


def download_all():
    log_path = EUROSTAT_DIR / "download_log.txt"
    all_results = []

    total = len(CN8_CODES) * len(EU27_2020) * len(PARTNERS)
    current = 0

    with open(log_path, "w") as log:
        log.write(f"Eurostat CN8 Download Log — {datetime.now()}\n")
        log.write(f"Total queries planned: {total}\n\n")

        for product_code, product_desc in CN8_CODES.items():
            for partner_code, partner_desc in PARTNERS.items():
                dfs = []
                for reporter in EU27_2020:
                    current += 1
                    url, params = build_url(reporter, partner_code, product_code)
                    print(f"[{current}/{total}] {reporter} <- {partner_desc} | {product_code} ({product_desc[:30]})")

                    data = fetch_sdmx_json(url, params)
                    df = parse_sdmx_series(data)

                    if len(df) > 0:
                        df["reporter"] = reporter
                        df["partner"] = partner_code
                        df["product"] = product_code
                        df["product_desc"] = product_desc
                        dfs.append(df)
                        log.write(f"  OK: {reporter} {partner_code} {product_code} -> {len(df)} obs\n")
                    else:
                        log.write(f"  EMPTY: {reporter} {partner_code} {product_code}\n")

                    time.sleep(1.5)

                if dfs:
                    combined = pd.concat(dfs, ignore_index=True)
                    fname = f"eurostat_{product_code}_{partner_code}_imports.csv"
                    combined.to_csv(EUROSTAT_DIR / fname, index=False)
                    all_results.append((product_code, partner_code, len(combined)))
                    log.write(f"  SAVED: {fname} ({len(combined)} rows)\n\n")
                else:
                    log.write(f"  NO DATA for {product_code} {partner_code}\n\n")

        log.write(f"\nDownload complete. {datetime.now()}\n")
        for code, partner, n in all_results:
            log.write(f"  {code} {partner}: {n} observations\n")

    print(f"\nDownload complete. Log at: {log_path}")
    print(f"Files saved in: {EUROSTAT_DIR}")
    for code, partner, n in all_results:
        print(f"  eurostat_{code}_{partner}_imports.csv: {n} obs")


if __name__ == "__main__":
    print("=" * 70)
    print("Eurostat CN8 Download — Ga, Ge, In, V (unwrought)")
    print("=" * 70)
    print(f"Output: {EUROSTAT_DIR}")
    print(f"Products: {list(CN8_CODES.keys())}")
    print(f"Reporters: {len(EU27_2020)} EU member states")
    print(f"Partners: {list(PARTNERS.keys())}")
    print(f"Period: {START} to {END}")
    print()
    download_all()
