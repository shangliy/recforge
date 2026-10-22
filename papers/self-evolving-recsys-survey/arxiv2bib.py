"""Build BibTeX entries for arXiv ids from the arXiv API (no guessing: every field comes from the API).

usage: python3 arxiv2bib.py ids.txt manual.bib > refs.bib
ids.txt: one "key arxiv_id" per line (# comments allowed). manual.bib is appended verbatim (non-arXiv entries).
"""
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}


def fetch(ids):
    url = "http://export.arxiv.org/api/query?max_results=200&id_list=" + ",".join(ids)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as e:  # rate limits
            print(f"% retry {attempt}: {e}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    raise SystemExit("arXiv API unreachable")


def tex(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")


def main():
    pairs = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
    out = []
    for i in range(0, len(pairs), 50):
        chunk = pairs[i:i + 50]
        root = fetch([p[1] for p in chunk])
        entries = root.findall("a:entry", NS)
        by_id = {}
        for e in entries:
            aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[1]
            by_id[re.sub(r"v\d+$", "", aid)] = e
        for key, aid in chunk:
            e = by_id.get(aid)
            if e is None or e.find("a:title", NS) is None:
                print(f"% MISSING {key} {aid}", file=sys.stderr)
                continue
            title = tex(e.find("a:title", NS).text)
            authors = " and ".join(tex(a.find("a:name", NS).text) for a in e.findall("a:author", NS))
            year = e.find("a:published", NS).text[:4]
            out.append(f"@misc{{{key},\n  title = {{{{{title}}}}},\n  author = {{{authors}}},\n  year = {{{year}}},\n"
                       f"  eprint = {{{aid}}},\n  archivePrefix = {{arXiv}},\n  howpublished = {{arXiv:{aid}}},\n"
                       f"  url = {{https://arxiv.org/abs/{aid}}}\n}}\n")
        time.sleep(3)
    print("\n".join(out))
    if len(sys.argv) > 2:
        print(open(sys.argv[2]).read())


if __name__ == "__main__":
    main()
