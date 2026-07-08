"""
Download missing 2023-2024 data for HS 2504 (graphite).
Checks for files that contain only 'skip' and retries them.
"""

import requests
import pandas as pd
import time
import os
import sys
from datetime import datetime
from pathlib import Path

KEYS = [
    "COMTRADE_API_KEY_1",
    "COMTRADE_API_KEY_2",
]
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

REPORTERS = [
    '276','97','392','344','410','826','842','56','124','156',
    '724','818','251','764','752','757','975','76','380','792',
    '100','203','376','398','528','804','191','702','428','36',
    '616','31','554','704','440','348','642','579','372',
    '32','484','620','604','508','703','84','682','705','404',
    '360','699','710','834','860','854','788',
]

HS = "2504"
DATA_DIR = Path("<repo-root>/03_data/raw")
HS_DIR = DATA_DIR / f"imports_{HS}"

PERIODS_2023 = "202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311,202312"
PERIODS_2024 = "202401,202402,202403,202404,202405,202406,202407,202408,202409,202410,202411,202412"

YEARS_NEEDED = [
    ("2023", PERIODS_2023),
    ("2024", PERIODS_2024),
]


def is_bad_file(fpath):
    if not os.path.exists(fpath):
        return True
    if os.path.getsize(fpath) <= 20:
        return True
    try:
        df = pd.read_csv(fpath, nrows=1)
        if len(df) == 0 or 'skip' in df.columns:
            return True
    except:
        return True
    return False


def fetch(period, reporter, key):
    params = {
        "reporterCode": reporter,
        "flowCode": "M",
        "cmdCode": HS,
        "period": period,
        "subscription-key": key,
    }
    try:
        r = requests.get(BASE, params=params, timeout=30)
        if r.status_code == 200:
            return r.json().get("data", [])
        if r.status_code == 403:
            return "quota"
        if r.status_code == 409:
            return None
        print(f"    HTTP {r.status_code} for {reporter}/{period}", flush=True)
    except Exception as e:
        print(f"    Error: {e}", flush=True)
    return None


def main():
    key_idx = 0
    total_new = 0

    for year, period in YEARS_NEEDED:
        year_new = 0
        for rep in REPORTERS:
            fpath = HS_DIR / f"{year}_{rep}.csv"

            if not is_bad_file(fpath):
                continue

            data = fetch(period, rep, KEYS[key_idx % 2])

            if data == "quota":
                key_idx += 1
                print(f"  Key exhausted, switching to key {key_idx % 2}", flush=True)
                data = fetch(period, rep, KEYS[key_idx % 2])

            if data == "quota":
                print(f"  Both keys quota. Waiting 5 min...", flush=True)
                time.sleep(300)
                key_idx += 1
                data = fetch(period, rep, KEYS[key_idx % 2])

            if data == "quota":
                print(f"  QUOTA EXHAUSTED. Stopping.", flush=True)
                print(f"  Progress: {year_new} new files for {year}", flush=True)
                return

            if data and len(data) > 0:
                df = pd.DataFrame(data)
                df.to_csv(fpath, index=False)
                year_new += len(data)
                print(f"  {year}_{rep}: {len(data)} rows", flush=True)
            else:
                with open(fpath, "w") as f:
                    f.write("skip")

            time.sleep(0.3)

        total_new += year_new
        print(f"  {year}: {year_new} total new rows", flush=True)

    print(f"\nTotal new rows: {total_new}", flush=True)

    merged_path = DATA_DIR / f"comtrade_{HS}_imports.csv"
    all_dfs = []
    for f in HS_DIR.glob("*.csv"):
        if not is_bad_file(f):
            try:
                df = pd.read_csv(f)
                if len(df) > 0:
                    all_dfs.append(df)
            except:
                pass

    if all_dfs:
        merged = pd.concat(all_dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        merged.to_csv(merged_path, index=False)
        print(f"Merged: {len(merged):,} rows -> {merged_path}", flush=True)


if __name__ == "__main__":
    main()
