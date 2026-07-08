"""Prepare CEPII GeoDist covariates for the configured Comtrade reporters."""

import json
from pathlib import Path

import pandas as pd


REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "03_data" / "raw"
PROCESSED = REPO / "03_data" / "processed"

REPORTERS = [
    276, 97, 392, 344, 410, 826, 842, 56, 124, 156, 724, 818, 251, 764,
    752, 757, 975, 76, 380, 792, 100, 203, 376, 398, 528, 804, 191, 702,
    428, 36, 616, 31, 554, 704, 440, 348, 642, 579, 372, 32, 484, 620,
    604, 508, 703, 84, 682, 705, 404, 360, 699, 710, 834, 860, 854, 788,
]

ISO_ALIASES = {"ROU": "ROM"}
AGGREGATE_REPORTERS = {97, 975}


def main():
    reporters_path = RAW / "comtrade_reporters.json"
    geodist_path = RAW / "geodist" / "dist_cepii.dta"
    if not reporters_path.exists():
        raise FileNotFoundError(reporters_path)
    if not geodist_path.exists():
        raise FileNotFoundError(geodist_path)

    reference = json.loads(reporters_path.read_text())["results"]
    lookup = {int(row["reporterCode"]): row for row in reference}
    reporters = pd.DataFrame(
        [
            {
                "reporterCode": code,
                "reporter": lookup[code]["reporterDesc"],
                "iso3": lookup[code]["reporterCodeIsoAlpha3"],
                "is_aggregate_reporter": code in AGGREGATE_REPORTERS,
            }
            for code in REPORTERS
        ]
    )
    reporters["geodist_iso3"] = reporters["iso3"].replace(ISO_ALIASES)

    geodist = pd.read_stata(geodist_path, convert_categoricals=False)
    china = geodist[geodist["iso_o"] == "CHN"].copy()
    if china.duplicated("iso_d").any():
        raise ValueError("GeoDist contains duplicate China-destination dyads")

    output = reporters.merge(
        china,
        left_on="geodist_iso3",
        right_on="iso_d",
        how="left",
        validate="one_to_one",
    )
    country_rows = output[~output["is_aggregate_reporter"]]
    unmatched = country_rows[country_rows["distw"].isna()]
    if len(unmatched):
        raise ValueError(
            "Unmatched country reporters:\n"
            + unmatched[["reporterCode", "reporter", "iso3"]].to_string(index=False)
        )

    output["geodist_match"] = output["distw"].notna()
    keep = [
        "reporterCode", "reporter", "iso3", "geodist_iso3",
        "is_aggregate_reporter", "geodist_match",
        "dist", "distcap", "distw", "distwces",
        "contig", "comlang_off", "comlang_ethno",
        "colony", "comcol", "curcol", "col45", "smctry",
    ]
    output = output[keep].sort_values("reporterCode")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    path = PROCESSED / "geodist_china_reporters.csv"
    output.to_csv(path, index=False)
    print(f"Saved {len(output)} reporters -> {path}")
    print(
        f"Matched countries: {int(country_rows['distw'].notna().sum())}/"
        f"{len(country_rows)}; aggregates excluded: {len(output) - len(country_rows)}"
    )


if __name__ == "__main__":
    main()
