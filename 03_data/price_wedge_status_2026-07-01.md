# Price-Wedge Data Status, 2026-07-01

This is the current working status after the Bloomberg/Wind downloads on
2026-07-01. The reproducible source is
`04_scripts/prepare_wind_prices_controls.py`; the machine-readable status table
is `03_data/output/tables/price_wedge_candidate_coverage_2026-07-01.csv`.

## Rule For Tomorrow

Only one treated or partially treated price-wedge download remains:

1. International antimony oxide, preferably antimony trioxide
   Rotterdam/Europe/CIF Antwerp-Rotterdam.

International molybdenum is still useful, but it is a candidate-control/proxy
download rather than a treated-product wedge in the current 31-product design.
MOFCOM Announcement No. 10/2025 controls narrow molybdenum powder under HS
810210, while the thesis keeps molybdates and molybdenum oxides as candidate
controls under HS 284170 and HS 282570.

Graphite does not need a new download yet; it needs Bloomberg description
verification for the already downloaded `GPCN*` tickers. Tellurium and tungsten
are treated as complete under the current assumption that `TEEUUQPU Index` and
`TGEUWOQR Index` are the intended international benchmarks.

## Candidate Status

| Candidate | Domestic side | International side | Status | Next action |
|---|---|---|---|---|
| Gallium | Present | Present | Complete | None. |
| Germanium metal | Present | Present | Complete | None. |
| Indium metal | Present | Present | Within-bundle control/proxy complete | No terminal action; not a treated-product wedge for ordinary indium metal. |
| Antimony metal | Present | Present | Complete | None. |
| Bismuth | Present | Present | Complete | None. |
| GeO2 | Present | Present through 2026-01 | Usable partial | Use as-is and document endpoint. |
| Vanadium | Present, including China V2O5 from 2020-10 | Present | Complete with full-window proxies | Use V2O5 where exact; use V nitrogen/ferrovanadium for full-window proxy checks. |
| Tellurium | Present | Present, assumed `TEEUUQPU Index` | Complete assumed | Archive Bloomberg DES tomorrow. |
| Tungsten | Present | Present, assumed `TGEUWOQR Index` plus Rotterdam ferro-tungsten | Complete/usable assumed | Archive Bloomberg DES tomorrow. |
| Graphite | Present, natural flake through 2026-03 | Present but descriptions missing | Pending description | Verify `GPCNLCLW`, `GPCNASPZ`, `GPCNASKZ`, `GPCNN190`, `GPCNP195`; choose natural flake 94-95% / -100 mesh primary. |
| Molybdenum | Present | Missing monthly benchmark | Candidate-control/proxy download | Search `MB-FEO-0003`, `MB-FEO-0004`, `MB-FEO-0001`, molybdic oxide Rotterdam/Busan only if time allows after treated wedges. |
| Antimony oxides | Present | Missing | Download required | Search `MB-SB-0004`, `MB-SB-0009`, antimony trioxide Rotterdam/Europe/CIF Antwerp-Rotterdam. |

## Data-Control Status

Demand and alternative-shock controls now present in the cleaned monthly panel:

- Global semiconductor sales, 3-month moving average.
- China semiconductor sales value, quarterly/seasonal.
- China BEV sales.
- China BEV passenger and commercial output.
- China power-battery loading capacity.
- China crude steel output.
- China lead-acid battery output.
- China manufacturing PMI.
- China PPI for nonmetal ores, chemicals, and nonferrous ores.
- EUR/USD and USD/CNY exchange rates.

Not usable from the downloaded files:

- China semiconductor chip output, because the exported series ends before the
  thesis window.
- Rare-earth price wedges, because no clean rare-earth series were downloaded
  and HS `284690` is too aggregated for the current price-wedge design.
