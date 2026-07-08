# Deep Research Prompt: Literature Review for Critical-Mineral Export Controls

Use this prompt with a deep-research tool or research-capable agent. The output
should be a project-ready `02_literature/literature_master.md`, not a prose
literature review.

```text
You are a research assistant helping me build the canonical literature scope
file for an academic term paper and future master's thesis.

Your task is not to write a prose literature review. Your task is to conduct
structured source discovery and produce a project-ready Markdown file named:

literature_master.md

This file will become the operational literature control document for a
research repository. It should help me decide which sources belong in the
project, what role each source plays, how sources map into the manuscript, and
what remains missing.

1. PROJECT CONTEXT

Research topic:

China's 2023-2024 critical-mineral export controls and their effects on
foreign trade, with emphasis on graphite, gallium/germanium, and antimony.

Working research question:

When does China's export licensing for critical minerals become a binding trade
restriction rather than temporary administrative friction or strategic
signaling?

Working thesis / expected argument:

China's critical-mineral export controls are formally similar licensing
regimes, but their market effects may differ across minerals because licensing
credibility depends on legal design, administrative precedent, value-chain
position, market structure, demand conditions, and China's own cost of
withholding supply. The paper should not assume that high market share
automatically implies effective coercive power. The empirical paper will test
observable trade margins: China export departures, importer arrivals from
China, source share, timing/persistence, and substitution toward non-China
sources.

Project type:

Course term paper now, future empirical master's thesis.

Discipline / field:

Chinese economy, international trade, international political economy, economic
statecraft, China studies, empirical trade.

Expected final deliverable:

Minimum 5,000-word term paper for the course "Introduction to China's Foreign
Trade and Investment"; later expanded into a master's thesis.

Reader / evaluator:

Professor in a course on China's foreign trade and investment. The paper must
be readable as a China foreign-trade policy paper, not only as an econometrics
paper.

Implementation context:

The output will be saved as:

02_literature/literature_master.md

inside a research repository with this structure:

02_literature/
├── references.bib
├── literature_master.md
├── source_acquisition_checklist.md
├── sources/
│   └── author_year_short_title/
│       ├── README.md
│       ├── source.pdf
│       ├── metadata.md
│       ├── notes.md
│       ├── parsed/
│       │   └── text.md
│       └── assets/
└── summaries/
    └── summary_template.md

The final output must be useful for Zotero import, source downloading, PDF
organization, and source summarization.

2. RESEARCH SCOPE

Geographic scope:

China-centered, with global importer exposure. Include the United States, EU,
Japan, Korea, and other importers only when needed for policy context,
diversification, or trade-flow interpretation.

Time period:

Main policy period 2020-2026. Historical background may include China's 2010
rare-earth episode, the 2006 graphite controls, China's Export Control Law, and
earlier mineral industrial-policy sources.

Main concepts / keywords:

China export controls; critical minerals; export licensing; Chinese foreign
trade policy; economic statecraft; weaponized interdependence; supply-chain
security; graphite; gallium; germanium; antimony; rare earths; US-China
technology competition; semiconductor export controls; trade sanctions;
gravity model; PPML; event study; difference-in-differences; sanctions and
trade diversion.

Cases or units of analysis:

- MoFCOM/GAC Announcement No. 23 of 2023: gallium and germanium controls.
- MoFCOM/GAC Announcement No. 39 of 2023: graphite controls.
- MoFCOM/GAC Announcement No. 33 of 2024: antimony controls.
- Earlier graphite predecessor controls, especially Announcement No. 50 of
  2006.
- China's Export Control Law and official licensing process.
- Historical rare-earth export restrictions where useful as background, not as
  the main case.
- UN Comtrade HS codes: 2504, 3801, 811292, 282560, 8110, 261710, 282580, plus
  controls 2818, 8111, 2811.
- Eurostat CN8 codes 81129289, 81129295, 81129281, 81129291.

Methods or evidence types expected:

Mixed. The literature review must support institutional analysis, theory,
empirical trade design, data interpretation, and policy discussion.

Preferred source types, in order:

1. Peer-reviewed journal articles.
2. Academic books or book chapters from reputable presses.
3. Working papers from credible institutions.
4. Official reports from governments, international organizations, statistical
   agencies, or technical bodies.
5. Official Chinese primary sources from MoFCOM, GAC, State Council, or
   export-control portals.
6. High-quality datasets or methodology pages.
7. Reputable policy reports only if they provide factual or institutional
   detail not available elsewhere.
8. News articles only for chronology or contemporary statements when official
   sources are unavailable.

Avoid:

- generic blog posts;
- SEO summaries;
- unsourced claims about China's market share;
- news-only claims where official documents exist;
- sources that are interesting but do not support the term paper or thesis.

3. REQUIRED LITERATURE STREAMS

Conduct the research in these streams. You may add one extra stream if needed,
but do not produce an unfocused source dump.

Stream A: Economic statecraft and weaponized interdependence

Analytical function:

Explain why network concentration and asymmetric dependence can create
coercive power, and why supply-side mineral controls may differ from
demand-side technology or financial controls.

Project sections served:

Introduction, literature review, analytical framework, discussion.

Needed sources:

Core theory sources, critiques, and related economic statecraft/sanctions
literature.

Expected starting points:

Farrell and Newman (2019); Farrell and Newman (2023); sanctions/economic
statecraft literature such as Baldwin, Drezner, Felbermayr et al., Crozet and
Hinz, Egger et al. Include only the most useful sources.

Stream B: China's foreign trade policy and export-control system

Analytical function:

Explain China's Export Control Law, licensing procedures, national-security
framing, end-use documentation, and the difference between export licensing
and export prohibition.

Project sections served:

Literature/institutional background, data/treatment definition, policy
implications.

Needed sources:

Primary Chinese legal texts, official English/Chinese explanations, and
academic/policy analyses of China's export-control regime.

Expected starting points:

China Export Control Law; State Council white paper on export controls;
MoFCOM export-control portal; MoFCOM licensing guides; academic work on
China's export-control law if available.

Stream C: Official policy chronology for current minerals

Analytical function:

Build the exact legal and institutional context for Ga/Ge, graphite, and
antimony controls.

Project sections served:

Literature/institutional background, data treatment coding, analytical
framework, discussion.

Needed sources:

Official MoFCOM/GAC announcements, official FAQs, licensing guides, press
conferences, and any official statements on license approvals, suspensions, or
clarifications.

Mandatory primary sources to verify:

- Announcement No. 23 of 2023 on gallium and germanium.
- Announcement No. 39 of 2023 on graphite.
- Announcement No. 50 of 2006 on earlier graphite controls.
- Announcement No. 33 of 2024 on antimony.
- Relevant licensing-guide PDFs.
- Official MoFCOM press conferences stating controls are not export bans and
  whether licenses were approved.
- Any later official amendments, suspensions, destination-specific measures,
  or clarifications through June 2026 that affect these minerals.

For each official source, identify:

- Chinese title and English translation if available;
- announcement date;
- implementation date;
- issuing institutions;
- controlled products;
- customs/reference codes;
- whether it is new, adjusted, suspended, or repealed;
- legal basis;
- licensing documents required;
- any official evidence of approvals, denials, or enforcement.

Stream D: Critical-mineral supply chains and market structure

Analytical function:

Support the claim that China has large but different roles across gallium,
germanium, graphite, and antimony supply chains, and that value-chain position
matters.

Project sections served:

Introduction, literature/institutional background, analytical framework,
discussion.

Needed sources:

Official and technical sources for market shares, production, processing,
reserves, byproduct status, demand uses, substitutability, and supply-chain
vulnerability.

Expected starting points:

USGS Mineral Commodity Summaries; IEA Critical Minerals Market Review; European
Commission critical raw materials documents; academic literature on gallium
byproduct supply, graphite supply chains, antimony supply, and rare earths as
historical precedent.

Stream E: US-China technology competition and semiconductor controls

Analytical function:

Explain the geopolitical timing of China's controls without turning the paper
into a general geopolitical essay.

Project sections served:

Introduction, literature review, policy chronology, motivation.

Needed sources:

Sources on U.S. semiconductor export controls, allied technology controls, and
China's response through trade/security policy.

Expected starting points:

Bown (2020) and later credible sources on U.S. semiconductor export controls.
Find current sources covering 2022-2025 semiconductor-control escalation and
its connection to China's mineral export controls.

Stream F: Empirical trade, sanctions, and event-study methods

Analytical function:

Justify PPML, source-share triple difference, event timing, and careful
inference with few product-level treatments. Also explain why log returns are
not the primary estimator for sparse trade flows.

Project sections served:

Empirical strategy, limitations, robustness.

Needed sources:

PPML gravity literature, sanctions/trade-diversion empirical methods,
difference-in-differences/event-study references, and parallel-trends
sensitivity literature.

Expected starting points:

Santos Silva and Tenreyro (2006); Egger, Syropoulos, and Yotov (2024);
Callaway and Sant'Anna (2021); Sun and Abraham (2021); Rambachan and Roth
(2023); Roth (2022). Select only what is necessary for a course paper and
future thesis.

4. SOURCE CONTROL INSTRUCTIONS

Do not scrape shallow summaries. Prioritize sources that directly support the
research design, argument, or empirical claims.

Search deliberately across:

- Google Scholar or equivalent scholarly discovery;
- publisher pages;
- university repositories;
- SSRN, NBER, CEPR, IZA, RePEc, or field-specific working-paper platforms;
- official agencies and international organizations;
- MoFCOM, GAC, State Council, and Chinese export-control official portals;
- dataset and methodology pages where relevant.

When possible, prefer sources with:

- DOI;
- stable official URL;
- downloadable PDF;
- clear author/date/title metadata;
- direct connection to one part of the project.

If two sources do the same job, prefer the more authoritative, more recent,
more directly relevant, or more methodologically transparent source.

Recommended active corpus size:

- 20-35 active sources for the term paper and near-term thesis expansion.
- A smaller must-cite core of 10-15 sources.
- Additional deferred sources can be listed but should not bloat the active
  corpus.

5. REQUIRED OUTPUT FORMAT

Your final answer must be a single Markdown document with this structure:

# Literature Master

## Purpose

Explain that this is the canonical literature scope file for the project. It
controls which sources belong in the project, what role each source plays, how
sources map into the manuscript, and which sources are still missing.

## Project Context

| Field | Value |
|---|---|
| Topic | China's critical-mineral export controls |
| Working research question | When does China's export licensing for critical minerals become a binding trade restriction rather than temporary administrative friction or strategic signaling? |
| Working thesis / expected argument | Licensing credibility varies by legal design, administrative precedent, value-chain position, market structure, demand conditions, and China's self-cost. |
| Project type | Term paper now; empirical master's thesis later |
| Discipline / field | Chinese economy; international trade; international political economy |
| Expected deliverable | 5,000+ word term paper, later thesis |
| Geographic scope | China-centered, global importer exposure |
| Time period | 2020-2026 main period, with selected historical background |

## Scope Notes

Summarize search logic, inclusion criteria, exclusion criteria, and limits.

## Corpus Rules

Numbered rules for source inclusion.

## Stream Structure

| Stream | Short Name | Analytical Function | Project Sections Served | Evidence Needed |
|---|---|---|---|---|

## Priority Definitions

- must-cite:
- should-cite:
- optional:
- deferred:
- discard:

## Workflow Status Definitions

- candidate:
- approved-needs-integration:
- draft-ready:
- needs-pdf:
- needs-summary:
- deferred:
- discarded:

## Path Conventions

Use clean stable source folder names:

author_year_short_title/

Recommended paths:

| Asset | Path Convention |
|---|---|
| Source folder | 02_literature/sources/<filename_stem>/ |
| Original source | 02_literature/sources/<filename_stem>/source.pdf |
| Metadata | 02_literature/sources/<filename_stem>/metadata.md |
| Rough notes | 02_literature/sources/<filename_stem>/notes.md |
| Parsed text | 02_literature/sources/<filename_stem>/parsed/text.md |
| Summary | 02_literature/summaries/<filename_stem>.md |
| Bibliography | 02_literature/references.bib |

## Corpus Snapshot

| Metric | Count |
|---|---:|
| Active sources | |
| Must-cite | |
| Should-cite | |
| Optional | |
| Deferred | |
| Discarded | |
| Sources with DOI | |
| Sources with stable official URL | |
| Sources likely downloadable as PDF | |

## Canonical Source Table

| Source ID | Citation Key | Full Citation | Source Type | Priority | Stream / Bucket | Core Contribution | Main Use in Project | Key Claims I Can Safely Use | DOI / URL | Source Folder | Summary Path | Zotero Status | PDF / Source Status | Parse Status | Note Status | Caveats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Stream-by-Stream Source Notes

For each stream, create a subsection:

### Stream: [stream-name]

For each active source in that stream, include:

#### [Citation Key or Author Year Short Title]

- Full citation:
- Priority:
- Status:
- Why it belongs:
- Main use in project:
- Key claim(s) that can safely be used:
- Caveat / limitation:
- DOI / URL:
- Suggested filename stem:

## Deferred or Excluded Sources

| Source | Reason Deferred or Excluded | Possible Future Use |
|---|---|---|

## Missing Sources / Search Gaps

List source types or evidence still needed.

## Suggested Source Acquisition Checklist

| Target Source | Priority | Status | Zotero | PDF / Source Folder | Summary | Notes |
|---|---|---|---|---|---|---|

## Suggested Next Steps

Give concrete next steps:

1. Import must-cite sources into Zotero.
2. Export selected sources to 02_literature/references.bib.
3. Create source folders using suggested filename stems.
4. Download PDFs or official source files.
5. Write summaries for all must-cite sources.
6. Revisit deferred sources only if the argument needs them.

6. SOURCE QUALITY RULES

For every source, be explicit about what it can and cannot support.

Use this distinction:

- Can safely support: claim directly supported by the source.
- Useful background: helps framing but should not carry a key empirical claim.
- Caveat: limitation, bias, scope issue, non-peer-reviewed status,
  outdatedness, indirect relevance, or mismatch with the project.

Do not invent DOI numbers, page numbers, or download availability. If
uncertain, write "needs verification".

7. CITATION AND METADATA RULES

For each source, provide as much metadata as possible:

- author(s);
- year;
- title;
- journal/book/report/publisher;
- DOI if available;
- stable URL if available;
- source type;
- suggested citation key;
- suggested filename stem.

Citation key format:

author_year_short_title

For multiple authors, use the first author only unless ambiguity requires more
detail.

8. OUTPUT DISCIPLINE

The final output must be:

- Markdown only;
- structured as literature_master.md;
- operational, not verbose prose;
- finite and selective;
- honest about uncertainty;
- clear enough to directly guide Zotero import, PDF download, source
  summaries, and drafting.

Do not produce:

- a generic literature review essay;
- a long unstructured bibliography;
- unsourced claims;
- invented citations;
- irrelevant sources;
- a massive source dump.

9. FINAL QUALITY CHECK

Before finalizing, check:

- Does every active source serve a named project function?
- Are the streams useful and not redundant?
- Are must-cite sources truly indispensable?
- Are weak or tangential sources deferred rather than included?
- Are DOI/URL fields honest?
- Are caveats explicit?
- Is the corpus size appropriate for the project scale?
- Could this file directly guide Zotero import, PDF download, summaries, and
  drafting?

Now conduct the research and produce the final literature_master.md.
```
