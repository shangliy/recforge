"""Counts, the LaTeX audit table and the summary figure, generated from audit.csv so the paper and the data cannot
disagree.

usage: python3 summarize.py                   -> prints counts
       python3 summarize.py --tex FILE        -> also writes the table rows to FILE
       python3 summarize.py --paper PAPER.tex -> splices the rows between %BEGIN-AUDIT-ROWS and %END-AUDIT-ROWS
       python3 summarize.py --fig FILE        -> writes the TikZ summary figure
Coding conventions: README.md in this directory.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).with_name("audit.csv"))))
core = [r for r in rows if r["set"] == "core"]
# Strata: loops that keep or reject candidates offline, loops whose keep/reject decision is an online experiment,
# and loops that report only operational outcomes (c2 = na).
offline = [r for r in core if r["c2"] not in ("online", "na")]
online_sel = [r for r in core if r["c2"] == "online"]
ranking = [r for r in offline if r["c1"] in ("full", "sampled", "ranking-ns")]
with_ab = [r for r in core if r["online"] != "none"]

# Online-gate items not in audit.csv columns (evidence: audit/evidence-part1.md, review/sweep-2026-10-22.md):
# a correction for multiple testing across rounds (none applies one) and a fresh confirmation of the final candidate
# (Sortify re-tests its frozen round in a new seven-day experiment; PILOT designs a pre-registered confirmation but
# does not report it).
CONFIRM = {"cheng2026sortify": "Y", "pilot2026": "P"}


def count(rs, col):
    return dict(Counter(r[col] for r in rs).most_common())


def has_duration(r):
    return any(u in r["online"] for u in ("d", "wk", "mo"))


def has_sig(r):
    return "CI" in r["online"] or "sig" in r["online"]


if not any(a in sys.argv for a in ("--tex", "--paper", "--fig")):
    print(f"core {len(core)}: offline-selecting {len(offline)}, online-selecting {len(online_sel)}, "
          f"operational only {len(core) - len(offline) - len(online_sel)}; comparison {len(rows) - len(core)}")
    print(f"{'C1 metric (offline)':34s} {count(offline, 'c1')}")
    print(f"{'C1 metric (online-selecting)':34s} {count(online_sel, 'c1')}")
    print(f"{'C1 among ranking-metric loops':34s} {count(ranking, 'c1')} (n={len(ranking)})")
    for col, label in [("c2", "C2 selection"), ("c3", "C3 test once"), ("c4", "C4 repeats"), ("c5", "C5 held-out check"),
                       ("c6", "C6 null control"), ("c8", "C8 baselines"), ("c9", "C9 isolation design"),
                       ("incident", "C9 incident reported")]:
        print(f"{label + ' (offline)':34s} {count(offline, col)}")
    for col, label in [("c4", "C4 repeats"), ("c5", "C5 held-out check"), ("c6", "C6 null control"),
                       ("c9", "C9 isolation design"), ("incident", "C9 incident reported")]:
        print(f"{label + ' (online-selecting)':34s} {count(online_sel, col)}")
    for col, label in [("c8", "C8 baselines"), ("c9", "C9 isolation"), ("incident", "incident"), ("code", "code"),
                       ("llm_named", "LLM named")]:
        print(f"{label + ' (all core)':34s} {count(core, col)}")
    print(f"{'online A/B reported (core)':34s} {len(with_ab)}; duration {sum(map(has_duration, with_ab))}; "
          f"CI/significance {sum(map(has_sig, with_ab))}; correction 0; fresh confirmation {CONFIRM}")
    print(f"{'LLM tokens or cost (core)':34s} {sum(any(u in r['c7'] for u in ('$', 'tokens', 'RMB')) for r in core)}")
    # Kept edits (paper section "What the loops kept"): every "category:" tag in design.csv's kept_edits, for papers that
    # name concrete kept edits (Astar reports only case-study proposals and A-MLE only technique families).
    design = [r for r in csv.DictReader(open(Path(__file__).with_name("design.csv")))
              if r["key"] not in ("hu2026astar", "gao2026amle") and not r["kept_edits"].startswith("not reported")]
    tag = re.compile(r"\b(hparam|regularization|capacity|architecture(?:/capacity)?|feature|loss|data|strategy|other)\s*:")
    kept = {"config": Counter(), "code": Counter()}
    for r in design:
        kept["config" if r["object"] == "L1" else "code"].update(
            t.replace("architecture/capacity", "architecture") for t in tag.findall(r["kept_edits"]))
    print(f"{'kept edits':34s} {len(design)} papers, {sum(map(sum, (c.values() for c in kept.values())))} edits; "
          f"config-only ({sum(r['object'] == 'L1' for r in design)}): {dict(kept['config'])}; "
          f"code-level ({sum(r['object'] != 'L1' for r in design)}): {dict(kept['code'])}")
    named = sum(r["c2"] in ("val", "trainloss") for r in offline)
    once = sum(r["c3"] == "Y" for r in offline)
    print(f"{'bounds if every NS were Y':34s} C2 named: {named}..{named + sum(r['c2'] == 'NS' for r in offline)}; "
          f"C3 test once: {once}..{once + sum(r['c3'] == 'NS' for r in offline)}")

SHOW = {"c1": {"sampled": "Sampled", "ranking-ns": "Rank?", "auc": "AUC", "online": "A/B", "none": "?", "full": "Full",
               "other": "other"},
        "c2": {"val": "val", "NS": "\\ns", "online": "A/B", "test": "test", "trainloss": "loss"}}


def cell(col, v):
    v = SHOW.get(col, {}).get(v, v)
    return {"Y": "\\yes", "N": "\\no", "NS": "\\ns", "P": "\\pa", "na": "\\na"}.get(v, v)


if "--tex" in sys.argv or "--paper" in sys.argv:
    out = []
    for r in rows:
        if r["set"] == "comparison" and r is rows[[x["set"] for x in rows].index("comparison")]:
            out.append("\\midrule\n\\multicolumn{12}{@{}l}{\\emph{Comparison points outside recommendation}} \\\\")
        name = r["system"].replace("&", "\\&")
        cells = [cell(c, r[c]) for c in ("c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9")]
        cells[6] = {"untuned": "\\no", "tuned": "\\yes", "production": "prod.", "published": "pub.",
                    "seed": "seed", "NS": "\\ns", "P": "\\pa"}.get(r["c8"], r["c8"])
        if r["incident"] == "Y":
            cells[7] += "\\textsuperscript{G}"
        online = "\\no" if r["online"] == "none" else "\\yes"
        code = {"Y": "\\yes", "N": "\\no", "promised": "later"}[r["code"]]
        out.append(f"{name}~\\cite{{{r['key']}}} & {r['level']} & " + " & ".join(cells) + f" & {online} & {code} \\\\")
    rows_tex = "\n".join(out) + "\n"
    if "--tex" in sys.argv:
        Path(sys.argv[sys.argv.index("--tex") + 1]).write_text(rows_tex)
    if "--paper" in sys.argv:  # splice the rows into paper.tex (\input inside a tabular breaks \midrule)
        paper = Path(sys.argv[sys.argv.index("--paper") + 1])
        text = paper.read_text()
        a, b = text.index("%BEGIN-AUDIT-ROWS\n") + len("%BEGIN-AUDIT-ROWS\n"), text.index("%END-AUDIT-ROWS")
        paper.write_text(text[:a] + rows_tex + text[b:])

# Figure: share of systems meeting each criterion, in two panels. Each criterion's codes map onto five outcomes.
OUTCOMES = [("meets", "cOk"), ("partial", "cPart"), ("no", "cBad"), ("not stated", "cNS"), ("n/a", "white")]
YPN = {"Y": "meets", "P": "partial", "N": "no", "NS": "not stated", "na": "n/a"}
PANELS = [
    (f"Offline-selecting loops (n={len(offline)})", [  # (label, systems, value function, code -> outcome)
        ("C1 full ranking", ranking, lambda r: r["c1"], {"full": "meets", "sampled": "no", "ranking-ns": "not stated"}),
        ("C2 split named", offline, lambda r: r["c2"], {"val": "meets", "trainloss": "partial", "test": "no",
                                                        "NS": "not stated"}),
        ("C3 test once", offline, lambda r: r["c3"], YPN),
        ("C4 repeats + spread", offline, lambda r: r["c4"], YPN),
        ("C5 held-out check", offline, lambda r: r["c5"], YPN),
        ("C6 non-LLM null", offline, lambda r: r["c6"], YPN),
        ("C9 isolation", offline, lambda r: r["c9"], YPN),
    ]),
    (f"Loops with online experiments (n={len(with_ab)})", [
        ("duration stated", with_ab, lambda r: "Y" if has_duration(r) else "N", YPN),
        ("CI or significance", with_ab, lambda r: "Y" if has_sig(r) else "N", YPN),
        ("correction across rounds", with_ab, lambda r: "N", YPN),
        ("fresh confirmation", with_ab, lambda r: CONFIRM.get(r["key"], "N"), YPN),
    ]),
]

if "--fig" in sys.argv:
    W = 46.0  # bar length in mm for 100%
    out = ["% generated by audit/summarize.py --fig; do not edit", "\\begin{tikzpicture}[font=\\sffamily\\scriptsize]"]
    y = 0.0
    for title, bars in PANELS:
        out.append(f"\\node[anchor=west, font=\\sffamily\\scriptsize\\bfseries] at (-33mm,{y}mm) {{{title}}};")
        y -= 5.2
        for label, rs, value, m in bars:
            out.append(f"\\node[anchor=east] at (-1mm,{y:.1f}mm) {{{label} \\textcolor{{gray}}{{({len(rs)})}}}};")
            tally = Counter(m[value(r)] for r in rs)
            x = 0.0
            for name, colour in OUTCOMES:
                k = tally.get(name, 0)
                if not k:
                    continue
                w = W * k / len(rs)
                out.append(f"\\draw[fill={colour}, draw=black!40] ({x:.2f}mm,{y - 1.9:.1f}mm) rectangle "
                           f"({x + w:.2f}mm,{y + 1.9:.1f}mm);")
                if w > 1.2:
                    out.append(f"\\node at ({x + w / 2:.2f}mm,{y:.1f}mm) {{{k}}};")
                x += w
            y -= 5.2
        y -= 1.5
    x = -30.0
    for name, colour in OUTCOMES:
        out.append(f"\\draw[fill={colour}, draw=black!40] ({x}mm,{y - 1.4:.1f}mm) rectangle ({x + 2.8}mm,{y + 1.4:.1f}mm);")
        out.append(f"\\node[anchor=west] at ({x + 3.2}mm,{y:.1f}mm) {{{name}}};")
        x += 3.2 + 1.5 + 1.25 * len(name)
    out.append("\\end{tikzpicture}")
    Path(sys.argv[sys.argv.index("--fig") + 1]).write_text("\n".join(out) + "\n")
