# Proposal Pre-Writing Control

Status: active control note for drafting the revised master thesis proposal.
Updated: 2026-07-01.

This note locks the argument map, citation insertion map, source-use limits,
section boundaries, and proposal depth before full prose writing begins. It is
not proposal prose and should not be copied directly into `main.tex`.

## 1. Locked Argument Map

### Title

When Do Critical-Mineral Export Controls Bind? China's Licensing-Based Controls
and Heterogeneous Trade Responses

### Main Research Question

When do Chinese critical-mineral export licensing controls bind, and through
which adjustment margins?

### Subquestions

1. Do importer-product pairs with higher predicted China-source decline
   pressure show larger post-policy China-source declines?
2. Does switching pressure predict China-source decline, rest-of-world import
   growth, and stable or rising total imports?
3. Does compression pressure predict China-source decline, weak rest-of-world
   replacement, total import decline, and wider international-China price
   wedges where matched prices exist?

### Core Claim

The thesis should argue that a licensing control is not automatically binding
because the legal form of the measure is only one part of the shock. A control
binds when pre-policy importer exposure and non-China supplier structure
predict a post-policy market response. The response can appear as source
switching, import compression, or international-China price segmentation.

### Hypothesis Structure

| Hypothesis | Core prediction | Empirical home |
|---|---|---|
| H1 China-source pressure | Higher predicted pressure implies larger post-policy China-source decline | Source-share PPML with pressure interactions |
| H2 Switching channel | Switching pressure predicts China down, RoW up, and total imports stable or rising | China, RoW, and total import margin models |
| H3 Compression and price channel | Compression pressure predicts China down, weak RoW replacement, total imports down, and wider price wedges where matched prices exist | Margin models and international-China price-wedge model |
| H4 Timing | Effects appear after implementation plus importer-arrival lag, not as systematic pre-policy declines | Binned PPML event studies |
| H5 Measurement discipline | Clean, regular HS codes support stronger claims than bundled, partial, sparse, or price-unmatched products | Product-level estimates, scope audit, regularity diagnostics, CN8 evidence where useful |

### Claim Discipline

- "Binding" means an observed market restriction or adjustment pattern, not a
  blanket export ban, not a license-denial rate, and not proven coercive
  success.
- Current results are proof of feasibility. They should not be presented as
  final thesis findings.
- Mechanism language should be "consistent with" unless the pressure-index
  models, margin models, timing evidence, and price evidence align clearly.
- The old \(A_{ip}=E_{ip}\times O_{ip}\) split is preliminary evidence only.
  The revised framework uses \(P^S_{ip}\), \(P^C_{ip}\), and \(P^X_{ip}\).
- The final theoretical framework is locked in
  `01_notes/Theoretical Framework Lock.md`.
- The minimum empirical strategy is locked in
  `01_notes/Empirical Strategy Lock.md`; do not add extra estimators to the
  proposal unless they are needed for a specific argument.

## 2. Section Boundary Rules

| Proposal section | Job in the proposal | Should include | Should not include |
|---|---|---|---|
| 1. Research Background and Significance | Motivate the research problem and explain why it matters | Critical-mineral supply chains, economic statecraft, China's licensing episodes, main question, why the question matters | Literature catalogue, full methods, detailed result interpretation |
| 2. Literature Review | Synthesize the research streams and identify the gap | Economic statecraft, Chinese export licensing, mineral supply chains and adjustment, empirical trade methods, gap | Full equations, variable table, proof-of-feasibility results, long policy chronology |
| 3. Research Content and Design | Show feasibility and research design | Research questions, conceptual framework, hypotheses, variables, data sources, empirical models, preliminary feasibility evidence, thesis structure | Literature synthesis beyond what is needed to justify the design |
| 4. Contributions and Innovations | State what is new and useful | Academic contribution and policy contribution | Separate "data contribution" section unless it is folded into academic contribution |
| 5. Research Plan and Timeline | Show that the project can be completed | Current status, remaining data work, analysis sequence, writing and defense schedule | First-person project diary, script names, internal file names, excessive operational detail |

