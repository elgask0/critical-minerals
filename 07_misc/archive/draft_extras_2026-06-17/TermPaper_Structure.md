# Term Paper Structure

Status: active structure note for the ZJU course paper.

Course: **Introduction to China's Foreign Trade and Investment**

Deadline: **June 25, 2026, 24:00 local time**

Minimum length: **5,000 words**

Recommended target: **6,000-7,000 words**

Required sections: Abstract, Keywords, Introduction, Conclusion, References.

Required references: at least 10.

File name: `FullName+StudentID`.

## Recommended Title

**When Do China's Critical-Mineral Export Controls Bind? Evidence from
Graphite, Gallium-Germanium, and Antimony**

Alternative:

**Licensing or Restriction? China's Critical-Mineral Export Controls and
Importer Sourcing from China**

Avoid titles that promise proof of coercive success, welfare effects, or
China's strategic intent. The term paper identifies trade-flow patterns
consistent with binding licensing wedges.

## Final Research Question

> When do China's licensing-based critical mineral export controls reduce
> importers' reliance on China, and how do product scope and importer
> adjustment capacity shape the observed trade response?

This question fits the current evidence. It treats China's export controls as
foreign-trade policy instruments and asks when licensing becomes a real trade
restriction rather than a legal announcement, administrative friction, or
signaling.

## Core Argument

China's recent critical-mineral measures are licensing-based export controls,
not automatic export bans. A binding licensing control should reduce imports
from China relative to imports from the rest of the world. The effect should
not be uniform across products because HS-code scope, trade regularity, product
position in the value chain, and importer adjustment capacity differ.

The current evidence supports a selective licensing-wedge interpretation:

- HS 282580, antimony oxides, is the central case. It has a large negative
  source-share DDD estimate, clean pretrends, persistent post-control event
  effects, and the mechanism is concentrated among high switching-potential
  importers.
- HS 8110, antimony metal, is supportive but not central because pretrends are
  weak.
- HS 261710, antimony ores/concentrates, is descriptive only because trade is
  sparse and unstable.
- HS 2504, natural graphite, is suggestive. The sign and heterogeneity fit the
  model, but the evidence is weaker.
- HS 811292 and HS 282560, aggregate Ga/Ge categories, show no robust negative
  China-source effect. These nulls are useful because they reject the naive
  view that every controlled product mechanically collapses.
- Eurostat CN8 Ga/Ge evidence is useful for measurement discussion but too
  imprecise to carry the main claim.

## Data and Results Scope

The final term-paper panel is complete for the current design:

- period: 2019-01 to 2026-03;
- products:
  - treated: HS 2504, 811292, 282560, 8110, 261710, 282580;
  - controls: HS 2818, 8111, 2811;
  - descriptive: HS 3801;
- source split: China and rest of world;
- primary outcome: monthly bilateral import value;
- source panel: `03_data/processed/comtrade_thesis_source_panel.csv`;
- country-product panel:
  `03_data/processed/comtrade_thesis_country_product_month.csv`.

Do not include Bloomberg/international-price DiD in the term paper. Price
wedges can be mentioned as a future thesis extension because exact
international benchmark pairs are not complete.

Canonical scripts:

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

Key result tables:

- `03_data/output/tables/thesis_ppml_results.csv`
- `03_data/output/tables/thesis_event_study_results.csv`
- `03_data/output/tables/thesis_event_pretrend_tests.csv`
- `03_data/output/tables/thesis_switching_potential_split_results.csv`
- `03_data/output/tables/thesis_switching_potential_split_pretrends.csv`
- `03_data/output/tables/thesis_switching_potential_diagnostics.csv`
- `03_data/output/tables/licensing_wedge_result_alignment.csv`
- `03_data/output/tables/licensing_wedge_regularity_diagnostics.csv`
- `03_data/output/tables/licensing_wedge_substitution_compression_diagnostics.csv`

## Safe Claims

Use these claims unless a later rerun changes the tables:

- The strongest term-paper result is HS 282580 antimony oxides:
  - full-sample source-share PPML DDD: -81.5%, p = 0.0025;
  - main pretrend p = 0.680;
  - post-event effects become strongly negative and persistent.
- The switching-potential split strengthens the HS 282580 mechanism:
  - high-A importers: -87.4%, p = 0.00019, pretrend p = 0.354;
  - low-A importers: +103.1%, p = 0.035, pretrend p = 0.161.
- Graphite is suggestive:
  - full-sample DDD: -30.4%, p = 0.107;
  - high-A split: -34.1%, p = 0.080, pretrend p = 0.089.
