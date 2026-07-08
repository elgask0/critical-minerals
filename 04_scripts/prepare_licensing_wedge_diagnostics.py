"""
Reproduce the orphan licensing-wedge diagnostics from live data.

Outputs:
  thesis_regularity_diagnostics_live.csv
  thesis_substitution_compression_diagnostics_live.csv
  term_table3_reproduction_check.csv
  term_table6_reproduction_check.csv

Reads:
  processed/comtrade_thesis_source_panel.csv
  processed/comtrade_thesis_country_product_month.csv  (for the reported flag)

Run from repo root:
    python 04_scripts/prepare_licensing_wedge_diagnostics.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
PROC = REPO / "03_data" / "processed"
OUT = REPO / "03_data" / "output" / "tables"

TREATED = {
    "2504":   ("Natural graphite",                "202310", "202401"),
    "811292": ("Unwrought other-metals bundle",   "202307", "202309"),
    "282560": ("GeO2/ZrO2",                       "202307", "202309"),
    "8110":   ("Antimony metal",                  "202408", "202410"),
    "261710": ("Antimony ores/concentrates",      "202408", "202410"),
    "282580": ("Antimony oxides",                 "202408", "202410"),
}
CONTROLS = {
    "2818": "Alumina",
    "8111": "Manganese articles",
    "2811": "Inorganic acids",
}


def load():
    sp = pd.read_csv(PROC / "comtrade_thesis_source_panel.csv",
                     dtype={"hs": str, "period": str})
    sp["reporter"] = sp["reporterCode"].astype(str)
    cp = pd.read_csv(PROC / "comtrade_thesis_country_product_month.csv",
                     dtype={"hs": str, "period": str})
    flag = cp[["reporterCode", "period", "hs", "world_primaryValue_reported"]].copy()
    flag["reporter"] = flag["reporterCode"].astype(str)
    sp = sp.merge(flag[["reporter", "period", "hs", "world_primaryValue_reported"]],
                  on=["reporter", "period", "hs"], how="left")
    return sp


def regularity(sp):
    """Table 3 inputs.

    NOTE: the manuscript Table 3 column labelled "China value share" actually
    reports the full-panel POSITIVE-CELL share (share of reporter-months with
    any China-source value), not a value-weighted share. We compute both and
    flag the caption error in the comparison.
    """
    rows = []
    all_products = {**TREATED, **{k: (v, "", "") for k, v in CONTROLS.items()}}
    for hs, (label, announce, _) in all_products.items():
        sub = sp[sp["hs"] == hs]
        china = sub[sub["source"] == "China"]
        # full-panel positive-cell share (what the orphan/table actually reports)
        china_cells = china.copy()
        china_cells["reported"] = china_cells["world_primaryValue_reported"].fillna(True)
        positive_cell_share = (china_cells["trade_value_usd"] > 0).mean()
        # true value share (what the caption literally says)
        full_total = sub["trade_value_usd"].sum()
        full_china = china["trade_value_usd"].sum()
        value_share = (full_china / full_total) if full_total > 0 else np.nan
        if announce:
            pre_china = china[china["period"] < announce]
            positive_china_cells = (pre_china["trade_value_usd"] > 0).mean()
            active_china_importers = int(pre_china.loc[pre_china["trade_value_usd"] > 0, "reporter"].nunique())
        else:
            positive_china_cells = np.nan
            active_china_importers = np.nan
        rows.append({
            "hs": hs,
            "product": label,
            "china_positive_cell_share_full_panel": positive_cell_share,
            "china_value_share_true": value_share,
            "positive_china_cells_pre": positive_china_cells,
            "active_china_importers_pre": active_china_importers,
        })
    return pd.DataFrame(rows)


def substitution_compression(sp):
    """Table 6 inputs: pre vs post mean monthly trade value by source.

    Pre window = months strictly before the ANNOUNCEMENT month.
    Post window = months from the IMPORT-EFFECT month onward.
    (Months between announcement and import-effect are excluded.) This matches
    the Table 6 caption: "pre-announcement window to post expected-import-effect
    window."
    """
    rows = []
    for hs, (label, announce, import_effect) in TREATED.items():
        sub = sp[sp["hs"] == hs].copy()
        for source, slabel in [("China", "China"), ("RestOfWorld", "RestOfWorld")]:
            s = sub[sub["source"] == source]
            pre = s[s["period"] < announce]
            post = s[s["period"] >= import_effect]
            pre_mean = pre.groupby("period")["trade_value_usd"].sum().mean()
            post_mean = post.groupby("period")["trade_value_usd"].sum().mean()
            pct = 100 * (post_mean - pre_mean) / pre_mean if pre_mean > 0 else np.nan
            rows.append({
                "hs": hs,
                "product": label,
                "source": slabel,
                "pre_window_end": _prev_month(announce),
                "post_start": import_effect,
                "pre_window_def": "months < announcement",
                "pre_mean_monthly_usd": pre_mean,
                "post_mean_monthly_usd": post_mean,
                "post_vs_pre_percent_change": pct,
            })
        # total
        pre = sub[sub["period"] < announce]
        post = sub[sub["period"] >= import_effect]
        pre_tot = pre.groupby("period")["trade_value_usd"].sum().mean()
        post_tot = post.groupby("period")["trade_value_usd"].sum().mean()
        pct_tot = 100 * (post_tot - pre_tot) / pre_tot if pre_tot > 0 else np.nan
        rows.append({
            "hs": hs, "product": label, "source": "Total",
            "pre_window_end": _prev_month(announce),
            "post_start": import_effect,
            "pre_window_def": "months < announcement",
            "pre_mean_monthly_usd": pre_tot,
            "post_mean_monthly_usd": post_tot,
            "post_vs_pre_percent_change": pct_tot,
        })
    return pd.DataFrame(rows)


def _prev_month(yyyymm):
    y, m = int(yyyymm[:4]), int(yyyymm[4:])
    m -= 1
    if m == 0:
        y, m = y - 1, 12
    return f"{y:04d}{m:02d}"


def compare_live_to_orphan(live_reg, live_sub):
    orphan_reg = pd.read_csv(OUT / "licensing_wedge_regularity_diagnostics.csv",
                             dtype={"hs": str})
    orphan_sub = pd.read_csv(
        OUT / "licensing_wedge_substitution_compression_diagnostics.csv",
        dtype={"hs": str})

    # Table 3 check
    t3 = live_reg[live_reg["hs"].isin(TREATED)].copy()
    t3 = t3.merge(orphan_reg[orphan_reg["source"].eq("China")][
        ["hs", "pre_positive_observation_share", "pre_active_importers"]],
        on="hs", how="left")
    # china "value share" in Table 3 / audit CSV is the full-panel positive-cell share
    audit = pd.read_csv(OUT / "comtrade_thesis_data_audit.csv", dtype={"hs": str})
    t3 = t3.merge(audit[["hs", "positive_china_value_share"]], on="hs", how="left")
    t3["orphan_china_value_share"] = t3["positive_china_value_share"]
    t3["live_china_value_share"] = t3["china_positive_cell_share_full_panel"]
    t3["diff_share"] = t3["live_china_value_share"] - t3["orphan_china_value_share"]
    t3["orphan_positive_china_cells"] = t3["pre_positive_observation_share"]
    t3["live_positive_china_cells"] = t3["positive_china_cells_pre"]
    t3["diff_cells"] = t3["live_positive_china_cells"] - t3["orphan_positive_china_cells"]
    t3["orphan_active_china_importers"] = t3["pre_active_importers"]
    t3["live_active_china_importers"] = t3["active_china_importers_pre"]
    t3["diff_importers"] = t3["live_active_china_importers"] - t3["orphan_active_china_importers"]
    t3["live_china_true_value_share"] = t3["china_value_share_true"]
    cols = ["hs", "product", "orphan_china_value_share", "live_china_value_share",
            "diff_share", "live_china_true_value_share",
            "orphan_positive_china_cells", "live_positive_china_cells",
            "diff_cells", "orphan_active_china_importers", "live_active_china_importers",
            "diff_importers"]
    t3["match_status"] = np.where(
        (t3["diff_share"].abs() < 0.005) & (t3["diff_cells"].abs() < 0.005) &
        (t3["diff_importers"].abs() < 1), "MATCH", "MISMATCH")
    t3[cols + ["match_status"]].to_csv(OUT / "term_table3_reproduction_check.csv",
                                       index=False)

    # Table 6 check (orphan CSV uses column "series" for China/ROW/Total)
    orphan_sub = orphan_sub.rename(columns={"series": "source"})
    # normalise Total label to match
    orphan_sub["source"] = orphan_sub["source"].replace({"Total": "Total"})
    t6 = live_sub.copy()
    t6 = t6.merge(orphan_sub[["hs", "source", "pre_mean_monthly_usd",
                              "post_mean_monthly_usd", "post_vs_pre_percent_change"]].rename(
        columns={"pre_mean_monthly_usd": "orphan_pre_mean",
                 "post_mean_monthly_usd": "orphan_post_mean",
                 "post_vs_pre_percent_change": "orphan_pct_change"}),
        on=["hs", "source"], how="left")
    t6 = t6.rename(columns={"pre_mean_monthly_usd": "live_pre_mean",
                            "post_mean_monthly_usd": "live_post_mean",
                            "post_vs_pre_percent_change": "live_pct_change"})
    t6["diff_pct"] = t6["live_pct_change"] - t6["orphan_pct_change"]
    t6["match_status"] = np.where(t6["diff_pct"].abs() < 0.05, "MATCH", "MISMATCH")
    out_cols = ["hs", "product", "source", "pre_window_end", "post_start",
                "orphan_pre_mean", "live_pre_mean", "orphan_post_mean",
                "live_post_mean", "orphan_pct_change", "live_pct_change",
                "diff_pct", "match_status"]
    t6[out_cols].to_csv(OUT / "term_table6_reproduction_check.csv", index=False)
    return t3, t6


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sp = load()
    reg = regularity(sp)
    sub = substitution_compression(sp)
    reg.to_csv(OUT / "thesis_regularity_diagnostics_live.csv", index=False)
    sub.to_csv(OUT / "thesis_substitution_compression_diagnostics_live.csv",
               index=False)
    t3, t6 = compare_live_to_orphan(reg, sub)
    print("=== Table 3 reproduction ===")
    print(t3[["hs", "orphan_china_value_share", "live_china_value_share",
              "orphan_positive_china_cells", "live_positive_china_cells",
              "orphan_active_china_importers", "live_active_china_importers",
              "match_status"]].to_string(index=False))
    print("\n=== Table 6 reproduction (pct change) ===")
    print(t6[["hs", "source", "orphan_pct_change", "live_pct_change",
              "diff_pct", "match_status"]].to_string(index=False))


if __name__ == "__main__":
    main()
