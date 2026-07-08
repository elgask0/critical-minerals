#!/usr/bin/env python3
"""
Timing and robustness checks for wave/product source-share PPML models.

Outputs:
- event-study coefficients and plots;
- joint pretrend tests for pre-policy event terms;
- placebo-date PPML estimates using only pre-real-policy data;
- U.S. interaction estimates;
- net-weight PPML estimates for usable net-weight rows.
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


REPO = Path(__file__).resolve().parents[1]
LOCAL_SITE_PACKAGES = REPO / ".conda" / "lib" / "python3.12" / "site-packages"
if LOCAL_SITE_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

try:
    import pyfixest as pf
except ImportError as exc:
    raise ImportError(
        "estimate_pressure_timing_robustness.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"
FIGURES = REPO / "03_data" / "output" / "figures"

PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"

EVENT_RESULTS_PATH = TABLES / "pressure_event_study_results.csv"
PRETREND_RESULTS_PATH = TABLES / "pressure_event_study_pretrend_tests.csv"
PLACEBO_RESULTS_PATH = TABLES / "pressure_placebo_date_results.csv"
US_RESULTS_PATH = TABLES / "pressure_us_interaction_results.csv"
NET_WEIGHT_RESULTS_PATH = TABLES / "pressure_net_weight_ppml_results.csv"


CONTROL_ROLE = "candidate_control_pending_screen"
US_REPORTER_CODE = 842

GROUPS = {
    "wave2_graphite": {
        "family": "wave",
        "label": "Wave 2 graphite",
        "treated_hs": ["2504"],
        "post_month": "202401",
    },
    "wave3_antimony_clean": {
        "family": "wave",
        "label": "Wave 3 antimony metal",
        "treated_hs": ["8110"],
        "post_month": "202410",
    },
    "wave4_w_bi": {
        "family": "wave",
        "label": "Wave 4 W/Bi",
        "treated_hs": ["8106", "284180"],
        "post_month": "202503",
    },
    "hs2504_graphite": {
        "family": "product",
        "label": "HS 2504 graphite",
        "treated_hs": ["2504"],
        "post_month": "202401",
    },
    "hs8110_antimony_metal": {
        "family": "product",
        "label": "HS 8110 antimony metal",
        "treated_hs": ["8110"],
        "post_month": "202410",
    },
    "hs8106_bismuth": {
        "family": "product",
        "label": "HS 8106 bismuth",
        "treated_hs": ["8106"],
        "post_month": "202503",
    },
    "hs284180_tungstates": {
        "family": "product",
        "label": "HS 284180 tungstates",
        "treated_hs": ["284180"],
        "post_month": "202503",
    },
}

FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
    "fe_importer_product_source",
]

EVENT_MIN = -12
EVENT_MAX = 12
EVENT_BASE = -1


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def add_month_index(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["month_index"] = out["period"].str.slice(0, 4).astype(int) * 12 + out[
        "period"
    ].str.slice(4, 6).astype(int)
    return out


def month_to_index(period: str) -> int:
    return int(period[:4]) * 12 + int(period[4:6])


def shift_period(period: str, months: int) -> str:
    idx = month_to_index(period) + months
    year = (idx - 1) // 12
    month = idx - year * 12
    return f"{year:04d}{month:02d}"


def load_panel() -> pd.DataFrame:
    panel = pd.read_csv(PANEL_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    return add_month_index(panel)


def group_sample(panel: pd.DataFrame, group_key: str) -> pd.DataFrame:
    info = GROUPS[group_key]
    treated_hs = set(info["treated_hs"])
    sample = panel.loc[
        panel["analysis_role"].eq(CONTROL_ROLE) | panel["hs"].isin(treated_hs)
    ].copy()
    sample["group_key"] = group_key
    sample["group_label"] = info["label"]
    sample["group_family"] = info["family"]
    sample["treated_group"] = sample["hs"].isin(treated_hs)
    sample["post_group"] = sample["period"].ge(info["post_month"])
    sample["D_group"] = (
        sample["treated_group"] & sample["china_source"] & sample["post_group"]
    ).astype(int)
    return sample


def fit_model(work: pd.DataFrame, outcome: str, x_cols: list[str]) -> tuple[object, pd.Series, pd.Series, pd.DataFrame]:
    data = work[[outcome, "reporterCode", "hs", *x_cols, *FE]].dropna().copy()
    data["reporter_cluster"] = data["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(FE)}"
    model = pf.fepois(
        formula,
        data,
        vcov={"CRV1": "reporter_cluster"},
        separation_check=["fe"],
        iwls_maxiter=80,
        iwls_tol=1e-7,
        fixef_tol=1e-7,
        fixef_maxiter=100000,
        demeaner_backend="numba",
        lean=False,
    )
    coef = model.coef().reindex(x_cols)
    vcov = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se = pd.Series(np.sqrt(np.diag(vcov)), index=coef.index)
    return model, coef, se, vcov


def event_terms(sample: pd.DataFrame, post_month: str) -> tuple[pd.DataFrame, list[str], dict[str, int]]:
    out = sample.copy()
    rel = out["month_index"] - month_to_index(post_month)
    out["event_time"] = rel
    x_cols = []
    term_to_k = {}
    for k in range(EVENT_MIN, EVENT_MAX + 1):
        if k == EVENT_BASE:
            continue
        name = f"event_m{abs(k)}" if k < 0 else f"event_p{k}"
        out[name] = (
            out["treated_group"] & out["china_source"] & out["event_time"].eq(k)
        ).astype(int)
        x_cols.append(name)
        term_to_k[name] = k
    return out, x_cols, term_to_k


def joint_pretrend_test(coef: pd.Series, vcov: pd.DataFrame, terms: list[str]) -> tuple[float, int, float]:
    if not terms:
        return np.nan, 0, np.nan
    b = coef.reindex(terms).astype(float).to_numpy()
    v = vcov.reindex(index=terms, columns=terms).astype(float).to_numpy()
    stat = float(b.T @ np.linalg.pinv(v) @ b)
    df = len(terms)
    p = float(chi2.sf(stat, df))
    return stat, df, p


def plot_event(group_key: str, label: str, results: pd.DataFrame) -> str:
    sub = results[results["group_key"].eq(group_key)].sort_values("event_time")
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(-0.5, color="grey", linestyle="--", linewidth=0.8)
    ax.errorbar(
        sub["event_time"],
        sub["coef"],
        yerr=1.96 * sub["se_reporter"],
        fmt="o-",
        linewidth=1.2,
        markersize=3,
        color="#1f5f99",
        ecolor="#7aa6c2",
        capsize=2,
    )
    ax.set_title(label)
    ax.set_xlabel("Months relative to import-effect month")
    ax.set_ylabel("China-source event coefficient")
    ax.set_xticks(list(range(EVENT_MIN, EVENT_MAX + 1, 3)))
    fig.tight_layout()
    out = FIGURES / f"event_study_{group_key}.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return str(out)


def run_event_studies(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    FIGURES.mkdir(parents=True, exist_ok=True)
    all_rows = []
    pre_rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(panel, group_key)
        event_sample, x_cols, term_to_k = event_terms(sample, info["post_month"])
        print(f"Event study {group_key} ...", flush=True)
        model, coef, se, vcov = fit_model(event_sample, "trade_value_usd", x_cols)
        pre_terms = [term for term, k in term_to_k.items() if k < EVENT_BASE]
        stat, df, p = joint_pretrend_test(coef, vcov, pre_terms)
        rows = []
        for term in x_cols:
            beta = float(coef.loc[term])
            stderr = float(se.loc[term])
            rows.append(
                {
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "treated_hs": ",".join(info["treated_hs"]),
                    "post_month": info["post_month"],
                    "event_time": term_to_k[term],
                    "term": term,
                    "coef": beta,
                    "se_reporter": stderr,
                    "p_reporter": p_value(beta, stderr),
                    "percent_effect": percent_effect(beta),
                    "nobs": int(model._N),
                    "dropped_separation": int(len(event_sample) - int(model._N)),
                }
            )
        all_rows.extend(rows)
        event_df = pd.DataFrame(rows)
        fig_path = plot_event(group_key, info["label"], event_df)
        pre_rows.append(
            {
                "group_key": group_key,
                "group_family": info["family"],
                "group_label": info["label"],
                "treated_hs": ",".join(info["treated_hs"]),
                "post_month": info["post_month"],
                "pretrend_chi2": stat,
                "pretrend_df": df,
                "pretrend_p": p,
                "max_abs_pre_coef": float(
                    event_df.loc[event_df["event_time"].lt(0), "coef"].abs().max()
                ),
                "min_pre_p": float(
                    event_df.loc[event_df["event_time"].lt(0), "p_reporter"].min()
                ),
                "figure_path": fig_path,
                "nobs": int(model._N),
            }
        )
    return pd.DataFrame(all_rows), pd.DataFrame(pre_rows)


def run_placebo_dates(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        base = group_sample(panel, group_key)
        for lag in [-24, -12]:
            fake_month = shift_period(info["post_month"], lag)
            sample = base.loc[base["period"].lt(info["post_month"])].copy()
            sample["D_placebo"] = (
                sample["treated_group"] & sample["china_source"] & sample["period"].ge(fake_month)
            ).astype(int)
            if sample["D_placebo"].sum() == 0:
                continue
            print(f"Placebo {group_key} {fake_month} ...", flush=True)
            model, coef, se, _ = fit_model(sample, "trade_value_usd", ["D_placebo"])
            beta = float(coef.loc["D_placebo"])
            stderr = float(se.loc["D_placebo"])
            rows.append(
                {
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "treated_hs": ",".join(info["treated_hs"]),
                    "real_post_month": info["post_month"],
                    "placebo_month": fake_month,
                    "placebo_lag_months": lag,
                    "coef": beta,
                    "se_reporter": stderr,
                    "p_reporter": p_value(beta, stderr),
                    "percent_effect": percent_effect(beta),
                    "nobs": int(model._N),
                    "dropped_separation": int(len(sample) - int(model._N)),
                }
            )
    return pd.DataFrame(rows)


def linear_combo(beta: pd.Series, vcov: pd.DataFrame, terms: list[str]) -> tuple[float, float, float]:
    b = float(beta.reindex(terms).sum())
    v = vcov.reindex(index=terms, columns=terms).to_numpy()
    weights = np.ones(len(terms))
    se = float(np.sqrt(weights.T @ v @ weights))
    return b, se, p_value(b, se)


def run_us_interactions(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(panel, group_key)
        sample["is_us"] = sample["reporterCode"].eq(US_REPORTER_CODE)
        sample["D_us"] = sample["D_group"] * sample["is_us"].astype(int)
        print(f"US interaction {group_key} ...", flush=True)
        model, coef, se, vcov = fit_model(sample, "trade_value_usd", ["D_group", "D_us"])
        non_us_beta = float(coef.loc["D_group"])
        non_us_se = float(se.loc["D_group"])
        us_beta, us_se, us_p = linear_combo(coef, vcov, ["D_group", "D_us"])
        inter_beta = float(coef.loc["D_us"])
        inter_se = float(se.loc["D_us"])
        for estimate, beta, stderr, p in [
            ("non_us_effect", non_us_beta, non_us_se, p_value(non_us_beta, non_us_se)),
            ("us_increment", inter_beta, inter_se, p_value(inter_beta, inter_se)),
            ("us_total_effect", us_beta, us_se, us_p),
        ]:
            rows.append(
                {
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "treated_hs": ",".join(info["treated_hs"]),
                    "post_month": info["post_month"],
                    "estimate": estimate,
                    "coef": beta,
                    "se_reporter": stderr,
                    "p_reporter": p,
                    "percent_effect": percent_effect(beta),
                    "nobs": int(model._N),
                    "dropped_separation": int(len(sample) - int(model._N)),
                }
            )
    return pd.DataFrame(rows)


def run_net_weight(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(panel, group_key)
        sample = sample.loc[
            sample["net_weight_usable"].eq(True)
            & sample["net_weight_kg"].notna()
            & sample["net_weight_kg"].ge(0)
        ].copy()
        if sample.empty or sample["D_group"].sum() == 0:
            continue
        print(f"Net weight {group_key} ...", flush=True)
        model, coef, se, _ = fit_model(sample, "net_weight_kg", ["D_group"])
        beta = float(coef.loc["D_group"])
        stderr = float(se.loc["D_group"])
        rows.append(
            {
                "group_key": group_key,
                "group_family": info["family"],
                "group_label": info["label"],
                "treated_hs": ",".join(info["treated_hs"]),
                "post_month": info["post_month"],
                "coef": beta,
                "se_reporter": stderr,
                "p_reporter": p_value(beta, stderr),
                "percent_effect": percent_effect(beta),
                "nobs": int(model._N),
                "input_rows": len(sample),
                "dropped_separation": int(len(sample) - int(model._N)),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    panel = load_panel()

    event_results, pretrend_results = run_event_studies(panel)
    placebo_results = run_placebo_dates(panel)
    us_results = run_us_interactions(panel)
    net_weight_results = run_net_weight(panel)

    event_results.to_csv(EVENT_RESULTS_PATH, index=False)
    pretrend_results.to_csv(PRETREND_RESULTS_PATH, index=False)
    placebo_results.to_csv(PLACEBO_RESULTS_PATH, index=False)
    us_results.to_csv(US_RESULTS_PATH, index=False)
    net_weight_results.to_csv(NET_WEIGHT_RESULTS_PATH, index=False)

    print(f"Wrote {EVENT_RESULTS_PATH}")
    print(f"Wrote {PRETREND_RESULTS_PATH}")
    print(f"Wrote {PLACEBO_RESULTS_PATH}")
    print(f"Wrote {US_RESULTS_PATH}")
    print(f"Wrote {NET_WEIGHT_RESULTS_PATH}")
    print("\nPretrend tests:")
    print(pretrend_results.to_string(index=False))
    print("\nPlacebo dates:")
    print(placebo_results.to_string(index=False))
    print("\nUS interactions:")
    print(us_results.to_string(index=False))
    print("\nNet-weight PPML:")
    print(net_weight_results.to_string(index=False))


if __name__ == "__main__":
    main()
