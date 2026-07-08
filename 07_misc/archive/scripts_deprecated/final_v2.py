"""
FINAL ANALYSIS v2 — with corrections:
1. 3801 excluded from triple-diff (partially treated, not clean placebo)
2. Period FE added to shift-share DiD
3. Clean placebos: 2501, 2818 [, 8111 if available]
"""

import pandas as pd, numpy as np, statsmodels.api as sm, warnings, time
from pathlib import Path
warnings.filterwarnings('ignore')

DATA = Path("<repo-root>/03_data/raw")
PERIODS = [f"{y}{m:02d}" for y in range(2019,2025) for m in range(1,13)]
PMAP = {p:i for i,p in enumerate(PERIODS)}

TREAT = {"811292": "202308", "282560": "202308", "2504": "202312"}
TREAT_N = {h:PMAP[d] for h,d in TREAT.items()}

TREATED = {"2504": "Natural graphite", "811292": "Ga/Ge bundle", "282560": "GeO2"}
# 3801 EXCLUDED from placebos — it's partially treated
PLACEBOS = {"2501": "Salt", "2818": "Alumina", "8111": "Manganese"}
ALL_HS = {**TREATED, **PLACEBOS}

# ============================================================
# 1. LOAD DATA
# ============================================================
print("="*70)
print("LOADING DATA")
print("="*70)

def load(hs):
    fp = DATA / f"comtrade_{hs}_imports.csv"
    if not fp.exists(): return None
    
    df = pd.read_csv(fp, low_memory=False)
    df['primaryValue'] = pd.to_numeric(df['primaryValue'], errors='coerce').fillna(0)
    df['period'] = df['period'].astype(str)
    df['reporterCode'] = pd.to_numeric(df['reporterCode'], errors='coerce')
    
    # Total imports (all partners)
    total = df.groupby(['reporterCode','period'])['primaryValue'].sum().reset_index()
    total.columns = ['reporterCode','period','total_imports']
    
    # China imports (partner=156)
    china = df[df['partnerCode']==156].groupby(['reporterCode','period'])['primaryValue'].sum().reset_index()
    china.columns = ['reporterCode','period','china_imports']
    
    p = total.merge(china, on=['reporterCode','period'], how='left')
    p['china_imports'] = p['china_imports'].fillna(0)
    p['china_share'] = np.where(p['total_imports']>0, p['china_imports']/p['total_imports'], 0)
    p['hs'] = hs
    p['period_num'] = p['period'].map(PMAP)
    print(f"  {hs} {ALL_HS.get(hs,'?'):20s}: {len(p):>5} obs, "
          f"{(p['china_imports']>0).sum():>5} nonzero, "
          f"reporters={p['reporterCode'].nunique()}, "
          f"mean share={p['china_share'].mean():.3f}")
    return p

panels = {}
for hs in ALL_HS:
    p = load(hs)
    if p is not None: panels[hs] = p

# ============================================================
# 2. ITS
# ============================================================
print("\n"+"="*70)
print("1. ITS — China Export Volume")
print("="*70)

for hs, label in {**TREATED, "3801": "Artif graphite (excluded)"}.items():
    fp = DATA / f"comtrade_{hs}_china_exports.csv"
    if not fp.exists():
        print(f"  {hs}: no China export data"); continue
    ce = pd.read_csv(fp)
    ce['period'] = ce['period'].astype(str)
    ce['primaryValue'] = pd.to_numeric(ce['primaryValue'], errors='coerce').fillna(0)
    ts = ce.groupby('period')['primaryValue'].sum().reset_index()
    ts['t'] = ts['period'].map(PMAP) - TREAT_N.get(hs, 59)
    ts['post'] = (ts['t'] >= 0).astype(int)
    ts['ln_val'] = np.log(1 + ts['primaryValue'])
    
    m = sm.OLS(ts['ln_val'], sm.add_constant(ts[['t','post']])).fit(cov_type='HC1')
    pct = (np.exp(m.params['post'])-1)*100
    print(f"  {hs} ({label:25s}): pre-trend={m.params['t']:+.4f}/mo (p={m.pvalues['t']:.4f}), "
          f"shift={m.params['post']:+.4f} ({pct:+.1f}%, p={m.pvalues['post']:.4f})")

# ============================================================
# 3. SHIFT-SHARE DiD — WITH PERIOD FE
# ============================================================
print("\n"+"="*70)
print("2. SHIFT-SHARE DiD (correct share + PERIOD FE)")
print("="*70)

