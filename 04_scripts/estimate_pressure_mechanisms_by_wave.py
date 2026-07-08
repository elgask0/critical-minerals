#!/usr/bin/env python3
"""
Estimate wave-specific mechanism PPML models.

These models use importer-product-month outcomes:

- China imports
- non-China imports
- total imports

The source-share PPML model estimates the China-source decline. These mechanism
models ask whether pre-policy pressure indexes predict the margin of adjustment:
China-source decline, rest-of-world replacement, and total-import compression.

The specification includes importer-month, product-month, and importer-product
fixed effects. The common treated-post effect is therefore absorbed by the
product-month fixed effect. The estimated terms are the interactions between
treated-post status and standardized pressure indexes.
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
        "estimate_pressure_mechanisms_by_wave.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PRESSURE_PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_mechanisms_by_wave_results.csv"
AUDIT_PATH = TABLES / "pressure_mechanisms_by_wave_sample_audit.csv"
RUNLOG_PATH = TABLES / "pressure_mechanisms_by_wave_run_log.md"


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

OUTCOMES = {
    "china": {
        "column": "china_primaryValue",
        "label": "China imports",
        "switch_expected": "<0",
        "compress_expected": "<0",
    },
    "row": {
        "column": "non_china_primaryValue",
        "label": "Rest-of-world imports",
        "switch_expected": ">0",
        "compress_expected": "<=0",
    },
    "total": {
        "column": "world_primaryValue",
        "label": "Total imports",
        "switch_expected": ">=0",
        "compress_expected": "<0",
    },
}

CONTROL_ROLE = "candidate_control_pending_screen"
FE = ["fe_importer_month", "fe_product_month", "fe_importer_product"]


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = [
        path
        for path in [WIDE_PATH, PRESSURE_PANEL_PATH]
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(f"Missing required input(s): {missing}")

    wide = pd.read_csv(WIDE_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    pressure_cols = [
        "reporterCode",
        "hs",
        "p_switch_frequency",
        "p_compress_frequency",
        "p_switch_capacity",
        "p_compress_capacity",
        "p_switch_absorptive",
        "p_compress_absorptive",
    ]
    pressure = pd.read_csv(
        PRESSURE_PANEL_PATH,
        dtype={"hs": str},
        usecols=pressure_cols,
        low_memory=False,
    ).drop_duplicates(["reporterCode", "hs"])
    return wide, pressure


def prepare_base_panel(wide: pd.DataFrame, pressure: pd.DataFrame) -> pd.DataFrame:
    panel = wide.merge(pressure, on=["reporterCode", "hs"], how="left", validate="m:1")
    panel["fe_importer_month"] = panel["reporterCode"].astype(str) + "_" + panel["period"]
    panel["fe_product_month"] = panel["hs"] + "_" + panel["period"]
    panel["fe_importer_product"] = panel["reporterCode"].astype(str) + "_" + panel["hs"]
    return panel


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
    sample["D_wave"] = (sample["treated_wave"] & sample["post_wave"]).astype(int)
    return sample


def add_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
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
        out[f"D_wave_{pressure_type}_{variant}"] = out["D_wave"] * out[helper].fillna(0.0)
    return out


def fit_ppml(
    sample: pd.DataFrame,
    wave_key: str,
    outcome_key: str,
    variant: str,
) -> tuple[pd.DataFrame, dict]:
    outcome = OUTCOMES[outcome_key]
    x_cols = [
        f"D_wave_switch_{variant}",
        f"D_wave_compress_{variant}",
    ]
    keep_cols = [outcome["column"], "reporterCode", "hs", *x_cols, *FE]
    work = sample[keep_cols].dropna().copy()
    work = work.rename(columns={outcome["column"]: "y"})
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    work["product_cluster"] = work["hs"].astype(str)
    formula = f"y ~ {' + '.join(x_cols)} | {' + '.join(FE)}"

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

    info = WAVES[wave_key]
    term_labels = {
        f"D_wave_switch_{variant}": "switching-pressure interaction",
        f"D_wave_compress_{variant}": "compression-pressure interaction",
    }
    expected = {
        f"D_wave_switch_{variant}": outcome["switch_expected"],
        f"D_wave_compress_{variant}": outcome["compress_expected"],
    }

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
                "outcome": outcome_key,
                "outcome_label": outcome["label"],
                "variant": variant,
                "variant_description": VARIANTS[variant]["description"],
                "term": term,
                "term_label": term_labels[term],
                "expected_sign": expected[term],
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
        "outcome": outcome_key,
        "variant": variant,
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
                "treated_post_rows": int(sample["D_wave"].sum()),
                "treated_china_positive_post_rows": int(
                    sample.loc[sample["D_wave"].eq(1), "china_primaryValue"].gt(0).sum()
                ),
                "treated_row_positive_post_rows": int(
                    sample.loc[sample["D_wave"].eq(1), "non_china_primaryValue"].gt(0).sum()
                ),
                "treated_total_positive_post_rows": int(
                    sample.loc[sample["D_wave"].eq(1), "world_primaryValue"].gt(0).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def validate(results: pd.DataFrame, audit: pd.DataFrame) -> None:
    errors = []
    expected_rows = len(WAVES) * len(OUTCOMES) * len(VARIANTS) * 2
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


def write_runlog(results: pd.DataFrame, audit: pd.DataFrame, diagnostics: list[dict]) -> None:
    lines = [
        "# Wave-Specific Mechanism PPML Run",
        "",
        "Outcomes: China imports, rest-of-world imports, and total imports.",
        "",
        "Fixed effects: importer-month, product-month, and importer-product.",
        "",
        "The treated-post main effect is absorbed by product-month fixed effects. Only pressure interactions are estimated.",
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
            f"- {item['wave_key']} / {item['outcome']} / {item['variant']}: "
            f"nobs={item['nobs']}, input rows={item['rows_input']}, "
            f"dropped={item['dropped_separation']}, "
            f"reporters={item['reporter_clusters']}, products={item['product_clusters']}."
        )
    lines.extend(["", "## Results", ""])
    for _, row in results.iterrows():
        lines.append(
            f"- {row['wave_label']} / {row['outcome']} / {row['variant']} / "
            f"{row['term_label']}: coef={row['coef']:.4f}, "
            f"reporter p={row['p_reporter']:.4g}, "
            f"effect={row['percent_effect']:.1f}%."
        )
    RUNLOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    wide, pressure = load_inputs()
    panel = prepare_base_panel(wide, pressure)
    samples = {wave_key: wave_sample(panel, wave_key) for wave_key in WAVES}
    audit = sample_audit(samples)

    all_results = []
    diagnostics = []
    for wave_key, base_sample in samples.items():
        for variant in VARIANTS:
            print(f"Preparing {wave_key} / {variant} ...", flush=True)
            sample = add_pressure_terms(base_sample, variant)
            for outcome_key in OUTCOMES:
                print(
                    f"Estimating {wave_key} / {outcome_key} / {variant} ...",
                    flush=True,
                )
                result, diag = fit_ppml(sample, wave_key, outcome_key, variant)
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
                "wave_label",
                "outcome",
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
