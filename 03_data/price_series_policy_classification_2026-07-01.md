# Price Series Policy Classification, 2026-07-01

This note classifies the downloaded price series by policy role. It answers one
question: are the price data treated-product prices, placebo/control prices, or
non-product demand controls?

## Bottom Line

Most of the downloaded mineral price series are for treated, partially treated,
or marginally treated products. They are not placebos.

The main exception is molybdenum: the molybdenum oxide/molybdate price family is
a candidate-control/proxy family in the current thesis universe. MOFCOM
Announcement No. 10/2025 controls narrow molybdenum powder under HS 810210, but
the thesis dropped HS 8102 because the legal control is too narrow for the HS-6
trade heading. HS 284170 molybdates and HS 282570 molybdenum oxides remain
candidate controls.

Vanadium prices are also control/proxy prices. They are useful demand or
within-bundle comparison series, not direct treated-product price wedges.

## Classification Table

| Price family | HS link | Thesis role | Policy classification | Current data status | Analysis use |
|---|---:|---|---|---|---|
| Gallium metal | 811292 | Wave 1 partial treated | Treated subcomponent in bundled HS heading | Complete domestic/international | Price wedge for controlled gallium. |
| Germanium metal | 811292 | Wave 1 partial treated | Treated subcomponent in bundled HS heading | Complete domestic/international | Price wedge for controlled germanium metal. |
| Indium metal | 811292 | Not a treated ordinary-metal item inside same bundle | Within-bundle control/proxy | Complete domestic/international | Comparison price inside the mixed Ga/Ge/In/V/Nb heading; the 2025 indium controls cover indium phosphide and organo-indium compounds, not ordinary indium metal. |
| GeO2 | 282560 | Wave 1 partial treated | Treated subcomponent; HS heading also contains ZrO2 | Usable domestic/international, international ends 2026-01 | Price wedge with documented endpoint. |
| Natural graphite | 2504 | Wave 2 clean treated | Treated | Domestic complete; international downloaded but needs DES grade verification | Main graphite wedge if Bloomberg ticker is natural flake benchmark. |
| Spherical/processed graphite | 3801 / related subcodes | Wave 2 partial/descriptive | Treated or policy-contaminated, not clean placebo | Downloaded but needs DES grade verification | Secondary/descriptive only unless it clearly maps to natural flake benchmark. |
| Antimony metal | 8110 | Wave 3 clean treated | Treated | Complete domestic/international | Price wedge for controlled antimony metal. |
| Antimony concentrates | 261710 | Wave 3 clean treated but sparse | Treated | China-side series present | Descriptive supplement; no complete wedge yet. |
| Antimony oxides | 282580 | Wave 3 partial treated | Treated subcomponent; legal control is high-purity antimony oxide | China side present; international missing | Only remaining treated/partial treated terminal download. |
| Bismuth metal | 8106 | Wave 4 clean treated | Treated | Complete domestic/international | Price wedge for controlled bismuth metal. |
| Tungsten APT/tungstates | 284180 | Wave 4 clean treated | Treated | Complete assumed; Bloomberg DES still to archive | Price wedge for controlled APT/tungstate family. |
| Tungsten metal | 8101 | Wave 4 partial treated | Treated only for specific high-W solid forms and dimensions | Complete/usable assumed | Secondary tungsten wedge/proxy; not placebo. |
| Tellurium metal | 280450 | Wave 4 marginal treated | Marginal treated; HS heading bundles Te with B | Complete assumed; Bloomberg DES still to archive | Descriptive/marginal treated wedge, not clean control. |
| Rare earths | 284690 | Wave 5 marginal treated | Marginal treated and too aggregated | No clean price suite; dropped from wedge work | Do not spend terminal time unless a clean ready-made suite appears. |
| Vanadium | 282530 / 811292 | Candidate control/proxy | Not directly treated by the current MOFCOM mineral controls | Complete with proxies | Demand/alternative-shock control and within-bundle comparison. |
| Molybdenum oxides/molybdates | 282570 / 284170 | Candidate control/proxy | Not the controlled HS 810210 molybdenum powder item | China side complete; monthly international missing | Optional control/proxy download, not a treated wedge. |
| Demand and macro controls | N/A | Controls | Not product treatment/placebo classifications | Present for semiconductors, BEV, power battery, steel, lead-acid, PMI/PPI, FX | Regression controls and alternative-shock diagnostics. |

## What Is Definitely Not A Clean Placebo

- HS 2827: policy-contaminated because controlled germanium tetrachloride is in
  the 2023 gallium/germanium announcement.
- HS 380120 and related graphite products: not a clean graphite placebo because
  the legal graphite description covers natural flake graphite and products,
  including processed forms.
- HS 282590 tungsten oxides and HS 284990 tungsten carbide: controlled in the
  February 2025 tungsten announcement, so they are not placebos.
- HS 280450 tellurium/boron: marginal treated, not a clean control.
- HS 284690 rare earths: marginal treated and too aggregated for current price
  wedge work.

## Terminal Implications

1. Treated/partial treated price work: only international antimony oxide is
   still missing.
2. Graphite: do not redownload yet. Archive DES/descriptions for `GPCNLCLW`,
   `GPCNASPZ`, `GPCNASKZ`, `GPCNN190`, and `GPCNP195`, then choose the natural
   flake benchmark if present.
3. Tellurium and tungsten: archive DES/descriptions, but no new download is
   needed under the current assumption that `TEEUUQPU Index` and `TGEUWOQR
   Index` are correct.
4. Molybdenum: download only if time remains and label it as a control/proxy
   benchmark, not as a treated-product wedge.
5. Rare earths: keep dropped from price-wedge work unless a clean official or
   terminal suite is immediately available.

## Official Classification Sources

- MOFCOM / GACC Announcement No. 23/2023: gallium and germanium controls.
  https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202307/847.html
- MOFCOM / GACC Announcement No. 39/2023: graphite controls.
  https://www.mofcom.gov.cn/zcfb/blgg/art/2023/art_f6b1bc49e2c8482f8eb749012bc66dec.html
- MOFCOM / GACC Announcement No. 33/2024: antimony controls.
  https://aqygzj.mofcom.gov.cn/qdml/art/2024/art_b907a108e35945db9f8b04e1ed77b659.html
- MOFCOM Announcement No. 10/2025: tungsten, tellurium, bismuth, molybdenum,
  and indium-compound controls.
  https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/zcfggzqd/202502/1098.html
- MOFCOM / GACC Announcement No. 18/2025: medium and heavy rare-earth controls.
  https://english.mofcom.gov.cn/Policies/AnnouncementsOrders/art/2025/art_0dd87cbee7b045bf93fabe6ab2faceee.html