### Literature Review Boundary

The literature review should be a synthesis, not a source list. Each subsection
should answer one question:

1. Why are critical-mineral export controls an economic-statecraft problem?
2. What is specific about China's licensing regime?
3. Why should mineral supply chains and importer adjustment differ by product?
4. Which trade-flow, price, and inference literatures justify the empirical
   plan?
5. What remains missing in the literature, and what does this thesis add?

## 3. Citation Insertion Map

### Section 1: Research Background and Significance

| Claim type | Use these sources | Notes |
|---|---|---|
| Global networks can create coercive chokepoints | `farrell2019weaponized`; optionally `egger2024sanctions` | Use as motivation only. Do not imply the thesis tests geopolitical coercion directly. |
| Critical minerals are a plausible domain for supply-side statecraft | `oecd2026_crm_export_restrictions`, `iea_2025_global_critical_minerals_outlook`, USGS product sources | Use concentration and policy context. Do not use as causal evidence. |
| China has a legal and administrative export-control architecture | `prc_2020_export_control_law`, `scio_2021_chinas_export_controls`, `prc2024_dual_use_regulations` | Use for institutional setting. |
| Main treatment chronology | `mofcom_2023_gallium_germanium_controls`, `mofcom_2023_graphite_controls`, `mofcom_2024_antimony_controls` | Use for announcement, implementation, product scope, and licensing requirement. |

### Section 2.1: Economic Statecraft and Critical-Mineral Controls

Core citations: `farrell2019weaponized`,
`oecd2026_crm_export_restrictions`,
`bogdanova_wang2023_china_export_restrictions_wto`, `egger2024sanctions`.

Optional background only: `bown2020semiconductor`, `bown2024semiconductors`.
Use semiconductor-control papers only to show that export controls are part of
current technology competition. Keep them secondary.

### Section 2.2: China's Export-Licensing Regime

Core citations: `prc_2020_export_control_law`,
`scio_2021_chinas_export_controls`, `prc2024_dual_use_regulations`,
`mofcom_2023_gallium_germanium_controls`,
`mofcom_2023_graphite_controls`, `mofcom_2024_antimony_controls`,
`unctad2019ntm_classification`,
`gamberale_tarasenko2023_export_licensing`,
`djankov_freund_pham2010_trading_on_time`,
`hummels_schaur2013_time_trade_barrier`,
`handley_limao2017_policy_uncertainty`.

Important correction: do not rely on
`mofcom_2023_gallium_germanium_license_guide` or
`mofcom_2023_graphite_license_guide` unless those guide PDFs are recaptured.
The current local `source.pdf` files are failed-download placeholders. The
control announcements themselves support the licensing requirement and the
application-material logic.

Use `mofcom_2023_gallium_germanium_approvals`,
`mofcom_2024_graphite_approvals`, and
`mofcom_2024_antimony_license_review` only to show that the measures operated
as licensing regimes rather than automatic blanket bans. Do not infer approval
rates, denial rates, processing times, or non-binding effects from them.

### Section 2.3: Mineral Supply Chains and Importer Adjustment

Core citations: `usgs_2026_gallium`, `usgs_2026_germanium`,
`usgs_2026_graphite_natural`, `usgs_2026_antimony`,
`iea_2025_global_critical_minerals_outlook`,
`frenzel2017byproduct_metals`,
`handley_kamal_monarch2024_supply_chain_adjustments`.

Product-specific supporting citations: `park2025graphite_supply_chain`,
`vandenbrink2022antimony_resilience`, `xu2025antimony_material_flow`.

Use these sources to explain product heterogeneity and importer adjustment
margins. Do not claim they estimate the effect of China's 2023-2024 licensing
controls.

### Section 2.4: Trade Effects, Price Responses, and Empirical Methods

Core trade-method citations: `santossilva2006gravity`,
`fally2015_structural_gravity_fe`, `olden_moen2022_triple_difference`,
`callaway2021difference`, `sun2021eventstudies`,
`borusyak_jaravel_spiess2024_event_studies`, `dechaisemartin2020twfe`.

