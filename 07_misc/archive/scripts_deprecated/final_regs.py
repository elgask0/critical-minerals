"""
Final regressions: triple-diff, shift-share DiD, GeoDist robustness.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

DATA = Path("<repo-root>/03_data/raw")
RES = DATA / "results"
panel = pd.read_csv(RES / "full_panel.csv")

PERIODS = [f"{y}{m:02d}" for y in range(2019,2025) for m in range(1,13)]
PERIOD_ORDER = {p: i for i, p in enumerate(PERIODS)}
TREAT_PERIOD = PERIOD_ORDER["202312"]

panel['period'] = panel['period'].astype(str)
panel['period_num'] = panel['period'].map(PERIOD_ORDER)
panel['post'] = (panel['period_num'] >= TREAT_PERIOD).astype(int)

def its(hs, label, dv='ln_imports'):
    """Interrupted time series on China exports."""
    fp = DATA / f"comtrade_{hs}_china_exports.csv"
    if not fp.exists():
        print(f"  Skipping ITS for {hs}: no China export data")
        return
    ce = pd.read_csv(fp)
    ce['period'] = ce['period'].astype(str)
    ce['primaryValue'] = pd.to_numeric(ce['primaryValue'], errors='coerce').fillna(0)
    ts = ce.groupby('period')['primaryValue'].sum().reset_index()
    ts['period_num'] = ts['period'].map(PERIOD_ORDER)
    ts['post'] = (ts['period_num'] >= TREAT_PERIOD).astype(int)
    ts['ln_val'] = np.log(1 + ts['primaryValue'])
    ts['t'] = ts['period_num'] - TREAT_PERIOD
    
    X = sm.add_constant(ts[['t', 'post']])
    m = sm.OLS(ts['ln_val'], X).fit(cov_type='HC1')
    print(f"\n=== ITS: {hs} ({label}) ===")
    print(f"  N={len(ts)}, R²={m.rsquared:.3f}")
    print(f"  Pre-trend (t):    {m.params['t']:.4f} (p={m.pvalues['t']:.4f})")
    print(f"  Level shift (post): {m.params['post']:.4f} (p={m.pvalues['post']:.4f})")

def shift_share_did(hs, label):
    """Shift-share DiD on bilateral panel."""
    dv = f'imports_{hs}'
    if dv not in panel.columns:
        print(f"  Skipping DiD for {hs}: not in panel")
        return
    
    # Pre-treatment share of China's exports going to each reporter
    pre = panel[panel['period_num'] < TREAT_PERIOD]
    rep_total_pre = pre.groupby('reporterCode')[dv].sum()
    world_total_pre = rep_total_pre.sum()
    share = (rep_total_pre / world_total_pre).to_dict()
    panel[f'share_{hs}'] = panel['reporterCode'].map(share).fillna(0)
    
    sub = panel[['period_num', 'post', 'reporterCode', dv, f'share_{hs}']].dropna().copy()
    sub['ln_dv'] = np.log(1 + sub[dv])
    sub['treat'] = sub['post'] * sub[f'share_{hs}']
    
    # Reporter + Period one-way FE (reporter demean)
    sub['ln_dv'] = sub['ln_dv'] - sub.groupby('reporterCode')['ln_dv'].transform('mean')
    sub['treat'] = sub['treat'] - sub.groupby('reporterCode')['treat'].transform('mean')
    sub['post'] = sub['post'] - sub.groupby('reporterCode')['post'].transform('mean')
    sub['share'] = sub[f'share_{hs}'] - sub.groupby('reporterCode')[f'share_{hs}'].transform('mean')
    
    m_dd = sm.OLS(sub['ln_dv'], sm.add_constant(sub[['treat', 'post', 'share']])).fit(cov_type='HC1')
    
    print(f"\n=== Shift-Share DiD: {hs} ({label}) ===")
    print(f"  N={len(sub)}, Reporters={sub['reporterCode'].nunique()}, Periods={sub['period_num'].nunique()}")
    print(f"  Mean share={sub[f'share_{hs}'].mean():.4f}, N>0={ (sub[f'share_{hs}']>0).sum()}")
    print(f"  β (post × share) = {m_dd.params['treat']:.4f} (p={m_dd.pvalues['treat']:.4f})")
    print(f"  R²={m_dd.rsquared:.3f}")
    
    # Placebo tests
    for fake_t in ["202201", "202206", "202101"]:
        fake_num = PERIOD_ORDER[fake_t]
        sub2 = sub[sub['period_num'] < TREAT_PERIOD].copy()
        sub2['post_fake'] = (sub2['period_num'] >= fake_num).astype(int)
        sub2['treat_fake'] = sub2['post_fake'] * sub2[f'share_{hs}']
        if len(sub2) < 500:
            print(f"  Placebo {fake_t}: too few obs ({len(sub2)})")
            continue
        sub2['ln_dv'] = sub2['ln_dv'] - sub2.groupby('reporterCode')['ln_dv'].transform('mean')
        sub2['treat_fake'] = sub2['treat_fake'] - sub2.groupby('reporterCode')['treat_fake'].transform('mean')
        sub2['post_fake'] = sub2['post_fake'] - sub2.groupby('reporterCode')['post_fake'].transform('mean')
        sub2['share'] = sub2[f'share_{hs}'] - sub2.groupby('reporterCode')[f'share_{hs}'].transform('mean')
        m2 = sm.OLS(sub2['ln_dv'], sm.add_constant(sub2[['treat_fake', 'post_fake', 'share']])).fit(cov_type='HC1')
        print(f"  Placebo {fake_t}: β={m2.params['treat_fake']:.4f} (p={m2.pvalues['treat_fake']:.4f})")

def triple_diff():
    """Triple-diff: treated × post with placebo HS codes as control."""
    print("\n=== TRIPLE-DIFF: Pooled Treated + Placebos ===")
    
    # Melt to long by HS code
    treated_hs = ["2504", "811292", "282560"]
    placebo_hs = ["3801", "2501", "2818"]
    all_hs = treated_hs + placebo_hs
    
    long = panel.melt(
        id_vars=['period', 'period_num', 'post', 'reporterCode', 'reporterDesc'],
        value_vars=[f'imports_{h}' for h in all_hs],
        var_name='hs_col', value_name='imports'
    )
    long['hs'] = long['hs_col'].str.replace('imports_', '')
    long['treated'] = long['hs'].isin(treated_hs).astype(int)
    long['ln_imports'] = np.log(1 + long['imports'])
    
    print(f"  N={len(long):,}, Reporters={long['reporterCode'].nunique()}, HS codes={long['hs'].nunique()}")
    print(f"  Treated obs: {(long['treated']==1).sum():,}, Control: {(long['treated']==0).sum():,}")
    
    # Triple-diff: properly with reporter + period + HS FE
    long['treated_post'] = long['treated'] * long['post']
    
    # Step 1: absorb reporter FE (within-report demeaning)
    long['Y'] = long['ln_imports'] - long.groupby('reporterCode')['ln_imports'].transform('mean')
    long['X'] = long['treated_post'] - long.groupby('reporterCode')['treated_post'].transform('mean')
    
    # Step 2: absorb period FE + HS FE
    fe = pd.concat([
        pd.get_dummies(long['period_num'], prefix='p', drop_first=True).astype(float),
        pd.get_dummies(long['hs'], prefix='h', drop_first=True).astype(float),
    ], axis=1)
    m_fe_y = sm.OLS(long['Y'], sm.add_constant(fe)).fit()
    m_fe_x = sm.OLS(long['X'], sm.add_constant(fe)).fit()
    m = sm.OLS(m_fe_y.resid, m_fe_x.resid).fit(cov_type='HC1')
    print(f"\n  Model 1 (reporter + period + HS FE — pooled triple-diff):")
    print(f"  β (treated × post) = {m.params.iloc[0]:.4f} (p={m.pvalues.iloc[0]:.4f})")
    print(f"  R²={m.rsquared:.3f}")
    
    # Model 2: Individual treated HS × Post (reporter + period + HS FE)
    for hs in treated_hs:
        sub = long[long['hs'].isin([hs] + placebo_hs)].copy()
        sub['is_treated'] = (sub['hs'] == hs).astype(int)
        sub['treated_post2'] = sub['is_treated'] * sub['post']
        sub['Y'] = sub['ln_imports'] - sub.groupby('reporterCode')['ln_imports'].transform('mean')
        sub['X'] = sub['treated_post2'] - sub.groupby('reporterCode')['treated_post2'].transform('mean')
        d_period = pd.get_dummies(sub['period_num'], prefix='p', drop_first=True)
        d_hs = pd.get_dummies(sub['hs'], prefix='h', drop_first=True)
        fe = pd.concat([d_period, d_hs], axis=1).astype(float)
        m_fe_y = sm.OLS(sub['Y'], sm.add_constant(fe)).fit()
        m_fe_x = sm.OLS(sub['X'], sm.add_constant(fe)).fit()
        m2 = sm.OLS(m_fe_y.resid, m_fe_x.resid).fit(cov_type='HC1')
        print(f"  {hs}: β (× post) = {m2.params.iloc[0]:.4f} (p={m2.pvalues.iloc[0]:.4f})")

def geodist_check():
    """GeoDist: distance × post × treated interaction."""
    fp = DATA / "geodist" / "col_regfile09.dta"
    if not fp.exists():
        print("\n=== GeoDist: FILE NOT FOUND ===")
        return
    geo = pd.read_stata(fp)
    print(f"\n=== GeoDist ===")
    print(f"  GeoDist: {len(geo):,} rows, cols={list(geo.columns)}")
    
    # Merge with panel: reporterCode = iso3 numeric
    # geo has: iso_o (origin = China 156), iso_d (dest), dist (km)
    # We need dist between China and each reporter
    geo_china = geo[geo['iso_o'] == 156].copy()
    geo_china = geo_china[['iso_d', 'distw']].drop_duplicates()
    geo_china.columns = ['reporterCode', 'dist_km']
    
    # Merge
    merged = panel.merge(geo_china, on='reporterCode', how='left')
    merged['ln_dist'] = np.log(merged['dist_km'])
    print(f"  Matched: {merged['dist_km'].notna().sum()}/{len(merged)}")
    
    # Triple-diff with distance interaction
    treated_hs = ["2504", "811292", "282560"]
    placebo_hs = ["3801", "2501", "2818"]
    all_hs = treated_hs + placebo_hs
    
    long = merged.melt(
        id_vars=['period', 'period_num', 'post', 'reporterCode', 'reporterDesc', 'dist_km', 'ln_dist'],
        value_vars=[f'imports_{h}' for h in all_hs],
        var_name='hs_col', value_name='imports'
    )
    long['hs'] = long['hs_col'].str.replace('imports_', '')
    long['treated'] = long['hs'].isin(treated_hs).astype(int)
    long['ln_imports'] = np.log(1 + long['imports'])
    long['treated_post'] = long['treated'] * long['post']
    
    valid = long.dropna(subset=['ln_dist']).copy()
    valid['ln_dist'] = valid['ln_dist'].fillna(valid['ln_dist'].mean())
    valid['treated_post'] = valid['treated'] * valid['post']
    valid['dist_x_treat'] = valid['ln_dist'] * valid['treated']
    valid['dist_x_post'] = valid['ln_dist'] * valid['post']
    valid['dist_x_treat_post'] = valid['ln_dist'] * valid['treated'] * valid['post']
    
    # FWL: reporter + period + HS FE
    valid['Y'] = valid['ln_imports'] - valid.groupby('reporterCode')['ln_imports'].transform('mean')
    for c in ['treated_post', 'dist_x_treat', 'dist_x_post', 'dist_x_treat_post']:
        valid[c] = valid[c] - valid.groupby('reporterCode')[c].transform('mean')
    
    fe = pd.concat([
        pd.get_dummies(valid['period_num'], prefix='p', drop_first=True).astype(float),
        pd.get_dummies(valid['hs'], prefix='h', drop_first=True).astype(float),
    ], axis=1)
    fe = sm.add_constant(fe)
    
    resid_y = sm.OLS(valid['Y'], fe).fit().resid
    X_cols = ['treated_post', 'dist_x_treat', 'dist_x_post', 'dist_x_treat_post']
    resid_X = pd.DataFrame({c: sm.OLS(valid[c], fe).fit().resid for c in X_cols})
    m = sm.OLS(resid_y, resid_X).fit(cov_type='HC1')
    print(f"  Triple interaction (dist × post × treated):")
    print(f"  β = {m.params['dist_x_treat_post']:.4f} (p={m.pvalues['dist_x_treat_post']:.4f})")
    print(f"  Treated × post (baseline): β = {m.params['treated_post']:.4f} (p={m.pvalues['treated_post']:.4f})")
    print(f"  R²={m.rsquared:.3f}, N={len(valid):,}")

if __name__ == "__main__":
    print("=" * 60)
    print("FINAL REGRESSIONS — Differential Effectiveness of China's Export Controls")
    print("=" * 60)
    
    # 1. ITS
    print("\n--- 1. INTERRUPTED TIME SERIES ---")
    its("2504", "Natural graphite")
    its("811292", "Ga/Ge bundle")
    its("282560", "GeO2")
    its("3801", "Artificial graphite (internal placebo)")
    
    # 2. Shift-share DiD
    print("\n--- 2. SHIFT-SHARE DiD ---")
    for hs, label in [("2504", "Natural graphite"), ("811292", "Ga/Ge bundle"), ("282560", "GeO2")]:
        shift_share_did(hs, label)
    
    # 3. Triple-diff
    print("\n--- 3. TRIPLE-DIFF ---")
    triple_diff()
    
    # 4. GeoDist
    print("\n--- 4. GEODIST ROBUSTNESS ---")
    geodist_check()
    
    print("\n" + "=" * 60)
    print("DONE")
