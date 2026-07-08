"""
Analysis v2 — Run with available data (HS 811292 + 282560 + China exports + GeoDist).

Produces:
1. Panel dataset with China share, treatment dummies, gravity controls
2. Shift-share DiD regression (Ga/Ge episode)
3. Event study on China export volumes
4. Summary statistics tables
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

DATA_DIR = Path("<repo-root>/03_data/raw")
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

TREATMENT = {
    "ga_ge": {
        "hs": ["811292", "282560"],
        "effective": "2023-08-01",
        "label": "Ga/Ge controls",
    },
}

HS_LABELS = {
    "811292": "Ga+Ge+In+V+Nb (HS811292)",
    "282560": "GeO2+ZrO2 (HS282560)",
}


def load_imports(hs):
    f = DATA_DIR / f"comtrade_{hs}_imports.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f)
    df["period"] = df["period"].astype(str)
    df = df.groupby(["reporterCode", "partnerCode", "period"]).agg(
        {"primaryValue": "sum"}
    ).reset_index()
    df["hs6"] = hs
    return df


def load_exports(hs):
    f = DATA_DIR / f"comtrade_{hs}_china_exports.csv"
    if not f.exists():
        return None
    return pd.read_csv(f)


def load_geodist():
    f = DATA_DIR / "geodist" / "col_regfile09.dta"
    if not f.exists():
        return None
    gd = pd.read_stata(f)
    # Keep only country-pair characteristics (time-invariant or take latest year)
    gd_latest = gd.sort_values("year").groupby(["iso_o", "iso_d"]).last().reset_index()
    return gd_latest


def build_panel():
    dfs = []
    for hs in ["811292", "282560"]:
        df = load_imports(hs)
        if df is not None:
            dfs.append(df)
    
    if not dfs:
        print("No import data available")
        return None
    
    df = pd.concat(dfs, ignore_index=True)
    
    # Parse period
    df["period"] = df["period"].astype(str)
    df["year"] = df["period"].str[:4].astype(int)
    df["month"] = df["period"].str[4:6].astype(int)
    df["date"] = pd.to_datetime(df["period"], format="%Y%m")
    
    # Separate bilateral vs world totals
    bilateral = df[df["partnerCode"] != 0].copy()
    world = df[df["partnerCode"] == 0][["reporterCode", "period", "hs6", "primaryValue"]].copy()
    world = world.rename(columns={"primaryValue": "world_imports"})
    
    china = bilateral[bilateral["partnerCode"] == 156][["reporterCode", "period", "hs6", "primaryValue"]].copy()
    china = china.rename(columns={"primaryValue": "china_imports"})
    
    panel = world.merge(china, on=["reporterCode", "period", "hs6"], how="left")
    panel["china_imports"] = panel["china_imports"].fillna(0)
    panel["china_share"] = np.where(
        panel["world_imports"] > 0,
        panel["china_imports"] / panel["world_imports"],
        0
    )
    
    panel["ln_world_imports"] = np.log(1 + panel["world_imports"])
    panel["ln_china_imports"] = np.log(1 + panel["china_imports"])
    
    # Treatment timing
    treat_date = pd.to_datetime("2023-08-01")
    panel["date"] = pd.to_datetime(panel["period"], format="%Y%m")
    panel["post"] = (panel["date"] >= treat_date).astype(int)
    
    # Pre-treatment China share (Jan 2019 - Jul 2023)
    pre = panel[panel["date"] < treat_date].copy()
    pre_share = pre.groupby(["reporterCode", "hs6"]).agg(
        pre_china_share=("china_share", "mean"),
        pre_china_imports=("china_imports", "mean"),
        pre_world_imports=("world_imports", "mean"),
    ).reset_index()
    
    panel = panel.merge(pre_share, on=["reporterCode", "hs6"], how="left")
    
    # Shift-share instrument: pre_share × post
    panel["bartik"] = panel["pre_china_share"] * panel["post"]
    
    # Relative time to treatment (in months)
    panel["rel_time"] = (panel["date"] - treat_date) / pd.Timedelta(days=30.44)
    panel["rel_time_int"] = panel["rel_time"].round().astype(int)
    
    # Reporter-period and unit fixed effects IDs
    panel["reporterCode"] = panel["reporterCode"].astype(str)
    panel["reporter_id"] = panel["reporterCode"].astype("category").cat.codes
    panel["period_id"] = panel["period"].astype("category").cat.codes
    panel["unit_id"] = (panel["reporterCode"] + "_" + panel["hs6"]).astype("category").cat.codes
    
    return panel


def build_exports_panel():
    dfs = []
    for hs in ["811292", "282560", "2504", "3801", "8110", "2617"]:
        df = load_exports(hs)
        if df is not None:
            df["hs6"] = hs
            dfs.append(df)
    
    if not dfs:
        return None
    
    df = pd.concat(dfs, ignore_index=True)
    df["period"] = df["period"].astype(str)
    df["date"] = pd.to_datetime(df["period"], format="%Y%m")
    df["ln_exports"] = np.log(1 + df["primaryValue"])
    
    return df


def summary_stats(panel):
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\nPanel dimensions: {panel.shape[0]:,} observations")
    print(f"  Reporters: {panel['reporterCode'].nunique()}")
    print(f"  HS codes: {panel['hs6'].nunique()}")
    print(f"  Periods: {panel['period'].nunique()}")
    print(f"  Date range: {panel['date'].min()} to {panel['date'].max()}")
    
    print(f"\n--- By HS code ---")
    for hs in panel["hs6"].unique():
        sub = panel[panel["hs6"] == hs]
        china = sub[sub["china_imports"] > 0]
        print(f"\n  {HS_LABELS.get(hs, hs)}:")
        print(f"    Total obs: {len(sub):,}")
        print(f"    Reporters with China imports: {china['reporterCode'].nunique()}")
        print(f"    Total imports from world: ${sub['world_imports'].sum():,.0f}")
        print(f"    Total imports from China: ${sub['china_imports'].sum():,.0f}")
        print(f"    Avg China share: {sub[sub['world_imports']>0]['china_share'].mean():.3f}")
    
    print(f"\n--- Pre/Post treatment comparison (Ga/Ge, Aug 2023) ---")
    for hs in ["811292", "282560"]:
        sub = panel[panel["hs6"] == hs]
        pre = sub[sub["post"] == 0]
        post = sub[sub["post"] == 1]
        if len(pre) > 0 and len(post) > 0:
            print(f"\n  {HS_LABELS.get(hs, hs)}:")
            print(f"    Pre  (thru Jul 2023): avg China imports ${pre['china_imports'].mean():,.0f}/mo, avg share {pre[pre['world_imports']>0]['china_share'].mean():.3f}")
            print(f"    Post (Aug 2023+):     avg China imports ${post['china_imports'].mean():,.0f}/mo, avg share {post[post['world_imports']>0]['china_share'].mean():.3f}")
            pre_total = pre.groupby("period")["china_imports"].sum().mean()
            post_total = post.groupby("period")["china_imports"].sum().mean()
            print(f"    Pre total/month:  ${pre_total:,.0f}")
            print(f"    Post total/month: ${post_total:,.0f}")
            print(f"    Change: {(post_total/pre_total - 1)*100:+.1f}%")


def export_china_timeseries(exports):
    print("\n" + "="*60)
    print("CHINA EXPORT VOLUME TRENDS")
    print("="*60)
    
    for hs in exports["hs6"].unique():
        sub = exports[exports["hs6"] == hs].sort_values("date")
        label = HS_LABELS.get(hs, hs)
        
        treat_date = pd.to_datetime("2023-08-01")
        pre = sub[sub["date"] < treat_date]["primaryValue"]
        post = sub[sub["date"] >= treat_date]["primaryValue"]
        
        print(f"\n  {label}:")
        print(f"    Pre-treatment avg:  ${pre.mean():,.0f}/mo")
        print(f"    Post-treatment avg: ${post.mean():,.0f}/mo")
        if pre.mean() > 0:
            print(f"    Change: {(post.mean()/pre.mean() - 1)*100:+.1f}%")
    
    # Save for plotting
    pivot = exports.pivot_table(index="date", columns="hs6", values="primaryValue", aggfunc="sum")
    pivot.to_csv(RESULTS_DIR / "china_exports_timeseries.csv")
    print(f"\n  Saved time series to results/china_exports_timeseries.csv")


def save_panel(panel):
    panel.to_csv(RESULTS_DIR / "panel_gage.csv", index=False)
    print(f"\nPanel saved: {RESULTS_DIR / 'panel_gage.csv'} ({len(panel):,} rows)")


if __name__ == "__main__":
    print("Building panel from HS 811292 + 282560...")
    panel = build_panel()
    
    if panel is not None:
        summary_stats(panel)
        save_panel(panel)
    
    print("\nBuilding China exports panel...")
    exports = build_exports_panel()
    
    if exports is not None:
        export_china_timeseries(exports)
    
    print("\n" + "="*60)
    print("NEXT: Run regressions in Stata/R/Python")
    print(f"  Panel: {RESULTS_DIR / 'panel_gage.csv'}")
    print(f"  Exports: {RESULTS_DIR / 'china_exports_timeseries.csv'}")
    print("="*60)
