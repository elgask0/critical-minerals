"""
Term-paper robustness checks for HS 282580 (and selected others).

Reuses the exact PPML engine from analysis_thesis.py so every fit shares the
estimator used in the manuscript. Produces:

  - term_reporting_coverage_by_product.csv            (Part 1A)
  - term_reporting_coverage_by_month_hs282580.csv      (Part 1A)
  - term_late_reporting_ppml_hs282580.csv              (Part 1B)
  - term_late_reporting_eventstudy_hs282580.csv        (Part 1C)
  - term_late_reporting_switching_hs282580.csv         (Part 1D)
  - term_reported_only_ppml_hs282580.csv               (Part 1E)
  - term_donor_pool_sensitivity_hs282580.csv           (Part 5A)
  - term_leave_one_reporter_hs282580.csv               (Part 6A)
  - term_leave_one_reporter_summary_hs282580.csv       (Part 6B)
  - term_alternative_timing_hs282580.csv               (Part 9)

Run from repo root:
    python 04_scripts/term_paper_robustness_checks.py
"""

from datetime import datetime
from pathlib import Path
import sys
import traceback

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
LOCAL_SP = REPO / ".conda" / "lib" / "python3.12" / "site-packages"
if LOCAL_SP.exists():
    sys.path.insert(0, str(LOCAL_SP))
sys.path.insert(0, str(REPO / "04_scripts"))

from analysis_thesis import (  # noqa: E402
    TREATED, PLACEBOS, PERIODS, PERIOD_INDEX,
    fit_ppml_hdfe, add_case_treatment, add_event_terms, joint_pretrend_test,
    switching_potential_by_reporter, load_comtrade,
)

OUT = REPO / "03_data" / "output" / "tables"
COUNTRY_PANEL = REPO / "03_data" / "processed" / "comtrade_thesis_country_product_month.csv"

CUTOFFS = ["202603", "202512", "202509", "202506", "202503"]
T = "282580"


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def filter_periods(frame, cutoff):
    idx = PERIOD_INDEX[cutoff]
    keep = {p for p in PERIODS if PERIOD_INDEX[p] <= idx}
    return frame[frame["period"].isin(keep)].copy()


# --------------------------------------------------------------------------
# Part 1A: reporting coverage
# --------------------------------------------------------------------------
def reporting_coverage():
    log("Part 1A: reporting coverage")
    cp = pd.read_csv(COUNTRY_PANEL, dtype={"hs": str, "period": str})
    hs_order = ["2504", "811292", "282560", "8110", "261710", "282580",
                "2818", "8111", "2811"]
    rows = []
    for hs in hs_order:
        sub = cp[cp["hs"] == hs]
        for period in sorted(sub["period"].unique()):
            g = sub[sub["period"] == period]
            rows.append({
                "hs": hs,
                "period": period,
                "reporters_total": len(g),
                "reporters_reported": int(g["world_primaryValue_reported"].sum()),
                "coverage": float(g["world_primaryValue_reported"].mean()),
            })
    by_month = pd.DataFrame(rows)
    by_month.to_csv(OUT / "term_reporting_coverage_by_month_hs282580.csv",
                    index=False)

    summary = []
    for hs in hs_order:
        cov = by_month[by_month["hs"] == hs].set_index("period")["coverage"]
        info = TREATED.get(hs, {})
        post = info.get("import_effect", "202401" if hs == "2504" else "202309")
        pre = cov[cov.index < post]
        post_cov = cov[cov.index >= post]
        late6 = cov[cov.index >= "202510"]
        summary.append({
            "hs": hs,
            "post_start": post,
            "pre_mean_coverage": float(pre.mean()) if len(pre) else np.nan,
            "pre_min_coverage": float(pre.min()) if len(pre) else np.nan,
            "post_mean_coverage": float(post_cov.mean()) if len(post_cov) else np.nan,
            "post_min_coverage": float(post_cov.min()) if len(post_cov) else np.nan,
            "last6_mean_coverage": float(late6.mean()) if len(late6) else np.nan,
            "cov_202603": float(cov.get("202603", np.nan)),
            "cov_202512": float(cov.get("202512", np.nan)),
            "cov_202509": float(cov.get("202509", np.nan)),
        })
    sdf = pd.DataFrame(summary)
    sdf.to_csv(OUT / "term_reporting_coverage_by_product.csv", index=False)
    log(f"  coverage summary:\n{sdf.to_string(index=False)}")
    return by_month, sdf


