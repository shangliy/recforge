"""Counts, the LaTeX audit table and the summary figure, generated from audit.csv so the paper and the data cannot
disagree.

usage: python3 summarize.py                   -> prints counts
       python3 summarize.py --tex FILE        -> also writes the table rows to FILE
       python3 summarize.py --paper PAPER.tex -> splices the rows between %BEGIN-AUDIT-ROWS and %END-AUDIT-ROWS
       python3 summarize.py --fig FILE        -> writes the TikZ summary figure
       python3 summarize.py --tables DIR      -> writes crosstab.tex, pilot.tex and sensitivity.tex (taxonomy x outcomes; retrospective proxy check of the checklist)
       python3 summarize.py --headline        -> prints the value columns of the paper's headline table (Table 7)
Coding conventions: README.md in this directory.
"""
import csv
import re
import sys
sys.dont_write_bytecode = True  # leave no __pycache__ in the released folder
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

# Online-gate items (ab_* columns; evidence: evidence-online-gates.md). Loops that select on online experiments are
# checked for a correction across rounds and a fresh confirmation; loops that A/B-test one offline-selected candidate
# are confirmations by construction.
ab_select = [r for r in with_ab if r["ab_role"] in ("select", "both")]


def count(rs, col):
    return dict(Counter(r[col] for r in rs).most_common())


def has_duration(r):
    return r["ab_duration"] == "Y"


def has_sig(r):
    return r["ab_ci"] == "Y"


if not any(a in sys.argv for a in ("--tex", "--paper", "--fig", "--tables", "--headline")):
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
          f"CI/significance {sum(map(has_sig, with_ab))}; online-selecting {len(ab_select)}: "
          f"correction {count(ab_select, 'ab_correction')}, fresh confirmation {count(ab_select, 'ab_confirm')}")
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
        "c2": {"val": "val", "NS": "\\ns", "online": "A/B", "test": "rep.", "trainloss": "loss"}}


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
        if r in offline and r["c5"] == "P" and r["online"] != "none":
            cells[4] = "\\po"  # partial C5 resting only on an online confirmation (drawn apart in the figure too)
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
OUTCOMES = [("meets", "cOk"), ("partial", "cPart"), ("A/B only (post hoc)", "cPart!35"), ("no", "cBad"), ("not stated", "cNS"), ("n/a", "white")]
YPN = {"Y": "meets", "P": "partial", "N": "no", "NS": "not stated", "na": "n/a"}
PANELS = [
    (f"Offline-selecting loops (n={len(offline)})", [  # (label, systems, value function, code -> outcome)
        ("C1 full ranking", ranking, lambda r: r["c1"], {"full": "meets", "sampled": "no", "ranking-ns": "not stated"}),
        ("C2 split named", offline, lambda r: r["c2"], {"val": "meets", "trainloss": "partial", "test": "no",
                                                        "NS": "not stated"}),
        ("C3 test once", offline, lambda r: r["c3"], YPN),
        ("C4 repeats + spread", offline, lambda r: r["c4"], YPN),
        # a partial C5 whose only held-out evidence is an online test of the kept candidate is drawn apart
        ("C5 held-out check", offline, lambda r: "PA" if r["c5"] == "P" and r["online"] != "none" else r["c5"],
         {**YPN, "PA": "A/B only (post hoc)"}),
        ("C6 non-LLM null", offline, lambda r: r["c6"], YPN),
        ("C9 isolation", offline, lambda r: r["c9"], YPN),
    ]),
    (f"Loops with online experiments (n={len(with_ab)}; one coder)", [
        ("duration stated", with_ab, lambda r: "Y" if has_duration(r) else "N", YPN),
        ("CI or significance", with_ab, lambda r: "Y" if has_sig(r) else "N", YPN),
        ("correction (online-selecting)", ab_select, lambda r: r["ab_correction"], YPN),
        ("fresh confirmation (same)", ab_select, lambda r: r["ab_confirm"], YPN),
    ]),
]

LOW_AGREEMENT = {"C5", "C6"}  # pre-reconciliation kappa below 0.6 over the offline stratum

