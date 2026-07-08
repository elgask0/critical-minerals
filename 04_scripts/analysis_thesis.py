"""
Thesis-stage causal analysis for China's critical-mineral export controls.

This script replaces raw-row summation and HC1 inference with:

1. PPML on a balanced importer-product-source-month panel.
2. High-dimensional pairwise fixed effects estimated with pyfixest/fepois.
3. Reporter-clustered uncertainty as a conditional diagnostic.
4. Exact placebo-assignment ranks and warnings about the small number of
   product-level treatment shocks.
5. Implementation-centered dynamic event studies that retain anticipation.
6. Eurostat CN8 PPML analyses for Ga and Ge separately and jointly.
7. Constrained SCM and Synthetic DiD diagnostics using the current donor pool.

Product-level randomization inference cannot attain conventional significance
with only three Comtrade placebo products (minimum exact p = 0.25 for a
single treated product) or two Eurostat placebo products.
"""

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2, norm
import statsmodels.api as sm


REPO = Path(__file__).resolve().parent.parent
LOCAL_SITE_PACKAGES = (
    REPO / ".conda" / "lib" / "python3.12" / "site-packages"
)
if LOCAL_SITE_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

try:
    import pyfixest as pf
except ImportError as exc:
    raise ImportError(
        "analysis_thesis.py requires pyfixest in the repository-local prefix. "
        "Install it with: python -m pip install --prefix ./.conda "
        "pyfixest==0.40.1"
    ) from exc

PROCESSED = REPO / "03_data" / "processed"
RAW = REPO / "03_data" / "raw"
OUTPUT = REPO / "03_data" / "output" / "tables"

COMTRADE_SOURCE = PROCESSED / "comtrade_thesis_source_panel.csv"
EUROSTAT_COUNTRY = PROCESSED / "eurostat_cn8_eu27_country_month.csv"

PLACEBOS = ["2818", "8111", "2811"]
TREATED = {
    "2504": {
        "label": "Natural graphite",
        "implementation": "202312",
        "import_effect": "202401",
        "announcement": "202310",
        "baseline_event": -4,
    },
    "811292": {
        "label": "Ga/Ge bundle",
        "implementation": "202308",
        "import_effect": "202309",
        "announcement": "202307",
        "baseline_event": -3,
    },
    "282560": {
        "label": "GeO2/ZrO2",
        "implementation": "202308",
        "import_effect": "202309",
        "announcement": "202307",
        "baseline_event": -3,
    },
    "8110": {
        "label": "Antimony metal",
        "implementation": "202409",
        "import_effect": "202410",
        "announcement": "202408",
        "baseline_event": -3,
    },
    "261710": {
        "label": "Antimony ores/concentrates",
        "implementation": "202409",
        "import_effect": "202410",
        "announcement": "202408",
        "baseline_event": -3,
        "status": "Sparse upstream antimony series; interpret as value-chain evidence.",
    },
    "282580": {
        "label": "Antimony oxides",
        "implementation": "202409",
        "import_effect": "202410",
        "announcement": "202408",
        "baseline_event": -3,
        "status": "HS-6 partial treatment: only high-purity antimony oxides are controlled.",
    },
}
EXPORT_CASES = {
    **TREATED,
    "3801": {
        "label": "Artificial/colloidal graphite",
        "implementation": "202312",
        "status": "Partially treated product; descriptive robustness only.",
    },
}
PERIODS = [
    f"{year}{month:02d}"
    for year in range(2019, 2026)
    for month in range(1, 13)
] + [f"2026{month:02d}" for month in range(1, 4)]
PERIOD_INDEX = {period: index for index, period in enumerate(PERIODS)}


@dataclass
class PPMLResult:
    beta: np.ndarray
    covariance_reporter: np.ndarray
    covariance_product: np.ndarray
    names: list
    nobs: int
    dropped_separated: int
    iterations: int
    converged: bool
    product_clusters: int
    reporter_clusters: int
    deviance: float


def fit_ppml_hdfe(
    frame,
    outcome,
    x_columns,
    fe_interactions=None,
    max_iter=60,
    tolerance=1e-7,
):
    columns = [
        "reporter",
        "product",
        "period",
        "source",
        outcome,
        *x_columns,
    ]
    work = frame[columns].dropna().copy()
    work["calendar_month"] = work["period"].str[-2:]
    interactions = fe_interactions or {
        "fe_ip": ["reporter", "product"],
        "fe_isource": ["reporter", "source"],
        "fe_pt": ["product", "period"],
        "fe_st": ["source", "period"],
        "fe_ps": ["product", "source"],
        "fe_it": ["reporter", "period"],
    }
    for name, parts in interactions.items():
        work[name] = work[parts].astype(str).agg("|".join, axis=1)

    formula = (
        f"{outcome} ~ {' + '.join(x_columns)} | "
        + " + ".join(interactions)
    )
    model = pf.fepois(
        formula,
        work,
        vcov={"CRV1": "reporter"},
        separation_check=["fe"],
        iwls_maxiter=max_iter,
        iwls_tol=tolerance,
        fixef_tol=tolerance,
        fixef_maxiter=100000,
        demeaner_backend="numba",
        lean=False,
    )
    coefficients = model.coef().reindex(x_columns)
    covariance_reporter = np.asarray(model._vcov).copy()
    model.vcov({"CRV1": "product"})
    covariance_product = np.asarray(model._vcov).copy()
    nobs = int(model._N)
    return PPMLResult(
        beta=coefficients.to_numpy(dtype=float),
        covariance_reporter=covariance_reporter,
        covariance_product=covariance_product,
        names=x_columns,
        nobs=nobs,
        dropped_separated=len(work) - nobs,
        iterations=int(getattr(model, "_n_iter", 0) or 0),
        converged=True,
        product_clusters=work["product"].nunique(),
        reporter_clusters=work["reporter"].nunique(),
        deviance=float(getattr(model, "_deviance", np.nan)),
    )