# --------------------------------------------------------------------------
# helpers to run a single static DDD + optional event study + pretrend
# --------------------------------------------------------------------------
def run_static(frame, treated, controls, import_effect, label,
               fe_interactions=None):
    products = [treated, *controls]
    sample = frame[frame["product"].isin(products)].copy()
    sample = add_case_treatment(sample, treated, import_effect)
    try:
        result = fit_ppml_hdfe(sample, "trade_value_usd", ["treatment"],
                               fe_interactions=fe_interactions)
    except Exception as exc:
        return {"sample": label, "error": f"{type(exc).__name__}: {exc}"}
    beta = float(result.beta[0])
    se = float(np.sqrt(max(result.covariance_reporter[0, 0], 0)))
    p = float(2 * (1 - 0.5 * (1 + np.sign(beta) * 0)))  # placeholder
    from scipy.stats import norm
    z = beta / se if se > 0 else np.nan
    p = float(2 * norm.sf(abs(z))) if np.isfinite(z) else np.nan
    # pretrend via event study at import_effect
    ev_data, ev_names, base = add_event_terms(
        sample, treated, import_effect, TREATED[treated]["baseline_event"])
    try:
        ev_result = fit_ppml_hdfe(ev_data, "trade_value_usd", ev_names,
                                  fe_interactions=fe_interactions)
        pt_p, pt_df = joint_pretrend_test(ev_result, base)
    except Exception as exc:
        pt_p, pt_df = np.nan, 0
    return {
        "sample": label,
        "beta": beta,
        "percent_effect": 100 * (np.exp(beta) - 1),
        "se_reporter": se,
        "p_reporter": p,
        "pretrend_p": float(pt_p) if np.isfinite(pt_p) else np.nan,
        "pretrend_df": pt_df,
        "nobs": result.nobs,
        "dropped_separated": result.dropped_separated,
        "reporter_clusters": result.reporter_clusters,
        "product_clusters": result.product_clusters,
        "converged": result.converged,
        "exact_p_floor": 1.0 / result.product_clusters,
    }


# --------------------------------------------------------------------------
# Part 1B + 1C: late-reporting PPML + event study
# --------------------------------------------------------------------------
def late_reporting_ppml(comtrade_full):
    log("Part 1B/1C: truncated PPML + event study for HS 282580")
    static_rows, event_rows = [], []
    info = TREATED[T]
    for cutoff in CUTOFFS:
        log(f"  cutoff {cutoff}")
        frame = filter_periods(comtrade_full, cutoff)
        # static
        srow = run_static(frame, T, PLACEBOS, info["import_effect"],
                          f"282580 through {cutoff}")
        srow["cutoff"] = cutoff
        srow["n_periods"] = frame[frame["product"] == T]["period"].nunique()
        static_rows.append(srow)
        # event study
        products = [T, *PLACEBOS]
        sample = frame[frame["product"].isin(products)].copy()
        sample = add_case_treatment(sample, T, info["import_effect"])
        ev_data, ev_names, base = add_event_terms(
            sample, T, info["import_effect"], info["baseline_event"])
        try:
            ev_result = fit_ppml_hdfe(ev_data, "trade_value_usd", ev_names)
            ev_rows.extend(_coef_rows(ev_result, "PPML DDD event study",
                                      f"282580 through {cutoff}; baseline={base}",
                                      cutoff, base))
        except Exception as exc:
            event_rows.append({"cutoff": cutoff, "error": str(exc)})
    pd.DataFrame(static_rows).to_csv(
        OUT / "term_late_reporting_ppml_hs282580.csv", index=False)
    pd.DataFrame(event_rows).to_csv(
        OUT / "term_late_reporting_eventstudy_hs282580.csv", index=False)
    sdf = pd.DataFrame(static_rows)
    log(f"  static results:\n{sdf[['cutoff','percent_effect','p_reporter','pretrend_p','nobs','converged']].to_string(index=False)}")
    return sdf, pd.DataFrame(event_rows)