- Antimony metal is supportive but not clean:
  - full-sample DDD: -86.8%, p < 0.001;
  - pretrends remain problematic.
- Antimony ores/concentrates are descriptive only:
  - full-sample DDD: -98.9%, p = 0.0033;
  - sparse trade and failed pretrends make the result unsuitable for a main
    mechanism claim.
- Aggregate Ga/Ge products do not show robust negative China-source effects:
  - HS 811292: +19.3%, p = 0.365;
  - HS 282560: +17.5%, p = 0.271.
- Eurostat CN8 Ga/Ge is imprecise and should be a measurement case study, not
  the empirical spine.
- Reporter-clustered p-values are conditional diagnostics because treatment
  varies by product-time. With one treated product and three placebos, exact
  product-level inference cannot attain p < 0.25.

## Final Section Plan

### Abstract, 300-500 words

Write this last. It should state:

- policy context;
- research question;
- data and source-split PPML strategy;
- main result for antimony oxides;
- heterogeneous/null findings for graphite and Ga/Ge;
- cautious policy implication.

### Keywords

Suggested:

`China; export controls; critical minerals; foreign trade policy; antimony;
graphite; gallium; germanium; PPML; supply chains`

### 1 Introduction, 700-900 words

Purpose:

- introduce China's critical-mineral export controls as a foreign-trade policy
  instrument;
- connect the topic to US-China technology competition and supply-chain
  concentration;
- explain why licensing controls are not the same as bans;
- state the research question;
- preview the empirical strategy and main finding;
- state the contribution in course-readable language.

Opening logic:

China's 2023-2024 controls on gallium, germanium, graphite, and antimony show
how foreign-trade policy now operates inside technology competition. Because
these measures work through licensing, their market effect cannot be inferred
from the announcement alone. The empirical question is when licensing becomes a
binding source-specific trade wedge.

Avoid:

- "China weaponized minerals successfully";
- "this proves coercive effectiveness";
- "first causal estimate";
- any claim about political concessions.

### 2 Literature Review and Institutional Background, 1,300-1,700 words

This section combines the literature review and policy background. It should
not be a long descriptive chronology.

#### 2.1 Economic Statecraft, Chokepoints, and Supply Chains

Use the literature to explain:

- economic statecraft and weaponized interdependence;
- supply-chain chokepoints;
- why mineral export controls differ from tariffs, financial sanctions, and
  technology bans;
- why heterogeneous effects are theoretically expected.

#### 2.2 China's Export-Control System

Use official and academic sources to explain:

- Export Control Law;
- MOFCOM/GAC licensing;
- end-use and end-user documentation;
- official language that export controls are not export bans;
- the role of export controls in China's foreign trade governance.

#### 2.3 Policy Episodes

Use a compact table:

| Episode | Announcement | Implementation | Expected import effect | Main products |
|---|---:|---:|---:|---|
| Ga/Ge | 2023-07 | 2023-08 | 2023-09 | HS 811292, 282560 |
| Graphite | 2023-10 | 2023-12 | 2024-01 | HS 2504, 3801 |
| Antimony | 2024-08 | 2024-09 | 2024-10 | HS 8110, 261710, 282580 |

Use primary MOFCOM/GAC documents where possible.

#### 2.4 Product Scope and Market Structure

Explain why similar legal instruments can produce different trade effects:

- product scope and HS aggregation;
- value-chain position;
- regular versus sparse trade;
- Chinese market position and importer dependence;
- feasible non-China sourcing.

### 3 Analytical Framework, 700-900 words

Use the reduced-form licensing-wedge framework from:

`01_notes/Licensing Wedge Framework.md`

Core model:

\[
\ln \left(\frac{M_{ikt}^{China}}{M_{ikt}^{ROW}}\right)
=
\alpha_{ik}+\lambda_t-W_{kt}+u_{ikt}.
\]

Explain that this is intuition only. The empirical model uses PPML because
trade has zeros.

Main hypotheses:

1. A binding licensing wedge reduces China-source imports relative to rest of
   world.
2. Effects differ across products because product scope, enforcement relevance,
   value-chain stage, and measurement quality differ.
3. A clean binding-wedge case should show no strong pretrend and negative
   post-treatment event-study effects.
4. The effect should be stronger among importers with high pre-policy China
   exposure and observed rest-of-world access.
5. Sparse upstream products should be interpreted cautiously.

### 4 Data, 700-900 words

#### 4.1 UN Comtrade Source-Split Panel

Describe:

- monthly bilateral imports, 2019-01 to 2026-03;
- 53 reporters in the final balanced panel;
- China versus rest-of-world source construction;
- canonical aggregate Comtrade rows only;
- trade value as the primary outcome;
- net weight and unit value as incomplete/descriptive.

