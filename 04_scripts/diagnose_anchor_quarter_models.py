#!/usr/bin/env python3
"""
Anchor and quarterly diagnostics for the pressure-panel PPML design.

This script is exploratory. It compares announcement, implementation, and
import-effect timing for:
- monthly source-share PPML average effects;
- monthly local-window event-study pretrend tests;
- quarterly source-share PPML average effects;
- quarterly local-window event-study pretrend tests.

The purpose is to distinguish timing assumptions from substantive results.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


REPO = Path(__file__).resolve().parents[1]
LOCAL_SITE_PACKAGES = REPO / ".conda" / "lib" / "python3.12" / "site-packages"
if LOCAL_SITE_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

import pyfixest as pf


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"
PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"

CONTROL_ROLE = "candidate_control_pending_screen"

GROUPS = {
    "wave2_graphite": {
        "family": "wave",
        "label": "Wave 2 graphite",
        "treated_hs": ["2504"],
        "announcement_month": "202310",
        "implementation_month": "202312",
        "import_effect_month": "202401",
    },
    "wave3_antimony_clean": {
        "family": "wave",
        "label": "Wave 3 antimony metal",
        "treated_hs": ["8110"],
        "announcement_month": "202408",
        "implementation_month": "202409",
        "import_effect_month": "202410",
    },
    "wave4_w_bi": {
        "family": "wave",
        "label": "Wave 4 W/Bi",
        "treated_hs": ["8106", "284180"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
    "hs2504_graphite": {
        "family": "product",
        "label": "HS 2504 graphite",
        "treated_hs": ["2504"],
        "announcement_month": "202310",
        "implementation_month": "202312",
        "import_effect_month": "202401",
    },
    "hs8110_antimony_metal": {
        "family": "product",
        "label": "HS 8110 antimony metal",
        "treated_hs": ["8110"],
        "announcement_month": "202408",
        "implementation_month": "202409",
        "import_effect_month": "202410",
    },
    "hs8106_bismuth": {
        "family": "product",
        "label": "HS 8106 bismuth",
        "treated_hs": ["8106"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
    "hs284180_tungstates": {
        "family": "product",
        "label": "HS 284180 tungstates",
        "treated_hs": ["284180"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
}

ANCHORS = {
    "announcement": "announcement_month",
    "implementation": "implementation_month",
    "import_effect": "import_effect_month",
}

MONTHLY_FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
    "fe_importer_product_source",
]

QUARTERLY_FE = [
    "fe_importer_quarter",
    "fe_product_quarter",
    "fe_source_quarter",
    "fe_importer_product_source",
]


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def month_index(period: str) -> int:
    return int(period[:4]) * 12 + int(period[4:6])


def month_to_quarter(period: str) -> str:
    year = int(period[:4])
    month = int(period[4:6])
    q = (month - 1) // 3 + 1
    return f"{year}Q{q}"


def quarter_index(q: str) -> int:
    return int(q[:4]) * 4 + int(q[-1])


def add_time_columns(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    out["period"] = out["period"].astype(str)
    out["month_index"] = out["period"].map(month_index)
    out["quarter"] = out["period"].map(month_to_quarter)
    out["quarter_index"] = out["quarter"].map(quarter_index)
    return out


def load_monthly_panel() -> pd.DataFrame:
    panel = pd.read_csv(PANEL_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    return add_time_columns(panel)


def make_quarterly_panel(monthly: pd.DataFrame) -> pd.DataFrame:
    meta_cols = [
        "product",
        "analysis_role",
        "policy_screened",
        "wave",
        "policy_episode",
        "announcement_date",
        "implementation_date",
        "import_effect_month",
        "treatment_status",
        "scope_status",
        "usable_as_control",
        "e_china_exposure",
        "o_row_frequency",
        "o_row_capacity",
        "p_switch_frequency",
        "p_compress_frequency",
        "p_switch_capacity",
        "p_compress_capacity",
        "p_switch_absorptive",
        "p_compress_absorptive",
    ]
    for col in meta_cols:
        if col not in monthly.columns:
            monthly[col] = np.nan
    group_cols = ["reporterCode", "quarter", "hs", "source", "china_source"]
    q = (
        monthly.groupby(group_cols, as_index=False)
        .agg(
            trade_value_usd=("trade_value_usd", "sum"),
            net_weight_kg=("net_weight_kg", "sum"),
            **{col: (col, "first") for col in meta_cols},
        )
        .copy()
    )
    q["quarter_index"] = q["quarter"].map(quarter_index)
    q["fe_importer_quarter"] = q["reporterCode"].astype(str) + "_" + q["quarter"]
    q["fe_product_quarter"] = q["hs"].astype(str) + "_" + q["quarter"]
    q["fe_source_quarter"] = q["source"].astype(str) + "_" + q["quarter"]
    q["fe_importer_product_source"] = (
        q["reporterCode"].astype(str) + "_" + q["hs"].astype(str) + "_" + q["source"]
    )
    return q


def group_sample(panel: pd.DataFrame, group_key: str) -> pd.DataFrame:
    info = GROUPS[group_key]
    treated_hs = set(info["treated_hs"])
    sample = panel.loc[
        panel["analysis_role"].eq(CONTROL_ROLE) | panel["hs"].isin(treated_hs)
    ].copy()
    sample["treated_group"] = sample["hs"].isin(treated_hs)
    return sample


def fit_ppml(data: pd.DataFrame, outcome: str, x_cols: list[str], fe_cols: list[str]):
    work = data[[outcome, "reporterCode", "hs", *x_cols, *fe_cols]].dropna().copy()
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(fe_cols)}"
    model = pf.fepois(
        formula,
        work,
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
    return model, coef, se, vcov, len(work)


def joint_test(coef: pd.Series, vcov: pd.DataFrame, terms: list[str]):
    terms = [t for t in terms if t in coef.index and np.isfinite(coef.loc[t])]
    if not terms:
        return np.nan, 0, np.nan
    b = coef.reindex(terms).astype(float).to_numpy()
    v = vcov.reindex(index=terms, columns=terms).astype(float).to_numpy()
    stat = float(b.T @ np.linalg.pinv(v) @ b)
    df = len(terms)
    return stat, df, float(chi2.sf(stat, df))


def run_average_monthly(monthly: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(monthly, group_key)
        for anchor, field in ANCHORS.items():
            anchor_month = info[field]
            work = sample.copy()
            work["D"] = (
                work["treated_group"]
                & work["china_source"]
                & work["period"].ge(anchor_month)
            ).astype(int)
            print(f"Monthly PPML {group_key} anchor={anchor}", flush=True)
            model, coef, se, _, input_rows = fit_ppml(
                work, "trade_value_usd", ["D"], MONTHLY_FE
            )
            beta = float(coef.loc["D"])
            stderr = float(se.loc["D"])
            rows.append(
                {
                    "frequency": "monthly",
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "anchor": anchor,
                    "anchor_period": anchor_month,
                    "coef": beta,
                    "se_reporter": stderr,
                    "p_reporter": p_value(beta, stderr),
                    "percent_effect": percent_effect(beta),
                    "nobs": int(model._N),
                    "input_rows": input_rows,
                    "dropped_separation": input_rows - int(model._N),
                }
            )
    return pd.DataFrame(rows)


def run_average_quarterly(quarterly: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(quarterly, group_key)
        for anchor, field in ANCHORS.items():
            anchor_q = month_to_quarter(info[field])
            work = sample.copy()
            work["D"] = (
                work["treated_group"]
                & work["china_source"]
                & work["quarter"].map(quarter_index).ge(quarter_index(anchor_q))
            ).astype(int)
            print(f"Quarterly PPML {group_key} anchor={anchor}", flush=True)
            model, coef, se, _, input_rows = fit_ppml(
                work, "trade_value_usd", ["D"], QUARTERLY_FE
            )
            beta = float(coef.loc["D"])
            stderr = float(se.loc["D"])
            rows.append(
                {
                    "frequency": "quarterly",
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "anchor": anchor,
                    "anchor_period": anchor_q,
                    "coef": beta,
                    "se_reporter": stderr,
                    "p_reporter": p_value(beta, stderr),
                    "percent_effect": percent_effect(beta),
                    "nobs": int(model._N),
                    "input_rows": input_rows,
                    "dropped_separation": input_rows - int(model._N),
                }
            )
    return pd.DataFrame(rows)


def run_monthly_event(monthly: pd.DataFrame, window: int = 12, base: int = -1) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(monthly, group_key)
        for anchor, field in ANCHORS.items():
            anchor_month = info[field]
            anchor_idx = month_index(anchor_month)
            work = sample.copy()
            work["event_time"] = work["month_index"] - anchor_idx
            work = work.loc[work["event_time"].between(-window, window)].copy()
            x_cols = []
            term_to_k = {}
            for k in range(-window, window + 1):
                if k == base:
                    continue
                name = f"event_m{abs(k)}" if k < 0 else f"event_p{k}"
                work[name] = (
                    work["treated_group"]
                    & work["china_source"]
                    & work["event_time"].eq(k)
                ).astype(int)
                x_cols.append(name)
                term_to_k[name] = k
            pre_terms = [term for term, k in term_to_k.items() if k < 0]
            print(f"Monthly event {group_key} anchor={anchor}", flush=True)
            model, coef, se, vcov, input_rows = fit_ppml(
                work, "trade_value_usd", x_cols, MONTHLY_FE
            )
            stat, df, p = joint_test(coef, vcov, pre_terms)
            rows.append(
                {
                    "frequency": "monthly",
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "anchor": anchor,
                    "anchor_period": anchor_month,
                    "window": window,
                    "base_event_time": base,
                    "pretrend_chi2": stat,
                    "pretrend_df": df,
                    "pretrend_p": p,
                    "max_abs_pre_coef": float(
                        max(abs(float(coef.loc[t])) for t in pre_terms)
                    ),
                    "min_pre_p": float(
                        min(p_value(float(coef.loc[t]), float(se.loc[t])) for t in pre_terms)
                    ),
                    "nobs": int(model._N),
                    "input_rows": input_rows,
                    "dropped_separation": input_rows - int(model._N),
                }
            )
    return pd.DataFrame(rows)


def run_quarterly_event(quarterly: pd.DataFrame, window: int = 4, base: int = -1) -> pd.DataFrame:
    rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(quarterly, group_key)
        for anchor, field in ANCHORS.items():
            anchor_q = month_to_quarter(info[field])
            anchor_idx = quarter_index(anchor_q)
            work = sample.copy()
            work["event_time"] = work["quarter_index"] - anchor_idx
            work = work.loc[work["event_time"].between(-window, window)].copy()
            x_cols = []
            term_to_k = {}
            for k in range(-window, window + 1):
                if k == base:
                    continue
                name = f"event_qm{abs(k)}" if k < 0 else f"event_qp{k}"
                work[name] = (
                    work["treated_group"]
                    & work["china_source"]
                    & work["event_time"].eq(k)
                ).astype(int)
                x_cols.append(name)
                term_to_k[name] = k
            pre_terms = [term for term, k in term_to_k.items() if k < 0]
            print(f"Quarterly event {group_key} anchor={anchor}", flush=True)
            model, coef, se, vcov, input_rows = fit_ppml(
                work, "trade_value_usd", x_cols, QUARTERLY_FE
            )
            stat, df, p = joint_test(coef, vcov, pre_terms)
            rows.append(
                {
                    "frequency": "quarterly",
                    "group_key": group_key,
                    "group_family": info["family"],
                    "group_label": info["label"],
                    "anchor": anchor,
                    "anchor_period": anchor_q,
                    "window": window,
                    "base_event_time": base,
                    "pretrend_chi2": stat,
                    "pretrend_df": df,
                    "pretrend_p": p,
                    "max_abs_pre_coef": float(
                        max(abs(float(coef.loc[t])) for t in pre_terms)
                    ),
                    "min_pre_p": float(
                        min(p_value(float(coef.loc[t]), float(se.loc[t])) for t in pre_terms)
                    ),
                    "nobs": int(model._N),
                    "input_rows": input_rows,
                    "dropped_separation": input_rows - int(model._N),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    monthly = load_monthly_panel()
    quarterly = make_quarterly_panel(monthly)

    monthly_avg = run_average_monthly(monthly)
    quarterly_avg = run_average_quarterly(quarterly)
    monthly_event = run_monthly_event(monthly)
    quarterly_event = run_quarterly_event(quarterly)

    avg = pd.concat([monthly_avg, quarterly_avg], ignore_index=True)
    event = pd.concat([monthly_event, quarterly_event], ignore_index=True)
    avg.to_csv(TABLES / "anchor_quarter_average_ppml.csv", index=False)
    event.to_csv(TABLES / "anchor_quarter_event_pretrend.csv", index=False)

    print("\nAverage PPML:")
    print(avg.to_string(index=False))
    print("\nEvent pretrend:")
    print(event.to_string(index=False))


if __name__ == "__main__":
    main()
