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


TINY_TIGER = {"text_encoder": "random", "rq_hidden": [64, 32], "rq_latent": 16, "rq_levels": 2, "rq_codebook": 16,
              "rq_epochs": 30, "rq_batch": 256, "d_model": 64, "d_kv": 32, "d_ff": 128, "heads": 2, "layers": 2,
              "user_buckets": 50, "max_items": 5, "steps": 1500, "batch_size": 64, "lr": 0.01, "warmup_steps": 200,
              "eval_every": 500, "patience": 3, "beam": 20}


def test_tiger_semantic_ids_are_unique_and_index_round_trips():
    from recforge.models.tiger import TIGER, PrefixIndex, semantic_ids
    emb = np.random.default_rng(0).standard_normal((200, 768)).astype(np.float32)
    codes, stats = semantic_ids(emb, {**TIGER.DEFAULTS, **TINY_TIGER}, seed=1, device="cpu")
    assert codes.shape == (201, 3) and len({tuple(r) for r in codes[1:]}) == 200
    sizes = [16, 16, int(codes[:, -1].max()) + 1]
    idx = PrefixIndex(codes, sizes, "cpu")
    key = torch.zeros(200, dtype=torch.long)
    for t, k in enumerate(sizes):
        assert idx.allowed(t, key)[torch.arange(200), torch.as_tensor(codes[1:, t])].all()
        key = key * k + torch.as_tensor(codes[1:, t])
    assert idx.items(key).tolist() == list(range(1, 201))


def test_tiger_learns_the_synthetic_rule(workspace):
    rec = run_one("synthetic", "tiger", TINY_TIGER)
    assert rec["fit"]["max_collisions"] >= 1 and rec["test"]["hr@10"] > 0.6, rec["test"]


def test_tiger_beam_scores_equal_exact_sequence_log_probs():
    """With a beam wider than the catalogue, constrained beam search must return every item with its exact log p."""
    from transformers import T5Config, T5ForConditionalGeneration
    from recforge.models.tiger import TIGER, PrefixIndex, semantic_ids
    cfg = {**TIGER.DEFAULTS, **TINY_TIGER, "beam": 64}
    emb = np.random.default_rng(0).standard_normal((40, 768)).astype(np.float32)
    codes, _ = semantic_ids(emb, cfg, seed=1, device="cpu")
    m = TIGER(cfg, seed=1, device="cpu")
    m._layout(codes)
    m.index = PrefixIndex(codes, m.sizes, "cpu")
    torch.manual_seed(0)
    m.net = T5ForConditionalGeneration(T5Config(vocab_size=m.vocab, d_model=32, d_kv=8, d_ff=64, num_layers=1,
                                                num_decoder_layers=1, num_heads=2, feed_forward_proj="relu",
                                                pad_token_id=0, eos_token_id=1, decoder_start_token_id=0)).eval()
    users, hist = np.array([3]), [np.array([5, 9, 2])]
    got = m.score(users, hist)[0]
    ids, mask = m._encode_inputs(users, hist)
    with torch.no_grad():
        labels = m.tokens[1:]
        logits = m.net(input_ids=ids.repeat(40, 1), attention_mask=mask.repeat(40, 1), labels=labels).logits
        exact = torch.log_softmax(logits, -1).gather(2, labels[:, :, None]).squeeze(-1).sum(1)
    assert torch.isfinite(got[1:]).all()
    assert torch.allclose(got[1:], exact, atol=1e-4)
