"""
Comtrade downloader v9 — Dead simple. No Session, no retry adapter.
Sequential per-reporter. Skips failures. Saves per-reporter.
"""

import requests
import pandas as pd
import time
import os
import sys
from datetime import datetime

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

HS_CODES = {
    "811292": "Ga+Ge+In+V+Nb",
    "282560": "GeO2+ZrO2",
    "2504":   "Natural graphite",
    "3801":   "Artificial graphite",
    "8110":   "Antimony metal",
    "2617":   "Antimony ores",
    "2501": "Salt",
    "2523": "Portland cement",
    "2804": "Hydrogen/noble gases",
    "2818": "Aluminum oxide",
    "2827": "Chlorides",
    "3815": "Catalysts",
    "3824": "Chemical preparations",
    "8111": "Manganese",
    "8112": "Other metals",
}

YEARS = [
    ("2019", "201901,201902,201903,201904,201905,201906,201907,201908,201909,201910,201911,201912"),
    ("2020", "202001,202002,202003,202004,202005,202006,202007,202008,202009,202010,202011,202012"),
    ("2021", "202101,202102,202103,202104,202105,202106,202107,202108,202109,202110,202111,202112"),
    ("2022", "202201,202202,202203,202204,202205,202206,202207,202208,202209,202210,202211,202212"),
    ("2023", "202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311,202312"),
    ("2024", "202401,202402,202403,202404,202405,202406,202407,202408,202409,202410,202411,202412"),
]

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def fetch(hs, year, period, reporter, key):
    params = {
        "reporterCode": reporter,
        "flowCode": "M",
        "cmdCode": hs,
        "period": period,
        "subscription-key": key,
    }
    try:
        r = requests.get(BASE, params=params, timeout=20)
        if r.status_code == 200:
            d = r.json()
            return d.get("data", [])
        if r.status_code == 403:
            return "quota"
    except:
        pass
    return None


def download_hs(hs):
    final = os.path.join(DATA_DIR, f"comtrade_{hs}_imports.csv")
    if os.path.exists(final):
        print(f"HS {hs}: already merged", flush=True)
        return True

    hs_dir = os.path.join(DATA_DIR, f"imports_{hs}")
    os.makedirs(hs_dir, exist_ok=True)

    key_idx = 0
    total = 0

    for year, period in YEARS:
        year_total = 0
        for rep in REPORTERS:
            fpath = os.path.join(hs_dir, f"{year}_{rep}.csv")
            if os.path.exists(fpath) and os.path.getsize(fpath) > 20:
                try:
                    df = pd.read_csv(fpath)
                    year_total += len(df)
                except:
                    pass
                continue

            data = fetch(hs, year, period, rep, KEYS[key_idx % 2])

            if data == "quota":
                key_idx += 1
                data = fetch(hs, year, period, rep, KEYS[key_idx % 2])

            if data == "quota":
                print(f"  {year}: quota exceeded, sleeping 5 min...", flush=True)
                time.sleep(300)
                data = fetch(hs, year, period, rep, KEYS[key_idx % 2])

            if data == "quota":
                print(f"  {year}: still quota, sleeping 10 min...", flush=True)
                time.sleep(600)
                data = fetch(hs, year, period, rep, KEYS[key_idx % 2])

            if data == "quota":
                print(f"  {year}: QUOTA EXCEEDED, giving up for now", flush=True)
                return False

            if data and len(data) > 0:
                df = pd.DataFrame(data)
                df.to_csv(fpath, index=False)
                year_total += len(data)
            else:
                with open(fpath, "w") as f:
                    f.write("skip")

            time.sleep(0.2)

        total += year_total
        print(f"  {year}: {year_total} rows", flush=True)

    # Merge
    all_dfs = []
    for year, _ in YEARS:
        for rep in REPORTERS:
            fpath = os.path.join(hs_dir, f"{year}_{rep}.csv")
            if os.path.exists(fpath) and os.path.getsize(fpath) > 20:
                try:
                    df = pd.read_csv(fpath)
                    if len(df) > 0:
                        all_dfs.append(df)
                except:
                    pass

    if all_dfs:
        merged = pd.concat(all_dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        merged.to_csv(final, index=False)
        print(f"HS {hs}: MERGED {len(merged):,} rows", flush=True)
        return True

    print(f"HS {hs}: NO DATA", flush=True)
    return False


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else None
    if hs:
        download_hs(hs)
    else:
        for h in HS_CODES:
            download_hs(h)
