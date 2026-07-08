"""
Build the language/overclaim patch (Part 12) and the HS 811292 label patch
(Part 11).

Outputs:
  output/tables/term_language_patch_table.csv
  05_draft/language_patch.diff
  05_draft/main_corrected.tex
  05_draft/product_label_replacement_patch.diff
"""
from pathlib import Path
import csv
import difflib

REPO = Path(__file__).resolve().parent.parent
DRAFT = REPO / "05_draft"
OUT = REPO / "03_data" / "output" / "tables"

MAIN = (DRAFT / "main.tex").read_text()

# (must_fix, file, original_substring, replacement_substring, problem)
REPLACEMENTS = [
    (True, "main.tex", "source-share triple difference", "source-split triple difference",
     "dependent variable is import value (USD), not a share"),
    (True, "main.tex", "source-share triple-difference", "source-split triple-difference",
     "dependent variable is import value (USD), not a share"),
    (True, "main.tex", "Using a source-share", "Using a source-split",
     "source-share terminology"),
    (True, "main.tex", "PPML source-share triple difference", "PPML source-split triple difference",
     "section heading: source-share -> source-split"),
    (True, "main.tex", "Product-level source-share effects", "Product-level source-split effects",
     "subsection heading"),
    (True, "main.tex", "static source-share triple difference", "static source-split triple difference",
     "source-share -> source-split"),
    (True, "main.tex", "The wedge does not fade; it widens.",
     "The relative China-source decline does not fade; it deepens.",
     "beta is not the wedge; calling the coefficient 'the wedge' overclaims"),
    (True, "main.tex", "not with a collapse in overall availability.",
     "not with a collapse in total observed import value.",
     "data are trade values, not physical availability"),
    (True, "main.tex", "not compression of total availability.",
     "not compression of total observed import value.",
     "data are trade values, not physical availability"),
    (True, "main.tex",
     "China's coercive capacity is real but not automatic, and a binding",
     "China-source supply leverage is visible in some product-source margins, but not uniformly; a binding",
     "violates project rule 'avoid coercive capacity is real'"),
    (True, "main.tex",
     "now a routine trade-policy tool, that its effect must be measured",
     "a recurrent instrument in China's critical-mineral trade policy, that its effect must be measured",
     "violates project rule 'avoid routine trade-policy tool'"),
    # China-source share -> relative China-source import value (only where beta is meant)
    (True, "main.tex",
     "China-source share of the treated product falls. In the PPML triple difference of",
     "relative China-source import value of the treated product falls. In the PPML triple difference of",
     "beta measures relative import value, not a share"),
    (True, "main.tex",
     "The implied change in the China-source share of product $k$ is",
     "The implied relative change in China-source import value of product $k$ is",
     "beta measures relative import value, not a share"),
    (True, "main.tex",
     "\\text{percent change in China-source share}",
     "\\text{percent change in relative China-source import value}",
     "beta measures relative import value, not a share"),
    (True, "main.tex",
     "the \\emph{combined} effect of the license on the China-source share. It does not",
     "the \\emph{combined} effect of the license on relative China-source import value. It does not",
     "beta measures relative import value, not a share"),
    (True, "main.tex",
     "relative fall in the China-source share (Equation~\\ref{eq:magnitude}). The raw",
     "relative fall in China-source import value (Equation~\\ref{eq:magnitude}). The raw",
     "beta measures relative import value, not a share"),
    (True, "main.tex",
     "effect of the license on the China-source share, not the denial probability or",
     "effect of the license on relative China-source import value, not the denial probability or",
     "beta measures relative import value, not a share"),
    # NOT must-fix (wedge-component description in theory, legitimate)
    (False, "main.tex",
     "risk, paperwork, uncertainty, reduced availability---in a single latent wedge",
     "risk, paperwork, uncertainty, reduced availability---in a single latent wedge",
     "keep: describes latent wedge components, not the regression outcome"),
]


def build_patch_table():
    lines = MAIN.split("\n")
    rows = []
    for must_fix, fname, old, new, problem in REPLACEMENTS:
        hits = [i + 1 for i, ln in enumerate(lines) if old in ln]
        for ln_no in hits:
            rows.append({
                "file": fname,
                "line": ln_no,
                "original": old,
                "replacement": new,
                "problem": problem,
                "must_fix": "yes" if must_fix else "no",
            })
    with open(OUT / "term_language_patch_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "line", "original",
                                          "replacement", "problem", "must_fix"])
        w.writeheader()
        w.writerows(rows)
    print(f"language patch table: {len(rows)} entries "
          f"({sum(1 for r in rows if r['must_fix']=='yes')} must-fix)")
    return rows


def build_corrected_main():
    text = MAIN
    for must_fix, fname, old, new, _ in REPLACEMENTS:
        if must_fix and old in text:
            text = text.replace(old, new)
    (DRAFT / "main_corrected.tex").write_text(text)
    # diff
    orig_lines = MAIN.splitlines(keepends=True)
    new_lines = text.splitlines(keepends=True)
    diff = difflib.unified_diff(orig_lines, new_lines,
                                fromfile="05_draft/main.tex",
                                tofile="05_draft/main_corrected.tex",
                                n=2)
    (DRAFT / "language_patch.diff").write_text("".join(diff))
    n_changes = sum(1 for l in diff_lines_count() if l)
    print(f"wrote main_corrected.tex and language_patch.diff")


def diff_lines_count():
    # helper to count changed hunks
    text = (DRAFT / "language_patch.diff").read_text()
    return [l for l in text.splitlines() if l.startswith("+") or l.startswith("-")]


def build_label_patch():
    """HS 811292 label: 'Ga/Ge/In/V/Nb' -> 'unwrought other-metals bundle'."""
    targets = ["main.tex", "main_corrected.tex", "t2_products.tex",
               "t4_main_ddd.tex", "t6_switching.tex", "t7_subcompression.tex",
               "t8_eurostat.tex"]
    label_old_variants = [
        "Ga/Ge/In/V/Nb bundle",
        "Ga/Ge/In/V/Nb unwrought bundle",
    ]
    label_new = "Unwrought other-metals bundle (incl. Ga, Ge, In, V, Nb, and others)"
    diff_parts = []
    for fname in targets:
        path = DRAFT / fname
        if not path.exists():
            continue
        orig = path.read_text()
        new = orig
        for v in label_old_variants:
            new = new.replace(v, label_new)
        if new != orig:
            diff = difflib.unified_diff(
                orig.splitlines(keepends=True),
                new.splitlines(keepends=True),
                fromfile=f"05_draft/{fname}", tofile=f"05_draft/{fname} (corrected)", n=1)
            diff_parts.append("".join(diff))
    (DRAFT / "product_label_replacement_patch.diff").write_text("\n".join(diff_parts))
    print(f"wrote product_label_replacement_patch.diff "
          f"({len(diff_parts)} files touched)")


if __name__ == "__main__":
    build_patch_table()
    build_corrected_main()
    build_label_patch()
