"""
COMPREHENSIVE DIAGNOSTIC — All Possible Model Specifications
=============================================================
Runs every combination of model, FE structure, and HS code to produce
a complete results table for critical comparison.
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
    "2504":   {"label": "Graphite",    "treat": "202312"},
    "811292": {"label": "Ga/Ge",       "treat": "202308"},
    "282560": {"label": "GeO2",        "treat": "202308"},
}
PLACEBO = {
    "2818": {"label": "Alumina"},
    "8111": {"label": "Manganese"},
    "2811": {"label": "Inorganic acids"},
}
ALL_HS = {**TREATED, **PLACEBO}


def load_panel(hs, info):
    fp = DATA / f"comtrade_{hs}_imports.csv"
    if not fp.exists():
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
    p["ln_china"] = np.log(1 + p["china_imports"])
    return p


def load_china_exports(hs):
    fp = DATA / f"comtrade_{hs}_china_exports.csv"
    if not fp.exists():
        return None
    ce = pd.read_csv(fp)
    ce["period"] = ce["period"].astype(str)
    ce["primaryValue"] = pd.to_numeric(ce["primaryValue"], errors="coerce").fillna(0)
    ts = ce.groupby("period")["primaryValue"].sum().reset_index()
    return ts


# ====================================================================
# MODEL A: ITS on aggregate China exports (time series, no FE needed)
# ====================================================================
def run_its(ts_df, treat_period, label):
    tn = PMAP[treat_period]
    ts = ts_df.copy()
    ts["t"] = ts["period"].map(PMAP) - tn
    ts["post"] = (ts["t"] >= 0).astype(int)
    ts["ln_val"] = np.log(1 + ts["primaryValue"])

    m = sm.OLS(ts["ln_val"], sm.add_constant(ts[["t", "post"]])).fit(cov_type="HC1")
    pct = (np.exp(m.params["post"]) - 1) * 100
    pre = ts[ts["post"] == 0]
    r2_pre = sm.OLS(pre["ln_val"], sm.add_constant(pre["t"])).fit().rsquared

    return {
        "model": "A: ITS (aggregate)",
        "HS": label,
        "FE": "none (time series)",
        "beta": m.params["post"],
        "p": m.pvalues["post"],
        "pct": pct,
        "pre_trend": m.params["t"],
        "pre_trend_p": m.pvalues["t"],
        "pre_R2": r2_pre,
        "R2": m.rsquared,
        "N": len(ts),
    }


# ====================================================================
# MODEL B: Bilateral panel DiD per HS code (different FE structures)
# ====================================================================
def run_panel_did(panel, hs, label, treat_period):
    tn = PMAP[treat_period]
    p = panel.copy()
    p["post"] = (p["period_num"] >= tn).astype(int)

    keep = p.groupby("reporterCode")["china_imports"].sum()
    p = p[p["reporterCode"].isin(keep[keep > 0].index)].copy()

    results = []

    # B1: No FE
    try:
        m = sm.OLS(p["ln_china"], sm.add_constant(p["post"])).fit(cov_type="HC1")
        results.append({
            "model": "B1: Panel DiD (no FE)",
            "HS": label,
            "FE": "none",
            "beta": m.params["post"],
            "p": m.pvalues["post"],
            "N": len(p),
            "R2": m.rsquared,
        })
    except Exception as e:
        results.append({"model": "B1: Panel DiD (no FE)", "HS": label, "FE": "none", "error": str(e)[:50]})

    # B2: Reporter FE only
    try:
        m = sm.OLS.from_formula("ln_china ~ C(reporterCode) + post", data=p).fit(cov_type="HC1")
        results.append({
            "model": "B2: Panel DiD (reporter FE)",
            "HS": label,
            "FE": "reporter",
            "beta": m.params["post"],
            "p": m.pvalues["post"],
            "N": len(p),
            "R2": m.rsquared,
        })
    except Exception as e:
        results.append({"model": "B2: Panel DiD (reporter FE)", "HS": label, "FE": "reporter", "error": str(e)[:50]})

    # B3: Reporter + period FE
    try:
        m = sm.OLS.from_formula("ln_china ~ C(reporterCode) + C(period_num) + post", data=p).fit(cov_type="HC1")
        results.append({
            "model": "B3: Panel DiD (reporter+period FE)",
            "HS": label,
            "FE": "reporter+period",
            "beta": m.params["post"],
            "p": m.pvalues["post"],
            "N": len(p),
            "R2": m.rsquared,
        })
    except Exception as e:
        results.append({"model": "B3: Panel DiD (reporter+period FE)", "HS": label, "FE": "reporter+period", "error": str(e)[:50]})

    return results


# ====================================================================
# MODEL C: Shift-share DiD per HS code (different FE structures)
# ====================================================================
def run_shift_share(panel, hs, label, treat_period):
    tn = PMAP[treat_period]
    p = panel.copy()

    pre = p[p["period_num"] < tn]
    pre_share = pre.groupby("reporterCode")["china_share"].mean()
    p["share_i"] = p["reporterCode"].map(pre_share).fillna(0)
    p["post"] = (p["period_num"] >= tn).astype(int)

    keep = p.groupby("reporterCode")["china_imports"].sum()
    p = p[p["reporterCode"].isin(keep[keep > 0].index)].copy()

    results = []

    # C1: Reporter FE only (no period FE)
    try:
        m = sm.OLS.from_formula("ln_china ~ C(reporterCode) + share_i:post", data=p).fit(cov_type="HC1")
        results.append({
            "model": "C1: Shift-share (reporter FE)",
            "HS": label,
            "FE": "reporter",
            "beta": m.params["share_i:post"],
            "p": m.pvalues["share_i:post"],
            "N": len(p),
            "R2": m.rsquared,
            "mean_share": p["share_i"].mean(),
            "max_share": p["share_i"].max(),
        })
    except Exception as e:
        results.append({"model": "C1: Shift-share (reporter FE)", "HS": label, "FE": "reporter", "error": str(e)[:50]})

    # C2: Reporter + period FE
    try:
        m = sm.OLS.from_formula("ln_china ~ C(reporterCode) + C(period_num) + share_i:post", data=p).fit(cov_type="HC1")
        results.append({
            "model": "C2: Shift-share (reporter+period FE)",
            "HS": label,
            "FE": "reporter+period",
            "beta": m.params["share_i:post"],
            "p": m.pvalues["share_i:post"],
            "N": len(p),
            "R2": m.rsquared,
            "mean_share": p["share_i"].mean(),
            "max_share": p["share_i"].max(),
        })
    except Exception as e:
        results.append({"model": "C2: Shift-share (reporter+period FE)", "HS": label, "FE": "reporter+period", "error": str(e)[:50]})

    return results


# ====================================================================
# MODEL D: Triple-diff (pooled, different FE structures)
# ====================================================================
def run_triple_diff(panels, per_hs=False):
    avail_t = [h for h in TREATED if h in panels]
    avail_p = [h for h in PLACEBO if h in panels]

    results = []

    targets = ["pooled"] + avail_t if not per_hs else avail_t

    for target in targets:
        if target == "pooled":
            hs_list = avail_t + avail_p
            target_label = "All treated"
        else:
            hs_list = [target] + avail_p
            target_label = TREATED[target]["label"]

        long = []
        for hs in hs_list:
            h = panels[hs]
            sub = h[["period", "period_num", "reporterCode", "china_imports", "hs"]].copy()
            sub["treated"] = 1 if hs in avail_t else 0
            if hs in avail_t:
                sub["post"] = (sub["period_num"] >= PMAP[TREATED[hs]["treat"]]).astype(int)
            else:
                sub["post"] = 0
            sub["ln_imports"] = np.log(1 + sub["china_imports"])
            long.append(sub)

        df = pd.concat(long, ignore_index=True)

        # D1: No FE
        try:
            m = sm.OLS(df["ln_imports"], sm.add_constant(df[["treated", "post", "treated_post"]])).fit(cov_type="HC1")
        except:
            df["treated_post"] = df["treated"] * df["post"]
            m = sm.OLS(df["ln_imports"], sm.add_constant(df[["treated_post"]])).fit(cov_type="HC1")

        # D1: Reporter FE
        try:
            df["treated_post"] = df["treated"] * df["post"]
            m1 = sm.OLS.from_formula("ln_imports ~ C(reporterCode) + treated_post", data=df).fit(cov_type="HC1")
            results.append({
                "model": "D1: Triple-diff (reporter FE)",
                "target": target_label,
                "FE": "reporter",
                "beta": m1.params["treated_post"],
                "p": m1.pvalues["treated_post"],
                "N": len(df),
                "R2": m1.rsquared,
            })
        except Exception as e:
            results.append({"model": "D1: Triple-diff (reporter FE)", "target": target_label, "error": str(e)[:60]})

        # D2: Reporter + period FE
        try:
            m2 = sm.OLS.from_formula("ln_imports ~ C(reporterCode) + C(period_num) + treated_post", data=df).fit(cov_type="HC1")
            results.append({
                "model": "D2: Triple-diff (reporter+period FE)",
                "target": target_label,
                "FE": "reporter+period",
                "beta": m2.params["treated_post"],
                "p": m2.pvalues["treated_post"],
                "N": len(df),
                "R2": m2.rsquared,
            })
        except Exception as e:
            results.append({"model": "D2: Triple-diff (reporter+period FE)", "target": target_label, "error": str(e)[:60]})

        # D3: Reporter + period + HS FE (the full triple-diff)
        try:
            m3 = sm.OLS.from_formula("ln_imports ~ C(reporterCode) + C(period_num) + C(hs) + treated_post", data=df).fit(cov_type="HC1")
            results.append({
                "model": "D3: Triple-diff (reporter+period+HS FE)",
                "target": target_label,
                "FE": "reporter+period+HS",
                "beta": m3.params["treated_post"],
                "p": m3.pvalues["treated_post"],
                "N": len(df),
                "R2": m3.rsquared,
            })
        except Exception as e:
            results.append({"model": "D3: Triple-diff (reporter+period+HS FE)", "target": target_label, "error": str(e)[:60]})

    return results


# ====================================================================
# MODEL E: Price ITS (same as Model A but for prices)
# ====================================================================
def run_price_its():
    fp = DATA / "bloomberg_prices_monthly.csv"
    if not fp.exists():
        return []
    pm = pd.read_csv(fp, index_col=0, parse_dates=True)
    pm.index = pd.to_datetime(pm.index)

    price_series = {
        "2504": {"col": "graphite_flake_avg", "label": "Graphite price", "treat": "2023-12"},
        "811292": {"col": "Ga_9999_price", "label": "Gallium price", "treat": "2023-08"},
        "282560": {"col": "Ge_ingot_avg", "label": "Germanium price", "treat": "2023-08"},
    }

    results = []
    for hs, info in price_series.items():
        col = info["col"]
        if col not in pm.columns:
            continue
        s = pm[col].dropna()
        treat_dt = pd.Timestamp(info["treat"])
        s = s[(s.index >= "2019-01-01") & (s.index <= "2024-12-31")]
        if len(s) < 24:
            continue

        df = pd.DataFrame({"price": s})
        df["t"] = np.arange(len(df)) - np.searchsorted(df.index, treat_dt)
        df["post"] = (df.index >= treat_dt).astype(int)
        df["ln_price"] = np.log(df["price"])

        m = sm.OLS(df["ln_price"], sm.add_constant(df[["t", "post"]])).fit(cov_type="HC1")
        pct = (np.exp(m.params["post"]) - 1) * 100
        pre_mean = df.loc[df["post"] == 0, "price"].mean()
        post_mean = df.loc[df["post"] == 1, "price"].mean()
        raw_pct = (post_mean / pre_mean - 1) * 100

        results.append({
            "model": "E: Price ITS",
            "HS": info["label"],
            "FE": "none (time series)",
            "beta": m.params["post"],
            "p": m.pvalues["post"],
            "pct": pct,
            "raw_pct": raw_pct,
            "pre_mean": pre_mean,
            "post_mean": post_mean,
            "pre_trend": m.params["t"],
            "pre_trend_p": m.pvalues["t"],
            "R2": m.rsquared,
            "N": len(df),
        })

    # Placebo price
    for col in ["In_refined_avg"]:
        if col not in pm.columns:
            continue
        for treat_dt_str, treat_label in [("2023-08", "Indium @ Aug23"), ("2023-12", "Indium @ Dec23")]:
            s = pm[col].dropna()
            treat_dt = pd.Timestamp(treat_dt_str)
            s = s[(s.index >= "2019-01-01") & (s.index <= "2024-12-31")]
            df = pd.DataFrame({"price": s})
            df["t"] = np.arange(len(df)) - np.searchsorted(df.index, treat_dt)
            df["post"] = (df.index >= treat_dt).astype(int)
            df["ln_price"] = np.log(df["price"])
            m = sm.OLS(df["ln_price"], sm.add_constant(df[["t", "post"]])).fit(cov_type="HC1")
            pct = (np.exp(m.params["post"]) - 1) * 100
            results.append({
                "model": "E: Price ITS (placebo)",
                "HS": treat_label,
                "FE": "none (time series)",
                "beta": m.params["post"],
                "p": m.pvalues["post"],
                "pct": pct,
                "R2": m.rsquared,
                "N": len(df),
            })

    return results


def main():
    print("=" * 80)
    print("COMPREHENSIVE DIAGNOSTIC — All Model Specifications")
    print("=" * 80)

    # Load all panels
    panels = {}
    for hs, info in ALL_HS.items():
        p = load_panel(hs, info)
        if p is not None:
            panels[hs] = p

    all_results = []

    # ===== PANEL A: ITS =====
    print("\n" + "=" * 80)
    print("MODEL A: ITS on Aggregate China Exports")
    print("=" * 80)
    print("Specification: ln(1+Exports_ht) = a + b1*(t-T_h) + b2*Post_ht + e")
    print("b2 = level shift at treatment. pct = exp(b2)-1.")
    print("Pre-trend: b1 should be ~0 for valid ITS.\n")

    for hs, info in TREATED.items():
        ts = load_china_exports(hs)
        if ts is not None:
            r = run_its(ts, info["treat"], info["label"])
            all_results.append(r)
            print(f"  {info['label']:10s}: beta={r['beta']:+.4f} ({r['pct']:+.1f}%, p={r['p']:.4f}), "
                  f"pre_trend={r['pre_trend']:+.4f} (p={r['pre_trend_p']:.4f}), pre_R2={r['pre_R2']:.3f}")

    # 3801 descriptive
    ts = load_china_exports("3801")
    if ts is not None:
        r = run_its(ts, "202312", "Art.graphite")
        r["model"] = "A: ITS (aggregate, excluded)"
        all_results.append(r)
        print(f"  Art.graph.: beta={r['beta']:+.4f} ({r['pct']:+.1f}%, p={r['p']:.4f}), "
              f"pre_trend={r['pre_trend']:+.4f} (p={r['pre_trend_p']:.4f}), pre_R2={r['pre_R2']:.3f}")

    # ===== PANEL B: Bilateral Panel DiD =====
    print("\n" + "=" * 80)
    print("MODEL B: Bilateral Panel DiD per HS Code")
    print("=" * 80)
    print("Specification: ln(1+Imports_rht) = [FE] + b*Post_ht + e")
    print("B1: No FE | B2: Reporter FE | B3: Reporter + Period FE")
    print("This is a simple before/after test per HS code (no control group).\n")

    for hs, info in TREATED.items():
        if hs in panels:
            results = run_panel_did(panels[hs], hs, info["label"], info["treat"])
            for r in results:
                all_results.append(r)
                if "error" in r:
                    print(f"  {r['model']:35s} | {r['HS']:10s} | ERROR: {r['error']}")
                else:
                    pct = (np.exp(r["beta"]) - 1) * 100
                    print(f"  {r['model']:35s} | {r['HS']:10s} | b={r['beta']:+.4f} ({pct:+.1f}%, p={r['p']:.4f}) | N={r['N']}")

    # ===== PANEL C: Shift-share DiD =====
    print("\n" + "=" * 80)
    print("MODEL C: Shift-Share DiD per HS Code")
    print("=" * 80)
    print("Specification: ln(1+Imports_rht) = [FE] + b*(Share_r * Post_t) + e")
    print("C1: Reporter FE | C2: Reporter + Period FE")
    print("Share_r = pre-treatment mean China share for reporter r.")
    print("b < 0 means: high-exposure reporters saw bigger import declines.\n")

    for hs, info in TREATED.items():
        if hs in panels:
            results = run_shift_share(panels[hs], hs, info["label"], info["treat"])
            for r in results:
                all_results.append(r)
                if "error" in r:
                    print(f"  {r['model']:40s} | {r['HS']:10s} | ERROR: {r['error']}")
                else:
                    print(f"  {r['model']:40s} | {r['HS']:10s} | b={r['beta']:+.4f} (p={r['p']:.4f}) | N={r['N']}")

    # ===== PANEL D: Triple-diff =====
    print("\n" + "=" * 80)
    print("MODEL D: Triple-Diff (pooled treated + placebo HS codes)")
    print("=" * 80)
    print("Specification: ln(1+Imports_rht) = [FE] + b*(Treated_h * Post_ht) + e")
    print("D1: Reporter FE | D2: Reporter+Period FE | D3: Reporter+Period+HS FE")
    print("Treated_h=1 for controlled HS codes, Post_ht=1 after treatment date.")
    print("b < 0 means: treated HS codes declined relative to placebos.\n")

    results = run_triple_diff(panels, per_hs=True)
    for r in results:
        all_results.append(r)
        if "error" in r:
            print(f"  {r['model']:40s} | {r['target']:15s} | ERROR: {r['error']}")
        else:
            pct = (np.exp(r["beta"]) - 1) * 100
            sig = "***" if r["p"] < 0.01 else "**" if r["p"] < 0.05 else "*" if r["p"] < 0.1 else ""
            print(f"  {r['model']:40s} | {r['target']:15s} | b={r['beta']:+.4f} ({pct:+.1f}%, p={r['p']:.4f}) {sig} | N={r['N']:,}")

    # ===== PANEL E: Price ITS =====
    print("\n" + "=" * 80)
    print("MODEL E: Domestic Price ITS (Bloomberg/Wind)")
    print("=" * 80)
    print("Specification: ln(Price_ht) = a + b1*(t-T_h) + b2*Post_ht + e")
    print("If controls restrict exports -> domestic oversupply -> price falls.\n")

    results = run_price_its()
    for r in results:
        all_results.append(r)
        if "raw_pct" in r:
            print(f"  {r['HS']:20s}: ITS={r['pct']:+.1f}%, raw={r['raw_pct']:+.1f}%, p={r['p']:.4f} | pre_trend={r.get('pre_trend',0):+.4f}")
        else:
            print(f"  {r['HS']:20s}: ITS={r['pct']:+.1f}%, p={r['p']:.4f}")

    # ===== MASTER TABLE =====
    print("\n\n" + "=" * 80)
    print("MASTER RESULTS TABLE (all specifications)")
    print("=" * 80)

    rows = []
    for r in all_results:
        if "error" in r:
            continue
        beta = r.get("beta", np.nan)
        pval = r.get("p", np.nan)
        pct = r.get("pct", (np.exp(beta) - 1) * 100 if not np.isnan(beta) else np.nan)
        n = r.get("N", "")
        target = r.get("HS", r.get("target", ""))
        fe = r.get("FE", "")
        sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
        rows.append({
            "Model": r["model"],
            "Target": target,
            "FE": fe,
            "beta": f"{beta:+.4f}" if not np.isnan(beta) else "",
            "pct": f"{pct:+.1f}%" if not np.isnan(pct) else "",
            "p": f"{pval:.4f}" if not np.isnan(pval) else "",
            "sig": sig,
            "N": n,
        })

    master = pd.DataFrame(rows)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.width", 140)
    pd.set_option("display.max_colwidth", 45)
    print(master.to_string(index=False))

    print(f"\n\nDONE — {time.strftime('%H:%M:%S')}")
    return master


if __name__ == "__main__":
    main()
