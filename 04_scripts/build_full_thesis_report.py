#!/usr/bin/env python3
"""
Build a thesis-facing empirical report from the production-A pressure pipeline.

This script does not overwrite the production-A model outputs. It consolidates
them into results/full_thesis_report/ and adds RoW/total event-study diagnostics
that are needed for the final thesis report structure.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "04_scripts"))

import run_revised_pressure_k_prod_a as prod  # noqa: E402


SOURCE = REPO / "results" / "revised_pressure_K_prod_A_2023"
SOURCE_2024 = REPO / "results" / "revised_pressure_K_prod_A_2024"
OUT = REPO / "results" / "full_thesis_report"

BASELINE_ANCHOR = "first_full_post_quarter"
BASELINE_FREQ = "quarterly"
BASELINE_VARIANT = "capacity"


def read_csv(name: str, source: Path = SOURCE) -> pd.DataFrame:
    path = source / name
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / name, index=False)


def percent(beta: float) -> float:
    if pd.isna(beta):
        return np.nan
    return float(100 * (np.exp(float(beta)) - 1))


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def event_terms_for_wide(work: pd.DataFrame, outcome_label: str) -> list[str]:
    terms: list[str] = []
    for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
        name = f"{outcome_label}_event_{'m' if k < 0 else 'p'}{abs(k)}"
        work[name] = (
            work["treated_group"].astype(bool) & work["event_time"].eq(k)
        ).astype(int)
        terms.append(name)
    return terms


def run_wide_event_studies() -> pd.DataFrame:
    """Run RoW and total-import event studies on the wide panel."""
    pressure = read_csv("pressure_indices_prod_importer_product.csv")
    pressure["hs"] = pressure["hs"].astype(str)
    wide_m = prod.attach_pressure(prod.load_wide_panel(), pressure)
    wide_q = prod.make_quarterly_wide(wide_m)
    panels = {
        "monthly": wide_m,
        "quarterly": wide_q,
    }
    outcomes = {
        "row_imports": "non_china_primaryValue",
        "total_imports": "world_primaryValue",
        "china_imports": "china_primaryValue",
    }
    rows: list[dict] = []
    for freq, panel in panels.items():
        fe = prod.WIDE_MONTHLY_FE if freq == "monthly" else prod.WIDE_QUARTERLY_FE
        for group in prod.GROUPS:
            base = prod.sample_for_group(panel, group)
            for anchor in prod.ANCHORS:
                for outcome_label, outcome in outcomes.items():
                    work = base.copy()
                    work["event_time"] = prod.local_event_time(work, group, anchor, freq)
                    work = work.loc[work["event_time"].between(-4, 4)].copy()
                    terms = event_terms_for_wide(work, outcome_label)
                    meta = {
                        "frequency": freq,
                        "model": f"{outcome_label}_event_study",
                        "group": group.key,
                        "group_label": group.label,
                        "family": group.family,
                        "anchor": anchor,
                        "pressure_variant": "none",
                        "row_type": "coefficient",
                    }
                    fit_rows, coef, vcov = prod.fit_ppml_with_vcov(
                        work, outcome, terms, fe, meta
                    )
                    rows.extend(fit_rows)
                    rows.extend(
                        prod.joint_pretrend_rows(
                            coef,
                            vcov,
                            [
                                f"{outcome_label}_event_m4",
                                f"{outcome_label}_event_m3",
                                f"{outcome_label}_event_m2",
                            ],
                            meta,
                            fe,
                        )
                    )
    return pd.DataFrame(rows)


def build_data_audit() -> pd.DataFrame:
    production = read_csv("production_A_audit.csv")
    sample = read_csv("product_sample_table.csv")
    mapping = production.merge(
        sample[
            [
                "hs",
                "product_name",
                "wave",
                "policy_episode",
                "announcement_date",
                "implementation_date",
                "import_effect_month",
                "treatment_status",
                "scope_status",
                "analysis_role",
            ]
        ],
        on=["hs", "product_name"],
        how="left",
    )
    mapping["source_file"] = "World_Data_Release_MCS_2025/MCS2025_World_Data.csv"
    return mapping


def build_summary_stats() -> pd.DataFrame:
    dist = read_csv("pressure_index_summary_prod.csv")
    dist["stat_type"] = "distribution"
    corr = read_csv("pressure_index_correlations_prod.csv")
    corr = corr.rename(columns={"left": "variable", "right": "product", "correlation": "mean"})
    corr["stat_type"] = "correlation"
    for col in ["count", "sd", "min", "p25", "median", "p75", "max"]:
        corr[col] = np.nan
    corr = corr[dist.columns]
    return pd.concat([dist, corr], ignore_index=True, sort=False)


def build_main_results() -> pd.DataFrame:
    files = {
        "baseline_ppml_quarterly": "main_average_ppml_quarterly_prod.csv",
        "baseline_ppml_monthly": "main_average_ppml_monthly_prod.csv",
        "exposure_quarterly": "china_exposure_interaction_quarterly_prod.csv",
        "exposure_monthly": "china_exposure_interaction_monthly_prod.csv",
        "mechanism_source_quarterly": "source_contrast_PS_PC_quarterly_prod.csv",
        "mechanism_source_monthly": "source_contrast_PS_PC_monthly_prod.csv",
        "e_k_quarterly": "source_contrast_E_K_quarterly_prod.csv",
        "e_k_monthly": "source_contrast_E_K_monthly_prod.csv",
    }
    frames = []
    for module, name in files.items():
        df = read_csv(name)
        df.insert(0, "report_module", module)
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False)


def build_mechanisms() -> pd.DataFrame:
    files = {
        "row_quarterly": "mechanism_row_quarterly_prod.csv",
        "row_monthly": "mechanism_row_monthly_prod.csv",
        "total_quarterly": "mechanism_total_quarterly_prod.csv",
        "total_monthly": "mechanism_total_monthly_prod.csv",
        "summary": "mechanism_summary_prod.csv",
    }
    frames = []
    for module, name in files.items():
        df = read_csv(name)
        df.insert(0, "report_module", module)
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False)


def build_event_study() -> pd.DataFrame:
    files = {
        "source_average_quarterly": "event_study_average_quarterly_prod.csv",
        "source_average_monthly": "event_study_average_monthly_prod.csv",
        "source_pressure_quarterly": "event_study_pressure_quarterly_prod.csv",
        "source_pressure_monthly": "event_study_pressure_monthly_prod.csv",
    }
    frames = []
    for module, name in files.items():
        df = read_csv(name)
        df.insert(0, "report_module", module)
        frames.append(df)
    wide_events = OUT / "EVENT_STUDY_MECHANISMS.csv"
    if wide_events.exists():
        wide = pd.read_csv(wide_events)
    else:
        wide = run_wide_event_studies()
        write_csv(wide, "EVENT_STUDY_MECHANISMS.csv")
    wide.insert(0, "report_module", "wide_china_row_total")
    frames.append(wide)
    return pd.concat(frames, ignore_index=True, sort=False)


def build_placebos() -> pd.DataFrame:
    files = {
        "average": "placebo_average_prod.csv",
        "exposure": "placebo_exposure_prod.csv",
        "pressure": "placebo_pressure_prod.csv",
    }
    frames = []
    for module, name in files.items():
        df = read_csv(name)
        df.insert(0, "report_module", module)
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False)


def build_robustness() -> pd.DataFrame:
    files = {
        "us_excluded_quarterly": "us_excluded_quarterly_prod.csv",
        "us_excluded_monthly": "us_excluded_monthly_prod.csv",
        "us_interactions": "us_interactions_prod.csv",
        "net_weight": "net_weight_robustness_prod.csv",
        "tradeA_vs_prodA": "old_tradeA_vs_new_prodA_comparison.csv",
    }
    frames = []
    for module, name in files.items():
        df = read_csv(name)
        df.insert(0, "report_module", module)
        frames.append(df)
    for module, name in {
        "prodA_2024_source": "source_contrast_PS_PC_quarterly_prod_2024.csv",
        "prodA_2024_row": "mechanism_row_quarterly_prod_2024.csv",
        "prodA_2024_total": "mechanism_total_quarterly_prod_2024.csv",
    }.items():
        df = read_csv(name, SOURCE_2024)
        df.insert(0, "report_module", module)
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False)


def baseline_slice(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "frequency" in out:
        out = out.loc[out["frequency"].eq(BASELINE_FREQ)]
    if "anchor" in out:
        out = out.loc[out["anchor"].eq(BASELINE_ANCHOR)]
    if "pressure_variant" in out:
        out = out.loc[out["pressure_variant"].isin([BASELINE_VARIANT, "none", "exposure"])]
    return out


def first_value(df: pd.DataFrame, group: str, term: str, model_contains: str | None = None) -> pd.Series | None:
    sub = df.loc[df["group"].eq(group) & df["term"].eq(term)].copy()
    if model_contains and "model" in sub:
        sub = sub.loc[sub["model"].astype(str).str.contains(model_contains, na=False)]
    if sub.empty:
        return None
    return sub.iloc[0]


def p_clean(p: object) -> bool:
    try:
        return bool(float(p) >= 0.10)
    except Exception:
        return False


def p_problem(p: object) -> bool:
    try:
        return bool(float(p) < 0.05)
    except Exception:
        return False


def classify_product(row: dict) -> str:
    avg_neg = row["average_effect_negative"]
    row_switch = row["row_switch_positive"]
    total_comp = row["total_compression_negative"]
    price_pos = row["price_wedge_positive"]
    if not avg_neg and not price_pos:
        return "weak/null case"
    if row_switch and total_comp:
        return "mixed case"
    if row_switch:
        return "switching case"
    if total_comp:
        return "compression case"
    if price_pos:
        return "segmentation case"
    return "mixed case"


def build_interpretation_table() -> pd.DataFrame:
    avg = baseline_slice(read_csv("main_average_ppml_quarterly_prod.csv"))
    source = baseline_slice(read_csv("source_contrast_PS_PC_quarterly_prod.csv"))
    mech = baseline_slice(read_csv("mechanism_summary_prod.csv"))
    event = read_csv("event_study_average_quarterly_prod.csv")
    event = event.loc[
        event["row_type"].eq("joint_pretrend")
        & event["frequency"].eq(BASELINE_FREQ)
    ].copy()
    placebo = read_csv("placebo_pressure_prod.csv")
    placebo = placebo.loc[
        placebo["frequency"].eq(BASELINE_FREQ)
        & placebo["anchor"].eq(BASELINE_ANCHOR)
        & placebo["pressure_variant"].eq(BASELINE_VARIANT)
    ]
    price = read_csv("price_wedge_diagnostics_prod.csv")
    price = price.loc[price["model"].eq("pair_its_hac3")].copy()

    group_to_hs = {
        "hs2504_graphite": "2504",
        "hs8110_antimony_metal": "8110",
        "hs8106_bismuth": "8106",
        "hs284180_tungstates": "284180",
    }
    hs_to_pair = {
        "2504": "graphite_gpcnlclw",
        "8110": "antimony_metal",
        "8106": "bismuth_metal",
        "284180": "tungsten_tgeuwoqr",
    }
    rows = []
    for group, hs in group_to_hs.items():
        avg_row = first_value(avg, group, "D")
        ps_row = first_value(source, group, "D_P_S_cap_prod")
        pc_row = first_value(source, group, "D_P_C_cap_prod")
        row_s = first_value(mech, group, "TP_P_S_cap_prod", "row_switch_only")
        total_c = first_value(mech, group, "TP_P_C_cap_prod", "total_compress_only")
        pre_candidates = event.loc[event["group"].eq(group)].copy()
        pre = pd.DataFrame()
        for anchor_choice in [
            BASELINE_ANCHOR,
            "import_effect",
            "implementation",
            "announcement",
        ]:
            candidate = pre_candidates.loc[pre_candidates["anchor"].eq(anchor_choice)]
            if not candidate.empty:
                pre = candidate
                break
        placebo_g = placebo.loc[placebo["group"].eq(group)]
        price_g = price.loc[price["pair_id"].eq(hs_to_pair[hs])]

        avg_coef = np.nan if avg_row is None else avg_row["coef"]
        ps_coef = np.nan if ps_row is None else ps_row["coef"]
        pc_coef = np.nan if pc_row is None else pc_row["coef"]
        row_coef = np.nan if row_s is None else row_s["coef"]
        total_coef = np.nan if total_c is None else total_c["coef"]
        price_coef = np.nan if price_g.empty else price_g.iloc[0]["coef"]

        row_dict = {
            "group": group,
            "hs": hs,
            "product": {
                "2504": "Natural graphite",
                "8110": "Antimony metal",
                "8106": "Bismuth metal",
                "284180": "Tungstates/APT",
            }[hs],
            "average_coef": avg_coef,
            "average_p_value": np.nan if avg_row is None else avg_row["p_value"],
            "average_percent_effect": percent(avg_coef),
            "average_effect_negative": bool(pd.notna(avg_coef) and avg_coef < 0),
            "D_PS_coef": ps_coef,
            "D_PS_p_value": np.nan if ps_row is None else ps_row["p_value"],
            "D_PS_expected_negative": bool(pd.notna(ps_coef) and ps_coef < 0),
            "D_PC_coef": pc_coef,
            "D_PC_p_value": np.nan if pc_row is None else pc_row["p_value"],
            "D_PC_expected_negative": bool(pd.notna(pc_coef) and pc_coef < 0),
            "row_switch_coef": row_coef,
            "row_switch_p_value": np.nan if row_s is None else row_s["p_value"],
            "row_switch_positive": bool(pd.notna(row_coef) and row_coef > 0),
            "total_compression_coef": total_coef,
            "total_compression_p_value": np.nan if total_c is None else total_c["p_value"],
            "total_compression_negative": bool(pd.notna(total_coef) and total_coef < 0),
            "price_wedge_coef": price_coef,
            "price_wedge_p_value": np.nan if price_g.empty else price_g.iloc[0]["p_value"],
            "price_wedge_positive": bool(pd.notna(price_coef) and price_coef > 0),
            "pretrend_p_value": np.nan if pre.empty else pre.iloc[0]["p_value"],
            "pretrend_anchor_used": "" if pre.empty else pre.iloc[0]["anchor"],
            "pretrend_acceptable_p_ge_0_10": False if pre.empty else p_clean(pre.iloc[0]["p_value"]),
            "placebo_problem_any_p_lt_0_05": bool(
                not placebo_g.empty and placebo_g["p_value"].dropna().lt(0.05).any()
            ),
        }
        row_dict["final_classification"] = classify_product(row_dict)
        rows.append(row_dict)
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame, cols: list[str], n: int | None = None) -> str:
    use = df[cols].copy()
    if n is not None:
        use = use.head(n)
    return use.to_markdown(index=False)


def write_theory() -> None:
    text = r"""# Theory

