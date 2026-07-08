"""
Download international (non-Chinese) mineral prices for price DiD analysis.

Current state: We have domestic Chinese prices but lack a complete set of
grade-matched international, China-export, and antimony benchmarks. The exact
request list is maintained in 03_data/DOWNLOAD_CHECKLIST.md.

Data sources (all require manual access):
  1. Bloomberg Terminal: European spot prices for Ga, Ge, graphite
     - Ga Rotterdam spot (USD/kg)
     - Ge dioxide European spot (USD/kg)
     - Graphite flake FOB Europe (USD/ton)
  
  2. Fastmarkets (Metal Bulletin): Assessment prices
     - https://www.fastmarkets.com/methodology/industrial-minerals/
     - Ga spot CIF Europe, Ge spot CIF Europe
  
  3. Argus Media: Price assessments
     - https://www.argusmedia.com/
  
  4. Asian Metal: China-export FOB prices
     - https://www.asianmetal.com/
     - Ga FOB China, Ge FOB China

  5. London Metal Exchange (LME): No Ga/Ge/graphite contracts exist

This script does NOT automate downloads (these are paywalled).
It provides a template for importing manually downloaded data.

Usage:
  1. Download price data from Bloomberg Terminal at ZJU:
     - In Bloomberg Terminal: 
       Ga European: <GALLIUM> <SPOT> <EU> 
       Ge European: <GERMANI> <SPOT> <EU>
       Graphite European: <GRPHTE> <FLAKE> <CIF EU>
     - Or Wind codes for export FOB prices
  
  2. Save the Excel/CSV to: 03_data/raw/international_prices.xlsx
  
  3. Run this script:
     python 04_scripts/prepare_international_prices.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "03_data" / "raw"
INTERIM = REPO / "03_data" / "interim"
INTERIM.mkdir(exist_ok=True)


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def check_domestic_prices():
    fp = DATA / "bloomberg_prices_monthly.csv"
    if fp.exists():
        df = pd.read_csv(fp)
        log(f"Domestic prices: {len(df)} rows, columns: {list(df.columns)}")
        log(f"Date range: {df.iloc[:, 0].min()} to {df.iloc[:, 0].max()}")
        return df
    else:
        log(f"ERROR: {fp} not found")
        return None


def load_manual_data():
    xlsx = DATA / "international_prices.xlsx"
    csv = DATA / "international_prices.csv"

    if xlsx.exists():
        log(f"Loading {xlsx.name}...")
        xl = pd.ExcelFile(xlsx)
        log(f"  Sheets: {xl.sheet_names}")
        for sheet in xl.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet)
            log(f"  {sheet}: {len(df)} rows, columns: {list(df.columns)}")
        return True
    elif csv.exists():
        log(f"Loading {csv.name}...")
        df = pd.read_csv(csv)
        log(f"  {len(df)} rows, columns: {list(df.columns)}")
        return True
    else:
        log("No international price file found.")
        log(f"  Expected: {xlsx}")
        log(f"  Or:       {csv}")
        return False


def create_price_template():
    template = pd.DataFrame(
        {
            "year": [y for y in range(2019, 2025) for _ in range(12)],
            "month": [m for _ in range(6) for m in range(1, 13)],
        }
    )
    template["period"] = template["year"].astype(str) + template["month"].astype(str).str.zfill(2)
    columns = [
        "ga_mb_ga_0001_rotterdam_usd_kg",
        "ga_mb_ga_0002_china_cny_kg",
        "ge_metal_mb_ger_0003_rotterdam_usd_kg",
        "ge_metal_mb_ger_0004_china_cny_kg",
        "geo2_mb_ger_0005_rotterdam_usd_kg",
        "geo2_mb_ger_0006_china_cny_kg",
        "indium_mb_in_0002_rotterdam_usd_kg",
        "indium_mb_in_0003_china_cny_kg",
        "graphite_mb_gra_0042_94_minus100_fob_china_usd_ton",
        "graphite_platts_bataa00_94_95_fob_china_usd_ton",
        "graphite_platts_batba00_94_95_cif_ne_asia_usd_ton",
        "spherical_graphite_mb_gra_0036_fob_china_usd_ton",
        "spherical_graphite_platts_batab00_fob_china_usd_ton",
        "spherical_graphite_platts_batbb00_cif_ne_asia_usd_ton",
        "antimony_metal_mb_sb_0003_ddp_china_cny_ton",
        "antimony_metal_mb_sb_0002_rotterdam_usd_ton",
        "antimony_metal_mb_sb_0001_low_bi_rotterdam_usd_ton",
        "antimony_metal_9965_exworks_china_cny_ton",
        "antimony_metal_9965_fob_china_usd_ton",
        "antimony_trioxide_995_delivered_china_cny_ton",
        "antimony_trioxide_995_fob_china_usd_ton",
        "antimony_trioxide_995_rotterdam_eur_kg",
        "antimony_concentrate_50_delivered_china_cny_contained_ton",
        "cny_per_usd",
        "eur_per_usd",
    ]
    for column in columns:
        template[column] = np.nan

    out = DATA / "international_prices_TEMPLATE.csv"
    template.to_csv(out, index=False)
    log(f"Template saved to {out}")
    log("Fill in the price columns and rename to international_prices.csv")
    return template


def build_price_did():
    domestic = DATA / "bloomberg_prices_monthly.csv"
    international = DATA / "international_prices.csv"

    if not domestic.exists():
        log("ERROR: Domestic prices not found")
        return
    if not international.exists():
        log("ERROR: International prices not found. Use the template first.")
        return

    dom = pd.read_csv(domestic)
    intl = pd.read_csv(international)

    log(f"Domestic: {len(dom)} rows")
    log(f"International: {len(intl)} rows")

    log("\nPrice DiD design:")
    log("  D_it = (price_domestic - price_international) for mineral i, month t")
    log("  Treatment = 1 if month >= effective date")
    log("  Graphite: expect price gap to narrow (domestic falls, international rises)")
    log("  Ga/Ge: expect no significant change (controls not binding)")


def main():
    log("=" * 60)
    log("INTERNATIONAL PRICES — SETUP AND IMPORT")
    log("=" * 60)

    log("\n--- Domestic price check ---")
    check_domestic_prices()

    log("\n--- International price check ---")
    found = load_manual_data()

    if not found:
        log("\nCreating template for manual data entry...")
        create_price_template()

        log("\n" + "!" * 60)
        log("MANUAL ACTION REQUIRED")
        log("!" * 60)
        log("")
        log("To get international prices:")
        log("")
        log("1. Bloomberg Terminal (ZJU):")
        log("   Use the exact identifiers and specifications in:")
        log(f"   {REPO / '03_data' / 'DOWNLOAD_CHECKLIST.md'}")
        log("")
        log("2. Export original histories and metadata; do not interpolate raw data.")
        log("")
        log("3. Save data to:")
        log(f"   {DATA / 'international_prices.csv'}")
        log("   or")
        log(f"   {DATA / 'international_prices.xlsx'}")
        log("")
        log("4. Re-run this script to build the price DiD dataset")
    else:
        build_price_did()


if __name__ == "__main__":
    main()
