#!/usr/bin/env python3
"""
Run the revised K-based pressure-index preliminary battery with USGS production A.

This script keeps the trade-based pressure-index outputs intact. It builds a
separate result package for the production-based logic:

    K = O * A
    P_S = E * K
    P_C = E * (1 - K)
    P_X = E

The preferred access measure is capacity access. The product availability
measure is built from USGS country-level world production data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from typing import Iterable
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


REPO = Path(__file__).resolve().parents[1]
LOCAL_SITE_PACKAGES = REPO / ".conda" / "lib" / "python3.12" / "site-packages"
if LOCAL_SITE_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

import pyfixest as pf


PROCESSED = REPO / "03_data" / "processed"
TABLES = REPO / "03_data" / "output" / "tables"
RESULTS = REPO / "results" / "revised_pressure_K_prod_A_2023"
RESULTS_2024 = REPO / "results" / "revised_pressure_K_prod_A_2024"
USGS_ARCHIVE = Path("/Users/elgask0/Downloads/Archive.zip")
USGS_EXTRACT = REPO / "03_data" / "interim" / "usgs_mcs_2025_archive"
USGS_WORLD_CSV = USGS_EXTRACT / "World_Data_Release_MCS_2025" / "MCS2025_World_Data.csv"

SOURCE_PANEL = PROCESSED / "pressure_ppml_estimation_panel.csv"
WIDE_PANEL = PROCESSED / "comtrade_pressure_country_product_month.csv"
PRODUCT_META = PROCESSED / "product_scope_metadata.csv"

CONTROL_ROLE = "candidate_control_pending_screen"
MAIN_TREATED_HS = ["2504", "8110", "8106", "284180"]

MONTHLY_FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
    "fe_importer_product_source",
]

QUARTERLY_FE = [
    "fe_importer_quarter",
    "fe_product_quarter",
    "fe_source_quarter",
    "fe_importer_product_source",
]

WIDE_MONTHLY_FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_importer_product",
]

WIDE_QUARTERLY_FE = [
    "fe_importer_quarter",
    "fe_product_quarter",
    "fe_importer_product",
]


@dataclass(frozen=True)
class Group:
    key: str
    label: str
    family: str
    treated_hs: tuple[str, ...]


GROUPS = [
    Group("pooled_clean", "Pooled clean treated", "pooled", tuple(MAIN_TREATED_HS)),
    Group("wave2_graphite", "Wave 2 graphite", "wave", ("2504",)),
    Group("wave3_antimony_clean", "Wave 3 antimony metal", "wave", ("8110",)),
    Group("wave4_w_bi", "Wave 4 W/Bi", "wave", ("8106", "284180")),
    Group("hs2504_graphite", "HS 2504 graphite", "product", ("2504",)),
    Group("hs8110_antimony_metal", "HS 8110 antimony metal", "product", ("8110",)),
    Group("hs8106_bismuth", "HS 8106 bismuth", "product", ("8106",)),
    Group("hs284180_tungstates", "HS 284180 tungstates", "product", ("284180",)),
]

POLICY_MONTHS = {
    "2504": {
        "announcement": "202310",
        "implementation": "202312",
        "import_effect": "202401",
        "first_full_post_quarter": "202401",
    },
    "8110": {
        "announcement": "202408",
        "implementation": "202409",
        "import_effect": "202410",
        "first_full_post_quarter": "202410",
    },
    "8106": {
        "announcement": "202502",
        "implementation": "202502",
        "import_effect": "202503",
        "first_full_post_quarter": "202504",
    },
    "284180": {
        "announcement": "202502",
        "implementation": "202502",
        "import_effect": "202503",
        "first_full_post_quarter": "202504",
    },
}

ANCHORS = [
    "announcement",
    "implementation",
    "import_effect",
    "first_full_post_quarter",
]

PRESSURE_VARIANTS = {
    "capacity": {
        "O": "O_cap",
        "K": "K_cap_prod",
        "PS": "P_S_cap_prod",
        "PC": "P_C_cap_prod",
        "A": "A_prod_2023",
        "preferred": True,
    },
    "frequency": {
        "O": "O_freq",
        "K": "K_freq_prod",
        "PS": "P_S_freq_prod",
        "PC": "P_C_freq_prod",
        "A": "A_prod_2023",
        "preferred": False,
    },
    "binary": {
        "O": "O_bin",
        "K": "K_bin_prod",
        "PS": "P_S_bin_prod",
        "PC": "P_C_bin_prod",
        "A": "A_prod_2023",
        "preferred": False,
    },
    "capacity_2024": {
        "O": "O_cap",
        "K": "K_cap_prod_2024",
        "PS": "P_S_cap_prod_2024",
        "PC": "P_C_cap_prod_2024",
        "A": "A_prod_2024",
        "preferred": False,
    },
}

USGS_PRODUCT_MAP = {
    "2504": {
        "product_name": "Natural graphite",
        "commodity": "Graphite",
        "type": "Mine production",
        "interpretation": "Good direct proxy for HS 2504 natural graphite.",
    },
    "8110": {
        "product_name": "Antimony metal and articles",
        "commodity": "Antimony",
        "type": "Mine production, antimony content",
        "interpretation": "Upstream proxy for antimony metal supply base.",
    },
    "8106": {
        "product_name": "Bismuth metal",
        "commodity": "Bismuth",
        "type": "Refinery production",
        "interpretation": "Best available production proxy for bismuth metal.",
    },
    "284180": {
        "product_name": "Tungstates and APT",
        "commodity": "Tungsten",
        "type": "Mine production, tungsten content",
        "interpretation": "Upstream proxy for tungstates/APT supply base.",
    },
}

warnings_log: list[str] = []
standardization_audit_rows: list[dict] = []


def warn(message: str) -> None:
    warnings_log.append(message)
    print(f"[warn] {message}")


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def month_index(period: str) -> int:
    period = str(period)
    return int(period[:4]) * 12 + int(period[4:6])


def month_to_quarter(period: str) -> str:
    period = str(period)
    year = int(period[:4])
    month = int(period[4:6])
    q = (month - 1) // 3 + 1
    return f"{year}Q{q}"


def quarter_index(quarter: str) -> int:
    quarter = str(quarter)
    return int(quarter[:4]) * 4 + int(quarter[-1])


def anchor_period(hs: str, anchor: str, freq: str) -> str:
    month = POLICY_MONTHS[str(hs)][anchor]
    if freq == "monthly":
        return month
    return month_to_quarter(month)


def period_ge(left: pd.Series, right: pd.Series | str, freq: str) -> pd.Series:
    if isinstance(right, str):
        if freq == "monthly":
            return left.astype(str).map(month_index).ge(month_index(right))
        return left.astype(str).map(quarter_index).ge(quarter_index(right))
    if freq == "monthly":
        return left.astype(str).map(month_index).ge(right.astype(str).map(month_index))
    return left.astype(str).map(quarter_index).ge(right.astype(str).map(quarter_index))


def period_lt(left: pd.Series, right: pd.Series | str, freq: str) -> pd.Series:
    if isinstance(right, str):
        if freq == "monthly":
            return left.astype(str).map(month_index).lt(month_index(right))
        return left.astype(str).map(quarter_index).lt(quarter_index(right))
    if freq == "monthly":
        return left.astype(str).map(month_index).lt(right.astype(str).map(month_index))
    return left.astype(str).map(quarter_index).lt(right.astype(str).map(quarter_index))


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["period"] = out["period"].astype(str)
    out["month_index"] = out["period"].map(month_index)
    out["quarter"] = out["period"].map(month_to_quarter)
    out["quarter_index"] = out["quarter"].map(quarter_index)
    return out


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype(float)


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).replace("\xa0", " ").split()).strip()


def extract_usgs_archive() -> None:
    if USGS_WORLD_CSV.exists():
        return
    if not USGS_ARCHIVE.exists():
        raise FileNotFoundError(f"USGS archive not found: {USGS_ARCHIVE}")
    USGS_EXTRACT.mkdir(parents=True, exist_ok=True)
    with ZipFile(USGS_ARCHIVE) as archive:
        archive.extractall(USGS_EXTRACT)


def load_usgs_world_data() -> pd.DataFrame:
    extract_usgs_archive()
    world = pd.read_csv(USGS_WORLD_CSV, low_memory=False)
    world["commodity_norm"] = world["COMMODITY"].map(normalize_text)
    world["country_norm"] = world["COUNTRY"].map(normalize_text)
    world["type_norm"] = world["TYPE"].map(normalize_text)
    for col in ["PROD_2023", "PROD_EST_ 2024"]:
        world[col] = clean_numeric(world[col])
    return world


def match_usgs_rows(world: pd.DataFrame, commodity: str, prod_type: str) -> pd.DataFrame:
    commodity_norm = normalize_text(commodity)
    type_norm = normalize_text(prod_type)
    sub = world.loc[world["commodity_norm"].eq(commodity_norm)].copy()
    exact = sub.loc[sub["type_norm"].eq(type_norm)].copy()
    if not exact.empty:
        return exact
    type_words = [w for w in type_norm.lower().replace(",", " ").split() if len(w) > 2]
    fallback = sub.loc[
        sub["type_norm"].str.lower().map(lambda x: all(w in x for w in type_words))
    ].copy()
    if not fallback.empty:
        warn(f"USGS type fallback used for {commodity}: requested '{prod_type}'")
        return fallback
    raise ValueError(f"No USGS rows matched commodity={commodity}, type={prod_type}")


def build_production_availability() -> tuple[pd.DataFrame, pd.DataFrame]:
    world = load_usgs_world_data()
    audit_rows: list[dict] = []
    country_rows: list[dict] = []
    year_cols = {2023: "PROD_2023", 2024: "PROD_EST_ 2024"}

    for hs, spec in USGS_PRODUCT_MAP.items():
        matched = match_usgs_rows(world, spec["commodity"], spec["type"])
        actual_commodity = matched["commodity_norm"].dropna().iloc[0]
        actual_type = matched["type_norm"].dropna().iloc[0]
        for year, prod_col in year_cols.items():
            sub = matched.copy()
            sub["production"] = clean_numeric(sub[prod_col])
            sub["is_china"] = sub["country_norm"].eq("China")
            sub["is_world_total"] = sub["country_norm"].str.startswith("World total")
            sub["is_row"] = ~sub["is_china"] & ~sub["is_world_total"]

            china_prod = float(sub.loc[sub["is_china"], "production"].sum(min_count=1))
            world_total_vals = sub.loc[sub["is_world_total"], "production"].dropna()
            world_total = float(world_total_vals.iloc[0]) if not world_total_vals.empty else np.nan

            row_listed_df = sub.loc[
                sub["is_row"] & sub["production"].notna() & sub["production"].gt(0)
            ].copy()
            row_listed = float(row_listed_df["production"].sum()) if not row_listed_df.empty else np.nan
            row_world_minus = (
                float(world_total - china_prod)
                if np.isfinite(world_total) and np.isfinite(china_prod)
                else np.nan
            )

            hhi_values = row_listed_df["production"].astype(float).tolist()
            notes = [spec["interpretation"]]
            residual = np.nan
            if np.isfinite(row_world_minus) and np.isfinite(row_listed):
                residual = row_world_minus - row_listed
                if residual > max(1e-9, 0.001 * max(row_world_minus, 1.0)):
                    hhi_values.append(float(residual))
                    notes.append(f"positive residual added to HHI: {residual:g}")
                elif abs(residual) > max(1e-9, 0.001 * max(row_world_minus, 1.0)):
                    notes.append(f"world-minus-China differs from listed RoW by {residual:g}")
                else:
                    notes.append(f"rounding residual {residual:g}")

            hhi_total = float(np.nansum(hhi_values)) if hhi_values else np.nan
            if np.isfinite(hhi_total) and hhi_total > 0:
                shares = np.array(hhi_values, dtype=float) / hhi_total
                hhi = float(np.sum(shares**2))
            else:
                hhi = np.nan
            diversity = 1 - hhi if np.isfinite(hhi) else np.nan

            scale_listed = (
                float(min(1.0, row_listed / china_prod))
                if np.isfinite(row_listed) and np.isfinite(china_prod) and china_prod > 0
                else np.nan
            )
            scale_world = (
                float(min(1.0, row_world_minus / china_prod))
                if np.isfinite(row_world_minus) and np.isfinite(china_prod) and china_prod > 0
                else np.nan
            )
            scale_pref = scale_world if np.isfinite(scale_world) else scale_listed
            a_prod = (
                float(np.clip(scale_pref * diversity, 0, 1))
                if np.isfinite(scale_pref) and np.isfinite(diversity)
                else np.nan
            )

            countries_used = "; ".join(row_listed_df["country_norm"].astype(str).tolist())
            audit_rows.append(
                {
                    "hs": hs,
                    "product_name": spec["product_name"],
                    "usgs_commodity": actual_commodity,
                    "usgs_type": actual_type,
                    "year": year,
                    "china_production": china_prod,
                    "row_production_listed": row_listed,
                    "world_total": world_total,
                    "row_production_world_minus_china": row_world_minus,
                    "scale_prod_listed": scale_listed,
                    "scale_prod_world_total": scale_world,
                    "scale_prod_preferred": scale_pref,
                    "hhi_row_prod": hhi,
                    "diversity_prod": diversity,
                    "A_prod": a_prod,
                    "countries_used": countries_used,
                    "notes": " ".join(notes),
                }
            )

            for _, row in sub.iterrows():
                prod = row["production"]
                if pd.isna(prod):
                    continue
                country_rows.append(
                    {
                        "hs": hs,
                        "product_name": spec["product_name"],
                        "usgs_commodity": actual_commodity,
                        "usgs_type": actual_type,
                        "year": year,
                        "country": row["country_norm"],
                        "production": float(prod),
                        "is_china": bool(row["is_china"]),
                        "is_row": bool(row["is_row"]),
                        "is_world_total": bool(row["is_world_total"]),
                        "source_file": str(USGS_WORLD_CSV),
                    }
                )
            if np.isfinite(residual) and residual > max(1e-9, 0.001 * max(row_world_minus, 1.0)):
                country_rows.append(
                    {
                        "hs": hs,
                        "product_name": spec["product_name"],
                        "usgs_commodity": actual_commodity,
                        "usgs_type": actual_type,
                        "year": year,
                        "country": "Unlisted residual (world total minus listed rows)",
                        "production": float(residual),
                        "is_china": False,
                        "is_row": True,
                        "is_world_total": False,
                        "source_file": str(USGS_WORLD_CSV),
                    }
                )

    return pd.DataFrame(audit_rows), pd.DataFrame(country_rows)


def load_source_panel() -> pd.DataFrame:
    source = pd.read_csv(SOURCE_PANEL, dtype={"hs": str, "period": str}, low_memory=False)
    return add_time_columns(source)


def load_wide_panel() -> pd.DataFrame:
    wide = pd.read_csv(WIDE_PANEL, dtype={"hs": str, "period": str}, low_memory=False)
    wide = add_time_columns(wide)
    wide["fe_importer_month"] = (
        wide["reporterCode"].astype(str) + "_" + wide["period"].astype(str)
    )
    wide["fe_product_month"] = wide["hs"].astype(str) + "_" + wide["period"].astype(str)
    wide["fe_importer_product"] = (
        wide["reporterCode"].astype(str) + "_" + wide["hs"].astype(str)
    )
    return wide


def make_quarterly_source(monthly: pd.DataFrame) -> pd.DataFrame:
    meta_cols = [
        "product",
        "analysis_role",
        "policy_screened",
        "wave",
        "policy_episode",
        "announcement_date",
        "implementation_date",
        "import_effect_month",
        "treatment_status",
        "scope_status",
        "usable_as_control",
        "net_weight_usable",
    ]
    pressure_cols = [c for c in monthly.columns if c.startswith(("E_", "O_", "K_", "P_", "A_", "R_"))]
    keep_cols = meta_cols + pressure_cols
    for col in keep_cols:
        if col not in monthly.columns:
            monthly[col] = np.nan

    group_cols = ["reporterCode", "quarter", "hs", "source", "china_source"]
    q = (
        monthly.groupby(group_cols, as_index=False)
        .agg(
            trade_value_usd=("trade_value_usd", "sum"),
            net_weight_kg=("net_weight_kg", "sum"),
            **{col: (col, "first") for col in keep_cols},
        )
        .copy()
    )
    q["quarter_index"] = q["quarter"].map(quarter_index)
    q["fe_importer_quarter"] = q["reporterCode"].astype(str) + "_" + q["quarter"]
    q["fe_product_quarter"] = q["hs"].astype(str) + "_" + q["quarter"]
    q["fe_source_quarter"] = q["source"].astype(str) + "_" + q["quarter"]
    q["fe_importer_product_source"] = (
        q["reporterCode"].astype(str) + "_" + q["hs"].astype(str) + "_" + q["source"]
    )
    return q


def make_quarterly_wide(monthly: pd.DataFrame) -> pd.DataFrame:
    meta_cols = [
        "product",
        "analysis_role",
        "policy_screened",
        "wave",
        "policy_episode",
        "announcement_date",
        "implementation_date",
        "import_effect_month",
        "treatment_status",
        "scope_status",
        "usable_as_control",
        "world_net_weight_usable",
        "china_net_weight_usable",
        "non_china_net_weight_usable",
    ]
    pressure_cols = [c for c in monthly.columns if c.startswith(("E_", "O_", "K_", "P_", "A_", "R_"))]
    keep_cols = meta_cols + pressure_cols
    for col in keep_cols:
        if col not in monthly.columns:
            monthly[col] = np.nan

    group_cols = ["reporterCode", "quarter", "hs"]
    q = (
        monthly.groupby(group_cols, as_index=False)
        .agg(
            china_primaryValue=("china_primaryValue", "sum"),
            non_china_primaryValue=("non_china_primaryValue", "sum"),
            world_primaryValue=("world_primaryValue", "sum"),
            china_netWgt=("china_netWgt", "sum"),
            non_china_netWgt=("non_china_netWgt", "sum"),
            world_netWgt=("world_netWgt", "sum"),
            **{col: (col, "first") for col in keep_cols},
        )
        .copy()
    )
    q["quarter_index"] = q["quarter"].map(quarter_index)
    q["fe_importer_quarter"] = q["reporterCode"].astype(str) + "_" + q["quarter"]
    q["fe_product_quarter"] = q["hs"].astype(str) + "_" + q["quarter"]
    q["fe_importer_product"] = q["reporterCode"].astype(str) + "_" + q["hs"].astype(str)
    return q


def build_revised_pressure(source: pd.DataFrame, production_audit: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "reporterCode",
        "hs",
        "product",
        "analysis_role",
        "policy_screened",
        "wave",
        "policy_episode",
        "announcement_date",
        "implementation_date",
        "import_effect_month",
        "treatment_status",
        "scope_status",
        "usable_as_control",
        "pre_month_count",
        "pre_china_value",
        "pre_row_value",
        "pre_world_value",
        "pre_row_positive_months",
        "row_total_value_loo",
        "row_hhi_loo",
        "row_diversification_loo",
        "row_market_scale_loo",
    ]
    for col in cols:
        if col not in source.columns:
            source[col] = np.nan
    ip = source[cols].drop_duplicates(["reporterCode", "hs"]).copy()
    for col in [
        "pre_month_count",
        "pre_china_value",
        "pre_row_value",
        "pre_world_value",
        "pre_row_positive_months",
        "row_total_value_loo",
        "row_hhi_loo",
        "row_diversification_loo",
        "row_market_scale_loo",
    ]:
        ip[col] = clean_numeric(ip[col])

    a_wide = (
        production_audit.pivot_table(index="hs", columns="year", values="A_prod", aggfunc="first")
        .rename(columns={2023: "A_prod_2023", 2024: "A_prod_2024"})
        .reset_index()
    )
    for col in ["A_prod_2023", "A_prod_2024"]:
        if col not in a_wide.columns:
            a_wide[col] = np.nan
    a_wide["A_prod_avg_2023_2024"] = a_wide[["A_prod_2023", "A_prod_2024"]].mean(axis=1)
    ip = ip.merge(a_wide, on="hs", how="left")

    total = ip["pre_china_value"] + ip["pre_row_value"]
    ip["E_china"] = np.where(total.gt(0), ip["pre_china_value"] / total, np.nan)

    ip["O_cap"] = np.nan
    china_pos = ip["pre_china_value"].gt(0)
    row_pos = ip["pre_row_value"].gt(0)
    ip.loc[china_pos, "O_cap"] = np.minimum(
        1.0,
        ip.loc[china_pos, "pre_row_value"] / ip.loc[china_pos, "pre_china_value"],
    )
    ip.loc[~china_pos & row_pos, "O_cap"] = 1.0

    ip["O_freq"] = np.where(
        ip["pre_month_count"].gt(0),
        ip["pre_row_positive_months"] / ip["pre_month_count"],
        np.nan,
    )
    ip["O_freq"] = ip["O_freq"].clip(lower=0, upper=1)

    row_china_ratio = np.where(
        ip["pre_china_value"].gt(0),
        ip["pre_row_value"] / ip["pre_china_value"],
        np.nan,
    )
    meaningful = ip["O_freq"].ge(0.25) & (
        (ip["pre_china_value"].gt(0) & pd.Series(row_china_ratio, index=ip.index).ge(0.10))
        | (ip["pre_china_value"].eq(0) & ip["pre_row_value"].gt(0))
    )
    ip["O_bin"] = np.where(total.gt(0), meaningful.astype(float), np.nan)

    ip["A_trade_loo_reference"] = (
        ip["row_market_scale_loo"] * ip["row_diversification_loo"]
    ).clip(lower=0, upper=1)
    ip["R_prod_2023"] = 1 - ip["A_prod_2023"]
    ip["R_prod_2024"] = 1 - ip["A_prod_2024"]
    ip["P_X"] = ip["E_china"]

    for variant, cfg in PRESSURE_VARIANTS.items():
        o_col = cfg["O"]
        a_col = cfg["A"]
        k_col = cfg["K"]
        ps_col = cfg["PS"]
        pc_col = cfg["PC"]
        ip[k_col] = (ip[o_col] * ip[a_col]).clip(lower=0, upper=1)
        ip[ps_col] = ip["E_china"] * ip[k_col]
        ip[pc_col] = ip["E_china"] * (1 - ip[k_col])

    edge_rows = [
        ("zero_pre_world_exposure_missing", int(total.eq(0).sum())),
        ("china_zero_row_positive", int((ip["pre_china_value"].eq(0) & row_pos).sum())),
        ("china_positive_row_zero", int((china_pos & ip["pre_row_value"].eq(0)).sum())),
        ("a_prod_2023_missing", int(ip["A_prod_2023"].isna().sum())),
        ("a_prod_2024_missing", int(ip["A_prod_2024"].isna().sum())),
        ("capacity_missing", int(ip["O_cap"].isna().sum())),
    ]
    for name, count in edge_rows:
        warn(f"pressure edge case {name}: {count}")

    return ip


def attach_pressure(df: pd.DataFrame, pressure: pd.DataFrame) -> pd.DataFrame:
    pressure_cols = [
        "reporterCode",
        "hs",
        "E_china",
        "O_cap",
        "O_freq",
        "O_bin",
        "A_trade_loo_reference",
        "A_prod_2023",
        "A_prod_2024",
        "A_prod_avg_2023_2024",
        "R_prod_2023",
        "R_prod_2024",
        "P_X",
    ]
    for cfg in PRESSURE_VARIANTS.values():
        pressure_cols.extend([cfg["K"], cfg["PS"], cfg["PC"]])
    pressure_cols = list(dict.fromkeys(pressure_cols))
    keep = pressure[pressure_cols].drop_duplicates(["reporterCode", "hs"])
    base = df.drop(columns=[c for c in pressure_cols if c in df.columns and c not in {"reporterCode", "hs"}])
    return base.merge(keep, on=["reporterCode", "hs"], how="left")


def sample_for_group(df: pd.DataFrame, group: Group) -> pd.DataFrame:
    treated = set(group.treated_hs)
    out = df.loc[df["analysis_role"].eq(CONTROL_ROLE) | df["hs"].isin(treated)].copy()
    out["treated_group"] = out["hs"].isin(treated)
    out["US_i"] = out["reporterCode"].astype(str).eq("842").astype(int)
    return out


def add_post_and_d(sample: pd.DataFrame, group: Group, anchor: str, freq: str, source_panel: bool) -> pd.DataFrame:
    out = sample.copy()
    period_col = "period" if freq == "monthly" else "quarter"
    anchor_map = {hs: anchor_period(hs, anchor, freq) for hs in group.treated_hs}
    default_anchor = next(iter(anchor_map.values()))
    out["_anchor_period"] = out["hs"].map(anchor_map).fillna(default_anchor)
    post = period_ge(out[period_col], out["_anchor_period"], freq)
    out["post_group"] = np.where(out["treated_group"], post, False).astype(int)
    if source_panel:
        out["D"] = (
            out["treated_group"] & out["china_source"].astype(bool) & out["post_group"].astype(bool)
        ).astype(int)
    else:
        out["TP"] = (out["treated_group"] & out["post_group"].astype(bool)).astype(int)
    return out


def standardize_for_group(
    sample: pd.DataFrame,
    group: Group,
    variables: Iterable[str],
    suffix: str = "_std",
) -> tuple[pd.DataFrame, dict[str, tuple[float, float, int]]]:
    out = sample.copy()
    stats: dict[str, tuple[float, float, int]] = {}
    ip = out[["reporterCode", "hs", "treated_group", *variables]].drop_duplicates(
        ["reporterCode", "hs"]
    )
    treated_mask = ip["treated_group"].eq(True)
    for var in variables:
        values = clean_numeric(ip.loc[treated_mask, var]).dropna()
        n = int(values.shape[0])
        if n == 0:
            mean = np.nan
            sd = np.nan
            out[f"{var}{suffix}"] = np.nan
            warn(f"{group.key}: no treated values for standardizing {var}")
        else:
            mean = float(values.mean())
            sd = float(values.std(ddof=0))
            if not np.isfinite(sd) or sd <= 0:
                out[f"{var}{suffix}"] = np.nan
                warn(f"{group.key}: zero variance for standardizing {var}")
            else:
                out[f"{var}{suffix}"] = (clean_numeric(out[var]) - mean) / sd
        stats[var] = (mean, sd, n)
        standardization_audit_rows.append(
            {
                "variable": var,
                "group": group.key,
                "mean_used": mean,
                "sd_used": sd,
                "n_cells_used": n,
                "standardization_scope": group.family,
            }
        )
    return out, stats


def fit_ppml(
    data: pd.DataFrame,
    outcome: str,
    x_cols: list[str],
    fe_cols: list[str],
    meta: dict,
    min_rows: int = 50,
) -> list[dict]:
    needed = [outcome, "reporterCode", "hs", *x_cols, *fe_cols]
    missing_cols = [c for c in needed if c not in data.columns]
    if missing_cols:
        warn(f"{meta}: missing columns {missing_cols}")
        return []

    work = data[needed].copy()
    work[outcome] = clean_numeric(work[outcome])
    for col in x_cols:
        work[col] = clean_numeric(work[col])
    work = work.dropna()
    work = work.loc[work[outcome].ge(0)].copy()
    input_rows = int(work.shape[0])
    if input_rows < min_rows:
        warn(f"{meta}: skipped, only {input_rows} usable rows")
        return []

    for col in x_cols:
        if work[col].nunique(dropna=True) <= 1:
            warn(f"{meta}: skipped, {col} has no variation")
            return []

    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(fe_cols)}"
    try:
        model = pf.fepois(
            formula,
            work,
            vcov={"CRV1": "reporter_cluster"},
            separation_check=["fe"],
            iwls_maxiter=100,
            iwls_tol=1e-7,
            fixef_tol=1e-7,
            fixef_maxiter=100000,
            demeaner_backend="numba",
            lean=False,
        )
    except Exception as exc:  # noqa: BLE001
        warn(f"{meta}: PPML failed: {exc}")
        return []

    coef_actual = model.coef()
    actual_terms = list(coef_actual.index)
    vcov = pd.DataFrame(model._vcov, index=actual_terms, columns=actual_terms)
    se_actual = pd.Series(np.sqrt(np.diag(vcov)), index=actual_terms)
    n_used = int(getattr(model, "_N", input_rows))
    rows = []
    for term in x_cols:
        if term not in coef_actual.index:
            warn(f"{meta}: term dropped or unavailable after estimation: {term}")
        beta = float(coef_actual.get(term, np.nan))
        term_se = float(se_actual.get(term, np.nan))
        row = {
            **meta,
            "outcome": outcome,
            "term": term,
            "coef": beta,
            "se": term_se,
            "p_value": p_value(beta, term_se),
            "percent_effect": percent_effect(beta),
            "n_before_ppml": input_rows,
            "n_used": n_used,
            "n_dropped_separation": input_rows - n_used,
            "fixed_effects": " + ".join(fe_cols),
            "cluster": "reporterCode",
            "formula": formula,
        }
        rows.append(row)
    return rows


def fit_ppml_with_vcov(
    data: pd.DataFrame,
    outcome: str,
    x_cols: list[str],
    fe_cols: list[str],
    meta: dict,
) -> tuple[list[dict], pd.Series | None, pd.DataFrame | None]:
    needed = [outcome, "reporterCode", "hs", *x_cols, *fe_cols]
    missing_cols = [c for c in needed if c not in data.columns]
    if missing_cols:
        warn(f"{meta}: missing columns {missing_cols}")
        return [], None, None

    work = data[needed].copy()
    work[outcome] = clean_numeric(work[outcome])
    for col in x_cols:
        work[col] = clean_numeric(work[col])
    work = work.dropna()
    work = work.loc[work[outcome].ge(0)].copy()
    input_rows = int(work.shape[0])
    if input_rows < 50:
        warn(f"{meta}: skipped, only {input_rows} usable rows")
        return [], None, None

    for col in x_cols:
        if work[col].nunique(dropna=True) <= 1:
            warn(f"{meta}: skipped, {col} has no variation")
            return [], None, None

    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(fe_cols)}"
    try:
        model = pf.fepois(
            formula,
            work,
            vcov={"CRV1": "reporter_cluster"},
            separation_check=["fe"],
            iwls_maxiter=100,
            iwls_tol=1e-7,
            fixef_tol=1e-7,
            fixef_maxiter=100000,
            demeaner_backend="numba",
            lean=False,
        )
    except Exception as exc:  # noqa: BLE001
        warn(f"{meta}: PPML vcov refit failed: {exc}")
        return [], None, None
    coef_actual = model.coef()
    actual_terms = list(coef_actual.index)
    vcov = pd.DataFrame(model._vcov, index=actual_terms, columns=actual_terms)
    se_actual = pd.Series(np.sqrt(np.diag(vcov)), index=actual_terms)
    n_used = int(getattr(model, "_N", input_rows))
    rows = []
    for term in x_cols:
        if term not in coef_actual.index:
            warn(f"{meta}: term dropped or unavailable after estimation: {term}")
        beta = float(coef_actual.get(term, np.nan))
        term_se = float(se_actual.get(term, np.nan))
        rows.append(
            {
                **meta,
                "outcome": outcome,
                "term": term,
                "coef": beta,
                "se": term_se,
                "p_value": p_value(beta, term_se),
                "percent_effect": percent_effect(beta),
                "n_before_ppml": input_rows,
                "n_used": n_used,
                "n_dropped_separation": input_rows - n_used,
                "fixed_effects": " + ".join(fe_cols),
                "cluster": "reporterCode",
                "formula": formula,
            }
        )
    return rows, coef_actual, vcov


def add_interaction_terms(
    data: pd.DataFrame,
    group: Group,
    anchor: str,
    freq: str,
    source_panel: bool,
    variables: list[str],
    prefix: str,
) -> tuple[pd.DataFrame, list[str]]:
    work = add_post_and_d(data, group, anchor, freq, source_panel=source_panel)
    work, _stats = standardize_for_group(work, group, variables)
    base = "D" if source_panel else "TP"
    terms = []
    for var in variables:
        std = f"{var}_std"
        term = f"{prefix}_{var}"
        work[term] = work[base] * work[std].fillna(0.0)
        terms.append(term)
    return work, terms


def filter_pressure_missing(
    data: pd.DataFrame,
    group: Group,
    variables: list[str],
) -> pd.DataFrame:
    out = data.copy()
    treated_ip = out["treated_group"].eq(True)
    missing = treated_ip & out[variables].isna().any(axis=1)
    if missing.any():
        dropped_ips = (
            out.loc[missing, ["reporterCode", "hs"]].drop_duplicates().shape[0]
        )
        warn(f"{group.key}: dropping {dropped_ips} treated importer-product cells with missing {variables}")
    return out.loc[~missing].copy()


def run_source_average(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ANCHORS:
            work = add_post_and_d(base, group, anchor, freq, source_panel=True)
            rows.extend(
                fit_ppml(
                    work,
                    "trade_value_usd",
                    ["D"],
                    fe,
                    {
                        "frequency": freq,
                        "model": "average_source_contrast",
                        "group": group.key,
                        "group_label": group.label,
                        "family": group.family,
                        "anchor": anchor,
                        "pressure_variant": "none",
                    },
                )
            )
    return pd.DataFrame(rows)


def run_source_exposure(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ANCHORS:
            work, terms = add_interaction_terms(
                base, group, anchor, freq, True, ["E_china"], "D"
            )
            work = filter_pressure_missing(work, group, ["E_china"])
            rows.extend(
                fit_ppml(
                    work,
                    "trade_value_usd",
                    ["D", *terms],
                    fe,
                    {
                        "frequency": freq,
                        "model": "source_contrast_E",
                        "group": group.key,
                        "group_label": group.label,
                        "family": group.family,
                        "anchor": anchor,
                        "pressure_variant": "exposure",
                    },
                )
            )
    return pd.DataFrame(rows)


def run_source_ps_pc(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ANCHORS:
            for variant, cfg in PRESSURE_VARIANTS.items():
                variables = [cfg["PS"], cfg["PC"]]
                work, terms = add_interaction_terms(
                    base, group, anchor, freq, True, variables, "D"
                )
                work = filter_pressure_missing(work, group, variables)
                rows.extend(
                    fit_ppml(
                        work,
                        "trade_value_usd",
                        ["D", *terms],
                        fe,
                        {
                            "frequency": freq,
                            "model": "source_contrast_PS_PC",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
    return pd.DataFrame(rows)


def run_source_e_k(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    variants = {"capacity": PRESSURE_VARIANTS["capacity"]}
    warn(f"{freq} E/K diagnostic restricted to capacity baseline to keep the auxiliary grid tractable")
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ANCHORS:
            for variant, cfg in variants.items():
                variables = ["E_china", cfg["K"]]
                work, terms = add_interaction_terms(
                    base, group, anchor, freq, True, variables, "D"
                )
                work = filter_pressure_missing(work, group, variables)
                rows.extend(
                    fit_ppml(
                        work,
                        "trade_value_usd",
                        ["D", *terms],
                        fe,
                        {
                            "frequency": freq,
                            "model": "source_contrast_E_K",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
    return pd.DataFrame(rows)


def run_mechanism(panel: pd.DataFrame, freq: str, outcome: str, kind: str) -> pd.DataFrame:
    rows = []
    fe = WIDE_MONTHLY_FE if freq == "monthly" else WIDE_QUARTERLY_FE
    for group in GROUPS:
        base = sample_for_group(panel, group)
        anchor = "first_full_post_quarter"
        for variant, cfg in PRESSURE_VARIANTS.items():
            variables = [cfg["PS"], cfg["PC"]]
            work, terms = add_interaction_terms(
                base, group, anchor, freq, False, variables, "TP"
            )
            work = filter_pressure_missing(work, group, variables)
            ps_term, pc_term = terms
            if kind == "row":
                rows.extend(
                    fit_ppml(
                        work,
                        outcome,
                        [ps_term],
                        fe,
                        {
                            "frequency": freq,
                            "model": "row_switch_only",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
                rows.extend(
                    fit_ppml(
                        work,
                        outcome,
                        [ps_term, pc_term],
                        fe,
                        {
                            "frequency": freq,
                            "model": "row_full_PS_PC",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
            else:
                rows.extend(
                    fit_ppml(
                        work,
                        outcome,
                        [pc_term],
                        fe,
                        {
                            "frequency": freq,
                            "model": "total_compress_only",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
                rows.extend(
                    fit_ppml(
                        work,
                        outcome,
                        [ps_term, pc_term],
                        fe,
                        {
                            "frequency": freq,
                            "model": "total_full_PS_PC",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "pressure_variant": variant,
                        },
                    )
                )
    return pd.DataFrame(rows)


def local_event_time(sample: pd.DataFrame, group: Group, anchor: str, freq: str) -> pd.Series:
    period_col = "period" if freq == "monthly" else "quarter"
    anchor_map = {hs: anchor_period(hs, anchor, freq) for hs in group.treated_hs}
    default_anchor = next(iter(anchor_map.values()))
    anchor_series = sample["hs"].map(anchor_map).fillna(default_anchor)
    if freq == "monthly":
        return sample[period_col].astype(str).map(month_index) - anchor_series.astype(str).map(month_index)
    return sample[period_col].astype(str).map(quarter_index) - anchor_series.astype(str).map(quarter_index)


def joint_pretrend_rows(
    coef: pd.Series | None,
    vcov: pd.DataFrame | None,
    lead_terms: list[str],
    meta: dict,
    fe_cols: list[str] | None = None,
) -> list[dict]:
    if coef is None or vcov is None:
        return []
    terms = [t for t in lead_terms if t in coef.index]
    if not terms:
        return []
    b = coef.reindex(terms).astype(float).to_numpy()
    v = vcov.reindex(index=terms, columns=terms).astype(float).to_numpy()
    stat = float(b.T @ np.linalg.pinv(v) @ b)
    df = len(terms)
    return [
        {
            **meta,
            "row_type": "joint_pretrend",
            "term": "joint_pretrend",
            "coef": stat,
            "se": np.nan,
            "p_value": float(chi2.sf(stat, df)),
            "percent_effect": np.nan,
            "joint_df": df,
            "n_before_ppml": np.nan,
            "n_used": np.nan,
            "n_dropped_separation": np.nan,
            "fixed_effects": " + ".join(fe_cols or QUARTERLY_FE),
            "cluster": "reporterCode",
            "formula": "",
        }
    ]


def run_event_average(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ["announcement", "implementation", "import_effect", "first_full_post_quarter"]:
            work = base.copy()
            work["event_time"] = local_event_time(work, group, anchor, freq)
            work = work.loc[work["event_time"].between(-4, 4)].copy()
            event_terms = []
            for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
                name = f"event_{'m' if k < 0 else 'p'}{abs(k)}"
                work[name] = (
                    work["treated_group"]
                    & work["china_source"].astype(bool)
                    & work["event_time"].eq(k)
                ).astype(int)
                event_terms.append(name)
            meta = {
                "frequency": freq,
                "model": "average_event_study",
                "group": group.key,
                "group_label": group.label,
                "family": group.family,
                "anchor": anchor,
                "pressure_variant": "none",
                "row_type": "coefficient",
            }
            fit_rows, coef, vcov = fit_ppml_with_vcov(
                work, "trade_value_usd", event_terms, fe, meta
            )
            rows.extend(fit_rows)
            rows.extend(
                joint_pretrend_rows(
                    coef, vcov, ["event_m4", "event_m3", "event_m2"], meta, fe
                )
            )
    return pd.DataFrame(rows)


def run_event_pressure(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    gradients = ["E_china", "P_S_cap_prod", "P_C_cap_prod"]
    for group in GROUPS:
        base = sample_for_group(panel, group)
        base, _stats = standardize_for_group(base, group, gradients)
        base = filter_pressure_missing(base, group, gradients)
        for anchor in ["announcement", "implementation", "import_effect", "first_full_post_quarter"]:
            work0 = base.copy()
            work0["event_time"] = local_event_time(work0, group, anchor, freq)
            work0 = work0.loc[work0["event_time"].between(-4, 4)].copy()
            for gradient in gradients:
                work = work0.copy()
                event_terms = []
                for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
                    name = f"event_{'m' if k < 0 else 'p'}{abs(k)}_{gradient}"
                    work[name] = (
                        work["treated_group"].astype(bool)
                        & work["china_source"].astype(bool)
                        & work["event_time"].eq(k)
                    ).astype(int) * work[f"{gradient}_std"].fillna(0.0)
                    event_terms.append(name)
                meta = {
                    "frequency": freq,
                    "model": "pressure_gradient_event_study",
                    "group": group.key,
                    "group_label": group.label,
                    "family": group.family,
                    "anchor": anchor,
                    "pressure_variant": "capacity",
                    "gradient": gradient,
                    "row_type": "coefficient",
                }
                fit_rows, coef, vcov = fit_ppml_with_vcov(
                    work, "trade_value_usd", event_terms, fe, meta
                )
                rows.extend(fit_rows)
                rows.extend(
                    joint_pretrend_rows(
                        coef,
                        vcov,
                        [
                            f"event_m4_{gradient}",
                            f"event_m3_{gradient}",
                            f"event_m2_{gradient}",
                        ],
                        meta,
                        fe,
                    )
                )
    return pd.DataFrame(rows)


def run_event_average_quarterly(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group in GROUPS:
        base = sample_for_group(panel, group)
        for anchor in ["announcement", "implementation", "import_effect", "first_full_post_quarter"]:
            work = base.copy()
            work["event_time"] = local_event_time(work, group, anchor, "quarterly")
            work = work.loc[work["event_time"].between(-4, 4)].copy()
            event_terms = []
            for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
                name = f"event_{'m' if k < 0 else 'p'}{abs(k)}"
                work[name] = (
                    work["treated_group"]
                    & work["china_source"].astype(bool)
                    & work["event_time"].eq(k)
                ).astype(int)
                event_terms.append(name)
            meta = {
                "frequency": "quarterly",
                "model": "average_event_study",
                "group": group.key,
                "group_label": group.label,
                "family": group.family,
                "anchor": anchor,
                "pressure_variant": "none",
                "row_type": "coefficient",
            }
            fit_rows, coef, vcov = fit_ppml_with_vcov(
                work, "trade_value_usd", event_terms, QUARTERLY_FE, meta
            )
            rows.extend(fit_rows)
            rows.extend(joint_pretrend_rows(coef, vcov, ["event_m4", "event_m3", "event_m2"], meta))
    return pd.DataFrame(rows)


def run_event_pressure_quarterly(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    gradients = ["E_china", "P_S_cap_prod", "P_C_cap_prod"]
    for group in GROUPS:
        base = sample_for_group(panel, group)
        base, _stats = standardize_for_group(base, group, gradients)
        base = filter_pressure_missing(base, group, gradients)
        for anchor in ["announcement", "implementation", "import_effect", "first_full_post_quarter"]:
            work0 = base.copy()
            work0["event_time"] = local_event_time(work0, group, anchor, "quarterly")
            work0 = work0.loc[work0["event_time"].between(-4, 4)].copy()
            for gradient in gradients:
                work = work0.copy()
                event_terms = []
                for k in [-4, -3, -2, 0, 1, 2, 3, 4]:
                    name = f"event_{'m' if k < 0 else 'p'}{abs(k)}_{gradient}"
                    work[name] = (
                        work["treated_group"].astype(bool)
                        & work["china_source"].astype(bool)
                        & work["event_time"].eq(k)
                    ).astype(int) * work[f"{gradient}_std"].fillna(0.0)
                    event_terms.append(name)
                meta = {
                    "frequency": "quarterly",
                    "model": "pressure_gradient_event_study",
                    "group": group.key,
                    "group_label": group.label,
                    "family": group.family,
                    "anchor": anchor,
                    "pressure_variant": "capacity",
                    "gradient": gradient,
                    "row_type": "coefficient",
                }
                fit_rows, coef, vcov = fit_ppml_with_vcov(
                    work, "trade_value_usd", event_terms, QUARTERLY_FE, meta
                )
                rows.extend(fit_rows)
                rows.extend(
                    joint_pretrend_rows(
                        coef,
                        vcov,
                        [
                            f"event_m4_{gradient}",
                            f"event_m3_{gradient}",
                            f"event_m2_{gradient}",
                        ],
                        meta,
                    )
                )
    return pd.DataFrame(rows)


def shift_month(month: str, delta: int) -> str:
    idx = month_index(month) + delta
    year = (idx - 1) // 12
    mon = idx - year * 12
    return f"{year:04d}{mon:02d}"


def shift_quarter(quarter: str, delta_quarters: int) -> str:
    idx = quarter_index(quarter) + delta_quarters
    year = (idx - 1) // 4
    q = idx - year * 4
    return f"{year:04d}Q{q}"


def run_placebo(panel: pd.DataFrame, freq: str, pressure: bool) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    lags = [-24, -12] if freq == "monthly" else [-24, -12, -36]
    anchors = (
        ["first_full_post_quarter"]
        if freq == "monthly"
        else ["implementation", "import_effect", "first_full_post_quarter"]
    )
    if freq == "monthly":
        warn(
            "monthly placebo diagnostics restricted to first_full_post_quarter with -24 and -12 month placebo dates"
        )
    for group in GROUPS:
        base = sample_for_group(panel, group)
        if pressure:
            base, _stats = standardize_for_group(base, group, ["P_S_cap_prod", "P_C_cap_prod", "E_china"])
            base = filter_pressure_missing(base, group, ["P_S_cap_prod", "P_C_cap_prod", "E_china"])
        for lag in lags:
            for anchor in anchors:
                work = base.copy()
                real_map = {hs: anchor_period(hs, anchor, freq) for hs in group.treated_hs}
                if freq == "monthly":
                    placebo_map = {hs: shift_month(p, lag) for hs, p in real_map.items()}
                else:
                    placebo_map = {
                        hs: shift_quarter(p, int(lag / 3)) for hs, p in real_map.items()
                    }
                default_real = next(iter(real_map.values()))
                default_placebo = next(iter(placebo_map.values()))
                real_series = work["hs"].map(real_map).fillna(default_real)
                placebo_series = work["hs"].map(placebo_map).fillna(default_placebo)
                period_col = "period" if freq == "monthly" else "quarter"
                pre_real = period_lt(work[period_col], real_series, freq)
                work = work.loc[~work["treated_group"] | pre_real].copy()
                placebo_series = work["hs"].map(placebo_map).fillna(default_placebo)
                post_fake = period_ge(work[period_col], placebo_series, freq)
                work["D_placebo"] = (
                    work["treated_group"]
                    & work["china_source"].astype(bool)
                    & post_fake
                ).astype(int)
                if pressure:
                    work["D_placebo_PS_cap_prod"] = work["D_placebo"] * work["P_S_cap_prod_std"].fillna(0.0)
                    work["D_placebo_PC_cap_prod"] = work["D_placebo"] * work["P_C_cap_prod_std"].fillna(0.0)
                    x_cols = ["D_placebo", "D_placebo_PS_cap_prod", "D_placebo_PC_cap_prod"]
                    model = "placebo_pressure"
                else:
                    x_cols = ["D_placebo"]
                    model = "placebo_average"
                rows.extend(
                    fit_ppml(
                        work,
                        "trade_value_usd",
                        x_cols,
                        fe,
                        {
                            "frequency": freq,
                            "model": model,
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "placebo_lag_months": lag,
                            "pressure_variant": "capacity" if pressure else "none",
                        },
                    )
                )
    return pd.DataFrame(rows)


def run_placebo_exposure(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    lags = [-24, -12] if freq == "monthly" else [-24, -12, -36]
    anchors = (
        ["first_full_post_quarter"]
        if freq == "monthly"
        else ["implementation", "import_effect", "first_full_post_quarter"]
    )
    for group in GROUPS:
        base = sample_for_group(panel, group)
        base, _stats = standardize_for_group(base, group, ["E_china"])
        base = filter_pressure_missing(base, group, ["E_china"])
        for lag in lags:
            for anchor in anchors:
                work = base.copy()
                real_map = {hs: anchor_period(hs, anchor, freq) for hs in group.treated_hs}
                if freq == "monthly":
                    placebo_map = {hs: shift_month(p, lag) for hs, p in real_map.items()}
                else:
                    placebo_map = {
                        hs: shift_quarter(p, int(lag / 3)) for hs, p in real_map.items()
                    }
                default_real = next(iter(real_map.values()))
                default_placebo = next(iter(placebo_map.values()))
                real_series = work["hs"].map(real_map).fillna(default_real)
                period_col = "period" if freq == "monthly" else "quarter"
                pre_real = period_lt(work[period_col], real_series, freq)
                work = work.loc[~work["treated_group"] | pre_real].copy()
                placebo_series = work["hs"].map(placebo_map).fillna(default_placebo)
                post_fake = period_ge(work[period_col], placebo_series, freq)
                work["D_placebo"] = (
                    work["treated_group"]
                    & work["china_source"].astype(bool)
                    & post_fake
                ).astype(int)
                work["D_placebo_E_china"] = work["D_placebo"] * work["E_china_std"].fillna(0.0)
                rows.extend(
                    fit_ppml(
                        work,
                        "trade_value_usd",
                        ["D_placebo", "D_placebo_E_china"],
                        fe,
                        {
                            "frequency": freq,
                            "model": "placebo_exposure",
                            "group": group.key,
                            "group_label": group.label,
                            "family": group.family,
                            "anchor": anchor,
                            "placebo_lag_months": lag,
                            "pressure_variant": "exposure",
                        },
                    )
                )
    return pd.DataFrame(rows)


def run_us_interactions(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    anchor = "first_full_post_quarter"
    for group in GROUPS:
        base = sample_for_group(panel, group)
        base, _stats = standardize_for_group(base, group, ["E_china", "P_S_cap_prod", "P_C_cap_prod"])
        base = filter_pressure_missing(base, group, ["E_china", "P_S_cap_prod", "P_C_cap_prod"])
        work = add_post_and_d(base, group, anchor, freq, source_panel=True)
        work["D_US"] = work["D"] * work["US_i"]
        work["D_E_china"] = work["D"] * work["E_china_std"].fillna(0.0)
        work["D_P_S_cap_prod"] = work["D"] * work["P_S_cap_prod_std"].fillna(0.0)
        work["D_P_C_cap_prod"] = work["D"] * work["P_C_cap_prod_std"].fillna(0.0)
        specs = [
            ("us_average", ["D", "D_US"]),
            ("us_exposure", ["D", "D_E_china", "D_US"]),
            (
                "us_pressure",
                ["D", "D_P_S_cap_prod", "D_P_C_cap_prod", "D_US"],
            ),
        ]
        for model, x_cols in specs:
            meta = {
                "frequency": freq,
                "model": model,
                "group": group.key,
                "group_label": group.label,
                "family": group.family,
                "anchor": anchor,
                "pressure_variant": "capacity",
            }
            fit_rows, coef, vcov = fit_ppml_with_vcov(
                work, "trade_value_usd", x_cols, fe, meta
            )
            rows.extend(fit_rows)
            if coef is not None and vcov is not None and "D" in coef.index and "D_US" in coef.index:
                total = float(coef["D"] + coef["D_US"])
                var = float(
                    vcov.loc["D", "D"] + vcov.loc["D_US", "D_US"] + 2 * vcov.loc["D", "D_US"]
                )
                se = float(np.sqrt(var)) if var >= 0 else np.nan
                rows.append(
                    {
                        **meta,
                        "outcome": "trade_value_usd",
                        "term": "D_plus_D_US",
                        "coef": total,
                        "se": se,
                        "p_value": p_value(total, se),
                        "percent_effect": percent_effect(total),
                        "n_before_ppml": fit_rows[0]["n_before_ppml"] if fit_rows else np.nan,
                        "n_used": fit_rows[0]["n_used"] if fit_rows else np.nan,
                        "n_dropped_separation": fit_rows[0]["n_dropped_separation"] if fit_rows else np.nan,
                        "fixed_effects": " + ".join(fe),
                        "cluster": "reporterCode",
                        "formula": "",
                        "interpretation": "implied_total_us_effect",
                    }
                )
    return pd.DataFrame(rows)


def run_us_excluded(source_panel: pd.DataFrame, wide_panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    no_us_source = source_panel.loc[~source_panel["reporterCode"].astype(str).eq("842")].copy()
    no_us_wide = wide_panel.loc[~wide_panel["reporterCode"].astype(str).eq("842")].copy()
    pieces = [
        add_sign_columns(run_source_average(no_us_source, freq)),
        add_sign_columns(run_source_exposure(no_us_source, freq)),
        add_sign_columns(run_source_ps_pc(no_us_source, freq)),
        add_sign_columns(run_mechanism(no_us_wide, freq, "non_china_primaryValue", "row")),
        add_sign_columns(run_mechanism(no_us_wide, freq, "world_primaryValue", "total")),
    ]
    out = pd.concat(pieces, ignore_index=True, sort=False)
    out["sample_restriction"] = "exclude_us_reporter_842"
    return out


def run_net_weight(panel: pd.DataFrame, freq: str) -> pd.DataFrame:
    rows = []
    fe = MONTHLY_FE if freq == "monthly" else QUARTERLY_FE
    if "net_weight_kg" not in panel.columns:
        warn("net_weight_kg missing from source panel")
        return pd.DataFrame()
    usable = panel.loc[clean_numeric(panel["net_weight_kg"]).ge(0)].copy()
    if "net_weight_usable" in usable.columns:
        usable = usable.loc[usable["net_weight_usable"].fillna(False).astype(bool)].copy()
    anchor = "first_full_post_quarter"
    for group in GROUPS:
        base = sample_for_group(usable, group)
        base, _stats = standardize_for_group(base, group, ["E_china", "P_S_cap_prod", "P_C_cap_prod"])
        base = filter_pressure_missing(base, group, ["E_china", "P_S_cap_prod", "P_C_cap_prod"])
        work = add_post_and_d(base, group, anchor, freq, source_panel=True)
        work["D_E_china"] = work["D"] * work["E_china_std"].fillna(0.0)
        work["D_P_S_cap_prod"] = work["D"] * work["P_S_cap_prod_std"].fillna(0.0)
        work["D_P_C_cap_prod"] = work["D"] * work["P_C_cap_prod_std"].fillna(0.0)
        specs = [
            ("net_weight_average", ["D"]),
            ("net_weight_exposure", ["D", "D_E_china"]),
            ("net_weight_PS_PC", ["D", "D_P_S_cap_prod", "D_P_C_cap_prod"]),
        ]
        for model, x_cols in specs:
            rows.extend(
                fit_ppml(
                    work,
                    "net_weight_kg",
                    x_cols,
                    fe,
                    {
                        "frequency": freq,
                        "model": model,
                        "group": group.key,
                        "group_label": group.label,
                        "family": group.family,
                        "anchor": anchor,
                        "pressure_variant": "capacity",
                    },
                )
            )
    return pd.DataFrame(rows)


def pressure_summary_tables(pressure: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    clean = pressure.loc[pressure["hs"].isin(MAIN_TREATED_HS)].copy()
    variables = [
        "E_china",
        "O_cap",
        "O_freq",
        "O_bin",
        "A_prod_2023",
        "A_prod_2024",
        "K_cap_prod",
        "P_S_cap_prod",
        "P_C_cap_prod",
        "K_freq_prod",
        "P_S_freq_prod",
        "P_C_freq_prod",
        "K_bin_prod",
        "P_S_bin_prod",
        "P_C_bin_prod",
        "K_cap_prod_2024",
        "P_S_cap_prod_2024",
        "P_C_cap_prod_2024",
    ]
    rows = []
    for group_name, group_df in [("pooled_clean_treated", clean), *list(clean.groupby("hs"))]:
        if isinstance(group_name, tuple):
            group_key = str(group_name[0])
        else:
            group_key = str(group_name)
        product = "pooled" if group_key == "pooled_clean_treated" else group_df["product"].iloc[0]
        for var in variables:
            vals = clean_numeric(group_df[var]).dropna()
            q = vals.quantile([0.25, 0.5, 0.75]) if len(vals) else pd.Series([np.nan, np.nan, np.nan], index=[0.25, 0.5, 0.75])
            rows.append(
                {
                    "group": group_key,
                    "product": product,
                    "variable": var,
                    "count": int(vals.shape[0]),
                    "mean": float(vals.mean()) if len(vals) else np.nan,
                    "sd": float(vals.std(ddof=0)) if len(vals) else np.nan,
                    "min": float(vals.min()) if len(vals) else np.nan,
                    "p25": float(q.loc[0.25]) if len(vals) else np.nan,
                    "median": float(q.loc[0.5]) if len(vals) else np.nan,
                    "p75": float(q.loc[0.75]) if len(vals) else np.nan,
                    "max": float(vals.max()) if len(vals) else np.nan,
                }
            )
    summary = pd.DataFrame(rows)

    product_rows = []
    for hs, group_df in clean.groupby("hs", sort=False):
        row = {
            "hs": hs,
            "product": group_df["product"].iloc[0],
            "n_cells": group_df[["reporterCode", "hs"]].drop_duplicates().shape[0],
        }
        for var in variables:
            row[f"mean_{var}"] = clean_numeric(group_df[var]).mean()
            row[f"sd_{var}"] = clean_numeric(group_df[var]).std(ddof=0)
        row["corr_E_K_cap_prod"] = clean_numeric(group_df["E_china"]).corr(clean_numeric(group_df["K_cap_prod"]))
        row["corr_PS_PC_cap_prod"] = clean_numeric(group_df["P_S_cap_prod"]).corr(clean_numeric(group_df["P_C_cap_prod"]))
        row["corr_PS_E_cap_prod"] = clean_numeric(group_df["P_S_cap_prod"]).corr(clean_numeric(group_df["E_china"]))
        row["corr_PC_E_cap_prod"] = clean_numeric(group_df["P_C_cap_prod"]).corr(clean_numeric(group_df["E_china"]))
        row["corr_K_PC_cap_prod"] = clean_numeric(group_df["K_cap_prod"]).corr(clean_numeric(group_df["P_C_cap_prod"]))
        product_rows.append(row)
    by_product = pd.DataFrame(product_rows)

    corr_rows = []
    for group_name, group_df in [("pooled_clean_treated", clean), *list(clean.groupby("hs"))]:
        group_key = str(group_name[0]) if isinstance(group_name, tuple) else str(group_name)
        for left in ["E_china", "K_cap_prod", "P_S_cap_prod", "P_C_cap_prod"]:
            for right in ["E_china", "K_cap_prod", "P_S_cap_prod", "P_C_cap_prod"]:
                corr_rows.append(
                    {
                        "group": group_key,
                        "left": left,
                        "right": right,
                        "correlation": clean_numeric(group_df[left]).corr(clean_numeric(group_df[right])),
                    }
                )
    correlations = pd.DataFrame(corr_rows)
    return summary, by_product, correlations


def product_sample_table(meta_path: Path) -> pd.DataFrame:
    meta = pd.read_csv(meta_path, dtype={"hs": str}, low_memory=False)
    keep_hs = set(MAIN_TREATED_HS)
    roles = {CONTROL_ROLE, "main_clean_treated"}
    out = meta.loc[meta["hs"].isin(keep_hs) | meta["analysis_role"].isin(roles)].copy()
    cols = [
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
        "usable_as_control",
        "price_pair_status",
    ]
    return out[[c for c in cols if c in out.columns]].sort_values(["analysis_role", "hs"])


def run_price_wedges(pressure: pd.DataFrame) -> pd.DataFrame:
    script = REPO / "04_scripts" / "estimate_price_wedges.py"
    if script.exists():
        try:
            subprocess.run([sys.executable, str(script)], check=True, cwd=REPO)
            warn("price wedge script rerun; generated outputs were refreshed in 03_data/output/tables")
        except Exception as exc:  # noqa: BLE001
            warn(f"price wedge script failed: {exc}")
    else:
        warn("price wedge script not found")

    pieces = []
    for path, source_name in [
        (TABLES / "price_wedge_pair_its_results.csv", "pair_its"),
        (TABLES / "price_wedge_panel_did_results.csv", "panel_did"),
        (TABLES / "price_wedge_pair_audit_preliminary.csv", "pair_audit"),
    ]:
        if path.exists():
            df = pd.read_csv(path, dtype={"hs": str}, low_memory=False)
            df["price_output_source"] = source_name
            pieces.append(df)
        else:
            warn(f"missing price wedge output: {path}")
    if not pieces:
        return pd.DataFrame()
    prices = pd.concat(pieces, ignore_index=True, sort=False)
    product_pressure = (
        pressure.loc[pressure["hs"].isin(MAIN_TREATED_HS)]
        .groupby("hs", as_index=False)
        .agg(
            avg_E_china=("E_china", "mean"),
            avg_K_cap_prod=("K_cap_prod", "mean"),
            avg_P_S_cap_prod=("P_S_cap_prod", "mean"),
            avg_P_C_cap_prod=("P_C_cap_prod", "mean"),
            avg_A_prod_2023=("A_prod_2023", "mean"),
            avg_A_prod_2024=("A_prod_2024", "mean"),
        )
    )
    if "hs" in prices.columns:
        prices = prices.merge(product_pressure, on="hs", how="left")
    return prices


def old_trade_prod_comparison(outputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    old_root = REPO / "results" / "revised_pressure_K_trade_A"
    comparisons = []
    mapping = [
        (
            "source_contrast_PS_PC_quarterly.csv",
            outputs.get("source_contrast_PS_PC_quarterly", pd.DataFrame()),
            {"D_P_S_cap": "D_P_S_cap_prod", "D_P_C_cap": "D_P_C_cap_prod", "D": "D"},
        ),
        (
            "mechanism_row_quarterly.csv",
            outputs.get("mechanism_row_quarterly", pd.DataFrame()),
            {"TP_P_S_cap": "TP_P_S_cap_prod", "TP_P_C_cap": "TP_P_C_cap_prod"},
        ),
        (
            "mechanism_total_quarterly.csv",
            outputs.get("mechanism_total_quarterly", pd.DataFrame()),
            {"TP_P_S_cap": "TP_P_S_cap_prod", "TP_P_C_cap": "TP_P_C_cap_prod"},
        ),
        (
            "main_average_ppml_quarterly.csv",
            outputs.get("main_average_ppml_quarterly", pd.DataFrame()),
            {"D": "D"},
        ),
    ]
    for filename, new_df, term_map in mapping:
        old_path = old_root / filename
        if not old_path.exists() or new_df.empty:
            warn(f"trade-A comparison skipped for {filename}")
            continue
        old = pd.read_csv(old_path, low_memory=False)
        if "pressure_variant" in old.columns:
            old = old.loc[old["pressure_variant"].isin(["capacity", "none"])].copy()
        if "pressure_variant" in new_df.columns:
            new = new_df.loc[new_df["pressure_variant"].isin(["capacity", "none"])].copy()
        else:
            new = new_df.copy()
        if "anchor" in old.columns:
            old = old.loc[old["anchor"].eq("first_full_post_quarter")].copy()
        if "anchor" in new.columns:
            new = new.loc[new["anchor"].eq("first_full_post_quarter")].copy()
        for old_term, new_term in term_map.items():
            left = old.loc[old["term"].eq(old_term)].copy()
            right = new.loc[new["term"].eq(new_term)].copy()
            if left.empty or right.empty:
                continue
            keep = ["group", "model", "term", "coef", "p_value", "percent_effect", "matches_expected_sign"]
            left = left[[c for c in keep if c in left.columns]].rename(
                columns={
                    "term": "tradeA_term",
                    "coef": "tradeA_coef",
                    "p_value": "tradeA_p_value",
                    "percent_effect": "tradeA_percent_effect",
                    "matches_expected_sign": "tradeA_matches_expected_sign",
                }
            )
            right = right[[c for c in keep if c in right.columns]].rename(
                columns={
                    "term": "prodA_term",
                    "coef": "prodA_coef",
                    "p_value": "prodA_p_value",
                    "percent_effect": "prodA_percent_effect",
                    "matches_expected_sign": "prodA_matches_expected_sign",
                }
            )
            merged = left.merge(right, on=["group", "model"], how="outer")
            merged["source_file"] = filename
            merged["comparison_term"] = old_term.replace("_cap", "")
            comparisons.append(merged)
    if not comparisons:
        warn("trade-A versus production-A comparison produced no rows")
        return pd.DataFrame()
    return pd.concat(comparisons, ignore_index=True, sort=False)


def add_sign_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    expected = []
    for _, row in out.iterrows():
        model = str(row.get("model", ""))
        term = str(row.get("term", ""))
        sign = ""
        if model.startswith("source") and term != "D" and ("E_china" in term or "P_S" in term or "P_C" in term):
            sign = "negative"
        elif model == "average_source_contrast" and term == "D":
            sign = "negative"
        elif "row" in model and "P_S" in term:
            sign = "positive"
        elif "row" in model and "P_C" in term:
            sign = "zero_or_negative"
        elif "total" in model and "P_C" in term:
            sign = "negative"
        elif "total" in model and "P_S" in term:
            sign = "zero_positive_or_ambiguous"
        elif "K" in term:
            sign = "ambiguous"
        expected.append(sign)
    out["expected_sign"] = expected
    out["matches_expected_sign"] = np.select(
        [
            out["expected_sign"].eq("negative") & out["coef"].lt(0),
            out["expected_sign"].eq("positive") & out["coef"].gt(0),
            out["expected_sign"].eq("zero_or_negative") & out["coef"].le(0),
            out["expected_sign"].eq("zero_positive_or_ambiguous"),
            out["expected_sign"].eq("ambiguous"),
            out["expected_sign"].eq(""),
        ],
        [True, True, True, True, np.nan, np.nan],
        default=False,
    )
    return out


def write_summary(
    outputs: dict[str, pd.DataFrame],
    product_table: pd.DataFrame,
    production_audit: pd.DataFrame,
) -> None:
    lines = []
    lines.append("# Production-A K-Based Pressure Results Summary\n")
    lines.append("## Formulas\n")
    lines.append("- `E_ip = M_C_pre / (M_C_pre + M_R_pre)`, missing if pre-policy total imports are zero.\n")
    lines.append("- `O_cap = min(1, M_R_pre / M_C_pre)` when China pre imports are positive.\n")
    lines.append("- `O_freq = pre-policy months with RoW imports / pre-policy months`.\n")
    lines.append("- `O_bin = 1` when RoW access is frequent and at least 10 percent of China pre imports, with documented zero-China edge handling.\n")
    lines.append("- `A_prod = min(1, RoW production / China production) * (1 - HHI_ROW_prod)`.\n")
    lines.append("- `K = O_cap * A_prod`, `P_S = E * K`, `P_C = E * (1 - K)`, `P_X = E`.\n")
    lines.append("- 2023 USGS production A is the baseline. 2024 production A is a robustness check.\n")
    lines.append("\n## Production Data Audit\n")
    prod_show = production_audit.loc[
        production_audit["year"].isin([2023, 2024]),
        [
            "product_name",
            "hs",
            "usgs_commodity",
            "usgs_type",
            "year",
            "china_production",
            "world_total",
            "A_prod",
            "notes",
        ],
    ].copy()
    lines.append(prod_show.to_markdown(index=False))
    lines.append("\n## Sample\n")
    lines.append(product_table.to_markdown(index=False))
    lines.append("\n\n## Main Quarterly Average Effects\n")
    avg = outputs.get("main_average_ppml_quarterly", pd.DataFrame())
    if not avg.empty:
        show = avg.loc[
            avg["anchor"].eq("first_full_post_quarter")
            & avg["term"].eq("D"),
            ["group", "coef", "p_value", "percent_effect", "n_used", "n_dropped_separation"],
        ]
        lines.append(show.to_markdown(index=False))
    lines.append("\n\n## Capacity Pressure Source-Contrast, Quarterly First Full Post\n")
    pspc = outputs.get("source_contrast_PS_PC_quarterly", pd.DataFrame())
    if not pspc.empty:
        show = pspc.loc[
            pspc["anchor"].eq("first_full_post_quarter")
            & pspc["pressure_variant"].eq("capacity")
            & pspc["term"].isin(["D", "D_P_S_cap_prod", "D_P_C_cap_prod"]),
            ["group", "term", "coef", "p_value", "percent_effect", "expected_sign", "matches_expected_sign", "n_used"],
        ]
        lines.append(show.to_markdown(index=False))
    lines.append("\n\n## Capacity Mechanism Results, Quarterly\n")
    for key in ["mechanism_row_quarterly", "mechanism_total_quarterly"]:
        df = outputs.get(key, pd.DataFrame())
        if df.empty:
            continue
        lines.append(f"\n### {key}\n")
        show = df.loc[
            df["pressure_variant"].eq("capacity"),
            ["group", "model", "term", "coef", "p_value", "expected_sign", "matches_expected_sign", "n_used"],
        ]
        lines.append(show.to_markdown(index=False))
    lines.append("\n\n## Event And Placebo Diagnostics\n")
    event = outputs.get("event_study_average_quarterly", pd.DataFrame())
    if not event.empty:
        show = event.loc[
            event["row_type"].eq("joint_pretrend"),
            ["group", "anchor", "p_value"],
        ]
        lines.append("Average quarterly joint pretrend p-values:\n")
        lines.append(show.to_markdown(index=False))
    placebo = outputs.get("placebo_pressure", pd.DataFrame())
    if not placebo.empty:
        show = placebo.loc[
            placebo["frequency"].eq("quarterly")
            & placebo["term"].isin(["D_placebo_PS_cap_prod", "D_placebo_PC_cap_prod"]),
            ["group", "anchor", "placebo_lag_months", "term", "coef", "p_value"],
        ].head(80)
        lines.append("\nQuarterly pressure placebo excerpt:\n")
        lines.append(show.to_markdown(index=False))
    lines.append("\n\n## Price Wedge Diagnostics\n")
    price = outputs.get("price_wedge_diagnostics", pd.DataFrame())
    if not price.empty:
        cols = [c for c in ["pair_id", "family", "hs", "price_output_source", "coef", "p_value", "percent_change", "avg_E_china", "avg_K_cap_prod", "avg_P_S_cap_prod", "avg_P_C_cap_prod"] if c in price.columns]
        lines.append(price[cols].head(80).to_markdown(index=False))
    comparison = outputs.get("old_tradeA_vs_new_prodA_comparison", pd.DataFrame())
    lines.append("\n\n## Trade-A Versus Production-A Comparison\n")
    if not comparison.empty:
        cols = [c for c in ["source_file", "group", "model", "comparison_term", "tradeA_coef", "tradeA_p_value", "prodA_coef", "prodA_p_value", "tradeA_matches_expected_sign", "prodA_matches_expected_sign"] if c in comparison.columns]
        lines.append(comparison[cols].head(120).to_markdown(index=False))
    else:
        lines.append("No comparison rows were produced.\n")
    lines.append("\n\n## Warnings\n")
    if warnings_log:
        lines.extend([f"- {w}" for w in warnings_log])
    else:
        lines.append("- No warnings logged.")
    lines.append("\n\n## Final Interpretation Checklist Template\n")
    lines.append("For each product/group, answer:\n")
    checklist = [
        "Is average China-source effect negative?",
        "Is D * E negative?",
        "Is D * P_S negative in the source-contrast model?",
        "Is D * P_C negative in the source-contrast model?",
        "Is RoW * P_S positive?",
        "Is total * P_C negative?",
        "Are placebo tests clean?",
        "Are pretrends acceptable?",
        "Does U.S. heterogeneity change interpretation?",
        "Is the product best interpreted as switching, compression, price segmentation, mixed, or weak/null?",
    ]
    for i, item in enumerate(checklist, 1):
        lines.append(f"{i}. {item}\n")
    (RESULTS / "summary_for_review_prod.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme() -> None:
    text = """# Revised Pressure K-Production-A Results

