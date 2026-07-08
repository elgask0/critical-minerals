---
description: "Why graphite controls were effective but Ga/Ge were not — differential effectiveness of China's critical mineral export controls"
created: 2026-06-07
modified: 2026-06-11
group: idea
tags: [project, critical-minerals, export-controls, graphite, gallium, germanium, china, differential-effectiveness]
status: superseded
created_by: opencode
---

# Differential effectiveness in China's critical mineral export controls

> **Status:** Superseded result-development note. The bilateral estimates and
> causal interpretation below predate the canonical Comtrade dimensional
> cleaning and corrected inference. Do not cite its numbers. See
> `Thesis Design.md` and `03_data/output/tables/thesis_*.csv`.

China imposed export licensing requirements on two sets of critical minerals in 2023. The graphite controls (December 2023) produced a **massive, statistically significant drop** in export volumes. The gallium/germanium controls (August 2023) produced **no reduction at all** — in fact, Ga/Ge exports *increased* 318% post-controls. This differential effectiveness is the paper's core finding.

## The empirical fact

| Mineral | Level shift (ln exports) | t-stat | p-value | Pre-trend slope | Pre avg/mo | Post avg/mo | Volume change |
|---------|--------------------------|--------|---------|-----------------|------------|-------------|---------------|
| Natural graphite (HS 2504) | **-6.07** | **-4.85** | **<0.0001*** | +0.05%/mo (p=0.79) | $27.6M | $16.1M | **-41.8%** |
| Artificial graphite (HS 3801) | +0.33 | 0.37 | 0.71 | — | $118.7M | $130.8M | +10.2% |
| Ga/Ge (HS 811292) | -0.03 | -0.01 | 0.99 | **+3.72%/mo (p<0.0001)** | $8.3M | $34.7M | **+318%** |
| GeO₂ (HS 282560) | -0.93 | -1.21 | 0.23 | +0.77%/mo (p<0.001) | $11.2M | $10.9M | -2.7% |

Model: $\ln(\text{Exports}_t) = \alpha + \beta_1 \text{Trend}_t + \beta_2 \text{Post}_t + \beta_3 (\text{Trend} \times \text{Post})_t + \varepsilon_t$

**Key identification asymmetry:** Graphite has a flat pre-trend (R²=0.001 on pre-period alone) — the -42% drop is a clear structural break. Ga/Ge has a strong pre-trend (R²=0.463, +3.72%/month) — the +318% post-treatment is trend continuation, not a treatment effect.

## Why graphite worked and Ga/Ge didn't: three mechanisms

### 1. Design differences in the control regime

Verified official documents (see [[Official Documents]]) reveal critical structural differences:

**Ga/Ge (Announcement No. 23 of 2023):**
- Title verb: **实施** (implement) — explicitly ==NEW controls== on previously unrestricted items
- **No predecessor** — no prior licensing requirement existed for Ga/Ge
- **Identity-based control** — lists substances by chemical name (metallic gallium, GaN, GaAs, Ga₂O₃, GaP, InGaAs, GaSe, GaSb; metallic Ge, zone-refined Ge, ZnGeP, Ge epitaxial, GeO₂, GeCl₄) with "including but not limited to" language covering all forms (wafers, powder, scrap, polycrystal, single crystal, epitaxial)
- ==No purity or performance thresholds== in the announcement text
- 4-week lead time (July 3 → August 1)
- No separate annex — items listed directly in body text
- No pre-existing customs infrastructure for Ga/Ge licensing

**Graphite (Announcement No. 39 of 2023):**
- Title verb: **优化调整** (optimize and adjust) — explicitly framed as ==restructuring existing controls==
- **Predecessor:** Announcement No. 50 of 2006 (in force for 17 years), issued under the nuclear dual-use export-control regulation
- **Performance-threshold control** for synthetic graphite: purity >99.9% AND flexural strength >30 MPa AND density >1.73 g/cm³ — ==all three must be met simultaneously== (confirmed by official MoFCOM FAQ)
- Natural flake graphite and products (spherical, expanded) controlled without numeric threshold
- Paragraph 2 **removes** all other items from 2006 No. 50 — the 2023 regime is a ==narrowing== of prior controls, not an expansion
- Artificial graphite powder, graphite packing/gaskets, and reinforced composites ==explicitly excluded== (per FAQ)
- 6-week lead time (October 20 → December 1)
- 17 years of customs experience administering graphite export licenses (since 2006)

**Implication:** The graphite controls were more credible because: (a) bureaucratic infrastructure existed since 2006, (b) the control was technically targeted (cumulative thresholds) rather than blanket, and (c) the 2023 measure actually *narrowed* the 2006 regime, signaling restraint rather than escalation. The Ga/Ge controls were a novel, formidably broad licensing requirement that customs had no experience implementing — and MoFCOM approved licenses en masse within months (confirmed Nov 30, 2023 press conference).

### 2. Market structure: monopoly vs oligopoly

| Dimension | Ga/Ge | Graphite |
|-----------|-------|----------|
| China market share | 98% Ga, 68% Ge | 65% natural, 90% spherical processing |
| Market size | ~$150M/year | ~$2.5B/year (natural + artificial) |
| Number of alternative suppliers | ~0 for Ga | Mozambique, Brazil, Madagascar |
| Substitutes | None for defense apps | Silicon anodes (emerging, not cost-competitive) |
| Concentration | Extreme monopoly | Processing monopoly, not mining monopoly |

