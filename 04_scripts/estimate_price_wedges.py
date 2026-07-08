#!/usr/bin/env python3
"""
Build and estimate preliminary international-China price-wedge models.

The price wedge is:

    log(international price in USD/common unit)
    - log(China domestic price in USD/common unit)

The script writes:

- a long price-wedge panel;
- a pair coverage audit;
- product-level interrupted time-series results;
- small panel DiD results with pair and month fixed effects;
- a pressure-alignment table for clean treated products.

These are preliminary diagnostics. Several price pairs are marked as assumed or
exploratory because Bloomberg descriptions/grades still need to be archived.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


REPO = Path(__file__).resolve().parents[1]
PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"

PRICE_PATH = PROCESSED / "wind_prices_controls_monthly_2019_2026m03.csv"
PRESSURE_SUMMARY_PATH = PROCESSED / "pressure_indices_product_summary.csv"

WEDGE_PANEL_PATH = PROCESSED / "price_wedge_panel_preliminary.csv"
PAIR_AUDIT_PATH = TABLES / "price_wedge_pair_audit_preliminary.csv"
PAIR_ITS_RESULTS_PATH = TABLES / "price_wedge_pair_its_results.csv"
PANEL_DID_RESULTS_PATH = TABLES / "price_wedge_panel_did_results.csv"
PRESSURE_ALIGNMENT_PATH = TABLES / "price_wedge_pressure_alignment.csv"
RUNLOG_PATH = TABLES / "price_wedge_preliminary_run_log.md"

LB_TO_KG = 0.45359237
TON_TO_KG = 1000.0


@dataclass(frozen=True)
class PricePair:
    pair_id: str
    family: str
    hs: str
    role: str
    status: str
    wave: int | None
    post_month: str | None
    international_var: str
    domestic_var: str
    international_unit: str
    domestic_unit: str
    model_use: str
    notes: str


PAIRS = [
    PricePair(
        "gallium_metal",
        "Gallium metal",
        "811292",
        "partial_treated",
        "complete_bundled_hs",
        1,
        "2023-09",
        "ga_int_rotterdam_9999_usd_kg",
        "ga_china_domestic_9999_cny_kg",
        "usd_kg",
        "cny_kg",
        "extended",
        "Treated subcomponent inside bundled HS 811292.",
    ),
    PricePair(
        "germanium_metal",
        "Germanium metal",
        "811292",
        "partial_treated",
        "complete_bundled_hs",
        1,
        "2023-09",
        "ge_metal_int_rotterdam_50ohm_usd_kg",
        "ge_metal_china_avg_50ohm_cny_kg",
        "usd_kg",
        "cny_kg",
        "extended",
        "Treated subcomponent inside bundled HS 811292.",
    ),
    PricePair(
        "geo2",
        "Germanium dioxide",
        "282560",
        "partial_treated",
        "usable_partial_endpoint",
        1,
        "2023-09",
        "geo2_int_rotterdam_9999_usd_kg",
        "geo2_china_99999_cny_kg",
        "usd_kg",
        "cny_kg",
        "extended",
        "International series ends before March 2026.",
    ),
    PricePair(
        "graphite_gpcnlclw",
        "Natural graphite",
        "2504",
        "clean_treated",
        "exploratory_bloomberg_description_missing",
        2,
        "2024-01",
        "graphite_int_bloomberg_gpcnlclw_px_last",
        "graphite_china_natural_flake_cny_ton",
        "index_level",
        "cny_ton",
        "exploratory",
        "Bloomberg ticker description not archived; use only as graphite sensitivity.",
    ),
    PricePair(
        "antimony_metal",
        "Antimony metal",
        "8110",
        "clean_treated",
        "complete",
        3,
        "2024-10",
        "sb_int_rotterdam_9965_usd_ton",
        "sb_china_ingot_9965_cny_ton",
        "usd_ton",
        "cny_ton",
        "core",
        "Clean treated product with matched 99.65% metal benchmarks.",
    ),
    PricePair(
        "bismuth_metal",
        "Bismuth metal",
        "8106",
        "clean_treated",
        "complete",
        4,
        "2025-03",
        "bi_int_rotterdam_9999_usd_lb",
        "bi_china_refined_9999_cny_ton",
        "usd_lb",
        "cny_ton",
        "core",
        "Clean treated product with matched bismuth metal benchmarks.",
    ),
    PricePair(
        "tungsten_tgeuwoqr",
        "Tungsten APT/tungstates",
        "284180",
        "clean_treated",
        "complete_assumed_description_pending",
        4,
        "2025-03",
        "w_int_bloomberg_tgeuwoqr_px_last",
        "w_china_concentrate_65_cny_ton",
        "index_level",
        "cny_ton",
        "core_assumed",
        "Treat only as assumed until Bloomberg DES confirms benchmark and unit.",
    ),
    PricePair(
        "tungsten_ferro_proxy",
        "Tungsten ferro/metal proxy",
        "8101",
        "secondary_treated_proxy",
        "proxy",
        4,
        "2025-03",
        "w_int_ferrotungsten_80_85_rotterdam_usd_kg",
        "w_china_avg_1_9995_cny_kg",
        "usd_kg",
        "cny_kg",
        "secondary",
        "Secondary tungsten metal proxy, not the main HS 284180 pair.",
    ),
    PricePair(
        "indium_metal_control",
        "Indium metal",
        "811292",
        "control_proxy",
        "within_bundle_control_complete",
        None,
        None,
        "in_int_rotterdam_9999_usd_kg",
        "in_china_refined_99995_cny_kg",
        "usd_kg",
        "cny_kg",
        "control",
        "Within-bundle comparison; ordinary indium metal is not the 2025 treated item.",
    ),
    PricePair(
        "vanadium_v2o5_control",
        "Vanadium V2O5",
        "282530",
        "control_proxy",
        "control_exact_starts_2020m10",
        None,
        None,
        "v_int_v2o5_98_rotterdam_usd_lb",
        "v_china_v2o5_98_flake_cny_ton",
        "usd_lb",
        "cny_ton",
        "control",
        "Control/proxy; China V2O5 starts in 2020-10.",
    ),
    PricePair(
        "vanadium_ferro_control",
        "Vanadium ferro",
        "282530",
        "control_proxy",
        "control_proxy_complete",
        None,
        None,
        "v_int_ferrovanadium_80_rotterdam_usd_kg",
        "v_china_ferrovanadium_50_cny_ton",
        "usd_kg",
        "cny_ton",
        "control",
        "Control/proxy with full-window coverage but grade mismatch.",
    ),
]


def convert_to_usd_common_unit(
    value: pd.Series, unit: str, fx_usd_cny: pd.Series
) -> pd.Series:
    if unit == "usd_kg":
        return value
    if unit == "usd_ton":
        return value / TON_TO_KG
    if unit == "usd_lb":
        return value / LB_TO_KG
    if unit == "cny_kg":
        return value / fx_usd_cny
    if unit == "cny_ton":
        return value / fx_usd_cny / TON_TO_KG
    if unit == "index_level":
        # Used only when the benchmark unit is not archived. Constant unit
        # scaling would not change post coefficients, but this remains
        # exploratory until the Bloomberg DES is saved.
        return value
    raise ValueError(f"Unknown unit: {unit}")


def load_prices() -> pd.DataFrame:
    if not PRICE_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PRICE_PATH}. Run prepare_wind_prices_controls.py first."
        )
    df = pd.read_csv(PRICE_PATH, parse_dates=["month_date"], low_memory=False)
    if "fx_usd_cny_cfets_spot" not in df.columns:
        raise ValueError("Missing fx_usd_cny_cfets_spot")
    return df


def build_wedge_panel(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    audit_rows = []
    for pair in PAIRS:
        if pair.international_var not in prices.columns or pair.domestic_var not in prices.columns:
            audit_rows.append(
                {
                    **pair.__dict__,
                    "usable_months": 0,
                    "first_month": "",
                    "last_month": "",
                    "pre_months": 0,
                    "post_months": 0,
                    "missing_reason": "missing variable",
                }
            )
            continue
        fx = prices["fx_usd_cny_cfets_spot"]
        international = convert_to_usd_common_unit(
            prices[pair.international_var], pair.international_unit, fx
        )
        domestic = convert_to_usd_common_unit(prices[pair.domestic_var], pair.domestic_unit, fx)
        work = pd.DataFrame(
            {
                "month_date": prices["month_date"],
                "period": prices["month_date"].dt.strftime("%Y-%m"),
                "pair_id": pair.pair_id,
                "family": pair.family,
                "hs": pair.hs,
                "role": pair.role,
                "status": pair.status,
                "wave": pair.wave,
                "post_month": pair.post_month,
                "model_use": pair.model_use,
                "notes": pair.notes,
                "international_usd_unit": international,
                "domestic_usd_unit": domestic,
            }
        )
        usable = work["international_usd_unit"].gt(0) & work["domestic_usd_unit"].gt(0)
        work = work.loc[usable].copy()
        if pair.post_month:
            post_start = pd.Timestamp(pair.post_month + "-01")
            work["post"] = work["month_date"].ge(post_start).astype(int)
        else:
            post_start = pd.NaT
            work["post"] = 0
        work["trend"] = (work["month_date"].dt.year - 2019) * 12 + work["month_date"].dt.month
        work["log_international"] = np.log(work["international_usd_unit"])
        work["log_domestic"] = np.log(work["domestic_usd_unit"])
        work["log_wedge"] = work["log_international"] - work["log_domestic"]
        work["wedge_ratio"] = np.exp(work["log_wedge"])
        work["treated_price_pair"] = work["role"].isin(
            ["clean_treated", "partial_treated", "secondary_treated_proxy"]
        )
        work["clean_treated_pair"] = work["role"].eq("clean_treated")
        work["control_pair"] = work["role"].eq("control_proxy")
        rows.append(work)
        audit_rows.append(
            {
                **pair.__dict__,
                "usable_months": len(work),
                "first_month": work["period"].min() if not work.empty else "",
                "last_month": work["period"].max() if not work.empty else "",
                "pre_months": int(work["post"].eq(0).sum()) if pair.post_month else 0,
                "post_months": int(work["post"].eq(1).sum()) if pair.post_month else 0,
                "missing_reason": "",
            }
        )

    panel = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    audit = pd.DataFrame(audit_rows)
    return panel, audit


def fit_pair_its(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pair_id, group in panel[panel["post_month"].notna()].groupby("pair_id", sort=False):
        if group["post"].nunique() < 2 or len(group) < 24:
            continue
        model = smf.ols("log_wedge ~ post + trend", data=group).fit(
            cov_type="HAC", cov_kwds={"maxlags": 3}
        )
        for term in ["post"]:
            beta = float(model.params[term])
            se = float(model.bse[term])
            rows.append(
                {
                    "model": "pair_its_hac3",
                    "pair_id": pair_id,
                    "family": group["family"].iloc[0],
                    "hs": group["hs"].iloc[0],
                    "role": group["role"].iloc[0],
                    "status": group["status"].iloc[0],
                    "model_use": group["model_use"].iloc[0],
                    "post_month": group["post_month"].iloc[0],
                    "term": term,
                    "coef": beta,
                    "se": se,
                    "p_value": float(model.pvalues[term]),
                    "percent_change": float(100 * (np.exp(beta) - 1)),
                    "nobs": int(model.nobs),
                    "pre_months": int(group["post"].eq(0).sum()),
                    "post_months": int(group["post"].eq(1).sum()),
                    "mean_pre_wedge": float(group.loc[group["post"].eq(0), "log_wedge"].mean()),
                    "mean_post_wedge": float(group.loc[group["post"].eq(1), "log_wedge"].mean()),
                    "formula": "log_wedge ~ post + trend",
                }
            )
    return pd.DataFrame(rows)


def fit_panel_did(panel: pd.DataFrame) -> pd.DataFrame:
    specs = [
        {
            "sample": "wave2_graphite_exploratory",
            "treated_pairs": ["graphite_gpcnlclw"],
            "control_pairs": [
                "indium_metal_control",
                "vanadium_v2o5_control",
                "vanadium_ferro_control",
            ],
            "post_month": "2024-01",
            "notes": "Graphite benchmark description is not archived.",
        },
        {
            "sample": "wave3_antimony_core",
            "treated_pairs": ["antimony_metal"],
            "control_pairs": [
                "indium_metal_control",
                "vanadium_v2o5_control",
                "vanadium_ferro_control",
            ],
            "post_month": "2024-10",
            "notes": "Clean antimony metal wedge against control/proxy wedges.",
        },
        {
            "sample": "wave4_bismuth_tungsten_core_assumed",
            "treated_pairs": ["bismuth_metal", "tungsten_tgeuwoqr"],
            "control_pairs": [
                "indium_metal_control",
                "vanadium_v2o5_control",
                "vanadium_ferro_control",
            ],
            "post_month": "2025-03",
            "notes": "Tungsten benchmark still needs DES confirmation.",
        },
        {
            "sample": "clean_core_no_graphite",
            "treated_pairs": ["antimony_metal", "bismuth_metal", "tungsten_tgeuwoqr"],
            "control_pairs": [
                "indium_metal_control",
                "vanadium_v2o5_control",
                "vanadium_ferro_control",
            ],
            "post_month": None,
            "notes": "Product-specific post months for clean treated pairs; no graphite.",
        },
        {
            "sample": "extended_partial_plus_core",
            "treated_pairs": [
                "gallium_metal",
                "germanium_metal",
                "geo2",
                "antimony_metal",
                "bismuth_metal",
                "tungsten_tgeuwoqr",
            ],
            "control_pairs": [
                "indium_metal_control",
                "vanadium_v2o5_control",
                "vanadium_ferro_control",
            ],
            "post_month": None,
            "notes": "Adds partial/bundled Ga/Ge/GeO2 pairs.",
        },
    ]
    rows = []
    for spec in specs:
        ids = spec["treated_pairs"] + spec["control_pairs"]
        work = panel.loc[panel["pair_id"].isin(ids)].copy()
        work["treated"] = work["pair_id"].isin(spec["treated_pairs"]).astype(int)
        if spec["post_month"] is not None:
            post_start = pd.Timestamp(spec["post_month"] + "-01")
            work["post_for_model"] = work["month_date"].ge(post_start).astype(int)
        else:
            post_map = {
                pair.pair_id: pair.post_month for pair in PAIRS if pair.post_month is not None
            }
            work["pair_post_month"] = work["pair_id"].map(post_map)
            pair_post_date = pd.to_datetime(
                work["pair_post_month"].fillna("2099-12") + "-01"
            )
            work["post_for_model"] = np.where(
                work["treated"].eq(1),
                work["month_date"].ge(pair_post_date),
                0,
            ).astype(int)
        work["treated_post"] = work["treated"] * work["post_for_model"]
        work = work.dropna(subset=["log_wedge", "treated_post"]).copy()
        work["month_fe"] = work["month_date"].dt.strftime("%Y-%m")
        if work["treated_post"].nunique() < 2:
            continue
        formula = "log_wedge ~ treated_post + C(pair_id) + C(month_fe)"
        hc = smf.ols(formula, data=work).fit(cov_type="HC1")
        try:
            clustered = smf.ols(formula, data=work).fit(
                cov_type="cluster", cov_kwds={"groups": work["pair_id"]}
            )
            cluster_se = float(clustered.bse["treated_post"])
            cluster_p = float(clustered.pvalues["treated_post"])
        except Exception:
            cluster_se = np.nan
            cluster_p = np.nan
        beta = float(hc.params["treated_post"])
        rows.append(
            {
                "sample": spec["sample"],
                "treated_pairs": ",".join(spec["treated_pairs"]),
                "control_pairs": ",".join(spec["control_pairs"]),
                "post_month": spec["post_month"] or "pair_specific",
                "coef": beta,
                "se_hc1": float(hc.bse["treated_post"]),
                "p_hc1": float(hc.pvalues["treated_post"]),
                "se_pair_cluster": cluster_se,
                "p_pair_cluster": cluster_p,
                "percent_change": float(100 * (np.exp(beta) - 1)),
                "nobs": int(hc.nobs),
                "pairs": int(work["pair_id"].nunique()),
                "treated_pairs_n": len(spec["treated_pairs"]),
                "control_pairs_n": len(spec["control_pairs"]),
                "notes": spec["notes"],
                "formula": formula,
            }
        )
    return pd.DataFrame(rows)


def build_pressure_alignment(pair_results: pd.DataFrame) -> pd.DataFrame:
    if not PRESSURE_SUMMARY_PATH.exists() or pair_results.empty:
        return pd.DataFrame()
    pressure = pd.read_csv(PRESSURE_SUMMARY_PATH, dtype={"hs": str}, low_memory=False)
    keep = pressure[
        [
            "hs",
            "weighted_china_import_share" if "weighted_china_import_share" in pressure.columns else "weighted_e_china_exposure",
        ]
    ]
    # Use the richer diagnostics file when available.
    diagnostics_path = TABLES / "pressure_product_diagnostics.csv"
    if diagnostics_path.exists():
        keep = pd.read_csv(diagnostics_path, dtype={"hs": str}, low_memory=False)[
            [
                "hs",
                "weighted_china_import_share",
                "weighted_p_switch_capacity",
                "weighted_p_compress_capacity",
                "weighted_p_switch_absorptive",
                "weighted_p_compress_absorptive",
                "compression_share_capacity",
                "compression_share_absorptive",
            ]
        ]
    out = pair_results[pair_results["model"].eq("pair_its_hac3")].merge(
        keep, on="hs", how="left"
    )
    return out


def write_runlog(audit: pd.DataFrame, pair_results: pd.DataFrame, panel_results: pd.DataFrame) -> None:
    audit_cols = [
        "pair_id",
        "family",
        "hs",
        "role",
        "status",
        "model_use",
        "usable_months",
        "pre_months",
        "post_months",
    ]
    lines = [
        "# Preliminary Price-Wedge Run",
        "",
        "Outcome: `log_wedge = log(international price) - log(China domestic price)`.",
        "",
        "Product-level tests use `log_wedge ~ post + trend` with HAC(3) standard errors.",
        "",
        "Panel tests use pair and month fixed effects. HC1 p-values are reported; pair-cluster p-values are only diagnostics because there are few price pairs.",
        "",
        "## Pair Audit",
        "",
        audit[audit_cols].to_string(index=False),
        "",
        "## Product-Level Results",
        "",
    ]
    if pair_results.empty:
        lines.append("- No product-level models estimated.")
    else:
        for _, row in pair_results.iterrows():
            lines.append(
                f"- {row['pair_id']}: coef={row['coef']:.4f}, p={row['p_value']:.4g}, "
                f"change={row['percent_change']:.1f}%, n={row['nobs']}."
            )
    lines += ["", "## Panel Results", ""]
    if panel_results.empty:
        lines.append("- No panel models estimated.")
    else:
        for _, row in panel_results.iterrows():
            lines.append(
                f"- {row['sample']}: coef={row['coef']:.4f}, HC1 p={row['p_hc1']:.4g}, "
                f"pair-cluster p={row['p_pair_cluster']:.4g}, change={row['percent_change']:.1f}%, "
                f"pairs={row['pairs']}."
            )
    RUNLOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(panel: pd.DataFrame, audit: pd.DataFrame) -> None:
    errors = []
    if panel.empty:
        errors.append("price wedge panel is empty")
    if audit["usable_months"].max() <= 0:
        errors.append("no usable price pair months")
    if panel["log_wedge"].isna().any():
        errors.append("missing log wedge in built panel")
    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    prices = load_prices()
    panel, audit = build_wedge_panel(prices)
    validate(panel, audit)
    pair_results = fit_pair_its(panel)
    panel_results = fit_panel_did(panel)
    alignment = build_pressure_alignment(pair_results)

    panel.to_csv(WEDGE_PANEL_PATH, index=False)
    audit.to_csv(PAIR_AUDIT_PATH, index=False)
    pair_results.to_csv(PAIR_ITS_RESULTS_PATH, index=False)
    panel_results.to_csv(PANEL_DID_RESULTS_PATH, index=False)
    alignment.to_csv(PRESSURE_ALIGNMENT_PATH, index=False)
    write_runlog(audit, pair_results, panel_results)

    print(f"Wrote {WEDGE_PANEL_PATH}")
    print(f"Wrote {PAIR_AUDIT_PATH}")
    print(f"Wrote {PAIR_ITS_RESULTS_PATH}")
    print(f"Wrote {PANEL_DID_RESULTS_PATH}")
    print(f"Wrote {PRESSURE_ALIGNMENT_PATH}")
    print(f"Wrote {RUNLOG_PATH}")
    print("\nPair audit:")
    print(
        audit[
            [
                "pair_id",
                "family",
                "role",
                "status",
                "model_use",
                "usable_months",
                "pre_months",
                "post_months",
            ]
        ].to_string(index=False)
    )
    print("\nProduct-level results:")
    print(
        pair_results[
            [
                "pair_id",
                "role",
                "status",
                "coef",
                "p_value",
                "percent_change",
                "nobs",
                "pre_months",
                "post_months",
            ]
        ].to_string(index=False)
    )
    print("\nPanel DiD results:")
    print(
        panel_results[
            [
                "sample",
                "coef",
                "p_hc1",
                "p_pair_cluster",
                "percent_change",
                "nobs",
                "pairs",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