def run_exporter_its():
    rows = []
    for product, info in EXPORT_CASES.items():
        path = RAW / f"comtrade_{product}_china_exports.csv"
        coverage_path = RAW / f"comtrade_{product}_china_exports_coverage.csv"
        exports = pd.read_csv(path, dtype={"period": str})
        coverage = pd.read_csv(coverage_path, dtype={"period": str})
        data = pd.DataFrame({"period": PERIODS}).merge(
            coverage[["period", "api_record_returned", "status"]],
            on="period",
            how="left",
        )
        data = data.merge(
            exports[["period", "primaryValue"]],
            on="period",
            how="left",
        ).sort_values("period")
        data["primaryValue"] = data["primaryValue"].fillna(0)
        treatment_index = PERIOD_INDEX[info["implementation"]]
        data["time"] = data["period"].map(PERIOD_INDEX) - treatment_index
        data["post"] = data["period"].ge(info["implementation"]).astype(int)
        data["log_value"] = np.log1p(data["primaryValue"])

        model = sm.OLS(
            data["log_value"],
            sm.add_constant(data[["time", "post"]]),
        ).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        pre = data[data["post"].eq(0)]
        pre_model = sm.OLS(
            pre["log_value"],
            sm.add_constant(pre[["time"]]),
        ).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        beta = float(model.params["post"])
        rows.append(
            {
                "product": product,
                "label": info["label"],
                "implementation": info["implementation"],
                "beta": beta,
                "percent_effect": 100 * np.expm1(beta),
                "se_hac_6": float(model.bse["post"]),
                "p_hac_6": float(model.pvalues["post"]),
                "pre_log_trend_per_month": float(pre_model.params["time"]),
                "pre_trend_p_hac_6": float(pre_model.pvalues["time"]),
                "pre_r_squared": float(pre_model.rsquared),
                "pre_mean_usd": float(pre["primaryValue"].mean()),
                "post_mean_usd": float(
                    data.loc[data["post"].eq(1), "primaryValue"].mean()
                ),
                "months": len(data),
                "reported_months": int(data["api_record_returned"].fillna(False).sum()),
                "zero_or_no_record_months": int(data["primaryValue"].eq(0).sum()),
                "status": info.get(
                    "status",
                    "Descriptive interrupted time series on log1p exports; no untreated counterfactual.",
                ),
            }
        )
    return rows


def coefficient_rows(result, model, sample, outcome):
    rows = []
    for index, name in enumerate(result.names):
        beta = result.beta[index]
        se_reporter = np.sqrt(max(result.covariance_reporter[index, index], 0))
        se_product = np.sqrt(max(result.covariance_product[index, index], 0))
        z_reporter = beta / se_reporter if se_reporter > 0 else np.nan
        z_product = beta / se_product if se_product > 0 else np.nan
        rows.append(
            {
                "model": model,
                "sample": sample,
                "outcome": outcome,
                "term": name,
                "beta": beta,
                "percent_effect": 100 * (np.exp(beta) - 1),
                "se_reporter_cluster": se_reporter,
                "p_reporter_cluster": (
                    2 * norm.sf(abs(z_reporter)) if np.isfinite(z_reporter) else np.nan
                ),
                "se_product_cluster_unreliable": se_product,
                "p_product_cluster_unreliable": (
                    2 * norm.sf(abs(z_product)) if np.isfinite(z_product) else np.nan
                ),
                "reporter_clusters": result.reporter_clusters,
                "product_clusters": result.product_clusters,
                "minimum_exact_product_p": 1 / result.product_clusters,
                "nobs": result.nobs,
                "dropped_separated": result.dropped_separated,
                "iterations": result.iterations,
                "converged": result.converged,
                "deviance": result.deviance,
            }
        )
    return rows


def product_assignment_rank(
    frame,
    products,
    implementation,
    outcome,
    observed_beta,
    treated_count=1,
    fe_interactions=None,
):
    estimates = []
    treatment_index = PERIOD_INDEX[implementation]
    for assigned in combinations(products, treated_count):
        work = frame.copy()
        work["post"] = (
            work["period"].map(PERIOD_INDEX).ge(treatment_index).astype(int)
        )
        work["assigned_product"] = work["product"].isin(assigned).astype(int)
        work["treatment"] = work["china"] * work["assigned_product"] * work["post"]
        result = fit_ppml_hdfe(
            work,
            outcome,
            ["treatment"],
            fe_interactions=fe_interactions,
        )
        estimates.append(float(result.beta[0]))
    estimates = np.asarray(estimates)
    rank_p = float(
        np.mean(np.abs(estimates) >= abs(observed_beta) - 1e-12)
    )
    return rank_p, len(estimates)


def load_comtrade():
    data = pd.read_csv(COMTRADE_SOURCE, dtype={"hs": str, "period": str})
    data = data.rename(
        columns={"reporterCode": "reporter", "hs": "product_code"}
    )
    data["reporter"] = data["reporter"].astype(str)
    data["product"] = data["product_code"].astype(str)
    data["china"] = data["source"].eq("China").astype(int)
    return data


def add_case_treatment(frame, treated_product, implementation):
    work = frame.copy()
    treatment_index = PERIOD_INDEX[implementation]
    work["post"] = work["period"].map(PERIOD_INDEX).ge(treatment_index).astype(int)
    work["treated_product"] = work["product"].eq(treated_product).astype(int)
    work["treatment"] = work["china"] * work["treated_product"] * work["post"]
    return work


