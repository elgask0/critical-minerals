---
description: "Current post-defense thesis plan, model hierarchy, data state, and preliminary result map"
created: 2026-07-02
modified: 2026-07-02
group: structure
tags: [project, critical-minerals, thesis, post-defense, pressure-indexes, quarterly-ppml]
status: active
created_by: codex
---

# Post-Defense Thesis Plan

This note is the current source of truth after the proposal defense. It
supersedes the earlier term-paper-centered execution plan. Keep the older
notes for provenance, but use this file to decide what to estimate and how to
describe the results.

## 1. Current Direction

Keep the project. Revise the thesis so the mechanism is central.

The old weak version was:

> export restrictions reduce trade.

The revised version is:

> Chinese critical-mineral export licensing controls bind when pre-policy
> China exposure meets limited or uneven outside replacement capacity. The
> observed adjustment can be source switching, import compression, or price
> segmentation.

The average PPML coefficient is no longer the main result. It is the first
measurement step. The core test is whether pre-policy pressure predicts where
the China-source decline appears and which margin absorbs the shock.

## 2. Research Question

> When do Chinese critical-mineral export licensing controls bind in
> international trade, and do affected importers adjust through substitution
> toward non-China suppliers, compression of total imports, or price
> segmentation?

## 3. Baseline Sample

Use the strict clean sample for the main model.

| Role | Products |
|---|---|
| Clean treated | HS 2504 graphite; HS 8110 antimony metal; HS 8106 bismuth; HS 284180 tungstates/APT |
| Clean controls | The 12 screened donor products in the pressure panel |
| Secondary only | HS 261710, HS 282580, HS 282560, HS 811292, HS 3801, HS 8101 |

HS 261710 is clean in legal scope but sparse in trade. It is not part of the
strict baseline. HS 282580 remains useful as a feasibility and secondary
antimony case, but it is partial at HS-6 because the control applies to high
purity antimony oxides.

## 4. Timing Hierarchy

Use different dates for different jobs.

| Purpose | Timing |
|---|---|
| Main quarterly PPML | First full post-implementation quarter |
| Legal-policy reference | Implementation date |
| Anticipation/front-loading diagnostic | Announcement date |
| Monthly lag robustness | Implementation month + 1 month |
| Event-study diagnostics | Announcement and implementation anchors |

The first full post-implementation quarter is the preferred baseline because
implementation often occurs inside a month or quarter. It avoids treating a
mixed transition quarter as a clean post-policy period.

## 5. Pressure Variables

All pressure variables use pre-announcement trade data only.

Importer China exposure:

\[
E_{ip}=
\frac{\sum_{t<T_p^{ann}}M^C_{ipt}}
{\sum_{t<T_p^{ann}}M^C_{ipt}+\sum_{t<T_p^{ann}}M^R_{ipt}}.
\]

Switching pressure:

\[
P^S_{ip}=E_{ip}O_{ip}A^{ROW}_{-i,p}.
\]

Compression pressure:

\[
P^C_{ip}=E_{ip}(1-O_{ip})R_{-i,p}.
\]

where:

\[
R_{-i,p}=1-A^{ROW}_{-i,p}.
\]

Use three pressure variants until the final baseline is chosen:

| Variant | Use |
|---|---|
| Frequency | \(O_{ip}\) is the share of pre-policy months with positive RoW imports |
| Capacity | \(O_{ip}=\min(1,M^R_{ip,pre}/M^C_{ip,pre})\) |
| Absorptive | Scale-adjusted version that penalizes tiny RoW capacity relative to China supply |

Do not make \(P^X_{ip}=P^S_{ip}+P^C_{ip}\) the main thesis object. It is a
summary of China-source decline pressure, but it hides the switching versus
compression distinction.

## 6. Main Trade Model

Let:

\[
D_{ipst}=Treated_p\times China_s\times Post_{pt}.
\]

The preferred source-contrast PPML is:

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

Interpretation:

- \(\beta_0\) is the China-source post-policy effect at average pressure.
- \(\theta_S\) asks whether switching pressure predicts a stronger
  China-source decline.
- \(\theta_C\) asks whether compression pressure predicts a stronger
  China-source decline.

Expected signs:

\[
\theta_S<0,\qquad \theta_C<0.
\]

The pressure coefficients do not all need to be significant for the thesis to
remain viable. But if the mechanism is the main contribution, at least one
pressure channel must work clearly in the preferred design or the positive
claim must be downgraded.

