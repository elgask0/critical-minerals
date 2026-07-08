---
description: "Policy episodes, mineral market structure, and geopolitical backdrop for China's critical mineral export controls"
created: 2026-06-04
modified: 2026-06-09
group: structure
tags: [project, critical-minerals, context, policy, china]
status: active
created_by: opencode
---

# Context

## The Policy Episodes

China imposed export licensing requirements on five critical mineral categories between July 2023 and April 2025. Each was announced by the Ministry of Commerce/General Administration of Customs, citing China's Export Control Law (effective December 1, 2020) and "national security."

### Episode 1: Gallium and Germanium (Aug 2023)

- **Announced**: July 3, 2023
- **Effective**: August 1, 2023
- **Products**: Metallic gallium; GaN, Ga₂O₃, GaP, GaAs, InGaAs, GaSe, GaSb (all forms: wafers, powder, scrap, polycrystal, single crystal, epitaxial); metallic germanium, zone-refined Ge ingots, ZnGeP, Ge epitaxial substrates, GeO₂, GeCl₄
- **Control logic**: Identity-based (chemical name + form), ==no purity thresholds==
- **HS codes (6-digit)**: 811292 (Ga + Ge + In + V + Nb bundled), 282560 (GeO₂ + ZrO₂ bundled)
- **China market share**: ~98% gallium, ~68% germanium
- **Trigger**: Widely interpreted as retaliation for U.S. semiconductor export controls (Oct 2022, updated Oct 2023)
- **Key framing**: Title uses 实施 (implement) — signaling ==new== controls on previously unrestricted items
- **Licensing**: Approved licenses confirmed by MoFCOM as early as November 30, 2023 ("not an export ban")
- **Empirical result**: +318% export volume post-controls (not significant as reduction). Pre-trend +3.72%/month (p<0.0001) — boom continuation, not treatment effect. Shift-share DiD fails placebo test (fake Jan 2022: beta=+1.13, p=0.013).

### Episode 2: Graphite (Dec 2023)

- **Announced**: October 20, 2023
- **Effective**: December 1, 2023
- **Predecessor**: Announcement No. 50 of 2006 (17 years of prior controls, repealed by No. 39)
- **Products controlled**: Synthetic graphite meeting cumulative thresholds (>99.9% purity AND >30 MPa flexural strength AND >1.73 g/cm³ density); natural flake graphite and products (spherical, expanded). ==Not all graphite== — powder, packing, gaskets, reinforced composites excluded (per MoFCOM FAQ)
- **HS codes**: 2504 (natural), 3801 (artificial + colloidal)
- **China market share**: ~65% natural graphite production, ~90% spherical graphite processing for EV battery anodes
- **Trigger**: Announced one week after U.S. expanded semiconductor export controls (Oct 17, 2023)
- **Key framing**: Title uses 优化调整 (optimize and adjust), not 实施 (implement) — signaling continuity, not new restriction
- **Empirical result**: -41.8% export volume (p<0.001), flat pre-trend (+0.05%/mo, p=0.79). November 2023 spike ($51.9M) suggests stockpiling before effective date; December 2023 collapse to $4.1M. Gradual recovery but still below pre-treatment average.

### Episode 3: Antimony (Sep 2024)

- **Official measure**: MoFCOM/GAC Announcement No. 33 of 2024
- **Announced**: August 15, 2024
- **Effective**: September 15, 2024
- **Products**: Antimony metal, trioxide, ores/concentrates, gold-antimony ore, processing equipment
- **HS codes**: 8110 (metal), 2617 (ores), 2825.80 (oxides)
- **China market share**: ~48% mine production, ~70% processing
- **Notable**: Explicit inclusion of military applications (armor-piercing ammunition, infrared sensors)
- **Pre-existing trend**: China's antimony exports were already declining 3-5%/yr due to reserve depletion (Xikuangshan mine aging)

### Episode 4: Tungsten, Bismuth, Tellurium (Feb 2025)

