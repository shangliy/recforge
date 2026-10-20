"""Run one (dataset, model, config, seed) and write a result record.

A record is the unit of the leaderboard. It carries everything needed to trust
or rerun it: the resolved config and its hash, protocol version, code commit,
validation and test metrics, and wall time. Records are written once; rerunning
the same key returns the stored record unless force=True.
"""
from __future__ import annotations

import hashlib
import json
import platform
import random
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import torch

from . import PROTOCOL_VERSION
from .data import ROOT, load
from .eval import evaluate
from .models import get

RUNS_DIR = ROOT / "runs"


def resolve_config(model: str, overrides: Optional[Dict] = None) -> Dict:
    cls = get(model)
    unknown = set(overrides or {}) - set(cls.DEFAULTS)
    if unknown:
        raise KeyError(f"{model} has no config keys {sorted(unknown)}; known: {sorted(cls.DEFAULTS)}")
    return {**cls.DEFAULTS, **(overrides or {})}


def config_hash(dataset: str, model: str, cfg: Dict) -> str:
    key = json.dumps({"protocol": PROTOCOL_VERSION, "dataset": dataset, "model": model, "cfg": cfg}, sort_keys=True)
    return hashlib.sha1(key.encode()).hexdigest()[:10]


def _git_commit() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "recforge"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return (sha or "uncommitted") + ("+dirty" if dirty else "")
    except OSError:
        return "unknown"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def run_one(dataset: str, model: str, overrides: Optional[Dict] = None, seed: int = 1, device: str = "cpu",
            runs_dir: Path = RUNS_DIR, force: bool = False, val_users: Optional[int] = None) -> Dict:
    cfg = resolve_config(model, overrides)
    h = config_hash(dataset, model, cfg)
    path = runs_dir / dataset / model / f"{h}-s{seed}.json"
    if path.exists() and not force:
        return json.loads(path.read_text())

    data = load(dataset)
    set_seed(seed)
    rec = get(model)(cfg, seed, device)
    val_fn = lambda: evaluate(rec, data, "val", max_users=val_users)["ndcg@10"]
    t0 = time.time()
    fit_info = rec.fit(data, val_fn)
    fit_s = time.time() - t0
    t0 = time.time()
    val, test = evaluate(rec, data, "val"), evaluate(rec, data, "test")
    record = {
        "dataset": dataset, "model": model, "seed": seed, "config": cfg, "config_hash": h,
        "protocol": PROTOCOL_VERSION, "data_stats": data.stats(),
        "val": val, "test": test, "fit": fit_info,
        "fit_seconds": round(fit_s, 1), "eval_seconds": round(time.time() - t0, 1),
        "device": device if device == "cpu" else torch.cuda.get_device_name(torch.device(device)),
        "commit": _git_commit(), "torch": torch.__version__, "python": platform.python_version(),
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=1))
    return record
