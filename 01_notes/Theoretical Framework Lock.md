---
description: "Locked theoretical framework for the master thesis after proposal-defense feedback"
created: 2026-06-27
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, thesis, theoretical-framework, licensing-pressure, switching, compression]
status: active
created_by: codex
---

# Theoretical Framework Lock

This note is the canonical theoretical framework for the revised master thesis
proposal and full thesis. It supersedes the older single licensing-wedge model,
the two-period commitment model, and the compact switching-potential proxy as
the main theory.

## Bottom Line

Use a theory-first framework:

> Chinese critical-mineral export licensing controls bind when pre-policy
> importer exposure and non-China supplier structure convert a legal rule into
> source switching, import compression, or price segmentation.

The PPML triple difference is not the theoretical contribution. It is the main
trade estimator used to test whether the theory predicts heterogeneous
China-source declines.

The central chain is:

\[
\text{legal licensing rule}
\rightarrow
\text{predicted importer-product pressure}
\rightarrow
\begin{cases}
\text{source switching},\\
\text{import compression},\\
\text{price segmentation},\\
\text{weak or measurement-limited response}.
\end{cases}
\]

## Definition Of Binding

A Chinese critical-mineral export-licensing control is binding when it creates
an observable market restriction or adjustment after the expected import-effect
month.

Binding does not mean:

- an export ban;
- observed license denial;
- low approval rates;
- Chinese strategic intent;
- coercive political success;
- welfare loss;
- downstream production disruption.

The revised thesis distinguishes three terms:

| Term | Meaning | Main evidence |
|---|---|---|
| Legal licensing | The official rule requires licenses for covered exports | MOFCOM and customs documents |
| Trade binding | China-source trade falls where pre-policy pressure predicts it should fall | Source-share PPML and timing diagnostics |
| Adjustment margin | The economic meaning of the China-source decline | RoW imports, total imports, supplier structure, and price wedges |

The thesis does not claim that every legal control should reduce measured HS-6
trade. Some codes are bundled, partial, sparse, or poorly matched to the legal
scope. HS observability affects interpretation, but it is not the main
economic mechanism.

## Treatment-Scope Hierarchy

The main theoretical test should start with clean treated products. Clean
products are the cases where the HS code maps closely to the legal control and
trade is regular enough to support interpretation.

Partial, bundled, and scope-contaminated products are secondary scope cases:

| Scope class | Examples | Interpretation |
|---|---|---|
| Clean treated baseline | 2504, 8110, 8106, 284180 | Main pressure and mechanism tests |
| Clean but sparse | 261710 | Secondary antimony upstream case; descriptive unless coverage improves |
| Partial treated | 282580, 8101 | Legal control covers a narrower item inside the HS code |
| Bundled treated | 811292, 282560 | HS code mixes controlled and uncontrolled products |
| Graphite scope case | 3801 | Artificial/colloidal graphite may overlap the graphite regime, but the heading is not clean |

Do not treat the unknown controlled share of a partial HS code as an estimated
structural parameter in the baseline model. Without external fine-code data,
the controlled share and the treatment effect are not separately identified
from HS-6 trade. Partial and bundled cases can still test whether a response
is visible at the measured HS level.

## Feasible Primitives

Let \(i\) index importers, \(p\) products, \(s\) source groups, and \(t\)
months. Let China and rest of world be the two source groups.

### Importer China Exposure

\[
E_{ip}=
\frac{\sum_{t<T_p^{ann}}M^C_{ipt}}
{\sum_{t<T_p^{ann}}M^C_{ipt}+\sum_{t<T_p^{ann}}M^R_{ipt}}.
\]

\(E_{ip}\) measures whether importer \(i\) depended on China for product \(p\)
before the policy. It is the only China-exposure term in the main pressure
indexes.

### Importer Outside Access

