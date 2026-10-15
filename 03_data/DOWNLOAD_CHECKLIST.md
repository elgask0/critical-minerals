# Data Download Checklist

This is the only operational acquisition checklist. Coverage truth is in
`01_notes/Data.md`. Last updated July 13, 2026.

## UN Comtrade API

Hard endpoint: **March 2026**. The scripts request 2019-2025 in annual batches
and January-March only for 2026.

The two registered keys have a nominal combined allowance of 1,000 calls per
day. Comtrade does not expose the exact remaining quota. Use a working cap of
800 requests so retries and audits retain headroom. Completed data and valid
`skip` responses are skipped. If both keys sustain 60-90 second timeouts, stop
the run and resume in the next API window.

Always preview a batch:

```bash
python 04_scripts/download_all_gaps.py --batch antimony --dry-run
```

## Completion Scope Before Any Expansion

Finish these ten bilateral products through March 2026 and eight China-export
series, including broad HS 2617 as a diagnostic. Do not download new placebos
or additional 2025 mineral cases until this block is complete.

| Role | HS codes |
|---|---|
| Existing treated | 2504, 811292, 282560 |
| Existing partially treated/descriptive | 3801 |
| Existing controls | 2818, 8111, 2811 |
| Antimony value chain | 261710, 8110, 282580 |
| Retained broad diagnostic | 2617 exports only |

Total bilateral target: 10 products x 448 reporter-year files = 4,480.
Currently persisted: 4,480. Remaining: **0**.

### Antimony export series first

Extend the existing six export series, including broad HS 2617, and acquire the
precise HS 261710 ore series plus antimony oxides:

```bash
# Existing series: request 2025 and Jan-Mar 2026 only.
python 04_scripts/download_china_exports.py \
  --products 2504,3801,8110,2617,811292,282560 --from-year 2025

# New precise ore and oxide series: full 2019-Mar 2026 histories.
python 04_scripts/download_china_exports.py --products 261710,282580
```

The June 12, 2026 audit completed these requests. HS 261710 has 27 reported
months in 2019-2024; HS 282580 has all 72 months. Successful requests returned
no China records for 2025-March 2026.

### Remaining API windows

#### Sunday, June 14, 2026

Status: mostly completed. The refreshed API window persisted 465 of the 467
remaining antimony reporter-year responses, then both keys returned
quota-exhausted responses. HS 8110 and HS 261710 are complete through March
2026. HS 282580 has two remaining 2026 reporter-year gaps: reporters `620` and
`854`.

The command used was:

```bash
python 04_scripts/download_all_gaps.py \
  --batch antimony --through 202603 --max-calls 800 --workers 2
```

Follow-up retry used:

```bash
python 04_scripts/download_all_gaps.py \
  --batch antimony --through 202603 --max-calls 100 --workers 1
python 04_scripts/download_all_gaps.py \
  --products 282580 --through 202603 --max-calls 10 --workers 1
```

After the HS 282580 dry run reports zero, extend all seven established
products:

```bash
python 04_scripts/download_all_gaps.py \
  --batch extend-current --through 202603 --max-calls 800 --workers 2
```

The seven extensions require 784 requests. The dry-run gap count, not the
calendar estimate, is authoritative.

#### Monday, June 15, 2026

Status: antimony completed and established-product extension mostly completed.

First, the remaining two HS 282580 requests were downloaded:

```bash
python 04_scripts/download_all_gaps.py \
  --products 282580 --through 202603 --max-calls 10 --workers 1
```

Result: 2 API calls, 146 rows, 1 no-data response, 0 errors. HS 8110, HS
261710, and HS 282580 now all report zero gaps through March 2026.

Second, the established-product extension was run:

```bash
python 04_scripts/download_all_gaps.py \
  --batch extend-current --through 202603 --max-calls 1000 --workers 2
```

Result: 753 API calls, 112,503 rows, 128 no-data responses, 31 errors, and
41 rate-limit responses. The successful files were merged. A follow-up retry
of the high-priority remaining products used 48 additional calls but did not
close any gaps; the script's handling indicates likely 403/409 quota/refusal
responses rather than genuine no-data confirmations.

Remaining extension gaps after the June 15 window:

| HS | Remaining | Year breakdown |
|---|---:|---|
| 2504 | 14 | 2025: 7; 2026: 7 |
| 811292 | 14 | 2025: 8; 2026: 6 |
| 282560 | 10 | 2025: 5; 2026: 5 |
| 2818 | 10 | 2025: 4; 2026: 6 |
| 8111 | 52 | 2025: 7; 2026: 45 |
| 2811 | 112 | 2025: 56; 2026: 56 |
| 3801 | 112 | 2025: 56; 2026: 56 |
| **Total** | **324** |  |

Next quota-window order:

```bash
python 04_scripts/download_all_gaps.py \
  --products 2504,811292,282560,2818 --through 202603 --max-calls 80 --workers 1
python 04_scripts/download_all_gaps.py \
  --products 8111 --through 202603 --max-calls 80 --workers 1
python 04_scripts/download_all_gaps.py \
  --products 2811 --through 202603 --max-calls 140 --workers 1
python 04_scripts/download_all_gaps.py \
  --products 3801 --through 202603 --max-calls 140 --workers 1
```

#### Tuesday, June 16, 2026

Status: completed. The remaining 324 established-product extension requests
were downloaded, merged, and verified. Final dry run:

```bash
python 04_scripts/download_all_gaps.py --batch antimony --through 202603 --dry-run
python 04_scripts/download_all_gaps.py --batch extend-current --through 202603 --dry-run
```

Both commands return `Total gaps: 0`.

Final merged raw import rows:

| HS | Rows |
|---|---:|
| 2504 | 157,995 |
| 811292 | 73,408 |
| 282560 | 91,369 |
| 2818 | 406,561 |
| 8111 | 88,288 |
| 2811 | 680,018 |
| 3801 | 311,474 |
| 8110 | 49,396 |
| 261710 | 9,134 |
| 282580 | 74,910 |

After the core term-paper universe was complete, the same quota window was used
for the first thesis-expansion block:

```bash
python 04_scripts/download_all_gaps.py \
  --products 2615,811221,282530,282520,282570 \
  --through 202603 --max-calls 700 --workers 2
```

The run was stopped after direct API probes confirmed both keys were
quota-exhausted. The successful partial files were merged manually with the
script's `merge_all` logic. Result: HS 2615 had 171/448 reporter-year files
persisted and 31,251 merged rows after the June 16 run.

On June 17, 2026, a renewed API window saved a few additional HS 2615 responses
before Comtrade began returning rate-limit and read-timeout failures even for
known completed requests. After merging, HS 2615 has 180/448 reporter-year
responses persisted and 31,959 merged rows. Remaining expansion gaps are 2,060:
HS 2615 (268), HS 811221 (448), HS 282530 (448), HS 282520 (448), and HS 282570
(448).

On June 18, 2026, HS 2615 was nearly completed. The main HS 2615 run downloaded
23,552 rows and 13 no-data responses, then a small retry downloaded another
109 rows. The merged HS 2615 file now contains 69,463 rows and has four
remaining reporter-year gaps. The same quota window started HS 811221 and
downloaded 43,840 rows plus 43 no-data responses before errors and rate-limit
behavior returned. HS 811221 has 129 remaining reporter-year gaps. Current
expansion gaps are 1,477: HS 2615 (4), HS 811221 (129), HS 282530 (448),
HS 282520 (448), and HS 282570 (448).

On June 19, 2026, the residual HS 2615/811221 block closed most remaining
gaps. HS 2615 now has 75,088 merged rows and one remaining reporter-year gap.
HS 811221 now has 57,900 merged rows and nine remaining reporter-year gaps.
Short probes also started HS 284170, HS 380130, and HS 282530, but full-product
runs were stopped because the API became slow and error-prone. Current closest
candidate gaps are 2,214: HS 2615 (1), HS 811221 (9), HS 284170 (443),
HS 380130 (432), HS 282530 (433), HS 282520 (448), and HS 282570 (448). The
policy-screened 31-product bilateral universe has 8,486 remaining
reporter-year gaps.

On June 21, 2026, the reset API window completed HS 2615, HS 811221, and
HS 284170. HS 2615 has 75,088 merged rows, HS 811221 has 65,314 merged rows,
and HS 284170 has 105,418 merged rows. HS 380130 was advanced to 39,592 merged
rows and 234 remaining reporter-year gaps before the long chunk was
interrupted and force-merged. Current closest-candidate gaps are 1,563:
HS 380130 (234), HS 282530 (433), HS 282520 (448), and HS 282570 (448). The
full downloader universe has 9,179 remaining reporter-year gaps.

On June 22, 2026, the scheduled automation failed to use the available Python
interpreter, so the manual retry used `/Users/elgask0/miniconda/bin/python`.
HS 380130 advanced to 47,316 merged rows and 204 remaining reporter-year gaps.
HS 282530 advanced to 3,410 merged rows and 388 remaining reporter-year gaps.
A small HS 282520 probe then failed immediately with zero counted API calls, so
the run was stopped as a degraded API window. Current close-candidate gaps are
1,488: HS 380130 (204), HS 282530 (388), HS 282520 (448), and HS 282570 (448).
The policy-screened 31-product bilateral universe now stands at 7,760 remaining
reporter-year gaps; excluded diagnostics HS 380120, HS 2827, and broad HS 2617
add another 1,344 gaps outside the main acquisition target.

A later June 22 small-chunk retry advanced HS 380130 further to 58,199 merged
rows and 152 remaining reporter-year gaps. HS 282530 then failed immediately
with zero counted API calls, so the retry stopped. Current close-candidate gaps
are 1,436: HS 380130 (152), HS 282530 (388), HS 282520 (448), and HS 282570
(448). The full downloader universe has 9,052 remaining reporter-year gaps.

