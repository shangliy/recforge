"""A dataset with a known answer, for tests: each user walks item ids upward from a random start.

The next item is always last + 1, so a sequential model can reach HR@10 near 1
while popularity cannot.
"""
from __future__ import annotations

import numpy as np

from .schema import SeqData


def make_synthetic(n_users: int = 600, n_items: int = 200, min_len: int = 8, max_len: int = 20,
                   seed: int = 0) -> SeqData:
    rng = np.random.default_rng(seed)
    seqs = []
    for _ in range(n_users):
        start = rng.integers(n_items)
        length = rng.integers(min_len, max_len + 1)
        seqs.append(((start + np.arange(length)) % n_items + 1).astype(np.int64))
    return SeqData("synthetic", n_items, seqs, {}, {"source": "generated", "rule": "next = last + 1"})
