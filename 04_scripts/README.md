# Scripts

This folder contains data acquisition, processing, diagnostics, and estimation
scripts. The active thesis-stage workflow is the post-defense pressure-design
pipeline. `analysis_thesis.py` is retained for archived term-paper
reproducibility.

## Active Pressure-Design Pipeline

Run from the repository root:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
```

Outputs:

- `03_data/processed/product_scope_metadata.csv`
- `03_data/processed/comtrade_pressure_country_product_month.csv`
- `03_data/processed/comtrade_pressure_source_panel.csv`
- `03_data/processed/comtrade_pressure_partner_panel.csv`
- `03_data/processed/pressure_indices_importer_product.csv`
- `03_data/processed/pressure_indices_product_summary.csv`
- `03_data/processed/pressure_ppml_estimation_panel.csv`

## Active Estimation And Diagnostics

- `diagnose_pressure_indices.py`: pressure-index descriptive tables and
  figures.
- `diagnose_anchor_quarter_models.py`: monthly versus quarterly timing
  diagnostics, average PPML, and event-pretrend checks under announcement,
  implementation, and import-effect anchors.
- `estimate_quarterly_pressure_mechanisms.py`: quarterly China, RoW, and
  total import mechanism PPML models using first full post-quarter timing.
- `estimate_price_wedges.py`: product-level and panel price-wedge diagnostics.

Important current outputs:

- `03_data/output/tables/quarterly_first_full_post_pressure_ppml.csv`
- `03_data/output/tables/anchor_quarter_average_ppml.csv`
- `03_data/output/tables/anchor_quarter_event_pretrend.csv`
- `03_data/output/tables/quarterly_event_pretrend_coefficients_check.csv`
- `03_data/output/tables/quarterly_pressure_mechanisms_first_full_post.csv`
- `03_data/output/tables/price_wedge_pair_its_results.csv`
- `03_data/output/tables/price_wedge_panel_did_results.csv`

## Supporting And Robustness Scripts

- `estimate_pressure_ppml.py`: preliminary source-contrast PPML pressure
  models for the frequency, capacity, and absorptive pressure variants.
- `estimate_pressure_ppml_by_wave.py`: monthly wave-specific clean-sample PPML
  models for Wave 2, Wave 3, and Wave 4.
- `estimate_pressure_ppml_by_product.py`: monthly product-specific PPML models.
- `estimate_pressure_ppml_by_wave_exclude_us.py`: U.S.-exclusion robustness.
- `estimate_pressure_ppml_staggered.py`: pooled clean-staggered PPML summary.
  Do not use it as the main result.
- `estimate_pressure_timing_robustness.py`: monthly event studies, placebo
  dates, U.S. interactions, and net-weight robustness.
- `diagnose_pretrend_alternatives.py`: exploratory local-window and binned
  pretrend diagnostics.

## Data Acquisition And Preparation

- `download_all_gaps.py`: current Comtrade gap downloader.
- `download_china_exports.py`: China aggregate export audit for treated
  candidates.
- `download_eurostat_cn8.py`: raw Eurostat CN8 acquisition.
- `prepare_eurostat_cn8.py`: canonical Eurostat cleaning and validation.
- `prepare_geodist.py`: China-to-reporter CEPII GeoDist covariates.
- `prepare_international_prices.py`: imports manually exported Bloomberg price
  histories.
- `prepare_wind_prices_controls.py`: prepares Wind control price exports.

`download_missing.py` is retained for historical reference. Use
`download_all_gaps.py` for current Comtrade work.

## Archived Term-Paper Reproducibility

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

This reproduces the older term-paper-style HS 282580 and source-share outputs.
It is useful for provenance and archived preliminary evidence. It is not the
current thesis backbone.

`analysis_final.py` remains legacy and must not be used for new thesis claims.