- **Announced and effective**: February 4, 2025
- **Products (confirmed from Ann. 10/2025 official text)**:
  - Tungsten: APT (284180), W oxides (282590), WC (284990), solid W≥97% with dimension requirements (8101)
  - Bismuth: ALL forms of Bi metal (8106, all sub-codes), BGO (284190), organic Bi compounds (293190)
  - Tellurium: Te metal (280450), CdTe/CZT/MCT crystals
  - Molybdenum: ONLY Mo powder for missile parts, Mo≥97%, ≤50μm (8102, extremely narrow)
  - Indium: InP, trimethyl/triethyl In only (285390, 293190). **In metal NOT controlled.**
- **HS codes (at HS-6, clean)**: 8106 (Bi, all forms), 284180 (APT/tungstates)
- **HS codes (at HS-6, partial)**: 8101 (W, specific forms), 280450 (Te+B)
- **HS codes (DROPPED)**: 8102 (Mo, only missile-grade powder ~1-5% of trade)
- **China market share**: ~85% tungsten mining, ~60% bismuth, ~70% Te
- **Notable**: Mo control is extremely narrow (missile end-use + specs); In metal not controlled; W has dimension requirements excluding powder/wire/scrap

### Episode 5: Rare Earth Elements (Apr 2025) — Marginal

- **Announced**: April 4, 2025
- **Effective**: April 2025
- **Products (confirmed from Ann. 18/2025 official text)**: Sm, Gd, Tb, Dy, Lu, Sc, Y — metals, alloys, targets, oxides, and compounds with extensive CN-10 sub-code listings
- **HS codes**: 280530 (REE metals, partial), 284690 (non-cerium REE compounds, partial)
- **China market share**: ~70% mining, ~85-90% processing
- **Exclusion reason**: At HS-6, controlled REEs are a fraction of total trade (La, Pr, Nd NOT controlled). Too diluted for main analysis.
- **Placebo**: 284610 (cerium compounds, NOT controlled)

### Episode 6: Li batteries, synthetic graphite anode (Nov 2025) — Excluded

- **Announced**: ~October 2025
- **Effective**: November 2025
- **Products**: Li-ion batteries, synthetic graphite anode materials
- **HS codes**: 380110 (already partially treated in 2023), 8507 (too broad)
- **Exclusion reason**: Announcement 70/2025 suspended the proposed November
  2025 measures before implementation. HS 380110 remains contaminated by the
  2023 graphite regime, while HS 8507 has no implemented treatment and a
  massive underlying growth trend.

## Mineral Market Structure

### Why China dominates

Three structural factors explain China's dominance in critical mineral processing:

1. **Deliberate industrial policy** — Decades of state investment in processing capacity, export rebates, and below-market pricing that drove competitors out of business (Mancheri, 2015)
2. **Byproduct economics** — Gallium (from bauxite), germanium (from zinc), many REEs (from ion-adsorption clays) are byproducts. China processes the primary metals at scale, making byproduct recovery economical. New entrants face the chicken-and-egg problem of needing primary metal capacity first (Frenzel et al., 2017)
3. **Environmental arbitrage** — REE processing generates toxic and radioactive waste. China's historically weaker environmental enforcement lowered production costs. Catching up on regulation is raising costs but not enough to erode the dominant position

### Mineral-specific demand drivers

| Mineral | Primary demand | Key downstream industries |
|---------|---------------|--------------------------|
| Gallium | GaAs/GaN wafers, LEDs | Semiconductors, 5G, defense radar |
| Germanium | Fiber optics, IR optics, SiGe chips | Telecommunications, night vision, satellite |
| Graphite | EV battery anodes (spherical graphite) | Electric vehicles, energy storage |
| Antimony | Flame retardants, lead-acid batteries, munitions | Construction, automotive, defense |
| REE | NdFeB magnets (Nd, Dy, Tb) | EV motors, wind turbines, precision-guided munitions |