if "--fig" in sys.argv:
    W = 46.0  # bar length in mm for 100%
    out = ["% generated by audit/summarize.py --fig; do not edit", "\\begin{tikzpicture}[font=\\sffamily\\scriptsize]"]
    y = 0.0
    for title, bars in PANELS:
        out.append(f"\\node[anchor=west, font=\\sffamily\\scriptsize\\bfseries] at (-33mm,{y}mm) {{{title}}};")
        y -= 5.2
        for label, rs, value, m in bars:
            weak = label.split()[0] in LOW_AGREEMENT  # low-agreement bars are drawn faded and dashed
            mark = "$^\\dagger$" if weak else ""
            out.append(f"\\node[anchor=east] at (-1mm,{y:.1f}mm) {{{label}{mark} \\textcolor{{gray}}{{({len(rs)})}}}};")
            tally = Counter(m[value(r)] for r in rs)
            x = 0.0
            for name, colour in OUTCOMES:
                k = tally.get(name, 0)
                if not k:
                    continue
                w = W * k / len(rs)
                style = f"fill={colour}, draw=black!40" + (", fill opacity=0.5, densely dashed" if weak else "")
                out.append(f"\\draw[{style}] ({x:.2f}mm,{y - 1.9:.1f}mm) rectangle "
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

# Tables relating the taxonomy to the audit outcomes (tab:crosstab) and piloting the minimum tier of the reporting
# checklist by proxy on the audit coding (tab:pilot; the paper calls it a retrospective proxy check). Both are written as complete table environments.
proposer = {r["key"]: r["proposer"] for r in csv.DictReader(open(Path(__file__).with_name("design.csv")))}
# design.csv repeats the isolation code of audit.csv's c9 for reading convenience; audit.csv is authoritative
AUDIT = {r["key"]: r for r in rows}
for r in csv.DictReader(open(Path(__file__).with_name("design.csv"))):
    if r["key"] in AUDIT and r["c9_isolation"] != AUDIT[r["key"]]["c9"]:
        sys.exit(f"design.csv c9_isolation of {r['key']} differs from audit.csv")
PROPOSER = {"llm": "LLM", "llm+space": "hybrid", "learned": "learned", "learned+llm": "learned"}


def frac(rs, test, among=None):
    base = [r for r in rs if among is None or among(r)]
    return f"{sum(map(test, base))}/{len(base)}" if base else "--"


GROUPS = [("All core", lambda r: True)] + \
         [(f"{p[0].upper() + p[1:]} proposer", (lambda p: lambda r: PROPOSER[proposer[r['key']]] == p)(p)) for p in ("LLM", "hybrid", "learned")] + \
         [("Meta-evolving", lambda r: r["meta"] == "Y"), ("Not meta", lambda r: r["meta"] == "N"),
          ("Config only (L1)", lambda r: r["level"] == "L1"),
          ("Code or model (L2+)", lambda r: r["level"] != "L1")]
is_off = lambda r: r in offline


def crosstab():
    out = ["% generated by audit/summarize.py --tables; do not edit",
           "\\begin{table}[t]",
           "\\caption{Taxonomy against audit outcomes (core loops; groups as small as $n=2$ and $n=6$ are listed for completeness, and their shares should not be compared). Offline: share of loops that select offline; the next two "
           "columns, a named validation split (Val) and test used once (Test), are among those loops. Null: a non-LLM null run in full or in part (C6 \\yes{} or \\pa); Isol.: C9 "
           "\\yes{} or \\pa; Incid.: a gaming or leakage incident reported. Cells are counts over the group, so small groups "
           "describe, not estimate.}\\label{tab:crosstab}",
           "\\footnotesize\\setlength{\\tabcolsep}{2.5pt}",
           "\\begin{tabular}{@{}lrrrrrr@{}}", "\\toprule",
           "Group & Offline & Val & Test & Null (Y/P) & Isol. (Y/P) & Incid. \\\\", "\\midrule"]
    for label, g in GROUPS:
        rs = [r for r in core if g(r)]
        out.append(f"{label} ($n={len(rs)}$) & {frac(rs, is_off)} & "
                   f"{frac(rs, lambda r: r['c2'] in ('val', 'trainloss'), is_off)} & "
                   f"{frac(rs, lambda r: r['c3'] == 'Y', is_off)} & {frac(rs, lambda r: r['c6'] in ('Y', 'P'))} & "
                   f"{frac(rs, lambda r: r['c9'] in ('Y', 'P'))} & {frac(rs, lambda r: r['incident'] == 'Y')} \\\\")
        if label == "All core":
            out.append("\\midrule")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out) + "\n"


