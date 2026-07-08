---
description: "Post-defense empirical strategy and interpretation rules"
created: 2026-06-27
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, methodology, ppml, inference, pressure-indexes]
status: active
created_by: codex
---

# Empirical Strategy Lock

This note locks the revised empirical design after the proposal-defense
feedback. The design is theory first and PPML second.

## Bottom Line

The thesis should not center on one average effect of licensing controls on
trade. The main empirical question is:

> Do pre-policy importer exposure and non-China supplier structure predict
> where Chinese critical-mineral licensing controls create source switching,
> import compression, or price segmentation?

The main trade estimator remains PPML on an importer-product-source-month
panel. Its role changes. It now tests whether the pressure indexes predict
heterogeneous China-source declines.

## Core Data Structure

Use the importer-product-source-month panel as the raw source-share data. The
preferred baseline aggregates it to quarters:

- importer \(i\);
- product \(p\);
- source group \(s\), China or rest of world;
- month \(t\);
- import value \(M_{ipst}\).

The main Comtrade importer panel uses 53 non-group reporter countries. The
raw acquisition scripts may download 56 reporter codes, but the analysis
excludes reporter code 97 (European Union), reporter code 975 (ASEAN), and
reporter code 156 (China). The first two are aggregate reporter groups. China
is the source country in the source-share design, not an importer in the main
reporter panel.

Use collapsed importer-product-month panels for mechanism outcomes:

\[
M^C_{ipt},\qquad M^R_{ipt},\qquad M^T_{ipt}.
\]

Use product-month price panels where matched prices exist:

\[
\pi_{pt}=\log P^{INT}_{pt}-\log P^{CN}_{pt}.
\]

## Pre-Policy Pressure Indexes

All pressure variables must be built from pre-policy data only.

Importer China exposure:

\[
E_{ip}=
\frac{\sum_{t<T_p^{ann}}M^C_{ipt}}
{\sum_{t<T_p^{ann}}M^C_{ipt}+\sum_{t<T_p^{ann}}M^R_{ipt}}.
\]

Importer outside access:

\[
O_{ip}=
\frac{\#\{t<T_p^{ann}:M^R_{ipt}>0\}}
{\#\{t<T_p^{ann}\}}.
\]

Leave-one-importer-out non-China outside-market strength:

\[
A^{ROW}_{-i,p}
=
Depth^{ROW}_{-i,p}(1-HHI^{ROW}_{-i,p}),
\]

where:

\[
Depth^{ROW}_{-i,p}
=
\frac{\log(1+N^{ROW}_{-i,p})}
{\log(1+N^{ROW}_{max})}.
\]

Product replacement rigidity:

\[
R_{-i,p}=1-A^{ROW}_{-i,p}.
\]

Switching pressure:

\[
P^S_{ip}=E_{ip}O_{ip}A^{ROW}_{-i,p}.
\]

Compression pressure:

\[
P^C_{ip}=E_{ip}(1-O_{ip})R_{-i,p}.
\]

China-source decline pressure:

\[
P^X_{ip}=P^S_{ip}+P^C_{ip}.
\]

Standardize \(P^S_{ip}\) and \(P^C_{ip}\) before using them in interaction
models:

\[
\widetilde P^S_{ip}
=
\frac{P^S_{ip}-\bar P^S}{sd(P^S)},
\qquad
\widetilde P^C_{ip}
=
\frac{P^C_{ip}-\bar P^C}{sd(P^C)}.
\]

## Main Source-Share PPML

Let:

\[
D_{ipst}=Treated_p\times China_s\times Post_{pt}.
\]

The average source-share model is:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_0D_{ipst}
+
\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}
].
\]

This model estimates the average China-source response. It is useful, but it
does not answer the main post-defense question by itself.

The preferred theory-guided model is:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_0D_{ipst}
+
\theta_S(D_{ipst}\times \widetilde P^S_{ip})
+
\theta_C(D_{ipst}\times \widetilde P^C_{ip})
+
\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}
].
\]

Expected signs:

\[
\theta_S<0,\qquad \theta_C<0.
\]

Interpretation:

- \(\beta_0\) is the China-source effect for an importer-product pair with
  average switching pressure and average compression pressure.
- \(\theta_S\) is the log-point change in the China-source effect for a one
  standard deviation increase in switching pressure.
- \(\theta_C\) is the log-point change in the China-source effect for a one
  standard deviation increase in compression pressure.

The predicted importer-product China-source effect is:

\[
\widehat{\beta}_{ip}
=
\widehat{\beta}_0
+
\widehat{\theta}_S\widetilde P^S_{ip}
+
\widehat{\theta}_C\widetilde P^C_{ip}.
\]

The PPML percent effect for any log coefficient \(b\) is:

\[
100(e^b-1).
\]

## Treatment-Scope Hierarchy

Estimate the main pressure-interaction model on clean treated products and
clean eligible controls first. Partial and bundled products should not carry
the main thesis result unless finer data identify the controlled subcomponent.

Main strict clean-treated set:

- 2504 natural graphite;
- 8110 antimony metal;
- 8106 bismuth metal;
- 284180 tungstates/APT.

