---
description: "Authoritative data inventory, coverage, source definitions, and remaining acquisition tasks"
created: 2026-06-04
modified: 2026-07-13
group: structure
tags: [project, critical-minerals, data, comtrade, eurostat, bloomberg, cepii]
status: active
---

# Data

This is the authoritative data-status document. Operational download items live
in `03_data/DOWNLOAD_CHECKLIST.md`.

## 1. UN Comtrade Monthly Trade

The current pressure-design panel covers January 2019 through March 2026. The
analysis panel uses 53 non-group reporters after excluding aggregate reporters
and China as an importer. The raw downloader may still target 56 configured
reporter codes, but reporter codes 97 (European Union), 975 (ASEAN), and 156
(China) are not part of the main importer panel.

A reporter-year file containing `skip` records a successful API response with
no observations; it is not a failed request.

### Current pressure-design panels

Run:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
```

Main outputs:

- `03_data/processed/product_scope_metadata.csv`;
- `03_data/processed/comtrade_pressure_country_product_month.csv`;
- `03_data/processed/comtrade_pressure_source_panel.csv`;
- `03_data/processed/comtrade_pressure_partner_panel.csv`;
- `03_data/processed/pressure_indices_importer_product.csv`;
- `03_data/processed/pressure_indices_product_summary.csv`;
- `03_data/processed/pressure_ppml_estimation_panel.csv`.

The strict clean estimation sample contains 147,552 source-level rows, 53
reporters, 16 products, 87 months, and two source groups. It includes four
main clean treated products and 12 donor candidates. The broader
policy-plus-control panel contains 202,884 source-level rows, 22 products, and
five secondary policy-scope cases.

### Bilateral imports

| HS | Product | Current coverage | Status |
|---|---|---:|---|
| 2504 | Natural graphite | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 811292 | Ga/Ge/In/V/Nb unwrought bundle | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 282560 | GeO2/ZrO2 | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 2818 | Alumina placebo | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 8111 | Manganese placebo | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 2811 | Inorganic-acids placebo | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026 |
| 3801 | Artificial and colloidal graphite | 448/448 reporter-year responses persisted through Mar 2026 | Complete through March 2026; special graphite scope case, not a clean control |
| 8110 | Antimony metal | 448/448 reporter-year responses persisted | Complete through March 2026 |
| 261710 | Antimony ores/concentrates | 448/448 reporter-year responses persisted | Complete through March 2026 |
| 282580 | Antimony oxides | 448/448 reporter-year responses persisted | Complete through March 2026 |

The final pre-download audit found 239 HS 8110 requests remaining for
2019-2024. On June 12, 2026, the downloader persisted 114 additional HS 8110
responses in the first run. A later run added another 209 HS 8110 responses
and seven HS 261710 responses before both keys began timing out. Failed and
interrupted tasks remain correctly classified as gaps. Extending a completed
product from December 2024 to March 2026 adds 112 reporter-year requests: 56
for 2025 and 56 for January-March 2026.

On June 13, 2026, a fresh quota window added 23 HS 8110, 384 HS 261710, and 43
HS 282580 responses before the API again stopped producing usable responses.
The exact remaining antimony gap count is 467.

On June 14, 2026, the refreshed API window completed HS 8110 and HS 261710
through March 2026 and added nearly all HS 282580. The merged antimony import
files now contain 49,396 rows for HS 8110, 9,134 rows for HS 261710, and 74,764
rows for HS 282580. Only two HS 282580 reporter-year files remain, both for
2026 (`2026_620.csv` and `2026_854.csv`). Direct API probes for those two files
returned quota-exhausted responses, so the remaining gaps are quota-related,
not known no-record responses.

On June 15, 2026, the final two HS 282580 reporter-year responses were
persisted, completing all three antimony bilateral series through March 2026.
The same quota window then downloaded most of the established-product
extension: 753 API calls returned 112,503 rows, 128 no-data responses, 31
errors, and 41 rate-limit responses. After merging, 324 extension gaps remain:
2504 (14), 811292 (14), 282560 (10), 2818 (10), 8111 (52), 2811 (112), and
3801 (112). A follow-up 48-call retry of 2504/811292/282560/2818 returned no
rows and did not close gaps, consistent with quota/refusal responses rather
than verified no-data.

On June 16, 2026, the remaining 324 established-product extension gaps were
closed. Final merged import-row counts are: 2504 (157,995), 811292 (73,408),
282560 (91,369), 2818 (406,561), 8111 (88,288), 2811 (680,018), 3801
(311,474), 8110 (49,396), 261710 (9,134), and 282580 (74,910). Dry-run audits
report zero gaps for both the antimony batch and the established-product batch
through March 2026.

On July 1, 2026, the downloader completed HS 8108 through March 2026. The
merged HS 8108 bilateral import file now contains 584,113 rows. The same run
also advanced HS 8109 to 6,871 merged rows with 422 reporter-year gaps
remaining and HS 8104 to 686 merged rows with 445 gaps remaining. End-of-run
dry-run audits report 5,347 downloader gaps in total: 4,003 in the main
31-product acquisition universe and 1,344 in excluded diagnostics HS 380120,
HS 2827, and broad HS 2617. The day ended because of API unreliability across
new-product probes, not confirmed quota exhaustion; direct probes on both keys
still returned immediate `200` no-data responses.

Later on July 1, 2026, the same day was continued. The downloader pushed
further on the unstable metal-family block and reduced the total gap count to
5,292, of which 3,948 remain in the main 31-product acquisition universe and
1,344 remain in excluded diagnostics. HS 8109 advanced again to 7,529 merged
rows with 401 gaps remaining. HS 8105 was the most productive target in this
continuation: it now has 15,810 merged rows with 417 gaps remaining. HS 8104
remained at 686 merged rows but now has 445 gaps remaining, and HS 282110
appears to have saved only no-data responses, reducing it to 445 remaining
gaps without creating a merged row file. Direct probes on both keys still
returned immediate `200` no-data responses for HS 8105 and HS 282110, so this
continuation also ended because of API unreliability and uneven product
behavior rather than confirmed quota exhaustion.

On July 2, 2026, the automation resumed with the required explicit Python path
and opened with a full dry-run audit. That audit showed 5,244 total downloader
gaps: 3,900 in the main 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. All earlier priority
products remained complete through March 2026, including HS 282570, HS 8106,
HS 284180, HS 8101, HS 8103, and HS 8108.

The run then tried to reopen the remaining metal-family queue in priority
order. HS 8109 was probed three times with one-worker chunks and two enforced
cooldowns. The product only partially moved: its merged bilateral import file
increased to 10,571 rows and the remaining gap count fell from 401 to 398.
HS 8104 was then probed once, but it immediately showed the same one-call,
one-error behavior and remained at 686 merged rows with 445 gaps.

The closing dry run settled at 5,241 total downloader gaps: 3,897 in the main
31-product acquisition universe and 1,344 in excluded diagnostics. The current
main-universe queue is HS 8109 (398), HS 8104 (445), HS 8105 (382), HS 282110
(432), HS 2820 (448), HS 2833 (448), HS 284610 (448), HS 280450 (448), and
HS 284690 (448). No additional products were completed today. Approximate
counted API usage was only about 4-6 calls because repeated requests slowed to
roughly one completion per minute and mostly ended in transport errors rather
than productive responses. The day therefore ended because of extended API
unreliability and reachability problems, not confirmed quota exhaustion.

Later on July 2, 2026, the automation resumed again and found that the live
queue had already shifted before any new calls were made. A fresh dry-run
audit opened at 5,193 total downloader gaps: 3,849 in the main 31-product
acquisition universe and 1,344 in excluded diagnostics. HS 8109 had already
fallen to 350 remaining gaps at that point, indicating that some previously
saved files had settled onto disk between runs.

The continuation first retried HS 8109 with one-worker chunks. Live behavior
was still unstable, but force-merges revealed meaningful saved progress. The
merged HS 8109 bilateral import file increased from 10,571 rows to 24,832
rows, and the remaining gap count fell further to 311.

The run then pivoted hard to HS 8104 because it was the first product to yield
steady counted calls rather than pure transport churn. Three completed chunks
plus one interrupted partial chunk pushed HS 8104 from 686 merged rows with
445 remaining gaps to 148,953 merged rows with only 179 remaining gaps. The
productive completed chunks alone delivered 134 counted API calls, 93,806 new
rows, 7 valid no-data files, and 16 logged errors, with one explicit
rate-limit response in the first productive chunk. The interrupted fourth
chunk added further rows before being force-merged once its pace degraded.

The closing dry run for this later July 2 continuation settled at 4,888 total
downloader gaps: 3,544 in the main 31-product acquisition universe and 1,344
in excluded diagnostics. The updated main-universe queue is HS 8109 (311), HS
8104 (179), HS 8105 (382), HS 282110 (432), HS 2820 (448), HS 2833 (448), HS
284610 (448), HS 280450 (448), and HS 284690 (448). Approximate counted API
usage for the continuation was about 275-315 calls after including the
completed HS 8104 chunks, the interrupted partial HS 8104 chunk, and the
unstable HS 8109 probes. This continuation still did not end by confirmed true
quota exhaustion. It ended because the active chunk had become increasingly
uneven, so the progress was banked with a force-merge and a fresh full audit.

On July 3, 2026, the automation resumed with the required explicit Python path
and a full dry-run audit over the complete downloader universe. The opening
audit showed 4,880 total downloader gaps: 3,536 in the main 31-product
acquisition universe and 1,344 in excluded diagnostics HS 380120, HS 2827,
and broad HS 2617. All earlier priority products were already complete through
March 2026, so the active queue began at HS 8109, then HS 8104, HS 8105, and
the deferred products.

The most productive completed chunk was an HS 8109 one-worker 150-call run. It
returned 147 counted API calls, 32,260 new rows, 10 valid no-data files, and 3
errors, cutting HS 8109 from 311 remaining gaps to 164. Follow-up partial
retries on HS 8109, HS 8104, and HS 8105 were then manually stopped and
force-merged once they slowed into a low-yield pattern. After cleaning up
lingering downloader processes and re-merging the touched products, the merged
files settled at 66,800 rows for HS 8109, 202,890 rows for HS 8104, and 47,504
rows for HS 8105.

The settled final audit for July 3 reports 4,632 total downloader gaps: 3,288
in the main 31-product universe and 1,344 in excluded diagnostics. The current
main-universe queue is HS 2820 (448), HS 2833 (448), HS 284610 (448), HS
280450 (448), HS 284690 (448), HS 282110 (432), HS 8105 (373), HS 8109 (139),
and HS 8104 (104). No additional product was fully completed today, but the
day still closed 248 main-universe reporter-year gaps. Approximate counted API
usage was about 260-275 calls after combining the completed HS 8109 chunk with
the partial HS 8109, HS 8104, and HS 8105 continuations. This run did not end
by true quota exhaustion. There were no persistent `429` walls, no repeated
cross-key `403 Out of call volume quota` refusals, and no terminal
`Retry-After` signal. It ended because Comtrade remained reachable but slow and
uneven, making further same-session chunks low-yield.

Later on July 3, 2026, the same run was continued after user instruction to
wait through the slowdown and keep trying until true exhaustion was observed.
After a 10-minute cooldown, HS 8109 reopened cleanly. Three more one-worker
chunks plus a final one-file probe fully completed the product. Those follow-on
HS 8109 runs delivered 139 counted API calls, 23 valid no-data files, 6
errors, and 23,780 additional rows, moving the merged HS 8109 file from 66,800
rows to 90,580 rows and reducing the remaining gap count from 139 to zero.

The same live window then shifted to HS 8104. A 75-call one-worker chunk and a
29-file cleanup run both executed cleanly, adding 40,304 rows, 27 valid
no-data files, and zero errors. HS 8104 therefore moved from 202,890 merged
rows with 104 remaining gaps to 243,194 merged rows with zero remaining gaps.

HS 8105 did not reopen as well. One partial chunk before cooldown pushed its
merged file from 47,504 rows to 52,064 rows and cut the remaining gaps from
373 to 366, but a post-cooldown retry reverted to the familiar sterile
one-completion-per-minute pattern with no saved rows or no-data files. The run
rotated once to HS 282110, and that product showed the same sterile pattern.
Because the downloader script can mask subscription refusals as zero-row
completions, both keys were then probed directly on a still-missing HS 282110
request.

Those direct probes finally confirmed true quota exhaustion on both keys. At
17:12 CST on July 3, 2026, each key returned `403 Out of call volume quota`
with `Retry-After` headers of about 53,258 seconds, implying replenishment in
roughly 14 hours 47 minutes. This is the first hard stop condition of the day
and supersedes the earlier temporary API-unreliability stop.

The settled final audit for the full July 3 run reports 4,382 total downloader
gaps: 3,038 in the main 31-product universe and 1,344 in excluded diagnostics.
The remaining main-universe queue is now HS 2820 (448), HS 2833 (448), HS
284610 (448), HS 280450 (448), HS 284690 (448), HS 282110 (432), and HS 8105
(366). The main-universe products HS 8109 and HS 8104 are now complete through
March 2026. Approximate total counted API usage for the full July 3 run was
about 400-420 calls plus two direct quota-confirmation probes. The day ended by
confirmed true quota exhaustion, not by mere API unreliability.

On July 4, 2026, the automation resumed with the required explicit Python path
and opened with the mandatory full dry-run audit. That audit confirmed 4,382
total downloader gaps at the start of the session: 3,038 in the main
31-product universe and 1,344 in excluded diagnostics HS 380120, HS 2827, and
broad HS 2617. All higher-priority unfinished products ahead of HS 8105 were
already complete through March 2026, so the run stayed on cobalt.

An initial oversized 150-call HS 8105 chunk proved too slow to be a sensible
checkpoint and was manually interrupted after a small amount of saved progress.
Two follow-up one-worker 25-call HS 8105 chunks then completed cleanly,
returning 29,417 rows, four valid no-data responses, zero errors, and zero
rate-limit responses. A final 25-call HS 8105 continuation degraded again into
low-yield behavior after only a few saved files and was manually interrupted,
then force-merged.

After all forced and normal merges settled, HS 8105 advanced from 52,064
merged rows with 366 remaining reporter-year gaps to 82,820 merged rows with
303 remaining gaps. The closing full dry run for July 4 reports 4,319 total
downloader gaps: 2,975 in the main 31-product universe and 1,344 in excluded
diagnostics. The remaining main-universe queue is now HS 2820 (448), HS 2833
(448), HS 284610 (448), HS 280450 (448), HS 284690 (448), HS 282110 (432),
and HS 8105 (303). Approximate counted API usage was about 58-60 calls after
combining the two completed 25-call chunks with the two interrupted partial HS
8105 chunks. The day did not end by confirmed quota exhaustion: there were no
persistent `429` walls, no repeated cross-key `403 Out of call volume quota`
refusals, and no terminal `Retry-After` signal. It ended because same-session
throughput degraded back into a low-yield pattern, so the productive cobalt
progress was banked with a force-merge and fresh dry-run audit.

Later on July 4, 2026, the automation was resumed again with explicit
instruction to keep downloading until true exhaustion rather than stopping at a
mere slowdown checkpoint. The continuation opened from the settled earlier
July 4 audit state: 4,319 total downloader gaps, of which 2,975 were in the
main 31-product universe and 1,344 were in excluded diagnostics HS 380120,
HS 2827, and broad HS 2617.

The continuation first stayed on HS 8105. Productive one-worker chunks plus a
small force-merged partial reopening completed cobalt through March 2026. The
merged HS 8105 file rose from 82,820 rows with 303 remaining gaps to 225,694
rows with zero remaining gaps. The late-year tail proved especially productive:
after the 2024 files were closed, the 2025-2026 block returned many valid
no-data responses and the final 32-file 2026 tail completed in 1.6 minutes
with 11 saved empty responses and no errors.

After HS 8105 completed, the run rotated to HS 282110. That product was much
more open than in earlier sessions. Three completed one-worker chunks plus one
force-merged partial chunk increased the merged HS 282110 file from 8,138 rows
with 432 remaining gaps to 92,052 rows with 296 remaining gaps. The remaining
HS 282110 gaps are now concentrated in 2021-2026, with only 2021 partially
closed.

Approximate counted API usage for the full later-July-4 continuation was about
446 downloader calls plus two direct quota-confirmation probes. Across the two
main touched products, the continuation saved about 226,788 additional merged
rows. The stop condition is now confirmed true quota exhaustion rather than
mere API unreliability. At about 15:33 CST on July 4, 2026, both keys were
probed directly on a still-missing HS 282110 request and each returned
`403 Out of call volume quota` with `Retry-After` headers of about 59,172
seconds, implying replenishment in roughly 16 hours 26 minutes.

The settled closing dry run for the full July 4 work reports 3,880 total
downloader gaps: 2,536 in the main 31-product universe and 1,344 in excluded
diagnostics. The remaining main-universe queue is now HS 282110 (296), HS 2820
(448), HS 2833 (448), HS 284610 (448), HS 280450 (448), and HS 284690 (448).
HS 8105 is now complete through March 2026. The day therefore ended by
confirmed true quota exhaustion, not by low-yield API behavior alone.

On July 5, 2026, the automation resumed from that settled state with the
required explicit Python path and a fresh full dry-run audit. The opening audit
again reported 3,880 total downloader gaps: 2,536 in the main 31-product
universe and 1,344 in excluded diagnostics HS 380120, HS 2827, and broad
HS 2617.

The run first stayed on HS 282110 and fully completed it through March 2026.
Multiple completed one-worker chunks plus a late exact-tail cleanup moved the
merged HS 282110 file from 92,052 rows with 296 remaining gaps to 250,828 rows
with zero remaining gaps. The final remaining 2026 tail closed cleanly with a
mix of saved no-data responses and one final 21-row file.

The same quota window then shifted to HS 2820. Three productive completed
chunks and one force-merged partial chunk increased the merged HS 2820 file
from zero to 39,990 rows and reduced its remaining gap count from 448 to 294.
The product then entered the familiar masked-refusal pattern: one-completion
per minute stretches with no new rows, no valid no-data files, and no counted
errors. Two cooldown cycles plus smaller reopen attempts did not restore useful
responses on HS 2820, so the run rotated to HS 2833 as required by the
persistence rule.

HS 2833 immediately showed the same sterile completion pattern. Direct probes
on a still-missing HS 2833 request then confirmed true quota exhaustion on both
keys. At about 15:36 CEST on July 5, 2026, each key returned
`403 Out of call volume quota` with `Retry-After` headers of about 37,427
seconds, implying replenishment in roughly 10 hours 24 minutes.

The settled closing dry run for July 5 reports 3,430 total downloader gaps:
2,086 in the main 31-product universe and 1,344 in excluded diagnostics. The
remaining main-universe queue is now HS 2820 (294), HS 2833 (448), HS 284610
(448), HS 280450 (448), and HS 284690 (448). HS 282110 is now complete through
March 2026. Approximate counted downloader usage for July 5 was about 509
downloader calls plus two direct quota-confirmation probes. The day therefore
ended by confirmed true quota exhaustion, not by mere API unreliability.

On July 6, 2026, the automation resumed with the required explicit Python path
and a full dry-run audit. The opening audit again showed 3,430 total
downloader gaps: 2,086 in the main 31-product acquisition universe and 1,344
in excluded diagnostics HS 380120, HS 2827, and broad HS 2617. All higher
priority products above HS 2820 remained complete, so the run stayed on the
remaining deferred/marginal queue.

HS 2820 reopened first. Short one-worker chunks initially looked sterile, but
the early interrupted process continued running in the background and was only
fully reconciled after explicit cleanup. After killing the stale chunk process
and force-merging again, the merged HS 2820 file rose from 39,990 rows to
53,127 rows and its remaining gaps fell from 294 to 231.

HS 2833 was then tested twice. The first short chunk saved only a few files,
but a completed 25-call one-worker chunk then delivered 22 counted API calls,
21,390 new rows, three errors, and one rate-limit response. A later interrupted
HS 2833 chunk also continued briefly in the background until it was cleaned up
and re-merged. After that cleanup, the merged HS 2833 file stood at 32,487
rows and its remaining gaps had fallen from 448 to 414.

Two direct probes on a still-missing HS 2833 request clarified the stop
condition. One key returned a clean `200` response with `count: 0`; the other
returned a transient `429` with `Retry-After: 1`. That pattern is not true
quota exhaustion. It shows that Comtrade remained reachable but unstable, with
some requests resolving cleanly and others briefly throttled.

The settled closing audits for July 6 report 3,333 total downloader gaps:
1,989 in the main 31-product universe and 1,344 in excluded diagnostics. The
remaining main-universe queue is now HS 2820 (231), HS 2833 (414), HS 284610
(448), HS 280450 (448), and HS 284690 (448). No additional product was fully
completed today. Approximate observed usage was at least about 31 counted
downloader calls plus two direct quota-state probes, and the true call count
was likely somewhat higher because two interrupted one-worker chunks kept
running briefly in the background before they were killed and force-merged. The
day therefore ended by renewed API unreliability, not by confirmed quota
exhaustion.

On July 7, 2026, the automation resumed with the required explicit Python path
and the mandatory full dry-run audit. That opening audit reported 3,333 total
downloader gaps: 1,989 in the main 31-product acquisition universe and 1,344
in excluded diagnostics HS 380120, HS 2827, and broad HS 2617. All earlier
priority products above HS 2820 again remained complete, so the run stayed on
the remaining deferred and marginal main-universe queue.

HS 2820 reopened cleanly and remained productive throughout two completed
one-worker chunks plus a short cleanup pass. The first 150-target chunk
delivered 150 counted API calls, 37,018 new rows, 14 valid no-data responses,
zero errors, and 11 rate-limit responses. A second 92-target chunk delivered
92 counted API calls, 8,484 additional rows, 28 valid no-data responses, zero
errors, and 16 rate-limit responses. A final 16-file cleanup pass added 1,161
rows, two valid no-data responses, one error, and two rate-limit responses.
After normal merges, the HS 2820 bilateral import file rose from 53,127 rows
to 99,790 rows and its remaining gaps fell from 231 to just 3.

The run then pivoted to HS 2833. The initial 150-target one-worker chunk was
productive but would have taken too long to finish cleanly inside the current
run, so it was manually interrupted at a checkpoint and then force-merged with
the downloader's `merge_all` helper. The settled post-merge HS 2833 file rose
from 32,487 rows to 95,441 rows and its remaining gaps fell from 414 to 359.

The settled closing audit for July 7 reports 3,050 total downloader gaps:
1,706 in the main 31-product universe and 1,344 in excluded diagnostics. The
remaining main-universe queue is now HS 2820 (3), HS 2833 (359), HS 284610
(448), HS 280450 (448), and HS 284690 (448). Approximate observed usage was at
least about 309 counted downloader calls. The true total was slightly higher
because the interrupted HS 2833 chunk kept advancing briefly between the last
progress report and the forced merge. The run did not end by true quota
exhaustion. It also did not hit a sterile unreliability wall. It ended by a
manual checkpoint while the API was still producing usable responses.

At the current backlog, the optimistic remaining timeline is about 2 more API
days if the downloader can consistently use 900-1,000 useful calls. A more
realistic near-term pace is about 5-7 days if the window behaves like the
recent 250-350 call sessions. A pessimistic pace with repeated low-yield
windows would be roughly 15-22 days. The next priority is to finish the last 3
HS 2820 gaps, then continue down HS 2833, HS 284610, HS 280450, and HS 284690.

On July 8, 2026, the automation resumed with the required explicit Python path
and the mandatory full dry-run audit over the full downloader universe. That
opening audit reported 3,050 total downloader gaps: 1,706 in the main
31-product acquisition universe and 1,344 in excluded diagnostics HS 380120,
HS 2827, and broad HS 2617. All earlier priority products above HS 2820 again
remained complete, so the live main-universe queue was HS 2820 (3), HS 2833
(359), HS 284610 (448), HS 280450 (448), and HS 284690 (448).

HS 2820 was closed first with a tiny one-worker cleanup chunk. All three
remaining reporter-year requests succeeded cleanly, adding 1,489 rows and
lifting the merged HS 2820 bilateral import file from 99,790 rows to 101,279
rows. HS 2820 is now complete through March 2026.

The run then moved to HS 2833. A 150-target one-worker chunk opened
productively but degraded into an extremely slow pattern of roughly one saved
file every 35-40 seconds, so it was manually interrupted and force-merged to
bank the valid partial progress. The settled HS 2833 file rose from 95,441
rows to 111,731 rows and its remaining gaps fell from 359 to 354.

After the required cooldown, HS 284610 was probed with a smaller one-worker
chunk. That retry confirmed the session had become unreliable rather than
quota-exhausted: over a 25-target chunk, only one counted API call succeeded,
producing 258 rows, while the remaining attempts resolved as downloader
errors. After the normal merge, HS 284610 now has 258 merged rows and 447
remaining gaps.

The settled closing audit for July 8 reports 3,041 total downloader gaps:
1,697 in the main 31-product universe and 1,344 in excluded diagnostics. The
remaining main-universe queue is now HS 2833 (354), HS 284610 (447), HS 280450
(448), and HS 284690 (448). Approximate counted API usage for the day was only
about 9 successful downloader calls: 3 for HS 2820, about 5 banked through the
interrupted HS 2833 chunk, and 1 for HS 284610. The day did not end by true
quota exhaustion. There was no persistent `429` wall, no repeated cross-key
`403 Out of call volume quota` refusal, and no explicit quota-reset signal. It
ended by severe API unreliability and very low throughput after the initial
HS 2820 cleanup.

At the current backlog, the optimistic remaining timeline is still about 2 API
days if the downloader can actually use a full 900-1,000 useful calls. A more
realistic near-term pace is now about 7-10 days if usable windows close
roughly 170-250 gaps per day. A pessimistic low-yield path like July 8 would
stretch the remaining main-universe download time to roughly 30-40 days. The
next priority is HS 2833, then HS 284610, then HS 280450, and finally HS
284690.

On July 9, 2026, the automation resumed with the required explicit Python path
and the mandatory full dry-run audit over the full downloader universe. That
audit again reported 3,041 total downloader gaps: 1,697 in the main
31-product acquisition universe and 1,344 in excluded diagnostics HS 380120,
HS 2827, and broad HS 2617. The live main-universe queue therefore remained HS
2833 (354), HS 284610 (447), HS 280450 (448), and HS 284690 (448).

The run then attempted to reopen HS 2833 with a conservative one-worker
50-target chunk. That chunk immediately completed with zero counted API calls,
zero rows, zero valid no-data responses, and zero logged rate-limit events.
Its verification pass left HS 2833 unchanged at 111,731 merged rows and 354
remaining gaps. A direct credential audit then established the real blocker:
the automation shell had no `COMTRADE_API_KEYS`, `COMTRADE_API_KEY`,
`COMTRADE_API_KEY_1`, or `COMTRADE_API_KEY_2` in its environment, and
`04_scripts/comtrade_auth.py` raised `RuntimeError: No Comtrade API key
configured`.

No products advanced on July 9, and no additional merged rows were created.
Approximate counted API usage was zero because the downloader never obtained a
usable key and therefore never reached the Comtrade endpoint. The day did not
end by true quota exhaustion and did not end by API unreliability. It ended
because the execution environment was missing Comtrade credentials entirely.

At the unchanged backlog, the optimistic remaining timeline is still about 2
API days if future runs can actually consume 900-1,000 useful calls. A more
realistic near-term pace remains about 7-10 days if usable windows close
roughly 170-250 gaps per day. A pessimistic low-yield path like July 8 would
still stretch the remaining main-universe download time to roughly 30-40 days.
The next priority remains HS 2833, then HS 284610, then HS 280450, and
finally HS 284690, but the automation must restore `COMTRADE_API_KEYS` or
`COMTRADE_API_KEY_1`/`COMTRADE_API_KEY_2` before any further downloader run can
spend quota.

Later on July 9, 2026, a follow-up rerun confirmed that the blocker had not
changed. The standard full dry-run audit still reported 3,041 total downloader
gaps: 1,697 in the main 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. A second HS 2833 probe used
`--max-calls 75 --workers 1`, but it again completed with zero counted API
calls and left HS 2833 unchanged at 111,731 merged rows and 354 remaining
gaps. Additional checks found no Comtrade credential wiring in the repository,
`~/.zshrc`, `~/.zprofile`, or recent Codex shell snapshots, so the run again
ended because credentials were missing entirely, not because of quota
exhaustion or API unreliability. No products advanced and observed counted API
usage remained zero. Estimated days left and the next-priority queue are
therefore unchanged: optimistic about 2 API days, realistic about 7-10 days,
pessimistic about 30-40 days, with HS 2833 still first, then HS 284610, HS
280450, and HS 284690 once credentials are restored.

An additional retry later the same day produced the same result. A fresh full
dry-run audit still reported 3,041 total downloader gaps, and a one-file live
HS 2833 probe with `--max-calls 1 --workers 1` again finished with zero
counted API calls, zero rows, zero no-data files, zero errors, and zero
rate-limit responses. A direct call to `load_comtrade_keys()` still raised
`RuntimeError: No Comtrade API key configured`, and the shell still lacked
`COMTRADE_API_KEYS`, `COMTRADE_API_KEY`, `COMTRADE_API_KEY_1`, and
`COMTRADE_API_KEY_2`. The backlog, ETA range, and next-priority queue are
therefore unchanged.

Later on July 9, 2026, the credential source was restored and persisted
locally, which reopened the downloader immediately. A one-file HS 2833 probe
returned a normal `200` response with 194 rows, confirming that the earlier
July 9 failures had been caused by missing credentials rather than by expired
keys, quota exhaustion, or a Comtrade outage.

The same continuation then stayed on HS 2833 until it was complete through
March 2026. Including the opening one-file probe, the completed HS 2833 chunks
returned 394 counted API calls, 377,200 new rows, 38 valid no-data files, one
timeout, and repeated but non-terminal rate-limit responses in the late-2025
/2026 tail. The merged HS 2833 bilateral import file increased from 111,731
rows to 488,931 rows and its remaining gap count fell from 354 to zero.

With HS 2833 closed, the run pivoted to HS 284610. An opening one-worker
25-call chunk returned 25 counted API calls, 9,152 new rows, two valid no-data
files, zero errors, and zero rate-limit responses. The merged HS 284610 file
increased from 258 rows to 9,410 rows, and its remaining gap count fell from
447 to 422.

The closing July 9 audit reported 2,662 total downloader gaps: 1,318 in the
main 31-product acquisition universe and 1,344 in excluded diagnostics HS
380120, HS 2827, and broad HS 2617. The remaining main-universe queue is now
HS 284610 (422), HS 280450 (448), and HS 284690 (448). Approximate counted API
usage for this productive continuation was 419 successful/rate-limited
requests. The run did not end by true quota exhaustion and did not end by API
unreliability. It ended by a manual checkpoint while the API was still
producing useful rows and valid no-data responses. At the new backlog, the
optimistic remaining timeline is about 2 API days, a realistic near-term pace
is about 4-6 days, and a pessimistic low-yield path is about 12-18 days. The
next priority is HS 284610, then HS 280450, then HS 284690.

Later that same run, continuing into just after midnight local time on July 10,
2026, the downloader resumed from the restored-key state and continued until
true exhaustion was visible across products. A fresh full audit opened at
2,662 total downloader gaps: 1,318 in the main 31-product acquisition universe
and 1,344 in excluded diagnostics. The live main-universe queue therefore
began at HS 284610, then HS 280450, then HS 284690.

The run spent the next useful block on HS 284610 with a one-worker 100-call
chunk. That block remained productive through most of the run, then slowed into
a late refusal tail. After a manual checkpoint and force-merge, the merged HS
284610 file increased from 9,410 rows to 21,592 rows, and the remaining gap
count fell from 422 to 337. The settled continuation gain on HS 284610 was
12,182 rows and 85 closed reporter-year gaps, with approximately 91 counted
API calls inside the interrupted 100-target block.

To test whether the slowdown was product-specific or a true daily stop, the run
then probed HS 280450 and HS 284690 with minimal one-worker chunks. HS 280450
returned one counted API call with zero rows, zero valid no-data responses, and
a terminal `failed_retries` status after the refusal cycle. HS 284690 then
returned two counted API calls with zero rows, zero valid no-data responses,
and `failed_retries` on both requests in the same process. That cross-product,
cross-key refusal pattern meets the run rule for true exhaustion more closely
than API unreliability: the endpoint remained reachable, but the calls stopped
yielding usable responses and instead cycled through non-productive refusals.

The closing audit after those exhaustion probes reported 2,577 total downloader
gaps: 1,233 in the main 31-product acquisition universe and 1,344 in excluded
diagnostics. The remaining main-universe queue is now HS 284610 (337), HS
280450 (448), and HS 284690 (448). Approximate counted API usage for this
late continuation was 94 calls: about 91 in the productive/interrupted
HS 284610 block, one refusal probe on HS 280450, and two refusal probes on
HS 284690. This continuation ended by true quota/refusal exhaustion rather
than by API unreliability. At the new backlog, the optimistic remaining
timeline is still about 2 API days, a realistic near-term pace is about 4-5
days, and a pessimistic low-yield path is about 10-15 days. The next priority
remains HS 284610, then HS 280450, then HS 284690 on the next quota window.

Later on July 10, 2026, the automation resumed from that checkpoint with the
required explicit Python path and a fresh full dry-run audit. That opening
audit still showed 2,577 total downloader gaps, split into 1,233 gaps in the
main 31-product acquisition universe and 1,344 gaps in excluded diagnostics HS
380120, HS 2827, and broad HS 2617. The live main-universe queue therefore
began at HS 284610 (337), then HS 280450 (448), then HS 284690 (448).

The first HS 284610 probe remained low-yield. An interrupted one-worker chunk
added only two persisted reporter-year files at first, and a later retry in
the improved API window added only two more. After both force-merges, the
merged HS 284610 file increased from 21,592 rows to 24,682 rows and its
remaining gap count fell from 337 to 333. That behavior never crossed into a
true quota wall, but it stayed too slow and uneven to justify spending the
rest of the day there while another product was producing real progress.

The productive center of the run was HS 280450. After one weak opening probe
and one required cooldown, successive one-worker chunks closed the product
through March 2026. The merged HS 280450 bilateral import file rose from no
merged file at all to 40,516 rows, and the remaining gap count fell from 448
to zero. Productive completed chunks on HS 280450 included a 25-target retry
that delivered 23 counted calls and 2,327 rows, three straight 100-target
chunks that delivered 100 counted calls each, a 28-file cleanup chunk, a
6-file tail chunk, and a final 1-file no-data closeout. Across the full day,
HS 280450 accounted for 391 counted calls by itself and was the only product
that behaved like a normal usable Comtrade window for a sustained stretch.

The final priority product, HS 284690, did not reopen. Two separate one-worker
probes, one before a 10-minute cooldown and one after, both fell into the same
non-productive pattern: roughly one counted call per minute, zero rows, zero
valid no-data files, zero logged errors, no terminal 429 wall, and no
persisted files to merge. Because that behavior persisted across retries
without a cross-key refusal pattern strong enough to classify as true quota
exhaustion, the run is best classified as ending because of API unreliability
and endpoint unevenness rather than because the daily quota was clearly spent.

The closing audit for this later July 10 continuation reports 2,125 total
downloader gaps: 781 in the main 31-product acquisition universe and 1,344 in
excluded diagnostics. The remaining main-universe queue is now HS 284690
(448), then HS 284610 (333). Approximate counted API usage for the day was
about 408 calls: roughly 391 on HS 280450, about 7 on the two interrupted HS
284610 probes, about 7 on the two non-productive HS 284690 probes, and about 3
on the initial low-yield HS 280450 opening probe. One main-universe product
was fully completed today: HS 280450. At the new backlog, the optimistic
remaining timeline is about 1 more strong API day, a realistic near-term pace
is about 2-3 days, and a pessimistic low-yield path is about 5-8 days. The
next priority remains HS 284610, then HS 284690.

On July 11, 2026, the automation resumed with the required explicit Python
path and a fresh full dry-run audit. That opening audit showed 2,125 total
downloader gaps: 781 in the main 31-product acquisition universe and 1,344 in
excluded diagnostics HS 380120, HS 2827, and broad HS 2617. All earlier
priority products were already complete through March 2026, so the live
main-universe queue had narrowed to HS 284610 first and HS 284690 second.

The productive center of the run was HS 284610. Two completed 150-target
one-worker chunks and one completed 67-file cleanup chunk pushed the merged HS
284610 bilateral import file from 24,682 rows to 93,612 rows. The remaining
gap count fell from 333 to 20. Across those completed cerium chunks, the
downloader recorded 366 counted API calls, 68,930 new rows, 53 valid no-data
responses, 1 logged error, and 53 reported rate-limit/refusal-cycle outcomes.
The late-stage cerium tail then reverted to the sterile one-completion-per-
minute pattern seen on the previous day, so the final partial cerium retry was
interrupted and force-merged with no new saved files.

HS 284690 opened productively at first but never stabilized after its first
large pass. One completed 150-target one-worker chunk added 45,832 rows and 12
valid no-data responses, cutting HS 284690 from 448 remaining gaps to 315.
After that, the product repeatedly fell into sterile post-cooldown retries:
roughly one completed request per minute, zero rows, zero valid no-data files,
zero logged errors, and no clear 429 wall. Two cooldown cycles plus a final
rotation back to cerium failed to restore productive behavior on either
remaining main-universe product.

The closing audit for July 11 reports 1,679 total downloader gaps: 335 in the
main 31-product acquisition universe and 1,344 in excluded diagnostics. The
remaining main-universe queue is now HS 284690 (315), then HS 284610 (20).
Approximate counted API usage for the day was about 520-530 calls: 516 from
the four completed productive chunks plus roughly a dozen sterile partial
completions in the interrupted retries. No main-universe product fully closed
today, but the run still eliminated 446 main-universe reporter-year gaps. The
day ended because of extended API unreliability and non-closing behavior
across both remaining products, not confirmed true quota exhaustion. At the new
backlog, the optimistic remaining timeline is about 1 more strong API day, a
realistic near-term pace is about 2 days, and a pessimistic low-yield path is
about 4-7 days. The next priority remains HS 284610, then HS 284690.

On July 12, 2026, the automation resumed with the required explicit Python
path and a fresh full dry-run audit. That opening audit again showed 1,679
total downloader gaps: 335 in the main 31-product acquisition universe and
1,344 in excluded diagnostics HS 380120, HS 2827, and broad HS 2617. All
earlier priority products were already complete through March 2026, so only
HS 284610 and HS 284690 remained in the live main-universe queue.

The run fully closed the planned 31-product universe in one sustained session.
HS 284610 was taken from 20 remaining gaps to zero, and its merged bilateral
import file increased from 93,612 rows to 94,308 rows. HS 284690 was then
taken from 315 remaining gaps to zero, and its merged bilateral import file
increased from 45,832 rows to 136,050 rows. Across the full day, the
downloader recorded 391 counted API calls, 90,914 new rows, 58 valid no-data
responses, zero logged errors, and repeated but non-terminal rate-limit/
refusal-cycle outcomes during several tail chunks.

The closing audit for July 12 reports 1,344 total downloader gaps, all in the
excluded diagnostics HS 380120, HS 2827, and broad HS 2617. The main
31-product acquisition universe now has zero remaining gaps through March
2026. The run ended by objective completion, not by true quota exhaustion and
not by API unreliability. For the planned universe, the optimistic, realistic,
and pessimistic remaining timelines are all zero days. No remaining
main-universe priority product is left.

On July 13, 2026, the automation ran the required full dry-run audit before
attempting any new calls:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

The audit again reported 1,344 total downloader gaps, all in the excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. The main 31-product
acquisition universe remained fully complete through March 2026 with zero
remaining gaps, so the automation correctly made no additional download
attempts and consumed approximately zero counted API calls today.

The completed main-universe merged bilateral row counts are unchanged: HS 8110
(49,396), HS 261710 (9,134), HS 282580 (74,910), HS 2504 (157,995), HS 811292
(73,408), HS 282560 (91,369), HS 2818 (406,561), HS 8111 (88,288), HS 2811
(680,018), HS 3801 (311,474), HS 8106 (56,196), HS 284180 (41,003), HS 8101
(298,432), HS 2615 (75,088), HS 284170 (105,418), HS 811221 (65,314), HS
380130 (75,309), HS 282530 (28,858), HS 282520 (51,644), HS 282570 (40,217),
HS 8103 (90,354), HS 8108 (584,113), HS 8109 (90,580), HS 8104 (243,194), HS
8105 (225,694), HS 282110 (250,828), HS 2820 (101,279), HS 2833 (488,931), HS
284610 (94,308), HS 280450 (40,516), and HS 284690 (136,050).

The stop reason for July 13 is still objective completion of the planned
universe, not true quota exhaustion and not API unreliability. Estimated days
left for the planned 31-product universe remain zero under optimistic,
realistic, and pessimistic assumptions. If excluded diagnostics are ever
reactivated, the remaining backlog is unchanged at 448 gaps each for HS
380120, HS 2827, and broad HS 2617.

HS 2501 remains excluded because bilateral coverage is too sparse. It should
not be described as a rare-earth case. HS 3801 is not a valid untreated
placebo: some artificial graphite grades were controlled under the December
2023 policy. Its final role is a special graphite scope case, not a clean
control.

### Canonical thesis panel

Run:

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
```

