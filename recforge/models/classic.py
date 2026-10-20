"""Non-neural baselines: popularity and item-based kNN."""
from __future__ import annotations

from typing import Dict, List

import numpy as np
import scipy.sparse as sp

from .base import Recommender


def _user_item_matrix(seqs: List[np.ndarray], n_items: int) -> sp.csr_matrix:
    rows = np.repeat(np.arange(len(seqs)), [len(s) for s in seqs])
    cols = np.concatenate(seqs)
    return sp.csr_matrix((np.ones(len(cols), dtype=np.float32), (rows, cols)), shape=(len(seqs), n_items + 1))


class Pop(Recommender):
    name = "pop"

    def fit(self, data, val_fn):
        self.counts = np.bincount(np.concatenate(data.train_seqs()), minlength=data.n_items + 1).astype(np.float32)
        return {}

    def score(self, users, histories):
        return np.repeat(self.counts[None], len(users), 0)


class ItemKNN(Recommender):
    """Cosine similarity on the user-item matrix, keeping the top-k neighbours of each item."""
    name = "itemknn"
    DEFAULTS = {"k": 100, "shrink": 10.0, "block": 512}

    def fit(self, data, val_fn):
        x = _user_item_matrix(data.train_seqs(), data.n_items).tocsc()
        norms = np.sqrt(np.asarray(x.sum(0)).ravel())
        xt = x.T.tocsr()
        k, shrink, n = self.cfg["k"], self.cfg["shrink"], data.n_items + 1
        rows, cols, vals = [], [], []
        for lo in range(0, n, self.cfg["block"]):
            hi = min(n, lo + self.cfg["block"])
            co = (xt[lo:hi] @ x).toarray()
            sim = co / (norms[lo:hi, None] * norms[None, :] + shrink + 1e-8)
            sim[np.arange(hi - lo), np.arange(lo, hi)] = 0.0
            kk = min(k, n - 1)
            top = np.argpartition(-sim, kk - 1, axis=1)[:, :kk]
            v = np.take_along_axis(sim, top, 1)
            keep = v > 0
            rows.append(np.repeat(np.arange(lo, hi), kk)[keep.ravel()])
            cols.append(top[keep])
            vals.append(v[keep])
        self.sim = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
        self.n_items = data.n_items
        return {"nnz": int(self.sim.nnz)}

    def score(self, users, histories):
        return (_user_item_matrix(histories, self.n_items) @ self.sim).toarray()
