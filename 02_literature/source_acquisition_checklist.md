# Source Acquisition Checklist

Status: thesis-proposal corpus after the 2026-06-27 extra-paper intake.

This checklist tracks whether sources are available and usable for proposal
writing. It does not decide whether every source must be cited. Use
`02_literature/literature_master.md` for source roles and use
`02_literature/references.bib` as the only bibliography.

## Current Status

- Source folders: 57.
- Paper summaries: 57.
- Zotero collection: `Critical Minerals Export Controls` (`CUS6JZXH`).
- Zotero top-level bibliographic items in the collection: 57.
- Required Zotero tags: `critical-minerals` and `critical-minerals-export-controls`.
- Zotero citation-key audit: 57 citation keys, 0 missing, 0 duplicate citation keys.
- Local `references.bib` entries: 57.
- Local BibTeX alignment: 0 missing source-folder keys, 0 extra keys, 0 duplicate keys.
- Local source-folder convention: one folder per source under `02_literature/sources/`, with matching summary names.

## Ready For Proposal Use

| Role | Sources | Status |
|---|---|---|
| Economic statecraft and technology-control context | `farrell2019weaponized`, `farrell2023underground_empire`, `egger2024sanctions`, `bown2020semiconductor`, `bown2024semiconductors`, BIS 2022/2024 controls | Organized, summarized, in Zotero |
| Chinese legal and institutional background | `prc_2020_export_control_law`, `scio_2021_chinas_export_controls`, `prc2024_dual_use_regulations` | Organized, summarized, in Zotero |
| Core Chinese mineral-control episodes | MOFCOM Ga/Ge, graphite, antimony controls, license guides, approvals, FAQ, and review statements | Organized, summarized, in Zotero |
| Product and supply-chain heterogeneity | USGS 2026 mineral summaries, IEA 2025, Frenzel 2017, Park 2025, van den Brink 2022, Xu 2025 | Organized, summarized, in Zotero |
| Export licensing and NTM classification | `unctad2019ntm_classification`, `gamberale_tarasenko2023_export_licensing`, `oecd2026_crm_export_restrictions` | Organized, summarized, in Zotero |
| Administrative delay, time costs, policy uncertainty, and adjustment margins | `djankov_freund_pham2010_trading_on_time`, `hummels_schaur2013_time_trade_barrier`, `handley_limao2017_policy_uncertainty`, `handley_kamal_monarch2024_supply_chain_adjustments` | Organized, summarized, in Zotero |
| Trade-flow and panel methods | `santossilva2006gravity`, `fally2015_structural_gravity_fe`, `olden_moen2022_triple_difference`, `callaway2021difference`, `sun2021eventstudies`, `borusyak_jaravel_spiess2024_event_studies`, `dechaisemartin2020twfe`, `roth2022pretest`, `rambachan2023honest` | Organized, summarized, in Zotero |
| Few-shock and few-treated inference | `conley_taber2011_small_policy_changes`, `ferman_pinto2019_few_treated`, `mackinnon_webb2018_few_treated_clusters` | Organized, summarized, in Zotero |
| Price-wedge and commodity-market context | `martin_anderson2012_price_insulation`, `brander_bernauer_huss2023_trade_policy_volatility`, `worldbank2026_commodity_markets_outlook` | Organized, summarized, in Zotero |

## Manual Caveats

- The Zotero export is now installed as `02_literature/references.bib`.
- Use `prc2024_dual_use_regulations` only for claims visible in the local parsed text.
- Do not cite official approval statements as proof that controls were non-binding. Use them only to show that licensing systems allowed approval and review.
- Do not use product facts from USGS, IEA, OECD, or World Bank as causal evidence. They motivate exposure, market structure, and price-data interpretation.
- Keep 2025 W/Te/Bi/Mo/In and rare-earth controls as thesis expansion candidates unless the empirical design is explicitly expanded.

## Bibliography Check

Current check:

```bash
python - <<'PY2'
from pathlib import Path
import re
text = Path('02_literature/references.bib').read_text(errors='ignore')
keys = re.findall(r'@\w+\{([^,]+),', text)
print('entries', len(keys))
print('duplicate_keys', len(keys) - len(set(keys)))
PY2
```

Expected result: 57 entries and 0 duplicate keys.
