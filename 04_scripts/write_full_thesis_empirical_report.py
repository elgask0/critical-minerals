#!/usr/bin/env python3
"""Write the consolidated thesis empirical Markdown report from existing outputs."""

from __future__ import annotations

from pathlib import Path
import math
import re

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "results" / "full_thesis_report"
FULL_OUT = BASE / "FULL_THESIS_EMPIRICAL_REPORT.md"
SHORT_OUT = BASE / "FULL_THESIS_EMPIRICAL_REPORT_SHORT.md"

REQUIRED = [
    "THEORY.md",
    "DATA_AUDIT.csv",
    "SUMMARY_STATS.csv",
    "SUMMARY_STATS_BY_PRODUCT.csv",
    "MAIN_RESULTS.csv",
    "MECHANISMS.csv",
    "EVENT_STUDY.csv",
    "PLACEBO.csv",
    "ROBUSTNESS.csv",
    "PRICE_WEDGES.csv",
    "FINAL_INTERPRETATION.md",
    "THESIS_SUMMARY_1_PAGE.md",
    "REPORT_BUILD_WARNINGS.md",
    "MODEL_WARNINGS.txt",
    "README.md",
]

GROUP_ORDER = [
    "pooled_clean",
    "wave4_w_bi",
    "hs2504_graphite",
    "hs8110_antimony_metal",
    "hs8106_bismuth",
    "hs284180_tungstates",
]

PRODUCT_GROUPS = [
    "hs2504_graphite",
    "hs8110_antimony_metal",
    "hs8106_bismuth",
    "hs284180_tungstates",
]

GROUP_LABELS = {
    "pooled_clean": "Pooled clean",
    "wave2_graphite": "Wave 2 graphite",
    "wave3_antimony_clean": "Wave 3 antimony",
    "wave4_w_bi": "Wave 4 W/Bi",
    "hs2504_graphite": "Natural graphite",
    "hs8110_antimony_metal": "Antimony metal",
    "hs8106_bismuth": "Bismuth metal",
    "hs284180_tungstates": "Tungstates/APT",
}

STRICT_CLASSIFICATION = {
    "hs2504_graphite": "mixed switching/compression quantity mechanism",
    "hs8110_antimony_metal": "strong disruption with switching and price segmentation; timing caveat",
    "hs8106_bismuth": "strong disruption with price segmentation; weaker quantity mechanism",
    "hs284180_tungstates": "weak/null or unresolved",
}


def load(name: str) -> pd.DataFrame:
    path = BASE / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_text(name: str) -> str:
    path = BASE / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def fmt_num(x: object, digits: int = 3) -> str:
    try:
        val = float(x)
    except Exception:
        return ""
    if not math.isfinite(val):
        return ""
    return f"{val:.{digits}f}"


def fmt_pct(x: object) -> str:
    try:
        val = float(x)
    except Exception:
        return ""
    if not math.isfinite(val):
        return ""
    return f"{val:.1f}%"


def fmt_p(x: object) -> str:
    try:
        val = float(x)
    except Exception:
        return ""
    if not math.isfinite(val):
        return ""
    if val < 0.001 and val > 0:
        return f"{val:.2e}"
    return f"{val:.3f}"


def yes_no(value: object) -> str:
    return "Yes" if bool(value) else "No"


def md_table(rows: list[dict], headers: list[str]) -> str:
    if not rows:
        return "_No table could be produced from the available outputs._"
    labels = headers
    data = [[str(row.get(h, "")) for h in headers] for row in rows]
    widths = [
        max(len(labels[i]), *(len(row[i]) for row in data))
        for i in range(len(labels))
    ]
    header = "| " + " | ".join(labels[i].ljust(widths[i]) for i in range(len(labels))) + " |"
    sep = "| " + " | ".join("-" * widths[i] for i in range(len(labels))) + " |"
    body = [
        "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(labels))) + " |"
        for row in data
    ]
    return "\n".join([header, sep, *body])


def file_inventory() -> tuple[list[str], dict[str, pd.DataFrame], dict[str, str]]:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    csvs = {
        "data": load("DATA_AUDIT.csv"),
        "summary": load("SUMMARY_STATS.csv"),
        "summary_product": load("SUMMARY_STATS_BY_PRODUCT.csv"),
        "main": load("MAIN_RESULTS.csv"),
        "mechanisms": load("MECHANISMS.csv"),
        "event": load("EVENT_STUDY.csv"),
        "placebo": load("PLACEBO.csv"),
        "robustness": load("ROBUSTNESS.csv"),
        "price": load("PRICE_WEDGES.csv"),
        "classification": load("PRODUCT_CLASSIFICATION.csv"),
        "mapping": load("production_mapping.csv"),
    }
    texts = {
        "theory": read_text("THEORY.md"),
        "final": read_text("FINAL_INTERPRETATION.md"),
        "summary": read_text("THESIS_SUMMARY_1_PAGE.md"),
        "build_warnings": read_text("REPORT_BUILD_WARNINGS.md"),
        "model_warnings": read_text("MODEL_WARNINGS.txt"),
    }
    return missing, csvs, texts


def baseline(df: pd.DataFrame, module: str | None = None) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if module is not None and "report_module" in out:
        out = out[out["report_module"].eq(module)]
    for col, val in [
        ("frequency", "quarterly"),
        ("anchor", "first_full_post_quarter"),
    ]:
        if col in out:
            out = out[out[col].eq(val)]
    return out


def row_for(df: pd.DataFrame, group: str, term: str, module: str | None = None, model: str | None = None) -> pd.Series | None:
    if df.empty:
        return None
    sub = df[df["group"].eq(group) & df["term"].eq(term)].copy()
    if module is not None and "report_module" in sub:
        sub = sub[sub["report_module"].eq(module)]
    if model is not None and "model" in sub:
        sub = sub[sub["model"].eq(model)]
    if sub.empty:
        return None
    return sub.iloc[0]


def display_result(row: pd.Series | None, prefix: str = "") -> dict:
    if row is None:
        return {
            f"{prefix}coef": "",
            f"{prefix}p-value": "",
            f"{prefix}effect": "",
            f"{prefix}n used": "",
            f"{prefix}dropped": "",
        }
    return {
        f"{prefix}coef": fmt_num(row.get("coef")),
        f"{prefix}p-value": fmt_p(row.get("p_value")),
        f"{prefix}effect": fmt_pct(row.get("percent_effect", row.get("percent_change"))),
        f"{prefix}n used": str(int(row.get("n_used"))) if pd.notna(row.get("n_used", np.nan)) else "",
        f"{prefix}dropped": str(int(row.get("n_dropped_separation"))) if pd.notna(row.get("n_dropped_separation", np.nan)) else "",
    }


