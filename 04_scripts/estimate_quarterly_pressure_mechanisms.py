#!/usr/bin/env python3
"""
Estimate quarterly mechanism PPML models for the clean pressure design.

This script is the quarterly counterpart to the monthly mechanism scripts. It
collapses the importer-product-month panel to importer-product-quarter and
estimates China, rest-of-world, and total import outcomes with pressure
interactions.

Preferred use:

    python 04_scripts/estimate_quarterly_pressure_mechanisms.py

Output:

    03_data/output/tables/quarterly_pressure_mechanisms_first_full_post.csv
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
        "estimate_quarterly_pressure_mechanisms.py requires pyfixest in the "
        "repository-local prefix."
    ) from exc


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PRESSURE_PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
RESULTS_PATH = TABLES / "quarterly_pressure_mechanisms_first_full_post.csv"

CONTROL_ROLE = "candidate_control_pending_screen"

GROUPS = {
    "wave2_graphite": {
        "family": "wave",
        "label": "Wave 2 graphite",
        "treated_hs": ["2504"],
        "post_quarter": "2024Q1",
    },
    "wave3_antimony_clean": {
        "family": "wave",
        "label": "Wave 3 antimony metal",
        "treated_hs": ["8110"],
        "post_quarter": "2024Q4",
    },
    "wave4_w_bi": {
        "family": "wave",
        "label": "Wave 4 W/Bi",
        "treated_hs": ["8106", "284180"],
        "post_quarter": "2025Q2",
    },
    "hs2504_graphite": {
        "family": "product",
        "label": "HS 2504 graphite",
        "treated_hs": ["2504"],
        "post_quarter": "2024Q1",
    },
    "hs8110_antimony_metal": {
        "family": "product",
        "label": "HS 8110 antimony metal",
        "treated_hs": ["8110"],
        "post_quarter": "2024Q4",
    },
    "hs8106_bismuth": {
        "family": "product",
        "label": "HS 8106 bismuth",
        "treated_hs": ["8106"],
        "post_quarter": "2025Q2",
    },
    "hs284180_tungstates": {
        "family": "product",
        "label": "HS 284180 tungstates",
        "treated_hs": ["284180"],
        "post_quarter": "2025Q2",
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
        "label": "RoW imports",
        "switch_expected": ">0",
        "compress_expected": "~0 or <=0",
    },
    "total": {
        "column": "world_primaryValue",
        "label": "Total imports",
        "switch_expected": ">=0",
        "compress_expected": "<0",
    },
}

FE = ["fe_importer_quarter", "fe_product_quarter", "fe_importer_product"]


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def month_to_quarter(period: str) -> str:
    year = int(period[:4])
    month = int(period[4:6])
    quarter = (month - 1) // 3 + 1
    return f"{year}Q{quarter}"


def load_quarterly_panel() -> pd.DataFrame:
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
        *[col for spec in VARIANTS.values() for col in [spec["switch"], spec["compress"]]],
    ]
    pressure = pd.read_csv(
        PRESSURE_PANEL_PATH,
        dtype={"hs": str},
        usecols=pressure_cols,
        low_memory=False,
    ).drop_duplicates(["reporterCode", "hs"])

    panel = wide.merge(pressure, on=["reporterCode", "hs"], how="left", validate="m:1")
    panel["quarter"] = panel["period"].map(month_to_quarter)

    meta_cols = [
        "product",
        "analysis_role",
        *[col for spec in VARIANTS.values() for col in [spec["switch"], spec["compress"]]],
    ]
    aggregation = {col: (col, "first") for col in meta_cols}
    for outcome in OUTCOMES.values():
        aggregation[outcome["column"]] = (outcome["column"], "sum")

    quarterly = panel.groupby(["reporterCode", "quarter", "hs"], as_index=False).agg(
        **aggregation
    )
    quarterly["fe_importer_quarter"] = (
        quarterly["reporterCode"].astype(str) + "_" + quarterly["quarter"]
    )
    quarterly["fe_product_quarter"] = quarterly["hs"] + "_" + quarterly["quarter"]
    quarterly["fe_importer_product"] = (
        quarterly["reporterCode"].astype(str) + "_" + quarterly["hs"]
    )
    return quarterly


def group_sample(panel: pd.DataFrame, group_key: str) -> pd.DataFrame:
    group = GROUPS[group_key]
    treated_hs = set(group["treated_hs"])
    sample = panel.loc[
        panel["analysis_role"].eq(CONTROL_ROLE) | panel["hs"].isin(treated_hs)
    ].copy()
    sample["treated_group"] = sample["hs"].isin(treated_hs)
    sample["post_group"] = sample["quarter"].ge(group["post_quarter"])
    sample["D_group"] = (sample["treated_group"] & sample["post_group"]).astype(int)
    return sample


def add_pressure_terms(sample: pd.DataFrame, variant: str) -> pd.DataFrame:
    out = sample.copy()
    spec = VARIANTS[variant]
    ip = out.drop_duplicates(["reporterCode", "hs"])[
        ["reporterCode", "hs", "treated_group", spec["switch"], spec["compress"]]
    ].copy()
    treated_ip = ip["treated_group"].eq(True)

    for pressure_type, col in [("switch", spec["switch"]), ("compress", spec["compress"])]:
        values = ip.loc[treated_ip, col].astype(float)
        sd = values.std(ddof=0)
        z_col = f"{pressure_type}_z"
        if values.notna().sum() == 0 or pd.isna(sd) or sd <= 0:
            ip[z_col] = np.nan
        else:
            ip[z_col] = (ip[col] - values.mean()) / sd

    out = out.merge(
        ip[["reporterCode", "hs", "switch_z", "compress_z"]],
        on=["reporterCode", "hs"],
        how="left",
    )
    out["D_switch"] = out["D_group"] * out["switch_z"].fillna(0.0)
    out["D_compress"] = out["D_group"] * out["compress_z"].fillna(0.0)
    return out


def fit_model(
    sample: pd.DataFrame,
    group_key: str,
    variant: str,
    outcome_key: str,
) -> list[dict]:
    outcome = OUTCOMES[outcome_key]
    keep_cols = [
        outcome["column"],
        "reporterCode",
        "hs",
        "D_switch",
        "D_compress",
        *FE,
    ]
    work = sample[keep_cols].dropna().copy()
    work = work.rename(columns={outcome["column"]: "y"})
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"y ~ D_switch + D_compress | {' + '.join(FE)}"

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

    coef = model.coef().reindex(["D_switch", "D_compress"])
    vcov = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se = np.sqrt(np.diag(vcov))
    group = GROUPS[group_key]

    rows = []
    for idx, term in enumerate(["D_switch", "D_compress"]):
        beta = float(coef.loc[term])
        stderr = float(se[idx])
        term_label = "switch" if term == "D_switch" else "compress"
        rows.append(
            {
                "group_key": group_key,
                "group_family": group["family"],
                "group_label": group["label"],
                "post_quarter": group["post_quarter"],
                "variant": variant,
                "variant_description": VARIANTS[variant]["description"],
                "outcome": outcome_key,
                "outcome_label": outcome["label"],
                "term": term_label,
                "expected_sign": (
                    outcome["switch_expected"]
                    if term_label == "switch"
                    else outcome["compress_expected"]
                ),
                "coef": beta,
                "se_reporter": stderr,
                "p_reporter": p_value(beta, stderr),
                "percent_effect": percent_effect(beta),
                "nobs": int(model._N),
                "input_rows": len(work),
                "dropped_separation": int(len(work) - int(model._N)),
                "reporter_clusters": int(work["reporter_cluster"].nunique()),
                "formula": formula,
            }
        )
    return rows


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = load_quarterly_panel()
    rows: list[dict] = []

    for group_key in GROUPS:
        sample = group_sample(panel, group_key)
        for variant in VARIANTS:
            variant_sample = add_pressure_terms(sample, variant)
            for outcome_key in OUTCOMES:
                rows.extend(fit_model(variant_sample, group_key, variant, outcome_key))

    results = pd.DataFrame(rows)
    results.to_csv(RESULTS_PATH, index=False)
    print(f"Wrote {RESULTS_PATH} ({len(results)} rows)")


if __name__ == "__main__":
    main()
