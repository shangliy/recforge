"""Run one (dataset, model, config, seed) and write a result record.

A record is the unit of the leaderboard. It carries everything needed to trust
or rerun it: the model spec and its source hash, the resolved config, protocol
version, code commit, validation and test metrics, and wall time. Records are
written once; rerunning the same key returns the stored record unless force=True.

With sealed=True (evolve sessions) the test metrics go to a separate file and
the returned record has none; the session reveals them once, at finalize.
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
from .data import HOME, ROOT, load
from .eval import metrics_from_lists
from .models import describe

RUNS_DIR = HOME / "runs"


def resolve_config(spec: str, overrides: Optional[Dict] = None, preset: Optional[str] = None) -> Dict:
    """DEFAULTS, then the named preset, then explicit overrides."""
    cls, _ = describe(spec)
    if preset is not None and preset not in cls.PRESETS:
        raise KeyError(f"{cls.name} has no preset {preset!r}; known: {sorted(cls.PRESETS)}")
    unknown = set(overrides or {}) - set(cls.DEFAULTS)
    if unknown:
        raise KeyError(f"{cls.name} has no config keys {sorted(unknown)}; known: {sorted(cls.DEFAULTS)}")
    return {**cls.DEFAULTS, **(cls.PRESETS.get(preset) or {}), **(overrides or {})}


def config_hash(dataset: str, model: str, code: str, cfg: Dict) -> str:
    key = json.dumps({"protocol": PROTOCOL_VERSION, "dataset": dataset, "model": model, "code": code, "cfg": cfg},
                     sort_keys=True)
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


def record_path(runs_dir: Path, dataset: str, model: str, h: str, seed: int) -> Path:
    return runs_dir / dataset / model / f"{h}-s{seed}.json"


def run_one(dataset: str, spec: str, overrides: Optional[Dict] = None, seed: int = 1, device: str = "cpu",
            runs_dir: Optional[Path] = None, force: bool = False, val_users: Optional[int] = None,
            sealed: bool = False, preset: Optional[str] = None) -> Dict:
    from .worker import train_and_rank

    runs_dir = RUNS_DIR if runs_dir is None else runs_dir
    cls, code = describe(spec)
    cfg = resolve_config(spec, overrides, preset)
    h = config_hash(dataset, cls.name, code, cfg)
    path = record_path(runs_dir, dataset, cls.name, h, seed)
    if path.exists() and not force:
        return json.loads(path.read_text())

    data = load(dataset)
    t0 = time.time()
    fit_info, val_lists, test_lists = train_and_rank(spec, cfg, seed, device, data, val_users)
    seconds = time.time() - t0
    _, val_t = data.split("val")
    _, test_t = data.split("test")
    test = metrics_from_lists(test_lists, test_t)
    record = {
        "dataset": dataset, "model": cls.name, "spec": spec, "code_hash": code, "seed": seed,
        "preset": preset, "config": cfg, "config_hash": h, "protocol": PROTOCOL_VERSION, "data_stats": data.stats(),
        "val": metrics_from_lists(val_lists, val_t), "test": None if sealed else test, "fit": fit_info,
        "seconds": round(seconds, 1),
        "device": device if device == "cpu" else torch.cuda.get_device_name(torch.device(device)),
        "commit": _git_commit(), "torch": torch.__version__, "python": platform.python_version(),
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=1))
    if sealed:
        path.with_suffix(".sealed").write_text(json.dumps(test))
    return record
