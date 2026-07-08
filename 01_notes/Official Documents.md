---
description: "Verified and working official Chinese government documents on critical-mineral export controls"
created: 2026-06-07
modified: 2026-06-27
group: source
tags: [project, critical-minerals, export-controls, china, mofcom, primary-sources]
status: active
created_by: opencode
---

# Official Documents — China Critical Mineral Export Controls

This note is the repository control file for official Chinese policy
documents. It consolidates the verified 2023 episodes, the antimony episode,
and later U.S.-destination measures from `/Users/elgask0/Downloads/mofcom.md`.
It also records corrections to that downloaded report.

Use this note for treatment timing and legal-design language. Use
`01_notes/Data.md` for data coverage and HS-code download status.

## Corrections To The Downloaded MOFCOM Report

The downloaded `mofcom.md` report is a useful discovery source, not a frozen
policy dataset. These corrections are binding for the project:

- **GeO2 code correction:** Announcement No. 23/2023 assigns germanium dioxide
  to reference code `2825600002`. The downloaded report incorrectly lists
  `2825800010`. The latter belongs to high-purity antimony oxides under
  Announcement No. 33/2024.
- **GeO2 code nuance:** Chinese tariff lookups distinguish `2825600001`
  as broader "germanium oxides" and `2825600002` as specifically germanium
  dioxide (`二氧化锗`). For policy coding, use the official Announcement
  No. 23/2023 reference code `2825600002` for GeO2 and the HS-6 heading
  `282560` in Comtrade.
- **HS-6 implication:** GeO2 remains in HS `282560`, bundled with ZrO2 in
  Comtrade. Antimony oxides belong to HS `282580`.
- **Graphite-anode 2025 correction:** Announcement No. 58/2025 should not be
  coded as an implemented treatment unless the suspension is explicitly
  handled. Announcement No. 70/2025 suspended Announcements 55-58 and 61-62 on
  November 7, 2025, before the scheduled November 8, 2025 implementation,
  through November 10, 2026.
- **2006 graphite source correction:** Announcement No. 50/2006 is available
  on the MOFCOM export-control site. A local capture exists, but the
  controlled-item table is image-based and still needs manual verification
  before exact product-scope quotation.
- **Periodization:** Announcement No. 46/2024 and Announcement No. 72/2025 are
  later U.S.-destination measures. They should not be mixed into the baseline
  country-neutral 2023-2024 licensing treatments.

## Core Legal Framework

### Export Control Law of the PRC

- **Official text:** https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/flfg/202111/226.html
- **State Council white paper (English):** https://english.www.gov.cn/archive/whitepaper/202112/29/content_WS61cc01b8c6d09c94e48a2df0.html

Correct article mapping:

| Topic | Correct Article | What it does |
|---|---:|---|
| Temporary controls | Article 9 | Controls on items not on the list, maximum two years, State Council approval |
| Review factors for licenses | Article 13 | National security, international obligations, end-use, item sensitivity, destination |
| General licenses | Article 14 | Facilitation for compliant exporters |
| End-use proof | Article 15 | Final-user and final-use documentation |
| Re-export/transit | Article 45 | Transit, transshipment, re-export, bonded zones covered |
| Reciprocal measures | Article 48 | Countermeasures against countries abusing export controls |
| Extraterritorial liability | Article 44 | Liability for overseas organizations and individuals |

## Policy Chronology For Current Project

| Date | Event | Empirical use | Source status |
|---|---|---|---|
| 2006-07-27 | Announcement No. 50/2006 introduces temporary controls on certain graphite-related products | Pre-existing graphite licensing infrastructure | Local source captured; item table needs manual verification |
| 2023-07-03 | Announcement No. 23/2023 announced for gallium and germanium items | Announcement month for Ga/Ge | Verified official source |
| 2023-08-01 | Ga/Ge controls take effect | Exporter implementation month | Verified official source |
| 2023-09-21 | MOFCOM states compliant Ga/Ge applications had been approved | Evidence licensing was not an automatic ban | Official press evidence |
| 2023-10-20 | Announcement No. 39/2023 announced for graphite | Announcement month for graphite | Verified official source |
| 2023-12-01 | Graphite controls take effect and No. 50/2006 is repealed | Exporter implementation month | Verified official source |
| 2024-01-18 | MOFCOM states compliant graphite applications had been approved | Evidence licensing was not an automatic ban | Official press evidence |
| 2024-08-15 | Announcement No. 33/2024 announced for antimony and superhard materials | Announcement month for antimony | Verified official source; local capture available |
| 2024-09-15 | Antimony/superhard controls take effect | Exporter implementation month | Verified official source; local capture available |
| 2024-12-03 | Announcement No. 46/2024 tightens controls for U.S.-destination dual-use exports | Later destination-specific policy stage | Verified official source; local capture available |
| 2024-12-05 | MOFCOM reports antimony applications received and under review | Antimony licensing evidence | Verified official press source; local capture available |
| 2025-02-04 | Announcement No. 10/2025 covers tungsten, tellurium, bismuth, molybdenum, indium | Thesis expansion candidate | Verified official source; HS crosswalk still needs coding |
| 2025-04-04 | Announcement No. 18/2025 covers medium/heavy rare earth items | Thesis expansion candidate | Verified official source; HS crosswalk still needs coding |
| 2025-11-07 | Announcement No. 70/2025 suspends Announcements 55-58 and 61-62 before implementation | Prevents false lithium/graphite-anode treatment coding | Verified official source; local capture available |
| 2025-11-09 | Announcement No. 72/2025 suspends paragraph 2 of No. 46/2024 through Nov. 27, 2026 | Current-through-2026 U.S. policy chronology | Verified official source; local capture available |

