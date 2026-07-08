# ADVERSARIAL REVIEW PROMPT

You are a senior applied-microeconomics advisor (think: a demanding thesis
committee chair who has supervised many international-trade / economic-statecraft
papers, reads *AER*, *REStat*, *JoE*, and *International Security* regularly, and
cares about identification, honest inference, and clean writing). I am giving you
my term paper as a PDF. Your job is to tear it apart, constructively but
brutally, so I can fix it now and then extend it into my master's thesis.

**Stance to adopt.** Assume nothing is correct until you have checked it. Do not
praise. Do not summarize the paper back to me. Find every weakness you can:
identification holes, mis-specified or mis-described empirical models, broken
logic in the theoretical framework, numbers that do not line up, claims that
overstate the evidence, missing results that I could produce with the data I
already have, redundancy, and grammar. I want the harshest, most specific review
you can write. Where you can, give the *exact* fix (the specification to run, the
sentence to cut, the table to add, the robustness check to implement).

## What this paper is (and is not)

- It is a **course term paper** for "Introduction to China's Foreign Trade and
  Investment," to be extended later into a **master's thesis**. It is NOT a
  journal submission. Judge it against that bar, but tell me clearly which of
  your points are "fix now for the term paper" vs "thesis extension."
- Research question: *When do China's licensing-based critical-mineral export
  controls reduce importers' reliance on China, and how do product scope and
  importer adjustment capacity shape the answer?*
- Core claim: the controls are **licensing regimes, not bans**; a binding
  licensing wedge should reduce China-source imports relative to rest-of-world
  (ROW) and to untreated products. The effect should vary across products.

## Data I actually have (so your suggestions stay feasible)

- **UN Comtrade** monthly bilateral imports, **2019-01 to 2026-03 (87 months)**,
  **53 reporting countries**, **10 products**. Built only from the canonical
  aggregate rows (partner2=0, customs=C00, mode-of-transport=0, mode-of-shipment=0).
  Each flow split into **China** vs **ROW**. Primary outcome: **monthly trade
  value in USD** (net weight is incomplete for several products).
- Treated products: HS 2504 (natural graphite), 811292 (Ga/Ge/In/V/Nb bundle),
  282560 (GeO2/ZrO2), 8110 (antimony metal), 261710 (antimony ores), 282580
  (antimony oxides).
- Control products: HS 2818 (alumina), 8111 (manganese), 2811 (inorganic acids).
- Descriptive only: HS 3801 (artificial/colloidal graphite, partially treated).
- **Eurostat Comext CN8**, current EU27, 72 months: unwrought Ga and Ge
  (controlled) vs unwrought In and V (within-bundle comparators). Sparse.
- **Switching-potential index** $A_{ik}=E_{ik}\times O_{ik}$ from pre-period
  (China exposure × ROW access), computed per importer-product.
- **China-reported aggregate exports** (for a descriptive exporter
  interrupted-time-series check).
- CEPII GeoDist dyadic controls are available but not used in the main spec.

**Data I do NOT have (yet):** exact-grade domestic vs international price pairs
(Bloomberg is partial; exact-grade matching incomplete), downstream demand
indicators (semiconductors, batteries, steel), license approval/denial
microdata, inventory data.

## Hard rules I must respect (please respect them, BUT challenge them if you think one is wrong for the thesis)

- The model is **reduced-form**. I cannot claim enforcement intensity,
  license-denial probabilities, inventories, coercive success, welfare, or
  strategic intent.
- I must **not pool** antimony ores/metal/oxides.
- HS 3801 is **not a placebo** (partially treated).
- Language discipline: use "supports" **only** for the HS 282580
  switching-potential pattern; "consistent with" for graphite and antimony
  metal; "descriptive only" for HS 261710; "no aggregate negative effect" for
  the Ga/Ge codes.
- Out of scope for the term paper (thesis extensions): SCM, Synthetic DiD,
  Matrix Completion, CausalImpact, Callaway–Sant'Anna, Rambachan–Roth, and a
  price DiD. Do not ask me to put these in the term-paper main text, but tell me
  which should be the FIRST thesis extensions.

## The empirical spine (use these to check internal consistency)

- Inference floor: treatment is at the product-month level, 1 treated + 3
  control products per comparison ⇒ minimum exact product-assignment p-value =
  **0.25**. Reporter-clustered p-values are conditional diagnostics only.
