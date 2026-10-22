"""Static checks of refs.bib against draft/paper.tex (no network).

usage: python3 review/check_bib.py  (from the survey root)
Reports: cited-but-missing keys, uncited entries, duplicate keys, duplicate works (same eprint / same normalised
title / same DOI), malformed fields (unescaped & % _ #, non-ASCII, unbalanced braces, titles not brace-protected,
acronyms in titles that lose capitalisation), and a list of cite keys per paper.tex line.
"""
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from bibparse import norm, parse_bib  # noqa: E402

bibtext = open("refs.bib").read()
entries = parse_bib(bibtext)
tex = open("draft/paper.tex").read()

# cite keys with line numbers (cite commands may span lines)
cites = defaultdict(list)
for m in re.finditer(r"\\cite[pt]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", tex):
    line = tex.count("\n", 0, m.start()) + 1
    for k in m.group(1).split(","):
        k = k.strip()
        if k:
            cites[k].append(line)

keys = [e["key"] for e in entries]
keyset = set(keys)
report = {}
report["n_entries"] = len(entries)
report["n_cited_keys"] = len(cites)
report["missing_in_bib"] = {k: v for k, v in cites.items() if k not in keyset}
report["uncited"] = [k for k in keys if k not in cites]
report["duplicate_keys"] = sorted({k for k in keys if keys.count(k) > 1})

dups = []
by = defaultdict(list)
for e in entries:
    f = e["fields"]
    if "eprint" in f:
        by["eprint:" + f["eprint"]].append(e["key"])
    if "doi" in f:
        by["doi:" + f["doi"].lower()].append(e["key"])
    by["title:" + norm(f.get("title", ""))].append(e["key"])
for k, v in by.items():
    if len(v) > 1:
        dups.append((k, v))
report["duplicate_works"] = dups

ACRONYMS = ["LLM", "CTR", "HSTU", "OneRec", "BERT4Rec", "SASRec", "AutoML", "NAS", "ML", "AI", "GPU", "LTR"]
issues = []
for e in entries:
    f = e["fields"]
    raw = e["raw"]
    if raw.count("{") != raw.count("}"):
        issues.append((e["key"], "unbalanced braces"))
    for name, val in f.items():
        if name == "url":
            continue
        v = re.sub(r"\$[^$]*\$", "", val)
        for ch in "&%#":
            if re.search(r"(?<!\\)" + re.escape(ch), v):
                issues.append((e["key"], f"unescaped {ch} in {name}"))
        if name not in ("eprint", "howpublished") and re.search(r"(?<!\\)_", v) and "\\url" not in v:
            issues.append((e["key"], f"unescaped _ in {name}"))
        if re.search(r"[^\x00-\x7f]", val):
            chars = "".join(sorted(set(re.findall(r"[^\x00-\x7f]", val))))
            issues.append((e["key"], f"non-ASCII {chars!r} in {name}"))
    t = f.get("title", "")
    protected = t.startswith("{") and t.endswith("}")
    if not protected:
        for a in ACRONYMS:
            if re.search(r"\b" + re.escape(a) + r"\b", t) and "{" + a not in t:
                issues.append((e["key"], f"title acronym {a} not brace-protected"))
    if "author" in f and re.search(r"\bothers\b", f["author"]):
        issues.append((e["key"], "author list truncated with 'and others'"))
    if e["type"] == "misc" and "eprint" not in f and "howpublished" not in f:
        issues.append((e["key"], "misc without howpublished"))
report["field_issues"] = issues
report["cites"] = cites
json.dump(report, open("review/bib_static.json", "w"), indent=1)
for k in ["n_entries", "n_cited_keys", "missing_in_bib", "uncited", "duplicate_keys", "duplicate_works", "field_issues"]:
    print(k, ":", json.dumps(report[k]) if not isinstance(report[k], int) else report[k])
