"""SASRec (Kang & McAuley, 2018): causal self-attention over the item sequence.

Pre-LayerNorm blocks. Trained with softmax losses (seqtrain.py) rather than the
original binary loss, as in later reproductions.

Presets:
  hstu-repo   the training setup of the SASRec baseline in meta-recsys/generative-recommenders
              (configs/ml-1m/sasrec-sampled-softmax-n128-final.gin, commit 10c4950): dim 50, 1 head,
              FFN 50 ReLU, dropout 0.2, 128 per-position negatives, temperature 0.05, L2 norm, 101 epochs.
              That repo reports ML-1M HR@10 0.2853 / NDCG@10 0.1603, training on seq[:-1] with no
              validation split; under loo-2 the model trains on one item fewer per user.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .seqtrain import LOSS_DEFAULTS, SeqModel, left_pad  # noqa: F401  (left_pad re-exported)


class Block(nn.Module):
    def __init__(self, dim: int, heads: int, ffn_dim: int, activation: str, dropout: float):
        super().__init__()
        self.heads, self.dropout = heads, dropout
        self.ln1, self.ln2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        self.qkv, self.out = nn.Linear(dim, 3 * dim), nn.Linear(dim, dim)
        act = {"gelu": nn.GELU, "relu": nn.ReLU}[activation]
        self.ffn = nn.Sequential(nn.Linear(dim, ffn_dim), act(), nn.Dropout(dropout), nn.Linear(ffn_dim, dim))
        self.drop = nn.Dropout(dropout)

    def forward(self, x, mask):
        b, l, d = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(b, l, 3, self.heads, d // self.heads).permute(2, 0, 3, 1, 4)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, dropout_p=self.dropout if self.training else 0.0)
        x = x + self.drop(self.out(a.transpose(1, 2).reshape(b, l, d)))
        return x + self.drop(self.ffn(self.ln2(x)))


class SASRecNet(nn.Module):
    def __init__(self, n_items: int, dim: int, layers: int, heads: int, ffn_dim: int, activation: str,
                 max_len: int, dropout: float):
        super().__init__()
        self.dim = dim
        self.item = nn.Embedding(n_items + 1, dim, padding_idx=0)
        self.pos = nn.Embedding(max_len, dim)
        self.blocks = nn.ModuleList(Block(dim, heads, ffn_dim, activation, dropout) for _ in range(layers))
        self.ln = nn.LayerNorm(dim)
        self.drop = nn.Dropout(dropout)
        nn.init.normal_(self.item.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)

    def encode(self, seq: torch.Tensor, times=None) -> torch.Tensor:
        """seq: (B, L) left-padded -> hidden states (B, L, D)."""
        b, l = seq.shape
        x = self.item(seq) * math.sqrt(self.dim) + self.pos(torch.arange(l, device=seq.device))
        x = self.drop(x) * (seq > 0).unsqueeze(-1)
        causal = torch.ones(l, l, dtype=torch.bool, device=seq.device).tril()
        # Queries see earlier real items; every position may also see itself, so no row is fully masked.
        mask = (causal & (seq > 0)[:, None, :]) | torch.eye(l, dtype=torch.bool, device=seq.device)
        mask = mask[:, None]
        for blk in self.blocks:
            x = blk(x, mask)
        return self.ln(x)


class SASRec(SeqModel):
    name = "sasrec"
    DEFAULTS = {"dim": 64, "layers": 2, "heads": 2, "ffn_dim": 256, "activation": "gelu", "dropout": 0.2,
                "max_len": 200, "lr": 1e-3, "weight_decay": 0.0, "batch_size": 128, "epochs": 200,
                "patience": 10, **LOSS_DEFAULTS}
    PRESETS = {"hstu-repo": {"dim": 50, "heads": 1, "ffn_dim": 50, "activation": "relu", "dropout": 0.2,
                             "max_len": 200, "lr": 1e-3, "weight_decay": 0.0, "batch_size": 128,
                             "epochs": 101, "patience": 101, "loss": "sampled", "n_neg": 128,
                             "neg_sharing": "position", "temperature": 0.05, "l2norm": True}}

    def build_net(self, data):
        c = self.cfg
        return SASRecNet(data.n_items, c["dim"], c["layers"], c["heads"], c["ffn_dim"], c["activation"],
                         c["max_len"], c["dropout"])