Secondary treatment-scope cases:

- 261710, antimony ores and concentrates, legally clean but sparse;
- 811292, bundled Ga/Ge/In/V/Nb;
- 282560, bundled GeO2/ZrO2;
- 282580, partial antimony oxides because only high-purity oxides are
  controlled;
- 8101, partial tungsten metal/articles because only specified forms are
  controlled;
- 3801, special graphite scope case because artificial or colloidal graphite
  may overlap the graphite control but is not a clean untreated product.

Do not put an estimated hidden treated share directly into the baseline PPML.
For a partial product \(p\), the true treated share \(\chi_p\) and the
treatment effect are not separately identified from HS-6 trade alone. A
coefficient on a partial code is therefore an HS-level diluted response, not a
controlled-item response.

If partial products enter a secondary model, use separate scope interactions:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_{clean}D_{ipst}Clean_p
+
\beta_{partial}D_{ipst}Partial_p
+
\beta_{bundle}D_{ipst}Bundle_p
+
\beta_{gscope}D_{ipst}GraphiteScope_p
+FE
].
\]

The same split can be applied to pressure interactions only if the sample has
enough variation:

\[
D_{ipst}\times \widetilde P^S_{ip}\times Clean_p,\qquad
D_{ipst}\times \widetilde P^S_{ip}\times Partial_p,
\]

and similarly for \(\widetilde P^C_{ip}\). If the split is unstable, keep
partial and bundled products as product-level case studies.

## Mechanism Models

Raw movements in China, RoW, and total imports are not enough. Estimate the
mechanism margins with fixed effects.

For China imports:

\[
\mathbb{E}[M^C_{ipt}\mid X]
=
\exp[
\theta^C_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+
\theta^C_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+
\alpha_{ip}+\delta_{it}+\lambda_{pt}
].
\]

Expected:

\[
\theta^C_S<0,\qquad \theta^C_C<0.
\]

For rest-of-world imports:

\[
\mathbb{E}[M^R_{ipt}\mid X]
=
\exp[
\theta^R_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+
\theta^R_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+
\alpha_{ip}+\delta_{it}+\lambda_{pt}
].
\]

Expected:

\[
\theta^R_S>0,\qquad \theta^R_C\leq 0.
\]

For total imports:

\[
\mathbb{E}[M^T_{ipt}\mid X]
=
\exp[
\theta^T_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+
\theta^T_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+
\alpha_{ip}+\delta_{it}+\lambda_{pt}
].
\]

Expected:

\[
\theta^T_S\geq 0,\qquad \theta^T_C<0.
\]

The fixed effects absorb:

- \(\alpha_{ip}\): stable importer-product trade scale;
- \(\delta_{it}\): importer-month shocks, including macro demand, exchange
  rates, and importer-level disruptions;
- \(\lambda_{pt}\): product-month shocks, including global product demand,
  global price cycles, and product-specific supply shocks.

## Price-Wedge Model

Price wedges are central outcomes, not controls in the trade PPML.

Define:

\[
\pi_{pt}
=
\log P^{INT}_{pt}
-
\log P^{CN}_{pt}.
\]

Aggregate pressure to product level using pre-policy trade weights:

\[
\bar P^C_p=\sum_i w_{ip}P^C_{ip},
\qquad
\bar P^S_p=\sum_i w_{ip}P^S_{ip}.
\]

The preferred price-wedge model is:

\[
\pi_{pt}
=
\alpha_p+\tau_t
+
\rho_C(Post_{pt}\times \bar P^C_p)
+
\rho_S(Post_{pt}\times \bar P^S_p)
+
u_{pt}.
\]

Expected:

\[
\rho_C>0,\qquad \rho_S\approx 0.
\]

If the matched price panel is too small for this model, report product case
studies using the same logic:

- switching: China down, RoW up, price wedge weak;
- compression: China down, RoW weak, total down, price wedge up;
- price segmentation: trade effect weak or mixed, price wedge up.

Use price data only when grade, unit, currency, location, tax basis, and quote
convention are close enough for comparison.

## Timing

The preferred baseline is quarterly. The main post period starts in the first
full post-implementation quarter. This avoids treating transition months or
mixed implementation quarters as clean post-policy periods.

Monthly import-effect timing is still useful for robustness:

| Wave | Announcement | Implementation | Expected import effect |
|---|---|---|---|
| Gallium/germanium | 2023-07 | 2023-08 | 2023-09 |
| Graphite | 2023-10 | 2023-12 | 2024-01 |
| Antimony | 2024-08 | 2024-09 | 2024-10 |
| Tungsten/bismuth | 2025-02 | 2025-02 | 2025-03 |

Quarterly main post starts:

| Wave | Strict clean treated products | Main post quarter |
|---|---|---|
| Wave 2 graphite | 2504 | 2024Q1 |
| Wave 3 antimony | 8110 | 2024Q4 |
| Wave 4 W/Bi | 8106, 284180 | 2025Q2 |

Event studies are diagnostics for timing and persistence. Pretrend tests
should focus on pre-announcement months. Announcement and implementation
months may include anticipation, contract adjustment, shipment timing, or
stockpiling.

