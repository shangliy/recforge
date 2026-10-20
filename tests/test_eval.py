import numpy as np

from recforge.eval import metrics_from_lists, rank_lists, target_ranks


def test_target_ranks_and_misses():
    lists = np.array([[5, 3, 9], [1, 2, 4], [7, 8, 6]])
    assert target_ranks(lists, np.array([5, 4, 1])).tolist() == [0, 2, 3]


def test_metric_values_by_hand():
    lists = np.zeros((4, 100), dtype=np.int32)
    targets = np.array([11, 12, 13, 14])
    for row, pos in enumerate([0, 1, 15, 30]):
        lists[row, pos] = targets[row]
    m = metrics_from_lists(lists, targets, ks=(10, 20))
    assert m["hr@10"] == 0.5 and m["hr@20"] == 0.75
    assert np.isclose(m["ndcg@10"], (1 + 1 / np.log2(3)) / 4)
    assert np.isclose(m["ndcg@20"], (1 + 1 / np.log2(3) + 1 / np.log2(17)) / 4)
    assert np.isclose(m["mrr@100"], (1 + 1 / 2 + 1 / 16 + 1 / 31) / 4)


class _ById:
    """Scores item i as i: highest id ranks first."""
    def __init__(self, n_items):
        self.n_items = n_items

    def score(self, users, histories):
        return np.tile(np.arange(self.n_items + 1, dtype=np.float32), (len(users), 1))


def test_rank_lists_remove_history_and_padding():
    lists = rank_lists(_ById(10), np.array([0]), [np.array([1, 2, 9, 10])], n_items=10, k=8)
    assert lists[0].tolist() == [8, 7, 6, 5, 4, 3, 0, 0]
