"""
UN Comtrade v8 — Bullet-proof sequential downloader.
- 1 reporter at a time, saves per-reporter CSVs
- Auto-retry with exponential backoff
- Full resume capability (skips already-downloaded reporters)
- Uses requests.Session with retry adapter
- Alternates keys to spread quota usage
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import time
import os
import sys
from datetime import datetime

KEYS = [
    "COMTRADE_API_KEY_1",
    "COMTRADE_API_KEY_2",
]
BASE_URL = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

TOP_REPORTERS = [
    '276','97','392','344','410','826','842','56','124','156',
    '724','818','251','764','752','757','975','76','380','792',
    '100','203','376','398','528','804','191','702','428','36',
    '616','31','554','704','440','348','642','579','372',
    '32','484','620','604','508','703','84','682','705','404',
    '360','699','710','834','860','854','788',
]

REPORTERS = TOP_REPORTERS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "data")

HS_TREATED = {
    "811292": "Ga+Ge+In+V+Nb unwrought",
    "282560": "GeO2+ZrO2",
    "2504":   "Natural graphite",
    "3801":   "Artificial graphite",
    "8110":   "Antimony metal",
    "2617":   "Antimony ores",
}

HS_PLACEBO = {
    "2501": "Salt",
    "2523": "Portland cement",
    "2804": "Hydrogen, noble gases",
    "2818": "Aluminum oxide",
    "2827": "Chlorides",
    "3815": "Catalysts",
    "3824": "Chemical preparations",
    "8111": "Manganese unwrought",
    "8112": "Other unwrought metals",
}

ALL_HS = {**HS_TREATED, **HS_PLACEBO}

PERIOD_BATCHES = [
    ("2019", "201901,201902,201903,201904,201905,201906,201907,201908,201909,201910,201911,201912"),
    ("2020", "202001,202002,202003,202004,202005,202006,202007,202008,202009,202010,202011,202012"),
    ("2021", "202101,202102,202103,202104,202105,202106,202107,202108,202109,202110,202111,202112"),
    ("2022", "202201,202202,202203,202204,202205,202206,202207,202208,202209,202210,202211,202212"),
    ("2023", "202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311,202312"),
    ("2024", "202401,202402,202403,202404,202405,202406,202407,202408,202409,202410,202411,202412"),
]


def make_session():
    s = requests.Session()
    retry = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503])
    adapter = HTTPAdapter(max_retries=retry, pool_maxsize=1)
    s.mount("https://", adapter)
    return s


def download_imports(cmd_code, description):
    final_file = os.path.join(OUTPUT_DIR, f"comtrade_{cmd_code}_imports.csv")
    if os.path.exists(final_file):
        df = pd.read_csv(final_file)
        print(f"  Final file exists ({len(df)} rows), skipping")
        return

    hs_dir = os.path.join(OUTPUT_DIR, f"imports_{cmd_code}")
    os.makedirs(hs_dir, exist_ok=True)

    session = make_session()
    total_rows = 0
    key_idx = 0

    for year, period_batch in PERIOD_BATCHES:
        year_rows = 0
        for rep in REPORTERS:
            rep_file = os.path.join(hs_dir, f"{year}_{rep}.csv")
            if os.path.exists(rep_file):
                if os.path.getsize(rep_file) > 10:
                    try:
                        df_rep = pd.read_csv(rep_file)
                        year_rows += len(df_rep)
                    except:
                        pass
                continue

            params = {
                "reporterCode": rep,
                "flowCode": "M",
                "cmdCode": cmd_code,
                "period": period_batch,
                "subscription-key": KEYS[key_idx % len(KEYS)],
            }
            key_idx += 1

            success = False
            for attempt in range(2):
                try:
                    r = session.get(BASE_URL, params=params, timeout=25)
                    if r.status_code == 403:
                        key_idx += 1
                        params["subscription-key"] = KEYS[key_idx % len(KEYS)]
                        continue
                    if r.status_code == 200:
                        d = r.json()
                        if d.get("data"):
                            df_rep = pd.DataFrame(d["data"])
                            df_rep.to_csv(rep_file, index=False)
                            year_rows += len(df_rep)
                        success = True
                    break
                except:
                    if attempt == 0:
                        key_idx += 1
                        params["subscription-key"] = KEYS[key_idx % len(KEYS)]
                    time.sleep(1)
            if not success and not os.path.exists(rep_file):
                open(rep_file, "w").write("skip")

            time.sleep(0.3)

        total_rows += year_rows
        print(f"  {year}: {year_rows} rows")

    # Merge all per-reporter files
    all_dfs = []
    for year, _ in PERIOD_BATCHES:
        for rep in REPORTERS:
            rep_file = os.path.join(hs_dir, f"{year}_{rep}.csv")
            if os.path.exists(rep_file) and os.path.getsize(rep_file) > 10:
                all_dfs.append(pd.read_csv(rep_file))

    if all_dfs:
        df = pd.concat(all_dfs, ignore_index=True)
        df["hs_description"] = description
        df["download_date"] = datetime.now().strftime("%Y-%m-%d")
        df.to_csv(final_file, index=False)
        print(f"  MERGED: {len(df)} total rows → {final_file}")


def download_china_exports(cmd_code, description):
    final_file = os.path.join(OUTPUT_DIR, f"comtrade_{cmd_code}_china_exports.csv")
    if os.path.exists(final_file):
        print(f"  Already exists")
        return

    session = make_session()
    all_data = []
    for year, period_batch in PERIOD_BATCHES:
        params = {
            "reporterCode": "156",
            "flowCode": "X",
            "cmdCode": cmd_code,
            "period": period_batch,
            "partnerCode": "0",
            "subscription-key": KEYS[0],
        }
        for attempt in range(3):
            try:
                r = session.get(BASE_URL, params=params, timeout=60)
                d = r.json()
                if d.get("data"):
                    all_data.extend(d["data"])
                    total = sum(r2["primaryValue"] for r2 in d["data"])
                    print(f"  {year}: ${total:,.0f}")
                else:
                    print(f"  {year}: no data")
                break
            except:
                time.sleep(3)
        time.sleep(0.5)

    if all_data:
        df = pd.DataFrame(all_data)
        df["hs_description"] = description
        df["download_date"] = datetime.now().strftime("%Y-%m-%d")
        df.to_csv(final_file, index=False)
        print(f"  Saved {len(df)} records")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["imports", "china_exports", "all"], default="all")
    parser.add_argument("--hs", type=str, default=None)
    parser.add_argument("--scope", choices=["treated", "placebo", "all"], default="all")
    args = parser.parse_args()

    if args.hs:
        hs_set = {args.hs: ALL_HS[args.hs]}
    elif args.scope == "treated":
        hs_set = HS_TREATED
    elif args.scope == "placebo":
        hs_set = HS_PLACEBO
    else:
        hs_set = ALL_HS

    start = datetime.now()

    if args.mode in ("china_exports", "all"):
        print(f"\nCHINA EXPORTS | {len(hs_set)} HS")
        for hs, desc in hs_set.items():
            print(f"\n--- HS {hs}: {desc} ---")
            download_china_exports(hs, desc)

    if args.mode in ("imports", "all"):
        print(f"\nIMPORTS | {len(hs_set)} HS")
        for hs, desc in hs_set.items():
            print(f"\n--- HS {hs}: {desc} ---")
            download_imports(hs, desc)

    elapsed = (datetime.now() - start).total_seconds() / 60
    print(f"\nDONE in {elapsed:.1f} min")