China ==cannot credibly throttle Ga/Ge== because it has 98% of the market. If it denies licenses, buyers have nowhere to go in the short run — but they invest aggressively in alternatives (long-run self-damage). This is the ==commitment problem== in weaponized interdependence: the monopolist's threat is not credible because carrying it out hurts the monopolist most. MoFCOM's own statements confirm this: by November 2023 they were already announcing approved Ga/Ge export licenses, and by December 2023 for graphite — the rhetoric was "not an export ban" (Ga/Ge, Jul 2023) and "not an export prohibition" (graphite, Dec 2023).

Graphite is different: China has 65% of *mining* but 90% of *processing*. Alternative miners exist (Mozambique, Brazil). The controls raise costs for Chinese exporters relative to these alternatives, but they ==don't eliminate the exporter's market==. China can credibly restrict high-purity grades because buyers can still source lower-grade graphite elsewhere and upgrade. Moreover, the 2006 predecessor controls (Announcement No. 50, under the nuclear dual-use regulation) had already established HS code 6815100000 ("non-electrical articles of graphite") as a controlled export category — the customs infrastructure was battle-tested.

### 3. Demand-side dynamics: boom continuation vs real friction

**Ga/Ge exports +318% post-controls** is ==not a treatment effect== — it is the continuation of a pre-existing exponential boom. The data shows:
- 2019 avg: ~$22.5M/semester → 2022-H2: $117M/semester (**×5.2 in 3 years**)
- Pre-trend: +3.72%/month (p<0.0001, R²=0.463) — the trend alone explains nearly half the variance
- Nov-Dec peaks grew exponentially: $16.9M (2021) → $51.8M (2022) → $127.9M (2023) → $218.5M (2024)
- The growth is **consistent across semesters**: 2023-H1=$86.5M, 2024-H1=$100.6M (post-treatment but still growing)
- This is the semiconductor demand boom, not seasonal variation

MoFCOM's own actions confirm the controls were not binding: by November 30, 2023, MoFCOM stated it had "already received and approved some compliant gallium/germanium export applications." The licensing regime created ==bureaucratic friction but not quantity restriction==.

**Graphite -41.8%** reflects real trade disruption:
- Pre-trend was flat (+0.05%/month, p=0.79, R²=0.001)
- November 2023 saw a spike to $51.9M (vs ~$20-34M typical) — ==last-minute stockpiling before December 1==
- December 2023: $4.1M — an **84% drop from November** (the stockpile emptied, then controls bit)
- Recovery was gradual: $7.8M (Jan 2024) → $10.8M (Feb) → $19.3M (Mar) → still below pre-treatment average through 2024
- The slope change coefficient (+0.084, p<0.0001) captures this gradual recovery — but from a massively reduced level

## Theoretical contribution

This finding challenges the weaponized interdependence thesis ([[Farrell & Newman 2019|@farrell_newman_2019]]). The original framework assumes that ==network centrality == coercive leverage==. But the Ga/Ge case shows that extreme centrality (98% monopoly) can ==undermine== coercive leverage because the monopolist faces a commitment problem. The graphite case, where centrality is more moderate (65% mining, 90% processing), shows more effective coercion.

**Important caveat:** This non-monotonic relationship is *consistent with the evidence* from two cases, not *statistically demonstrated* across a range of market structures. With N=2 (graphite effective, Ga/Ge ineffective), we can propose the mechanism but not confirm it. The paper should frame this as:

> "The evidence is consistent with a non-monotonic relationship between market dominance and coercive effectiveness. Moderate dominance (60-90%) may provide more credible leverage than extreme monopoly (>95%), because the monopolist faces a commitment problem — carrying out the threat destroys the monopolist's own market."

The key variable is not ==market share== but ==credible commitment to restriction==. This depends on:
1. **Pre-existing institutional infrastructure** — 17 years of graphite controls (No. 50/2006) vs. novel Ga/Ge licensing
2. **Technical specificity** — cumulative performance thresholds (graphite) vs. blanket identity-based control (Ga/Ge)
3. **Availability of alternatives** — Mozambique/Brazil for graphite vs. ~0 for gallium
4. **Self-damage calculus** — China's graphite exporters face competition; Ga exporters face no alternatives for buyers
5. **Pre-existing market conditions** — flat demand (graphite) amplifies the treatment signal; exponential boom (Ga/Ge) drowns it out

## Implications for the paper

The paper's argument should be reframed as:

> China's 2023 critical mineral export controls had ==differential effectiveness== across minerals. Graphite controls — an optimization of pre-existing regulations dating to 2006, with technically targeted cumulative thresholds — produced a significant drop in export volumes (-41.8%, p<0.001). Gallium/germanium controls — a novel, identity-based licensing regime with no predecessor — coincided with a massive *increase* (+318%, not significant as a reduction) driven by a pre-existing semiconductor demand boom (+3.72%/month, p<0.0001). This differential is consistent with a non-monotonic relationship between market dominance and coercive leverage: extreme monopoly (98% Ga) creates a commitment problem that undermines coercion, while moderate dominance with pre-existing institutional infrastructure (graphite) enables more credible restriction. The finding suggests that the ==effectiveness of economic statecraft is bounded by the weaponizer's own economic interests and institutional capacity==.

## See also

- [[Official Documents]] — verified primary sources with URLs
- [[Context]] — policy episodes and market structure
- [[Methodology]] — shift-share DiD specification
- [[Data]] — HS codes and data sources
- [[@farrell_newman_2019]] — weaponized interdependence framework
