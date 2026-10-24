# AGENTS.md

## Project Environment

This project uses a repository-local uv environment (`.venv`, Python 3.12).
Dependencies are pinned in `pyproject.toml` and locked in `uv.lock`; the pins
match the versions the pipeline ran with before the uv migration, so results
stay reproducible.

```bash
cd <repo-root>
uv sync                      # create or refresh .venv (add --all-groups for Jupyter)
uv run python 04_scripts/build_pressure_estimation_panel.py
```

Add or change a dependency with `uv add <package>` (it updates `pyproject.toml`
and `uv.lock`). Do not install into any global or base Python. The legacy
`./.conda` pip prefix is gone; the scripts' `sys.path` fallback to it is inert.

## Project Structure

* `01_notes/`: planning, argument, evidence, data documentation, methodology.
* `02_literature/`: sources, parsed files, summaries, bibliography.
* `03_data/raw/`: original Comtrade CSVs, Bloomberg prices, CEPII GeoDist.
* `03_data/interim/`: intermediate cleaning outputs.
* `03_data/processed/`: cleaned analysis-ready data.
* `03_data/output/`: generated figures and tables.
* `04_scripts/`: analysis scripts. The active thesis-stage pipeline is the pressure-design pipeline (`build_product_scope_metadata.py`, `prepare_comtrade_pressure_panel.py`, `build_pressure_indices.py`, `build_pressure_estimation_panel.py`, and the quarterly pressure/price scripts). `analysis_thesis.py` is archived term-paper reproducibility. `analysis_final.py` is legacy.
* `05_draft/`: manuscript source. `05_draft/proposal/main.tex` is the active master thesis proposal source. `05_draft/term_paper/` contains archived term-paper source and preliminary-evidence material.
* `06_output/`: exported and submitted files.
* `07_misc/archive/`: deprecated scripts.
* `08_admin/proposal_defense/`: ZJU proposal-defense bureaucracy, official forms, templates, and formatting rules.

## Active Drafting Rules

* Always follow `08_admin/proposal_defense/zju_thesis_formatting_guidelines.md` for the master thesis proposal and any thesis-facing written output.
* Compile the proposal with XeLaTeX/Tectonic from `05_draft/proposal/`; do not use pdfLaTeX because the ZJU format requires Times New Roman plus FangSong-compatible Chinese fonts.
* Use `05_draft/proposal/main.tex` as the single active proposal source. Do not create a parallel Markdown source for the proposal.
* After every edit to `05_draft/proposal/main.tex`, regenerate the Overleaf-safe copy with `python make_overleaf_copy.py` from `05_draft/proposal/`.
* Always compile `main.tex` locally with Tectonic after proposal edits, then remove generated PDFs unless the user asks for them. The user will compile `main_overleaf.tex` on Overleaf.
* Keep the proposal in ZJU format: top margin 3 cm, bottom margin 2.5 cm, left/right margins 2.6 cm, 1.5-line spacing, no extra blank lines between paragraphs, Times New Roman for English and STFangsong/FangSong for Chinese.
* Use TeX-safe ASCII punctuation in proposal `.tex` sources for apostrophes and quotes unless a typographic character has been visually checked in the compiled PDF.
* Number figures, tables, and equations by section/chapter as `Figure 1-1`, `Table 1-1`, and `(1-1)`.
* Use three-line, full-text-width tables with `booktabs`; avoid vertical rules.
* Put table captions above tables and figure captions below figures; include source notes where needed.
* Use `02_literature/references.bib` as the only bibliography source and format references according to the ZJU guideline before final submission.

## Current Pressure-Design Results

The current thesis direction is documented in
`01_notes/Post-Defense Thesis Plan.md`. The active empirical design uses
quarterly source-contrast PPML with switching-pressure and
compression-pressure interactions.

Current outputs must be reproducible from:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
python 04_scripts/diagnose_anchor_quarter_models.py
python 04_scripts/estimate_quarterly_pressure_mechanisms.py
python 04_scripts/estimate_price_wedges.py
```

Current preliminary reading:

- Strict clean sample: 53 reporters, 16 products, 87 months, two source groups, four clean treated products, and 12 donor candidates.
- Quarterly average PPML, first full post-quarter: graphite -30.1% (p=0.076), antimony metal -86.7% (p=9.13e-09), Wave 4 W/Bi -42.4% (p=0.021), bismuth -74.4% (p=0.000305), tungstates/APT -15.2% (p=0.683).
- Switching pressure is more credible than compression pressure in current trade quantities.
- Price wedges strongly support antimony and bismuth segmentation.
- Compression remains a plausible channel, not yet a clean headline result.

Archived term-paper outputs remain reproducible from
`04_scripts/analysis_thesis.py`:

- Term-paper panel: 53 reporters, 10 products, 87 months, 2019-01 to 2026-03.
- Source-share PPML Antimony oxides (HS 282580): -81.5% (conditional reporter p=0.0025; pretrend p=0.680).
- Switching-potential split HS 282580, high-A importers: -87.4% (conditional p=0.00019; pretrend p=0.354).
- Source-share PPML Graphite: -30.4% (conditional p=0.107; suggestive only).
- Source-share PPML Antimony metal (HS 8110): -86.8% (conditional p<0.001; pretrends fail).
- Source-share PPML Antimony ores/concentrates (HS 261710): -98.9% (conditional p=0.0033; sparse/descriptive only).
- Source-share PPML Ga/Ge bundle (HS 811292): +19.3% (conditional p=0.365; no aggregate negative effect).
- Source-share PPML GeO2/ZrO2 (HS 282560): +17.5% (conditional p=0.271; no aggregate negative effect).
- Exact product-level inference cannot attain p<0.25 with three placebos.

## Rules

* Do not modify raw data in `03_data/raw/`.
* Use `03_data/interim/` for intermediate outputs.
* Use `03_data/output/figures/` and `tables/` for generated outputs.
* Keep submitted files in `06_output/submitted/`.
* Use `02_literature/references.bib` as the only bibliography source.
* Mechanisms are "consistent with" unless the preferred pressure-design model shows the predicted sign, plausible timing, and mechanism-consistent margin evidence.
* HS 3801 (partially treated) and HS 2501 (too sparse) are excluded from main analysis.
* Comtrade API keys must stay out of Git. Set `COMTRADE_API_KEYS` or
  `COMTRADE_API_KEY_1`/`COMTRADE_API_KEY_2` in the local shell before running
  download scripts.
* `05_draft/Paper.md` and the old flat term-paper draft files are superseded. Use `05_draft/proposal/main.tex` for the proposal and `05_draft/term_paper/main.tex` only as archived preliminary-evidence source material.
* `analysis_thesis.py` is no longer the current thesis backbone. Use it only for archived term-paper reproducibility.
* Never use the legacy raw-row triple-difference estimates for thesis claims.
