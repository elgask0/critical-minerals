import requests, pandas as pd, time, os
from datetime import datetime
from pathlib import Path
DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
YEAR_STR = {str(y):",".join([f"{y}{m:02d}" for m in range(1,13)]) for y in range(2019,2025)}

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

log("Downloading HS 8111 (Manganese — placebo chapter 81)")
hs_dir = DATA / "imports_8111"
hs_dir.mkdir(exist_ok=True)
total = 0
calls = 0
ki = 0

for year in ["2019","2020","2021","2022","2023","2024"]:
    period = YEAR_STR[year]
    ynew = 0
    for rep in REPORTERS:
        fp = hs_dir / f"{year}_{rep}.csv"
        if fp.exists() and os.path.getsize(fp) > 20:
            continue
        for _ in range(3):
            try:
                r = requests.get("https://comtradeapi.un.org/data/v1/get/C/M/HS",
                    params={"reporterCode": rep, "flowCode": "M", "cmdCode": "8111", "period": period, "subscription-key": KEYS[ki % 2]},
                    timeout=30)
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
                    ki += 1
                    time.sleep(2)
                else:
                    fp.write_text("skip")
                    break
            except:
                time.sleep(5)
        time.sleep(0.3)
    total += ynew
    log(f"  8111 {year}: {ynew} new, {calls} calls")

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
    merged.to_csv(DATA / "comtrade_8111_imports.csv", index=False)
    log(f"  MERGED 8111: {len(merged):,} rows")
log("DONE 8111")