def switching_potential_by_reporter(data, treated_product, announcement):
    pre = data[
        data["product"].eq(treated_product)
        & data["period"].lt(announcement)
    ].copy()
    totals = (
        pre.groupby(["reporter", "source"], as_index=False)["trade_value_usd"]
        .sum()
        .pivot(index="reporter", columns="source", values="trade_value_usd")
        .fillna(0)
    )
    monthly = (
        pre.pivot_table(
            index=["reporter", "period"],
            columns="source",
            values="trade_value_usd",
            aggfunc="sum",
        )
        .fillna(0)
        .reset_index()
    )
    row_months = monthly.groupby("reporter").agg(
        pre_months=("period", "nunique"),
        row_positive_months=("RestOfWorld", lambda values: int((values > 0).sum())),
    )
    exposure = totals.join(row_months, how="outer").fillna(0)
    exposure["pre_total_trade"] = (
        exposure.get("China", 0) + exposure.get("RestOfWorld", 0)
    )
    exposure["china_exposure"] = np.where(
        exposure["pre_total_trade"] > 0,
        exposure.get("China", 0) / exposure["pre_total_trade"],
        np.nan,
    )
    exposure["row_access"] = np.where(
        exposure["pre_months"] > 0,
        exposure["row_positive_months"] / exposure["pre_months"],
        np.nan,
    )
    exposure["switching_potential"] = (
        exposure["china_exposure"] * exposure["row_access"]
    )
    exposure = exposure.reset_index()
    return exposure


def run_switching_potential_split_ppml(data):
    result_rows = []
    pretrend_rows = []
    summary_rows = []
    for treated_product, info in TREATED.items():
        print(f"Switching-potential split PPML: {treated_product}", flush=True)
        exposure = switching_potential_by_reporter(
            data, treated_product, info["announcement"]
        )
        pre_traders = exposure[exposure["pre_total_trade"].gt(0)].copy()
        if pre_traders.empty:
            continue
        median_switching = float(pre_traders["switching_potential"].median())
        pre_traders["switching_group"] = np.where(
            pre_traders["switching_potential"].gt(median_switching),
            "high_switching_potential",
            "low_switching_potential",
        )
        for group_name, reporters in pre_traders.groupby("switching_group")[
            "reporter"
        ]:
            reporter_list = set(reporters.astype(str))
            products = [treated_product, *PLACEBOS]
            sample = data[
                data["product"].isin(products)
                & data["reporter"].astype(str).isin(reporter_list)
            ].copy()
            sample = add_case_treatment(
                sample, treated_product, info["import_effect"]
            )
            if sample["reporter"].nunique() < 5:
                continue
            result = fit_ppml_hdfe(
                sample, "trade_value_usd", ["treatment"]
            )
            rows = coefficient_rows(
                result,
                model="Switching-potential split PPML DDD",
                sample=f"{treated_product} vs three placebos; {group_name}",
                outcome="trade_value_usd",
            )
            group_exposure = pre_traders[
                pre_traders["switching_group"].eq(group_name)
            ]
            for row in rows:
                row["switching_group"] = group_name
                row["treated_product"] = treated_product
                row["reporters_in_split"] = len(reporter_list)
                row["median_switching_potential_all_pretraders"] = (
                    median_switching
                )
                row["split_mean_china_exposure"] = float(
                    group_exposure["china_exposure"].mean()
                )
                row["split_mean_row_access"] = float(
                    group_exposure["row_access"].mean()
                )
                row["split_mean_switching_potential"] = float(
                    group_exposure["switching_potential"].mean()
                )
            result_rows.extend(rows)

            event_data, event_names, baseline = add_event_terms(
                sample,
                treated_product,
                info["import_effect"],
                info["baseline_event"],
            )
            event_result = fit_ppml_hdfe(
                event_data, "trade_value_usd", event_names
            )
            pretrend_p, pretrend_df = joint_pretrend_test(event_result, baseline)
            pretrend_rows.append(
                {
                    "sample": (
                        f"{treated_product} vs three placebos; {group_name}"
                    ),
                    "treated_product": treated_product,
                    "switching_group": group_name,
                    "baseline_event_bin": baseline,
                    "announcement": info["announcement"],
                    "implementation": info["implementation"],
                    "import_effect": info["import_effect"],
                    "joint_pretrend_p_reporter_cluster": pretrend_p,
                    "joint_pretrend_df": pretrend_df,
                    "reporters_in_split": len(reporter_list),
                    "product_clusters": event_result.product_clusters,
                    "inference_note": (
                        "Split-sample pretrend test is conditional and "
                        "mechanism-oriented; product-level treatment count "
                        "remains small."
                    ),
                }
            )

        summary_rows.append(
            {
                "treated_product": treated_product,
                "product_label": info["label"],
                "announcement": info["announcement"],
                "pretrade_reporters": int(pre_traders.shape[0]),
                "no_pretrade_reporters": int(
                    exposure["pre_total_trade"].eq(0).sum()
                ),
                "median_china_exposure": float(
                    pre_traders["china_exposure"].median()
                ),
                "median_row_access": float(pre_traders["row_access"].median()),
                "median_switching_potential": median_switching,
                "high_switching_reporters": int(
                    pre_traders["switching_potential"].gt(median_switching).sum()
                ),
                "low_switching_reporters": int(
                    pre_traders["switching_potential"].le(median_switching).sum()
                ),
            }
        )
    return result_rows, pretrend_rows, summary_rows


