"""Benchmark suites: one call runs a method on fixed datasets and seeds and places it among the baselines."""
from __future__ import annotations

from typing import Dict, List, Optional

from .board import aggregate, collect
from .run import run_one

SUITES: Dict[str, Dict] = {
    "smoke": {"datasets": ["synthetic"], "seeds": [1], "about": "seconds on CPU; checks that a model runs end to end"},
    "ml1m": {"datasets": ["ml1m"], "seeds": [1, 2, 3], "about": "MovieLens-1M, 3 seeds"},
    "standard": {"datasets": ["ml1m", "mind"], "seeds": [1, 2, 3], "about": "movies and news, 3 seeds each"},
}
BASELINES = ["pop", "itemknn", "bpr", "sasrec"]


def run_suite(spec: str, suite: str, device: str = "cpu", overrides: Optional[Dict] = None,
              with_baselines: bool = False, val_users: Optional[int] = None, log=print) -> Dict:
    if suite not in SUITES:
        raise KeyError(f"unknown suite {suite!r}; known: {sorted(SUITES)}")
    s = SUITES[suite]
    specs: List[str] = ([b for b in BASELINES if b != spec] if with_baselines else []) + [spec]
    model_names = []
    for sp in specs:
        for ds in s["datasets"]:
            for seed in s["seeds"]:
                rec = run_one(ds, sp, overrides if sp == spec else None, seed, device, val_users=val_users)
                log(f"{ds} {rec['model']} s{seed} [{rec['config_hash']}] test ndcg@10={rec['test']['ndcg@10']:.4f}")
        model_names.append(rec["model"])
    table = aggregate(collect(), "test", s["datasets"])
    return {"suite": suite, "spec": spec, "model": model_names[-1], "seeds": s["seeds"], "leaderboard": table}