def production_table(data: pd.DataFrame) -> list[dict]:
    if data.empty:
        return []
    base23 = data[data["year"].eq(2023)].copy()
    base24 = data[data["year"].eq(2024)][["hs", "A_prod"]].rename(columns={"A_prod": "A_prod_2024"})
    merged = base23.merge(base24, on="hs", how="left")
    rows = []
    for _, r in merged.iterrows():
        rows.append(
            {
                "Product": clean_product(r["product_name"]),
                "HS": str(r["hs"]),
                "USGS commodity": r["usgs_commodity"],
                "USGS production type": r["usgs_type"],
                "China prod. 2023": fmt_num(r["china_production"], 0),
                "World total 2023": fmt_num(r["world_total"], 0),
                "A_prod 2023": fmt_num(r["A_prod"]),
                "A_prod 2024": fmt_num(r["A_prod_2024"]),
                "Caveat": short_caveat(str(r.get("notes", ""))),
            }
        )
    return rows


def clean_product(value: object) -> str:
    text = str(value)
    return {
        "Antimony metal and articles": "Antimony metal",
        "Tungstates and APT": "Tungstates/APT",
    }.get(text, text)


def short_caveat(notes: str) -> str:
    if "Good direct proxy" in notes:
        return "Direct proxy."
    if "Upstream proxy" in notes:
        return "Upstream proxy."
    if "Best available" in notes:
        return "Best available match."
    return notes[:80]


def policy_table(mapping: pd.DataFrame) -> list[dict]:
    if mapping.empty:
        return []
    treated = mapping[mapping["analysis_role"].eq("main_clean_treated")].copy()
    treated = treated.sort_values(["wave", "hs"])
    rows = []
    for _, r in treated.iterrows():
        rows.append(
            {
                "HS code": str(r["hs"]),
                "Product": clean_product(r["product_name"]),
                "Wave": str(int(r["wave"])) if pd.notna(r["wave"]) else "",
                "Announcement": str(r["announcement_date"]),
                "Implementation": str(r["implementation_date"]),
                "Import-effect month": str(r["import_effect_month"]),
                "Status": str(r["scope_status"]),
                "Role": str(r["analysis_role"]),
            }
        )
    return rows


def pooled_stats(summary: pd.DataFrame) -> list[dict]:
    if summary.empty:
        return []
    var_map = {
        "E_china": "E",
        "O_cap": "O_cap",
        "A_prod_2023": "A_prod",
        "K_cap_prod": "K",
        "P_S_cap_prod": "P_S",
        "P_C_cap_prod": "P_C",
    }
    sub = summary[
        summary["group"].eq("pooled_clean_treated")
        & summary["stat_type"].eq("distribution")
        & summary["variable"].isin(var_map)
    ].copy()
    rows = []
    for variable in var_map:
        r = sub[sub["variable"].eq(variable)]
        if r.empty:
            continue
        s = r.iloc[0]
        rows.append(
            {
                "Variable": var_map[variable],
                "Mean": fmt_num(s["mean"]),
                "SD": fmt_num(s["sd"]),
                "Min": fmt_num(s["min"]),
                "P25": fmt_num(s["p25"]),
                "Median": fmt_num(s["median"]),
                "P75": fmt_num(s["p75"]),
                "Max": fmt_num(s["max"]),
            }
        )
    return rows


def product_pressure_table(summary_product: pd.DataFrame) -> list[dict]:
    if summary_product.empty:
        return []
    rows = []
    for _, r in summary_product.iterrows():
        rows.append(
            {
                "Product": clean_product(r["product"]),
                "HS": str(r["hs"]),
                "N": str(int(r["n_cells"])),
                "Mean E": fmt_num(r["mean_E_china"]),
                "Mean O": fmt_num(r["mean_O_cap"]),
                "A_prod": fmt_num(r["mean_A_prod_2023"]),
                "Mean K": fmt_num(r["mean_K_cap_prod"]),
                "Mean P_S": fmt_num(r["mean_P_S_cap_prod"]),
                "Mean P_C": fmt_num(r["mean_P_C_cap_prod"]),
            }
        )
    return rows


def correlation_table(summary: pd.DataFrame, summary_product: pd.DataFrame) -> list[dict]:
    rows = []
    if not summary.empty:
        corr = summary[
            summary["group"].eq("pooled_clean_treated")
            & summary["stat_type"].eq("correlation")
        ]

        def corr_val(left: str, right: str) -> str:
            a = corr[corr["product"].eq(left) & corr["variable"].eq(right)]
            b = corr[corr["product"].eq(right) & corr["variable"].eq(left)]
            use = a if not a.empty else b
            if use.empty:
                return ""
            return fmt_num(use.iloc[0]["mean"])

        rows.append(
            {
                "Product/group": "Pooled clean",
                "Corr(E,K)": corr_val("E_china", "K_cap_prod"),
                "Corr(P_S,P_C)": corr_val("P_S_cap_prod", "P_C_cap_prod"),
                "Corr(E,P_S)": corr_val("E_china", "P_S_cap_prod"),
                "Corr(E,P_C)": corr_val("E_china", "P_C_cap_prod"),
                "Corr(K,P_C)": corr_val("K_cap_prod", "P_C_cap_prod"),
            }
        )
    if not summary_product.empty:
        for _, r in summary_product.iterrows():
            rows.append(
                {
                    "Product/group": clean_product(r["product"]),
                    "Corr(E,K)": fmt_num(r["corr_E_K_cap_prod"]),
                    "Corr(P_S,P_C)": fmt_num(r["corr_PS_PC_cap_prod"]),
                    "Corr(E,P_S)": fmt_num(r["corr_PS_E_cap_prod"]),
                    "Corr(E,P_C)": fmt_num(r["corr_PC_E_cap_prod"]),
                    "Corr(K,P_C)": fmt_num(r["corr_K_PC_cap_prod"]),
                }
            )
    return rows


def main_average_table(main: pd.DataFrame) -> list[dict]:
    sub = baseline(main, "baseline_ppml_quarterly")
    rows = []
    for group in GROUP_ORDER:
        r = row_for(sub, group, "D")
        if r is None:
            continue
        d = display_result(r)
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                "coef": d["coef"],
                "p-value": d["p-value"],
                "percent effect": d["effect"],
                "n used": d["n used"],
                "separation dropped": d["dropped"],
            }
        )
    return rows


def exposure_table(main: pd.DataFrame) -> list[dict]:
    sub = baseline(main, "exposure_quarterly")
    rows = []
    for group in GROUP_ORDER:
        r = row_for(sub, group, "D_E_china")
        if r is None:
            continue
        sign = "negative" if r["coef"] < 0 else "positive"
        interp = "Higher China exposure predicts stronger China-source decline." if r["coef"] < 0 else "Wrong-signed for the exposure prediction."
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                "D x E coef": fmt_num(r["coef"]),
                "p-value": fmt_p(r["p_value"]),
                "sign": sign,
                "interpretation": interp,
            }
        )
    return rows


