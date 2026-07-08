# Proposal Defense Speaker Notes

Target time: 5:00.
Hard limit: 7:00.

## Slide 1: Title, 5 seconds

Good morning. My proposal is titled "When Do Critical-Mineral Export Controls Bind?" It studies China's licensing-based controls and why similar legal measures can produce different trade responses across minerals.

## Slide 2: Research Background, 35 seconds

Critical minerals are inputs for chips, batteries, defense, and energy equipment. China is central in many refining and processing stages. The policy setting is export licensing, not automatic export bans. So the research question is not whether a rule exists. The question is why similar licensing controls generate different trade and price disruptions across minerals.

## Slide 3: Literature Review, 40 seconds

The literature gives four pieces. Economic statecraft explains why dependence can become pressure. Export-control documents define the legal treatment and timing. Critical-mineral reports show concentration and restriction risks, but also product heterogeneity. Trade methods show how to estimate source-specific monthly trade with zeros, timing, and few policy shocks. The gap is connecting recent Chinese licensing waves to product-source monthly trade evidence.

## Slide 4: Empirical Design: Data Sources, 55 seconds

The main dataset is UN Comtrade monthly bilateral imports. The current feasibility panel has 53 reporters, 10 HS products, and monthly data from January 2019 to March 2026. The main outcome is import value. I also use China versus rest-of-world imports, total imports, supplier count, and supplier concentration. Auxiliary data cover policy timing, prices, demand cycles, market concentration, and geography.

## Slide 5: Empirical Design: Product Waves, 45 seconds

The treated waves are gallium and germanium in August 2023, graphite in December 2023, antimony in September 2024, and the 2025 expansion for tungsten, bismuth, and related products. The current estimates use three current controls: alumina, manganese, and inorganic acids. The expanded donor candidates are fixed in the data plan, but final use still depends on policy-status, coverage, trade-regularity, and suitability checks.

## Slide 6: Empirical Design: Model, 75 seconds

The main model is a source-contrast PPML triple difference. PPML means Poisson pseudo-maximum likelihood. I use it because import values include zeros, differ by orders of magnitude, and are heteroskedastic. The treatment term is treated product, times China source, times the post-policy import-effect period. Beta is the relative post-policy change in China-sourced imports. The fixed effects absorb baseline sourcing, importer-month shocks, product-month shocks, and source-month shocks.

## Slide 7: Empirical Design: Diagnostics, 45 seconds

The diagnostics map to the hypotheses. H1 is a negative source-contrast PPML coefficient. H2 asks whether the event study shows no systematic pre-policy decline. H3 asks whether the response looks like source switching or import compression. Product scope, price wedges, exposure/access splits, and inference checks decide how strongly each result can be interpreted.

## Slide 8: Preliminary Results, 45 seconds

These are feasibility results from the current 10-product panel. Each row estimates the same PPML model for one treated product against the three current controls: HS 2818, HS 8111, and HS 2811. The clearest case is HS 282580, antimony oxides: the effect is negative, statistically clear in the conditional diagnostic, and the pre-period diagnostic is not rejected. Other products are useful but weaker because they are bundled, sparse, or have rejected pre-period diagnostics.

## Slide 9: Preliminary Results: HS 282580, 50 seconds

This figure shows the event-study pattern for HS 282580. The expected import-effect month is October 2024. The main effect is minus 81.5 percent, with a conditional p-value of 0.002. The pre-period diagnostic is a joint test that the pre-policy event coefficients are zero. It is not rejected, with p equal to 0.680. This is feasibility evidence. It does not prove license denial, welfare loss, or coercive success.

## Slide 10: References, 5 seconds

These are the main sources behind the slides. I can use the backup slides if there are questions about price wedges or the exposure-and-access split.

## One-Sentence Backup Answer

Legal export licensing is not automatically trade-binding, so the thesis tests when China's controls produce a China-source import decline in product-source monthly trade data.