Outputs:

- `03_data/processed/comtrade_thesis_country_product_month.csv`;
- `03_data/processed/comtrade_thesis_source_panel.csv`;
- `03_data/output/tables/comtrade_thesis_data_audit.csv`.

The balanced country-product panel contains 53 country reporters x 10 products
x 87 months = 46,110 rows. The China/rest-of-world source panel contains
92,220 rows.

The preparation script retains only the canonical aggregate record:

- `partner2Code = 0`;
- `customsCode = C00`;
- `motCode = 0`;
- `mosCode = 0`.

This matters because the raw files contain World totals, bilateral partners,
secondary-partner records, customs-procedure records, and transport-mode
records. Summing those rows together double counts trade. `analysis_final.py`
does this in its legacy triple-difference construction and is not a valid
source for new thesis claims.

World totals reconcile to the sum of bilateral partners up to rounding error.
China-reported export files are already one World-partner aggregate record per
month and do not have this duplication problem.

### Outcome coverage

Trade value is the primary bilateral outcome. China net-weight coverage is:

| HS | China net-weight coverage |
|---|---:|
| 2504 | 46.9% |
| 811292 | 26.7% |
| 282560 | 44.9% |
| 3801 | 64.5% |
| 2818 | 77.5% |
| 8111 | 57.4% |
| 2811 | 84.1% |

