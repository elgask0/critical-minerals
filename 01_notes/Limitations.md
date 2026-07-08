---
description: "Known threats to identification, data constraints, and what we cannot estimate"
created: 2026-06-04
modified: 2026-06-11
group: structure
tags: [project, critical-minerals, limitations, identification]
status: active
created_by: opencode
---

# Limitations

## Identification threats

### 0. Few independent treatment clusters

**Problem**: Policy treatment is assigned by product and implementation month,
not by importer. The current PPML comparison has one treated product and three
placebo products. Fifty-three importers provide outcome variation but not 53
independent policy shocks.

**Impact**: Reporter-clustered p-values are conditional. Conventional
product-clustered standard errors are unreliable with four clusters. Exact
assignment inference has a minimum attainable p-value of 0.25.

**Mitigation**: Report product and reporter counts, use product-placebo
assignment diagnostics, expand the pre-specified placebo universe, and avoid
claiming that importer-level sample size solves product-level inference.

### 1. HS code aggregation (attenuation bias)

**Problem**: HS 811292 bundles gallium with germanium, indium, vanadium, and niobium. Only Ga and Ge were subject to export controls. Trade in In, V, Nb was unaffected. This contaminates the treatment group with untreated trade flows, pushing the estimated effect toward zero.

**Direction**: Not necessarily a simple lower bound. Untreated components can
attenuate a negative effect, but changing product composition can also change
the sign or timing.

**Mitigation**: EU CN8 data are downloaded and normalized for the current
EU27. They separate Ga, Ge, In, and V within HS 811292. The sample remains
limited to EU importers and sparse country-month flows, so it is a robustness
design rather than a replacement for the global Comtrade analysis.

### 2. Antimony short post-period and pre-existing trend

**Problem**: Chinese antimony exports were declining ~3-5%/year before the September 2024 controls, due to reserve depletion and rising domestic consumption. Parallel trends assumption is violated.

**Direction**: Biased toward finding an effect even without treatment (the declining pre-trend would be attributed to the controls).

**Mitigation**: Treat antimony as a short-run value-chain comparison. Report
exporter ITS descriptively and estimate the same PPML design only if pretrends
and zero-flow diagnostics are acceptable. Do not automatically replace DiD
with ITS and call it causal.

### 3. Treatment endogeneity

**Problem**: China's export controls are strategic, not random. They were motivated by U.S. semiconductor controls and domestic resource concerns. The timing may correlate with trade flow dynamics (e.g., China may have imposed controls when Ga demand was already falling due to the semiconductor cycle downturn).

**Direction**: Ambiguous. If controls were imposed during a demand slump, the true treatment effect is smaller than estimated (downward bias on the trade volume decline). If controls were imposed during stable demand, no bias.

**Mitigation**: Product-month and importer-month fixed effects absorb many
common shocks in the source-share PPML. Monthly downstream demand indicators
test whether product-specific demand cycles remain a plausible alternative.
Event-study timing is informative but does not by itself establish causality.

### 4. Licensing opacity

**Problem**: We observe export volumes but not which license applications were granted or denied. The export control is a licensing requirement, not an outright ban. Some exports continued post-treatment.

**Direction**: Attenuation bias — the estimated effect averages over denied licenses (large effect) and granted licenses (zero effect). The effect of a hypothetical outright ban would be larger.

**Mitigation**: None available (licensing data is not public). Acknowledge in the paper.

### 5. Anticipation effects

**Problem**: After Ga/Ge controls (Jul 2023), forward-looking importers may have anticipated graphite controls (Dec 2023) and antimony controls (Sep 2024). Anticipatory stockpiling would show up as an import spike before treatment, violating no-anticipation.

**Direction**: Biased toward zero (stockpiling before treatment partially offsets the post-treatment decline).

**Mitigation**: Test for anticipation by examining import volumes in the announcement-to-implementation window. Recode treatment at announcement date if stockpiling is detected.

## Data constraints

### 6. REE exclusion

The April 2025 REE controls are the most consequential episode (defense + clean energy applications) but are excluded from the main analysis because UN Comtrade monthly data only covers through ~December 2024. No post-treatment data exists.

