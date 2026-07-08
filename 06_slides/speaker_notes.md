# Speaker Notes

Target time without references: about 8 minutes.

## Slide 1 - Title

Target time: 0:15.

Say: My paper asks when China's critical-mineral export controls actually bind in trade data. I focus on graphite, Gallium-Germanium, and Antimony controls from 2023 and 2024. The core point is simple: a licensing rule is not automatically a collapse in imports from China. I show where the evidence is strongest and where it is weaker.

Transition: I will first give the roadmap so the model does not arrive out of nowhere.

## Slide 2 - Roadmap

Target time: 0:20.

Say: I will start with the policy motivation: why export licensing may or may not matter. Then I explain the research question and the simple logic behind the test. After that I introduce the data and the empirical model in plain language. The final part shows the product results and what they imply.

Transition: The first distinction is that licensing is not the same thing as a ban.

## Slide 3 - Motivation: Licensing Is Not a Ban

Target time: 0:50.

Say: In this paper, a controlled mineral means a product covered by China's export-license rule. That does not mean exports automatically stop. A license can create delays, paperwork, uncertainty, or denial risk. That is why I treat the legal announcement as the start of the question, not as the answer. The timeline shows the expected import-effect months I use for Gallium, Germanium, graphite, and Antimony.

Transition: The next slide turns that motivation into the research question.

## Slide 4 - Research Question

Target time: 0:45.

Say: The research question is when licensing-based controls reduce importers' reliance on China. Wedge means friction. I cannot see this friction directly. I only observe trade flows, so I test whether China-source imports fall in the pattern expected if the license became binding. China exposure means how dependent the importer was on China before the control, adjustment capacity means whether the importer already had non-China suppliers, and product scope means whether the legal control maps cleanly to the trade code.

Transition: To test this, I need data that separates product, importer, source, and month.

## Slide 5 - Data: What the Model Sees

Target time: 0:55.

Say: The data come from monthly UN Comtrade import values from January 2019 through March 2026. The panel has 53 reporting importers, 10 Harmonized System product headings, and two source categories: China and Rest of World, or ROW. ROW means all non-China partners combined. One observation is very concrete: for example, Germany importing HS 282580, Antimony oxides, from China in November 2024, with a dollar value.

Transition: The model asks whether that China-source value changes differently after a product becomes controlled.

## Slide 6 - Empirical Model: What Is Being Compared?

Target time: 1:10.

Say: The full equation is the econometric specification. The simplified version is the intuition: treated product, China source, after policy. Beta asks whether that interaction is negative after controlling for normal country, product, source, and month differences through the fixed effects. In plain English, this is a source-split triple difference: treated versus untreated products, China versus ROW sources, and after versus before the control. If beta is negative, relative China-source import value fell for the treated product.

Transition: The model is estimated with PPML because trade data have many zeros and uneven values.

## Slide 7 - Why PPML?

Target time: 0:45.

Say: PPML stands for Poisson pseudo-maximum likelihood. Even though the name sounds like counts, here PPML models trade values. It is useful because many country-product-source-month flows are zero, and trade values are extremely uneven. PPML keeps those zero flows in the regression and lets the coefficient be translated into a percent effect. For example, beta around minus 1.69 corresponds to about minus 81.5 percent.

Transition: With that setup, the first result is that effects are selective across products.

## Slide 8 - Product-Level Results: Effects Are Selective

Target time: 1:10.

Say: This table is the main scorecard. A pretrend asks whether the treated and comparison flows were already moving differently before the control; if that check fails, the result is harder to interpret. The clean central case is HS 282580, Antimony oxides, with a negative 81.5 percent effect and a pretrend p-value of 0.680. HS 8110, Antimony metal, and HS 261710, Antimony ores, are also negative, but their pretrends fail, and the ores market is sparse. The Gallium/Germanium-related HS codes show no aggregate negative effect, which is different from saying there was no effect on every controlled item inside those broad codes.

Transition: The next slide shows why Antimony oxides carry most of the interpretation.

## Slide 9 - Central Case: HS 282580 (Antimony Oxides)

Target time: 1:15.

Say: For Antimony, the announcement was August 2024, implementation was September, and the expected import effect is October. I use July, \(t=-3\), as the baseline because it is before announcement and implementation. This avoids using the announcement or effective months as the comparison point. The x-axis is event time, meaning months relative to October 2024. The pretrend p-value is 0.680, and negative values mean China-source import value fell relative to ROW and control products.

Transition: The final empirical slide asks which importers adjust most.

## Slide 10 - HS 282580: Who Adjusts?

Target time: 1:05.

Say: Switching potential is measured before the antimony control. The high-A group is not mechanically rich countries or large importers. It means countries that were exposed to China but already had non-China supply links for that product before the control. I split importers into high and low switching potential and re-run the same model for HS 282580, Antimony oxides. The high switching-potential group has a negative 87.4 percent relative effect, while the low switching-potential group has no China-source decline; this supports a source-switching interpretation for antimony oxides.

Transition: I close with the implications for how to read licensing controls.

## Slide 11 - What Should We Learn?

Target time: 0:55.

Say: The first lesson is not to infer disruption from legal coverage alone. Countries with non-China suppliers can shift sourcing more easily. Product scope also matters because HS product codes can mix controlled and uncontrolled items together. The main limitation is that observed import value cannot tell us separately about prices, quantities, rerouting, inventories, or demand. The result is selective, not universal: one clean product effect, several caveated or null cases.

Transition: If there is time, I can briefly point to the references behind the policy dates, data, and interpretation.

## Slide 12 - Key References

Target time: skip or 0:15.

Say: This slide is mostly for transparency. The official MOFCOM and GAC announcements provide the legal dates and product scope, while UN Comtrade provides the monthly import data. IEA and USGS motivate the mineral-concentration background. Farrell and Newman, Bown, Bown and Wang, and Roth provide the conceptual and empirical context.

Transition: End after the main conclusion unless someone asks about sources.