def _coef_rows(result, model, sample, cutoff, baseline):
    from scipy.stats import norm
    rows = []
    for i, name in enumerate(result.names):
        beta = float(result.beta[i])
        se = float(np.sqrt(max(result.covariance_reporter[i, i], 0)))
        z = beta / se if se > 0 else np.nan
        p = float(2 * norm.sf(abs(z))) if np.isfinite(z) else np.nan
        rows.append({
            "cutoff": cutoff,
            "model": model,
            "sample": sample,
            "baseline": baseline,
            "term": name,
            "beta": beta,
            "percent_effect": 100 * (np.exp(beta) - 1),
            "se_reporter": se,
            "p_reporter": p,
            "nobs": result.nobs,
        })
    return rows


# --------------------------------------------------------------------------
# Part 1D: switching split under truncations
# --------------------------------------------------------------------------
def late_reporting_switching(comtrade_full):
    log("Part 1D: switching split under truncations for HS 282580")
    info = TREATED[T]
    rows = []
    # A_ik computed on FULL data pre-announcement (unchanged by late cutoff)
    exposure_full = switching_potential_by_reporter(comtrade_full, T, info["announcement"])
    pre_traders = exposure_full[exposure_full["pre_total_trade"] > 0].copy()
    median_a = float(pre_traders["switching_potential"].median())
    pre_traders["switching_group"] = np.where(
        pre_traders["switching_potential"] > median_a,
        "high_switching_potential", "low_switching_potential")
    log(f"  median A (full pre-period) = {median_a:.4f}; "
        f"high={int((pre_traders['switching_group']=='high_switching_potential').sum())}, "
        f"low={int((pre_traders['switching_group']=='low_switching_potential').sum())}")
    for cutoff in ["202603", "202512", "202509"]:
        log(f"  cutoff {cutoff}")
        frame = filter_periods(comtrade_full, cutoff)
        for group, grp_df in pre_traders.groupby("switching_group"):
            reporter_list = set(grp_df["reporter"].astype(str))
            products = [T, *PLACEBOS]
            sample = frame[frame["product"].isin(products) &
                           frame["reporter"].astype(str).isin(reporter_list)].copy()
            sample = add_case_treatment(sample, T, info["import_effect"])
            try:
                result = fit_ppml_hdfe(sample, "trade_value_usd", ["treatment"])
                beta = float(result.beta[0])
                se = float(np.sqrt(max(result.covariance_reporter[0, 0], 0)))
                from scipy.stats import norm
                z = beta / se if se > 0 else np.nan
                p = float(2 * norm.sf(abs(z))) if np.isfinite(z) else np.nan
                # split pretrend
                ev_data, ev_names, base = add_event_terms(
                    sample, T, info["import_effect"], info["baseline_event"])
                ev_result = fit_ppml_hdfe(ev_data, "trade_value_usd", ev_names)
                pt_p, _ = joint_pretrend_test(ev_result, base)
                rows.append({
                    "cutoff": cutoff,
                    "switching_group": group,
                    "reporters_in_split": len(reporter_list),
                    "beta": beta,
                    "percent_effect": 100 * (np.exp(beta) - 1),
                    "se_reporter": se,
                    "p_reporter": p,
                    "pretrend_p": float(pt_p),
                    "nobs": result.nobs,
                    "dropped_separated": result.dropped_separated,
                    "converged": result.converged,
                    "median_A_full_pre": median_a,
                })
            except Exception as exc:
                rows.append({"cutoff": cutoff, "switching_group": group,
                             "error": f"{type(exc).__name__}: {exc}"})
    pd.DataFrame(rows).to_csv(
        OUT / "term_late_reporting_switching_hs282580.csv", index=False)
    log(f"  switching done ({len(rows)} rows)")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Part 1E: reported-only
