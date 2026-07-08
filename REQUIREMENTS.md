# Requirements

## Assignment / Project Requirements

- ZJU "China's International Trade and Investment" (中国国际经贸投资) term paper
- Instructor: [see Course Requirements.md for details]
- Grading: 50% term paper, 50% other components

## Deliverables

- Written term paper (minimum 5,000 words)
- 20-minute PowerPoint presentation
- Minimum 10 academic references

## Formatting Rules

- Chinese academic formatting (18pt/14pt/12pt font sizes, 1.5 spacing)
- See `01_notes/Course Requirements.md` for full formatting spec

## Citation Rules

- Standard academic citation style (author-year)
- 16 references currently in paper

## Data / Evidence Requirements

- UN Comtrade monthly bilateral trade data (2019-2024, 72 months)
- Bloomberg/Wind domestic Chinese price data
- Minimum: ITS + triple-difference with placebo HS codes
- Mechanism tests: stockpiling, price direction, HK rerouting, substitution

## Deadlines

- **June 25, 2026**: Paper submission + presentation

## Non-Negotiables

- All numbers in paper must be exactly reproducible from `04_scripts/analysis_final.py`
- Mechanisms framed as "consistent with" not "evidence for" (N=2 cannot identify separate mechanisms)
- HS 3801 excluded (partially treated), HS 2501 excluded (too sparse)
- Graphite decline is 47.8% (exp(β)-1), not 64.9% (β×100)
