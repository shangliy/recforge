"""Evolvers run under the session rules: budget, validation only, one finalize, val->test gap reported."""
import importlib.util
import json
import sys

import pytest

from recforge import evolve
from recforge.cli import main
from recforge.evolvers import run_evolver
from recforge.evolvers.random_search import sample


def test_random_search_spends_budget_and_reports_gap(workspace):
    r = run_evolver("random", "synthetic", "itemknn", max_trials=4, session="r", log=lambda m: None)
    s = evolve.load("r")
    assert r["used"]["trials"] == 4 == len(s["trials"]) and s["evolver"] == "random"
    assert all("test" not in t for t in s["trials"])
    assert s["trials"][0]["note"] == "random: defaults"
    assert len({t["config_hash"] for t in s["trials"]}) == 4
    best = max(s["trials"], key=lambda t: t["val"]["ndcg@10"])
    assert r["final_trial"] == best["id"] and r["finalized_by"].startswith("recforge")
    assert r["val_test_gap"]["ndcg@10"] == round(r["test"]["ndcg@10"] - r["val"]["ndcg@10"], 4)
    published = json.loads(next((workspace / "runs").glob("synthetic/itemknn/*.json")).read_text())
    assert published["evolve_session"]["evolver"] == "random"
    with pytest.raises(PermissionError):
        evolve.trial("r", "pop")


def test_search_space_sampling_is_seeded():
    import random
    space = {"k": [1, 2, 3], "lr": {"log": [1e-4, 1e-2]}, "n": {"int": [1, 4]}}
    a, b = sample(space, random.Random(0)), sample(space, random.Random(0))
    assert a == b and 1e-4 <= a["lr"] <= 1e-2 and a["k"] in (1, 2, 3) and 1 <= a["n"] <= 4


def test_bad_evolver_setting_fails_before_a_session(workspace):
    with pytest.raises(KeyError, match="no settings"):
        run_evolver("random", "synthetic", "itemknn", session="x", evolver_cfg={"nope": 1})
    assert not (workspace / "sessions" / "x").exists()


def test_evolver_from_a_file_via_cli(tmp_path, capsys, workspace):
    f = tmp_path / "mine.py"
    f.write_text("from recforge.evolvers.base import Evolver\n\n"
                 "class Mine(Evolver):\n    name = 'mine'\n"
                 "    def run(self, ctx):\n        self.trial(ctx, note='only one')\n        return {'ok': True}\n")
    assert main(["evolve", "--evolver", f"{f}:Mine", "--dataset", "synthetic", "--base", "pop",
                 "--session", "m", "--max-trials", "3", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["used"]["trials"] == 1 and out["evolver_info"] == {"ok": True} and "ndcg@10" in out["val_test_gap"]


def test_cli_agent_runs_the_command_and_recforge_finalizes(tmp_path, workspace):
    agent = tmp_path / "fake_agent.py"
    agent.write_text(
        "import os, subprocess, sys\n"
        "assert os.path.exists(os.environ['RECFORGE_PROMPT'])\n"
        "for m in ('pop', 'itemknn'):\n"
        "    subprocess.run([os.environ['RECFORGE_PYTHON'], '-m', 'recforge', 'session', 'trial',\n"
        "                    os.environ['RECFORGE_SESSION'], '--model', m, '--note', 'fake ' + m, '--json'],\n"
        "                   check=True)\n")
    r = run_evolver("cli-agent", "synthetic", "pop", max_trials=5, session="a",
                    evolver_cfg={"cmd": f"{sys.executable} {agent} --prompt {{prompt}}"}, log=lambda m: None)
    assert r["evolver_info"]["exit_code"] == 0, (workspace / "sessions/a/work/agent.log").read_text()
    s = evolve.load("a")
    assert [t["note"] for t in s["trials"]] == ["fake pop", "fake itemknn"]
    assert "--prompt " + str(workspace / "sessions/a/work/PROMPT.md") in r["evolver_info"]["cmd"]
    assert r["model"] == "itemknn" and r["finalized_by"].startswith("recforge")
    assert "session trial a" in (workspace / "sessions/a/work/PROMPT.md").read_text()


def test_cli_agent_without_a_command_is_an_error(workspace):
    with pytest.raises(ValueError, match="needs a command"):
        run_evolver("cli-agent", "synthetic", "pop", session="n", log=lambda m: None)


def test_openevolve_adapter_writes_a_working_evaluator(workspace):
    try:
        import openevolve  # noqa: F401
        pytest.skip("openevolve is installed; this test covers the not-installed path")
    except ImportError:
        pass
    with pytest.raises(RuntimeError, match="pip install openevolve"):
        run_evolver("openevolve", "synthetic", "itemknn", max_trials=3, session="o", log=lambda m: None)
    d = workspace / "sessions" / "o" / "work" / "openevolve"
    assert "EVOLVE-BLOCK-START" in (d / "initial_program.py").read_text()
    spec = importlib.util.spec_from_file_location("ev", d / "evaluator.py")
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    score = ev.evaluate(str(d / "initial_program.py"))
    s = evolve.load("o")
    assert score["combined_score"] == s["trials"][0]["val"]["ndcg@10"] > 0
    assert s["trials"][0]["model"] == "evolved_itemknn" and "test" not in s["trials"][0]