# --------------------------------------------------------------------------
def reported_only(comtrade_full):
    log("Part 1E: reported-only PPML for HS 282580")
    cp = pd.read_csv(COUNTRY_PANEL, dtype={"hs": str, "period": str})
    # comtrade_full has "product" (renamed from hs); country panel has "hs"
    rep_flag = cp[["reporterCode", "period", "hs", "world_primaryValue_reported"]].copy()
    rep_flag = rep_flag.rename(columns={"reporterCode": "reporter", "hs": "product"})
    rep_flag["reporter"] = rep_flag["reporter"].astype(str)
    merged = comtrade_full.merge(rep_flag, on=["reporter", "period", "product"], how="left")
    reported_only_df = merged[merged["world_primaryValue_reported"].fillna(False)].copy()
    log(f"  reported-only rows: {len(reported_only_df)} / {len(merged)} "
        f"({100*len(reported_only_df)/len(merged):.1f}%)")
    rows = []
    for cutoff in ["202603", "202512", "202509"]:
        log(f"  cutoff {cutoff}")
        frame = filter_periods(reported_only_df, cutoff)
        info = TREATED[T]
        srow = run_static(frame, T, PLACEBOS, info["import_effect"],
                          f"282580 reported-only through {cutoff}")
        srow["cutoff"] = cutoff
        srow["n_periods"] = frame[frame["product"] == T]["period"].nunique()
        rows.append(srow)
    pd.DataFrame(rows).to_csv(
        OUT / "term_reported_only_ppml_hs282580.csv", index=False)
    log(f"  reported-only done")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Part 5: donor-pool sensitivity
# --------------------------------------------------------------------------
def donor_sensitivity(comtrade_full):
    log("Part 5: donor-pool sensitivity for HS 282580")
    info = TREATED[T]
    configs = [
        ("baseline_3ctrl", ["2818", "8111", "2811"]),
        ("drop_2818", ["8111", "2811"]),
        ("drop_8111", ["2818", "2811"]),
        ("drop_2811", ["2818", "8111"]),
        ("only_2818", ["2818"]),
        ("only_8111", ["8111"]),
        ("only_2811", ["2811"]),
    ]
    rows = []
    for name, controls in configs:
        log(f"  {name}: controls={controls}")
        srow = run_static(comtrade_full, T, controls, info["import_effect"],
                          f"282580 [{name}]")
        srow["config"] = name
        srow["controls"] = ",".join(controls)
        srow["n_controls"] = len(controls)
        rows.append(srow)
    pd.DataFrame(rows).to_csv(
        OUT / "term_donor_pool_sensitivity_hs282580.csv", index=False)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Part 6: leave-one-reporter-out
