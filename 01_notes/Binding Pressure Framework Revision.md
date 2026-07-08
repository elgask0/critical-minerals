---
description: "Post-defense theory-first revision note for the critical-mineral binding-pressure framework"
created: 2026-06-30
modified: 2026-07-01
group: structure
tags: [project, critical-minerals, thesis, theoretical-framework, binding-pressure, revision]
status: active
created_by: codex
---

# Binding Pressure Framework Revision

This note records the post-defense theory revision. It does not replace the
current proposal source by itself. It is the design target for the revised
proposal and the full thesis.

## 1. Diagnosis

The proposal was too centered on the average PPML coefficient. That made the
project vulnerable to the critique that it only tests whether export controls
reduce trade.

The revised thesis should make the theoretical object central:

> Pre-policy importer exposure and non-China supplier structure predict how
> Chinese critical-mineral licensing controls bind.

The key outcome is not only a negative China-source coefficient. The thesis
should explain whether the control produces source switching, import
compression, price segmentation, or a weak measured response.

The PPML triple difference remains useful, but it is now a test of the theory.
It measures whether predicted pressure explains heterogeneous China-source
declines and adjustment margins.

## 2. What The Theory Must Predict

The theory should predict three trade margins and one price margin.

China-source decline:

\[
\Delta M^C_{ipt}<0.
\]

Rest-of-world switching:

\[
\Delta M^R_{ipt}>0.
\]

Total import compression:

\[
\Delta M^T_{ipt}<0.
\]

International-China price segmentation:

\[
\Delta \pi_{pt}>0,
\qquad
\pi_{pt}=\log P^{INT}_{pt}-\log P^{CN}_{pt}.
\]

These are different outcomes. A China-source decline can happen through
switching or compression.

Switching means:

\[
M^C \downarrow,\qquad M^R \uparrow,\qquad M^T \text{ stable or rising}.
\]

Compression means:

\[
M^C \downarrow,\qquad M^R \text{ weak},\qquad M^T \downarrow.
\]

Price segmentation means international prices rise relative to comparable
Chinese domestic prices. It is most informative when trade values alone mix
quantity and price changes.

## 3. Feasible Primitives

Use only variables that can be built from pre-policy Comtrade data, fine-code
customs data where available, or matched price series from Bloomberg, Wind, or
open official sources.

Let \(i\) index importers, \(p\) products, \(s\) source groups, and \(t\)
months.

### Importer China Exposure

\[
E_{ip}=
\frac{\sum_{t<T_p^{ann}}M^C_{ipt}}
{\sum_{t<T_p^{ann}}M^C_{ipt}+\sum_{t<T_p^{ann}}M^R_{ipt}}.
\]

\(E_{ip}\) asks whether importer \(i\) depended on China for product \(p\)
before the policy. It is the only China-exposure term in the main index.
Product-level China share is not included again, to avoid double counting.

### Importer Outside Access

