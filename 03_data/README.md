Data workflow root: raw, interim, processed, and output. Do not edit raw data in place.

## Contents

- `raw/`: Original Comtrade CSVs, Bloomberg/Wind prices, CEPII GeoDist.
- `interim/`: Intermediate extraction and cleaning outputs.
- `processed/`: Cleaned analysis-ready data.
- `output/`: Generated figures and tables.

Authoritative coverage: `01_notes/Data.md`.
Operational acquisition list: `03_data/DOWNLOAD_CHECKLIST.md`.

Active thesis-stage processed data:

- `processed/comtrade_pressure_country_product_month.csv`;
- `processed/comtrade_pressure_source_panel.csv`;
- `processed/comtrade_pressure_partner_panel.csv`;
- `processed/pressure_indices_importer_product.csv`;
- `processed/pressure_ppml_estimation_panel.csv`.

The older `comtrade_thesis_*` panels are retained for archived term-paper
reproducibility.
