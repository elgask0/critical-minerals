"""
Download 2811 (inorganic acids) + 2821 (iron oxides) for placebo pool.
Parallel to existing 8111 download — will share API keys.
Uses key rotation + retry logic from mass_dl.py
"""
import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_2"]  # second key only (8111 has first)
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
YEARS = ["2019","2020","2021","2022","2023","2024"]
YEAR_PERIODS = {str(y): ",".join(f"{y}{m:02d}" for m in range(1,13)) for y in range(2019,2025)}

HS_DICT = {"2811": "Inorganic acids", "2821": "Iron oxides"}
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

total_calls = 0

def fetch(hs, period, reporter):
    global total_calls
    for attempt in range(3):
        key = KEYS[0]
        try:
            r = requests.get(BASE, params={"reporterCode": reporter, "flowCode": "M", "cmdCode": hs, "period": period, "subscription-key": key}, timeout=30)
            total_calls += 1
            if r.status_code == 200:
                return r.json().get("data", [])
            if r.status_code in (403, 409):
                log(f"  Rate limited (key usage), sleeping 60s...")
                time.sleep(60); continue
            if r.status_code == 429:
                log(f"  Quota exhausted, sleeping 120s...")
                time.sleep(120); continue
            return None
        except Exception as e:
            if "timeout" in str(e).lower():
                time.sleep(5); continue
            return "error"
    return None

for hs, label in HS_DICT.items():
    hs_dir = DATA / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    total = 0
    log(f"Starting HS {hs} ({label})")
    for year in YEARS:
        period = YEAR_PERIODS[year]
        ynew = 0
        log(f"  {hs} {year}: starting ({len(REPORTERS)} reporters)")
        for rep in REPORTERS:
            fp = hs_dir / f"{year}_{rep}.csv"
            if fp.exists() and os.path.getsize(fp) > 20:
                continue
            data = fetch(hs, period, rep)
            if data == "timeout":
                fp.write_text("skip")
                time.sleep(1)
                continue
            if data == "error":
                fp.write_text("skip")
                time.sleep(2)
                continue
            if data and len(data) > 0:
                pd.DataFrame(data).to_csv(fp, index=False)
                ynew += len(data)
            else:
                fp.write_text("skip")
            time.sleep(0.35)
        total += ynew
        log(f"  {hs} {year}: {ynew} new rows, {total_calls} API calls")
    
    # Merge
    dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
        try:
            d = pd.read_csv(f)
            if len(d) > 0: dfs.append(d)
        except: pass
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        merged.to_csv(DATA / f"comtrade_{hs}_imports.csv", index=False)
        log(f"  MERGED {hs}: {len(merged):,} rows -> comtrade_{hs}_imports.csv")
    else:
        log(f"  {hs}: NO DATA merged!")
    log(f"  HS {hs} COMPLETE ({total:,} new rows)\n")

log(f"ALL DONE. Total API calls: {total_calls}")