\[
O_{ip}=
\frac{\#\{t<T_p^{ann}:M^R_{ipt}>0\}}
{\#\{t<T_p^{ann}\}}.
\]

\(O_{ip}\) measures whether importer \(i\) had observed non-China sourcing
channels before the policy.

### Product Outside-Market Strength

Outside-market strength is measured outside importer \(i\):

\[
A^{ROW}_{-i,p}
=
Depth^{ROW}_{-i,p}(1-HHI^{ROW}_{-i,p}).
\]

Depth is:

\[
Depth^{ROW}_{-i,p}
=
\frac{\log(1+N^{ROW}_{-i,p})}
{\log(1+N^{ROW}_{max})}.
\]

\(N^{ROW}_{-i,p}\) is the number of distinct non-China supplier countries for
product \(p\), excluding importer \(i\), in the pre-policy period.

\(1-HHI^{ROW}_{-i,p}\) measures non-China supplier diversification. The
baseline interpretation is that concentrated non-China supply creates
bottleneck risk. A robustness version can use:

\[
A^{ROW,alt}_{-i,p}
=
Depth^{ROW}_{-i,p}HHI^{ROW}_{-i,p}
\]

to test whether one large non-China supplier acts as scalable substitute
capacity.

### Product Replacement Rigidity

\[
R_{-i,p}=1-A^{ROW}_{-i,p}.
\]

\(R_{-i,p}\) is high when non-China replacement is shallow or concentrated.
It is a feasible proxy for product replacement rigidity. It does not require
unobserved license approvals, administrative frictions, inventories, or firm
contracts.

## Pressure Indexes

The theory uses two pressure indexes. A single scalar cannot cleanly predict
both switching and compression.

### Switching Pressure

\[
P^S_{ip}
=
E_{ip}O_{ip}A^{ROW}_{-i,p}.
\]

Switching pressure is high when an importer was exposed to China, already had
non-China access, and the product has a broad non-China market.

Prediction:

\[
P^S_{ip}\uparrow
\Rightarrow
M^C\downarrow,\quad M^R\uparrow,\quad M^T \text{ stable or rising}.
\]

### Compression Pressure

\[
P^C_{ip}
=
E_{ip}(1-O_{ip})R_{-i,p}.
\]

or:

\[
P^C_{ip}
=
E_{ip}(1-O_{ip})(1-A^{ROW}_{-i,p}).
\]

Compression pressure is high when an importer was exposed to China, lacked
non-China access, and the product has a rigid non-China replacement market.

Prediction:

\[
P^C_{ip}\uparrow
\Rightarrow
M^C\downarrow,\quad M^R \text{ weak},\quad M^T\downarrow.
\]

Compression pressure should also predict price segmentation where comparable
price benchmarks exist:

\[
P^C_{ip}\uparrow
\Rightarrow
\Delta \pi_{pt}>0.
\]

### China-Source Decline Pressure

\[
P^X_{ip}=P^S_{ip}+P^C_{ip}.
\]

Expanded:

\[
P^X_{ip}
=
E_{ip}O_{ip}A^{ROW}_{-i,p}
+
E_{ip}(1-O_{ip})(1-A^{ROW}_{-i,p}).
\]

\(P^X_{ip}\) predicts the China-source decline. The two components remain
separate because they imply different RoW, total-import, and price outcomes.

## PPML Mapping

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
+FE
].
\]

The theory-guided model is:

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
FE
].
\]

The pressure indexes should be standardized:

\[
\widetilde P^S_{ip}
=
\frac{P^S_{ip}-\bar P^S}{sd(P^S)},
\qquad
\widetilde P^C_{ip}
=
\frac{P^C_{ip}-\bar P^C}{sd(P^C)}.
\]

\(\beta_0\) is the China-source effect for an importer-product pair with
average switching pressure and average compression pressure.

\(\theta_S\) is the log-point change in the China-source effect for a one
standard deviation increase in switching pressure.

\(\theta_C\) is the log-point change in the China-source effect for a one
standard deviation increase in compression pressure.

Expected signs:

\[
\theta_S<0,\qquad \theta_C<0.
\]

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

The pressure indexes do not need the same units as \(\beta\). The regression
maps pre-policy pressure into post-policy log trade effects.

The pressure coefficients do not all need to be statistically significant for
the thesis to remain valid. But if the thesis makes a positive mechanism
claim, the preferred design should show at least one pressure channel with the
expected sign, plausible timing, and mechanism-consistent margin evidence.

## Mechanism Tests

The mechanism cannot be inferred from raw trade movements alone. Estimate
margin models with fixed effects.

For China imports:

\[
\mathbb{E}[M^C_{ipt}\mid X]
=
\exp[
\theta^C_S(Post_{pt}\times Treated_p\times \widetilde P^S_{ip})
+
\theta^C_C(Post_{pt}\times Treated_p\times \widetilde P^C_{ip})
+
FE
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
FE
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
FE
].
\]

Expected:

\[
\theta^T_S\geq 0,\qquad \theta^T_C<0.
\]

For source-share PPML, use:

\[
\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}.
\]

For China, RoW, and total outcome models, source \(s\) disappears. Use:

\[
\alpha_{ip}+\delta_{it}+\lambda_{pt}.
\]

These fixed effects absorb stable importer-product relationships,
importer-month shocks, and product-month shocks. The tests remain conditional
evidence because the data do not observe license approvals, inventories,
contracts, or firm-level buyer-supplier links.

