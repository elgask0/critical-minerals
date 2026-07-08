---
description: "Canonical thesis design, theoretical model, empirical architecture, and minimum-success criteria"
created: 2026-06-11
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, thesis, research-design, model]
status: active
created_by: codex
---

# Thesis Design

This is the canonical intellectual design for the master's thesis. It
supersedes the stronger result-led claims in `Motivation.md`,
`Differential Effectiveness.md`, and the current term-paper draft.

Theory lock, 2026-07-01: the revised proposal uses the post-defense
importer-product pressure framework in `Theoretical Framework Lock.md` and
`Binding Pressure Framework Revision.md`. The older two-period commitment
model and the single switching-potential proxy are no longer the proposal
backbone.

## 1. Supervisory Assessment

The project is viable as a master's thesis in Chinese economy if it is framed
as a transparent comparative evaluation of Chinese export-licensing regimes,
not as a definitive test of a universal theory of economic coercion.

The current data support one strong descriptive fact: China's reported natural
graphite exports exhibit a sharp implementation break. They do not yet support
the claim that graphite controls had a persistent causal effect across all
trade measures, nor that extreme monopoly independently explains the
difference between graphite and gallium.

The thesis should therefore make three disciplined contributions:

1. reconstruct the legal design and timing of China's licensing regimes;
2. build pre-policy pressure indexes from importer exposure and non-China
   supplier structure;
3. test whether these indexes predict source switching, import compression,
   and price segmentation.

## 2. Reframing

### Previous broad claim

The term-paper argument was:

> Graphite controls worked, gallium/germanium controls did not, and extreme
> monopoly creates a commitment problem that makes coercion non-monotonic in
> China's market share.

This is too strong because it is inferred from two heterogeneous cases,
bundled HS codes, incomplete price evidence, and estimators whose apparent
precision came partly from treating importer-month observations as independent
policy shocks.

### Motivation

China's recent critical-mineral measures are formally similar export-licensing
regimes, but they do not have to produce the same market response. A licensing
announcement is not itself a quantity restriction. The economically important
question is when a legal rule creates source switching, import compression, or
price segmentation.

### Primary research question

> **When do Chinese critical-mineral export licensing controls bind, and
> through which adjustment margins?**

This is the locked master thesis question. It keeps the project focused on
observable market responses rather than unobserved licensing decisions,
welfare, or foreign-policy concessions.

### Definition of binding

A licensing control is treated as binding when it creates an observable market
restriction or adjustment after the expected import-effect month. Empirically,
binding can appear as a pressure-predicted China-source decline, source
switching toward non-China suppliers, total import compression, or a wider
international-China price wedge.

The thesis does not observe MOFCOM approval probabilities, license denials,
inventories, or foreign-policy concessions. "Binding" therefore means market
restriction and adjustment, not an export ban and not coercive political
success.

### Subquestions

1. **Pressure and trade:** Do importer-product pairs with higher predicted
   pressure show larger post-policy China-source declines?
2. **Switching and compression:** Does switching pressure predict RoW
   replacement, while compression pressure predicts weak RoW replacement and
   total import decline?
3. **Price segmentation:** Do products with higher compression pressure show
   wider international-China price wedges where matched prices exist?

## 3. Hypotheses

### H1: China-source pressure hypothesis

Higher predicted China-source decline pressure should imply a larger
post-policy decline in China-sourced imports of treated products.

This is tested with source-share PPML interactions between the treatment
indicator and pre-policy pressure indexes.

### H2: Switching channel hypothesis

Switching pressure should predict a China-source decline, a rise in
rest-of-world imports, and stable or rising total imports.

This is tested with China, rest-of-world, and total import PPML margin models.

### H3: Compression and price-segmentation hypothesis

Compression pressure should predict a China-source decline, weak rest-of-world
replacement, total import decline, and a wider international-China price wedge
where comparable prices exist.

This is tested with the margin models and the matched price-wedge panel.

