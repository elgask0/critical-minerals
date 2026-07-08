#!/usr/bin/env python3
"""
Build the frozen source-level panel for preliminary pressure-index PPML models.

The output keeps the expanded Comtrade source panel intact and adds the three
current pressure variants:

1. frequency access: importer ever/regularly used RoW before policy;
2. capacity access: importer RoW value relative to China value before policy;
3. scale-adjusted absorptive: exposed China trade split by estimated switching
   capacity, where total pressure equals China exposure.

This script does not estimate regressions. It prepares and validates the panel
needed for the next PPML step.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

SOURCE_PATH = PROCESSED / "comtrade_pressure_source_panel.csv"
WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PRESSURE_PATH = PROCESSED / "pressure_indices_importer_product.csv"

ESTIMATION_PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"
SAMPLE_AUDIT_PATH = TABLES / "pressure_ppml_estimation_sample_audit.csv"
PRODUCT_AUDIT_PATH = TABLES / "pressure_ppml_estimation_product_audit.csv"
VARIANT_AUDIT_PATH = TABLES / "pressure_ppml_pressure_variant_audit.csv"


MAIN_CLEAN_ROLES = {"main_clean_treated", "main_clean_treated_sparse_caution"}
SECONDARY_ROLES = {"secondary_scope_case"}
CONTROL_ROLE = "candidate_control_pending_screen"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    missing = [
        path
        for path in [SOURCE_PATH, WIDE_PATH, PRESSURE_PATH]
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(f"Missing required input(s): {missing}")

    source = pd.read_csv(
        SOURCE_PATH,
        dtype={"hs": str, "period": str},
        low_memory=False,
    )
    wide = pd.read_csv(
        WIDE_PATH,
        dtype={"hs": str, "period": str},
        low_memory=False,
    )
    pressure = pd.read_csv(PRESSURE_PATH, dtype={"hs": str}, low_memory=False)
    return source, wide, pressure


def capacity_access(row: pd.Series) -> float:
    china = float(row["pre_china_value"])
    row_value = float(row["pre_row_value"])
    if china > 0:
        return min(1.0, row_value / china)
    if row_value > 0:
        return 1.0
    return 0.0


def add_market_scale(pressure: pd.DataFrame, wide: pd.DataFrame) -> pd.DataFrame:
    out = pressure.copy()
    policy = out["has_policy_event"].eq(True)
    out["china_market_value_loo"] = np.nan

    for hs, group in out.loc[policy].groupby("hs", sort=False):
        announcement_period = str(group["announcement_period"].iloc[0])
        pre = wide[wide["hs"].eq(hs) & wide["period"].lt(announcement_period)].copy()
        china_by_reporter = pre.groupby("reporterCode")["china_primaryValue"].sum()
        total_china = float(china_by_reporter.sum())

        for idx, row in group.iterrows():
            reporter = row["reporterCode"]
            own_china = float(china_by_reporter.get(reporter, 0.0))
            out.at[idx, "china_market_value_loo"] = max(total_china - own_china, 0.0)

    out["row_market_scale_loo"] = np.nan
    valid = policy & out["china_market_value_loo"].gt(0)
    out.loc[valid, "row_market_scale_loo"] = np.minimum(
        1.0,
        out.loc[valid, "row_total_value_loo"] / out.loc[valid, "china_market_value_loo"],
    )

    no_china = policy & out["china_market_value_loo"].le(0)
    out.loc[no_china, "row_market_scale_loo"] = np.where(
        out.loc[no_china, "row_total_value_loo"].gt(0), 1.0, 0.0
    )
    return out


def add_pressure_variants(pressure: pd.DataFrame, wide: pd.DataFrame) -> pd.DataFrame:
    out = add_market_scale(pressure, wide)
    policy = out["has_policy_event"].eq(True)

    # Variant 1: frequency access, current canonical construction.
    out["o_row_frequency"] = out["o_row_access"]
    out["p_switch_frequency"] = out["p_switch"]
    out["p_compress_frequency"] = out["p_compress"]
    out["p_x_frequency"] = out["p_x_decline"]

    # Variant 2: capacity access, current diagnostic construction.
    out["o_row_capacity"] = np.nan
    out.loc[policy, "o_row_capacity"] = out.loc[policy].apply(capacity_access, axis=1)
    out["p_switch_capacity"] = np.where(
        policy,
        out["e_china_exposure"] * out["o_row_capacity"] * out["a_row_strength_loo"],
        np.nan,
    )
    out["p_compress_capacity"] = np.where(
        policy,
        out["e_china_exposure"]
        * (1 - out["o_row_capacity"])
        * out["r_replacement_rigidity_loo"],
        np.nan,
    )
    out["p_x_capacity"] = out["p_switch_capacity"] + out["p_compress_capacity"]

    # Variant 3: scale-adjusted absorptive construction.
    out["a_row_strength_scaled_loo"] = np.where(
        policy,
        out["a_row_strength_loo"] * out["row_market_scale_loo"],
        np.nan,
    )
    out["q_switch_absorptive"] = np.where(
        policy,
        out["o_row_frequency"] * out["a_row_strength_scaled_loo"],
        np.nan,
    )
    out["p_switch_absorptive"] = np.where(
        policy,
        out["e_china_exposure"] * out["q_switch_absorptive"],
        np.nan,
    )
    out["p_compress_absorptive"] = np.where(
        policy,
        out["e_china_exposure"] * (1 - out["q_switch_absorptive"]),
        np.nan,
    )
    out["p_x_absorptive"] = out["p_switch_absorptive"] + out["p_compress_absorptive"]

    # Experimental full-capacity variant kept for later sensitivity checks, not
    # counted as one of the three frozen headline variants.
    out["q_switch_capacity_scaled"] = np.where(
        policy,
        out["o_row_capacity"] * out["a_row_strength_scaled_loo"],
        np.nan,
    )
    out["p_switch_capacity_scaled"] = np.where(
        policy,
        out["e_china_exposure"] * out["q_switch_capacity_scaled"],
        np.nan,
    )
    out["p_compress_capacity_scaled"] = np.where(
        policy,
        out["e_china_exposure"] * (1 - out["q_switch_capacity_scaled"]),
        np.nan,
    )

    return out


def standardize_for_sample(df: pd.DataFrame, mask: pd.Series, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        z_col = f"{col}_z_main_clean"
        helper_col = f"{z_col}_for_interaction"
        values = out.loc[mask, col].astype(float)
        sd = values.std(ddof=0)
        if values.notna().sum() == 0 or pd.isna(sd) or sd <= 0:
            out[z_col] = np.nan
        else:
            out[z_col] = (out[col] - values.mean()) / sd
        out[helper_col] = out[z_col].where(out[z_col].notna(), 0.0)
    return out


def prepare_pressure_for_merge(pressure: pd.DataFrame, wide: pd.DataFrame) -> pd.DataFrame:
    out = add_pressure_variants(pressure, wide)
    out["is_main_clean_pressure_product"] = out["analysis_role"].isin(MAIN_CLEAN_ROLES)
    out["is_secondary_pressure_product"] = out["analysis_role"].isin(SECONDARY_ROLES)
    out["is_control_pressure_product"] = out["analysis_role"].eq(CONTROL_ROLE)

    pressure_cols = [
        "p_switch_frequency",
        "p_compress_frequency",
        "p_x_frequency",
        "p_switch_capacity",
        "p_compress_capacity",
        "p_x_capacity",
        "p_switch_absorptive",
        "p_compress_absorptive",
        "p_x_absorptive",
    ]
    main_mask = out["is_main_clean_pressure_product"].eq(True)
    out = standardize_for_sample(out, main_mask, pressure_cols)

    keep = [
        "reporterCode",
        "hs",
        "pre_month_count",
        "pre_china_value",
        "pre_row_value",
        "pre_world_value",
        "pre_row_positive_months",
        "has_policy_event",
        "e_china_exposure",
        "o_row_frequency",
        "o_row_capacity",
        "row_supplier_count_loo",
        "row_total_value_loo",
        "row_hhi_loo",
        "row_diversification_loo",
        "row_depth_loo",
        "a_row_strength_loo",
        "r_replacement_rigidity_loo",
        "china_market_value_loo",
        "row_market_scale_loo",
        "a_row_strength_scaled_loo",
        "q_switch_absorptive",
        "q_switch_capacity_scaled",
        "is_main_clean_pressure_product",
        "is_secondary_pressure_product",
        "is_control_pressure_product",
        "p_switch_capacity_scaled",
        "p_compress_capacity_scaled",
    ]
    for col in pressure_cols:
        keep.extend([col, f"{col}_z_main_clean", f"{col}_z_main_clean_for_interaction"])
    return out[keep].copy()


def add_sample_flags(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    out["sample_main_clean"] = out["analysis_role"].isin(MAIN_CLEAN_ROLES) | out[
        "analysis_role"
    ].eq(CONTROL_ROLE)
    out["sample_main_clean_strict"] = out["analysis_role"].isin(
        {"main_clean_treated"}
    ) | out["analysis_role"].eq(CONTROL_ROLE)
    out["sample_all_policy_plus_controls"] = out["analysis_role"].isin(
        MAIN_CLEAN_ROLES | SECONDARY_ROLES | {CONTROL_ROLE}
    )
    out["sample_secondary_scope_plus_controls"] = out["analysis_role"].isin(
        SECONDARY_ROLES | {CONTROL_ROLE}
    )

    out["treated_main_clean"] = out["analysis_role"].isin(MAIN_CLEAN_ROLES)
    out["treated_main_clean_strict"] = out["analysis_role"].eq("main_clean_treated")
    out["treated_any_policy"] = out["analysis_role"].isin(MAIN_CLEAN_ROLES | SECONDARY_ROLES)
    out["treated_secondary_scope"] = out["analysis_role"].isin(SECONDARY_ROLES)

    out["did_main_clean"] = (
        out["treated_main_clean"] & out["china_source"] & out["post_import_effect"]
    )
    out["did_main_clean_strict"] = (
        out["treated_main_clean_strict"]
        & out["china_source"]
        & out["post_import_effect"]
    )
    out["did_any_policy"] = (
        out["treated_any_policy"] & out["china_source"] & out["post_import_effect"]
    )
    return out


def add_interactions(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    variants = {
        "frequency": ("p_switch_frequency", "p_compress_frequency", "p_x_frequency"),
        "capacity": ("p_switch_capacity", "p_compress_capacity", "p_x_capacity"),
        "absorptive": (
            "p_switch_absorptive",
            "p_compress_absorptive",
            "p_x_absorptive",
        ),
    }

    for variant, cols in variants.items():
        switch_col, compress_col, x_col = cols
        for pressure_type, col in [
            ("switch", switch_col),
            ("compress", compress_col),
            ("x", x_col),
        ]:
            helper = f"{col}_z_main_clean_for_interaction"
            out[f"did_main_clean_{pressure_type}_{variant}"] = (
                out["did_main_clean"].astype(int) * out[helper].fillna(0.0)
            )
            out[f"did_main_clean_strict_{pressure_type}_{variant}"] = (
                out["did_main_clean_strict"].astype(int) * out[helper].fillna(0.0)
            )

    # Fixed-effect keys for source-level PPML.
    out["fe_importer_month"] = out["reporterCode"].astype(str) + "_" + out["period"]
    out["fe_product_month"] = out["hs"] + "_" + out["period"]
    out["fe_source_month"] = out["source"].astype(str) + "_" + out["period"]
    out["fe_importer_product_source"] = (
        out["reporterCode"].astype(str)
        + "_"
        + out["hs"]
        + "_"
        + out["source"].astype(str)
    )
    return out


def weighted_average(values: pd.Series, weights: pd.Series) -> float:
    valid = values.notna() & weights.notna()
    if not valid.any():
        return np.nan
    if weights[valid].sum() > 0:
        return float((values[valid] * weights[valid]).sum() / weights[valid].sum())
    return float(values[valid].mean())


def build_product_audit(panel: pd.DataFrame) -> pd.DataFrame:
    product = panel.drop_duplicates(["reporterCode", "hs"])[
        [
            "reporterCode",
            "hs",
            "product",
            "analysis_role",
            "scope_status",
            "wave",
            "pre_world_value",
            "e_china_exposure",
            "o_row_frequency",
            "o_row_capacity",
            "a_row_strength_loo",
            "a_row_strength_scaled_loo",
            "p_switch_frequency",
            "p_compress_frequency",
            "p_switch_capacity",
            "p_compress_capacity",
            "p_switch_absorptive",
            "p_compress_absorptive",
            "p_x_absorptive",
        ]
    ].copy()

    rows = []
    for hs, group in product.groupby("hs", sort=False):
        weights = group["pre_world_value"].fillna(0)
        rows.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "scope_status": group["scope_status"].iloc[0],
                "wave": group["wave"].iloc[0],
                "importer_products": len(group),
                "pre_world_value_sum": weights.sum(),
                "weighted_china_exposure": weighted_average(
                    group["e_china_exposure"], weights
                ),
                "weighted_row_frequency": weighted_average(
                    group["o_row_frequency"], weights
                ),
                "weighted_row_capacity": weighted_average(group["o_row_capacity"], weights),
                "weighted_row_strength": weighted_average(
                    group["a_row_strength_loo"], weights
                ),
                "weighted_row_strength_scaled": weighted_average(
                    group["a_row_strength_scaled_loo"], weights
                ),
                "weighted_switch_frequency": weighted_average(
                    group["p_switch_frequency"], weights
                ),
                "weighted_compress_frequency": weighted_average(
                    group["p_compress_frequency"], weights
                ),
                "weighted_switch_capacity": weighted_average(
                    group["p_switch_capacity"], weights
                ),
                "weighted_compress_capacity": weighted_average(
                    group["p_compress_capacity"], weights
                ),
                "weighted_switch_absorptive": weighted_average(
                    group["p_switch_absorptive"], weights
                ),
                "weighted_compress_absorptive": weighted_average(
                    group["p_compress_absorptive"], weights
                ),
                "weighted_x_absorptive": weighted_average(
                    group["p_x_absorptive"], weights
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(["analysis_role", "hs"], kind="stable")


def build_sample_audit(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sample_cols = [
        "sample_main_clean",
        "sample_main_clean_strict",
        "sample_all_policy_plus_controls",
        "sample_secondary_scope_plus_controls",
    ]
    for col in sample_cols:
        sample = panel[panel[col].eq(True)]
        products = sample[["hs", "analysis_role"]].drop_duplicates()
        rows.append(
            {
                "sample": col,
                "rows": len(sample),
                "reporters": sample["reporterCode"].nunique(),
                "products": sample["hs"].nunique(),
                "months": sample["period"].nunique(),
                "sources": sample["source"].nunique(),
                "treated_products_main_clean": int(
                    products["analysis_role"].isin(MAIN_CLEAN_ROLES).sum()
                ),
                "treated_products_secondary": int(
                    products["analysis_role"].isin(SECONDARY_ROLES).sum()
                ),
                "control_products": int(products["analysis_role"].eq(CONTROL_ROLE).sum()),
                "did_main_clean_rows": int(sample["did_main_clean"].sum()),
                "did_main_clean_strict_rows": int(sample["did_main_clean_strict"].sum()),
                "did_any_policy_rows": int(sample["did_any_policy"].sum()),
            }
        )
    return pd.DataFrame(rows)


def build_variant_audit(panel: pd.DataFrame) -> pd.DataFrame:
    product = panel.drop_duplicates(["reporterCode", "hs"]).copy()
    main = product[product["is_main_clean_pressure_product"].eq(True)]
    rows = []
    for variant in ["frequency", "capacity", "absorptive"]:
        for col in [f"p_switch_{variant}", f"p_compress_{variant}", f"p_x_{variant}"]:
            if col not in main:
                continue
            rows.append(
                {
                    "variant": variant,
                    "variable": col,
                    "rows_nonmissing_main_clean": int(main[col].notna().sum()),
                    "min": float(main[col].min()),
                    "mean": float(main[col].mean()),
                    "sd": float(main[col].std(ddof=0)),
                    "max": float(main[col].max()),
                    "values_outside_0_1": int(
                        (main[col].dropna().lt(-1e-10) | main[col].dropna().gt(1 + 1e-10)).sum()
                    ),
                }
            )
    return pd.DataFrame(rows)


def validate(panel: pd.DataFrame, source: pd.DataFrame) -> None:
    errors: list[str] = []
    key = ["reporterCode", "period", "hs", "source"]
    if len(panel) != len(source):
        errors.append(f"row count changed: {len(source)} -> {len(panel)}")
    if panel.duplicated(key).any():
        errors.append("duplicate source-panel keys")
    for col in ["trade_value_usd", "did_main_clean", "did_any_policy"]:
        if col not in panel:
            errors.append(f"missing required column {col}")

    pressure_cols = [
        "p_switch_frequency",
        "p_compress_frequency",
        "p_x_frequency",
        "p_switch_capacity",
        "p_compress_capacity",
        "p_x_capacity",
        "p_switch_absorptive",
        "p_compress_absorptive",
        "p_x_absorptive",
    ]
    policy = panel["has_policy_event"].eq(True)
    for col in pressure_cols:
        values = panel.loc[policy, col].dropna()
        if values.lt(-1e-10).any() or values.gt(1 + 1e-10).any():
            errors.append(f"{col} outside [0,1]")

    ip = panel.drop_duplicates(["reporterCode", "hs"]).copy()
    policy_ip = ip["has_policy_event"].eq(True)
    absorb_gap = (
        ip.loc[policy_ip, "p_x_absorptive"] - ip.loc[policy_ip, "e_china_exposure"]
    ).abs()
    if absorb_gap.max() > 1e-8:
        errors.append("absorptive total pressure does not equal China exposure")

    control_interactions = panel["analysis_role"].eq(CONTROL_ROLE)
    interaction_cols = [col for col in panel.columns if col.startswith("did_main_clean_")]
    for col in interaction_cols:
        if panel.loc[control_interactions, col].abs().sum() > 1e-10:
            errors.append(f"control interaction not zero: {col}")
            break

    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    source, wide, pressure = load_inputs()
    pressure_for_merge = prepare_pressure_for_merge(pressure, wide)
    panel = source.merge(pressure_for_merge, on=["reporterCode", "hs"], how="left")
    panel = add_sample_flags(panel)
    panel = add_interactions(panel)

    validate(panel, source)

    panel.to_csv(ESTIMATION_PANEL_PATH, index=False)
    sample_audit = build_sample_audit(panel)
    product_audit = build_product_audit(panel)
    variant_audit = build_variant_audit(panel)
    sample_audit.to_csv(SAMPLE_AUDIT_PATH, index=False)
    product_audit.to_csv(PRODUCT_AUDIT_PATH, index=False)
    variant_audit.to_csv(VARIANT_AUDIT_PATH, index=False)

    print(f"Wrote {ESTIMATION_PANEL_PATH}")
    print(f"Wrote {SAMPLE_AUDIT_PATH}")
    print(f"Wrote {PRODUCT_AUDIT_PATH}")
    print(f"Wrote {VARIANT_AUDIT_PATH}")
    print("\nSample audit:")
    print(sample_audit.to_string(index=False))
    print("\nPressure variant audit:")
    print(variant_audit.to_string(index=False))


if __name__ == "__main__":
    main()
