# Deep Research Prompt: Thesis-Stage Literature Extension

You are a research assistant helping me extend the canonical literature corpus for an academic master thesis proposal and later master thesis.

Your task is **not** to write the literature review prose. Your task is to conduct structured source discovery and produce a thesis-stage literature control document that can replace or extend:

```text
02_literature/literature_master.md
```

The current `literature_master.md` is term-paper oriented. The thesis now needs a stronger theoretical framework and a stronger empirical-methods foundation. The output should be operational: it should tell me which sources belong in the corpus, what each source supports, where each source maps into the proposal/thesis, and what still needs to be collected.

## 1. Project Context

Working title:

```text
When Do Critical-Mineral Export Controls Bind? China's Licensing-Based Controls and Heterogeneous Trade Responses
```

Locked research question:

```text
Why do formally similar Chinese export-licensing controls generate different trade and price disruptions across critical minerals?
```

Project type:

```text
Master thesis proposal, later expanded into a master thesis.
```

Field:

```text
Chinese economy, international political economy, international trade, empirical economics, economic statecraft, critical minerals.
```

Reader/evaluator:

```text
Master thesis supervisor and proposal-defense committee at Zhejiang University. The supervisor has a strong China and econometrics background and specializes in electricity markets.
```

Expected proposal sections served by this literature work:

1. Research background and significance.
2. Literature review and research gap.
3. Conceptual framework and hypotheses.
4. Data sources and empirical strategy.
5. Contributions and research plan.

The output should support the thesis proposal first. Do not write as if final thesis results already exist.

## 2. Current Thesis Argument

The thesis studies Chinese critical-mineral export controls as **licensing-based China-source trade wedges**, not as automatic export bans.

A control is treated as **binding** when it creates an observable China-specific licensing wedge. Empirically, this means that imports from China fall relative to rest-of-world sourcing, untreated products, or pre-control timing patterns, and the trade result is supported by timing, price, or adjustment evidence.

The thesis does **not** observe MOFCOM approval probabilities, license denials, inventories, or foreign-policy concessions. "Binding" therefore means market restriction and adjustment, not export-ban status and not coercive political success.

Current subquestions:

1. **Trade and timing:** Do Chinese licensing controls reduce China-sourced imports of treated critical minerals relative to rest-of-world sourcing and untreated products, and do the effects appear after the expected implementation/import-arrival month?
2. **Adjustment and disruption:** When China-sourced imports fall, do importers mainly switch toward non-China suppliers, or do total imports contract?
3. **Price and heterogeneity:** Do binding controls widen domestic-international price wedges, and are stronger disruptions concentrated in products and importers with higher China exposure, cleaner treatment scope, fewer outside options, or more credible policy design?

Current thesis hypotheses:

1. **Binding licensing-wedge hypothesis:** If a licensing control binds, China-sourced imports of the treated product should fall relative to rest-of-world imports and relative to untreated comparison products after the expected import-effect month.
2. **Adjustment-margin hypothesis:** The trade response depends on importer adjustment capacity. Where importers have both high pre-policy China exposure and observable access to non-China suppliers, the China-source decline should be stronger and should be accompanied by increased rest-of-world sourcing. Where outside options are weak, disruption should appear more as total import contraction or price pressure.
3. **Price-and-product-conditions hypothesis:** Binding controls should widen international prices relative to comparable Chinese domestic prices, especially for cleaner treated products and products where China's supply position is difficult to replace. Bundled, partial, sparse, or demand-boom products should show weaker, noisier, or null aggregate trade effects.

## 3. Current Empirical Design

Primary unit:

```text
importer i x product p x source s x month t
```

Primary outcome:

```text
Monthly trade value in USD from UN Comtrade bilateral import data.
```

Primary source split:

```text
China versus rest of world.
```

Primary estimator:

```text
Source-share PPML triple difference with high-dimensional fixed effects.
```

Conceptual model:

```text
E[M_ipst | X] =
exp[
  beta (Treated_p x China_s x Post_t)
  + importer-product FE
  + importer-source FE
  + product-month FE
  + source-month FE
  + product-source FE
  + importer-month FE
]
```

Planned thesis extensions:

1. Wave-specific source-share triple differences for each treatment cohort.
2. Staggered triple-difference/event-study diagnostics across treatment waves.
3. Domestic-international price-wedge analysis for treated products.
4. Heterogeneity by product scope, value-chain position, China exposure, outside-option proxy, and market concentration.
5. Robustness checks for timing, donor pools, pretrends, sparse flows, re-export hubs, quantities where complete, and alternative placebo sets.

Important inference constraint:

```text
Treatment varies at product-time, not reporter-time. Reporter-clustered p-values are conditional diagnostics and cannot by themselves solve the small number of independent product-level policy shocks.
```

## 4. Existing Project Files to Use

