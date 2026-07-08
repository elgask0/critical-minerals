---
description: "Copy-ready protocol for collecting official Chinese export-control documents and constructing the policy chronology"
created: 2026-06-11
modified: 2026-06-11
group: evidence
tags: [project, critical-minerals, mofcom, primary-sources, deep-research]
status: active
created_by: codex
---

# MOFCOM Deep Research Prompt

Use the following prompt in a deep-research system with web access. The output
is a primary-source policy dataset and report, not a general literature review.

## Copy-Ready Prompt

```text
You are conducting primary-source legal and policy research for a master's
thesis on China's critical-mineral export controls.

RESEARCH OBJECTIVE

Construct the complete official Chinese policy chronology and product-scope
crosswalk for export controls on:

1. gallium and germanium, including MoFCOM/GAC Announcement No. 23 of 2023;
2. graphite, including MoFCOM/GAC Announcement No. 39 of 2023, its official
   FAQ, and predecessor Announcement No. 50 of 2006;
3. antimony and superhard materials, including MoFCOM/GAC Announcement No. 33
   of 2024;
4. the December 2024 measures directed at the United States, including MoFCOM
   Announcement No. 46 of 2024;
5. every later suspension, amendment, clarification, country-specific measure,
   license rule, FAQ, press-conference statement, enforcement notice, or
   replacement affecting those measures through June 11, 2026;
6. for a later expansion appendix, the 2025 controls on
   tungsten/tellurium/bismuth/molybdenum/indium and medium/heavy rare earth
   items, including Announcement No. 18 of 2025 and any later revisions.

Do not assume that an announcement, implementation, country-specific
prohibition, or later suspension is the same treatment. Record each as a
separate legal event.

SOURCE RESTRICTIONS

Use official Chinese primary sources as evidence:

- mofcom.gov.cn
- exportcontrol.mofcom.gov.cn
- english.mofcom.gov.cn
- customs.gov.cn
- gov.cn
- egov.mofcom.gov.cn
- official State Council, General Administration of Customs, and competent
  ministry pages

Media, law-firm alerts, think-tank reports, and commercial databases may be
used only to discover an official document. They cannot support a factual
claim in the final report. If an official page is unavailable, search official
archives and record that the original could not be retrieved.

SEARCH IN CHINESE AND ENGLISH

Search by:

- announcement number and year;
- mineral name and 出口管制;
- 优化调整, 实施, 暂停, 停止, 禁止, 许可, 两用物项;
- 新闻发布会, 答记者问, 政策解读, 业务问答;
- 许可证, 最终用户, 最终用途, 申请材料, 审批时限;
- 海关商品编号, 商品名称及描述, 参考海关商品编号;
- 违法, 处罚, 查处, 执法, 拒绝, 不予许可, 已批准.

REQUIRED OUTPUT 1: SOURCE REGISTER

Create one row per official document with:

- stable document ID;
- exact Chinese title;
- English translation of title;
- issuing authority;
- announcement/order number;
- publication date and time;
- announced effective date;
- date actually implemented, if separately documented;
- legal basis;
- document type;
- official URL;
- archived URL if available;
- access date;
- predecessor document;
- documents amended, repealed, suspended, or superseded;
- affected destination countries, if any;
- confidence level and unresolved ambiguity.

REQUIRED OUTPUT 2: LEGAL-EVENT CHRONOLOGY

Create a day-level chronology. Separate:

- announcement;
- effective date;
- license-application opening;
- first official statement that applications were received;
- first official statement that licenses were approved;
- documented delay, denial, suspension, or enforcement;
- country-specific prohibition;
- later suspension, amendment, expiry, or reactivation.

For every date, state which empirical event it represents:

- market information/announcement;
- exporter implementation;
- expected importer-arrival effect;
- later regime change.

Do not infer an importer-arrival month from the legal text. Flag it for
empirical shipping-lag analysis.

REQUIRED OUTPUT 3: PRODUCT AND CUSTOMS-CODE CROSSWALK

Create one row per controlled item, not one row per broad mineral. Include:

- mineral family;
- Chinese controlled-item name;
- English translation;
- chemical formula;
- physical form;
- purity threshold;
- particle size, density, strength, or performance threshold;
- whether thresholds are cumulative or alternative;
- included derivatives, compounds, equipment, and technologies;
- explicit exclusions and exemptions;
- "reference customs commodity number" exactly as printed;
- HS/CN interpretation and likely 6-digit aggregation problem;
- predecessor status;
- destination-specific scope;
- source document and page/section.

Do not treat a reference customs number as the legal definition when the
Chinese product description is narrower. Preserve all 8-, 10-, or 13-digit
codes printed by the authority.

REQUIRED OUTPUT 4: LICENSING-DESIGN MATRIX

For each policy episode, extract:

- implementing authority;
- application portal and responsible office;
- required exporter qualifications;
- contract and technical-document requirements;
- end-user and end-use certificates;
- government-issued end-user assurances;
- national-security review language;
- statutory or stated processing period;
- whether consultation or expert review can extend the period;
- reporting and customs-declaration requirements;
- license duration and shipment limits;
- humanitarian, research, sample, repair, or temporary-export exemptions;
- penalties and legal liabilities;
- whether a prior licensing infrastructure existed.

Classify design features only after quoting the supporting official text.
Distinguish "new implementation," "optimization/adjustment," expansion,
narrowing, destination-specific prohibition, and suspension.

REQUIRED OUTPUT 5: ENFORCEMENT-EVIDENCE MATRIX

Search official press conferences, FAQs, customs releases, and enforcement
notices for evidence that:

- applications were received;
- applications were approved;
- exporters experienced processing delays;
- applications were denied or returned;
- licenses were destination-specific;
- customs detained or rejected shipments;
- firms or individuals were penalized;
- the government stated the measure was not an export ban;
- implementation was suspended or modified.

For each claim, record exact date, mineral, destination, official source, and
whether the evidence is direct or only an official general statement. Absence
of a public denial is not evidence that all applications were approved.

REQUIRED OUTPUT 6: COMPARATIVE DESIGN TABLE

Compare gallium/germanium, graphite, and antimony on:

- novelty versus administrative continuity;
- lead time;
- technical specificity;
- breadth of covered value-chain stages;
- military/end-use language;
- pre-existing licensing capacity;
- destination neutrality versus destination specificity;
- documented approvals, delays, denials, and enforcement;
- later suspension or amendment.

Do not label one policy "more credible" as a fact. State which observable
features are consistent with greater administrative capacity or enforcement
cost, and list competing interpretations.

REQUIRED OUTPUT 7: EMPIRICAL MAPPING

For each episode, propose:

- announcement month;
- implementation month;
- first plausible importer-arrival month to test;
- anticipation window;
- post-treatment censoring or regime-change dates;
- exact treated HS codes;
- codes that are only partially treated;
- codes containing untreated products;
- outcomes that would distinguish temporary administrative friction from a
  persistent supply restriction.

Flag every date or code that remains uncertain. Never choose treatment timing
from news coverage when an official document exists.

QUOTATION AND TRANSLATION RULES

- Preserve the original Chinese for every legally material phrase.
- Provide a careful English translation.
- Keep direct quotations short, normally under 25 words per source.
- Cite paragraph, section, annex item, or page where possible.
- Mark machine translation and ambiguous technical terminology.
- Do not convert "including but not limited to" into a closed product list.

QUALITY CONTROL

1. Verify every announcement number against the original official page.
2. Verify every date in at least one official source.
3. Check whether later measures changed the legal status through June 11,
   2026.
4. Reconcile Chinese and English official versions and report discrepancies.
5. Separate legal scope from reference customs codes.
6. List missing documents and failed official URLs.
7. Do not make a causal claim.

FINAL DELIVERABLE

Return:

1. a concise executive summary;
2. the source register;
3. the legal-event chronology;
4. the product/customs-code crosswalk;
5. the licensing-design matrix;
6. the enforcement-evidence matrix;
7. the comparative design table;
8. the empirical mapping;
9. unresolved questions and missing official evidence;
10. a machine-readable CSV schema for all tables.
```

## Repository Integration

After the report is complete:

1. save official documents under one source folder per document in
   `02_literature/sources/`;
2. add metadata and stable citation keys to `references.bib`;
3. store the machine-readable chronology and product crosswalk under
   `03_data/raw/policy/`;
4. create cleaned event and HS crosswalk files under `03_data/processed/`;
5. update `Context.md`, `Data.md`, and `Thesis Design.md` only from verified
   official evidence.
