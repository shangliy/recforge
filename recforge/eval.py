"""Evaluation in two halves, so model code never holds a target.

Model side (runs next to the model): `rank_lists` turns the model's full-catalogue
scores into a ranked top-K list per user, after removing padding and the user's
history items. Every item is a candidate; there are no sampled negatives.

Judge side (holds the targets): `metrics_from_lists` finds each target in its
list. A target outside the top K counts as a miss. Ties are whatever order the
model's list commits to.
"""
from __future__ import annotations

import inspect
from typing import Dict, List, Optional, Sequence

import numpy as np
import torch

KS = (10, 20)
LIST_LEN = 100


@torch.no_grad()
def rank_lists(model, users: np.ndarray, histories: List[np.ndarray], n_items: int,
               times: Optional[List[np.ndarray]] = None, k: int = LIST_LEN, batch_size: int = 512) -> np.ndarray:
    """(len(users), k) int32 item ids, best first; 0 fills slots when fewer than k candidates remain.

    A model whose score() takes a `times` argument also gets the history timestamps.
    """
    k = min(k, n_items)
    wants_times = "times" in inspect.signature(model.score).parameters
    out = np.zeros((len(users), k), dtype=np.int32)
    for lo in range(0, len(users), batch_size):
        u = users[lo:lo + batch_size]
        hist = histories[lo:lo + batch_size]
        if wants_times:
            raw = model.score(u, hist, times=None if times is None else times[lo:lo + batch_size])
        else:
            raw = model.score(u, hist)
        scores = torch.as_tensor(raw, dtype=torch.float32).cpu().clone()
        if scores.shape != (len(u), n_items + 1):
            raise ValueError(f"score() returned shape {tuple(scores.shape)}, expected {(len(u), n_items + 1)}")
        scores[:, 0] = -torch.inf
        rows = np.repeat(np.arange(len(u)), [len(h) for h in hist])
        if len(rows):
            scores[rows, np.concatenate(hist)] = -torch.inf
        vals, idx = scores.topk(k, dim=1)
        idx[torch.isinf(vals) & (vals < 0)] = 0
        out[lo:lo + len(u)] = idx.numpy()
    return out


def target_ranks(lists: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """0-based position of each target in its list; len(list) when absent."""
    hit = lists == targets[:, None]
    return np.where(hit.any(1), hit.argmax(1), lists.shape[1])


def metrics_from_lists(lists: np.ndarray, targets: np.ndarray, ks: Sequence[int] = KS) -> Dict[str, float]:
    ranks = target_ranks(lists, targets)
    out = {}
    for k in ks:
        hit = ranks < k
        out[f"hr@{k}"] = float(hit.mean())
        out[f"ndcg@{k}"] = float(np.where(hit, 1.0 / np.log2(ranks + 2.0), 0.0).mean())
    found = ranks < lists.shape[1]
    out[f"mrr@{lists.shape[1]}"] = float(np.where(found, 1.0 / (ranks + 1.0), 0.0).mean())
    return out