Core inference citations: `conley_taber2011_small_policy_changes`,
`ferman_pinto2019_few_treated`,
`mackinnon_webb2018_few_treated_clusters`, `roth2022pretest`,
`rambachan2023honest`.

Core price citations: `martin_anderson2012_price_insulation`,
`brander_bernauer_huss2023_trade_policy_volatility`.

Optional commodity benchmark: `worldbank2026_commodity_markets_outlook`.
Use it only if the price-data section needs a general commodity-market
benchmark.

### Section 2.5: Research Gap and Thesis Contribution

Use few citations here. The gap should be stated as a synthesis from the prior
subsections:

- existing work explains economic statecraft and export restrictions in general;
- official and legal sources document China's licensing controls;
- supply-chain studies explain why minerals differ;
- empirical trade methods provide tools for estimation;
- but the literature does not yet explain when formally similar Chinese
  licensing-based mineral controls bind differently across products, timing,
  margins, and prices.

### Section 3: Research Content and Design

Use methods citations only where they justify the proposed empirical design:

- PPML and fixed effects: `santossilva2006gravity`,
  `fally2015_structural_gravity_fe`.
- Triple difference: `olden_moen2022_triple_difference`.
- Staggered timing and event studies: `callaway2021difference`,
  `sun2021eventstudies`,
  `borusyak_jaravel_spiess2024_event_studies`, `dechaisemartin2020twfe`.
- Conservative inference: `conley_taber2011_small_policy_changes`,
  `ferman_pinto2019_few_treated`,
  `mackinnon_webb2018_few_treated_clusters`, `roth2022pretest`,
  `rambachan2023honest`.

Data-provider references for UN Comtrade, CEPII, Bloomberg, and Wind should be
handled in source notes or bibliography only when the final data section is
fixed. They are not part of the literature review.

## 4. Close-Read Support Claims

