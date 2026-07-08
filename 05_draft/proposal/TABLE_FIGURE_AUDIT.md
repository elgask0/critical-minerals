# Table And Figure Audit

## Current Main Proposal Tables And Figures

| Item | Label | File or location | Source for values |
|---|---|---|---|
| Figure 3-1 Research Design and Interpretation Route | `fig:pressure-framework` | Inline TikZ in `main.tex` | Author's design, based on the current proposal logic and inspired by the older grouped route figure. |
| Table 3-1 Main Outcomes and Pressure Variables | `tab:variables_outcomes` | `tables/variables_outcomes.tex` | Proposal variable definitions and framework equations. |
| Table 3-2 Clean Treated Products and Policy Timing | `tab:product-scope` | `tables/product_scope.tex` | Official policy chronology and author sample construction. |
| Table 3-3 USGS Production Availability Measures | `tab:production-availability` | `tables/production_availability.tex` | `production_A_audit.csv`; USGS `Mineral Commodity Summaries 2025`. |
| Table 3-4 China Source Response | `tab:china-source-response` | `tables/preliminary_results.tex` | Verified row by row below. |
| Table 3-5 Adjustment Mechanisms | `tab:adjustment-mechanisms` | `tables/adjustment_mechanisms.tex` | Verified row by row below. |
| Table 3-6 Price Diagnostics | `tab:price-diagnostics` | `tables/price_diagnostics.tex` | Verified row by row below. |
| Table 5-1 Thesis Completion Timeline | `tab:timeline` | `tables/timeline.tex` | Thesis completion plan and proposal constraints. |

## Result Verification Method

All reported result rows use the preferred quarterly production-based \(A\) specifications unless otherwise noted. Standard errors are present in the source CSV files. Displayed \(t\) statistics were verified as `coef / se`; for average China source effects, the displayed point estimate is the source `percent_effect`, while the displayed \(t\) statistic is still computed from the underlying PPML coefficient and standard error. Stars were verified from source `p_value` using * \(p<0.10\), ** \(p<0.05\), and *** \(p<0.01\).

The tables were reverified in the `main(12)` final pre-submission polish pass. Tables 3-4 and 3-5 use PPML standard errors clustered by `reporterCode`, as recorded in the result CSV `cluster` column. Table 3-6 uses the source `pair_its_hac3` price diagnostic standard errors and is not reporter-clustered. No displayed coefficient, percent effect, \(t\) statistic, \(p\)-value star, or product classification changed.

## Table 3-4 Verification