# Pilot of the checklist: for each item, the audit code that stands in for it, the tier that code measures, the loops it
# applies to, and the test. The coding records whether a practice was reported, not every field an item asks for, so a
# minimum-tier count is an upper bound; where the minimum is not coded we show the recommended practice instead.
offline_metric = [r for r in core if r["c1"] in ("full", "sampled", "ranking-ns", "auc")]
PILOT = [
    # RecEvolve counts as in F1 (sampled, stated in its batch-size incident); the stricter reading gives one fewer
    ("R1 Metric", "min.", "candidate set or AUC stated", offline_metric,
     lambda r: r["c1"] != "ranking-ns"),
    ("R2 Selection", "min.", "selection data stated", [r for r in core if r["c2"] != "na"], lambda r: r["c2"] != "NS"),
    ("R3 Test once", "rec.", "test used once (C3)", [r for r in offline if r["c3"] != "na"], lambda r: r["c3"] == "Y"),
    ("R4 Sessions", "rec.", "repeats with spread (C4)", core, lambda r: r["c4"] == "Y"),
    ("R5 Null control", "rec.", "any equal-budget non-LLM search (C6)", core, lambda r: r["c6"] == "Y"),
    # the strict reading is a judgement on top of C6 (F6), so it is listed by name rather than coded
    ("R5 Null control", "rec.", "same space, total budget incl. LLM cost (F6)", core, lambda r: r["key"] == "cao2026virtualmle"),
    ("R6 Budget", "min.", "some budget stated (C7)", core, lambda r: r["c7"] != "NS"),
    ("R7 Baselines", "min.", "baseline tuning described (C8)", core, lambda r: r["c8"] in ("tuned", "P")),
    ("R8 Access", "min.", "access design stated (C9)", core, lambda r: r["c9"] != "NS"),
    ("R9 Online gates", "min.", "duration and CI or sig. stated", with_ab, lambda r: has_duration(r) and has_sig(r)),
    ("R9 Online gates", "rec.", "correction and confirmation", ab_select,
     lambda r: r["ab_correction"] == "Y" and r["ab_confirm"] == "Y"),
]


def pilot():
    out = ["% generated by audit/summarize.py --tables; do not edit",
           "\\begin{table}[tp]",
           "\\caption{Retrospective proxy mapping of the proposed reporting checklist on the 27 core papers, read off the audit "
           "coding by the authors; it is not an application of the checklist by independent raters, and the last column "
           "is not a compliance rate: most proxies are lenient (strict readings: R1 10 of 15, without RecEvolve, whose candidate set is stated only in its incident description; R5 1 of 27, R9 2 of 19; "
           f"R2 is met by {sum(r['c2'] != 'NS' for r in offline)} of the {len(offline)} offline-selecting loops). Each item is "
           "approximated by the audit code shown; rows marked rec. proxy the recommended tier only, and the minimum tier of R3--R5 is not coded, so no row measures minimum-tier compliance. The notes below give each item's tier, leniency and denominator.}\\label{tab:pilot}",
           "\\footnotesize\\setlength{\\tabcolsep}{3pt}",
           "\\begin{tabular}{@{}lllr@{}}", "\\toprule", "Item & Tier & Proxy & Lenient proxy satisfied (not compliance) \\\\", "\\midrule"]
    note = ("\\emph{min.}: the code checks part of the minimum tier, so the count is an upper bound on papers meeting the "
           "minimum (except R7, Appendix~\\ref{app:exemplars}). \\emph{rec.}: the minimum (for R3, R4 and R5, stating "
           "what was done) is not coded, so the count is not a bound on the minimum: it counts papers that already follow "
           "the recommended practice. The R1, R2, R6 and R8 proxies are lenient, R3's reads C3 only, although Table~\\ref{tab:checklist} also "
           "maps R3 to C5, and R5's counts any equal-budget non-LLM search. Denominators: R1, core loops whose headline is a "
           "ranking metric or AUC; R2, all except the operational loop; R3, the 16 offline-selecting loops (including AutoLR, "
           "which selects offline but headlines only online lifts); R9, loops with an online experiment (min.) or that "
           "select online (rec.); otherwise all 27. Appendix~\\ref{app:exemplars} details each proxy's leniency.")
    for item, tier, proxy, rs, test in PILOT:
        out.append(f"{item} & {tier} & {proxy} & {sum(map(test, rs))}/{len(rs)} \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\par\\smallskip\\parbox{\\linewidth}{\\scriptsize " + note + "}",
            "\\end{table}"]
    return "\n".join(out) + "\n"