| Source | Proposal claim supported | Anchor | Boundary |
|---|---|---|---|
| `farrell2019weaponized` | Network centrality can create state power through chokepoints and informational advantages | PDF pp. 2, 4-5 | Conceptual motivation only; not a mineral or China-specific estimate |
| `oecd2026_crm_export_restrictions` | Critical-raw-material export restrictions have increased and licensing remains a common instrument | PDF pp. 6, 8 | Context and typology only; not causal evidence |
| `bogdanova_wang2023_china_export_restrictions_wto` | China's export restrictions have a legal and historical background in WTO disputes and unilateral economic measures | Summary and parsed source | Legal/historical synthesis only |
| `prc_2020_export_control_law` | China has a unified export-control system, temporary controls, licensing for controlled items, and customs license checks | Parsed text lines 100, 156, 175-178, 279 | Legal architecture; cite article-specific claims only after checking text |
| `scio_2021_chinas_export_controls` | Official English framing of China's export-control architecture | Local parsed web source | Institutional framing, not treatment effect evidence |
| `prc2024_dual_use_regulations` | Dual-use controls use license types, review procedures, end-user/end-use documents, and customs release conditions | Parsed text lines 137-150, 181-189, 242-243, 262 | Use only claims visible in local parsed text |
| `mofcom_2023_gallium_germanium_controls` | Ga/Ge controls required licenses and took effect on 2023-08-01 | Parsed text lines 18, 64, 84, 90, 98 | Treatment timing and scope only |
| `mofcom_2023_graphite_controls` | Graphite controls required licenses, optimized prior controls, and took effect on 2023-12-01 | Parsed text lines 21, 39, 67, 75, 85 | Treatment timing and scope only; detailed 2006 predecessor scope needs manual check |
| `mofcom_2024_antimony_controls` | Antimony-related controls required licenses and took effect on 2024-09-15 | Parsed text lines 19, 81, 109, 117, 127 | Treatment timing and scope only |
| `mofcom_2024_graphite_approvals` | MOFCOM publicly stated graphite control was not an export prohibition and that qualified exporters had been approved | Parsed text lines 48-50 | Shows licensing design; do not infer approval rates or non-binding effects |
| `mofcom_2024_antimony_license_review` | MOFCOM stated antimony applications had been received and were under review, with licenses to be granted if requirements were met | Parsed press-conference Reuters question paragraph | Shows licensing design; do not infer approval rates or timing |
| `unctad2019ntm_classification` | Non-tariff measures are measures other than ordinary customs tariffs that can affect quantities or prices; export measures include quotas and prohibitions | PDF pp. 6, 10, 92-93 | Classification only |
| `gamberale_tarasenko2023_export_licensing` | Export licensing is an administrative procedure requiring government authorization and documents before exportation | PDF pp. 6-7, 19 | Legal/institutional source, not causal evidence |
| `djankov_freund_pham2010_trading_on_time` | Administrative delays before shipment reduce trade and can be interpreted as trade costs | PDF pp. 1-2 | General delay evidence, not export licensing specifically |
| `hummels_schaur2013_time_trade_barrier` | Time in transit has a measurable ad valorem trade-cost equivalent | PDF p. 1 | General time-cost evidence |
| `handley_limao2017_policy_uncertainty` | Policy uncertainty affects trade, prices, entry, and welfare through firm investment decisions | PDF p. 1 | General uncertainty channel, not mineral licensing |
| `usgs_2026_gallium` | Gallium is largely byproduct supply and China dominates primary low-purity production | PDF pp. 1-2 | Descriptive product facts only |
| `usgs_2026_germanium` | Germanium trade and supply are tied to zinc concentrates, recycling, and import reliance | PDF pp. 1-2 | Descriptive product facts only |
| `usgs_2026_graphite_natural` | Natural graphite has battery and industrial uses, high import reliance, and China is the leading supplier | PDF pp. 1-2 | Descriptive product facts only |
| `usgs_2026_antimony` | Antimony has flame-retardant, metal, and defense-relevant uses with high import reliance and China exposure in key forms | PDF pp. 1-2 | Descriptive product facts only |
| `iea_2025_global_critical_minerals_outlook` | Critical-mineral outlook tracks demand, supply, concentration, refining, and diversification | Parsed text lines 321, 375 | General market context; not product-level causal evidence |
| `frenzel2017byproduct_metals` | Gallium, germanium, and indium availability is constrained by byproduct production and host-material dynamics | PDF pp. 1-2 | Use for byproduct logic, not short-run export-control effects |
| `handley_kamal_monarch2024_supply_chain_adjustments` | Trade shocks can work through importer exit, buyer-supplier relationship discontinuation, and supplier-concentration heterogeneity | PDF pp. 1-2 | Tariff shock context, not mineral licensing |
| `park2025graphite_supply_chain` | Graphite supply-chain details differ across mining, processing, and battery-anode stages | Summary and parsed source | Product-specific context only |
| `vandenbrink2022antimony_resilience` | Antimony has supply-chain resilience and vulnerability concerns | Summary and parsed source | Product-specific context only |
| `xu2025antimony_material_flow` | Antimony material flows and demand context can help interpret antimony heterogeneity | Summary and parsed source | Product-specific context only |
| `santossilva2006gravity` | Log-linear OLS can be biased under heteroskedasticity and PPML naturally handles zeros | PDF pp. 1-2 | Supports estimator choice; not full identification |
| `fally2015_structural_gravity_fe` | PPML with exporter/importer fixed effects is consistent with structural-gravity adding-up constraints and multilateral resistance logic | PDF pp. 1-2 | Gravity-method support only |
| `olden_moen2022_triple_difference` | DDD is a difference between DiD comparisons and relies on equal-bias logic rather than two separate parallel-trends assumptions | PDF pp. 1-2 | Linear DDD identification logic; explain PPML implementation separately |
| `callaway2021difference` | Multi-period DiD should account for treatment-timing variation | Summary and parsed source | Methods justification only |
| `sun2021eventstudies` | Event-study estimates can be contaminated under heterogeneous treatment timing | Summary and parsed source | Methods caution only |
| `borusyak_jaravel_spiess2024_event_studies` | Imputation-based event-study logic addresses staggered-adoption problems | Summary and parsed source | Does not solve few-shock inference alone |
| `dechaisemartin2020twfe` | TWFE can behave poorly with heterogeneous treatment effects | Summary and parsed source | Methods caution only |
| `conley_taber2011_small_policy_changes` | DiD inference is difficult when identification comes from few policy changes | PDF pp. 1, 4 | Inference caution |
| `ferman_pinto2019_few_treated` | Few treated groups and heteroskedasticity can invalidate standard DiD inference | PDF pp. 1-3 | Inference caution |
| `mackinnon_webb2018_few_treated_clusters` | Cluster-robust and wild-bootstrap inference can fail with very few treated clusters | Summary and parsed source | Linear-cluster inference caution |
| `roth2022pretest` | Pretrend testing can create interpretation problems | Summary and parsed source | Use when discussing diagnostics |
| `rambachan2023honest` | Sensitivity analysis can relax strict parallel-trends assumptions | Summary and parsed source | Thesis-stage robustness plan |
| `martin_anderson2012_price_insulation` | Export restrictions can insulate domestic prices from world prices and affect international prices | PDF pp. 1-2 | Commodity-price mechanism, not mineral-specific |
| `brander_bernauer_huss2023_trade_policy_volatility` | Trade-policy announcements can affect commodity-price volatility | Summary and parsed source | Food commodity setting; use narrowly |

