#!/usr/bin/env python3
"""
Build the expanded Comtrade panel for the pressure-index thesis design.

Inputs are raw Comtrade CSVs and the frozen product-scope metadata table. The
script reads only canonical aggregate import records and writes new processed
outputs. It does not modify raw data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "03_data" / "raw"
PROCESSED = REPO / "03_data" / "processed"
OUTPUT = REPO / "03_data" / "output" / "tables"
METADATA_PATH = PROCESSED / "product_scope_metadata.csv"

PERIODS = [
    f"{year}{month:02d}"
    for year in range(2019, 2026)
    for month in range(1, 13)
] + [f"2026{month:02d}" for month in range(1, 4)]

REPORTERS = [
    276, 392, 344, 410, 826, 842, 56, 124, 724, 818, 251, 764, 752,
    757, 76, 380, 792, 100, 203, 376, 398, 528, 804, 191, 702, 428,
    36, 616, 31, 554, 704, 440, 348, 642, 579, 372, 32, 484, 620,
    604, 508, 703, 84, 682, 705, 404, 360, 699, 710, 834, 860, 854,
    788,
]

MEASURES = ["primaryValue", "netWgt", "qty"]
RAW_COLUMNS = [
    "reporterCode",
    "reporterISO",
    "reporterDesc",
    "period",
    "partnerCode",
    "partnerISO",
    "partnerDesc",
    "partner2Code",
    "customsCode",
    "motCode",
    "mosCode",
    "primaryValue",
    "netWgt",
    "qty",
    "isNetWgtEstimated",
    "isQtyEstimated",
]

METADATA_COLUMNS = [
    "hs",
    "product_name",
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
    "price_pair_status",
]


def load_metadata() -> pd.DataFrame:
    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {METADATA_PATH}. Run build_product_scope_metadata.py first."
        )
    metadata = pd.read_csv(METADATA_PATH, dtype={"hs": str})
    metadata = metadata[metadata["ready_for_next_processed_panel"].eq(True)].copy()
    metadata = metadata.sort_values(["analysis_role", "hs"], kind="stable")
    if metadata.empty:
        raise ValueError("No products marked ready_for_next_processed_panel.")
    missing = [
        hs
        for hs in metadata["hs"]
        if not (RAW / f"comtrade_{hs}_imports.csv").exists()
    ]
    if missing:
        raise FileNotFoundError(f"Missing merged raw Comtrade files: {missing}")
    return metadata[METADATA_COLUMNS].copy()


def canonical_rows(hs: str) -> pd.DataFrame:
    path = RAW / f"comtrade_{hs}_imports.csv"
    raw = pd.read_csv(path, usecols=lambda col: col in RAW_COLUMNS, low_memory=False)

    for col in ["reporterCode", "partnerCode", "partner2Code", "motCode", "mosCode"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in MEASURES:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    raw["period"] = (
        pd.to_numeric(raw["period"], errors="coerce")
        .astype("Int64")
        .astype(str)
        .str.zfill(6)
    )

    aggregate = raw[
        raw["reporterCode"].isin(REPORTERS)
        & raw["period"].isin(PERIODS)
        & raw["partner2Code"].eq(0)
        & raw["customsCode"].eq("C00")
        & raw["motCode"].eq(0)
        & raw["mosCode"].eq(0)
    ].copy()

    key = ["reporterCode", "period", "partnerCode"]
    duplicates = aggregate.duplicated(key, keep=False)
    if duplicates.any():
        sample = aggregate.loc[duplicates, key].head().to_dict("records")
        raise ValueError(f"Duplicate canonical partner records in HS {hs}: {sample}")

    aggregate["hs"] = hs
    return aggregate


def product_metadata_row(metadata: pd.DataFrame, hs: str) -> dict[str, object]:
    row = metadata.loc[metadata["hs"].eq(hs)].iloc[0].to_dict()
    row["product"] = row.pop("product_name")
    return row


def supplier_statistics(rows: pd.DataFrame) -> pd.DataFrame:
    bilateral = rows[rows["partnerCode"].ne(0)].copy()
    bilateral["value"] = bilateral["primaryValue"].fillna(0).clip(lower=0)
    bilateral["value_sq"] = bilateral["value"] ** 2
    keys = ["reporterCode", "period"]

    totals = bilateral.groupby(keys, as_index=False).agg(
        bilateral_value=("value", "sum"),
        supplier_count=("value", lambda values: int((values > 0).sum())),
        supplier_value_sq=("value_sq", "sum"),
    )
    totals["supplier_hhi"] = np.where(
        totals["bilateral_value"] > 0,
        totals["supplier_value_sq"] / totals["bilateral_value"] ** 2,
        np.nan,
    )

    non_china = bilateral[bilateral["partnerCode"].ne(156)]
    non_china_totals = non_china.groupby(keys, as_index=False).agg(
        bilateral_non_china_value=("value", "sum"),
        non_china_supplier_count=("value", lambda values: int((values > 0).sum())),
        non_china_value_sq=("value_sq", "sum"),
    )
    non_china_totals["non_china_supplier_hhi"] = np.where(
        non_china_totals["bilateral_non_china_value"] > 0,
        non_china_totals["non_china_value_sq"]
        / non_china_totals["bilateral_non_china_value"] ** 2,
        np.nan,
    )

    keep = [
        "reporterCode",
        "period",
        "bilateral_non_china_value",
        "non_china_supplier_count",
        "non_china_supplier_hhi",
    ]
    out = totals.merge(non_china_totals[keep], on=keys, how="left")
    for col in ["bilateral_value", "supplier_count", "bilateral_non_china_value", "non_china_supplier_count"]:
        out[col] = out[col].fillna(0)
    return out


def build_country_product_panel(
    hs: str, rows: pd.DataFrame, metadata: pd.DataFrame
) -> pd.DataFrame:
    grid = pd.MultiIndex.from_product(
        [REPORTERS, PERIODS], names=["reporterCode", "period"]
    ).to_frame(index=False)
    keys = ["reporterCode", "period"]

    world = rows[rows["partnerCode"].eq(0)].copy()
    china = rows[rows["partnerCode"].eq(156)].copy()

    world = world[keys + MEASURES].rename(
        columns={measure: f"world_{measure}" for measure in MEASURES}
    )
    china = china[keys + MEASURES].rename(
        columns={measure: f"china_{measure}" for measure in MEASURES}
    )

    panel = grid.merge(world, on=keys, how="left").merge(china, on=keys, how="left")
    panel = panel.merge(supplier_statistics(rows), on=keys, how="left")

    for key, value in product_metadata_row(metadata, hs).items():
        panel[key] = value

    for measure in MEASURES:
        world_col = f"world_{measure}"
        china_col = f"china_{measure}"
        non_china_col = f"non_china_{measure}"
        panel[f"{world_col}_reported"] = panel[world_col].notna()
        panel[f"{china_col}_reported"] = panel[china_col].notna()
        panel[world_col] = panel[world_col].fillna(0)
        panel[china_col] = panel[china_col].fillna(0)
        panel[non_china_col] = panel[world_col] - panel[china_col]

    for col in ["bilateral_value", "supplier_count", "bilateral_non_china_value", "non_china_supplier_count"]:
        panel[col] = panel[col].fillna(0)

    tolerance = np.maximum(1.0, panel["world_primaryValue"].abs() * 1e-8)
    invalid = panel["non_china_primaryValue"] < -tolerance
    if invalid.any():
        sample = panel.loc[
            invalid,
            ["reporterCode", "period", "world_primaryValue", "china_primaryValue"],
        ].head()
        raise ValueError(f"China value exceeds World for HS {hs}:\n{sample}")
    panel["non_china_primaryValue"] = panel["non_china_primaryValue"].clip(lower=0)

    panel["china_share_value"] = np.where(
        panel["world_primaryValue"] > 0,
        panel["china_primaryValue"] / panel["world_primaryValue"],
        0,
    )
    panel["unit_value_world_usd_kg"] = np.where(
        panel["world_netWgt"] > 0,
        panel["world_primaryValue"] / panel["world_netWgt"],
        np.nan,
    )
    panel["unit_value_china_usd_kg"] = np.where(
        panel["china_netWgt"] > 0,
        panel["china_primaryValue"] / panel["china_netWgt"],
        np.nan,
    )
    panel["world_net_weight_usable"] = (
        panel["world_netWgt_reported"] | panel["world_primaryValue"].eq(0)
    )
    panel["china_net_weight_usable"] = (
        panel["china_netWgt_reported"] | panel["china_primaryValue"].eq(0)
    )
    panel["non_china_net_weight_usable"] = (
        panel["world_net_weight_usable"] & panel["china_net_weight_usable"]
    )

    panel["bilateral_world_gap"] = panel["bilateral_value"] - panel["world_primaryValue"]
    panel["bilateral_non_china_gap"] = (
        panel["bilateral_non_china_value"] - panel["non_china_primaryValue"]
    )
    panel["post_import_effect"] = (
        panel["import_effect_month"].notna()
        & panel["import_effect_month"].astype(str).ne("")
        & panel["period"].ge(panel["import_effect_month"].astype(str).str.replace("-", ""))
    )
    panel["is_clean_treated"] = panel["analysis_role"].isin(
        ["main_clean_treated", "main_clean_treated_sparse_caution"]
    )
    panel["is_secondary_scope_case"] = panel["analysis_role"].eq("secondary_scope_case")
    panel["is_candidate_control"] = panel["analysis_role"].eq(
        "candidate_control_pending_screen"
    )
    return panel


def build_partner_panel(
    hs: str, rows: pd.DataFrame, metadata: pd.DataFrame
) -> pd.DataFrame:
    partner = rows[rows["partnerCode"].ne(0)].copy()
    keep = [
        "reporterCode",
        "period",
        "partnerCode",
        "primaryValue",
        "netWgt",
        "qty",
        "isNetWgtEstimated",
        "isQtyEstimated",
    ]
    partner = partner[keep].copy()
    for key, value in product_metadata_row(metadata, hs).items():
        partner[key] = value
    partner["partner_is_china"] = partner["partnerCode"].eq(156)
    partner["source"] = np.where(partner["partner_is_china"], "China", "RestOfWorld")
    partner["trade_value_usd"] = partner["primaryValue"].fillna(0).clip(lower=0)
    partner["net_weight_kg"] = partner["netWgt"]
    partner["quantity"] = partner["qty"]
    partner["positive_trade_value"] = partner["trade_value_usd"].gt(0)
    return partner[
        [
            "reporterCode",
            "period",
            "hs",
            "product",
            "partnerCode",
            "source",
            "partner_is_china",
            "trade_value_usd",
            "net_weight_kg",
            "quantity",
            "isNetWgtEstimated",
            "isQtyEstimated",
            "positive_trade_value",
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
        ]
    ]


def to_source_long(panel: pd.DataFrame) -> pd.DataFrame:
    common = [
        "reporterCode",
        "period",
        "hs",
        "product",
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
        "post_import_effect",
        "is_clean_treated",
        "is_secondary_scope_case",
        "is_candidate_control",
        "supplier_count",
        "supplier_hhi",
        "non_china_supplier_count",
        "non_china_supplier_hhi",
    ]
    frames = []
    for source, prefix in [("China", "china"), ("RestOfWorld", "non_china")]:
        frame = panel[common].copy()
        frame["source"] = source
        frame["china_source"] = source == "China"
        frame["trade_value_usd"] = panel[f"{prefix}_primaryValue"]
        usable = panel[f"{prefix}_net_weight_usable"]
        frame["net_weight_kg"] = panel[f"{prefix}_netWgt"].where(usable)
        frame["net_weight_usable"] = usable
        frame["quantity"] = panel[f"{prefix}_qty"]
        frame["treatment_cell"] = (
            frame["is_clean_treated"] & frame["china_source"] & frame["post_import_effect"]
        )
        frame["scope_treatment_cell"] = (
            frame["is_secondary_scope_case"]
            & frame["china_source"]
            & frame["post_import_effect"]
        )
        frames.append(frame)
    return pd.concat(frames, ignore_index=True).sort_values(
        ["hs", "reporterCode", "period", "source"]
    )


def coverage_table(panel: pd.DataFrame, partner_panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for hs, group in panel.groupby("hs", sort=False):
        partners = partner_panel[partner_panel["hs"].eq(hs)]
        rows.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "treatment_status": group["treatment_status"].iloc[0],
                "scope_status": group["scope_status"].iloc[0],
                "rows": len(group),
                "reporters": group["reporterCode"].nunique(),
                "months": group["period"].nunique(),
                "positive_world_value_share": group["world_primaryValue"].gt(0).mean(),
                "positive_china_value_share": group["china_primaryValue"].gt(0).mean(),
                "positive_non_china_value_share": group["non_china_primaryValue"].gt(0).mean(),
                "world_net_weight_coverage": group["world_netWgt_reported"].mean(),
                "china_net_weight_coverage": group["china_netWgt_reported"].mean(),
                "median_abs_world_bilateral_gap": group["bilateral_world_gap"].abs().median(),
                "max_abs_world_bilateral_gap": group["bilateral_world_gap"].abs().max(),
                "median_abs_non_china_bilateral_gap": group[
                    "bilateral_non_china_gap"
                ].abs().median(),
                "max_abs_non_china_bilateral_gap": group[
                    "bilateral_non_china_gap"
                ].abs().max(),
                "distinct_positive_non_china_partners": partners.loc[
                    partners["source"].eq("RestOfWorld")
                    & partners["positive_trade_value"],
                    "partnerCode",
                ].nunique(),
            }
        )
    return pd.DataFrame(rows)


def validate_outputs(
    panel: pd.DataFrame, source_panel: pd.DataFrame, partner_panel: pd.DataFrame
) -> None:
    expected_rows = len(REPORTERS) * len(PERIODS) * panel["hs"].nunique()
    if len(panel) != expected_rows:
        raise ValueError(f"Expected {expected_rows} wide rows, found {len(panel)}.")
    if source_panel["trade_value_usd"].lt(-1e-8).any():
        raise ValueError("Negative source-panel trade values detected.")
    if partner_panel["trade_value_usd"].lt(-1e-8).any():
        raise ValueError("Negative partner-panel trade values detected.")
    if panel["reporterCode"].nunique() != len(REPORTERS):
        raise ValueError("Reporter count mismatch.")
    if panel["period"].nunique() != len(PERIODS):
        raise ValueError("Period count mismatch.")
    bad_controls = panel.loc[
        panel["is_candidate_control"]
        & panel["treatment_status"].astype(str).str.contains("treated", na=False),
        "hs",
    ].unique()
    if len(bad_controls):
        raise ValueError(f"Treated products marked as candidate controls: {bad_controls}")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    metadata = load_metadata()

    panels = []
    partner_panels = []
    for hs in metadata["hs"]:
        rows = canonical_rows(hs)
        panels.append(build_country_product_panel(hs, rows, metadata))
        partner_panels.append(build_partner_panel(hs, rows, metadata))

    panel = pd.concat(panels, ignore_index=True).sort_values(
        ["hs", "reporterCode", "period"]
    )
    partner_panel = pd.concat(partner_panels, ignore_index=True).sort_values(
        ["hs", "reporterCode", "period", "partnerCode"]
    )
    source_panel = to_source_long(panel)
    audit = coverage_table(panel, partner_panel)

    validate_outputs(panel, source_panel, partner_panel)

    panel_path = PROCESSED / "comtrade_pressure_country_product_month.csv"
    source_path = PROCESSED / "comtrade_pressure_source_panel.csv"
    partner_path = PROCESSED / "comtrade_pressure_partner_panel.csv"
    audit_path = OUTPUT / "comtrade_pressure_data_audit.csv"

    panel.to_csv(panel_path, index=False)
    source_panel.to_csv(source_path, index=False)
    partner_panel.to_csv(partner_path, index=False)
    audit.to_csv(audit_path, index=False)

    print(f"Wide panel: {len(panel):,} rows -> {panel_path}")
    print(f"Source panel: {len(source_panel):,} rows -> {source_path}")
    print(f"Partner panel: {len(partner_panel):,} rows -> {partner_path}")
    print(f"Audit: {audit_path}")
    print(audit.to_string(index=False))


if __name__ == "__main__":
    main()
