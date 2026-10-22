"""Counts and the LaTeX audit table, generated from audit.csv so the paper and the data cannot disagree.

usage: python3 summarize.py            -> prints counts
       python3 summarize.py --tex FILE -> also writes the table rows
Coding conventions: README.md in this directory.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).with_name("audit.csv"))))
core = [r for r in rows if r["set"] == "core"]
offline = [r for r in core if r["c2"] not in ("online", "na")]


def count(rs, col):
    return dict(Counter(r[col] for r in rs).most_common())


print(f"core systems: {len(core)}; offline-selection loops: {len(offline)}; comparison: {len(rows) - len(core)}")
for col, rs, label in [("c1", core, "C1 metric (core)"), ("c2", offline, "C2 selection (offline loops)"),
                       ("c3", offline, "C3 test once (offline loops)"), ("c4", core, "C4 repeated runs (core)"),
                       ("c5", core, "C5 gap/transfer (core)"), ("c6", core, "C6 null control (core)"),
                       ("c8", core, "C8 baselines (core)"), ("c9", core, "C9 isolation (core)"),
                       ("code", core, "code (core)"), ("llm_named", core, "LLM named (core)")]:
    print(f"{label:32s} {count(rs, col)}")
online = [r for r in core if r["online"] != "none"]
print(f"{'online A/B (core)':32s} {len(online)}; with duration: "
      f"{sum(any(u in r['online'] for u in ('d', 'wk', 'mo')) for r in online)}; with CI/significance: "
      f"{sum('CI' in r['online'] for r in online)}")
print(f"{'LLM tokens or cost (core)':32s} {sum(any(u in r['c7'] for u in ('$', 'tokens', 'RMB')) for r in core)}")

SHOW = {"c1": {"sampled": "Sampled", "ranking-ns": "Rank?", "auc": "AUC", "online": "A/B", "none": "?", "full": "Full",
               "other": "other"},
        "c2": {"val": "val", "NS": "\\ns", "online": "A/B", "test": "test", "trainloss": "loss"}}


def cell(col, v):
    v = SHOW.get(col, {}).get(v, v)
    return {"Y": "\\yes", "N": "\\no", "NS": "\\ns", "P": "\\pa", "na": "\\na", "gaming": "G", "Y+caught": "\\yes{}+G"}.get(v, v)


if "--tex" in sys.argv:
    out = []
    for r in rows:
        if r["set"] == "comparison" and r is rows[[x["set"] for x in rows].index("comparison")]:
            out.append("\\midrule\n\\multicolumn{12}{@{}l}{\\emph{Comparison points outside recommendation}} \\\\")
        name = r["system"].replace("&", "\\&")
        cells = [cell(c, r[c]) for c in ("c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9")]
        cells[6] = {"untuned": "\\no", "tuned": "\\yes", "production": "prod.", "published": "pub.",
                    "seed": "seed", "NS": "\\ns", "P": "\\pa"}.get(r["c8"], r["c8"])
        online = "\\no" if r["online"] == "none" else "\\yes"
        code = {"Y": "\\yes", "N": "\\no", "promised": "later"}[r["code"]]
        out.append(f"{name}~\\cite{{{r['key']}}} & {r['level']} & " + " & ".join(cells) + f" & {online} & {code} \\\\")
    Path(sys.argv[sys.argv.index("--tex") + 1]).write_text("\n".join(out) + "\n")
