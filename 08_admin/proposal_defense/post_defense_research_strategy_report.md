# Post-Defense Research Strategy Report

Date: 2026-06-30

Purpose: convert the defense feedback into a stronger thesis design. This note
does not edit the proposal. It explains how to revise the proposal and how to
develop the final thesis by November.

## 1. Core Diagnosis

The reviewers' critique is valid. If the thesis is framed as "Chinese export
restrictions reduce trade," the contribution is weak. That result is intuitive.
It may be new for these policy episodes, but novelty in episode and data is not
enough for a high-level external review.

The thesis should not be centered on the average negative PPML coefficient. It
should be centered on heterogeneity:

> Under what product and importer conditions do Chinese export-licensing
> controls create observable trade-binding wedges, and do those wedges appear
> as source switching, import compression, or price segmentation?

This is a stronger question because it is not obvious. A licensing control can
be legally active but weak in trade data. It can bind in one HS code and not in
another. It can reduce China sourcing while total imports rise. It can widen
price gaps without a clean quantity collapse. It can disappear inside a bundled
HS code. These are the patterns the thesis can explain.

The current proposal already contains the pieces of this answer. They are not
yet organized as the answer. They are still written as secondary diagnostics
after the main DDD model. That is the main structural problem.

## 2. What Must Change In The Revised Proposal

### 2.1 Change The Center Of The Contribution

Current implicit center:

> Estimate whether Chinese mineral export controls reduce China-sourced imports.

Better center:

> Explain why formally similar licensing controls produce different observed
> market responses across minerals, products, and importers.

The source-share PPML model remains important, but it becomes the first
measurement step. The thesis contribution becomes the interpretation framework:
product scope, supply conditions, importer outside options, timing, and price
evidence determine whether a legal license becomes a trade-binding wedge.

### 2.2 Revise The Main Research Question

The existing question is close but too easy to misread:

> Why do formally similar Chinese export-licensing controls generate different
> trade and price disruptions across critical minerals?

Keep the spirit, but make the mechanism visible:

> Under what product and importer conditions do Chinese export-licensing
> controls create observable trade-binding wedges, and do they appear through
> source switching, import compression, or price segmentation?

This version forces the proposal to answer "when" and "why." It also prevents
the thesis from sounding like a simple policy-effect paper.

### 2.3 Bring Back Mechanism Hypotheses

The proposal currently keeps H1-H3 for simplicity. That helped clarity, but it
weakened the intellectual contribution. For the revised proposal, the mechanism
hypotheses should be explicit.

Recommended hypothesis structure:

1. **H1: Trade-binding source wedge.** Treated products show a post-policy
   decline in China-sourced imports relative to rest-of-world sourcing and
   untreated products.
2. **H2: Timing and persistence.** A trade-binding wedge appears after the
   expected import-effect month, not before the policy window, and should
   persist or deepen rather than appear as a one-month break.
3. **H3: Product observability and scope.** Clean and regularly traded HS codes
   should show clearer effects. Bundled, partial, or sparse codes should show
   attenuated, noisy, null, or descriptive results.
4. **H4: Importer adjustment capacity.** Among importers with meaningful
   pre-policy China exposure, observed rest-of-world access predicts source
   switching. Exposed importers without outside access should show compression
   or price pressure.
5. **H5: Adjustment margin and price wedge.** A binding wedge can appear as
   source switching, total import compression, or a domestic-international price
   gap. These are different economic outcomes, not interchangeable versions of
   "trade fell."

H1 is the intuitive part. H3-H5 are the nontrivial contribution.

## 3. The Stronger Theoretical Framework

### 3.1 Keep The Licensing-Wedge Framework

Do not drop the theoretical framework. It is the right direction. But it should
be rewritten so it answers the reviewers' question directly.

The thesis should say:

> A legal licensing rule is only the first condition. It becomes visible in
> trade data when the latent licensing wedge is strong enough, the HS code
> measures the controlled item clearly enough, and importers are exposed enough
> for the wedge to matter.

