"""
Exporter-ITS decision (Part 13) + donor/leave-one-out appendix tables (Parts 5C, 6C).
"""
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "03_data" / "output" / "tables"
DRAFT = REPO / "05_draft"


def exporter_its_decision():
    its = pd.read_csv(OUT / "thesis_exporter_its_results.csv")
    rows = []
    for _, r in its.iterrows():
        rows.append({
            "product": r["product"],
            "label": r["label"],
            "break_date": r["implementation"],
            "post_effect_pct": round(r["percent_effect"], 2),
            "hac_p": round(r["p_hac_6"], 4),
            "reported_months": int(r["reported_months"]),
            "total_months": int(r["months"]),
            "zero_or_no_record_months": int(r["zero_or_no_record_months"]),
            "caveat": "descriptive only; no untreated counterfactual; not causal; "
                      "missing export records coded as zero can mechanically affect log1p",
        })
    pd.DataFrame(rows).to_csv(OUT / "term_exporter_its_decision.csv", index=False)
    rec = ("KEEP_AS_FOOTNOTE_OR_CUT: The ITS uses China-reported exports with "
           "15-18 missing months coded as zero for most products and only 27/87 "
           "months reported for HS 261710. The log1p outcome mechanically drives "
           "the -99% to -99.99% estimates. For a term paper, CUT the prose "
           "mention or reduce to a one-sentence footnote; do NOT add as a table "
           "in the main text. If kept, label explicitly as descriptive timing "
           "check with no untreated counterfactual.")
    with open(OUT / "term_exporter_its_decision.csv", "a") as f:
        f.write(f"\nRECOMMENDATION,{rec}\n")
    # optional appendix table
    lines = [
        r"\begin{table}[H]", r"\centering",
        r"\caption{Descriptive exporter-side interrupted-time-series (ITS) on",
        r"China-reported aggregate exports. \textbf{Descriptive only:} no",
        r"untreated counterfactual; not a causal design. The dependent variable",
        r"is $\ln(1+\text{exports})$; months with no export record are coded as",
        r"zero, which can mechanically depress the $\ln(1+\cdot)$ series for",
        r"late and sparse products. HAC SE with 6 lags. Source:",
        r"\texttt{thesis\_exporter\_its\_results.csv}.}",
        r"\label{tab:exporter_its}", r"\footnotesize",
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"HS & Product & Break & Effect (\%) & HAC $p$ & Reported/total mo.\\",
        r"\midrule",
    ]
    for r in rows:
        pct = r["post_effect_pct"]
        sign = "-" if pct < 0 else "+"
        p = r["hac_p"]
        pstr = "$<0.001$" if p < 0.001 else f"${p:.3f}$"
        lines.append(
            f"{r['product']} & {r['label']} & {r['break_date']} & "
            f"${sign}{abs(pct):.1f}$ & {pstr} & "
            f"{r['reported_months']}/{r['total_months']} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (DRAFT / "appendix_exporter_its.tex").write_text("\n".join(lines))
    print("wrote exporter_its_decision.csv + appendix_exporter_its.tex")


def donor_appendix():
    df = pd.read_csv(OUT / "term_donor_pool_sensitivity_hs282580.csv")
    lines = [
        r"\begin{table}[H]", r"\centering",
        r"\caption{Donor-pool sensitivity for HS 282580 antimony oxides. Each row",
        r"re-estimates the source-split PPML triple difference with a different",
        r"set of control products. \textbf{Conditional robustness only}: the",
        r"exact product-assignment $p$-value floor worsens as controls are",
        r"removed ($1/4 \to 1/3 \to 1/2$). Reporter-clustered $p$-values are",
        r"conditional diagnostics. Source:",
        r"\texttt{term\_donor\_pool\_sensitivity\_hs282580.csv}.}",
        r"\label{tab:donor_sensitivity}", r"\footnotesize",
        r"\begin{tabular}{lcrrrrr}",
        r"\toprule",
        r"Controls & $N_{ctrl}$ & Effect (\%) & Reporter $p$ & Pretrend $p$ & Exact floor & $N$ \\",
        r"\midrule",
    ]
    label_map = {
        "baseline_3ctrl": "2818, 8111, 2811",
        "drop_2818": "8111, 2811",
        "drop_8111": "2818, 2811",
        "drop_2811": "2818, 8111",
        "only_2818": "2818 only",
        "only_8111": "8111 only",
        "only_2811": "2811 only",
    }
    for _, r in df.iterrows():
        pct = r["percent_effect"]
        sign = "-" if pct < 0 else "+"
        def fp(x):
            return "$<0.001$" if x < 0.001 else f"${x:.3f}$"
        lines.append(
            f"{label_map.get(r['config'], r['config'])} & {int(r['n_controls'])} & "
            f"${sign}{abs(pct):.1f}$ & {fp(r['p_reporter'])} & "
            f"{fp(r['pretrend_p'])} & ${r['exact_p_floor']:.3f}$ & {int(r['nobs'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (DRAFT / "appendix_donor_sensitivity_hs282580.tex").write_text("\n".join(lines))
    print("wrote appendix_donor_sensitivity_hs282580.tex")


def loro_appendix():
    full = pd.read_csv(OUT / "term_leave_one_reporter_hs282580.csv")
    summ = pd.read_csv(OUT / "term_leave_one_reporter_summary_hs282580.csv")
    numeric = full.dropna(subset=["percent_effect"]).copy()
    # top 5 most influential
    numeric = numeric.sort_values("percent_effect")
    strongest = numeric.head(3)  # most negative when dropped = weakening most
    weakest = numeric.tail(3)
    s = summ.iloc[0]
    lines = [
        r"\begin{table}[H]", r"\centering",
        r"\caption{Leave-one-reporter-out influence for HS 282580 antimony",
        r"oxides. Each row drops one of the 53 reporters and re-estimates the",
        r"source-split PPML triple difference. Reporter-clustered $p$-values",
        r"are conditional diagnostics. Source:",
        r"\texttt{term\_leave\_one\_reporter\_hs282580.csv}.}",
        r"\label{tab:loro}", r"\footnotesize",
        r"\begin{tabular}{lr}",
        r"\toprule",
        r"Statistic & Value \\", r"\midrule",
        f"Baseline effect & $-81.5\\%$ \\\\",
        f"Min LOO effect & ${s['min_loo_pct']:.1f}\\%$ \\\\",
        f"Max LOO effect & ${s['max_loo_pct']:.1f}\\%$ \\\\",
        f"Median LOO effect & ${s['median_loo_pct']:.1f}\\%$ \\\\",
        f"LOO still $< -50\\%$ & {int(s['n_below_minus50'])}/{int(s['n_total'])} \\\\",
        f"LOO still $< -75\\%$ & {int(s['n_below_minus75'])}/{int(s['n_total'])} \\\\",
        f"Failed models & {int(s['n_failed'])} \\\\",
        r"\bottomrule", r"\end{tabular}", r"\end{table}", "",
        r"\smallskip",
        r"\footnotesize Dropping the reporter that most strengthens the",
        f"effect is reporter \\texttt{{{s['reporter_most_strengthening']}}}; "
        f"dropping reporter \\texttt{{{s['reporter_most_weakening']}}} most "
        r"weakens it. The effect stays negative and below $-50\%$ in every "
        r"leave-one-out permutation.",
        "",
    ]
    (DRAFT / "appendix_leave_one_reporter_hs282580.tex").write_text("\n".join(lines))
    print("wrote appendix_leave_one_reporter_hs282580.tex")


if __name__ == "__main__":
    exporter_its_decision()
    donor_appendix()
    loro_appendix()
