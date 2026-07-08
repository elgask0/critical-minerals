# Data Dictionary

## Comtrade

| Dataset | Variable | Definition | Unit |
|---|---|---|---|
| `comtrade_{hs}_imports.csv` | `reporterCode` | UN M49 numeric reporter | Code |
| | `partnerCode` | UN M49 numeric partner; China = 156 | Code |
| | `period` | Monthly period, YYYYMM | Month |
| | `primaryValue` | Reported trade value | USD |
| | `netWgt` | Net weight where reported | kg |
| `comtrade_{hs}_china_exports.csv` | `period` | Monthly China export period | Month |
| | `primaryValue` | China exports to world | USD |
| `comtrade_{hs}_china_exports_coverage.csv` | `api_record_returned` | Whether the annual API audit returned a row for the month | Boolean |

### Canonical thesis panels

| Dataset | Key variables | Definition |
|---|---|---|
| `processed/comtrade_thesis_country_product_month.csv` | `reporterCode`, `hs`, `period` | Balanced 53-country x 10-product x 87-month panel |
| | `world_value_usd` | Canonical World-partner import total | USD |
| | `china_value_usd` | Canonical China-partner imports | USD |
| | `non_china_value_usd` | World less China, bounded at zero | USD |
| | `china_share_value` | China value divided by World value | Ratio |
| | `supplier_count` | Number of positive bilateral suppliers | Count |
| | `supplier_hhi` | Sum of squared bilateral value shares | 0-1 |
| `processed/comtrade_thesis_source_panel.csv` | `reporterCode`, `hs`, `period`, `source` | Two-row source panel: China and RestOfWorld, 92,220 rows |
| | `trade_value_usd` | Source-specific import value used by PPML | USD |

Canonical raw records require `partner2Code=0`, `customsCode=C00`, `motCode=0`,
and `mosCode=0`. World, bilateral, partner-two, customs, and transport records
must not be summed together.

## Eurostat CN8

| Dataset | Key variables | Definition |
|---|---|---|
| `interim/eurostat_cn8_eu27_balanced_long.csv` | reporter, CN8, partner, period | Balanced 27-country long panel; omitted API cells filled with zero and flagged |
| `processed/eurostat_cn8_eu27_country_month.csv` | `china_imports_eur`, `world_imports_eur`, `non_china_imports_eur`, `china_share` | Analysis-ready country-product-month panel |
| `processed/eurostat_cn8_eu27_monthly.csv` | same flow variables | EU27 sums calculated from country rows, excluding UK and API aggregate artifacts |

## Prices

| Column | Definition | Unit | Coverage |
|---|---|---|---:|
| `Ga_9999_price` | Domestic gallium >=99.99% | CNY/kg | 72 |
| `Ge_ingot_avg` | Domestic germanium ingot average | CNY/kg | 72 |
| `graphite_flake_avg` | Domestic natural flake graphite | CNY/ton | 72 |
| `In_rotterdam_usd` | Rotterdam indium 99.99% | USD/kg | 71 |
| `In_refined_avg` | Domestic refined indium >=99.995% | CNY/kg | 72 |
| `V_nitrogen_10k_cny_ton` | Domestic vanadium nitrogen Vn16 | CNY 10,000/ton | 71 |
| `V_nitrogen_cny_ton` | Converted vanadium nitrogen Vn16 | CNY/ton | 71 |
| `V_pentoxide` | Domestic vanadium pentoxide 98% flake | CNY/ton | 51 |

## GeoDist

`raw/geodist/dist_cepii.dta` is the canonical static dyadic file. Relevant
variables include `iso_o`, `iso_d`, `distw`, `contig`, `comlang_off`,
`comlang_ethno`, `colony`, `comcol`, and `curcol`.

`processed/geodist_china_reporters.csv` maps all 56 configured Comtrade
reporters to China-origin GeoDist covariates and flags the EU and ASEAN
aggregates as non-country observations.

## Thesis Result Tables

| Dataset | Definition |
|---|---|
| `output/tables/thesis_exporter_its_results.csv` | China-export interrupted time series with HAC(6) uncertainty |
| `output/tables/thesis_ppml_results.csv` | Static Comtrade and Eurostat PPML estimates |
| `output/tables/thesis_event_study_results.csv` | Dynamic PPML coefficients |
| `output/tables/thesis_event_pretrend_tests.csv` | Conditional joint pretrend tests |
| `output/tables/thesis_scm_sdid_diagnostics.csv` | Appendix-only SCM and Synthetic DiD diagnostics |
