"""
Download missing data files for the critical minerals analysis.
Only downloads files that are missing or marked as 'skip' in imports_ subdirectories.

Priority:
  1. 2818 (Alumina) — missing 2019-2020 (all reporters)
  2. 8111 (Manganese) — 8 missing files (2019: 4, 2020: 4)
  3. 811292 (Ga/Ge) — 20 missing files (2019: 10, 2020: 10)
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime
from pathlib import Path

from comtrade_auth import load_comtrade_keys

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "03_data" / "raw"
KEYS: list[str] = []
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"
YEAR_STR = {str(y): ",".join(f"{y}{m:02d}" for m in range(1, 13)) for y in range(2019, 2025)}

REPORTERS = [
    '276', '97', '392', '344', '410', '826', '842', '56', '124', '156',
    '724', '818', '251', '764', '752', '757', '975', '76', '380', '792',
    '100', '203', '376', '398', '528', '804', '191', '702', '428', '36',
    '616', '31', '554', '704', '440', '348', '642', '579', '372',
    '32', '484', '620', '604', '508', '703', '84', '682', '705', '404',
    '360', '699', '710', '834', '860', '854', '788',
]

TASKS = [
    {"hs": "2818", "label": "Alumina", "years": ["2019", "2020"]},
    {"hs": "8111", "label": "Manganese", "years": ["2019", "2020"]},
    {"hs": "811292", "label": "Ga/Ge bundle", "years": ["2019", "2020"]},
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


def ensure_keys() -> list[str]:
    global KEYS
    if not KEYS:
        KEYS = load_comtrade_keys()
    return KEYS


def is_bad(fp):
    if not fp.exists():
        return True
    if os.path.getsize(fp) <= 20:
        return True
    try:
        df = pd.read_csv(fp, nrows=1)
        return len(df) == 0 or "skip" in df.columns
    except Exception:
        return True


def fetch(hs, period, reporter, key):
    try:
        r = requests.get(
            BASE,
            params={
                "reporterCode": reporter,
                "flowCode": "M",
                "cmdCode": hs,
                "period": period,
                "subscription-key": key,
            },
            timeout=60,
        )
        if r.status_code == 200:
            return "ok", r.json().get("data", [])
        if r.status_code in (403, 409):
            return "quota", None
        if r.status_code == 429:
            return "rate_limit", None
        return "error", f"status={r.status_code}"
    except requests.Timeout:
        return "timeout", None
    except Exception as e:
        return "error", str(e)


def merge_hs(hs):
    hs_dir = DATA / f"imports_{hs}"
    merged_path = DATA / f"comtrade_{hs}_imports.csv"
    dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
        if not is_bad(f):
            try:
                d = pd.read_csv(f)
                if len(d) > 0:
                    dfs.append(d)
            except Exception:
                pass
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        merged.to_csv(merged_path, index=False)
        log(f"  MERGED {hs}: {len(merged):,} rows -> {merged_path.name}")
    else:
        log(f"  {hs}: NO DATA to merge")


def main():
    log("=" * 60)
    log("DOWNLOAD MISSING DATA")
    log("=" * 60)

    ki = 0
    total_calls = 0

    for task in TASKS:
        hs = task["hs"]
        label = task["label"]
        years = task["years"]
        hs_dir = DATA / f"imports_{hs}"
        hs_dir.mkdir(exist_ok=True)

        log(f"\n--- HS {hs} ({label}) ---")
        total_new = 0

        for year in years:
            period = YEAR_STR[year]
            year_new = 0
            year_skip = 0

            for rep in REPORTERS:
                fp = hs_dir / f"{year}_{rep}.csv"
                if not is_bad(fp):
                    year_skip += 1
                    continue

                for attempt in range(3):
                    keys = ensure_keys()
                    key = keys[ki % len(keys)]
                    status, data = fetch(hs, period, rep, key)
                    total_calls += 1

                    if status == "ok":
                        if data:
                            pd.DataFrame(data).to_csv(fp, index=False)
                            year_new += len(data)
                        else:
                            fp.write_text("skip")
                        break
                    elif status == "quota":
                        log(f"  QUOTA key {ki % len(keys)}, sleeping 2h...")
                        time.sleep(7200)
                        ki += 1
                        continue
                    elif status == "rate_limit":
                        log(f"  Rate limited, sleeping 60s...")
                        time.sleep(60)
                        ki += 1
                        continue
                    elif status == "timeout":
                        log(f"  Timeout {hs} {year}_{rep}, attempt {attempt + 1}/3")
                        time.sleep(10)
                        continue
                    else:
                        log(f"  Error {hs} {year}_{rep}: {data}")
                        fp.write_text("skip")
                        break

                time.sleep(0.3)

            total_new += year_new
            log(f"  {hs} {year}: {year_new} new, {year_skip} existing ({total_calls} calls)")

        merge_hs(hs)
        log(f"  HS {hs} done: {total_new} new rows ({total_calls} calls)")

    log(f"\n{'=' * 60}")
    log(f"ALL DONE. Total API calls: {total_calls}")
    log(f"{'=' * 60}")


if __name__ == "__main__":
    main()