## Wave-Specific And Staggered Design

Estimate wave-specific models before any pooled summary. Each wave needs its
own treated set and screened donor pool.

The wave-specific source-share model is:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_w(Treated_{pw}\times China_s\times Post_{wt})
+FE
].
\]

The theory-guided wave model replaces \(\beta_w\) with pressure interactions:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_{0w}D_{ipst}
+
\theta_{Sw}(D_{ipst}\times \widetilde P^S_{ip})
+
\theta_{Cw}(D_{ipst}\times \widetilde P^C_{ip})
+FE
].
\]

A pooled staggered model can summarize all waves:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\sum_w \beta_w(Treated_{pw}\times China_s\times Post_{wt})
+FE
].
\]

But the thesis should not let the pooled coefficient hide heterogeneity. The
main interpretation should come from pressure-predicted differences across
importer-product pairs and adjustment margins.

## Identification Language

Use this assumption for the source-share design:

> Absent the licensing control, treated products would not have experienced a
> China-specific relative import-value shift at the policy timing, compared
> with untreated products, after absorbing product-month, source-month,
> importer-month, and baseline sourcing differences.

Use this assumption for the pressure interactions:

> Absent the licensing control, high-pressure and low-pressure
> importer-product pairs would not have experienced differential post-policy
> China-source shifts exactly at the policy timing, after absorbing
> importer-month and product-month shocks.

Do not write that the design simply identifies "the causal effect of Chinese
export controls." That is too broad.

## Inference Language

Treatment is assigned at product-month level, not importer level. Reporter
clusters are useful conditional diagnostics, but reporters are not independent
policy shocks. Product-level inference is limited because the number of
treated and comparison products is small.

Interpretation should rest on the joint pattern:

1. sign;
2. magnitude;
3. timing;
4. persistence;
5. pressure-predicted heterogeneity;
6. switching or compression margins;
7. price-wedge evidence where available;
8. product-scope and trade-regularity limits.

## Required Robustness

Required:

1. quarterly average source-share PPML with first full post-quarter timing;
2. pressure-interaction source-share PPML;
3. quarterly event-study timing diagnostics plus monthly timing figures;
4. quarterly China, RoW, and total import mechanism models;
5. price-wedge model or product case studies where matched prices exist;
6. frequency, capacity, and absorptive pressure variants;
7. high/low or tercile pressure groups;
8. placebo dates using the same timing hierarchy;
9. exclusion of the United States reporter, code 842;
10. optional U.S.-specific interaction for the late 2024 U.S.-destination
    policy environment;
11. net-weight complete-case robustness where coverage permits;
12. donor-pool and product-assignment diagnostics;
13. alternative HHI interpretation \(A^{ROW,alt}_{-i,p}\) if time permits;
14. alternative 12- and 24-month pre-policy windows for pressure construction.

The United States check is not part of the main identification strategy.
Importer-month fixed effects already absorb U.S.-level demand and macro
shocks, but they do not fully absorb source-specific U.S.-China shocks. The
U.S. robustness should therefore answer a narrow question: do the pressure
coefficients survive when the U.S. importer is excluded or separately flagged?

## Estimators Not Central

Do not make these the core thesis design:

- synthetic control;
- synthetic DiD;
- Callaway-Sant'Anna disaggregated ATT;
- matrix completion;
- CausalImpact;
- firm-level license-denial models;
- welfare or downstream-output models.

These can appear only as appendix diagnostics if the data support them.

## Current Evidence Status

Current results remain preliminary and thesis-design-stage. The old
term-paper result table is superseded by the pressure-design outputs.

| Case | Quarterly average PPML, first full post-quarter | Current status |
|---|---:|---|
| HS 2504 natural graphite | -30.1%, p = 0.076 | Suggestive; pressure-switching evidence is stronger than the average effect |
| HS 8110 antimony metal | -86.7%, p = 9.13e-09 | Strong average effect, but timing and placebo-date concerns remain |
| Wave 4 W/Bi | -42.4%, p = 0.021 | Supported aggregate wave result |
| HS 8106 bismuth | -74.4%, p = 0.000305 | Strong average effect and strong price-wedge support |
| HS 284180 tungstates/APT | -15.2%, p = 0.683 | Weak or informative null under the current benchmark |

Current mechanism reading:

- switching pressure is more credible than compression pressure;
- compression should be framed as a plausible channel and price-supported
  diagnostic, not as a clean trade-quantity result yet;
- price wedges strongly support antimony and bismuth segmentation;
- graphite does not currently have price-wedge support;
- tungsten/APT needs price-benchmark verification before interpretation.

See `Post-Defense Thesis Plan.md` for the current result map and next
decisions.

## Minimal Revised Proposal Structure

Use four methods parts:

1. pressure-index construction from pre-policy data;
2. source-share PPML with pressure interactions;
3. mechanism models for China, RoW, and total imports;
4. price-wedge model and inference limits.

This is enough for the revised proposal. The full thesis can contain the
larger robustness suite after the final data are complete.
