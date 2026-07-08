"""
Parallel download: 2811 + 2821 simultaneously.
Strategy: batch 10 reporters per call, 2 parallel processes (one per API key).
"""
import requests, pandas as pd, time, os, sys
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA = Path("<repo-root>/03_data/raw")
KEYS = ["COMTRADE_API_KEY_1", "COMTRADE_API_KEY_2"]
REPORTERS = ['276','97','392','344','410','826','842','56','124','156','724','818','251','764','752','757','975','76','380','792','100','203','376','398','528','804','191','702','428','36','616','31','554','704','440','348','642','579','372','32','484','620','604','508','703','84','682','705','404','360','699','710','834','860','854','788']
YEARS = ["2019","2020","2021","2022","2023","2024"]
HALVES = [("H1", "01,02,03,04,05,06"), ("H2", "07,08,09,10,11,12")]
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

# Batch reporters into groups of 15 to balance speed vs response size
REP_BATCHES = [",".join(REPORTERS[i:i+15]) for i in range(0, len(REPORTERS), 15)]
log_lock = False

def log(msg):
    global log_lock
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def fetch_batch(hs, year, half_label, half_period, rep_batch, key):
    """Fetch one batch of reporters for one half-year."""
    period = f"{year}{half_period}"
    try:
        r = requests.get(BASE,
            params={"reporterCode": rep_batch, "flowCode": "M", "cmdCode": hs, "period": period, "subscription-key": key},
            timeout=120)
        if r.status_code == 200:
            return r.json().get("data", [])
        if r.status_code in (403, 409):
            msg = r.json().get("message", "")
            if "quota" in msg.lower():
                return "QUOTA"
            return "KEY_SWITCH"
        return "ERROR"
    except Exception as e:
        return f"EXCEPTION:{e}"

def download_hs(hs, label, key_idx):
    """Download one HS code using one API key."""
    hs_dir = DATA / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    total_rows = 0
    total_calls = 0
    ki = key_idx

    log(f"[{label}] Starting on key {key_idx}")

    for year in YEARS:
        ynew = 0
        for half_label, half_period in HALVES:
            for batch_idx, rep_batch in enumerate(REP_BATCHES):
                fp = hs_dir / f"{year}_{half_label}_batch{batch_idx}.csv"
                if fp.exists() and os.path.getsize(fp) > 20:
                    try:
                        pd.read_csv(fp, nrows=1)
                        continue
                    except: pass

                for attempt in range(5):
                    key = KEYS[ki % 2]
                    result = fetch_batch(hs, year, half_label, half_period, rep_batch, key)
                    total_calls += 1

                    if isinstance(result, list):
                        if result:
                            pd.DataFrame(result).to_csv(fp, index=False)
                            ynew += len(result)
                        else:
                            fp.write_text("skip")
                        break
                    elif result == "QUOTA":
                        log(f"[{label}] QUOTA key {ki%2}, sleeping 2h")
                        time.sleep(7200)
                        ki += 1
                        continue
                    elif result == "KEY_SWITCH":
                        ki += 1
                        time.sleep(1)
                        continue
                    else:
                        log(f"[{label}] {year} batch{batch_idx}: {result}, retry {attempt+1}")
                        time.sleep(5)
                        continue

                time.sleep(0.5)

        total_rows += ynew
        log(f"[{label}] {year}: {ynew:,} rows ({total_calls} calls)")

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
        log(f"[{label}] MERGED: {len(merged):,} rows -> {out.name}")
    else:
        log(f"[{label}] NO DATA!")
    return total_rows

# Run 2811 on key 0, 2821 on key 1, in PARALLEL
log("Starting parallel downloads")
with ThreadPoolExecutor(max_workers=2) as ex:
    f1 = ex.submit(download_hs, "2811", "2811 Acids", 0)
    f2 = ex.submit(download_hs, "2821", "2821 FeOx", 1)
    for f in as_completed([f1, f2]):
        log(f"Done: {f.result():,} rows")

log("ALL DONE")