Physical quantities are a complete-case robustness outcome, not a substitute
for trade value.

### China aggregate exports

| HS | Coverage | Status |
|---|---:|---|
| 2504 | 72/72 | Complete |
| 811292 | 72/72 | Complete |
| 282560 | 72/72 | Complete |
| 3801 | 72/72 | Complete |
| 8110 | 69/72 reported months | Audited; Oct-Dec 2024 are genuine no-record months |
| 2617 | 55/72 reported months | Broad HS-4 diagnostic; 17 genuine no-record months |
| 261710 | 27/72 reported months | Full 2019-2024 audit; sparse exports |
| 282580 | 72/72 reported months | Full 2019-2024 audit |

The 2019-2024 export audit was completed on June 12, 2026. The API returned
successful annual responses for every year, so the absent months are genuine
no-record months rather than quota failures. The companion coverage files
record each month explicitly. `04_scripts/download_china_exports.py` can repeat
this six-year audit or extend the series through March 2026. Separate
successful requests returned no China records for 2025-March 2026 for the
current graphite, Ga/Ge, and antimony acquisition codes.

### Antimony timing

Controls were announced in MoFCOM/GAC Announcement No. 33 on August 15, 2024
and took effect September 15, 2024.
Data through March 2026 provide 19 post-treatment calendar months, although the
first month is only partially treated because implementation began on September
15, 2024. HS 8110, HS 261710, and HS 282580 are complete through March 2026
and are kept separate by value-chain stage. Current model use is:
HS 282580 as the main antimony result, HS 8110 as supportive but
pretrend-limited, and HS 261710 as descriptive because of sparse trade and
failed pretrends.

