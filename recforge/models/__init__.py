"""Model registry and loader.

A model spec is either a built-in name ("sasrec") or a file reference
("path/to/my_model.py:MyModel"), so a method can be benchmarked without
touching this package. The source file's hash is part of every result key:
edit the code and the next run is a new record.
"""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Dict, Tuple, Type

from .base import Recommender
from .bpr import BPR
from .classic import ItemKNN, Pop
from .sasrec import SASRec

MODELS: Dict[str, Type[Recommender]] = {m.name: m for m in (Pop, ItemKNN, BPR, SASRec)}


def _from_file(spec: str) -> Type[Recommender]:
    path, _, cls_name = spec.rpartition(":")
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"model file {path} not found (spec {spec!r})")
    mod_name = "recforge_user_" + hashlib.sha1(str(path).encode()).hexdigest()[:8]
    mod_spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(mod_spec)
    sys.modules[mod_name] = module
    mod_spec.loader.exec_module(module)
    cls = getattr(module, cls_name, None)
    if not (isinstance(cls, type) and issubclass(cls, Recommender)):
        raise TypeError(f"{spec!r}: {cls_name} must be a subclass of recforge.models.base.Recommender")
    if cls.name in MODELS or cls.name == Recommender.name:
        raise ValueError(f"{spec!r}: set a unique class attribute `name` (got {cls.name!r})")
    return cls


def get(spec: str) -> Type[Recommender]:
    if spec in MODELS:
        return MODELS[spec]
    if ":" in spec and spec.rpartition(":")[0].endswith(".py"):
        return _from_file(spec)
    raise KeyError(f"unknown model {spec!r}; built-ins: {sorted(MODELS)}, or give path/to/file.py:ClassName")


def describe(spec: str) -> Tuple[Type[Recommender], str]:
    """(class, short hash of the file that defines it)."""
    cls = get(spec)
    src = Path(inspect.getsourcefile(cls)).read_bytes()
    return cls, hashlib.sha1(src).hexdigest()[:10]
