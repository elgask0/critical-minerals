# Master Thesis Proposal Draft

Active workspace for the ZJU master thesis proposal / opening report.

## Working Source

- `main.tex`: proposal skeleton.
- `main_overleaf.tex`: generated Overleaf-friendly copy for copy/paste or upload.
- `make_overleaf_copy.py`: regenerates the Overleaf copy from `main.tex`.
- `tables/`: proposal-specific tables.
- `figures/`: proposal-specific figures.

## Formatting Authority

Always follow:

```text
../../08_admin/proposal_defense/zju_thesis_formatting_guidelines.md
```

The LaTeX source is configured for XeLaTeX/Tectonic with:

- Times New Roman as the main English font;
- STFangsong as the FangSong-compatible Chinese font;
- ZJU margins: top 3 cm, bottom 2.5 cm, left/right 2.6 cm;
- 1.5-line spacing and no extra blank lines between paragraphs;
- section/chapter numbering for figures, tables, and equations;
- `booktabs` three-line tables.

Compile from this folder:

```bash
tectonic main.tex
```

Do not compile with pdfLaTeX.

## Overleaf Workflow

Overleaf usually does not have macOS fonts such as `STFangsong`, and may not have `Times New Roman`. Use the generated copy:

```text
main_overleaf.tex
```

Regenerate it after every text or structural edit to `main.tex`:

```bash
python make_overleaf_copy.py
tectonic main.tex
rm -f main.pdf
```

In Overleaf:

- set compiler to XeLaTeX;
- paste/upload `main_overleaf.tex`;
- upload `references.bib` beside it once citations are used;
- upload the `figures/` folder when figures are included.

Local verification is for `main.tex`, the ZJU-font source that uses Times New Roman and STFangsong. The Overleaf copy is generated locally, but compiled by the user on Overleaf.

Use TeX-safe ASCII punctuation in the source for apostrophes and quotes unless a typographic character has been visually checked in the compiled PDF. In particular, write `China's` in the `.tex` source rather than pasting a smart apostrophe.

The bibliography should be drawn from the project bibliography:

```text
02_literature/references.bib
```

## Required Content

Post-defense revision rule: before final submission, align the proposal prose
with `../../01_notes/Post-Defense Thesis Plan.md`. The revised proposal should
make the pressure framework central and should not present the average PPML
effect as the thesis's main contribution.

The proposal should satisfy the stricter interpretation of the ZJU documents and WeChat guidance:

1. Research question and importance.
2. Literature review and contribution.
3. Structure and content.
4. Empirical method, equations, data, variables, summary statistics, and possible results.
5. Innovation.
6. Research plan and time schedule.
7. References.

Working targets:

- at least 10,000 Chinese characters/words for the merged proposal plus literature review;
- 30+ references;
- later, a 5-7 minute defense slide deck.

Current empirical backbone for the revised proposal:

- quarterly source-contrast PPML;
- first full post-implementation quarter as baseline timing;
- switching-pressure and compression-pressure interactions;
- mechanism models for China, RoW, and total imports;
- price wedges as mechanism diagnostics;
- monthly timing, U.S., net-weight, and placebo checks as robustness.