The framework should have four observable filters:

| Filter | Meaning | Feasible measurement |
|---|---|---|
| Product wedge strength | China is hard to replace in that product, grade, or value-chain stage | China share, concentration, byproduct status, value-chain stage, product use |
| HS observability | The HS code captures the legal controlled item | Clean, partial, bundled, sparse classification; CN8/HTS extensions |
| Importer exposure | Importer depended on China before the policy | Pre-policy China import share |
| Outside-option access | Importer had observed non-China sourcing channels | Pre-policy frequency of RoW sourcing, supplier count, supplier HHI |

Then the empirical question is not "does beta go down?" It is:

> Do products and importers with stronger predicted wedge visibility show
> clearer China-source adjustment, and does the adjustment margin match their
> outside options?

### 3.2 Recommended Model Language

Use the model as a mapping, not as a structural estimation claim.

Legal rule:

```tex
L_{pt}=1
```

Latent product wedge:

```tex
W_{pt}=L_{pt}\omega_p
```

Observed HS-level wedge:

```tex
\widetilde W_{pt}=\chi_p W_{pt}
```

Importer-level exposure channel:

```tex
\Delta M^C_{ip} < 0 \quad \text{is more likely when} \quad
E_{ip}\widetilde W_{pt} \text{ is large.}
```

Adjustment margin:

```tex
\Delta M^R_{ip}>0 \quad \text{if outside access is high;}
```

```tex
\Delta M^{Total}_{ip}<0 \text{ or } \Delta \pi_p>0
\quad \text{if outside access is weak and supply is tight.}
```

This is simpler and clearer than a long structural-looking equation. It also
matches the data better. The thesis does not estimate license denial,
processing time, or welfare. It estimates observable outcomes implied by the
framework.

## 4. What The Literature Can And Cannot Support

### 4.1 What The Literature Supports Well

The current literature corpus can support a stronger thesis if used correctly.

| Literature | What it supports | Key sources already read |
|---|---|---|
| Economic statecraft | Central network positions can create chokepoints, but this does not prove mineral controls work | Farrell and Newman 2019; Egger et al. 2024 |
| Export licensing | Licensing is an administrative procedure, distinct from bans and quotas | UNCTAD 2019; Gamberale and Tarasenko 2023 |
| Delay and uncertainty | Administrative time and policy uncertainty can reduce trade even without a formal ban | Djankov et al. 2010; Hummels and Schaur 2013; Handley and Limao 2017 |
| Product heterogeneity | Minerals differ by byproduct status, processing concentration, supply rigidity, and uses | USGS 2026; IEA 2025; Frenzel et al. 2017; Park 2025; van den Brink et al. 2022 |
| Adjustment margins | Trade shocks can work through supplier switching, relationship exit, entry, and concentration | Handley, Kamal, and Monarch 2024 |
| Trade methods | PPML and DDD are suitable for source-specific trade panels, but inference is limited by few product shocks | Santos Silva and Tenreyro 2006; Olden and Moen 2022; Conley and Taber 2011; Ferman and Pinto 2019 |
| Price wedges | Export restrictions can create domestic-international price separation, but only if benchmark prices are comparable | Martin and Anderson 2012; Brander et al. 2023 |

### 4.2 What The Literature Does Not Support

The literature does not support these claims:

- Chinese licensing controls automatically bind.
- A negative trade coefficient proves license denial.
- A legal announcement proves foreign scarcity.
- A null HS-6 estimate proves controlled items were unaffected.
- Reporter-clustered p-values solve the few-policy-shock problem.
- Price series can be compared without matching grade, unit, currency,
  location, tax basis, and quotation basis.

### 4.3 Revised Literature Contribution

The literature contribution should be stated as:

> Existing work explains network power, critical-mineral concentration, export
> licensing, and trade-flow methods. What is missing is a framework and
> empirical design for distinguishing legal licensing from observable
> trade-binding, and for explaining why binding appears through different
> margins across products and importers.