## Price-Wedge Outcome

Price wedges are central outcomes, not controls inside the trade PPML.

Define:

\[
\pi_{pt}
=
\log P^{INT}_{pt}
-
\log P^{CN}_{pt}.
\]

If licensing segments the market, international prices should rise relative to
Chinese domestic prices:

\[
\Delta \pi_{pt}>0.
\]

Aggregate product-level pressure using pre-policy trade weights:

\[
\bar P^C_p=\sum_i w_{ip}P^C_{ip},
\qquad
\bar P^S_p=\sum_i w_{ip}P^S_{ip}.
\]

The price-wedge model is:

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

Interpretation:

- high compression pressure should widen the international-China price wedge;
- high switching pressure should produce weaker price segmentation because
  non-China sourcing absorbs part of the shock.

Use price evidence only when grade, unit, currency, location, tax basis, and
quote convention are close enough for comparison.

## Locked Hypotheses

| Hypothesis | Prediction | Main tests |
|---|---|---|
| H1 China-source pressure | Higher \(P^X_{ip}\), or higher \(P^S_{ip}\) and \(P^C_{ip}\), predicts a larger post-policy China-source decline | Source-share PPML with pressure interactions |
| H2 Switching channel | Higher \(P^S_{ip}\) predicts China-source decline, RoW increase, and stable or rising total imports | China, RoW, and total PPML margin models |
| H3 Compression and price channel | Higher \(P^C_{ip}\) predicts China-source decline, weak RoW replacement, total import decline, and wider international-China price wedge where matched prices exist | Margin models and price-wedge model |
| H4 Timing discipline | Effects should appear after the expected import-effect month, not as systematic pre-policy declines | Event-study PPML |
| H5 Measurement discipline | Clean and regular HS codes support stronger claims than bundled, partial, sparse, or price-unmatched products | Product-scope audit, trade regularity, fine-code extensions |

## Interpretation Rules

### Binding With Switching

Use this label when:

- China-source imports fall;
- timing is plausible;
- RoW imports rise;
- total imports are stable or rising;
- high \(P^S_{ip}\) predicts the pattern.

HS 282580 antimony oxides currently supports this interpretation better than
the other completed cases.

### Binding With Compression

Use this label when:

- China-source imports fall;
- timing is plausible;
- RoW replacement is weak;
- total imports fall or price wedges widen;
- high \(P^C_{ip}\) predicts the pattern.

### Binding With Price Segmentation

Use this label when comparable international and Chinese domestic prices show
a post-policy widening of \(\pi_{pt}\), especially where compression pressure
is high.

### Suggestive Only

Use this label when the direction fits but timing, inference, product scope,
or mechanism evidence is weak. HS 2504 natural graphite currently belongs
here.

### Descriptive Only

Use this label when trade is sparse, estimates are driven by a small number of
cells, or the design lacks a credible untreated comparison. HS 261710 antimony
ores/concentrates currently belongs here.

### Informative Null

A null is informative when a clean, regular, well-matched product shows no
China-source decline and no margin or price support.

### Measurement-Limited Null

A null is measurement-limited when the HS code is bundled, partial, sparse, or
poorly matched to the legal scope. HS 811292 and HS 282560 currently belong
closer to this category than to a strong economic null.

## Dropped Or Demoted Ideas

| Idea | Decision | Reason |
|---|---|---|
| Non-monotonic monopoly or commitment model | Drop as core theory | Requires unobserved enforcement, inventories, welfare, and strategic intent |
| License approval or denial rates | Use only as institutional context if found | Not observed systematically |
| One scalar \(A_{ip}=E_{ip}O_{ip}\) as main mechanism | Demote | It cannot distinguish switching from compression |
| Product-level China share inside pressure index | Drop from main index | It double-counts China exposure already captured by \(E_{ip}\) |
| HS observability as main theory | Demote to measurement discipline | The theory should explain market adjustment, not only data visibility |
| Price wedge as side diagnostic | Promote to central outcome | It captures segmentation when trade values mix quantity and price |

## Proposal Subsection Skeleton

Use the following structure for the revised "Conceptual Framework and
Hypotheses" subsection.

1. Legal licensing is not the same as market binding.
2. Importer exposure and non-China supplier structure define predicted
   pressure.
3. Switching pressure and compression pressure predict different margins.
4. PPML tests whether predicted pressure explains China-source declines.
5. RoW, total imports, and price wedges classify the adjustment margin.
6. HS-code scope and trade regularity define interpretation limits.
7. Hypotheses and expected signs.