def sensitivity():
    """Headline counts under each coding of the scored criteria: the first coder's sheet before reconciliation, the
    second coder's returned sheets, and the released coding."""
    sc = Path(__file__).with_name("second-coder")
    keys = {r["key"] for r in core}
    first = [r for r in csv.DictReader(open(sc / "coder1-prereconciliation.csv")) if r["key"] in keys]
    second = [{k: (v or "").strip() for k, v in r.items()} for f in ("coder2.csv", "coder2-part2.csv")
              for r in csv.DictReader(open(sc / "returned" / f)) if r["key"] in keys and (r.get("c1") or "").strip()]
    assert len(first) == len(second) == len(core)

    def cells(rs):
        off = [r for r in rs if r["c2"] not in ("online", "na")]
        n = lambda c, *v: sum(r[c] in v for r in off)
        tl = n("c2", "trainloss")
        return [str(len(off)),
                f"{n('c1', 'full')} / {n('c1', 'sampled')} / {n('c1', 'ranking-ns')}",
                str(n("c1", "auc")),
                f"{n('c2', 'val')}{'+' + str(tl) if tl else ''} / {n('c2', 'test')} / {n('c2', 'NS')}",
                f"{n('c3', 'Y')} / {n('c3', 'NS')}",
                str(n("c4", "Y")),
                f"{n('c5', 'Y')} / {n('c5', 'P')}",
                f"{n('c6', 'Y')} / {n('c6', 'P')} / {n('c6', 'N')}",
                str(sum(r["incident"].strip().upper() == "Y" for r in rs))]
    labels = ["Offline-selecting loops", "F1 ranking: full / sampled / not stated", "F1 AUC",
              "F2 selection: validation / reported data / not stated", "F3 test-once: yes / not stated",
              "F4 spread over sessions: yes", "F5 held-out check: yes / partial", "F6 null: yes / partial / none",
              "F7 incidents (all 27)"]
    cols = [cells(first), cells(second), cells(core)]
    out = ["% generated by audit/summarize.py --tables; do not edit",
           "\\begin{table}[tp]",
           "\\caption{Headline counts of the scored criteria under each coding: the first coder's sheet before "
           "reconciliation, the second coder's returned sheets, and the released coding. F1--F6 are over each coding's own "
           "offline-selecting loops. The first coding predates the rules written during reconciliation (for example, "
           "that an online test of an offline-selected candidate is partial transfer evidence, which accounts for most of "
           "the change in F5), so its column differs partly by rule, not only by reading. ``+1'' in F2: one loop the "
           "first coding coded as selecting on training loss. Computed by \\texttt{summarize.py} from the released "
           "sheets.}\\label{tab:sensitivity}",
           "\\footnotesize\\setlength{\\tabcolsep}{4pt}",
           "\\begin{tabular}{@{}lccc@{}}", "\\toprule", "Count & First coder & Second coder & Released \\\\", "\\midrule"]
    for i, lab in enumerate(labels):
        out.append(f"{lab} & {cols[0][i]} & {cols[1][i]} & {cols[2][i]} \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out) + "\n"


if "--tables" in sys.argv:
    d = Path(sys.argv[sys.argv.index("--tables") + 1])
    d.mkdir(parents=True, exist_ok=True)
    (d / "crosstab.tex").write_text(crosstab())
    (d / "pilot.tex").write_text(pilot())
    (d / "sensitivity.tex").write_text(sensitivity())


def headline():
    """The 'Value (range)' and 'With uncoded' columns of the headline table. The two F7 qualifiers, F6's strict
    reading and F9's strict significance count are judgements on top of the coded columns, so they are listed by name (as for R5 in the proxy check); the
    F8 range is read from f8-lifts.md; the agreement column comes from second-coder/kappa.py and online_agreement.py."""
    n, m, extra = len(offline), len(online_sel), 6  # six in-scope loops not yet coded

    def k(rs, col, v):
        return sum(r[col] == v for r in rs)

    ns2 = [r for r in offline if r["c2"] == "NS"]
    c3y, c3ns = k(offline, "c3", "Y"), k(offline, "c3", "NS")
    c4y, c5y = k(offline, "c4", "Y"), k(offline, "c5", "Y")
    inc = [r for r in core if r["incident"] == "Y"]
    not_by_agent = {"fu2026evopilot"}  # its paper does not attribute the shortcut to the agent (F7)
    catcher_stated = {"pan2026recevolve", "chen2026rankevolve", "chandran2026autoresearch"}  # F7, evidence files
    same_space = {"cao2026virtualmle", "liu2026nova"}  # the null searches the loop's own space (F6)
    strict_null = {"cao2026virtualmle"}  # same space and matched total budget, LLM cost included (F6, R5)
    named_test = {"wang2026selfevolving", "mu2026evorec", "hu2026astar"}  # report an interval or a named test (F9)
    ab = [r for r in core if r["ab_ci"] != "na"]
    lifts = []
    for line in Path(__file__).with_name("f8-lifts.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 3 and cells[2] == "yes":
            lifts.append(float(re.search(r"\+([0-9.]+)", cells[1]).group(1)))
    out = [
        ("F2 not stating selection data", f"{len(ns2)} of {n} ({sum(r['online'] != 'none' for r in ns2)} confirm online; "
         f"{k(offline, 'c2', 'test')} select on reported data, {k(offline, 'c2', 'val')} on validation; "
         f"{k(offline, 'c2', 'test')}-{k(offline, 'c2', 'test') + len(ns2)} may select on reported data)",
         f"{len(ns2)}-{len(ns2) + extra} of {n}-{n + extra}"),
        ("F3 test-once", f"{c3y} of {n} ({c3y}-{c3y + c3ns})", f"{c3y}-{c3y + extra} of {n}-{n + extra}"),  # reported count only (footnote e); not-stated range not added
        ("F4 spread over sessions", f"{c4y} of {n} ({k(offline, 'c4', 'P')} partial)", f"{c4y}-{c4y + extra} of {n}-{n + extra}"),
        ("F5 same-task check", f"{c5y} of {n} ({sum(r['c5'] == 'P' and r['online'] == 'none' for r in offline)} partial; "
         f"{sum(r['c5'] == 'P' and r['online'] != 'none' for r in offline)} online confirmations only)", f"{c5y}-{c5y + extra} of {n}-{n + extra}"),
        ("F6 equal-budget null", f"{k(offline, 'c6', 'Y')} of {n} ({len(same_space)} over the same space, {len(strict_null)} also at a total budget incl. LLM cost, R5)",
         f"{k(offline, 'c6', 'Y')}-{k(offline, 'c6', 'Y') + extra} of {n}-{n + extra}"),
        ("F7 incidents", f"{len(inc)} of {len(core)} ({sum(r['key'] not in not_by_agent for r in inc)} by the agent; "
         f"{sum(r['key'] in catcher_stated for r in inc)} say what caught it)",
         f"{len(inc)}-{len(inc) + extra} of {len(core) + extra}"),
        ("F8 broad-metric lifts", f"+{min(lifts)}% to +{max(lifts)}% ({len(lifts)} loops)", "not bounded"),
        ("F9 correction across rounds", f"{k(ab_select, 'ab_correction', 'Y')} of {m} ({k(ab_select, 'ab_correction', 'P')} partial)",
         f"{k(ab_select, 'ab_correction', 'Y')}-{k(ab_select, 'ab_correction', 'Y') + extra} of {m}-{m + extra}"),
        ("F9 fresh confirmation", f"{k(ab_select, 'ab_confirm', 'Y')} of {m} ({k(ab_select, 'ab_confirm', 'P')} partial)",
         f"{k(ab_select, 'ab_confirm', 'Y')}-{k(ab_select, 'ab_confirm', 'Y') + extra} of {m}-{m + extra}"),
        ("F9 interval or named test", f"{len(named_test)} of {len(ab)} ({k(ab, 'ab_ci', 'Y')} counting bare claims of significance)",
         f"{len(named_test)}-{len(named_test) + extra} of {len(ab)}-{len(ab) + extra}"),
    ]
    assert named_test <= {r["key"] for r in ab if r["ab_ci"] == "Y"}
    for lab, val, unc in out:
        print(f"{lab:32s} {val:70s} {unc}")


if "--headline" in sys.argv:
    headline()