This is stronger than claiming only that the thesis studies recent events.

## 5. Data Reality Check

### 5.1 What Is Already Strong

The current data can already support part of the mechanism story.

| Evidence | Current status | Use |
|---|---|---|
| Global Comtrade HS-6 monthly panel | Current 10-product panel complete through March 2026 | Main source-share PPML and decomposition |
| HS 282580 antimony oxides | Strongest feasibility case: -81.5%, conditional p=0.002, pretrend p=0.680 | Main proof-of-concept |
| HS 282580 high exposure/access split | -87.4%, conditional p<0.001, pretrend not rejected | Mechanism support for source switching |
| Source decomposition | HS 282580 China falls, RoW and total imports rise | Supports switching/demand expansion, not pure compression |
| Eurostat CN8 Ga/Ge panel | Separates gallium and germanium inside HS 811292 for EU countries | Tests HS aggregation problem |
| Product observability classification | Already in notes: clean, partial, bundled, sparse | Can become a central mechanism |

### 5.2 What Is Still Weak

| Weak point | Why it matters | Fix |
|---|---|---|
| Current proposal makes beta look central | Reviewers see trivial "trade restriction reduces trade" claim | Reframe beta as one input into mechanism classification |
| Price evidence incomplete | Cannot yet distinguish switching from scarcity or segmentation | Prioritize matched Bloomberg/Wind price pairs |
| Expanded donor pool not fully audited | Product-level inference still weak | Complete coverage and donor-suitability audit |
| Product-level mechanisms mostly descriptive | Few products make formal cross-product regression weak | Use pre-specified case classification plus product-level evidence |
| License approval data unavailable | Cannot identify the administrative mechanism directly | Treat licensing intensity as latent; use timing, trade, and price patterns |

### 5.3 Data That Should Be Prioritized

Priority 1: finish data that directly answers mechanisms.

1. **Matched price pairs from Bloomberg/Wind**
   - Gallium: Fastmarkets China vs Rotterdam.
   - Germanium metal and germanium dioxide: China vs Rotterdam.
   - Antimony metal: China vs Rotterdam.
   - Antimony trioxide: China, FOB/export, Rotterdam if available.
   - Graphite: only use matched grade pairs, such as FOB China vs CIF Northeast
     Asia if exact grade is available.
   - APT/tungsten and bismuth only if Wave 4 enters the final design.

2. **Expanded donor and treated product audit**
   - Bismuth HS 8106 and APT/tungstates HS 284180 are promising Wave 4 cases.
   - Tungsten HS 8101 is partial and should be treated carefully.
   - Candidate controls must pass policy-status, coverage, regularity, and
     donor-suitability checks.

3. **High-resolution customs data**
   - Eurostat CN8 is already useful for Ga/Ge.
   - Consider U.S. HTS10, Japan HS9, or Korea HS10 only for exact product-scope
     tests. Do not make them the new baseline unless acquisition is fast.
   - These data are most useful for bundled products, not for every product.

4. **Demand and market-structure variables**
   - Semiconductor sales for Ga/Ge.
   - Battery/NEV indicators for graphite.
   - Lead-acid battery or related antimony demand.
   - USGS/IEA concentration, China share, HHI, top-three share.
   - Use these mainly as product descriptors and alternative-explanation
     checks. With few minerals, do not overfit regressions.

### 5.4 Data Not Worth Chasing As Main Evidence

1. **MOFCOM license approval rates**
   - These would be ideal, but there is no clear public panel by product,
     destination, firm, and month.
   - Use official approval/review statements only to prove the instrument is
     licensing, not to measure intensity.

2. **Firm-level China customs export data**
   - It would be excellent, but access is uncertain and probably not feasible
     within the thesis timeline.
   - Do not build the revised proposal around it.

3. **Broad downstream welfare or production effects**
   - Too far from the data.
   - Keep the thesis on trade, source adjustment, product scope, and prices.

