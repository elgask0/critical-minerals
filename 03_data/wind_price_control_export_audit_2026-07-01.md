# Wind Price and Control Export Audit, 2026-07-01

## Files Parsed

- `03_data/raw/wind_exports_2026-07-01/wind_export_gallium_rotterdam_multi_series.csv`
- `03_data/raw/wind_exports_2026-07-01/wind_export_indium_rotterdam_controls_multi_series.csv`
- `03_data/raw/wind_exports_2026-07-01/wind_export_ev_steel_lead_semiconductors_controls.csv`
- `03_data/raw/wind_exports_2026-07-01/wind_export_minerals_data_2026-06-09.xlsx`
- `03_data/raw/wind_exports_2026-07-01/bloomberg_export_mineral_prices_2026-07-01.xlsx`

## Clean Outputs

- `03_data/processed/wind_prices_controls_monthly_2019_2026m03.csv`
- `03_data/interim/wind_prices_controls_long_2026-07-01.csv`
- `03_data/output/tables/wind_series_inventory_2026-07-01.csv`
- `03_data/output/tables/wind_product_coverage_audit_2026-07-01.csv`
- `03_data/output/tables/price_wedge_candidate_coverage_2026-07-01.csv`

## Summary

- Raw series columns parsed: 98.
- Unique Wind series IDs: 80.
- Duplicate raw series columns: 32. These are deduplicated in the clean panel.
- Monthly panel shape: 87 months x 79 data columns.
- Daily and weekly prices are averaged to monthly means; monthly series keep their monthly observations.
- The panel is trimmed to January 2019 through March 2026.

## Important Caveats

- The later CSV-exported China V2O5 flake series is blank, but the older Wind workbook supplies usable China V2O5 from 2020-10 onward.
- Bloomberg graphite tickers are present, but the workbook did not preserve descriptions, grades, locations, or units.
- The exports contain no rare-earth price series; rare-earth price-wedge analysis should be dropped unless new data are found.
- Tellurium is treated as complete under the current assumption that `TEEUUQPU Index` is the intended international tellurium benchmark; archive the DES tomorrow.
- Tungsten is treated as complete/usable under the current assumption that `TGEUWOQR Index` is the intended international tungsten benchmark; archive the DES tomorrow.
- Remaining treated/partial-treated price download: international antimony oxide.
- International molybdenum is useful only as a candidate-control/proxy benchmark, not as a treated-product wedge.
- The new controls file adds BEV sales/output, crude steel, lead-acid battery output, and China semiconductor sales value.

## Blank Or Superseded Raw Export Columns

- `wind_export_gallium_rotterdam_multi_series.csv`: `S9976462` / `v_china_v2o5_98_flake_cny_ton`: China: Market Price: Vanadium Pentoxide (98%, Flake Vanadium)
- `wind_export_ev_steel_lead_semiconductors_controls.csv`: `S5603672` / `demand_china_semiconductor_chip_output_10k_units`: China: Output: Semiconductor Chip

## Price-Wedge Candidate Coverage

| Candidate | Status | International months | Domestic months | Notes |
|---|---|---:|---:|---|
| Gallium | complete | 86 | 87 | Use Rotterdam gallium against China domestic/industrial gallium. |
| Germanium metal | complete | 85 | 87 | Use Rotterdam metal germanium against China 50 ohm/cm series. |
| Indium | within_bundle_control_complete | 86 | 87 | Indium metal is complete as a within-bundle comparison/proxy; the 2025 indium controls cover indium phosphide and organo-indium compounds, not ordinary indium metal. |
| Antimony metal | complete | 85 | 87 | Use Rotterdam 99.65% antimony against China ingot/non-ferrous benchmarks. |
| Bismuth | complete | 86 | 87 | Use Rotterdam bismuth against China refined/average bismuth. |
| GeO2 | usable_partial | 82 | 87 | International GeO2 is present but ends before 2026-03 in this export; domestic is complete. |
| Vanadium | complete_from_2020m10_with_full_proxy | 87 | 87 | Exact China V2O5 is now present from 2020-10; V nitrogen/ferrovanadium give full-window proxies. |
| Tungsten | complete_assumed | 87 | 87 | Treat `TGEUWOQR Index` as the intended international tungsten benchmark under the current assumption; archive DES tomorrow. |
| Molybdenum | candidate_control_proxy_optional | 7 | 87 | China molybdenum coverage is strong; only annual FCX international proxy is present. A monthly molybdenum oxide or ferro-moly benchmark is useful only as a candidate-control/proxy series, not as a treated-product wedge. |
| Antimony oxides | download_required | 0 | 86 | China antimony oxide is present; need Rotterdam/Europe/CIF antimony trioxide. |
| Tellurium | complete_assumed | 87 | 87 | Treat `TEEUUQPU Index` as the intended international tellurium benchmark under the current assumption; archive DES tomorrow. |
| Graphite | present_needs_bloomberg_description | 87 | 87 | Bloomberg graphite tickers are present but descriptions were not exported; verify grade/location before using. |