On June 23, 2026, an extended manual API window recovered after an initial DNS
failure. HS 380130 was completed with 75,309 merged rows. HS 282530 advanced to
28,662 merged rows and only 32 remaining 2026 reporter-year gaps. HS 282520,
HS 282570, HS 8106, and HS 284180 were probed but entered a non-closing
one-request-per-minute pattern with no rows, no valid no-data files, and no
rate-limit responses, so those probes were interrupted and force-merged.
Current close-candidate gaps are 928: HS 282530 (32), HS 282520 (448), and
HS 282570 (448). The full downloader universe has 8,544 remaining
reporter-year gaps.

On June 25, 2026, the daily automation used
`/Users/elgask0/miniconda/bin/python` throughout, first audited all remaining
gaps, then closed HS 282530 and HS 282520 in conservative one-worker chunks.
HS 282530 is now complete with 28,858 merged rows. HS 282520 is now complete
with 51,644 merged rows. HS 282570 was started and now has 4,120 merged rows,
but it entered a non-closing one-request-per-minute pattern and was
interrupted/force-merged. The June 25 pattern was API unreliability rather than
quota exhaustion because valid responses continued after cooldown and no
429-only rate-limit end state appeared. The policy-screened 31-product
bilateral universe now has 6,701 remaining reporter-year gaps. Excluded
diagnostics HS 380120, HS 2827, and broad HS 2617 still add 1,344 gaps outside
the main acquisition target, for 8,045 total downloader gaps.
Late-evening retries of HS 282570 and HS 284180 did not close additional
files. HS 282570 remained at 4,120 merged rows and 429 gaps after a 10-call
probe consumed counted calls but returned no rows, no valid no-data files, and
no rate-limit responses. Treat the next window as an API-reliability retry, not
as a quota reset issue.

On June 26, 2026, the run eventually recovered from the earlier degraded API
pattern. HS 282570 was completed and now has 40,217 merged rows, completing the
full close-candidate block. HS 8106 was then started and advanced to 11,722
merged rows, with 378 reporter-year gaps remaining. HS 284180 was probed late
but remained in a non-closing one-request-per-minute pattern and saved no
files. The day ended because of API unreliability, not true quota exhaustion:
no persistent 429-only rate-limit boundary appeared, and cooldown/retry cycles
restored productive responses for HS 282570. Final dry run: 7,546 total
downloader gaps, of which 6,202 remain in the main 31-product acquisition
universe and 1,344 remain in excluded diagnostics.

In the early June 27 continuation, a 25-call HS 8106 diagnostic consumed calls
but saved no rows and no valid no-data files. Direct probes on both Comtrade
keys returned `403 Out of call volume quota`, with replenishment due roughly
five hours after the probe. This is confirmed quota exhaustion, not merely API
instability. Resume with HS 8106 after the reset.

Later on June 27, the reset window had already advanced before the manual
audit: HS 8106 was complete and HS 284180 had 13,401 merged rows with 327
reporter-year gaps remaining. A new HS 284180 chunk immediately returned to
the one-request-per-minute no-save pattern; direct probes on both keys then
confirmed `403 Out of call volume quota`, with replenishment due roughly
17 hours after the probe. Current full dry run: 7,047 total gaps, of which
5,703 are in the main 31-product universe and 1,344 are excluded diagnostics.
Resume with HS 284180 after the next reset, then HS 8101.

Later on June 27, 2026, the post-reset window was used until true exhaustion
returned. HS 8106 was completed through March 2026 and now has 56,196 merged
rows. Productive chunks cut it from 378 remaining reporter-year gaps to zero,
with the final tail reducing to a single 2026 file that then closed on a
one-call retry. HS 284180 then advanced to 13,401 merged rows and 327
remaining reporter-year gaps. Its first 100-target chunk was productive, but a
later chunk entered a non-closing one-request-per-minute pattern, and two
cooldown cycles plus a small retry did not restore useful responses. A brief
HS 8101 opening probe then showed the same immediate zero-yield pattern.

Approximate counted API usage for the June 27 window was about 525-530 calls.
The run stopped because of true quota exhaustion, not mere API unreliability:
at approximately 11:19 on June 27, 2026, direct probes on both keys returned
`403 Out of call volume quota` with replenishment due in roughly 20 hours
40 minutes. Final dry runs now report 7,047 total downloader gaps: 5,703 in
the main 31-product acquisition universe and 1,344 in excluded diagnostics.

Current remaining requests after the June 27 run are:

- HS 284180: 327
- HS 8101: 448
- HS 8103: 448
- HS 8108: 448
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Next quota-window order:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284180 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8101 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
```

Start with HS 284180 because it already has rows landing cleanly after the
reset, but if it re-enters the non-closing pattern after two cooldown cycles,
rotate immediately to HS 8101 and then the metal-family block.

### Priority 0: Antimony export audit completed

Completed June 12, 2026. The 12 successful annual responses confirmed:

- HS 8110: October-December 2024 are genuine no-record months.
- HS 2617: all 17 scattered missing months are genuine no-record months.

### Priority 1: Complete HS 8110 through March 2026

HS 8110 is complete through March 2026. The previously planned HS 2617
bilateral panel is cancelled because that HS-4 heading also includes
non-antimony ores under HS 261790.

### Priority 2: Complete all antimony bilateral series through March 2026

Order: HS 8110 metal, HS 261710 ores/concentrates, then HS 282580 oxides.
Current remaining requests are 0, 0, and 0 respectively. Completed June 15,
2026.

### Priority 3: Extend the seven established products

Completed June 16, 2026. HS 2504, 811292, 282560, 2818, 8111, 2811, and 3801
all have 448/448 reporter-year files through March 2026. HS 3801 is acquired
but is not an untreated control.

### Deferred Until Completion: new controls and new treatments

```bash
python 04_scripts/download_all_gaps.py \
  --products 2615,811221,282530,282520,282570 \
  --through 202603 --max-calls 700 --workers 2
```

The close-candidate block is now complete. HS 2615, HS 811221, HS 284170,
HS 380130, HS 282530, HS 282520, and HS 282570 all have zero gaps through
March 2026. These products provide carbon-, metal-, and oxide-stage candidates;
none is automatically a valid placebo.

The next acquisition block starts with the remaining wave-4 treated products.
Current remaining requests after the June 27 continuation are: HS 284180 (327)
and HS 8101 (448). HS 8106 is complete. HS 284180 has 13,401 merged rows.

Next quota-window order:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284180 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8101 --through 202603 --max-calls 100 --workers 1
```

Use one worker and keep the chunk size at 50-100 calls while the API remains
slow. Treat 429 clusters as quota pressure. Treat DNS failures, connection
errors, timeouts, or long one-request-per-minute non-closing stretches as
API/network unreliability; in that case force-merge, wait 10-15 minutes,
retry the same product once, then rotate to the next priority product and come
back later in the same run.

On June 28, 2026, the automation resumed with
`/Users/elgask0/miniconda/bin/python` and a full dry-run audit, which
confirmed 7,047 total gaps at the start of the window: 5,703 in the main
31-product universe and 1,344 in excluded diagnostics HS 380120, HS 2827, and
broad HS 2617. The run then used approximately 448 counted API calls in
productive one-worker chunks without reaching a confirmed 429 or `403 Out of
call volume quota` boundary.

HS 284180 was finished first. A 75-call chunk, a 100-call chunk, and a
153-call chunk reduced it from 327 remaining reporter-year gaps to one, and a
final one-call retry closed the tail completely. HS 284180 is now complete
through March 2026 with 41,003 merged rows.

The same window then moved to HS 8101. One full 100-call chunk and one
interrupted-but-force-merged chunk advanced HS 8101 to 89,298 merged rows.
After the interrupted merge settled, the final full dry run reported 6,592
total downloader gaps: 5,248 in the main 31-product universe and 1,344 in the
excluded diagnostics. The remaining main-universe requests are now:

- HS 8101: 320
- HS 8103: 448
- HS 8108: 448
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

This checkpoint ended by manual stop and force-merge while the API was still
productive, not by true quota exhaustion and not by API unreliability. Next
priority is to continue HS 8101 in 100-200 call one-worker chunks while it is
landing rows cleanly, then move to HS 8103, HS 8108, HS 8109, HS 8104, and HS
8105 before the deferred or marginal products.

Later on June 28, 2026, a direct probe confirmed the API was still usable:
both keys returned `200` and 2,668 rows for a still-missing HS 8101
reporter-year file. The downloader therefore resumed immediately. A productive
HS 8101 chunk advanced the merged file from 89,298 rows to 128,215 rows and
cut remaining HS 8101 gaps from 320 to 277. The same run then degraded back
into the non-closing one-request-per-minute pattern. Two cooldown cycles and
25-call one-worker retries on HS 8101 did not close any additional files, so
the run rotated to HS 8103. HS 8103 showed the same immediate non-closing
behavior, after which direct probes on both keys returned `403 Out of call
volume quota` with `Retry-After` values of roughly 15 hours 9 minutes.

Approximate additional counted API usage in this continuation was about 31
productive HS 8101 calls, about 11 non-closing HS 8101 calls, 4 non-closing
retry calls, and 2 non-closing HS 8103 calls before the final direct quota
probe. This continuation therefore ended by confirmed true quota exhaustion,
not by mere API unreliability. The settled full dry run now reports 6,549
total downloader gaps: 5,205 in the main 31-product universe and 1,344 in
excluded diagnostics.

Current remaining main-universe requests after the June 28 continuation are:

