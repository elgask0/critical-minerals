# China's Critical-Mineral Export Controls

Master's thesis project on when Chinese export-licensing regimes become
binding market restrictions rather than only legal announcements, temporary
administrative disruptions, or strategic signals.

## Research Question

When do Chinese critical-mineral export licensing controls bind in
international trade, and do affected importers adjust through substitution
toward non-China suppliers, compression of total imports, or price
segmentation?

The current post-defense plan is locked in
`01_notes/Post-Defense Thesis Plan.md`. The theoretical model is in
`01_notes/Theoretical Framework Lock.md`; the estimator hierarchy is in
`01_notes/Empirical Strategy Lock.md`; the broader thesis architecture is in
`01_notes/Thesis Design.md`.

## Current Status

- Pressure-design Comtrade panel: 53 country reporters, 22 products, 87 months
  from 2019-01 to 2026-03, with raw dimensional duplication removed.
- Strict clean estimation sample: 53 reporters, 16 products, four clean
  treated products, and 12 donor candidates.
- Eurostat CN8: balanced current-EU27 panel for Ga, Ge, In, and V.
- CEPII GeoDist: validated for country reporters.
- Primary current estimator: quarterly PPML source-contrast model with
  switching-pressure and compression-pressure interactions.
- Mechanism models estimate China, RoW, and total import outcomes.
- Price wedges are mechanism diagnostics, strongest so far for antimony and
  bismuth.
- Monthly PPML, term-paper HS 282580 results, and Eurostat CN8 are retained
  as supporting evidence and provenance.

The safest current reading is that switching pressure is clearer than pure
compression in trade quantities. Antimony and bismuth also show strong
international-China price-wedge evidence. Compression remains a plausible
channel, but it should not be the headline unless later estimates improve.

## Reproduce Current Results

```bash
cd /Users/elgask0/REPOS/critical-minerals
uv sync
uv run python 04_scripts/build_product_scope_metadata.py
uv run python 04_scripts/prepare_comtrade_pressure_panel.py
uv run python 04_scripts/build_pressure_indices.py
uv run python 04_scripts/build_pressure_estimation_panel.py
uv run python 04_scripts/diagnose_anchor_quarter_models.py
uv run python 04_scripts/estimate_quarterly_pressure_mechanisms.py
uv run python 04_scripts/estimate_price_wedges.py
```

`analysis_thesis.py` reproduces the archived term-paper-style results.
`analysis_final.py` and the old `05_draft/Paper.md` workflow are superseded.
The archived term-paper source is under `05_draft/term_paper/` and is retained
only as preliminary-evidence/provenance material.

## Active Proposal Draft

The active master thesis proposal source is:

```text
05_draft/proposal/main.tex
```

The submitted proposal (2026-07-04, 36 pages) is archived locally as
`06_output/submitted/2026-07-04_proposal_revised_final.pdf`. It was verified on
2026-10-15 against the copy downloaded from the submission system: identical
file, and a fresh Tectonic build of `main.tex` reproduces the same text.

All proposal writing and thesis-facing LaTeX material must follow:

```text
08_admin/proposal_defense/zju_thesis_formatting_guidelines.md
```

Compile the proposal with XeLaTeX/Tectonic from `05_draft/proposal/`:

```bash
tectonic main.tex
```

For Overleaf, use the generated XeLaTeX-safe copy:

```bash
cd 05_draft/proposal
python make_overleaf_copy.py
```

The local compile check is for `main.tex`; the user compiles `main_overleaf.tex` on Overleaf.

## Structure

- `01_notes/`: thesis design, data, methods, policy evidence, roadmap.
- `02_literature/`: sources, summaries, and `references.bib`.
- `03_data/`: raw, interim, processed, and generated outputs.
- `04_scripts/`: download, preparation, and analysis scripts.
- `05_draft/`: proposal source and archived term-paper source.
- `06_output/`: exported and submitted files.
- `07_misc/`: local-only reference material; `07_misc/archive/` holds
  superseded scripts, term-paper docs, and old slide sources.
- `08_admin/proposal_defense/`: ZJU proposal-defense forms, templates,
  screenshots, and formatting rules.

See `NEXT_STEPS.md` for the next execution sequence.