\[
O_{ip}=
\frac{\#\{t<T_p^{ann}:M^R_{ipt}>0\}}
{\#\{t<T_p^{ann}\}}.
\]

\(O_{ip}\) asks whether importer \(i\) already had non-China sourcing channels
before the policy.

### Product Outside-Market Strength

Product outside-market strength is measured outside importer \(i\), so it does
not mechanically repeat \(O_{ip}\).

\[
A^{ROW}_{-i,p}
=
Depth^{ROW}_{-i,p}
\times
Diversification^{ROW}_{-i,p}.
\]

Depth is:

\[
Depth^{ROW}_{-i,p}
=
\frac{\log(1+N^{ROW}_{-i,p})}
{\log(1+N^{ROW}_{max})},
\]

where \(N^{ROW}_{-i,p}\) is the number of distinct non-China supplier
countries for product \(p\), excluding importer \(i\), in the pre-policy
period.

Diversification is:

\[
Diversification^{ROW}_{-i,p}
=
1-HHI^{ROW}_{-i,p}.
\]

So:

\[
A^{ROW}_{-i,p}
=
Depth^{ROW}_{-i,p}(1-HHI^{ROW}_{-i,p}).
\]

This baseline uses the bottleneck interpretation of HHI: concentrated
non-China supply means replacement is harder because many importers may
compete for the same few suppliers.

The alternative interpretation is also possible. A high non-China HHI may mean
one large supplier has scalable substitute capacity. Test this as robustness:

\[
A^{ROW,alt}_{-i,p}
=
Depth^{ROW}_{-i,p}HHI^{ROW}_{-i,p}.
\]

If this alternative predicts switching better, that is a result. It would mean
concentrated non-China supply acts more like scalable substitute capacity than
bottleneck risk for these products.

### Product Replacement Rigidity

\[
R_{-i,p}=1-A^{ROW}_{-i,p}.
\]

\(R_{-i,p}\) is high when non-China replacement is shallow or concentrated.
It is feasible, pre-policy, and built from observed supplier structure.

## 4. Pressure Indexes

A single scalar cannot explain both switching and compression. Use two
pressure indexes first, then sum them only when the outcome is China-source
decline.

### Switching Pressure

Switching requires exposure to China, pre-policy access to non-China suppliers,
and a broad non-China market.

\[
P^S_{ip}
=
E_{ip}O_{ip}A^{ROW}_{-i,p}.
\]

Prediction:

\[
P^S_{ip}\uparrow
\Rightarrow
M^C \downarrow,\quad M^R \uparrow,\quad M^T \text{ stable or rising}.
\]

### Compression Pressure

Compression requires exposure to China, weak importer outside access, and a
rigid non-China market.

\[
P^C_{ip}
=
E_{ip}(1-O_{ip})R_{-i,p}.
\]

Equivalently:

\[
P^C_{ip}
=
E_{ip}(1-O_{ip})(1-A^{ROW}_{-i,p}).
\]

Prediction:

\[
P^C_{ip}\uparrow
\Rightarrow
M^C \downarrow,\quad M^R \text{ weak},\quad M^T \downarrow.
\]

Compression pressure should also predict price segmentation where comparable
prices exist:

\[
P^C_{ip}\uparrow
\Rightarrow
\Delta \pi_{pt}>0.
\]

### China-Source Decline Pressure

For the source-share PPML, both channels imply a China-source decline.

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

\(P^X_{ip}\) is useful for the China-source outcome. It should not replace the
two-channel interpretation.

## 5. PPML Integration

Let:

\[
D_{ipst}=Treated_p\times China_s\times Post_{pt}.
\]

\(D_{ipst}\) is the treated-product, China-source, post-policy switch.

The average model is:

\[
\mathbb{E}[M_{ipst}\mid X]
=
\exp[
\beta_0D_{ipst}
+FE
].
\]

This gives one average China-source effect. That is no longer the central
result.

The theory-guided source-share model is:

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

\(\widetilde P^S_{ip}\) and \(\widetilde P^C_{ip}\) should be standardized:

\[
\widetilde P^S_{ip}
=
\frac{P^S_{ip}-\bar P^S}{sd(P^S)},
\qquad
\widetilde P^C_{ip}
=
\frac{P^C_{ip}-\bar P^C}{sd(P^C)}.
\]

\(\beta_0\) is the estimated China-source effect for an importer-product pair
with average switching pressure and average compression pressure.

\(\theta_S\) is the log-point change in the China-source effect when switching
pressure is one standard deviation higher.

\(\theta_C\) is the log-point change in the China-source effect when
compression pressure is one standard deviation higher.

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

This is the bridge from theory to PPML. The pressure indexes do not need the
same units as \(\beta\). The regression maps pre-policy pressure into
post-policy log trade effects.

Use the source-share fixed effects:

\[
\alpha_{ips}+\delta_{it}+\lambda_{pt}+\mu_{st}.
\]

\(\alpha_{ips}\) absorbs stable importer-product-source sourcing patterns.
\(\delta_{it}\) absorbs importer-month shocks. \(\lambda_{pt}\) absorbs
product-month shocks. \(\mu_{st}\) absorbs source-month shocks.

### Clean And Partial Treatment Scope

The main pressure-interaction model should first use clean treated products
and clean eligible controls. This avoids making the average coefficient depend
on HS codes where the legal control covers only part of the measured product.

Partial, bundled, and scope-contaminated products remain useful, but they
should enter as secondary scope tests. They include:

| Product type | Examples | Main interpretation |
|---|---|---|
| Clean treated | 2504, 8110, 261710, 8106, 284180 | Main effect and mechanism evidence |
| Partial treated | 282580, 8101 | HS code contains the controlled item, but legal scope is narrower |
| Bundled treated | 811292, 282560 | HS code mixes controlled and uncontrolled products |
| Graphite scope-contaminated | 3801 | Some artificial or colloidal graphite may fall under graphite controls, but not the whole heading |

Do not estimate an unknown treated fraction \(\chi_p\) from the same HS-6
PPML that estimates the treatment effect. Without external information,
\(\chi_p\) is not separately identified from the product-specific treatment
effect. A small or null estimate for a partial code could mean weak binding or
measurement dilution.

The preferred secondary specification is a scope-split model:

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

Pressure interactions can be split in the same way only if the sample is large
enough. Otherwise, report partial and bundled products as case studies with
the same pressure indexes. If CN8, tariff-line, or price data identify a
treated subcomponent, use those sources as measurement extensions rather than
forcing an unidentified HS-6 share into the main model.

## 6. Mechanism Tests

Raw movements in \(M^C\), \(M^R\), and \(M^T\) are not enough. They also
reflect demand, exchange rates, inventories, shipping, and unrelated supply
shocks. The margin tests should use PPML with fixed effects.

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

For collapsed China, RoW, and total outcomes, source \(s\) disappears. Use:

\[
\alpha_{ip}+\delta_{it}+\lambda_{pt}.
\]

\(\alpha_{ip}\) absorbs stable importer-product trade scale. \(\delta_{it}\)
absorbs importer-month shocks. \(\lambda_{pt}\) absorbs product-month shocks.

These tests are conditional mechanism evidence. They do not observe license
approvals, inventories, contracts, or firm-level buyer-supplier links.

## 7. Price-Wedge Integration

The price wedge should be a central outcome, not a right-hand-side control in
the trade PPML. Putting it inside the trade equation would control for part of
the mechanism.

Define:

\[
\pi_{pt}
=
\log P^{INT}_{pt}
-
\log P^{CN}_{pt}.
\]

\(P^{INT}_{pt}\) is the international benchmark price. \(P^{CN}_{pt}\) is the
Chinese domestic benchmark price. The two series must match grade, unit,
currency, location, tax basis, and quote convention as closely as possible.

Aggregate compression and switching pressure to product level with pre-policy
trade weights:

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

The interpretation is:

- high compression pressure should widen the international-China price wedge;
- high switching pressure should produce weaker price segmentation because
  non-China sourcing can absorb part of the shock.

If the price panel is too small for this regression, keep the same logic in
product case studies:

| Pattern | Interpretation |
|---|---|
| China down, RoW up, price wedge weak | Switching |
| China down, RoW weak, total down, price wedge up | Compression or scarcity pressure |
| China weak or null, price wedge up | Price pressure appears more clearly than trade value |
| China down, no price wedge | Replacement, inventories, rerouting, or demand shift may dominate |

## 8. Data Construction Rules

Use pre-policy data only to construct \(E_{ip}\), \(O_{ip}\),
\(A^{ROW}_{-i,p}\), \(R_{-i,p}\), \(P^S_{ip}\), \(P^C_{ip}\), and \(P^X_{ip}\).

Do not tune the pressure formulas after seeing final treatment effects.

Compute product outside-market variables using leave-one-importer-out supplier
structure when possible. This separates importer-specific access from global
non-China supply structure.

Do not include unobservable administrative friction, license approvals, denial
rates, or processing times in the quantitative pressure index. Official MOFCOM
approval and review statements can support institutional interpretation, but
they are not measured covariates.

Do not make HS-code observability the main theory. HS scope remains a
measurement and interpretation issue. Clean codes support stronger inference;
bundled, partial, or sparse codes require caution.

## 9. Interpretation Rules

The revised thesis should classify results by margin:

| Class | Evidence |
|---|---|
| Binding with switching | China-source decline, timing support, RoW rise, total stable or rising, high \(P^S\) predicts the pattern |
| Binding with compression | China-source decline, timing support, weak RoW replacement, total import decline, high \(P^C\) predicts the pattern |
| Binding with price segmentation | International-China price wedge widens, especially in high-compression products |
| Suggestive | Direction fits but timing, inference, or measurement is weak |
| Informative null | Clean product shows no China-source decline and no margin or price support |
| Measurement-limited null | Bundled, partial, or sparse code cannot support a strong null |

The strongest final thesis would show that:

\[
P^S \Rightarrow M^C\downarrow,\ M^R\uparrow,\ M^T \text{ stable/rising},
\]

while:

\[
P^C \Rightarrow M^C\downarrow,\ M^R \text{ weak},\ M^T\downarrow,
\ \pi\uparrow.
\]

That directly answers the defense critique. It explains why formally similar
licensing controls produce different observed market responses.

## 10. Minimum Success Standard

The thesis does not need every treated product to show a negative significant
effect.

A defensible final thesis needs:

1. pressure indexes built only from pre-policy data;
2. source-share PPML evidence that predicted pressure explains heterogeneous
   China-source declines;
3. margin evidence that switching pressure and compression pressure predict
   different outcomes;
4. price-wedge evidence for compression or segmentation where matched prices
   exist;
5. clear limits for bundled, partial, sparse, or price-unmatched products.

This standard is stronger than a larger list of estimators. The contribution
is not that restrictions reduce trade. The contribution is a feasible,
pre-specified framework for predicting when licensing controls create source
switching, import compression, or price segmentation.
