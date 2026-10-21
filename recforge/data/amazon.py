"""Amazon Reviews 2014 5-core categories (the TIGER / P5 / S3-Rec benchmarks).

Each review is an interaction; sequences are ordered by review time (day resolution, file order for ties).
The 5-core files already have >= 5 reviews per user and item. Item text comes from the category's metadata
file: title, brand, categories, price.

Metadata lines are Python dict literals, parsed with ast.literal_eval (data only, nothing is executed).
"""
from __future__ import annotations

import ast
import gzip
import json
import urllib.request
from pathlib import Path

import pandas as pd

from .schema import SeqData, build

BASE = "http://snap.stanford.edu/data/amazon/productGraph/categoryFiles"
CATEGORIES = {"beauty": "Beauty", "sports": "Sports_and_Outdoors", "toys": "Toys_and_Games"}


def _ensure(path: Path, url: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".part")
        urllib.request.urlretrieve(url, tmp)
        tmp.rename(path)


def _category_text(cats) -> str | None:
    if not cats:
        return None
    return ", ".join(dict.fromkeys(c for path in cats for c in path))


def build_amazon(raw: Path, name: str) -> SeqData:
    cat = CATEGORIES[name]
    reviews, meta_file = raw / f"reviews_{cat}_5.json.gz", raw / f"meta_{cat}.json.gz"
    _ensure(reviews, f"{BASE}/reviews_{cat}_5.json.gz")
    _ensure(meta_file, f"{BASE}/meta_{cat}.json.gz")

    with gzip.open(reviews, "rt") as f:
        rows = [json.loads(line) for line in f]
    r = pd.DataFrame({"user": [x["reviewerID"] for x in rows], "item": [x["asin"] for x in rows],
                      "ts": [x["unixReviewTime"] for x in rows]})
    del rows
    items = set(r.item)
    meta = {"title": {}, "brand": {}, "categories": {}, "price": {}}
    with gzip.open(meta_file, "rt") as f:
        for line in f:
            d = ast.literal_eval(line)
            a = d.get("asin")
            if a not in items:
                continue
            for k in ("title", "brand", "price"):
                if d.get(k) is not None:
                    meta[k][a] = d[k]
            c = _category_text(d.get("categories"))
            if c:
                meta["categories"][a] = c
    r = r.sort_values(["user", "ts"], kind="stable")
    g = r.groupby("user", sort=False)
    return build(name, g["item"].apply(list).to_dict(), meta,
                 {"source": f"{BASE}/reviews_{cat}_5.json.gz", "feedback": "reviews (5-core)",
                  "order": "review day, file order for ties"},
                 user_times=g["ts"].apply(list).to_dict())
