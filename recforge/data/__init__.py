"""Dataset registry. `load(name)` returns a cached SeqData, building it from raw files on first use."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Dict

from .. import PROTOCOL_VERSION
from .schema import SeqData

ROOT = Path(__file__).resolve().parents[2]  # the code checkout, used for the git commit in records
HOME = Path(os.environ.get("RECFORGE_HOME", ROOT))  # workspace: data/, runs/, sessions/
RAW_DIR = Path(os.environ.get("RECFORGE_RAW", HOME / "data" / "raw"))
CACHE_DIR = HOME / "data" / "cache"
DATA_VERSION = "d2"  # cache layout: d2 adds timestamps


def _ml1m() -> SeqData:
    from .movielens import build_ml1m
    return build_ml1m(RAW_DIR / "ml-1m")


def _mind() -> SeqData:
    from .mind import build_mind
    return build_mind(RAW_DIR / "mind")


def _amazon(name: str) -> Callable[[], SeqData]:
    def build() -> SeqData:
        from .amazon import build_amazon
        return build_amazon(RAW_DIR / "amazon2014", name)
    return build


BUILDERS: Dict[str, Callable[[], SeqData]] = {"ml1m": _ml1m, "mind": _mind,
                                              **{n: _amazon(n) for n in ("beauty", "sports", "toys")}}


def load(name: str) -> SeqData:
    if name.startswith("synthetic"):
        from .synthetic import make_synthetic
        return make_synthetic()
    if name not in BUILDERS:
        raise KeyError(f"unknown dataset {name!r}; known: {sorted(BUILDERS)} or 'synthetic'")
    path = CACHE_DIR / f"{name}.{PROTOCOL_VERSION}.{DATA_VERSION}.npz"
    if path.exists():
        return SeqData.load(path)
    data = BUILDERS[name]()
    data.save(path)
    return data