# --------------------------------------------------------------------------
def leave_one_reporter(comtrade_full):
    log("Part 6: leave-one-reporter-out for HS 282580")
    info = TREATED[T]
    products = [T, *PLACEBOS]
    base_sample = comtrade_full[comtrade_full["product"].isin(products)].copy()
    reporters = sorted(base_sample["reporter"].astype(str).unique())
    log(f"  {len(reporters)} reporters")
    rows = []
    for i, drop in enumerate(reporters):
        if i % 10 == 0:
            log(f"  LORO {i+1}/{len(reporters)} dropping {drop}")
        sub = base_sample[base_sample["reporter"].astype(str) != drop].copy()
        srow = run_static(sub, T, PLACEBOS, info["import_effect"],
                          f"282580 drop {drop}")
        srow["dropped_reporter"] = drop
        rows.append(srow)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "term_leave_one_reporter_hs282580.csv", index=False)
    # summary
    ok = df[df.get("beta", pd.Series(dtype=float)).notna() & ~df.get("beta", pd.Series(dtype=float)).apply(lambda x: isinstance(x, str))] if "beta" in df.columns else df
    numeric = df.dropna(subset=["beta"]).copy() if "beta" in df.columns else df
    if "percent_effect" in numeric.columns and len(numeric):
        summary = {
            "baseline_effect_pct": 100 * (np.exp(float(TREATED[T].get("beta_ref", 0))) - 1),
            "baseline_observed_pct": -81.5,
            "min_loo_pct": float(numeric["percent_effect"].min()),
            "max_loo_pct": float(numeric["percent_effect"].max()),
            "median_loo_pct": float(numeric["percent_effect"].median()),
            "n_negative": int((numeric["percent_effect"] < 0).sum()),
            "n_below_minus50": int((numeric["percent_effect"] < -50).sum()),
            "n_below_minus75": int((numeric["percent_effect"] < -75).sum()),
            "n_total": len(numeric),
            "reporter_most_weakening": str(numeric.loc[numeric["percent_effect"].idxmax(), "dropped_reporter"]) if len(numeric) else "",
            "reporter_most_strengthening": str(numeric.loc[numeric["percent_effect"].idxmin(), "dropped_reporter"]) if len(numeric) else "",
            "n_failed": int(len(df) - len(numeric)),
        }
    else:
        summary = {"error": "no successful fits"}
    pd.DataFrame([summary]).to_csv(
        OUT / "term_leave_one_reporter_summary_hs282580.csv", index=False)
    log(f"  summary: {summary}")
    return df, pd.DataFrame([summary])


# --------------------------------------------------------------------------
# Part 9: alternative timing
# --------------------------------------------------------------------------
def alternative_timing(comtrade_full):
    log("Part 9: alternative timing for HS 282580")
    info = TREATED[T]
    rows = []
    for anchor_key in ["announcement", "implementation", "import_effect"]:
        post = info[anchor_key]
        log(f"  anchor {anchor_key} = {post}")
        srow = run_static(comtrade_full, T, PLACEBOS, post,
                          f"282580 post@{anchor_key}({post})")
        srow["timing_anchor"] = anchor_key
        srow["post_month"] = post
        rows.append(srow)
    pd.DataFrame(rows).to_csv(
        OUT / "term_alternative_timing_hs282580.csv", index=False)
    return pd.DataFrame(rows)


def _exists(*names):
    return all((OUT / n).exists() for n in names)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = datetime.now()
    log(f"START {t0}")
    comtrade = load_comtrade()
    log(f"loaded comtrade source panel: {len(comtrade)} rows")

    if not _exists("term_reporting_coverage_by_product.csv",
                   "term_reporting_coverage_by_month_hs282580.csv"):
        reporting_coverage()
    if not _exists("term_late_reporting_ppml_hs282580.csv",
                   "term_late_reporting_eventstudy_hs282580.csv"):
        late_reporting_ppml(comtrade)
    if not _exists("term_late_reporting_switching_hs282580.csv"):
        late_reporting_switching(comtrade)
    if not _exists("term_reported_only_ppml_hs282580.csv"):
        reported_only(comtrade)
    if not _exists("term_donor_pool_sensitivity_hs282580.csv"):
        donor_sensitivity(comtrade)
    if not _exists("term_leave_one_reporter_hs282580.csv"):
        leave_one_reporter(comtrade)
    if not _exists("term_alternative_timing_hs282580.csv"):
        alternative_timing(comtrade)

    log(f"DONE in {datetime.now() - t0}")


if __name__ == "__main__":
    main()
