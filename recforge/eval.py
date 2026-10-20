"""Full-ranking evaluation: every item is a candidate, no sampled negatives.

Items already in the user's history are removed from the ranking. Ties are
broken pessimistically (an item scored equal to the target counts as ranked
above it), so a model that outputs constants cannot score well by luck.
"""
from __future__ import annotations

from typing import Dict, Sequence

import numpy as np
import torch

from .data.schema import SeqData

KS = (10, 20)


def target_ranks(scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """0-based rank of each target among all candidates. scores: (B, V), targets: (B,)."""
    t = scores.gather(1, targets[:, None])
    greater = (scores > t).sum(1)
    ties = (scores == t).sum(1) - 1
    return greater + ties


def metrics_from_ranks(ranks: np.ndarray, ks: Sequence[int] = KS) -> Dict[str, float]:
    out = {}
    for k in ks:
        hit = ranks < k
        out[f"hr@{k}"] = float(hit.mean())
        out[f"ndcg@{k}"] = float(np.where(hit, 1.0 / np.log2(ranks + 2.0), 0.0).mean())
    out["mrr"] = float((1.0 / (ranks + 1.0)).mean())
    return out


@torch.no_grad()
def evaluate(model, data: SeqData, split: str, batch_size: int = 512, max_users: int | None = None,
             ks: Sequence[int] = KS) -> Dict[str, float]:
    histories, targets = data.split(split)
    users = np.arange(data.n_users)
    if max_users is not None and max_users < data.n_users:
        users = np.random.default_rng(0).choice(data.n_users, max_users, replace=False)
    ranks = []
    for lo in range(0, len(users), batch_size):
        u = users[lo:lo + batch_size]
        hist = [histories[i] for i in u]
        scores = torch.as_tensor(model.score(u, hist), dtype=torch.float32).cpu().clone()
        scores[:, 0] = -torch.inf
        rows = np.repeat(np.arange(len(u)), [len(h) for h in hist])
        scores[rows, np.concatenate(hist)] = -torch.inf
        ranks.append(target_ranks(scores, torch.as_tensor(targets[u])).numpy())
    return metrics_from_ranks(np.concatenate(ranks), ks)