- HS 8101: 277
- HS 8103: 448
- HS 8108: 448
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Next quota-window order:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8101 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
```

On June 29, 2026, the automation resumed with the required explicit
`/Users/elgask0/miniconda/bin/python` audit. Opening dry runs confirmed
6,549 total downloader gaps: 5,205 in the main 31-product universe and 1,344
in excluded diagnostics HS 380120, HS 2827, and broad HS 2617. HS 8101 was
then finished first in two productive one-worker chunks. The first 100-call
chunk returned 75,111 rows and four valid no-data responses. The second
177-call chunk returned 95,106 rows and 36 valid no-data responses, completing
HS 8101 through March 2026 with 298,432 merged rows.

The same window then moved into the metal-family block. HS 8103 used 145
counted API calls in a 150-target chunk, landing 30,244 rows, 15 valid
no-data responses, and five errors before the merge settled at 303 remaining
reporter-year gaps and 30,244 merged rows. HS 8108 then used 95 counted API
calls in a 100-target chunk, landing 93,794 rows, two valid no-data
responses, and five errors before the merge settled at 369 remaining gaps and
93,794 merged rows. A small HS 8109 probe immediately fell into the familiar
one-request-per-minute non-closing pattern with zero rows, zero valid no-data
files, and zero counted errors, so it was interrupted and force-merged with no
persisted files.

Direct quota probes on a still-missing HS 8109 request then returned `403 Out
of call volume quota` on both keys, with `Retry-After` values of roughly
76,774 seconds and explicit replenishment messages of about 21 hours 19
minutes. That is confirmed true quota exhaustion, not mere API unreliability.
Approximate counted API usage for the June 29 window was about 519-521 calls:
277 productive HS 8101 calls, 145 counted HS 8103 calls, 95 counted HS 8108
calls, and 2 direct quota-confirmation probes, plus an interrupted zero-yield
HS 8109 probe that did not produce any persisted files.

The settled final dry run now reports 6,048 total downloader gaps: 4,704 in
the main 31-product acquisition universe and 1,344 in excluded diagnostics.
Current remaining main-universe requests after the June 29 run are:

- HS 8103: 303
- HS 8108: 369
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448

On July 4, 2026, the automation resumed with the required explicit Python path
and started with the mandatory full dry-run audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening audit: 4,382 total downloader gaps, of which 3,038 were in the main
31-product universe and 1,344 were in excluded diagnostics HS 380120, HS 2827,
and broad HS 2617. All unfinished higher-priority products ahead of HS 8105
were already complete, so the run stayed on cobalt.

The first HS 8105 attempt used an oversized 150-call one-worker chunk and was
manually interrupted once it became clear the current API window was too slow
for such a long checkpoint. Two follow-up HS 8105 25-call one-worker chunks
completed cleanly:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 25 --workers 1
```

Those two completed chunks delivered 50 counted API calls, 29,417 new rows,
4 valid no-data responses, 0 errors, and 0 rate-limit responses. A final
25-call continuation degraded into low-yield behavior after a few saved files
and was manually interrupted, then force-merged with the script's `merge_all`
helper.

Settled July 4 results:

- HS 8105 moved from 52,064 merged rows and 366 remaining gaps to 82,820
  merged rows and 303 remaining gaps.
- Main-universe remaining gaps fell from 3,038 to 2,975.
- Full-universe remaining gaps fell from 4,382 to 4,319.
- Excluded diagnostics remained unchanged at 1,344 gaps.
- Approximate counted API usage was about 58-60 calls including the two
  interrupted partial HS 8105 chunks.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final dry run: 4,319 total downloader gaps, of which 2,975 remain in
the main 31-product acquisition universe and 1,344 remain in excluded
diagnostics. Current main-universe queue:

- HS 8105: 303
- HS 282110: 432
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

This run did not end by confirmed true quota exhaustion. No persistent `429`
cluster appeared, and there were no repeated cross-key `403 Out of call volume
quota` refusals or `Retry-After` headers. It ended because live throughput
degraded again into a low-yield pattern, so the saved cobalt files were
force-merged and the session was closed on a fresh audit. Next priority remains
HS 8105, then HS 282110 if cobalt again stalls after cooldown.

Later on July 4, 2026, the automation was resumed with explicit instruction to
continue until a hard quota stop. It reopened from the settled earlier-July-4
state:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening continuation audit:

- Main 31-product universe: 2,975
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 4,319

The continuation stayed on HS 8105 first. Productive 50-, 25-, 50-, 75-, and
32-call one-worker chunks, plus one small interrupted/force-merged reopening,
completed the product through March 2026. Settled HS 8105 result:

- merged rows: 225,694
- remaining gaps: 0
- net gain in this continuation: 142,874 rows and 303 closed reporter-year gaps

HS 282110 was then opened and proved productive. One 25-call one-worker chunk,
two completed 50-call one-worker chunks, and one interrupted/force-merged
partial 50-call chunk advanced the product materially before a masked-refusal
pattern appeared. Settled HS 282110 result:

- merged rows: 92,052
- remaining gaps: 296
- net gain in this continuation: 83,914 rows and 136 closed reporter-year gaps

Approximate counted downloader usage for the continuation was about 446 calls
plus two direct quota-confirmation probes. Across HS 8105 and HS 282110, the
continuation saved about 226,788 merged rows.

The stop condition is now confirmed true quota exhaustion. At about 15:33 CST
on July 4, 2026, both keys were probed directly on a still-missing HS 282110
request after the downloader entered a long one-completion-per-minute pattern
with no new rows, no valid empty files, and no counted errors. Probe result on
both keys:

- status: `403 Out of call volume quota`
- `Retry-After`: about 59,172 seconds
- replenishment message: about 16 hours 26 minutes remaining

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final full-July-4 gap counts:

- Main 31-product universe: 2,536
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,880

Current remaining main-universe queue:

- HS 282110: 296
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

HS 8105 is now complete through March 2026. The next quota-window order is
HS 282110 first, then HS 2820, HS 2833, HS 284610, HS 280450, and HS 284690.
This later July 4 continuation supersedes the earlier same-day stop reason:
the final day-end condition is confirmed true quota exhaustion, not mere API
unreliability.

On July 5, 2026, the automation resumed from that settled July 4 close with
the required explicit Python path and opened with the standard full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 5 gap counts:

- Main 31-product universe: 2,536
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,880

The run first stayed on HS 282110. Productive 50-, 50-, 75-, 75-, 50-, 38-,
11-, and 1-call one-worker chunks completed the product through March 2026.
Settled HS 282110 result:

- merged rows: 250,828
- remaining gaps: 0
- net gain in this July 5 run: 158,776 rows and 296 closed reporter-year gaps

The same quota window then moved to HS 2820. Three productive completed
one-worker chunks and one interrupted/force-merged partial chunk advanced the
product materially:

- merged rows: 39,990
- remaining gaps: 294
- net gain in this July 5 run: 39,990 rows and 154 closed reporter-year gaps

Local file counts show HS 2820 is now complete for 2019 and 2020 and partly
closed in 2021; the remaining gaps are 2021 (14), 2022 (56), 2023 (56), 2024
(56), 2025 (56), and 2026 (56). After the productive partial chunk, HS 2820
entered the familiar one-completion-per-minute masked-refusal pattern with no
new rows, no valid empty files, and no counted errors. Two cooldown cycles and
smaller reopen attempts did not restore useful responses, so the run rotated to
HS 2833 per the persistence rule.

HS 2833 immediately reproduced the same sterile completion pattern. At that
point both keys were probed directly on a still-missing HS 2833 request. Probe
result on both keys:

- status: `403 Out of call volume quota`
- `Retry-After`: about 37,427 seconds
- replenishment message: about 10 hours 24 minutes remaining

The probe time was about 15:36 CEST on July 5, 2026. This is confirmed true
quota exhaustion, not just a product-level slowdown.

Approximate counted downloader usage for the July 5 run was about 509 calls,
plus two direct quota-confirmation probes. Across the two productive main
products, the run saved about 198,766 merged rows.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final July 5 gap counts:

- Main 31-product universe: 2,086
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,430

Current remaining main-universe queue:

- HS 2820: 294
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

HS 282110 is now complete through March 2026. The next quota-window order is
HS 2820 first, then HS 2833, HS 284610, HS 280450, and HS 284690. Because
HS 2820 failed two cooldown reopen cycles at the end of this run, it should be
retried cautiously with a small chunk after the next reset rather than with a
large initial block. The day ended by confirmed true quota exhaustion.
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

On July 6, 2026, the automation resumed from that settled July 5 close with
the required explicit Python path and the standard full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 6 gap counts:

- Main 31-product universe: 2,086
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,430

The run stayed on the remaining priority order and reopened HS 2820 first.
Two short one-worker chunks were manually interrupted because they looked like
the same sterile one-completion-per-minute pattern as late July 5. However,
both interrupted chunks continued briefly in the background. After the stale
processes were explicitly killed and the product was force-merged again, the
settled HS 2820 state was:

- merged rows: 53,127
- remaining gaps: 231
- net gain in this July 6 run: 13,137 rows and 63 closed reporter-year gaps

HS 2833 was then tested twice. The first 25-file chunk saved only a few files
before it was stopped. The second 25-file chunk completed cleanly and showed
that HS 2833 can still use the window productively:

- completed chunk result: 22 counted API calls, 21,390 rows, 3 errors, 1
  rate-limit response

A third HS 2833 chunk then slipped back into a low-yield error pattern and was
also interrupted. As with HS 2820, the interrupted process kept running
briefly in the background until it was explicitly killed and force-merged.
Settled HS 2833 state after cleanup:

