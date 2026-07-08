"""
Generate corrected LaTeX table files and check CSVs for Parts 3, 4, 10.

Reads existing thesis_*.csv outputs and writes:
  05_draft/t5_eventstudy_corrected.tex       (Part 3)
  05_draft/t4_main_ddd_corrected.tex         (Part 4)
  05_draft/t8_eurostat_corrected.tex         (Part 10)
  output/tables/term_eventstudy_baseline_check.csv
  output/tables/term_table4_exact_rank_check.csv
  output/tables/term_eurostat_cn8_check.csv
"""
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "03_data" / "output" / "tables"
DRAFT = REPO / "05_draft"


def fmt_p(p):
    if pd.isna(p):
        return "---"
    if p < 0.001:
        return "$<0.001$"
    return f"${p:.3f}$"


def part3_eventstudy():
    ev = pd.read_csv(OUT / "thesis_event_study_results.csv")
    sub = ev[(ev["model"] == "PPML DDD event study") &
             (ev["sample"].str.contains("282580"))].copy()
    # the omitted baseline is m3 (sample label says baseline=m3)
    baseline = "m3"
    order = [
        ("event_m13_or_earlier", "m13 or earlier"),
        ("event_m12_to_m7", "m12 to m7"),
        ("event_m6_to_m4", "m6 to m4"),
        ("event_m3", "m3 (base)"),
        ("event_m2", "m2"),
        ("event_m1", "m1"),
        ("event_p0", "p0"),
        ("event_p1", "p1"),
        ("event_p2", "p2"),
        ("event_p3", "p3"),
        ("event_p4_to_p6", "p4 to p6"),
        ("event_p7_to_p12", "p7 to p12"),
        ("event_p13_or_later", "p13 or later"),
    ]
    rows_by_term = {r["term"]: r for _, r in sub.iterrows()}

    # check CSV
    chk = []
    for term, label in order:
        if term in rows_by_term:
            r = rows_by_term[term]
            chk.append({"term": term, "label": label, "beta": r["beta"],
                        "percent_effect": r["percent_effect"],
                        "se_reporter_cluster": r["se_reporter_cluster"],
                        "p_reporter_cluster": r["p_reporter_cluster"],
                        "is_baseline": term == "event_m3"})
        else:
            chk.append({"term": term, "label": label, "beta": None,
                        "percent_effect": None, "se_reporter_cluster": None,
                        "p_reporter_cluster": None, "is_baseline": term == "event_m3"})
    pd.DataFrame(chk).to_csv(OUT / "term_eventstudy_baseline_check.csv", index=False)

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Event-study coefficients for the main case, HS 282580 antimony",
        r"oxides, from the source-\emph{split} PPML triple difference. The omitted",
        r"baseline is event month \textbf{m3} (three months before the expected",
        r"import-effect month, 2024-10). Months are relative to the expected",
        r"import-effect month. Reporter-clustered $p$-values are conditional",
        r"diagnostics (Section~\ref{sec:inference}). Source:",
        r"\texttt{thesis\_event\_study\_results.csv}.}",
        r"\label{tab:eventstudy}",
        r"\footnotesize",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        r"Event window & Effect (\%) & Reporter $p$ \\",
        r"\midrule",
    ]
    for term, label in order:
        if term == "event_m3":
            lines.append(f"{label:24s} & \\multicolumn{{1}}{{c}}{{---}} & --- \\\\")
        elif term in rows_by_term:
            r = rows_by_term[term]
            pct = r["percent_effect"]
            sign = "-" if pct < 0 else "+"
            lines.append(f"{label:24s} & ${sign}{abs(pct):.1f}$ & {fmt_p(r['p_reporter_cluster'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (DRAFT / "t5_eventstudy_corrected.tex").write_text("\n".join(lines) + "\n")
    print("wrote t5_eventstudy_corrected.tex (baseline = m3)")


def part4_main_ddd():
    ppml = pd.read_csv(OUT / "thesis_ppml_results.csv")
    pretr = pd.read_csv(OUT / "thesis_event_pretrend_tests.csv")
    ddd = ppml[ppml["model"] == "PPML DDD"].copy()
    pt_map = {r["sample"]: r["joint_pretrend_p_reporter_cluster"]
              for _, r in pretr.iterrows()}

    label_map = {
        "2504":   ("Natural graphite", "Suggestive"),
        "811292": ("Unwrought other-metals bundle", "No aggregate negative effect"),
        "282560": ("GeO$_2$/ZrO$_2$", "No aggregate negative effect"),
        "8110":   ("Antimony metal", "Consistent; pretrends fail"),
        "261710": ("Antimony ores/conc.", "Descriptive only"),
        "282580": ("Antimony oxides", "Central result"),
    }
    chk_rows = []
    for _, r in ddd.iterrows():
        hs = r["sample"].split(" ")[0]
        pt = pt_map.get(hs, float("nan"))
        chk_rows.append({
            "hs": hs, "product": label_map[hs][0],
            "beta": r["beta"], "percent_effect": r["percent_effect"],
            "p_reporter_cluster": r["p_reporter_cluster"],
            "placebo_assignment_rank_p": r["placebo_assignment_rank_p"],
            "minimum_exact_product_p": r["minimum_exact_product_p"],
            "pretrend_p": pt, "nobs": r["nobs"],
        })
    pd.DataFrame(chk_rows).to_csv(OUT / "term_table4_exact_rank_check.csv", index=False)

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Main source-\emph{split} PPML triple-difference results. The",
        r"dependent variable is monthly bilateral import value in USD. The reported",
        r"effect is $100(\exp\hat\beta-1)$ for the",
        r"\textit{Treated}$\times$\textit{China}$\times$\textit{Post} interaction,",
        r"with standard errors clustered by reporter. ``Exact rank $p$'' is the",
        r"exact product-assignment rank $p$-value over the four possible",
        r"single-product assignments (floor $1/4=0.25$); reporter-clustered",
        r"$p$-values are conditional diagnostics, not product-level assignment",
        r"inference (Section~\ref{sec:inference}). ``Pretrend $p$'' is the joint",
        r"$p$-value of the pre-period event-time coefficients. Source:",
        r"\texttt{thesis\_ppml\_results.csv}, \texttt{thesis\_event\_pretrend\_tests.csv}.}",
        r"\label{tab:main_ddd}",
        r"\footnotesize",
        r"\begin{tabular}{llrrrrl}",
        r"\toprule",
        r"HS-6 & Product & Effect (\%) & Reporter $p$ & Exact rank $p$ & Pretrend $p$ & Assessment \\",
        r"\midrule",
    ]
    order = ["2504", "811292", "282560", "8110", "261710", "282580"]
    for hs in order:
        r = next(row for _, row in ddd.iterrows() if row["sample"].startswith(hs))
        label, assess = label_map[hs]
        pct = r["percent_effect"]
        sign = "-" if pct < 0 else "+"
        pt = pt_map.get(hs, float("nan"))
        lines.append(
            f"{hs} & {label} & ${sign}{abs(pct):.1f}$ & "
            f"{fmt_p(r['p_reporter_cluster'])} & "
            f"{fmt_p(r['placebo_assignment_rank_p'])} & "
            f"{fmt_p(pt)} & {assess} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (DRAFT / "t4_main_ddd_corrected.tex").write_text("\n".join(lines) + "\n")
    print("wrote t4_main_ddd_corrected.tex (added Exact rank p column, source-split, 811292 label)")


def part10_eurostat():
    ppml = pd.read_csv(OUT / "thesis_ppml_results.csv")
    eu = ppml[ppml["model"].isin(["Eurostat CN8 PPML DDD",
                                  "Eurostat CN8 pooled PPML DDD"])].copy()
    eu_rows = []
    for _, r in eu.iterrows():
        sample = r["sample"]
        if "Ga/Ge" in sample:
            label = "Pooled Ga/Ge vs In/V"
            minp = 1.0 / 6
        elif sample.startswith("Ga"):
            label = "Ga vs In/V"
            minp = 1.0 / 3
        else:
            label = "Ge vs In/V"
            minp = 1.0 / 3
        eu_rows.append({"comparison": label, "beta": r["beta"],
                        "percent_effect": r["percent_effect"],
                        "p_reporter_cluster": r["p_reporter_cluster"],
                        "exact_min_p": minp, "nobs": r["nobs"]})
    pd.DataFrame(eu_rows).to_csv(OUT / "term_eurostat_cn8_check.csv", index=False)

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Eurostat CN8 case-study results for gallium and germanium",
        r"within the HS 811292 unwrought bundle, using indium and vanadium as",
        r"within-bundle comparators on the balanced current-EU27 panel (27",
        r"countries, 72 months, 2019-01 to 2024-12). Dependent variable is monthly",
        r"import value in EUR. CN8 codes used: gallium 81129289, germanium",
        r"81129295, indium 81129281, vanadium 81129291. The minimum exact",
        r"product-assignment $p$-value is $1/3\approx 0.333$ for the two",
        r"single-metal comparisons (one treated of three products) and",
        r"$1/6\approx 0.167$ for the pooled comparison (two treated of four).",
        r"Reporter-clustered $p$-values are conditional. Source:",
        r"\texttt{thesis\_ppml\_results.csv}.}",
        r"\label{tab:eurostat}",
        r"\footnotesize",
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Comparison & Effect (\%) & Reporter $p$ & Exact min.\ $p$ \\",
        r"\midrule",
    ]
    for r in eu_rows:
        pct = r["percent_effect"]
        sign = "-" if pct < 0 else "+"
        lines.append(
            f"{r['comparison']:24s} & ${sign}{abs(pct):.1f}$ & "
            f"{fmt_p(r['p_reporter_cluster'])} & ${r['exact_min_p']:.3f}$ \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (DRAFT / "t8_eurostat_corrected.tex").write_text("\n".join(lines) + "\n")
    print("wrote t8_eurostat_corrected.tex (CN8 codes + 1/6 pooled p)")


if __name__ == "__main__":
    part3_eventstudy()
    part4_main_ddd()
    part10_eurostat()
