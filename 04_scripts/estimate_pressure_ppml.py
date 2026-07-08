#!/usr/bin/env python3
"""
Estimate preliminary PPML pressure-index models.

The main model keeps the same source-contrast PPML structure as the proposal,
but replaces a single average treatment effect with interactions between the
treated-China-post cell and pre-policy pressure indexes.

For each pressure variant v:

    trade_value_usd ~ D
                    + D x switch_pressure_v
                    + D x compression_pressure_v
                    | importer-month
                    + product-month
                    + source-month
                    + importer-product-source

Reporter-clustered p-values are conditional diagnostics. Product-level
inference remains limited because treatment variation is at product-wave level.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm


REPO = Path(__file__).resolve().parents[1]
LOCAL_SITE_PACKAGES = REPO / ".conda" / "lib" / "python3.12" / "site-packages"
if LOCAL_SITE_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

try:
    import pyfixest as pf
except ImportError as exc:
    raise ImportError(
        "estimate_pressure_ppml.py requires pyfixest in the repository-local "
        "prefix. Install it with: python -m pip install --prefix ./.conda "
        "pyfixest==0.40.1"
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_ppml_results.csv"
COMPARISON_PATH = TABLES / "pressure_ppml_variant_comparison.csv"
RUNLOG_PATH = TABLES / "pressure_ppml_run_log.md"


VARIANTS = {
    "frequency": {
        "switch": "did_main_clean_switch_frequency",
        "compress": "did_main_clean_compress_frequency",
        "description": "RoW access frequency",
    },
    "capacity": {
        "switch": "did_main_clean_switch_capacity",
        "compress": "did_main_clean_compress_capacity",
        "description": "RoW value relative to China value",
    },
    "absorptive": {
        "switch": "did_main_clean_switch_absorptive",
        "compress": "did_main_clean_compress_absorptive",
        "description": "scale-adjusted absorptive switching capacity",
    },
}

FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
    "fe_importer_product_source",
]


def load_panel() -> pd.DataFrame:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PANEL_PATH}. Run build_pressure_estimation_panel.py first."
        )
    panel = pd.read_csv(
        PANEL_PATH,
        dtype={"hs": str, "period": str},
        low_memory=False,
    )
    return panel


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def fit_model(data: pd.DataFrame, variant: str, sample_col: str) -> tuple[pd.DataFrame, dict]:
    spec = VARIANTS[variant]
    x_cols = ["did_main_clean", spec["switch"], spec["compress"]]
    keep_cols = ["trade_value_usd", "reporterCode", "hs", *x_cols, *FE]
    work = data.loc[data[sample_col].eq(True), keep_cols].dropna().copy()
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    work["product_cluster"] = work["hs"].astype(str)

    formula = f"trade_value_usd ~ {' + '.join(x_cols)} | {' + '.join(FE)}"
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
    vcov_reporter = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se_reporter = np.sqrt(np.diag(vcov_reporter))

    model.vcov({"CRV1": "product_cluster"})
    vcov_product = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se_product = np.sqrt(np.diag(vcov_product))

    rows = []
    term_labels = {
        "did_main_clean": "baseline treated-China-post effect at average pressure",
        spec["switch"]: "switching-pressure interaction",
        spec["compress"]: "compression-pressure interaction",
    }
    for idx, term in enumerate(x_cols):
        beta = float(coef.loc[term])
        se_r = float(se_reporter[idx])
        se_p = float(se_product[idx])
        rows.append(
            {
                "sample": sample_col,
                "variant": variant,
                "variant_description": spec["description"],
                "term": term,
                "term_label": term_labels[term],
                "coef": beta,
                "se_reporter": se_r,
                "p_reporter": p_value(beta, se_r),
                "se_product": se_p,
                "p_product": p_value(beta, se_p),
                "percent_effect": percent_effect(beta),
                "nobs": int(model._N),
                "rows_input": len(work),
                "dropped_separation": int(len(work) - int(model._N)),
                "reporter_clusters": int(work["reporter_cluster"].nunique()),
                "product_clusters": int(work["product_cluster"].nunique()),
                "converged": True,
                "iterations": int(getattr(model, "_n_iter", 0) or 0),
                "formula": formula,
            }
        )

    diagnostics = {
        "sample": sample_col,
        "variant": variant,
        "nobs": int(model._N),
        "rows_input": len(work),
        "dropped_separation": int(len(work) - int(model._N)),
        "reporter_clusters": int(work["reporter_cluster"].nunique()),
        "product_clusters": int(work["product_cluster"].nunique()),
        "formula": formula,
    }
    return pd.DataFrame(rows), diagnostics


def compare_variants(results: pd.DataFrame) -> pd.DataFrame:
    main = results[results["sample"].eq("sample_main_clean")].copy()
    pivot = main.pivot_table(
        index=["variant", "variant_description"],
        columns="term_label",
        values=["coef", "p_reporter", "percent_effect"],
        aggfunc="first",
    )
    pivot.columns = ["__".join(col).strip() for col in pivot.columns]
    pivot = pivot.reset_index()
    return pivot


def write_runlog(results: pd.DataFrame, diagnostics: list[dict]) -> None:
    lines = [
        "# Pressure PPML Preliminary Run",
        "",
        "Outcome: `trade_value_usd`.",
        "",
        "Fixed effects: importer-month, product-month, source-month, and importer-product-source.",
        "",
        "Main sample: `sample_main_clean`, which includes 5 clean/sparse treated products and 12 donor candidates.",
        "",
        "Reporter-clustered p-values are conditional diagnostics. Product-clustered p-values are reported only as a sensitivity check with few product clusters.",
        "",
        "## Diagnostics",
        "",
    ]
    for item in diagnostics:
        lines.append(
            f"- {item['sample']} / {item['variant']}: nobs={item['nobs']}, "
            f"input rows={item['rows_input']}, dropped={item['dropped_separation']}, "
            f"reporters={item['reporter_clusters']}, products={item['product_clusters']}."
        )
    lines.extend(["", "## Main Results", ""])
    main = results[results["sample"].eq("sample_main_clean")].copy()
    for variant, group in main.groupby("variant", sort=False):
        lines.append(f"### {variant}")
        for _, row in group.iterrows():
            lines.append(
                f"- {row['term_label']}: coef={row['coef']:.4f}, "
                f"reporter p={row['p_reporter']:.4g}, "
                f"product p={row['p_product']:.4g}, "
                f"percent={row['percent_effect']:.1f}%."
            )
        lines.append("")
    RUNLOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate_results(results: pd.DataFrame) -> None:
    errors = []
    expected_rows = 3 * 2 * 3
    if len(results) != expected_rows:
        errors.append(f"expected {expected_rows} result rows, got {len(results)}")
    if results["coef"].isna().any():
        errors.append("missing coefficients")
    if results["p_reporter"].isna().any():
        errors.append("missing reporter p-values")
    if not results["nobs"].gt(0).all():
        errors.append("nonpositive nobs")
    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = load_panel()
    all_results = []
    diagnostics = []
    for sample_col in ["sample_main_clean", "sample_main_clean_strict"]:
        for variant in VARIANTS:
            print(f"Estimating {sample_col} / {variant} ...", flush=True)
            result, diag = fit_model(panel, variant, sample_col)
            all_results.append(result)
            diagnostics.append(diag)

    results = pd.concat(all_results, ignore_index=True)
    validate_results(results)
    comparison = compare_variants(results)

    results.to_csv(RESULTS_PATH, index=False)
    comparison.to_csv(COMPARISON_PATH, index=False)
    write_runlog(results, diagnostics)

    print(f"Wrote {RESULTS_PATH}")
    print(f"Wrote {COMPARISON_PATH}")
    print(f"Wrote {RUNLOG_PATH}")
    print("\nMain sample results:")
    print(
        results.loc[
            results["sample"].eq("sample_main_clean"),
            [
                "variant",
                "term_label",
                "coef",
                "se_reporter",
                "p_reporter",
                "se_product",
                "p_product",
                "percent_effect",
                "nobs",
                "dropped_separation",
            ],
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
