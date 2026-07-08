"""Download 2811+2821 using quarterly periods for faster responses."""
import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
YEARS = ["2019","2020","2021","2022","2023","2024"]
QUARTERS = {"Q1":"01,02,03","Q2":"04,05,06","Q3":"07,08,09","Q4":"10,11,12"}
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def is_good(fp):
    if not fp.exists() or os.path.getsize(fp) <= 20: return False
    try:
        df = pd.read_csv(fp, nrows=1)
        return len(df) > 0
    except: return False

def fetch(hs, year, q_label, q_months, rep, key):
    period = f"{year}{q_months}"
    r = requests.get(BASE, params={"reporterCode": rep, "flowCode": "M", "cmdCode": hs, "period": period, "subscription-key": key}, timeout=30)
    if r.status_code == 200:
        return "ok", r.json().get("data", [])
    if r.status_code in (403, 409):
        msg = r.json().get("message","")
        if "quota" in msg.lower():
            return "quota", msg
        return "key_switch", msg
    if r.status_code == 429:
        return "rate_limit", None
    return "error", f"status={r.status_code}"

# One session per HS to avoid stale connections
ki = 0
total_calls = 0

for hs, label in [("2811", "Inorganic acids"), ("2821", "Iron oxides")]:
    hs_dir = DATA / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    total_new = 0
    log(f"\n=== HS {hs} ({label}) ===")
    
    for year in YEARS:
        ynew = 0
        yskip = 0
        
        for rep in REPORTERS:
            # Individual monthly files named: year_rep_q1.csv etc
            # We'll collect quarterly data and merge per-reporter later
            for q_label, q_months in QUARTERS.items():
                fp = hs_dir / f"{year}_{rep}_{q_label}.csv"
                if is_good(fp):
                    continue
                
                # Only try if this rep has ANY files for this year (to save calls)
                # Actually, just try — many reporters won't have data for 2811
                for attempt in range(3):
                    key = KEYS[ki % 2]
                    status, data = fetch(hs, year, q_label, q_months, rep, key)
                    total_calls += 1
                    
                    if status == "ok":
                        if data:
                            pd.DataFrame(data).to_csv(fp, index=False)
                            ynew += len(data)
                        else:
                            fp.write_text("skip")
                        break
                    elif status == "quota":
                        log(f"  QUOTA key {ki%2}, sleeping 2h")
                        time.sleep(7200)
                        ki += 1
                        continue
                    elif status == "key_switch":
                        ki += 1; time.sleep(1); continue
                    elif status == "rate_limit":
                        log(f"  Rate limited, sleeping 60s")
                        time.sleep(60); ki += 1; continue
                    else:
                        log(f"  Error {hs} {year}_{rep}_{q_label}: {status}")
                        time.sleep(3); continue
                
                time.sleep(0.5)
        
        log(f"  {hs} {year}: {ynew} rows ({total_calls} calls)")
    
    # Merge quarterly files into yearly reporter files, then full merge
    # First, consolidate: for each (year, rep), combine Q1-Q4 into year_rep.csv
    for year in YEARS:
        for rep in REPORTERS:
            yr_fp = hs_dir / f"{year}_{rep}.csv"
            if yr_fp.exists(): continue  # already merged
            
            qdfs = []
            for q_label in QUARTERS:
                qfp = hs_dir / f"{year}_{rep}_{q_label}.csv"
                try:
                    d = pd.read_csv(qfp)
                    if len(d) > 0: qdfs.append(d)
                except: pass
            
            if qdfs:
                pd.concat(qdfs, ignore_index=True).to_csv(yr_fp, index=False)
    
    # Final merge
    dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
        # Skip quarterly files, only use merged YYYY_REP files
        name = f.stem
        if len(name.split('_')) == 3: continue  # skip 2019_276_Q1.csv
        try:
            d = pd.read_csv(f)
            if len(d) > 0: dfs.append(d)
        except: pass
    
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
        out = DATA / f"comtrade_{hs}_imports.csv"
        merged.to_csv(out, index=False)
        log(f"  MERGED {hs}: {len(merged):,} rows -> {out.name}")
    else:
        log(f"  {hs}: NO DATA!")
    
    log(f"  HS {hs} DONE\n")

log(f"ALL DONE. Total calls: {total_calls}")