Use these files as the starting corpus and project context:

```text
02_literature/literature_master.md
02_literature/references.bib
02_literature/summaries/
02_literature/sources/
01_notes/Research Question.md
01_notes/Thesis Design.md
01_notes/Licensing Wedge Framework.md
01_notes/Methodology.md
05_draft/proposal/main.tex
```

Do not assume the existing `literature_master.md` is complete. It was designed for a term paper and must be upgraded for the thesis proposal.

## 5. Existing Source Corpus

The following sources already exist in `02_literature/references.bib`. Treat them as the starting corpus. Do not duplicate them under new citation keys. If a source should be promoted, demoted, or renamed, say so explicitly.

### Economic Statecraft and Technology Competition

| Citation key | Current role |
|---|---|
| `farrell2019weaponized` | Network power, chokepoints, weaponized interdependence. |
| `farrell2023underground_empire` | Book-length contemporary framing of weaponized network power. |
| `egger2024sanctions` | Sanctions/economic coercion theory, data, and quantification overview. |
| `bown2020semiconductor` | U.S.-China semiconductor trade-war context. |
| `bown2024semiconductors` | Modern semiconductor industrial policy and controls. |
| `bis_2022_oct7_semiconductor_controls` | Primary U.S. semiconductor-control chronology. |
| `bis_2024_dec2_semiconductor_controls` | Late-2024 U.S. semiconductor-control escalation. |

### Chinese Export-Control Institutions and Policy Episodes

| Citation key | Current role |
|---|---|
| `prc_2020_export_control_law` | Legal basis for China's export-control system. |
| `scio_2021_chinas_export_controls` | Official English overview of China's export-control system. |
| `mofcom_2006_graphite_temporary_controls` | Earlier graphite temporary-control precedent. |
| `mofcom_2023_gallium_germanium_controls` | Core gallium/germanium treatment-start document. |
| `mofcom_2023_gallium_germanium_approvals` | Official evidence that compliant gallium/germanium applications were approved. |
| `mofcom_2023_gallium_germanium_license_guide` | Operational licensing requirements for gallium/germanium. |
| `mofcom_2023_graphite_controls` | Core graphite treatment-start document. |
| `mofcom_2023_graphite_license_guide` | Operational licensing requirements for graphite. |
| `mofcom_2024_graphite_faq` | Official graphite scope clarification. |
| `mofcom_2024_graphite_approvals` | Official evidence that compliant graphite applications were approved. |
| `mofcom_2024_antimony_controls` | Core antimony treatment-start document. |
| `mofcom_2024_antimony_license_review` | Official evidence on antimony license applications under review. |
| `mofcom_2024_us_controls_critical_minerals` | Later U.S.-destination escalation, contextual only unless periodized separately. |
| `mofcom_2025_w_te_bi_mo_in_controls` | Thesis expansion candidate: tungsten, tellurium, bismuth, molybdenum, indium. |
| `mofcom_2025_medium_heavy_rare_earth_controls` | Thesis expansion candidate: medium and heavy rare earth controls. |
| `mofcom_2025_suspend_us_controls_art2` | Suspension/adjustment of U.S.-destination measures. |
| `mofcom_2025_suspend_55_58_61_62` | Suspension preventing false treatment coding for later 2025 measures. |

### Critical Minerals and Market Structure

| Citation key | Current role |
|---|---|
| `usgs_2026_gallium` | Gallium market structure, supply, uses, and China position. |
| `usgs_2026_germanium` | Germanium market structure, supply, uses, and China position. |
| `usgs_2026_graphite_natural` | Natural graphite supply and use profile. |
| `usgs_2026_antimony` | Antimony supply and use profile. |
| `iea_2025_global_critical_minerals_outlook` | Critical-mineral concentration and diversification context. |
| `frenzel2017byproduct_metals` | Byproduct-metal supply mechanism for gallium, germanium, and indium. |
| `park2025graphite_supply_chain` | Graphite supply-chain supplement. |
| `vandenbrink2022antimony_resilience` | Antimony supply-chain resilience supplement. |
| `xu2025antimony_material_flow` | Antimony material-flow and energy-transition demand context. |

### Empirical Methods

| Citation key | Current role |
|---|---|
| `santossilva2006gravity` | PPML for zeros and heteroskedastic trade flows. |
| `callaway2021difference` | Difference-in-differences with multiple periods and staggered timing. |
| `sun2021eventstudies` | Dynamic event studies with heterogeneous treatment effects. |
| `dechaisemartin2020twfe` | TWFE problems with heterogeneous treatment effects. |
| `rambachan2023honest` | Sensitivity to violations of parallel trends. |
| `roth2022pretest` | Caution on pretrend testing. |

## 6. Main Literature Gaps to Fill