## Product Coverage

| HS | Product | Coverage now | Remaining gap |
|---|---|---|---|
| 2504 | Graphite | China natural flake graphite is present through 2026-03. Bloomberg graphite tickers are present, but their descriptions/grades were not preserved in the workbook. | Verify Bloomberg graphite ticker descriptions; then choose the natural flake 94-95% / -100 mesh series as primary. |
| 811292 | Ga/Ge/In/V bundle | Gallium, germanium metal, indium, and vanadium prices are present with China and international series. Global and China semiconductor controls are present. | No niobium price. |
| 282560 | GeO2/ZrO2 | GeO2 has Rotterdam and China series. | No zirconium dioxide/sponge price. |
| 8110 | Antimony metal | Rotterdam antimony, several China antimony metal series, and lead-acid battery demand are present. | Good enough for Sb metal wedge. |
| 261710 | Antimony ores/concentrates | China antimony concentrate 50% is present. | No international concentrate benchmark. |
| 282580 | Antimony oxides | China antimony oxide in CNY and USD is present. | No Rotterdam/Europe antimony trioxide benchmark. |
| 8106 | Bismuth | Rotterdam bismuth, China refined bismuth, average bismuth, and bismuth oxide are present. | Bismuth oxide international benchmark still missing. |
| 284180 | Tungstates/APT | Tungsten China series and international `TGEUWOQR Index` are present; treat tungsten as usable under the current assumption. | Archive `TGEUWOQR Index` description tomorrow, but no new tungsten download is required unless the description contradicts the assumption. |
| 8101 | Tungsten articles | Tungsten rod, powder, carbide powder, average tungsten, Rotterdam ferro-tungsten, and `TGEUWOQR Index` are present. | No new tungsten download required under the current assumption. |
| 280450 | Tellurium/boron | China tellurium series and international `TEEUUQPU Index` are present; treat tellurium as usable under the current assumption. | Archive `TEEUUQPU Index` description tomorrow; boron contamination proxy absent. |
| 284170 | Molybdates | China molybdenum concentrate/oxide/metal/powder series and annual FCX selling price are present. | Candidate-control/proxy family; no monthly Rotterdam/Asia molybdenum oxide benchmark. |
| 282570 | Molybdenum oxides | China molybdenum oxide and high-purity MoO3 series are present. | Candidate-control/proxy family; no monthly international molybdenum oxide benchmark. |
| 284690 | Non-cerium rare-earth compounds | No rare-earth series in these files. | Drop rare-earth price-wedge analysis unless new data are found. |
| 284610 | Cerium compounds | No cerium series in these files. | No price wedge. |
| 2818 | Alumina | No alumina series in these files. | Missing. |
| 8111 | Manganese articles | No manganese series in these files. | Missing. |
| 2811 | Inorganic acids | Chemical PPI controls are present, but no acid price. | Acid-specific price missing. |
| 2615 | Nb/Ta/V/Zr ores | Vanadium and molybdenum proxies are present. | Niobium, tantalum, and zirconium ore proxies missing. |
| 811221 | Chromium | No chromium/ferrochrome series in these files. | Missing. |
| 380130 | Carbon electrode pastes | No electrode paste, needle coke, or synthetic graphite series in these files. | Missing. |
| 282530 | Vanadium oxides | Rotterdam V2O5, China V2O5 flake, China V nitrogen/ferrovanadium, and China crude steel demand are present. | China V2O5 starts in 2020-10, so use ferrovanadium/V nitrogen for a full-window robustness proxy. |
| 282520 | Lithium oxide/hydroxide | Power-battery and BEV demand controls are present. | Lithium hydroxide/carbonate prices missing. |
| 8103 | Tantalum | No tantalum series in these files. | Missing. |
| 8108 | Titanium | No titanium series in these files. | Missing. |
| 8109 | Zirconium | No zirconium series in these files. | Missing. |
| 8104 | Magnesium | No magnesium series in these files. | Missing. |
| 8105 | Cobalt | Power-battery and BEV demand controls are present. | Cobalt price series missing in these files. |
| 282110 | Iron oxide pigments | No iron oxide pigment series in these files. | Missing. |
| 2820 | Manganese oxides | No manganese oxide/EMD series in these files. | Missing. |
| 2833 | Sulfates | Broad chemical PPI controls are present. | Sulfate-specific prices missing. |
