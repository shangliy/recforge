"""A recforge model. Copy this file, rename the class and `name`, and replace fit/score.

Run it:
    python -m recforge bench --model path/to/this_file.py:MarkovChain --suite smoke
    python -m recforge bench --model path/to/this_file.py:MarkovChain --suite ml1m --device cuda

Contract (docs/AGENTS.md):
- fit(data, val_fn) gets a train view: data.train_seqs() are per-user item-id arrays in time order, ids
  1..data.n_items, 0 is padding; data.item_meta has per-item text such as "title". val_fn() returns
  validation NDCG@10 of the model as it is now; call it for early stopping, and leave the model in its
  best state. fit returns a dict of anything worth logging.
- score(users, histories) returns a (len(users), data.n_items + 1) array or tensor, higher is better.
  histories[i] is user i's items so far; history items are removed from the ranking for you.
- All settings live in DEFAULTS; `--set key=value` overrides them and every value is logged.
"""
import numpy as np
import scipy.sparse as sp

from recforge.models.base import Recommender


class MarkovChain(Recommender):
    """Scores the next item by how often it followed the user's last item in training."""
    name = "markov"
    DEFAULTS = {"smoothing": 1.0}

    def fit(self, data, val_fn):
        prev = np.concatenate([s[:-1] for s in data.train_seqs()])
        nxt = np.concatenate([s[1:] for s in data.train_seqs()])
        n = data.n_items + 1
        self.trans = sp.csr_matrix((np.ones(len(prev), dtype=np.float32), (prev, nxt)), shape=(n, n))
        self.pop = np.bincount(nxt, minlength=n).astype(np.float32)
        self.pop /= self.pop.sum()
        return {"transitions": int(self.trans.nnz), "val_ndcg@10": val_fn()}

    def score(self, users, histories):
        last = np.array([h[-1] if len(h) else 0 for h in histories])
        return self.trans[last].toarray() + self.cfg["smoothing"] * self.pop