| Row | Product | Source file | Row identifier | Source effect or coef | Source se | Verified \(t\) | Source \(p\) | Display |
|---|---|---|---|---:|---:|---:|---:|---|
| Average China source effect | Natural graphite | `main_average_ppml_quarterly_prod.csv` | `group=hs2504_graphite`, `anchor=first_full_post_quarter`, `term=D` | -30.129521 | 0.202125 | -1.773788 | 0.076098 | -30.1* (-1.77) |
| Average China source effect | Antimony metal | `main_average_ppml_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `anchor=first_full_post_quarter`, `term=D` | -86.701621 | 0.351115 | -5.746059 | 9.13e-09 | -86.7*** (-5.75) |
| Average China source effect | Bismuth metal | `main_average_ppml_quarterly_prod.csv` | `group=hs8106_bismuth`, `anchor=first_full_post_quarter`, `term=D` | -74.358698 | 0.376867 | -3.611266 | 0.000305 | -74.4*** (-3.61) |
| Average China source effect | Tungstates/APT | `main_average_ppml_quarterly_prod.csv` | `group=hs284180_tungstates`, `anchor=first_full_post_quarter`, `term=D` | -15.213228 | 0.404044 | -0.408447 | 0.682945 | -15.2 (-0.41) |
| China exposure | Natural graphite | `china_exposure_interaction_quarterly_prod.csv` | `group=hs2504_graphite`, `anchor=first_full_post_quarter`, `term=D_E_china` | -0.364235 | 0.089698 | -4.060694 | 4.89e-05 | -0.364*** (-4.06) |
| China exposure | Antimony metal | `china_exposure_interaction_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `anchor=first_full_post_quarter`, `term=D_E_china` | -0.179414 | 0.381384 | -0.470428 | 0.638049 | -0.179 (-0.47) |
| China exposure | Bismuth metal | `china_exposure_interaction_quarterly_prod.csv` | `group=hs8106_bismuth`, `anchor=first_full_post_quarter`, `term=D_E_china` | -0.583795 | 0.377455 | -1.546660 | 0.121945 | -0.584 (-1.55) |
| China exposure | Tungstates/APT | `china_exposure_interaction_quarterly_prod.csv` | `group=hs284180_tungstates`, `anchor=first_full_post_quarter`, `term=D_E_china` | -0.363409 | 0.134184 | -2.708292 | 0.006763 | -0.363*** (-2.71) |
| Switching pressure | Natural graphite | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs2504_graphite`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_S_cap_prod` | 0.190536 | 0.183447 | 1.038643 | 0.298971 | 0.191 (1.04) |
| Switching pressure | Antimony metal | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_S_cap_prod` | -0.077919 | 0.337343 | -0.230979 | 0.817331 | -0.078 (-0.23) |
| Switching pressure | Bismuth metal | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs8106_bismuth`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_S_cap_prod` | -0.195057 | 0.441861 | -0.441445 | 0.658891 | -0.195 (-0.44) |
| Switching pressure | Tungstates/APT | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs284180_tungstates`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_S_cap_prod` | 0.156358 | 0.133087 | 1.174855 | 0.240053 | 0.156 (1.17) |
| Compression pressure | Natural graphite | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs2504_graphite`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_C_cap_prod` | -0.217871 | 0.107726 | -2.022459 | 0.043129 | -0.218** (-2.02) |
| Compression pressure | Antimony metal | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_C_cap_prod` | -0.127546 | 0.159855 | -0.797888 | 0.424936 | -0.128 (-0.80) |
| Compression pressure | Bismuth metal | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs8106_bismuth`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_C_cap_prod` | -0.593104 | 0.300614 | -1.972978 | 0.048498 | -0.593** (-1.97) |
| Compression pressure | Tungstates/APT | `source_contrast_PS_PC_quarterly_prod.csv` | `group=hs284180_tungstates`, `anchor=first_full_post_quarter`, `pressure_variant=capacity`, `term=D_P_C_cap_prod` | -0.183211 | 0.221627 | -0.826664 | 0.408428 | -0.183 (-0.83) |

## Table 3-5 Verification

