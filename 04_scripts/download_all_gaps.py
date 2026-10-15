"""
Download missing Comtrade bilateral import files.

An existing ``skip`` file records a successful API response with no rows and is
therefore complete. Failed requests are logged but do not create a data file, so
they remain eligible for a later retry.

Examples:

    python 04_scripts/download_all_gaps.py --batch antimony --dry-run
    python 04_scripts/download_all_gaps.py --products 8110 --max-calls 180
    python 04_scripts/download_all_gaps.py --batch core-placebos
"""

import argparse
import requests
import pandas as pd
import time
import os
import threading
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from comtrade_auth import load_comtrade_keys

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "03_data" / "raw"
LOG_FILE = DATA / "comtrade_download_log.txt"
KEYS: list[str] = []
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"
LAST_PERIOD = "202603"
PERIODS_BY_YEAR = {
    **{
        str(year): ",".join(f"{year}{month:02d}" for month in range(1, 13))
        for year in range(2019, 2026)
    },
    "2026": ",".join(f"2026{month:02d}" for month in range(1, 4)),
}

REPORTERS = [
    "276", "97", "392", "344", "410", "826", "842", "56", "124", "156",
    "724", "818", "251", "764", "752", "757", "975", "76", "380", "792",
    "100", "203", "376", "398", "528", "804", "191", "702", "428", "36",
    "616", "31", "554", "704", "440", "348", "642", "579", "372",
    "32", "484", "620", "604", "508", "703", "84", "682", "705", "404",
    "360", "699", "710", "834", "860", "854", "788",
]

HS_LABELS = {
    "2504": "graphite", "8110": "antimony", "2617": "other_ores_broad",
    "261710": "antimony_ores",
    "8106": "bismuth", "284180": "tungstates",
    "811292": "GaGe", "282560": "GeO2", "282580": "Sb_oxides", "8101": "tungsten",
    "280450": "Te_B", "284690": "REE_noncerium",
    "2818": "alumina", "8111": "manganese", "2811": "acids",
    "8103": "tantalum", "8104": "magnesium", "8105": "cobalt",
    "8108": "titanium", "8109": "zirconium",
    "282530": "V_oxides", "282520": "Li_hydroxide", "282110": "Fe_oxide_pigments",
    "2820": "Mn_oxides", "2827": "chlorides", "2833": "sulfates",
    "284610": "cerium", "282570": "Mo_oxides", "284170": "molybdates",
    "811221": "chromium",
    "2615": "Nb_Ta_V_Zr_ores",
    "380120": "colloidal_graphite", "380130": "carbon_electrodes",
    "3801": "art.graphite",
}

BATCHES = {
    # Highest-value additions to the current 2023-2024 thesis cases.
    "antimony": ["8110", "261710", "282580"],
    "extend-current": [
        "2504", "811292", "282560", "2818", "8111", "2811", "3801"
    ],
    # Clean February 2025 cases, followed by the usable partial case.
    "wave4-clean": ["8106", "284180"],
    "wave4-partial": ["8101"],
    # Closest policy-screened controls. These are candidates, not automatically
    # valid placebos; pre-treatment fit must still be checked.
    "core-placebos": [
        "2615", "284170", "811221", "380130",
        "282530", "282520", "282570",
    ],
    "metal-placebos": ["8103", "8108", "8109", "8104", "8105"],
    # Broad or episode-specific controls with lower expected information value.
    "deferred-placebos": [
        "282110", "2820", "2833", "284610",
    ],
    # Not clean controls: 380120 may fall within natural-flake graphite
    # products; HS 2827 includes controlled germanium tetrachloride.
    "policy-contaminated": ["380120", "2827"],
    "broad-diagnostics": ["2617"],
    "marginal-treated": ["280450", "284690"],
}
ALL_PRODUCTS = list(dict.fromkeys(
    product
    for products in BATCHES.values()
    for product in products
))

