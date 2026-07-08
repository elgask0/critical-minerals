"""
FINAL CLEAN ANALYSIS — China Critical Mineral Export Controls
==============================================================
Treated:  2504 (graphite, Dec 2023), 811292 (Ga/Ge, Aug 2023), 282560 (GeO2, Aug 2023)
Placebo:  2818 (alumina, HS 28), 8111 (manganese, HS 81), 2811 (inorganic acids, HS 28)
Excluded: 3801 (partially treated), 2501 (sparse, 12 reporters only)
Methods:  ITS, Shift-Share DiD (two-way FE), Triple-Diff, High-Exposure Analysis
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
import time
from pathlib import Path

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "03_data" / "raw"
PERIODS = [f"{y}{m:02d}" for y in range(2019, 2025) for m in range(1, 13)]
PMAP = {p: i for i, p in enumerate(PERIODS)}

TREATED = {
    "2504":   {"label": "Natural graphite",   "treat": "202312"},
    "811292": {"label": "Ga/Ge bundle",       "treat": "202308"},
    "282560": {"label": "GeO2 (+ ZrO2)",      "treat": "202308"},
}
PLACEBO = {
    "2818": {"label": "Alumina (HS 28)"},
    "8111": {"label": "Manganese (HS 81)"},
    "2811": {"label": "Inorganic acids (HS 28)"},
}
ALL_HS = {**TREATED, **PLACEBO}


def load_hs(hs, info):
    fp = DATA / f"comtrade_{hs}_imports.csv"
    if not fp.exists():
        print(f"  MISSING: {hs}")
        return None
    df = pd.read_csv(fp, low_memory=False)
    df["primaryValue"] = pd.to_numeric(df["primaryValue"], errors="coerce").fillna(0)
    df["period"] = df["period"].astype(str)
    df["reporterCode"] = pd.to_numeric(df["reporterCode"], errors="coerce")

    total = df.groupby(["reporterCode", "period"])["primaryValue"].sum().reset_index()
    total.columns = ["reporterCode", "period", "total_imports"]

    china = (
        df[df["partnerCode"] == 156]
        .groupby(["reporterCode", "period"])["primaryValue"]
        .sum()
        .reset_index()
    )
    china.columns = ["reporterCode", "period", "china_imports"]

    p = total.merge(china, on=["reporterCode", "period"], how="left")
    p["china_imports"] = p["china_imports"].fillna(0)
    p["china_share"] = np.where(
        p["total_imports"] > 0, p["china_imports"] / p["total_imports"], 0
    )
    p["hs"] = hs
    p["period_num"] = p["period"].map(PMAP)

    tp = info.get("treat")
    if tp:
        p["post"] = (p["period_num"] >= PMAP[tp]).astype(int)
    else:
        p["post"] = 0

    nz = (p["china_imports"] > 0).sum()
    n_reps = p["reporterCode"].nunique()
    n_periods = p["period"].nunique()
    print(
        f"  {hs} ({info['label']:25s}): {len(p):>5} obs, {nz:>5} nonzero, "
        f"reps={n_reps}, periods={n_periods}, mean_share={p['china_share'].mean():.3f}"
    )
    return p


def its(hs, label, treat_period):
    fp = DATA / f"comtrade_{hs}_china_exports.csv"
    if not fp.exists():
        print(f"  {hs}: no China export data")
        return None
    ce = pd.read_csv(fp)
    ce["period"] = ce["period"].astype(str)
    ce["primaryValue"] = pd.to_numeric(ce["primaryValue"], errors="coerce").fillna(0)
    ts = ce.groupby("period")["primaryValue"].sum().reset_index()
    tn = PMAP[treat_period]
    ts["t"] = ts["period"].map(PMAP) - tn
    ts["post"] = (ts["t"] >= 0).astype(int)
    ts["ln_val"] = np.log(1 + ts["primaryValue"])

    m = sm.OLS(ts["ln_val"], sm.add_constant(ts[["t", "post"]])).fit(cov_type="HC1")
    pct = (np.exp(m.params["post"]) - 1) * 100

    pre = ts[ts["post"] == 0]
    r2_pre = sm.OLS(pre["ln_val"], sm.add_constant(pre["t"])).fit().rsquared if len(pre) > 2 else np.nan

    print(
        f"  {hs} ({label:25s}): pre-trend={m.params['t']:+.4f}/mo (p={m.pvalues['t']:.4f}), "
        f"shift={m.params['post']:+.4f} ({pct:+.1f}%, p={m.pvalues['post']:.4f}), "
        f"R\u00b2={m.rsquared:.3f}, pre_R\u00b2={r2_pre:.3f}, N={len(ts)}"
    )
    return {
        "hs": hs, "label": label, "pre_trend": m.params["t"],
        "pre_p": m.pvalues["t"], "shift": m.params["post"],
        "shift_p": m.pvalues["post"], "pct": pct,
        "r2": m.rsquared, "r2_pre": r2_pre, "n": len(ts),
    }


def shift_share_did(panel, hs, label, treat_period):
    p = panel.copy()
    tn = PMAP[treat_period]

    pre = p[p["period_num"] < tn]
    pre_share = pre.groupby("reporterCode")["china_share"].mean()
    p["share_i"] = p["reporterCode"].map(pre_share).fillna(0)
    p["post"] = (p["period_num"] >= tn).astype(int)
    p["ln_china"] = np.log(1 + p["china_imports"])

    keep = p.groupby("reporterCode")["china_imports"].sum()
    p = p[p["reporterCode"].isin(keep[keep > 0].index)].copy()
    if len(p) < 200:
        print(f"  {hs}: too few obs ({len(p)})")
        return None

    m = sm.OLS.from_formula(
        "ln_china ~ C(reporterCode) + C(period_num) + share_i:post",
        data=p,
    ).fit(cov_type="HC1")
    b = m.params["share_i:post"]
    pb = m.pvalues["share_i:post"]

    print(f"\n  {hs} ({label}): N={len(p)}, reporters={p['reporterCode'].nunique()}")
    print(f"    \u03b2 = {b:+.4f} (p={pb:.4f})")
    print(f"    Mean share = {p['share_i'].mean():.3f}, max = {p['share_i'].max():.3f}")

    placebo_results = []
    sub = p[p["period_num"] < tn].copy()
    for fake in ["202201", "202101", "202006"]:
        fn = PMAP[fake]
        sub = sub.copy()
        sub["post_f"] = (sub["period_num"] >= fn).astype(int)
        mf = sm.OLS.from_formula(
            "ln_china ~ C(reporterCode) + C(period_num) + share_i:post_f",
            data=sub,
        ).fit(cov_type="HC1")
        bf = mf.params["share_i:post_f"]
        pf = mf.pvalues["share_i:post_f"]
        sig = "\u274c" if pf < 0.05 else "\u2705"
        print(f"    Placebo {fake}: \u03b2={bf:+.4f} (p={pf:.4f}) {sig}")
        placebo_results.append({"fake": fake, "beta": bf, "p": pf, "pass": pf >= 0.05})

    failures = sum(1 for r in placebo_results if not r["pass"])
    print(f"    Placebo failures: {failures}/3")

    return {"hs": hs, "beta": b, "p": pb, "placebo_failures": failures}


def triple_diff(panels):
    avail_t = [h for h in TREATED if h in panels]
    avail_p = [h for h in PLACEBO if h in panels]
    print(f"  Treated: {avail_t}")
    print(f"  Placebos: {avail_p}")

    long = []
    for hs in avail_t + avail_p:
        h = panels[hs]
        sub = h[["period", "period_num", "reporterCode", "china_imports", "hs"]].copy()
        sub["treated"] = 1 if hs in avail_t else 0
        sub["post"] = (sub["period_num"] >= PMAP[TREATED[hs]["treat"]]).astype(int) if hs in avail_t else 0
        sub["ln_imports"] = np.log(1 + sub["china_imports"])
        long.append(sub)

    df = pd.concat(long, ignore_index=True)
    print(f"  N={len(df):,}, reporters={df['reporterCode'].nunique()}, HS codes={df['hs'].nunique()}")

    results = {}

    m = sm.OLS.from_formula(
        "ln_imports ~ C(reporterCode) + C(period_num) + C(hs) + treated:post",
        data=df,
    ).fit(cov_type="HC1")
    pooled_b = m.params["treated:post"]
    pooled_p = m.pvalues["treated:post"]
    print(f"\n  Pooled: \u03b2 = {pooled_b:+.4f} (p={pooled_p:.4f})")
    results["pooled"] = {"beta": pooled_b, "p": pooled_p}

    for hs in avail_t:
        sub = df[df["hs"].isin([hs] + avail_p)].copy()
        m2 = sm.OLS.from_formula(
            "ln_imports ~ C(reporterCode) + C(period_num) + C(hs) + treated:post",
            data=sub,
        ).fit(cov_type="HC1")
        b2 = m2.params["treated:post"]
        p2 = m2.pvalues["treated:post"]
        pct = (np.exp(b2) - 1) * 100
        print(f"  {hs} ({TREATED[hs]['label']:20s}): \u03b2 = {b2:+.4f} (p={p2:.4f}, {pct:+.1f}%)")
        results[hs] = {"beta": b2, "p": p2}

    return results


def high_exposure(panels):
    for hs, info in TREATED.items():
        if hs not in panels:
            continue
        p = panels[hs]
        tn = PMAP[info["treat"]]
        pre_m = p[p["period_num"] < tn].groupby("reporterCode")["china_imports"].mean()
        post_m = p[p["period_num"] >= tn].groupby("reporterCode")["china_imports"].mean()
        share = p[p["period_num"] < tn].groupby("reporterCode")["china_share"].mean()

        chg = pd.DataFrame({"pre": pre_m, "post": post_m, "share": share}).dropna()
        chg["pct"] = (chg["post"] / chg["pre"].replace(0, np.nan) - 1) * 100
        high = chg[chg["share"] > 0.3].sort_values("share", ascending=False)

        if len(high) > 0:
            print(f"\n  {hs} ({info['label']}) \u2014 >30% China share:")
            for idx, r in high.iterrows():
                print(
                    f"    Reporter {int(idx)}: share={r['share']:.1%}, "
                    f"pre=${r['pre']:,.0f}, post=${r['post']:,.0f}, "
                    f"\u0394={r['pct']:+.1f}%"
                )
            wa = (high["pct"] * high["share"]).sum() / high["share"].sum()
            print(f"    Weighted avg \u0394: {wa:+.1f}%")
        else:
            print(f"\n  {hs} ({info['label']}): no reporters >30%")


def price_event_study():
    fp = DATA / "bloomberg_prices_monthly.csv"
    if not fp.exists():
        print("  SKIP: bloomberg_prices_monthly.csv not found")
        return None
    pm = pd.read_csv(fp, index_col=0, parse_dates=True)
    pm.index = pd.to_datetime(pm.index)
    print(f"  Loaded: {pm.shape[0]} months, {pm.shape[1]} series")
    print(f"  Date range: {pm.index.min().strftime('%Y-%m')} to {pm.index.max().strftime('%Y-%m')}")

    price_series = {
        "2504": {
            "col": "graphite_flake_avg",
            "label": "Natural flake graphite",
            "unit": "CNY/ton",
            "treat": "2023-12",
        },
        "811292": {
            "col": "Ga_9999_price",
            "label": "Gallium (>=99.99%)",
            "unit": "CNY/kg",
            "treat": "2023-08",
        },
        "282560": {
            "col": "Ge_ingot_avg",
            "label": "Germanium ingot",
            "unit": "CNY/kg",
            "treat": "2023-08",
        },
    }
    placebo_prices = {
        "In_refined_avg": {"label": "Refined indium (placebo)", "unit": "CNY/kg"},
    }

    results = {}
    for hs, info in price_series.items():
        col = info["col"]
        if col not in pm.columns:
            print(f"  {hs}: {col} not found")
            continue
        s = pm[col].dropna()
        treat_dt = pd.Timestamp(info["treat"])
        s = s[(s.index >= "2019-01-01") & (s.index <= "2024-12-31")]
        if len(s) < 24:
            print(f"  {hs}: too few observations ({len(s)})")
            continue

        df = pd.DataFrame({"price": s})
        df["t"] = np.arange(len(df)) - np.searchsorted(df.index, treat_dt)
        df["post"] = (df.index >= treat_dt).astype(int)
        df["ln_price"] = np.log(df["price"])

        m = sm.OLS(df["ln_price"], sm.add_constant(df[["t", "post"]])).fit(cov_type="HC1")
        pct = (np.exp(m.params["post"]) - 1) * 100

        pre = df[df["post"] == 0]
        r2_pre = sm.OLS(pre["ln_price"], sm.add_constant(pre["t"])).fit().rsquared if len(pre) > 2 else np.nan

        pre_mean = df.loc[df["post"] == 0, "price"].mean()
        post_mean = df.loc[df["post"] == 1, "price"].mean()
        raw_pct = (post_mean / pre_mean - 1) * 100 if pre_mean > 0 else np.nan

        print(f"\n  {hs} ({info['label']}, {info['unit']}):")
        print(f"    Pre-trend: {m.params['t']:+.6f}/mo (p={m.pvalues['t']:.4f})")
        print(f"    ITS shift: {pct:+.1f}% (β={m.params['post']:+.4f}, p={m.pvalues['post']:.4f})")
        print(f"    Raw Δ: {raw_pct:+.1f}% (pre=${pre_mean:,.0f}, post=${post_mean:,.0f})")
        print(f"    R²={m.rsquared:.3f}, pre_R²={r2_pre:.3f}, N={len(df)}")

        results[hs] = {
            "label": info["label"],
            "beta": m.params["post"],
            "p": m.pvalues["post"],
            "pct": pct,
            "raw_pct": raw_pct,
            "pre_mean": pre_mean,
            "post_mean": post_mean,
            "pre_trend": m.params["t"],
            "pre_trend_p": m.pvalues["t"],
            "r2": m.rsquared,
            "r2_pre": r2_pre,
            "n": len(df),
        }

    print(f"\n  Placebo price checks:")
    for col, info in placebo_prices.items():
        if col not in pm.columns:
            continue
        for treat_dt_str in ["2023-08", "2023-12"]:
            s = pm[col].dropna()
            treat_dt = pd.Timestamp(treat_dt_str)
            s = s[(s.index >= "2019-01-01") & (s.index <= "2024-12-31")]
            df = pd.DataFrame({"price": s})
            df["t"] = np.arange(len(df)) - np.searchsorted(df.index, treat_dt)
            df["post"] = (df.index >= treat_dt).astype(int)
            df["ln_price"] = np.log(df["price"])
            m = sm.OLS(df["ln_price"], sm.add_constant(df[["t", "post"]])).fit(cov_type="HC1")
            pct = (np.exp(m.params["post"]) - 1) * 100
            sig = "***" if m.pvalues["post"] < 0.01 else "**" if m.pvalues["post"] < 0.05 else "*" if m.pvalues["post"] < 0.1 else ""
            print(f"    {info['label']} @ {treat_dt_str}: {pct:+.1f}% (p={m.pvalues['post']:.4f}) {sig}")

    return results


EUROSTAT_PRODUCTS = {
    "Ga": {"label": "Gallium (CN8 81129289)", "treated": True, "cn8": "81129289"},
    "Ge": {"label": "Germanium (CN8 81129295)", "treated": True, "cn8": "81129295"},
    "In": {"label": "Indium (CN8 81129281, placebo)", "treated": False, "cn8": "81129281"},
    "V":  {"label": "Vanadium (CN8 81129291, placebo)", "treated": False, "cn8": "81129291"},
}


def load_eurostat_cn8():
    country_fp = REPO / "03_data" / "interim" / "eurostat_cn8_eu27_balanced_long.csv"
    monthly_fp = REPO / "03_data" / "processed" / "eurostat_cn8_eu27_monthly.csv"
    if not country_fp.exists() or not monthly_fp.exists():
        print("  SKIP: normalized Eurostat CN8 files not found")
        print("  Run: python 04_scripts/prepare_eurostat_cn8.py")
        return None

    country = pd.read_csv(country_fp)
    country = country[
        ["reporter", "partner", "product", "period", "value_eur"]
    ].copy()

    monthly = pd.read_csv(monthly_fp)
    eu_china = monthly[
        ["product", "period", "china_imports_eur"]
    ].rename(columns={"china_imports_eur": "value_eur"})
    eu_china["reporter"] = "EU27"
    eu_china["partner"] = "CN"

    eu_world = monthly[
        ["product", "period", "world_imports_eur"]
    ].rename(columns={"world_imports_eur": "value_eur"})
    eu_world["reporter"] = "EU27"
    eu_world["partner"] = "WORLD"

    df = pd.concat(
        [
            country,
            eu_china[country.columns],
            eu_world[country.columns],
        ],
        ignore_index=True,
    )
    df["period"] = df["period"].str.replace("-", "")
    df["period_num"] = df["period"].map(PMAP)
    df = df.dropna(subset=["period_num"])
    df["period_num"] = df["period_num"].astype(int)
    tn = PMAP["202308"]
    df["post"] = (df["period_num"] >= tn).astype(int)
    df["ln_value"] = np.log(1 + df["value_eur"])
    print(f"  Loaded: {len(df)} rows, products={df['product'].unique().tolist()}, "
          f"reporters={df['reporter'].nunique()}, period={df['period'].min()}-{df['period'].max()}")
    return df


def eurostat_eu_its(df):
    if df is None:
        return {}
    eu = df[df["reporter"] == "EU27"].copy()
    print(f"  EU27 aggregate rows: {len(eu)}")
    results = {}
    for prod, info in EUROSTAT_PRODUCTS.items():
        for partner in ["CN", "WORLD"]:
            sub = eu[(eu["product"] == prod) & (eu["partner"] == partner)].copy()
            if len(sub) < 24:
                print(f"    {prod}<-{partner}: too few obs ({len(sub)})")
                continue
            tn = PMAP["202308"]
            sub["t"] = sub["period_num"] - tn
            m = sm.OLS(sub["ln_value"], sm.add_constant(sub[["t", "post"]])).fit(cov_type="HC1")
            pct = (np.exp(m.params["post"]) - 1) * 100
            pre = sub[sub["post"] == 0]
            r2_pre = sm.OLS(pre["ln_value"], sm.add_constant(pre["t"])).fit().rsquared if len(pre) > 2 else np.nan
            tag = "TREATED" if info["treated"] else "PLACEBO"
            print(f"    {prod}<-{partner} [{tag}]: "
                  f"shift={pct:+.1f}% (β={m.params['post']:+.4f}, p={m.pvalues['post']:.4f}), "
                  f"pre-trend={m.params['t']:+.4f}/mo, R²={m.rsquared:.3f}, N={len(sub)}")
            key = f"{prod}_{partner}"
            results[key] = {
                "product": prod, "partner": partner,
                "label": info["label"], "treated": info["treated"],
                "beta": m.params["post"], "p": m.pvalues["post"],
                "pct": pct, "pre_trend": m.params["t"],
                "pre_trend_p": m.pvalues["t"],
                "r2": m.rsquared, "r2_pre": r2_pre, "n": len(sub),
            }
    return results


def eurostat_cn8_triple_diff(df):
    if df is None:
        return {}
    eu = df[(df["reporter"] == "EU27") & (df["partner"] == "CN")].copy()
    if len(eu) < 50:
        print("  Too few EU27×CN obs for triple-diff")
        return {}
    eu["treated_prod"] = eu["product"].map(
        {p: 1 if i["treated"] else 0 for p, i in EUROSTAT_PRODUCTS.items()}
    )
    m = sm.OLS.from_formula(
        "ln_value ~ C(product) + C(period_num) + treated_prod:post",
        data=eu,
    ).fit(cov_type="HC1")
    b = m.params["treated_prod:post"]
    p_val = m.pvalues["treated_prod:post"]
    pct = (np.exp(b) - 1) * 100
    print(f"  EU27 CN8 Triple-Diff (Ga/Ge treated vs In/V placebo):")
    print(f"    β = {b:+.4f} (p={p_val:.4f}, {pct:+.1f}%) | N={len(eu)}")
    results = {"eu27_cn": {"beta": b, "p": p_val, "pct": pct, "n": len(eu)}}

    bilateral = df[(df["reporter"] != "EU27") & (df["partner"] == "CN")].copy()
    bilateral["treated_prod"] = bilateral["product"].map(
        {p: 1 if i["treated"] else 0 for p, i in EUROSTAT_PRODUCTS.items()}
    )
    if len(bilateral) > 100:
        m2 = sm.OLS.from_formula(
            "ln_value ~ C(reporter) + C(product) + C(period_num) + treated_prod:post",
            data=bilateral,
        ).fit(cov_type="HC1")
        b2 = m2.params["treated_prod:post"]
        p2 = m2.pvalues["treated_prod:post"]
        pct2 = (np.exp(b2) - 1) * 100
        print(f"  Bilateral CN8 Triple-Diff (27 EU countries × CN):")
        print(f"    β = {b2:+.4f} (p={p2:.4f}, {pct2:+.1f}%) | N={len(bilateral)}")
        results["bilateral_cn"] = {"beta": b2, "p": p2, "pct": pct2, "n": len(bilateral)}

    return results


def eurostat_bilateral_did(df):
    if df is None:
        return {}
    bilat = df[
        (df["reporter"] != "EU27") &
        (df["partner"].isin(["CN", "WORLD"]))
    ].dropna(subset=["reporter"]).copy()
    eu_countries = sorted(bilat["reporter"].unique())
    print(f"  Bilateral panel: {len(eu_countries)} EU countries, {len(bilat)} obs")

    ga_cn = bilat[(bilat["product"] == "Ga") & (bilat["partner"] == "CN")]
    ga_world = bilat[(bilat["product"] == "Ga") & (bilat["partner"] == "WORLD")]
    if len(ga_world) > 0:
        ga_cn_share = ga_cn.groupby("reporter")["value_eur"].sum() / ga_world.groupby("reporter")["value_eur"].sum()
        ga_cn_share = ga_cn_share.fillna(0).replace([np.inf, -np.inf], 0)
    else:
        ga_cn_share = pd.Series(dtype=float)

    if len(ga_cn) > 100:
        m = sm.OLS.from_formula(
            "ln_value ~ C(reporter) + C(period_num) + post",
            data=ga_cn,
        ).fit(cov_type="HC1")
        b = m.params["post"]
        p_val = m.pvalues["post"]
        pct = (np.exp(b) - 1) * 100
        print(f"  Ga<-CN bilateral DID (two-way FE):")
        print(f"    β = {b:+.4f} (p={p_val:.4f}, {pct:+.1f}%) | N={len(ga_cn)}")

    if len(ga_cn_share) > 3:
        top5 = ga_cn_share.nlargest(5)
        print(f"  Ga<-CN top-5 exposed (by China share):")
        for country, share in top5.items():
            country_data = ga_cn[ga_cn["reporter"] == country]
            if len(country_data) == 0:
                continue
            pre = country_data[country_data["post"] == 0]["value_eur"].mean()
            post = country_data[country_data["post"] == 1]["value_eur"].mean()
            if pre > 0 and not np.isnan(post):
                chg = ((post / pre) - 1) * 100
                print(f"    {country}: share={share:.1%}, pre=€{pre/1e3:.0f}K, post=€{post/1e3:.0f}K, Δ={chg:+.1f}%")
            else:
                print(f"    {country}: share={share:.1%}, pre=€{pre/1e3:.0f}K, post=€{post/1e3:.0f}K, Δ=n/a")

    return {}


def main():
    print("=" * 70)
    print("FINAL CLEAN ANALYSIS — China Critical Mineral Export Controls")
    print("=" * 70)
    print(f"  Treated:  {list(TREATED.keys())}")
    print(f"  Placebo:  {list(PLACEBO.keys())}")
    print(f"  Excluded: 3801 (partially treated), 2501 (sparse)")
    print()

    print("=" * 70)
    print("1. DATA LOADING")
    print("=" * 70)
    panels = {}
    for hs, info in ALL_HS.items():
        p = load_hs(hs, info)
        if p is not None:
            panels[hs] = p
    print(f"\n  Loaded: {len(panels)}/{len(ALL_HS)} HS codes")

    print("\n" + "=" * 70)
    print("2. INTERRUPTED TIME SERIES (China Export Volume)")
    print("=" * 70)
    its_results = {}
    for hs, info in TREATED.items():
        r = its(hs, info["label"], info["treat"])
        if r:
            its_results[hs] = r
    print("\n  Descriptive: 3801 (Artificial graphite, internal placebo)")
    its("3801", "Artificial graphite (excluded)", "202312")

    print("\n" + "=" * 70)
    print("3. SHIFT-SHARE DiD (two-way FE: reporter + period)")
    print("=" * 70)
    ss_results = {}
    for hs, info in TREATED.items():
        if hs in panels:
            r = shift_share_did(panels[hs], hs, info["label"], info["treat"])
            if r:
                ss_results[hs] = r

    print("\n" + "=" * 70)
    print("4. TRIPLE-DIFF (reporter + period + HS FE)")
    print("=" * 70)
    td_results = triple_diff(panels)

    print("\n" + "=" * 70)
    print("5. HIGH-EXPOSURE REPORTERS (>30% China share)")
    print("=" * 70)
    high_exposure(panels)

    print("\n" + "=" * 70)
    print("6. DOMESTIC PRICE EVENT STUDY (Bloomberg/Wind data)")
    print("=" * 70)
    price_results = price_event_study()

    print("\n" + "=" * 70)
    print("7. EUROSTAT CN8 DISAGGREGATED ANALYSIS (EU imports)")
    print("=" * 70)
    cn8_df = load_eurostat_cn8()
    cn8_its_results = eurostat_eu_its(cn8_df)

    print("\n  --- CN8 Triple-Diff (treated Ga/Ge vs placebo In/V) ---")
    cn8_td_results = eurostat_cn8_triple_diff(cn8_df)

    print("\n  --- CN8 Bilateral Analysis ---")
    eurostat_bilateral_did(cn8_df)

    print("\n" + "=" * 70)
    print("FINAL RESULTS SUMMARY")
    print("=" * 70)
    print(f"""
