"""MIND-small (Microsoft News) as click sequences.

A user's sequence is the click history listed on their first impression (clicked
before the logging window; its order is kept but it has no timestamps), followed
by the items they clicked in impressions, in time order. Train and dev logs are
concatenated; the leave-one-out split then applies like any other dataset.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

import pandas as pd

from .schema import SeqData, build

BASE = "https://huggingface.co/datasets/huyva/MIND-small/resolve/main"
SPLITS = ("train", "dev")


def _ensure_raw(raw: Path) -> None:
    for s in SPLITS:
        for f in ("behaviors.tsv", "news.tsv"):
            p = raw / s / f
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(f"{BASE}/{s}/{f}", p)


def build_mind(raw: Path) -> SeqData:
    _ensure_raw(raw)
    news = pd.concat([pd.read_csv(raw / s / "news.tsv", sep="\t", header=None, quoting=3, usecols=[0, 1, 2, 3],
                                  names=["item", "category", "subcategory", "title"]) for s in SPLITS])
    news = news.drop_duplicates("item").set_index("item")
    b = pd.concat([pd.read_csv(raw / s / "behaviors.tsv", sep="\t", header=None, quoting=3,
                               names=["imp", "user", "time", "history", "impressions"]) for s in SPLITS])
    b["ts"] = pd.to_datetime(b.time, format="%m/%d/%Y %I:%M:%S %p")
    b = b.sort_values(["user", "ts"], kind="stable")

    user_items = {}
    for user, g in b.groupby("user", sort=False):
        first_hist = g.history.iloc[0]
        items = first_hist.split() if isinstance(first_hist, str) else []
        for imp in g.impressions:
            items.extend(tok[:-2] for tok in imp.split() if tok.endswith("-1"))
        user_items[user] = items
    return build("mind", user_items,
                 {"title": news.title.to_dict(), "category": news.category.to_dict(),
                  "subcategory": news.subcategory.to_dict()},
                 {"source": BASE, "feedback": "clicks",
                  "order": "pre-window history (untimed) then impression clicks by time"})
