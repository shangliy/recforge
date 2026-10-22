"""Drive an external coding agent (Claude Code, Codex, ...) as the evolver.

recforge writes a prompt that explains the session, its budget and the trial commands, then runs the
agent command once with a timeout. The agent proposes trials itself through `recforge session trial`;
recforge counts and seals them like any other trial. The command is a shell string with placeholders:

    --agent-cmd 'claude -p "$(cat {prompt})" --permission-mode acceptEdits'
    --agent-cmd 'codex exec "$(cat {prompt})"'

{prompt}, {session}, {workdir}, {python} and {device} are filled in, and the same values are in the
environment as RECFORGE_PROMPT, RECFORGE_SESSION, RECFORGE_WORKDIR, RECFORGE_PYTHON, RECFORGE_DEVICE.
The agent runs with its own permissions on this machine: for an agent you do not trust, run it inside a
container (see docs/AGENTS.md, "What isolation does and does not cover").
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from typing import Dict

from .. import evolve
from ..data import ROOT
from .base import Context, Evolver

PROMPT = """You are improving a recommender inside a recforge evolve session.

session: {session}
dataset: {dataset} (protocol loo-2: leave-one-out, full-catalogue ranking)
starting model: {base}
budget: {trials} trials or {minutes} minutes of training, whichever runs out first
your working directory for new model files: {workdir}

Run a trial (validation metrics only; test metrics are sealed until the session is finalized):
  {python} -m recforge session trial {session} --model {base} --set key=value --note "why" --device {device} --json
  {python} -m recforge session trial {session} --model {workdir}/my_model.py:MyModel --note "why" --device {device} --json
See what you have tried:
  {python} -m recforge session status {session} --json

Write the hypothesis of each trial in --note. You may finalize one trial yourself with
  {python} -m recforge session finalize {session} --trial ID --json
otherwise recforge finalizes the trial with the best validation NDCG@10 when you stop.
Do not read files under data/ or sessions/ directly; work only through these commands.
{contract}"""


class CLIAgent(Evolver):
    name = "cli-agent"
    DEFAULTS = {"cmd": None, "timeout_minutes": None}

    def run(self, ctx: Context) -> Dict:
        if not self.cfg["cmd"]:
            raise ValueError("cli-agent needs a command: --agent-cmd 'claude -p \"$(cat {prompt})\"'")
        s = evolve.load(ctx.session)
        guide = ROOT / "docs" / "AGENTS.md"
        values = {"session": ctx.session, "workdir": str(ctx.workdir), "python": sys.executable,
                  "device": ctx.device}
        prompt = ctx.workdir / "PROMPT.md"
        prompt.write_text(PROMPT.format(
            **values, dataset=s["dataset"], base=ctx.base, trials=s["budget"]["trials"],
            minutes=s["budget"]["minutes"],
            contract=("\nThe model contract (docs/AGENTS.md):\n\n" + guide.read_text()) if guide.exists() else ""))
        values["prompt"] = str(prompt)
        env = {**os.environ, "RECFORGE_HOME": str(evolve.SESSIONS_DIR.parent),
               **{f"RECFORGE_{k.upper()}": v for k, v in values.items()}}
        timeout = self.cfg["timeout_minutes"] or 1.5 * s["budget"]["minutes"]
        cmd = self.cfg["cmd"]
        for k, v in values.items():  # plain replace, so shell ${VAR} in the command is left alone
            cmd = cmd.replace("{" + k + "}", v)
        ctx.log(f"[cli-agent] running: {cmd}")
        t0, timed_out = time.time(), False
        with open(ctx.workdir / "agent.log", "w") as out:
            try:
                code = subprocess.run(cmd, shell=True, env=env, cwd=ctx.workdir, stdout=out, stderr=subprocess.STDOUT,
                                      timeout=60 * timeout).returncode
            except subprocess.TimeoutExpired:
                code, timed_out = None, True
        return {"cmd": cmd, "exit_code": code, "timed_out": timed_out,
                "agent_minutes": round((time.time() - t0) / 60, 2), "log": str(ctx.workdir / "agent.log")}
