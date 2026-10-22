"""Emit the published-version upgrade table (markdown) from review/meta.json (Crossref + S2 + arXiv comments).

usage: python3 review/upgrades.py > review/upgrades.md   (from the survey root)
"""
import json
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from bibparse import norm  # noqa: E402

meta = json.load(open("review/meta.json"))
cites = json.load(open("review/bib_static.json"))["cites"]


def nn(s):
    s = unicodedata.normalize("NFKD", s)
    return norm("".join(c for c in s if not unicodedata.combining(c))).replace(" ", "")


rows = []
for k, v in meta.items():
    c = v.get("crossref")
    a = v["arxiv"]
    if not c:
        continue
    pages = c["page"] or (f"article {c['article-number']}" if c.get("article-number") else "n/a")
    vol = "/".join(x for x in (c.get("volume"), c.get("issue")) if x) or "-"
    year = c["issued"][0][0] if c["issued"] else "?"
    notes = []
    if norm(c["title"]) != norm(a["title"]):
        notes.append(f"published title differs: \"{c['title']}\"")
    pa = [nn(x) for x in c["authors"]]
    aa = [nn(x) for x in a["authors"]]
    if pa != aa:
        extra = [x for x in c["authors"] if nn(x) not in aa]
        missing = [x for x in a["authors"] if nn(x) not in pa]
        if extra or missing or len(pa) != len(aa):
            notes.append(f"author list differs (published {len(pa)}, arXiv {len(aa)}; +{extra} -{missing})")
    if c["via"] == "title":
        notes.append("matched by exact title (no DOI on arXiv/S2)")
    rows.append((0 if k in cites else 1, k, "yes" if k in cites else "no", c["container"].replace("&amp;", "&"),
                 year, vol, pages, c["doi"], "; ".join(notes)))
rows.sort()
print("| key | cited | published in | year | vol/issue | pages | DOI | notes |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(str(x) for x in r[1:]) + " |")