Prioritize gaps that strengthen the **theoretical framework** and the **empirical strategy**. Do not expand the corpus just because sources are interesting.

### Gap A: Theory of Licensing-Based Export Controls

Find sources that help distinguish:

1. export licensing from outright export bans;
2. administrative trade frictions from quantity restrictions;
3. approval uncertainty, delay, compliance costs, and end-use documentation as mechanisms;
4. de jure policy design versus de facto binding constraint;
5. national-security review as an economic shock.

Preferred source types:

- peer-reviewed work on export controls, trade restrictions, sanctions, economic coercion, and non-tariff barriers;
- legal-institutional sources only if they clarify the mechanism of export licensing;
- official sources only if they provide institutional detail unavailable elsewhere.

### Gap B: Theoretical Framework for Heterogeneous Binding

Find sources that help formalize why formally similar licensing controls bind differently across products.

Search for theory or empirical evidence on:

1. supply-chain chokepoints and state power;
2. market concentration, substitution costs, and outside options;
3. byproduct metals and supply inelasticity;
4. value-chain stage: mining, refining, processing, downstream demand;
5. product scope and HS-code aggregation;
6. importer adjustment capacity and supplier switching;
7. stockpiling, anticipation, inventory adjustment, and delayed trade responses;
8. price wedges as evidence of segmented markets or scarcity.

The goal is to support a compact model of a latent licensing wedge:

```text
licensing wedge = delay/denial risk + compliance cost + uncertainty + reduced Chinese availability
```

The model should connect this wedge to:

```text
China-source import decline;
rest-of-world switching;
total import contraction;
domestic-international price wedge;
heterogeneity by product and importer characteristics.
```

### Gap C: Export Controls, Critical Minerals, and China

Find sources that connect China's critical-mineral controls to:

1. Chinese industrial policy and national security;
2. critical-mineral supply-chain concentration;
3. technology competition;
4. mineral-specific cases beyond the current official MOFCOM documents;
5. past rare-earth disputes only where they help the argument without pulling the thesis into WTO/legal history.

Avoid generic critical-minerals reports unless they provide product-specific evidence for gallium, germanium, graphite, antimony, tungsten/APT, bismuth, indium, tellurium, or rare earths.

### Gap D: Empirical Strategy for Trade-Flow Shocks

Find sources that justify or improve the empirical strategy:

1. PPML gravity/trade-flow estimation with high-dimensional fixed effects;
2. triple-difference designs in trade or policy-evaluation settings;
3. event studies with staggered adoption and heterogeneous treatment timing;
4. inference when treatment varies at an aggregate level and the number of treated units is small;
5. product-level placebo diagnostics, donor-pool screening, or permutation/placebo methods, if directly useful;
6. trade responses on source shares, total imports, supplier count, HHI, and rerouting.

Do not add generic methods papers unless they directly support one planned estimator or one known inference problem in this thesis.

### Gap E: Price-Wedge and Market-Segmentation Evidence

Find sources that help design and interpret domestic-international price comparisons:

1. price DiD or event-study designs with domestic and international benchmark prices;
2. law-of-one-price deviations, market segmentation, export restrictions, or commodity arbitrage constraints;
3. unit, grade, location, currency, and incoterm harmonization for commodity prices;
4. how to interpret price wedges when trade-flow evidence is mixed.

The output should say whether price evidence is best treated as causal, supporting, descriptive, or mechanism evidence.

## 7. Source Discovery Rules

Search deliberately across:

1. Google Scholar or equivalent scholarly discovery.
2. Publisher pages.
3. NBER, CEPR, SSRN, RePEc, arXiv, and working-paper platforms when relevant.
4. Official agencies and international organizations for product-specific facts.
5. WTO, OECD, World Bank, IMF, IEA, USGS, EU/JRC, European Commission, BIS, MOFCOM, and Chinese official sources when directly relevant.

Prioritize:

1. peer-reviewed journal articles;
2. academic books or book chapters from reputable presses;
3. credible working papers with clear methods;
4. official reports with product-specific data or institutional detail;
5. datasets or methodology pages only when needed for measurement.

Avoid:

1. generic critical-minerals commentary;
2. news articles except for chronology leads;
3. compliance-client alerts unless no better source explains licensing mechanics;
4. broad sanctions literature that does not help with trade flows, export controls, or identification;
5. sources that duplicate the existing corpus without adding a named function.

## 8. Required Output

Produce a single Markdown document with this structure:

