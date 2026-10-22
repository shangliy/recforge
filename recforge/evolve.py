"""Evolve sessions: a budgeted search where the searcher sees validation only.

    create(name, dataset, max_trials, max_minutes, evolver=None)
    trial(name, spec, overrides)   -> validation metrics; counts against the budget
    finalize(name, trial_id)       -> test metrics of one chosen trial; the session is then closed

The searcher can be a person, a script or a coding agent (see recforge.evolvers);
recforge enforces the rules, not the prompt. Test metrics are computed with every trial but sealed,
so finalize does not retrain. A finalized trial is copied to the main runs
directory and appears on the leaderboard like any other record, with its
session attached.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, Optional

from .data import HOME
from .run import RUNS_DIR, record_path, run_one

SESSIONS_DIR = HOME / "sessions"


def _path(name: str) -> Path:
    return SESSIONS_DIR / name / "session.json"


def _save(s: Dict) -> None:
    _path(s["name"]).write_text(json.dumps(s, indent=1))


def load(name: str) -> Dict:
    p = _path(name)
    if not p.exists():
        raise FileNotFoundError(f"no session {name!r}")
    return json.loads(p.read_text())


def create(name: str, dataset: str, max_trials: int = 20, max_minutes: float = 120.0, seed: int = 1,
           evolver: Optional[str] = None) -> Dict:
    if _path(name).exists():
        raise FileExistsError(f"session {name!r} exists")
    _path(name).parent.mkdir(parents=True)
    s = {"name": name, "dataset": dataset, "seed": seed, "evolver": evolver,
         "budget": {"trials": max_trials, "minutes": max_minutes}, "used": {"trials": 0, "minutes": 0.0},
         "trials": [], "final": None, "created": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    _save(s)
    return s


def trial(name: str, spec: str, overrides: Optional[Dict] = None, device: str = "cpu",
          val_users: Optional[int] = None, note: str = "", preset: Optional[str] = None) -> Dict:
    s = load(name)
    if s["final"] is not None:
        raise PermissionError(f"session {name!r} is finalized")
    if s["used"]["trials"] >= s["budget"]["trials"] or s["used"]["minutes"] >= s["budget"]["minutes"]:
        raise PermissionError(f"session {name!r} budget spent: {s['used']} of {s['budget']}")
    rec = run_one(s["dataset"], spec, overrides, s["seed"], device, runs_dir=SESSIONS_DIR / name / "records",
                  val_users=val_users, sealed=True, preset=preset)
    t = {"id": len(s["trials"]) + 1, "model": rec["model"], "spec": spec, "config": rec["config"],
         "config_hash": rec["config_hash"], "code_hash": rec["code_hash"], "val": rec["val"],
         "minutes": round(rec["seconds"] / 60, 2), "note": note}
    s["trials"].append(t)
    s["used"]["trials"] += 1
    s["used"]["minutes"] = round(s["used"]["minutes"] + t["minutes"], 2)
    _save(s)
    return {"trial": t, "used": s["used"], "budget": s["budget"]}


def finalize(name: str, trial_id: int) -> Dict:
    s = load(name)
    if s["final"] is not None:
        raise PermissionError(f"session {name!r} already finalized on trial {s['final']['trial']}")
    t = next((t for t in s["trials"] if t["id"] == trial_id), None)
    if t is None:
        raise KeyError(f"session {name!r} has no trial {trial_id}")
    src = record_path(SESSIONS_DIR / name / "records", s["dataset"], t["model"], t["config_hash"], s["seed"])
    test = json.loads(src.with_suffix(".sealed").read_text())
    s["final"] = {"trial": trial_id, "test": test, "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    _save(s)
    rec = json.loads(src.read_text())
    rec["test"], rec["evolve_session"] = test, {"name": name, "trial": trial_id, "evolver": s.get("evolver"),
                                                "used": s["used"], "budget": s["budget"]}
    dst = record_path(RUNS_DIR, s["dataset"], t["model"], t["config_hash"], s["seed"])
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(rec, indent=1))
    return {"session": name, "trial": t, "test": test, "used": s["used"]}
