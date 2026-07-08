---
description: "Reduced-form licensing-wedge framework and result alignment for the term-paper panel"
created: 2026-06-16
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, model, ppml, term-paper]
status: superseded
created_by: codex
---

# Licensing Wedge Framework

Superseded note, 2026-07-01: this file records the term-paper framework and
preliminary-evidence alignment. The current thesis framework is
`Theoretical Framework Lock.md`, with the post-defense revision in
`Binding Pressure Framework Revision.md`. Do not use this file as the current
theoretical model.

This note records the current term-paper framework after extending the panel to
2019-01--2026-03 and adding antimony products. It supersedes the stronger
structural commitment-game framing for the term paper. The older commitment
model can remain a thesis-stage possibility, but the current data support a
reduced-form model more cleanly.

Proposal note, 2026-06-27: the final proposal-stage framework is now locked in
`Theoretical Framework Lock.md`. This file remains the term-paper
preliminary-evidence alignment note.

## Research Question

> When do China's licensing-based critical mineral export controls reduce
> importers' reliance on China, and how do product scope and importer adjustment
> capacity shape the observed trade response?

The question is intentionally narrower than "do export controls reduce
exports?" China's measures are licensing regimes, not automatic export bans.
The paper identifies trade-flow patterns consistent with binding licensing
wedges. It does not identify MOFCOM's enforcement intensity, license denial
probabilities, strategic intent, inventories, or welfare effects.

## Core Model

For product \(k\) and month \(t\), let \(W_{kt}\) denote the effective
China-specific licensing wedge. The wedge is latent. It summarizes possible
delay, denial risk, compliance costs, uncertainty, or reduced availability from
Chinese suppliers after an export-control measure.

The intuition is:

\[
\ln \left(\frac{M_{ikt}^{China}}{M_{ikt}^{ROW}}\right)
=
\alpha_{ik}+\lambda_t-W_{kt}+u_{ikt}.
\]

This log-ratio equation is only a conceptual expression. The empirical models
use PPML because bilateral trade contains many zeros and strong
heteroskedasticity.

The main empirical implication is:

\[
W_{kt}>0 \Rightarrow \beta_k<0
\]

where \(\beta_k\) is the coefficient on
\(China_s \times Treated_p \times Post_{kt}\) in the product-level PPML
triple-difference model.

A near-zero or positive \(\beta_k\) does not prove that the policy was
irrelevant. It means the current HS-level trade design does not detect a
negative China-source response. Possible reasons include non-binding licensing,
routine approvals, HS-code dilution, stockpiling, reclassification, offsetting
demand shocks, slow adjustment, or limited statistical power.

## Empirical Architecture

The main model is product-level PPML triple difference on the balanced
importer-product-source-month panel:

- importer \(i\);
- product \(p\);
- source \(s \in \{China, RestOfWorld\}\);
- month \(t\);
- outcome: monthly trade value in USD.

For each treated product, the stack contains that product and the three
placebos: HS 2818, HS 8111, and HS 2811. The coefficient of interest measures
whether the treated product's China-source imports changed after the control
relative to rest-of-world sourcing and relative to placebo products.

Reporter-clustered p-values are conditional diagnostics. They do not solve the
small number of product-level policy shocks. With one treated product and three
placebos, the minimum exact product-assignment p-value is 0.25.

Event studies are the main timing check. They test whether pre-period
differences are limited and whether post-control effects appear after the
expected import-effect month:

| Product group | Announcement | Implementation | Expected import effect |
|---|---:|---:|---:|
| Ga/Ge | 2023-07 | 2023-08 | 2023-09 |
| Graphite | 2023-10 | 2023-12 | 2024-01 |
| Antimony | 2024-08 | 2024-09 | 2024-10 |

## Mechanism Extension

The term paper can add importer heterogeneity as a secondary mechanism, not as
the main identifying model.

For importer \(i\) and treated product \(k\), define pre-announcement China
exposure:

\[
E_{ik}=
\frac{\sum_{t<Announce_k}M_{ikt}^{China}}
{\sum_{t<Announce_k}M_{ikt}^{China}
+\sum_{t<Announce_k}M_{ikt}^{ROW}}.
\]

Define observed pre-policy rest-of-world access:

\[
O_{ik}=
\frac{\#\{t<Announce_k:M_{ikt}^{ROW}>0\}}
{\#\{t<Announce_k\}}.
\]

Then:

\[
A_{ik}=E_{ik}\times O_{ik}.
\]

\(A_{ik}\) is a switching-potential proxy. It is not a true outside option.
It measures whether an importer was both exposed to China and had observable
pre-policy non-China sourcing. The cleanest term-paper version is a split
sample by high versus low \(A_{ik}\). An interaction model can be added only if
it is stable and easy to explain.

## Hypotheses

| Hypothesis | Prediction | Current test | Current status |
|---|---|---|---|
| H1 Binding licensing wedge | China-source imports fall relative to ROW after treatment | PPML DDD | Strong only for HS 282580; partly for HS 8110; weak for graphite; not supported for aggregate Ga/Ge |
| H2 Dynamic adjustment | Post effects appear after expected import-effect month and may strengthen | Event study | Strongest for HS 282580 |
| H3 Product heterogeneity | Effects differ across products | Cross-product comparison | Strongly supported |
| H4 Exposure-adjustment | High exposure and ROW access imply stronger switching | \(A_{ik}\) split sample | Supported for HS 282580; weakly consistent for graphite |
| H5 Substitution vs compression | China decline may be offset by ROW sourcing or total import loss | China/ROW/total diagnostics | Current aggregates point more to substitution/demand expansion than pure compression |
| H6 HS aggregation | Bundled HS codes can attenuate effects | Eurostat CN8 Ga/Ge | Useful but imprecise |
| H7 Sparse-flow fragility | Sparse products can produce extreme estimates and bad pretrends | regularity diagnostics and pretrends | Strongly relevant for HS 261710 |

## Current Result Alignment

The pipeline was rerun on 2026-06-17 with:

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

Saved result tables:

- `03_data/output/tables/thesis_ppml_results.csv`
- `03_data/output/tables/thesis_event_study_results.csv`
- `03_data/output/tables/thesis_event_pretrend_tests.csv`
- `03_data/output/tables/thesis_extended_pretrend_tests.csv`
- `03_data/output/tables/thesis_trend_break_results.csv`
- `03_data/output/tables/thesis_scm_sdid_diagnostics.csv`
- `03_data/output/tables/thesis_switching_potential_split_results.csv`
- `03_data/output/tables/thesis_switching_potential_split_pretrends.csv`
- `03_data/output/tables/thesis_switching_potential_diagnostics.csv`
- `03_data/output/tables/licensing_wedge_result_alignment.csv`
- `03_data/output/tables/licensing_wedge_regularity_diagnostics.csv`
- `03_data/output/tables/licensing_wedge_substitution_compression_diagnostics.csv`
- `03_data/output/tables/licensing_wedge_switching_potential_diagnostics.csv`

### HS 282580: Antimony Oxides

This is the central term-paper case.

- Static PPML DDD: -81.5%, reporter-clustered p = 0.0025.
- Main source-share pretrend p = 0.680.
- Extended source-share pretrend p-values remain high across anchors:
  0.580, 0.451, and 0.635.
- Event-study post effects are negative and persistent:
  - p1: -55.4%;
  - p4--p6: -71.7%;
  - p7--p12: -90.2%;
  - p13 or later: -94.6%.

This aligns best with the binding-wedge model. The raw aggregate
substitution/compression diagnostic shows China-sourced imports falling by
27.7% after the expected effect month, while rest-of-world imports rise by
315.2% and total imports rise by 135.7%. That means the current evidence fits
source switching or demand expansion better than pure import compression. The
main DDD result is still a relative China-source decline.

### HS 8110: Antimony Metal

This is supportive but not central.

- Static PPML DDD: -86.8%, reporter-clustered p < 0.001.
- Main source-share pretrend p is very small.
- Extended pretrend checks are mixed: the announcement anchor is less severe
  than the implementation and import-effect anchors, but the design is not
  clean enough to carry the causal claim.
- Event-study post effects become strongly negative later.

This is consistent with a binding wedge, but the pretrend behavior means it
should be used as supporting evidence for antimony-related disruption, not as
the main result.

### HS 261710: Antimony Ores and Concentrates

This is descriptive only.

- Static PPML DDD: -98.9%, reporter-clustered p = 0.0033.
- Main and extended pretrends fail badly.
- Pre-policy China-positive observations are only 1.9% of source-panel cells.
- Only 12 reporters have positive China imports before announcement.

The result is too sparse and unstable for a main causal claim. It is useful as
evidence that upstream antimony trade is empirically fragile.

### HS 2504: Natural Graphite

This is weakly aligned with the model.

- Static PPML DDD: -30.4%, reporter-clustered p = 0.107.
- Pretrends fail in the main and extended tests.
- The aggregate diagnostic shows China imports falling 21.1%, ROW imports
  rising 13.4%, and total imports falling 6.4%.

Graphite remains economically interesting, but it should be described as
suggestive rather than decisive in the term paper.

### HS 811292 and HS 282560: Aggregate Ga/Ge Cases

These are meaningful nulls or measurement-sensitive cases.

- HS 811292 static PPML DDD: +19.3%, p = 0.365.
- HS 282560 static PPML DDD: +17.5%, p = 0.271.
- Event and extended pretrend behavior is not clean enough to support a
  negative China-source effect.
- Eurostat CN8 estimates are negative for Ga but imprecise, positive for Ge,
  and imprecise when pooled.

These results are not failures of the framework. They reject the simple
"controlled product equals export collapse" story and support treating
licensing controls as product-specific, scope-sensitive shocks.

## Importer Switching-Potential Split

The switching-potential split uses only pre-announcement data. For each treated
product, reporters with positive pre-announcement trade are split at the median
of:

\[
A_{ik}=E_{ik}\times O_{ik}.
\]

High-\(A_{ik}\) importers had both higher China exposure and more observable
pre-policy access to rest-of-world sourcing. No-pre-trade reporters are
excluded from this mechanism test.

### Split Diagnostics

| Product | Pre-trade reporters | High A | Low A | Median A |
|---|---:|---:|---:|---:|
| HS 2504 | 53 | 26 | 27 | 0.155 |
| HS 811292 | 49 | 24 | 25 | 0.060 |
| HS 282560 | 50 | 25 | 25 | 0.157 |
| HS 8110 | 52 | 26 | 26 | 0.088 |
| HS 261710 | 34 | 12 | 22 | 0.000 |
| HS 282580 | 50 | 25 | 25 | 0.163 |

HS 261710 is again visibly fragile: 19 reporters have no pre-policy trade, and
the median switching potential is zero.

### Split-Sample DDD Results

| Product | High-A effect | High-A p | High-A pretrend p | Low-A effect | Low-A p | Low-A pretrend p | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| HS 2504 | -34.1% | 0.080 | 0.089 | +34.5% | 0.623 | 0.006 | Weak mechanism support; high-A group moves in predicted direction, but this remains suggestive |
| HS 811292 | +9.2% | 0.648 | <0.001 | +705.4% | 0.002 | <0.001 | No support; aggregate Ga/Ge remains a measurement-sensitive null |
| HS 282560 | +1.4% | 0.905 | 0.267 | +30.2% | 0.739 | <0.001 | No support; clean high-A pretrend but no negative response |
| HS 8110 | -86.8% | <0.001 | <0.001 | -64.2% | 0.243 | <0.001 | Directionally consistent but pretrends still prevent a clean mechanism claim |
| HS 261710 | -100.0% | <0.001 | 0.000 | very large positive | <0.001 | <0.001 | Not interpretable as mechanism evidence because the product is sparse and unstable |
| HS 282580 | -87.4% | <0.001 | 0.354 | +103.1% | 0.035 | 0.161 | Strong mechanism support; the negative effect is concentrated in high-A importers |

### Model Power

The switching-potential extension has real explanatory power for HS 282580.
The full-sample antimony-oxide result is not merely an average negative effect.
It is concentrated among importers that were exposed to China and had observed
pre-policy access to non-China sources:

- high-A group: -87.4%, p < 0.001, pretrend p = 0.354;
- low-A group: +103.1%, p = 0.035, pretrend p = 0.161.

This is exactly the pattern predicted by the source-switching version of the
licensing-wedge model: the China-source decline is strongest where importers
both needed to adjust and had some observed capacity to do so.

The extension weakly helps graphite. High-A graphite importers show a negative
effect (-34.1%, p = 0.080) and a less problematic pretrend than the full sample
(p = 0.089). Low-A importers do not show a negative effect and fail pretrends.
This supports describing graphite as suggestive rather than central.

The extension does not rescue aggregate Ga/Ge. HS 811292 and HS 282560 do not
show negative effects in the high-A group. HS 282560 is especially useful as a
disciplining null: the high-A group has an acceptable pretrend but no negative
response.

For antimony metal, high-A importers show the predicted negative effect, but
pretrends remain poor in both splits. The result is therefore consistent with
the model but not clean evidence for it.

For antimony ores, the split confirms the product should not be used for
mechanism claims. The high-A estimate is mechanically huge, the low-A estimate
is explosively positive, and both splits fail pretrends.

## Term-Paper Narrative

The best term-paper claim is:

> China’s critical mineral export controls should be understood as
> licensing-based China-source trade wedges rather than automatic export bans.
> A binding wedge should reduce imports from China relative to imports from the
> rest of the world. In the current panel, the strongest evidence appears for
> antimony oxides, where the source-share DDD estimate is large, negative, and
> dynamically clean. Antimony metal is supportive but weakened by pretrends;
> antimony ores are too sparse for a main claim; graphite is suggestive; and
> aggregate Ga/Ge categories show no robust detected decline. The results
> therefore support selective and heterogeneous sourcing responses, not a
> uniform export-collapse model.

## What Still Needs to Be Added

The current pipeline aligns well with H1, H2, H3, H4, H6, and H7. H4 is now
supported mainly by HS 282580 and weakly by HS 2504. It is not supported for
aggregate Ga/Ge, and it is not clean for HS 8110 or HS 261710.

Priority additions:

1. Add source-specific event plots or product-level event summaries for China,
   ROW, and total imports, especially for HS 282580.
2. Report regularity diagnostics in the results section to justify why HS
   261710 is descriptive and HS 282580 is central.

These additions are feasible with the current data and do not require
international price data.