def pressure_table(main: pd.DataFrame) -> list[dict]:
    sub = baseline(main, "mechanism_source_quarterly")
    sub = sub[sub["pressure_variant"].eq("capacity")]
    rows = []
    for group in GROUP_ORDER:
        ps = row_for(sub, group, "D_P_S_cap_prod")
        pc = row_for(sub, group, "D_P_C_cap_prod")
        if ps is None and pc is None:
            continue
        interpretation = []
        if ps is not None:
            interpretation.append("P_S sign fits" if ps["coef"] < 0 else "P_S wrong-signed")
        if pc is not None:
            interpretation.append("P_C sign fits" if pc["coef"] < 0 else "P_C wrong-signed")
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                "D x P_S coef": fmt_num(None if ps is None else ps["coef"]),
                "P_S p-value": fmt_p(None if ps is None else ps["p_value"]),
                "D x P_C coef": fmt_num(None if pc is None else pc["coef"]),
                "P_C p-value": fmt_p(None if pc is None else pc["p_value"]),
                "interpretation": "; ".join(interpretation),
            }
        )
    return rows


def mechanism_rows(mech: pd.DataFrame, kind: str) -> list[dict]:
    if mech.empty:
        return []
    if kind == "row":
        sub = baseline(mech, "row_quarterly")
        sub = sub[
            sub["pressure_variant"].eq("capacity")
            & sub["model"].eq("row_switch_only")
            & sub["term"].eq("TP_P_S_cap_prod")
        ]
        coef_name = "RoW P_S coef"
        expectation = "positive"
    else:
        sub = baseline(mech, "total_quarterly")
        sub = sub[
            sub["pressure_variant"].eq("capacity")
            & sub["model"].eq("total_compress_only")
            & sub["term"].eq("TP_P_C_cap_prod")
        ]
        coef_name = "Total P_C coef"
        expectation = "negative"
    rows = []
    for group in GROUP_ORDER:
        r = sub[sub["group"].eq(group)]
        if r.empty:
            continue
        s = r.iloc[0]
        if kind == "row":
            interpretation = "supports switching" if s["coef"] > 0 else "does not support switching"
        else:
            interpretation = "supports compression" if s["coef"] < 0 else "does not support compression"
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                coef_name: fmt_num(s["coef"]),
                "p-value": fmt_p(s["p_value"]),
                "expected sign": expectation,
                "interpretation": interpretation,
            }
        )
    return rows


def event_table(event: pd.DataFrame) -> list[dict]:
    if event.empty:
        return []
    sub = event[
        event["frequency"].eq("quarterly")
        & event["model"].eq("average_event_study")
        & event["row_type"].eq("joint_pretrend")
    ].copy()
    anchor_pref = {
        "pooled_clean": "first_full_post_quarter",
        "wave4_w_bi": "import_effect",
        "hs2504_graphite": "first_full_post_quarter",
        "hs8110_antimony_metal": "first_full_post_quarter",
        "hs8106_bismuth": "import_effect",
        "hs284180_tungstates": "import_effect",
    }
    rows = []
    for group in GROUP_ORDER:
        anchor = anchor_pref[group]
        r = sub[sub["group"].eq(group) & sub["anchor"].eq(anchor)]
        if r.empty:
            continue
        s = r.iloc[0]
        ok = float(s["p_value"]) >= 0.10
        if group == "hs8110_antimony_metal":
            comment = "borderline; use caution"
        elif group == "hs284180_tungstates":
            comment = "problematic pretrends"
        elif ok:
            comment = "acceptable"
        else:
            comment = "problematic"
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                "anchor": anchor,
                "joint pretrend p-value": fmt_p(s["p_value"]),
                "acceptable?": "Yes" if ok else "No",
                "comment": comment,
            }
        )
    return rows


def placebo_table(placebo: pd.DataFrame) -> list[dict]:
    if placebo.empty:
        return []
    sub = placebo[
        placebo["frequency"].eq("quarterly")
        & placebo["anchor"].eq("first_full_post_quarter")
        & placebo["pressure_variant"].isin(["capacity", "none", "exposure"])
    ].copy()
    rows = []
    for group in GROUP_ORDER:
        g = sub[sub["group"].eq(group)].copy()
        if g.empty:
            continue
        g["abs_t"] = (g["coef"] / g["se"]).abs()
        strongest = g.sort_values("p_value", na_position="last").iloc[0]
        issue = bool(g["p_value"].dropna().lt(0.05).any())
        interpretation = "clean enough for a placebo diagnostic" if not issue else "placebo caution; do not treat timing as clean"
        rows.append(
            {
                "Product/group": GROUP_LABELS[group],
                "placebo issue?": "Yes" if issue else "No",
                "strongest placebo problem": f"{int(strongest['placebo_lag_months'])}m, {strongest['term']}, coef {fmt_num(strongest['coef'])}, p {fmt_p(strongest['p_value'])}",
                "interpretation": interpretation,
            }
        )
    return rows


def price_table(price: pd.DataFrame) -> list[dict]:
    if price.empty:
        return []
    sub = price[price["model"].eq("pair_its_hac3")].copy()
    rows = []
    for _, r in sub.iterrows():
        if pd.isna(r.get("pair_id")):
            continue
        coef = r["coef"]
        if r["role"] == "partial_treated":
            interp = "supportive outside clean baseline" if coef > 0 else "partial product; weak support"
        elif coef > 0:
            interp = "segmentation/scarcity diagnostic"
        else:
            interp = "no positive segmentation support"
        rows.append(
            {
                "Product": str(r["family"]),
                "HS": "" if pd.isna(r["hs"]) else str(int(float(r["hs"]))),
                "coef": fmt_num(r["coef"]),
                "p-value": fmt_p(r["p_value"]),
                "percent change": fmt_pct(r["percent_change"]),
                "interpretation": interp,
            }
        )
    return rows


def price_panel_table(price: pd.DataFrame) -> list[dict]:
    if price.empty or "sample" not in price:
        return []
    sub = price[price["sample"].notna()].copy()
    rows = []
    for _, r in sub.iterrows():
        rows.append(
            {
                "Sample": str(r["sample"]),
                "coef": fmt_num(r["coef"]),
                "HC1 p-value": fmt_p(r.get("p_hc1")),
                "pair-cluster p-value": fmt_p(r.get("p_pair_cluster")),
                "percent change": fmt_pct(r["percent_change"]),
            }
        )
    return rows