### Antimony product scope

The empirical antimony group contains three trade stages:

| HS | Stage | Legal coverage | Empirical role |
|---|---|---|---|
| 261710 | Antimony ores and concentrates | Antimony-specific basic HS-6 code | Primary upstream/mining and concentrate trade |
| 8110 | Antimony metal and articles | Unwrought metal, powder, waste/scrap, and other metal forms | Refined-metal stage |
| 282580 | Antimony oxides | Only oxides with purity at least 99.99% are legally controlled | Downstream chemical stage; partial treatment at HS-6 |

HS 2617 is the parent HS-4 heading. It combines HS 261710 antimony ores with
HS 261790 ores explicitly classified as other than antimony. The existing HS
2617 China-export series is retained for reconciliation, but no bilateral HS
2617 panel will be downloaded. This avoids spending 448 requests on a
contaminated outcome when the antimony-specific HS-6 series is available.

HS 8110 is also an HS-4 heading, but its three HS-6 children are all antimony:
811010 unwrought antimony and powders, 811020 waste and scrap, and 811090 other
wrought antimony articles. The control announcement's reference codes span
these forms, so the aggregate heading is a defensible broad metal-stage
outcome. Subheading results can later test whether the effect is concentrated
in primary unwrought metal.

Announcement No. 33/2024 also controls narrower antimony products:
high-purity organo-antimony compounds under HS 293190, antimony hydride under
HS 285000, specified indium antimonide crystals under HS 285390, gold-antimony
separation technology, and superhard-material equipment. These are not part of
the main Comtrade antimony group because their HS-6 headings are extremely
broad relative to the legally controlled items, the trade is likely sparse,
or the item is technology/equipment rather than an antimony commodity stage.
They can be considered later as a descriptive appendix, but downloading them
now would not mean “completing” the main antimony value-chain design.