lock = threading.Lock()
stats = {"calls": 0, "rows": 0, "empty": 0, "errors": 0, "rate_limits": 0}
key_idx = 0


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    with lock:
        print(line, flush=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


def is_bad(fp):
    if not fp.exists():
        return True
    if os.path.getsize(fp) <= 20:
        return fp.read_text(errors="ignore").strip() != "skip"
    try:
        df = pd.read_csv(fp, nrows=1)
        return len(df) == 0 and "skip" not in df.columns
    except Exception:
        return True


def ensure_keys() -> list[str]:
    global KEYS
    if not KEYS:
        KEYS = load_comtrade_keys()
    return KEYS


def get_key():
    global key_idx
    with lock:
        keys = ensure_keys()
        k = keys[key_idx % len(keys)]
        key_idx += 1
        return k


def rotate_key():
    global key_idx
    with lock:
        key_idx += 1


def fetch_one(hs, yr, rep, fp, max_attempts=2):
    period = PERIODS_BY_YEAR[yr]
    for attempt in range(max_attempts):
        try:
            key = get_key()
            r = requests.get(
                BASE,
                params={
                    "reporterCode": rep,
                    "flowCode": "M",
                    "cmdCode": hs,
                    "period": period,
                    "subscription-key": key,
                },
                timeout=60,
            )
            with lock:
                stats["calls"] += 1

            if r.status_code == 200:
                data = r.json().get("data", [])
                if data:
                    pd.DataFrame(data).to_csv(fp, index=False)
                    with lock:
                        stats["rows"] += len(data)
                    return "ok_data", len(data)
                else:
                    fp.write_text("skip")
                    with lock:
                        stats["empty"] += 1
                    return "ok_empty", 0
            elif r.status_code == 429:
                with lock:
                    stats["rate_limits"] += 1
                rotate_key()
                time.sleep(30)
                continue
            elif r.status_code in (403, 409):
                rotate_key()
                time.sleep(60)
                continue
            elif r.status_code == 404:
                fp.write_text("skip")
                with lock:
                    stats["empty"] += 1
                return "no_data", 0
            else:
                with lock:
                    stats["errors"] += 1
                return f"http_{r.status_code}", 0
        except requests.Timeout:
            with lock:
                stats["errors"] += 1
            if attempt + 1 < max_attempts:
                time.sleep(5)
                continue
            return "timeout", 0
        except Exception as e:
            with lock:
                stats["errors"] += 1
            return str(e)[:50], 0
    return "failed_retries", 0


def scan_gaps(products, through):
    gaps = []
    final_year = 2024 if through == "202412" else 2026
    for hs in products:
        hs_dir = DATA / f"imports_{hs}"
        hs_dir.mkdir(exist_ok=True)
        for yr in PERIODS_BY_YEAR:
            if int(yr) > final_year:
                continue
            for rep in REPORTERS:
                fp = hs_dir / f"{yr}_{rep}.csv"
                if is_bad(fp):
                    gaps.append((hs, yr, rep, fp))
    return gaps


def merge_all(products):
    for hs in products:
        hs_dir = DATA / f"imports_{hs}"
        merged_path = DATA / f"comtrade_{hs}_imports.csv"
        dfs = []
        for f in sorted(hs_dir.glob("*.csv")):
            if is_bad(f):
                continue
            try:
                d = pd.read_csv(f)
                if len(d) > 0:
                    dfs.append(d)
            except Exception:
                pass
        if dfs:
            merged = pd.concat(dfs, ignore_index=True)
            merged["download_date"] = datetime.now().strftime("%Y-%m-%d")
            merged.to_csv(merged_path, index=False)
            log(f"  MERGED {hs}: {len(merged):,} rows")
        else:
            log(f"  {hs}: NO DATA")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch",
        choices=[*BATCHES, "all"],
        default="antimony",
        help="Named priority batch. Default: antimony.",
    )
    parser.add_argument(
        "--products",
        help="Comma-separated HS codes; overrides --batch.",
    )
    parser.add_argument(
        "--max-calls",
        type=int,
        help="Stop after this many currently missing reporter-year requests.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Concurrent requests. Default 2 to reduce rate-limit collisions.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print missing requests without calling the API.",
    )
    parser.add_argument(
        "--through",
        choices=["202412", "202603"],
        default="202603",
        help="Coverage endpoint. Use 202412 for the historical antimony audit.",
    )
    return parser.parse_args()


def selected_products(args):
    if args.products:
        products = [item.strip() for item in args.products.split(",") if item.strip()]
        unknown = [item for item in products if item not in HS_LABELS]
        if unknown:
            raise ValueError(f"Unknown HS codes: {', '.join(unknown)}")
        return products
    if args.batch == "all":
        return ALL_PRODUCTS
    return BATCHES[args.batch]


