---
description: "Key references and the gap this paper fills in the literature"
created: 2026-06-04
modified: 2026-06-04
group: structure
tags: [project, critical-minerals, literature, references]
status: active
created_by: opencode
---

# Literature

## Theoretical foundation

### Weaponized interdependence

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| Farrell and Newman (2019) "Weaponized Interdependence" *Int. Security* 44(1) | Core framework: network concentration → chokepoints → coercive leverage | Theoretical foundation. We extend to supply-side weaponization |
| Farrell and Newman (2023) "Weaponized Interdependence in the Age of Tech War" *TNSR* 6(3) | Extension to technology domain; financial and digital networks | Shows demand-side focus of existing literature |
| Bown (2020) "How the US Marched the Semiconductor Industry into Its Trade War with China" *EAER* 24(4) | Documents incremental escalation of US semiconductor controls | Demand-side weaponization case study. [[03_Garden/Sources/@bown_2020|Vault note]] |

### Economic statecraft and sanctions

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| Egger, Syropoulos, and Yotov (2024) "Analyzing the Effects of Economic Sanctions" *ROIE* 32(1) | Gravity models for sanctions; GSDB methodology | Econometric methodology. [[03_Garden/Sources/@egger_syropoulos_yotov_2024|Vault note]] |
| Hinz et al. (2022) "Sanctions and the Russian Economy" *VoxEU* | Gravity model of sanctions on Russia; trade diversion | Methodological precedent for sanctions impact quantification |
| Crozet and Hinz (2020) "Friendly Fire" *Economic Policy* 35(101) | Costs of sanctions on sanctioning countries | Framework for thinking about costs to China of its own controls |
| Felbermayr et al. (2020) "Global Sanctions Data Base" *EER* 129 | Systematic sanctions data | Data infrastructure reference |

## Econometric methodology

### Shift-share / Bartik designs

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| Goldsmith-Pinkham, Sorkin, and Swift (2020) "Bartik Instruments" *AER* 110(8) | When do shift-share designs identify causal effects? | Justifies our identification strategy |
| Borusyak, Hull, and Jaravel (2022) "Quasi-Experimental Shift-Share Research Designs" *Restud* 89(1) | Shock-level identification in shift-share | Alternative identification via exogeneity of timing |
| Adao, Kolesár, and Morales (2019) "Shift-Share Designs" *QJE* 134(4) | Inference in shift-share designs (clustered SE) | Standard errors that account for shock correlation |

### DiD methodology (staggered treatment)

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| Callaway and Sant'Anna (2021) "DiD with Multiple Time Periods" *JoE* 225(2) | Group-time ATT estimator | Reference if we use bilateral DiD as robustness |
| Sun and Abraham (2021) "Estimating Dynamic Treatment Effects" *JoE* 225(2) | Interaction-weighted estimator | Alternative estimator |
| Roth (2022) "Pretest with Caution" *AER: Insights* 4(3) | Pre-trend tests have low power | Cautions against over-reliance on pre-trend tests |
| Rambachan and Roth (2023) "A More Credible Approach to Parallel Trends" *Restud* 90(5) | Sensitivity analysis for parallel trends violations | Robustness: honest bounds on treatment effects |
| de Chaisemartin and D'Haultfoeuille (2020) "TWFE with Heterogeneous Treatment Effects" *AER* 110(9) | TWFE bias under heterogeneous effects | Why simple TWFE is insufficient |

### Gravity model and trade estimation

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| Santos Silva and Tenreyro (2006) "The Log of Gravity" *REStat* 88(4) | PPML estimator for gravity models | Justifies PPML for trade flow estimation |
| Santos Silva and Tenreyro (2011) "Further Simulation Evidence" *Economics Letters* | PPML works with many zeros | Addresses zero-inflation concern |

## Critical minerals

### Market structure and supply chains

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| International Energy Agency (2023) *Critical Minerals Market Review* | Demand growth, supply concentration, policy responses | Background data on market structure |
| U.S. Geological Survey (2024) *Mineral Commodity Summaries* | Production, trade, price data by mineral | Primary data source (annual prices) |
| Frenzel et al. (2017) "On the Current and Future Availability of Gallium" *Resources Policy* 52 | Gallium is a byproduct metal; supply inelastic | Explains why gallium supply can't quickly ramp up |
| Mancheri (2015) "World Trade in Rare Earths and Chinese Policies" | China's consolidation of REE supply chain | Historical precedent for China's mineral dominance |
| Golev et al. (2014) "Rare Earths Supply Chains" *Resources Policy* 41 | Post-2010 diversification efforts | Shows "use it or lose it" dynamic in weaponized interdependence |

### Policy responses

| Reference | Contribution | Relevance |
|-----------|-------------|-----------|
| European Commission (2023) *Critical Raw Materials Act* | EU diversification targets | Policy context |
| Department of Energy (2024) *Critical Materials Strategy* | US diversification strategy | Policy context |
| Bacchus (2024) "China's Critical Mineral Export Controls" *Cato Policy Analysis* 965 | Qualitative analysis of the controls | Most detailed policy-oriented assessment to date |
| Sanderson (2023) "China's Gallium and Germanium Controls" *FT* | Contemporary reporting | Announcement coverage |

## The gap

**No existing paper provides causal estimates of the trade flow or price effects of China's 2023-2025 critical mineral export controls.** The literature covers:

1. **Demand-side weaponization** (US semiconductor controls) — extensively studied
2. **Qualitative commentary** on China's mineral controls — no causal inference
3. **Historical case** (2010 rare earth dispute) — single event, no systematic comparison
4. **Supply chain concentration** — descriptive, not causal

This paper fills the gap with the first systematic quasi-experimental analysis.

## Vault cross-references

- [[03_Garden/Sources/@farrell_newman_2019|Weaponized Interdependence]]
- [[03_Garden/Sources/@bown_2020|Bown 2020 — Semiconductor Trade War]]
- [[03_Garden/Sources/@egger_syropoulos_yotov_2024|Egger et al. 2024 — Sanctions Methodology]]
- [[03_Garden/Concepts/Gravity model of trade|Gravity Model of Trade]]
- [[04_Projects/chip-war-index/_Index|Chip War Index]] — demand-side mirror of this project