## 2. Eurostat CN8

Source: Eurostat Comext dataset DS-045409. Raw files cover:

| CN8 | Product | Treatment status |
|---|---|---|
| 81129289 | Unwrought gallium | Treated |
| 81129295 | Unwrought germanium | Treated |
| 81129281 | Unwrought indium | Within-bundle placebo |
| 81129291 | Unwrought vanadium | Within-bundle placebo |

Each product has China-partner and world-partner files. HS 282560 cannot be
split at CN8 level; the only useful disaggregation is within HS 811292.

The raw API files contain country rows, UK rows, an `EU27` aggregate in the
China files, and duplicate blank-reporter aggregate rows. They must not be
analyzed directly.

Run:

```bash
python 04_scripts/prepare_eurostat_cn8.py
```

Canonical cleaned outputs:

- `03_data/interim/eurostat_cn8_eu27_balanced_long.csv`
- `03_data/interim/eurostat_cn8_source_audit.csv`
- `03_data/processed/eurostat_cn8_eu27_country_month.csv`
- `03_data/processed/eurostat_cn8_eu27_monthly.csv`

The country panel contains exactly 27 EU countries x 4 products x 72 months =
7,776 rows. UK and aggregate rows are excluded. Omitted API cells are filled
with zero while retaining flags that identify whether a record was reported.
China imports never exceed world imports.

At EU27 aggregate level, germanium has one zero China-flow month (August 2019)
and vanadium has 14 zero China-flow months. These are sparse-trade observations,
not download failures.

## 3. Bloomberg/Wind Prices

Original workbook: `/Users/elgask0/Desktop/minerals data.xlsx`.

The workbook contains price histories only. It does not contain a
semiconductor, battery, steel, or lead-acid demand index.

### Available monthly series

| Series | Identifier | Unit | Coverage |
|---|---|---|---:|
| Gallium >=99.99%, domestic | S5811361 | CNY/kg | 72/72 |
| Germanium ingot, Shanghai Longtai | S5801747 | CNY/kg | 72/72 |
| Germanium ingot, domestic average | S6949812 | CNY/kg | 72/72 |
| Natural flake graphite average | K1272331 | CNY/ton | 72/72 |
| Refined indium >=99.995%, domestic | S6949799 | CNY/kg | 72/72 |
| Rotterdam indium 99.99% | S5810683 | USD/kg | 71/72; June 2024 absent |
| Vanadium nitrogen Vn16 | S6949753 | CNY 10,000/ton | 71/72; February 2020 absent |
| Vanadium pentoxide 98%, flake | S9976462 | CNY/ton | 51/72; begins October 2020 |

Vanadium nitrogen is the preferred long-window vanadium placebo. Vanadium
pentoxide remains a useful product-specific robustness series around the August
2023 treatment date.

The June 2024 Rotterdam indium gap is present in the original workbook. The
primary analysis should leave it missing. Interpolation may be reported only as
a sensitivity check.

### Required Bloomberg acquisition

The exact request list and status are in `03_data/DOWNLOAD_CHECKLIST.md`.
Priority benchmark families are:

- Fastmarkets gallium `MB-GA-0001` and China comparator `MB-GA-0002`;
- Fastmarkets germanium metal `MB-GER-0003`/`MB-GER-0004`;
- Fastmarkets germanium dioxide `MB-GER-0005`/`MB-GER-0006`;
- Fastmarkets indium `MB-IN-0002`/`MB-IN-0003`;
- graphite grade-matched FOB China and non-China delivered benchmarks;
- Fastmarkets antimony metal `MB-SB-0002`, `MB-SB-0001`, and `MB-SB-0003`;
- antimony trioxide 99.5% delivered China, FOB China, and Rotterdam;
- antimony concentrate 50% minimum, delivered China, quoted per contained Sb;
- monthly CNY/USD exchange rates.