def robustness_tables(rob: pd.DataFrame, main: pd.DataFrame) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    monthly = baseline(main, "baseline_ppml_monthly")
    out["monthly"] = []
    for group in PRODUCT_GROUPS:
        q = row_for(baseline(main, "baseline_ppml_quarterly"), group, "D")
        m = row_for(monthly, group, "D")
        out["monthly"].append(
            {
                "Product": GROUP_LABELS[group],
                "quarterly effect": fmt_pct(None if q is None else q["percent_effect"]),
                "monthly effect": fmt_pct(None if m is None else m["percent_effect"]),
                "monthly p-value": fmt_p(None if m is None else m["p_value"]),
                "summary": "same sign" if q is not None and m is not None and np.sign(q["coef"]) == np.sign(m["coef"]) else "sign differs or unavailable",
            }
        )

    net = rob[
        rob["report_module"].eq("net_weight")
        & rob["frequency"].eq("quarterly")
        & rob["anchor"].eq("first_full_post_quarter")
        & rob["model"].eq("average_source_contrast")
        & rob["term"].eq("D")
    ] if not rob.empty else pd.DataFrame()
    out["net"] = []
    for group in PRODUCT_GROUPS:
        r = net[net["group"].eq(group)]
        if r.empty:
            continue
        s = r.iloc[0]
        out["net"].append(
            {
                "Product": GROUP_LABELS[group],
                "net-weight coef": fmt_num(s["coef"]),
                "p-value": fmt_p(s["p_value"]),
                "percent effect": fmt_pct(s["percent_effect"]),
                "interpretation": "same negative direction" if s["coef"] < 0 else "does not confirm value decline",
            }
        )

    us = rob[
        rob["report_module"].eq("us_excluded_quarterly")
        & rob["frequency"].eq("quarterly")
        & rob["anchor"].eq("first_full_post_quarter")
        & rob["model"].eq("average_source_contrast")
        & rob["term"].eq("D")
    ] if not rob.empty else pd.DataFrame()
    out["us"] = []
    for group in GROUP_ORDER:
        r = us[us["group"].eq(group)]
        if r.empty:
            continue
        s = r.iloc[0]
        out["us"].append(
            {
                "Product/group": GROUP_LABELS[group],
                "US-excluded coef": fmt_num(s["coef"]),
                "p-value": fmt_p(s["p_value"]),
                "percent effect": fmt_pct(s["percent_effect"]),
                "interpretation": "result remains negative" if s["coef"] < 0 else "US exclusion weakens sign",
            }
        )

    src = baseline(main, "mechanism_source_quarterly")
    access_rows = []
    for variant in ["capacity", "frequency", "binary", "capacity_2024"]:
        v = src[src["pressure_variant"].eq(variant)]
        ps = v[v["term"].str.contains("P_S", na=False) & v["group"].isin(PRODUCT_GROUPS)]
        pc = v[v["term"].str.contains("P_C", na=False) & v["group"].isin(PRODUCT_GROUPS)]
        access_rows.append(
            {
                "variant": variant,
                "P_S expected signs": f"{int((ps['coef'] < 0).sum())}/{len(ps)}",
                "P_C expected signs": f"{int((pc['coef'] < 0).sum())}/{len(pc)}",
                "pooled P_S coef": fmt_num(row_for(v, "pooled_clean", next((t for t in v[v['group'].eq('pooled_clean')]['term'] if "P_S" in t), ""))["coef"]) if not v[v["group"].eq("pooled_clean") & v["term"].str.contains("P_S", na=False)].empty else "",
                "pooled P_C coef": fmt_num(row_for(v, "pooled_clean", next((t for t in v[v['group'].eq('pooled_clean')]['term'] if "P_C" in t), ""))["coef"]) if not v[v["group"].eq("pooled_clean") & v["term"].str.contains("P_C", na=False)].empty else "",
            }
        )
    out["access"] = access_rows

    comp = rob[rob["report_module"].eq("tradeA_vs_prodA")] if not rob.empty else pd.DataFrame()
    out["trade_prod"] = []
    if not comp.empty:
        for _, r in comp[comp["group"].isin(["pooled_clean", *PRODUCT_GROUPS])].head(12).iterrows():
            out["trade_prod"].append(
                {
                    "Product/group": GROUP_LABELS.get(r["group"], r["group"]),
                    "term": str(r["comparison_term"]),
                    "trade-A coef": fmt_num(r["tradeA_coef"]),
                    "prod-A coef": fmt_num(r["prodA_coef"]),
                    "prod-A p-value": fmt_p(r["prodA_p_value"]),
                }
            )
    return out


def product_interpretation_rows(cls: pd.DataFrame) -> list[dict]:
    if cls.empty:
        return []
    rows = []
    for group in PRODUCT_GROUPS:
        r = cls[cls["group"].eq(group)]
        if r.empty:
            continue
        s = r.iloc[0]
        rows.append(
            {
                "Product": s["product"],
                "Average effect": f"{fmt_pct(s['average_percent_effect'])} (p {fmt_p(s['average_p_value'])})",
                "Switching": f"{fmt_num(s['row_switch_coef'])} (p {fmt_p(s['row_switch_p_value'])})",
                "Compression": f"{fmt_num(s['total_compression_coef'])} (p {fmt_p(s['total_compression_p_value'])})",
                "Price wedge": f"{fmt_num(s['price_wedge_coef'])} (p {fmt_p(s['price_wedge_p_value'])})",
                "Timing validity": "acceptable" if s["pretrend_acceptable_p_ge_0_10"] else "caution",
                "Final classification": STRICT_CLASSIFICATION[group],
            }
        )
    return rows


def warnings_summary(model_warnings: str) -> list[dict]:
    if not model_warnings:
        return []
    patterns = {
        "missing pressure or exposure cells": r"dropping .* missing",
        "PPML event/model failures": r"PPML .* failed",
        "no-variation event terms": r"no variation|skipped",
        "demeaning failures": r"Demeaning failed",
        "edge-case logs": r"pressure edge case",
    }
    rows = []
    for label, pattern in patterns.items():
        rows.append({"Warning type": label, "count": str(len(re.findall(pattern, model_warnings)))})
    return rows


def reviewer_attacks() -> list[dict]:
    return [
        {"Attack": "You do not observe license applications or approvals.", "Severity": "High", "Response": "State that the design estimates observed market responses, not denial probabilities or administrative processing."},
        {"Attack": "Production is not tradable spare capacity.", "Severity": "High", "Response": "Treat A_prod as external availability, not marginal capacity. Keep price and trade mechanisms as diagnostics."},
        {"Attack": "HS codes do not perfectly match controlled items.", "Severity": "High", "Response": "Keep the clean HS sample as baseline and move bundled products to secondary analysis."},
        {"Attack": "Antimony has placebo problems.", "Severity": "High", "Response": "Report the issue directly. Interpret antimony as strong disruption with timing caveat, not clean causal timing."},
        {"Attack": "Tungsten is weak.", "Severity": "High", "Response": "Classify tungstates/APT as weak or unresolved rather than forcing a mechanism."},
        {"Attack": "Pooled pretrends fail.", "Severity": "High", "Response": "Use pooled estimates as summary evidence only. Product-level interpretation carries the thesis claim."},
        {"Attack": "Price wedges are not causal.", "Severity": "Medium", "Response": "Label price wedges as segmentation/scarcity diagnostics, not a causal estimate of licensing."},
        {"Attack": "Pressure indexes still use trade data for E and O.", "Severity": "Medium", "Response": "E and O are importer behavior primitives. A_prod is the external product-level component."},
        {"Attack": "PPML separation may affect estimates.", "Severity": "Medium", "Response": "Report dropped observations and use robustness checks rather than hiding separation."},
    ]


