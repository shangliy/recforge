"""SASRec (Kang & McAuley, 2018): causal self-attention over the item sequence.

Trained with softmax cross-entropy rather than the original binary loss, as in
later reproductions (e.g. the HSTU paper's SASRec baseline). loss="ce" uses the
full catalogue; loss="sampled" uses n_neg uniform negatives shared across the
batch, for catalogues too large for a full softmax.
"""
from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .base import EarlyStopper, Recommender


def left_pad(seqs, max_len: int) -> torch.Tensor:
    out = np.zeros((len(seqs), max_len), dtype=np.int64)
    for i, s in enumerate(seqs):
        s = s[-max_len:]
        if len(s):
            out[i, -len(s):] = s
    return torch.as_tensor(out)


class Block(nn.Module):
    def __init__(self, dim: int, heads: int, dropout: float):
        super().__init__()
        self.heads, self.dropout = heads, dropout
        self.ln1, self.ln2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        self.qkv, self.out = nn.Linear(dim, 3 * dim), nn.Linear(dim, dim)
        self.ffn = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Dropout(dropout), nn.Linear(4 * dim, dim))
        self.drop = nn.Dropout(dropout)

    def forward(self, x, mask):
        b, l, d = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(b, l, 3, self.heads, d // self.heads).permute(2, 0, 3, 1, 4)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, dropout_p=self.dropout if self.training else 0.0)
        x = x + self.drop(self.out(a.transpose(1, 2).reshape(b, l, d)))
        return x + self.drop(self.ffn(self.ln2(x)))


class SASRecNet(nn.Module):
    def __init__(self, n_items: int, dim: int, layers: int, heads: int, max_len: int, dropout: float):
        super().__init__()
        self.dim = dim
        self.item = nn.Embedding(n_items + 1, dim, padding_idx=0)
        self.pos = nn.Embedding(max_len, dim)
        self.blocks = nn.ModuleList(Block(dim, heads, dropout) for _ in range(layers))
        self.ln = nn.LayerNorm(dim)
        self.drop = nn.Dropout(dropout)
        nn.init.normal_(self.item.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)

    def forward(self, seq: torch.Tensor) -> torch.Tensor:
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


class SASRec(Recommender):
    name = "sasrec"
    DEFAULTS = {"dim": 64, "layers": 2, "heads": 2, "dropout": 0.2, "max_len": 200, "lr": 1e-3,
                "weight_decay": 0.0, "batch_size": 128, "epochs": 200, "patience": 10,
                "loss": "auto", "n_neg": 512}

    def fit(self, data, val_fn):
        c = self.cfg
        loss_kind = c["loss"] if c["loss"] != "auto" else ("ce" if data.n_items <= 20000 else "sampled")
        seqs = [s for s in data.train_seqs() if len(s) >= 2]
        inp = left_pad([s[:-1] for s in seqs], c["max_len"])
        tgt = left_pad([s[1:] for s in seqs], c["max_len"])
        self.net = SASRecNet(data.n_items, c["dim"], c["layers"], c["heads"], c["max_len"], c["dropout"]).to(self.device)
        opt = torch.optim.AdamW(self.net.parameters(), lr=c["lr"], weight_decay=c["weight_decay"])
        gen = torch.Generator().manual_seed(self.seed)
        stopper = EarlyStopper(self.net, c["patience"])
        for _ in range(c["epochs"]):
            self.net.train()
            for idx in torch.randperm(len(inp), generator=gen).split(c["batch_size"]):
                x, y = inp[idx].to(self.device), tgt[idx].to(self.device)
                h = self.net(x)[y > 0]
                y = y[y > 0]
                if loss_kind == "ce":
                    logits = h @ self.net.item.weight.T
                    logits[:, 0] = -torch.inf
                    loss = F.cross_entropy(logits, y)
                else:
                    neg = torch.randint(1, data.n_items + 1, (c["n_neg"],), generator=gen).to(self.device)
                    pos_logit = (h * self.net.item(y)).sum(-1, keepdim=True)
                    neg_logit = h @ self.net.item(neg).T
                    neg_logit = neg_logit.masked_fill(neg[None, :] == y[:, None], -torch.inf)
                    loss = F.cross_entropy(torch.cat([pos_logit, neg_logit], 1),
                                           torch.zeros(len(y), dtype=torch.long, device=self.device))
                opt.zero_grad()
                loss.backward()
                opt.step()
            stopper.update(val_fn())
            if stopper.stop():
                break
        info = stopper.restore()
        info["loss"] = loss_kind
        return info

    @torch.no_grad()
    def score(self, users, histories):
        self.net.eval()
        x = left_pad(histories, self.cfg["max_len"]).to(self.device)
        return self.net(x)[:, -1] @ self.net.item.weight.T
