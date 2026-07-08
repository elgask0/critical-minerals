#!/usr/bin/env python3
"""
Build the frozen product-scope metadata table for thesis-stage analysis.

The table is the gatekeeper for later processing. It separates clean treated
products, secondary scope cases, candidate controls, diagnostics, and excluded
guardrails before any PPML model is estimated.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import pandas as pd


REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "03_data" / "raw"
PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

EXPECTED_REPORTER_YEAR_FILES = 56 * 8
FREEZE_DATE = date.today().isoformat()


PRODUCTS: list[dict[str, object]] = [
    # Clean treated products for the first main model.
    dict(hs="2504", product_name="Natural graphite", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="2", policy_episode="Graphite", announcement_date="2023-10-20", implementation_date="2023-12-01", import_effect_month="2024-01", treatment_status="clean_treated", scope_status="clean", analysis_role="main_clean_treated", usable_as_control=False, exclusion_reason="Treated graphite product."),
    dict(hs="8110", product_name="Antimony metal and articles", download_batch="antimony", design_universe="downloader_34", policy_screened=True, wave="3", policy_episode="Antimony", announcement_date="2024-08-15", implementation_date="2024-09-15", import_effect_month="2024-10", treatment_status="clean_treated", scope_status="clean", analysis_role="main_clean_treated", usable_as_control=False, exclusion_reason="Treated antimony product."),
    dict(hs="261710", product_name="Antimony ores and concentrates", download_batch="antimony", design_universe="downloader_34", policy_screened=True, wave="3", policy_episode="Antimony", announcement_date="2024-08-15", implementation_date="2024-09-15", import_effect_month="2024-10", treatment_status="clean_treated", scope_status="clean_sparse", analysis_role="main_clean_treated_sparse_caution", usable_as_control=False, exclusion_reason="Treated antimony product."),
    dict(hs="8106", product_name="Bismuth metal", download_batch="wave4-clean", design_universe="downloader_34", policy_screened=True, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="clean_treated", scope_status="clean", analysis_role="main_clean_treated", usable_as_control=False, exclusion_reason="Treated bismuth product."),
    dict(hs="284180", product_name="Tungstates and APT", download_batch="wave4-clean", design_universe="downloader_34", policy_screened=True, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="clean_treated", scope_status="clean", analysis_role="main_clean_treated", usable_as_control=False, exclusion_reason="Treated tungsten/APT product."),

    # Secondary scope cases. These are not clean donors.
    dict(hs="811292", product_name="Ga/Ge/In/V/Nb unwrought bundle", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="1", policy_episode="Ga/Ge", announcement_date="2023-07-03", implementation_date="2023-08-01", import_effect_month="2023-09", treatment_status="bundled_treated", scope_status="bundled", analysis_role="secondary_scope_case", usable_as_control=False, exclusion_reason="HS heading bundles treated Ga/Ge with untreated metals."),
    dict(hs="282560", product_name="Germanium dioxide / zirconium dioxide", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="1", policy_episode="Ga/Ge", announcement_date="2023-07-03", implementation_date="2023-08-01", import_effect_month="2023-09", treatment_status="bundled_treated", scope_status="bundled", analysis_role="secondary_scope_case", usable_as_control=False, exclusion_reason="HS heading contains controlled GeO2 and uncontrolled ZrO2."),
    dict(hs="282580", product_name="Antimony oxides", download_batch="antimony", design_universe="downloader_34", policy_screened=True, wave="3", policy_episode="Antimony", announcement_date="2024-08-15", implementation_date="2024-09-15", import_effect_month="2024-10", treatment_status="partial_treated", scope_status="partial", analysis_role="secondary_scope_case", usable_as_control=False, exclusion_reason="Only high-purity antimony oxides are controlled at fine code level."),
    dict(hs="8101", product_name="Tungsten metal and articles", download_batch="wave4-partial", design_universe="downloader_34", policy_screened=True, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="partial_treated", scope_status="partial", analysis_role="secondary_scope_case", usable_as_control=False, exclusion_reason="Only specified high-W solid forms and dimensions are controlled."),
    dict(hs="3801", product_name="Artificial and colloidal graphite", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="2", policy_episode="Graphite", announcement_date="2023-10-20", implementation_date="2023-12-01", import_effect_month="2024-01", treatment_status="scope_contaminated_treated", scope_status="graphite_scope_contaminated", analysis_role="secondary_scope_case", usable_as_control=False, exclusion_reason="Some artificial or colloidal graphite may overlap the graphite control scope."),

    # Marginal treated products in the downloader design.
    dict(hs="280450", product_name="Tellurium and boron", download_batch="marginal-treated", design_universe="downloader_34", policy_screened=True, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="marginal_treated", scope_status="marginal_bundled", analysis_role="descriptive_only", usable_as_control=False, exclusion_reason="Tellurium is controlled, but HS heading is bundled with boron."),
    dict(hs="284690", product_name="Non-cerium rare-earth compounds", download_batch="marginal-treated", design_universe="downloader_34", policy_screened=True, wave="5", policy_episode="Medium/heavy rare earths", announcement_date="2025-04-04", implementation_date="2025-04-04", import_effect_month="2025-05", treatment_status="marginal_treated", scope_status="marginal_bundled", analysis_role="descriptive_only", usable_as_control=False, exclusion_reason="Controlled rare earths are only part of the HS-6 heading."),

    # Candidate controls. Final donor use still requires pre-treatment screening.
    dict(hs="2818", product_name="Alumina", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="8111", product_name="Manganese articles", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="2811", product_name="Inorganic acids", download_batch="extend-current", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="2615", product_name="Niobium, tantalum, vanadium, or zirconium ores", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="284170", product_name="Molybdates", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason="Molybdenum powder control is not this HS heading; still screen by wave."),
    dict(hs="811221", product_name="Chromium unwrought and powders", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="380130", product_name="Carbon electrode pastes", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="282530", product_name="Vanadium oxides and hydroxides", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="282520", product_name="Lithium oxide and hydroxide", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="282570", product_name="Molybdenum oxides and hydroxides", download_batch="core-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason="Molybdenum powder control is not this HS heading; still screen by wave."),
    dict(hs="8103", product_name="Tantalum metal and articles", download_batch="metal-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="8108", product_name="Titanium metal and articles", download_batch="metal-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="8109", product_name="Zirconium metal and articles", download_batch="metal-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="8104", product_name="Magnesium metal and articles", download_batch="metal-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="8105", product_name="Cobalt mattes and metal", download_batch="metal-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="282110", product_name="Iron oxides and hydroxides", download_batch="deferred-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="2820", product_name="Manganese oxides", download_batch="deferred-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="2833", product_name="Sulfates", download_batch="deferred-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason=""),
    dict(hs="284610", product_name="Cerium compounds", download_batch="deferred-placebos", design_universe="downloader_34", policy_screened=True, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="candidate_control", scope_status="control_candidate", analysis_role="candidate_control_pending_screen", usable_as_control=True, exclusion_reason="Cerium itself is not in the medium/heavy rare-earth control list, but wave-specific screening is still required."),

    # Downloader diagnostics.
    dict(hs="380120", product_name="Colloidal or semi-colloidal graphite", download_batch="policy-contaminated", design_universe="downloader_34", policy_screened=False, wave="2", policy_episode="Graphite", announcement_date="2023-10-20", implementation_date="2023-12-01", import_effect_month="2024-01", treatment_status="policy_contaminated_diagnostic", scope_status="policy_contaminated", analysis_role="diagnostic_only", usable_as_control=False, exclusion_reason="May fall within graphite-control scope; not a clean donor."),
    dict(hs="2827", product_name="Chlorides and related halides", download_batch="policy-contaminated", design_universe="downloader_34", policy_screened=False, wave="1", policy_episode="Ga/Ge", announcement_date="2023-07-03", implementation_date="2023-08-01", import_effect_month="2023-09", treatment_status="policy_contaminated_diagnostic", scope_status="policy_contaminated", analysis_role="diagnostic_only", usable_as_control=False, exclusion_reason="Contains controlled germanium tetrachloride."),
    dict(hs="2617", product_name="Other ores and concentrates, broad heading", download_batch="broad-diagnostics", design_universe="downloader_34", policy_screened=False, wave="3", policy_episode="Antimony", announcement_date="2024-08-15", implementation_date="2024-09-15", import_effect_month="2024-10", treatment_status="broad_diagnostic", scope_status="broad_hs4", analysis_role="diagnostic_only", usable_as_control=False, exclusion_reason="HS-4 heading mixes antimony and non-antimony ores."),

    # Raw probes and donor-pool guardrails outside the downloader universe.
    dict(hs="2501", product_name="Salt, sodium chloride, and brine", download_batch="raw_probe", design_universe="raw_probe_excluded", policy_screened=False, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="excluded_sparse", scope_status="sparse_or_incomplete", analysis_role="excluded", usable_as_control=False, exclusion_reason="Coverage is sparse/incomplete; not a rare-earth case."),
    dict(hs="2821", product_name="Iron oxides/hydroxides broad probe", download_batch="raw_probe", design_universe="raw_probe_excluded", policy_screened=False, wave="", policy_episode="", announcement_date="", implementation_date="", import_effect_month="", treatment_status="outside_design_probe", scope_status="outside_design", analysis_role="excluded", usable_as_control=False, exclusion_reason="Raw probe outside the frozen thesis design."),
    dict(hs="282590", product_name="Tungsten oxides", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="treated_guardrail", scope_status="treated_not_downloaded", analysis_role="excluded", usable_as_control=False, exclusion_reason="Treated tungsten product under Announcement No. 10/2025; never a placebo."),
    dict(hs="284990", product_name="Tungsten carbide", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="treated_guardrail", scope_status="treated_not_downloaded", analysis_role="excluded", usable_as_control=False, exclusion_reason="Treated tungsten product under Announcement No. 10/2025; never a placebo."),
    dict(hs="8102", product_name="Molybdenum metal and articles", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="4", policy_episode="W/Te/Bi/Mo/In", announcement_date="2025-02-04", implementation_date="2025-02-04", import_effect_month="2025-03", treatment_status="excluded_narrow_treated", scope_status="too_narrow_for_hs6", analysis_role="excluded", usable_as_control=False, exclusion_reason="Only narrow missile-grade molybdenum powder is controlled; HS-6 heading is too broad."),
    dict(hs="280530", product_name="Rare-earth metals", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="5", policy_episode="Medium/heavy rare earths", announcement_date="2025-04-04", implementation_date="2025-04-04", import_effect_month="2025-05", treatment_status="excluded_partial_treated", scope_status="too_diluted_for_hs6", analysis_role="excluded", usable_as_control=False, exclusion_reason="Controlled rare earths are a fraction of this HS-6 heading."),
    dict(hs="380110", product_name="Artificial graphite subcode", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="2", policy_episode="Graphite", announcement_date="2023-10-20", implementation_date="2023-12-01", import_effect_month="2024-01", treatment_status="excluded_scope_contaminated", scope_status="graphite_scope_contaminated", analysis_role="excluded", usable_as_control=False, exclusion_reason="Already treated or partially treated under the 2023 graphite regime."),
    dict(hs="380190", product_name="Other graphite subcode", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="2", policy_episode="Graphite", announcement_date="2023-10-20", implementation_date="2023-12-01", import_effect_month="2024-01", treatment_status="excluded_scope_contaminated", scope_status="graphite_scope_contaminated", analysis_role="excluded", usable_as_control=False, exclusion_reason="Already treated or partially treated under the 2023 graphite regime."),
    dict(hs="8507", product_name="Electric accumulators", download_batch="guardrail", design_universe="guardrail_excluded", policy_screened=False, wave="", policy_episode="Suspended later measure", announcement_date="", implementation_date="", import_effect_month="", treatment_status="excluded_suspended_policy", scope_status="broad_growth_heading", analysis_role="excluded", usable_as_control=False, exclusion_reason="Later battery measure was suspended before implementation; heading has strong independent demand trend."),
]


PRICE_STATUS_OVERRIDES = {
    "261710": "china_side_present_no_complete_wedge (China antimony concentrate 50% series present; no complete international concentrate benchmark.)",
    "2818": "missing_alumina_price_pair",
    "8111": "missing_manganese_price_pair",
    "2811": "chemical_ppi_controls_only_no_acid_price_pair",
    "2615": "family_proxy_partial (vanadium and molybdenum proxies present; niobium, tantalum, and zirconium ore proxies missing.)",
    "811221": "missing_chromium_price_pair",
    "380130": "missing_carbon_electrode_paste_price_pair",
    "282520": "battery_demand_controls_present_lithium_price_pair_missing",
    "8103": "missing_tantalum_price_pair",
    "8108": "missing_titanium_price_pair",
    "8109": "missing_zirconium_price_pair",
    "8104": "missing_magnesium_price_pair",
    "8105": "battery_demand_controls_present_cobalt_price_pair_missing",
    "282110": "missing_iron_oxide_price_pair",
    "2820": "missing_manganese_oxide_price_pair",
    "2833": "chemical_ppi_controls_only_no_sulfate_price_pair",
    "284610": "missing_cerium_price_pair",
    "284690": "no_clean_rare_earth_price_suite; dropped from price-wedge work unless new data are found",
}


def count_lines(path: Path) -> int | None:
    if not path.exists():
        return None
    with path.open("rb") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def classify_request_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.stat().st_size <= 20:
        if path.read_text(errors="ignore").strip() == "skip":
            return "skip"
        return "bad"
    try:
        frame = pd.read_csv(path, nrows=1)
    except Exception:
        return "bad"
    if len(frame) > 0:
        return "data"
    return "bad"


def raw_coverage(hs: str) -> dict[str, object]:
    hs_dir = RAW / f"imports_{hs}"
    request_files = sorted(hs_dir.glob("*.csv")) if hs_dir.exists() else []
    states = [classify_request_file(path) for path in request_files]
    data_files = states.count("data")
    skip_files = states.count("skip")
    bad_files = states.count("bad")
    valid_files = data_files + skip_files
    merged_path = RAW / f"comtrade_{hs}_imports.csv"
    merged_rows = count_lines(merged_path)

    if not hs_dir.exists() and not merged_path.exists():
        status = "not_downloaded"
    elif valid_files >= EXPECTED_REPORTER_YEAR_FILES and merged_path.exists():
        status = "complete_ready"
    elif valid_files >= EXPECTED_REPORTER_YEAR_FILES and not merged_path.exists():
        status = "complete_no_merged_file"
    else:
        status = "incomplete"

    return {
        "raw_dir_exists": hs_dir.exists(),
        "merged_file_exists": merged_path.exists(),
        "request_files": len(request_files),
        "valid_request_files": valid_files,
        "data_request_files": data_files,
        "skip_request_files": skip_files,
        "bad_request_files": bad_files,
        "merged_rows": merged_rows if merged_rows is not None else "",
        "trade_data_status": status,
    }


def price_status_by_hs() -> dict[str, list[str]]:
    path = TABLES / "price_wedge_candidate_coverage_2026-07-01.csv"
    if not path.exists():
        return {}
    table = pd.read_csv(path)
    mapping: dict[str, list[str]] = {}
    for row in table.to_dict("records"):
        for hs in str(row.get("hs_mapping", "")).split(";"):
            hs = hs.strip()
            if not hs:
                continue
            item = (
                f"{row['candidate']}: {row['status']} "
                f"({row.get('notes', '')})"
            )
            mapping.setdefault(hs, []).append(item)
    return mapping


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    price_map = price_status_by_hs()

    rows = []
    seen = set()
    for product in PRODUCTS:
        hs = str(product["hs"])
        if hs in seen:
            raise ValueError(f"Duplicate HS metadata row: {hs}")
        seen.add(hs)
        coverage = raw_coverage(hs)
        price_notes = price_map.get(hs, [])
        price_pair_status = (
            " | ".join(price_notes)
            if price_notes
            else PRICE_STATUS_OVERRIDES.get(hs, "not_available_or_not_required")
        )
        ready_for_next_panel = (
            bool(product["policy_screened"])
            and coverage["trade_data_status"] == "complete_ready"
        )
        ready_for_main_clean = (
            product["analysis_role"]
            in {"main_clean_treated", "main_clean_treated_sparse_caution"}
            and coverage["trade_data_status"] == "complete_ready"
        )
        ready_for_donor_screen = (
            product["analysis_role"] == "candidate_control_pending_screen"
            and coverage["trade_data_status"] == "complete_ready"
        )
        row = {
            **product,
            "expected_request_files": EXPECTED_REPORTER_YEAR_FILES,
            **coverage,
            "ready_for_next_processed_panel": ready_for_next_panel,
            "ready_for_main_clean_treated_sample": ready_for_main_clean,
            "ready_for_clean_donor_screen": ready_for_donor_screen,
            "price_pair_status": price_pair_status,
            "metadata_freeze_date": FREEZE_DATE,
        }
        rows.append(row)

    output = pd.DataFrame(rows).sort_values(
        ["design_universe", "download_batch", "hs"], kind="stable"
    )
    path = PROCESSED / "product_scope_metadata.csv"
    output.to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL)

    audit = output.groupby(
        ["design_universe", "analysis_role", "trade_data_status"],
        dropna=False,
        as_index=False,
    ).agg(products=("hs", "nunique"))
    audit_path = TABLES / "product_scope_metadata_audit.csv"
    audit.to_csv(audit_path, index=False)

    print(f"Wrote {path} ({len(output)} products)")
    print(f"Wrote {audit_path}")
    print("\nReady for next processed panel:")
    print(
        output.loc[
            output["ready_for_next_processed_panel"],
            ["hs", "product_name", "analysis_role", "trade_data_status"],
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