```markdown
# Literature Master - Thesis Extension

## Purpose

Explain that this is the thesis-stage literature control document for the critical-minerals export-control project.

## Project Context

| Field | Value |
|---|---|
| Title | When Do Critical-Mineral Export Controls Bind? China's Licensing-Based Controls and Heterogeneous Trade Responses |
| Research question | Why do formally similar Chinese export-licensing controls generate different trade and price disruptions across critical minerals? |
| Project type | Master thesis proposal and later master thesis |
| Field | Chinese economy; international trade; empirical economics; economic statecraft |
| Core empirical design | UN Comtrade importer-product-source-month panel; source-share PPML triple difference; staggered/event-study diagnostics; price-wedge analysis |

## Corpus Rules

State rules for including, excluding, promoting, and demoting sources.

## Existing Corpus Audit

Audit every existing citation key listed above. For each source, classify:

- keep as must-cite;
- keep as should-cite;
- keep as optional;
- demote/defer;
- replace or supplement;
- citation-key cleanup needed.

## Stream Structure

Create 5-7 literature streams. At minimum include:

1. Economic statecraft and export controls.
2. China's export-control institutions and critical-mineral policy episodes.
3. Critical-mineral supply chains and product heterogeneity.
4. Licensing-wedge theory and adjustment mechanisms.
5. Trade-flow empirical strategy.
6. Staggered/event-study inference and small-treatment-unit problems.
7. Price-wedge and market-segmentation evidence.

For each stream, explain:

- analytical function;
- proposal/thesis sections served;
- existing sources;
- new sources needed;
- claims the stream can safely support.

## Canonical Source Table

| Citation Key | Full Citation | Source Type | Priority | Stream | Role in Thesis | Can Safely Support | Cannot Support | DOI / URL | Repository Status | Action |
|---|---|---|---|---|---|---|---|---|---|---|

Include both existing sources and newly discovered candidate sources.

## New Source Candidates

For each newly discovered source:

### `[suggested citation key]`

- **Full citation:**
- **Source type:**
- **Priority:** must-cite / should-cite / optional / deferred
- **Stream:**
- **Why it belongs:**
- **Main use in proposal/thesis:**
- **Claim(s) it can safely support:**
- **Caveat / limitation:**
- **DOI / stable URL:**
- **Download status:** available / needs verification / not found
- **Suggested folder name:** `author_year_short_title`
- **BibTeX needed:** yes / no

## Theoretical Framework Upgrade

Synthesize the sources into a compact thesis-stage framework. Do not write final prose, but give:

1. the central mechanism;
2. the key product-level moderators;
3. the key importer-level moderators;
4. the expected trade margins;
5. the expected price margin;
6. how this framework differs from a simple "export control equals export collapse" story.

## Empirical Strategy Upgrade

Map methods sources to the planned empirical designs:

| Design Element | Current Plan | Existing Support | Missing/Needed Source Support | Recommended Source(s) |
|---|---|---|---|---|

Include:

- source-share PPML triple difference;
- wave-specific DDD;
- staggered/event-study diagnostics;
- price-wedge DiD/event study;
- switching-potential heterogeneity;
- donor-pool and placebo diagnostics;
- inference limits with few product-level treatments.

## Missing Sources / Search Gaps

List remaining gaps after the search. Be concrete.

## Source Acquisition Checklist

| Target Source | Priority | Zotero | PDF/HTML | Source Folder | Summary Needed | Notes |
|---|---|---|---|---|---|---|

## Suggested Next Steps

Give the next steps for integrating the literature into:

1. `02_literature/references.bib`;
2. `02_literature/sources/`;
3. `02_literature/summaries/`;
4. the proposal literature review;
5. the theoretical-framework section;
6. the empirical-strategy section.
```

## 9. Quality Rules

Be selective. For a thesis proposal, the active corpus should not become a source dump. The current repository already has 39 BibTeX entries, many of which are official policy documents. Add sources only if they perform a named theoretical, empirical, or institutional function.

Use this priority standard:

- `must-cite`: indispensable for the proposal argument or method.
- `should-cite`: likely to appear in the proposal or thesis, but not structurally indispensable.
- `optional`: useful for a narrow point, appendix, or backup.
- `deferred`: relevant but not admitted to the active corpus now.
- `discard`: found but should not be used, with a reason.

For every source, distinguish:

- **Can safely support:** a claim directly supported by the source.
- **Useful background:** context only.
- **Cannot support:** claims the source does not justify.
- **Caveat:** scope, data, method, publication status, or relevance limits.

Do not invent DOI numbers, page numbers, datasets, or download availability. If uncertain, write `needs verification`.

## 10. Final Check

Before finalizing, check:

1. Does every active source serve a named project function?
2. Does the theoretical-framework upgrade explain heterogeneous binding, not just economic statecraft in general?
3. Does the empirical-methods upgrade support the actual models planned for the thesis?
4. Are official documents separated from academic literature?
5. Are current citation-key mismatches identified rather than silently duplicated?
6. Are weak or redundant sources demoted?
7. Is the result directly usable for Zotero import, BibTeX cleanup, source folders, summaries, and proposal drafting?

Now conduct the research and produce the final Markdown document.