The proposal baseline should focus on the country-neutral 2023-2024 regimes:
Ga/Ge, graphite, and antimony. Later U.S.-specific measures can be used as
context, not as the main treatment unless the empirical design explicitly adds
destination-specific outcomes.

## Announcement No. 23 of 2023 — Gallium And Germanium

- **Title:** 商务部 海关总署关于对镓和锗相关物项实施出口管制的公告
- **Effective:** August 1, 2023
- **MOFCOM main:** https://www.mofcom.gov.cn/zcfb/dwmygl/art/2023/art_52b9a321087f402bb3d310d18b07967e.html
- **MOFCOM export-control mirror:** https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202307/847.html
- **Licensing guide (PDF):** https://egov.mofcom.gov.cn/xzxksx/18017/18017_11.pdf

Key features:

- Framing verb: 实施, meaning implementation of a new control regime.
- No predecessor announcement is cited.
- Control logic is identity-based: listed substances by chemical name and
  form, without a broad performance-threshold test.
- The announcement covers metallic gallium, gallium compounds, metallic
  germanium, germanium compounds, GeO2, and GeCl4.
- The relevant HS-6 aggregates in the current Comtrade work are mainly
  `811292` and `282560`, both with partial-treatment risk.

Licensing requires the usual dual-use export-control materials: export
contract, technical description or test report, final-user and final-use proof,
importer and ultimate-user information, and assurances against unauthorized
end-use change, third-party transfer, and WMD use.

## Announcement No. 39 of 2023 — Graphite

- **Title:** 商务部 海关总署关于优化调整石墨物项临时出口管制措施的公告
- **Effective:** December 1, 2023
- **Repeals:** Announcement No. 50 of 2006
- **MOFCOM main:** https://www.mofcom.gov.cn/zcfb/blgg/art/2023/art_f6b1bc49e2c8482f8eb749012bc66dec.html
- **MOFCOM export-control mirror:** https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202310/912.html
- **Licensing guide (PDF):** https://egov.mofcom.gov.cn/xzxksx/18017/18017_12.pdf
- **Official FAQ:** https://exportcontrol.mofcom.gov.cn/article/cjwt/202403/974.html

Key features:

- Framing verb: 优化调整, meaning optimization/adjustment of an existing
  temporary-control regime.
- The announcement explicitly cites and repeals Announcement No. 50/2006.
- Controlled artificial graphite must satisfy all three cumulative thresholds:
  carbon purity above 99.9%, flexural strength above 30 MPa, and density above
  1.73 g/cm3.
- Natural flake graphite and its products, including spherical and expanded
  graphite, are controlled.
- The official FAQ clarifies that artificial graphite powder and reinforced
  graphite composite products are outside the controlled scope.

This is not a clean blanket expansion. It is a restructuring of an older
temporary-control regime, with both newly specified controlled high-grade items
and the removal of other 2006 items.

## Announcement No. 50 of 2006 — Graphite Predecessor

- **Title:** Decision to Implement Temporary Export Control Measures on
  Graphite-related Products
- **Issued:** July 27, 2006
- **MOFCOM export-control site:** https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202111/432.html
- **Legal basis:** Article 17 of the Regulations on Export Control of Nuclear
  Dual-Use Items

Project use:

- Establishes that graphite had administrative precedent before 2023.
- Supports the interpretation that No. 39/2023 was an optimization of an
  existing regime rather than a wholly new licensing category.
- Local capture exists, but the image-like item table still needs manual
  verification before final citation of exact product scope.

## Announcement No. 33 of 2024 — Antimony And Superhard Materials

- **Title:** 商务部 海关总署公告2024年第33号 关于对锑等物项实施出口管制的公告
- **Published:** August 15, 2024
- **Effective:** September 15, 2024
- **Export-control source:** https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202408/1024.html

