"""Download remaining: 8111(missing)+2811+2821. Verbose logging per reporter."""
import requests, pandas as pd, time, os, sys
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
    """Check if file exists and has valid CSV data."""
    if not fp.exists() or os.path.getsize(fp) <= 20: return False
    try:
        df = pd.read_csv(fp, nrows=1)
        return len(df) > 0
    except: return False

def fetch(hs, period_str, rep, key, attempt=0):
    try:
        r = requests.get(BASE, params={"reporterCode": rep, "flowCode": "M", "cmdCode": hs, "period": period_str, "subscription-key": key}, timeout=30)
        if r.status_code == 200:
            return "ok", r.json().get("data", [])
        if r.status_code == 403:
            msg = r.json().get("message", "")
            if "quota" in msg.lower():
                return "quota", msg
            return "key_switch", msg
        if r.status_code == 429:
            return "rate_limit", None
        return "error", f"status={r.status_code}"
    except requests.Timeout:
        return "timeout", None
    except Exception as e:
        return "error", str(e)

ki = 0
total_calls = 0

# Tasks: (hs, label, years, skip_existing)
for hs, label, years, skip in [
    ("8111", "Manganese (missing 2024)", ["2024"], True),
    ("2811", "Inorganic acids", YEARS, True),
    ("2821", "Iron oxides", YEARS, True),
]:
    hs_dir = DATA / f"imports_{hs}"
    hs_dir.mkdir(exist_ok=True)
    total_new = 0
    log(f"\n=== HS {hs} ({label}) ===")

    for year in years:
        period_str = YEAR_PERIODS[year]
        ynew = 0
        yskip = 0
        for rep in REPORTERS:
            fp = hs_dir / f"{year}_{rep}.csv"
            if skip and is_good(fp):
                yskip += 1
                continue

            # Try both keys with retry
            for attempt in range(5):
                key = KEYS[ki % 2]
                status, data = fetch(hs, period_str, rep, key, attempt)
                total_calls += 1

                if status == "ok":
                    if data:
                        pd.DataFrame(data).to_csv(fp, index=False)
                        ynew += len(data)
                    else:
                        fp.write_text("skip")
                    break
                elif status == "quota":
                    log(f"  QUOTA EXHAUSTED on key {ki%2}. Sleeping 7200s (2h)...")
                    time.sleep(7200)
                    ki += 1
                    continue
                elif status == "key_switch":
                    ki += 1
                    time.sleep(1)
                    continue
                elif status == "rate_limit":
                    log(f"  Rate limited key {ki%2}, sleeping 60s...")
                    time.sleep(60)
                    ki += 1
                    continue
                elif status == "timeout":
                    log(f"  Timeout {hs} {year}_{rep}, retry {attempt+1}/5")
                    time.sleep(5)
                    continue
                else:
                    log(f"  Error {hs} {year}_{rep}: {data}, retry {attempt+1}/5")
                    time.sleep(3)
                    continue

            time.sleep(0.35)

        total_new += ynew
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
        log(f"  {hs}: NO DATA merged!")

log(f"\nALL DONE. Total API calls: {total_calls}")