For graphite, there is no established CIF-Europe counterpart in the current
Fastmarkets specification for `MB-GRA-0042` (94% C, -100 mesh, FOB China).
Download multiple grade-matched alternatives and select the closest common
product after coverage is known. Platts `BATAA00` (94-95% C FOB China) and
`BATBA00` (94-95% C CIF Northeast Asia) form one exact-grade regional pair.

For antimony concentrate, use a 50% minimum delivered-China benchmark quoted
per metric tonne of contained antimony, such as Argus or Asian Metal. Do not
compare a contained-metal quote directly with an ore-tonne quote.

## 4. CEPII GeoDist

Canonical file:

`03_data/raw/geodist/dist_cepii.dta`

This is the official static GeoDist dyadic file:

- 50,176 unique directed country pairs;
- 224 origins and 224 destinations;
- population-weighted distance;
- contiguity;
- common official and ethnic language;
- colonial relationships.

China-to-reporter matching succeeds for 54 of the 56 configured reporter
codes. The matched set includes China itself. The main importer panel still
uses 53 reporters because China is the source country in the source-share
design, not an importer. The unmatched reporters are the EU and ASEAN
aggregates, which are not countries and must be excluded from country-level
gravity regressions.

Run `python 04_scripts/prepare_geodist.py` to regenerate
`03_data/processed/geodist_china_reporters.csv`, which contains the 54 matched
country dyads plus explicit flags for the two excluded aggregate reporters.
Downstream thesis panels should then drop China as reporter code 156 and keep
the 53 non-group importer countries.

`col_regfile09.dta` is retained only as a legacy CEPII annual gravity panel. It
covers 1948-2006 and must not be used for contemporary GDP or population
controls.

## 5. Downstream Demand Indicators

Acquire monthly January 2019 onward:

| Mineral case | Required series | Preferred source |
|---|---|---|
| Ga/Ge | Global semiconductor sales, USD | SIA/WSTS |
| Ga/Ge | Optoelectronics/discretes sales if licensed | WSTS |
| Graphite | China power-battery production and installations, GWh | China Automotive Power Battery Industry Innovation Alliance/MIIT |
| Graphite | China NEV production and sales, vehicles | CAAM |
| Vanadium | World and China crude steel production, tonnes | World Steel Association |
| Antimony | China lead-acid battery output, 10,000 kVAh | National Bureau of Statistics/Wind |
| Antimony | Optional refined lead usage | ILZSG/Wind |

Store raw releases unchanged. Build monthly log indexes normalized to
2019=100, retaining release vintage, unit, seasonal-adjustment status, and
source URL. Use predetermined lags where economically justified.

These variables test demand-cycle alternatives. They are not automatically
included in every fixed-effect specification, and post-treatment downstream
outcomes must not be controlled for when they may be mediators.

## 6. USGS Production and Concentration

Build a country-mineral-stage-year table from USGS Mineral Commodity Summaries
2020-2026 with:

- country production and world total;
- China production share;
- HHI, top-three share, and number of active producers;
- reserves where available;
- mine, refinery, and processing stage kept separate;
- units and estimated-value flags;
- publication year, URL, and page.

Use the last pre-treatment year: 2022 for 2023 cases and 2023 for antimony.
These measures describe cases and discipline the theoretical comparison. With
only a few treated minerals they cannot identify a market-share coefficient.
USGS may not report country-level refining shares for every mineral; use an
official IEA or European Commission source where necessary and document that
the concepts differ.

## 7. Policy Chronology

The policy dataset must distinguish announcement, implementation, expected
importer arrival, subsequent destination-specific restrictions, and later
suspensions or amendments. It must also preserve item-level technical
definitions and all official reference customs codes.

Use `01_notes/MOFCOM Deep Research Prompt.md` as the collection protocol.

## 8. Canonical Data Extension Plan

### Scope and hard endpoint

The final available UN Comtrade month is March 2026. All acquisition scripts
request January 2019 through **March 2026**, exactly 87 months.
April-December 2026 must not be requested or recorded as no-trade months.

The downloader knows 34 HS products. The policy-screened bilateral acquisition
universe is 31 products because HS 380120 and HS 2827 are policy-contaminated,
and broad HS 2617 is retained only as a China-export diagnostic. Raw
acquisition uses 56 reporter codes when available, but the analysis panel
should use 53 non-group reporter countries. Exclude reporter code 97
(European Union), reporter code 975 (ASEAN), and reporter code 156 (China).
The first two are aggregate reporter groups. China is the source country in
the source-share design, not a reporter in the main importer panel.

HS 3801 is deliberately downloaded for later classification, but it is not an
untreated placebo because it contains artificial or colloidal graphite items
that may overlap the graphite-control scope. Treat it as a special
scope-contaminated graphite case.

### Treatment candidates

| Cohort | Effective | Main HS candidates | Status |
|---|---|---|---|
| Ga/Ge | Aug 2023 | 811292, 282560 | Partial HS-6 treatment |
| Graphite | Dec 2023 | 2504 | Clean natural-graphite case |
| Antimony | Sep 2024 | 8110, 261710, 282580 | Metal/ore clean; oxide purity threshold |
| Wave 4 | Feb 2025 | 8106, 284180, 8101 | Bi and APT clean; W metal partial |
| Wave 5 | Apr 2025 | 284690 | Marginal at HS-6 |

HS 280450 is a marginal tellurium/boron bundle. HS 8102, 280530, 380110,
380190, and 8507 are excluded from the main acquisition priority because
treatment is too narrow, diluted, repeated, or too recent. HS 282590 and
HS 284990 are different: they are tungsten treated products under Announcement
No. 10/2025, so they must not enter any untreated donor pool.

The downloaded `mofcom.md` report incorrectly lists customs code `2825800010`
for both GeO2 and antimony oxides. The official No. 23/2023 text gives
`2825600002` for germanium dioxide; No. 33/2024 gives `2825800010` for
high-purity antimony oxides. The empirical HS-6 fact remains that 282560
combines GeO2 with ZrO2, while 282580 is an antimony-oxide heading.
Chinese tariff lookups distinguish `2825600001` as broader germanium oxides
and `2825600002` as specifically germanium dioxide, so this is a CN-10
specificity issue rather than evidence that the official announcement miscoded
the HS-6 product.

### Placebo audit

A downloaded product is only a **candidate control**. It enters an estimator
only after passing:

1. no Chinese export control during its estimation window;
2. adequate positive trade and reporter coverage;
3. acceptable pre-treatment fit for the specific treated product;
4. no obvious simultaneous product-specific shock;
5. stability to excluding it from the donor pool.

There is no universal 20-product placebo set.

#### Closest candidates: download first

| HS | Product | Best comparison | Assessment |
|---|---|---|---|
| 2615 | Nb/Ta/V/Zr ores | 261710 antimony ores | Best available ore-stage candidate |
| 284170 | Molybdates | 284180 tungstates/APT | Same heading; high priority |
| 811221 | Unwrought chromium | 811292 and metal cases | Same heading/family |
| 380130 | Carbon electrode pastes | 2504/3801 graphite | Adjacent carbon product |
| 282530 | Vanadium oxides | 282560/282580 | Same heading |
| 282520 | Lithium oxide/hydroxide | 282560/282580 | Same heading, different demand cycle |
| 282570 | Molybdenum oxides | Oxide cases | Same heading; general Mo oxides not controlled in Wave 4 |

June 17, 2026 partial expansion status: after completing the term-paper
universe, remaining quota was used on this block. HS 2615 now has 180/448
reporter-year responses persisted and 31,959 merged rows. The remaining gaps
are 2615 (268), 811221 (448), 282530 (448), 282520 (448), and 282570 (448),
for 2,060 pending reporter-year requests in this expansion block.
The June 17 API window became unusable after a few saved HS 2615 responses:
direct probes to both keys timed out even for known completed products.

June 18, 2026 API window: HS 2615 was nearly completed. The run saved 23,552
rows plus 13 valid no-data responses, then a small retry saved another 109
rows. The merged HS 2615 import file now has 69,463 rows and only four
reporter-year gaps remain. The same window started HS 811221, saving 43,840
rows plus 43 valid no-data responses before the API began returning failures
again. HS 811221 has 129 reporter-year gaps remaining. Current expansion gaps
are 1,477 total: 2615 (4), 811221 (129), 282530 (448), 282520 (448), and
282570 (448).

June 19, 2026 API window: the residual HS 2615/811221 block closed most
remaining gaps. HS 2615 now has 75,088 merged rows and one remaining
reporter-year gap. HS 811221 now has 57,900 merged rows and nine remaining
reporter-year gaps. Short probes also started HS 284170, HS 380130, and HS
282530, but the API was too slow and error-prone for full-product runs. Current
closest-candidate gaps are 2,214 total: 2615 (1), 811221 (9), 284170 (443),
380130 (432), 282530 (433), 282520 (448), and 282570 (448). The policy-screened
31-product bilateral universe has 8,486 remaining reporter-year gaps.

June 21, 2026 API window: the previously stubborn residual gaps for HS 2615,
HS 811221, and HS 284170 were completed. HS 2615 remains at 75,088 merged rows
because the final missing reporter-year was a valid no-data response. HS 811221
now has 65,314 merged rows, and HS 284170 now has 105,418 merged rows. The same
window partially advanced HS 380130 to 39,592 merged rows and 234 remaining
reporter-year gaps. Current closest-candidate gaps are 1,563 total: 380130
(234), 282530 (433), 282520 (448), and 282570 (448). The full downloader
universe has 9,179 remaining reporter-year gaps.

June 22, 2026 manual API window: the scheduled automation did not use the
available Python interpreter correctly, so the manual run used
`/Users/elgask0/miniconda/bin/python`. HS 380130 advanced to 47,316 merged rows
and 204 remaining reporter-year gaps. HS 282530 advanced to 3,410 merged rows
and 388 remaining reporter-year gaps. A small HS 282520 probe then failed
immediately with zero counted API calls, so the window was stopped as degraded.
Current closest-candidate gaps are 1,488 total: 380130 (204), 282530 (388),
282520 (448), and 282570 (448). The policy-screened 31-product bilateral
universe has 7,760 remaining reporter-year gaps, while excluded diagnostics
HS 380120, HS 2827, and broad HS 2617 account for another 1,344 gaps outside
the main acquisition target.

