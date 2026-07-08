"""
Re-run all regressions with PROPERLY AGGREGATED data.
The old panel_gage.csv had duplicate (reporter, period, hs) entries
because raw Comtrade data has multiple customs codes per trade flow.
This script aggregates before building the panel.
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
from pathlib import Path

DATA_DIR = Path("<repo-root>/03_data/raw")
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

TREAT_DATE = pd.Timestamp("2023-08-01")


def load_and_aggregate(hs):
    f = DATA_DIR / f"comtrade_{hs}_imports.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f)
    df["period"] = df["period"].astype(str)
    agg = df.groupby(["reporterCode", "partnerCode", "period"]).agg(
        {"primaryValue": "sum"}
    ).reset_index()
    agg["hs6"] = hs
    return agg


def build_panel():
    dfs = []
    for hs in ["811292", "282560"]:
        df = load_and_aggregate(hs)
        if df is not None:
            dfs.append(df)

    if not dfs:
        return None

    df = pd.concat(dfs, ignore_index=True)
    df["date"] = pd.to_datetime(df["period"], format="%Y%m")

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

    panel["date"] = pd.to_datetime(panel["period"], format="%Y%m")
    panel["post"] = (panel["date"] >= TREAT_DATE).astype(int)

    pre = panel[panel["date"] < TREAT_DATE].copy()
    pre_share = pre.groupby(["reporterCode", "hs6"]).agg(
        pre_china_share=("china_share", "mean"),
        pre_china_imports=("china_imports", "mean"),
        pre_world_imports=("world_imports", "mean"),
    ).reset_index()

    panel = panel.merge(pre_share, on=["reporterCode", "hs6"], how="left")

    panel["bartik"] = panel["pre_china_share"] * panel["post"]

    panel["rel_time"] = (panel["date"] - TREAT_DATE) / pd.Timedelta(days=30.44)
    panel["rel_time_int"] = panel["rel_time"].round().astype(int)

    panel["reporterCode"] = panel["reporterCode"].astype(str)
    panel["reporter_id"] = panel["reporterCode"].astype("category").cat.codes
    panel["period_id"] = panel["period"].astype("category").cat.codes
    panel["unit_id"] = (panel["reporterCode"] + "_" + panel["hs6"]).astype("category").cat.codes

    return panel


def shift_share_did(panel, dv, label):
    df = panel.copy()

    pre = df[(df["post"] == 0) & (df["world_imports"] > 0)]
    valid = pre.groupby("unit_id").filter(lambda x: len(x) >= 6)["unit_id"].unique()
    df = df[df["unit_id"].isin(valid)]

    df = df.set_index(["unit_id", "date"])

    spec = PanelOLS(
        df[dv],
        df[["bartik"]],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)

    print(f"\n{'='*60}")
    print(f"SHIFT-SHARE DiD — Ga/Ge (AGGREGATED DATA)")
    print(f"DV: {dv}  {label}")
    print(f"{'='*60}")
    print(res.summary.tables[1])
    print(f"  beta: {res.params['bartik']:.4f}")
    print(f"  se: {res.std_errors['bartik']:.4f}")
    print(f"  t: {res.tstats['bartik']:.2f}")
    print(f"  p: {res.pvalues['bartik']:.4f}")
    print(f"  N: {res.nobs}, R2 within: {res.rsquared_within:.4f}")

    return res


def event_study(panel):
    df = panel.copy()

    pre = df[(df["post"] == 0) & (df["world_imports"] > 0)]
    valid = pre.groupby("unit_id").filter(lambda x: len(x) >= 6)["unit_id"].unique()
    df = df[df["unit_id"].isin(valid)]

    df["ln_china"] = np.log(1 + df["china_imports"])

    df["rel_time_int"] = df["rel_time_int"].astype(int)
    leads_lags = sorted(df["rel_time_int"].unique())
    leads_lags = [k for k in leads_lags if -24 <= k <= 18]

    for k in leads_lags:
        df[f"D_k{k}"] = ((df["rel_time_int"] == k) & (df["pre_china_share"] > 0)).astype(float)
        df[f"DD_k{k}"] = df[f"D_k{k}"] * df["pre_china_share"]

    dd_cols = [f"DD_k{k}" for k in leads_lags if k != -1]
    df = df.set_index(["unit_id", "date"])

    spec = PanelOLS(
        df["ln_china"],
        df[dd_cols],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
        drop_absorbed=True,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)

    print(f"\n{'='*60}")
    print(f"EVENT STUDY — Ga/Ge (AGGREGATED DATA)")
    print(f"Reference: k=-1 (Jul 2023)")
    print(f"{'='*60}")
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
    es_df.to_csv(RESULTS_DIR / "event_study_aggregated.csv", index=False)
    print(f"  Saved to event_study_aggregated.csv")

    # Check parallel trends: count significant pre-treatment
    pre_sig = sum(1 for d in es_data if d["month"] < 0 and d["p"] < 0.05)
    total_pre = sum(1 for d in es_data if d["month"] < 0)
    print(f"\n  Pre-treatment periods significant at 5%: {pre_sig}/{total_pre}")
    if pre_sig > 0:
        print("  WARNING: Parallel trends violated")
    else:
        print("  PASS: No pre-treatment periods significant")

    return res


def placebo(panel, fake_date_str):
    fake_date = pd.Timestamp(fake_date_str)
    df = panel.copy()

    df["fake_post"] = (df["date"] >= fake_date).astype(int)

    fake_pre = df[df["date"] < fake_date].copy()
    fake_pre_share = fake_pre.groupby("unit_id").agg(
        fake_pre_china_share=("china_share", "mean"),
    ).reset_index()

    df = df.merge(fake_pre_share, on="unit_id", how="left")
    df["fake_bartik"] = df["fake_pre_china_share"] * df["fake_post"]

    valid = df[(df["date"] < fake_date) & (df["world_imports"] > 0)]
    valid_units = valid.groupby("unit_id").filter(lambda x: len(x) >= 6)["unit_id"].unique()
    df = df[df["unit_id"].isin(valid_units)]

    df = df.set_index(["unit_id", "date"])

    spec = PanelOLS(
        df["ln_china_imports"],
        df[["fake_bartik"]],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)

    print(f"\n  PLACEBO (fake={fake_date_str}): beta={res.params['fake_bartik']:.4f}, p={res.pvalues['fake_bartik']:.4f}, N={res.nobs}")
    if res.pvalues["fake_bartik"] < 0.05:
        print(f"  FAIL: Placebo significant")
    else:
        print(f"  PASS: Placebo not significant")

    return res


if __name__ == "__main__":
    print("Building panel with AGGREGATED data...")
    panel = build_panel()

    # Verify no duplicates
    dupes = panel.groupby(["reporterCode", "period", "hs6"]).size()
    print(f"Panel: {len(panel):,} rows, {panel['reporterCode'].nunique()} reporters")
    print(f"  Max duplicates per (reporter,period,hs): {dupes.max()}")
    print(f"  Periods: {panel['period'].nunique()}, date range: {panel['date'].min()} to {panel['date'].max()}")

    panel.to_csv(RESULTS_DIR / "panel_gage_v2_aggregated.csv", index=False)
    print(f"  Saved to panel_gage_v2_aggregated.csv")

    # Summary
    pre = panel[panel["post"] == 0]
    post = panel[panel["post"] == 1]
    print(f"\n  Pre avg China imports/mo: ${pre.groupby('period')['china_imports'].sum().mean():,.0f}")
    print(f"  Post avg China imports/mo: ${post.groupby('period')['china_imports'].sum().mean():,.0f}")

    # 1. DiD — China imports
    r1 = shift_share_did(panel, "ln_china_imports", "(China imports)")

    # 2. DiD — World imports
    r2 = shift_share_did(panel, "ln_world_imports", "(World imports)")

    # 3. Event study
    r3 = event_study(panel)

    # 4. Placebo
    print(f"\n{'='*60}")
    print("PLACEBO TESTS")
    print(f"{'='*60}")
    p1 = placebo(panel, "2022-01-01")
    p2 = placebo(panel, "2022-06-01")

    print(f"\n{'='*60}")
    print("ALL REGRESSIONS COMPLETE (AGGREGATED DATA)")
    print(f"{'='*60}")
