"""
Graphite (HS 2504) bilateral imports panel construction and shift-share DiD.
Treatment: December 1, 2023 (Announcement No. 39 of 2023).
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import os
from pathlib import Path

DATA_DIR = Path("<repo-root>/03_data/raw")
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
RAW_DIR = DATA_DIR / "imports_2504"

TREAT_DATE = pd.Timestamp("2023-12-01")


def load_raw_imports():
    dfs = []
    for f in sorted(RAW_DIR.glob("*.csv")):
        df = pd.read_csv(f)
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df["period"] = df["period"].astype(int).astype(str)
    df = df.groupby(["reporterCode", "partnerCode", "period"]).agg(
        {"primaryValue": "sum"}
    ).reset_index()
    return df


def build_panel():
    df = load_raw_imports()
    print(f"Raw data: {len(df):,} rows")
    print(f"  Reporters: {df['reporterCode'].nunique()}")
    print(f"  Partners: {df['partnerCode'].nunique()}")
    print(f"  Periods: {df['period'].nunique()}")

    df["year"] = df["period"].str[:4].astype(int)
    df["month"] = df["period"].str[4:6].astype(int)
    df["date"] = pd.to_datetime(df["period"], format="%Y%m")

    bilateral = df[df["partnerCode"] != 0].copy()
    world = df[df["partnerCode"] == 0][["reporterCode", "period", "primaryValue"]].copy()
    world = world.rename(columns={"primaryValue": "world_imports"})

    china = bilateral[bilateral["partnerCode"] == 156][["reporterCode", "period", "primaryValue"]].copy()
    china = china.rename(columns={"primaryValue": "china_imports"})

    panel = world.merge(china, on=["reporterCode", "period"], how="left")
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
    pre_share = pre.groupby("reporterCode").agg(
        pre_china_share=("china_share", "mean"),
        pre_china_imports=("china_imports", "mean"),
        pre_world_imports=("world_imports", "mean"),
    ).reset_index()

    panel = panel.merge(pre_share, on="reporterCode", how="left")

    panel["bartik"] = panel["pre_china_share"] * panel["post"]

    panel["rel_time"] = (panel["date"] - TREAT_DATE) / pd.Timedelta(days=30.44)
    panel["rel_time_int"] = panel["rel_time"].round().astype(int)

    panel["reporterCode"] = panel["reporterCode"].astype(str)
    panel["reporter_id"] = panel["reporterCode"].astype("category").cat.codes
    panel["period_id"] = panel["period"].astype("category").cat.codes
    panel["unit_id"] = panel["reporterCode"].astype("category").cat.codes

    panel = panel.sort_values(["reporterCode", "period"]).reset_index(drop=True)

    print(f"\nPanel: {len(panel):,} obs, {panel['reporterCode'].nunique()} reporters, {panel['period'].nunique()} periods")
    print(f"  Date range: {panel['date'].min()} to {panel['date'].max()}")
    print(f"  Pre obs: {(panel['post']==0).sum()}, Post obs: {(panel['post']==1).sum()}")

    return panel


def summary_stats(panel):
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS — Graphite (HS 2504)")
    print("=" * 60)

    pre = panel[panel["post"] == 0]
    post = panel[panel["post"] == 1]

    with_china = panel[panel["china_imports"] > 0]["reporterCode"].nunique()
    total_reporters = panel["reporterCode"].nunique()

    print(f"\n  Reporters with any China imports: {with_china}/{total_reporters}")
    print(f"  Total world imports (panel): ${panel['world_imports'].sum():,.0f}")
    print(f"  Total China imports (panel): ${panel['china_imports'].sum():,.0f}")
    print(f"  Avg China share (pre): {pre[pre['world_imports']>0]['china_share'].mean():.3f}")
    print(f"  Avg China share (post): {post[post['world_imports']>0]['china_share'].mean():.3f}")

    print(f"\n--- Pre/Post aggregates ---")
    pre_total_china = pre.groupby("period")["china_imports"].sum()
    post_total_china = post.groupby("period")["china_imports"].sum()
    print(f"  Pre avg China exports/month:  ${pre_total_china.mean():,.0f}")
    print(f"  Post avg China exports/month: ${post_total_china.mean():,.0f}")
    if pre_total_china.mean() > 0:
        print(f"  Change: {(post_total_china.mean() / pre_total_china.mean() - 1) * 100:+.1f}%")

    pre_total_world = pre.groupby("period")["world_imports"].sum()
    post_total_world = post.groupby("period")["world_imports"].sum()
    print(f"\n  Pre avg world imports/month:  ${pre_total_world.mean():,.0f}")
    print(f"  Post avg world imports/month: ${post_total_world.mean():,.0f}")
    if pre_total_world.mean() > 0:
        print(f"  Change: {(post_total_world.mean() / pre_total_world.mean() - 1) * 100:+.1f}%")

    print(f"\n--- Exposure distribution (pre-treatment China share) ---")
    reporters = panel.drop_duplicates("reporterCode")[["reporterCode", "pre_china_share", "pre_china_imports", "pre_world_imports"]]
    reporters = reporters.sort_values("pre_china_imports", ascending=False)
    top15 = reporters.head(15)
    print(f"  Top 15 reporters by pre-treatment China imports:")
    for _, r in top15.iterrows():
        print(f"    Reporter {r['reporterCode']}: share={r['pre_china_share']:.3f}, China=${r['pre_china_imports']:,.0f}/mo, World=${r['pre_world_imports']:,.0f}/mo")

    share_bins = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01]
    share_labels = ["0-10%", "10-30%", "30-50%", "50-70%", "70-90%", "90-100%"]
    reporters["share_bin"] = pd.cut(reporters["pre_china_share"], bins=share_bins, labels=share_labels, right=False)
    print(f"\n  Exposure distribution:")
    for label in share_labels:
        n = (reporters["share_bin"] == label).sum()
        print(f"    {label}: {n} reporters")


def shift_share_did(panel, dv="ln_china_imports", label=""):
    df = panel.copy()

    pre = df[(df["post"] == 0) & (df["world_imports"] > 0)]
    valid = pre.groupby("reporterCode").filter(lambda x: len(x) >= 6)["reporterCode"].unique()
    df = df[df["reporterCode"].isin(valid)]

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
    print(f"SHIFT-SHARE DiD — Graphite (HS 2504)")
    print(f"DV: {dv}  {label}")
    print(f"Treatment: Dec 1, 2023")
    print(f"{'='*60}")
    print(res.summary.tables[1])
    print(f"\n  beta (bartik): {res.params['bartik']:.4f}")
    print(f"  se (clustered): {res.std_errors['bartik']:.4f}")
    print(f"  t-stat: {res.tstats['bartik']:.2f}")
    print(f"  p-value: {res.pvalues['bartik']:.4f}")
    print(f"  N: {res.nobs}, R2 within: {res.rsquared_within:.4f}")

    return res


def event_study(panel):
    df = panel.copy()

    pre = df[(df["post"] == 0) & (df["world_imports"] > 0)]
    valid = pre.groupby("reporterCode").filter(lambda x: len(x) >= 6)["reporterCode"].unique()
    df = df[df["reporterCode"].isin(valid)]

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
    print(f"EVENT STUDY — Graphite (HS 2504) bilateral imports")
    print(f"Reference period: k=-1 (Nov 2023)")
    print(f"{'='*60}")
    print(f"\n{'Month':>6} {'beta':>10} {'se':>10} {'p':>10} {'sig':>5}")
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
    es_df.to_csv(RESULTS_DIR / "event_study_graphite_2504.csv", index=False)
    print(f"\n  Saved to results/event_study_graphite_2504.csv")

    return res


def placebo_test(panel, fake_date_str="2022-12-01"):
    fake_date = pd.Timestamp(fake_date_str)
    df = panel.copy()

    df["fake_post"] = (df["date"] >= fake_date).astype(int)

    fake_pre = df[df["date"] < fake_date].copy()
    fake_pre_share = fake_pre.groupby("reporterCode").agg(
        fake_pre_china_share=("china_share", "mean"),
    ).reset_index()

    df = df.merge(fake_pre_share, on="reporterCode", how="left")
    df["fake_bartik"] = df["fake_pre_china_share"] * df["fake_post"]

    valid = df[(df["date"] < fake_date) & (df["world_imports"] > 0)]
    valid_reporters = valid.groupby("reporterCode").filter(lambda x: len(x) >= 6)["reporterCode"].unique()
    df = df[df["reporterCode"].isin(valid_reporters)]

    df = df.set_index(["unit_id", "date"])

    spec = PanelOLS(
        df["ln_china_imports"],
        df[["fake_bartik"]],
        entity_effects=True,
        time_effects=True,
        check_rank=False,
    )
    res = spec.fit(cov_type="clustered", cluster_entity=True)

    print(f"\n{'='*60}")
    print(f"PLACEBO TEST — Fake treatment at {fake_date_str}")
    print(f"{'='*60}")
    print(f"  beta (fake bartik): {res.params['fake_bartik']:.4f}")
    print(f"  p-value: {res.pvalues['fake_bartik']:.4f}")
    print(f"  N: {res.nobs}, R2 within: {res.rsquared_within:.4f}")
    if res.pvalues["fake_bartik"] < 0.05:
        print("  WARNING: Placebo significant — effect may be pre-existing trend")
    else:
        print("  PASS: Placebo not significant — supports causal interpretation")

    return res


if __name__ == "__main__":
    print("Building graphite (HS 2504) bilateral imports panel...")
    panel = build_panel()

    panel.to_csv(RESULTS_DIR / "panel_graphite_2504.csv", index=False)
    print(f"Saved to results/panel_graphite_2504.csv")

    summary_stats(panel)

    print("\n\n")
    res_china = shift_share_did(panel, dv="ln_china_imports", label="(China imports)")

    print("\n\n")
    res_world = shift_share_did(panel, dv="ln_world_imports", label="(World imports)")

    print("\n\n")
    es_res = event_study(panel)

    print("\n\n")
    placebo_res = placebo_test(panel, fake_date_str="2022-12-01")
    placebo_res2 = placebo_test(panel, fake_date_str="2022-06-01")

    print("\n" + "=" * 60)
    print("ALL GRAPHITE REGRESSIONS COMPLETE")
    print(f"Results in: {RESULTS_DIR}")
    print("=" * 60)
