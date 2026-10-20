"""Model registry. Add a model by subclassing Recommender and listing it here."""
from __future__ import annotations

from typing import Dict, Type

from .base import Recommender
from .bpr import BPR
from .classic import ItemKNN, Pop
from .sasrec import SASRec

MODELS: Dict[str, Type[Recommender]] = {m.name: m for m in (Pop, ItemKNN, BPR, SASRec)}


def get(name: str) -> Type[Recommender]:
    if name not in MODELS:
        raise KeyError(f"unknown model {name!r}; known: {sorted(MODELS)}")
    return MODELS[name]