def ss_did(hs, label):
    p = panels[hs].copy()
    
    # Pre-treatment share
    pre = p[p['period_num'] < TREAT_N.get(hs, 59)]
    pre_share = pre.groupby('reporterCode')['china_share'].mean()
    p['share_i'] = p['reporterCode'].map(pre_share).fillna(0)
    p['ln_china'] = np.log(1 + p['china_imports'])
    p['treat'] = p['post'] * p['share_i']  # post is per HS code
    
    # Only reporters with any China imports
    keep = p.groupby('reporterCode')['china_imports'].sum()
    p = p[p['reporterCode'].isin(keep[keep>0].index)].copy()
    
    if len(p) < 200: print(f"  {hs}: too few obs"); return
    
    # METHOD A: one-way reporter FE (original)
    y1 = p['ln_china'] - p.groupby('reporterCode')['ln_china'].transform('mean')
    x1 = p['treat'] - p.groupby('reporterCode')['treat'].transform('mean')
    m1 = sm.OLS(y1, x1).fit(cov_type='HC1')
    b1, p1 = m1.params.iloc[0], m1.pvalues.iloc[0]
    
    # METHOD B: two-way reporter + PERIOD FE
    y2 = p['ln_china'] - p.groupby('reporterCode')['ln_china'].transform('mean') \
                       - p.groupby('period_num')['ln_china'].transform('mean') \
                       + p['ln_china'].mean()
    x2 = p['treat'] - p.groupby('reporterCode')['treat'].transform('mean') \
                     - p.groupby('period_num')['treat'].transform('mean') \
                     + p['treat'].mean()
    m2 = sm.OLS(y2, x2).fit(cov_type='HC1')
    b2, p2 = m2.params.iloc[0], m2.pvalues.iloc[0]
    
    print(f"\n  {hs} ({label})")
    print(f"    N={len(p)}, Reporters={p['reporterCode'].nunique()}, "
          f"Mean share={p['share_i'].mean():.3f}, Max={p['share_i'].max():.3f}")
    print(f"    One-way FE: β={b1:+.4f} (p={p1:.4f})")
    print(f"    Two-way FE (w/period): β={b2:+.4f} (p={p2:.4f})")
    
    # Placebos (with two-way FE)
    for fake in ["202201","202101","202006"]:
        fn = PMAP[fake]
        sub = p[p['period_num'] < TREAT_N.get(hs, 59)].copy()
        sub['post_f'] = (sub['period_num'] >= fn).astype(int)
        sub['treat_f'] = sub['post_f'] * sub['share_i']
        sub['yf'] = sub['ln_china'] - sub.groupby('reporterCode')['ln_china'].transform('mean') \
                                      - sub.groupby('period_num')['ln_china'].transform('mean') \
                                      + sub['ln_china'].mean()
        sub['xf'] = sub['treat_f'] - sub.groupby('reporterCode')['treat_f'].transform('mean') \
                                     - sub.groupby('period_num')['treat_f'].transform('mean') \
                                     + sub['treat_f'].mean()
        mf = sm.OLS(sub['yf'], sub['xf']).fit(cov_type='HC1')
        sig = '❌' if mf.pvalues.iloc[0] < 0.05 else '✅'
        print(f"    Placebo {fake}: β={mf.params.iloc[0]:+.4f} (p={mf.pvalues.iloc[0]:.4f}) {sig}")
    
    return b2, p2  # return two-way estimate

ss_results = {}
for hs, label in TREATED.items():
    if hs in panels:
        r = ss_did(hs, label)
        if r: ss_results[hs] = r

# ============================================================
# 4. TRIPLE-DIFF (3801 EXCLUDED)
# ============================================================
print("\n"+"="*70)
print("3. TRIPLE-DIFF (3801 EXCLUDED — partially treated)")
print("="*70)

available_treated = [h for h in TREATED if h in panels]
available_placebos = [h for h in PLACEBOS if h in panels]
print(f"  Treated: {available_treated}")
print(f"  Placebos: {available_placebos}")

# Build long panel
long = []
for hs in available_treated + available_placebos:
    h = panels[hs]
    sub = h[['period','period_num','reporterCode','china_imports','hs']].copy()
    sub['treated'] = 1 if hs in available_treated else 0
    sub['post'] = (sub['period_num'] >= TREAT_N.get(hs, 999)).astype(int)
    sub['ln_imports'] = np.log(1 + sub['china_imports'])
    long.append(sub)

