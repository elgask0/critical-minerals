#!/usr/bin/env python3
"""
Estimate product-specific source-share PPML pressure models.

Each clean treated product is estimated separately against the same 12 donor
products. This keeps the main source-contrast design but avoids pooling HS 8106
and HS 284180 inside Wave 4.
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
        "estimate_pressure_ppml_by_product.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_ppml_by_product_results.csv"
AUDIT_PATH = TABLES / "pressure_ppml_by_product_sample_audit.csv"
RUNLOG_PATH = TABLES / "pressure_ppml_by_product_run_log.md"


PRODUCTS = {
    "hs2504_graphite": {
        "label": "HS 2504 natural graphite",
        "wave": 2,
        "post_month": "202401",
        "treated_hs": "2504",
    },
    "hs8110_antimony_metal": {
        "label": "HS 8110 antimony metal",
        "wave": 3,
        "post_month": "202410",
        "treated_hs": "8110",
    },
    "hs8106_bismuth": {
        "label": "HS 8106 bismuth",
        "wave": 4,
        "post_month": "202503",
        "treated_hs": "8106",
    },
    "hs284180_tungstates": {
        "label": "HS 284180 tungstates",
        "wave": 4,
        "post_month": "202503",
        "treated_hs": "284180",
    },
}

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

CONTROL_ROLE = "candidate_control_pending_screen"
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


def load_panel() -> pd.DataFrame:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PANEL_PATH}. Run build_pressure_estimation_panel.py first."
        )
    return pd.read_csv(PANEL_PATH, dtype={"hs": str, "period": str}, low_memory=False)


def product_sample(panel: pd.DataFrame, product_key: str) -> pd.DataFrame:
    info = PRODUCTS[product_key]
    controls = panel["analysis_role"].eq(CONTROL_ROLE)
    treated = panel["hs"].eq(info["treated_hs"])
    sample = panel.loc[controls | treated].copy()
    sample["product_key"] = product_key
    sample["product_label"] = info["label"]
    sample["product_post_month"] = info["post_month"]
    sample["treated_product"] = sample["hs"].eq(info["treated_hs"])
    sample["post_product"] = sample["period"].ge(info["post_month"])
    sample["did_product"] = (
        sample["treated_product"] & sample["china_source"] & sample["post_product"]
    ).astype(int)
    return sample


def add_product_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
    out = sample.copy()
    spec = VARIANTS[variant]
    ip = out.drop_duplicates(["reporterCode", "hs"])[
        ["reporterCode", "hs", "treated_product", spec["switch"], spec["compress"]]
    ].copy()
    treated_ip = ip["treated_product"].eq(True)

    for pressure_type, col in [("switch", spec["switch"]), ("compress", spec["compress"])]:
        z_col = f"{col}_z_product"
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
        out[f"did_product_{pressure_type}_{variant}"] = (
            out["did_product"] * out[helper].fillna(0.0)
        )
    return out


def fit_ppml(
    sample: pd.DataFrame,
    product_key: str,
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

    term_labels = {"did_product": "baseline product treated-China-post effect"}
    if variant is not None:
        term_labels[f"did_product_switch_{variant}"] = "switching-pressure interaction"
        term_labels[f"did_product_compress_{variant}"] = "compression-pressure interaction"

    info = PRODUCTS[product_key]
    rows = []
    for idx, term in enumerate(x_cols):
        beta = float(coef.loc[term])
        se_r = float(se_reporter[idx])
        se_p = float(se_product[idx])
        rows.append(
            {
                "product_key": product_key,
                "product_label": info["label"],
                "wave_number": info["wave"],
                "post_month": info["post_month"],
                "treated_hs": info["treated_hs"],
                "model_type": model_type,
                "variant": variant or "average",
                "variant_description": VARIANTS.get(variant, {}).get(
                    "description", "average product DDD"
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
                "formula": formula,
            }
        )
    diagnostics = {
        "product_key": product_key,
        "model_type": model_type,
        "variant": variant or "average",
        "nobs": int(model._N),
        "rows_input": len(work),
        "dropped_separation": int(len(work) - int(model._N)),
        "reporter_clusters": int(work["reporter_cluster"].nunique()),
        "product_clusters": int(work["product_cluster"].nunique()),
    }
    return pd.DataFrame(rows), diagnostics


def sample_audit(samples: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for product_key, sample in samples.items():
        info = PRODUCTS[product_key]
        products = sample.drop_duplicates("hs")
        rows.append(
            {
                "product_key": product_key,
                "product_label": info["label"],
                "post_month": info["post_month"],
                "rows": len(sample),
                "reporters": sample["reporterCode"].nunique(),
                "products": sample["hs"].nunique(),
                "treated_product": info["treated_hs"],
                "control_products": int(products["analysis_role"].eq(CONTROL_ROLE).sum()),
                "months": sample["period"].nunique(),
                "sources": sample["source"].nunique(),
                "did_product_rows": int(sample["did_product"].sum()),
                "treated_china_post_positive": int(
                    sample.loc[sample["did_product"].eq(1), "trade_value_usd"].gt(0).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def validate(results: pd.DataFrame, audit: pd.DataFrame) -> None:
    errors = []
    expected_rows = len(PRODUCTS) * (1 + len(VARIANTS) * 3)
    if len(results) != expected_rows:
        errors.append(f"expected {expected_rows} result rows, got {len(results)}")
    if results["coef"].isna().any():
        errors.append("missing coefficients")
    if not results["nobs"].gt(0).all():
        errors.append("nonpositive nobs")
    if not audit["control_products"].eq(12).all():
        errors.append("not all products use 12 controls")
    if errors:
        raise ValueError("; ".join(errors))


def write_runlog(results: pd.DataFrame, audit: pd.DataFrame, diagnostics: list[dict]) -> None:
    lines = [
        "# Product-Specific Pressure PPML Run",
        "",
        "Each product uses the same 12 donor products.",
        "",
        "Fixed effects: importer-month, product-month, source-month, and importer-product-source.",
        "",
        "Reporter-clustered p-values are conditional diagnostics.",
        "",
        "## Sample Audit",
        "",
        audit.to_markdown(index=False),
        "",
        "## Diagnostics",
        "",
    ]
    for item in diagnostics:
        lines.append(
            f"- {item['product_key']} / {item['variant']}: nobs={item['nobs']}, "
            f"input rows={item['rows_input']}, dropped={item['dropped_separation']}, "
            f"reporters={item['reporter_clusters']}, products={item['product_clusters']}."
        )
    lines.extend(["", "## Results", ""])
    for _, row in results.iterrows():
        lines.append(
            f"- {row['product_label']} / {row['variant']} / {row['term_label']}: "
            f"coef={row['coef']:.4f}, reporter p={row['p_reporter']:.4g}, "
            f"effect={row['percent_effect']:.1f}%."
        )
    RUNLOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = load_panel()
    samples = {product_key: product_sample(panel, product_key) for product_key in PRODUCTS}
    audit = sample_audit(samples)
    all_results = []
    diagnostics = []

    for product_key, base_sample in samples.items():
        print(f"Estimating {product_key} average model ...", flush=True)
        result, diag = fit_ppml(
            base_sample,
            product_key,
            model_type="average",
            variant=None,
            x_cols=["did_product"],
        )
        all_results.append(result)
        diagnostics.append(diag)

        for variant in VARIANTS:
            print(f"Estimating {product_key} / {variant} pressure model ...", flush=True)
            sample = add_product_pressure_terms(base_sample, variant)
            result, diag = fit_ppml(
                sample,
                product_key,
                model_type="pressure",
                variant=variant,
                x_cols=[
                    "did_product",
                    f"did_product_switch_{variant}",
                    f"did_product_compress_{variant}",
                ],
            )
            all_results.append(result)
            diagnostics.append(diag)

    results = pd.concat(all_results, ignore_index=True)
    validate(results, audit)
    results.to_csv(RESULTS_PATH, index=False)
    audit.to_csv(AUDIT_PATH, index=False)
    write_runlog(results, audit, diagnostics)

    print(f"Wrote {RESULTS_PATH}")
    print(f"Wrote {AUDIT_PATH}")
    print(f"Wrote {RUNLOG_PATH}")
    print(
        results[
            [
                "product_label",
                "variant",
                "term_label",
                "coef",
                "se_reporter",
                "p_reporter",
                "percent_effect",
                "nobs",
                "dropped_separation",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