## 4. Locked Theoretical Framework

The revised framework is specified in `Theoretical Framework Lock.md` and
`Binding Pressure Framework Revision.md`. The legal control is not the
estimand. The estimand is whether pre-policy pressure predicts post-policy
trade and price adjustment.

The locked causal chain is:

\[
\text{legal licensing rule}
\rightarrow
\text{pre-policy importer-product pressure}
\rightarrow
\begin{cases}
\text{source switching},\\
\text{import compression},\\
\text{price segmentation},\\
\text{weak or measurement-limited response}.
\end{cases}
\]

Importer China exposure is:

\[
E_{ip}=
\frac{\sum_{t<T_p^{ann}}M^C_{ipt}}
{\sum_{t<T_p^{ann}}M^C_{ipt}+\sum_{t<T_p^{ann}}M^R_{ipt}}.
\]

Importer outside access is:

\[
O_{ip}=
\frac{\#\{t<T_p^{ann}:M^R_{ipt}>0\}}
{\#\{t<T_p^{ann}\}}.
\]

Leave-one-importer-out non-China outside-market strength is:

\[
A^{ROW}_{-i,p}
=
Depth^{ROW}_{-i,p}(1-HHI^{ROW}_{-i,p}).
\]

Replacement rigidity is:

\[
R_{-i,p}=1-A^{ROW}_{-i,p}.
\]

Switching pressure is:

\[
P^S_{ip}=E_{ip}O_{ip}A^{ROW}_{-i,p}.
\]

Compression pressure is:

\[
P^C_{ip}=E_{ip}(1-O_{ip})R_{-i,p}.
\]

China-source decline pressure is:

\[
P^X_{ip}=P^S_{ip}+P^C_{ip}.
\]

The old commitment model is demoted. It can motivate possible self-cost or
credibility language only if observable trade, price, and adjustment patterns
support it. It should not appear as the proposal's main theoretical model.

## 5. Outcomes to Reconstruct

The outcome is not a single trade total. For every product and month, construct:

| Margin | Outcome | Interpretation |
|---|---|---|
| Export departure | China-reported world exports | Earliest direct measure of implementation |
| Import arrival | Reporter imports from China | Mirror measure, shifted by shipping/customs lag |
| Source share | China imports / world imports | China's position within importer demand |
| Total demand | World imports by reporter | Distinguishes source loss from demand contraction |
| Rerouting | Non-China imports | Alternative sourcing or intermediated trade |
| Diversification | Supplier count and HHI | Importer adjustment |
| Physical quantity | Net weight where available | Robustness only because coverage is incomplete |
| Unit value | Value/net weight | Descriptive only; composition-sensitive |
| Price wedge | International less comparable China price | Foreign scarcity and domestic redirection |

Trade value is the primary bilateral outcome because China net-weight coverage
ranges from 26.7% to 84.1% across current products. Quantity estimates must use
the complete-case subset and report coverage.

## 6. Empirical Architecture

### 6.1 Descriptive exporter interruption

Estimate a log-level interrupted time series for China-reported aggregate
exports with a trend and implementation indicator. Use Newey-West/HAC standard
errors with six monthly lags. This establishes timing but has no untreated
counterfactual, so it is descriptive supporting evidence.

### 6.2 Primary trade estimator

Use quarterly PPML as the preferred baseline. Monthly PPML remains useful for
timing diagnostics, anticipation, and robustness. The preferred source panel
is importer-product-source-quarter, built from the monthly Comtrade panel:

\[
E[M_{ipst}|X] =
\exp\left[
\beta_0(Treated_p \times China_s \times Post_{pt})
+\Gamma_{ip}+\Gamma_{is}+\Gamma_{pt}
+\Gamma_{st}+\Gamma_{ps}+\Gamma_{it}
\right].
\]

This is the average source-share triple difference. It is useful for reporting
the average China-source response, but it is no longer the main theoretical
test. The main post period is the first full post-implementation quarter.

The preferred theory-guided model is:

\[
E[M_{ipst}|X] =
\exp\left[
\beta_0D_{ipst}
+\theta_S(D_{ipst}\times \widetilde P^S_{ip})
+\theta_C(D_{ipst}\times \widetilde P^C_{ip})
+\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}
\right],
\]

where:

\[
D_{ipst}=Treated_p\times China_s\times Post_{pt}.
\]

Expected signs:

\[
\theta_S<0,\qquad \theta_C<0.
\]

\(\theta_S\) and \(\theta_C\) test whether predicted switching pressure and
compression pressure explain heterogeneous China-source declines. This is the
main post-defense empirical test.

The policy shock is assigned at product-time, not importer-time. Reporter
clustering is therefore conditional and cannot alone justify conventional
causal p-values. Product-assignment placebo inference and the number of
independent products must be reported prominently.

### 6.2.1 Mechanism margin models

Estimate China, rest-of-world, and total import outcomes on collapsed
importer-product-quarter panels in the baseline. Monthly versions remain
robustness and timing diagnostics.

For China imports:

\[
E[M^C_{ipt}|X] =
\exp\left[
\theta^C_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+\theta^C_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+\alpha_{ip}+\delta_{it}+\lambda_{pt}
\right].
\]

For rest-of-world imports:

\[
E[M^R_{ipt}|X] =
\exp\left[
\theta^R_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+\theta^R_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+\alpha_{ip}+\delta_{it}+\lambda_{pt}
\right].
\]

For total imports:

\[
E[M^T_{ipt}|X] =
\exp\left[
\theta^T_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+\theta^T_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+\alpha_{ip}+\delta_{it}+\lambda_{pt}
\right].
\]

Expected signs:

\[
\theta^C_S<0,\quad \theta^R_S>0,\quad \theta^T_S\geq 0,
\]

\[
\theta^C_C<0,\quad \theta^R_C\leq 0,\quad \theta^T_C<0.
\]

These margin models are needed because raw trade movements can reflect demand,
exchange rates, inventories, shipping, and unrelated supply shocks.

### 6.3 Dynamic PPML

Re-estimate the triple difference with event-time interactions centered on the
first plausible importer-arrival month. Keep announcement and implementation
markers on every figure. Test recent pre-treatment coefficients jointly, while
acknowledging that the same small-cluster constraint applies.

Use:

- August 2023 implementation and September 2023 first importer exposure for
  gallium/germanium;
- December 2023 implementation and January 2024 first importer exposure for
  graphite;
- September 2024 implementation and October 2024 first importer exposure for
  antimony, subject to shipment-lag verification.

### 6.4 Price-wedge outcome

For each matched price pair, convert prices to a common currency and unit.
Define:

\[
\pi_{pt}
=
\log P^{INT}_{pt}
-
\log P^{CN}_{pt}.
\]

Aggregate pressure to product level with pre-policy trade weights:

\[
\bar P^C_p=\sum_i w_{ip}P^C_{ip},
\qquad
\bar P^S_p=\sum_i w_{ip}P^S_{ip}.
\]

Estimate:

\[
\pi_{pt}
=
\alpha_p+\tau_t
+\rho_C(Post_{pt}\times \bar P^C_p)
+\rho_S(Post_{pt}\times \bar P^S_p)
+u_{pt}.
\]

Expected signs:

\[
\rho_C>0,\qquad \rho_S\approx 0.
\]

The estimand is a regional price wedge, not a frictionless
law-of-one-price gap. The price wedge is a central outcome because import
values mix quantity and price changes. It should not be used as a control
inside the trade PPML.

### 6.5 SCM and Synthetic DiD

SCM and Synthetic DiD may be reported only as descriptive appendix
diagnostics with the current three donors. Their minimum exact placebo
p-value is 0.25 and donor fit is not robust. They become credible only after a
larger, policy-screened donor pool is built.

### 6.6 Estimators not used

- Matrix completion: dropped from the current thesis.
- CausalImpact: dropped because the prior and donor choices add little beyond
  transparent SCM diagnostics.
- Callaway-Sant'Anna: deferred until there are enough independently treated
  product codes across multiple implementation cohorts.
- ITS: retained only as descriptive supporting evidence, not the primary
  causal estimator.

## 7. Inference and Robustness

Required:

1. PPML rather than log-one-plus OLS as the primary bilateral estimator.
2. Reporter-clustered standard errors labeled as conditional.
3. Pressure indexes constructed only from pre-policy data.
4. Pressure-interaction PPML for source-share outcomes.
5. China, rest-of-world, and total import margin models.
6. Product-assignment placebo/randomization diagnostics.
7. Recent-window and full-window pretrend tests.
8. Announcement versus implementation timing and explicit shipping lags.
9. Alternative 12- and 24-month pre-periods.
10. Alternative HHI interpretation for outside-market strength.
11. Exclusion of re-export hubs and countries with negligible pre-treatment
   trade.
12. Trade value primary; net weight complete-case robustness.
13. Alternative placebo sets chosen before viewing post-treatment estimates.
14. Rambachan-Roth bounds only for a clearly specified linear event-study
    outcome with enough pre-period support. It cannot repair four treatment
    clusters.

## 8. Current Evidence

The original three-treated-product, three-control results are superseded. The
current evidence comes from the post-defense pressure panel and the strict
clean quarterly design. Older HS 282580 and Ga/Ge results remain useful for
provenance and secondary interpretation, not as the current thesis backbone.

The current result map is in `Post-Defense Thesis Plan.md`.

### Quarterly pressure-design summary

| Case | Quarterly average PPML, first full post-quarter | Current status |
|---|---:|---|
| HS 2504 natural graphite | -30.1%, p = 0.076 | Suggestive; pressure-switching evidence is stronger than the average effect |
| HS 8110 antimony metal | -86.7%, p = 9.13e-09 | Strong average effect, but timing and placebo-date concerns remain |
| Wave 4 W/Bi | -42.4%, p = 0.021 | Supported aggregate wave result |
| HS 8106 bismuth | -74.4%, p = 0.000305 | Strong average effect and strong price-wedge support |
| HS 284180 tungstates/APT | -15.2%, p = 0.683 | Weak or informative null under current evidence |

The current mechanism reading is that switching pressure is clearer than
compression pressure. Price wedges support segmentation for antimony and
bismuth. Compression remains plausible but mixed in trade quantities.

The term-paper result hierarchy is:

1. HS 282580 antimony oxides: central result;
2. HS 2504 graphite: suggestive;
3. HS 8110 antimony metal: supportive but pretrend-limited;
4. HS 261710 antimony ores/concentrates: descriptive only;
5. HS 811292 and HS 282560: aggregate nulls or measurement-sensitive cases.

### Exporter ITS with HAC(6)

| Product | Estimated break | p-value | Assessment |
|---|---:|---:|---|
| Natural graphite 2504 | -99.7% | 0.142 | Descriptive; 2025-2026 no-record months affect interpretation |
| Ga/Ge bundle 811292 | -89.2% | 0.587 | Descriptive only |
| GeO2/ZrO2 282560 | -91.6% | 0.513 | Descriptive only |
| Antimony metal 8110 | -100.0% | <0.001 | Descriptive timing support |
| Antimony ores 261710 | -99.8% | 0.004 | Sparse upstream series |
| Antimony oxides 282580 | -100.0% | <0.001 | Descriptive timing support |
| Artificial graphite 3801 | -99.9% | 0.151 | Partially treated; descriptive only |

### Corrected source-share PPML

| Case | Estimate | Reporter-cluster p | Pretrend p | Assessment |
|---|---:|---:|---:|---|
| Graphite 2504 | -30.4% | 0.107 | 0.020 | Suggestive only |
| Ga/Ge 811292 | +19.3% | 0.365 | <0.001 | No aggregate negative effect |
| GeO2/ZrO2 282560 | +17.5% | 0.271 | 0.260 | No aggregate negative effect |
| Antimony metal 8110 | -86.8% | <0.001 | <0.001 | Supportive, but pretrends fail |
| Antimony ores 261710 | -98.9% | 0.003 | <0.001 | Sparse/descriptive only |
| Antimony oxides 282580 | -81.5% | 0.002 | 0.680 | Central result |

### Switching-potential split

| Case | High-A estimate | High-A pretrend p | Low-A estimate | Low-A pretrend p | Assessment |
|---|---:|---:|---:|---:|---|
| Graphite 2504 | -34.1% | 0.089 | +34.5% | 0.006 | Weak mechanism support |
| Ga/Ge 811292 | +9.2% | <0.001 | +705.4% | <0.001 | No support |
| GeO2/ZrO2 282560 | +1.4% | 0.267 | +30.2% | <0.001 | No support |
| Antimony metal 8110 | -86.8% | <0.001 | -64.2% | <0.001 | Directional but not clean |
| Antimony ores 261710 | -100.0% | 0.000 | very large positive | <0.001 | Not interpretable |
| Antimony oxides 282580 | -87.4% | 0.354 | +103.1% | 0.161 | Strong mechanism support |

With one treated product and three placebos, an exact product-assignment test
cannot attain a p-value below 0.25. The extremely small four-cluster standard
errors produced by conventional product clustering are invalid and must not be
reported as evidence. The observed static source-share coefficient ranks as
the most extreme assignment in the current one-treated-product comparisons,
giving a placebo-assignment rank of 0.25. This is a diagnostic, not a literal
randomization p-value, because the policy was not randomly assigned and the
products are not fully exchangeable.

### Dynamic pattern

HS 282580 antimony oxides has the cleanest dynamic pattern. The source-share
event study shows increasingly negative post-treatment effects, with clean
source-share pretrends across announcement, implementation, and import-effect
anchors. Graphite has a weaker negative pattern, while antimony metal and
ores/concentrates have large post coefficients but fail pretrend diagnostics.
Aggregate Ga/Ge cases do not show robust negative static effects.

### SCM and Synthetic DiD

The current donor pool produces diagnostic effects broadly consistent with the
main hierarchy: negative for graphite and antimony, positive for aggregate
Ga/Ge, and strongest for sparse antimony ores. With three donors and limited
placebo support, SCM and Synthetic DiD remain descriptive diagnostics only.

## 9. Data Required Next

### Global demand controls

Download monthly January 2019 onward:

| Case | Preferred indicator | Exact field |
|---|---|---|
| Ga/Ge | SIA/WSTS world semiconductor sales | Monthly global sales, USD; total and optoelectronics/discretes if licensed |
| Graphite | China power-battery production and installations | Monthly GWh, total and chemistry where available |
| Graphite | CAAM China NEV production and sales | Monthly vehicles |
| Vanadium | World Steel Association crude steel | Monthly world and China tonnes |
| Antimony | NBS China lead-acid battery output | Monthly 10,000 kVAh |
| Antimony | Optional ILZSG refined lead usage | Monthly global/China tonnes |

The current `/Users/elgask0/Desktop/minerals data.xlsx` contains price series
only. It does not contain a semiconductor or downstream-demand index.

Demand variables should be converted to log indexes with 2019=100 and tested
with predetermined lags. Do not control for post-treatment outcomes that are
themselves affected by the policy.

### Production and concentration

Build a country-mineral-stage-year table from USGS Mineral Commodity Summaries
2020-2026:

- country production and world total;
- China share;
- HHI, top-three share, and number of active producers;
- reserves where available;
- mine, refinery, and processing stage kept separate;
- unit, estimate flag, publication year, source URL, and page.

Use 2022 values for the 2023 cases and 2023 values for antimony. These are
case-level theoretical descriptors, not regression covariates with the current
number of minerals. Where USGS lacks refining data, supplement only with
documented IEA, European Commission, or other official estimates.

### Policy design

The official-document collection must produce:

- announcement and implementation dates;
- complete controlled-product and customs-code crosswalk;
- predecessor rules and repeals;
- licensing documents, processing rules, end-use requirements, and FAQs;
- subsequent country-specific prohibitions, suspensions, and amendments;
- official evidence of approvals, delays, denials, enforcement, or penalties.

The copy-ready protocol is in `MOFCOM Deep Research Prompt.md`.

## 10. Expanded Product Design

### 10.1 Product classification

The downloader knows 34 products, including HS 3801 for later classification
and HS 2615 as an ore-stage candidate control. The policy-screened bilateral
acquisition universe is 31 products because HS 380120 and HS 2827 are
policy-contaminated, and broad HS 2617 is retained only as a China-export
diagnostic. Downloading a product does not commit it to the estimation sample.
The raw acquisition universe uses 56 reporter codes, but the analysis panel
uses 53 non-group reporters after excluding the European Union aggregate (97),
China as a reporter (156), and ASEAN aggregate (975).

#### Strict clean treated baseline (4)

| HS | Product | Wave | Implementation | China share |
|---|---|---|---|---|
| 2504 | Natural graphite | 2 | Dec 1, 2023 | ~65% mine, ~90% processing |
| 8110 | Antimony metal | 3 | Sep 15, 2024 | ~48% mine, ~70% processing |
| 8106 | Bismuth metal | 4 | Feb 4, 2025 | ~60% |
| 284180 | Tungstates (APT) | 4 | Feb 4, 2025 | ~85% |

HS 261710 antimony ores and concentrates is legally clean but sparse. Keep it
as a secondary upstream antimony case unless later coverage and diagnostics
support a stronger role.

#### Partial, bundled, and scope-contaminated treated cases

| HS | Product | Wave | Scope status | Reason |
|---|---|---|---|---|
| 811292 | Ga/Ge/In/V/Nb bundle | 1 | Bundled | HS bundles treated and untreated metals |
| 282560 | GeO₂/ZrO₂ | 1 | Bundled | GeO₂ controlled, ZrO₂ not |
| 282580 | Sb oxides | 3 | Partial | Only ≥99.99% purity (CN-10 2825800010) |
| 8101 | Tungsten metal | 4 | Partial | Only solid W≥97% with dimension reqs |
| 3801 | Artificial and colloidal graphite | 2 | Scope-contaminated | Some artificial or colloidal graphite may overlap graphite controls; not a clean placebo |

These products are not equivalent to clean treated products. The main model
should first use clean treated products. Partial, bundled, and
scope-contaminated cases can enter secondary specifications or case studies.
Do not estimate an unknown treated fraction from HS-6 data alone. Without
external fine-code information, the treated share and treatment effect are not
separately identified.

#### Marginal treated (2 — descriptive only)

| HS | Product | Wave | Issue |
|---|---|---|---|
| 280450 | Te + B bundle | 4 | Te controlled, B also in heading; small trade |
| 284690 | Non-cerium REE | 5 | Only Sm/Gd/Tb/Dy/Lu/Sc/Y controlled, La/Pr/Nd not |

#### Candidate controls

Closest candidates: 2615, 284170, 811221, 380130, 282530, 282520, and
282570.

Metal-family candidates: 8103, 8108, 8109, 8104, and 8105.

Broad or episode-specific candidates: 2818, 8111, 2811, 282110, 2820, 2833,
and 284610.

HS 2827 is policy-contaminated because it contains controlled germanium
tetrachloride. HS 380120 is also excluded from the main donor pool because
colloidal graphite may fall within the legal description of natural flake
graphite and its products even though that code is not printed as a reference
code. These products may be retained for descriptive diagnostics only.

Each wave receives a separately screened donor set. A candidate must be
untreated in the relevant window, have adequate trade coverage, fit the
treated product before policy, and survive leave-one-donor-out checks. There is
no predetermined universal 20-product placebo pool.

### 10.2 Estimator architecture

Four wave-specific DDDs plus one staggered DiD:

#### Wave-specific DDD (×4)

For each wave $w$ with implementation date $\tau_w$:

$$E[M_{ipst}|X] = \exp[\beta_w(Treated_p \times China_s \times Post_{\tau_w}) + \text{FE}]$$

- Wave 1 (Aug 2023): Ga/Ge, treated = {811292, 282560}.
- Wave 2 (Dec 2023): graphite, treated = {2504}.
- Wave 3 (Sep 2024): strict clean baseline treated = {8110}. HS 261710 is a
  sparse upstream secondary case and HS 282580 is a partial downstream
  secondary case. Analyze antimony stages separately before any pooled result.
- Wave 4 (Feb 2025): W/Bi, clean treated = {8106, 284180}; 8101 is partial.

The first pass should estimate the clean-treated sample. Secondary estimates
may add bundled, partial, or graphite-scope products with separate scope
interactions. Those estimates answer a measurement question: whether the
HS-level response remains visible when the legal treatment covers only part of
the measured code.

Product-assignment ranks are diagnostics over the eligible wave-specific donor
set. If 20 controls survive screening, the theoretical minimum rank for one
treated product is 1/21, approximately 0.048. This does not establish random
assignment, exchangeability, statistical power, or causal validity.

#### Staggered DiD (×1)

Pool all treated and placebo products with wave-specific `post` indicators:

$$E[M_{ipst}|X] = \exp[\sum_w \beta_w(Treated_p \times China_s \times Post_{\tau_w}) + \text{FE}]$$

Any pooled assignment exercise must preserve treatment cohort and treatment
quality and use only eligible controls. The combinatorial number of possible
relabels is not evidence of statistical power.

#### Callaway-Sant'Anna

CS disaggregated ATT(g,t) is NOT viable: 1-3 treated units per cohort. CS aggregated event-study is usable as a diagnostic only.

### 10.3 Inference with the expanded product pool

Inference depends on the number of controls that survive policy, coverage, and
pre-treatment-fit screening for each wave. With `J` eligible controls, the
smallest possible rank for a single treated product is `1/(J+1)`. This is a
theoretical support limit only. It is not evidence of random assignment,
exchangeability, power, or validity. The thesis will report the eligible donor
set and leave-one-donor-out results for each wave.

### 10.4 Data requirements

- Period: 201901–202603 (87 months)
- 53 non-group reporters in the main analysis panel
- Downloader universe of 34 products x 56 reporter codes x 8 annual requests
- Policy-screened bilateral acquisition universe of 31 products
- China aggregate exports for 11 treated candidates plus HS 3801
- Download scripts updated: `download_all_gaps.py` (34 HS, 2019–March 2026), `download_china_exports.py` (13 acquisition HS codes, 2019–March 2026)
- Panel builder update: `prepare_comtrade_thesis_panel.py` PRODUCTS dict and PERIODS range

### 10.5 Products dropped

| HS | Product | Reason |
|---|---|---|
| 8102 | Molybdenum | Only missile-grade powder (Mo≥97%, ≤50μm), ~1-5% of HS-6 trade |
| 280530 | REE metals | Too diluted at HS-6 (La, Pr, Nd not controlled) |
| 380110/380190 | Synthetic graphite sub-codes | Already treated or partially treated under the 2023 graphite regime; not controls |
| 8507 | Li batteries | Announced 2025 measure was suspended before implementation; broad growth-driven heading |
| 282590 | Tungsten oxides | Controlled in Wave 4 — NOT a placebo |
| 284990 | Tungsten carbide | Controlled in Wave 4 — NOT a placebo |
| 2501 | Salt / sodium chloride / brine heading | Current downloads are incomplete and trade coverage is too sparse |

HS 282590 and HS 284990 are not conceptual placebo problems. They are treated
under Announcement No. 10/2025. They are excluded from the donor pool because
they are treated products, not because they are invalid mineral cases.

The October 2025 measures on batteries, graphite-anode materials, expanded
rare-earth items, and related extraterritorial controls are not additional
treatment cohorts in the March 2026 panel. Announcement 70/2025 suspended
Announcements 55-58 and 61-62 on November 7, 2025, before their scheduled
November 8 implementation, through November 10, 2026.

## 11. Staggered DiD Design

Different announcement and implementation dates do not by themselves justify
two treatment dates per product. Choose implementation as treatment and model
announcement as anticipation.

The acquisition universe makes a staggered design assessable, but viability
depends on how many treated cases and never-treated controls survive the
product-level audit:

- 4 cohorts (Waves 1-4), each with 1-3 treated products
- cohort-specific estimates will be imprecise when only one product is treated
- never-treated shares and weighting properties must be recomputed from the
  final estimation sample
- Callaway-Sant'Anna aggregated event-study usable as diagnostic
- CS disaggregated ATT(g,t) still NOT viable (1-3 units per cohort)

## 12. Minimum Successful Thesis

Statistical significance is not a formal requirement for a valid master's
thesis. A transparent null result can be valuable. For this project to make a
compelling positive claim, the minimum is:

1. pressure indexes built only from pre-policy data;
2. source-share PPML evidence that predicted pressure explains heterogeneous
   China-source declines;
3. margin evidence that switching pressure and compression pressure predict
   different outcomes;
4. price-wedge evidence for compression or segmentation where matched prices
   exist;
5. no decisive recent pretrend failure in the main positive case;
6. one informative contrast, null, or measurement-limited case;
7. conservative interpretation language.

The project now has preliminary evidence for parts of that positive-result
threshold. Switching pressure is clearer than compression in trade quantities,
and antimony plus bismuth show strong price-wedge support. The positive claim
is not yet final because compression remains mixed, antimony has timing and
placebo-date concerns, and tungsten/APT is weak under current evidence. The
thesis remains valid if the final conclusion is that licensing produced
heterogeneous and sometimes measurement-limited market responses.

## 13. Proposed Thesis Structure

1. **Introduction:** licensing versus binding restriction, research question,
   contribution, and findings.
2. **Institutional Background:** legal chronology, product scope, licensing
   process, and Chinese industrial context.
3. **Theory:** importer-product pressure framework and hypotheses.
4. **Data and Outcome Reconstruction:** Comtrade, prices, demand,
   concentration, and timing.
5. **Empirical Strategy:** pressure-index construction, PPML interactions,
   margin models, price wedges, timing, and inference limits.
6. **Results:** source-share effects, switching margins, compression margins,
   prices, and product contrasts.
7. **Mechanisms and Comparative Interpretation:** switching, compression,
   price segmentation, measurement-limited nulls, and demand alternatives.
8. **Robustness and Appendix Diagnostics:** alternative placebos, quantities,
   timing, Rambachan-Roth where applicable, SCM, and Synthetic DiD.
9. **Conclusion and Policy Implications:** what licensing can and cannot
   achieve, with explicit limits on external validity.

## 14. Policy Recommendations Conditional on Results

- Importing economies should distinguish announcement risk from persistent
  physical scarcity; stockpiles address the former, diversified processing
  capacity addresses the latter.
- Exposure metrics should be stage-specific. Mine share alone is inadequate
  when China dominates refining or anode processing.
- Chinese policymakers face a trade-off between short-run leverage and
  accelerating foreign substitution. Technically narrow, administratively
  credible controls may preserve leverage better than broad but weakly
  enforced licensing.
- None of these recommendations should be written as final conclusions until
  the trade, price, and policy-chronology evidence is complete.
