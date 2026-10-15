---
description: "Audit of the thesis project on 2026-10-15 and the plan to a near-final draft by 1 November 2026"
created: 2026-10-15
modified: 2026-10-15
group: structure
tags: [project, critical-minerals, thesis, audit, plan, external-review]
status: active
created_by: claude
---

# Thesis Audit 2026-10

Audit date: 15 October 2026. Scope: everything in the repository that feeds the thesis, read-only. The benchmarks are two local-only documents: Reference thesis A (a finished master thesis from the same programme, English, six chapters, about 60 pages) and Reference B (a 2022 proposal in Chinese plus the same author's final-defense slides). Nothing from either is quoted at length here.

Deadlines used throughout: checkpoint 1 on 22 October (complete skeleton), checkpoint 2 on 1 November (complete near-final draft), mid-term check on 20 November, pre-defense before 20 February 2027, external blind review submission 20 March 2027.

## 1. Executive Verdict

The research is done. The manuscript does not exist. Those two sentences describe the whole situation.

The results package of 3 July 2026 (`results/full_thesis_report/`) is complete for the four clean treated products and already contains every table the thesis needs: average effects, exposure and pressure gradients, mechanism models, price wedges, event studies, placebos, and five robustness families. The submitted proposal of 4 July 2026 is a real base text: 8,700 words of introduction, literature, framework, data, methods and preliminary results that already follow the ZJU format. But `05_draft/thesis/` has never been created, the git log shows no work between 9 July and 15 October, and the July-to-September tasks promised in the proposal's own timeline (Table 5-1) were not executed. The thesis chapters that external reviewers actually read in a 15-minute skim, namely the abstract, the results summary, the conclusions and the policy implications, are the chapters with zero words written.

Five things matter most for the next five weeks.

1. **Antimony cannot carry the headline.** The largest coefficient in the project (-86.7 percent) sits on a pre-existing decline. The quarterly placebo regressions put fake policy dates 12, 24 and 36 months before the real one, and every one of them returns a China-source decline of 57 to 67 percent at p below 0.01. The descriptive China-share series for HS 8110 falls steadily from about 0.45 in 2020 to about 0.2 by mid-2024, before the August 2024 announcement. The proposal calls this a "timing caveat". A PhD reviewer will call it a failed identification. The fix is not new analysis. It is a reclassification: antimony becomes "large decline whose timing the design cannot separate from the pre-existing trend; the price wedge is the usable evidence", and it leaves the abstract's first finding. Bismuth and graphite become the lead cases. Section 4 gives the exact wording.
2. **The switching mechanism must be shown in the model that identifies it.** Because switching and compression pressure add up to exposure by construction, the single-term RoW model that the proposal reports (Table 3-5) cannot separate switching from exposure. The joint model that can is already estimated and is in the results package. In the joint model switching holds for the pooled sample and for graphite, and disappears for antimony. Compression pressure predicts higher rest-of-world imports in Wave 4 and for tungstates, the opposite of compression. The thesis must print both specifications and frame switching as a graphite and pooled result, with price segmentation as the channel for bismuth and antimony. Section 4 has the numbers.
3. **The canonical notes contradict the submitted proposal.** `Theoretical Framework Lock.md`, `Empirical Strategy Lock.md`, `Thesis Design.md`, `Research Question.md`, `NEXT_STEPS.md` and the "Current Pressure-Design Results" block of `AGENTS.md` still describe the trade-based framework (leave-one-out non-China market strength, three pressure variants, standardized pressure summing to a separate China-decline index). The proposal and the results use the production-based framework (USGS availability, replacement feasibility, switching plus compression equals exposure). Any writing session that reads the notes first will reproduce the wrong model. Marking those notes superseded is a 30-minute job and must happen on day one. `Limitations.md` is older still and belongs to the term paper.
4. **The reproducibility chain has a silent break.** The results use 12 donor products (53 reporters times 16 products times 2 sources times 29 quarters equals the 49,184 rows the pooled model starts from). The processed estimation panel was rebuilt on 13 July with 19 donor candidates. Rerunning the pipeline today would change every number without anyone changing a line of code. The thesis must freeze the July results, list the 12 donors in an appendix, and the repository must record the freeze.
5. **Clarity is an architecture problem, not a sentence problem.** The proposal repeats the "does not identify license denial, approval probability, welfare or coercive success" disclaimer in at least nine places. Paragraphs open with context rather than claims. Three different names are used for the same object (licensing wedge, trade-binding wedge, observed binding). A skimming reviewer reads this as defensiveness. The readability blueprint in Section 6 fixes the architecture now; sentence polish waits until November.

Nothing in the design needs rethinking. The question, the framework, the estimator hierarchy and the product typology survive a hostile reading. The risk to a first-round pass is not the research. It is that the manuscript is not written, and that the antimony and mechanism claims are currently pitched one notch above what the diagnostics support.

## 2. Honest Status

### 2.1 Research done versus manuscript written

| Component | Status | Evidence |
|---|---|---|
| Trade panel, 2019-01 to 2026-03, 53 reporters | Final | `03_data/processed/`, `pressure_ppml_estimation_sample_audit.csv` |
| Clean treated set (2504, 8110, 8106, 284180) and 12 donors | Final, but see the donor-count break in 4.4 | `results/full_thesis_report/PRESSURE_INDEX_IMPORTER_PRODUCT.csv` |
| Pressure variables (E, O, A from USGS, K, switching, compression) | Final | `THEORY.md`, `SUMMARY_STATS.csv`, `DATA_AUDIT.csv` |
| Quarterly average PPML, exposure and pressure interactions | Final | `MAIN_RESULTS.csv`, 1,152 rows |
| Mechanism models (RoW, total), single-term and joint | Final | `MECHANISMS.csv` |
| Event studies and joint pretrend tests | Final for products; pooled wide-panel versions failed | `EVENT_STUDY.csv`, `REPORT_BUILD_WARNINGS.md` |
| Placebo dates (quarterly, three lags, three anchors) | Final | `PLACEBO.csv` |
| Robustness: U.S. excluded, U.S. interaction, net weight, monthly, access variants, 2024 production A, trade-A comparison | Final | `ROBUSTNESS.csv` |
| Price wedges: antimony and bismuth | Final, matched benchmarks | `PRICE_WEDGES.csv` |
| Price wedges: graphite, tungsten | Exploratory only; benchmark descriptions not archived | `PRICE_WEDGES.csv` status column |
| Tercile or high/low pressure bins, alternative pre-windows | Never run | Listed in the lock notes only |
| Event-study figures (monthly, per product) | Exist as PNG from 2 July | `03_data/output/figures/event_study_*.png` |
| Thesis manuscript `05_draft/thesis/main.tex` | Does not exist | directory absent |
| Abstract EN and CN, conclusions, policy implications, results chapter | Not written | nothing in the repository |
| Thesis-formatted tables from the results package | Not built | proposal tables cover 3 of roughly 12 needed |

### 2.2 What is final quality, draft, or missing

Final quality (reuse with light edits): the literature review (proposal Section 2, 2,481 words), the legal and policy background paragraphs (1.1.2, 2.2), the framework equations (3.2.1), the model equations (3.5), the limitations (4.3), the three result tables and their verification trail (`TABLE_FIGURE_AUDIT.md`), the research-route figure, the bibliography (58 entries, none in Chinese).

Draft quality (adapt): the research background (1.1.1, too abstract for an opening), the research problem and question (1.2, 3.1; three slightly different formulations of the question coexist), the preliminary results prose (3.6; written for a proposal, not a results chapter), the contributions (4.1, 4.2; must be rewritten after the antimony reclassification).

Missing (write from scratch): front matter in the ZJU template (Chinese cover, English cover, declaration, acknowledgements, 摘要, Abstract, lists), a policy-chronology chapter with a timeline table, descriptive statistics and figures, the full results chapter, the product typology that answers the title, conclusions, policy implications, future research, all appendices.

### 2.3 Size

The proposal body is 8,678 words: background 1,472, literature 2,481, content and methods 3,752, contributions and limitations 828, timeline 166. Reference thesis A has about 14,800 words of body text in six chapters (introduction 1.5k, literature 4.7k, theory 1.5k, design 1.3k, empirical analysis 4.8k, conclusions 1.0k), 11 tables and 4 figures, and runs to about 60 pages. The target for this thesis is 15,000 to 18,000 words of body text, 12 to 14 tables, 6 to 8 figures, and 60 to 70 pages including appendices. Roughly 55 percent of the proposal text transfers; roughly 9,000 to 11,000 words are new.

## 3. Target Table of Contents

The structure follows Reference thesis A (introduction, literature, theory, design, results, conclusions) and adds the institutional-background chapter that Chinese economics theses usually carry and that this topic needs. Reference B's final structure (绪论, 文献综述, 理论机制, 实证研究, 结论与政策建议) confirms the same spine. Effort is in focused hours. "Writing session" means a fresh session with the writing skill loaded and no other task; "mechanical" means scripting, copying, formatting.

| Section | Pages | Source material | Status | Effort |
|---|---|---|---|---|
| Front matter: Chinese cover, English cover, declaration and authorization, acknowledgements, 摘要, Abstract, contents, list of tables and figures | 8 | ZJU template structure as seen in Reference A; cover assets in `05_draft/proposal/figures/cover_assets/` | write | 3 h mechanical, 3 h writing (abstracts) |
| **1 Introduction** | 7 | | | |
| 1.1 Background: licensing controls and the heterogeneity puzzle | 2 | proposal 1.1.1 and 1.2 (cut by a third) | adapt | 2 h writing |
| 1.2 Research question and the definition of binding | 1.5 | proposal 3.1 (one formulation only) | adapt | 1 h writing |
| 1.3 Significance | 1 | proposal 1.3 | ready | 0.5 h |
| 1.4 Contributions | 1.5 | proposal 4.1 and 4.2, rewritten to the final classification | adapt | 1.5 h writing |
| 1.5 Structure of the thesis | 1 | proposal 3.7 plus a structure figure | adapt | 1 h |
| **2 China's Critical-Mineral Export Licensing Controls** | 6 | | | |
| 2.1 Legal basis of export licensing | 1.5 | proposal 1.1.2 and 2.2 first half | ready | 1 h |
| 2.2 Chronology of the four waves, 2023 to 2025 (Table 2-1, Figure 2-1 timeline) | 2 | `01_notes/Policy Chronology Audit.md`, `01_notes/Official Documents.md`, `tables/product_scope.tex` | write from notes | 3 h writing, 1 h mechanical |
| 2.3 Product scope and HS observability: clean, partial, bundled, sparse (Table 2-2) | 1.5 | proposal 3.4.2, `Theoretical Framework Lock.md` scope table (the scope table is still valid) | adapt | 1.5 h |
| 2.4 Why licensing can bind without a ban | 1 | proposal 2.2 second half | ready | 0.5 h |
| **3 Literature Review** | 8 | | | |
| 3.1 Economic statecraft and critical minerals | 2 | proposal 2.1 | ready | 0.5 h |
| 3.2 Export licensing as a trade cost | 1.5 | proposal 2.2 (parts not used in Chapter 2) | ready | 0.5 h |
| 3.3 Mineral supply chains and importer adjustment | 2 | proposal 2.3 | ready | 0.5 h |
| 3.4 Trade effects, prices and empirical methods | 2 | proposal 2.4 | ready | 0.5 h |
| 3.5 Research gap | 0.5 | proposal 2.5 | ready | 0.5 h |
| **4 Theoretical Framework and Hypotheses** | 7 | | | |
| 4.1 From legal coverage to observed binding (Figure 4-1 research route) | 1.5 | proposal 3.2.1 first paragraph, Figure 3-1 | adapt | 1 h |
| 4.2 Exposure, outside access and production availability | 2 | proposal 3.2.1 equations, `THEORY.md` | ready | 1 h |
| 4.3 Replacement feasibility, switching pressure, compression pressure | 1.5 | proposal 3.2.1, with the identity stated once and its consequence for interpretation | adapt | 1.5 h writing |
| 4.4 Hypotheses H1 to H5 and the binding typology (Table 4-1) | 2 | proposal 3.2.2; typology from `post_defense_research_strategy_report.md` Section 6 | adapt | 2 h writing |
| **5 Data and Empirical Design** | 9 | | | |
| 5.1 Trade data, sample and donor products (Table 5-1 sample; Appendix A donors) | 2 | proposal 3.4.1, `pressure_ppml_estimation_sample_audit.csv`, 12-donor list | adapt plus write | 1.5 h writing, 1 h mechanical |
| 5.2 Pressure variables and descriptive statistics (Table 5-2 variables, Table 5-3 descriptives, Figure 5-1 distributions) | 2.5 | proposal 3.3, 3.4.3, `tables/variables_outcomes.tex`, `SUMMARY_STATS.csv`, `tables/production_availability.tex` | adapt plus mechanical | 1.5 h writing, 2 h mechanical |
| 5.3 Price benchmarks (Table 5-4 pairs) | 1 | proposal 3.4.4, `PRICE_WEDGES.csv` pair audit rows | adapt | 1 h |
| 5.4 Estimating equations (5-1 to 5-6) | 2 | proposal 3.5.1 to 3.5.5 | ready, add the standardization statement | 1 h |
| 5.5 Timing, inference and robustness plan | 1.5 | proposal 3.5.6, `Empirical Strategy Lock.md` identification and inference language (still valid) | adapt | 1.5 h writing |
| **6 Empirical Results** | 16 | | | |
| 6.0 Results map: question, hypothesis, table, answer (Table 6-1) | 0.5 | new | write | 1 h |
| 6.1 Descriptive evidence (Figure 6-1 China share by product; Figure 6-2 event studies, four panels) | 2 | `pressure_china_share_over_time.png`, `event_study_hs*.png`, `EVENT_STUDY.csv` | mechanical plus write | 2 h mechanical, 1.5 h writing |
| 6.2 Average China-source response (Table 6-2) | 2 | `tables/preliminary_results.tex` row 1, `MAIN_RESULTS.csv` | adapt | 1.5 h writing |
| 6.3 Exposure and pressure gradients (Table 6-3) | 2 | `tables/preliminary_results.tex` rows 2 to 4 | adapt | 1.5 h writing |
| 6.4 Adjustment mechanisms: switching and compression, single-term and joint (Table 6-4) | 2.5 | `tables/adjustment_mechanisms.tex`, `MECHANISMS.csv` joint rows | write | 2.5 h writing, 1 h mechanical |
| 6.5 Price segmentation (Table 6-5) | 1.5 | `tables/price_diagnostics.tex`, `PRICE_WEDGES.csv` | adapt | 1 h |
| 6.6 Timing and placebo diagnostics (Table 6-6) | 2 | `EVENT_STUDY.csv` joint pretrend rows, `PLACEBO.csv` | write | 2 h writing, 1 h mechanical |
| 6.7 Robustness (Table 6-7: U.S. excluded, net weight, monthly, access variants, production A 2024) | 1.5 | `ROBUSTNESS.csv`, `MAIN_RESULTS.csv` monthly rows | write | 1.5 h writing, 1.5 h mechanical |
| 6.8 When do the controls bind? Product classification (Table 6-8) | 2 | `FULL_THESIS_EMPIRICAL_REPORT.md` Section 16, revised per Section 4 of this audit | write | 2.5 h writing |
| **7 Conclusions and Policy Implications** | 6 | | | |
| 7.1 Main findings by research question | 1.5 | new, from 6.8 | write | 1.5 h writing |
| 7.2 Policy implications for importing economies and for China | 2 | proposal 4.2, extended | write | 2 h writing |
| 7.3 Limitations | 1.5 | proposal 4.3 (the only limitations text to reuse; `Limitations.md` is obsolete) | adapt | 1 h |
| 7.4 Future research | 0.5 | new | write | 0.5 h |
| References (ZJU numbered format, English then Chinese) | 4 | `02_literature/references.bib`, `plainnat` with the numbered-label patch already in `main.tex` | mechanical, check against the guideline | 2 h |
| Appendix A Donor products and screening | 1 | `product_sample_table.csv`, `pressure_ppml_estimation_product_audit.csv` | write | 1.5 h |
| Appendix B Full regression tables with N, separation drops, fixed effects | 4 | result CSVs | mechanical | 3 h |
| Appendix C Price benchmark metadata | 1 | `PRICE_WEDGES.csv` pair audit, `03_data/price_series_policy_classification_2026-07-01.md` | mechanical | 1 h |
| Appendix D Model warnings and failed diagnostics | 1 | `MODEL_WARNINGS.txt` summary, `REPORT_BUILD_WARNINGS.md` | mechanical | 1 h |
| Appendix E USGS production availability construction | 1 | `DATA_AUDIT.csv`, `production_country_rows_used.csv` | mechanical | 1 h |

Totals: about 68 pages, roughly 45 hours of writing and 22 hours of mechanical work. That fits 16 working days at 4 to 5 hours per day, which is what the plan in Section 7 assumes.

## 4. Results Assessment

### 4.1 Solid enough for the headline

The headline is heterogeneous binding under one legal instrument, with four products that respond in four different ways. Every number below is from the preferred quarterly specification (first full post-implementation quarter, reporter-clustered standard errors, importer-product-source, importer-quarter, product-quarter and source-quarter fixed effects).

| Product | Average China-source effect | Pretrend joint p | Placebo dates | U.S. excluded | Net weight | Verdict |
|---|---|---|---|---|---|---|
| Bismuth (8106) | -74.4%, p < 0.001 | 0.32 | all three near zero, p > 0.70 | -65.7%, p < 0.001 | -77.1%, p = 0.012 | clean, strong |
| Graphite (2504) | -30.1%, p = 0.076 | 0.39 | positive and insignificant | -27.8%, p = 0.20 | -33.2%, p = 0.16 | moderate, clean timing, fades after three quarters |
| Tungstates/APT (284180) | -15.2%, p = 0.68 | 0.001 (individual leads all insignificant) | -16% to -40%, p 0.09 to 0.40 | -36.0%, p = 0.42 | -31.8%, p = 0.13 | no detectable response |
| Antimony metal (8110) | -86.7%, p < 0.001 | 0.058 | -57% to -67% at all three fake dates, p < 0.01 | -87.9%, p < 0.001 | -88.3%, p < 0.001 | large, but timing not separable from the pre-existing decline |

Three further results are solid.

- **Exposure gradient.** Higher pre-policy China exposure predicts a larger China-source decline for graphite (-0.364 per standard deviation, p < 0.001), tungstates (-0.363, p = 0.007) and the Wave 4 group (-0.492, p = 0.033); the sign is negative but imprecise for bismuth (-0.584, p = 0.12) and antimony. This is the cleanest evidence that the response is not uniform across importers and it is the first answer to the "obvious result" critique.
- **Switching in the identifying model.** In the rest-of-world import model with both pressure terms, switching pressure raises non-China imports in the pooled sample (0.231, p = 0.006) and for graphite (0.320, p = 0.010). These two cells, plus the single-term versions (0.309 and 0.342), are the switching result.
- **Price segmentation for bismuth and antimony.** The international-to-China log price wedge widens by 0.837 (about 131 percent, p < 0.001, 73 pre-months, 13 post-months) for bismuth and 0.460 (about 58 percent, p < 0.001) for antimony, with HAC(3) standard errors on matched 99.99 and 99.65 percent benchmarks.

### 4.2 Fragile, with the exact conservative framing

**Antimony timing.** Use: "Antimony metal shows the largest China-source decline in the sample, but the decline began before the August 2024 announcement. Placebo policy dates 12, 24 and 36 months earlier produce declines of similar size, and the joint pretrend test is borderline (p = 0.058). The quarterly estimate therefore measures a continuation and deepening of an existing shift away from Chinese supply, not a clean policy break. The price wedge, which opens only after implementation, is the evidence that the licensing regime itself changed market conditions." Do not use "strong disruption with timing caveat". Do not put -86.7 percent in the abstract.

**Compression.** Quantity evidence does not support compression anywhere once exposure is held fixed. Single-term total-import coefficients: graphite -0.165 (p = 0.042), bismuth -0.134 (p = 0.51), antimony +0.287, tungstates +0.441 (p < 0.001, wrong sign). Joint model: graphite -0.089 (p = 0.17), pooled -0.097 (p = 0.22). In the joint RoW model compression pressure predicts higher non-China imports for Wave 4 (0.838, p < 0.001), bismuth (0.420, p = 0.037) and tungstates (1.046). Use: "Total imports do not fall with compression pressure in any product once exposure is controlled for. Where compression pressure is high, non-China imports rise, which is consistent with switching by importers that had been most dependent on China. Compression therefore remains a plausible channel for which the trade data give no quantity support; for bismuth and antimony the price wedge is the evidence of constrained replacement."

**Source-contrast pressure gradients (D times switching, D times compression).** Switching pressure has the wrong sign for graphite (+0.191), tungstates (+0.156) and Wave 4 (+0.082), none significant. Compression pressure has the expected negative sign in every product and is significant for graphite (-0.218, p = 0.043), bismuth (-0.593, p = 0.048) and pooled (-0.240, p = 0.048). Use: "Because the two pressure terms add up to exposure, this model asks which component of exposure carries the China-source decline. The decline loads on the compression component, that is on exposed importers with low replacement feasibility." Keep this table in the main text but after the exposure gradient and before the mechanism models, and do not lead with it.

**Pooled estimates.** Pooled pretrends fail (p = 0.010) and the -36-month pooled placebo is -0.30 (p = 0.04). Use pooled rows only as a summary line in tables, never in prose claims.

**Graphite magnitude.** The effect is -30 percent at p = 0.076 and the quarterly event study shows -0.63, -0.44, -0.37, -0.21 and +0.08 over the first five post quarters. Use: "moderate and short-lived" rather than "suggestive". The descriptive China share for graphite falls sharply only in 2025, which the thesis should mention and not explain.

**Tungstates and graphite price wedges.** The tungsten benchmark is marked "assumed, description pending" and the graphite Bloomberg ticker description was never archived. Report both only in Appendix C with that status stated, and keep the main price table to antimony, bismuth and (as outside-baseline support) gallium and germanium.

**Price panel inference.** The panel difference-in-differences wedge for Wave 3 reports a pair-clustered p-value of 2e-45 with four price pairs. That number must not appear anywhere. Report HC1 standard errors and say that with three control pairs the panel estimate is descriptive support for the pair-level interrupted time series.

**Inference language.** Treatment varies at product-time; reporters are not independent policy shocks; four treated products. State this once in 5.5 and once in 7.3, present p-values as conditional on reporter clustering, and use "consistent with" for every mechanism claim.

### 4.3 Standardization is not stated anywhere in the proposal

The estimation code standardizes exposure, switching pressure and compression pressure within each estimation group using the treated cells only (`pressure_standardization_audit.csv`). The proposal equations show raw pressure and the table notes do not mention standardization. Every interaction coefficient in the thesis must be labelled "per one standard deviation of pressure among treated importer-product cells", and equation (5-2) onwards must show the tilde notation.

### 4.4 Inconsistencies between scripts, tables, notes and text

1. **Donor count.** The proposal, `README.md` and `AGENTS.md` say 12 donor candidates and 16 products. The processed panel rebuilt on 13 July (`pressure_ppml_estimation_sample_audit.csv`, `product_scope_metadata.csv`) has 19 donor candidates and 23 products. The results package used 12: HS 2615, 2811, 2818, 282520, 282530, 282570, 284170, 380130, 8103, 8108, 8111, 811221. Do not rerun `run_revised_pressure_k_prod_a.py`; freeze `results/full_thesis_report/` as the thesis source, list the 12 donors in Appendix A, and add a one-line note to `NEXT_STEPS.md` recording the freeze.
2. **Framework version.** The lock notes describe the trade-based framework; the proposal and results use the production-based one. The "Current Pressure-Design Results" block in `AGENTS.md` quotes results from the trade-based run (graphite switching interactions negative and significant) that the production-based run contradicts (graphite switching interaction +0.191). Mark the lock notes and that block as superseded by the proposal and `results/full_thesis_report/THEORY.md`.
3. **Automatic classification labels.** `FINAL_INTERPRETATION.md` and `THESIS_SUMMARY_1_PAGE.md` label antimony and tungstates "switching case" by rule; the main report overrides this by hand. Never use the automatic labels.
4. **Monthly and net-weight tables.** The full report prints an empty monthly table and "no table could be produced" for net weight. Both exist in the CSVs: monthly graphite -30.0 percent (p = 0.075), antimony -86.7, bismuth -74.3 (p < 0.001), tungstates -19.3 (p = 0.60); net weight as in the table in 4.1. Both are supportive and belong in Table 6-7.
5. **Pretrend p for antimony.** `Post-Defense Thesis Plan.md` quotes 0.046 and 0.058; the results package has 0.058 under the preferred anchor. Use 0.058.
6. **Event-study figures.** The PNGs in `03_data/output/figures/` are monthly, dated 2 July, and come from `estimate_pressure_timing_robustness.py`, which predates the production-based run. The average event study does not depend on the pressure variant, and the donor pool was the same 12 products on that date, so they are reusable, but the thesis figures should be regenerated from `EVENT_STUDY.csv` quarterly rows in one consistent style so that the figure and the table in 6.6 agree.
7. **Research question wording.** The proposal uses three formulations (1.2, 3.1, and the dossier's "why do formally similar..."). The thesis uses one, in 1.2, and repeats it verbatim in 6.0 and 7.1.
8. **Timeline table.** Proposal Table 5-1 promised manuscript work for July to September. It does not go into the thesis.
9. **`Limitations.md`.** Written for the term paper (rare earths excluded for lack of data, data to December 2024, graphite exporter break as the strongest result). Do not reuse; proposal Section 4.3 is the current limitations text.
10. **Vocabulary drift.** "Licensing wedge", "trade-binding wedge", "observed binding", "disruption", "outside options", "outside access", "exposed demand", "raw China pressure" all appear. Section 6 fixes the list.

### 4.5 Closed list of remaining empirical work

No new estimation is needed for a first-round pass. Three presentation changes, all from existing output:

1. Print the joint RoW and total-import models next to the single-term models (Table 6-4). Justification: the identity switching plus compression equals exposure makes the single-term model uninterpretable as a mechanism test, and a reviewer who notices will stop reading.
2. Report price-wedge inference with HAC(3) for pairs and HC1 for the panel; drop pair-clustered p-values. Justification: four clusters.
3. Add the antimony placebo rows and the China-share figure to the main text (6.6 and 6.1). Justification: a reviewer who finds the pre-trend themselves after the thesis hid it will fail the thesis; one who is shown it will accept the reclassification.

One optional item, only if the supervisor asks: tercile pressure bins as a transparency check on the linear interactions. It was planned in the lock notes and never run. It is a half-day job with `run_revised_pressure_k_prod_a.py` as the template, but it would have to be run on the frozen 12-donor panel, which means rebuilding that panel first. Recommendation: do not run it before 20 November.

## 5. External-Review Risk Register

Ranked by the probability that a skimming PhD reviewer raises it multiplied by the damage if unanswered.

| Rank | Objection as the reviewer would write it | Fix | Where |
|---|---|---|---|
| 1 | "The antimony result is a pre-trend. Figure shows China share falling since 2020." | Reclassify as in 4.2; show the placebo table and the China-share figure; move antimony out of the abstract's first finding | 6.1, 6.6, 6.8, Abstract, 7.1 |
| 2 | "Export restrictions reduce exports. Obvious." (defense critique a) | First paragraph of 1.1 states the puzzle in two sentences: one legal instrument, four products, responses from -74 percent to zero; the thesis explains the spread with pre-policy exposure and replacement feasibility. Typology table 6-8 and the results map 6-0 make it visible on any page | 1.1, Abstract, 6-0, 6-8, 7.1 |
| 3 | "You explain Comtrade with Comtrade." (defense critique b) | One paragraph in 4.2 titled by its claim: exposure and outside access are pre-policy importer primitives, product availability is USGS production; none is a post-policy outcome. Repeat in 5.2 in one sentence; acknowledge in 7.3 that E and O are trade-based | 4.2, 5.2, 7.3 |
| 4 | "Descriptive. Does not say when controls bind." (defense critique c) | The exposure gradient, the pressure interactions and the mechanism models are the answer; Table 6-8 states for each product the condition under which binding was observed | 6.3, 6.4, 6.8 |
| 5 | "Four treated products, reporter clustering, few shocks." | 5.5 states the assignment level and that reporter clustering is conditional; p-values presented as such; no "causal effect of Chinese export controls" phrase anywhere | 5.5, 7.3, every table note |
| 6 | "Switching and compression pressure add to exposure; the single-term mechanism model does not identify switching." | Table 6-4 shows both specifications; 4.3 states the identity and 6.4 interprets the joint model | 4.3, 6.4 |
| 7 | "Compression pressure predicts higher RoW imports. Your theory is contradicted." | Say so, in 6.4, with the framing in 4.2 of this audit; keep compression as an unsupported quantity channel and a price-supported one | 6.4, 6.8, 7.1 |
| 8 | "Price wedges are not causal and the benchmarks may not match." | Core pairs only in the main table; Appendix C metadata; "consistent with segmentation"; HAC and HC1 inference only | 5.3, 6.5, Appendix C |
| 9 | "Where are gallium, germanium and rare earths? The title says critical minerals." | 2.3 explains the clean, partial, bundled, sparse hierarchy and why Ga/Ge HS codes cannot carry the baseline; Ga/Ge price wedges reported as outside-baseline support; rare earths excluded by date and scope in one sentence | 2.3, 6.5, 7.4 |
| 10 | "Graphite is -30 percent at p = 0.076 and fades." | Call it moderate and short-lived; show the event study; do not count it as strong in the abstract | 6.1, 6.2, Abstract |
| 11 | "Pooled pretrends fail." | Pooled rows as summary only; one sentence in 6.2 | 6.2, 6.6 |
| 12 | "PPML separation drops 15 percent of observations; 780 missing pressure cells." | N and separation drops in every table; Appendix D | all tables, Appendix D |
| 13 | "Staggered treatment, TWFE problems." | Wave-specific estimation; no pooled dynamic claim; one paragraph in 5.5 citing the staggered-DiD literature already in the bibliography | 5.5 |
| 14 | "December 2024 U.S.-destination controls confound Waves 3 and 4." | U.S.-excluded column in Table 6-7; U.S. interaction (pooled D_US = +0.43, p = 0.005, so the U.S. response is smaller, not larger) in Appendix B | 6.7, Appendix B |
| 15 | "Prose is dense and defensive; cannot find the claim." | Section 6 blueprint | everywhere |
| 16 | "The Chinese abstract reads like a translation." | Terminology list with fixed Chinese terms; native-speaker check in November | 摘要 |
| 17 | "Format does not follow the ZJU template." | Front matter copied from the template structure; tables three-line and full width; numbering by chapter; references in the numbered ZJU style | front matter, all |

### 5.1 Abstract, English (draft, about 320 words)

> China's recent critical-mineral export controls are licensing requirements, not bans. The same legal instrument was applied to natural graphite in December 2023, antimony in September 2024, and bismuth and tungsten compounds in February 2025, yet the trade responses differ sharply. This thesis asks when such controls bind in international trade and through which margin importers adjust.
>
> The thesis separates legal coverage from observed binding. A control is treated as binding when imports from China fall after the expected import-effect quarter relative to non-China sourcing and untreated products. It then explains where binding appears with a pressure framework built from pre-policy data: an importer's China exposure, its revealed access to non-China suppliers, and the product's non-China production availability measured from USGS production statistics. Exposure with feasible replacement generates switching pressure; exposure without feasible replacement generates compression pressure.
>
> The data are monthly UN Comtrade imports for 53 reporting economies, four clean treated products and twelve untreated comparison products from January 2019 to March 2026, aggregated to quarters and estimated with Poisson pseudo-maximum likelihood with importer-product-source, importer-time, product-time and source-time fixed effects, complemented by matched international and Chinese domestic price benchmarks.
>
> Three findings follow. First, binding is heterogeneous: imports from China fell by about three quarters for bismuth and about one third for graphite, show no detectable response for tungstates, and for antimony continue a decline that began before the control. Second, the China-source decline is larger where importers were more exposed to China before the policy, and the switching channel is visible for graphite and in the pooled sample, where switching pressure raises imports from other suppliers. Third, compression is not visible in trade quantities, but international prices rose relative to Chinese domestic prices by about 130 percent for bismuth and 60 percent for antimony, consistent with price segmentation where replacement is hard.
>
> The results imply that export licensing binds where exposed importers lack feasible replacement, and that the observed margin is more often supplier switching or price segmentation than import collapse.
>
> Keywords: export controls; critical minerals; export licensing; PPML; supplier switching; price segmentation

### 5.2 Abstract, Chinese (draft, to be checked by a native speaker)

> 中国近年对关键矿产实施的出口管制采取许可证管理而非禁运。同一法律工具先后适用于天然石墨（2023年12月）、锑（2024年9月）以及铋和钨制品（2025年2月），但贸易反应差异显著。本文研究此类出口管制何时在国际贸易中形成实际约束，以及进口方通过何种渠道进行调整。
>
> 本文区分法律覆盖与可观测约束：当受管制产品自中国的进口在预期生效季度之后相对于非中国来源和未受管制产品出现下降时，视为管制形成约束。本文进一步利用政策前数据构建压力框架解释约束出现的条件：进口方对华依赖度、已有的非中国采购渠道，以及基于美国地质调查局产量数据度量的中国以外产量可得性。依赖度与可行替代相结合形成转移压力，依赖度与不可行替代相结合形成压缩压力。
>
> 数据为联合国商品贸易数据库2019年1月至2026年3月53个报告经济体的月度进口数据，包含四种清洁处理产品和十二种对照产品，按季度加总并采用含进口方—产品—来源、进口方—时间、产品—时间和来源—时间固定效应的泊松伪极大似然估计，并辅以匹配的国际与中国国内价格基准。
>
> 研究发现：第一，约束具有异质性，铋自中国进口下降约四分之三，石墨下降约三分之一，钨酸盐无可检测反应，锑的下降延续了管制前已存在的趋势；第二，政策前对华依赖度越高，自中国进口下降越大，石墨及合并样本中转移压力显著提高了自其他供应方的进口；第三，贸易数量中未观察到压缩，但铋和锑的国际价格相对中国国内价格分别上升约130%和60%，与替代困难条件下的价格分割一致。
>
> 结论表明，出口许可证管制在依赖中国且缺乏可行替代的进口方处形成约束，其可观测的调整渠道更多表现为供应来源转移或价格分割，而非进口崩溃。
>
> 关键词：出口管制；关键矿产；出口许可证；泊松伪极大似然；供应来源转移；价格分割

### 5.3 Chapter openings (first paragraph of each chapter, draft)

Each opening states the chapter's claim in the first sentence and its route in the second.

- **1 Introduction.** China's export-licensing controls on critical minerals are the same legal instrument applied to different minerals, but the trade response ranges from a three-quarters fall in imports from China to no detectable change. This thesis explains that spread with conditions that can be measured before each control takes effect: how dependent an importer was on China, whether it already bought from other suppliers, and whether non-China production existed at scale.
- **2 China's Critical-Mineral Export Licensing Controls.** The controls studied here are authorizations, not prohibitions, and their timing, product scope and customs codes determine what trade data can show. This chapter reconstructs the legal basis and the four waves of 2023 to 2025 and classifies each controlled product by how cleanly its HS code records the controlled item.
- **3 Literature Review.** Existing work explains why concentrated supply chains give leverage, why licensing acts as a trade cost, and how trade data should be analyzed, but it does not say when a licensing rule becomes visible in trade. This chapter reviews four literatures and locates that gap.
- **4 Theoretical Framework and Hypotheses.** Legal coverage becomes observed binding only where importers were exposed to Chinese supply and replacement was limited. This chapter defines exposure, outside access, production availability and replacement feasibility, combines them into switching pressure and compression pressure, and derives five testable predictions.
- **5 Data and Empirical Design.** The design compares imports from China with imports from other sources, treated products with untreated products, and quarters after implementation with quarters before, and then asks whether pre-policy pressure predicts where the China-source decline appears. This chapter documents the trade panel, the pressure variables, the price benchmarks and the estimating equations.
- **6 Empirical Results.** The controls bound in bismuth and graphite, not in tungstates, and in antimony only as the continuation of an earlier decline; where they bound, the decline was concentrated among exposed importers and absorbed by supplier switching or by price segmentation rather than by import compression. The chapter reports descriptive evidence, average effects, pressure gradients, mechanism models, price wedges, timing diagnostics and robustness, and closes with a product classification that answers the research question.
- **7 Conclusions and Policy Implications.** Export licensing binds where exposed importers lack feasible replacement, and the margin that absorbs it is more often switching or price segmentation than import collapse. This chapter restates the findings by research question, draws implications for importing economies and for the design of China's controls, and states the limits of the evidence.

### 5.4 How the defense critiques are answered, and whether the answer is visible

| Critique (June 2026) | Answer in the thesis | Visible to a skimmer? | Action |
|---|---|---|---|
| (a) Obvious result | Heterogeneity is the object; exposure gradient and typology | Only if the first paragraph of Chapter 1, the abstract's first finding and Table 6-8 all say it | Write all three to the same sentence; put Table 6-8 on its own page |
| (b) Comtrade explains Comtrade | USGS production availability inside replacement feasibility | Not yet: the proposal mentions USGS in 3.4.3 but never names the critique | Add the claim-titled paragraph in 4.2 and the sentence in 5.2 |
| (c) Descriptive, does not answer when | Pressure interactions, mechanism models, classification | Partly: the proposal's Table 3-4 shows it but the prose around it hedges | Lead 6.3 with the exposure gradient; Table 6-8 column "condition under which binding was observed" |

The proposal answers all three in substance. None of the answers is visible on a 15-minute skim, because the proposal never names the objection it is answering and buries the answer under disclaimers. The thesis should name each objection once, in 1.4 (contributions), in one sentence each.

## 6. Readability Blueprint

### 6.1 Section-opening pattern

Every numbered section opens with the same three moves: the claim or purpose in sentence one; what evidence or steps the section uses in sentence two; and, for results sections, the one-line takeaway repeated as the last sentence before the next heading. No section opens with history, literature or a definition. Subsections of the results chapter open with the takeaway of their table: "Imports from China fell for bismuth and graphite, not for tungstates (Table 6-2)."

### 6.2 Terminology list

One term per concept, used identically in text, tables, figures, abstract and 摘要. The symbol column is the only notation allowed in equations.

| Term (use this) | Symbol | Chinese | Do not use |
|---|---|---|---|
| legal coverage | | 法律覆盖 | legal licensing, legal treatment |
| observed binding | | 可观测约束 | trade binding, trade-binding wedge, licensing wedge, disruption |
| China-source decline | β, D | 自中国进口下降 | China-source response, China source effect (as a concept) |
| China exposure | E | 对华依赖度 | China dependence, raw China pressure, P^X |
| outside access | O | 非中国采购渠道 | outside options, revealed access, capacity access (in prose) |
| production availability | A | 中国以外产量可得性 | external availability, outside-market strength |
| replacement feasibility | K | 替代可行性 | replacement rigidity |
| switching pressure | P^S | 转移压力 | switchable exposed demand |
| compression pressure | P^C | 压缩压力 | non-switchable exposed demand |
| supplier switching | | 供应来源转移 | substitution, rerouting, diversification |
| import compression | | 进口压缩 | contraction, collapse |
| price segmentation | | 价格分割 | scarcity premium, decoupling |
| clean treated product | | 清洁处理产品 | clean baseline product |
| donor product | | 对照产品 | control product, placebo product, untreated comparison product |
| first full post-implementation quarter | | 生效后首个完整季度 | main post quarter |
| import-effect month | | 预期进口影响月 | importer-arrival month |
| exposure gradient | θ_E | 依赖度梯度 | exposure interaction, heterogeneity term |

Drop P^X entirely. Drop "wedge" except in "price wedge". The word "disruption" is banned. "Robust" means a specific check passed, never "good".

### 6.3 Table and figure rule

- Caption states what is estimated and on which sample, in one line: "Table 6-2 Average China-source decline after implementation, four clean treated products, quarterly PPML".
- The first sentence of the notes is the takeaway, marked "Takeaway:". The text that introduces the table repeats that sentence.
- Product columns always in the order graphite, antimony, bismuth, tungstates (policy chronology), with HS codes in the header.
- Every regression table reports coefficient, t-statistic in parentheses, stars, N used, observations dropped by separation, fixed effects, clustering, and "pressure standardized per one SD among treated cells" where relevant.
- Pooled rows, when present, come last and are labelled "summary only; pooled pretrends fail".
- Figures have a title that states the result ("China's share of bismuth imports fell after February 2025"), dashed lines for announcement and implementation, the same product order, and a source line in the ZJU caption style.
- Nothing in the main text is a table that a reader must decode; raw coefficient dumps go to Appendix B.

### 6.4 Results-to-question map (Table 6-0 and 7.1)

| Question | Hypothesis | Table or figure | Answer in one line |
|---|---|---|---|
| RQ1 Did imports from China fall after the controls, and for which products? | H1 | 6-2, Figure 6-2 | Yes for bismuth and graphite; no for tungstates; antimony continues a prior decline |
| RQ2 Is the decline larger where exposure was higher, and do exposed importers switch or compress? | H2, H3, H4 | 6-3, 6-4 | Larger with exposure; switching visible for graphite and pooled; compression not visible in quantities |
| RQ3 Do price wedges widen where replacement is hard? | H5 | 6-5 | Yes for bismuth and antimony; not for graphite |
| Title: when do the controls bind? | all | 6-8 | Where exposed importers lack feasible replacement, through switching or price segmentation |

### 6.5 Paragraph rule

Claim in the first sentence. One idea per paragraph, 60 to 120 words. One hedge per paragraph at most. The disclaimer that the design does not identify license denials, approval rates, welfare or coercive success appears exactly twice: in 1.2 where binding is defined and in 7.3. Every other occurrence is deleted. Equations are introduced by a sentence that says what the equation measures, and followed by one sentence per symbol that is new.

### 6.6 Before and after

Before (proposal 3.6.1, as submitted):

> The preferred preliminary evidence starts with quarterly PPML estimates using the first full quarter after implementation timing anchor. Table 3-4 reports the average China source response and the China source pressure specifications by product. Antimony metal and bismuth metal have the strongest average declines in imports from China. Natural graphite is negative but weaker. Tungstates/APT are weak or null in the average China source row.
>
> The pressure rows are useful because they ask whether observed declines are stronger where the framework predicts more exposure or harder replacement. Natural graphite has a negative China exposure coefficient and a negative compression pressure coefficient. Bismuth has a negative compression pressure coefficient, but the broader quantity mechanism evidence is less precise. Tungstates/APT show a negative exposure coefficient but do not show a persuasive average decline, so the pressure row is not treated as a positive product case. The pooled clean estimate is negative, but because pooled pretrends fail, it is used only as summary evidence. Interpretation rests on the product results.

After (thesis 6.2 and 6.3, same content, same numbers):

> Imports from China fell after implementation for bismuth and graphite but not for tungstates (Table 6-2). Bismuth imports from China fell by 74 percent in the quarters after February 2025 (p < 0.001) and graphite imports by 30 percent after December 2023 (p = 0.076). Tungstates show a 15 percent decline that is indistinguishable from zero. Antimony shows the largest decline, 87 percent, but Section 6.6 shows that it continues a fall that began two years before the control. The pooled estimate is negative and large; it is reported for completeness only because pooled pretrends fail.
>
> The decline is concentrated among importers that depended on China before the policy (Table 6-3). A one standard deviation higher pre-policy China exposure deepens the China-source decline by 0.36 log points for graphite (p < 0.001) and for tungstates (p = 0.007), and by 0.58 for bismuth with less precision (p = 0.12). The decline also loads on the compression component of exposure, that is on exposed importers with low replacement feasibility, for graphite, bismuth and the pooled sample. Whether those importers switched suppliers or cut imports is the question of Section 6.4.

The rewrite is shorter, every paragraph starts with its claim, the numbers are in the prose where the reader needs them, and the hedges that remain are specific.

## 7. Work Plan

Sixteen working days from 16 October to 1 November, four to five focused hours each. "W" marks a task that needs a fresh writing-focused session with the writing skill loaded and this audit plus the proposal as the only inputs. "M" marks mechanical work that can run in any session. Every day ends with `tectonic main.tex` compiling and a commit on `main`.

### Block 0: Housekeeping and skeleton, 16 to 17 October

| Day | Task | Type | Done when |
|---|---|---|---|
| 16 Oct | Add a "Superseded on 2026-10-16 by the submitted proposal and results/full_thesis_report/THEORY.md" header to `Theoretical Framework Lock.md`, `Empirical Strategy Lock.md`, `Thesis Design.md` Section 4 and 6, `Research Question.md`, `Limitations.md`; replace the "Current Pressure-Design Results" block in `AGENTS.md` with a pointer to the frozen results package; add the results freeze and the 12-donor list to `NEXT_STEPS.md` | M | notes no longer contradict the proposal |
| 16 Oct | Create `05_draft/thesis/` with `main.tex` (preamble copied from the proposal, `\documentclass{report}` or chapter-level sectioning so that headings read 1, 1.1, 1.1.1), one file per chapter under `chapters/`, `tables/`, `figures/`, and the ZJU front matter in the order of the template: Chinese cover, English cover, declaration and authorization page, acknowledgements, 摘要, Abstract, contents, list of figures and tables. Compile with Tectonic. Update `make_overleaf_copy.py` or copy it for the thesis | M | PDF compiles with all headings and placeholder text |
| 17 Oct | Write `04_scripts/build_thesis_tables.py`: reads `results/full_thesis_report/*.csv` and writes `05_draft/thesis/tables/*.tex` for Tables 5-3, 6-2 to 6-7 and Appendix B, using the three-line `tabularx` style of the proposal tables and the `\estcell` macro; stars from p-values; N and separation drops in every table. Write `04_scripts/build_thesis_figures.py`: China-share panel for the four clean products from the processed panel, quarterly event-study plots for the four products from `EVENT_STUDY.csv`, pressure distributions from `PRESSURE_INDEX_IMPORTER_PRODUCT.csv`, one consistent style, 13.5 by 9 cm | M | every table and figure in the TOC exists as a file and is included |

### Block 1: Chapters 1 to 5 from the proposal, 18 to 21 October

| Day | Task | Type |
|---|---|---|
| 18 Oct | Chapter 1: split proposal 1.1 to 1.3 and 3.1 into 1.1 to 1.5; write the new opening paragraph; one research question; contributions rewritten to the Section 4 classification; naming the three defense critiques once each in 1.4 | W |
| 19 Oct | Chapter 2: legal basis from 1.1.2 and 2.2; chronology table and timeline figure from `Policy Chronology Audit.md` and `Official Documents.md`; scope table; "licensing without a ban" | W |
| 19 Oct | Chapter 3: paste proposal Section 2 with the five openings rewritten to the pattern; remove paragraphs now in Chapter 2 | W, short |
| 20 Oct | Chapter 4: framework from 3.2.1 with the identity stated once, the "why pressure is not an outcome" paragraph, hypotheses and typology table | W |
| 21 Oct | Chapter 5: data, sample, donors, descriptive statistics, price pairs, equations with tilde notation and standardization statement, timing and inference | W |
| 21 Oct | Insert all generated tables and figures into Chapter 6 with `[[GAP: ...]]` markers for prose; write the results map Table 6-0; appendices A, C, D, E from the CSVs | M |

### Checkpoint 1: 22 October

Complete skeleton: chapters 1 to 5 adapted, Chapter 6 with all tables and figures and gap markers, Chapter 7 headings, front matter placeholders, references compiling, PDF building with Tectonic, Overleaf copy generated. Self-review against the TOC in Section 3; list every gap in `05_draft/thesis/GAPS.md`. Commit and push.

### Block 2: Results and conclusions, 23 to 28 October

| Day | Task | Type |
|---|---|---|
| 23 Oct | 6.1 descriptive evidence and 6.2 average response | W |
| 24 Oct | 6.3 gradients and 6.4 mechanisms (both specifications; the compression paragraph exactly as framed in 4.2 of this audit) | W |
| 25 Oct | 6.5 prices, 6.6 timing and placebos (antimony paragraph exactly as framed), 6.7 robustness | W |
| 26 Oct | 6.8 product classification and Table 6-8; then 7.1 findings by question | W |
| 27 Oct | 7.2 policy implications, 7.3 limitations from proposal 4.3, 7.4 future research | W |
| 28 Oct | Abstract EN and 摘要 from the drafts in 5.1 and 5.2, updated to the final numbers; keywords; acknowledgements placeholder; structure figure for 1.5 | W |

### Block 3: Consistency and the skim test, 29 October to 1 November

| Day | Task | Type |
|---|---|---|
| 29 Oct | Number check: a script that greps every percentage and p-value in the chapter files and matches it to the CSVs; terminology grep against the banned list in 6.2; count occurrences of the disclaimer (target: two); verify every table has a "Takeaway:" line; verify figure and table numbering by chapter | M |
| 30 Oct | References in the ZJU numbered format (English first, alphabetical; [J], [M], [R], [EB/OL] codes); check that each of the 58 entries has complete fields; confirm the `plainnat` label patch produces the required style or switch to a custom `.bst` | M |
| 30 Oct | The 15-minute skim test: read only the abstract, the first paragraph of every section, every table caption and takeaway, and Table 6-8, as a hostile reviewer; fix what fails | W |
| 31 Oct | Full read-through for logic and numbers; compile final PDF; regenerate the Overleaf copy; commit | W |
| 1 Nov | Checkpoint 2: near-final draft sent to the supervisor with a one-page cover note listing the three decisions in Section 8 that need their view | |

### 2 to 20 November (margin)

Supervisor feedback and iteration; native-speaker check of the 摘要 and of all Chinese terms; sentence-level polish of Chapters 1, 4, 6 and 7 against the writing skill; the mid-term check form; the optional tercile check only if requested. Reserve two days for a last read before 20 November. The ChatGPT external review happens in this window and is out of scope here.

## 8. Decisions and Questions

### 8.1 Decisions for Mario

1. **Chapter count.** Seven chapters with a separate policy-background chapter (recommended; it carries the China-economy content of the programme and the chronology table), or six chapters with the chronology inside Chapter 1. Decide before 18 October.
2. **Antimony reclassification.** Accept the framing in 4.2 and remove antimony from the abstract's first finding. The alternative, keeping "strong disruption with timing caveat", is the single largest first-round risk.
3. **Pressure-gradient table placement.** Keep the D times switching and D times compression rows in the main text after the exposure gradient (recommended), or move them to Appendix B and keep only the exposure gradient in Table 6-3.
4. **Price table scope.** Main text with antimony, bismuth, gallium and germanium (recommended), or clean baseline products only with gallium and germanium in the appendix.
5. **Tercile robustness.** Do not run before 20 November (recommended); run only if the supervisor asks.
6. **Results freeze.** Freeze `results/full_thesis_report/` as the thesis source and never rerun the pipeline on the 19-donor panel before the defense (recommended). The alternative is to rebuild the 12-donor panel so that the pipeline reproduces the frozen numbers; that is a half-day job and worth doing in November, not now.
7. **Gallium and germanium.** One paragraph in 2.3 and the price wedges as outside-baseline support (recommended); no HS-6 regression for the bundled codes in the thesis.
8. **Drop P^X.** Remove the raw China pressure object from the thesis entirely (recommended); it is identical to exposure and only adds a symbol.

### 8.2 Questions for the supervisor

1. The registered title is "When Do Critical Mineral Export Controls Bind?". May the cover carry a subtitle, or must it appear alone? Is a Chinese title required on the Chinese cover page, and who confirms the translation?
2. Is an English thesis with a Chinese 摘要 and keywords acceptable for the School of Economics, as in the earlier programme thesis used as the benchmark, and is there a page or word minimum the external reviewers expect?
3. Is a separate institutional-background chapter expected, or should the policy chronology sit inside the introduction?
4. What exactly is submitted for the 20 November mid-term check: the form only, or the form plus the draft? Is there a presentation?
5. Do external reviewers from economics schools expect Chinese-language literature in the review? The bibliography has 58 entries and none in Chinese.
6. Should the policy implications address the design of China's own controls, or stay on the importing-economy side? Section 7.2 can be written either way; the choice affects tone.
7. Is a PDF compiled from LaTeX acceptable for the pre-defense and blind review, or must the final file be in the Word template?
8. What must be removed for the blind review (acknowledgements, supervisor name, author name in headers)?
9. Does the supervisor agree with reclassifying antimony as a continuation of a pre-existing decline, given that the price wedge still supports a licensing effect?
