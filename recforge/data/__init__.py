"""Dataset registry. `load(name)` returns a cached SeqData, building it from raw files on first use."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Dict

from .. import PROTOCOL_VERSION
from .schema import SeqData

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = Path(os.environ.get("RECFORGE_RAW", ROOT / "data" / "raw"))
CACHE_DIR = ROOT / "data" / "cache"


def _ml1m() -> SeqData:
    from .movielens import build_ml1m
    return build_ml1m(RAW_DIR / "ml-1m")


def _mind() -> SeqData:
    from .mind import build_mind
    return build_mind(RAW_DIR / "mind")


BUILDERS: Dict[str, Callable[[], SeqData]] = {"ml1m": _ml1m, "mind": _mind}


def load(name: str) -> SeqData:
    if name.startswith("synthetic"):
        from .synthetic import make_synthetic
        return make_synthetic()
    if name not in BUILDERS:
        raise KeyError(f"unknown dataset {name!r}; known: {sorted(BUILDERS)} or 'synthetic'")
    path = CACHE_DIR / f"{name}.{PROTOCOL_VERSION}.npz"
    if path.exists():
        return SeqData.load(path)
    data = BUILDERS[name]()
    data.save(path)
    return data
