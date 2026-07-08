#!/usr/bin/env python3
"""
Estimate wave-specific PPML pressure models for the clean treated sample.

Wave definition used here:

- Wave 2 graphite: HS 2504.
- Wave 3 antimony: HS 8110 only. HS 261710 is dropped because it is sparse.
- Wave 4 W/Bi: HS 8106 and HS 284180.

Each wave uses the same 12 donor products. Pressure variables are standardized
within the treated importer-product cells of the wave. This keeps the wave
models interpretable when a wave has only one treated product.
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
        "estimate_pressure_ppml_by_wave.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_ppml_by_wave_results.csv"
AUDIT_PATH = TABLES / "pressure_ppml_by_wave_sample_audit.csv"
RUNLOG_PATH = TABLES / "pressure_ppml_by_wave_run_log.md"


WAVES = {
    "wave2_graphite": {
        "wave": 2,
        "label": "Wave 2 graphite",
        "post_month": "202401",
        "treated_hs": ["2504"],
    },
    "wave3_antimony_clean": {
        "wave": 3,
        "label": "Wave 3 antimony clean",
        "post_month": "202410",
        "treated_hs": ["8110"],
    },
    "wave4_w_bi": {
        "wave": 4,
        "label": "Wave 4 W/Bi",
        "post_month": "202503",
        "treated_hs": ["8106", "284180"],
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


def wave_sample(panel: pd.DataFrame, wave_key: str) -> pd.DataFrame:
    info = WAVES[wave_key]
    treated_hs = set(info["treated_hs"])
    controls = panel["analysis_role"].eq(CONTROL_ROLE)
    treated = panel["hs"].isin(treated_hs)
    sample = panel.loc[controls | treated].copy()
    sample["wave_key"] = wave_key
    sample["wave_label"] = info["label"]
    sample["wave_post_month"] = info["post_month"]
    sample["treated_wave"] = sample["hs"].isin(treated_hs)
    sample["post_wave"] = sample["period"].ge(info["post_month"])
    sample["did_wave"] = (
        sample["treated_wave"] & sample["china_source"] & sample["post_wave"]
    ).astype(int)
    return sample


def add_wave_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
    out = sample.copy()
    spec = VARIANTS[variant]
    ip = out.drop_duplicates(["reporterCode", "hs"])[
        ["reporterCode", "hs", "treated_wave", spec["switch"], spec["compress"]]
    ].copy()
    treated_ip = ip["treated_wave"].eq(True)

    for pressure_type, col in [("switch", spec["switch"]), ("compress", spec["compress"])]:
        z_col = f"{col}_z_wave"
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
        out[f"did_wave_{pressure_type}_{variant}"] = (
            out["did_wave"] * out[helper].fillna(0.0)
        )
    return out


def fit_ppml(
    sample: pd.DataFrame,
    wave_key: str,
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

    term_labels = {"did_wave": "baseline wave treated-China-post effect"}
    if variant is not None:
        term_labels[f"did_wave_switch_{variant}"] = "switching-pressure interaction"
        term_labels[f"did_wave_compress_{variant}"] = "compression-pressure interaction"

    info = WAVES[wave_key]
    rows = []
    for idx, term in enumerate(x_cols):
        beta = float(coef.loc[term])
        se_r = float(se_reporter[idx])
        se_p = float(se_product[idx])
        rows.append(
            {
                "wave_key": wave_key,
                "wave_label": info["label"],
                "wave_number": info["wave"],
                "post_month": info["post_month"],
                "treated_hs": ",".join(info["treated_hs"]),
                "model_type": model_type,
                "variant": variant or "average",
                "variant_description": VARIANTS.get(variant, {}).get(
                    "description", "average wave DDD"
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
        "wave_key": wave_key,
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
    for wave_key, sample in samples.items():
        info = WAVES[wave_key]
        products = sample.drop_duplicates("hs")
        rows.append(
            {
                "wave_key": wave_key,
                "wave_label": info["label"],
                "post_month": info["post_month"],
                "rows": len(sample),
                "reporters": sample["reporterCode"].nunique(),
                "products": sample["hs"].nunique(),
                "treated_products": ",".join(info["treated_hs"]),
                "control_products": int(products["analysis_role"].eq(CONTROL_ROLE).sum()),
                "months": sample["period"].nunique(),
                "sources": sample["source"].nunique(),
                "did_wave_rows": int(sample["did_wave"].sum()),
                "treated_china_post_positive": int(
                    sample.loc[sample["did_wave"].eq(1), "trade_value_usd"].gt(0).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def write_runlog(results: pd.DataFrame, audits: pd.DataFrame, diagnostics: list[dict]) -> None:
    lines = [
        "# Wave-Specific Pressure PPML Run",
        "",
        "Each wave uses the same 12 donor products. Wave 1 is excluded because it has no clean treated HS product.",
        "",
        "Wave 3 drops HS 261710 because it is sparse.",
        "",
        "Fixed effects: importer-month, product-month, source-month, importer-product-source.",
        "",
        "Reporter-clustered p-values are conditional diagnostics. Product-clustered p-values are weak with 13 or 14 product clusters and only 1 or 2 treated products per wave.",
        "",
        "## Sample Audit",
        "",
        audits.to_markdown(index=False),
        "",
        "## Model Diagnostics",
        "",
    ]
    for item in diagnostics:
        lines.append(
            f"- {item['wave_key']} / {item['variant']}: nobs={item['nobs']}, "
            f"input rows={item['rows_input']}, dropped={item['dropped_separation']}, "
            f"reporters={item['reporter_clusters']}, products={item['product_clusters']}."
        )
    lines.extend(["", "## Average Wave Effects", ""])
    avg = results[
        results["model_type"].eq("average") & results["term"].eq("did_wave")
    ]
    for _, row in avg.iterrows():
        lines.append(
            f"- {row['wave_label']} ({row['treated_hs']}): coef={row['coef']:.4f}, "
            f"reporter p={row['p_reporter']:.4g}, product p={row['p_product']:.4g}, "
            f"effect={row['percent_effect']:.1f}%."
        )
    RUNLOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate(results: pd.DataFrame, audit: pd.DataFrame) -> None:
    errors = []
    expected_rows = len(WAVES) * (1 + len(VARIANTS) * 3)
    if len(results) != expected_rows:
        errors.append(f"expected {expected_rows} result rows, got {len(results)}")
    if results["coef"].isna().any():
        errors.append("missing coefficients")
    if not results["nobs"].gt(0).all():
        errors.append("nonpositive nobs")
    if not audit["control_products"].eq(12).all():
        errors.append("not all waves use 12 controls")
    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = load_panel()
    samples = {wave_key: wave_sample(panel, wave_key) for wave_key in WAVES}
    audit = sample_audit(samples)

    all_results = []
    diagnostics = []
    for wave_key, base_sample in samples.items():
        print(f"Estimating {wave_key} average model ...", flush=True)
        result, diag = fit_ppml(
            base_sample,
            wave_key,
            model_type="average",
            variant=None,
            x_cols=["did_wave"],
        )
        all_results.append(result)
        diagnostics.append(diag)

        for variant in VARIANTS:
            print(f"Estimating {wave_key} / {variant} pressure model ...", flush=True)
            sample = add_wave_pressure_terms(base_sample, variant)
            result, diag = fit_ppml(
                sample,
                wave_key,
                model_type="pressure",
                variant=variant,
                x_cols=[
                    "did_wave",
                    f"did_wave_switch_{variant}",
                    f"did_wave_compress_{variant}",
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
    print("\nSample audit:")
    print(audit.to_string(index=False))
    print("\nResults:")
    print(
        results[
            [
                "wave_label",
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
