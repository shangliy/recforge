"""Semantic Scholar batch lookup (one POST for all arXiv ids; the per-paper endpoint is rate-limited to uselessness).

usage: python3 review/fetch_s2_batch.py  (from the survey root) -> adds "s2" to review/meta.json
"""
import json
import time
import urllib.request

meta = json.load(open("review/meta.json"))
keys = list(meta)
body = json.dumps({"ids": [f"ARXIV:{meta[k]['eprint']}" for k in keys]}).encode()
url = ("https://api.semanticscholar.org/graph/v1/paper/batch"
       "?fields=title,venue,year,publicationVenue,externalIds,journal,publicationDate,publicationTypes")
for attempt in range(8):
    try:
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                              "User-Agent": "ref-check/0.1"})
        res = json.loads(urllib.request.urlopen(req, timeout=120).read())
        break
    except Exception as e:
        print("retry", attempt, e, flush=True)
        time.sleep(20 * (attempt + 1))
else:
    raise SystemExit("S2 unreachable")
for k, r in zip(keys, res):
    meta[k]["s2"] = r if r else {"error": "not found"}
json.dump(meta, open("review/meta.json", "w"), indent=1)
print("found", sum(1 for r in res if r), "of", len(keys))
