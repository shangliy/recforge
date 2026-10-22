"""Evolvers: searchers that improve a model inside a budgeted evolve session.

    run_evolver("random", "synthetic", "itemknn", max_trials=10)   -> summary with the val->test gap

An evolver spec is a built-in name or "path/to/file.py:Class" (a subclass of evolvers.base.Evolver).
Every evolver gets the same session rules, so their summaries are comparable.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import time
from pathlib import Path
from typing import Callable, Dict, Optional, Type

from .. import evolve
from .base import Context, Evolver
from .cli_agent import CLIAgent
from .openevolve_adapter import OpenEvolveAdapter
from .random_search import RandomSearch

EVOLVERS: Dict[str, Type[Evolver]] = {e.name: e for e in (RandomSearch, CLIAgent, OpenEvolveAdapter)}
GAP_KEYS = ("hr@10", "ndcg@10", "hr@20", "ndcg@20", "mrr@100")


def get(spec: str) -> Type[Evolver]:
    if spec in EVOLVERS:
        return EVOLVERS[spec]
    path, _, cls_name = spec.rpartition(":")
    if not path.endswith(".py"):
        raise KeyError(f"unknown evolver {spec!r}; built-ins: {sorted(EVOLVERS)}, or give path/to/file.py:ClassName")
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"evolver file {path} not found (spec {spec!r})")
    mod_name = "recforge_evolver_" + hashlib.sha1(str(path).encode()).hexdigest()[:8]
    mod_spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(mod_spec)
    sys.modules[mod_name] = module
    mod_spec.loader.exec_module(module)
    cls = getattr(module, cls_name, None)
    if not (isinstance(cls, type) and issubclass(cls, Evolver)):
        raise TypeError(f"{spec!r}: {cls_name} must be a subclass of recforge.evolvers.base.Evolver")
    return cls


def best_trial(session: Dict) -> Optional[Dict]:
    return max(session["trials"], key=lambda t: t["val"]["ndcg@10"], default=None)


def run_evolver(evolver: str, dataset: str, base: str, max_trials: int = 20, max_minutes: float = 120.0,
                session: Optional[str] = None, evolver_cfg: Optional[Dict] = None, device: str = "cpu",
                seed: int = 1, preset: Optional[str] = None, val_users: Optional[int] = None,
                log: Callable[[str], None] = print) -> Dict:
    """Create a session, let the evolver spend its budget, finalize, and report the val->test gap."""
    cls = get(evolver)
    ev = cls(evolver_cfg, seed=seed)  # bad settings fail before a session exists
    session = session or f"{cls.name}-{dataset}-{time.strftime('%Y%m%d-%H%M%S')}"
    evolve.create(session, dataset, max_trials, max_minutes, seed, evolver=evolver)
    ctx = Context(session, base, device, preset, val_users, log)
    info = ev.run(ctx) or {}
    s = evolve.load(session)
    if s["final"] is None:
        best = best_trial(s)
        if best is None:
            raise RuntimeError(f"evolver {cls.name} ran no trials in session {session!r}")
        evolve.finalize(session, best["id"])
        s, by = evolve.load(session), "recforge (best validation ndcg@10)"
    else:
        by = "evolver"
    t = next(t for t in s["trials"] if t["id"] == s["final"]["trial"])
    test = s["final"]["test"]
    return {"session": session, "evolver": evolver, "dataset": dataset, "base": base, "used": s["used"],
            "budget": s["budget"], "finalized_by": by, "final_trial": t["id"], "model": t["model"],
            "spec": t["spec"], "config": t["config"], "val": t["val"], "test": test,
            "val_test_gap": {k: round(test[k] - t["val"][k], 4) for k in GAP_KEYS if k in test and k in t["val"]},
            "best_val_trial": best_trial(s)["id"], "evolver_info": info}