- Static source-share PPML DDD (% effect; reporter p; joint pretrend p):
  - HS 282580 antimony oxides: **−81.5%**, p=0.0025, pretrend p=0.680 (central).
  - HS 8110 antimony metal: −86.8%, p<0.001, pretrends fail.
  - HS 261710 antimony ores: −98.9%, p=0.0033, sparse, descriptive only.
  - HS 2504 graphite: −30.4%, p=0.107, pretrend fails (suggestive).
  - HS 811292 Ga/Ge bundle: +19.3%, p=0.365.
  - HS 282560 GeO2/ZrO2: +17.5%, p=0.271.
- HS 282580 event study: pre-period ≈ 0; p1 −55.4%; p4–6 −71.7%; p7–12 −90.2%;
  p13+ −94.6% (deepens over time).
- HS 282580 switching split: high-A −87.4% (p<0.001, pretrend 0.354);
  low-A +103.1% (p=0.035, pretrend 0.161).
- Substitution/compression (HS 282580, post vs pre): China −27.7%, ROW +315.2%,
  total +135.7% ⇒ switching/expansion, not compression.
- Eurostat CN8: Ga vs In/V −59.8% (p=0.307); Ge vs In/V +25.1% (p=0.419);
  pooled Ga/Ge vs In/V −32.7% (p=0.355).

## What I want from you — critique across these dimensions

1. **Theoretical model.** Is the licensing-wedge model coherent? Are the
   equations internally consistent and correctly mapped to the PPML estimand? Is
   the link between the latent wedge $W_{kt}$ and the coefficient $\beta_k$
   honest? Is the magnitude mapping $100(e^{\beta_k}-1)$ applied correctly? What
   is missing or hand-wavy? Where would a slightly richer model (still
   reduced-form) buy real explanatory power without overclaiming?
2. **Empirical strategy & identification.** Scrutinize the source-share triple
   difference (the fixed-effects structure, the source split, the timing of
   "Post", the placebo/donor choice). Is identification credible given the
   constraints? What are the real threats (anticipation/stockpiling, rerouting,
   demand shocks, HS-code aggregation, endogenous policy timing)? Which threats
   can I test with the data I have?
3. **Inference.** Is the p≥0.25 floor handled honestly? Is the reliance on
   reporter-clustered p-values defensible? Should I report anything else
   (wild-cluster bootstrap, adjacency/inference-on-count, Conley spatial)? Am I
   over- or under-stating anywhere?
4. **Results, heterogeneity, robustness.** What robustness checks are missing
   that I **can run with the current data** (leave-one-product-out,
   leave-one-importer-out, alternative placebo sets, announcement vs
   implementation timing, alternative pre-period windows, excluding re-export
   hubs, net-weight complete-case, winsorizing, alternative $A_{ik}$
   thresholds)? What heterogeneity margins am I leaving on the table (e.g.,
   geography, EU vs non-EU, BRI vs non-BRI, reporter income, exposure
   quartiles)? Are the event-study bins optimal?
5. **Missing results that are feasible.** Given the data inventory, which
   additional tables/figures would materially strengthen the paper at term-paper
   cost? (e.g., a clean event-study figure, source-trend figure, a first-stage
   on China exposure, a placebo-date test, a dose-response in $A_{ik}$.)
6. **Internal consistency & number-checking.** Cross-check every number in the
   text against the tables and against the spine above. Flag any mismatch, any
   sign error, any place a percentage is mis-stated, any table that does not
   support the sentence citing it.
7. **Writing, grammar, structure.** Flag grammar errors, awkward or unclear
   sentences, redundant paragraphs, anything that should be **trimmed** or
   **expanded**, and any place the logic jumps. The top priority is clarity for
   a reader who is not a mineral-policy specialist.
8. **Overclaims and under-claims.** Where do I go too far? Where am I too
   hedging and could state something more forcefully? Is the language discipline
   (supports / consistent with / descriptive only / no aggregate effect)
   applied correctly throughout?

## Output format

Give me:
- A **prioritized punch-list**: (A) must fix for the term paper now, (B) add for
  the thesis. Each item: the problem, the exact fix, and the section/table/line.
- A **"biggest 3 risks"** shortlist: the three things that most weaken the paper.
- A **feasible-extensions** list: concrete extra results I can produce from the
  data I already have, ranked by payoff.
- **Line-level edits**: specific grammar/clarity fixes with the original phrase
  and the replacement.

Be specific, be harsh, be useful. Do not pad the review with generic advice.
