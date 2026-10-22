"""Compare refs.bib arXiv entries against review/meta.json (from fetch_meta.py).

usage: python3 review/compare_meta.py  (from the survey root) -> prints mismatches and publication info,
writes review/meta_report.json
"""
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from bibparse import norm, parse_bib  # noqa: E402


def tex(s):  # same escaping as arxiv2bib.py
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")


def nname(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return norm(s)


entries = {e["key"]: e for e in parse_bib(open("refs.bib").read())}
meta = json.load(open("review/meta.json"))
rep = {"title": [], "authors": [], "year": [], "missing": [], "published": [], "s2_venue": [], "versions": []}
for key, m in meta.items():
    f = entries[key]["fields"]
    a = m.get("arxiv")
    if not a:
        rep["missing"].append(key)
        continue
    bt = f["title"].strip()
    if bt.startswith("{") and bt.endswith("}"):
        bt = bt[1:-1]
    if bt != tex(a["title"]):
        rep["title"].append((key, bt, tex(a["title"]), "norm-equal" if norm(bt) == norm(a["title"]) else "DIFF"))
    ba = [x.strip() for x in re.split(r"\s+and\s+", f["author"])]
    aa = [tex(x) for x in a["authors"]]
    if ba != aa:
        rep["authors"].append((key, ba, aa))
    if f.get("year") != a["published"][:4]:
        rep["year"].append((key, f.get("year"), a["published"][:4]))
    if a.get("journal_ref") or a.get("doi"):
        rep["published"].append((key, m["eprint"], a.get("journal_ref"), a.get("doi")))
    if a.get("comment") and re.search(r"accepted|published|appear|proceedings|conference|KDD|RecSys|SIGIR|WWW|NeurIPS|ICLR|ICML|CIKM|WSDM|AAAI|IJCAI|ACL|EMNLP|TOIS|TKDE|journal", a["comment"], re.I):
        rep["versions"].append((key, m["eprint"], a["comment"]))
    s2 = m.get("s2", {})
    if s2 and not s2.get("error"):
        pv = s2.get("publicationVenue") or {}
        ext = s2.get("externalIds") or {}
        venue = s2.get("venue") or ""
        if venue and venue.lower() not in ("arxiv.org", "arxiv"):
            rep["s2_venue"].append((key, m["eprint"], venue, pv.get("name"), s2.get("year"), ext.get("DOI"),
                                    (s2.get("journal") or {}).get("name"), (s2.get("journal") or {}).get("pages")))
    elif s2.get("error"):
        rep.setdefault("s2_error", []).append((key, s2.get("error")))
json.dump(rep, open("review/meta_report.json", "w"), indent=1)
for k, v in rep.items():
    print(f"== {k}: {len(v)}")
    for x in v:
        print("  ", x)
