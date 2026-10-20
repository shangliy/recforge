"""The one data shape every model sees (as a train view; see SeqData.train_view).

A dataset is a list of per-user item sequences in chronological order. Item ids
run from 1 to n_items; 0 is padding. Each sequence has no repeated items, so a
leave-one-out target never appears in its own history.

Leave-one-out split (the protocol of SASRec, BERT4Rec, TIGER and HSTU papers):
  train: seq[:-2]
  val:   history seq[:-2], target seq[-2]
  test:  history seq[:-1], target seq[-1]
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

MIN_SEQ_LEN = 5


@dataclass
class SeqData:
    name: str
    n_items: int
    seqs: List[np.ndarray]
    item_meta: Dict[str, list] = field(default_factory=dict)  # each list has n_items + 1 entries, index 0 unused
    info: Dict = field(default_factory=dict)
    # A train view holds seq[:-2] only: it is what model code receives, so no target is reachable from it.
    is_train_view: bool = False

    @property
    def n_users(self) -> int:
        return len(self.seqs)

    def train_seqs(self) -> List[np.ndarray]:
        return list(self.seqs) if self.is_train_view else [s[:-2] for s in self.seqs]

    def train_view(self) -> "SeqData":
        return SeqData(self.name, self.n_items, self.train_seqs(), self.item_meta, self.info, is_train_view=True)

    def split(self, which: str) -> Tuple[List[np.ndarray], np.ndarray]:
        """(histories, targets) for 'val' or 'test'."""
        if self.is_train_view:
            raise PermissionError("a train view has no validation or test targets")
        if which == "val":
            return [s[:-2] for s in self.seqs], np.array([s[-2] for s in self.seqs], dtype=np.int64)
        if which == "test":
            return [s[:-1] for s in self.seqs], np.array([s[-1] for s in self.seqs], dtype=np.int64)
        raise ValueError(f"unknown split {which!r}")

    def stats(self) -> Dict:
        lens = np.array([len(s) for s in self.seqs])
        n = int(lens.sum())
        return {"users": self.n_users, "items": self.n_items, "interactions": n,
                "avg_len": round(float(lens.mean()), 1), "median_len": int(np.median(lens)),
                "density": round(n / (self.n_users * self.n_items), 5)}

    # ---- cache -------------------------------------------------------------
    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lens = np.array([len(s) for s in self.seqs], dtype=np.int64)
        np.savez_compressed(path, items=np.concatenate(self.seqs), lens=lens)
        path.with_suffix(".json").write_text(json.dumps(
            {"name": self.name, "n_items": self.n_items, "item_meta": self.item_meta, "info": self.info,
             "is_train_view": self.is_train_view}))

    @classmethod
    def load(cls, path: Path) -> "SeqData":
        z = np.load(path)
        meta = json.loads(path.with_suffix(".json").read_text())
        seqs = np.split(z["items"], np.cumsum(z["lens"])[:-1])
        return cls(meta["name"], meta["n_items"], seqs, meta["item_meta"], meta["info"],
                   meta.get("is_train_view", False))


def build(name: str, user_items: Dict[object, List[object]], item_meta_raw: Dict[str, Dict[object, object]],
          info: Dict, min_len: int = MIN_SEQ_LEN) -> SeqData:
    """Raw {user: [item, ...] in time order} -> SeqData.

    Repeats keep their first occurrence. Users with fewer than min_len distinct
    items are dropped. Items are numbered in order of first appearance after
    filtering, so ids are stable for a given raw file.
    """
    item_ids: Dict[object, int] = {}
    seqs = []
    for items in user_items.values():
        seen, seq = set(), []
        for it in items:
            if it not in seen:
                seen.add(it)
                seq.append(it)
        if len(seq) < min_len:
            continue
        for it in seq:
            if it not in item_ids:
                item_ids[it] = len(item_ids) + 1
        seqs.append(np.array([item_ids[it] for it in seq], dtype=np.int64))
    n_items = len(item_ids)
    raw_by_id = [None] * (n_items + 1)
    for raw, i in item_ids.items():
        raw_by_id[i] = raw
    meta = {"raw_id": [None if r is None else str(r) for r in raw_by_id]}
    for key, table in item_meta_raw.items():
        meta[key] = [None if r is None else table.get(r) for r in raw_by_id]
    return SeqData(name, n_items, seqs, meta, info)
