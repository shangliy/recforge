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


def _write_openonerec(raw):
    import pyarrow as pa
    import pyarrow.parquet as pq
    raw.mkdir()
    users = []
    for u in range(4):
        users.append({"uid": u, "split": 0, "hist_video_pid": [10 * u + j for j in range(8)],
                      "hist_video_longview": [1, 1, 0, 1, 1, 1, 0, 1], "hist_video_like": [0, 0, 1, 0, 0, 0, 0, 0],
                      "hist_video_follow": [0] * 8, "hist_video_forward": [0] * 8,
                      "hist_video_not_interested": [0, 0, 0, 1, 0, 0, 0, 0],
                      "target_video_pid": [100 + u], "hist_goods_pid": [500 + 10 * u + j for j in range(4)],
                      "target_goods_pid": [600 + u]})
    pq.write_table(pa.Table.from_pylist(users), raw / "onerec_bench_release.parquet", row_group_size=2)
    pq.write_table(pa.Table.from_pylist([{"pid": 0, "caption": "first video"}, {"pid": 999, "caption": "unused"}]),
                   raw / "pid2caption.parquet")


def test_openonerec_video_keeps_positive_views_then_targets(tmp_path):
    from recforge.data.openonerec import build_openonerec
    raw = tmp_path / "openonerec"
    _write_openonerec(raw)
    data = build_openonerec(raw, "kuai-video")
    assert data.n_users == 4
    raw_ids = data.item_meta["raw_id"]
    # pid 2 is a like, 3 is not-interested, 6 is a plain view; the target comes last
    assert [int(raw_ids[i]) for i in data.seqs[0]] == [0, 1, 2, 4, 5, 7, 100]
    assert data.item_meta["title"][data.seqs[0][0]] == "first video"


def test_openonerec_goods_and_sample(tmp_path):
    from recforge.data import openonerec
    raw = tmp_path / "openonerec"
    _write_openonerec(raw)
    goods = openonerec.build_openonerec(raw, "kuai-goods")
    assert goods.n_users == 4 and goods.seqs[0].tolist() == [1, 2, 3, 4, 5]
    openonerec.SAMPLES["kuai-video-2"] = ("kuai-video", 2)
    try:
        a, b = (openonerec.build_openonerec(raw, "kuai-video-2") for _ in range(2))
    finally:
        del openonerec.SAMPLES["kuai-video-2"]
    assert a.n_users == 2 and [s.tolist() for s in a.seqs] == [s.tolist() for s in b.seqs]