## 6. How To Answer "When Do Controls Bind?"

The final thesis should answer with a typology.

### 6.1 Binding With Switching

Conditions:

- meaningful pre-policy China exposure;
- observed non-China sourcing access;
- negative China-source PPML effect;
- no serious pretrend failure;
- RoW imports rise or total imports remain stable/rise.

Current likely example:

- HS 282580 antimony oxides.

Interpretation:

> The control appears trade-binding on the China-source margin, but the
> adjustment looks more like source switching than pure import compression.

### 6.2 Binding With Compression

Conditions:

- China-source imports fall;
- RoW replacement is weak;
- total imports fall;
- price wedge may widen if price data match.

Current status:

- Not yet clearly established.
- This is an important target for final thesis evidence.

Interpretation:

> This is the strongest form of market disruption because importers do not fully
> replace Chinese supply.

### 6.3 Price-Only Or Price-Supported Binding

Conditions:

- trade effect may be modest;
- matched international price rises relative to China domestic price;
- product is supply-tight or outside supply is constrained.

Current status:

- Not yet established because matched price data are incomplete.

Interpretation:

> Licensing may bind through market segmentation or scarcity even when trade
> quantities do not collapse.

### 6.4 Informative Null

Conditions:

- clean product code;
- enough trade regularity;
- no negative China-source effect;
- no price wedge or adjustment evidence.

Current possible example:

- None fully clean yet except some future Wave 4 products may provide this.

Interpretation:

> Legal licensing did not create a detected aggregate HS-level China-source
> wedge in that product.

### 6.5 Measurement-Limited Null

Conditions:

- bundled HS code;
- partial legal scope;
- sparse trade;
- noisy event timing.

Current examples:

- HS 811292 Ga/Ge bundle.
- HS 282560 GeO2/ZrO2.
- HS 261710 antimony ores is more sparse/descriptive than clean causal
  evidence.

Interpretation:

> The HS-6 data do not show a detected aggregate decline, but the code is too
> broad or sparse to prove that the controlled item was unaffected.

This typology directly answers the reviewers. It also makes nulls useful.

## 7. Empirical Design After The Defense

### 7.1 Keep The Main PPML DDD

Do not abandon the source-share PPML triple difference. It remains the right
main estimator because it compares:

- China vs rest of world;
- treated vs untreated products;
- post-policy vs pre-policy timing.

But the revised proposal must stop presenting it as the whole thesis. The PPML
coefficient is the first screen for a trade-binding wedge. It is not the final
answer.

### 7.2 Add A Mechanism Evidence Table

For each product, the final thesis should report:

| Product | Scope | Regularity | Beta | Timing | China | RoW | Total | Price wedge | Interpretation |
|---|---|---|---:|---|---:|---:|---:|---|---|

This table is more important than adding another estimator. It tells reviewers
how each coefficient becomes an interpretation.

### 7.3 Use Interaction/Heterogeneity Carefully

The current high/low switching-potential split is useful. The final thesis can
extend it in two ways:

1. Report \(E_{ip}\) and \(O_{ip}\) separately, not only \(A_{ip}=E_{ip}O_{ip}\).
2. Use high/low groups or simple interactions only if they remain stable.

Do not overfit a complex continuous interaction model unless the results are
clear and interpretable.

### 7.4 Staggered DiD Is Not The Main Rescue

Staggered DiD can help organize multiple waves, but it will not solve the
reviewers' main critique. A staggered model can still produce the trivial
answer: controls reduce China imports.

Use staggered DiD only as a secondary summary after wave-specific results.
The main intellectual answer should remain product and mechanism heterogeneity.

## 8. One-Week Revision Plan

The one-week revised proposal should make the defense critique visibly solved.
It does not need every final dataset.

### Must revise now

1. Rewrite the research problem so the target is not "negative trade effect"
   but "conditions for observable binding."
