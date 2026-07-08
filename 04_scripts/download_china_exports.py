"""
Audit and download China export series for all treated HS codes.

Each product is re-requested in annual batches through March 2026. A companion
coverage file records whether every month was returned by Comtrade, allowing
genuine zero/no-record months to be distinguished from quota or network
failures. Existing output files are replaced only after every annual request
succeeds.
"""

import argparse
import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

from comtrade_auth import load_comtrade_keys

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "03_data" / "raw"
BASE = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

TASKS = [
    {"hs": "2504", "label": "Natural graphite exports"},
    {"hs": "3801", "label": "Artificial and colloidal graphite exports"},
    {"hs": "8110", "label": "Antimony metal exports"},
    {"hs": "2617", "label": "Broad other-ores exports (diagnostic)"},
    {"hs": "261710", "label": "Antimony ores and concentrates exports"},
    {"hs": "8106", "label": "Bismuth metal exports"},
    {"hs": "284180", "label": "Tungstates/APT exports"},
    {"hs": "811292", "label": "Ga/Ge bundle exports"},
    {"hs": "282560", "label": "GeO2/ZrO2 exports"},
    {"hs": "282580", "label": "Sb oxides exports"},
    {"hs": "8101", "label": "Tungsten metal exports"},
    {"hs": "280450", "label": "Te+B exports"},
    {"hs": "284690", "label": "Non-cerium REE exports"},
]
FULL_PERIODS_BY_YEAR = {
    **{
        year: ",".join(f"{year}{month:02d}" for month in range(1, 13))
        for year in range(2019, 2026)
    },
    2026: ",".join(f"2026{month:02d}" for month in range(1, 4)),
}
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def fetch_exports(hs, period, key):
    try:
        r = requests.get(
            BASE,
            params={
                "reporterCode": "156",
                "flowCode": "X",
                "cmdCode": hs,
                "period": str(period),
                "partnerCode": "0",
                "partner2Code": "0",
                "customsCode": "C00",
                "motCode": "0",
                "maxRecords": "500",
                "subscription-key": key,
            },
            timeout=30,
        )
        if r.status_code == 200:
            return "ok", r.json().get("data", [])
        if r.status_code in (403, 409):
            return "quota", r.headers.get("Retry-After")
        if r.status_code == 429:
            return "rate_limit", None
        return "error", f"HTTP {r.status_code}"
    except Exception as e:
        return "error", str(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--products",
        help="Comma-separated HS codes. Default: all configured treated products.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request plan without calling the API.",
    )
    parser.add_argument(
        "--through",
        choices=["202412", "202603"],
        default="202603",
        help="Audit endpoint. Use 202412 to reproduce the 12-call antimony audit.",
    )
    parser.add_argument(
        "--from-year",
        type=int,
        choices=range(2019, 2027),
        default=2019,
        help="First annual request. Existing output is preserved and merged.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    tasks = TASKS
    if args.products:
        selected = {item.strip() for item in args.products.split(",") if item.strip()}
        tasks = [task for task in TASKS if task["hs"] in selected]
        missing = selected - {task["hs"] for task in tasks}
        if missing:
            raise ValueError(f"Unknown export HS codes: {', '.join(sorted(missing))}")

    final_year = 2024 if args.through == "202412" else 2026
    periods_by_year = {
        year: periods
        for year, periods in FULL_PERIODS_BY_YEAR.items()
        if args.from_year <= year <= final_year
    }
    target_periods_by_year = {
        year: periods
        for year, periods in FULL_PERIODS_BY_YEAR.items()
        if year <= final_year
    }
    expected_periods = [
        int(period)
        for periods in target_periods_by_year.values()
        for period in periods.split(",")
    ]

    log("=" * 60)
    log("CHINA EXPORT SERIES — ALL TREATED HS CODES")
    log("=" * 60)
    log(
        f"Products={','.join(task['hs'] for task in tasks)}; "
        f"annual requests={len(tasks) * len(periods_by_year)}; "
        f"request_years={args.from_year}-{final_year}; "
        f"coverage_target=201901-{args.through}"
    )
    if args.dry_run:
        log("DRY RUN: no API requests made and no files changed.")
        return

    keys = load_comtrade_keys()
    key_index = 0

    for task in tasks:
        hs = task["hs"]
        label = task["label"]
        fp = DATA / f"comtrade_{hs}_china_exports.csv"
        coverage_fp = DATA / f"comtrade_{hs}_china_exports_coverage.csv"
        all_periods = expected_periods

        log(f"\n--- {hs} ({label}) ---")
        rows = []
        completed_years = []
        for year in periods_by_year:
            period = periods_by_year[year]
            for attempt in range(3):
                key = keys[key_index % len(keys)]
                status, data = fetch_exports(hs, period, key)
                if status == "ok":
                    rows.extend(data)
                    completed_years.append(year)
                    returned = sorted(
                        pd.to_numeric(
                            pd.Series([row.get("period") for row in data]),
                            errors="coerce",
                        ).dropna().astype(int).unique()
                    )
                    expected = len(periods_by_year[year].split(","))
                    log(f"  {year}: {len(returned)}/{expected} months returned")
                    break
                elif status == "quota":
                    key_index += 1
                    log(f"  Quota exhausted; switching key (retry after: {data})")
                    time.sleep(2)
                    continue
                elif status == "rate_limit":
                    key_index += 1
                    time.sleep(30)
                    continue
                else:
                    log(f"  {year}: {data}")
                    break
            time.sleep(1)

        if len(completed_years) != len(periods_by_year):
            log(
                f"  INCOMPLETE: received {len(completed_years)}/{len(periods_by_year)} annual responses. "
                "Existing files were not changed."
            )
            continue

        exports = pd.DataFrame(rows)
        if fp.exists():
            existing = pd.read_csv(fp)
            exports = pd.concat([existing, exports], ignore_index=True)
        if len(exports):
            exports["period"] = pd.to_numeric(exports["period"], errors="coerce")
            exports = exports.dropna(subset=["period"])
            exports["period"] = exports["period"].astype(int)
            exports = exports.sort_values("period").drop_duplicates("period", keep="last")
            keep = [
                "reporterCode", "partnerCode", "period", "cmdCode", "flowCode",
                "primaryValue", "qty", "netWgt", "fobvalue", "cifvalue",
            ]
            exports = exports[[col for col in keep if col in exports.columns]]
        returned_periods = set(exports["period"]) if len(exports) else set()
        prior = None
        if coverage_fp.exists():
            prior = pd.read_csv(coverage_fp)
            prior_periods = pd.to_numeric(
                prior["period"], errors="coerce"
            ).dropna().astype(int)
            all_periods = sorted(set(all_periods) | set(prior_periods))

        coverage = pd.DataFrame({"period": all_periods})
        coverage["api_record_returned"] = coverage["period"].isin(returned_periods)
        previous_status = {}
        if prior is not None:
            previous_status = dict(zip(prior["period"], prior["status"]))
        requested_periods = {
            int(period)
            for periods in periods_by_year.values()
            for period in periods.split(",")
        }
        coverage["status"] = (
            coverage["period"].map(previous_status).astype("object")
        )
        coverage.loc[coverage["api_record_returned"], "status"] = "reported"
        coverage.loc[
            coverage["period"].isin(requested_periods)
            & ~coverage["api_record_returned"],
            "status",
        ] = "no_record_returned"
        coverage["status"] = coverage["status"].fillna("not_audited")
        coverage["audit_date"] = datetime.now().strftime("%Y-%m-%d")

        exports["hs_description"] = label
        exports["download_date"] = datetime.now().strftime("%Y-%m-%d")
        exports.to_csv(fp, index=False)
        coverage.to_csv(coverage_fp, index=False)
        missing = coverage.loc[
            ~coverage["api_record_returned"], "period"
        ].tolist()
        log(
            f"  SAVED: {fp.name} "
            f"({len(exports)}/{len(expected_periods)} reported months)"
        )
        log(f"  COVERAGE: {coverage_fp.name}; no-record months={missing}")

    log(f"\n{'=' * 60}")
    log("DONE")
    log("=" * 60)


if __name__ == "__main__":
    main()