| Row | Product | Source file | Row identifier | Source coef | Source se | Verified \(t\) | Source \(p\) | Display |
|---|---|---|---|---:|---:|---:|---:|---|
| Rest of world switching | Natural graphite | `mechanism_row_quarterly_prod.csv` | `group=hs2504_graphite`, `model=row_switch_only`, `anchor=first_full_post_quarter`, `term=TP_P_S_cap_prod` | 0.341606 | 0.131739 | 2.593065 | 0.009512 | 0.342*** (2.59) |
| Rest of world switching | Antimony metal | `mechanism_row_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `model=row_switch_only`, `anchor=first_full_post_quarter`, `term=TP_P_S_cap_prod` | 0.405396 | 0.118399 | 3.423992 | 0.000617 | 0.405*** (3.42) |
| Rest of world switching | Bismuth metal | `mechanism_row_quarterly_prod.csv` | `group=hs8106_bismuth`, `model=row_switch_only`, `anchor=first_full_post_quarter`, `term=TP_P_S_cap_prod` | 0.195626 | 0.141689 | 1.380674 | 0.167379 | 0.196 (1.38) |
| Rest of world switching | Tungstates/APT | `mechanism_row_quarterly_prod.csv` | `group=hs284180_tungstates`, `model=row_switch_only`, `anchor=first_full_post_quarter`, `term=TP_P_S_cap_prod` | 0.160911 | 0.151742 | 1.060430 | 0.288949 | 0.161 (1.06) |
| Total import compression | Natural graphite | `mechanism_total_quarterly_prod.csv` | `group=hs2504_graphite`, `model=total_compress_only`, `anchor=first_full_post_quarter`, `term=TP_P_C_cap_prod` | -0.165150 | 0.081197 | -2.033945 | 0.041957 | -0.165** (-2.03) |
| Total import compression | Antimony metal | `mechanism_total_quarterly_prod.csv` | `group=hs8110_antimony_metal`, `model=total_compress_only`, `anchor=first_full_post_quarter`, `term=TP_P_C_cap_prod` | 0.286744 | 0.207568 | 1.381445 | 0.167142 | 0.287 (1.38) |
| Total import compression | Bismuth metal | `mechanism_total_quarterly_prod.csv` | `group=hs8106_bismuth`, `model=total_compress_only`, `anchor=first_full_post_quarter`, `term=TP_P_C_cap_prod` | -0.133663 | 0.202579 | -0.659806 | 0.509378 | -0.134 (-0.66) |
| Total import compression | Tungstates/APT | `mechanism_total_quarterly_prod.csv` | `group=hs284180_tungstates`, `model=total_compress_only`, `anchor=first_full_post_quarter`, `term=TP_P_C_cap_prod` | 0.441032 | 0.121538 | 3.628769 | 0.000285 | 0.441*** (3.63) |

## Table 3-6 Verification

| Row | Product | Source file | Row identifier | Source coef | Source se | Verified \(t\) | Source \(p\) | Display |
|---|---|---|---|---:|---:|---:|---:|---|
| Price wedge | Natural graphite | `price_wedge_diagnostics_prod.csv` | `pair_id=graphite_gpcnlclw`, `model=pair_its_hac3`, `term=post` | -0.067085 | 0.036514 | -1.837243 | 0.066174 | -0.067* (-1.84) |
| Price wedge | Antimony metal | `price_wedge_diagnostics_prod.csv` | `pair_id=antimony_metal`, `model=pair_its_hac3`, `term=post` | 0.459592 | 0.118373 | 3.882564 | 0.000103 | 0.460*** (3.88) |
| Price wedge | Bismuth metal | `price_wedge_diagnostics_prod.csv` | `pair_id=bismuth_metal`, `model=pair_its_hac3`, `term=post` | 0.837060 | 0.124559 | 6.720185 | 1.81e-11 | 0.837*** (6.72) |
| Price wedge | Tungstates/APT | `price_wedge_diagnostics_prod.csv` | `pair_id=tungsten_tgeuwoqr`, `model=pair_its_hac3`, `term=post` | -0.114911 | 0.054336 | -2.114836 | 0.034444 | -0.115** (-2.11) |

## Removed Or Omitted

| Removed or omitted item | Status | Reason |
|---|---|---|
| Old HS 282580 event study figure | Removed from active proposal and deleted from proposal figure assets. | Old feasibility evidence is not part of the current clean treated product sample. |
| Old 10 product feasibility table | Removed. | The current proposal uses four clean treated products and 12 donor candidates. |
| Combined product mechanism table | Replaced. | Tables 3-4, 3-5, and 3-6 now separate China source response, adjustment mechanisms, and price diagnostics. |
| Coefficient plot figure | Removed and deleted from active figure assets. | The coefficients are now reported in regression table form. |
| New empirical event study figure | Omitted. | No final clean event study figure is visually and diagnostically defensible as main proposal evidence. Event study estimates remain timing diagnostics only. |

## Verification Notes

- Table 3-4 is product specific and does not include a pooled row.
- Pooled estimates are described only as summary evidence because pooled pretrends fail.
- Table cells use coefficients or percent effects with t statistics in parentheses.
- No p values in square brackets remain in Tables 3-4 through 3-6.
- No sign commentary appears inside coefficient cells.
- Tungstates/APT remain weak, null, or unresolved.
- Price wedges remain diagnostic and are not presented as causal proof.
