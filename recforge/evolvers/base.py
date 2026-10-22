"""Evolver interface. An evolver searches inside one evolve session and sees validation metrics only.

It does not need to call finalize: `recforge.evolvers.run_evolver` creates the session, hands the evolver a
Context, and afterwards finalizes the trial with the best validation NDCG@10, unless the evolver (or the
agent it drives) has finalized one itself. Budget, sealing and the leaderboard entry are enforced by
recforge.evolve, so every evolver is held to the same rules.

A proposal is a config override (`self.trial(ctx, {"lr": 3e-3})`), a new model file (write it under
`ctx.workdir` and pass `spec="path.py:Class"`), or both.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional

from .. import evolve


@dataclass
class Context:
    session: str
    base: str                       # model spec the search starts from
    device: str = "cpu"
    preset: Optional[str] = None
    val_users: Optional[int] = None
    log: Callable[[str], None] = print

    @property
    def workdir(self) -> Path:
        """Where an evolver may write model files and logs; kept with the session."""
        d = evolve.SESSIONS_DIR / self.session / "work"
        d.mkdir(parents=True, exist_ok=True)
        return d


class Evolver:
    name = "base"
    DEFAULTS: Dict = {}

    def __init__(self, cfg: Optional[Dict] = None, seed: int = 1):
        unknown = set(cfg or {}) - set(self.DEFAULTS)
        if unknown:
            raise KeyError(f"evolver {self.name} has no settings {sorted(unknown)}; known: {sorted(self.DEFAULTS)}")
        self.cfg = {**self.DEFAULTS, **(cfg or {})}
        self.seed = seed

    def run(self, ctx: Context) -> Dict:
        """Spend the session's budget through self.trial; return anything worth logging."""
        raise NotImplementedError

    def trial(self, ctx: Context, overrides: Optional[Dict] = None, spec: Optional[str] = None,
              note: str = "") -> Optional[Dict]:
        """Run one trial. Returns it (validation metrics only), or None once the budget is spent."""
        if self.spent(ctx):
            return None
        r = evolve.trial(ctx.session, spec or ctx.base, overrides, ctx.device, ctx.val_users,
                         note or self.name, ctx.preset)
        t = r["trial"]
        ctx.log(f"[{self.name}] trial {t['id']} val ndcg@10={t['val']['ndcg@10']:.4f}  {t['note']}")
        return t

    @staticmethod
    def spent(ctx: Context) -> bool:
        s = evolve.load(ctx.session)
        return (s["final"] is not None or s["used"]["trials"] >= s["budget"]["trials"]
                or s["used"]["minutes"] >= s["budget"]["minutes"])