This folder contains the preliminary empirical battery for the revised pressure-index architecture:

`K = O * A`, `P_S = E * K`, `P_C = E * (1 - K)`, and `P_X = E`.

Capacity access is the baseline. Frequency and binary access versions are included as robustness checks. Product availability is based on USGS 2025 world production data, with 2023 as the baseline and 2024 as robustness. All pressure variables use pre-announcement trade data plus pre-policy production availability. The main clean treated products are HS 2504, HS 8110, HS 8106, and HS 284180. Donor products are the current clean donor products in the processed panel.

The files are generated by `04_scripts/run_revised_pressure_k_prod_a.py`. Trade-A pressure outputs are not deleted.
"""
    (RESULTS / "README_results.md").write_text(text, encoding="utf-8")


def mechanism_summary(outputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    sources = [
        ("D_E", outputs.get("china_exposure_interaction_quarterly", pd.DataFrame())),
        ("D_PS_PC", outputs.get("source_contrast_PS_PC_quarterly", pd.DataFrame())),
        ("RoW", outputs.get("mechanism_row_quarterly", pd.DataFrame())),
        ("Total", outputs.get("mechanism_total_quarterly", pd.DataFrame())),
    ]
    wanted_terms = {
        "D_E_china",
        "D_P_S_cap_prod",
        "D_P_C_cap_prod",
        "TP_P_S_cap_prod",
        "TP_P_C_cap_prod",
    }
    for block, df in sources:
        if df.empty:
            continue
        use = df.copy()
        if "anchor" in use.columns:
            use = use.loc[use["anchor"].eq("first_full_post_quarter")].copy()
        if "pressure_variant" in use.columns:
            use = use.loc[use["pressure_variant"].isin(["capacity", "exposure"])].copy()
        use = use.loc[use["term"].isin(wanted_terms)].copy()
        if use.empty:
            continue
        use["summary_block"] = block
        rows.append(use)
    if not rows:
        return pd.DataFrame()
    out = pd.concat(rows, ignore_index=True, sort=False)
    cols = [
        "summary_block",
        "group",
        "frequency",
        "model",
        "term",
        "coef",
        "p_value",
        "percent_effect",
        "expected_sign",
        "matches_expected_sign",
        "n_used",
        "n_dropped_separation",
    ]
    return out[[c for c in cols if c in out.columns]]


def write_2024_robustness(
    production_audit: pd.DataFrame,
    pressure_summary: pd.DataFrame,
    outputs: dict[str, pd.DataFrame],
) -> None:
    RESULTS_2024.mkdir(parents=True, exist_ok=True)
    production_audit.loc[production_audit["year"].eq(2024)].to_csv(
        RESULTS_2024 / "production_A_audit_2024.csv", index=False
    )
    pressure_summary.loc[
        pressure_summary["variable"].isin(
            ["A_prod_2024", "K_cap_prod_2024", "P_S_cap_prod_2024", "P_C_cap_prod_2024"]
        )
    ].to_csv(RESULTS_2024 / "pressure_index_summary_prod_2024.csv", index=False)
    files = [
        ("source_contrast_PS_PC_quarterly", "source_contrast_PS_PC_quarterly_prod_2024.csv"),
        ("mechanism_row_quarterly", "mechanism_row_quarterly_prod_2024.csv"),
        ("mechanism_total_quarterly", "mechanism_total_quarterly_prod_2024.csv"),
    ]
    lines = ["# Production-A 2024 Robustness Summary\n"]
    for key, filename in files:
        df = outputs.get(key, pd.DataFrame())
        if df.empty:
            out = pd.DataFrame()
        else:
            out = df.loc[df.get("pressure_variant", pd.Series(index=df.index)).eq("capacity_2024")].copy()
        out.to_csv(RESULTS_2024 / filename, index=False)
        lines.append(f"\n## {filename}\n")
        if out.empty:
            lines.append("No rows.\n")
        else:
            cols = [c for c in ["group", "term", "coef", "p_value", "percent_effect", "matches_expected_sign", "n_used"] if c in out.columns]
            lines.append(out[cols].head(80).to_markdown(index=False))
    (RESULTS_2024 / "summary_for_review_prod_2024.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def save_output(name: str, df: pd.DataFrame, filename: str) -> pd.DataFrame:
    path = RESULTS / filename
    df.to_csv(path, index=False)
    (RESULTS / "model_failures_and_warnings_prod.txt").write_text(
        "\n".join(warnings_log) + "\n", encoding="utf-8"
    )
    (RESULTS / "us_model_failures_prod.txt").write_text(
        "\n".join([w for w in warnings_log if "us_" in w or "US" in w or "U.S." in w]) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {name}: {len(df)} rows -> {path.name}")
    return df


def load_existing(filename: str) -> pd.DataFrame | None:
    path = RESULTS / filename
    if path.exists() and path.stat().st_size > 0:
        try:
            df = pd.read_csv(path, low_memory=False)
            print(f"Reusing existing {path.name}: {len(df)} rows")
            return df
        except Exception:  # noqa: BLE001
            return None
    return None


def run_stage(
    outputs: dict[str, pd.DataFrame],
    key: str,
    filename: str,
    label: str,
    func,
    reuse_existing: bool = True,
) -> pd.DataFrame:
    if reuse_existing:
        existing = load_existing(filename)
        if existing is not None:
            outputs[key] = existing
            return existing
    print(label)
    df = func()
    outputs[key] = save_output(key, df, filename)
    return df


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    print("Loading panels")
    source_monthly = load_source_panel()
    wide_monthly = load_wide_panel()

    print("Building USGS production availability")
    production_audit, production_country_rows = build_production_availability()
    production_audit.to_csv(RESULTS / "production_A_audit.csv", index=False)
    production_country_rows.to_csv(RESULTS / "production_country_rows_used.csv", index=False)

    print("Building revised production-A pressure indices")
    pressure = build_revised_pressure(source_monthly, production_audit)
    pressure.to_csv(RESULTS / "pressure_indices_prod_importer_product.csv", index=False)

    source_monthly = attach_pressure(source_monthly, pressure)
    wide_monthly = attach_pressure(wide_monthly, pressure)
    source_quarterly = make_quarterly_source(source_monthly)
    wide_quarterly = make_quarterly_wide(wide_monthly)

    summary, by_product, correlations = pressure_summary_tables(pressure)
    summary.to_csv(RESULTS / "pressure_index_summary_prod.csv", index=False)
    by_product.to_csv(RESULTS / "pressure_index_by_product_prod.csv", index=False)
    correlations.to_csv(RESULTS / "pressure_index_correlations_prod.csv", index=False)

    product_table = product_sample_table(PRODUCT_META)
    product_table.to_csv(RESULTS / "product_sample_table.csv", index=False)

    outputs: dict[str, pd.DataFrame] = {}

    run_stage(
        outputs,
        "main_average_ppml_quarterly",
        "main_average_ppml_quarterly_prod.csv",
        "Running quarterly source average models",
        lambda: add_sign_columns(run_source_average(source_quarterly, "quarterly")),
    )
    run_stage(
        outputs,
        "main_average_ppml_monthly",
        "main_average_ppml_monthly_prod.csv",
        "Running monthly source average models",
        lambda: add_sign_columns(run_source_average(source_monthly, "monthly")),
    )
    run_stage(
        outputs,
        "china_exposure_interaction_quarterly",
        "china_exposure_interaction_quarterly_prod.csv",
        "Running quarterly exposure interaction models",
        lambda: add_sign_columns(run_source_exposure(source_quarterly, "quarterly")),
    )
    run_stage(
        outputs,
        "china_exposure_interaction_monthly",
        "china_exposure_interaction_monthly_prod.csv",
        "Running monthly exposure interaction models",
        lambda: add_sign_columns(run_source_exposure(source_monthly, "monthly")),
    )
    run_stage(
        outputs,
        "source_contrast_PS_PC_quarterly",
        "source_contrast_PS_PC_quarterly_prod.csv",
        "Running quarterly P_S/P_C source-contrast models",
        lambda: add_sign_columns(run_source_ps_pc(source_quarterly, "quarterly")),
    )
    run_stage(
        outputs,
        "source_contrast_PS_PC_monthly",
        "source_contrast_PS_PC_monthly_prod.csv",
        "Running monthly P_S/P_C source-contrast models",
        lambda: add_sign_columns(run_source_ps_pc(source_monthly, "monthly")),
    )
    run_stage(
        outputs,
        "source_contrast_E_K_quarterly",
        "source_contrast_E_K_quarterly_prod.csv",
        "Running quarterly E/K diagnostic source-contrast models",
        lambda: add_sign_columns(run_source_e_k(source_quarterly, "quarterly")),
    )
    run_stage(
        outputs,
        "source_contrast_E_K_monthly",
        "source_contrast_E_K_monthly_prod.csv",
        "Running monthly E/K diagnostic source-contrast models",
        lambda: add_sign_columns(run_source_e_k(source_monthly, "monthly")),
    )
    run_stage(
        outputs,
        "mechanism_row_quarterly",
        "mechanism_row_quarterly_prod.csv",
        "Running quarterly RoW mechanism models",
        lambda: add_sign_columns(
            run_mechanism(wide_quarterly, "quarterly", "non_china_primaryValue", "row")
        ),
    )
    run_stage(
        outputs,
        "mechanism_total_quarterly",
        "mechanism_total_quarterly_prod.csv",
        "Running quarterly total-import mechanism models",
        lambda: add_sign_columns(
            run_mechanism(wide_quarterly, "quarterly", "world_primaryValue", "total")
        ),
    )
    run_stage(
        outputs,
        "mechanism_row_monthly",
        "mechanism_row_monthly_prod.csv",
        "Running monthly RoW mechanism models",
        lambda: add_sign_columns(
            run_mechanism(wide_monthly, "monthly", "non_china_primaryValue", "row")
        ),
    )
    run_stage(
        outputs,
        "mechanism_total_monthly",
        "mechanism_total_monthly_prod.csv",
        "Running monthly total-import mechanism models",
        lambda: add_sign_columns(
            run_mechanism(wide_monthly, "monthly", "world_primaryValue", "total")
        ),
    )
    run_stage(
        outputs,
        "event_study_average_quarterly",
        "event_study_average_quarterly_prod.csv",
        "Running quarterly average event studies",
        lambda: run_event_average(source_quarterly, "quarterly"),
    )
    run_stage(
        outputs,
        "event_study_average_monthly",
        "event_study_average_monthly_prod.csv",
        "Running monthly average event studies",
        lambda: run_event_average(source_monthly, "monthly"),
    )
    run_stage(
        outputs,
        "event_study_pressure_quarterly",
        "event_study_pressure_quarterly_prod.csv",
        "Running quarterly pressure-gradient event studies",
        lambda: run_event_pressure(source_quarterly, "quarterly"),
    )
    run_stage(
        outputs,
        "event_study_pressure_monthly",
        "event_study_pressure_monthly_prod.csv",
        "Running monthly pressure-gradient event studies",
        lambda: run_event_pressure(source_monthly, "monthly"),
    )
    run_stage(
        outputs,
        "placebo_average",
        "placebo_average_prod.csv",
        "Running placebo average diagnostics",
        lambda: add_sign_columns(
            pd.concat(
                [
                    run_placebo(source_quarterly, "quarterly", pressure=False),
                    run_placebo(source_monthly, "monthly", pressure=False),
                ],
                ignore_index=True,
                sort=False,
            )
        ),
    )
    run_stage(
        outputs,
        "placebo_exposure",
        "placebo_exposure_prod.csv",
        "Running placebo exposure diagnostics",
        lambda: add_sign_columns(
            pd.concat(
                [
                    run_placebo_exposure(source_quarterly, "quarterly"),
                    run_placebo_exposure(source_monthly, "monthly"),
                ],
                ignore_index=True,
                sort=False,
            )
        ),
    )
    run_stage(
        outputs,
        "placebo_pressure",
        "placebo_pressure_prod.csv",
        "Running placebo pressure diagnostics",
        lambda: add_sign_columns(
            pd.concat(
                [
                    run_placebo(source_quarterly, "quarterly", pressure=True),
                    run_placebo(source_monthly, "monthly", pressure=True),
                ],
                ignore_index=True,
                sort=False,
            )
        ),
    )
    run_stage(
        outputs,
        "us_excluded_quarterly",
        "us_excluded_quarterly_prod.csv",
        "Running U.S.-excluded quarterly robustness",
        lambda: run_us_excluded(source_quarterly, wide_quarterly, "quarterly"),
    )
    run_stage(
        outputs,
        "us_excluded_monthly",
        "us_excluded_monthly_prod.csv",
        "Running U.S.-excluded monthly robustness",
        lambda: run_us_excluded(source_monthly, wide_monthly, "monthly"),
    )
    run_stage(
        outputs,
        "us_interactions",
        "us_interactions_prod.csv",
        "Running U.S. heterogeneity",
        lambda: add_sign_columns(
            pd.concat(
                [
                    run_us_interactions(source_quarterly, "quarterly"),
                    run_us_interactions(source_monthly, "monthly"),
                ],
                ignore_index=True,
                sort=False,
            )
        ),
    )
    run_stage(
        outputs,
        "net_weight_robustness",
        "net_weight_robustness_prod.csv",
        "Running net-weight robustness",
        lambda: add_sign_columns(
            pd.concat(
                [
                    run_net_weight(source_quarterly, "quarterly"),
                    run_net_weight(source_monthly, "monthly"),
                ],
                ignore_index=True,
                sort=False,
            )
        ),
    )
    run_stage(
        outputs,
        "price_wedge_diagnostics",
        "price_wedge_diagnostics_prod.csv",
        "Running price wedge diagnostics",
        lambda: run_price_wedges(pressure),
        reuse_existing=False,
    )
    run_stage(
        outputs,
        "mechanism_summary",
        "mechanism_summary_prod.csv",
        "Building mechanism summary",
        lambda: mechanism_summary(outputs),
        reuse_existing=False,
    )
    run_stage(
        outputs,
        "old_tradeA_vs_new_prodA_comparison",
        "old_tradeA_vs_new_prodA_comparison.csv",
        "Building trade-A versus production-A pressure comparison",
        lambda: old_trade_prod_comparison(outputs),
        reuse_existing=False,
    )
    if standardization_audit_rows:
        pd.DataFrame(standardization_audit_rows).drop_duplicates().to_csv(
            RESULTS / "pressure_standardization_audit.csv", index=False
        )
    else:
        pd.DataFrame(
            columns=["variable", "group", "mean_used", "sd_used", "n_cells_used", "standardization_scope"]
        ).to_csv(RESULTS / "pressure_standardization_audit.csv", index=False)
    write_readme()
    write_summary(outputs, product_table, production_audit)
    write_2024_robustness(production_audit, summary, outputs)
    print(f"Done. Results written to {RESULTS}")


if __name__ == "__main__":
    main()
