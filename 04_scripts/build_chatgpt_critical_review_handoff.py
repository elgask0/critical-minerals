from __future__ import annotations

import math
import re
import shutil
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [
    REPO / "results" / "full_thesis_report",
    REPO / "results" / "revised_pressure_K_prod_A_2023",
    REPO / "results" / "revised_pressure_K_prod_A_2024",
    REPO / "results" / "revised_pressure_K_trade_A",
]
OUT = REPO / "results" / "chatgpt_critical_review_handoff"
SOURCE_COPY = OUT / "source_results"
ZIP_OUT = OUT / "Handoff_Package.zip"

GROUP_ORDER = [
    "pooled_clean",
    "wave2_graphite",
    "wave3_antimony_clean",
    "wave4_w_bi",
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
ANCHORS = ["announcement", "implementation", "import_effect", "first_full_post_quarter"]
FREQS = ["quarterly", "monthly"]


def load(name: str, folder: Path | None = None) -> pd.DataFrame:
    p = (folder or SOURCE_DIRS[0]) / name
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()


def read_text(name: str, folder: Path | None = None) -> str:
    p = (folder or SOURCE_DIRS[0]) / name
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def fmt_num(x: object, digits: int = 3) -> str:
    try:
        val = float(x)
    except Exception:
        return ""
    if not math.isfinite(val):
        return ""
    return f"{val:.{digits}f}"


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


def fmt_pct(x: object) -> str:
    try:
        val = float(x)
    except Exception:
        return ""
    if not math.isfinite(val):
        return ""
    return f"{val:.1f}%"


def clean_label(x: object) -> str:
    text = str(x)
    return GROUP_LABELS.get(text, text)


def md_table(rows: list[dict], headers: list[str], max_rows: int | None = None) -> str:
    if max_rows is not None and len(rows) > max_rows:
        rows = rows[:max_rows]
    labels = headers
    if not rows:
        return "_No rows available._"
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


def table_from_df(df: pd.DataFrame, cols: list[str], max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows available._"
    rows: list[dict] = []
    for _, r in df.iterrows():
        row: dict[str, str] = {}
        for c in cols:
            if c not in df.columns:
                row[c] = ""
                continue
            value = r[c]
            if c in {"coef", "se"} or c.endswith("_coef") or c.endswith("_se"):
                row[c] = fmt_num(value)
            elif "p_value" in c or c.startswith("p_") or c.endswith("_p_value"):
                row[c] = fmt_p(value)
            elif "percent" in c:
                row[c] = fmt_pct(value)
            elif c in {"n_used", "n_before_ppml", "n_dropped_separation", "joint_df", "nobs"}:
                row[c] = "" if pd.isna(value) else str(int(float(value)))
            elif isinstance(value, float):
                row[c] = fmt_num(value)
            else:
                row[c] = "" if pd.isna(value) else str(value)
        rows.append(row)
    note = ""
    if max_rows is not None and len(rows) > max_rows:
        note = f"\n\n_Showing first {max_rows} of {len(rows)} rows. The complete CSV is included in the handoff package._"
    return md_table(rows, cols, max_rows=max_rows) + note


def select(df: pd.DataFrame, **kwargs: object) -> pd.DataFrame:
    out = df.copy()
    for col, val in kwargs.items():
        if col not in out.columns:
            return pd.DataFrame()
        if isinstance(val, (list, tuple, set)):
            out = out[out[col].isin(val)]
        else:
            out = out[out[col].eq(val)]
    return out


def first_full(df: pd.DataFrame) -> pd.DataFrame:
    return select(df, anchor="first_full_post_quarter")


def result_cols() -> list[str]:
    return [
        "frequency",
        "group",
        "anchor",
        "model",
        "pressure_variant",
        "term",
        "coef",
        "p_value",
        "percent_effect",
        "n_used",
        "n_dropped_separation",
        "expected_sign",
        "matches_expected_sign",
    ]


def main_rows(main: pd.DataFrame, frequency: str, module: str | None = None) -> pd.DataFrame:
    df = main[main["frequency"].eq(frequency)].copy()
    if module:
        df = df[df["report_module"].eq(module)]
    return df


def compact_average(main: pd.DataFrame, frequency: str, anchor: str | None = None) -> pd.DataFrame:
    df = main_rows(main, frequency, f"baseline_ppml_{frequency}")
    df = df[df["term"].eq("D")]
    if anchor:
        df = df[df["anchor"].eq(anchor)]
    return df.sort_values(["anchor", "group"])


def production_table(data: pd.DataFrame) -> list[dict]:
    if data.empty:
        return []
    d23 = data[data["year"].eq(2023)].copy()
    d24 = data[data["year"].eq(2024)][["hs", "A_prod"]].rename(columns={"A_prod": "A_prod_2024"})
    merged = d23.merge(d24, on="hs", how="left")
    rows = []
    for _, r in merged.iterrows():
        rows.append(
            {
                "Product": str(r["product_name"]),
                "HS": str(r["hs"]),
                "USGS commodity": str(r["usgs_commodity"]),
                "Type": str(r["usgs_type"]),
                "China production 2023": fmt_num(r["china_production"], 0),
                "World total 2023": fmt_num(r["world_total"], 0),
                "A_prod 2023": fmt_num(r["A_prod"]),
                "A_prod 2024": fmt_num(r.get("A_prod_2024")),
                "Caveat": str(r.get("notes", "")),
            }
        )
    return rows


def policy_table(mapping: pd.DataFrame) -> list[dict]:
    if mapping.empty:
        return [
            {"HS": "2504", "Product": "Natural graphite", "Wave": "2", "Announcement": "2023-10-20", "Implementation": "2023-12-01", "Import-effect month": "2024-01", "Status": "clean treated"},
            {"HS": "8110", "Product": "Antimony metal", "Wave": "3", "Announcement": "2024-08-15", "Implementation": "2024-09-15", "Import-effect month": "2024-10", "Status": "clean treated"},
            {"HS": "8106", "Product": "Bismuth metal", "Wave": "4", "Announcement": "2025-02-04", "Implementation": "2025-02-04", "Import-effect month": "2025-03", "Status": "clean treated"},
            {"HS": "284180", "Product": "Tungstates/APT", "Wave": "4", "Announcement": "2025-02-04", "Implementation": "2025-02-04", "Import-effect month": "2025-03", "Status": "clean treated"},
        ]
    df = mapping[mapping["analysis_role"].eq("main_clean_treated")].copy()
    df = df.sort_values(["wave", "hs"])
    rows = []
    for _, r in df.iterrows():
        rows.append(
            {
                "HS": str(r["hs"]),
                "Product": str(r["product_name"]),
                "Wave": str(int(r["wave"])),
                "Announcement": str(r["announcement_date"]),
                "Implementation": str(r["implementation_date"]),
                "Import-effect month": str(r["import_effect_month"]),
                "Status": "clean treated",
            }
        )
    return rows


def pooled_pressure_stats(summary: pd.DataFrame) -> list[dict]:
    variables = ["E_china", "O_cap", "A_prod_2023", "K_cap_prod", "P_S_cap_prod", "P_C_cap_prod"]
    labels = {
        "E_china": "E",
        "O_cap": "O_cap",
        "A_prod_2023": "A_prod",
        "K_cap_prod": "K",
        "P_S_cap_prod": "P_S",
        "P_C_cap_prod": "P_C",
    }
    if summary.empty:
        return []
    df = summary[
        summary["group"].eq("pooled_clean_treated")
        & summary["stat_type"].eq("distribution")
        & summary["variable"].isin(variables)
    ]
    rows = []
    for v in variables:
        s = df[df["variable"].eq(v)]
        if s.empty:
            continue
        r = s.iloc[0]
        rows.append(
            {
                "Variable": labels[v],
                "mean": fmt_num(r["mean"]),
                "sd": fmt_num(r["sd"]),
                "min": fmt_num(r["min"]),
                "p25": fmt_num(r["p25"]),
                "median": fmt_num(r["median"]),
                "p75": fmt_num(r["p75"]),
                "max": fmt_num(r["max"]),
            }
        )
    return rows


def product_pressure_stats(by_product: pd.DataFrame) -> list[dict]:
    if by_product.empty:
        return []
    rows = []
    for _, r in by_product.iterrows():
        rows.append(
            {
                "Product": str(r["product"]),
                "HS": str(r["hs"]),
                "N": str(int(r["n_cells"])),
                "Mean E": fmt_num(r["mean_E_china"]),
                "Mean O_cap": fmt_num(r["mean_O_cap"]),
                "A_prod": fmt_num(r["mean_A_prod_2023"]),
                "Mean K": fmt_num(r["mean_K_cap_prod"]),
                "Mean P_S": fmt_num(r["mean_P_S_cap_prod"]),
                "Mean P_C": fmt_num(r["mean_P_C_cap_prod"]),
            }
        )
    return rows


def correlation_stats(summary: pd.DataFrame, by_product: pd.DataFrame) -> list[dict]:
    rows: list[dict] = []
    if not summary.empty:
        corr = summary[summary["group"].eq("pooled_clean_treated") & summary["stat_type"].eq("correlation")]

        def c(a: str, b: str) -> str:
            left = corr[corr["product"].eq(a) & corr["variable"].eq(b)]
            right = corr[corr["product"].eq(b) & corr["variable"].eq(a)]
            use = left if not left.empty else right
            return "" if use.empty else fmt_num(use.iloc[0]["mean"])

        rows.append(
            {
                "Product/group": "Pooled clean",
                "Corr(E,K)": c("E_china", "K_cap_prod"),
                "Corr(P_S,P_C)": c("P_S_cap_prod", "P_C_cap_prod"),
                "Corr(E,P_S)": c("E_china", "P_S_cap_prod"),
                "Corr(E,P_C)": c("E_china", "P_C_cap_prod"),
                "Corr(K,P_C)": c("K_cap_prod", "P_C_cap_prod"),
            }
        )
    if not by_product.empty:
        for _, r in by_product.iterrows():
            rows.append(
                {
                    "Product/group": str(r["product"]),
                    "Corr(E,K)": fmt_num(r["corr_E_K_cap_prod"]),
                    "Corr(P_S,P_C)": fmt_num(r["corr_PS_PC_cap_prod"]),
                    "Corr(E,P_S)": fmt_num(r["corr_PS_E_cap_prod"]),
                    "Corr(E,P_C)": fmt_num(r["corr_PC_E_cap_prod"]),
                    "Corr(K,P_C)": fmt_num(r["corr_K_PC_cap_prod"]),
                }
            )
    return rows


def summarize_placebo(placebo: pd.DataFrame) -> list[dict]:
    if placebo.empty:
        return []
    rows = []
    cols = ["group", "frequency", "model"]
    for keys, g in placebo.groupby(cols, dropna=False):
        group, freq, model = keys
        g2 = g.copy()
        any_issue = g2["p_value"].dropna().lt(0.05).any()
        s = g2.sort_values("p_value", na_position="last").iloc[0]
        rows.append(
            {
                "group": clean_label(group),
                "frequency": str(freq),
                "model": str(model),
                "any p < 0.05": "yes" if any_issue else "no",
                "strongest": f"{int(s['placebo_lag_months'])}m {s['term']} coef {fmt_num(s['coef'])}, p {fmt_p(s['p_value'])}",
                "interpretation": "problematic placebo signal" if any_issue else "no strong placebo signal",
            }
        )
    return rows


def classify_product_rows(classification: pd.DataFrame) -> list[dict]:
    rows = []
    strict = {
        "hs2504_graphite": "mixed switching/compression quantity mechanism",
        "hs8110_antimony_metal": "strong disruption with switching and price segmentation; timing caveat",
        "hs8106_bismuth": "strong disruption with price segmentation; weaker quantity mechanism",
        "hs284180_tungstates": "weak/null or unresolved",
    }
    if classification.empty:
        return []
    for group in ["hs2504_graphite", "hs8110_antimony_metal", "hs8106_bismuth", "hs284180_tungstates"]:
        r = classification[classification["group"].eq(group)]
        if r.empty:
            continue
        s = r.iloc[0]
        rows.append(
            {
                "Product": str(s["product"]),
                "Average effect": f"{fmt_pct(s['average_percent_effect'])} (p {fmt_p(s['average_p_value'])})",
                "Switching": f"{fmt_num(s['row_switch_coef'])} (p {fmt_p(s['row_switch_p_value'])})",
                "Compression": f"{fmt_num(s['total_compression_coef'])} (p {fmt_p(s['total_compression_p_value'])})",
                "Price wedge": f"{fmt_num(s['price_wedge_coef'])} (p {fmt_p(s['price_wedge_p_value'])})",
                "Timing": "acceptable" if bool(s["pretrend_acceptable_p_ge_0_10"]) else "caution",
                "Strict classification": strict[group],
            }
        )
    return rows


def build_coverage(csv: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict] = []

    def add(block: str, frequency: str, model_type: str, group: str, anchor: str, exists: bool, source: str, included_master: bool, included_appendix: bool, failure: str = "", notes: str = "") -> None:
        rows.append(
            {
                "result_block": block,
                "frequency": frequency,
                "model_type": model_type,
                "group": group,
                "timing_anchor": anchor,
                "exists": bool(exists),
                "source_file": source if exists else "",
                "included_in_master": bool(included_master),
                "included_in_appendix": bool(included_appendix),
                "failure_reason": "" if exists else failure,
                "notes": notes,
            }
        )

    main = csv["MAIN_RESULTS.csv"]
    mech = csv["MECHANISMS.csv"]
    event = csv["EVENT_STUDY.csv"]
    placebo = csv["PLACEBO.csv"]
    robustness = csv["ROBUSTNESS.csv"]
    price = csv["PRICE_WEDGES.csv"]

    main_specs = [
        ("Average PPML", "average_source_contrast", "D", "none"),
        ("D x E", "source_contrast_E", "D_E_china", "exposure"),
        ("D x P_S/P_C", "source_contrast_PS_PC", "D_P_S_cap_prod", "capacity"),
        ("E-K diagnostic", "source_contrast_E_K", "D_K_cap_prod", "capacity"),
    ]
    for freq in FREQS:
        for block, model, term, variant in main_specs:
            for group in GROUP_ORDER:
                for anchor in ANCHORS:
                    exists = not main[
                        main["frequency"].eq(freq)
                        & main["model"].eq(model)
                        & main["group"].eq(group)
                        & main["anchor"].eq(anchor)
                        & main["term"].eq(term)
                        & main["pressure_variant"].eq(variant)
                    ].empty
                    add(block, freq, model, group, anchor, exists, "MAIN_RESULTS.csv", True, True, "not generated or term dropped")

    mech_specs = [
        ("RoW switching", "row_switch_only", "TP_P_S_cap_prod", "capacity"),
        ("RoW full P_S/P_C", "row_full_PS_PC", "TP_P_S_cap_prod", "capacity"),
        ("Total compression", "total_compress_only", "TP_P_C_cap_prod", "capacity"),
        ("Total full P_S/P_C", "total_full_PS_PC", "TP_P_C_cap_prod", "capacity"),
    ]
    for freq in FREQS:
        for block, model, term, variant in mech_specs:
            for group in GROUP_ORDER:
                exists = not mech[
                    mech["frequency"].eq(freq)
                    & mech["model"].eq(model)
                    & mech["group"].eq(group)
                    & mech["term"].eq(term)
                    & mech["pressure_variant"].eq(variant)
                ].empty
                add(block, freq, model, group, "first_full_post_quarter", exists, "MECHANISMS.csv", True, True, "not generated or term dropped")

    for freq in FREQS:
        for model in ["average_event_study", "pressure_gradient_event_study"]:
            block = "Event study average" if model == "average_event_study" else "Event study pressure-gradient"
            for group in GROUP_ORDER:
                for anchor in ANCHORS:
                    exists = not event[
                        event["frequency"].eq(freq)
                        & event["model"].eq(model)
                        & event["group"].eq(group)
                        & event["anchor"].eq(anchor)
                        & event["row_type"].eq("joint_pretrend")
                    ].empty
                    note = "joint pretrend row checked"
                    add(block, freq, model, group, anchor, exists, "EVENT_STUDY.csv", True, True, "event model failed, covariance failed, or no variation", note)

    for freq in FREQS:
        for model, block in [
            ("placebo_average", "Placebo average"),
            ("placebo_exposure", "Placebo D x E"),
            ("placebo_pressure", "Placebo D x P_S/P_C"),
        ]:
            for group in GROUP_ORDER:
                for anchor in ["implementation", "import_effect", "first_full_post_quarter"]:
                    exists = not placebo[
                        placebo["frequency"].eq(freq)
                        & placebo["model"].eq(model)
                        & placebo["group"].eq(group)
                        & placebo["anchor"].eq(anchor)
                    ].empty
                    add(block, freq, model, group, anchor, exists, "PLACEBO.csv", True, True, "placebo model missing or failed")

    robust_specs = [
        ("U.S.-excluded", "us_excluded_quarterly", "quarterly"),
        ("U.S.-excluded", "us_excluded_monthly", "monthly"),
        ("U.S. interactions", "us_interactions", "quarterly"),
        ("U.S. interactions", "us_interactions", "monthly"),
        ("Net-weight robustness", "net_weight", "quarterly"),
        ("A_prod 2024 robustness", "prodA_2024_source", "quarterly"),
    ]
    for block, module, freq in robust_specs:
        for group in GROUP_ORDER:
            exists = not robustness[
                robustness["report_module"].eq(module)
                & robustness["frequency"].eq(freq)
                & robustness["group"].eq(group)
            ].empty
            add(block, freq, module, group, "various", exists, "ROBUSTNESS.csv", True, True, "robustness block missing or model terms dropped")

    for group in GROUP_ORDER:
        exists = not robustness[
            robustness["report_module"].eq("tradeA_vs_prodA")
            & robustness["group"].eq(group)
        ].empty
        add(
            "trade-A comparison",
            "not frequency-specific",
            "tradeA_vs_prodA",
            group,
            "first_full_post_quarter",
            exists,
            "ROBUSTNESS.csv",
            True,
            True,
            "trade-A comparison rows missing",
            "comparison block has no frequency column by design",
        )

    exists_price = not price.empty
    add("Price wedges", "monthly", "pair_its_hac3", "price_pairs", "product post month", exists_price, "PRICE_WEDGES.csv", True, True, "price wedge file missing")
    add("Model warnings", "all", "warnings", "all", "all", (SOURCE_DIRS[0] / "MODEL_WARNINGS.txt").exists(), "MODEL_WARNINGS.txt", True, True, "warning file missing")
    return pd.DataFrame(rows)


def compact_coverage_table(coverage: pd.DataFrame) -> list[dict]:
    rows = []
    for block, g in coverage.groupby("result_block"):
        total = len(g)
        exists = int(g["exists"].sum())
        missing = total - exists
        src = ", ".join(sorted(s for s in g["source_file"].dropna().unique() if s)) or ""
        rows.append(
            {
                "Result block": block,
                "available": f"{exists}/{total}",
                "missing/failing": str(missing),
                "source": src,
                "note": "complete or mostly complete" if missing == 0 else "see RESULT_COVERAGE_AUDIT.csv",
            }
        )
    return rows


def strongest_event_table(event: pd.DataFrame) -> pd.DataFrame:
    if event.empty:
        return pd.DataFrame()
    return event[event["row_type"].eq("joint_pretrend")].sort_values(["frequency", "model", "group", "anchor", "gradient"])


def file_sources() -> list[Path]:
    files: list[Path] = []
    for d in SOURCE_DIRS:
        if not d.exists():
            continue
        for p in d.iterdir():
            if p.is_file() and p.suffix.lower() in {".csv", ".md", ".txt"}:
                files.append(p)
    return sorted(set(files))


def source_rel(p: Path) -> Path:
    for d in SOURCE_DIRS:
        try:
            rel = p.relative_to(d)
            return Path(d.name) / rel
        except ValueError:
            continue
    return Path(p.name)


def copy_source_files() -> list[Path]:
    SOURCE_COPY.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for p in file_sources():
        rel = source_rel(p)
        dest = SOURCE_COPY / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        copied.append(dest)
    return copied


def load_all() -> tuple[dict[str, pd.DataFrame], dict[str, str]]:
    names = [
        "DATA_AUDIT.csv",
        "SUMMARY_STATS.csv",
        "SUMMARY_STATS_BY_PRODUCT.csv",
        "MAIN_RESULTS.csv",
        "MECHANISMS.csv",
        "EVENT_STUDY.csv",
        "EVENT_STUDY_MECHANISMS.csv",
        "PLACEBO.csv",
        "ROBUSTNESS.csv",
        "PRICE_WEDGES.csv",
        "PRODUCT_CLASSIFICATION.csv",
        "production_mapping.csv",
        "PRESSURE_INDEX_IMPORTER_PRODUCT.csv",
    ]
    csv = {name: load(name) for name in names}
    texts = {
        "THEORY.md": read_text("THEORY.md"),
        "FINAL_INTERPRETATION.md": read_text("FINAL_INTERPRETATION.md"),
        "THESIS_SUMMARY_1_PAGE.md": read_text("THESIS_SUMMARY_1_PAGE.md"),
        "REPORT_BUILD_WARNINGS.md": read_text("REPORT_BUILD_WARNINGS.md"),
        "MODEL_WARNINGS.txt": read_text("MODEL_WARNINGS.txt"),
        "README.md": read_text("README.md"),
    }
    return csv, texts


def main_result_table(df: pd.DataFrame, cols: list[str] | None = None, max_rows: int | None = None) -> str:
    if cols is None:
        cols = result_cols()
    use = [c for c in cols if c in df.columns]
    return table_from_df(df[use].copy(), use, max_rows=max_rows)


def build_master(csv: dict[str, pd.DataFrame], texts: dict[str, str], coverage: pd.DataFrame) -> str:
    data = csv["DATA_AUDIT.csv"]
    summary = csv["SUMMARY_STATS.csv"]
    by_product = csv["SUMMARY_STATS_BY_PRODUCT.csv"]
    main = csv["MAIN_RESULTS.csv"]
    mech = csv["MECHANISMS.csv"]
    event = csv["EVENT_STUDY.csv"]
    placebo = csv["PLACEBO.csv"]
    robustness = csv["ROBUSTNESS.csv"]
    price = csv["PRICE_WEDGES.csv"]
    classification = csv["PRODUCT_CLASSIFICATION.csv"]
    mapping = csv["production_mapping.csv"]

    quarterly_average = compact_average(main, "quarterly", "first_full_post_quarter")
    monthly_average = compact_average(main, "monthly", None)
    quarterly_pressure = first_full(main[main["frequency"].eq("quarterly")])
    quarterly_pressure = quarterly_pressure[
        quarterly_pressure["term"].isin(["D_E_china", "D_P_S_cap_prod", "D_P_C_cap_prod", "D_K_cap_prod"])
    ].copy()
    monthly_pressure = main[main["frequency"].eq("monthly")]
    monthly_pressure = monthly_pressure[
        monthly_pressure["term"].isin(["D_E_china", "D_P_S_cap_prod", "D_P_C_cap_prod", "D_K_cap_prod"])
    ].copy()
    q_mech = mech[mech["frequency"].eq("quarterly")].copy()
    m_mech = mech[mech["frequency"].eq("monthly")].copy()
    event_joint = strongest_event_table(event)
    placebo_summary = summarize_placebo(placebo)

    lines: list[str] = []

    def add(s: str = "") -> None:
        lines.append(s)

    add("# MASTER CRITICAL REVIEW DOSSIER")
    add("")
    add("## 0. Purpose of this dossier")
    add("")
    add("This dossier is designed for a new ChatGPT 5.5 Pro instance that has no access to previous conversations. It gives enough theory, data construction, empirical specification, result tables, robustness checks, warnings, and raw file references to judge the current thesis design critically.")
    add("")
    add("The task is not to praise the design. The task is to judge whether the theory and results align, decide what should remain in the thesis, and flag overclaims, weak mechanisms, inconsistent signs, bad pretrends, placebo problems, and fragile robustness.")
    add("")
    add("## 1. Project overview")
    add("")
    add("Working title: **When Do Chinese Critical-Mineral Export Controls Bind? China's Licensing-Based Controls and Heterogeneous Trade Responses**.")
    add("")
    add("Field: international economics, trade policy, critical minerals, and economic statecraft.")
    add("")
    add("Research question: **Why do formally similar Chinese export-licensing controls generate different trade and price disruptions across critical minerals?**")
    add("")
    add("The original design was vulnerable to the criticism that it only estimated whether export restrictions reduce trade. That claim is intuitive and not enough for a strong thesis. The revised contribution shifts the question from an average treatment effect to heterogeneous binding: which products and importers experience an observable market response, and whether the response appears through non-China substitution, total import compression, or domestic-international price segmentation.")
    add("")
    add("## 2. Policy context and treated products")
    add("")
    add(md_table(policy_table(mapping), ["HS", "Product", "Wave", "Announcement", "Implementation", "Import-effect month", "Status"]))
    add("")
    add("The baseline sample uses only clean treated products. Bundled or partial HS codes are excluded from the main baseline because the legal product and the customs category do not match closely enough. They can still be used as secondary diagnostics, but they should not carry the main mechanism claim.")
    add("")
    add("## 3. Data")
    add("")
    add("The trade panel is monthly UN Comtrade importer-product-source data from 2019-01 to 2026-03. Source is collapsed into China and rest of world (RoW). Quarterly aggregation is the preferred baseline because customs reporting and policy implementation do not map cleanly to exact announcement days. Monthly models remain robustness and timing diagnostics. Import value in U.S. dollars is the main outcome; net weight is a robustness outcome where quantity reporting is usable.")
    add("")
    add(md_table([
        {"Data component": "Trade flows", "Source": "UN Comtrade", "Frequency": "monthly, aggregated to quarterly", "Role": "China/RoW/total import outcomes"},
        {"Data component": "Production", "Source": "USGS Mineral Commodity Summaries 2025 world data", "Frequency": "annual", "Role": "External product availability A_prod"},
        {"Data component": "Prices", "Source": "Bloomberg/Wind and related price exports", "Frequency": "monthly where available", "Role": "Domestic-international price wedges"},
        {"Data component": "Policy timing", "Source": "MOFCOM/GACC announcements", "Frequency": "policy dates", "Role": "Announcement, implementation, import-effect timing"},
    ], ["Data component", "Source", "Frequency", "Role"]))
    add("")
    add("## 4. Theory and pressure-index framework")
    add("")
    add("### 4.1 Exposure")
    add("")
    add(r"\[E_{ip}=\frac{M^C_{ip,pre}}{M^C_{ip,pre}+M^R_{ip,pre}}\]")
    add("")
    add(r"\(E_{ip}\) is importer-product China exposure. \(M^C_{ip,pre}\) is cumulative pre-announcement imports from China. \(M^R_{ip,pre}\) is cumulative pre-announcement imports from non-China sources. Pressure cells with zero total pre-policy imports are undefined rather than silently set to zero.")
    add("")
    add("### 4.2 Importer outside access")
    add("")
    add(r"\[O^{cap}_{ip}=\min\left(1,\frac{M^R_{ip,pre}}{M^C_{ip,pre}}\right)\]")
    add("")
    add("Capacity access is the baseline. `O_freq` measures the share of pre-policy months with positive RoW sourcing. `O_bin` is a binary meaningful-access proxy. Capacity is preferred because it has a quantity interpretation.")
    add("")
    add("### 4.3 External production availability")
    add("")
    add(r"\[A^{prod}_{p}=Scale^{prod}_{p}\times(1-HHI^{ROW,prod}_{p})\]")
    add("")
    add(r"\[Scale^{prod}_{p}=\min\left(1,\frac{ROW\ production_p}{China\ production_p}\right)\]")
    add("")
    add(r"\[HHI^{ROW,prod}_{p}=\sum_{c\neq China}s_{cp}^{2}\]")
    add("")
    add("Production-based `A_prod` is better than the earlier trade-based `A` because the product-level availability measure is external to Comtrade. It reduces the critique that trade data are being used to explain trade data. It does not eliminate all concerns: production is not spare capacity, antimony and tungsten use upstream production proxies, and bismuth production is constrained by refining and byproduct economics.")
    add("")
    add("### 4.4 Replacement feasibility")
    add("")
    add(r"\[K_{ip}=O_{ip}\times A^{prod}_{p}\]")
    add("")
    add("### 4.5 Switching and compression pressure")
    add("")
    add(r"\[P^S_{ip}=E_{ip}\times K_{ip}\]")
    add("")
    add(r"\[P^C_{ip}=E_{ip}\times(1-K_{ip})\]")
    add("")
    add(r"\[P^X_{ip}=E_{ip}\]")
    add("")
    add(r"The identity is \(P^S_{ip}+P^C_{ip}=E_{ip}\). `P_S` is switchable exposed demand. `P_C` is non-switchable exposed demand. Compression is a residual constraint outcome, not directly observed behavior.")
    add("")
    add("### 4.6 Edge cases")
    add("")
    add("1. China-only supplier: `A=0`, `K=0`, `P_S=0`, `P_C=E`.")
    add("2. Strong RoW supply plus importer access: `K` is high and switching is likely.")
    add("3. RoW supply exists but importer lacks access: `K` remains low and compression/scarcity risk remains.")
    add("4. Importer has access but product is China-dominated: `K` is low or moderate, so partial switching is more plausible than clean replacement.")
    add("")
    add("## 5. Production data construction")
    add("")
    add(md_table(production_table(data), ["Product", "HS", "USGS commodity", "Type", "China production 2023", "World total 2023", "A_prod 2023", "A_prod 2024", "Caveat"]))
    add("")
    add("The 2023 production value is the baseline. The 2024 production value is a robustness check. The earlier trade-A measure remains an appendix comparison. The production mapping is strongest for graphite, acceptable but upstream for antimony and tungsten, and best-available for bismuth using refinery production.")
    add("")
    add("## 6. Pressure-index summary statistics")
    add("")
    add("Pooled clean treated sample:")
    add("")
    add(md_table(pooled_pressure_stats(summary), ["Variable", "mean", "sd", "min", "p25", "median", "p75", "max"]))
    add("")
    add("By product:")
    add("")
    add(md_table(product_pressure_stats(by_product), ["Product", "HS", "N", "Mean E", "Mean O_cap", "A_prod", "Mean K", "Mean P_S", "Mean P_C"]))
    add("")
    add("Correlations:")
    add("")
    add(md_table(correlation_stats(summary, by_product), ["Product/group", "Corr(E,K)", "Corr(P_S,P_C)", "Corr(E,P_S)", "Corr(E,P_C)", "Corr(K,P_C)"]))
    add("")
    add("Interpretation: `P_C` is mechanically close to exposure when `K` is low. `P_S` depends more on importer access and product availability. High correlation does not invalidate the index, but it means full models with both `P_S` and `P_C` should be read as diagnostic rather than as clean structural separation.")
    add("")
    add("## 7. Econometric specifications")
    add("")
    add("### 7.1 Average source-contrast PPML")
    add("")
    add(r"\[\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+FE]\]")
    add("")
    add(r"\[D_{ipst}=China_s\times Treated_p\times Post_{pt}\]")
    add("")
    add("### 7.2 Exposure heterogeneity")
    add("")
    add(r"\[\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+\theta_X(D_{ipst}\times E_{ip})+FE]\]")
    add("")
    add(r"Expected sign: \(\theta_X<0\).")
    add("")
    add("### 7.3 Full pressure source-contrast")
    add("")
    add(r"\[\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+\theta_S(D_{ipst}\times P^S_{ip})+\theta_C(D_{ipst}\times P^C_{ip})+FE]\]")
    add("")
    add(r"Expected signs: \(\theta_S<0\), \(\theta_C<0\). Both `P_S` and `P_C` can predict China-source decline. This model is diagnostic and does not cleanly distinguish switching from compression.")
    add("")
    add("### 7.4 E-K diagnostic model")
    add("")
    add(r"\[\mathbb{E}[M_{ipst}\mid X]=\exp[\beta D_{ipst}+\theta_E(D_{ipst}\times E_{ip})+\theta_K(D_{ipst}\times K_{ip})+FE]\]")
    add("")
    add(r"Expected sign: \(\theta_E<0\). \(\theta_K\) is ambiguous in the China-source equation because replacement feasibility affects where displaced imports go, not only whether China-source imports fall.")
    add("")
    add("### 7.5 RoW switching mechanism")
    add("")
    add(r"\[\mathbb{E}[M^R_{ipt}\mid X]=\exp[\gamma_S(Treated_p\times Post_{pt}\times P^S_{ip})+FE]\]")
    add("")
    add(r"Expected sign: \(\gamma_S>0\). The full version also includes \(P_C\), but `P_C` in the RoW equation is not expected to be the primary switching term.")
    add("")
    add("### 7.6 Total-import compression mechanism")
    add("")
    add(r"\[\mathbb{E}[M^T_{ipt}\mid X]=\exp[\eta_C(Treated_p\times Post_{pt}\times P^C_{ip})+FE]\]")
    add("")
    add(r"Expected sign: \(\eta_C<0\). The full version also includes \(P_S\).")
    add("")
    add("### 7.7 Price wedge")
    add("")
    add(r"\[\pi_{pt}=\log(P^{INT}_{pt})-\log(P^{CN}_{pt})\]")
    add("")
    add("A positive wedge is consistent with segmentation, scarcity, international demand pressure, or domestic-international decoupling. It is not compression-only and is not causal license-denial evidence.")
    add("")
    add("## 8. Full results coverage map")
    add("")
    add(md_table(compact_coverage_table(coverage), ["Result block", "available", "missing/failing", "source", "note"]))
    add("")
    add("The machine-readable version is `RESULT_COVERAGE_AUDIT.csv`. Missing cells usually mean no row was generated, a term was dropped, or the relevant PPML/event-study fit failed.")
    add("")
    add("## 9. Main quarterly results")
    add("")
    add(main_result_table(quarterly_average, ["group", "anchor", "term", "coef", "p_value", "percent_effect", "n_used", "n_dropped_separation"]))
    add("")
    add("Interpretation: average China-source effects are strong for antimony and bismuth, moderate for graphite, and weak for tungstates/APT. Pooled clean estimates are negative but inherit pooled pretrend concerns.")
    add("")
    add("## 10. Main monthly results")
    add("")
    add(main_result_table(monthly_average, ["group", "anchor", "term", "coef", "p_value", "percent_effect", "n_used", "n_dropped_separation"]))
    add("")
    add("Monthly average results are available for all clean groups and timing anchors in `MAIN_RESULTS.csv`. They should be treated as robustness and timing diagnostics, not the preferred baseline.")
    add("")
    add("## 11. Quarterly exposure and pressure results")
    add("")
    add(main_result_table(quarterly_pressure, result_cols()))
    add("")
    add("Interpretation: `D x E` is negative for all preferred first-full-quarter rows, but precision varies. `D x P_C` is usually negative in source-contrast models. `D x P_S` is mixed. This supports the theory more through sign patterns and mechanisms than through uniformly significant interaction terms.")
    add("")
    add("## 12. Monthly exposure and pressure results")
    add("")
    add(main_result_table(monthly_pressure, result_cols(), max_rows=160))
    add("")
    add("The complete monthly pressure table is included in `MAIN_RESULTS.csv`. Monthly interactions should be used to test stability, not to replace the quarterly baseline unless the thesis explicitly changes its timing convention.")
    add("")
    add("## 13. Quarterly mechanism results")
    add("")
    add("### 13.1 RoW switching")
    add("")
    add(main_result_table(q_mech[q_mech["model"].isin(["row_switch_only", "row_full_PS_PC"])], result_cols()))
    add("")
    add("### 13.2 Total imports")
    add("")
    add(main_result_table(q_mech[q_mech["model"].isin(["total_compress_only", "total_full_PS_PC"])], result_cols()))
    add("")
    add("Switching is the strongest mechanism. Compression is product-specific. Full RoW `P_C` coefficients can be positive, so the reviewer should not read `P_C` as mechanically implying no RoW movement.")
    add("")
    add("## 14. Monthly mechanism results")
    add("")
    add(main_result_table(m_mech, result_cols(), max_rows=160))
    add("")
    add("The complete monthly mechanism table is included in `MECHANISMS.csv`. If any monthly mechanism was dropped, it appears in `MODEL_WARNINGS.txt` or the coverage audit.")
    add("")
    add("## 15. Event-study results")
    add("")
    add("### 15.1 Average event study")
    add("")
    add(main_result_table(event_joint[event_joint["model"].eq("average_event_study")], ["frequency", "model", "group", "anchor", "term", "p_value", "joint_df", "n_used", "n_dropped_separation"], max_rows=120))
    add("")
    add("### 15.2 Pressure-gradient event study")
    add("")
    add(main_result_table(event_joint[event_joint["model"].eq("pressure_gradient_event_study")], ["frequency", "model", "group", "anchor", "gradient", "term", "p_value", "joint_df", "n_used", "n_dropped_separation"], max_rows=160))
    add("")
    add("Full coefficient rows are in `EVENT_STUDY.csv` and `EVENT_STUDY_MECHANISMS.csv`. Main warning: pooled source-contrast pretrends are problematic; antimony is borderline; tungstates/APT fail important timing checks.")
    add("")
    add("## 16. Placebo tests")
    add("")
    add(md_table(placebo_summary, ["group", "frequency", "model", "any p < 0.05", "strongest", "interpretation"], max_rows=160))
    add("")
    add("If a placebo coefficient is positive, it does not mimic the final negative treatment effect. It still indicates pre-dynamics or pressure-gradient behavior that weakens a clean timing story. Antimony and some wave 4 pressure placebo rows require caution.")
    add("")
    add("## 17. Robustness checks")
    add("")
    add("### 17.1 Quarterly vs monthly comparison")
    add("")
    q = compact_average(main, "quarterly", "first_full_post_quarter")[["group", "coef", "p_value", "percent_effect"]].rename(columns={"coef": "quarterly_coef", "p_value": "quarterly_p", "percent_effect": "quarterly_effect"})
    m = compact_average(main, "monthly", "first_full_post_quarter")[["group", "coef", "p_value", "percent_effect"]].rename(columns={"coef": "monthly_coef", "p_value": "monthly_p", "percent_effect": "monthly_effect"})
    qm = q.merge(m, on="group", how="outer")
    qm["agreement"] = np.where(np.sign(qm["quarterly_coef"]) == np.sign(qm["monthly_coef"]), "same sign", "different or missing")
    add(table_from_df(qm, ["group", "quarterly_coef", "quarterly_p", "quarterly_effect", "monthly_coef", "monthly_p", "monthly_effect", "agreement"]))
    add("")
    add("### 17.2 Net-weight robustness")
    add("")
    add(main_result_table(robustness[robustness["report_module"].eq("net_weight")], result_cols(), max_rows=120))
    add("")
    add("### 17.3 U.S.-excluded results")
    add("")
    add(main_result_table(robustness[robustness["report_module"].str.startswith("us_excluded", na=False)], result_cols(), max_rows=160))
    add("")
    add("### 17.4 U.S. interactions")
    add("")
    add(main_result_table(robustness[robustness["report_module"].eq("us_interactions")], result_cols(), max_rows=120))
    add("")
    add("### 17.5 Alternative access definitions")
    add("")
    access = main[main["model"].eq("source_contrast_PS_PC") & main["frequency"].eq("quarterly") & main["anchor"].eq("first_full_post_quarter")]
    add(main_result_table(access, result_cols(), max_rows=120))
    add("")
    add("### 17.6 A_prod 2024 robustness")
    add("")
    add(main_result_table(robustness[robustness["report_module"].str.contains("prodA_2024", na=False)], result_cols(), max_rows=120))
    add("")
    add("### 17.7 trade-A vs production-A")
    add("")
    trade = robustness[robustness["report_module"].eq("tradeA_vs_prodA")]
    add(table_from_df(trade, ["group", "model", "comparison_term", "tradeA_coef", "tradeA_p_value", "prodA_coef", "prodA_p_value", "prodA_matches_expected_sign"], max_rows=120))
    add("")
    add("## 18. Price-wedge diagnostics")
    add("")
    add(table_from_df(price, ["model", "pair_id", "family", "hs", "role", "coef", "p_value", "percent_change", "nobs", "mean_pre_wedge", "mean_post_wedge", "avg_E_china", "avg_K_cap_prod", "avg_P_S_cap_prod", "avg_P_C_cap_prod"], max_rows=120))
    add("")
    add("Antimony and bismuth have strong positive wedges. Graphite is negative or weak. Tungsten APT/tungstates are benchmark-sensitive and negative in the main pair. Gallium/germanium are supportive but outside the clean baseline because the HS mapping is bundled or partial.")
    add("")
    add("## 19. Product-by-product critical interpretation")
    add("")
    add(md_table(classify_product_rows(classification), ["Product", "Average effect", "Switching", "Compression", "Price wedge", "Timing", "Strict classification"]))
    add("")
    add("### 19.1 Natural graphite")
    add("")
    add("Keep the average quarterly result as moderate/suggestive, the positive RoW switching mechanism, the negative total compression coefficient, and clean timing diagnostics. Move weaker monthly and alternative-access details to appendix. Main caveat: price wedge does not support segmentation.")
    add("")
    add("### 19.2 Antimony metal")
    add("")
    add("Keep the strong average effect, strong RoW switching, and strong positive price wedge. State the placebo/pretrend caution directly. Do not claim clean timing identification.")
    add("")
    add("### 19.3 Bismuth metal")
    add("")
    add("Keep the strong average decline and very strong price wedge. Treat quantity mechanisms as weaker. Timing is cleaner than antimony, but the mechanism is not pure switching or pure compression.")
    add("")
    add("### 19.4 Tungstates/APT")
    add("")
    add("Do not classify tungstates/APT as a clean switching case. The average effect is weak, pretrends are bad, switching is weak, compression is wrong-signed, and the price wedge is negative. Use as weak/null or unresolved.")
    add("")
    add("## 20. Which results should remain in the thesis?")
    add("")
    keep_rows = [
        {"Result block": "theory and production-A index", "Keep in main text?": "yes", "Appendix?": "no", "Drop?": "no", "Reason": "central contribution after the defense critique"},
        {"Result block": "average quarterly PPML", "Keep in main text?": "yes", "Appendix?": "no", "Drop?": "no", "Reason": "main quantity result"},
        {"Result block": "D x E model", "Keep in main text?": "yes, compact", "Appendix?": "yes full", "Drop?": "no", "Reason": "tests exposure component"},
        {"Result block": "D x P_S/P_C model", "Keep in main text?": "yes, diagnostic", "Appendix?": "yes full", "Drop?": "no", "Reason": "links theory to China-source heterogeneity but not clean mechanism"},
        {"Result block": "RoW switching model", "Keep in main text?": "yes", "Appendix?": "yes full", "Drop?": "no", "Reason": "strongest mechanism"},
        {"Result block": "total compression model", "Keep in main text?": "yes, cautious", "Appendix?": "yes full", "Drop?": "no", "Reason": "product-specific and weaker"},
        {"Result block": "event study", "Keep in main text?": "yes, diagnostic", "Appendix?": "yes full", "Drop?": "no", "Reason": "needed for timing credibility"},
        {"Result block": "placebo", "Keep in main text?": "yes, compact", "Appendix?": "yes full", "Drop?": "no", "Reason": "reveals antimony and wave concerns"},
        {"Result block": "U.S.-excluded", "Keep in main text?": "yes, compact", "Appendix?": "yes full", "Drop?": "no", "Reason": "addresses bilateral political concern"},
        {"Result block": "U.S. interactions", "Keep in main text?": "no", "Appendix?": "yes", "Drop?": "no", "Reason": "terms are saturated and sometimes fragile"},
        {"Result block": "monthly results", "Keep in main text?": "no, except summary", "Appendix?": "yes", "Drop?": "no", "Reason": "robustness/timing only"},
        {"Result block": "net-weight robustness", "Keep in main text?": "brief", "Appendix?": "yes", "Drop?": "no", "Reason": "quantity reporting varies"},
        {"Result block": "access variants", "Keep in main text?": "brief", "Appendix?": "yes", "Drop?": "no", "Reason": "checks index construction"},
        {"Result block": "A_prod 2024", "Keep in main text?": "brief", "Appendix?": "yes", "Drop?": "no", "Reason": "external availability stability"},
        {"Result block": "trade-A comparison", "Keep in main text?": "no", "Appendix?": "yes", "Drop?": "no", "Reason": "addresses old index and trade-data critique"},
        {"Result block": "price wedges", "Keep in main text?": "yes", "Appendix?": "yes full", "Drop?": "no", "Reason": "important segmentation diagnostic"},
        {"Result block": "pooled clean results", "Keep in main text?": "summary only", "Appendix?": "yes", "Drop?": "no", "Reason": "pooled pretrends fail"},
        {"Result block": "tungsten results", "Keep in main text?": "yes as weak/null", "Appendix?": "yes", "Drop?": "no", "Reason": "important negative/unresolved case"},
    ]
    add(md_table(keep_rows, ["Result block", "Keep in main text?", "Appendix?", "Drop?", "Reason"]))
    add("")
    add("## 21. Do coefficients need to be significant?")
    add("")
    add("Average effects need stronger statistical support because they establish whether there is an observed China-source disruption. Pressure interactions do not all need to be significant if the signs and mechanism patterns are coherent, because `P_S` and `P_C` are decomposed indexes with high mechanical correlation through exposure. RoW switching should have some significant support because it is the strongest mechanism claim. Compression can be weaker because it is residual and product-specific. Price wedges are diagnostic, not causal; significance helps, but a null price wedge for one product does not invalidate quantity mechanisms. Event-study, pretrend, and placebo failures matter more for causal credibility than pressure-index p-values.")
    add("")
    add("## 22. Final critical assessment")
    add("")
    add(md_table([
        {"Dimension": "Theory", "Assessment": "strong-medium", "Reason": "clear mechanism, but pressure indexes remain proxies"},
        {"Dimension": "Data construction", "Assessment": "medium", "Reason": "external production improves design; production is not spare capacity"},
        {"Dimension": "Average effects", "Assessment": "strong for antimony/bismuth, medium for graphite, weak for tungsten", "Reason": "large negative estimates are not uniform"},
        {"Dimension": "Mechanism evidence", "Assessment": "medium", "Reason": "switching strongest; compression weak and product-specific"},
        {"Dimension": "Robustness", "Assessment": "medium", "Reason": "many checks exist, but not all align"},
        {"Dimension": "Causal timing", "Assessment": "medium-weak", "Reason": "pooled and tungsten pretrends; antimony placebo issues"},
        {"Dimension": "Thesis viability", "Assessment": "medium-strong if claims are disciplined", "Reason": "viable mechanism thesis if overclaims are avoided"},
    ], ["Dimension", "Assessment", "Reason"]))
    add("")
    add("## 23. Limitations and reviewer attack points")
    add("")
    add("- No license-level data: the design cannot observe applications, approvals, denials, or processing delays.")
    add("- Production is not capacity: USGS output does not measure spare tradable supply.")
    add("- Upstream production proxies: antimony and tungsten production measures are upstream of the HS trade categories.")
    add("- Byproduct constraints: bismuth production may not respond independently to demand.")
    add("- HS mapping: clean products are baseline; bundled products remain secondary.")
    add("- Comtrade reporting lags: monthly timing can misalign with implementation.")
    add("- Small treated product count: only four clean products carry the main design.")
    add("- PPML separation: several models drop observations.")
    add("- Pooled pretrend failure: pooled results should not be the main causal claim.")
    add("- Antimony placebo issue: strong effects but weak timing cleanliness.")
    add("- Tungsten weak/null: do not force it into a strong mechanism class.")
    add("- Price benchmark uncertainty: domestic and international benchmark matching is imperfect.")
    add("- Pressure indexes still use trade data for `E` and `O`; only `A_prod` is external.")
    add("")
    add("## 24. Final handoff instructions to ChatGPT reviewer")
    add("")
    add("### Prompt for the next ChatGPT 5.5 Pro reviewer")
    add("")
    add("> You are reviewing my master thesis empirical design and results. Read the full dossier and all appendices. Your task is to judge critically and objectively whether the theory is coherent, whether the pressure-index construction is defensible, whether the results align with the hypotheses, which coefficients need to be significant, which results should remain in the main thesis, which should be moved to appendix, and what claims are too strong. Do not rewrite the thesis. Produce an adversarial review memo.")
    add("")
    return "\n".join(lines) + "\n"


def appendix_section(title: str, source: str, df: pd.DataFrame, cols: list[str], max_rows: int = 200) -> str:
    lines = [f"## {title}", "", f"Source CSV: `{source}`", ""]
    lines.append(table_from_df(df, [c for c in cols if c in df.columns], max_rows=max_rows))
    lines.append("")
    return "\n".join(lines)


def build_appendix(csv: dict[str, pd.DataFrame], texts: dict[str, str]) -> str:
    main = csv["MAIN_RESULTS.csv"]
    mech = csv["MECHANISMS.csv"]
    event = csv["EVENT_STUDY.csv"]
    event_mech = csv["EVENT_STUDY_MECHANISMS.csv"]
    placebo = csv["PLACEBO.csv"]
    robust = csv["ROBUSTNESS.csv"]
    price = csv["PRICE_WEDGES.csv"]
    cols = result_cols()
    lines = ["# FULL RESULTS APPENDIX", "", "This appendix keeps the raw result references visible. Large tables show the first rows and point to complete CSV files included in the handoff zip.", ""]
    sections = [
        ("1. Quarterly average PPML", "MAIN_RESULTS.csv", main[(main["frequency"].eq("quarterly")) & main["model"].eq("average_source_contrast")], cols),
        ("2. Monthly average PPML", "MAIN_RESULTS.csv", main[(main["frequency"].eq("monthly")) & main["model"].eq("average_source_contrast")], cols),
        ("3. Quarterly D x E", "MAIN_RESULTS.csv", main[(main["frequency"].eq("quarterly")) & main["model"].eq("source_contrast_E")], cols),
        ("4. Monthly D x E", "MAIN_RESULTS.csv", main[(main["frequency"].eq("monthly")) & main["model"].eq("source_contrast_E")], cols),
        ("5. Quarterly D x P_S/P_C", "MAIN_RESULTS.csv", main[(main["frequency"].eq("quarterly")) & main["model"].eq("source_contrast_PS_PC")], cols),
        ("6. Monthly D x P_S/P_C", "MAIN_RESULTS.csv", main[(main["frequency"].eq("monthly")) & main["model"].eq("source_contrast_PS_PC")], cols),
        ("7. Quarterly E-K", "MAIN_RESULTS.csv", main[(main["frequency"].eq("quarterly")) & main["model"].eq("source_contrast_E_K")], cols),
        ("8. Monthly E-K", "MAIN_RESULTS.csv", main[(main["frequency"].eq("monthly")) & main["model"].eq("source_contrast_E_K")], cols),
        ("9. Quarterly RoW mechanisms", "MECHANISMS.csv", mech[(mech["frequency"].eq("quarterly")) & mech["model"].str.startswith("row", na=False)], cols),
        ("10. Monthly RoW mechanisms", "MECHANISMS.csv", mech[(mech["frequency"].eq("monthly")) & mech["model"].str.startswith("row", na=False)], cols),
        ("11. Quarterly total mechanisms", "MECHANISMS.csv", mech[(mech["frequency"].eq("quarterly")) & mech["model"].str.startswith("total", na=False)], cols),
        ("12. Monthly total mechanisms", "MECHANISMS.csv", mech[(mech["frequency"].eq("monthly")) & mech["model"].str.startswith("total", na=False)], cols),
        ("13. Event-study coefficients", "EVENT_STUDY.csv", event, ["frequency", "model", "group", "anchor", "gradient", "row_type", "term", "coef", "p_value", "percent_effect", "n_used", "n_dropped_separation"]),
        ("14. Mechanism event-study coefficients", "EVENT_STUDY_MECHANISMS.csv", event_mech, ["frequency", "model", "group", "anchor", "row_type", "term", "coef", "p_value", "percent_effect", "n_used", "n_dropped_separation"]),
        ("15. Placebo quarterly", "PLACEBO.csv", placebo[placebo["frequency"].eq("quarterly")], cols + ["placebo_lag_months"]),
        ("16. Placebo monthly", "PLACEBO.csv", placebo[placebo["frequency"].eq("monthly")], cols + ["placebo_lag_months"]),
        ("17. U.S.-excluded", "ROBUSTNESS.csv", robust[robust["report_module"].str.startswith("us_excluded", na=False)], cols + ["sample_restriction"]),
        ("18. U.S. interactions", "ROBUSTNESS.csv", robust[robust["report_module"].eq("us_interactions")], cols + ["sample_restriction"]),
        ("19. Net-weight", "ROBUSTNESS.csv", robust[robust["report_module"].eq("net_weight")], cols),
        ("20. Access variants", "MAIN_RESULTS.csv", main[(main["model"].eq("source_contrast_PS_PC")) & main["pressure_variant"].isin(["capacity", "frequency", "binary"])], cols),
        ("21. 2024 A_prod", "ROBUSTNESS.csv", robust[robust["report_module"].str.contains("prodA_2024", na=False)], cols),
        ("22. trade-A comparison", "ROBUSTNESS.csv", robust[robust["report_module"].eq("tradeA_vs_prodA")], ["group", "model", "comparison_term", "tradeA_term", "tradeA_coef", "tradeA_p_value", "tradeA_percent_effect", "prodA_term", "prodA_coef", "prodA_p_value", "prodA_percent_effect", "prodA_matches_expected_sign"]),
        ("23. Price wedges", "PRICE_WEDGES.csv", price, ["model", "pair_id", "family", "hs", "role", "coef", "p_value", "percent_change", "nobs", "mean_pre_wedge", "mean_post_wedge", "avg_E_china", "avg_K_cap_prod", "avg_P_S_cap_prod", "avg_P_C_cap_prod"]),
    ]
    for title, source, df, columns in sections:
        lines.append(appendix_section(title, source, df, columns))
    lines.append("## 24. Model failures and warnings")
    lines.append("")
    lines.append("Source TXT: `MODEL_WARNINGS.txt` and `REPORT_BUILD_WARNINGS.md`")
    lines.append("")
    lines.append("The complete warning files are included in the handoff package. Summary:")
    lines.append("")
    lines.append(summarize_warnings(texts["MODEL_WARNINGS.txt"]))
    lines.append("")
    return "\n".join(lines)


def summarize_warnings(warnings: str) -> str:
    patterns = {
        "missing pressure/exposure cell messages": r"dropping \d+ treated importer-product cells",
        "edge-case messages": r"pressure edge case",
        "PPML/event/model failure messages": r"failed|failure|singular|covariance",
        "no-variation messages": r"no variation|No variation",
        "separation mentions": r"separation|separated",
    }
    rows = []
    for k, pat in patterns.items():
        rows.append({"Warning category": k, "count": str(len(re.findall(pat, warnings, flags=re.IGNORECASE)))})
    return md_table(rows, ["Warning category", "count"])


def build_manifest(copied: list[Path]) -> str:
    rows = []
    generated = [
        OUT / "MASTER_CRITICAL_REVIEW_DOSSIER.md",
        OUT / "FULL_RESULTS_APPENDIX.md",
        OUT / "FULL_RESULTS_FILE_MANIFEST.md",
        OUT / "RESULT_COVERAGE_AUDIT.csv",
        OUT / "MISSING_OR_FAILED_MODELS.md",
    ]
    for p in generated:
        rows.append(
            {
                "filename": p.name,
                "description": "Generated handoff file",
                "key columns": "n/a",
                "dossier section": "all",
                "role": "main handoff",
            }
        )
    for p in copied:
        rel = p.relative_to(OUT)
        desc = "source result file"
        cols = ""
        if p.suffix.lower() == ".csv":
            try:
                df = pd.read_csv(p, nrows=0)
                cols = ", ".join(list(df.columns)[:12])
                desc = f"CSV result source ({p.parent.name})"
            except Exception:
                cols = "unreadable/empty"
        elif p.suffix.lower() == ".txt":
            desc = "model warning text"
        elif p.suffix.lower() == ".md":
            desc = "source markdown report or notes"
        rows.append(
            {
                "filename": str(rel),
                "description": desc,
                "key columns": cols,
                "dossier section": "referenced by source name",
                "role": "main" if "full_thesis_report" in str(rel) else "appendix/diagnostic",
            }
        )
    return "# FULL RESULTS FILE MANIFEST\n\n" + md_table(rows, ["filename", "description", "key columns", "dossier section", "role"]) + "\n"


def build_missing_or_failed(coverage: pd.DataFrame, texts: dict[str, str]) -> str:
    missing = coverage[~coverage["exists"]].copy()
    lines = ["# MISSING OR FAILED MODELS", ""]
    if missing.empty:
        lines.append("No expected result block in the coverage audit is completely missing. Some individual fits still have warnings, separation, missing pressure cells, or event-study failures.")
    else:
        lines.append("Coverage-audit missing rows:")
        lines.append("")
        lines.append(table_from_df(missing, ["result_block", "frequency", "model_type", "group", "timing_anchor", "failure_reason", "notes"], max_rows=200))
    lines.append("")
    lines.append("## Missing file")
    lines.append("")
    required = ["THEORY.md", "DATA_AUDIT.csv", "SUMMARY_STATS.csv", "MAIN_RESULTS.csv", "MECHANISMS.csv", "EVENT_STUDY.csv", "PLACEBO.csv", "ROBUSTNESS.csv", "PRICE_WEDGES.csv", "MODEL_WARNINGS.txt"]
    missing_files = [name for name in required if not (SOURCE_DIRS[0] / name).exists()]
    lines.append("None." if not missing_files else "\n".join(f"- `{m}`" for m in missing_files))
    lines.append("")
    lines.append("## Warning summary")
    lines.append("")
    lines.append(summarize_warnings(texts["MODEL_WARNINGS.txt"]))
    lines.append("")
    lines.append("## Main known failures and caveats")
    lines.append("")
    lines.append("- Wide-panel pooled China/RoW/total event studies failed with singular covariance matrices. Product and wave-level rows exist.")
    lines.append("- PPML separation occurs in many models; separation counts are reported in the result CSVs.")
    lines.append("- Some importer-product pressure cells are missing because pre-policy exposure is undefined.")
    lines.append("- Event-study no-variation cases and demeaning/covariance failures are recorded in `MODEL_WARNINGS.txt`.")
    lines.append("- Antimony has placebo/pretrend concerns. Tungstates/APT have weak effects and bad timing diagnostics.")
    lines.append("")
    lines.append("## Why it matters")
    lines.append("")
    lines.append("These failures do not make the whole project unusable. They determine which claims are safe. Product-level evidence should carry more weight than pooled claims. Antimony should be presented with timing caveats. Tungstates/APT should be weak/null or unresolved.")
    lines.append("")
    return "\n".join(lines)


def write_zip() -> None:
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            if p == ZIP_OUT or p.is_dir():
                continue
            z.write(p, p.relative_to(OUT))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if SOURCE_COPY.exists():
        shutil.rmtree(SOURCE_COPY)
    copied = copy_source_files()
    csv, texts = load_all()
    coverage = build_coverage(csv)
    coverage.to_csv(OUT / "RESULT_COVERAGE_AUDIT.csv", index=False)
    (OUT / "MASTER_CRITICAL_REVIEW_DOSSIER.md").write_text(build_master(csv, texts, coverage), encoding="utf-8")
    (OUT / "FULL_RESULTS_APPENDIX.md").write_text(build_appendix(csv, texts), encoding="utf-8")
    (OUT / "MISSING_OR_FAILED_MODELS.md").write_text(build_missing_or_failed(coverage, texts), encoding="utf-8")
    manifest = build_manifest(copied)
    (OUT / "FULL_RESULTS_FILE_MANIFEST.md").write_text(manifest, encoding="utf-8")
    write_zip()
    print(f"Wrote {OUT}")
    print(f"Wrote {ZIP_OUT}")


if __name__ == "__main__":
    main()