June 22, 2026 follow-up retry: a later small-chunk retry advanced HS 380130 to
58,199 merged rows and 152 remaining reporter-year gaps. HS 282530 then failed
immediately with zero counted API calls, so downloads stopped again. Current
closest-candidate gaps are 1,436 total: 380130 (152), 282530 (388), 282520
(448), and 282570 (448). The full downloader universe has 9,052 remaining
reporter-year gaps.

June 23, 2026 extended API window: after an initial DNS failure, waiting and
retrying recovered the API. HS 380130 was completed with 75,309 merged rows.
HS 282530 advanced to 28,662 merged rows and only 32 remaining 2026
reporter-year gaps. HS 282520, HS 282570, HS 8106, and HS 284180 were probed
but entered a non-closing one-request-per-minute pattern with no rows, no valid
no-data files, and no rate-limit responses, so those probes were interrupted
and force-merged. Current close-candidate gaps are 928 total: 282530 (32),
282520 (448), and 282570 (448). The full downloader universe has 8,544
remaining reporter-year gaps.

June 25, 2026 automation window: the scheduled run again used
`/Users/elgask0/miniconda/bin/python` explicitly. The opening dry run reported
8,544 total downloader gaps: 7,200 in the policy-screened 31-product
acquisition universe and 1,344 in excluded diagnostics HS 380120, HS 2827, and
broad HS 2617. HS 282530 was completed and now has 28,858 merged rows. HS
282520 was then completed through repeated chunks and now has 51,644 merged
rows. HS 282570 was started and now has 4,120 merged rows, but it entered a
non-closing one-request-per-minute pattern and was interrupted/force-merged.
The final full dry run now reports 8,045 total downloader gaps: 6,701 in the
main 31-product acquisition universe and 1,344 excluded-diagnostic gaps. The
close-candidate block has only HS 282570 remaining, with 429 reporter-year
gaps. This window was API-unreliable rather than quota-exhausted: no 429-only
rate-limit end state appeared, and waiting/retrying restored productive
responses for HS 282520. Immediate next priority is HS 282570, then wave-4
treated products, metal-family placebos, and deferred/marginal products.
Late-evening retries of HS 282570 and HS 284180 did not close additional
files. HS 282570 remained at 4,120 merged rows and 429 gaps after a 10-call
probe consumed counted calls but returned no rows, no valid no-data files, and
no rate-limit responses. Treat the next window as an API-reliability retry, not
as a quota reset issue.

On June 26, 2026, the run eventually recovered from the earlier degraded API
pattern. HS 282570 was completed and now has 40,217 merged rows, completing
the full close-candidate block. HS 8106 was then started and advanced to
11,722 merged rows, with 378 reporter-year gaps remaining. HS 284180 was probed
late but remained in a non-closing one-request-per-minute pattern and saved no
files. The final dry run reported 7,546 total downloader gaps: 6,202 in the
main 31-product universe and 1,344 excluded-diagnostic gaps. This remained an
API-unreliability day rather than confirmed quota exhaustion: no persistent
429-only rate-limit boundary appeared, and cooldown/retry cycles restored
productive responses for HS 282570. Immediate next priority is HS 8106, then
HS 284180 and HS 8101, with the same cooldown-and-rotate rule if the API stays
non-closing.

In the early June 27 continuation, a 25-call HS 8106 diagnostic saved no rows
and no valid no-data files. Direct probes on both Comtrade keys returned
`403 Out of call volume quota`, with replenishment due roughly five hours after
the probe. This confirmed true quota exhaustion rather than the earlier
ambiguous non-closing pattern. HS 8106 remains at 11,722 merged rows and
378 gaps.

Later on June 27, the reset window had already made progress before the manual
audit: HS 8106 was complete and HS 284180 had advanced to 13,401 merged rows,
with 327 reporter-year gaps remaining. A new manual HS 284180 chunk immediately
fell into the one-request-per-minute no-save pattern; direct probes on both
Comtrade keys confirmed `403 Out of call volume quota`, with replenishment due
roughly 17 hours after the probe. The full downloader dry run now reports
7,047 total gaps: 5,703 in the main 31-product universe and 1,344 excluded
diagnostics. Resume with HS 284180 after the next reset, then HS 8101.

Later on June 27, 2026, the refreshed quota window was used heavily before
true exhaustion returned. HS 8106 was completed through March 2026 and now has
56,196 merged rows. HS 284180 then advanced to 13,401 merged rows and
327 remaining reporter-year gaps before it entered repeated non-closing
stretches; two cooldown cycles and a small retry did not restore productive
responses. A short opening probe on HS 8101 also immediately entered the same
zero-yield pattern, so the run stopped only after direct API checks on both
keys confirmed `403 Out of call volume quota` with replenishment due in roughly
20 hours 40 minutes. Approximate counted API usage for the day was about
525-530 calls, plus a few interrupted zero-yield completions that did not
change files. The final dry run reported 7,047 total downloader gaps: 5,703 in
the policy-screened 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. Immediate next priority
after the quota reset is HS 284180, then HS 8101, followed by the metal-family
candidates and deferred or marginal products.

On June 28, 2026, the daily downloader resumed with a fresh audit and then
used approximately 448 counted API calls without hitting a confirmed quota
boundary. HS 284180 was completed through March 2026 in three productive
one-worker chunks plus a one-file tail retry, and its merged raw import file
now contains 41,003 rows. HS 8101 then advanced productively from zero saved
files to 89,298 merged rows. The final in-flight HS 8101 chunk was stopped
manually and force-merged to preserve partial progress, after which the settled
full dry run reported 6,592 total downloader gaps: 5,248 in the
policy-screened 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. Current main-universe
remaining gaps are HS 8101 (320), HS 8103 (448), HS 8108 (448), HS 8109
(448), HS 8104 (448), HS 8105 (448), HS 282110 (448), HS 2820 (448), HS 2833
(448), HS 284610 (448), HS 280450 (448), and HS 284690 (448). This checkpoint
ended by manual stop for a clean handoff while the API was still productive,
not by true quota exhaustion and not by a renewed API-unreliability failure.
Immediate next priority is to continue HS 8101, then move to the metal-family
placebos, and only then the deferred and marginal products.

Later on June 28, 2026, direct confirmation showed the quota window was still
open: both keys returned `200` responses with 2,668 rows for a still-missing
HS 8101 reporter-year request. The downloader then resumed HS 8101, lifting
its merged file from 89,298 to 128,215 rows and cutting remaining HS 8101 gaps
from 320 to 277. After that progress, HS 8101 entered the familiar non-closing
one-request-per-minute pattern. Two cooldown cycles and small one-worker retry
chunks did not restore file-closing behavior, so the run rotated to HS 8103.
HS 8103 immediately showed the same non-closing pattern, and direct probes on
both keys then returned `403 Out of call volume quota` plus `Retry-After`
headers of roughly 15 hours 9 minutes. That confirmed true quota exhaustion at
the end of the continuation. The settled final dry run now reports 6,549 total
downloader gaps: 5,205 in the main 31-product acquisition universe and 1,344
in excluded diagnostics. Immediate next priority after replenishment remains HS
8101 (277 gaps), then HS 8103 and the rest of the metal-family block.

On June 29, 2026, the next quota window was used productively before confirmed
exhaustion returned. A fresh audit again reported 6,549 total downloader gaps:
5,205 in the policy-screened 31-product acquisition universe and 1,344 in
excluded diagnostics HS 380120, HS 2827, and broad HS 2617. HS 8101 was then
completed through March 2026 in two productive one-worker chunks. The first
100-call chunk returned 75,111 rows and four valid no-data responses; the
second 177-call chunk returned 95,106 rows and 36 valid no-data responses.
HS 8101 is now complete with 298,432 merged rows.

The same window then started the metal-placebo block in earnest. HS 8103 used
145 counted API calls in a 150-target chunk, landing 30,244 rows, 15 valid
no-data responses, and five errors. Its merged raw import file now contains
30,244 rows and has 303 remaining reporter-year gaps. HS 8108 then used
95 counted API calls in a 100-target chunk, landing 93,794 rows, two valid
no-data responses, and five errors. Its merged raw import file now contains
93,794 rows and has 369 remaining reporter-year gaps. A small HS 8109 probe
immediately re-entered the non-closing one-request-per-minute pattern, so it
was interrupted and force-merged without any persisted files.

This run ended by confirmed true quota exhaustion, not by API unreliability.
Direct probes on a still-missing HS 8109 request returned `403 Out of call
volume quota` on both keys, with `Retry-After` values of about 76,774 seconds
and explicit replenishment messages of roughly 21 hours 19 minutes. Approximate
counted API usage for the June 29 window was about 519-521 calls: 277
productive HS 8101 calls, 145 counted HS 8103 calls, 95 counted HS 8108
calls, and 2 direct quota-confirmation probes.

The settled final dry run now reports 6,048 total downloader gaps: 4,704 in
the policy-screened 31-product acquisition universe and 1,344 in excluded
diagnostics. Immediate next priority after replenishment is HS 8103, then
HS 8108, then HS 8109; if HS 8109 again fails to close files after one retry,
rotate to HS 8104 and return later.

On June 30, 2026, the downloader resumed with the required full dry-run audit
and confirmed that HS 282570, HS 8106, HS 284180, and HS 8101 were already
closed. The live start-of-run backlog was 6,048 total downloader gaps:
4,704 in the main 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617.

