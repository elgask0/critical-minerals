---
description: "Canonical research question and testable hypotheses"
created: 2026-06-04
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, research-question, hypotheses]
status: active
created_by: codex
---

# Research Question

## Primary Question

### Term-Paper Question

> **When do China's licensing-based critical mineral export controls reduce
> importers' reliance on China, and how do product scope and importer
> adjustment capacity shape the observed trade response?**

This was the active question for the ZJU term paper and is now treated as a
preliminary-evidence version of the broader thesis question.

### Revised Thesis Question

> **When do Chinese critical-mineral export licensing controls bind, and
> through which adjustment margins?**

This is the post-defense master thesis question.

The point is not to show only that restrictions reduce trade. The thesis asks
whether pre-policy importer exposure and non-China supplier structure predict
where licensing controls produce source switching, import compression, or
price segmentation.

## Definition Of Binding

A Chinese critical-mineral licensing control is treated as binding when it
creates an observable market restriction or adjustment after the expected
import-effect month.

Binding can appear as:

- a pressure-predicted decline in China-sourced imports;
- source switching toward non-China suppliers;
- total import compression;
- widening international-China price wedges.

Binding does not mean an outright export ban, universal license denial,
observed MOFCOM approval probabilities, downstream welfare loss, or achieved
foreign-policy concession.

## Subquestions

1. **Pressure and trade:** Do importer-product pairs with higher predicted
   China-source decline pressure show larger post-policy China-source declines?
2. **Switching:** Does switching pressure predict China-source decline, RoW
   import growth, and stable or rising total imports?
3. **Compression and prices:** Does compression pressure predict China-source
   decline, weak RoW replacement, total import decline, and wider
   international-China price wedges where matched prices exist?
4. **Timing and measurement:** Do these effects appear after implementation
   or the expected import-effect window, and how do HS-code scope and trade
   regularity limit interpretation?

## Hypotheses

### H1: China-Source Pressure Hypothesis

Higher predicted China-source decline pressure should imply a larger
post-policy decline in China-sourced imports of treated products.

Primary data/test: UN Comtrade importer-product-source panel, with quarterly
PPML as the baseline and monthly PPML as robustness; source-share PPML with
interactions between treatment and pre-policy pressure indexes.

### H2: Switching Channel Hypothesis

Higher switching pressure should predict:

\[
M^C\downarrow,\qquad M^R\uparrow,\qquad M^T \text{ stable or rising}.
\]

Primary data/test: China, rest-of-world, and total import PPML margin models.

### H3: Compression And Price-Segmentation Hypothesis

Higher compression pressure should predict:

\[
M^C\downarrow,\qquad M^R \text{ weak},\qquad M^T\downarrow.
\]

Where matched prices exist, it should also predict:

\[
\Delta \pi_{pt}>0,
\qquad
\pi_{pt}=\log P^{INT}_{pt}-\log P^{CN}_{pt}.
\]

Primary data/test: margin models and matched international-China price-wedge
models.

### H4: Timing Hypothesis

Effects should appear after the policy timing, not as systematic pre-policy
declines. The quarterly baseline uses the first full post-implementation
quarter. Monthly diagnostics still report announcement, implementation, and
implementation-plus-one-month import-effect timing.

Primary data/test: quarterly event-study interactions, with monthly
announcement, implementation, and importer-arrival diagnostics reported as
timing references.

### H5: Measurement Discipline Hypothesis

Clean and regularly traded HS codes should support stronger claims than
bundled, partial, sparse, or price-unmatched products.

Primary data/test: product-specific estimates, product-scope classification,
trade-regularity diagnostics, and fine-code extensions where available.

Definitions, equations, estimators, current results, and falsification criteria
are maintained in `Theoretical Framework Lock.md`, `Empirical Strategy
Lock.md`, and `Methodology.md`.