def build_full_report() -> str:
    missing, csv, texts = file_inventory()
    data = csv["data"]
    main = csv["main"]
    mechanisms = csv["mechanisms"]
    event = csv["event"]
    placebo = csv["placebo"]
    robustness = csv["robustness"]
    price = csv["price"]
    classification = csv["classification"]
    summary = csv["summary"]
    summary_product = csv["summary_product"]
    mapping = csv["mapping"]

    main_table = main_average_table(main)
    exp_table = exposure_table(main)
    press_table = pressure_table(main)
    row_switch = mechanism_rows(mechanisms, "row")
    total_comp = mechanism_rows(mechanisms, "total")
    evt_table = event_table(event)
    plac_table = placebo_table(placebo)
    price_rows = price_table(price)
    price_panel = price_panel_table(price)
    rob_tables = robustness_tables(robustness, main)
    interp_rows = product_interpretation_rows(classification)

    lines: list[str] = []
    add = lines.append
    add("# FULL THESIS EMPIRICAL REPORT")
    add("")
    add("## Executive Summary")
    add("")
    add("This report asks when Chinese critical-mineral export licensing controls bind in international trade. The revised contribution is not the average claim that export restrictions reduce trade. It is a mechanism test: licensing binds when pre-policy China exposure meets limited replacement feasibility. Replacement feasibility combines importer outside access with external non-China production availability from USGS data. The preferred quarterly PPML estimates show a negative China-source effect for the pooled clean sample, graphite, antimony metal, bismuth, and the wave 4 W/Bi group. The mechanism evidence ranks switching first, price segmentation second, and total-import compression third. Strict product classifications are: graphite as a mixed switching/compression quantity case; antimony as strong disruption with switching and price segmentation but timing caveats; bismuth as strong disruption with price segmentation and weaker quantity mechanisms; and tungstates/APT as weak, null, or unresolved. The safe thesis claim is that licensing controls do not bind mechanically. They bind most clearly where exposed importers face limited replacement feasibility, and the observed margin is often switching or price segmentation rather than simple import collapse.")
    add("")
    if missing:
        add("## Missing outputs")
        add("")
        add("\n".join(f"- `{m}`" for m in missing))
        add("")
    add("## 1. Research Question and Contribution")
    add("")
    add("The research question is: when do Chinese critical-mineral export licensing controls bind in international trade, and through which adjustment margin do importers respond? The original criticism was fair: a design centered only on a negative PPML coefficient can look like the trivial claim that trade restrictions reduce trade. The revised design makes the theoretical object narrower and more useful. It asks why formally similar licensing controls generate different observed outcomes across products and importers.")
    add("")
    add("The mechanism has five pieces. First, importers differ in pre-policy China exposure. Second, importers differ in prior access to non-China suppliers. Third, products differ in external non-China production availability. Fourth, exposed demand can be switchable or non-switchable. Fifth, non-switchable pressure can appear as total import compression or as a price wedge between international and Chinese domestic markets. The contribution is therefore a pressure framework that predicts where China-source imports should fall and which margin should absorb the shock.")
    add("")
    add("## 2. Policy Context and Treated Products")
    add("")
    add(md_table(policy_table(mapping), ["HS code", "Product", "Wave", "Announcement", "Implementation", "Import-effect month", "Status", "Role"]))
    add("")
    add("The baseline uses only clean treated products. HS 2504, HS 8110, HS 8106, and HS 284180 are closer to the controlled product scope than bundled gallium/germanium or partial rare-earth categories. This choice reduces HS-code contamination and makes the mechanism tests more defensible. Bundled and partial products can still appear in secondary or price-diagnostic work, but they should not carry the main thesis claim.")
    add("")
    add("## 3. Data")
    add("")
    add("The trade data are monthly UN Comtrade importer-product-source observations from 2019-01 to 2026-03. Source is collapsed into China and rest of world (RoW). The preferred baseline aggregates the monthly panel to quarters because the policy shocks and customs reporting process are not clean daily events. Monthly estimates remain timing and robustness diagnostics. Import value in U.S. dollars is the main outcome. Net weight is used only where quantity reporting is reliable.")
    add("")
    add("The production data come from the USGS Mineral Commodity Summaries 2025 world data release. These data supply the external product-level availability measure, `A_prod`. Price data compare Chinese domestic benchmarks with international benchmarks and are used for price-wedge diagnostics.")
    add("")
    add(md_table([
        {"Component": "Trade flows", "Source": "UN Comtrade", "Use": "Main China/RoW/total import outcomes"},
        {"Component": "Production", "Source": "USGS MCS 2025 world data", "Use": "External `A_prod` availability"},
        {"Component": "Prices", "Source": "Bloomberg/Wind and related price exports", "Use": "Domestic-international price wedges"},
        {"Component": "Policy timing", "Source": "MOFCOM/GACC policy dates", "Use": "Treatment timing and event windows"},
    ], ["Component", "Source", "Use"]))
    add("")
    add("## 4. Theoretical Framework")
    add("")
    add("The framework separates legal licensing from observed market restriction. A legal control creates empirical pressure only when importers were exposed to China and replacement is limited.")
    add("")
    add("### 4.1 Exposure")
    add("")
    add(r"Importer China dependence is measured before the announcement:")
    add("")
    add(r"\[")
    add(r"E_{ip}=\frac{M^C_{ip,pre}}{M^C_{ip,pre}+M^R_{ip,pre}}.")
    add(r"\]")
    add("")
    add(r"Here, \(M^C_{ip,pre}\) is cumulative pre-announcement imports from China, and \(M^R_{ip,pre}\) is cumulative pre-announcement imports from non-China sources. If total pre-policy imports are zero, exposure is undefined.")
    add("")
    add("### 4.2 Importer Outside Access")
    add("")
    add(r"The baseline access measure is capacity access:")
    add("")
    add(r"\[")
    add(r"O^{cap}_{ip}=\min\left(1,\frac{M^R_{ip,pre}}{M^C_{ip,pre}}\right).")
    add(r"\]")
    add("")
    add(r"This measures whether importer \(i\) had non-China sourcing capacity before the policy. Robustness checks use frequency access, \(O^{freq}\), and binary access, \(O^{bin}\).")
    add("")
    add("### 4.3 External Production Availability")
    add("")
    add(r"External product availability is:")
    add("")
    add(r"\[")
    add(r"A^{prod}_{p}=Scale^{prod}_{p}\times(1-HHI^{ROW,prod}_{p}),")
    add(r"\]")
    add("")
    add(r"with")
    add("")
    add(r"\[")
    add(r"Scale^{prod}_{p}=\min\left(1,\frac{ROW\ production_p}{China\ production_p}\right),")
    add(r"\]")
    add("")
    add(r"and")
    add("")
    add(r"\[")
    add(r"HHI^{ROW,prod}_{p}=\sum_{c\neq China}s_{cp}^{2}.")
    add(r"\]")
    add("")
    add("This improves on trade-based product availability because it brings in an external supply measure rather than asking trade data to explain trade data. It remains a proxy. Production is not marginal spare capacity, and upstream production is not always the same as the exact HS product.")
    add("")
    add("### 4.4 Replacement Feasibility")
    add("")
    add(r"\[")
    add(r"K_{ip}=O_{ip}\times A^{prod}_{p}.")
    add(r"\]")
    add("")
    add(r"High \(K_{ip}\) means the importer had prior non-China access and the product has a larger, more diversified non-China production base.")
    add("")
    add("### 4.5 Switching and Compression Pressure")
    add("")
    add(r"\[")
    add(r"P^S_{ip}=E_{ip}\times K_{ip},")
    add(r"\]")
    add("")
    add(r"\[")
    add(r"P^C_{ip}=E_{ip}\times(1-K_{ip}),")
    add(r"\]")
    add("")
    add(r"\[")
    add(r"P^X_{ip}=E_{ip}.")
    add(r"\]")
    add("")
    add(r"The identity is \(P^S_{ip}+P^C_{ip}=E_{ip}\). \(P^S\) is switchable exposed demand. \(P^C\) is exposed demand that is not easily replaced.")
    add("")
    add("### 4.6 Edge Cases")
    add("")
    add(r"If China is the only effective supplier, \(A=0\), \(K=0\), \(P^S=0\), and \(P^C=E\). If non-China production is strong and the importer already has access, \(K\) is high and switching is likely. If RoW production exists but the importer lacks access, \(K\) stays low and compression or scarcity risk remains. If the importer has some RoW access but the product market is China-dominated, \(K\) is low to moderate and only partial switching is expected.")
    add("")
    add("## 5. Production-Based A Construction")
    add("")
    add(md_table(production_table(data), ["Product", "HS", "USGS commodity", "USGS production type", "China prod. 2023", "World total 2023", "A_prod 2023", "A_prod 2024", "Caveat"]))
    add("")
    add("Graphite uses mine production and is the cleanest direct production proxy for HS 2504. Antimony uses mine production in antimony content, which is upstream of antimony metal but captures the supply base. Bismuth uses refinery production, which is the best match among the USGS rows. Tungsten uses mine production in tungsten content, which is upstream of tungstates/APT. The 2023 value is the baseline because it is pre-policy for the later waves and close to the graphite announcement window. The 2024 value is used as a robustness check.")
    add("")
    add("## 6. Pressure Index Summary Statistics")
    add("")
    add("### 6.1 Pooled clean treated sample")
    add("")
    add(md_table(pooled_stats(summary), ["Variable", "Mean", "SD", "Min", "P25", "Median", "P75", "Max"]))
    add("")
    add("### 6.2 By product")
    add("")
    add(md_table(product_pressure_table(summary_product), ["Product", "HS", "N", "Mean E", "Mean O", "A_prod", "Mean K", "Mean P_S", "Mean P_C"]))
    add("")
    add("### 6.3 Correlations")
    add("")
    add(md_table(correlation_table(summary, summary_product), ["Product/group", "Corr(E,K)", "Corr(P_S,P_C)", "Corr(E,P_S)", "Corr(E,P_C)", "Corr(K,P_C)"]))
    add("")
    add(r"Antimony has the highest production availability in the clean sample because its non-China production base is larger relative to China than the others. Bismuth and tungsten have low `A_prod`, which makes replacement feasibility lower even when importers have some observed RoW access. Compression pressure is strongly tied to China exposure because \(P_C=E(1-K)\), while switching pressure depends on both exposure and replacement feasibility.")
    add("")
    add("## 7. Empirical Specification")
    add("")
    add("### 7.1 Average source-contrast PPML")
    add("")
    add(r"\[")
    add(r"\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+FE],")
    add(r"\]")
    add("")
    add(r"where \(D_{ipst}=China_s\times Treated_p\times Post_{pt}\).")
    add("")
    add("### 7.2 Exposure heterogeneity")
    add("")
    add(r"\[")
    add(r"\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+\theta_X(D_{ipst}\times E_{ip})+FE].")
    add(r"\]")
    add("")
    add(r"The expected sign is \(\theta_X<0\).")
    add("")
    add("### 7.3 Full pressure source-contrast model")
    add("")
    add(r"\[")
    add(r"\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+\theta_S(D_{ipst}\times P^S_{ip})+\theta_C(D_{ipst}\times P^C_{ip})+FE].")
    add(r"\]")
    add("")
    add(r"The expected signs are \(\theta_S<0\) and \(\theta_C<0\). Both channels can reduce China-source imports, but they imply different non-China and total-import responses.")
    add("")
    add("### 7.4 RoW switching mechanism")
    add("")
    add(r"\[")
    add(r"\mathbb{E}[M^R_{ipt}\mid X]=\exp[\gamma_S(Treated_p\times Post_{pt}\times P^S_{ip})+FE].")
    add(r"\]")
    add("")
    add(r"The expected sign is \(\gamma_S>0\).")
    add("")
    add("### 7.5 Total-import compression mechanism")
    add("")
    add(r"\[")
    add(r"\mathbb{E}[M^T_{ipt}\mid X]=\exp[\eta_C(Treated_p\times Post_{pt}\times P^C_{ip})+FE].")
    add(r"\]")
    add("")
    add(r"The expected sign is \(\eta_C<0\).")
    add("")
    add("### 7.6 Price wedge")
    add("")
    add(r"\[")
    add(r"\pi_{pt}=\log(P^{INT}_{pt})-\log(P^{CN}_{pt}).")
    add(r"\]")
    add("")
    add("A positive post-policy wedge is consistent with segmentation, scarcity, international demand pressure, or domestic-international decoupling. It is not a direct estimate of license denials and should not be read as compression only.")
    add("")
    add("## 8. Main Results: Average China-Source Effects")
    add("")
    add(md_table(main_table, ["Product/group", "coef", "p-value", "percent effect", "n used", "separation dropped"]))
    add("")
    add("The pooled clean estimate is negative and large, but pooled pretrends are problematic. Graphite is moderate and borderline. Antimony is the strongest quantity result. Bismuth also shows a large negative China-source effect. Tungstates/APT are negative but weak and statistically uninformative in the preferred baseline.")
    add("")
    add("## 9. Exposure and Pressure Heterogeneity Results")
    add("")
    add("### 9.1 D x E results")
    add("")
    add(md_table(exp_table, ["Product/group", "D x E coef", "p-value", "sign", "interpretation"]))
    add("")
    add("The exposure interaction is most persuasive for graphite, wave 4 W/Bi, and tungstates/APT. It is negative but weak for the pooled sample, antimony, and bismuth. This means exposure matters in some cells, but it is not a sufficient explanation by itself.")
    add("")
    add("### 9.2 D x P_S and D x P_C source-contrast results")
    add("")
    add(md_table(press_table, ["Product/group", "D x P_S coef", "P_S p-value", "D x P_C coef", "P_C p-value", "interpretation"]))
    add("")
    add(r"The source-contrast pressure model is diagnostic. Both \(P_S\) and \(P_C\) can predict China-source declines, so the sign in this model does not by itself distinguish switching from compression. The cleaner distinction appears in the RoW and total-import mechanism models.")
    add("")
    add("## 10. Mechanism Results")
    add("")
    add("### 10.1 RoW Switching")
    add("")
    add(md_table(row_switch, ["Product/group", "RoW P_S coef", "p-value", "expected sign", "interpretation"]))
    add("")
    add("Switching evidence is strongest for graphite and antimony. The pooled estimate is also positive. Bismuth and tungstates/APT have positive but weaker RoW switching coefficients.")
    add("")
    add("### 10.2 Total Import Compression")
    add("")
    add(md_table(total_comp, ["Product/group", "Total P_C coef", "p-value", "expected sign", "interpretation"]))
    add("")
    add("Compression is not general. The cleanest compression evidence is graphite. Bismuth has the expected sign but weak precision. Antimony and tungstates/APT do not support a pure total-import compression interpretation.")
    add("")
    add("### 10.3 Mechanism Ranking")
    add("")
    add("The current mechanism ranking is: 1. switching; 2. price segmentation; 3. compression. Switching has the broadest support in RoW import models. Price segmentation is strong for antimony and bismuth. Compression appears for graphite but is not a general result.")
    add("")
    add("## 11. Event Study and Pretrend Diagnostics")
    add("")
    add(md_table(evt_table, ["Product/group", "anchor", "joint pretrend p-value", "acceptable?", "comment"]))
    add("")
    add("> Warning: event-study diagnostics are not uniformly clean. Pooled source-contrast pretrends fail. Antimony is borderline. Tungstates/APT fail the pretrend diagnostic. Wide-panel China/RoW/total event studies do not include pooled-clean rows because those PPML fits failed with singular covariance matrices.")
    add("")
    add("Graphite has acceptable average pretrends. Bismuth is acceptable using the import-effect anchor. Wave 4 pooled timing is acceptable, but tungsten alone is not. These diagnostics support product-level interpretation over pooled claims.")
    add("")
    add("## 12. Placebo Diagnostics")
    add("")
    add(md_table(plac_table, ["Product/group", "placebo issue?", "strongest placebo problem", "interpretation"]))
    add("")
    add("Graphite is the cleanest placebo case. Antimony has clear placebo problems and should not be presented as clean timing identification. Wave 4 and tungstates also require caution. Some placebo coefficients are positive, so they do not always mimic the final negative treatment effect, but they still weaken a simple timing story.")
    add("")
    add("## 13. Robustness Checks")
    add("")
    add("### 13.1 Monthly robustness")
    add("")
    add(md_table(rob_tables["monthly"], ["Product", "quarterly effect", "monthly effect", "monthly p-value", "summary"]))
    add("")
    add("Monthly estimates mostly preserve the sign pattern, but monthly timing is noisier. Quarterly aggregation remains the preferred baseline because it is more consistent with customs reporting and the policy implementation window.")
    add("")
    add("### 13.2 Net-weight robustness")
    add("")
    add(md_table(rob_tables["net"], ["Product", "net-weight coef", "p-value", "percent effect", "interpretation"]))
    add("")
    add("Net weight is a robustness check, not the baseline. Quantity reporting is less reliable for some HS codes. Treat confirming signs as useful support and conflicting signs as a warning about unit heterogeneity.")
    add("")
    add("### 13.3 U.S. exclusion")
    add("")
    add(md_table(rob_tables["us"], ["Product/group", "US-excluded coef", "p-value", "percent effect", "interpretation"]))
    add("")
    add("The main negative effects do not depend only on the United States. U.S. exclusion preserves the negative direction for the pooled sample, antimony, wave 4 W/Bi, bismuth, and tungstates/APT. Graphite remains weaker.")
    add("")
    add("### 13.4 Alternative access definitions")
    add("")
    add(md_table(rob_tables["access"], ["variant", "P_S expected signs", "P_C expected signs", "pooled P_S coef", "pooled P_C coef"]))
    add("")
    add("Capacity access is the preferred baseline because it has a clear quantity interpretation. Frequency and binary access checks are useful but can change the sign of some pressure terms. These variants should be used as robustness, not as the main specification.")
    add("")
    add("### 13.5 Alternative A")
    add("")
    add(md_table(rob_tables["trade_prod"], ["Product/group", "term", "trade-A coef", "prod-A coef", "prod-A p-value"]))
    add("")
    add("The 2024 production-A robustness is close to the 2023 baseline because the USGS production structure changes little between the two years. The production-A version reduces the concern that product availability is being measured only with Comtrade flows. The trade-A comparison is useful for appendix discussion.")
    add("")
    add("### 13.6 Main robustness interpretation")
    add("")
    add("The average negative China-source effect survives several checks for antimony and bismuth. Graphite remains suggestive but not as strong. Tungstates/APT should be kept weak or unresolved. The pressure framework is more credible as a mechanism classification tool than as a search for uniformly significant interaction terms.")
    add("")
    add("## 14. Price-Wedge Diagnostics")
    add("")
    add(md_table(price_rows, ["Product", "HS", "coef", "p-value", "percent change", "interpretation"]))
    add("")
    if price_panel:
        add("Panel price-wedge DiD summaries:")
        add("")
        add(md_table(price_panel, ["Sample", "coef", "HC1 p-value", "pair-cluster p-value", "percent change"]))
        add("")
    add("Antimony has a strong positive price wedge. Bismuth has the strongest positive wedge. Graphite is negative and weak, so it does not support a segmentation story. The tungsten APT/tungstates benchmark is negative and should be treated as unresolved or benchmark-sensitive. Gallium and germanium price wedges are supportive but belong outside the clean baseline because the HS mapping is bundled or partial.")
    add("")
    add("## 15. Product-by-Product Interpretation")
    add("")
    add("### 15.1 Natural graphite")
    add("")
    add(r"Graphite has a moderate average China-source decline of about -30.1 percent with borderline precision. Its \(D\times P_C\) source-contrast coefficient is negative and statistically stronger than \(D\times P_S\). The RoW switching coefficient is positive and significant, and the total-import compression coefficient is negative. The price wedge is negative, so price segmentation is not supported. Pretrends and placebos are acceptable. Classification: mixed switching/compression quantity mechanism.")
    add("")
    add("### 15.2 Antimony metal")
    add("")
    add("Antimony has the strongest average China-source decline, about -86.7 percent. The RoW switching coefficient is positive and significant, while total-import compression is wrong-signed. The price wedge is strongly positive. The evidence supports strong disruption, switching, and price segmentation. Timing is not clean because the pretrend is borderline and placebo tests are problematic. Classification: strong disruption with switching and price segmentation; timing caveat.")
    add("")
    add("### 15.3 Bismuth metal")
    add("")
    add(r"Bismuth has a large average China-source decline, about -74.4 percent. The source-contrast pressure terms have expected signs, especially \(D\times P_C\). Quantity mechanisms are weaker: RoW switching is positive but imprecise, and total compression is negative but imprecise. The price wedge is very large and strongly significant. Pretrend and placebo diagnostics are cleaner than antimony. Classification: strong disruption with price segmentation; weaker quantity mechanism.")
    add("")
    add("### 15.4 Tungstates/APT")
    add("")
    add("Tungstates/APT have a weak average China-source estimate, about -15.2 percent, with a high p-value. The switching coefficient is positive but imprecise. Compression is wrong-signed in the total-import model. The price wedge is negative, and pretrends are problematic. The earlier automatic switching classification is too generous. Classification: weak/null or unresolved.")
    add("")
    add("## 16. Final Classification Table")
    add("")
    add(md_table(interp_rows, ["Product", "Average effect", "Switching", "Compression", "Price wedge", "Timing validity", "Final classification"]))
    add("")
    add("## 17. Final Research Answer")
    add("")
    add("Chinese licensing controls do not bind mechanically. They bind most clearly when pre-policy China exposure interacts with limited replacement feasibility. The most consistent observed margin is RoW switching, while total-import compression is weaker and product-specific. Price wedges reveal segmentation or scarcity for antimony and bismuth. Tungstates/APT remain weak or unresolved.")
    add("")
    add("## 18. Limitations")
    add("")
    add("- The data do not observe license applications, approvals, denials, processing time, or firm-level contract terms.")
    add("- HS codes imperfectly map to legal product scope, especially outside the clean baseline.")
    add("- Production data are not spare capacity data.")
    add("- Antimony and tungsten production proxies are upstream of the HS products used in trade regressions.")
    add("- Bismuth has byproduct and refining constraints that production totals may not capture.")
    add("- Comtrade reporting can lag policy implementation.")
    add("- PPML separation removes observations in several models.")
    add("- The clean treated sample has only four products.")
    add("- Pooled pretrend diagnostics are weak.")
    add("- Antimony placebo diagnostics are problematic.")
    add("- Tungsten has weak average effects, bad pretrends, and benchmark-sensitive price evidence.")
    add("")
    add("## 19. External Reviewer Attack Points")
    add("")
    add(md_table(reviewer_attacks(), ["Attack", "Severity", "Response"]))
    add("")
    add("## 20. Final One-Page Thesis Summary")
    add("")
    add("The thesis contributes a mechanism-based framework for Chinese critical-mineral export licensing controls. The key object is not the average PPML coefficient. It is the interaction between importer China exposure and replacement feasibility, where replacement feasibility combines importer outside access and external non-China production availability. The mechanism ranking is switching first, price segmentation second, and compression third. Final classifications are: graphite as mixed switching/compression; antimony as strong disruption with switching and price segmentation but timing caveats; bismuth as strong disruption with price segmentation and weaker quantity mechanisms; and tungstates/APT as weak/null or unresolved. The safe thesis claim is that Chinese licensing controls bind unevenly. They produce the clearest market responses when exposed importers face limited replacement feasibility, and those responses can appear as switching or price segmentation rather than import collapse.")
    add("")
    add("## 21. Build Warnings and Estimation Failures")
    add("")
    add("Build warnings:")
    add("")
    build_warning = texts["build_warnings"].strip() or "_No build-warning file was available._"
    add(build_warning)
    add("")
    add("Model-warning summary:")
    add("")
    add(md_table(warnings_summary(texts["model_warnings"]), ["Warning type", "count"]))
    add("")
    add("The main warnings are PPML separation, missing pressure cells, no-variation event bins, pooled wide event-study failures, and monthly demeaning or covariance failures in some event-study models. These warnings do not invalidate the whole report, but they define which claims should remain cautious.")
    return "\n".join(lines) + "\n"