- merged rows: 32,487
- remaining gaps: 414
- net gain in this July 6 run: 32,487 rows and 34 closed reporter-year gaps

Because the downloader can mask subscription behavior, both keys were directly
probed on a still-missing HS 2833 request before stopping. Probe result:

- key 1: `200` with `count: 0`
- key 2: `429 Rate limit is exceeded. Try again in 1 seconds.`

This is not true quota exhaustion. It indicates an unstable but still-live API
window with mixed clean no-data and short-throttle responses.

Approximate observed counted usage for July 6 was at least about 31 downloader
calls plus two direct quota-state probes. The true downloader-call total was
likely somewhat higher because the two interrupted one-worker chunk processes
continued briefly in the background before being killed and force-merged.

Closing audits:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2820,2833,284610,280450,284690 --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 380120,2827,2617 --through 202603 --dry-run
```

Settled final July 6 gap counts:

- Main 31-product universe: 1,989
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,333

Current remaining main-universe queue:

- HS 2820: 231
- HS 2833: 414
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

No product was fully completed on July 6. The next quota-window order remains
HS 2820 first, then HS 2833, HS 284610, HS 280450, and HS 284690. Because
both HS 2820 and HS 2833 can leave live worker processes behind after manual
interrupts, the next run should explicitly check for lingering
`download_all_gaps.py` processes before trusting any fresh audit. The day
ended by API unreliability, not by confirmed quota exhaustion.

On July 7, 2026, the automation resumed from that settled July 6 close with
the required explicit Python path and the standard full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 7 gap counts:

- Main 31-product universe: 1,989
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,333

The run stayed on the remaining main-universe priority order. HS 2820 reopened
first and proved clearly productive, so it was allowed to complete two large
one-worker chunks plus a cleanup pass:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2820 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2820 --through 202603 --max-calls 92 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2820 --through 202603 --max-calls 25 --workers 1
```

Settled HS 2820 state after those completed chunks:

- merged rows: 99,790
- remaining gaps: 3
- net gain in this July 7 run: 46,663 rows and 228 closed reporter-year gaps

Observed completed-chunk details for HS 2820:

- 150-target chunk: 150 counted API calls, 37,018 rows, 14 valid no-data
  responses, 0 errors, 11 rate-limit responses
- 92-target chunk: 92 counted API calls, 8,484 rows, 28 valid no-data
  responses, 0 errors, 16 rate-limit responses
- 16-file cleanup pass: 15 counted API calls, 1,161 rows, 2 valid no-data
  responses, 1 error, 2 rate-limit responses

The same window then moved to HS 2833:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 150 --workers 1
```

The HS 2833 chunk was productive but long-running, so it was manually stopped
at a checkpoint after 52 counted completions had been observed and then
force-merged with the downloader helper:

```bash
/Users/elgask0/miniconda/bin/python -c 'import sys; sys.path.insert(0, "04_scripts"); import download_all_gaps as d; d.merge_all(["2833"])'
```

Settled HS 2833 state after that force-merge:

- merged rows: 95,441
- remaining gaps: 359
- net gain in this July 7 run: 62,954 rows and 55 closed reporter-year gaps

Approximate observed counted usage for July 7 was at least about 309
downloader calls. The true total was slightly higher because the interrupted
HS 2833 worker continued advancing briefly between the last visible progress
line and the forced merge. The stop condition was not true quota exhaustion:
there was no persistent cross-key `403 Out of call volume quota` refusal, no
terminal `Retry-After` wall, and no dead zero-progress API pattern. The day
ended by a manual checkpoint while the API was still producing usable
responses.

On July 8, 2026, the automation resumed from that July 7 close with the
required explicit Python path and the standard full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 8 gap counts:

- Main 31-product universe: 1,706
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,050

All earlier priority products above HS 2820 remained complete, so the run
stayed on the remaining main-universe queue: HS 2820, HS 2833, HS 284610,
HS 280450, and HS 284690.

HS 2820 closed first with a short one-worker cleanup chunk:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2820 --through 202603 --max-calls 10 --workers 1
```

Settled HS 2820 state after the completed cleanup chunk:

- merged rows: 101,279
- remaining gaps: 0
- net gain in this July 8 run: 1,489 rows and 3 closed reporter-year gaps

Observed completed-chunk details for HS 2820:

- 3 counted API calls, 1,489 rows, 0 valid no-data responses, 0 errors, and
  0 rate-limit responses

