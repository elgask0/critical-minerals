"""
Build full analysis panel: all treated + placebo HS codes + GeoDist.
Merge, clean, aggregate, then export for regression.
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path("<repo-root>/03_data/raw")
GEO = DATA / "geodist" / "col_regfile09.dta"

# —— HS codes ——
TREATED = {
    "2504": "Natural graphite",
    "811292": "Ga, Ge, etc. (bundle)",
    "282560": "GeO2 (+ ZrO2)",
}
INTERNAL_PLACEBO = {"3801": "Artificial graphite"}  # same chemical sector
EXTERNAL_PLACEBOS = {
    "2501": "Salt (chapter 25)",
    "2818": "Alumina (chapter 28)",
}
ALL_HS = {**TREATED, **INTERNAL_PLACEBO, **EXTERNAL_PLACEBOS}

PERIODS = [f"{y}{m:02d}" for y in range(2019,2025) for m in range(1,13)]
TREATMENT_MONTH = 12  # December 2023
PERIOD_ORDER = {p: i for i, p in enumerate(PERIODS)}
POST = {p: i >= PERIOD_ORDER[f"2023{TREATMENT_MONTH:02d}"] for p, i in PERIOD_ORDER.items()}

def load_imports(hs):
    fp = DATA / f"comtrade_{hs}_imports.csv"
    if not fp.exists():
        print(f"  MISSING: {hs}")
        return None
    df = pd.read_csv(fp, low_memory=False)
    if len(df) == 0:
        print(f"  EMPTY: {hs}")
        return None
    
    # Normalize column names
    col_map = {
        'reporterCode': 'reporterCode',
        'reporterDesc': 'reporterDesc',
        'partnerCode': 'partnerCode',
        'partnerDesc': 'partnerDesc',
        'cmdCode': 'cmdCode',
        'cmdDesc': 'cmdDesc',
        'period': 'period',
        'periodDesc': 'periodDesc',
        'primaryValue': 'primaryValue',
        'netWgt': 'netWgt',
        'tradeQuantity': 'tradeQuantity',
        'tradeQuantityUnit': 'tradeQuantityUnit',
        'qtyUnitCode': 'qtyUnitCode',
        'rgDesc': 'rgDesc',
        'rtCode': 'rtCode',
        'rtTitle': 'rtTitle',
        'estCode': 'estCode',
        'ageCode': 'ageCode',
    }
    # Only keep columns that exist
    keep = [v for v in col_map.values() if v in df.columns]
    df = df[keep].copy()
    if 'primaryValue' not in df.columns and 'tradeValue' in df.columns:
        df = df.rename(columns={'tradeValue': 'primaryValue'})
    
    # Partner = China (156) only
    if 'partnerCode' in df.columns:
        df = df[df['partnerCode'] == 156].copy()
    elif 'partnerDesc' in df.columns:
        df = df[df['partnerDesc'].str.contains('China', case=False, na=False)].copy()
    
    if len(df) == 0:
        print(f"  No China partner data for {hs}")
        return None
    
    df['hs'] = hs
    df['period'] = df['period'].astype(str)
    df['primaryValue'] = pd.to_numeric(df['primaryValue'], errors='coerce').fillna(0)
    
    # Aggregate customs codes
    agg = df.groupby(['reporterCode', 'period'], as_index=False)['primaryValue'].sum()
    agg.rename(columns={'primaryValue': f'imports_{hs}'}, inplace=True)
    
    # Reporter description
    rep_desc = df[['reporterCode', 'reporterDesc']].drop_duplicates()
    agg = agg.merge(rep_desc, on='reporterCode', how='left')
    
    total = agg[f'imports_{hs}'].sum()
    print(f"  {hs} ({ALL_HS[hs]}): {len(agg)} obs, ${total/1e6:.1f}M total")
    return agg

def main():
    print("Loading all HS codes...")
    panels = {}
    for hs in ALL_HS:
        d = load_imports(hs)
        if d is not None:
            panels[hs] = d
    
    if len(panels) == 0:
        print("NO DATA LOADED")
        return
    
    # Merge all into wide panel
    print("\nMerging into panel...")
    first_hs = list(panels.keys())[0]
    panel = panels[first_hs][['period', 'reporterCode', 'reporterDesc', f'imports_{first_hs}']].copy()
    
    for hs in list(panels.keys())[1:]:
        panel = panel.merge(
            panels[hs][['period', 'reporterCode', f'imports_{hs}']],
            on=['period', 'reporterCode'],
            how='outer'
        )
    
    # Fill missing imports with 0
    for hs in ALL_HS:
        col = f'imports_{hs}'
        if col in panel.columns:
            panel[col] = panel[col].fillna(0)
    
    print(f"Panel: {len(panel):,} rows, {panel['reporterCode'].nunique()} reporters, {panel['period'].nunique()} periods")
    
    # Add period features
    panel['period_num'] = panel['period'].map(PERIOD_ORDER)
    panel['year'] = panel['period'].str[:4].astype(int)
    panel['month'] = panel['period'].str[4:6].astype(int)
    panel['post'] = (panel['period_num'] >= PERIOD_ORDER["202312"]).astype(int)
    panel['period_float'] = panel['period_num'] - PERIOD_ORDER["202312"]  # 0 at treatment
    
    # China total exports for shift-share (from China export data)
    print("\nLoading China export data for shift-share weights...")
    china_exp = {}
    for hs in ["2504", "811292", "282560", "3801"]:
        fp = DATA / f"comtrade_{hs}_china_exports.csv"
        if fp.exists():
            d = pd.read_csv(fp)
            if 'primaryValue' in d.columns:
                d['primaryValue'] = pd.to_numeric(d['primaryValue'], errors='coerce').fillna(0)
                d['period'] = d['period'].astype(str)
                china_exp[hs] = d.groupby('period')['primaryValue'].sum().to_dict()
    
    # Shift-share weights: reporter's China share = reporter imports / world imports from China
    # World imports from China = sum across all reporters
    print("\nComputing shift-share weights (pre-treatment averages)...")
    for hs in TREATED:
        col = f'imports_{hs}'
        if col not in panel.columns:
            continue
        
        # Total world imports from China (approximated by sum across reporters)
        pre_mask = panel['period_num'] < PERIOD_ORDER["202312"]
        world_china = panel[pre_mask].groupby('period')[col].sum()
        world_china_avg = world_china.mean()
        
        # Reporter-specific China share (pre-treatment average)
        rep_share = panel[pre_mask].groupby('reporterCode')[col].sum() / (world_china_avg * pre_mask.sum() / 12)
        # Cap at 1
        rep_share = rep_share.clip(upper=1.0)
        
        panel[f'share_china_{hs}'] = panel['reporterCode'].map(rep_share).fillna(0)
        print(f"  {hs}: mean share = {rep_share.mean():.3f}, median = {rep_share.median():.3f}, "
              f"N > 0 = {(rep_share > 0.01).sum()}/{len(rep_share)}")
    
    # Treated HS flag for triple-diff
    panel['treated'] = 0
    for hs in TREATED:
        col = f'imports_{hs}'
        if col in panel.columns:
            has_imports = panel[col] > 0
            panel.loc[has_imports, 'treated'] = 1
    
    # Log-transformed DVs
    for hs in ALL_HS:
        col = f'imports_{hs}'
        if col in panel.columns:
            panel[f'ln_{col}'] = np.log(1 + panel[col])
    
    # Save
    out = DATA / "results" / "full_panel.csv"
    panel.to_csv(out, index=False)
    print(f"\nSaved: {out}")
    print(f"Panel shape: {panel.shape}")
    
    # Quick summary stats
    print("\n=== DATA COMPLETENESS ===")
    for hs in ALL_HS:
        col = f'imports_{hs}'
        if col in panel.columns:
            nz = (panel[col] > 0).sum()
            total = len(panel)
            n_reps = panel.loc[panel[col] > 0, 'reporterCode'].nunique()
            print(f"  {hs} {ALL_HS[hs]:30s}: {nz:>5}/{total} nonzero, {n_reps:>2} reporters")

if __name__ == "__main__":
    main()
