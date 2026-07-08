"""
Mass downloader for all missing HS codes.
Handles: partial downloads (skips existing good files), bad files (replaces 'skip'),
and quota management across 2 API keys.

Priority order:
1. HS 2504 graphite (2023-2024 only — pre-treatment already downloaded)
2. HS 811292 Ga/Ge (2022-2024 — 2019-2021 exists)
3. HS 3801 artificial graphite (all years)
4. HS 8110 antimony metal (all years)
5. HS 2617 antimony ores (all years)
6. 9 placebo HS codes (all years)
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

ALL_HS = {
    "2504": {"label": "Natural graphite", "years": ["2023", "2024"]},
    "811292": {"label": "Ga/Ge metals", "years": ["2022", "2023", "2024"]},
    "3801": {"label": "Artificial graphite", "years": ["2019","2020","2021","2022","2023","2024"]},
    "8110": {"label": "Antimony metal", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2617": {"label": "Antimony ores", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2501": {"label": "Salt (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2523": {"label": "Cement (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2804": {"label": "H/noble gases (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2818": {"label": "Alumina (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "2827": {"label": "Chlorides (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "3815": {"label": "Catalysts (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "3824": {"label": "Chem prep (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "8111": {"label": "Manganese (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
    "8112": {"label": "Other metals (placebo)", "years": ["2019","2020","2021","2022","2023","2024"]},
}

YEAR_PERIODS = {
    "2019": "201901,201902,201903,201904,201905,201906,201907,201908,201909,201910,201911,201912",
    "2020": "202001,202002,202003,202004,202005,202006,202007,202008,202009,202010,202011,202012",
    "2021": "202101,202102,202103,202104,202105,202106,202107,202108,202109,202110,202111,202112",
    "2022": "202201,202202,202203,202204,202205,202206,202207,202208,202209,202210,202211,202212",
    "2023": "202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311,202312",
    "2024": "202401,202402,202403,202404,202405,202406,202407,202408,202409,202410,202411,202412",
}

DATA_DIR = Path("<repo-root>/03_data/raw")
LOG_FILE = DATA_DIR / "mass_dl.log"


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


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


def fetch(hs, period, reporter, key):
    params = {
        "reporterCode": reporter,
        "flowCode": "M",
        "cmdCode": hs,
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
            return "rate_limit"
    except Exception as e:
        if "timed out" in str(e):
            return "timeout"
        return "error"
    return None


def download_hs(hs, years_needed):
    label = ALL_HS[hs]["label"]
    hs_dir = DATA_DIR / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)

    key_idx = 0
    total_new = 0
    calls = 0

    for year in years_needed:
        period = YEAR_PERIODS[year]
        year_new = 0
        year_skip = 0

        for rep in REPORTERS:
            fpath = hs_dir / f"{year}_{rep}.csv"

            if not is_bad_file(fpath):
                year_skip += 1
                continue

            data = fetch(hs, period, rep, KEYS[key_idx % 2])
            calls += 1

            if data in ("quota", "rate_limit"):
                key_idx += 1
                data = fetch(hs, period, rep, KEYS[key_idx % 2])
                calls += 1

            if data in ("quota", "rate_limit"):
                log(f"  {hs} {year}_{rep}: quota on both keys, sleeping 3 min...")
                time.sleep(180)
                key_idx += 1
                data = fetch(hs, period, rep, KEYS[key_idx % 2])
                calls += 1

            if data in ("quota", "rate_limit"):
                log(f"  {hs} {year}: QUOTA EXHAUSTED after 3 tries. Stopping this HS.")
                return total_new, calls, False

            if data == "timeout":
                log(f"  {hs} {year}_{rep}: timeout, skipping")
                with open(fpath, "w") as f:
                    f.write("skip")
                time.sleep(1)
                continue

            if data == "error":
                log(f"  {hs} {year}_{rep}: connection error, skipping")
                with open(fpath, "w") as f:
                    f.write("skip")
                time.sleep(2)
                continue

            if data and len(data) > 0:
                df = pd.DataFrame(data)
                df.to_csv(fpath, index=False)
                year_new += len(data)
            else:
                with open(fpath, "w") as f:
                    f.write("skip")

            time.sleep(0.25)

        total_new += year_new
        log(f"  {hs} ({label}) {year}: {year_new} new rows, {year_skip} existing. Calls so far: {calls}")

    return total_new, calls, True


def merge_hs(hs):
    hs_dir = DATA_DIR / f"imports_{hs}"
    merged_path = DATA_DIR / f"comtrade_{hs}_imports.csv"

    all_dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
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
        log(f"  MERGED {hs}: {len(merged):,} rows -> {merged_path.name}")
        return len(merged)
    else:
        log(f"  MERGE {hs}: NO DATA")
        return 0


def main():
    log("=" * 60)
    log("MASS DOWNLOAD START")
    log(f"HS codes: {len(ALL_HS)}")
    total_calls = 0

    for hs in ALL_HS:
        years_needed = ALL_HS[hs]["years"]
        label = ALL_HS[hs]["label"]
        log(f"\n--- HS {hs} ({label}) ---")
        log(f"  Years needed: {years_needed}")

        new_rows, calls, ok = download_hs(hs, years_needed)
        total_calls += calls

        if ok:
            n = merge_hs(hs)
            log(f"  HS {hs} COMPLETE: {new_rows} new rows, {n:,} total merged")
        else:
            log(f"  HS {hs} INCOMPLETE: quota exhausted after {calls} calls")
            merge_hs(hs)

        log(f"  Total API calls so far: {total_calls}")

    log(f"\n{'=' * 60}")
    log(f"ALL DONE. Total API calls: {total_calls}")
    log(f"{'=' * 60}")


if __name__ == "__main__":
    main()
