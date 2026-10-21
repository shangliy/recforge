"""MovieLens-1M as implicit feedback: every rating is an interaction (the SASRec / HSTU convention)."""
from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from .schema import SeqData, build

URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"


def _ensure_raw(raw: Path) -> None:
    if (raw / "ratings.dat").exists():
        return
    raw.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL) as r:
        zipfile.ZipFile(io.BytesIO(r.read())).extractall(raw.parent)


def build_ml1m(raw: Path) -> SeqData:
    _ensure_raw(raw)
    rd = lambda f, cols: pd.read_csv(raw / f, sep="::", engine="python", names=cols, encoding="latin-1")
    r = rd("ratings.dat", ["user", "item", "rating", "ts"])
    m = rd("movies.dat", ["item", "title", "genres"]).set_index("item")
    # Stable sort keeps file order for equal timestamps, which are common in ML-1M.
    r = r.sort_values(["user", "ts"], kind="stable")
    g = r.groupby("user", sort=False)
    user_items, user_times = g["item"].apply(list).to_dict(), g["ts"].apply(list).to_dict()
    return build("ml1m", user_items,
                 {"title": m.title.to_dict(), "genres": m.genres.to_dict()},
                 {"source": URL, "feedback": "all ratings as implicit interactions",
                  "order": "timestamp, file order for ties"}, user_times=user_times)