def event_category(relative_month):
    if relative_month <= -13:
        return "m13_or_earlier"
    if relative_month <= -7:
        return "m12_to_m7"
    if relative_month <= -4:
        return "m6_to_m4"
    if relative_month in {-3, -2, -1, 0, 1, 2, 3}:
        prefix = "m" if relative_month < 0 else "p"
        return f"{prefix}{abs(relative_month)}"
    if relative_month <= 6:
        return "p4_to_p6"
    if relative_month <= 12:
        return "p7_to_p12"
    return "p13_or_later"


EVENT_ORDER = [
    "m13_or_earlier",
    "m12_to_m7",
    "m6_to_m4",
    "m3",
    "m2",
    "m1",
    "p0",
    "p1",
    "p2",
    "p3",
    "p4_to_p6",
    "p7_to_p12",
    "p13_or_later",
]


def add_event_terms(frame, treated_product, implementation, baseline):
    work = frame.copy()
    treatment_index = PERIOD_INDEX[implementation]
    work["event_month"] = work["period"].map(PERIOD_INDEX) - treatment_index
    work["event_bin"] = work["event_month"].map(event_category)
    baseline_name = event_category(baseline)
    names = []
    for category in EVENT_ORDER:
        if category == baseline_name or category not in set(work["event_bin"]):
            continue
        name = f"event_{category}"
        work[name] = (
            work["product"].eq(treated_product)
            & work["source"].eq("China")
            & work["event_bin"].eq(category)
        ).astype(int)
        names.append(name)
    return work, names, baseline_name


def joint_pretrend_test(result, baseline_name, exclude_categories=None):
    pre_categories = {
        "m13_or_earlier",
        "m12_to_m7",
        "m6_to_m4",
        "m3",
        "m2",
        "m1",
    }
    pre_categories.discard(baseline_name)
    if exclude_categories:
        pre_categories -= set(exclude_categories)
    indexes = [
        index
        for index, name in enumerate(result.names)
        if name.removeprefix("event_") in pre_categories
    ]
    if not indexes:
        return np.nan, 0
    beta = result.beta[indexes]
    covariance = result.covariance_reporter[np.ix_(indexes, indexes)]
    statistic = float(beta.T @ np.linalg.pinv(covariance) @ beta)
    return float(chi2.sf(statistic, len(indexes))), len(indexes)


def contaminated_categories(info, anchor_date):
    anchor_idx = PERIOD_INDEX[anchor_date]
    announce_idx = PERIOD_INDEX[info["announcement"]]
    cats = set()
    for month_idx in range(announce_idx, anchor_idx):
        cats.add(event_category(month_idx - anchor_idx))
    return cats


def run_anchor_event_study(
    frame,
    treated_product,
    info,
    anchor_date,
    baseline_offset,
    outcome,
    model_label,
    sample_label,
    fe_interactions=None,
    exclude_contaminated=True,
):
    event_data, event_names, baseline_name = add_event_terms(
        frame, treated_product, anchor_date, baseline_offset
    )
    event_result = fit_ppml_hdfe(
        event_data, outcome, event_names, fe_interactions=fe_interactions
    )
    exclude = None
    if exclude_contaminated:
        exclude = contaminated_categories(info, anchor_date)
    pretrend_p, pretrend_df = joint_pretrend_test(
        event_result, baseline_name, exclude_categories=exclude
    )
    event_rows = coefficient_rows(
        event_result,
        model=f"{model_label} ({anchor_date} anchor)",
        sample=f"{sample_label}; baseline={baseline_name}",
        outcome=outcome,
    )
    pretrend_row = {
        "sample": sample_label,
        "model": model_label,
        "anchor": anchor_date,
        "baseline_event_bin": baseline_name,
        "baseline_offset": baseline_offset,
        "announcement": info["announcement"],
        "implementation": info.get("implementation", anchor_date),
        "import_effect": info.get("import_effect", info.get("implementation", anchor_date)),
        "joint_pretrend_p_reporter_cluster": pretrend_p,
        "joint_pretrend_df": pretrend_df,
        "excluded_categories": ";".join(sorted(exclude)) if exclude else "",
        "product_clusters": event_result.product_clusters,
        "reporter_clusters": event_result.reporter_clusters,
    }
    return event_rows, pretrend_row


def run_trend_break_ppml(
    frame,
    treated_product,
    info,
    anchor_date,
    outcome,
    model_label,
    sample_label,
    fe_interactions=None,
):
    work = frame.copy()
    treatment_index = PERIOD_INDEX[anchor_date]
    work["post"] = (
        work["period"].map(PERIOD_INDEX).ge(treatment_index).astype(int)
    )
    work["treated_product"] = work["product"].eq(treated_product).astype(int)
    work["treatment"] = work["china"] * work["treated_product"] * work["post"]
    work["rel_time"] = work["period"].map(PERIOD_INDEX) - treatment_index
    work["diff_trend"] = (
        work["rel_time"] * work["china"] * work["treated_product"]
    )
    work["trend_break"] = work["diff_trend"] * work["post"]
    x_cols = ["treatment", "diff_trend", "trend_break"]
    result = fit_ppml_hdfe(work, outcome, x_cols, fe_interactions=fe_interactions)
    rows = coefficient_rows(
        result,
        model=f"Trend-break {model_label} ({anchor_date} anchor)",
        sample=sample_label,
        outcome=outcome,
    )
    return rows


