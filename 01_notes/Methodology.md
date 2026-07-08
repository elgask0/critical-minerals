---
description: "Canonical empirical strategy for the master's thesis"
created: 2026-06-04
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, methodology, ppml, event-study, pressure-indexes]
status: active
created_by: codex
---

# Methodology

The full design is in `Thesis Design.md`. The locked theoretical model is in
`Theoretical Framework Lock.md`, and the post-defense empirical design is in
`Empirical Strategy Lock.md`. This file is the operational estimator
specification.

## Primary Panel

Raw unit: importer \(i\) x product \(p\) x source \(s\) x month \(t\).
Preferred baseline unit: importer \(i\) x product \(p\) x source \(s\) x
quarter \(q\).

Sources are China and rest of world. The primary outcome is trade value
because bilateral net-weight coverage is incomplete. The quarterly baseline
sums monthly trade value inside each quarter. Monthly data remain necessary
for timing diagnostics and robustness. The panel must be built only from
canonical Comtrade aggregate rows:

- `partner2Code = 0`;
- `customsCode = C00`;
- `motCode = 0`;
- `mosCode = 0`.

World totals, bilateral partners, secondary-partner records, customs
breakdowns, and transport-mode breakdowns must never be summed together.

The main panel uses 53 non-group reporter countries. Exclude reporter code 97
(European Union), reporter code 975 (ASEAN), and reporter code 156 (China).
The first two are aggregate reporter groups. China is a source group in the
source-share design, not an importer in the main reporter panel.

## Pre-Policy Pressure Construction

All pressure variables must use pre-policy data only.

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

Leave-one-importer-out outside-market strength:

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

Replacement rigidity:

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

Standardize \(P^S_{ip}\) and \(P^C_{ip}\) before interaction models.

## Source-Share PPML

Let:

\[
D_{ipst}=Treated_p\times China_s\times Post_{pt}.
\]

For the quarterly baseline, replace \(t\) with quarter \(q\) and let
\(Post_{pq}\) begin in the first full post-implementation quarter.

The average source-share model is:

\[
E[M_{ipst}|X] =
\exp\left[
\beta_0D_{ipst}
+\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}
\right].
\]

This estimates the average China-source response. It is useful for reporting,
but it is not the main theoretical test.

The preferred theory-guided model is:

\[
E[M_{ipst}|X] =
\exp\left[
\beta_0D_{ipst}
+\theta_S(D_{ipst}\times \widetilde P^S_{ip})
+\theta_C(D_{ipst}\times \widetilde P^C_{ip})
+\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}
\right].
\]

Expected signs:

\[
\theta_S<0,\qquad \theta_C<0.
\]

The first-pass estimation sample should use clean treated products and clean
eligible controls. Partial, bundled, and graphite-scope products enter only in
secondary specifications or product case studies unless finer data identify
the controlled subcomponent. HS 3801 is a special graphite scope case, not an
untreated control.

Estimate with `pyfixest.fepois`. The fixed effects absorb:

- \(\alpha_{ips}\): stable importer-product-source sourcing patterns;
- \(\delta_{it}\): importer-month demand and macro shocks;
- \(\lambda_{pt}\): product-month global shocks;
- \(\mu_{st}\): source-month shocks.

The six pairwise fixed-effect model remains a term-paper comparability and
robustness specification. The importer-product-source fixed-effect version is
preferred for the full thesis.

## Mechanism Margin Models

Estimate China, rest-of-world, and total import outcomes on collapsed
importer-product-quarter panels for the baseline. Monthly versions are
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

These margin models are conditional mechanism tests. They do not observe
license approvals, inventories, contracts, or firm-level buyer-supplier links.

## Dynamic Specification

Replace the static treatment interaction with event-time interactions. The
preferred event-study diagnostic is quarterly, with monthly versions retained
for announcement, implementation, and front-loading checks. Center monthly
event time on the first plausible importer-arrival month:

| Episode | Announcement | Implementation | First arrival exposure |
|---|---|---|---|
| Ga/Ge | July 2023 | August 2023 | September 2023 |
| Graphite | October 2023 | December 2023 | January 2024 |
| Antimony | August 2024 | September 2024 | October 2024 |
| Tungsten/bismuth | February 2025 | February 2025 | March 2025 |

Departure and importer-arrival results must be presented together. A shipping
lag is measurement timing, not a second policy treatment.

## Price-Wedge Outcome

Use exact-grade or closest defensible domestic and international benchmark
pairs. Convert prices to a common currency and unit. Document location,
tax basis, and quote convention.

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

The price wedge is an outcome, not a control in the trade PPML. It captures
market segmentation when trade values mix quantity and price changes.

## Inference

Treatment varies at product-time. Reporter-clustered standard errors are
reported only as conditional uncertainty. They do not convert 53 reporters
into 53 independent treatments.

Required reporting:

- number of reporters and products;
- observations dropped by PPML separation;
- reporter-clustered coefficient and p-value;
- exact or placebo product-assignment diagnostic;
- minimum attainable product-level p-value;
- pre-announcement pretrend tests and timing diagnostics;
- pressure-index construction window;
- pressure-index summary statistics;
- margin and price-wedge consistency.

With one treated product and three placebos, the minimum exact assignment
p-value is 0.25. Conventional four-product cluster-robust p-values are
unreliable and must not be interpreted. The script reports the observed
coefficient's rank across all possible treated-product assignments as a
placebo diagnostic. It is not described as randomization inference because
actual policy assignment was not random.

## Supporting Analyses

### Exporter Interrupted Time Series

Estimate log China-reported exports on a linear trend and implementation
indicator. Use HAC/Newey-West standard errors with six monthly lags. This is a
descriptive timing test without an untreated counterfactual.

### Eurostat CN8

Estimate Ga versus In/V, Ge versus In/V, and pooled Ga/Ge versus In/V using the
same source-share PPML design. Use the balanced current-EU27 panel only.

### Diversification

Use non-China trade, supplier count, and supplier HHI. These outcomes help
distinguish switching through many suppliers from replacement by a few large
suppliers.

### Alternative HHI Interpretation

The baseline outside-market strength uses \(1-HHI^{ROW}_{-i,p}\), treating
concentration as bottleneck risk. Test the alternative:

\[
A^{ROW,alt}_{-i,p}
=
Depth^{ROW}_{-i,p}HHI^{ROW}_{-i,p}.
\]

If the alternative predicts switching better, concentrated non-China supply may
act as scalable substitute capacity rather than bottleneck risk.

### SCM And Synthetic DiD

Appendix diagnostics only until the donor pool is materially expanded and
pre-treatment fit is credible.

## Robustness

- alternative 12- and 24-month pre-periods;
- trade value versus net-weight complete cases;
- alternative pre-specified placebo sets;
- announcement versus implementation timing;
- zero-flow and minimum-trade thresholds;
- excluding re-export hubs;
- excluding the United States reporter, code 842;
- optional U.S.-specific interaction for the late-2024 U.S.-destination policy
  environment;
- leave-one-importer-out estimates;
- placebo implementation dates;
- alternative HHI interpretation;
- Rambachan-Roth sensitivity for a compatible linear event study;
- SCM and Synthetic DiD appendix diagnostics.

Matrix completion and CausalImpact are dropped. Callaway-Sant'Anna is deferred
until a larger set of independently treated products and cohorts is available.

## Canonical Scripts

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

`analysis_final.py` reproduces the superseded term-paper analysis and must not
be used for new thesis claims.