The thesis separates a legal licensing rule from an observed market restriction. A license requirement can bind only for importer-product pairs that were exposed to China and had limited replacement feasibility after the control.

## Exposure

Importer China dependence is measured before the policy announcement:

\[
E_{ip}=\frac{M^C_{ip,pre}}{M^C_{ip,pre}+M^R_{ip,pre}}.
\]

\(M^C_{ip,pre}\) is cumulative pre-announcement imports from China. \(M^R_{ip,pre}\) is cumulative pre-announcement imports from non-China sources. If total pre-policy imports are zero, \(E_{ip}\) is undefined and the importer-product cell is not used for pressure-interaction estimates.

## Access

Importer substitution ability is measured with capacity access:

\[
O^{cap}_{ip}=\min\left(1,\frac{M^R_{ip,pre}}{M^C_{ip,pre}}\right).
\]

The baseline treats prior non-China sourcing capacity as evidence that the importer can redirect some demand away from China. Frequency and binary access measures are kept as robustness checks.

## External Supply Constraint

The production-based product availability measure uses USGS country-level world production data:

\[
A^{prod}_{p}=Scale^{prod}_{p}\times(1-HHI^{ROW,prod}_{p}).
\]

The scale term is:

\[
Scale^{prod}_{p}=\min\left(1,\frac{ROW\ production_p}{China\ production_p}\right).
\]