### Substitutability

- **Gallium**: No practical substitute for GaAs in high-frequency/defense applications. GaN can be produced from recycled Ga but capacity is limited
- **Germanium**: Silicon can substitute in some fiber optic applications but with performance loss. No substitute for IR optics
- **Graphite**: Silicon anodes are emerging but not yet cost-competitive. Synthetic graphite exists but requires petroleum coke (also energy-intensive)
- **Antimony**: Halogenated flame retardants can partially substitute but face their own regulatory restrictions
- **REE**: Long-term R&D into recycling and alternatives but 10-15 year timeline for significant substitution

## Geopolitical Context

The 2023-2025 export controls did not emerge in isolation. They are part of a tit-for-tat escalation:

| Date | U.S./Allied action | China's response |
|------|-------------------|-----------------|
| Oct 2022 | U.S. semiconductor export controls (advanced chips, equipment) | — |
| Jan 2023 | Japan/Netherlands align with U.S. on equipment controls | — |
| May 2023 | U.S. updates semiconductor controls (expand scope) | — |
| Jul 2023 | — | Ga/Ge export controls announced |
| Oct 2023 | U.S. expands semiconductor controls again | Graphite controls announced (1 week later) |
| Aug 2024 | — | Antimony controls announced |
| Dec 2024 | U.S. restricts advanced memory chips | — |
| Apr 2025 | — | REE controls announced |

This tit-for-tat pattern supports the "weaponized interdependence in reverse" framing: China is using its supply-side leverage as a symmetric response to U.S. demand-side leverage.

## Concurrent shocks (confounds)

| Shock | Period | Minerals affected | Identification concern |
|-------|--------|-------------------|----------------------|
| COVID-19 trade collapse | 2020 H1 | All | V-shaped recovery in 2021 makes 2020 unreliable |
| Semiconductor shortage/boom | 2021-2022 | Ga, Ge primarily | Demand-driven trend break |
| REE price spike (Myanmar coup) | Feb 2021 | REE | Myanmar supplies ~50% of China's heavy REE feedstock |
| China COVID reopening | Jan 2023 | All | One-time level shift, confounds Ga/Ge Aug 2023 treatment |
| EV demand surge | 2021-2023 | Graphite primarily | Upward demand trend before Dec 2023 controls |
| China environmental inspections | 2021-2022 | Graphite, antimony | Domestic supply restriction independent of export controls |

## Current Empirical Status

The corrected thesis panel does not confirm the earlier term-paper claim of a
59% causal graphite decline. That estimate summed overlapping raw Comtrade
dimensions and used HC1 inference.

| Evidence | Current result | Interpretation |
|---|---:|---|
| Graphite exporter ITS, HAC(6) | -47.8%, p=0.0017 | Strong descriptive implementation break |
| Graphite source-share PPML | -30.8%, p=0.217 | Correct direction, not confirmatory |
| Graphite first arrival month | about -54%, p=0.169 | Sharp temporary disruption |
| Ga/Ge source-share PPML | +27.9%, p=0.111 | No negative average effect; pretrends fail |
| Eurostat Ga source-share PPML | -59.8%, p=0.307 | Sparse and imprecise |
| Eurostat Ge source-share PPML | +25.1%, p=0.419 | Sparse and imprecise |

P-values above are reporter-clustered conditional diagnostics. Each main
comparison currently contains only one treated and three placebo products, so
exact product-level assignment inference cannot attain a p-value below 0.25.

The current comparative interpretation is:

- graphite shows a credible short-run implementation disruption, but
  persistence is not yet established;
- Ga/Ge do not show a stable negative average effect and have problematic
  pretrends;
- policy design, market structure, self-cost, and downstream demand remain
  competing explanations;
- the commitment mechanism is "consistent with" only if trade, price, and
  adjustment predictions align after the remaining data are added.

The canonical framework and full results are in `Thesis Design.md`.