The productive work stayed on the highest-priority remaining metal-placebo
partials. HS 8103 used 98 counted API calls in a one-worker 100-target chunk,
returning 29,477 new rows, 10 valid no-data responses, and two errors. Its
merged raw import file rose from 30,244 to 59,721 rows, and its remaining
gaps fell from 303 to 205. HS 8108 then used another 98 counted API calls in
a one-worker 100-target chunk, returning 155,380 new rows, five valid no-data
responses, and two errors. Its merged raw import file rose from 93,794 to
249,174 rows, and its remaining gaps fell from 369 to 271. Earlier in the
same API day, a productive HS 8108 chunk had already used 95 counted calls,
and a short HS 8109 probe had used about two counted calls without saving
files. Approximate counted API usage for the June 30 window was therefore
about 293 calls.

This checkpoint did not end because of true quota exhaustion and did not end
because of API unreliability. No persistent `429` boundary, `403 Out of call
volume quota`, `409` refusal pattern, or retry-after exhaustion signal
appeared. The handoff stopped manually after two full productive chunks so the
settled state could be logged cleanly. The post-run dry audit now reports
5,852 total downloader gaps: 4,508 in the main 31-product acquisition
universe and 1,344 in excluded diagnostics. The remaining main-universe
requests are HS 8103 (205), HS 8108 (271), HS 8109 (448), HS 8104 (448),
HS 8105 (448), HS 282110 (448), HS 2820 (448), HS 2833 (448), HS 284610
(448), HS 280450 (448), and HS 284690 (448). Immediate next priority is to
continue HS 8103, then HS 8108, then start HS 8109 and the rest of the
metal-family block.

Later on June 30, 2026, the same API day was used for a continuation run that
closed HS 8103 completely and advanced HS 8108 substantially further. HS 8103
used three one-worker chunks: a 100-target chunk with 98 counted calls,
16,482 new rows, 14 valid no-data responses, and two errors; a second
100-target chunk with 99 counted calls, 13,995 new rows, 29 valid no-data
responses, and one error; and a final 8-call tail retry that added 156 rows
plus five valid no-data responses. HS 8103 is now complete through March 2026
with 90,354 merged rows.

The same continuation then stayed on HS 8108 while it remained intermittently
productive. Productive HS 8108 chunks added 33,868 rows in a first 22-call
partial, 18,983 rows in a 25-call cooldown retry, 60,439 rows in a later
32-call partial, and 35,873 rows in a second 24-call cooldown retry. An
additional interrupted 100-target chunk saved 9,331 rows before re-entering
the non-productive one-request-per-minute pattern and was force-merged. After
all settled merges, HS 8108 rose from 249,174 merged rows at the midday
handoff to 407,668 rows, and its remaining gaps fell from 271 to 164.

After HS 8108's repeated non-quota stalls, the run rotated to new products.
Two separate HS 8109 probes and one HS 8104 probe all showed the same sterile
pattern: one completion per minute, zero rows, zero valid no-data files, zero
rate-limit signals, and no persisted files even after cooldown. That is API
unreliability, not confirmed quota exhaustion. Approximate counted API usage
for this continuation was about 326 calls, which implies about 619 counted
calls across the full June 30 API day when combined with the earlier midday
session.

The settled final dry audit for June 30 now reports 5,540 total downloader
gaps: 4,196 in the main 31-product acquisition universe and 1,344 in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. The remaining
main-universe requests are HS 8108 (164), HS 8109 (448), HS 8104 (448),
HS 8105 (448), HS 282110 (448), HS 2820 (448), HS 2833 (448), HS 284610
(448), HS 280450 (448), and HS 284690 (448). This day ended by API
unreliability on new-product probes, not by true quota exhaustion. Immediate
next priority after the next usable window is to finish HS 8108, then retry
HS 8109 once more before rotating to HS 8104 only if the same zero-yield
pattern persists.

#### Metal-family candidates: second tier

| HS | Product | Assessment |
|---|---|---|
| 8103 | Tantalum | Useful critical-metal comparator |
| 8108 | Titanium | Useful but substantially larger market |
| 8109 | Zirconium | Useful minor-metal comparator |
| 8104 | Magnesium | Broad and highly cyclical; lower priority |
| 8105 | Cobalt mattes/intermediates | Battery-cycle exposure; lower priority |

#### Broad or episode-specific candidates: defer

| HS | Product | Reason |
|---|---|---|
| 282110 | Iron oxide pigments | Chapter-level rather than close match |
| 2820 | Manganese oxides | Broad HS4 group |
| 2833 | Sulfates | Very broad heterogeneous group |
| 284610 | Cerium compounds | Useful only if marginal REE case 284690 is retained |

HS 2827 must not be used as an untreated control: the heading contains
germanium tetrachloride, which Announcement No. 23/2023 controls. HS 380120 is
also not a clean graphite control. It is not among the announcement's printed
reference codes, but colloidal graphite may still fall within the legal product
description covering natural flake graphite and its products. Both codes may be
downloaded for descriptive diagnostics only, not placed in the main donor pool.

HS 3801 should be handled separately from HS 380120. HS 3801 is already
downloaded and can be used as a special graphite scope case. It should not be
coded as a clean untreated control. It can appear in secondary
treatment-scope diagnostics if the model explicitly separates clean, partial,
bundled, and graphite-scope products.

The remaining close candidates are not directly listed in Announcements
23/2023, 39/2023, 33/2024, 10/2025, or 18/2025:

- HS 284170 and 282570 remain usable molybdenum-family candidates because
  Announcement 10/2025 controls specified molybdenum powder under HS 810210,
  not molybdates or molybdenum oxides.
- HS 282520 is not covered by the February 2025 mineral controls.
- HS 2615, 811221, 380130, and 282530 are not directly listed.
- HS 284610 cerium compounds are not among the medium/heavy rare-earth items
  in Announcement 18/2025, but remain a lower-priority control because the
  wider rare-earth industry experienced simultaneous policy shocks.

The downloaded MOFCOM report is not a complete through-2026 chronology. It
omits Announcements 56, 57, 61, 62, and especially Announcement 70/2025.
Announcement 70 suspended Announcements 55-58 and 61-62 on November 7, 2025,
before their November 8 implementation date, through November 10, 2026.
Therefore the October 2025 graphite-anode and expanded rare-earth measures
must not be coded as active treatments in the panel through March 2026.

The existing 2818, 8111, and 2811 controls remain available, but their broad
industrial composition means they are baseline controls, not automatically
preferred matches.

### Inference implication

With 20 eligible controls, the theoretical minimum assignment rank for one
treated product is approximately 1/21 = 0.048. This is only a **theoretical
resolution ceiling**. It is not a promise of significance, random assignment,
exchangeability, power, or causal validity. Invalid donors cannot be retained
merely to lower the minimum attainable rank.

### Completed quota-aware order

The term-paper Comtrade universe is complete through March 2026. The scripts
remain resumable and rotate the two keys across requests for future thesis
expansion, but no further Comtrade API calls are required for the current
course-paper design.

Completed order:

1. Extended existing aggregate exports, including broad HS 2617, and acquired
   precise HS 261710 plus HS 282580 export diagnostics.
2. Completed HS 8110 bilateral data through March 2026.
3. Completed HS 261710 bilateral data through March 2026.
4. Completed HS 282580 bilateral data through March 2026.
5. Extended HS 2504, 811292, 282560, 3801, 2818, 8111, and 2811 through
   March 2026.
6. Audited all ten completed bilateral panels and export series.
7. Began thesis-expansion downloads only after the term-paper universe was
   complete.

Exact commands are in `03_data/DOWNLOAD_CHECKLIST.md`.

### Pipeline status

`download_all_gaps.py` and `download_china_exports.py` implement the March 2026
endpoint and priority batches. The active thesis-stage processing pipeline is:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
```

`prepare_comtrade_thesis_panel.py` and `analysis_thesis.py` remain available
for archived term-paper reproducibility.

## 9. Reproducibility Status

The legacy log-OLS triple-difference estimates in `analysis_final.py` are
superseded because raw Comtrade dimensions were summed together and HC1
inference did not match the treatment assignment.

Current pressure-design outputs are generated by:

```bash
python 04_scripts/build_product_scope_metadata.py
python 04_scripts/prepare_comtrade_pressure_panel.py
python 04_scripts/build_pressure_indices.py
python 04_scripts/build_pressure_estimation_panel.py
python 04_scripts/diagnose_anchor_quarter_models.py
python 04_scripts/estimate_quarterly_pressure_mechanisms.py
python 04_scripts/estimate_price_wedges.py
```

Main current result tables:

- `03_data/output/tables/quarterly_first_full_post_pressure_ppml.csv`;
- `03_data/output/tables/anchor_quarter_average_ppml.csv`;
- `03_data/output/tables/anchor_quarter_event_pretrend.csv`;
- `03_data/output/tables/quarterly_pressure_mechanisms_first_full_post.csv`;
- `03_data/output/tables/price_wedge_pair_its_results.csv`;
- `03_data/output/tables/price_wedge_panel_did_results.csv`.

Archived term-paper outputs are generated by:

```bash
python 04_scripts/prepare_comtrade_thesis_panel.py
python 04_scripts/prepare_eurostat_cn8.py
python 04_scripts/analysis_thesis.py
```

Current source-share PPML estimates for the completed term-paper panel are:

| Case | Static DDD | Trend-break DDD | Extended pretrend |
|---|---:|---:|---|
| Graphite 2504 | -30.4% (p=0.107) | negative trend break in some anchors | Fails main/extended pretrends |
| Ga/Ge 811292 | +19.3% (p=0.365) | negative trend break but no static decline | Fails pretrends |
| GeO2/ZrO2 282560 | +17.5% (p=0.271) | negative trend break but no static decline | Mixed; no negative static effect |
| Antimony metal 8110 | -86.8% (p<0.001) | weak static trend-break treatment, negative trends | Fails pretrends |
| Antimony ores 261710 | -98.9% (p=0.003) | large but unstable | Sparse/descriptive only |
| Antimony oxides 282580 | -81.5% (p=0.002) | strong negative trend break | Passes main/extended source-share pretrends |

Reporter-clustered p-values are conditional. Exact product-assignment
inference is capped at p = 0.25 in each one-treated-product/three-placebo
comparison. The cleanest mechanism result is HS 282580 among high
switching-potential importers: -87.4%, p = 0.00019, pretrend p = 0.354.

The canonical framework and full results are in `Thesis Design.md`.
