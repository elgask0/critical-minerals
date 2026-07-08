"""
Regressions: Shift-share DiD + Event Study for Ga/Ge episode.
Uses HS 811292 + 282560 bilateral imports data.

Key spec: ln(1 + imports_from_china)_{ict} = alpha_ic + gamma_t + beta * (share_china_ic_pre * Post_t) + e_{ict}
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm
import os
from pathlib import Path

DATA_DIR = Path("<repo-root>/03_data/raw")
RESULTS_DIR = DATA_DIR / "results"

TREAT_DATE = pd.Timestamp("2023-08-01")


def load_panel():
    return pd.read_csv(RESULTS_DIR / "panel_gage.csv")


def prep_panel(df):
    df["date"] = pd.to_datetime(df["date"])
    df["reporterCode"] = df["reporterCode"].astype(str)
    df["period"] = df["period"].astype(str)

    # Keep only reporters with positive pre-treatment trade
    pre = df[(df["date"] < TREAT_DATE) & (df["world_imports"] > 0)]
    valid_reporters = pre.groupby("reporterCode").filter(lambda x: len(x) >= 6)["reporterCode"].unique()
    df = df[df["reporterCode"].isin(valid_reporters)]

    # Entity and time indices for linearmodels
    df = df.set_index(["unit_id", "date"])
    return df


def shift_share_did(df):
    print("\n" + "="*60)
    print("SHIFT-SHARE DID: Ga/Ge export controls (effective Aug 2023)")
    print("DV: ln(1 + imports from China)")
    print("="*60)

    df["ln_china"] = np.log(1 + df["china_imports"])
    df["ln_world"] = np.log(1 + df["world_imports"])

    spec = PanelOLS(
        df["ln_china"],
        df[["bartik"]],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)
    print(res.summary.tables[1])
    print(f"\n  beta (bartik): {res.params['bartik']:.4f}")
    print(f"  se (clustered): {res.std_errors['bartik']:.4f}")
    print(f"  t-stat: {res.tstats['bartik']:.2f}")
    print(f"  p-value: {res.pvalues['bartik']:.4f}")
    print(f"  N: {res.nobs}, R2 within: {res.rsquared_within:.4f}")

    return res


def shift_share_did_world(df):
    print("\n" + "="*60)
    print("SHIFT-SHARE DID: Effect on TOTAL imports (world)")
    print("DV: ln(1 + total imports from world)")
    print("="*60)

    df["ln_world"] = np.log(1 + df["world_imports"])

    spec = PanelOLS(
        df["ln_world"],
        df[["bartik"]],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)
    print(res.summary.tables[1])
    print(f"\n  beta: {res.params['bartik']:.4f}, p={res.pvalues['bartik']:.4f}, N={res.nobs}")

    return res


def event_study(df):
    print("\n" + "="*60)
    print("EVENT STUDY: Dynamic effects by relative month")
    print("="*60)

    df_rel = df.reset_index().copy()
    df_rel["rel_time_int"] = df_rel["rel_time_int"].astype(int)

    leads_lags = list(range(-18, 19))
    for k in leads_lags:
        df_rel[f"D_k{k}"] = ((df_rel["rel_time_int"] == k) & (df_rel["pre_china_share"] > 0)).astype(float)
        df_rel[f"DD_k{k}"] = df_rel[f"D_k{k}"] * df_rel["pre_china_share"]

    dd_cols = [f"DD_k{k}" for k in leads_lags if k != -1]
    df_rel = df_rel.set_index(["unit_id", "date"])

    spec = PanelOLS(
        df_rel["ln_china"],
        df_rel[dd_cols],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
        drop_absorbed=True,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)

    print("\nEvent study coefficients (relative to k=-1):")
    print(f"{'Month':>6} {'beta':>10} {'se':>10} {'p':>10} {'sig':>5}")
    print("-" * 45)
    es_data = []
    for k in leads_lags:
        col = f"DD_k{k}"
        if col in res.params.index:
            b = res.params[col]
            se = res.std_errors[col]
            p = res.pvalues[col]
            sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
            print(f"{k:>6} {b:>10.4f} {se:>10.4f} {p:>10.4f} {sig:>5}")
            es_data.append({"month": k, "beta": b, "se": se, "p": p})

    es_df = pd.DataFrame(es_data)
    es_df.to_csv(RESULTS_DIR / "event_study_coefficients.csv", index=False)
    print(f"\n  Saved to results/event_study_coefficients.csv")

    return res


def placebo_with_exports(exports_df):
    print("\n" + "="*60)
    print("CHINA EXPORT VOLUMES: Descriptive event study")
    print("="*60)

    for hs in exports_df["hs6"].unique():
        sub = exports_df[exports_df["hs6"] == hs].sort_values("date").copy()
        sub["month_idx"] = range(len(sub))

        treat_idx = sub[sub["date"] >= TREAT_DATE].index
        if len(treat_idx) == 0:
            continue
        treat_loc = sub.index.get_loc(treat_idx[0])

        pre_mean = sub.iloc[:treat_loc]["primaryValue"].mean()
        post_mean = sub.iloc[treat_loc:]["primaryValue"].mean()

        if pre_mean > 0:
            pct_change = (post_mean / pre_mean - 1) * 100
            print(f"  HS {hs}: pre=${pre_mean:,.0f}, post=${post_mean:,.0f}, change={pct_change:+.1f}%")

    exports_df.to_csv(RESULTS_DIR / "china_exports_panel.csv", index=False)


if __name__ == "__main__":
    print("Loading panel...")
    df = load_panel()
    print(f"Raw panel: {len(df)} obs, {df['reporterCode'].nunique()} reporters")

    df = prep_panel(df)
    print(f"Clean panel: {len(df)} obs")

    # Add ln_china for event study
    df["ln_china"] = np.log(1 + df["china_imports"])

    # 1. Main shift-share DiD
    did_res = shift_share_did(df.copy())

    # 2. Effect on total imports
    did_world = shift_share_did_world(df.copy())

    # 3. Event study
    es_res = event_study(df.copy())

    # 4. China export volumes
    exports = pd.read_csv(RESULTS_DIR / "china_exports_timeseries.csv", index_col=0, parse_dates=True)
    exports_long = exports.reset_index().melt(id_vars="date", var_name="hs6", value_name="primaryValue")
    placebo_with_exports(exports_long)

    print("\n" + "="*60)
    print("ALL REGRESSIONS COMPLETE")
    print(f"Results in: {RESULTS_DIR}")
    print("="*60)
