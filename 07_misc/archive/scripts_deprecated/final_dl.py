"""
Focused downloader: finish 3801, download 2501 salt, 2818 alumina.
Sequential, in order. Stops when quota runs out.
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime
from pathlib import Path

KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

REPORTERS = ['276','97','392','344','410','826','842','56','124','156',
    '724','818','251','764','752','757','975','76','380','792',
    '100','203','376','398','528','804','191','702','428','36',
    '616','31','554','704','440','348','642','579','372',
    '32','484','620','604','508','703','84','682','705','404',
    '360','699','710','834','860','854','788']

DATA_DIR = Path("<repo-root>/03_data/raw")
LOG = DATA_DIR / "final_dl.log"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)
    with open(LOG, "a") as f: f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

YEAR_PERIODS = {str(y): f"{y}{m:02d}" for y in range(2019,2025) for m in range(1,13)}
YEAR_STR = {str(y): ",".join([f"{y}{m:02d}" for m in range(1,13)]) for y in range(2019,2025)}

def is_bad(fpath):
    if not os.path.exists(fpath): return True
    if os.path.getsize(fpath) <= 20: return True
    try:
        df = pd.read_csv(fpath, nrows=1)
        return len(df) == 0 or 'skip' in df.columns
    except: return True

def fetch(hs, period, reporter, key):
    try:
        r = requests.get(BASE, params={"reporterCode": reporter, "flowCode": "M", "cmdCode": hs, "period": period, "subscription-key": key}, timeout=30)
        if r.status_code == 200: return r.json().get("data", [])
        if r.status_code == 403: return "quota"
        if r.status_code == 409: return "rate_limit"
    except: return "error"
    return None

def download_hs(hs, years):
    hs_dir = DATA_DIR / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    key_idx = 0
    total_new = 0
    calls = 0
    
    for year in years:
        period = YEAR_STR[year]
        year_new = 0
        for rep in REPORTERS:
            fpath = hs_dir / f"{year}_{rep}.csv"
            if not is_bad(fpath): continue
            
            data = fetch(hs, period, rep, KEYS[key_idx % 2])
            calls += 1
            
            if data in ("quota", "rate_limit"):
                key_idx += 1
                data = fetch(hs, period, rep, KEYS[key_idx % 2])
                calls += 1
            
            if data in ("quota", "rate_limit"):
                log(f"  {hs} {year}_{rep}: quota both keys, sleeping 4min")
                time.sleep(240)
                key_idx += 1
                data = fetch(hs, period, rep, KEYS[key_idx % 2])
                calls += 1
            
            if data in ("quota", "rate_limit"):
                log(f"  {hs}: QUOTA EXHAUSTED after {calls} calls. Stopping.")
                return total_new, calls, False
            
            if data == "error":
                with open(fpath, "w") as f: f.write("skip")
                continue
            
            if data and len(data) > 0:
                pd.DataFrame(data).to_csv(fpath, index=False)
                year_new += len(data)
            else:
                with open(fpath, "w") as f: f.write("skip")
            
            time.sleep(0.25)
        
        total_new += year_new
        log(f"  {hs} {year}: {year_new} new rows, {calls} calls")
    
    return total_new, calls, True

def merge(hs):
    hs_dir = DATA_DIR / f"imports_{hs}"
    merged_path = DATA_DIR / f"comtrade_{hs}_imports.csv"
    dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
        if not is_bad(f):
            try:
                df = pd.read_csv(f)
                if len(df) > 0: dfs.append(df)
            except: pass
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        merged.to_csv(merged_path, index=False)
        log(f"  MERGED {hs}: {len(merged):,} rows")

def main():
    log("=" * 50)
    log("FINAL DOWNLOAD RUN")
    
    # 1. Finish 3801 — needs 2023-2024
    log("\n1. HS 3801 (Artificial graphite) — finishing 2023-2024")
    n, c, ok = download_hs("3801", ["2023", "2024"])
    merge("3801")
    log(f"   3801 done: {n} new rows, {c} calls, ok={ok}")
    
    if not ok:
        log("QUOTA EXHAUSTED after 3801. Stopping.")
        return
    
    # 2. HS 2501 Salt
    log("\n2. HS 2501 (Salt — placebo chapter 25)")
    n, c, ok = download_hs("2501", ["2019","2020","2021","2022","2023","2024"])
    merge("2501")
    log(f"   2501 done: {n} new rows, {c} calls, ok={ok}")
    
    if not ok:
        log("QUOTA EXHAUSTED after 2501. Stopping.")
        return
    
    # 3. HS 2818 Alumina
    log("\n3. HS 2818 (Aluminum oxide — placebo chapter 28)")
    n, c, ok = download_hs("2818", ["2019","2020","2021","2022","2023","2024"])
    merge("2818")
    log(f"   2818 done: {n} new rows, {c} calls, ok={ok}")
    
    log("\n" + "=" * 50)
    log("ALL DONE")
    log("=" * 50)

if __name__ == "__main__":
    main()
