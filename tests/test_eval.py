import numpy as np
import torch

from recforge.data.schema import SeqData
from recforge.eval import evaluate, metrics_from_ranks, target_ranks


def test_ranks_break_ties_pessimistically():
    scores = torch.tensor([[0.0, 3.0, 1.0, 1.0, 2.0]])
    assert target_ranks(scores, torch.tensor([2])).item() == 3   # 1 and 4 above, 3 tied
    assert target_ranks(scores, torch.tensor([1])).item() == 0


def test_metric_values_by_hand():
    m = metrics_from_ranks(np.array([0, 1, 15, 30]), ks=(10, 20))
    assert m["hr@10"] == 0.5 and m["hr@20"] == 0.75
    assert np.isclose(m["ndcg@10"], (1 + 1 / np.log2(3)) / 4)
    assert np.isclose(m["ndcg@20"], (1 + 1 / np.log2(3) + 1 / np.log2(17)) / 4)
    assert np.isclose(m["mrr"], (1 + 1 / 2 + 1 / 16 + 1 / 31) / 4)


class _Fixed:
    """Scores item i as i: highest id ranks first."""
    def __init__(self, n_items):
        self.n_items = n_items

    def score(self, users, histories):
        return np.tile(np.arange(self.n_items + 1, dtype=np.float32), (len(users), 1))


def test_history_items_are_masked():
    # Items 9 and 10 are in the history, so the target 8 ranks first once they are masked.
    data = SeqData("t", 10, [np.array([1, 2, 9, 10, 8])])
    assert evaluate(_Fixed(10), data, "test")["hr@10"] == 1.0
    assert evaluate(_Fixed(10), data, "test", ks=(1,))["hr@1"] == 1.0
