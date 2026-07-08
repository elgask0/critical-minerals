#!/usr/bin/env python3
"""
Estimate product-specific mechanism PPML models.

Outcomes:
- China imports
- non-China imports
- total imports

Specification:
    y_ipt ~ D_product x pressure | importer-month + product-month + importer-product

The treated-post main effect is absorbed by product-month fixed effects. The
estimated terms therefore ask whether higher pressure importer-product pairs
move differently after the product-specific policy month.
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
        "estimate_pressure_mechanisms_by_product.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PRESSURE_PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "pressure_mechanisms_by_product_results.csv"
AUDIT_PATH = TABLES / "pressure_mechanisms_by_product_sample_audit.csv"


PRODUCTS = {
    "hs2504_graphite": {
        "label": "HS 2504 natural graphite",
        "wave": 2,
        "post_month": "202401",
        "treated_hs": ["2504"],
    },
    "hs8110_antimony_metal": {
        "label": "HS 8110 antimony metal",
        "wave": 3,
        "post_month": "202410",
        "treated_hs": ["8110"],
    },
    "hs8106_bismuth": {
        "label": "HS 8106 bismuth",
        "wave": 4,
        "post_month": "202503",
        "treated_hs": ["8106"],
    },
    "hs284180_tungstates": {
        "label": "HS 284180 tungstates",
        "wave": 4,
        "post_month": "202503",
        "treated_hs": ["284180"],
    },
}

VARIANTS = {
    "frequency": {
        "switch": "p_switch_frequency",
        "compress": "p_compress_frequency",
    },
    "capacity": {
        "switch": "p_switch_capacity",
        "compress": "p_compress_capacity",
    },
    "absorptive": {
        "switch": "p_switch_absorptive",
        "compress": "p_compress_absorptive",
    },
}

OUTCOMES = {
    "china": {
        "column": "china_primaryValue",
        "switch_expected": "<0",
        "compress_expected": "<0",
    },
    "row": {
        "column": "non_china_primaryValue",
        "switch_expected": ">0",
        "compress_expected": "<=0",
    },
    "total": {
        "column": "world_primaryValue",
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


def product_sample(panel: pd.DataFrame, product_key: str) -> pd.DataFrame:
    info = PRODUCTS[product_key]
    treated_hs = set(info["treated_hs"])
    controls = panel["analysis_role"].eq(CONTROL_ROLE)
    treated = panel["hs"].isin(treated_hs)
    sample = panel.loc[controls | treated].copy()
    sample["product_key"] = product_key
    sample["product_label"] = info["label"]
    sample["post_month"] = info["post_month"]
    sample["treated_product"] = sample["hs"].isin(treated_hs)
    sample["post_product"] = sample["period"].ge(info["post_month"])
    sample["D_product"] = (sample["treated_product"] & sample["post_product"]).astype(int)
    return sample


def add_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
    out = sample.copy()
    spec = VARIANTS[variant]
    ip = out.drop_duplicates(["reporterCode", "hs"])[
        ["reporterCode", "hs", "treated_product", spec["switch"], spec["compress"]]
    ].copy()
    treated_ip = ip["treated_product"].eq(True)

    for pressure_type, col in [("switch", spec["switch"]), ("compress", spec["compress"])]:
        z_col = f"{col}_z_product_mechanism"
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
        out[f"D_product_{pressure_type}_{variant}"] = (
            out["D_product"] * out[helper].fillna(0.0)
        )
    return out


def fit_ppml(
    sample: pd.DataFrame,
    product_key: str,
    outcome_key: str,
    variant: str,
) -> pd.DataFrame:
    outcome = OUTCOMES[outcome_key]
    x_cols = [
        f"D_product_switch_{variant}",
        f"D_product_compress_{variant}",
    ]
    work = sample[[outcome["column"], "reporterCode", "hs", *x_cols, *FE]].dropna().copy()
    work = work.rename(columns={outcome["column"]: "y"})
    work["reporter_cluster"] = work["reporterCode"].astype(str)
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
    info = PRODUCTS[product_key]
    expected = {
        f"D_product_switch_{variant}": outcome["switch_expected"],
        f"D_product_compress_{variant}": outcome["compress_expected"],
    }
    rows = []
    for idx, term in enumerate(x_cols):
        beta = float(coef.loc[term])
        se = float(se_reporter[idx])
        rows.append(
            {
                "product_key": product_key,
                "product_label": info["label"],
                "wave_number": info["wave"],
                "post_month": info["post_month"],
                "treated_hs": ",".join(info["treated_hs"]),
                "outcome": outcome_key,
                "variant": variant,
                "term": term,
                "term_label": "switching-pressure interaction"
                if "switch" in term
                else "compression-pressure interaction",
                "expected_sign": expected[term],
                "coef": beta,
                "se_reporter": se,
                "p_reporter": p_value(beta, se),
                "percent_effect": percent_effect(beta),
                "nobs": int(model._N),
                "rows_input": len(work),
                "dropped_separation": int(len(work) - int(model._N)),
                "reporter_clusters": int(work["reporter_cluster"].nunique()),
                "formula": formula,
            }
        )
    return pd.DataFrame(rows)


def sample_audit(samples: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for product_key, sample in samples.items():
        info = PRODUCTS[product_key]
        rows.append(
            {
                "product_key": product_key,
                "product_label": info["label"],
                "post_month": info["post_month"],
                "rows": len(sample),
                "reporters": sample["reporterCode"].nunique(),
                "products": sample["hs"].nunique(),
                "treated_product": ",".join(info["treated_hs"]),
                "months": sample["period"].nunique(),
                "treated_post_rows": int(sample["D_product"].sum()),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    wide, pressure = load_inputs()
    panel = prepare_base_panel(wide, pressure)
    samples = {key: product_sample(panel, key) for key in PRODUCTS}
    audit = sample_audit(samples)
    results = []
    for product_key, base_sample in samples.items():
        for variant in VARIANTS:
            sample = add_pressure_terms(base_sample, variant)
            for outcome_key in OUTCOMES:
                print(f"Estimating {product_key} / {outcome_key} / {variant} ...", flush=True)
                results.append(fit_ppml(sample, product_key, outcome_key, variant))
    out = pd.concat(results, ignore_index=True)
    out.to_csv(RESULTS_PATH, index=False)
    audit.to_csv(AUDIT_PATH, index=False)
    print(f"Wrote {RESULTS_PATH}")
    print(f"Wrote {AUDIT_PATH}")
    print(
        out[
            [
                "product_label",
                "outcome",
                "variant",
                "term_label",
                "coef",
                "p_reporter",
                "percent_effect",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
