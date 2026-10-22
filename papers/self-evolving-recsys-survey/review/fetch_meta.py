"""Fetch arXiv API + Semantic Scholar records for every refs.bib entry with an eprint.

usage: python3 review/fetch_meta.py  (run from the survey root) -> review/meta.json
arXiv: batches of <=50 ids, 3 s between calls. Semantic Scholar: one call per id, 3.5 s apart, retries on 429.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from bibparse import parse_bib  # noqa: E402

NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
OUT = os.path.join(os.path.dirname(__file__), "meta.json")
UA = {"User-Agent": "ref-check/0.1 (survey bibliography verification)"}


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def arxiv_batch(ids):
    url = "https://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids)
    for attempt in range(6):
        try:
            root = ET.fromstring(get(url))
            out = {}
            for e in root.findall("a:entry", NS):
                aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[1]
                base = aid.rsplit("v", 1)[0] if "v" in aid else aid
                jr = e.find("x:journal_ref", NS)
                doi = e.find("x:doi", NS)
                cm = e.find("x:comment", NS)
                out[base] = {
                    "version": aid,
                    "title": " ".join(e.find("a:title", NS).text.split()),
                    "authors": [a.find("a:name", NS).text.strip() for a in e.findall("a:author", NS)],
                    "published": e.find("a:published", NS).text,
                    "updated": e.find("a:updated", NS).text,
                    "journal_ref": jr.text.strip() if jr is not None else None,
                    "doi": doi.text.strip() if doi is not None else None,
                    "comment": " ".join(cm.text.split()) if cm is not None else None,
                    "abstract": " ".join(e.find("a:summary", NS).text.split()),
                }
            return out
        except Exception as ex:  # rate limit / transient
            print(f"arxiv retry {attempt}: {ex}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    raise SystemExit("arXiv API unreachable")


def s2(aid):
    url = (f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}"
           "?fields=title,venue,year,publicationVenue,externalIds,journal,publicationDate,authors")
    for attempt in range(6):
        try:
            return json.loads(get(url, 30))
        except urllib.error.HTTPError as ex:
            if ex.code == 404:
                return {"error": 404}
            time.sleep(15 * (attempt + 1))
        except Exception as ex:
            print(f"s2 retry {aid} {attempt}: {ex}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return {"error": "unreachable"}


def main():
    entries = parse_bib(open("refs.bib").read())
    ids = [(e["key"], e["fields"]["eprint"]) for e in entries if "eprint" in e["fields"]]
    meta = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = [i for i in ids if i[0] not in meta or "arxiv" not in meta[i[0]]]
    for b in range(0, len(todo), 50):
        chunk = todo[b:b + 50]
        res = arxiv_batch([a for _, a in chunk])
        for key, aid in chunk:
            meta.setdefault(key, {"eprint": aid})["arxiv"] = res.get(aid)
        json.dump(meta, open(OUT, "w"), indent=1)
        time.sleep(3)
    for key, aid in ids:
        if "s2" in meta.get(key, {}) and meta[key]["s2"].get("error") != "unreachable":
            continue
        meta[key]["s2"] = s2(aid)
        json.dump(meta, open(OUT, "w"), indent=1)
        time.sleep(3.5)
    print(f"done: {len(ids)} ids", file=sys.stderr)


if __name__ == "__main__":
    main()
