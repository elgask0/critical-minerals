"""
Source-level validation of the active TeX compile path.
Produces all required audit CSVs and the final validation report.
(Overleaf handles PDF compilation.)
"""
import re
import csv
from pathlib import Path

DRAFT = Path("/Users/elgask0/REPOS/critical-minerals/05_draft")
OUT = Path("/Users/elgask0/REPOS/critical-minerals/03_data/output/tables")

MAIN = (DRAFT / "main.tex").read_text()

# active files in the compile path (transitive \input closure)
def active_files():
    seen = set()
    queue = ["main.tex"]
    while queue:
        fn = queue.pop()
        if fn in seen:
            continue
        seen.add(fn)
        p = DRAFT / fn
        if not p.exists():
            continue
        txt = p.read_text()
        for m in re.finditer(r"\\input\{([^}]+)\}", txt):
            queue.append(m.group(1) + ".tex")
    return seen

ACTIVE = active_files()
ACTIVE_FILES = sorted(ACTIVE)


def read(fn):
    return (DRAFT / fn).read_text()


# ---- Part 2: validate inputs resolve ----
def validate_inputs():
    rows = []
    for m in re.finditer(r"\\input\{([^}]+)\}", MAIN):
        target = m.group(1) + ".tex"
        exists = (DRAFT / target).exists()
        rows.append({"input_target": target, "exists": exists,
                     "active": target in ACTIVE})
    # figures
    for fn in ACTIVE:
        txt = read(fn)
        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", txt):
            fig = m.group(1)
            # resolve relative to DRAFT
            fpath = DRAFT / fig
            rows.append({"input_target": fig, "exists": fpath.exists(),
                         "active": True, "type": "figure"})
    # bib
    bib = DRAFT / "references.bib"
    rows.append({"input_target": "references.bib", "exists": bib.exists()
                 or bib.is_symlink(), "active": True, "type": "bib"})
    return rows


# ---- Part 3: bad string audit ----
BAD_STRINGS = [
    ("source-share", "source-share wording (use source-split)"),
    ("source share triple difference", "source share triple difference"),
    ("The wedge does not fade", "wedge-widens claim"),
    ("it widens", "wedge widens"),
    ("overall availability", "availability for outcome"),
    ("total availability", "availability for outcome"),
    ("not compression of total availability", "availability for outcome"),
    ("result is a mechanism", "mechanism overclaim"),
    ("coercive capacity is real", "coercive capacity is real"),
    ("routine trade-policy tool", "routine trade-policy tool"),
    ("Ga/Ge/In/V/Nb", "811292 label incomplete"),
    ("m6-to-m4 as the omitted", "wrong baseline claim"),
    ("m6 to m4 (base)", "wrong baseline in table"),
    ("China value share", "Table 3 column mislabel"),
    ("licensing_wedge_substitution", "orphan CSV citation"),
    ("licensing_wedge_regularity", "orphan CSV citation"),
    ("minimum exact product-assignment $p$ is $1/3$", "eurostat pooled p wrong"),
]

def bad_string_audit():
    rows = []
    for fn in ACTIVE_FILES:
        txt = read(fn)
        for i, line in enumerate(txt.split("\n"), 1):
            for pat, issue in BAD_STRINGS:
                # unescape for matching: LaTeX \_ -> _
                line_norm = line.replace("\\_", "_").replace("\\$", "$")
                if pat.lower() in line_norm.lower():
                    allowed = (pat == "total availability" and
                               "observed import value" in line)
                    rows.append({
                        "file": fn, "line": i,
                        "bad_string": pat,
                        "issue": issue,
                        "sentence": line.strip()[:160],
                        "allowed": "yes" if allowed else "no",
                    })
    return rows