def run_comtrade_ppml(data):
    result_rows = []
    event_rows = []
    pretrend_rows = []
    for treated_product, info in TREATED.items():
        print(f"Comtrade PPML: {treated_product}", flush=True)
        products = [treated_product, *PLACEBOS]
        sample = data[data["product"].isin(products)].copy()
        sample = add_case_treatment(
            sample, treated_product, info["import_effect"]
        )
        result = fit_ppml_hdfe(
            sample, "trade_value_usd", ["treatment"]
        )
        static_rows = coefficient_rows(
            result,
            model="PPML DDD",
            sample=f"{treated_product} vs three placebos",
            outcome="trade_value_usd",
        )
        rank_p, assignments = product_assignment_rank(
            sample,
            products,
            info["import_effect"],
            "trade_value_usd",
            result.beta[0],
        )
        for row in static_rows:
            row["placebo_assignment_rank_p"] = rank_p
            row["placebo_assignments"] = assignments
        result_rows.extend(static_rows)

        event_data, event_names, baseline = add_event_terms(
            sample,
            treated_product,
            info["import_effect"],
            info["baseline_event"],
        )
        event_result = fit_ppml_hdfe(
            event_data, "trade_value_usd", event_names
        )
        event_rows.extend(
            coefficient_rows(
                event_result,
                model="PPML DDD event study",
                sample=f"{treated_product} vs three placebos; baseline={baseline}",
                outcome="trade_value_usd",
            )
        )
        pretrend_p, pretrend_df = joint_pretrend_test(event_result, baseline)
        pretrend_rows.append(
            {
                "sample": treated_product,
                "baseline_event_bin": baseline,
                "announcement": info["announcement"],
                "implementation": info["implementation"],
                "import_effect": info["import_effect"],
                "joint_pretrend_p_reporter_cluster": pretrend_p,
                "joint_pretrend_df": pretrend_df,
                "product_clusters": event_result.product_clusters,
                "inference_note": (
                    "Reporter-clustered pretrend test is conditional; "
                    "four product clusters do not support conventional "
                    "treatment-assignment inference."
                ),
            }
        )
    return result_rows, event_rows, pretrend_rows


def run_china_product_ppml(data):
    result_rows = []
    event_rows = []
    pretrend_rows = []
    china = data[data["source"].eq("China")].copy()
    product_did_fes = {
        "fe_ip": ["reporter", "product"],
        "fe_it": ["reporter", "period"],
        "fe_product_season": ["product", "calendar_month"],
    }
    for treated_product, info in TREATED.items():
        print(f"China-import PPML: {treated_product}", flush=True)
        products = [treated_product, *PLACEBOS]
        sample = china[china["product"].isin(products)].copy()
        sample = add_case_treatment(
            sample, treated_product, info["import_effect"]
        )
        result = fit_ppml_hdfe(
            sample,
            "trade_value_usd",
            ["treatment"],
            fe_interactions=product_did_fes,
        )
        static_rows = coefficient_rows(
            result,
            model="China-import PPML product DiD",
            sample=f"{treated_product} vs three placebos",
            outcome="trade_value_usd",
        )
        rank_p, assignments = product_assignment_rank(
            sample,
            products,
            info["import_effect"],
            "trade_value_usd",
            result.beta[0],
            fe_interactions=product_did_fes,
        )
        for row in static_rows:
            row["placebo_assignment_rank_p"] = rank_p
            row["placebo_assignments"] = assignments
        result_rows.extend(static_rows)
        event_data, event_names, baseline = add_event_terms(
            sample,
            treated_product,
            info["import_effect"],
            info["baseline_event"],
        )
        event_result = fit_ppml_hdfe(
            event_data,
            "trade_value_usd",
            event_names,
            fe_interactions=product_did_fes,
        )
        event_rows.extend(
            coefficient_rows(
                event_result,
                model="China-import PPML event study",
                sample=f"{treated_product} vs three placebos; baseline={baseline}",
                outcome="trade_value_usd",
            )
        )
        pretrend_p, pretrend_df = joint_pretrend_test(event_result, baseline)
        pretrend_rows.append(
            {
                "sample": f"China imports: {treated_product}",
                "baseline_event_bin": baseline,
                "announcement": info["announcement"],
                "implementation": info["implementation"],
                "import_effect": info["import_effect"],
                "joint_pretrend_p_reporter_cluster": pretrend_p,
                "joint_pretrend_df": pretrend_df,
                "product_clusters": event_result.product_clusters,
                "inference_note": (
                    "Reporter-clustered test is conditional; exact product-level "
                    "inference has minimum p=0.25 with three placebos."
                ),
            }
        )
    return result_rows, event_rows, pretrend_rows


def load_eurostat_source_panel():
    data = pd.read_csv(EUROSTAT_COUNTRY, dtype={"period": str})
    common = data[["reporter", "product", "period"]].copy()
    china = common.copy()
    china["source"] = "China"
    china["trade_value_eur"] = data["china_imports_eur"]
    rest = common.copy()
    rest["source"] = "RestOfWorld"
    rest["trade_value_eur"] = data["non_china_imports_eur"]
    panel = pd.concat([china, rest], ignore_index=True)
    panel["period"] = panel["period"].str.replace("-", "", regex=False)
    panel["reporter"] = panel["reporter"].astype(str)
    panel["china"] = panel["source"].eq("China").astype(int)
    return panel