df = pd.concat(long, ignore_index=True)
df['treated_post'] = df['treated'] * df['post']
print(f"  N={len(df):,}, Reporters={df['reporterCode'].nunique()}, "
      f"HS codes={df['hs'].nunique()}")

# Triple-diff with reporter + period + HS FE (two-way within)
fe_vars = []
for c in ['ln_imports', 'treated_post']:
    dm = df[c] - df.groupby('reporterCode')[c].transform('mean') \
                - df.groupby('period_num')[c].transform('mean') \
                + df[c].mean()
    # Also HS FE
    dm = dm - df.groupby('hs')[c].transform('mean') + dm.mean()
    fe_vars.append(dm)

m = sm.OLS(fe_vars[0], fe_vars[1]).fit(cov_type='HC1')
print(f"  Pooled β={m.params.iloc[0]:+.4f} (p={m.pvalues.iloc[0]:.4f})")

for hs in available_treated:
    sub = df[df['hs'].isin([hs] + available_placebos)].copy()
    sub['tp'] = sub['treated'] * sub['post']
    ys = sub['ln_imports'] - sub.groupby('reporterCode')['ln_imports'].transform('mean') \
                           - sub.groupby('period_num')['ln_imports'].transform('mean') \
                           + sub['ln_imports'].mean()
    ys = ys - sub.groupby('hs')['ln_imports'].transform('mean') + ys.mean()
    xs = sub['tp'] - sub.groupby('reporterCode')['tp'].transform('mean') \
                   - sub.groupby('period_num')['tp'].transform('mean') \
                   + sub['tp'].mean()
    xs = xs - sub.groupby('hs')['tp'].transform('mean') + xs.mean()
    m2 = sm.OLS(ys, xs).fit(cov_type='HC1')
    print(f"  {hs} ({TREATED[hs]}): β={m2.params.iloc[0]:+.4f} (p={m2.pvalues.iloc[0]:.4f})")

# ============================================================
# 5. HIGH-EXPOSURE ANALYSIS
# ============================================================
print("\n"+"="*70)
print("4. HIGH-EXPOSURE REPORTER ANALYSIS")
print("="*70)

for hs, label in TREATED.items():
    if hs not in panels: continue
    p = panels[hs].copy()
    pt = TREAT_N.get(hs, 59)
    pre_m = p[p['period_num'] < pt].groupby('reporterCode')['china_imports'].mean()
    post_m = p[p['period_num'] >= pt].groupby('reporterCode')['china_imports'].mean()
    share = p[p['period_num'] < pt].groupby('reporterCode')['china_share'].mean()
    
    chg = pd.DataFrame({'pre':pre_m,'post':post_m,'share':share}).dropna()
    chg['pct'] = (chg['post']/chg['pre'].replace(0,np.nan)-1)*100
    high = chg[chg['share']>0.3].sort_values('share',ascending=False)
    
    if len(high) > 0:
        print(f"\n  {hs} ({label}) — >30% China share:")
        for _, r in high.iterrows():
            print(f"    Reporter {int(_.real) if hasattr(_,'real') else _}: "
                  f"share={r['share']:.1%}, pre=${r['pre']:,.0f}, "
                  f"post=${r['post']:,.0f}, change={r['pct']:+.1f}%")
        wa = (high['pct']*high['share']).sum()/high['share'].sum()
        print(f"    Weighted avg: {wa:+.1f}%")
    else:
        print(f"\n  {hs} ({label}): no reporters >30%")

# ============================================================
# 6. SUMMARY
# ============================================================
print("\n"+ "="*70)
print("FINAL SUMMARY")
print("="*70)

print("""
ITS (primary):
  Graphite (2504): -48% (p<0.0001) | pre-trend FLAT    | ✅ CAUSAL
  Ga/Ge (811292):  +12% (p=0.68)   | pre-trend +3.7%/mo | ⬆️ Trend continuation
  GeO2 (282560):   -25% (p=0.004)  | pre-trend +0.8%/mo | ⚠️ Weak (pre-trend)

Shift-Share DiD (correct share + period FE):
  Graphite: β = ?  | Placebos: ?
  Ga/Ge:    β = ?  | Placebos: ?
  GeO2:     β = ?  | Placebos: ?

Triple-diff (3801 excluded):
  Pooled: β = ?
  Graphite: β = ?
  Ga/Ge: β = ?
  GeO2: β = ?

High-exposure analysis:
  Graphite: Japan -34%, Korea -46% — CONSISTENT
  Ga/Ge: Korea +123%, HK +167% — NO EFFECT (boom continues)
""")

print("DONE —", time.strftime("%H:%M:%S"))
