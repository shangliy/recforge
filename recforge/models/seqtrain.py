"""Shared training for next-item sequence encoders (SASRec, HSTU, ...).

A subclass builds a network with
    encode(items, times) -> (B, L, D)   items/times left-padded (B, L); 0 = pad
    item                                 nn.Embedding(n_items + 1, D, padding_idx=0)
and inherits fit/score. Every position predicts the next item.

Loss settings (all in the model's config, so all are logged):
    loss         "ce": softmax over the whole catalogue; "sampled": n_neg uniform negatives;
                 "auto": ce up to 20k items, else sampled
    neg_sharing  "batch": one negative set for the batch; "position": a fresh set per position
                 (the HSTU repository's LocalNegativesSampler). Negatives equal to the target are masked.
    temperature  logits are divided by it
    l2norm       L2-normalise sequence outputs and item embeddings before the dot product
"""
from __future__ import annotations

from typing import List, Optional

import numpy as np
import torch
import torch.nn.functional as F

from .base import EarlyStopper, Recommender

LOSS_DEFAULTS = {"loss": "auto", "n_neg": 512, "neg_sharing": "batch", "temperature": 1.0, "l2norm": False}


def left_pad(seqs: List[np.ndarray], max_len: int) -> torch.Tensor:
    out = np.zeros((len(seqs), max_len), dtype=np.int64)
    for i, s in enumerate(seqs):
        s = s[-max_len:]
        if len(s):
            out[i, -len(s):] = s
    return torch.as_tensor(out)


def per_position_logits(h: torch.Tensor, emb: torch.Tensor, neg: torch.Tensor, gather: bool) -> torch.Tensor:
    """(N, R) logits of h (N, D) against row-specific negatives neg (N, R).

    gather=True scores the whole catalogue and picks columns: the same numbers with less memory
    when the catalogue is smaller than R * D.
    """
    if gather:
        return (h @ emb.T).gather(1, neg)
    return torch.einsum("nd,nrd->nr", h, emb[neg])


class SeqModel(Recommender):
    def build_net(self, data) -> torch.nn.Module:
        raise NotImplementedError

    def _norm(self, x: torch.Tensor) -> torch.Tensor:
        return F.normalize(x, dim=-1, eps=1e-6) if self.cfg["l2norm"] else x

    def _loss(self, h: torch.Tensor, y: torch.Tensor, kind: str, n_items: int, gen: torch.Generator) -> torch.Tensor:
        c, emb = self.cfg, self.net.item.weight
        h = self._norm(h)
        if kind == "ce":
            logits = h @ self._norm(emb).T / c["temperature"]
            logits[:, 0] = -torch.inf
            return F.cross_entropy(logits, y)
        shape = (c["n_neg"],) if c["neg_sharing"] == "batch" else (len(y), c["n_neg"])
        neg = torch.randint(1, n_items + 1, shape, generator=gen).to(h.device)
        pos = (h * self._norm(emb[y])).sum(-1, keepdim=True)
        if c["neg_sharing"] == "batch":
            negl = h @ self._norm(emb[neg]).T
            hit = neg[None, :] == y[:, None]
        else:
            negl = per_position_logits(h, self._norm(emb), neg, gather=emb.shape[0] < c["n_neg"] * emb.shape[1])
            hit = neg == y[:, None]
        logits = torch.cat([pos, negl.masked_fill(hit, -torch.inf)], 1) / c["temperature"]
        return F.cross_entropy(logits, torch.zeros(len(y), dtype=torch.long, device=h.device))

    def fit(self, data, val_fn):
        c = self.cfg
        kind = c["loss"] if c["loss"] != "auto" else ("ce" if data.n_items <= 20000 else "sampled")
        pairs = [(s, t) for s, t in zip(data.train_seqs(), data.train_times()) if len(s) >= 2]
        inp = left_pad([s[:-1] for s, _ in pairs], c["max_len"])
        inp_t = left_pad([t[:-1] for _, t in pairs], c["max_len"])
        tgt = left_pad([s[1:] for s, _ in pairs], c["max_len"])
        self.net = self.build_net(data).to(self.device)
        opt = torch.optim.AdamW(self.net.parameters(), lr=c["lr"], weight_decay=c["weight_decay"])
        gen = torch.Generator().manual_seed(self.seed)
        stopper = EarlyStopper(self.net, c["patience"])
        for _ in range(c["epochs"]):
            self.net.train()
            for idx in torch.randperm(len(inp), generator=gen).split(c["batch_size"]):
                x, xt, y = inp[idx].to(self.device), inp_t[idx].to(self.device), tgt[idx].to(self.device)
                h = self.net.encode(x, xt)[y > 0]
                loss = self._loss(h, y[y > 0], kind, data.n_items, gen)
                opt.zero_grad()
                loss.backward()
                opt.step()
            stopper.update(val_fn())
            if stopper.stop():
                break
        info = stopper.restore()
        info["loss"] = kind
        return info

    @torch.no_grad()
    def score(self, users, histories, times: Optional[List[np.ndarray]] = None):
        self.net.eval()
        L = self.cfg["max_len"]
        x = left_pad(histories, L).to(self.device)
        xt = (left_pad(times, L) if times is not None else torch.zeros_like(x.cpu())).to(self.device)
        h = self._norm(self.net.encode(x, xt)[:, -1])
        return h @ self._norm(self.net.item.weight).T
