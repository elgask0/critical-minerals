#!/usr/bin/env python3
"""
Diagnose pretrend failures for the pressure-panel source-share PPML design.

This is an exploratory diagnostic script. It does not replace the canonical
analysis scripts. It checks whether event-study pretrend failures are driven by:
- the event anchor month;
- anticipation months between announcement and import-effect timing;
- using all months instead of a local event window;
- U.S. reporter behavior;
- switch-only pressure interactions.
"""

from __future__ import annotations

from pathlib import Path
import sys

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
PANEL_PATH = PROCESSED / "pressure_ppml_estimation_panel.csv"

CONTROL_ROLE = "candidate_control_pending_screen"
US_REPORTER_CODE = 842

FE = [
    "fe_importer_month",
    "fe_product_month",
    "fe_source_month",
    "fe_importer_product_source",
]

GROUPS = {
    "wave2_graphite": {
        "family": "wave",
        "label": "Wave 2 graphite",
        "treated_hs": ["2504"],
        "announcement_month": "202310",
        "implementation_month": "202312",
        "import_effect_month": "202401",
    },
    "wave3_antimony_clean": {
        "family": "wave",
        "label": "Wave 3 antimony metal",
        "treated_hs": ["8110"],
        "announcement_month": "202408",
        "implementation_month": "202409",
        "import_effect_month": "202410",
    },
    "wave4_w_bi": {
        "family": "wave",
        "label": "Wave 4 W/Bi",
        "treated_hs": ["8106", "284180"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
    "hs2504_graphite": {
        "family": "product",
        "label": "HS 2504 graphite",
        "treated_hs": ["2504"],
        "announcement_month": "202310",
        "implementation_month": "202312",
        "import_effect_month": "202401",
    },
    "hs8110_antimony_metal": {
        "family": "product",
        "label": "HS 8110 antimony metal",
        "treated_hs": ["8110"],
        "announcement_month": "202408",
        "implementation_month": "202409",
        "import_effect_month": "202410",
    },
    "hs8106_bismuth": {
        "family": "product",
        "label": "HS 8106 bismuth",
        "treated_hs": ["8106"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
    "hs284180_tungstates": {
        "family": "product",
        "label": "HS 284180 tungstates",
        "treated_hs": ["284180"],
        "announcement_month": "202502",
        "implementation_month": "202502",
        "import_effect_month": "202503",
    },
}

ANCHOR_FIELDS = {
    "announcement": "announcement_month",
    "implementation": "implementation_month",
    "import_effect": "import_effect_month",
}

SWITCH_VARIANTS = {
    "frequency": "p_switch_frequency_z_main_clean_for_interaction",
    "capacity": "p_switch_capacity_z_main_clean_for_interaction",
    "absorptive": "p_switch_absorptive_z_main_clean_for_interaction",
}


def month_index(period: str) -> int:
    return int(period[:4]) * 12 + int(period[4:6])


def add_month_index(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["month_index"] = out["period"].str[:4].astype(int) * 12 + out[
        "period"
    ].str[4:6].astype(int)
    return out


def p_value(beta: float, se: float) -> float:
    if not np.isfinite(beta) or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * norm.sf(abs(beta / se)))


def percent_effect(beta: float) -> float:
    if not np.isfinite(beta):
        return np.nan
    return float(100 * (np.exp(beta) - 1))


def fit_fepois(data: pd.DataFrame, outcome: str, x_cols: list[str]):
    work = data[[outcome, "reporterCode", "hs", *x_cols, *FE]].dropna().copy()
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(FE)}"
    model = pf.fepois(
        formula,
        work,
        vcov={"CRV1": "reporter_cluster"},
        separation_check=["fe"],
        iwls_maxiter=80,
        iwls_tol=1e-7,
        fixef_tol=1e-7,
        fixef_maxiter=100000,
        demeaner_backend="numba",
        lean=False,
    )
    coef = model.coef().reindex(x_cols)
    vcov = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se = pd.Series(np.sqrt(np.diag(vcov)), index=coef.index)
    return model, coef, se, vcov, formula, len(work)


def fit_feols(data: pd.DataFrame, outcome: str, x_cols: list[str]):
    work = data[[outcome, "reporterCode", "hs", *x_cols, *FE]].dropna().copy()
    work["reporter_cluster"] = work["reporterCode"].astype(str)
    formula = f"{outcome} ~ {' + '.join(x_cols)} | {' + '.join(FE)}"
    model = pf.feols(
        formula,
        work,
        vcov={"CRV1": "reporter_cluster"},
        lean=False,
    )
    coef = model.coef().reindex(x_cols)
    vcov = pd.DataFrame(model._vcov, index=coef.index, columns=coef.index)
    se = pd.Series(np.sqrt(np.diag(vcov)), index=coef.index)
    return model, coef, se, vcov, formula, len(work)


def group_sample(panel: pd.DataFrame, group_key: str, exclude_us: bool = False) -> pd.DataFrame:
    info = GROUPS[group_key]
    treated_hs = set(info["treated_hs"])
    sample = panel.loc[
        panel["analysis_role"].eq(CONTROL_ROLE) | panel["hs"].isin(treated_hs)
    ].copy()
    if exclude_us:
        sample = sample.loc[~sample["reporterCode"].eq(US_REPORTER_CODE)].copy()
    sample["treated_group"] = sample["hs"].isin(treated_hs)
    sample["post_import_effect"] = sample["period"].ge(info["import_effect_month"])
    sample["D_group"] = (
        sample["treated_group"] & sample["china_source"] & sample["post_import_effect"]
    ).astype(int)
    return sample


def event_design(
    sample: pd.DataFrame,
    group_key: str,
    anchor: str,
    window: int,
    base: int = -1,
) -> tuple[pd.DataFrame, list[str], dict[str, int], list[str], list[str]]:
    info = GROUPS[group_key]
    anchor_month = info[ANCHOR_FIELDS[anchor]]
    anchor_idx = month_index(anchor_month)
    out = sample.copy()
    out["event_time"] = out["month_index"] - anchor_idx
    out = out.loc[out["event_time"].between(-window, window)].copy()

    x_cols = []
    term_to_k = {}
    for k in range(-window, window + 1):
        if k == base:
            continue
        name = f"event_m{abs(k)}" if k < 0 else f"event_p{k}"
        out[name] = (
            out["treated_group"] & out["china_source"] & out["event_time"].eq(k)
        ).astype(int)
        x_cols.append(name)
        term_to_k[name] = k

    all_pre_terms = [term for term, k in term_to_k.items() if k < 0]

    ann_k = month_index(info["announcement_month"]) - anchor_idx
    clean_pre_terms = [term for term, k in term_to_k.items() if k < ann_k]
    return out, x_cols, term_to_k, all_pre_terms, clean_pre_terms


def joint_test(coef: pd.Series, vcov: pd.DataFrame, terms: list[str]) -> tuple[float, int, float]:
    terms = [term for term in terms if term in coef.index and np.isfinite(coef.loc[term])]
    if not terms:
        return np.nan, 0, np.nan
    b = coef.reindex(terms).astype(float).to_numpy()
    v = vcov.reindex(index=terms, columns=terms).astype(float).to_numpy()
    stat = float(b.T @ np.linalg.pinv(v) @ b)
    df = len(terms)
    return stat, df, float(chi2.sf(stat, df))


def run_event_diagnostics(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    event_rows = []
    specs = []
    for anchor in ["import_effect", "announcement", "implementation"]:
        specs.append((anchor, 12, False, "value_ppml"))
    for window in [9, 6]:
        specs.append(("import_effect", window, False, "value_ppml"))
    specs.append(("import_effect", 12, True, "value_ppml"))
    specs.append(("import_effect", 12, False, "log1p_feols"))

    for group_key, info in GROUPS.items():
        for anchor, window, exclude_us, estimator in specs:
            sample = group_sample(panel, group_key, exclude_us=exclude_us)
            event_sample, x_cols, term_to_k, all_pre, clean_pre = event_design(
                sample, group_key, anchor, window
            )
            if event_sample.empty:
                continue
            if estimator == "log1p_feols":
                event_sample["log_trade_value_usd"] = np.log1p(event_sample["trade_value_usd"])
                outcome = "log_trade_value_usd"
                fit = fit_feols
            else:
                outcome = "trade_value_usd"
                fit = fit_fepois
            print(
                f"Event diagnostic {group_key} anchor={anchor} window={window} "
                f"exclude_us={exclude_us} estimator={estimator}",
                flush=True,
            )
            try:
                model, coef, se, vcov, formula, input_rows = fit(event_sample, outcome, x_cols)
            except Exception as exc:
                rows.append(
                    {
                        "group_key": group_key,
                        "group_label": info["label"],
                        "anchor": anchor,
                        "window": window,
                        "exclude_us": exclude_us,
                        "estimator": estimator,
                        "status": f"failed: {type(exc).__name__}: {exc}",
                    }
                )
                continue

            all_stat, all_df, all_p = joint_test(coef, vcov, all_pre)
            clean_stat, clean_df, clean_p = joint_test(coef, vcov, clean_pre)
            pre_df = pd.DataFrame(
                {
                    "term": x_cols,
                    "event_time": [term_to_k[t] for t in x_cols],
                    "coef": coef.reindex(x_cols).to_numpy(),
                    "se_reporter": se.reindex(x_cols).to_numpy(),
                }
            )
            pre_df["p_reporter"] = [
                p_value(b, s) for b, s in zip(pre_df["coef"], pre_df["se_reporter"])
            ]
            max_abs_clean = (
                pre_df.loc[pre_df["term"].isin(clean_pre), "coef"].abs().max()
                if clean_pre
                else np.nan
            )
            min_p_clean = (
                pre_df.loc[pre_df["term"].isin(clean_pre), "p_reporter"].min()
                if clean_pre
                else np.nan
            )
            max_abs_all = (
                pre_df.loc[pre_df["term"].isin(all_pre), "coef"].abs().max()
                if all_pre
                else np.nan
            )
            min_p_all = (
                pre_df.loc[pre_df["term"].isin(all_pre), "p_reporter"].min()
                if all_pre
                else np.nan
            )
            rows.append(
                {
                    "group_key": group_key,
                    "group_label": info["label"],
                    "anchor": anchor,
                    "window": window,
                    "exclude_us": exclude_us,
                    "estimator": estimator,
                    "status": "ok",
                    "all_pre_chi2": all_stat,
                    "all_pre_df": all_df,
                    "all_pre_p": all_p,
                    "clean_pre_chi2": clean_stat,
                    "clean_pre_df": clean_df,
                    "clean_pre_p": clean_p,
                    "max_abs_all_pre_coef": max_abs_all,
                    "min_all_pre_p": min_p_all,
                    "max_abs_clean_pre_coef": max_abs_clean,
                    "min_clean_pre_p": min_p_clean,
                    "nobs": int(getattr(model, "_N", np.nan)),
                    "input_rows": input_rows,
                    "dropped_separation": input_rows - int(getattr(model, "_N", input_rows)),
                }
            )
            for term in x_cols:
                event_rows.append(
                    {
                        "group_key": group_key,
                        "group_label": info["label"],
                        "anchor": anchor,
                        "window": window,
                        "exclude_us": exclude_us,
                        "estimator": estimator,
                        "event_time": term_to_k[term],
                        "term": term,
                        "coef": float(coef.loc[term]),
                        "se_reporter": float(se.loc[term]),
                        "p_reporter": p_value(float(coef.loc[term]), float(se.loc[term])),
                    }
                )
    return pd.DataFrame(rows), pd.DataFrame(event_rows)


def run_switch_only(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    event_rows = []
    for group_key, info in GROUPS.items():
        sample = group_sample(panel, group_key)
        for variant, pressure_col in SWITCH_VARIANTS.items():
            work = sample.copy()
            work["D_switch"] = work["D_group"] * work[pressure_col]
            print(f"Switch-only PPML {group_key} {variant}", flush=True)
            try:
                model, coef, se, vcov, formula, input_rows = fit_fepois(
                    work, "trade_value_usd", ["D_group", "D_switch"]
                )
                for term in ["D_group", "D_switch"]:
                    beta = float(coef.loc[term])
                    stderr = float(se.loc[term])
                    rows.append(
                        {
                            "group_key": group_key,
                            "group_label": info["label"],
                            "variant": variant,
                            "term": term,
                            "coef": beta,
                            "se_reporter": stderr,
                            "p_reporter": p_value(beta, stderr),
                            "percent_effect": percent_effect(beta),
                            "nobs": int(model._N),
                            "input_rows": input_rows,
                            "dropped_separation": input_rows - int(model._N),
                        }
                    )
            except Exception as exc:
                rows.append(
                    {
                        "group_key": group_key,
                        "group_label": info["label"],
                        "variant": variant,
                        "term": "failed",
                        "coef": np.nan,
                        "se_reporter": np.nan,
                        "p_reporter": np.nan,
                        "percent_effect": np.nan,
                        "nobs": np.nan,
                        "input_rows": len(work),
                        "dropped_separation": np.nan,
                        "error": str(exc),
                    }
                )

            # Event-study version for switch heterogeneity. It tests whether the
            # switch-pressure interaction already appears before announcement.
            event_sample, x_cols, term_to_k, _, clean_pre = event_design(
                sample, group_key, "import_effect", 12
            )
            for term in x_cols:
                event_sample[f"{term}_switch"] = event_sample[term] * event_sample[pressure_col]
            switch_terms = [f"{term}_switch" for term in x_cols]
            x_all = x_cols + switch_terms
            print(f"Switch-event PPML {group_key} {variant}", flush=True)
            try:
                model, coef, se, vcov, formula, input_rows = fit_fepois(
                    event_sample, "trade_value_usd", x_all
                )
                clean_switch_terms = [f"{term}_switch" for term in clean_pre]
                stat, df, p = joint_test(coef, vcov, clean_switch_terms)
                event_rows.append(
                    {
                        "group_key": group_key,
                        "group_label": info["label"],
                        "variant": variant,
                        "clean_pre_switch_chi2": stat,
                        "clean_pre_switch_df": df,
                        "clean_pre_switch_p": p,
                        "nobs": int(model._N),
                        "input_rows": input_rows,
                        "dropped_separation": input_rows - int(model._N),
                    }
                )
            except Exception as exc:
                event_rows.append(
                    {
                        "group_key": group_key,
                        "group_label": info["label"],
                        "variant": variant,
                        "clean_pre_switch_chi2": np.nan,
                        "clean_pre_switch_df": np.nan,
                        "clean_pre_switch_p": np.nan,
                        "nobs": np.nan,
                        "input_rows": len(event_sample),
                        "dropped_separation": np.nan,
                        "error": str(exc),
                    }
                )
    return pd.DataFrame(rows), pd.DataFrame(event_rows)


def run_product_descriptives(panel: pd.DataFrame) -> pd.DataFrame:
    treated = ["2504", "8110", "8106", "284180"]
    rows = []
    for hs in treated:
        sub = panel.loc[panel["hs"].eq(hs)].copy()
        info_row = sub.iloc[0]
        ann = str(info_row["announcement_date"])[:7].replace("-", "")
        effect = str(info_row["import_effect_month"]).replace("-", "")
        pre = sub.loc[sub["period"].lt(effect)]
        post = sub.loc[sub["period"].ge(effect)]
        china_pre = pre.loc[pre["china_source"], "trade_value_usd"].sum()
        row_pre = pre.loc[~pre["china_source"], "trade_value_usd"].sum()
        china_post = post.loc[post["china_source"], "trade_value_usd"].sum()
        row_post = post.loc[~post["china_source"], "trade_value_usd"].sum()
        importer_product = sub.drop_duplicates(["reporterCode", "hs"])
        rows.append(
            {
                "hs": hs,
                "product": str(info_row["product"]),
                "announcement_month": ann,
                "import_effect_month": effect,
                "pre_china_share": china_pre / (china_pre + row_pre) if china_pre + row_pre else np.nan,
                "post_china_share": china_post / (china_post + row_post) if china_post + row_post else np.nan,
                "mean_e_china_exposure": importer_product["e_china_exposure"].mean(),
                "median_e_china_exposure": importer_product["e_china_exposure"].median(),
                "mean_o_frequency": importer_product["o_row_frequency"].mean(),
                "mean_o_capacity": importer_product["o_row_capacity"].mean(),
                "mean_p_switch_capacity": importer_product["p_switch_capacity"].mean(),
                "mean_p_compress_capacity": importer_product["p_compress_capacity"].mean(),
                "positive_china_pre_months": int(
                    pre.loc[pre["china_source"]]
                    .groupby("period")["trade_value_usd"]
                    .sum()
                    .gt(0)
                    .sum()
                ),
                "pre_months": int(pre["period"].nunique()),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PANEL_PATH, dtype={"hs": str, "period": str}, low_memory=False)
    panel = add_month_index(panel)

    pretrend, events = run_event_diagnostics(panel)
    switch_only, switch_event = run_switch_only(panel)
    descriptives = run_product_descriptives(panel)

    pretrend.to_csv(TABLES / "pretrend_alternative_diagnostics.csv", index=False)
    events.to_csv(TABLES / "pretrend_alternative_event_coefficients.csv", index=False)
    switch_only.to_csv(TABLES / "switch_only_pressure_results.csv", index=False)
    switch_event.to_csv(TABLES / "switch_event_pretrend_diagnostics.csv", index=False)
    descriptives.to_csv(TABLES / "treated_product_timing_descriptives.csv", index=False)

    print("\nPretrend alternatives:")
    print(pretrend.to_string(index=False))
    print("\nSwitch-only pressure:")
    print(switch_only.to_string(index=False))
    print("\nSwitch-event pretrend:")
    print(switch_event.to_string(index=False))
    print("\nProduct descriptives:")
    print(descriptives.to_string(index=False))


if __name__ == "__main__":
    main()
