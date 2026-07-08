"""
Generate the two HS 282580 figures for the term paper.

  05_draft/figures/hs282580_source_trends_indexed.{pdf,png}   (Part 7)
  05_draft/figures/hs282580_eventstudy.{pdf,png}              (Part 8)
  05_draft/fig_hs282580_source_trends.tex
  05_draft/fig_hs282580_eventstudy.tex
  output/tables/term_hs282580_source_trends_indexed.csv
  output/tables/term_hs282580_eventstudy_plot_data.csv

Uses matplotlib only (no seaborn). Reads existing processed/output CSVs.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "03_data" / "output" / "tables"
FIGS = REPO / "05_draft" / "figures"
DRAFT = REPO / "05_draft"
SOURCE = REPO / "03_data" / "processed" / "comtrade_thesis_source_panel.csv"
IMPORT_EFFECT = "202410"


def _month_label(p):
    return f"{p[:4]}-{p[4:]}"


def source_trends():
    sp = pd.read_csv(SOURCE, dtype={"hs": str, "period": str})
    sub = sp[sp["hs"] == "282580"].copy()
    agg = sub.groupby(["period", "source"])["trade_value_usd"].sum().unstack("source").fillna(0)
    agg = agg.sort_index()
    if "China" not in agg.columns:
        agg["China"] = 0.0
    if "RestOfWorld" not in agg.columns:
        agg["RestOfWorld"] = 0.0
    agg["Total"] = agg["China"] + agg["RestOfWorld"]

    pre_mask = agg.index < IMPORT_EFFECT
    base = {col: agg.loc[pre_mask, col].mean() for col in ["China", "RestOfWorld", "Total"]}
    idx = agg.copy()
    for col in ["China", "RestOfWorld", "Total"]:
        idx[col] = 100.0 * agg[col] / base[col] if base[col] > 0 else np.nan

    idx = idx.reset_index()
    idx["month_label"] = idx["period"].map(_month_label)
    idx[["period", "month_label", "China", "RestOfWorld", "Total"]].to_csv(
        OUT / "term_hs282580_source_trends_indexed.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = np.arange(len(idx))
    ax.plot(x, idx["China"], color="#c0392b", lw=1.8, label="China")
    ax.plot(x, idx["RestOfWorld"], color="#2980b9", lw=1.8, label="ROW")
    ax.plot(x, idx["Total"], color="#2c3e50", lw=1.4, ls="--", label="Total")
    ie_pos = int(np.where(idx["period"].values == IMPORT_EFFECT)[0][0])
    ax.axvline(ie_pos, color="k", ls=":", lw=1.0)
    ax.text(ie_pos + 0.5, ax.get_ylim()[1] * 0.95, "import-effect\n2024-10",
            fontsize=7, va="top")
    tick_step = 6
    ticks = x[::tick_step]
    ax.set_xticks(ticks)
    ax.set_xticklabels([idx["month_label"].iloc[i] for i in ticks], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Monthly import value (pre mean = 100)")
    ax.set_title("HS 282580 antimony oxides: China vs ROW import value, indexed")
    ax.axhline(100, color="grey", lw=0.6, alpha=0.5)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGS / f"hs282580_source_trends_indexed.{ext}", dpi=160)
    plt.close(fig)

    (DRAFT / "fig_hs282580_source_trends.tex").write_text(
        r"\begin{figure}[H]" "\n"
        r"\centering" "\n"
        r"\includegraphics[width=0.95\linewidth]{figures/hs282580_source_trends_indexed.pdf}" "\n"
        r"\caption{HS 282580 antimony oxides. Monthly import value (in USD, not" "\n"
        r"quantities) aggregated across all 53 reporters, indexed to the pre-period" "\n"
        r"mean (months before the expected import-effect month 2024-10) = 100." "\n"
        r"Visual diagnostic only; the figure is descriptive and does not identify a" "\n"
        r"causal effect. Source: \texttt{term\_hs282580\_source\_trends\_indexed.csv}.}" "\n"
        r"\label{fig:hs282580_trends}" "\n"
        r"\end{figure}" "\n")
    print("wrote source-trends figure + tex")


def eventstudy_figure():
    ev = pd.read_csv(OUT / "thesis_event_study_results.csv")
    sub = ev[(ev["model"] == "PPML DDD event study") &
             (ev["sample"].str.contains("282580"))].copy()

    bin_order = [
        ("event_m13_or_earlier", "m<=-13", -13),
        ("event_m12_to_m7", "m-12..-7", -9.5),
        ("event_m6_to_m4", "m-6..-4", -5),
        ("event_m3", "m-3 (base)", -3),
        ("event_m2", "m-2", -2),
        ("event_m1", "m-1", -1),
        ("event_p0", "p0", 0),
        ("event_p1", "p1", 1),
        ("event_p2", "p2", 2),
        ("event_p3", "p3", 3),
        ("event_p4_to_p6", "p4..6", 5),
        ("event_p7_to_p12", "p7..12", 9.5),
        ("event_p13_or_later", "p>=13", 13),
    ]
    rows = []
    for term, label, xpos in bin_order:
        if term == "event_m3":
            rows.append({"term": term, "label": label, "xpos": xpos,
                         "percent_effect": 0.0, "ci_lo": np.nan, "ci_hi": np.nan,
                         "is_baseline": True})
        else:
            r = sub[sub["term"] == term]
            if len(r):
                r = r.iloc[0]
                pct = r["percent_effect"]
                se = r["se_reporter_cluster"]
                rows.append({"term": term, "label": label, "xpos": xpos,
                             "percent_effect": pct,
                             "ci_lo": 100 * (np.exp(r["beta"] - 1.96 * se) - 1),
                             "ci_hi": 100 * (np.exp(r["beta"] + 1.96 * se) - 1),
                             "is_baseline": False})
    plot = pd.DataFrame(rows)
    plot.to_csv(OUT / "term_hs282580_eventstudy_plot_data.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    nonbase = plot[~plot["is_baseline"]]
    base = plot[plot["is_baseline"]].iloc[0]
    ax.errorbar(nonbase["xpos"], nonbase["percent_effect"],
                yerr=[nonbase["percent_effect"] - nonbase["ci_lo"],
                      nonbase["ci_hi"] - nonbase["percent_effect"]],
                fmt="o", color="#c0392b", ecolor="#c0392b", elinewidth=1.0,
                capsize=2, ms=4, label="coef +/- 1.96 SE")
    ax.scatter([base["xpos"]], [0], marker="s", color="#2c3e50", s=30, zorder=5,
               label="m-3 (omitted base)")
    ax.axvline(0, color="k", ls=":", lw=1.0)
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_xticks([r["xpos"] for r in bin_order if False] or plot["xpos"])
    ax.set_xticklabels(plot["label"], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Percent effect vs m-3 baseline")
    ax.set_title("HS 282580 antimony oxides: source-split PPML event study")
    ax.legend(loc="lower left", frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGS / f"hs282580_eventstudy.{ext}", dpi=160)
    plt.close(fig)

    (DRAFT / "fig_hs282580_eventstudy.tex").write_text(
        r"\begin{figure}[H]" "\n"
        r"\centering" "\n"
        r"\includegraphics[width=0.95\linewidth]{figures/hs282580_eventstudy.pdf}" "\n"
        r"\caption{HS 282580 antimony oxides. Source-split PPML triple-difference" "\n"
        r"event-study coefficients (percent effect relative to the omitted m-3" "\n"
        r"baseline), with 95\% reporter-clustered confidence intervals. Event time" "\n"
        r"is relative to the expected import-effect month 2024-10." "\n"
        r"Reporter-clustered intervals are conditional diagnostics. Source:" "\n"
        r"\texttt{term\_hs282580\_eventstudy\_plot\_data.csv}.}" "\n"
        r"\label{fig:hs282580_eventstudy}" "\n"
        r"\end{figure}" "\n")
    print("wrote event-study figure + tex")


if __name__ == "__main__":
    FIGS.mkdir(parents=True, exist_ok=True)
    source_trends()
    eventstudy_figure()