**Impact**: The paper analyzes only 3 of 4 episodes. The REE exclusion means we miss the largest and most policy-relevant treatment.

**Future**: The paper can be updated when 2025 data becomes available (likely Q3 2026).

### 7. Short post-treatment windows

| Mineral | Post-treatment months | Assessment |
|---------|----------------------|-----------|
| Ga/Ge | 17 | Adequate for event study |
| Graphite | 13 | Adequate but tight |
| Antimony | ~4 | **Too short for reliable DiD** |

For antimony, 4 months of post-treatment data may not capture the equilibrium effect. The licensing regime may tighten or loosen over time.

### 8. Zero-inflation in monthly data

Many bilateral mineral trade flows are zero in specific months (small countries don't import gallium every month). Monthly data has 35-50% zeros vs. ~30% in annual data.

**Impact**: PPML handles zeros correctly but may face separation issues (perfect prediction by fixed effects). Many observations may be dropped.

**Mitigation**: Use `pyfixest.fepois` with fixed-effect separation checks and
report dropped observations. Log-one-plus OLS is a sensitivity check only.

### 9. Raw Comtrade dimensional duplication

**Problem**: The raw downloads include World rows, bilateral partners,
secondary-partner breakdowns, customs procedures, and transport modes. Summing
all records double counts trade.

**Mitigation**: Use only the canonical aggregate dimensions documented in
`Data.md`. The cleaned thesis panel validates bilateral sums against World
totals. Legacy triple-difference estimates from `analysis_final.py` are
superseded.

### 10. Bloomberg price data limitations

Bloomberg spot prices for minor metals (Ga, Ge) may be:
- Based on thin dealer markets (few transactions, wide bid-ask spreads)
- Infrequently updated (some series may be weekly rather than truly daily)
- Sourced from specific regional markets (FOB China, CIF Rotterdam) that may not reflect global equilibrium

**Impact**: Price event study estimates may be noisy.

**Mitigation**: Cross-validate with USGS annual prices. Use monthly rather than daily frequency to reduce noise.

International price comparisons also require exact product matching. Purity,
mesh size, location, incoterm, and currency must match before interpreting a
domestic-international price gap. For graphite, an exact FOB-China/CIF-Europe
pair is not currently established; exact-grade regional pairs are preferable
to mismatched Europe labels. The Rotterdam indium series has one missing month
(June 2024), which should remain missing in the primary analysis.

## What we cannot estimate

### General equilibrium effects

The paper is a partial equilibrium analysis. It estimates the direct effect on trade flows and prices but does not quantify:

- **Downstream effects** on semiconductor fabrication (Ga/Ge → GaAs wafers → chips)
- **Downstream effects** on EV battery production (graphite → anodes → batteries)
- **Downstream effects** on defense procurement (REE → magnets → precision-guided munitions)
- **Welfare effects** on importing countries (consumer surplus loss, deadweight loss)
- **Welfare effects** on China (export revenue loss, domestic producer surplus gain from lower prices)

A structural general equilibrium model (Caliendo and Parro, 2022) would be needed but is beyond the scope of a term paper.

### Heterogeneous licensing

We cannot observe whether China granted licenses differentially by importer. If the U.S. and allies faced stricter licensing while Belt and Road partners received favorable treatment, the average treatment effect masks important heterogeneity.

**Mitigation**: Test for heterogeneous effects by splitting importers into groups (U.S. and allies vs. BRI countries vs. neutral). This is exploratory.

## Honest summary

The strongest current result is the HAC-corrected exporter ITS break for
natural graphite. It is not a complete causal design. The corrected bilateral
PPML produces a directionally negative graphite estimate but does not confirm a
persistent effect with conventional inference. Ga/Ge pretrends fail, Eurostat
is sparse. The planned extension through March 2026 gives antimony 19
post-treatment calendar months, with September 2024 only partially treated.

The thesis can still succeed with transparent heterogeneous or null results.
A compelling positive causal claim requires one stable primary estimate,
consistent timing in an independent outcome, acceptable recent pretrends, and
mechanism evidence aligned with the theoretical model.
