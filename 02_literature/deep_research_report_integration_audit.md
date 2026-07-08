# Deep Research Report Integration Audit

Updated: 2026-06-27 after the extra-paper intake and Zotero sync.

This audit integrates
`02_literature/deep_research_report_theory_empirical_extension_2026-06-27.md`
into the project literature system. The report is useful for source discovery
and corpus architecture, but the verified local source folders, summaries, and
Zotero records control the final corpus.

## Actions Taken

| Action | Status |
|---|---|
| Copied the user-provided report from `/Users/elgask0/Downloads/deep-research-report.md` into `02_literature/` | Done |
| Created the first missing-source download report | Done |
| Integrated user-downloaded extra papers into canonical source folders | Done |
| Parsed the new PDFs and created source summaries | Done |
| Synced the new records to Zotero and checked duplicate citation keys | Done |
| Updated literature master, source checklist, pairing audit, integration audit, and manual download requests | Done |
| Left final `references.bib` export to the user | Pending user Zotero export |

## Main Integration Decisions

| Report recommendation | Local decision | Reason |
|---|---|---|
| Strengthen the proposal with licensing-as-wedge sources | Accepted and integrated | UNCTAD 2019 and Gamberale and Tarasenko 2023 are now in the corpus |
| Add delay, time-cost, and policy-uncertainty sources | Accepted and integrated | Djankov et al. 2010, Hummels and Schaur 2013, and Handley and Limao 2017 now support the licensing-wedge logic |
| Add DDD, gravity-FE, staggered/event-study, and few-shock inference sources | Accepted and integrated | Fally 2015, Olden and Moen 2022, Borusyak et al. 2024, Conley and Taber 2011, Ferman and Pinto 2019, and MacKinnon and Webb 2018 are now local |
| Add price-wedge and benchmark-methodology sources | Partly integrated | Martin and Anderson 2012, Brander et al. 2023, and World Bank CMO 2026 are local; exact Bloomberg/Wind methodology waits until price-series selection |
| Move `02_literature/sources/` into `academic/`, `official/`, and `market_data_methodology/` subfolders | Rejected for now | The flat source-folder structure keeps citation keys, summaries, Zotero notes, and existing scripts aligned |
| Defer 2025 W/Te/Bi/Mo/In and rare-earth measures from the proposal baseline | Accepted | These remain thesis expansion candidates until HS crosswalks and data are complete |
| Treat official MOFCOM statements as evidence that licensing allowed approvals | Accepted with caveat | They cannot support approval rates, denial rates, or non-binding causal claims |

## Remaining Gaps

| Gap | Status |
|---|---|
| Full PRC 2024 dual-use regulation capture | Incomplete local PDF; request full official HTML/PDF before article-level citation |
| Final Zotero-to-BibTeX export | Completed; local BibTeX has 57 aligned entries |
| Bloomberg/Wind methodology for selected price series | Wait until actual series are chosen |
| Optional supply-chain adjustment and antimony-specific additions | Deferred unless later sections need them |

## Do Not Do Yet

- Do not build the theoretical-framework text yet.
- Do not rewrite the empirical-strategy section yet.
- Use the normalized project keys in `references.bib`.
