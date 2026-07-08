"""
Normalize the downloaded Eurostat CN8 files into analysis-ready EU27 panels.

Raw API files are preserved. This script:
  - keeps only the 27 current EU member states;
  - excludes UK and API-provided aggregate rows;
  - balances all country-product-partner-month cells for 2019-2024;
  - records whether Eurostat returned each cell before filling omissions with 0;
  - validates that China imports never exceed world imports; and
  - writes country and EU27 aggregate panels.
"""

from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "03_data" / "raw" / "eurostat_cn8"
INTERIM = REPO / "03_data" / "interim"
PROCESSED = REPO / "03_data" / "processed"

EU27 = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE",
]

PRODUCTS = {
    "81129289": "Ga",
    "81129295": "Ge",
    "81129281": "In",
    "81129291": "V",
}

PARTNERS = ["CN", "WORLD"]
PERIODS = pd.period_range("2019-01", "2024-12", freq="M").astype(str).tolist()


def load_country_rows():
    frames = []
    audit_rows = []

    for code, product in PRODUCTS.items():
        for partner in PARTNERS:
            path = RAW / f"eurostat_{code}_{partner}_imports.csv"
            if not path.exists():
                raise FileNotFoundError(path)

            raw = pd.read_csv(path, keep_default_na=False)
            required = {"reporter", "partner", "product", "period", "value_eur"}
            missing = required - set(raw.columns)
            if missing:
                raise ValueError(f"{path.name} lacks columns: {sorted(missing)}")

            country = raw[raw["reporter"].isin(EU27)].copy()
            if country.duplicated(["reporter", "period"]).any():
                raise ValueError(f"Duplicate country-period rows in {path.name}")
            if set(country["partner"]) - {partner}:
                raise ValueError(f"Unexpected partner values in {path.name}")
            if set(country["period"]) - set(PERIODS):
                raise ValueError(f"Out-of-range periods in {path.name}")

            country["cn8_code"] = code
            country["product"] = product
            country["partner"] = partner
            country["value_eur"] = pd.to_numeric(
                country["value_eur"], errors="raise"
            )
            frames.append(
                country[
                    ["reporter", "cn8_code", "product", "partner", "period", "value_eur"]
                ]
            )

            audit_rows.append(
                {
                    "file": path.name,
                    "raw_rows": len(raw),
                    "eu27_country_rows": len(country),
                    "eu27_reporters_with_records": country["reporter"].nunique(),
                    "months_with_records": country["period"].nunique(),
                    "excluded_uk_rows": int((raw["reporter"] == "UK").sum()),
                    "excluded_eu27_aggregate_rows": int(
                        (raw["reporter"] == "EU27").sum()
                    ),
                    "excluded_blank_aggregate_rows": int(
                        (raw["reporter"] == "").sum()
                    ),
                }
            )

    return pd.concat(frames, ignore_index=True), pd.DataFrame(audit_rows)


def build_balanced_panel(country_rows):
    grid = pd.MultiIndex.from_product(
        [EU27, PRODUCTS.keys(), PARTNERS, PERIODS],
        names=["reporter", "cn8_code", "partner", "period"],
    ).to_frame(index=False)
    grid["product"] = grid["cn8_code"].map(PRODUCTS)

    observed = country_rows.copy()
    observed["api_record_reported"] = True
    balanced = grid.merge(
        observed[
            [
                "reporter", "cn8_code", "partner", "period",
                "value_eur", "api_record_reported",
            ]
        ],
        on=["reporter", "cn8_code", "partner", "period"],
        how="left",
        validate="one_to_one",
    )
    balanced["api_record_reported"] = balanced["api_record_reported"].eq(True)
    balanced["zero_filled"] = ~balanced["api_record_reported"]
    balanced["value_eur"] = balanced["value_eur"].fillna(0).astype("int64")
    balanced["year"] = balanced["period"].str[:4].astype(int)
    balanced["month"] = balanced["period"].str[5:].astype(int)

    expected = len(EU27) * len(PRODUCTS) * len(PARTNERS) * len(PERIODS)
    if len(balanced) != expected:
        raise ValueError(f"Balanced panel has {len(balanced)} rows, expected {expected}")

    return balanced.sort_values(
        ["product", "partner", "reporter", "period"]
    ).reset_index(drop=True)