ITS (China export volume):
  Graphite (2504): {its_results.get('2504', {}).get('pct', '?'):+.1f}% (p={its_results.get('2504', {}).get('shift_p', '?'):.4f}) | pre-trend={its_results.get('2504', {}).get('pre_trend', 0):+.4f}/mo
  Ga/Ge (811292):  {its_results.get('811292', {}).get('pct', '?'):+.1f}% (p={its_results.get('811292', {}).get('shift_p', '?'):.4f}) | pre-trend={its_results.get('811292', {}).get('pre_trend', 0):+.4f}/mo
  GeO2 (282560):   {its_results.get('282560', {}).get('pct', '?'):+.1f}% (p={its_results.get('282560', {}).get('shift_p', '?'):.4f}) | pre-trend={its_results.get('282560', {}).get('pre_trend', 0):+.4f}/mo

Shift-Share DiD (two-way FE):
  Graphite: \u03b2={ss_results.get('2504', {}).get('beta', 0):+.4f} (p={ss_results.get('2504', {}).get('p', 0):.4f}) | placebo fails: {ss_results.get('2504', {}).get('placebo_failures', '?')}/3
  Ga/Ge:    \u03b2={ss_results.get('811292', {}).get('beta', 0):+.4f} (p={ss_results.get('811292', {}).get('p', 0):.4f}) | placebo fails: {ss_results.get('811292', {}).get('placebo_failures', '?')}/3
  GeO2:     \u03b2={ss_results.get('282560', {}).get('beta', 0):+.4f} (p={ss_results.get('282560', {}).get('p', 0):.4f}) | placebo fails: {ss_results.get('282560', {}).get('placebo_failures', '?')}/3

