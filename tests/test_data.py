import numpy as np

from recforge.data.schema import SeqData, build
from recforge.data.synthetic import make_synthetic


def test_build_dedupes_filters_and_numbers_items():
    data = build("t", {"a": ["x", "y", "x", "z", "w", "v"], "b": ["x", "y"]}, {"title": {"x": "X"}}, {}, min_len=5)
    assert data.n_users == 1 and data.n_items == 5
    assert data.seqs[0].tolist() == [1, 2, 3, 4, 5]
    assert data.item_meta["raw_id"][1] == "x" and data.item_meta["title"][1] == "X"


def test_leave_one_out_never_leaks_targets():
    data = make_synthetic()
    _, val_t = data.split("val")
    test_h, test_t = data.split("test")
    for s, train, vt, th, tt in zip(data.seqs, data.train_seqs(), val_t, test_h, test_t):
        assert vt not in train and tt not in train and tt not in th
        assert th[-1] == vt and len(train) == len(s) - 2


def test_cache_round_trip(tmp_path):
    data = build("t", {"a": list("abcdef"), "b": list("ghijk")}, {"title": {"a": "A"}}, {"source": "x"})
    path = tmp_path / "t.npz"
    data.save(path)
    back = SeqData.load(path)
    assert back.n_items == data.n_items and back.item_meta == data.item_meta
    assert all(np.array_equal(x, y) for x, y in zip(back.seqs, data.seqs))