# ---- Part 4: positive content checks ----
POSITIVE_CHECKS = [
    ("abstract", "main.tex", r"source-split triple difference", "abstract uses source-split"),
    ("abstract", "main.tex", r"robust to sample truncation", "abstract mentions robustness"),
    ("abstract", "main.tex", r"no aggregate negative effect", "abstract: Ga/Ge no aggregate negative effect"),
    ("abstract", "main.tex", r"leave-one-reporter", "abstract mentions LORO"),
    ("data", "main.tex", r"gallium and germanium with", "data section explains 811292 bundle"),
    ("data", "t3_coverage.tex", r"China cell share", "Table 3 relabelled"),
    ("data", "t3_coverage.tex", r"regularity_diagnostics_live", "Table 3 cites live source"),
    ("data", "t7_subcompression.tex", r"compression_diagnostics_live", "Table 6 cites live source"),
    ("data", "t2_products.tex", r"other-metals bundle", "811292 label fixed in t2"),
    ("theory", "main.tex", r"reduced-form", "theory says reduced-form"),
    ("theory", "main.tex", r"does not identify the wedge", "beta != W disclaimer"),
    ("strategy", "main.tex", r"source-split PPML triple difference", "strategy: source-split"),
    ("strategy", "main.tex", r"monthly bilateral import value", "DV is USD import value"),
    ("strategy", "main.tex", r"conditional diagnostics", "reporter p conditional"),
    ("strategy", "main.tex", r"0\.25|1/\(1\+3\)", "exact p floor explained"),
    ("results62", "main.tex", r"79\.6", "late-reporting truncation number"),
    ("results62", "main.tex", r"81\.7", "reported-only number"),
    ("results62", "main.tex", r"leave-one-reporter", "LORO mentioned"),
    ("results62", "main.tex", r"observed import value", "observed import value not availability"),
    ("results63", "main.tex", r"source-switching interpretation", "switching: supports interpretation, not 'mechanism'"),
    ("eurostat", "t8_eurostat.tex", r"81129289", "CN8 gallium code"),
    ("eurostat", "t8_eurostat.tex", r"81129295", "CN8 germanium code"),
    ("eurostat", "t8_eurostat.tex", r"81129281", "CN8 indium code"),
    ("eurostat", "t8_eurostat.tex", r"81129291", "CN8 vanadium code"),
    ("eurostat", "t8_eurostat.tex", r"1/6", "pooled exact p 1/6"),
    ("eurostat", "main.tex", r"1/6.*0\.167|0\.167.*1/6", "eurostat prose 1/6"),
    ("conclusion", "main.tex", r"recurrent instrument", "conclusion: recurrent, not routine"),
    ("table4", "t4_main_ddd.tex", r"Exact rank", "Table 4 has Exact rank p"),
    ("table4", "t4_main_ddd.tex", r"Other-metals bundle", "Table 4 811292 label"),
    ("table5", "t5_eventstudy.tex", r"m3 \(base\)", "Table 5 m3 baseline"),
    ("table5", "t5_eventstudy.tex", r"6\.7", "Table 5 shows m6-to-m4 coeff"),
    ("table6", "t7_subcompression.tex", r"Other-metals bundle", "Table 6 811292 label"),
    ("table7", "t6_switching.tex", r"source-split", "Table 7 source-split"),
    ("figures", "main.tex", r"fig_hs282580_eventstudy", "event-study figure included"),
    ("figures", "main.tex", r"fig_hs282580_source_trends", "source-trend figure included"),
    ("appendix", "main.tex", r"appendix_late_reporting", "late-reporting appendix"),
    ("appendix", "main.tex", r"appendix_donor_sensitivity", "donor appendix"),
    ("appendix", "main.tex", r"appendix_leave_one_reporter", "LORO appendix"),
    ("appendix", "main.tex", r"appendix_timing", "timing appendix"),
]

def positive_content_audit():
    rows = []
    for section, fn, pat, desc in POSITIVE_CHECKS:
        target = fn if fn == "main.tex" or fn.startswith("t") or fn.startswith("appendix") else fn
        if fn in ACTIVE:
            txt = read(fn).replace("\\_", "_")  # normalise LaTeX escaped underscores
        else:
            txt = ""
        found = bool(re.search(pat, txt, re.IGNORECASE))
        rows.append({"section": section, "file": fn, "check": desc,
                     "pattern": pat, "found": "yes" if found else "NO",
                     "status": "OK" if found else "MISSING"})
    return rows


# ---- Part 5: table value validation ----
TABLE4_EXPECTED = {
    "2504": (-30.4, "Suggestive"),
    "811292": (19.3, "No aggregate negative effect"),
    "282560": (17.5, "No aggregate negative effect"),
    "8110": (-86.8, "Consistent; pretrends fail"),
    "261710": (-98.9, "Descriptive only"),
    "282580": (-81.5, "Central result"),
}
TABLE6_282580 = {"China": -27.7, "ROW": 315.2, "Total": 135.7}
TABLE7_282580 = {"high_effect": -87.4, "high_p": "<0.001", "high_pt": 0.354,
                 "low_effect": 103.1, "low_p": 0.035, "low_pt": 0.161}