def main():
    args = parse_args()
    products = selected_products(args)
    log("=" * 70)
    log(
        f"COMTRADE DOWNLOAD — scope={'products' if args.products else args.batch}, "
        f"products={','.join(products)}, target={args.through}"
    )
    log("=" * 70)

    gaps = scan_gaps(products, args.through)
    total_missing = len(gaps)
    if args.max_calls is not None:
        gaps = gaps[: max(args.max_calls, 0)]
    log(f"Total gaps: {len(gaps)}")
    if len(gaps) != total_missing:
        log(f"  Limited from {total_missing} by --max-calls")

    by_hs = {}
    for hs, yr, rep, fp in gaps:
        by_hs.setdefault(hs, []).append((yr, rep, fp))
    for hs in products:
        n = len(by_hs.get(hs, []))
        if n:
            log(f"  {hs} ({HS_LABELS[hs]}): {n} files")

    if args.dry_run:
        log("DRY RUN: no API requests made and no files changed.")
        return

    if not gaps:
        log("Nothing to download!")
        return

    try:
        ensure_keys()
    except Exception as e:
        log(f"CREDENTIAL ERROR: {e}")
        return

    start = time.time()
    last_report = [start]
    report_interval = 30

    completed = 0
    total = len(gaps)
    status_counts = {}

    for hs in products:
        items = by_hs.get(hs, [])
        if not items:
            continue

        log(f"\n--- HS {hs} ({HS_LABELS[hs]}): {len(items)} files ---")

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {}
            for yr, rep, fp in items:
                max_attempts = 1 if args.max_calls is not None else 2
                fut = executor.submit(
                    fetch_one, hs, yr, rep, fp, max_attempts
                )
                futures[fut] = (yr, rep)

            for fut in as_completed(futures):
                yr, rep = futures[fut]
                try:
                    status, nrows = fut.result()
                except Exception as e:
                    with lock:
                        stats["errors"] += 1
                    status, nrows = str(e)[:50], 0

                status_counts[status] = status_counts.get(status, 0) + 1

                completed += 1

                now = time.time()
                if now - last_report[0] >= report_interval or completed == total:
                    elapsed = now - start
                    rate = completed / elapsed if elapsed > 0 else 0
                    eta = (total - completed) / rate if rate > 0 else 0
                    log(
                        f"  Progress: {completed}/{total} "
                        f"({stats['rows']:,} rows, {stats['empty']} empty, "
                        f"{stats['errors']} err) "
                        f"| {rate:.1f}/s | ETA {eta/60:.0f}m"
                    )
                    last_report[0] = now

    elapsed = time.time() - start
    log(f"\n{'=' * 70}")
    log(f"DOWNLOAD COMPLETE in {elapsed/60:.1f} min")
    log(f"  API calls: {stats['calls']}")
    log(f"  New rows: {stats['rows']:,}")
    log(f"  Empty (no data): {stats['empty']}")
    log(f"  Errors: {stats['errors']}")
    log(f"  Rate limits: {stats['rate_limits']}")
    bad_statuses = [
        (status, count)
        for status, count in status_counts.items()
        if status not in {"ok_data", "ok_empty", "no_data"}
    ]
    if bad_statuses:
        for status, count in sorted(bad_statuses, key=lambda item: (-item[1], item[0]))[:5]:
            log(f"  Status {status}: {count}")
    log(f"{'=' * 70}")

    log("\nMerging...")
    merge_all(products)

    log("\nVerifying...")
    remaining = scan_gaps(products, args.through)
    log(f"Remaining gaps: {len(remaining)}")
    if remaining:
        by_hs2 = {}
        for hs, yr, rep, fp in remaining:
            by_hs2.setdefault(hs, []).append(yr)
        for hs in products:
            yrs = by_hs2.get(hs, [])
            if yrs:
                from collections import Counter
                yr_counts = Counter(yrs)
                details = ", ".join(f"{yr}:{c}" for yr, c in sorted(yr_counts.items()))
                log(f"  {hs}: {len(yrs)} still missing ({details})")
            else:
                log(f"  {hs}: COMPLETE")

    log("DONE.")


if __name__ == "__main__":
    main()