Triple-Diff (placebos: 2818 alumina, 8111 manganese, 2811 inorganic acids):
  Pooled:   \u03b2={td_results.get('pooled', {}).get('beta', 0):+.4f} (p={td_results.get('pooled', {}).get('p', 0):.4f})
  Graphite: \u03b2={td_results.get('2504', {}).get('beta', 0):+.4f} (p={td_results.get('2504', {}).get('p', 0):.4f})
  Ga/Ge:    \u03b2={td_results.get('811292', {}).get('beta', 0):+.4f} (p={td_results.get('811292', {}).get('p', 0):.4f})
  GeO2:     \u03b2={td_results.get('282560', {}).get('beta', 0):+.4f} (p={td_results.get('282560', {}).get('p', 0):.4f})
""")

    if price_results:
        print("Domestic Price ITS (Bloomberg/Wind, 2019-2024):")
        for hs in ["2504", "811292", "282560"]:
            r = price_results.get(hs, {})
            if r:
                print(f"  {r.get('label', hs):25s}: {r.get('pct', 0):+.1f}% (p={r.get('p', 0):.4f}) | raw={r.get('raw_pct', 0):+.1f}% | pre_R²={r.get('r2_pre', 0):.3f}")
        print()

    if cn8_its_results:
        print("Eurostat CN8 ITS (EU27 imports from China, Aug 2023):")
        for key in ["Ga_CN", "Ge_CN", "In_CN", "V_CN"]:
            r = cn8_its_results.get(key, {})
            if r:
                tag = "TREATED" if r.get("treated") else "PLACEBO"
                print(f"  {r['label']:40s} [{tag}]: {r['pct']:+.1f}% (p={r['p']:.4f})")
        print()

    if cn8_td_results:
        print("Eurostat CN8 Triple-Diff (Ga/Ge treated vs In/V placebo):")
        for k, r in cn8_td_results.items():
            print(f"  {k:20s}: β={r['beta']:+.4f} (p={r['p']:.4f}, {r['pct']:+.1f}%)")
        print()

    print("DONE \u2014", time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