Empirical antimony codes for the current project:

| HS code | Product stage | Treatment interpretation |
|---|---|---|
| `8110` | Antimony metal and articles | Cleanest refined-metal HS family; all HS-6 children are antimony forms |
| `261710` | Antimony ores and concentrates | Clean upstream ore/concentrate code |
| `282580` | Antimony oxides | Partial treatment at HS-6 because the legal control targets high-purity antimony oxides |

Announcement No. 33/2024 also covers narrower antimony-related products and
technologies, including organometallic antimony compounds, stibine, and
equipment/technology for superhard materials. These are important for legal
scope but are not yet part of the main Comtrade panel.

Antimony should be analyzed as a value-chain case, not as one pooled product:
ore/concentrate, metal, and oxide can plausibly have different trade responses.

## Later U.S.-Destination Measures

### Announcement No. 46 of 2024

- **Title:** 商务部公告2024年第46号 关于加强相关两用物项对美国出口管制的公告
- **Published/effective:** December 3, 2024
- **Official URL:** https://www.mofcom.gov.cn/zwgk/zcfb/art/2024/art_3d5e990b43424e60828030f58a547b60.html

Project interpretation:

- This is a destination-specific escalation targeting the United States.
- It is not the same treatment as the earlier country-neutral Ga/Ge, graphite,
  and antimony licensing measures.
- It can be discussed as context for the strategic environment, but it should
  enter empirical work only through a destination-specific design.

### Announcement No. 72 of 2025

- **Title:** 商务部公告2025年第72号 公布调整实施商务部公告2024年第46号的决定
- **Published/effective:** November 9, 2025
- **Official URL:** https://www.mofcom.gov.cn/zwgk/zcfb/art/2025/art_5c68985a6b1a46778e2e8dbff1bb1601.html

Project interpretation:

- Suspends the second paragraph of Announcement No. 46/2024 from November 9,
  2025 through November 27, 2026.
- Relevant for keeping the chronology current through June 2026.
- More important for thesis extension than for the immediate proposal baseline.

## Official English-Language Statements

- **July 6, 2023 press conference:** https://english.mofcom.gov.cn/News/PressConference/art/2023/art_36fb2d80e4b4453891bb8fc83e2b3c4e.html
- **Nov. 30, 2023 press conference:** https://english.mofcom.gov.cn/News/PressConference/art/2023/art_cd46d6e56bb6486a928ea2f16182ae90.html
- **Dec. 14, 2023 graphite applications statement:** https://english.mofcom.gov.cn/News/PressConference/art/2024/art_611ccb87a71c41f493dae33c79ad5268.html
- **Jan. 18, 2024 graphite applications statement:** https://english.mofcom.gov.cn/News/PressConference/art/2024/art_7e1282d1fc37494aaa51bc84bb9b8014.html
- **Dec. 5, 2024 antimony applications statement:** https://english.mofcom.gov.cn/News/PressConference/art/2024/art_154e2df66a0e424c84307c680986fc47.html

These statements are useful because they show that MOFCOM publicly described
the regimes as licensing controls rather than blanket export bans. They do not
provide approval counts, destination breakdowns, denial counts, or processing
times.

## Structural Comparison For The Proposal

| Dimension | Ga/Ge (No. 23/2023) | Graphite (No. 39/2023) | Antimony (No. 33/2024) |
|---|---|---|---|
| Effective date | Aug. 1, 2023 | Dec. 1, 2023 | Sep. 15, 2024 |
| Legal framing | New implementation | Optimization/adjustment of temporary graphite controls | New implementation |
| Predecessor | None identified | No. 50/2006 | None identified for antimony |
| Product logic | Identity-based chemicals/forms | Performance thresholds plus natural flake products | Value-chain materials plus selected compounds/equipment |
| Main empirical HS codes | `811292`, `282560` | `2504`, descriptive `3801` | `8110`, `261710`, `282580` |
| Partial-treatment risk | High at HS-6 | High for `3801`; lower for natural graphite `2504` | Low for `8110`/`261710`; higher for oxide `282580` |
| License evidence | Approvals reported | Approvals reported | Applications received/under review reported |
| Main interpretation risk | Byproduct/demand contamination; HS aggregation | Existing regime and technical narrowing | Short post-treatment window before March 2026 |

## Empirical Coding Guidance

- Use announcement month and implementation month separately.
- For importer-arrival outcomes, allow at least a one-month shipping lag in
  event-time interpretation.
- Do not infer coercive intent or effectiveness from legal text alone.
- Treat public license statements as implementation evidence, not as
  quantitative approval data.
- Keep U.S.-destination measures out of baseline global treatment coding unless
  the empirical specification explicitly uses destination interactions.
