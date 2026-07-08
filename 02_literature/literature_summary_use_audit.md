# Literature Summary Use Audit

Updated: 2026-06-27 after integrating the extra thesis papers.

Purpose: proposal-use audit of the 57 local source summaries. This file does not
replace `literature_master.md`; it identifies which summaries can support
proposal drafting and which should stay contextual, optional, or deferred.

## Coverage

| Item | Status |
|---|---|
| Zotero top-level project items | 57 |
| Local source folders | 57 |
| Paper summary files | 57 |
| Source folders aligned with summary names | Yes |
| Missing summaries | None |
| Local `references.bib` entries | 57, aligned |

The summaries are source-control notes. They are suitable for planning the
literature review, but direct quotations and page-specific claims still require
close reading of the parsed source or PDF.

## Proposal-Ready Core Streams

| Stream | Core sources | Safe proposal use |
|---|---|---|
| Economic statecraft | `farrell2019weaponized`, `egger2024sanctions`, with `farrell2023underground_empire` optional | Motivate network/chokepoint power and connect export restrictions to economic coercion without claiming mineral controls automatically succeed. |
| Technology-control context | `bown2020semiconductor`, `bown2024semiconductors`, BIS 2022/2024 controls | Situate mineral licensing in the broader U.S.-China technology-control environment. |
| Chinese export-control institutions | `prc_2020_export_control_law`, `scio_2021_chinas_export_controls`, `prc2024_dual_use_regulations` | Establish legal and official institutional background. Use PRC 2024 only generally until full capture is available. |
| Core policy episodes and licensing mechanics | MOFCOM 2023 Ga/Ge, 2023 graphite, 2024 antimony controls, license guides, approval statements, FAQ, and review statements | Code announcement dates, implementation dates, product scope, and licensing procedure. Do not infer approval rates or non-binding effects. |
| Critical-mineral market structure | USGS 2026 mineral summaries, IEA 2025, Frenzel 2017, Park 2025, van den Brink 2022, Xu 2025 | Describe concentration, byproduct constraints, and product differences. Not causal evidence. |
| Licensing and administrative trade costs | `unctad2019ntm_classification`, `gamberale_tarasenko2023_export_licensing`, `djankov_freund_pham2010_trading_on_time`, `hummels_schaur2013_time_trade_barrier`, `handley_limao2017_policy_uncertainty` | Support the claim that licensing can bind through authorization, delay, documentation, discretion, and uncertainty. |
| Adjustment and outside options | `handley_kamal_monarch2024_supply_chain_adjustments`, with product sources above | Support heterogeneity by supplier concentration, switching options, and relationship adjustment margins. |
| Trade-flow and panel methods | `santossilva2006gravity`, `fally2015_structural_gravity_fe`, `olden_moen2022_triple_difference`, `callaway2021difference`, `sun2021eventstudies`, `borusyak_jaravel_spiess2024_event_studies`, `dechaisemartin2020twfe`, `roth2022pretest`, `rambachan2023honest` | Justify PPML/gravity, DDD logic, staggered/event-study caution, and pretrend sensitivity. Use sparingly in proposal prose. |
| Few-shock inference | `conley_taber2011_small_policy_changes`, `ferman_pinto2019_few_treated`, `mackinnon_webb2018_few_treated_clusters` | Explain why many country-product-month observations do not equal many independent policy shocks. |
| Price wedges and volatility | `martin_anderson2012_price_insulation`, `brander_bernauer_huss2023_trade_policy_volatility`, `worldbank2026_commodity_markets_outlook` | Support domestic-international price-gap interpretation and announcement-volatility caveats. Not mineral-specific causal proof. |

## Contextual Or Deferred Sources

| Source group | Use decision |
|---|---|
| `mofcom_2024_us_controls_critical_minerals`, `mofcom_2025_suspend_us_controls_art2`, `mofcom_2025_suspend_55_58_61_62` | Use for chronology and to avoid false coding; not baseline treatment evidence. |
| `mofcom_2025_w_te_bi_mo_in_controls`, `mofcom_2025_medium_heavy_rare_earth_controls` | Thesis expansion candidates; keep out of the proposal baseline unless data coverage changes. |
| `worldbank2026_commodity_markets_outlook` | Optional benchmark context; exact Bloomberg/Wind methodology remains outside the current source set. |
| `farrell2023underground_empire` | Optional book context; the 2019 article is the core theory citation. |

## Citation Hygiene

- Use only clean project citation keys in LaTeX and notes.
- Re-export `references.bib` from Zotero before final citation insertion.
- Do not cite the deep-research report itself.
- Do not quote from summaries. Quote only from checked source text with page or paragraph verification.
- Treat official documents as primary evidence on policy design and timing, not as literature.