def run_eurostat_ppml(data):
    result_rows = []
    event_rows = []
    pretrend_rows = []
    cases = {
        "Ga": ["Ga", "In", "V"],
        "Ge": ["Ge", "In", "V"],
    }
    for treated_product, products in cases.items():
        print(f"Eurostat PPML: {treated_product}", flush=True)
        sample = data[data["product"].isin(products)].copy()
        sample = add_case_treatment(sample, treated_product, "202309")
        result = fit_ppml_hdfe(sample, "trade_value_eur", ["treatment"])
        static_rows = coefficient_rows(
            result,
            model="Eurostat CN8 PPML DDD",
            sample=f"{treated_product} vs In/V",
            outcome="trade_value_eur",
        )
        rank_p, assignments = product_assignment_rank(
            sample,
            products,
            "202309",
            "trade_value_eur",
            result.beta[0],
        )
        for row in static_rows:
            row["placebo_assignment_rank_p"] = rank_p
            row["placebo_assignments"] = assignments
        result_rows.extend(static_rows)
        event_data, event_names, baseline = add_event_terms(
            sample, treated_product, "202309", -3
        )
        event_result = fit_ppml_hdfe(
            event_data, "trade_value_eur", event_names
        )
        event_rows.extend(
            coefficient_rows(
                event_result,
                model="Eurostat CN8 PPML event study",
                sample=f"{treated_product} vs In/V; baseline={baseline}",
                outcome="trade_value_eur",
            )
        )
        pretrend_p, pretrend_df = joint_pretrend_test(event_result, baseline)
        pretrend_rows.append(
            {
                "sample": treated_product,
                "baseline_event_bin": baseline,
                "announcement": "202307",
                "implementation": "202308",
                "import_effect": "202309",
                "joint_pretrend_p_reporter_cluster": pretrend_p,
                "joint_pretrend_df": pretrend_df,
                "product_clusters": event_result.product_clusters,
                "inference_note": (
                    "Only three products enter each case-specific comparison; "
                    "minimum exact product-assignment p is 1/3."
                ),
            }
        )

    pooled = data[data["product"].isin(["Ga", "Ge", "In", "V"])].copy()
    print("Eurostat PPML: pooled Ga/Ge", flush=True)
    pooled["post"] = pooled["period"].map(PERIOD_INDEX).ge(
        PERIOD_INDEX["202309"]
    ).astype(int)
    pooled["treated_product"] = pooled["product"].isin(["Ga", "Ge"]).astype(int)
    pooled["treatment"] = pooled["china"] * pooled["treated_product"] * pooled["post"]
    pooled_result = fit_ppml_hdfe(
        pooled, "trade_value_eur", ["treatment"]
    )
    pooled_rows = coefficient_rows(
        pooled_result,
        model="Eurostat CN8 pooled PPML DDD",
        sample="Ga/Ge vs In/V",
        outcome="trade_value_eur",
    )
    for row in pooled_rows:
        row["minimum_exact_product_p"] = 1 / len(
            list(combinations(["Ga", "Ge", "In", "V"], 2))
        )
    rank_p, assignments = product_assignment_rank(
        pooled,
        ["Ga", "Ge", "In", "V"],
        "202309",
        "trade_value_eur",
        pooled_result.beta[0],
        treated_count=2,
    )
    for row in pooled_rows:
        row["placebo_assignment_rank_p"] = rank_p
        row["placebo_assignments"] = assignments
    result_rows.extend(pooled_rows)
    return result_rows, event_rows, pretrend_rows


def run_extended_analyses(comtrade, eurostat):
    all_event_rows = []
    all_pretrend_rows = []
    all_trend_break_rows = []

    anchors = [
        ("announcement", -4),
        ("implementation", -4),
        ("import_effect", None),
    ]

    comtrade_fe = None
    china_fe = {
        "fe_ip": ["reporter", "product"],
        "fe_it": ["reporter", "period"],
        "fe_product_season": ["product", "calendar_month"],
    }

    for treated_product, info in TREATED.items():
        products = [treated_product, *PLACEBOS]
        sample = comtrade[comtrade["product"].isin(products)].copy()
        for anchor_key, baseline_offset in anchors:
            anchor_date = info[anchor_key]
            actual_baseline = (
                baseline_offset
                if baseline_offset is not None
                else info["baseline_event"]
            )
            label = f"{treated_product} vs three placebos"
            print(
                f"Extended PPML DDD: {treated_product} "
                f"{anchor_key}={anchor_date}",
                flush=True,
            )
            ev_rows, pt_row = run_anchor_event_study(
                sample,
                treated_product,
                info,
                anchor_date,
                actual_baseline,
                "trade_value_usd",
                "PPML DDD",
                label,
                fe_interactions=comtrade_fe,
            )
            all_event_rows.extend(ev_rows)
            all_pretrend_rows.append(pt_row)
            tb_rows = run_trend_break_ppml(
                sample,
                treated_product,
                info,
                anchor_date,
                "trade_value_usd",
                "PPML DDD",
                label,
                fe_interactions=comtrade_fe,
            )
            all_trend_break_rows.extend(tb_rows)

    china = comtrade[comtrade["source"].eq("China")].copy()
    for treated_product, info in TREATED.items():
        products = [treated_product, *PLACEBOS]
        sample = china[china["product"].isin(products)].copy()
        for anchor_key, baseline_offset in anchors:
            anchor_date = info[anchor_key]
            actual_baseline = (
                baseline_offset
                if baseline_offset is not None
                else info["baseline_event"]
            )
            label = f"{treated_product} vs three placebos"
            print(
                f"Extended China-import: {treated_product} "
                f"{anchor_key}={anchor_date}",
                flush=True,
            )
            ev_rows, pt_row = run_anchor_event_study(
                sample,
                treated_product,
                info,
                anchor_date,
                actual_baseline,
                "trade_value_usd",
                "China-import PPML",
                label,
                fe_interactions=china_fe,
            )
            all_event_rows.extend(ev_rows)
            all_pretrend_rows.append(pt_row)
            tb_rows = run_trend_break_ppml(
                sample,
                treated_product,
                info,
                anchor_date,
                "trade_value_usd",
                "China-import PPML",
                label,
                fe_interactions=china_fe,
            )
            all_trend_break_rows.extend(tb_rows)

    eurostat_cases = {
        "Ga": {
            "announcement": "202307",
            "implementation": "202308",
            "import_effect": "202309",
            "baseline_event": -3,
        },
        "Ge": {
            "announcement": "202307",
            "implementation": "202308",
            "import_effect": "202309",
            "baseline_event": -3,
        },
    }
    for treated_product, einfo in eurostat_cases.items():
        products_map = {"Ga": ["Ga", "In", "V"], "Ge": ["Ge", "In", "V"]}
        sample = eurostat[
            eurostat["product"].isin(products_map[treated_product])
        ].copy()
        for anchor_key, baseline_offset in anchors:
            anchor_date = einfo[anchor_key]
            actual_baseline = (
                baseline_offset
                if baseline_offset is not None
                else einfo["baseline_event"]
            )
            label = f"{treated_product} vs In/V"
            print(
                f"Extended Eurostat: {treated_product} "
                f"{anchor_key}={anchor_date}",
                flush=True,
            )
            ev_rows, pt_row = run_anchor_event_study(
                sample,
                treated_product,
                einfo,
                anchor_date,
                actual_baseline,
                "trade_value_eur",
                "Eurostat CN8 PPML",
                label,
            )
            all_event_rows.extend(ev_rows)
            all_pretrend_rows.append(pt_row)
            tb_rows = run_trend_break_ppml(
                sample,
                treated_product,
                einfo,
                anchor_date,
                "trade_value_eur",
                "Eurostat CN8 PPML",
                label,
            )
            all_trend_break_rows.extend(tb_rows)

    return (
        pd.DataFrame(all_event_rows),
        pd.DataFrame(all_pretrend_rows),
        pd.DataFrame(all_trend_break_rows),
    )


