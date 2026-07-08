#!/usr/bin/env python3
"""
Create descriptive diagnostics for pressure-index variables.

This script does not change the canonical pressure indexes. It compares the
current frequency-based RoW access measure with a capacity-style alternative
and produces tables and plots for understanding whether the baseline pressure
construction is too generous about switching capacity.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D


REPO = Path(__file__).resolve().parents[1]
PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"
FIGURES = REPO / "03_data" / "output" / "figures"

PRESSURE_PATH = PROCESSED / "pressure_indices_importer_product.csv"
WIDE_PATH = PROCESSED / "comtrade_pressure_country_product_month.csv"
PARTNER_PATH = PROCESSED / "comtrade_pressure_partner_panel.csv"

PRODUCT_DIAG_PATH = TABLES / "pressure_product_diagnostics.csv"
IMPORTER_DIAG_PATH = TABLES / "pressure_importer_product_diagnostics.csv"
PSEUDO_WAVE_PATH = TABLES / "pressure_pseudo_wave_diagnostics.csv"
ROW_STRUCTURE_PATH = TABLES / "pressure_row_market_structure.csv"
PSEUDO_PRODUCT_PATH = TABLES / "pressure_pseudo_wave_product_diagnostics.csv"


POLICY_WAVES = [
    dict(wave=1, wave_label="Wave 1: Ga/Ge", announcement_period="202307"),
    dict(wave=2, wave_label="Wave 2: graphite", announcement_period="202310"),
    dict(wave=3, wave_label="Wave 3: antimony", announcement_period="202408"),
    dict(wave=4, wave_label="Wave 4: W/Bi", announcement_period="202502"),
]


def setup_style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pressure = pd.read_csv(PRESSURE_PATH, dtype={"hs": str}, low_memory=False)
    wide = pd.read_csv(WIDE_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    partner = pd.read_csv(PARTNER_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    return pressure, wide, partner


def capacity_access(row: pd.Series) -> float:
    china = float(row["pre_china_value"])
    row_value = float(row["pre_row_value"])
    if china > 0:
        return min(1.0, row_value / china)
    if row_value > 0:
        return 1.0
    return 0.0


def add_capacity_pressure(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    policy = out["has_policy_event"].eq(True)
    out["o_row_capacity"] = np.nan
    out.loc[policy, "o_row_capacity"] = out.loc[policy].apply(capacity_access, axis=1)
    out["p_switch_capacity"] = np.where(
        policy,
        out["e_china_exposure"] * out["o_row_capacity"] * out["a_row_strength_loo"],
        np.nan,
    )
    out["p_compress_capacity"] = np.where(
        policy,
        out["e_china_exposure"]
        * (1 - out["o_row_capacity"])
        * out["r_replacement_rigidity_loo"],
        np.nan,
    )
    out["p_x_decline_capacity"] = out["p_switch_capacity"] + out["p_compress_capacity"]
    return out


def add_market_scale_pressure(df: pd.DataFrame, wide: pd.DataFrame) -> pd.DataFrame:
    """Add a stricter outside-market scale diagnostic.

    The canonical index uses supplier count and HHI for product-level outside
    market strength. This diagnostic adds a scale term: non-China market value
    outside importer i relative to China market value outside importer i.
    """
    out = df.copy()
    policy = out["has_policy_event"].eq(True)
    out["china_market_value_loo"] = np.nan

    for hs, group in out.loc[policy].groupby("hs", sort=False):
        announcement_period = str(group["announcement_period"].iloc[0])
        pre = wide[wide["hs"].eq(hs) & wide["period"].lt(announcement_period)].copy()
        china_by_reporter = pre.groupby("reporterCode")["china_primaryValue"].sum()
        total_china = float(china_by_reporter.sum())
        for idx, row in group.iterrows():
            reporter = row["reporterCode"]
            own_china = float(china_by_reporter.get(reporter, 0.0))
            out.at[idx, "china_market_value_loo"] = max(total_china - own_china, 0.0)

    out["row_market_scale_loo"] = np.nan
    valid = policy & out["china_market_value_loo"].gt(0)
    out.loc[valid, "row_market_scale_loo"] = np.minimum(
        1.0,
        out.loc[valid, "row_total_value_loo"] / out.loc[valid, "china_market_value_loo"],
    )
    no_china = policy & out["china_market_value_loo"].le(0)
    out.loc[no_china, "row_market_scale_loo"] = np.where(
        out.loc[no_china, "row_total_value_loo"].gt(0), 1.0, 0.0
    )

    out["a_row_strength_scaled_loo"] = np.where(
        policy,
        out["a_row_strength_loo"] * out["row_market_scale_loo"],
        np.nan,
    )
    out["q_switch_absorptive"] = np.where(
        policy,
        out["o_row_access"] * out["a_row_strength_scaled_loo"],
        np.nan,
    )
    out["p_switch_absorptive"] = np.where(
        policy,
        out["e_china_exposure"] * out["q_switch_absorptive"],
        np.nan,
    )
    out["p_compress_absorptive"] = np.where(
        policy,
        out["e_china_exposure"] * (1 - out["q_switch_absorptive"]),
        np.nan,
    )
    out["p_x_absorptive"] = out["p_switch_absorptive"] + out["p_compress_absorptive"]
    return out


def weighted_average(values: pd.Series, weights: pd.Series) -> float:
    values = values.astype(float)
    weights = weights.astype(float)
    valid = values.notna() & weights.notna()
    values = values[valid]
    weights = weights[valid]
    if values.empty:
        return np.nan
    if weights.sum() > 0:
        return float((values * weights).sum() / weights.sum())
    return float(values.mean())


def product_diagnostics(pressure: pd.DataFrame) -> pd.DataFrame:
    policy = pressure[pressure["has_policy_event"].eq(True)].copy()
    rows = []
    for hs, group in policy.groupby("hs", sort=False):
        weights = group["pre_world_value"]
        x_freq = group["p_x_decline"]
        x_cap = group["p_x_decline_capacity"]
        rows.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "scope_status": group["scope_status"].iloc[0],
                "wave": group["wave"].iloc[0],
                "pre_world_value_sum": weights.sum(),
                "weighted_china_import_share": weighted_average(
                    group["e_china_exposure"], weights
                ),
                "weighted_row_access_frequency": weighted_average(
                    group["o_row_access"], weights
                ),
                "weighted_row_access_capacity": weighted_average(
                    group["o_row_capacity"], weights
                ),
                "weighted_outside_market_strength": weighted_average(
                    group["a_row_strength_loo"], weights
                ),
                "weighted_replacement_rigidity": weighted_average(
                    group["r_replacement_rigidity_loo"], weights
                ),
                "weighted_row_market_scale": weighted_average(
                    group["row_market_scale_loo"], weights
                ),
                "weighted_outside_market_strength_scaled": weighted_average(
                    group["a_row_strength_scaled_loo"], weights
                ),
                "weighted_p_switch_frequency": weighted_average(
                    group["p_switch"], weights
                ),
                "weighted_p_compress_frequency": weighted_average(
                    group["p_compress"], weights
                ),
                "weighted_p_x_frequency": weighted_average(x_freq, weights),
                "weighted_p_switch_capacity": weighted_average(
                    group["p_switch_capacity"], weights
                ),
                "weighted_p_compress_capacity": weighted_average(
                    group["p_compress_capacity"], weights
                ),
                "weighted_p_x_capacity": weighted_average(x_cap, weights),
                "weighted_p_switch_absorptive": weighted_average(
                    group["p_switch_absorptive"], weights
                ),
                "weighted_p_compress_absorptive": weighted_average(
                    group["p_compress_absorptive"], weights
                ),
                "weighted_p_x_absorptive": weighted_average(
                    group["p_x_absorptive"], weights
                ),
                "compression_share_frequency": weighted_average(
                    group["p_compress"] / x_freq.replace(0, np.nan), weights
                ),
                "compression_share_capacity": weighted_average(
                    group["p_compress_capacity"] / x_cap.replace(0, np.nan), weights
                ),
                "compression_share_absorptive": weighted_average(
                    group["p_compress_absorptive"]
                    / group["p_x_absorptive"].replace(0, np.nan),
                    weights,
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("weighted_china_import_share", ascending=False)


def row_market_structure(wide: pd.DataFrame, partner: pd.DataFrame) -> pd.DataFrame:
    policy = wide[wide["announcement_date"].notna()].copy()
    policy["announcement_period"] = policy["announcement_date"].astype(str).str[:7].str.replace("-", "", regex=False)
    rows = []
    for hs, group in policy.groupby("hs", sort=False):
        announcement_period = group["announcement_period"].iloc[0]
        pre = partner[
            partner["hs"].eq(hs)
            & partner["period"].lt(announcement_period)
            & partner["source"].eq("RestOfWorld")
            & partner["trade_value_usd"].gt(0)
        ].copy()
        by_supplier = pre.groupby("partnerCode")["trade_value_usd"].sum().sort_values(ascending=False)
        total = by_supplier.sum()
        if total > 0:
            shares = by_supplier / total
            hhi = float((shares**2).sum())
            top1 = float(shares.head(1).sum())
            top3 = float(shares.head(3).sum())
            top5 = float(shares.head(5).sum())
        else:
            hhi = top1 = top3 = top5 = np.nan
        rows.append(
            {
                "hs": hs,
                "product": group["product"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "announcement_period": announcement_period,
                "row_supplier_count": int((by_supplier > 0).sum()),
                "row_market_value": total,
                "row_supplier_hhi": hhi,
                "row_top1_share": top1,
                "row_top3_share": top3,
                "row_top5_share": top5,
            }
        )
    return pd.DataFrame(rows).sort_values("row_top5_share", ascending=False)


def compute_pressure_for_wave(
    wide: pd.DataFrame,
    partner: pd.DataFrame,
    hs: str,
    announcement_period: str,
    reporters: list[int],
) -> pd.DataFrame:
    product_wide = wide[wide["hs"].eq(hs)].copy()
    product_partner = partner[partner["hs"].eq(hs)].copy()
    meta = product_wide.iloc[0]
    pre_wide = product_wide[product_wide["period"].lt(announcement_period)].copy()
    pre_partner = product_partner[
        product_partner["period"].lt(announcement_period)
        & product_partner["source"].eq("RestOfWorld")
        & product_partner["trade_value_usd"].gt(0)
    ].copy()

    grouped = pre_wide.groupby("reporterCode", as_index=False).agg(
        pre_month_count=("period", "nunique"),
        pre_china_value=("china_primaryValue", "sum"),
        pre_row_value=("non_china_primaryValue", "sum"),
        pre_row_positive_months=("non_china_primaryValue", lambda x: int((x > 0).sum())),
    )
    out = pd.DataFrame({"reporterCode": reporters}).merge(grouped, on="reporterCode", how="left")
    for col in ["pre_month_count", "pre_china_value", "pre_row_value", "pre_row_positive_months"]:
        out[col] = out[col].fillna(0)
    out["pre_world_value"] = out["pre_china_value"] + out["pre_row_value"]
    out["e_china_exposure"] = np.where(
        out["pre_world_value"] > 0,
        out["pre_china_value"] / out["pre_world_value"],
        0.0,
    )
    out["o_row_access"] = np.where(
        out["pre_month_count"] > 0,
        out["pre_row_positive_months"] / out["pre_month_count"],
        0.0,
    )
    out["o_row_capacity"] = out.apply(capacity_access, axis=1)

    global_by_supplier = pre_partner.groupby("partnerCode")["trade_value_usd"].sum()
    reporter_supplier = pre_partner.groupby(["reporterCode", "partnerCode"])["trade_value_usd"].sum()
    supplier_counts = []
    row_totals = []
    hhis = []
    for reporter in reporters:
        loo = global_by_supplier.copy()
        if reporter in reporter_supplier.index.get_level_values(0):
            own = reporter_supplier.loc[reporter]
            common = loo.index.intersection(own.index)
            loo.loc[common] = loo.loc[common] - own.loc[common]
        if reporter in loo.index:
            loo = loo.drop(index=reporter)
        loo = loo[loo > 0]
        supplier_counts.append(int(len(loo)))
        total = float(loo.sum())
        row_totals.append(total)
        if total > 0:
            share = loo / loo.sum()
            hhis.append(float((share**2).sum()))
        else:
            hhis.append(np.nan)
    out["row_supplier_count_loo"] = supplier_counts
    out["row_total_value_loo"] = row_totals
    out["row_hhi_loo"] = hhis
    out["row_diversification_loo"] = (1 - out["row_hhi_loo"]).fillna(0.0)
    total_china = float(pre_wide["china_primaryValue"].sum())
    out["china_market_value_loo"] = np.maximum(
        total_china - out["pre_china_value"], 0.0
    )
    out["row_market_scale_loo"] = np.where(
        out["china_market_value_loo"] > 0,
        np.minimum(1.0, out["row_total_value_loo"] / out["china_market_value_loo"]),
        np.where(out["row_total_value_loo"] > 0, 1.0, 0.0),
    )
    out["hs"] = hs
    out["product"] = meta["product"]
    out["analysis_role"] = meta["analysis_role"]
    out["scope_status"] = meta["scope_status"]
    return out


def pseudo_wave_diagnostics(wide: pd.DataFrame, partner: pd.DataFrame) -> pd.DataFrame:
    reporters = sorted(wide["reporterCode"].unique())
    products = wide[["hs", "product", "analysis_role", "wave"]].drop_duplicates()
    control_hs = products.loc[products["analysis_role"].eq("candidate_control_pending_screen"), "hs"].tolist()
    frames = []
    for wave in POLICY_WAVES:
        wave_no = wave["wave"]
        treated_hs = products.loc[
            products["wave"].eq(float(wave_no))
            & products["analysis_role"].isin(
                [
                    "main_clean_treated",
                    "main_clean_treated_sparse_caution",
                    "secondary_scope_case",
                ]
            ),
            "hs",
        ].tolist()
        for hs in [*treated_hs, *control_hs]:
            frame = compute_pressure_for_wave(
                wide,
                partner,
                hs,
                wave["announcement_period"],
                reporters,
            )
            frame["diagnostic_wave"] = wave_no
            frame["diagnostic_wave_label"] = wave["wave_label"]
            frame["diagnostic_announcement_period"] = wave["announcement_period"]
            frame["diagnostic_role"] = np.where(
                frame["hs"].isin(treated_hs), "treated_in_wave", "candidate_control"
            )
            frames.append(frame)
    out = pd.concat(frames, ignore_index=True)
    max_n = out["row_supplier_count_loo"].max()
    out["row_depth_loo"] = np.where(
        max_n > 0,
        np.log1p(out["row_supplier_count_loo"]) / np.log1p(max_n),
        0.0,
    )
    out["a_row_strength_loo"] = out["row_depth_loo"] * out["row_diversification_loo"]
    out["r_replacement_rigidity_loo"] = 1 - out["a_row_strength_loo"]
    out["a_row_strength_scaled_loo"] = (
        out["a_row_strength_loo"] * out["row_market_scale_loo"]
    )
    out["p_switch_frequency"] = (
        out["e_china_exposure"] * out["o_row_access"] * out["a_row_strength_loo"]
    )
    out["p_compress_frequency"] = (
        out["e_china_exposure"]
        * (1 - out["o_row_access"])
        * out["r_replacement_rigidity_loo"]
    )
    out["p_switch_capacity"] = (
        out["e_china_exposure"] * out["o_row_capacity"] * out["a_row_strength_loo"]
    )
    out["p_compress_capacity"] = (
        out["e_china_exposure"]
        * (1 - out["o_row_capacity"])
        * out["r_replacement_rigidity_loo"]
    )
    out["q_switch_absorptive"] = (
        out["o_row_access"] * out["a_row_strength_scaled_loo"]
    )
    out["p_switch_absorptive"] = (
        out["e_china_exposure"] * out["q_switch_absorptive"]
    )
    out["p_compress_absorptive"] = (
        out["e_china_exposure"] * (1 - out["q_switch_absorptive"])
    )
    for col in [
        "p_switch_frequency",
        "p_compress_frequency",
        "p_switch_capacity",
        "p_compress_capacity",
        "p_switch_absorptive",
        "p_compress_absorptive",
    ]:
        sd = out[col].std(ddof=0)
        out[f"{col}_z"] = (out[col] - out[col].mean()) / sd if sd > 0 else np.nan
    return out


def pseudo_product_diagnostics(pseudo: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, group in pseudo.groupby(
        ["diagnostic_wave", "diagnostic_wave_label", "hs"], sort=False
    ):
        diagnostic_wave, diagnostic_wave_label, hs = keys
        weights = group["pre_world_value"]
        rows.append(
            {
                "diagnostic_wave": diagnostic_wave,
                "diagnostic_wave_label": diagnostic_wave_label,
                "hs": hs,
                "product": group["product"].iloc[0],
                "diagnostic_role": group["diagnostic_role"].iloc[0],
                "analysis_role": group["analysis_role"].iloc[0],
                "scope_status": group["scope_status"].iloc[0],
                "pre_world_value_sum": weights.sum(),
                "weighted_china_import_share": weighted_average(
                    group["e_china_exposure"], weights
                ),
                "weighted_row_access_frequency": weighted_average(
                    group["o_row_access"], weights
                ),
                "weighted_row_access_capacity": weighted_average(
                    group["o_row_capacity"], weights
                ),
                "weighted_outside_market_strength": weighted_average(
                    group["a_row_strength_loo"], weights
                ),
                "weighted_outside_market_strength_scaled": weighted_average(
                    group["a_row_strength_scaled_loo"], weights
                ),
                "weighted_p_switch_capacity": weighted_average(
                    group["p_switch_capacity"], weights
                ),
                "weighted_p_compress_capacity": weighted_average(
                    group["p_compress_capacity"], weights
                ),
                "weighted_p_switch_absorptive": weighted_average(
                    group["p_switch_absorptive"], weights
                ),
                "weighted_p_compress_absorptive": weighted_average(
                    group["p_compress_absorptive"], weights
                ),
            }
        )
    return pd.DataFrame(rows)


def save_product_tables(
    pressure: pd.DataFrame,
    wide: pd.DataFrame,
    partner: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    importer_diag = add_capacity_pressure(pressure)
    importer_diag = add_market_scale_pressure(importer_diag, wide)
    product_diag = product_diagnostics(importer_diag)
    row_structure = row_market_structure(wide, partner)
    pseudo = pseudo_wave_diagnostics(wide, partner)
    pseudo_product = pseudo_product_diagnostics(pseudo)

    importer_diag.to_csv(IMPORTER_DIAG_PATH, index=False)
    product_diag.to_csv(PRODUCT_DIAG_PATH, index=False)
    row_structure.to_csv(ROW_STRUCTURE_PATH, index=False)
    pseudo.to_csv(PSEUDO_WAVE_PATH, index=False)
    pseudo_product.to_csv(PSEUDO_PRODUCT_PATH, index=False)
    return product_diag, row_structure, pseudo, pseudo_product


def savefig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def plot_switch_compress_actual(importer_diag: pd.DataFrame) -> None:
    policy = importer_diag[importer_diag["has_policy_event"].eq(True)].copy()
    policy["role_plot"] = np.where(policy["is_clean_treated"], "clean treated", "secondary scope")
    for mode, x_col, y_col, title, filename in [
        (
            "frequency",
            "p_compress_z_policy_event",
            "p_switch_z_policy_event",
            "Frequency access: actual policy products",
            "pressure_scatter_actual_frequency.png",
        ),
        (
            "capacity",
            "p_compress_capacity",
            "p_switch_capacity",
            "Capacity access: actual policy products",
            "pressure_scatter_actual_capacity.png",
        ),
    ]:
        plot = policy.copy()
        if mode == "capacity":
            for col in [x_col, y_col]:
                sd = plot[col].std(ddof=0)
                plot[col + "_z"] = (plot[col] - plot[col].mean()) / sd
            x = x_col + "_z"
            y = y_col + "_z"
        else:
            x = x_col
            y = y_col
        plt.figure(figsize=(7.5, 5.4))
        sns.scatterplot(
            data=plot,
            x=x,
            y=y,
            hue="role_plot",
            style="scope_status",
            size="pre_world_value",
            sizes=(20, 260),
            alpha=0.68,
            palette={"clean treated": "#c62828", "secondary scope": "#ef6c00"},
            edgecolor="white",
            linewidth=0.4,
        )
        plt.axhline(0, color="#666666", linewidth=0.8)
        plt.axvline(0, color="#666666", linewidth=0.8)
        plt.xlabel("Compression pressure, standardized")
        plt.ylabel("Switching pressure, standardized")
        plt.title(title)
        savefig(FIGURES / filename)


def plot_switch_compress_pseudo(pseudo: pd.DataFrame) -> None:
    sample = pseudo.copy()
    sample["role_plot"] = np.where(sample["diagnostic_role"].eq("treated_in_wave"), "treated", "candidate control")
    plt.figure(figsize=(8.2, 5.8))
    sns.scatterplot(
        data=sample,
        x="p_compress_capacity_z",
        y="p_switch_capacity_z",
        hue="role_plot",
        style="diagnostic_wave_label",
        size="pre_world_value",
        sizes=(12, 180),
        alpha=0.45,
        palette={"treated": "#c62828", "candidate control": "#1565c0"},
        edgecolor="white",
        linewidth=0.25,
    )
    plt.axhline(0, color="#666666", linewidth=0.8)
    plt.axvline(0, color="#666666", linewidth=0.8)
    plt.xlabel("Compression pressure, capacity version, standardized")
    plt.ylabel("Switching pressure, capacity version, standardized")
    plt.title("Importer-product pseudo-wave pressure, capacity version")
    plt.tight_layout()
    plt.savefig(
        FIGURES / "pressure_importer_product_pseudo_wave_capacity.png",
        bbox_inches="tight",
    )
    # Overwrite the older filename with the clarified title so stale plots do
    # not remain in the output folder.
    plt.savefig(FIGURES / "pressure_scatter_pseudo_wave_capacity.png", bbox_inches="tight")
    plt.close()


def plot_product_pressure_scatter(product_diag: pd.DataFrame) -> None:
    plot = product_diag.copy()
    plot["role_plot"] = np.where(
        plot["analysis_role"].str.contains("main_clean", na=False),
        "main clean",
        "secondary scope",
    )
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.6), sharex=False, sharey=False)
    specs = [
        (
            "weighted_p_compress_frequency",
            "weighted_p_switch_frequency",
            "Frequency access",
        ),
        (
            "weighted_p_compress_capacity",
            "weighted_p_switch_capacity",
            "Capacity access",
        ),
        (
            "weighted_p_compress_absorptive",
            "weighted_p_switch_absorptive",
            "Scale-adjusted absorptive",
        ),
    ]
    colors = {"main clean": "#c62828", "secondary scope": "#ef6c00"}
    for ax, (x_col, y_col, title) in zip(axes, specs):
        for role, sub in plot.groupby("role_plot"):
            sizes = 80 + 420 * (
                sub["pre_world_value_sum"] / plot["pre_world_value_sum"].max()
            )
            ax.scatter(
                sub[x_col],
                sub[y_col],
                s=sizes,
                color=colors[role],
                alpha=0.78,
                edgecolor="white",
                linewidth=0.6,
                label=role,
            )
            for _, row in sub.iterrows():
                ax.text(row[x_col] + 0.004, row[y_col] + 0.004, row["hs"], fontsize=7)
        ax.set_title(title)
        ax.set_xlabel("Compression pressure")
        ax.set_ylabel("Switching pressure")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.suptitle("Product-level pressure comparison: one point per policy product")
    savefig(FIGURES / "pressure_product_scatter_three_measures.png")


def plot_pseudo_product_pressure_scatter(pseudo_product: pd.DataFrame) -> None:
    plot = pseudo_product.copy()
    plot["role_plot"] = np.where(
        plot["diagnostic_role"].eq("treated_in_wave"),
        "treated in wave",
        "candidate control",
    )
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2), sharex=False, sharey=False)
    specs = [
        (
            "weighted_p_compress_capacity",
            "weighted_p_switch_capacity",
            "Capacity access",
        ),
        (
            "weighted_p_compress_absorptive",
            "weighted_p_switch_absorptive",
            "Scale-adjusted absorptive",
        ),
    ]
    palette = {"treated in wave": "#c62828", "candidate control": "#1565c0"}
    markers = {
        "Wave 1: Ga/Ge": "o",
        "Wave 2: graphite": "X",
        "Wave 3: antimony": "s",
        "Wave 4: W/Bi": "P",
    }
    for ax, (x_col, y_col, title) in zip(axes, specs):
        for (role, wave), sub in plot.groupby(["role_plot", "diagnostic_wave_label"]):
            sizes = 45 + 300 * (
                sub["pre_world_value_sum"] / plot["pre_world_value_sum"].max()
            )
            ax.scatter(
                sub[x_col],
                sub[y_col],
                s=sizes,
                color=palette[role],
                marker=markers[wave],
                alpha=0.72,
                edgecolor="white",
                linewidth=0.45,
            )
        treated = plot[plot["diagnostic_role"].eq("treated_in_wave")]
        for _, row in treated.iterrows():
            ax.text(row[x_col] + 0.003, row[y_col] + 0.003, row["hs"], fontsize=7)
        ax.set_title(title)
        ax.set_xlabel("Compression pressure")
        ax.set_ylabel("Switching pressure")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    role_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="treated in wave",
            markerfacecolor=palette["treated in wave"],
            markersize=8,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="candidate control",
            markerfacecolor=palette["candidate control"],
            markersize=8,
        ),
    ]
    wave_handles = [
        Line2D(
            [0],
            [0],
            marker=marker,
            color="#555555",
            label=wave,
            linestyle="",
            markersize=7,
        )
        for wave, marker in markers.items()
    ]
    fig.legend(
        role_handles + wave_handles,
        [h.get_label() for h in role_handles + wave_handles],
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        frameon=False,
        fontsize=8,
    )
    fig.suptitle("Product-wave pressure: treated products and donor candidates")
    savefig(FIGURES / "pressure_product_wave_scatter.png")


def plot_product_decomposition(product_diag: pd.DataFrame) -> None:
    order = product_diag.sort_values("weighted_china_import_share", ascending=True)["hs"]
    long = product_diag.melt(
        id_vars=["hs", "product", "analysis_role"],
        value_vars=[
            "weighted_china_import_share",
            "weighted_row_access_frequency",
            "weighted_row_access_capacity",
            "weighted_outside_market_strength",
            "weighted_outside_market_strength_scaled",
            "weighted_replacement_rigidity",
        ],
        var_name="component",
        value_name="value",
    )
    labels = {
        "weighted_china_import_share": "China exposure",
        "weighted_row_access_frequency": "RoW access, frequency",
        "weighted_row_access_capacity": "RoW access, capacity",
        "weighted_outside_market_strength": "RoW market strength",
        "weighted_outside_market_strength_scaled": "RoW strength, scale-adjusted",
        "weighted_replacement_rigidity": "Replacement rigidity",
    }
    long["component"] = long["component"].map(labels)
    long["hs"] = pd.Categorical(long["hs"], categories=order, ordered=True)
    plt.figure(figsize=(10.6, 6.2))
    ax = sns.barplot(data=long, y="hs", x="value", hue="component")
    plt.xlim(0, 1)
    plt.xlabel("Weighted product average")
    plt.ylabel("HS product")
    plt.title("Pressure-index components by policy product")
    ax.legend(
        title="component",
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        frameon=False,
    )
    savefig(FIGURES / "pressure_product_component_decomposition.png")


def plot_china_share(product_diag: pd.DataFrame) -> None:
    plot = product_diag.sort_values("weighted_china_import_share", ascending=True)
    plt.figure(figsize=(7.2, 5.4))
    colors = np.where(plot["analysis_role"].str.contains("main_clean", na=False), "#c62828", "#ef6c00")
    plt.barh(plot["hs"], plot["weighted_china_import_share"], color=colors)
    plt.xlabel("Pre-policy China share of reporter imports")
    plt.ylabel("HS product")
    plt.title("China import share in pre-policy trade data")
    plt.xlim(0, 1)
    savefig(FIGURES / "pressure_product_pre_china_share.png")


def plot_access_comparison(product_diag: pd.DataFrame) -> None:
    plot = product_diag.sort_values("weighted_row_access_frequency", ascending=False)
    x = np.arange(len(plot))
    width = 0.38
    plt.figure(figsize=(9.2, 5.2))
    plt.bar(x - width / 2, plot["weighted_row_access_frequency"], width, label="Frequency access", color="#1565c0")
    plt.bar(x + width / 2, plot["weighted_row_access_capacity"], width, label="Capacity access", color="#7b1fa2")
    plt.xticks(x, plot["hs"], rotation=45, ha="right")
    plt.ylim(0, 1)
    plt.ylabel("Weighted average")
    plt.title("RoW access: frequency measure versus capacity measure")
    plt.legend()
    savefig(FIGURES / "pressure_row_access_frequency_vs_capacity.png")


def plot_pressure_decomposition(product_diag: pd.DataFrame) -> None:
    plot = product_diag.sort_values("weighted_p_x_absorptive", ascending=True)
    x = np.arange(len(plot))
    fig, axes = plt.subplots(1, 3, figsize=(15.8, 5.2), sharey=True)
    axes[0].barh(x, plot["weighted_p_switch_frequency"], color="#2e7d32", label="Switching")
    axes[0].barh(x, plot["weighted_p_compress_frequency"], left=plot["weighted_p_switch_frequency"], color="#ad1457", label="Compression")
    axes[0].set_title("Frequency access")
    axes[0].set_xlabel("Weighted pressure")
    axes[0].set_yticks(x)
    axes[0].set_yticklabels(plot["hs"])
    axes[1].barh(x, plot["weighted_p_switch_capacity"], color="#2e7d32", label="Switching")
    axes[1].barh(x, plot["weighted_p_compress_capacity"], left=plot["weighted_p_switch_capacity"], color="#ad1457", label="Compression")
    axes[1].set_title("Capacity access")
    axes[1].set_xlabel("Weighted pressure")
    axes[2].barh(x, plot["weighted_p_switch_absorptive"], color="#2e7d32", label="Switching")
    axes[2].barh(x, plot["weighted_p_compress_absorptive"], left=plot["weighted_p_switch_absorptive"], color="#ad1457", label="Compression")
    axes[2].set_title("Scale-adjusted absorptive")
    axes[2].set_xlabel("Weighted pressure")
    axes[0].legend(loc="lower right")
    axes[1].legend(loc="lower right")
    axes[2].legend(loc="lower right")
    fig.suptitle("Switching versus compression pressure by product")
    savefig(FIGURES / "pressure_switch_compress_product_bars.png")


def plot_distributions(importer_diag: pd.DataFrame) -> None:
    policy = importer_diag[importer_diag["has_policy_event"].eq(True)].copy()
    plot = policy.melt(
        id_vars=["hs", "analysis_role"],
        value_vars=["e_china_exposure", "o_row_access", "o_row_capacity"],
        var_name="measure",
        value_name="value",
    )
    plot["measure"] = plot["measure"].map(
        {
            "e_china_exposure": "China exposure",
            "o_row_access": "RoW access, frequency",
            "o_row_capacity": "RoW access, capacity",
        }
    )
    plt.figure(figsize=(10, 6.8))
    sns.boxplot(data=plot, y="hs", x="value", hue="measure", fliersize=1.5)
    plt.xlim(0, 1)
    plt.xlabel("Importer-product value")
    plt.ylabel("HS product")
    plt.title("Importer-level exposure and access distributions")
    savefig(FIGURES / "pressure_exposure_access_distributions.png")


def plot_row_market_structure(row_structure: pd.DataFrame) -> None:
    plot = row_structure.sort_values("row_supplier_count", ascending=True)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), sharey=True)
    axes[0].barh(plot["hs"], plot["row_supplier_count"], color="#1565c0")
    axes[0].set_xlabel("Distinct positive RoW suppliers")
    axes[0].set_ylabel("HS product")
    axes[0].set_title("Supplier depth")
    axes[1].barh(plot["hs"], plot["row_top5_share"], color="#6a1b9a")
    axes[1].set_xlim(0, 1)
    axes[1].set_xlabel("Top 5 suppliers' share")
    axes[1].set_title("Supplier concentration")
    savefig(FIGURES / "pressure_row_market_structure.png")


def plot_china_share_over_time(wide: pd.DataFrame) -> None:
    policy = wide[wide["announcement_date"].notna()].copy()
    monthly = policy.groupby(["hs", "product", "period"], as_index=False).agg(
        china_value=("china_primaryValue", "sum"),
        world_value=("world_primaryValue", "sum"),
        announcement_date=("announcement_date", "first"),
        implementation_date=("implementation_date", "first"),
    )
    monthly["china_share"] = np.where(
        monthly["world_value"] > 0,
        monthly["china_value"] / monthly["world_value"],
        np.nan,
    )
    monthly["date"] = pd.to_datetime(monthly["period"] + "01", format="%Y%m%d")
    g = sns.FacetGrid(
        monthly,
        col="hs",
        col_wrap=5,
        height=2.15,
        sharey=True,
        sharex=True,
    )
    g.map_dataframe(sns.lineplot, x="date", y="china_share", color="#c62828", linewidth=1.4)
    for ax, (hs, sub) in zip(g.axes.flat, monthly.groupby("hs", sort=False)):
        ann = pd.to_datetime(sub["announcement_date"].iloc[0])
        imp = pd.to_datetime(sub["implementation_date"].iloc[0])
        ax.axvline(ann, color="#444444", linewidth=0.8, linestyle="--")
        ax.axvline(imp, color="#1565c0", linewidth=0.8, linestyle=":")
        ax.set_title(hs)
        ax.set_ylim(0, 1)
    g.set_axis_labels("", "China share")
    g.fig.suptitle("Monthly China share of imports by policy product", y=1.02)
    g.fig.autofmt_xdate(rotation=35)
    g.savefig(FIGURES / "pressure_china_share_over_time.png", bbox_inches="tight", dpi=220)
    plt.close(g.fig)


def make_plots(
    importer_diag: pd.DataFrame,
    product_diag: pd.DataFrame,
    row_structure: pd.DataFrame,
    pseudo: pd.DataFrame,
    pseudo_product: pd.DataFrame,
    wide: pd.DataFrame,
) -> None:
    plot_switch_compress_actual(importer_diag)
    plot_switch_compress_pseudo(pseudo)
    plot_product_pressure_scatter(product_diag)
    plot_pseudo_product_pressure_scatter(pseudo_product)
    plot_product_decomposition(product_diag)
    plot_china_share(product_diag)
    plot_access_comparison(product_diag)
    plot_pressure_decomposition(product_diag)
    plot_distributions(importer_diag)
    plot_row_market_structure(row_structure)
    plot_china_share_over_time(wide)


def validate_outputs(product_diag: pd.DataFrame, pseudo: pd.DataFrame) -> None:
    errors = []
    for col in [
        "weighted_row_access_frequency",
        "weighted_row_access_capacity",
        "weighted_china_import_share",
        "weighted_p_switch_frequency",
        "weighted_p_compress_frequency",
        "weighted_p_switch_capacity",
        "weighted_p_compress_capacity",
    ]:
        values = product_diag[col].dropna()
        if values.lt(-1e-10).any() or values.gt(1 + 1e-10).any():
            errors.append(f"{col} outside [0,1]")
    if product_diag["weighted_p_compress_capacity"].mean() <= product_diag["weighted_p_compress_frequency"].mean():
        errors.append("capacity compression did not increase on average")
    if pseudo.empty:
        errors.append("pseudo-wave diagnostics empty")
    if errors:
        raise ValueError("; ".join(errors))


def main() -> None:
    setup_style()
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    pressure, wide, partner = load_inputs()
    importer_diag = add_capacity_pressure(pressure)
    product_diag, row_structure, pseudo, pseudo_product = save_product_tables(
        importer_diag, wide, partner
    )
    validate_outputs(product_diag, pseudo)
    make_plots(importer_diag, product_diag, row_structure, pseudo, pseudo_product, wide)

    print(f"Wrote {PRODUCT_DIAG_PATH}")
    print(f"Wrote {IMPORTER_DIAG_PATH}")
    print(f"Wrote {PSEUDO_WAVE_PATH}")
    print(f"Wrote {PSEUDO_PRODUCT_PATH}")
    print(f"Wrote {ROW_STRUCTURE_PATH}")
    print("Wrote figures:")
    for path in sorted(FIGURES.glob("pressure_*.png")):
        print(f"  {path}")
    print("\nProduct diagnostics:")
    print(
        product_diag[
            [
                "hs",
                "product",
                "weighted_china_import_share",
                "weighted_row_access_frequency",
                "weighted_row_access_capacity",
                "weighted_p_compress_frequency",
                "weighted_p_compress_capacity",
                "weighted_p_compress_absorptive",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
