"""HSTU (Zhai et al., 2024, "Actions Speak Louder than Words"), dense re-implementation.

Follows meta-recsys/generative-recommenders (generative_recommenders/research/modeling/sequential/hstu.py,
commit 10c4950) without its jagged fbgemm kernels:

    u, v, q, k = split(SiLU(LayerNorm(x) W_uvqk))
    A = SiLU(q k^T + rab_pos(i - j) + rab_time(bucket(dt))) / N      no softmax; N = padded length
    y = x + W_o(dropout(u * LayerNorm(A v)))

Input: item embedding * sqrt(D) + learned absolute position, dropout. Output: the last block's state,
L2-normalised for scoring. Defaults are the repo's ML-1M config (hstu-sampled-softmax-n128-final.gin).

One deliberate difference: the repo's time bias at query i uses the timestamp of item i+1, which at
the last position is the target's timestamp. recforge never gives a model target information, so the
time bias here uses dt = t_i - t_j (time_bias="current"). Repo-reported ML-1M: HR@10 0.3097, NDCG@10 0.1720.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .seqtrain import LOSS_DEFAULTS, SeqModel


class RelativeBias(nn.Module):
    """Learned bias by relative position and by log-bucketed time gap."""

    def __init__(self, max_len: int, num_buckets: int = 128):
        super().__init__()
        self.max_len, self.num_buckets = max_len, num_buckets
        self.pos_w = nn.Parameter(torch.empty(2 * max_len - 1).normal_(0, 0.02))
        self.ts_w = nn.Parameter(torch.empty(num_buckets + 1).normal_(0, 0.02))

    def forward(self, times: torch.Tensor) -> torch.Tensor:
        """times (B, L) -> bias (B, L, L) for query i, key j."""
        b, l = times.shape
        idx = torch.arange(l, device=times.device)
        pos = self.pos_w[(idx[None, :] - idx[:, None]) + self.max_len - 1]
        dt = (times[:, :, None] - times[:, None, :]).abs().clamp(min=1).float()
        bucket = (torch.log(dt) / 0.301).long().clamp(0, self.num_buckets)
        return pos[None] + self.ts_w[bucket]


class HSTUBlock(nn.Module):
    def __init__(self, dim: int, dqk: int, dv: int, heads: int, dropout: float, max_len: int):
        super().__init__()
        self.dim, self.dqk, self.dv, self.heads, self.dropout = dim, dqk, dv, heads, dropout
        self.uvqk = nn.Parameter(torch.empty(dim, 2 * dv * heads + 2 * dqk * heads).normal_(0, 0.02))
        self.o = nn.Linear(dv * heads, dim)
        nn.init.xavier_uniform_(self.o.weight)
        self.rab = RelativeBias(max_len)

    def forward(self, x: torch.Tensor, times: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        b, l, _ = x.shape
        h = F.silu(F.layer_norm(x, [self.dim], eps=1e-6) @ self.uvqk)
        u, v, q, k = h.split([self.dv * self.heads] * 2 + [self.dqk * self.heads] * 2, dim=-1)
        q = q.view(b, l, self.heads, self.dqk)
        k = k.view(b, l, self.heads, self.dqk)
        attn = torch.einsum("bnhd,bmhd->bhnm", q, k) + self.rab(times)[:, None]
        attn = F.silu(attn) / l * mask[:, None]
        out = torch.einsum("bhnm,bmhd->bnhd", attn, v.view(b, l, self.heads, self.dv)).reshape(b, l, -1)
        out = u * F.layer_norm(out, [self.dv * self.heads], eps=1e-6)
        return x + self.o(F.dropout(out, self.dropout, self.training))


class HSTUNet(nn.Module):
    def __init__(self, n_items: int, dim: int, layers: int, heads: int, dqk: int, dv: int, max_len: int,
                 dropout: float):
        super().__init__()
        self.dim = dim
        self.item = nn.Embedding(n_items + 1, dim, padding_idx=0)
        nn.init.trunc_normal_(self.item.weight, std=0.02)
        self.pos = nn.Embedding(max_len, dim)
        nn.init.trunc_normal_(self.pos.weight, std=math.sqrt(1.0 / dim))
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList(HSTUBlock(dim, dqk, dv, heads, dropout, max_len) for _ in range(layers))

    def encode(self, seq: torch.Tensor, times: torch.Tensor) -> torch.Tensor:
        b, l = seq.shape
        valid = seq > 0
        x = self.item(seq) * math.sqrt(self.dim) + self.pos(torch.arange(l, device=seq.device))
        x = self.drop(x) * valid.unsqueeze(-1)
        causal = torch.ones(l, l, dtype=torch.bool, device=seq.device).tril()
        mask = (causal & valid[:, None, :] & valid[:, :, None]).float()
        for blk in self.blocks:
            x = blk(x, times, mask)
        return x


class HSTU(SeqModel):
    name = "hstu"
    DEFAULTS = {"dim": 50, "layers": 2, "heads": 1, "dqk": 50, "dv": 50, "dropout": 0.2, "max_len": 200,
                "lr": 1e-3, "weight_decay": 0.0, "batch_size": 128, "epochs": 101, "patience": 20,
                **LOSS_DEFAULTS, "loss": "sampled", "n_neg": 128, "neg_sharing": "position",
                "temperature": 0.05, "l2norm": True}
    # hstu-repo-large: hstu-sampled-softmax-n128-large-final.gin (repo-reported HR@10 0.3294, NDCG@10 0.1893).
    PRESETS = {"hstu-repo": {"patience": 101},
               "hstu-repo-large": {"layers": 8, "heads": 2, "dqk": 25, "dv": 25, "patience": 101}}

    def build_net(self, data):
        c = self.cfg
        return HSTUNet(data.n_items, c["dim"], c["layers"], c["heads"], c["dqk"], c["dv"], c["max_len"],
                       c["dropout"])
