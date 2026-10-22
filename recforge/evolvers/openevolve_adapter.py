"""OpenEvolve (open AlphaEvolve) as the evolver: LLM-proposed code edits, scored by recforge session trials.

recforge writes two files into the session's work directory:

    openevolve/initial_program.py   a recforge model; the EVOLVE-BLOCK is what OpenEvolve may rewrite
    openevolve/evaluator.py         evaluate(program_path) runs `recforge session trial` on the program
                                    and returns validation NDCG@10 as combined_score

and then runs OpenEvolve on them. Every evaluated program is one session trial, so the budget, the sealed
test and the single finalize apply as for any evolver. Each program is copied to openevolve/programs/ so
the trial's model file outlives OpenEvolve's temp files.

Needs `pip install openevolve` and an OpenEvolve config with your LLM endpoint
(`--evolver-set config=path/to/config.yaml`); recforge itself calls no LLM. The OpenEvolve call follows
the API in its README (OpenEvolve(initial_program_path, evaluation_file, config_path, output_dir) and
`await run(iterations=N)`); check it against the version you install.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Dict

from .. import evolve
from ..models import MODELS, get
from .base import Context, Evolver

BUILTIN_PROGRAM = '''"""recforge model evolved by OpenEvolve, starting from the built-in {base!r}."""
from recforge.models import get

Base = get({base!r})


# EVOLVE-BLOCK-START
class Evolved(Base):
    name = "evolved_{base}"
    DEFAULTS = dict(Base.DEFAULTS)
# EVOLVE-BLOCK-END
'''

EVALUATOR = '''"""OpenEvolve evaluator written by recforge: one recforge session trial per program."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

SESSION, PYTHON, DEVICE, CLASS = {session!r}, {python!r}, {device!r}, {cls!r}
PROGRAMS, HOME = {programs!r}, {home!r}


def evaluate(program_path):
    src = open(program_path).read()
    keep = os.path.join(PROGRAMS, hashlib.sha1(src.encode()).hexdigest()[:10] + ".py")
    shutil.copy(program_path, keep)
    p = subprocess.run([PYTHON, "-m", "recforge", "session", "trial", SESSION, "--model", keep + ":" + CLASS,
                        "--device", DEVICE, "--note", "openevolve " + os.path.basename(keep), "--json"],
                       capture_output=True, text=True, env={{**os.environ, "RECFORGE_HOME": HOME}})
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {{"error": "no JSON", "message": p.stderr[-2000:]}}
    if "error" in out:  # a broken program or a spent budget scores zero
        print("recforge trial failed: " + out["message"], file=sys.stderr)
        return {{"combined_score": 0.0}}
    v = out["trial"]["val"]
    return {{"combined_score": v["ndcg@10"], "val_ndcg@10": v["ndcg@10"], "val_hr@10": v["hr@10"]}}
'''


class OpenEvolveAdapter(Evolver):
    name = "openevolve"
    DEFAULTS = {"config": None, "iterations": None}

    def prepare(self, ctx: Context) -> Dict[str, Path]:
        d = ctx.workdir / "openevolve"
        (d / "programs").mkdir(parents=True, exist_ok=True)
        if ctx.base in MODELS:
            program, cls = BUILTIN_PROGRAM.format(base=ctx.base), "Evolved"
        else:
            path, _, cls = ctx.base.rpartition(":")
            get(ctx.base)  # fail early on a bad spec
            program = "# EVOLVE-BLOCK-START\n" + Path(path).read_text() + "\n# EVOLVE-BLOCK-END\n"
        init, ev = d / "initial_program.py", d / "evaluator.py"
        init.write_text(program)
        ev.write_text(EVALUATOR.format(session=ctx.session, python=sys.executable, device=ctx.device, cls=cls,
                                       programs=str(d / "programs"), home=str(evolve.SESSIONS_DIR.parent)))
        return {"initial_program": init, "evaluator": ev, "output": d / "output"}

    def run(self, ctx: Context) -> Dict:
        files = self.prepare(ctx)
        try:
            from openevolve import OpenEvolve
        except ImportError as e:
            raise RuntimeError(f"the openevolve evolver needs OpenEvolve: pip install openevolve "
                               f"(files are ready in {files['initial_program'].parent})") from e
        s = evolve.load(ctx.session)
        iterations = self.cfg["iterations"] or max(s["budget"]["trials"] - s["used"]["trials"] - 1, 1)
        evo = OpenEvolve(initial_program_path=str(files["initial_program"]), evaluation_file=str(files["evaluator"]),
                         config_path=self.cfg["config"], output_dir=str(files["output"]))
        best = asyncio.run(evo.run(iterations=iterations))
        return {"iterations": iterations, "output": str(files["output"]),
                "best_metrics": getattr(best, "metrics", None)}