def validate_tables():
    rows = []
    t4 = read("t4_main_ddd.tex")
    for hs, (val, assess) in TABLE4_EXPECTED.items():
        # find the row
        m = re.search(rf"{hs}\s*&\s*(.*?)&.*?\$([+-]?[\d.]+)\$.*?&.*?(?:\$[^\$]+\$|<0\.001).*?&.*?(?:\$[^\$]+\$|<0\.001).*?&\s*(.*?)\s*\\\\", t4)
        if m:
            found_val = float(m.group(2)) if m.group(2) else None
            ok_v = found_val is not None and abs(abs(found_val) - abs(val)) < 0.15
            ok_a = assess.lower() in m.group(3).lower()
            rows.append({"table": "Table 4", "hs": hs, "expected_effect": val,
                         "found_effect": found_val, "effect_ok": ok_v,
                         "expected_assessment": assess,
                         "found_assessment": m.group(3).strip(),
                         "assessment_ok": ok_a})
        else:
            rows.append({"table": "Table 4", "hs": hs, "expected_effect": val,
                         "found_effect": "PARSE_FAIL", "effect_ok": False,
                         "expected_assessment": assess,
                         "found_assessment": "", "assessment_ok": False})
    # Table 6
    t6 = read("t7_subcompression.tex")
    m = re.search(r"282580.*?&.*?antimony.*?\$([+-]?[\d.]+)\$.*?&.*?\$([+-]?[\d.]+)\$.*?&.*?\$([+-]?[\d.]+)\$", t6, re.IGNORECASE)
    if m:
        rows.append({"table": "Table 6", "hs": "282580", "source": "China",
                     "expected": -27.7, "found": float(m.group(1)), "ok": abs(float(m.group(1))+27.7)<0.15})
        rows.append({"table": "Table 6", "hs": "282580", "source": "ROW",
                     "expected": 315.2, "found": float(m.group(2)), "ok": abs(float(m.group(2))-315.2)<0.15})
        rows.append({"table": "Table 6", "hs": "282580", "source": "Total",
                     "expected": 135.7, "found": float(m.group(3)), "ok": abs(float(m.group(3))-135.7)<0.15})
    # Table 7
    t7 = read("t6_switching.tex")
    m = re.search(r"282580.*?Antimony.*?\\\$(-?[\d.]+)\\\$.*?\\\$([^$]+)\\\$.*?\\\$0\.354\\\$.*?\\\$\\+?103\.1\\\$", t7) or \
        re.search(r"282580.*?(-87\.4).*?(<0\.001|0\.000).*?(0\.354).*?(\+?103\.1).*?(0\.035).*?(0\.161)", t7)
    rows.append({"table": "Table 7", "check": "282580 high-A effect -87.4",
                 "found": "-87.4" in t7, "ok": "-87.4" in t7})
    rows.append({"table": "Table 7", "check": "282580 high-A pretrend 0.354",
                 "found": "0.354" in t7, "ok": "0.354" in t7})
    return rows


# ---- LaTeX syntax: balanced environments and braces ----
def syntax_check():
    issues = []
    for fn in ACTIVE_FILES:
        txt = read(fn)
        # count begin/end pairs
        begins = re.findall(r"\\begin\{(\w+\*?)\}", txt)
        ends = re.findall(r"\\end\{(\w+\*?)\}", txt)
        from collections import Counter
        bc, ec = Counter(begins), Counter(ends)
        for env in set(list(bc) + list(ec)):
            if bc[env] != ec[env]:
                issues.append({"file": fn, "issue": f"unbalanced {env}: {bc[env]} begin vs {ec[env]} end"})
        # brace balance (rough)
        if txt.count("{") != txt.count("}"):
            issues.append({"file": fn, "issue": f"brace count: {txt.count('{')} open vs {txt.count('}')} close"})
    return issues


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = validate_inputs()
    bad = bad_string_audit()
    pos = positive_content_audit()
    tbl = validate_tables()
    syn = syntax_check()

    # write CSVs
    def wcsv(name, rows):
        if not rows:
            return
        all_keys = []
        for r in rows:
            for k in r.keys():
                if k not in all_keys:
                    all_keys.append(k)
        with open(OUT / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=all_keys)
            w.writeheader()
            w.writerows(rows)

    wcsv("final_tex_bad_string_audit.csv", bad)
    wcsv("final_positive_content_audit.csv", pos)
    wcsv("final_table_validation.csv", tbl)
    wcsv("final_figure_validation.csv",
         [{"figure": "hs282580_source_trends_indexed.pdf",
           "exists": (DRAFT/"figures"/"hs282580_source_trends_indexed.pdf").exists(),
           "included": "fig_hs282580_source_trends" in MAIN},
          {"figure": "hs282580_eventstudy.pdf",
           "exists": (DRAFT/"figures"/"hs282580_eventstudy.pdf").exists(),
           "included": "fig_hs282580_eventstudy" in MAIN}])

    # print summary
    print("=== ACTIVE FILES ===")
    for f in ACTIVE_FILES:
        print(f"  {f}")
    print(f"\n=== INPUTS ({len(inputs)}) ===")
    miss = [r for r in inputs if not r.get("exists", True)]
    print(f"  missing: {len(miss)}")
    for m in miss:
        print(f"    {m}")
    print(f"\n=== BAD STRINGS: {len(bad)} matches ===")
    for r in bad:
        print(f"  {r['file']}:{r['line']} [{r['bad_string']}] allowed={r['allowed']}")
    print(f"\n=== POSITIVE CONTENT: {sum(1 for r in pos if r['found']=='yes')}/{len(pos)} found ===")
    for r in pos:
        if r['found'] != 'yes':
            print(f"  MISSING: {r['check']} in {r['file']}")
    print(f"\n=== TABLES ===")
    for r in tbl:
        ok = r.get("effect_ok", r.get("ok", False))
        print(f"  {r.get('table')} {r.get('hs','')}: {'OK' if ok else 'CHECK'} {r}")
    print(f"\n=== SYNTAX: {len(syn)} issues ===")
    for s in syn:
        print(f"  {s}")


if __name__ == "__main__":
    main()