2. Add a paragraph admitting that H1 alone is not the contribution.
3. Restore product observability and adjustment-margin hypotheses.
4. Recast preliminary evidence as a mechanism-classification pilot:
   - HS 282580: binding with switching-type evidence.
   - Ga/Ge HS-6: measurement-limited null.
   - graphite: suggestive but timing-limited.
   - antimony metal/ores: large but pretrend/sparsity limited.
5. Add a mechanism map table linking theory, data, test, and current status.
6. Add a revised data plan centered on price pairs, high-resolution HS/CN codes,
   and exposure/access measures.
7. Tone down the claim that the thesis "detects" effects. Use "classifies
   whether and how legal licensing becomes visible in trade and price data."

### Can wait until November

1. Full expanded donor pool.
2. Wave 4 bismuth/APT estimates.
3. Matched Bloomberg/Wind price wedge estimation.
4. U.S./Japan/Korea high-resolution customs extensions.
5. Staggered DiD summary.
6. Full robustness appendix.

## 9. November Thesis Plan

The final thesis should be built around three empirical chapters or result
blocks.

### Block 1: Legal treatment and product observability

Question:

> Which legal controls can be measured cleanly in trade data?

Output:

- policy chronology;
- HS/CN crosswalk;
- clean/partial/bundled/sparse classification;
- trade regularity audit;
- donor pool audit.

This makes measurement a contribution, not an apology.

### Block 2: Source-share trade-binding estimates

Question:

> Where does China-source trade fall after the policy window?

Output:

- wave-specific PPML DDD;
- event-time diagnostics;
- product-assignment diagnostics;
- donor sensitivity.

This is the main econometric block, but not the whole thesis.

### Block 3: Mechanism classification

Question:

> When trade-binding appears, does it mean switching, compression, or price
> segmentation?

Output:

- China/RoW/total decomposition;
- exposure/access heterogeneity;
- supplier count/HHI where useful;
- matched price wedges;
- final product typology.

This is the block that answers the reviewers.

## 10. What The Final Contribution Can Be

A strong final contribution would be:

> The thesis shows that China's critical-mineral licensing controls do not have
> a uniform trade effect. Their observed force depends on whether the legal item
> is visible in HS data, whether importers were exposed to Chinese supply,
> whether non-China sourcing channels existed before the control, and whether
> the market adjusted through switching, compression, or price segmentation.

This contribution is credible because it does not overclaim. It does not say
China always succeeds. It does not say licensing is equivalent to a ban. It
does not require license approval data. It turns the reviewers' objection into
the thesis:

> The average effect is less interesting than the conditions under which the
> same legal instrument becomes economically binding.

## 11. Proposed Revised Abstract Logic

Use this logic in the revision:

1. Recent Chinese controls use export licensing, not automatic bans.
2. A legal license may or may not become visible as a trade-binding wedge.
3. The thesis explains heterogeneity in binding across products and importers.
4. It combines source-share PPML DDD with product-scope coding, timing tests,
   source decomposition, exposure/access heterogeneity, and price wedges.
5. Preliminary evidence from HS 282580 shows a large China-source decline with
   timing support and switching-type adjustment.
6. Other products show why the mechanism matters: some are bundled, sparse, or
   timing-limited.
7. The expected contribution is a classification of when licensing controls
   bind, not a claim that all controls reduce trade.

## 12. Practical Recommendation

Keep the project. Do not drop it. But the revised proposal must be more
ambitious conceptually and more modest causally.

The safest high-quality path is:

1. Keep PPML DDD as the main estimator.
2. Make product-scope and importer-adjustment mechanisms central.
3. Add matched price wedges as a mechanism test, not as decorative evidence.
4. Use high-resolution customs data only where HS-6 bundling is the problem.
5. Treat the final output as a typology of binding, switching, compression,
   price segmentation, informative nulls, and measurement-limited nulls.

The thesis should not promise a universal causal estimate of Chinese economic
statecraft. It should promise a careful answer to a harder question:

> Why does the same legal tool become economically visible in some critical
> mineral markets and not in others?
