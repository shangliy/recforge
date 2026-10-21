"""Timestamps, presets and the shared sequence-loss options."""
import numpy as np
import pytest
import torch

from recforge.data import load
from recforge.eval import rank_lists
from recforge.models.hstu import RelativeBias
from recforge.run import resolve_config, run_one


def test_times_follow_the_same_cuts():
    data = load("synthetic")
    view = data.train_view()
    assert all(len(t) == len(s) for t, s in zip(view.times, view.seqs))
    hist, _, times = data.split_with_times("test")
    assert all(len(t) == len(h) for t, h in zip(times, hist))


class _NeedsTimes:
    def __init__(self):
        self.seen = None

    def score(self, users, histories, times):
        self.seen = times
        return np.zeros((len(users), 11), dtype=np.float32)


def test_times_reach_models_that_ask_for_them():
    m = _NeedsTimes()
    rank_lists(m, np.array([0]), [np.array([1, 2])], n_items=10, times=[np.array([5, 9])])
    assert m.seen[0].tolist() == [5, 9]


def test_presets_layer_between_defaults_and_overrides():
    cfg = resolve_config("sasrec", {"dim": 32}, preset="hstu-repo")
    assert cfg["temperature"] == 0.05 and cfg["neg_sharing"] == "position" and cfg["dim"] == 32
    with pytest.raises(KeyError, match="preset"):
        resolve_config("sasrec", preset="nope")


def test_relative_bias_depends_on_offsets_and_gaps_only():
    rab = RelativeBias(max_len=4)
    t = torch.tensor([[0, 10, 100, 1000]])
    b1, b2 = rab(t), rab(t + 12345)
    assert torch.allclose(b1, b2)
    assert b1.shape == (1, 4, 4)


@pytest.mark.parametrize("sharing", ["batch", "position"])
def test_sampled_softmax_learns(sharing, workspace):
    cfg = {"epochs": 15, "max_len": 20, "dim": 32, "dropout": 0.1, "loss": "sampled", "n_neg": 32,
           "neg_sharing": sharing, "temperature": 0.1, "l2norm": True}
    assert run_one("synthetic", "sasrec", cfg)["test"]["hr@10"] > 0.8


def test_per_position_logit_paths_agree():
    from recforge.models.seqtrain import per_position_logits
    g = torch.Generator().manual_seed(0)
    h, emb = torch.randn(7, 5, generator=g), torch.randn(30, 5, generator=g)
    neg = torch.randint(1, 30, (7, 11), generator=g)
    assert torch.allclose(per_position_logits(h, emb, neg, True), per_position_logits(h, emb, neg, False), atol=1e-5)
