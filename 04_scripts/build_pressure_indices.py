#!/usr/bin/env python3
"""
Build pre-policy importer-product pressure indexes.

All pressure variables are constructed only from months before the product's
announcement month. Candidate controls receive missing theory variables and
zero-filled interaction helpers, so later regressions do not accidentally drop
control rows when forming treatment interactions.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PARTNER_PATH = PROCESSED / "comtrade_pressure_partner_panel.csv"
METADATA_PATH = PROCESSED / "product_scope_metadata.csv"

PRESSURE_PATH = PROCESSED / "pressure_indices_importer_product.csv"
PRODUCT_SUMMARY_PATH = PROCESSED / "pressure_indices_product_summary.csv"
AUDIT_PATH = TABLES / "pressure_indices_audit.csv"


def yyyymm_from_date(value: object) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return ""
    return str(value)[:7].replace("-", "")


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    missing = [
        path
        for path in [WIDE_PATH, PARTNER_PATH, METADATA_PATH]
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(f"Missing required input(s): {missing}")

    wide = pd.read_csv(
        WIDE_PATH,
        dtype={"hs": str, "period": str},
        low_memory=False,
    )
    partner = pd.read_csv(
        PARTNER_PATH,
        dtype={"hs": str, "period": str},
        low_memory=False,
    )
    metadata = pd.read_csv(METADATA_PATH, dtype={"hs": str})
    metadata = metadata[metadata["ready_for_next_processed_panel"].eq(True)].copy()
    metadata["announcement_period"] = metadata["announcement_date"].map(yyyymm_from_date)
    return wide, partner, metadata


def outside_market_for_product(
    product_partner: pd.DataFrame,
    reporters: list[int],
) -> pd.DataFrame:
    """Compute leave-one-importer-out non-China market structure."""
    positive = product_partner[
        product_partner["source"].eq("RestOfWorld")
        & product_partner["trade_value_usd"].gt(0)
    ].copy()

    if positive.empty:
        return pd.DataFrame(
            {
                "reporterCode": reporters,
                "row_supplier_count_loo": 0,
                "row_total_value_loo": 0.0,
                "row_hhi_loo": np.nan,
            }
        )

    global_by_supplier = positive.groupby("partnerCode")["trade_value_usd"].sum()
    reporter_supplier = positive.groupby(
        ["reporterCode", "partnerCode"]
    )["trade_value_usd"].sum()

    rows = []
    for reporter in reporters:
        loo = global_by_supplier.copy()
        if reporter in reporter_supplier.index.get_level_values(0):
            own = reporter_supplier.loc[reporter]
            common = loo.index.intersection(own.index)
            loo.loc[common] = loo.loc[common] - own.loc[common]

        # The baseline measures external non-China import options. If the
        # importer is itself a supplier to other countries, that domestic
        # capacity is not counted as an import source for the importer.
        if reporter in loo.index:
            loo = loo.drop(index=reporter)

        loo = loo[loo > 0]
        total = float(loo.sum())
        if total > 0:
            shares = loo / total
            hhi = float((shares**2).sum())
            supplier_count = int(len(loo))
        else:
            hhi = np.nan
            supplier_count = 0
        rows.append(
            {
                "reporterCode": reporter,
                "row_supplier_count_loo": supplier_count,
                "row_total_value_loo": total,
                "row_hhi_loo": hhi,
            }
        )
    return pd.DataFrame(rows)


def pressure_for_product(
    hs: str,
    wide: pd.DataFrame,
    partner: pd.DataFrame,
    metadata_row: pd.Series,
    reporters: list[int],
) -> pd.DataFrame:
    announcement_period = str(metadata_row.get("announcement_period", ""))
    base = pd.DataFrame({"reporterCode": reporters})
    base["hs"] = hs
    base["product"] = metadata_row["product_name"]
    for col in [
        "policy_screened",
        "wave",
        "policy_episode",
        "announcement_date",
        "implementation_date",
        "import_effect_month",
        "treatment_status",
        "scope_status",
        "analysis_role",
        "usable_as_control",
    ]:
        base[col] = metadata_row[col]
    base["announcement_period"] = announcement_period
    base["has_policy_event"] = announcement_period != ""
    base["is_clean_treated"] = base["analysis_role"].isin(
        ["main_clean_treated", "main_clean_treated_sparse_caution"]
    )
    base["is_secondary_scope_case"] = base["analysis_role"].eq("secondary_scope_case")
    base["is_candidate_control"] = base["analysis_role"].eq(
        "candidate_control_pending_screen"
    )

    if announcement_period == "":
        for col in [
            "pre_month_count",
            "pre_china_value",
            "pre_row_value",
            "pre_world_value",
            "pre_row_positive_months",
            "e_china_exposure",
            "o_row_access",
            "row_supplier_count_loo",
            "row_total_value_loo",
            "row_hhi_loo",
            "row_diversification_loo",
            "row_depth_loo_raw",
            "a_row_strength_loo",
            "r_replacement_rigidity_loo",
            "p_switch",
            "p_compress",
            "p_x_decline",
        ]:
            base[col] = np.nan
        return base

    product_wide = wide[wide["hs"].eq(hs)].copy()
    pre_wide = product_wide[product_wide["period"].lt(announcement_period)].copy()
    pre_partner = partner[
        partner["hs"].eq(hs) & partner["period"].lt(announcement_period)
    ].copy()

    grouped = pre_wide.groupby("reporterCode", as_index=False).agg(
        pre_month_count=("period", "nunique"),
        pre_china_value=("china_primaryValue", "sum"),
        pre_row_value=("non_china_primaryValue", "sum"),
        pre_row_positive_months=(
            "non_china_primaryValue",
            lambda values: int((values > 0).sum()),
        ),
    )
    out = base.merge(grouped, on="reporterCode", how="left")
    for col in [
        "pre_month_count",
        "pre_china_value",
        "pre_row_value",
        "pre_row_positive_months",
    ]:
        out[col] = out[col].fillna(0)

    out["pre_world_value"] = out["pre_china_value"] + out["pre_row_value"]
    out["e_china_exposure"] = np.where(
        out["pre_world_value"] > 0,
        out["pre_china_value"] / out["pre_world_value"],
        0.0,
    )
    out["o_row_access"] = np.where(
        out["pre_month_count"] > 0,
        out["pre_row_positive_months"] / out["pre_month_count"],
        0.0,
    )

    outside = outside_market_for_product(pre_partner, reporters)
    out = out.merge(outside, on="reporterCode", how="left")
    out["row_supplier_count_loo"] = out["row_supplier_count_loo"].fillna(0)
    out["row_total_value_loo"] = out["row_total_value_loo"].fillna(0.0)
    out["row_diversification_loo"] = (1 - out["row_hhi_loo"]).fillna(0.0)
    out["row_depth_loo_raw"] = out["row_supplier_count_loo"]
    return out


def add_depth_and_pressure(rows: pd.DataFrame) -> pd.DataFrame:
    rows = rows.copy()
    policy_rows = rows["has_policy_event"].eq(True)
    max_n = rows.loc[policy_rows, "row_supplier_count_loo"].max()
    if pd.isna(max_n) or max_n <= 0:
        max_n = 0
    rows["row_supplier_count_loo_max_denominator"] = int(max_n)
    rows["row_depth_loo"] = np.where(
        policy_rows & (max_n > 0),
        np.log1p(rows["row_supplier_count_loo"]) / np.log1p(max_n),
        np.nan,
    )
    rows["a_row_strength_loo"] = np.where(
        policy_rows,
        rows["row_depth_loo"].fillna(0) * rows["row_diversification_loo"].fillna(0),
        np.nan,
    )
    rows["r_replacement_rigidity_loo"] = np.where(
        policy_rows,
        1 - rows["a_row_strength_loo"],
        np.nan,
    )
    rows["p_switch"] = np.where(
        policy_rows,
        rows["e_china_exposure"]
        * rows["o_row_access"]
        * rows["a_row_strength_loo"],
        np.nan,
    )
    rows["p_compress"] = np.where(
        policy_rows,
        rows["e_china_exposure"]
        * (1 - rows["o_row_access"])
        * rows["r_replacement_rigidity_loo"],
        np.nan,
    )
    rows["p_x_decline"] = rows["p_switch"] + rows["p_compress"]
    return rows


def zscore(series: pd.Series) -> tuple[pd.Series, float, float]:
    mean = float(series.mean())
    sd = float(series.std(ddof=0))
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.nan, index=series.index), mean, sd
    return (series - mean) / sd, mean, sd


def add_standardized_columns(rows: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = rows.copy()
    audit_rows = []
    samples = {
        "policy_event": rows["has_policy_event"].eq(True),
        "main_clean": rows["is_clean_treated"].eq(True),
    }
    for sample_name, mask in samples.items():
        for variable in ["p_switch", "p_compress", "p_x_decline"]:
            z_col = f"{variable}_z_{sample_name}"
            model_col = f"{z_col}_for_interaction"
            z, mean, sd = zscore(rows.loc[mask, variable])
            rows[z_col] = np.nan
            rows.loc[mask, z_col] = z
            rows[model_col] = rows[z_col].fillna(0.0)
            audit_rows.append(
                {
                    "standardization_sample": sample_name,
                    "variable": variable,
                    "n": int(mask.sum()),
                    "mean": mean,
                    "sd_ddof0": sd,
                }
            )
    return rows, pd.DataFrame(audit_rows)


def product_summary(rows: pd.DataFrame) -> pd.DataFrame:
    summaries = []
    policy = rows[rows["has_policy_event"].eq(True)].copy()
    for hs, group in policy.groupby("hs", sort=False):
        weight_den = group["pre_world_value"].sum()
        if weight_den > 0:
            weights = group["pre_world_value"] / weight_den
        else:
            weights = pd.Series(1 / len(group), index=group.index)
        summaries.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "scope_status": group["scope_status"].iloc[0],
                "wave": group["wave"].iloc[0],
                "announcement_date": group["announcement_date"].iloc[0],
                "implementation_date": group["implementation_date"].iloc[0],
                "import_effect_month": group["import_effect_month"].iloc[0],
                "importers": group["reporterCode"].nunique(),
                "pre_month_count_min": group["pre_month_count"].min(),
                "pre_month_count_max": group["pre_month_count"].max(),
                "pre_world_value_sum": weight_den,
                "mean_e_china_exposure": group["e_china_exposure"].mean(),
                "weighted_e_china_exposure": float((weights * group["e_china_exposure"]).sum()),
                "mean_o_row_access": group["o_row_access"].mean(),
                "weighted_o_row_access": float((weights * group["o_row_access"]).sum()),
                "mean_a_row_strength_loo": group["a_row_strength_loo"].mean(),
                "weighted_a_row_strength_loo": float((weights * group["a_row_strength_loo"]).sum()),
                "mean_r_replacement_rigidity_loo": group["r_replacement_rigidity_loo"].mean(),
                "weighted_r_replacement_rigidity_loo": float((weights * group["r_replacement_rigidity_loo"]).sum()),
                "mean_p_switch": group["p_switch"].mean(),
                "weighted_p_switch": float((weights * group["p_switch"]).sum()),
                "mean_p_compress": group["p_compress"].mean(),
                "weighted_p_compress": float((weights * group["p_compress"]).sum()),
                "mean_p_x_decline": group["p_x_decline"].mean(),
                "weighted_p_x_decline": float((weights * group["p_x_decline"]).sum()),
            }
        )
    return pd.DataFrame(summaries)


def validate_pressure(rows: pd.DataFrame, wide: pd.DataFrame, partner: pd.DataFrame) -> None:
    errors = []
    expected_rows = wide["hs"].nunique() * wide["reporterCode"].nunique()
    if len(rows) != expected_rows:
        errors.append(f"expected {expected_rows} pressure rows, found {len(rows)}")
    if rows.duplicated(["hs", "reporterCode"]).any():
        errors.append("duplicate hs-reporter pressure rows")

    policy = rows[rows["has_policy_event"].eq(True)].copy()
    bounded = [
        "e_china_exposure",
        "o_row_access",
        "row_diversification_loo",
        "row_depth_loo",
        "a_row_strength_loo",
        "r_replacement_rigidity_loo",
        "p_switch",
        "p_compress",
        "p_x_decline",
    ]
    for col in bounded:
        values = policy[col].dropna()
        if values.lt(-1e-10).any() or values.gt(1 + 1e-10).any():
            errors.append(f"{col} outside [0,1]")

    if (policy["p_x_decline"] - policy["p_switch"] - policy["p_compress"]).abs().max() > 1e-12:
        errors.append("p_x_decline is not p_switch + p_compress")
    if (policy["r_replacement_rigidity_loo"] - (1 - policy["a_row_strength_loo"])).abs().max() > 1e-12:
        errors.append("replacement rigidity is not 1 - outside strength")
    if policy.loc[policy["o_row_access"].eq(1), "p_compress"].abs().max() > 1e-12:
        errors.append("compression pressure positive when O_ip equals 1")
    if policy.loc[policy["o_row_access"].eq(0), "p_switch"].abs().max() > 1e-12:
        errors.append("switching pressure positive when O_ip equals 0")

    controls = rows[rows["is_candidate_control"].eq(True)]
    if controls[["p_switch", "p_compress", "p_x_decline"]].notna().any().any():
        errors.append("candidate controls have non-missing theory pressure variables")

    # Independent prototype check: HS 8110, United States reporter 842.
    proto = rows[(rows["hs"].eq("8110")) & (rows["reporterCode"].eq(842))]
    if not proto.empty:
        proto = proto.iloc[0]
        ann = "202408"
        pre_wide = wide[
            wide["hs"].eq("8110")
            & wide["reporterCode"].eq(842)
            & wide["period"].lt(ann)
        ]
        e = pre_wide["china_primaryValue"].sum() / (
            pre_wide["china_primaryValue"].sum()
            + pre_wide["non_china_primaryValue"].sum()
        )
        o = pre_wide["non_china_primaryValue"].gt(0).sum() / len(pre_wide)
        if abs(e - proto["e_china_exposure"]) > 1e-12:
            errors.append("prototype E_ip mismatch")
        if abs(o - proto["o_row_access"]) > 1e-12:
            errors.append("prototype O_ip mismatch")

        pre_partner = partner[
            partner["hs"].eq("8110")
            & partner["period"].lt(ann)
            & partner["source"].eq("RestOfWorld")
            & partner["trade_value_usd"].gt(0)
        ]
        others = pre_partner[
            pre_partner["reporterCode"].ne(842)
            & pre_partner["partnerCode"].ne(842)
        ]
        by_supplier = others.groupby("partnerCode")["trade_value_usd"].sum()
        by_supplier = by_supplier[by_supplier > 0]
        if int(len(by_supplier)) != int(proto["row_supplier_count_loo"]):
            errors.append("prototype supplier count mismatch")
        hhi = float(((by_supplier / by_supplier.sum()) ** 2).sum())
        if abs(hhi - proto["row_hhi_loo"]) > 1e-12:
            errors.append("prototype HHI mismatch")

    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    wide, partner, metadata = load_inputs()
    reporters = sorted(wide["reporterCode"].unique())

    frames = []
    for hs in sorted(wide["hs"].unique()):
        row = metadata.loc[metadata["hs"].eq(hs)].iloc[0]
        frames.append(pressure_for_product(hs, wide, partner, row, reporters))
    pressure = pd.concat(frames, ignore_index=True).sort_values(
        ["hs", "reporterCode"]
    )
    pressure = add_depth_and_pressure(pressure)
    pressure, z_audit = add_standardized_columns(pressure)
    product = product_summary(pressure)

    validate_pressure(pressure, wide, partner)

    audit = pd.concat(
        [
            z_audit,
            pd.DataFrame(
                [
                    {
                        "standardization_sample": "construction",
                        "variable": "policy_importer_product_rows",
                        "n": int(pressure["has_policy_event"].sum()),
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                    },
                    {
                        "standardization_sample": "construction",
                        "variable": "candidate_controls",
                        "n": int(pressure["is_candidate_control"].sum()),
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                    },
                    {
                        "standardization_sample": "construction",
                        "variable": "row_supplier_count_loo_max_denominator",
                        "n": int(pressure["row_supplier_count_loo_max_denominator"].max()),
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                    },
                    {
                        "standardization_sample": "construction_rule",
                        "variable": "pre_period",
                        "n": 0,
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                        "note": "Uses months strictly before the announcement month.",
                    },
                    {
                        "standardization_sample": "construction_rule",
                        "variable": "outside_market_leave_one_out",
                        "n": 0,
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                        "note": "Excludes importer i as reporter and as partner supplier; uses positive non-China bilateral import values.",
                    },
                    {
                        "standardization_sample": "construction_rule",
                        "variable": "depth_normalization",
                        "n": 0,
                        "mean": np.nan,
                        "sd_ddof0": np.nan,
                        "note": "Depth is log(1+N_loo)/log(1+max N_loo across policy-event importer-product rows).",
                    },
                ]
            ),
        ],
        ignore_index=True,
    )

    pressure.to_csv(PRESSURE_PATH, index=False)
    product.to_csv(PRODUCT_SUMMARY_PATH, index=False)
    audit.to_csv(AUDIT_PATH, index=False)

    print(f"Pressure rows: {len(pressure):,} -> {PRESSURE_PATH}")
    print(f"Product summary: {len(product):,} -> {PRODUCT_SUMMARY_PATH}")
    print(f"Audit: {AUDIT_PATH}")
    print("\nPolicy-product summary:")
    print(
        product[
            [
                "hs",
                "product",
                "analysis_role",
                "weighted_p_switch",
                "weighted_p_compress",
                "weighted_p_x_decline",
            ]
        ].to_string(index=False)
    )
    print("\nStandardization audit:")
    print(audit.to_string(index=False))


if __name__ == "__main__":
    main()
