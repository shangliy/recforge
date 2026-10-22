"""Resolve published versions via Crossref.

For each arXiv entry: collect a non-arXiv DOI from the arXiv record or Semantic Scholar and fetch its Crossref record;
if there is none, query Crossref by exact title and accept a hit only when the normalised title matches exactly and
the hit is not a posted-content/preprint record. Writes "crossref" into review/meta.json.
usage: python3 review/fetch_crossref.py (from the survey root)
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from bibparse import norm  # noqa: E402

UA = {"User-Agent": "ref-check/0.1"}


def get(url):
    for attempt in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5 * (attempt + 1))
        except Exception:
            time.sleep(5 * (attempt + 1))
    return None


def slim(m):
    return {"doi": m.get("DOI"), "type": m.get("type"), "title": (m.get("title") or [""])[0],
            "container": (m.get("container-title") or [""])[0], "page": m.get("page"),
            "volume": m.get("volume"), "issue": m.get("issue"), "article-number": m.get("article-number"),
            "issued": (m.get("issued") or {}).get("date-parts"), "publisher": m.get("publisher"),
            "authors": [(a.get("given", "") + " " + a.get("family", "")).strip() or a.get("name", "")
                        for a in m.get("author", [])],
            "event": (m.get("event") or {}).get("name")}


meta = json.load(open("review/meta.json"))
for key, m in meta.items():
    if "crossref" in m:
        continue
    dois = []
    a = m.get("arxiv") or {}
    if a.get("doi"):
        dois.append(a["doi"])
    s2doi = ((m.get("s2") or {}).get("externalIds") or {}).get("DOI")
    if s2doi and not s2doi.lower().startswith("10.48550"):
        dois.append(s2doi)
    res = None
    for d in dict.fromkeys(dois):
        r = get("https://api.crossref.org/works/" + urllib.parse.quote(d))
        if r:
            res = {"via": "doi", **slim(r["message"])}
            break
        time.sleep(1)
    if res is None and a.get("title"):
        q = urllib.parse.quote(a["title"])
        r = get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=5")
        if r:
            for it in r["message"]["items"]:
                t = (it.get("title") or [""])[0]
                if norm(t) == norm(a["title"]) and it.get("type") not in ("posted-content",) \
                        and not (it.get("DOI", "").lower().startswith("10.48550")):
                    res = {"via": "title", **slim(it)}
                    break
    m["crossref"] = res
    json.dump(meta, open("review/meta.json", "w"), indent=1)
    time.sleep(1)
print("crossref hits:", sum(1 for v in meta.values() if v.get("crossref")))