def build_wide_country_panel(balanced):
    values = balanced.pivot(
        index=["reporter", "cn8_code", "product", "period", "year", "month"],
        columns="partner",
        values="value_eur",
    ).reset_index()
    reported = balanced.pivot(
        index=["reporter", "cn8_code", "product", "period", "year", "month"],
        columns="partner",
        values="api_record_reported",
    ).reset_index()

    values = values.rename(
        columns={"CN": "china_imports_eur", "WORLD": "world_imports_eur"}
    )
    reported = reported.rename(
        columns={"CN": "china_record_reported", "WORLD": "world_record_reported"}
    )
    panel = values.merge(
        reported,
        on=["reporter", "cn8_code", "product", "period", "year", "month"],
        validate="one_to_one",
    )
    panel["non_china_imports_eur"] = (
        panel["world_imports_eur"] - panel["china_imports_eur"]
    )
    if (panel["non_china_imports_eur"] < 0).any():
        bad = panel.loc[
            panel["non_china_imports_eur"] < 0,
            ["reporter", "product", "period", "china_imports_eur", "world_imports_eur"],
        ]
        raise ValueError(f"China imports exceed world imports:\n{bad.head()}")

    panel["china_share"] = np.where(
        panel["world_imports_eur"] > 0,
        panel["china_imports_eur"] / panel["world_imports_eur"],
        0.0,
    )
    return panel.sort_values(["product", "reporter", "period"]).reset_index(drop=True)


def build_eu27_monthly(country_panel):
    monthly = (
        country_panel.groupby(
            ["cn8_code", "product", "period", "year", "month"], as_index=False
        )
        .agg(
            china_imports_eur=("china_imports_eur", "sum"),
            world_imports_eur=("world_imports_eur", "sum"),
            non_china_imports_eur=("non_china_imports_eur", "sum"),
            china_records_reported=("china_record_reported", "sum"),
            world_records_reported=("world_record_reported", "sum"),
            reporters_positive_china=("china_imports_eur", lambda x: int((x > 0).sum())),
            reporters_positive_world=("world_imports_eur", lambda x: int((x > 0).sum())),
        )
    )
    monthly["china_share"] = np.where(
        monthly["world_imports_eur"] > 0,
        monthly["china_imports_eur"] / monthly["world_imports_eur"],
        0.0,
    )
    expected = len(PRODUCTS) * len(PERIODS)
    if len(monthly) != expected:
        raise ValueError(f"EU27 monthly panel has {len(monthly)} rows, expected {expected}")
    return monthly.sort_values(["product", "period"]).reset_index(drop=True)


def main():
    INTERIM.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    country_rows, source_audit = load_country_rows()
    balanced = build_balanced_panel(country_rows)
    country_panel = build_wide_country_panel(balanced)
    eu27_monthly = build_eu27_monthly(country_panel)

    balanced_path = INTERIM / "eurostat_cn8_eu27_balanced_long.csv"
    audit_path = INTERIM / "eurostat_cn8_source_audit.csv"
    country_path = PROCESSED / "eurostat_cn8_eu27_country_month.csv"
    monthly_path = PROCESSED / "eurostat_cn8_eu27_monthly.csv"

    balanced.to_csv(balanced_path, index=False)
    source_audit.to_csv(audit_path, index=False)
    country_panel.to_csv(country_path, index=False)
    eu27_monthly.to_csv(monthly_path, index=False)

    print(f"Balanced long panel: {len(balanced):,} rows -> {balanced_path}")
    print(f"Country panel:       {len(country_panel):,} rows -> {country_path}")
    print(f"EU27 monthly panel:  {len(eu27_monthly):,} rows -> {monthly_path}")
    print(f"Source audit:        {len(source_audit):,} rows -> {audit_path}")


if __name__ == "__main__":
    main()
