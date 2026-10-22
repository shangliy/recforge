"""Random search over a declared search space: the null baseline every evolver should beat at equal budget.

A space maps a config key to a list of choices, or to {"log": [lo, hi]}, {"uniform": [lo, hi]} or
{"int": [lo, hi]}. A model can declare its own as the class attribute SEARCH_SPACE; otherwise the
built-in space below is used, and `--evolver-set space={...}` replaces either.
"""
from __future__ import annotations

import json
import math
import random
from typing import Dict

from ..models import get
from .base import Context, Evolver

_SEQ = {"dim": [32, 64, 128], "layers": [1, 2, 3], "dropout": [0.1, 0.2, 0.3, 0.5],
        "lr": {"log": [3e-4, 3e-3]}, "weight_decay": [0.0, 1e-5, 1e-4]}
SEARCH_SPACES: Dict[str, Dict] = {
    "itemknn": {"k": [10, 25, 50, 100, 200, 400], "shrink": [0.0, 1.0, 10.0, 100.0]},
    "bpr": {"dim": [32, 64, 128], "lr": {"log": [1e-4, 1e-2]}, "l2": {"log": [1e-7, 1e-3]}},
    "sasrec": {**_SEQ, "heads": [1, 2], "ffn_dim": [64, 128, 256]},
    "hstu": {"layers": [2, 4], "dropout": [0.1, 0.2, 0.3, 0.5], "lr": {"log": [3e-4, 3e-3]},
             "temperature": [0.03, 0.05, 0.1]},
    "markov": {"smoothing": {"log": [1e-3, 10.0]}},
}


def space_for(spec: str) -> Dict:
    cls = get(spec)
    space = getattr(cls, "SEARCH_SPACE", None) or SEARCH_SPACES.get(cls.name)
    if not space:
        raise KeyError(f"no search space for {cls.name!r}: give one with --evolver-set space={{...}} "
                       f"or a SEARCH_SPACE class attribute on the model")
    return space


def sample(space: Dict, rng: random.Random) -> Dict:
    out = {}
    for k, v in space.items():
        if isinstance(v, (list, tuple)):
            out[k] = rng.choice(list(v))
        elif isinstance(v, dict) and "log" in v:
            lo, hi = v["log"]
            out[k] = float(f"{math.exp(rng.uniform(math.log(lo), math.log(hi))):.3g}")
        elif isinstance(v, dict) and "uniform" in v:
            out[k] = float(f"{rng.uniform(*v['uniform']):.3g}")
        elif isinstance(v, dict) and "int" in v:
            out[k] = rng.randint(*v["int"])
        else:
            raise ValueError(f"search space entry {k}: {v!r} is not a list or a log/uniform/int range")
    return out


class RandomSearch(Evolver):
    name = "random"
    DEFAULTS = {"space": None, "start_from_defaults": True, "max_repeats": 50}

    def run(self, ctx: Context) -> Dict:
        space = self.cfg["space"] or space_for(ctx.base)
        rng = random.Random(self.seed)
        seen, repeats = set(), 0
        if self.cfg["start_from_defaults"]:
            self.trial(ctx, None, note="random: defaults")
            seen.add("{}")
        while not self.spent(ctx) and repeats < self.cfg["max_repeats"]:
            cfg = sample(space, rng)
            key = json.dumps(cfg, sort_keys=True)
            if key in seen:  # finite spaces run out before the budget does
                repeats += 1
                continue
            seen.add(key)
            repeats = 0
            self.trial(ctx, cfg, note=f"random: {key}")
        return {"space": space, "distinct_configs": len(seen)}
