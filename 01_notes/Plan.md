---
description: "Phased roadmap from current repository to a defensible master's thesis"
created: 2026-06-04
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, plan, roadmap]
status: active
created_by: codex
---

# Plan

The current post-defense source of truth is `Post-Defense Thesis Plan.md`.
The intellectual design is in `Thesis Design.md`. The locked theoretical
framework is in `Theoretical Framework Lock.md`. Operational acquisition
details are in `NEXT_STEPS.md` and `03_data/DOWNLOAD_CHECKLIST.md`.

## Phase 1: Lock the Current Baseline

- [x] Audit raw Comtrade dimensions.
- [x] Build a balanced canonical source panel without dimensional duplication.
- [x] Clean and balance Eurostat CN8 for the current EU27.
- [x] Audit CEPII GeoDist and exclude non-country aggregates.
- [x] Replace HC1 log-OLS with PPML and conditional clustered inference.
- [x] Rebuild dynamic event studies with importer-arrival timing.
- [x] Run SCM and Synthetic DiD as appendix diagnostics.
- [x] Document the current non-confirmatory bilateral results.

Gate: no old triple-difference number may be used in the thesis.

## Phase 2: Complete the Planned Data

- [x] Finish term-paper antimony bilateral Comtrade downloads:
      HS 8110, HS 261710, and HS 282580 through 2026-03.
- [x] Extend established term-paper products through 2026-03:
      HS 2504, 811292, 282560, 3801, 2818, 8111, and 2811.
- [x] Audit China-export coverage for current treated products.
- [ ] Export all exact-grade domestic and international Bloomberg benchmarks.
- [ ] Add exchange rates and retain benchmark metadata.
- [ ] Download semiconductor, battery, steel, and lead-acid demand indicators.
- [ ] Build the USGS production and concentration table.
- [ ] Run the official-document research protocol and build the legal-event
      and product-code crosswalks.

Gate: do not add antimony or a price pair to a model until coverage, units,
grade, location, treatment scope, and timing are documented.

## Phase 3: Reconstruct Outcomes

- [x] Regenerate the Comtrade source panel with antimony products.
- [x] Build exporter departures, importer arrivals, source share, total demand,
      non-China trade, supplier count, and HHI.
- [ ] Verify shipping lags by cross-correlation and episode plots.
- [ ] Build exact-grade domestic-international price wedges.
- [ ] Normalize downstream demand indexes to 2019=100.
- [x] Produce data-quality tables for zeros, missing weight, reporters, and
      pre/post coverage.

Gate: every outcome in the manuscript must point to one processed file and one
generating script.

## Phase 4: Estimate the Main Results

- [x] Re-run static source-share PPML for every pre-specified term-paper case.
- [x] Re-run dynamic PPML with announcement, implementation, and arrival
      markers.
- [x] Estimate preliminary importer switching-potential split DDD.
- [x] Build \(P^S_{ip}\), \(P^C_{ip}\), and \(P^X_{ip}\) from pre-policy data.
- [x] Estimate preliminary source-share PPML with pressure interactions.
- [x] Estimate preliminary China, RoW, and total import margin models.
- [x] Estimate preliminary price-wedge models for available benchmark pairs.
- [ ] Estimate supplier-structure outcomes.
- [x] Analyze metal, ore/concentrate, and oxide antimony separately.
- [x] Evaluate recent and full pretrends before interpreting post coefficients.

Gate: identify one main outcome and estimator before writing the Results
chapter. Do not select it solely because its p-value is smallest.

## Phase 5: Rationalize Robustness

- [x] Alternative announcement, implementation, import-effect, and quarterly
      event baselines.
- [x] Value versus physical quantity complete cases for current products.
- [ ] Alternative pre-specified placebo sets.
- [ ] Exclude re-export hubs and negligible-trade reporters.
- [x] Leave-one-importer-out pressure construction and preliminary placebo-date
      checks.
- [ ] Rambachan-Roth for a compatible linear event study.
- [ ] SCM and Synthetic DiD appendix with expanded donors.
- [x] Classify HS 3801 as a special graphite scope case: exclude it from the
      clean donor pool and use it only in secondary scope diagnostics.
- [ ] Decide whether Callaway-Sant'Anna is justified by the expanded number of
      treated product cohorts.

Gate: robustness methods must address a named threat. Matrix completion and
CausalImpact remain dropped.

## Phase 6: Comparative Mechanism Assessment

- [x] Compare switching pressure and compression pressure across products and
      importers.
- [x] Test whether \(P^S_{ip}\) predicts China down, RoW up, and total stable
      or rising.
- [x] Test whether \(P^C_{ip}\) predicts China down, weak RoW replacement,
      total down, and price-wedge widening.
- [x] Test timing, adjustment margin, price wedge, and supplier
      structure.
- [ ] Test demand-cycle alternatives using predetermined indicators.
- [ ] Classify each mechanism as identified, consistent, contradicted, or not
      testable.

Gate: the non-monotonic commitment mechanism is not a core thesis model. The
current evidence supports switching more clearly than compression. Compression
should remain a price-supported or secondary mechanism unless later estimates
improve.

## Phase 7: Write the Thesis

- [ ] Introduction and exact contribution.
- [ ] Chinese institutional and industrial background.
- [ ] Importer-product pressure framework and hypotheses.
- [ ] Data and outcome reconstruction.
- [ ] Empirical design and inference limitations.
- [ ] Results.
- [ ] Mechanisms and comparative interpretation.
- [ ] Robustness and appendix diagnostics.
- [ ] Conclusion and conditional policy implications.

The current `05_draft/Paper.md` is a superseded term-paper draft. Rewrite from
the thesis design after the completed-data estimates are frozen.

## Minimum Completion Standard

The thesis must have:

1. a clean legal treatment definition;
2. pre-policy pressure indexes built without post-treatment tuning;
3. correct treatment-level inference;
4. source-share PPML evidence on pressure-predicted China-source effects;
5. margin evidence distinguishing switching from compression;
6. price-wedge evidence where matched prices exist, or a clear reason why it
   cannot be used;
7. a mechanism discussion that does not exceed the evidence;
8. complete data and code documentation.
