"""
Complete remaining downloads:
1. 2811: 6 missing 2023 reporters + all 2024
2. 2821: all years
Timeout → skip to avoid getting stuck.
"""
import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"
YEAR_STR = {str(y):",".join([f"{y}{m:02d}" for m in range(1,13)]) for y in range(2019,2025)}

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def download_year(hs, year, hs_dir, ki):
    """Download one year for one HS code. Returns (new_rows, final_ki, calls)."""
    period = YEAR_STR[year]
    ynew = 0
    calls = 0
    for rep in REPORTERS:
        fp = hs_dir / f"{year}_{rep}.csv"
        if fp.exists() and os.path.getsize(fp) > 20:
            continue
        success = False
        for attempt in range(2):  # max 2 retries
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
                    success = True
                    break
                elif r.status_code in (403, 409):
                    ki += 1; time.sleep(2)
                else:
                    fp.write_text("skip"); break
            except:
                if attempt == 0:
                    time.sleep(5)  # retry once
                else:
                    fp.write_text("skip")  # skip on second failure
        if not success:
            fp.write_text("skip")
        time.sleep(0.3)
    return ynew, ki, calls

# 1. Finish 2811: missing 2023 + all 2024
ki = 0
total_calls = 0

hs_dir_2811 = DATA / "imports_2811"
hs_dir_2811.mkdir(exist_ok=True)

log("=== 2811: missing 2023 reporters ===")
n, ki, c = download_year("2811", "2023", hs_dir_2811, ki)
total_calls += c
log(f"  2811 2023 {n} new ({c} calls)")

# Re-merge 2023 (since we may have added skip files for missing reporters)
# Just merge everything at the end

log("=== 2811: 2024 ===")
n, ki, c = download_year("2811", "2024", hs_dir_2811, ki)
total_calls += c
log(f"  2811 2024 {n} new ({c} calls)")

# Merge 2811
dfs = []
for f in sorted(hs_dir_2811.glob("*.csv")):
    try:
        d = pd.read_csv(f)
        if len(d) > 0: dfs.append(d)
    except: pass
if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
    merged.to_csv(DATA / "comtrade_2811_imports.csv", index=False)
    log(f"MERGED 2811: {len(merged):,} rows")
else:
    log("2811: NO DATA!")

# 2. Download 2821
hs_dir_2821 = DATA / "imports_2821"
hs_dir_2821.mkdir(exist_ok=True)

log("\n=== 2821: all years ===")
for year in ["2019","2020","2021","2022","2023","2024"]:
    n, ki, c = download_year("2821", year, hs_dir_2821, ki)
    total_calls += c
    log(f"  2821 {year}: {n} new ({c} calls)")

# Merge 2821
dfs = []
for f in sorted(hs_dir_2821.glob("*.csv")):
    try:
        d = pd.read_csv(f)
        if len(d) > 0: dfs.append(d)
    except: pass
if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
    merged.to_csv(DATA / "comtrade_2821_imports.csv", index=False)
    log(f"MERGED 2821: {len(merged):,} rows")
else:
    log("2821: NO DATA!")

log(f"ALL DONE. Total calls: {total_calls}")