The concentration term is the Herfindahl index among non-China producers:

\[
HHI^{ROW,prod}_{p}=\sum_{c\neq China}s_{cp}^{2}.
\]

This makes \(A^{prod}_{p}\) high only when non-China production is large relative to China and is not concentrated in one or two suppliers.

## Replacement Feasibility

Importer-level replacement feasibility combines importer access and product-level external supply:

\[
K_{ip}=O_{ip}\times A^{prod}_{p}.
\]

High \(K_{ip}\) means the importer had non-China access and the product has a larger, more diversified non-China production base.

## Decomposition

Exposed China demand is decomposed into switchable and non-switchable components:

\[
P^S_{ip}=E_{ip}\times K_{ip},
\]

\[
P^C_{ip}=E_{ip}\times(1-K_{ip}),
\]

\[
P^X_{ip}=E_{ip}.
\]

\(P^S_{ip}\) is switchable exposed demand. It should predict a China-source decline and a rise in RoW imports. \(P^C_{ip}\) is non-switchable exposed demand. It should predict a China-source decline, weaker RoW replacement, total import compression, or price segmentation.

## Edge Cases

Cells with no pre-policy imports have undefined exposure. Cells with China pre-policy imports but no RoW imports have zero capacity access. Cells with RoW pre-policy imports but no China imports have no China exposure, so they do not create China-exposure pressure. Production values use world totals for scale when available. HHI uses listed non-China country rows plus a residual supplier if the world total implies unlisted production.
"""
    (OUT / "THEORY.md").write_text(text, encoding="utf-8")


def write_final_interpretation(table: pd.DataFrame) -> None:
    lines = [
        "# Final Interpretation",
        "",
        "This report does not rank results by statistical significance alone. The interpretation uses sign consistency, timing, placebo behavior, mechanism coherence, and price evidence.",
        "",
        "## Product Classification",
        "",
        md_table(
            table,
            [
                "product",
                "hs",
                "average_percent_effect",
                "average_p_value",
                "row_switch_coef",
                "total_compression_coef",
                "price_wedge_coef",
                "pretrend_p_value",
                "pretrend_anchor_used",
                "placebo_problem_any_p_lt_0_05",
                "final_classification",
            ],
        ),
        "",
    ]
    for _, row in table.iterrows():
        lines.extend(
            [
                f"## {row['product']} ({row['hs']})",
                "",
                f"Average China-source effect: {row['average_percent_effect']:.1f}% with p-value {row['average_p_value']:.4g}.",
                f"Switching evidence: RoW switching coefficient {row['row_switch_coef']:.3g}, p-value {row['row_switch_p_value']:.4g}.",
                f"Compression evidence: total-import compression coefficient {row['total_compression_coef']:.3g}, p-value {row['total_compression_p_value']:.4g}.",
                f"Price wedge evidence: coefficient {row['price_wedge_coef']:.3g}, p-value {row['price_wedge_p_value']:.4g}.",
                f"Timing and placebo: pretrend p-value {row['pretrend_p_value']:.4g} using {row['pretrend_anchor_used']}; placebo problem flag is {row['placebo_problem_any_p_lt_0_05']}.",
                f"Classification: {row['final_classification']}.",
                "",
            ]
        )
    (OUT / "FINAL_INTERPRETATION.md").write_text("\n".join(lines), encoding="utf-8")


def write_thesis_summary(table: pd.DataFrame) -> None:
    counts = table["final_classification"].value_counts().to_dict()
    product_line = "; ".join(
        f"{r.product}: {r.final_classification}" for r in table.itertuples(index=False)
    )
    lines = [
        "# THESIS SUMMARY (1 PAGE)",
        "",
        "The thesis studies when Chinese critical-mineral export licensing controls bind in international trade. The main contribution is a production-based pressure framework that combines importer China exposure, importer outside access, and external non-China production availability. This moves the empirical question away from a simple average effect and toward the mechanism behind heterogeneous trade responses.",
        "",
        r"The framework decomposes exposed China demand into switchable and non-switchable parts. Switchable pressure, \(P^S=E\times K\), should appear as a China-source decline with RoW replacement. Compression pressure, \(P^C=E\times(1-K)\), should appear as a China-source decline with weak RoW replacement, total import compression, or price segmentation.",
        "",
        "The preferred quarterly PPML results show a negative average China-source effect for the pooled clean sample, graphite, antimony metal, bismuth, and the wave 4 W/Bi group. Tungstates/APT have a negative but weak average estimate. The pooled pressure model gives negative coefficients for both switchable and compression pressure. Product-level pressure evidence is more uneven, so interpretation should rely on the full pattern rather than one coefficient.",
        "",
        "Mechanism ranking in the current evidence is: switching first, price segmentation second, compression third. RoW switching coefficients are often positive, especially for graphite and antimony. Price wedges are positive for several clean treated products, especially antimony and bismuth. Total-import compression is less consistent and should be interpreted cautiously.",
        "",
        f"Product classification: {product_line}.",
        "",
        f"Classification counts: {counts}.",
        "",
        "Final research answer: Chinese critical-mineral export licensing controls do not bind mechanically. They bind most clearly when importers were exposed to China and the product has limited non-China replacement capacity. The observed margin is not always import collapse. In several cases, the evidence is more consistent with source switching or price segmentation than with pure compression.",
    ]
    (OUT / "THESIS_SUMMARY_1_PAGE.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme() -> None:
    lines = [
        "# Full Thesis Report Outputs",
        "",
        "This folder consolidates the production-based pressure-index empirical pipeline.",
        "",
        "- `THEORY.md`: model and pressure-index logic.",
        "- `DATA_AUDIT.csv`: USGS production mapping and policy metadata.",
        "- `SUMMARY_STATS.csv`: pressure-index descriptive statistics and correlations.",
        "- `MAIN_RESULTS.csv`: baseline PPML, exposure, pressure, and E-K models.",
        "- `MECHANISMS.csv`: RoW and total-import mechanism models.",
        "- `EVENT_STUDY.csv`: source-contrast, pressure-gradient, China, RoW, and total-import timing diagnostics.",
        "- `PLACEBO.csv`: -12, -24, and -36 month placebo tests.",
        "- `ROBUSTNESS.csv`: monthly, net-weight, U.S., 2024 A, and trade-A comparison checks.",
        "- `PRICE_WEDGES.csv`: ITS and panel price-wedge diagnostics.",
        "- `FINAL_INTERPRETATION.md`: product-by-product classification.",
        "- `THESIS_SUMMARY_1_PAGE.md`: one-page thesis answer.",
    ]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_report_build_warnings() -> None:
    lines = ["# Report Build Warnings", ""]
    event_path = OUT / "EVENT_STUDY_MECHANISMS.csv"
    if event_path.exists():
        event = pd.read_csv(event_path)
        groups = set(event["group"].dropna().astype(str))
        if "pooled_clean" not in groups:
            lines.append(
                "- Wide-panel China/RoW/total event studies do not include pooled-clean rows. "
                "The pooled wide event-study PPML fits failed with singular covariance matrices. "
                "Product and wave-level wide event-study rows are available."
            )
        missing_first_full = []
        for group in ["wave4_w_bi", "hs8106_bismuth", "hs284180_tungstates"]:
            sub = event.loc[
                event["group"].eq(group)
                & event["anchor"].eq(BASELINE_ANCHOR)
                & event["row_type"].eq("coefficient")
            ]
            if sub.empty:
                missing_first_full.append(group)
        if missing_first_full:
            lines.append(
                "- First-full-post-quarter wide event-study rows are missing for "
                + ", ".join(missing_first_full)
                + " because the last event bin has no variation."
            )
    else:
        lines.append("- `EVENT_STUDY_MECHANISMS.csv` was not found.")
    lines.append(
        "- Main production-A warnings remain in `MODEL_WARNINGS.txt`, including PPML separation, "
        "missing treated pressure cells, and source-contrast event-study failures."
    )
    (OUT / "REPORT_BUILD_WARNINGS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    write_theory()

    data_audit = build_data_audit()
    write_csv(data_audit, "DATA_AUDIT.csv")
    read_csv("production_country_rows_used.csv").to_csv(
        OUT / "production_country_rows_used.csv", index=False
    )
    read_csv("product_sample_table.csv").to_csv(OUT / "production_mapping.csv", index=False)

    write_csv(build_summary_stats(), "SUMMARY_STATS.csv")
    write_csv(read_csv("pressure_index_by_product_prod.csv"), "SUMMARY_STATS_BY_PRODUCT.csv")
    write_csv(read_csv("pressure_indices_prod_importer_product.csv"), "PRESSURE_INDEX_IMPORTER_PRODUCT.csv")

    write_csv(build_main_results(), "MAIN_RESULTS.csv")
    write_csv(build_mechanisms(), "MECHANISMS.csv")
    write_csv(build_event_study(), "EVENT_STUDY.csv")
    write_csv(build_placebos(), "PLACEBO.csv")
    write_csv(build_robustness(), "ROBUSTNESS.csv")
    write_csv(read_csv("price_wedge_diagnostics_prod.csv"), "PRICE_WEDGES.csv")

    interpretation = build_interpretation_table()
    write_csv(interpretation, "PRODUCT_CLASSIFICATION.csv")
    write_final_interpretation(interpretation)
    write_thesis_summary(interpretation)
    write_readme()
    write_report_build_warnings()

    warnings = SOURCE / "model_failures_and_warnings_prod.txt"
    if warnings.exists():
        base_warnings = warnings.read_text(encoding="utf-8")
    else:
        base_warnings = ""
    extra_warnings = "\n".join(prod.warnings_log)
    (OUT / "MODEL_WARNINGS.txt").write_text(
        base_warnings
        + ("\n\n# Full report builder warnings\n" if extra_warnings else "")
        + extra_warnings,
        encoding="utf-8",
    )

    print(f"Full thesis report written to {OUT}")


if __name__ == "__main__":
    main()
