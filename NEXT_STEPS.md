# Next Steps

This file is the current execution order after the proposal-defense feedback.
The active plan is no longer the term-paper HS 282580 workflow. The active
plan is the quarterly pressure-mechanism thesis design.

Canonical notes:

- `01_notes/Post-Defense Thesis Plan.md`: current source of truth.
- `01_notes/Theoretical Framework Lock.md`: pressure framework and hypotheses.
- `01_notes/Empirical Strategy Lock.md`: estimator hierarchy and inference
  language.
- `01_notes/Thesis Design.md`: broader thesis architecture.
- `01_notes/Data.md`: data inventory and coverage.

## 1. Current Thesis Direction

Research question:

> When do Chinese critical-mineral export licensing controls bind in
> international trade, and do affected importers adjust through substitution
> toward non-China suppliers, compression of total imports, or price
> segmentation?

Main design:

1. build pre-policy pressure variables;
2. estimate quarterly source-contrast PPML;
3. test switching and compression pressure interactions;
4. estimate China, RoW, and total import mechanism models;
5. use price wedges as mechanism diagnostics;
6. use monthly timing and legacy term-paper models only as supporting
   robustness or provenance.

## 2. Active Data Pipeline

Run from the repository root:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
```

Main processed outputs:

- `03_data/processed/product_scope_metadata.csv`
- `03_data/processed/comtrade_pressure_country_product_month.csv`
- `03_data/processed/comtrade_pressure_source_panel.csv`
- `03_data/processed/comtrade_pressure_partner_panel.csv`
- `03_data/processed/pressure_indices_importer_product.csv`
- `03_data/processed/pressure_indices_product_summary.csv`
- `03_data/processed/pressure_ppml_estimation_panel.csv`

Strict clean estimation sample:

- 53 reporters;
- 16 products;
- 87 months;
- two source groups, China and RoW;
- four clean treated products;
- 12 donor candidates.

Clean treated baseline products:

- HS 2504 natural graphite;
- HS 8110 antimony metal;
- HS 8106 bismuth;
- HS 284180 tungstates/APT.

Secondary products:

- HS 261710 antimony ores and concentrates, sparse;
- HS 282580 antimony oxides, partial;
- HS 282560 GeO2/ZrO2, bundled;
- HS 811292 Ga/Ge bundle, bundled;
- HS 3801 artificial and colloidal graphite, graphite-scope case;
- HS 8101 tungsten metal/articles, partial.

## 3. Active Estimation Pipeline

Run the current preliminary results package:

```bash
python 04_scripts/diagnose_pressure_indices.py
python 04_scripts/diagnose_anchor_quarter_models.py
python 04_scripts/estimate_quarterly_pressure_mechanisms.py
python 04_scripts/estimate_price_wedges.py
```

Current source-contrast and robustness scripts:

```bash
python 04_scripts/estimate_pressure_ppml_by_wave.py
python 04_scripts/estimate_pressure_ppml_by_product.py
python 04_scripts/estimate_pressure_timing_robustness.py
```

Important output tables:

- `03_data/output/tables/quarterly_first_full_post_pressure_ppml.csv`
- `03_data/output/tables/anchor_quarter_average_ppml.csv`
- `03_data/output/tables/anchor_quarter_event_pretrend.csv`
- `03_data/output/tables/quarterly_event_pretrend_coefficients_check.csv`
- `03_data/output/tables/quarterly_pressure_mechanisms_first_full_post.csv`
- `03_data/output/tables/price_wedge_pair_its_results.csv`
- `03_data/output/tables/price_wedge_panel_did_results.csv`
- `03_data/output/tables/pressure_us_interaction_results.csv`
- `03_data/output/tables/pressure_placebo_date_results.csv`
- `03_data/output/tables/pressure_net_weight_ppml_results.csv`

## 4. Current Result Reading

Preliminary result hierarchy:

1. **Switching pressure is the clearest mechanism.**
2. **Antimony and bismuth have strong price-wedge support.**
3. **Compression is plausible but not yet clean in trade quantities.**
4. **Tungstates/APT is weak under current trade and price evidence.**
5. **Antimony metal has a strong average effect but timing/placebo concerns.**

Do not write that all licensing controls mechanically reduce trade. Do not
claim license denials, approval probabilities, inventories, welfare effects,
or coercive political success.

## 5. Immediate Work

1. Wait for the external critique of the current result package.
2. Decide whether absorptive pressure becomes the baseline or remains one of
   three variants.
3. Add high/low or tercile pressure-bin robustness.
4. Re-run placebo-date tests in the quarterly first-full-post framework.
5. Verify price benchmarks for graphite, antimony oxides, and tungsten/APT.
6. Decide how to treat antimony metal given the strong average effect but
   placebo-date warning.
7. Update the proposal only after the model hierarchy is frozen.

## 6. Legacy Reproducibility

The old term-paper pipeline remains reproducible:

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

Use it only for provenance and archived preliminary evidence. It is not the
current thesis empirical backbone.