def build_short_report() -> str:
    _missing, csv, _texts = file_inventory()
    main = csv["main"]
    mechanisms = csv["mechanisms"]
    classification = csv["classification"]
    price = csv["price"]
    summary_product = csv["summary_product"]

    lines: list[str] = []
    add = lines.append
    add("# FULL THESIS EMPIRICAL REPORT SHORT")
    add("")
    add("## Core idea")
    add("")
    add("The revised thesis does not ask only whether export controls reduce trade. It asks when licensing controls bind and through which margin importers adjust. The framework combines pre-policy China exposure, importer outside access, and USGS production-based non-China availability.")
    add("")
    add(r"\[E_{ip}=\frac{M^C_{ip,pre}}{M^C_{ip,pre}+M^R_{ip,pre}},\quad K_{ip}=O_{ip}\times A^{prod}_{p}\]")
    add("")
    add(r"\[P^S_{ip}=E_{ip}K_{ip},\quad P^C_{ip}=E_{ip}(1-K_{ip}),\quad P^S_{ip}+P^C_{ip}=E_{ip}.\]")
    add("")
    add("`P_S` is switchable exposed demand. `P_C` is non-switchable exposed demand.")
    add("")
    add("## Production-based availability")
    add("")
    add(md_table(product_pressure_table(summary_product), ["Product", "HS", "N", "Mean E", "Mean O", "A_prod", "Mean K", "Mean P_S", "Mean P_C"]))
    add("")
    add("## Main average effects")
    add("")
    add(md_table(main_average_table(main), ["Product/group", "coef", "p-value", "percent effect", "n used", "separation dropped"]))
    add("")
    add("## Mechanisms")
    add("")
    add("Switching:")
    add("")
    add(md_table(mechanism_rows(mechanisms, "row"), ["Product/group", "RoW P_S coef", "p-value", "expected sign", "interpretation"]))
    add("")
    add("Compression:")
    add("")
    add(md_table(mechanism_rows(mechanisms, "total"), ["Product/group", "Total P_C coef", "p-value", "expected sign", "interpretation"]))
    add("")
    add("## Price wedges")
    add("")
    add(md_table(price_table(price), ["Product", "HS", "coef", "p-value", "percent change", "interpretation"]))
    add("")
    add("## Product classification")
    add("")
    add(md_table(product_interpretation_rows(classification), ["Product", "Average effect", "Switching", "Compression", "Price wedge", "Timing validity", "Final classification"]))
    add("")
    add("## Final claim")
    add("")
    add("Chinese licensing controls do not bind mechanically. They bind most clearly when exposed importers face limited replacement feasibility. The most consistent observed margin is RoW switching. Price wedges support segmentation or scarcity for antimony and bismuth. Total-import compression is weaker and product-specific. Tungstates/APT remain weak or unresolved.")
    add("")
    add("## Main limitations")
    add("")
    add("- No license-level data are observed.")
    add("- Production data measure output, not spare tradable capacity.")
    add("- HS-product mapping is imperfect outside the clean baseline.")
    add("- Antimony has placebo and timing caveats.")
    add("- Tungstates/APT have weak average effects and problematic pretrends.")
    add("- PPML separation and missing pressure cells affect some specifications.")
    return "\n".join(lines) + "\n"


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    FULL_OUT.write_text(build_full_report(), encoding="utf-8")
    SHORT_OUT.write_text(build_short_report(), encoding="utf-8")
    print(f"Wrote {FULL_OUT}")
    print(f"Wrote {SHORT_OUT}")


if __name__ == "__main__":
    main()
