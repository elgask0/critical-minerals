#!/usr/bin/env python3
"""
Estimate common staggered PPML pressure models for the strict clean sample.

The common staggered model uses the four clean treated products:

- HS 2504, post 2024-01
- HS 8110, post 2024-10
- HS 8106, post 2025-03
- HS 284180, post 2025-03

The sample keeps the same 12 donor products used in the wave-specific runs.
Pressure variables are standardized over strict clean treated importer-product
cells only. HS 261710 is excluded because it is sparse.
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
        "estimate_pressure_ppml_staggered.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_ppml_staggered_pressure_results.csv"
RUNLOG_PATH = TABLES / "pressure_ppml_staggered_pressure_run_log.md"


VARIANTS = {
    "frequency": {
        "switch": "p_switch_frequency",
        "compress": "p_compress_frequency",
        "description": "RoW access frequency",
    },
    "capacity": {
        "switch": "p_switch_capacity",
        "compress": "p_compress_capacity",
        "description": "RoW value relative to China value",
    },
    "absorptive": {
        "switch": "p_switch_absorptive",
        "compress": "p_compress_absorptive",
        "description": "scale-adjusted absorptive switching capacity",
    },
}

FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
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


def load_sample() -> pd.DataFrame:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PANEL_PATH}. Run build_pressure_estimation_panel.py first."
        )
    panel = pd.read_csv(PANEL_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    sample = panel.loc[panel["sample_main_clean_strict"].eq(True)].copy()
    sample["D_staggered_common"] = sample["did_main_clean_strict"].astype(int)
    return sample


def add_strict_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
    out = sample.copy()
    spec = VARIANTS[variant]
    ip = out.drop_duplicates(["reporterCode", "hs"])[
        [
            "reporterCode",
            "hs",
            "treated_main_clean_strict",
            spec["switch"],
            spec["compress"],
        ]
    ].copy()
    treated_ip = ip["treated_main_clean_strict"].eq(True)

    for pressure_type, col in [("switch", spec["switch"]), ("compress", spec["compress"])]:
        z_col = f"{col}_z_strict_common"
        values = ip.loc[treated_ip, col].astype(float)
        sd = values.std(ddof=0)
        if values.notna().sum() == 0 or pd.isna(sd) or sd <= 0:
            ip[z_col] = np.nan
        else:
            ip[z_col] = (ip[col] - values.mean()) / sd
        helper = f"{z_col}_for_interaction"
        ip[helper] = ip[z_col].where(ip[z_col].notna(), 0.0)
        out = out.merge(
            ip[["reporterCode", "hs", helper]],
            on=["reporterCode", "hs"],
            how="left",
        )
        out[f"D_common_{pressure_type}_{variant}"] = (
            out["D_staggered_common"] * out[helper].fillna(0.0)
        )

    return out


def fit_ppml(
    sample: pd.DataFrame,
    model_type: str,
    variant: str | None,
    x_cols: list[str],
) -> tuple[pd.DataFrame, dict]:
    keep_cols = ["trade_value_usd", "reporterCode", "hs", *x_cols, *FE]
    work = sample[keep_cols].dropna().copy()
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

    term_labels = {"D_staggered_common": "common staggered treated-China-post effect"}
    if variant is not None:
        term_labels[f"D_common_switch_{variant}"] = "switching-pressure interaction"
        term_labels[f"D_common_compress_{variant}"] = "compression-pressure interaction"

    rows = []
    for idx, term in enumerate(x_cols):
        beta = float(coef.loc[term])
        se_r = float(se_reporter[idx])
        se_p = float(se_product[idx])
        rows.append(
            {
                "model_type": model_type,
                "variant": variant or "average",
                "variant_description": VARIANTS.get(variant, {}).get(
                    "description", "common staggered average"
                ),
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
                "treated_products": int(
                    work.loc[work["D_staggered_common"].eq(1), "hs"].nunique()
                ),
                "formula": formula,
            }
        )

    diagnostics = {
        "model_type": model_type,
        "variant": variant or "average",
        "nobs": int(model._N),
        "rows_input": len(work),
        "dropped_separation": int(len(work) - int(model._N)),
        "reporter_clusters": int(work["reporter_cluster"].nunique()),
        "product_clusters": int(work["product_cluster"].nunique()),
        "formula": formula,
    }
    return pd.DataFrame(rows), diagnostics


def validate(results: pd.DataFrame) -> None:
    errors = []
    expected_rows = 1 + len(VARIANTS) * 3
    if len(results) != expected_rows:
        errors.append(f"expected {expected_rows} result rows, got {len(results)}")
    if results["coef"].isna().any():
        errors.append("missing coefficients")
    if not results["nobs"].gt(0).all():
        errors.append("nonpositive nobs")
    if errors:
        raise ValueError("; ".join(errors))


def write_runlog(results: pd.DataFrame, diagnostics: list[dict]) -> None:
    lines = [
        "# Common Staggered Pressure PPML Run",
        "",
        "Sample: strict clean treated products plus the same 12 donor products.",
        "",
        "Treated products: HS 2504, HS 8110, HS 8106, HS 284180.",
        "",
        "HS 261710 is excluded because it is sparse.",
        "",
        "Outcome: `trade_value_usd`.",
        "",
        "Fixed effects: importer-month, product-month, source-month, and importer-product-source.",
        "",
        "Pressure variables are standardized over strict clean treated importer-product cells.",
        "",
        "Reporter-clustered p-values are conditional diagnostics. Product-clustered p-values are weak with 16 product clusters and only 4 treated products.",
        "",
        "## Diagnostics",
        "",
    ]
    for item in diagnostics:
        lines.append(
            f"- {item['variant']}: nobs={item['nobs']}, "
            f"input rows={item['rows_input']}, dropped={item['dropped_separation']}, "
            f"reporters={item['reporter_clusters']}, products={item['product_clusters']}."
        )
    lines.extend(["", "## Results", ""])
    for _, row in results.iterrows():
        lines.append(
            f"- {row['variant']} / {row['term_label']}: coef={row['coef']:.4f}, "
            f"reporter p={row['p_reporter']:.4g}, product p={row['p_product']:.4g}, "
            f"effect={row['percent_effect']:.1f}%."
        )
    RUNLOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    sample = load_sample()
    all_results = []
    diagnostics = []

    print("Estimating common staggered average model ...", flush=True)
    result, diag = fit_ppml(
        sample,
        model_type="average",
        variant=None,
        x_cols=["D_staggered_common"],
    )
    all_results.append(result)
    diagnostics.append(diag)

    for variant in VARIANTS:
        print(f"Estimating common staggered / {variant} pressure model ...", flush=True)
        variant_sample = add_strict_pressure_terms(sample, variant)
        result, diag = fit_ppml(
            variant_sample,
            model_type="pressure",
            variant=variant,
            x_cols=[
                "D_staggered_common",
                f"D_common_switch_{variant}",
                f"D_common_compress_{variant}",
            ],
        )
        all_results.append(result)
        diagnostics.append(diag)

    results = pd.concat(all_results, ignore_index=True)
    validate(results)
    results.to_csv(RESULTS_PATH, index=False)
    write_runlog(results, diagnostics)

    print(f"Wrote {RESULTS_PATH}")
    print(f"Wrote {RUNLOG_PATH}")
    print(
        results[
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
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
