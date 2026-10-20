"""BPR matrix factorisation (Rendle et al., 2009) with uniform negative sampling."""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from .base import EarlyStopper, Recommender


class BPR(Recommender):
    name = "bpr"
    DEFAULTS = {"dim": 64, "lr": 1e-3, "l2": 1e-5, "batch_size": 4096, "epochs": 200, "patience": 5}

    def fit(self, data, val_fn):
        c = self.cfg
        seqs = data.train_seqs()
        users = torch.as_tensor(np.repeat(np.arange(len(seqs)), [len(s) for s in seqs]))
        items = torch.as_tensor(np.concatenate(seqs))
        self.net = torch.nn.ModuleDict({"u": torch.nn.Embedding(data.n_users, c["dim"]),
                                        "i": torch.nn.Embedding(data.n_items + 1, c["dim"])}).to(self.device)
        for emb in self.net.values():
            torch.nn.init.normal_(emb.weight, std=0.1)
        opt = torch.optim.Adam(self.net.parameters(), lr=c["lr"])
        gen = torch.Generator().manual_seed(self.seed)
        stopper = EarlyStopper(self.net, c["patience"])
        for _ in range(c["epochs"]):
            self.net.train()
            perm = torch.randperm(len(users), generator=gen)
            for lo in range(0, len(perm), c["batch_size"]):
                idx = perm[lo:lo + c["batch_size"]]
                u, p = users[idx].to(self.device), items[idx].to(self.device)
                n = torch.randint(1, data.n_items + 1, (len(idx),), generator=gen).to(self.device)
                eu, ep, en = self.net["u"](u), self.net["i"](p), self.net["i"](n)
                loss = -F.logsigmoid((eu * (ep - en)).sum(-1)).mean()
                loss = loss + c["l2"] * (eu.pow(2).sum() + ep.pow(2).sum() + en.pow(2).sum()) / len(idx)
                opt.zero_grad()
                loss.backward()
                opt.step()
            stopper.update(val_fn())
            if stopper.stop():
                break
        return stopper.restore()

    @torch.no_grad()
    def score(self, users, histories):
        self.net.eval()
        u = self.net["u"](torch.as_tensor(users, device=self.device))
        return u @ self.net["i"].weight.T