def simplex_weights(target, donors, ridge=0.0):
    donors = np.asarray(donors, dtype=float)
    target = np.asarray(target, dtype=float)
    n_donors = donors.shape[0]

    def objective(weights):
        error = target - weights @ donors
        return float(error @ error + ridge * (weights @ weights))

    result = minimize(
        objective,
        np.full(n_donors, 1 / n_donors),
        method="SLSQP",
        bounds=[(0, 1)] * n_donors,
        constraints={"type": "eq", "fun": lambda weights: weights.sum() - 1},
        options={"ftol": 1e-12, "maxiter": 10000},
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def scm_and_sdid_diagnostics(data):
    aggregate = (
        data[data["source"].eq("China")]
        .groupby(["product", "period"], as_index=False)["trade_value_usd"]
        .sum()
    )
    wide = aggregate.pivot(index="product", columns="period", values="trade_value_usd")
    wide = wide.reindex(columns=PERIODS).fillna(0)
    rows = []

    for treated_product, info in TREATED.items():
        donors = PLACEBOS
        treatment_index = PERIOD_INDEX[info["import_effect"]]
        pre_periods = PERIODS[:treatment_index]
        post_periods = PERIODS[treatment_index:]
        transformed = np.log1p(wide.loc[[treated_product, *donors]])
        pre_means = transformed[pre_periods].mean(axis=1)
        transformed = transformed.sub(pre_means, axis=0)

        treated_pre = transformed.loc[treated_product, pre_periods].to_numpy()
        treated_post = transformed.loc[treated_product, post_periods].to_numpy()
        donor_pre = transformed.loc[donors, pre_periods].to_numpy()
        donor_post = transformed.loc[donors, post_periods].to_numpy()

        scm_weights = simplex_weights(treated_pre, donor_pre)
        synthetic_pre = scm_weights @ donor_pre
        synthetic_post = scm_weights @ donor_post
        scm_pre_rmse = float(np.sqrt(np.mean((treated_pre - synthetic_pre) ** 2)))
        scm_att = float(np.mean(treated_post - synthetic_post))
        scm_post_rmse = float(np.sqrt(np.mean((treated_post - synthetic_post) ** 2)))

        unit_weights = simplex_weights(treated_pre, donor_pre, ridge=1e-4)
        control_post_average = donor_post.mean(axis=1)
        time_weights = simplex_weights(
            control_post_average, donor_pre.T, ridge=1e-4
        )
        pre_gap = treated_pre - unit_weights @ donor_pre
        post_gap = treated_post - unit_weights @ donor_post
        sdid_att = float(post_gap.mean() - time_weights @ pre_gap)

        row = {
            "treated_product": treated_product,
            "implementation": info["implementation"],
            "import_effect": info["import_effect"],
            "donor_count": len(donors),
            "scm_att_log_points": scm_att,
            "scm_percent_effect": 100 * (np.exp(scm_att) - 1),
            "scm_pre_rmse": scm_pre_rmse,
            "scm_post_rmse": scm_post_rmse,
            "scm_post_pre_rmspe_ratio": (
                scm_post_rmse / scm_pre_rmse if scm_pre_rmse > 0 else np.nan
            ),
            "sdid_att_log_points": sdid_att,
            "sdid_percent_effect": 100 * (np.exp(sdid_att) - 1),
            "minimum_exact_placebo_p": 1 / (len(donors) + 1),
            "status": (
                "Diagnostic only: three donors cannot support conventional "
                "placebo inference or establish donor-pool robustness."
            ),
        }
        for donor, weight in zip(donors, scm_weights):
            row[f"scm_weight_{donor}"] = weight
        for donor, weight in zip(donors, unit_weights):
            row[f"sdid_unit_weight_{donor}"] = weight
        rows.append(row)
    return rows


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    comtrade = load_comtrade()
    eurostat = load_eurostat_source_panel()

    exporter_its_rows = run_exporter_its()
    ppml_rows, event_rows, pretrend_rows = run_comtrade_ppml(comtrade)
    china_ppml, china_events, china_pretrends = run_china_product_ppml(comtrade)
    euro_ppml, euro_event, euro_pretrend = run_eurostat_ppml(eurostat)
    (
        switching_ppml,
        switching_pretrends,
        switching_summary,
    ) = run_switching_potential_split_ppml(comtrade)
    scm_rows = scm_and_sdid_diagnostics(comtrade)

    (
        ext_events,
        ext_pretrends,
        ext_trend_break,
    ) = run_extended_analyses(comtrade, eurostat)

    ppml = pd.DataFrame([*ppml_rows, *china_ppml, *euro_ppml])
    events = pd.DataFrame([*event_rows, *china_events, *euro_event])
    pretrends = pd.DataFrame(
        [*pretrend_rows, *china_pretrends, *euro_pretrend]
    )
    switching = pd.DataFrame(switching_ppml)
    switching_pretrend = pd.DataFrame(switching_pretrends)
    switching_diagnostics = pd.DataFrame(switching_summary)
    scm = pd.DataFrame(scm_rows)
    exporter_its = pd.DataFrame(exporter_its_rows)

    exporter_its_path = OUTPUT / "thesis_exporter_its_results.csv"
    ppml_path = OUTPUT / "thesis_ppml_results.csv"
    event_path = OUTPUT / "thesis_event_study_results.csv"
    pretrend_path = OUTPUT / "thesis_event_pretrend_tests.csv"
    scm_path = OUTPUT / "thesis_scm_sdid_diagnostics.csv"
    ext_event_path = OUTPUT / "thesis_extended_event_study_results.csv"
    ext_pretrend_path = OUTPUT / "thesis_extended_pretrend_tests.csv"
    ext_trend_break_path = OUTPUT / "thesis_trend_break_results.csv"
    switching_path = OUTPUT / "thesis_switching_potential_split_results.csv"
    switching_pretrend_path = (
        OUTPUT / "thesis_switching_potential_split_pretrends.csv"
    )
    switching_diagnostics_path = (
        OUTPUT / "thesis_switching_potential_diagnostics.csv"
    )
    exporter_its.to_csv(exporter_its_path, index=False)
    ppml.to_csv(ppml_path, index=False)
    events.to_csv(event_path, index=False)
    pretrends.to_csv(pretrend_path, index=False)
    switching.to_csv(switching_path, index=False)
    switching_pretrend.to_csv(switching_pretrend_path, index=False)
    switching_diagnostics.to_csv(switching_diagnostics_path, index=False)
    scm.to_csv(scm_path, index=False)
    ext_events.to_csv(ext_event_path, index=False)
    ext_pretrends.to_csv(ext_pretrend_path, index=False)
    ext_trend_break.to_csv(ext_trend_break_path, index=False)

    print("\nEXPORTER INTERRUPTED TIME SERIES (HAC, 6 LAGS)")
    print(
        exporter_its[
            ["product", "percent_effect", "p_hac_6", "pre_r_squared", "status"]
        ].to_string(index=False)
    )
    print("\nPPML RESULTS")
    print(
        ppml[
            [
                "model",
                "sample",
                "beta",
                "percent_effect",
                "p_reporter_cluster",
                "product_clusters",
                "minimum_exact_product_p",
                "placebo_assignment_rank_p",
                "converged",
            ]
        ].to_string(index=False)
    )
    print("\nEVENT PRETREND TESTS")
    print(pretrends.to_string(index=False))
    print("\nSCM / SYNTHETIC DID DIAGNOSTICS")
    print(
        scm[
            [
                "treated_product",
                "scm_percent_effect",
                "scm_pre_rmse",
                "scm_post_pre_rmspe_ratio",
                "sdid_percent_effect",
                "minimum_exact_placebo_p",
            ]
        ].to_string(index=False)
    )
    print("\nSaved:")
    for path in [
        exporter_its_path,
        ppml_path,
        event_path,
        pretrend_path,
        scm_path,
        switching_path,
        switching_pretrend_path,
        switching_diagnostics_path,
        ext_event_path,
        ext_pretrend_path,
        ext_trend_break_path,
    ]:
        print(f"  {path}")

    print("\nSWITCHING-POTENTIAL SPLIT PPML")
    if not switching.empty:
        print(
            switching[
                [
                    "sample",
                    "switching_group",
                    "percent_effect",
                    "p_reporter_cluster",
                    "reporters_in_split",
                    "split_mean_china_exposure",
                    "split_mean_row_access",
                    "split_mean_switching_potential",
                ]
            ].to_string(index=False)
        )
    print("\nSWITCHING-POTENTIAL SPLIT PRETRENDS")
    if not switching_pretrend.empty:
        print(
            switching_pretrend[
                [
                    "sample",
                    "joint_pretrend_p_reporter_cluster",
                    "joint_pretrend_df",
                    "reporters_in_split",
                ]
            ].to_string(index=False)
        )

    print("\nEXTENDED PRETREND TESTS (MULTI-ANCHOR, EXCLUDING ANTICIPATION)")
    print(
        ext_pretrends[
            [
                "sample",
                "model",
                "anchor",
                "excluded_categories",
                "joint_pretrend_p_reporter_cluster",
                "joint_pretrend_df",
            ]
        ].to_string(index=False)
    )
    print("\nTREND-BREAK PPML (CHANGE IN GROWTH RATE)")
    for col in ext_trend_break["term"].unique():
        subset = ext_trend_break[ext_trend_break["term"].eq(col)]
        print(f"\n  {col}:")
        print(
            subset[
                [
                    "model",
                    "sample",
                    "percent_effect",
                    "p_reporter_cluster",
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()