Product table:

| HS | Product | Role |
|---|---|---|
| 2504 | natural graphite | treated, suggestive |
| 811292 | Ga/Ge/In/V/Nb bundle | treated aggregate, null/measurement-sensitive |
| 282560 | GeO2/ZrO2 | treated aggregate, null/measurement-sensitive |
| 8110 | antimony metal/articles | treated, supportive |
| 261710 | antimony ores/concentrates | treated, descriptive only |
| 282580 | antimony oxides | treated, main result |
| 2818 | alumina | control |
| 8111 | manganese | control |
| 2811 | inorganic acids | control |
| 3801 | artificial/colloidal graphite | descriptive, partially treated |

#### 4.2 Eurostat CN8

Use this as a data disaggregation case:

- gallium CN8;
- germanium CN8;
- indium and vanadium CN8 controls/placebos;
- current EU27 balanced panel.

Emphasize sparsity and limited power.

#### 4.3 Switching-Potential Measures

Define:

\[
E_{ik}=
\frac{\sum_{t<Announce_k}M_{ikt}^{China}}
{\sum_{t<Announce_k}M_{ikt}^{China}
+\sum_{t<Announce_k}M_{ikt}^{ROW}}
\]

\[
O_{ik}=
\frac{\#\{t<Announce_k:M_{ikt}^{ROW}>0\}}
{\#\{t<Announce_k\}}
\]

\[
A_{ik}=E_{ik}\times O_{ik}.
\]

State that \(A_{ik}\) is observed switching potential, not a true outside
option.

### 5 Empirical Strategy, 700-900 words

#### 5.1 Descriptive Exporter ITS

Use only as supporting timing evidence:

- China-reported exports;
- implementation indicator;
- HAC standard errors with six monthly lags;
- no untreated counterfactual.

#### 5.2 PPML Source-Share Triple Difference

Use:

\[
E[M_{ipst}|X] =
\exp\left[
\beta(Treated_p \times China_s \times Post_t)
+\Gamma_{ip}+\Gamma_{is}+\Gamma_{pt}
+\Gamma_{st}+\Gamma_{ps}+\Gamma_{it}
\right].
\]

Explain:

- China versus rest-of-world source comparison;
- treated product versus controls;
- before versus after expected import-effect month;
- pairwise fixed effects absorb source-neutral demand and persistent sourcing
  differences.

#### 5.3 Event Studies

Use event-time interactions to check:

- pretrends;
- timing after expected import-effect month;
- persistence.

#### 5.4 Switching-Potential Split

Split reporters with positive pre-policy trade into high and low \(A_{ik}\).
Estimate the same DDD separately by split. This is a mechanism test, not the
main estimator.

#### 5.5 Inference Limits

State:

- reporter-clustered p-values are conditional;
- treatment varies at product-time;
- exact product-level inference is limited by only three control products;
- mechanisms are "consistent with," not directly identified.

Do not include SCM, Synthetic DiD, Matrix Completion, CausalImpact,
Callaway-Sant'Anna, or Rambachan-Roth in the term-paper main text.

### 6 Results, 1,500-1,900 words

Present in order of credibility, not chronology.

#### 6.1 Product-Level Source-Share Effects

Main table:

| Product | DDD effect | p-value | Pretrend p | Assessment |
|---|---:|---:|---:|---|
| 2504 | -30.4% | 0.107 | 0.020 | suggestive |
| 811292 | +19.3% | 0.365 | <0.001 | no aggregate negative effect |
| 282560 | +17.5% | 0.271 | 0.260 | no aggregate negative effect |
| 8110 | -86.8% | <0.001 | <0.001 | supportive, weak pretrends |
| 261710 | -98.9% | 0.003 | <0.001 | descriptive only |
| 282580 | -81.5% | 0.002 | 0.680 | central result |

#### 6.2 Main Case: Antimony Oxides

Discuss:

- static DDD;
- clean pretrends;
- event-study persistence;
- China/ROW/total diagnostic.

Important interpretation:

The aggregate diagnostic suggests source switching or demand expansion rather
than pure import compression: China falls, while ROW and total imports rise.

#### 6.3 Importer Switching-Potential Mechanism

Main table:

| Product | High-A effect | High-A pretrend p | Low-A effect | Low-A pretrend p | Interpretation |
|---|---:|---:|---:|---:|---|
| 2504 | -34.1% | 0.089 | +34.5% | 0.006 | weak support |
| 811292 | +9.2% | <0.001 | +705.4% | <0.001 | no support |
| 282560 | +1.4% | 0.267 | +30.2% | <0.001 | no support |
| 8110 | -86.8% | <0.001 | -64.2% | <0.001 | directionally consistent but not clean |
| 261710 | -100.0% | 0.000 | very large positive | <0.001 | not interpretable |
| 282580 | -87.4% | 0.354 | +103.1% | 0.161 | strong support |

Conclusion:

For antimony oxides, the negative China-source effect is concentrated among
importers that were exposed to China and had observed access to alternative
sources. This is the strongest mechanism result in the paper.

#### 6.4 Graphite, Ga/Ge, and Antimony Caveats

Explain:

- graphite fits the model weakly but is not decisive;
- aggregate Ga/Ge nulls discipline the argument;
- antimony metal supports the broader antimony story but has bad pretrends;
- antimony ores show why sparse upstream products cannot carry the claim.

#### 6.5 Eurostat CN8

Use as a short measurement case:

- CN8 improves product disaggregation;
- estimates remain imprecise;
- supports caution about HS aggregation rather than a strong Ga/Ge conclusion.

### 7 Discussion, 800-1,100 words

Interpret results through the model:

1. Licensing controls do not operate like uniform bans.
2. The strongest evidence appears where the product is measured regularly and
   the post-control source shift is concentrated among exposed importers with
   ROW access.
3. Antimony oxides fit the binding-wedge mechanism best.
4. Graphite is consistent with a weaker or noisier wedge.
5. Ga/Ge aggregate nulls show that legal treatment does not guarantee
   detectable HS-level trade disruption.
6. Sparse upstream products can produce spectacular coefficients but weak
   evidence.

Use mechanism language carefully:

- "supports" for the HS 282580 switching-potential pattern;
- "consistent with" for antimony metal and graphite;
- "not supported" for aggregate Ga/Ge;
- "not interpretable" for HS 261710 mechanism tests.

### 8 Policy Implications, 400-600 words

Keep recommendations narrow:

1. Importing economies should distinguish legal announcement risk from binding
   trade disruption.
2. Diversification strategy should be product- and value-chain-stage specific.
3. Importer exposure matters only when alternative sourcing capacity exists.
4. Stockpiles may address short customs friction, but processing capacity and
   supplier development matter for persistent restrictions.
5. China's leverage is real but not automatic; controls can also accelerate
   substitution away from China.

### 9 Conclusion, 400-600 words

Return to the course theme:

- export licensing is now part of China's foreign trade policy toolkit;
- its effect must be evaluated empirically, not inferred from announcement;
- the term paper finds selective and heterogeneous sourcing responses;
- antimony oxides provide the cleanest case;
- the paper creates the foundation for a larger thesis with prices, broader
  products, and expanded robustness.

### References

Use `02_literature/references.bib` as the only bibliography source.

Use at least 10 references from:

- economic statecraft and weaponized interdependence;
- China's export-control law and trade policy;
- critical minerals and supply chains;
- US-China technology competition;
- PPML/event-study empirical methods.

## Tables and Figures

Minimum tables:

1. Policy chronology and product scope.
2. Product mapping and role in the paper.
3. Data coverage and regularity.
4. Main PPML DDD results.
5. Event-study/pretrend summary.
6. Switching-potential split results.
7. Eurostat CN8 case-study results.

Recommended figures:

1. Product-level China versus ROW source trends for HS 282580.
2. Event-study plot for HS 282580.
3. Switching-potential comparison for HS 282580.
4. Optional compact comparison figure for graphite and Ga/Ge.

## Writing Rules

- Do not use numerical claims from `05_draft/Paper.md` unless reproduced by
  `analysis_thesis.py`.
- Do not describe reporter-clustered p-values as definitive treatment-level
  inference.
- Do not call HS 3801 a placebo.
- Do not pool antimony metal, ore, and oxide in the main analysis.
- Use "binding licensing wedge" for the conceptual model.
- Use "supports" only where the empirical pattern is clean.
- Use "consistent with" for weaker mechanisms.
- Do not claim to estimate enforcement intensity, licensing denial
  probability, inventories, or strategic intent.
- Do not promise price DiD in the term paper.

## Drafting Sequence

1. Draft Sections 3-5 from the current notes and code outputs.
2. Draft Section 6 around HS 282580 as the main result.
3. Draft Section 2 from `literature_master.md` and `Official Documents.md`.
4. Draft the Introduction after Sections 2, 3, and 6 are stable.
5. Draft Discussion, Policy Implications, and Conclusion.
6. Write the Abstract last.
7. Export to Word and format according to the course requirements.