The same window then moved to HS 2833:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 150 --workers 1
```

The HS 2833 chunk initially saved files but then slowed into an extremely
long-running pattern of roughly one saved file every 35-40 seconds. It was
manually interrupted and force-merged to bank the valid partial progress:

```bash
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import importlib.util; p=Path("04_scripts/download_all_gaps.py"); spec=importlib.util.spec_from_file_location("download_all_gaps", p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.merge_all(["2833"])'
```

Settled HS 2833 state after that force-merge:

- merged rows: 111,731
- remaining gaps: 354
- net gain in this July 8 run: 16,290 rows and 5 closed reporter-year gaps

After a 10-minute cooldown, the run probed HS 284610 with a smaller chunk:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 25 --workers 1
```

Settled HS 284610 state after that completed chunk:

- merged rows: 258
- remaining gaps: 447
- net gain in this July 8 run: 258 rows and 1 closed reporter-year gap

Observed completed-chunk details for HS 284610:

- 1 counted API call, 258 rows, 0 valid no-data responses, 24 errors, and
  0 rate-limit responses

The final July 8 audit was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing July 8 gap counts:

- Main 31-product universe: 1,697
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,041

Remaining main-universe queue after the July 8 run:

- HS 2833: 354
- HS 284610: 447
- HS 280450: 448
- HS 284690: 448

Approximate observed counted usage for July 8 was only about 9 successful
downloader calls. The stop condition was not true quota exhaustion: there was
no persistent cross-key `403 Out of call volume quota` refusal, no explicit
quota-reset header, and no sustained `429` wall. The day ended by severe API
unreliability and very low throughput after the HS 2820 cleanup. The next
priority remains HS 2833, then HS 284610, then HS 280450, and finally
HS 284690.

On July 9, 2026, the automation resumed from that July 8 close with the
required explicit Python path and the standard full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 9 gap counts:

- Main 31-product universe: 1,697
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,041

All earlier priority products above HS 2833 remained complete, so the live
main-universe queue stayed HS 2833, HS 284610, HS 280450, and HS 284690.

The run attempted to reopen HS 2833 with a conservative one-worker chunk:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 50 --workers 1
```

Settled HS 2833 state after that completed zero-call chunk:

- merged rows: 111,731
- remaining gaps: 354
- net gain in this July 9 run: 0 rows and 0 closed reporter-year gaps

Observed completed-chunk details for HS 2833:

- 0 counted API calls, 0 rows, 0 valid no-data responses, 0 errors, and
  0 rate-limit responses

The zero-call result was not a product-level slowdown. A direct credential
audit showed that the automation shell had no `COMTRADE_API_KEYS`,
`COMTRADE_API_KEY`, `COMTRADE_API_KEY_1`, or `COMTRADE_API_KEY_2` configured,
and `/Users/elgask0/miniconda/bin/python` raised:

```text
RuntimeError: No Comtrade API key configured. Set COMTRADE_API_KEYS or COMTRADE_API_KEY_1/COMTRADE_API_KEY_2 before running downloads.
```

The final July 9 audit was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing July 9 gap counts:

- Main 31-product universe: 1,697
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 3,041

Remaining main-universe queue after the July 9 run:

- HS 2833: 354
- HS 284610: 447
- HS 280450: 448
- HS 284690: 448

Approximate observed counted usage for July 9 was zero successful downloader
calls. The stop condition was not true quota exhaustion and not API
unreliability. The run ended because the execution environment was missing
Comtrade credentials entirely, so no further downloader chunk could reach the
API until `COMTRADE_API_KEYS` or `COMTRADE_API_KEY_1`/`COMTRADE_API_KEY_2` is
restored. The next priority remains HS 2833, then HS 284610, then HS 280450,
and finally HS 284690 once credentials are available again.

Later on July 9, 2026, the automation reran the same audit and confirmed that
the blocker still sat upstream of the API:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 75 --workers 1
```

The dry run again reported 1,697 remaining gaps in the main 31-product
universe and 1,344 in excluded diagnostics, for 3,041 total downloader gaps.
The second HS 2833 probe again completed with 0 counted API calls, 0 rows, 0
valid no-data responses, 0 errors, and 0 rate-limit responses, leaving HS
2833 unchanged at 111,731 merged rows and 354 remaining gaps. Additional
checks found no Comtrade credential wiring in the repository, `~/.zshrc`,
`~/.zprofile`, or recent Codex shell snapshots, so the environment still could
not provide `COMTRADE_API_KEYS`, `COMTRADE_API_KEY`, `COMTRADE_API_KEY_1`, or
`COMTRADE_API_KEY_2`.

No products advanced in this follow-up July 9 rerun and observed counted API
usage remained zero. The stop condition again was missing credentials, not
quota exhaustion and not API unreliability. Estimated days left therefore
remain unchanged at roughly 2 optimistic API days, 7-10 realistic days, or
30-40 pessimistic days once credentials are restored. The next priority
remains HS 2833, then HS 284610, then HS 280450, and finally HS 284690.

Another retry later on July 9, 2026 confirmed the same blocker with the
smallest possible live probe:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 1 --workers 1
```

The full audit again reported 3,041 total downloader gaps. The one-file HS
2833 probe again finished with 0 counted API calls, 0 rows, 0 valid no-data
responses, 0 errors, and 0 rate-limit responses, so the merged HS 2833 file
stayed at 111,731 rows with 354 remaining gaps. A direct loader check still
raised `RuntimeError: No Comtrade API key configured`, and the shell still had
none of `COMTRADE_API_KEYS`, `COMTRADE_API_KEY`, `COMTRADE_API_KEY_1`, or
`COMTRADE_API_KEY_2`. No products advanced and observed counted API usage
remained zero. This retry again ended because credentials were absent before
the first request, not because of quota exhaustion or API unreliability.

Later on July 9, 2026, the missing-credential blocker was cleared and the
downloader resumed real API work immediately. The local credential source was
restored and persisted outside the repository, after which the smallest live
HS 2833 probe returned a normal `200` response with 194 rows and no errors.

The productive continuation then used these completed commands on HS 2833:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 75 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 2833 --through 202603 --max-calls 10 --workers 1
```

Settled HS 2833 results after those chunks:

- merged rows: 488,931
- remaining gaps: 0
- net gain in this continuation: 377,200 rows and 354 closed reporter-year gaps

Observed completed-chunk details on HS 2833:

- 394 counted API calls
- 377,200 new rows
- 38 valid no-data responses
- 1 timeout
- repeated but non-terminal rate-limit responses in the late-period tail

With HS 2833 complete, the same continuation opened HS 284610 with:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 25 --workers 1
```

Settled HS 284610 state after that opening chunk:

- merged rows: 9,410
- remaining gaps: 422
- net gain in this continuation: 9,152 rows and 25 closed reporter-year gaps

Observed completed-chunk details on HS 284610:

- 25 counted API calls
- 9,152 new rows
- 2 valid no-data responses
- 0 errors
- 0 rate-limit responses

The closing July 9 audit was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing July 9 gap counts after credential restoration:

- Main 31-product universe: 1,318
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,662

Remaining main-universe queue after the productive continuation:

- HS 284610: 422
- HS 280450: 448
- HS 284690: 448

Approximate observed counted usage for this productive continuation was 419
successful/rate-limited downloader calls. The stop condition was not true
quota exhaustion and not API unreliability. The run ended by a manual
checkpoint while the API was still producing useful rows and valid no-data
responses. Estimated days left at this point are about 2 optimistic API days,
4-6 realistic days, or 12-18 pessimistic days. The next priority is HS 284610,
then HS 280450, then HS 284690.

Later in the same run, continuing into just after midnight local time on
July 10, 2026, the downloader resumed from that restored-key checkpoint and
kept going until the refusal pattern crossed into true exhaustion territory.
The opening audit for this continuation was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening gap counts for the late continuation:

- Main 31-product universe: 1,318
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,662

The main productive command was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 100 --workers 1
```

That HS 284610 chunk was manually stopped once it entered a non-productive late
tail, and the touched files were then force-merged with the downloader's
`merge_all` helper. Settled HS 284610 state after the checkpoint:

- merged rows: 21,592
- remaining gaps: 337
- net gain in this late continuation: 12,182 rows and 85 closed reporter-year gaps

Observed settled details from the interrupted HS 284610 chunk:

- approximately 91 counted API calls
- 12,182 new rows
- 13 valid no-data responses
- 0 logged errors
- a late sequence of non-productive refusals consistent with `failed_retries`

To distinguish product-tail slowdown from true daily exhaustion, the run then
used these minimal cross-product probes:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 1 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 2 --workers 1
```

Settled exhaustion-probe results:

- HS 280450: 1 counted API call, 0 rows, 0 valid no-data responses, 0 errors,
  `Status failed_retries: 1`, no persisted files, 448 gaps remain.
- HS 284690: 2 counted API calls, 0 rows, 0 valid no-data responses, 0 errors,
  `Status failed_retries: 2`, no persisted files, 448 gaps remain.

Because those refusal probes hit across products and across both keys in the
same process while the endpoint itself remained reachable, this late
continuation is best classified as ending by true quota/refusal exhaustion
rather than by API unreliability.

The closing audit for the late continuation was:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing gap counts after the late continuation:

- Main 31-product universe: 1,233
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,577

Remaining main-universe queue after the late continuation:

- HS 284610: 337
- HS 280450: 448
- HS 284690: 448

Approximate observed counted usage for this late continuation was 94 calls:
about 91 in the productive/interrupted HS 284610 block, one refusal probe on
HS 280450, and two refusal probes on HS 284690. Estimated days left at this
point are about 2 optimistic API days, 4-5 realistic days, or 10-15
pessimistic days. The next priority remains HS 284610, then HS 280450, then
HS 284690 once the next quota window opens.

Later on July 10, 2026, the automation resumed again with the required
explicit Python path and reopened from that same 2,577-gap checkpoint:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening gap counts for this later July 10 continuation:

- Main 31-product universe: 1,233
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,577

The run first tested HS 284610 again:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 100 --workers 1
```

Both HS 284610 chunks were manually stopped and force-merged because the
product stayed in a low-yield pattern without a clean quota wall. Settled
state after both interrupted probes:

- merged rows: 24,682
- remaining gaps: 333
- net gain in this later continuation: 3,090 rows and 4 closed reporter-year gaps
- approximate counted usage on HS 284610 today: about 7 calls

The productive center of the run was HS 280450. After one weak opening probe,
a 10-minute cooldown, and a small retry that showed real rows again, the run
kept the same product open and scaled into larger chunks:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 10 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 280450 --through 202603 --max-calls 1 --workers 1
```

Settled HS 280450 result:

- merged rows: 40,516
- remaining gaps: 0
- one main-universe product completed through March 2026
- approximate counted usage on HS 280450 today: about 391 calls

The productive completed chunks on HS 280450 yielded:

- 23 counted calls, 2,327 rows, 1 valid no-data file, and 2 timeouts in the
  first successful 25-target retry after cooldown
- 100 counted calls, 8,230 rows, 23 valid no-data files, 0 logged errors, and
  2 rate-limit retries in the next 100-target chunk
- 100 counted calls, 11,083 rows, 16 valid no-data files, 0 logged errors,
  and 3 rate-limit retries in the following 100-target chunk
- 100 counted calls, 8,847 rows, 17 valid no-data files, 0 logged errors, and
  9 rate-limit retries in the third 100-target chunk
- 133 counted calls, 8,589 rows, 35 valid no-data files, 0 logged errors, and
  28 rate-limit retries in the 133-file finish attempt
- 28 counted calls, 648 rows, 11 valid no-data files, and 6 rate-limit
  retries in the cleanup pass
- 6 counted calls, 97 rows, and 1 rate-limit retry in the six-file tail
- 1 counted call and a final valid no-data closeout on the last remaining file

The run then tested HS 284690 twice, once before and once after a 10-minute
cooldown:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 25 --workers 1
```

Both HS 284690 probes were manually stopped and force-merged because they
remained non-productive. In both passes, counted requests advanced at about
one per minute but produced zero rows, zero valid no-data files, zero logged
errors, and no persisted files to merge. Settled state after both probes:

- merged file: still absent
- remaining gaps: 448
- approximate counted usage on HS 284690 today: about 7 calls

Because the late-day blocker was this uneven no-state behavior rather than a
clear 429 wall or persistent cross-key quota refusals, this continuation ended
because of API unreliability, not confirmed true quota exhaustion.

Closing audit for this later July 10 continuation:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing gap counts after this later July 10 continuation:

- Main 31-product universe: 781
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,125

Remaining main-universe queue after this later July 10 continuation:

- HS 284690: 448
- HS 284610: 333

Approximate observed counted usage for this later July 10 continuation was
about 408 calls. Estimated days left at this point are about 1 optimistic API
day, 2-3 realistic days, or 5-8 pessimistic days. The next priority is HS
284610, then HS 284690.

On July 11, 2026, the automation resumed from that checkpoint with the
required explicit Python path and the mandatory full dry-run audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening gap counts for July 11:

- Main 31-product universe: 781
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 2,125

Only two main-universe products remained in scope: HS 284610 (333) and
HS 284690 (448). The run therefore stayed on HS 284610 first.

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 75 --workers 1
```

Settled HS 284610 result after the three completed chunks:

- merged rows: 93,612
- remaining gaps: 20
- net gain: 68,930 rows and 313 closed reporter-year gaps
- completed-chunk usage: 366 counted API calls, 53 valid no-data files,
  1 logged error, and 53 rate-limit/refusal-cycle outcomes

The final short cerium retry then stalled in the sterile one-completion-per-
minute pattern with no saved rows or valid `skip` files, so it was interrupted
and force-merged:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps as d; d.merge_all(["284610"])'
```

The run then moved to HS 284690. Its first large chunk was still productive:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 150 --workers 1
```

Settled HS 284690 result after the productive chunk:

- merged rows: 45,832
- remaining gaps: 315
- net gain: 45,832 rows and 133 closed reporter-year gaps
- completed-chunk usage: 150 counted API calls, 12 valid no-data files,
  0 logged errors, and 2 rate-limit responses

After that first chunk, HS 284690 repeatedly failed to reopen productively.
The automation followed the persistence rules exactly: interrupt, force-merge,
wait 10 minutes, retry with a smaller chunk, and repeat once more before
rotating away:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps as d; d.merge_all(["284690"])'
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps as d; d.merge_all(["284690"])'
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps as d; d.merge_all(["284690"])'
```

Those post-productive retries all showed the same non-quota pattern: roughly
one completed request per minute, zero rows, zero valid no-data responses,
zero logged errors, and no clear 429 wall. A final rotation back to a tiny
HS 284610 retry showed the same sterile behavior. Because neither remaining
main-universe product could produce counted useful outcomes after repeated
cooldowns, the run stopped on extended API unreliability rather than confirmed
true quota exhaustion.

Closing audit for July 11:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Closing gap counts after July 11:

- Main 31-product universe: 335
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 1,679

Remaining main-universe queue after July 11:

- HS 284610: 20
- HS 284690: 315

Approximate observed counted usage for July 11 was about 520-530 calls. That
includes 516 counted calls from the four completed productive chunks plus
roughly a dozen sterile partial completions from the interrupted retries. The
day closed 446 main-universe reporter-year gaps but did not fully complete a
product. The stop reason is extended API unreliability, not confirmed quota
exhaustion. Immediate next priority: retry HS 284610 first, then return to
HS 284690.

On July 12, 2026, the automation resumed from that checkpoint with the
required explicit Python path and the mandatory full dry-run audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening gap counts for July 12:

- Main 31-product universe: 335
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 1,679

Only two main-universe products remained in scope: HS 284610 (20) and
HS 284690 (315). All earlier priority products were already complete, so the
run stayed on those two products until the main universe closed.

Completed productive chunks:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 10 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 173 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 40 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610 --through 202603 --max-calls 5 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284690 --through 202603 --max-calls 10 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 284610,284690 --through 202603 --max-calls 5 --workers 1
```

Settled product results after the July 12 run:

- HS 284610: merged rows increased from 93,612 to 94,308 and remaining gaps
  fell from 20 to 0.
- HS 284690: merged rows increased from 45,832 to 136,050 and remaining gaps
  fell from 315 to 0.

Closing audit for July 12:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8110,261710,282580,2504,811292,282560,2818,8111,2811,3801,8106,284180,8101,2615,284170,811221,380130,282530,282520,282570,8103,8108,8109,8104,8105,282110,2820,2833,284610,280450,284690 \
  --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 380120,2827,2617 --through 202603 --dry-run
```

Closing gap counts after July 12:

- Main 31-product universe: 0
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 1,344

Approximate observed counted usage for July 12 was 391 API calls. The run
added 90,914 rows, saved 58 valid no-data responses, logged zero errors, and
fully completed the planned 31-product acquisition universe through March
2026. The stop reason is objective completion, not true quota exhaustion and
not API unreliability. Estimated days left for the planned universe are 0
optimistic, 0 realistic, and 0 pessimistic. There is no remaining
main-universe priority; only the excluded diagnostics remain if they are ever
explicitly resumed.

On July 13, 2026, the automation opened with the mandatory completion audit and
did not download further because the planned universe was already closed:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening and closing gap counts for July 13 were identical:

- Main 31-product universe: 0
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 1,344

No additional products were touched. Approximate counted API usage for July 13
was zero calls because the audit confirmed that the objective was already met.
The stop reason is objective completion, not true quota exhaustion and not API
unreliability. Estimated days left for the planned universe remain 0
optimistic, 0 realistic, and 0 pessimistic. If excluded diagnostics are ever
resumed, the backlog remains HS 380120 (448), HS 2827 (448), and HS 2617
(448); otherwise there is no next priority inside the planned 31-product
scope.

On June 30, 2026, the automation resumed with the required explicit Python
path and full dry-run audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

The opening audit confirmed 6,048 total downloader gaps, of which 4,704 were
in the main 31-product acquisition universe and 1,344 were in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617. It also confirmed that the
earlier priorities HS 282570, HS 8106, HS 284180, and HS 8101 were already
fully closed, so the run moved directly to the remaining metal-placebo block.

Completed productive chunks:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
```

Results:

- HS 8103: 98 counted API calls, 29,477 new rows, 10 valid no-data files,
  2 errors; merged rows increased to 59,721 and remaining gaps fell from
  303 to 205.
- HS 8108: 98 counted API calls, 155,380 new rows, 5 valid no-data files,
  2 errors; merged rows increased to 249,174 and remaining gaps fell from
  369 to 271.

Earlier in the same API day, the log already contained one productive HS 8108
chunk with 95 counted calls plus a short HS 8109 probe that consumed about
two counted calls without persisting any files. Approximate counted API usage
for the June 30 window was therefore about 293 calls.

Closing audits:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103,8108,8109,8104,8105,282110,2820,2833,284610,280450,284690 \
  --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 380120,2827,2617 --through 202603 --dry-run
```

Settled post-run gap counts:

- Main 31-product universe: 4,508
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,852

Current main-universe queue:

- HS 8103: 205
- HS 8108: 271
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Stop reason: manual clean-handoff stop while the API was still productive.
This did not end by true quota exhaustion and did not end by API unreliability.
No persistent `429`, `403 Out of call volume quota`, `409` refusal loop, or
retry-after exhaustion signal appeared. Immediate next priority remains
HS 8103, then HS 8108, then HS 8109 and the rest of the metal-family block
before the deferred and marginal products.

Later on June 30, 2026, the same API day was continued rather than left at the
midday handoff. HS 8103 was completed first:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 10 --workers 1
```

HS 8103 results for the continuation:

- First 100-target chunk: 98 counted API calls, 16,482 new rows,
  14 valid no-data files, 2 errors.
- Second 100-target chunk: 99 counted API calls, 13,995 new rows,
  29 valid no-data files, 1 error.
- Tail retry: 8 counted API calls, 156 new rows, 5 valid no-data files,
  0 errors.

HS 8103 is now complete through March 2026 with 90,354 merged rows.

HS 8108 then remained intermittently productive but unstable. The continuation
used multiple chunks, cooldowns, and force-merges:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 25 --workers 1
```

HS 8108 continuation results:

- First partial 100-target chunk: 22 counted API calls, 33,868 new rows,
  0 valid no-data files, 78 errors; merged and cooled down.
- First 25-call retry after cooldown: 25 counted API calls, 18,983 new rows,
  3 valid no-data files, 0 errors.
- Second partial 100-target chunk: 32 counted API calls, 60,439 new rows,
  0 valid no-data files, 68 errors; merged and cooled down.
- Second 25-call retry after cooldown: 24 counted API calls, 35,873 new rows,
  3 valid no-data files, 1 error.
- Final interrupted 100-target chunk: 10 counted completions, 9,331 rows,
  then a zero-yield one-request-per-minute stretch; stopped manually and
  force-merged.

After all settled merges, HS 8108 increased from 249,174 merged rows at the
midday handoff to 407,668 merged rows and fell from 271 remaining gaps to 164.

The next product probes did not reopen cleanly:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 25 --workers 1
```

Both HS 8109 probes and the HS 8104 opening probe showed the same
non-productive pattern: one completion per minute, zero rows, zero valid
no-data files, zero rate-limit signals, and no persisted files even after
cooldown. Those probes were interrupted and force-merged, leaving both
products unchanged.

Approximate counted API usage for this continuation was about 326 calls.
Combined with the earlier June 30 session, approximate counted API usage for
the full June 30 API day was about 619 calls.

Final closing audits for the day:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108,8109,8104,8105,282110,2820,2833,284610,280450,284690 \
  --through 202603 --dry-run
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 380120,2827,2617 --through 202603 --dry-run
```

Settled final June 30 gap counts:

- Main 31-product universe: 4,196
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,540

Current main-universe queue at end of day:

- HS 8108: 164
- HS 8109: 448
- HS 8104: 448
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Stop reason: API unreliability on new-product probes, not true quota
exhaustion. No persistent `429`, no direct `403 Out of call volume quota`, and
no `409` subscription-refusal loop appeared at the end state. Immediate next
priority is to finish HS 8108, then retry HS 8109 once more before rotating to
HS 8104 only if the same zero-yield pattern persists.

Next quota-window order:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8103 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
```

On July 1, 2026, the automation resumed with the required explicit Python path
and a full dry-run audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

The opening audit confirmed 5,540 total downloader gaps, of which 4,196 were
in the main 31-product acquisition universe and 1,344 were in excluded
diagnostics HS 380120, HS 2827, and broad HS 2617.

HS 8108 was then fully closed in two productive one-worker chunks:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 100 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8108 --through 202603 --max-calls 75 --workers 1
```

HS 8108 results:

- First chunk: 99 counted API calls, 148,436 new rows, 11 valid no-data files,
  1 error.
- Tail chunk: 65 counted API calls, 28,009 new rows, 23 valid no-data files,
  0 errors.

HS 8108 is now complete through March 2026 with 584,113 merged rows.

The run then rotated through the remaining metal-family products using smaller
unstable-product probes and force-merges where needed:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 25 --workers 1
```

Settled partial results after manual interruption plus `merge_all`:

- HS 8109: advanced from 448 remaining gaps to 422 and now has 6,871 merged
  rows.
- HS 8104: advanced from 448 remaining gaps to 445 and now has 686 merged
  rows.
- HS 8105: opening probe did not persist any files.

HS 8109 was given a 10-minute cooldown and a second 25-call retry, but both
attempts returned to the same non-closing low-yield pattern after only a few
saved files. HS 8104 and HS 8105 also opened weakly, so the run stopped
instead of burning more time on one-request-per-minute stretches.

Direct probes on both registered keys against a still-missing request returned
immediate `200` no-data responses rather than `429`, `403 Out of call volume
quota`, or `409` refusal loops. This means the July 1 run ended because of API
unreliability and uneven product behavior, not confirmed true quota exhaustion.

Approximate counted API usage for the day was about 190-195 calls: 164 counted
HS 8108 calls, roughly 17 counted HS 8109 completions across two interrupted
chunks, roughly 7 counted HS 8104 completions, and 2 direct probes on the two
keys.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final July 1 gap counts:

- Main 31-product universe: 4,003
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,347

Current main-universe queue at end of day:

- HS 8109: 422
- HS 8104: 445
- HS 8105: 448
- HS 282110: 448
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Stop reason: API unreliability on unstable-product probes, not true quota
exhaustion. Immediate next priority is to resume HS 8109 with one-worker
25-50 call chunks after the next cooldown/reset window, then continue to
HS 8104 and HS 8105 before the deferred and marginal products.

If HS 8103 or HS 8108 keeps landing files cleanly, stay in 100-200 call
chunks. If HS 8109 immediately re-enters the zero-yield pattern after the next
reset, force-merge, wait 10-15 minutes, retry once, then rotate to HS 8104.

### Deferred: Clean February 2025 cases and matched control

```bash
python 04_scripts/download_all_gaps.py \
  --products 8106,284180,284170 --max-calls 160
```

- 8106: bismuth metal, clean HS-6 candidate.
- 284180: tungstates/APT, clean HS-6 candidate.
- 284170: same-heading untreated candidate for 284180.

Download 8106 first if only one treated product can be completed.

### Deferred: Graphite-adjacent control

```bash
python 04_scripts/download_all_gaps.py \
  --products 380130 --max-calls 160
```

HS 380130 is a candidate, not automatically a valid placebo. HS 380120 is
policy-ambiguous and excluded from the main donor pool.

### Deferred: Partial tungsten and metal controls

```bash
python 04_scripts/download_all_gaps.py --batch wave4-partial --max-calls 160
python 04_scripts/download_all_gaps.py --batch metal-placebos --max-calls 160
```

The metal-control order is 8103, 8108, 8109, then the more cyclical 8104 and
8105.

### Deferred: Broad acquisition

Run only if the main treated products lack enough acceptable controls:

```bash
python 04_scripts/download_all_gaps.py \
  --batch deferred-placebos --max-calls 160
python 04_scripts/download_all_gaps.py \
  --batch marginal-treated --max-calls 160
```

Deferred controls: 282110, 2820, 2833, and 284610. Marginal treated products:
280450 and 284690. HS 2827 is excluded because it contains controlled GeCl4.

### Product-count convention

- The downloader knows 34 HS products.
- The policy-screened bilateral acquisition universe is 31 products.
- The difference is deliberate: HS 380120 and HS 2827 are
  policy-contaminated, and broad HS 2617 is retained only as a China-export
  diagnostic because the HS-4 bilateral panel mixes antimony and non-antimony
  ores.
- HS 3801 is downloaded but not classified as a placebo.
- The final estimation sample will be smaller and selected by documented
  policy and pre-treatment diagnostics.

### Completion checks

For every downloaded product:

1. all expected reporter-year files exist as data or valid `skip`;
2. 2026 files contain only January-March requests;
3. merged periods do not exceed 202603;
4. canonical World and bilateral totals reconcile;
5. product coverage and zero shares are recorded before model inclusion.

## Eurostat

- [x] Eight raw CN8 files downloaded.
- [x] Country rows normalized to the current EU27.
- [x] UK and duplicate aggregate rows excluded.
- [x] Missing trade records balanced to zero with observation flags.
- [x] Country and EU27 monthly processed panels generated.

Regenerate with:

```bash
python 04_scripts/prepare_eurostat_cn8.py
```

Later on July 1, 2026, the automation was continued rather than left at the
morning handoff. Opening dry run:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

The continuation opened at 5,346 total downloader gaps: 4,002 in the main
31-product universe and 1,344 in excluded diagnostics HS 380120, HS 2827, and
broad HS 2617.

HS 8109 remained unstable. A 25-call one-worker chunk was interrupted after it
returned mostly one-completion-per-minute errors with only marginal progress.
After force-merging, HS 8109 moved from 422 remaining gaps to 420 and later
settled at 401 remaining gaps with 7,529 merged rows.

HS 8105 was the most productive target in this continuation. The first 25-call
one-worker chunk completed cleanly enough to be worth keeping:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 25 --workers 1
```

Result: 23 counted API calls, 14,925 new rows, 0 valid no-data files, and
2 errors. The merged HS 8105 file increased to 15,227 rows and the product
fell to 424 remaining gaps.

Follow-up attempts on HS 8105 and a fresh 25-call opening probe on HS 282110
did not reopen cleanly. Both fell back into the familiar low-yield pattern,
were interrupted, and were force-merged:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 282110 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 25 --workers 1
```

Settled post-merge status for the touched products:

- HS 8109: 7,529 merged rows, 401 remaining gaps.
- HS 8104: 686 merged rows, 445 remaining gaps.
- HS 8105: 15,810 merged rows, 417 remaining gaps.
- HS 282110: no merged row file yet, but remaining gaps fell from 448 to 445,
  consistent with valid no-data responses being persisted.

Direct probes on both keys for HS 8105 and HS 282110 still returned immediate
`200` no-data responses rather than `429`, `403 Out of call volume quota`, or
`409` refusal loops. This continuation therefore also ended because of API
unreliability and uneven product behavior, not true quota exhaustion.

Approximate counted API usage for the continuation was about 40-45 calls,
mostly from the productive first HS 8105 chunk plus a smaller number of
partially completed unstable probes and direct-key checks.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final July 1 continuation gap counts:

- Main 31-product universe: 3,948
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,292

Current main-universe queue after the continuation:

- HS 8109: 401
- HS 8104: 445
- HS 8105: 417
- HS 282110: 445
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Stop reason: repeated low-yield API unreliability across new chunks, not true
quota exhaustion. Immediate next priority remains HS 8109 first, but if it
again opens with one-completion-per-minute errors, rotate quickly to HS 8105,
then HS 8104, then HS 282110.

On July 2, 2026, the automation resumed from that handoff using the required
explicit Python path and began with the mandatory audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 2 gap counts:

- Main 31-product universe: 3,900
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,244

The opening audit also confirmed that the earlier priority blocks were already
complete through March 2026, so the live queue started at HS 8109, then HS
8104, then HS 8105 and the deferred products.

HS 8109 was retried first. A 150-call one-worker chunk immediately degraded to
roughly one counted error per minute, so it was interrupted and force-merged:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; \
sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps \
as d; d.merge_all(["8109"])'
```

After a cooldown, HS 8109 was retried twice more with 25-call one-worker
chunks. Both retries reproduced the same one-call, one-error pattern and were
again force-merged:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
```

Settled HS 8109 result for July 2:

- merged rows: 10,571
- remaining gaps: 398
- net change: 3 reporter-year files closed

Per the persistence rule, the run then rotated to the next priority product:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; \
sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps \
as d; d.merge_all(["8104"])'
```

HS 8104 opened with the same immediate one-call, one-error pattern and showed
no progress. Its merged file remains at 686 rows with 445 gaps.

Approximate counted API usage for July 2 was only about 4-6 calls. The run did
not encounter `429` rate limits, persistent `403 Out of call volume quota`, or
`409` subscription refusal loops. Instead it spent an extended period across
multiple products producing slow transport failures with minimal useful
closures. This day therefore ended because of API unreliability and likely
reachability problems, not true quota exhaustion.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final July 2 gap counts:

- Main 31-product universe: 3,897
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,241

Current main-universe queue after July 2:

- HS 8109: 398
- HS 8104: 445
- HS 8105: 382
- HS 282110: 432
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Immediate next priority: return to HS 8109 first. If it again opens with the
same one-completion-per-minute error pattern after a small probe, rotate
quickly to HS 8104, then HS 8105, then HS 282110 to salvage useful quota.

Later on July 2, 2026, the automation resumed again instead of waiting for the
next calendar day. Opening audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening later-July-2 gap counts:

- Main 31-product universe: 3,849
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 5,193

The opening audit already showed new settled progress on HS 8109: it had moved
from 398 remaining gaps to 350 before any new API requests were made in this
continuation.

HS 8109 was retried first with one-worker chunks:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; \
sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps \
as d; d.merge_all(["8109"])'
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; \
sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps \
as d; d.merge_all(["8109"])'
```

Live progress reports again looked poor, but the settled product still moved:

- HS 8109 merged rows: 24,832
- HS 8109 remaining gaps: 311

Because HS 8109 stayed unstable in live execution, the run rotated to HS 8104.
That rotation proved decisive. The following completed chunks all ran with one
worker:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 25 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 75 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 100 --workers 1
```

Completed HS 8104 chunk results:

- 25-call chunk: 21 counted API calls, 15,009 rows, 0 empties, 4 errors,
  1 rate-limit response. Remaining gaps fell from 445 to 425.
- 50-call chunk: 45 counted API calls, 19,588 rows, 2 valid empties,
  5 errors. Remaining gaps fell to 380.
- 75-call chunk: 68 counted API calls, 30,088 rows, 1 valid empty,
  7 errors. Remaining gaps fell to 312.
- 100-call chunk: 93 counted API calls, 59,210 rows, 4 valid empties,
  7 errors. Remaining gaps fell to 219.

The run then attempted one larger 150-call HS 8104 chunk, but stopped it early
once the pace became too uneven relative to the time cost. Per the execution
policy, the partial progress was force-merged rather than discarded:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 150 --workers 1
/Users/elgask0/miniconda/bin/python -c 'from pathlib import Path; import sys; \
sys.path.insert(0, str(Path("04_scripts").resolve())); import download_all_gaps \
as d; d.merge_all(["8104"])'
```

At interruption time the live progress report had reached 48/150 with 24,364
rows, 1 valid empty, and 10 errors. The settled merged file after force-merge
rose further to 148,953 rows, and the product fell again to 179 remaining
gaps.

Approximate counted API usage for this later July 2 continuation was about
275-315 calls after combining the four completed HS 8104 chunks, the partial
HS 8104 chunk, and the unstable HS 8109 probes. This still does not look like
true quota exhaustion: the run did not hit persistent `403 Out of call volume
quota`, persistent `409` subscription refusal loops, or a terminal wall of
`429` responses. It ended because the active large HS 8104 chunk had become
too slow and uneven, so progress was banked with a force-merge and a fresh
audit.

Closing audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Settled final later-July-2 gap counts:

- Main 31-product universe: 3,544
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 4,888

Current main-universe queue after the later July 2 continuation:

- HS 8109: 311
- HS 8104: 179
- HS 8105: 382
- HS 282110: 432
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Immediate next priority: finish HS 8104 while it is still yielding productive
calls, then return to HS 8109, then HS 8105, then HS 282110.

#### Friday, July 3, 2026

The daily automation again used `/Users/elgask0/miniconda/bin/python`
throughout and began with the required full audit:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --batch all --through 202603 --dry-run
```

Opening July 3 gap counts:

- Main 31-product universe: 3,536
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 4,880

The earlier standing priorities were already complete, including HS 282570,
HS 8106, HS 284180, HS 8101, HS 8103, and HS 8108. The live queue therefore
started at HS 8109, then HS 8104, then HS 8105, then the deferred and
marginal products.

Completed HS 8109 chunk:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 150 --workers 1
```

Result: 147 counted API calls, 32,260 new rows, 10 valid no-data files, 3
errors, 0 rate-limit responses. HS 8109 fell from 311 remaining gaps to 164
before the next retry opened much more slowly.

Follow-up partial retries were stopped manually once they became low-yield and
were force-merged with the script helper:

```bash
/Users/elgask0/miniconda/bin/python - <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location('dag', '04_scripts/download_all_gaps.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.merge_all(['8109', '8104', '8105'])
PY
```

Those partial continuations still advanced the metal-family block. After the
final process cleanup and force-merge pass, the touched merged files settled
at:

- HS 8109: 66,800 rows, 139 remaining gaps
- HS 8104: 202,890 rows, 104 remaining gaps
- HS 8105: 47,504 rows, 373 remaining gaps

Approximate counted API usage for the day was about 260-275 calls. That is far
below the theoretical 900-1000-call target, but the stop condition was not
true quota exhaustion. Comtrade stayed reachable and still produced some data
and valid no-data files, but throughput degraded into very slow, uneven,
low-yield chunks. No persistent `429` wall, no repeated cross-key `403 Out of
call volume quota`, and no terminal `Retry-After` exhaustion signal appeared.

Settled final July 3 gap counts:

- Main 31-product universe: 3,288
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 4,632

Current remaining main-universe requests after the July 3 run are:

- HS 8104: 104
- HS 8109: 139
- HS 8105: 373
- HS 282110: 432
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Immediate next priority by the standing order is HS 8109. If HS 8109 again
opens with the same slow, low-yield pattern, rotate quickly to HS 8104 to
finish it, then return to HS 8105, then HS 282110.

Later on July 3, 2026, the run was explicitly continued until true exhaustion
was confirmed rather than stopping at the first low-yield checkpoint. After a
10-minute cooldown, HS 8109 reopened productively and was pushed through three
additional chunks plus a final single-gap probe:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8109 --through 202603 --max-calls 5 --workers 1
```

Settled HS 8109 result after the continuation:

- merged rows: 90,580
- remaining gaps: 0
- product status: complete through March 2026

The same productive window then fully closed HS 8104:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 75 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8104 --through 202603 --max-calls 50 --workers 1
```

Settled HS 8104 result after the continuation:

- merged rows: 243,194
- remaining gaps: 0
- product status: complete through March 2026

HS 8105 only partially advanced before reverting to the non-closing pattern:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 100 --workers 1
```

That partial chunk was interrupted and force-merged, improving HS 8105 from
47,504 merged rows / 373 gaps to 52,064 merged rows / 366 gaps. After a
10-minute cooldown, a 50-call retry produced only sterile completions and no
new saved files, so the run rotated to HS 282110:

```bash
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 8105 --through 202603 --max-calls 50 --workers 1
/Users/elgask0/miniconda/bin/python 04_scripts/download_all_gaps.py \
  --products 282110 --through 202603 --max-calls 50 --workers 1
```

Both the stalled HS 8105 retry and the opening HS 282110 probe showed the same
sterile pattern: completed requests with no rows, no valid no-data files, and
no counted errors. Because the downloader can hide `403`/`409` refusals inside
that pattern, both keys were then probed directly on a still-missing HS 282110
request. The probe returned:

- key 1: `403 Out of call volume quota`, `Retry-After: 53259`
- key 2: `403 Out of call volume quota`, `Retry-After: 53257`

The probe time was about 17:12 CST on July 3, 2026. That is confirmed true
quota exhaustion with replenishment due in roughly 14 hours 47 minutes, not
mere API unreliability.

Settled final full-July-3 gap counts:

- Main 31-product universe: 3,038
- Excluded diagnostics HS 380120, HS 2827, and broad HS 2617: 1,344
- Total downloader universe: 4,382

Current remaining main-universe requests after the confirmed-exhaustion stop:

- HS 8105: 366
- HS 282110: 432
- HS 2820: 448
- HS 2833: 448
- HS 284610: 448
- HS 280450: 448
- HS 284690: 448

Approximate total counted API usage for the full July 3 run was about 400-420
calls plus two direct quota-confirmation probes. The stop reason for the day is
now confirmed true quota exhaustion. Immediate next priority after quota reset:
resume HS 8105, then HS 282110, then the deferred and marginal products.

## Bloomberg/Wind Terminal

Request January 2019-March 2026 at the highest available frequency. Export
the original history plus identifier metadata. Monthly averages will be built
in the repository.

### Minor metals: exact Fastmarkets specifications

| Priority | Identifier | Required series | Unit | Status |
|---|---|---|---|---|
| High | MB-GA-0001 | Gallium 99.99% min, in-warehouse Rotterdam | USD/kg | [ ] |
| High | MB-GA-0002 | Gallium 99.99% min, in-warehouse China | CNY/kg | [ ] |
| High | MB-GER-0003 | Germanium metal 99.999%, in-warehouse Rotterdam | USD/kg | [ ] |
| High | MB-GER-0004 | Germanium metal 99.999%, 50 ohm-cm, in-warehouse China | CNY/kg | [ ] |
| High | MB-GER-0005 | Germanium dioxide 99.99%, in-warehouse Rotterdam | USD/kg | [ ] |
| High | MB-GER-0006 | Germanium dioxide 99.99%, in-warehouse China | CNY/kg | [ ] |
| High | MB-IN-0002 | Indium 99.99%, in-warehouse Rotterdam | USD/kg | [ ] |
| High | MB-IN-0003 | Indium 99.995%, ex-works China | CNY/kg | [ ] |

### Graphite

| Priority | Identifier/provider | Specification | Unit | Status |
|---|---|---|---|---|
| High | MB-GRA-0042 | Natural flake graphite 94% C, -100 mesh, FOB China | USD/ton | [ ] |
| High | Platts BATAA00 | Natural flake graphite 94-95% C, FOB China | USD/ton | [ ] |
| High | Platts BATBA00 | Same 94-95% C grade, CIF Northeast Asia | USD/ton | [ ] |
| Medium | MB-GRA-0036 | Spherical graphite 99.95% C, 15 micron, FOB China | USD/ton | [ ] |

### Antimony metal

| Priority | Identifier/provider | Specification | Unit | Status |
|---|---|---|---|---|
| High | MB-SB-0003 | MMTA grade II, 99.65% min, Ddp China | CNY/ton | [ ] |
| High | MB-SB-0002 | MMTA grade II, 99.65% min, in-warehouse Rotterdam | USD/ton | [ ] |

### Antimony trioxide and concentrate

| Priority | Provider | Specification | Unit | Status |
|---|---|---|---|---|
| High | Asian Metal | Antimony trioxide 99.5% min, delivered China | CNY/ton | [ ] |
| High | Asian Metal | Antimony trioxide 99.5% min, FOB China | USD/ton | [ ] |
| High | Argus/Asian Metal | Antimony concentrate 50% min, delivered China | CNY/ton Sb | [ ] |

### Tungsten (NEW — for Wave 4 analysis)

| Priority | Provider | Specification | Unit | Status |
|---|---|---|---|---|
| High | Asian Metal | APT, FOB China | USD/mtu | [ ] |
| High | Fastmarkets/MB | APT, FOB China | USD/mtu | [ ] |
| Medium | Asian Metal | Tungsten concentrate 65%, FOB China | USD/ton | [ ] |

### Exchange rates and metadata

- [ ] Monthly CNY per USD.
- [ ] Monthly EUR per USD if Rotterdam trioxide is quoted in EUR/kg.

## Lower-Priority Validation

- [ ] CEPII BACI annual files for cross-validation.
- [ ] METI and Korea MOTIE qualitative supply-chain evidence.

## Downstream Demand Indicators

Request January 2019 onward and preserve original releases:

- [ ] SIA/WSTS monthly global semiconductor sales, USD.
- [ ] WSTS optoelectronics/discretes monthly sales if available.
- [ ] Monthly China power-battery production and installed capacity, GWh.
- [ ] CAAM monthly China NEV production and sales.
- [ ] World Steel Association monthly world and China crude-steel production.
- [ ] NBS/Wind monthly China lead-acid battery output, 10,000 kVAh.

## USGS Market Structure

- [ ] Download USGS Mineral Commodity Summaries 2020-2026.
- [ ] Extract country production, world total, reserves, units for all treated
      and placebo minerals.
- [ ] Calculate pre-treatment China share, HHI, top-three share.
- [ ] Record source URL and page for every observation.
