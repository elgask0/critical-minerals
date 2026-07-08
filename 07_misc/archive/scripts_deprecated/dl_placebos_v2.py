"""Download 2811+2821 with HTTP session and longer timeout."""
import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
YEARS = ["2019","2020","2021","2022","2023","2024"]
YEAR_PERIODS = {str(y): ",".join(f"{y}{m:02d}" for m in range(1,13)) for y in range(2019,2025)}
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def is_good(fp):
    if not fp.exists() or os.path.getsize(fp) <= 20: return False
    try:
        df = pd.read_csv(fp, nrows=1)
        return len(df) > 0
    except: return False

# Use a session for HTTP keep-alive
session = requests.Session()
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
        period_str = YEAR_PERIODS[year]
        
        for rep_idx, rep in enumerate(REPORTERS):
            fp = hs_dir / f"{year}_{rep}.csv"
            if is_good(fp):
                yskip += 1
                continue
            
            for attempt in range(5):
                key = KEYS[ki % 2]
                try:
                    r = session.get(BASE,
                        params={"reporterCode": rep, "flowCode": "M", "cmdCode": hs, "period": period_str, "subscription-key": key},
                        timeout=120)
                    total_calls += 1
                    
                    if r.status_code == 200:
                        data = r.json().get("data", [])
                        if data:
                            pd.DataFrame(data).to_csv(fp, index=False)
                            ynew += len(data)
                        else:
                            fp.write_text("skip")
                        break
                    elif r.status_code in (403, 409):
                        msg = r.json().get("message", "")
                        if "quota" in msg.lower():
                            log(f"  QUOTA on key {ki%2}, sleeping 2h")
                            time.sleep(7200)
                        ki += 1
                        continue
                    elif r.status_code == 429:
                        log(f"  Rate limited, sleeping 60s")
                        time.sleep(60)
                        ki += 1
                        continue
                    else:
                        fp.write_text("skip")
                        break
                except requests.Timeout:
                    log(f"  Timeout {hs} {year}_{rep}, attempt {attempt+1}/5")
                    time.sleep(10)
                    continue
                except Exception as e:
                    log(f"  Error {hs} {year}_{rep}: {e}")
                    time.sleep(5)
                    continue
            
            time.sleep(0.5)
        
        log(f"  {hs} {year}: {ynew} new, {yskip} existing ({total_calls} calls)")
    
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
        out = DATA / f"comtrade_{hs}_imports.csv"
        merged.to_csv(out, index=False)
        log(f"  MERGED {hs}: {len(merged):,} rows -> {out.name}")
    else:
        log(f"  {hs}: NO DATA!")

session.close()
log(f"ALL DONE. Calls: {total_calls}")
