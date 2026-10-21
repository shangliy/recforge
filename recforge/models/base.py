"""The model contract.

Every recommender, from popularity to a generative model, implements two calls:

    fit(data, val_fn) -> dict     train on data.train_seqs(); val_fn() returns validation NDCG@10
                                  for early stopping. Leave the model in its best-validation state.
    score(users, histories)       (B, n_items + 1) scores; column 0 is padding and ignored.

The runner never shows a model the test targets: fit sees train sequences and
validation scores only, and test histories end before the test item.
"""
from __future__ import annotations

import copy
from typing import Callable, Dict, List, Optional

import numpy as np
import torch

from ..data.schema import SeqData

ValFn = Callable[[], float]


class Recommender:
    name = "base"
    DEFAULTS: Dict = {}
    PRESETS: Dict[str, Dict] = {}  # named config bundles, e.g. a paper's published setup

    def __init__(self, cfg: Dict, seed: int, device: str):
        self.cfg, self.seed, self.device = cfg, seed, device

    def fit(self, data: SeqData, val_fn: Optional[ValFn]) -> Dict:
        raise NotImplementedError

    def score(self, users: np.ndarray, histories: List[np.ndarray]):
        raise NotImplementedError


class EarlyStopper:
    """Keeps the best state_dict by validation score; stop() is True after `patience` evals without gain."""

    def __init__(self, module: torch.nn.Module, patience: int):
        self.module, self.patience = module, patience
        self.best, self.best_state, self.bad, self.history = -1.0, None, 0, []

    def update(self, score: float) -> None:
        self.history.append(round(score, 5))
        if score > self.best:
            self.best, self.bad = score, 0
            self.best_state = copy.deepcopy(self.module.state_dict())
        else:
            self.bad += 1

    def stop(self) -> bool:
        return self.bad >= self.patience

    def restore(self) -> Dict:
        if self.best_state is not None:
            self.module.load_state_dict(self.best_state)
        return {"best_val_ndcg@10": self.best, "val_curve": self.history, "evals": len(self.history)}
