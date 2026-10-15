# Review Checklist

Status: term-paper writing readiness as of 2026-06-17.

## Term Paper: Ready

- [x] Research question distinguishes licensing announcements from binding
      trade restrictions.
- [x] Theoretical framework is reduced-form and observable: a latent licensing
      wedge should reduce China-source imports relative to rest-of-world
      imports.
- [x] Mechanism claim is disciplined: importer switching potential is measured
      from pre-announcement China exposure and rest-of-world access.
- [x] Core Comtrade term-paper panel is complete through March 2026.
- [x] Eurostat CN8 Ga/Ge case study is cleaned and balanced.
- [x] CEPII GeoDist is validated for country reporters, though it is not needed
      for the main term-paper estimator.
- [x] Canonical scripts reproduce the current tables:
      `prepare_comtrade_thesis_panel.py`, `prepare_eurostat_cn8.py`, and
      `analysis_thesis.py`.
- [x] PPML source-share DDD is the primary estimator.
- [x] Event studies and pretrend tests are regenerated from the current panel.
- [x] Switching-potential split DDD is implemented and regenerated.
- [x] Reporter-clustered p-values are described only as conditional
      diagnostics.
- [x] Exact product-level inference limits are disclosed.
- [x] HS 3801 is excluded from the control set and kept only as descriptive.
- [x] Antimony metal, antimony ores/concentrates, and antimony oxides are not
      pooled.
- [x] Main result selected before writing: HS 282580 antimony oxides.
- [x] Main mechanism result selected before writing: HS 282580
      high-switching-potential importers.
- [x] Literature folders, summaries, Zotero records, and `references.bib` are
      synchronized.
- [x] Term-paper structure is defined in `05_draft/TermPaper_Structure.md`.

## Required Cautions For Writing

- Do not claim to observe licensing denial probabilities, enforcement
  intensity, inventories, political concessions, or welfare effects.
- Use "supports" only for the clean HS 282580 switching-potential pattern.
- Use "consistent with" for graphite and antimony metal.
- Treat HS 261710 as descriptive only because of sparse flows and failed
  pretrends.
- Treat aggregate Ga/Ge nulls as measurement-sensitive evidence against a
  uniform export-collapse story, not as proof that the policies were irrelevant.
- Do not use `05_draft/Paper.md` numerical claims unless they are reproduced by
  `04_scripts/analysis_thesis.py`.

## Before Final Submission

- [ ] Draft the paper from `05_draft/TermPaper_Structure.md`.
- [ ] Export final references from Zotero and replace
      `02_literature/references.bib`.
- [ ] Verify at least 10 references are cited.
- [ ] Generate final tables and figures from `03_data/output/tables/`.
- [ ] Export to Word and apply course formatting.
- [ ] Save the submitted file under `06_output/submitted/`.

## Thesis Work Deferred

- [ ] Exact-grade international/domestic price DiD.
- [ ] Bloomberg/Wind benchmark expansion.
- [ ] Downstream demand indicators.
- [ ] USGS market-concentration panel beyond descriptive use.
- [ ] Broader product and placebo universe.
- [ ] Larger-product inference designs and thesis-level robustness.
