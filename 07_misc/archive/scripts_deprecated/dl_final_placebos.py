"""
Download 2811+2821 using quarterly periods.
3-month batches are much faster per call (8s vs 43s for yearly).
"""
import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

# Quarterly periods
QUARTERS = [
    ("Q1", "01,02,03"),
    ("Q2", "04,05,06"),
    ("Q3", "07,08,09"),
    ("Q4", "10,11,12"),
]

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

for hs, label in [("2811", "Inorganic acids"), ("2821", "Iron oxides")]:
    log(f"Downloading HS {hs} ({label})")
    hs_dir = DATA / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    total = 0
    calls = 0
    ki = 0
    
    for year in ["2019","2020","2021","2022","2023","2024"]:
        ynew = 0
        for rep in REPORTERS:
            for q_label, q_months in QUARTERS:
                fp = hs_dir / f"{year}_{rep}_{q_label}.csv"
                if fp.exists() and os.path.getsize(fp) > 20:
                    continue
                
                period = f"{year}{q_months}"
                for _ in range(3):
                    try:
                        r = requests.get(BASE,
                            params={"reporterCode": rep, "flowCode": "M", "cmdCode": hs, "period": period, "subscription-key": KEYS[ki % 2]},
                            timeout=60)
                        calls += 1
                        if r.status_code == 200:
                            d = r.json().get("data", [])
                            if d:
                                pd.DataFrame(d).to_csv(fp, index=False)
                                ynew += len(d)
                            else:
                                fp.write_text("skip")
                            break
                        elif r.status_code in (403, 409):
                            ki += 1; time.sleep(2)
                        else:
                            fp.write_text("skip"); break
                    except:
                        time.sleep(5)
                time.sleep(0.25)
        total += ynew
        log(f"  {hs} {year}: {ynew} rows ({calls} calls)")
    
    # Merge: combine Q1-Q4 into full year files
    log(f"  Merging {hs}...")
    for year in ["2019","2020","2021","2022","2023","2024"]:
        for rep in REPORTERS:
            yr_file = hs_dir / f"{year}_{rep}.csv"
            if yr_file.exists(): continue
            dfs = []
            for q_label, _ in QUARTERS:
                qfile = hs_dir / f"{year}_{rep}_{q_label}.csv"
                try:
                    d = pd.read_csv(qfile)
                    if len(d) > 0: dfs.append(d)
                except: pass
            if dfs:
                pd.concat(dfs, ignore_index=True).to_csv(yr_file, index=False)
            elif len([1 for q_label,_ in QUARTERS if (hs_dir / f"{year}_{rep}_{q_label}.csv").exists()]) > 0:
                # All quarters were skips → mark year as skip
                yr_file.write_text("skip")
    
    # Final merge
    dfs = []
    for f in sorted(hs_dir.glob("*.csv")):
        name = f.stem
        if len(name.split('_')) == 3 and name.split('_')[2] in ("Q1","Q2","Q3","Q4"):
            continue  # skip quarterly files, use merged year files
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

log("ALL DONE")