## 7. Mechanism Models

Estimate quarterly importer-product models for China, RoW, and total imports.

Expected pattern:

| Outcome | \(P^S\) | \(P^C\) |
|---|---:|---:|
| China imports | negative | negative |
| RoW imports | positive | zero or negative |
| Total imports | zero or positive | negative |
| Price wedge | weak or positive | positive |

The current evidence supports switching more clearly than compression.
Compression should not be the headline unless the final price and quantity
results improve.

## 8. Price-Wedge Role

Price wedges are mechanism diagnostics, not controls inside the trade PPML.

\[
\pi_{pt}=\log P^{INT}_{pt}-\log P^{CN}_{pt}.
\]

Use price evidence to diagnose segmentation or scarcity when trade quantities
do not fully reveal pressure. Current price evidence is strongest for antimony
and bismuth. Graphite does not currently show price-wedge support. Tungsten is
unresolved because the benchmark match still needs verification.

## 9. Current Preliminary Result Map

These are preliminary results from the current pressure-panel run. They are
not final thesis claims.

### Quarterly average PPML, first full post-quarter

| Case | Coefficient | Reporter p | Percent effect | Status |
|---|---:|---:|---:|---|
| Graphite | -0.359 | 0.076 | -30.1% | Suggestive |
| Antimony metal | -2.018 | 9.13e-09 | -86.7% | Strong average effect, timing/placebo caution |
| Wave 4 W/Bi | -0.551 | 0.021 | -42.4% | Supported |
| Bismuth | -1.361 | 0.000305 | -74.4% | Strong |
| Tungstates/APT | -0.165 | 0.683 | -15.2% | Weak or null |

### Pressure-interaction summary

Switching pressure is the clearer channel:

- Graphite: frequency and absorptive switching interactions are negative and
  significant.
- Wave 4: frequency and absorptive switching interactions are negative and
  significant.
- Bismuth: pressure signs are mixed, but the average effect and price wedge
  are strong.
- Antimony: the average effect is very large, but pressure interactions do not
  explain much of the heterogeneity.
- Tungstates: weak average effect and weak pressure evidence.

Compression pressure is not yet clean. It is often negative in the China
source model, but it is unstable in mechanism models and sometimes predicts
RoW increases. Treat compression as a secondary or price-supported mechanism
unless later estimates improve.

### Event-study diagnostics

Quarterly event pretrend tests are mostly acceptable:

| Case | Quarterly pretrend p |
|---|---:|
| Graphite | 0.400 |
| Antimony metal | 0.046 with announcement/implementation anchor; 0.058 with import-effect anchor |
| Wave 4 W/Bi | 0.611 |
| Bismuth | 0.325 |
| Tungstates/APT | 0.001 covariance-based joint test, but individual leads are small and insignificant |

Antimony has a real timing concern. Tungstates has an unstable joint test and
weak average effect, so it should not carry a positive claim.

### Price wedges

| Case | Price-wedge evidence |
|---|---|
| Antimony metal | Strong positive wedge: +58.3%, p = 1.03e-04 |
| Bismuth | Strong positive wedge: +131.0%, p = 1.81e-11 |
| Graphite | No supportive wedge in current exploratory benchmark |
| Tungsten/APT | Current benchmark gives the wrong sign; verify before using |
| Ga/Ge partial/bundled | Positive wedges, useful for secondary discussion only |

## 10. Current Interpretation

The safest central story is:

> The controls produced heterogeneous China-source declines. The clearest
> mechanism in trade data is source switching. Price wedges provide additional
> evidence of segmentation for antimony and bismuth. Pure import compression
> remains harder to identify from the current trade data.

Do not write:

> The model proves that licensing controls reduce trade through compression.

Better:

> The results are consistent with pressure-predicted switching in several
> products and with price segmentation in antimony and bismuth. Compression is
> a plausible channel, but current quantity evidence is mixed.

## 11. Required Next Steps

1. Wait for the external design critique before changing the model hierarchy.
2. Verify remaining price benchmarks, especially graphite, antimony oxides, and
   tungsten/APT.
3. Decide whether absorptive pressure is the baseline or one of three reported
   variants.
4. Add high/low or tercile pressure bins as a transparent robustness check.
5. Re-run placebo-date tests for the quarterly baseline, not only the old
   monthly import-effect model.
6. Decide how to describe antimony given its strong average effect but weak
   placebo-date evidence.
7. Update the proposal prose only after the model hierarchy is frozen.