## 5. Final Proposal Depth

The proposal should be written as a substantial ZJU opening report, not as a
short defense memo. The binding requirement from the ZJU Economics documents is
that the opening report and literature review are merged, formatted like a
thesis document, and reach at least 10,000 Chinese characters/words. The safer
reference-count target is at least 30 references.

Working depth target for the English proposal:

| Section | Target depth | Main function |
|---|---:|---|
| 1. Research Background and Significance | 1,200-1,600 words | Motivate and define the question |
| 2. Literature Review | 2,500-3,200 words | Synthesize streams and identify gap |
| 3. Research Content and Design | 3,000-3,800 words plus tables/equations | Show feasibility, hypotheses, data, methods, and preliminary evidence |
| 4. Contributions and Innovations | 600-900 words | State academic and policy contribution |
| 5. Research Plan and Timeline | 800-1,100 words plus schedule table | Show completion plan |
| Total before references | 8,100-10,600 words | Long enough for ZJU expectations, still proposal-sized |

Citation target:

- Final cited references should be above 30.
- The literature review should use citations selectively, likely 30-40 cited
  works across the whole proposal.
- Do not cite all 57 bibliography items unless each citation has a clear job.

## 6. Writing Order After This Note

1. Write the literature review first, because it will determine how much
   theoretical-framework and empirical-method prose is needed later.
2. Then revise the conceptual framework and hypotheses.
3. Then write the empirical strategy and data sections using only the minimum
   design in `01_notes/Empirical Strategy Lock.md`.
4. Then write research background, significance, contributions, and timeline.
5. Finally, compress, align citations, compile, and prepare the 5-7 minute
   slide deck.

## 7. Open Items Before Final Drafting

These do not block starting the literature-review prose, but they should be
remembered:

- The two MOFCOM license-guide source files are failed-download placeholders.
  Recapture them only if the final proposal needs to cite the guide documents
  specifically. Otherwise, rely on the official control announcements, the PRC
  law/regulation, and the MOFCOM approval/review statements.
- Add formal data-source citations or source notes for UN Comtrade, CEPII,
  Bloomberg, and Wind only when the final data section is fixed.
- Keep 2025 policy episodes as future thesis expansion candidates unless the
  empirical design is explicitly expanded.
- Keep Eurostat CN8 out of the proposal unless the user later decides to
  restore it as a separate robustness extension.
