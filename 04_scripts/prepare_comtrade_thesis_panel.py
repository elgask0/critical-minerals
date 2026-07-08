"""
Build the analysis-ready Comtrade panel for the term-paper/thesis
specifications.

The raw API responses contain a World partner row, bilateral partner rows, and
additional customs/mode breakdowns. Summing every raw row double-counts both
partners and reporting dimensions. This script uses the canonical aggregate
record (customs C00, mode of transport 0, means of transport 0), then separates
World, China, and rest-of-world flows without modifying raw data.
"""

from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "03_data" / "raw"
PROCESSED = REPO / "03_data" / "processed"
OUTPUT = REPO / "03_data" / "output" / "tables"

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
PRODUCTS = {
    "2504": "Natural graphite",
    "811292": "Ga/Ge/In/V/Nb bundle",
    "282560": "GeO2/ZrO2",
    "8110": "Antimony metal",
    "261710": "Antimony ores/concentrates",
    "282580": "Antimony oxides",
    "2818": "Alumina placebo",
    "8111": "Manganese placebo",
    "2811": "Inorganic acids placebo",
    "3801": "Artificial/colloidal graphite",
}
MEASURES = ["primaryValue", "netWgt", "qty"]


def canonical_rows(path):
    columns = [
        "reporterCode",
        "reporterISO",
        "period",
        "partnerCode",
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
    raw = pd.read_csv(path, usecols=lambda col: col in columns, low_memory=False)
    raw["period"] = raw["period"].astype(str)
    for col in ["reporterCode", "partnerCode", "partner2Code", "motCode", "mosCode"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in MEASURES:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")

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
        raise ValueError(f"Duplicate canonical partner records in {path.name}: {sample}")
    return aggregate


def supplier_statistics(rows):
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
    return totals.merge(non_china_totals[keep], on=keys, how="left")


def build_product_panel(hs, label):
    path = RAW / f"comtrade_{hs}_imports.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    rows = canonical_rows(path)
    grid = pd.MultiIndex.from_product(
        [REPORTERS, PERIODS], names=["reporterCode", "period"]
    ).to_frame(index=False)

    world = rows[rows["partnerCode"].eq(0)].copy()
    china = rows[rows["partnerCode"].eq(156)].copy()
    keys = ["reporterCode", "period"]

    world_columns = {measure: f"world_{measure}" for measure in MEASURES}
    china_columns = {measure: f"china_{measure}" for measure in MEASURES}
    world = world[keys + MEASURES].rename(columns=world_columns)
    china = china[keys + MEASURES].rename(columns=china_columns)

    panel = grid.merge(world, on=keys, how="left").merge(china, on=keys, how="left")
    panel = panel.merge(supplier_statistics(rows), on=keys, how="left")
    panel["hs"] = hs
    panel["product"] = label

    for measure in MEASURES:
        world_col = f"world_{measure}"
        china_col = f"china_{measure}"
        non_china_col = f"non_china_{measure}"
        panel[f"{world_col}_reported"] = panel[world_col].notna()
        panel[f"{china_col}_reported"] = panel[china_col].notna()
        panel[world_col] = panel[world_col].fillna(0)
        panel[china_col] = panel[china_col].fillna(0)
        panel[non_china_col] = panel[world_col] - panel[china_col]

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

    panel["bilateral_world_gap"] = (
        panel["bilateral_value"] - panel["world_primaryValue"]
    )
    panel["bilateral_non_china_gap"] = (
        panel["bilateral_non_china_value"] - panel["non_china_primaryValue"]
    )
    return panel


def coverage_table(panel):
    rows = []
    for hs, group in panel.groupby("hs", sort=False):
        rows.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "rows": len(group),
                "reporters": group["reporterCode"].nunique(),
                "months": group["period"].nunique(),
                "positive_china_value_share": (group["china_primaryValue"] > 0).mean(),
                "world_net_weight_coverage": (
                    group["world_netWgt"].notna() & group["world_netWgt"].gt(0)
                ).mean(),
                "china_net_weight_coverage": (
                    group["china_netWgt"].notna() & group["china_netWgt"].gt(0)
                ).mean(),
                "median_abs_world_bilateral_gap": group[
                    "bilateral_world_gap"
                ].abs().median(),
                "max_abs_world_bilateral_gap": group[
                    "bilateral_world_gap"
                ].abs().max(),
            }
        )
    return pd.DataFrame(rows)


def to_source_long(panel):
    common = [
        "reporterCode",
        "period",
        "hs",
        "product",
        "supplier_count",
        "supplier_hhi",
        "non_china_supplier_count",
        "non_china_supplier_hhi",
    ]
    frames = []
    for source, prefix in [("China", "china"), ("RestOfWorld", "non_china")]:
        frame = panel[common].copy()
        frame["source"] = source
        frame["trade_value_usd"] = panel[f"{prefix}_primaryValue"]
        usable = panel[f"{prefix}_net_weight_usable"]
        frame["net_weight_kg"] = panel[f"{prefix}_netWgt"].where(usable)
        frame["net_weight_usable"] = usable
        frame["quantity"] = panel[f"{prefix}_qty"]
        frames.append(frame)
    return pd.concat(frames, ignore_index=True).sort_values(
        ["hs", "reporterCode", "period", "source"]
    )


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    panels = [
        build_product_panel(hs, label)
        for hs, label in PRODUCTS.items()
    ]
    panel = pd.concat(panels, ignore_index=True).sort_values(
        ["hs", "reporterCode", "period"]
    )
    source_long = to_source_long(panel)
    audit = coverage_table(panel)

    panel_path = PROCESSED / "comtrade_thesis_country_product_month.csv"
    source_path = PROCESSED / "comtrade_thesis_source_panel.csv"
    audit_path = OUTPUT / "comtrade_thesis_data_audit.csv"
    panel.to_csv(panel_path, index=False)
    source_long.to_csv(source_path, index=False)
    audit.to_csv(audit_path, index=False)

    print(f"Wide panel: {len(panel):,} rows -> {panel_path}")
    print(f"Source panel: {len(source_long):,} rows -> {source_path}")
    print(f"Audit: {audit_path}")
    print(audit.to_string(index=False))


if __name__ == "__main__":
    main()
