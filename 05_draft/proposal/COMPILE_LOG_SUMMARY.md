# Compile Log Summary

## Compiler

- Compiler: Tectonic 0.16.9
- Command: `tectonic --keep-logs --keep-intermediates main.tex`
- Working directory: `05_draft/proposal/`
- Overleaf copy regenerated with: `python make_overleaf_copy.py`

## Result

- PDF compiled successfully.
- Output PDF: `05_draft/proposal/main.pdf`
- Final PDF metadata: 36 pages, approximately 490 KiB.
- The compiled `main.pdf` is intentionally retained at the user's request.

## Warnings

- Font reproducibility warnings: Tectonic accessed local macOS Times New Roman and STFangsong font paths. This is expected for the local ZJU font source; `main_overleaf.tex` was regenerated for Overleaf.
- Nonfatal underfull text warnings: `main.tex:566` near the price diagnostic paragraph. No overfull table or figure warnings remain.
- `Object @page.1 already defined` from the PDF backend; PDF was still written successfully.

## Missing References, Citations, Or Figures

- No fatal missing figure errors.
- No unresolved citation errors appeared in the Tectonic output.
- No unresolved cross reference errors appeared in the Tectonic output after reruns.
- No old HS 282580 event study figure is referenced.
- No Figure 3-2 coefficient plot is referenced.

## Visual QA

- Rendered and inspected the page containing the revised Figure 3-1 at 220 dpi. The final figure uses same-size inner boxes within groups, an eight-box design grid, side boxes, and clean arrow lanes with no crossing arrows or clipped labels. A final spacing pass reduced the group-title size and lowered the inner rows so the titles no longer crowd the boxes.
- Rendered and inspected pages containing Tables 3-1, 3-2, and 3-3. The timing table no longer produces overfull boxes.
- Rendered and inspected pages containing Tables 3-4, 3-5, and 3-6. The result tables use coefficient or percent effect entries with \(t\)-statistics in parentheses and no p values in square brackets. Table notes now state reported \(p\)-values and the verified uncertainty treatment: reporter-code clustered standard errors for PPML tables and HAC(3) reported standard errors for price diagnostics.
- Confirmed that no empirical event study figure is included in the main proposal.
