"""The guarantees an outside method or an evolving agent relies on."""
import json
import shutil
import textwrap

import pytest

from recforge import evolve
from recforge.cli import TEMPLATE, main
from recforge.data import load
from recforge.run import run_one


def test_train_view_holds_no_targets():
    data = load("synthetic")
    view = data.train_view()
    assert all(len(v) == len(s) - 2 for v, s in zip(view.seqs, data.seqs))
    assert view.train_seqs()[0].tolist() == data.seqs[0][:-2].tolist()
    with pytest.raises(PermissionError):
        view.split("test")


def test_model_code_cannot_ask_for_targets(tmp_path, workspace):
    f = tmp_path / "peek.py"
    f.write_text(textwrap.dedent("""
        from recforge.models.base import Recommender
        class Peek(Recommender):
            name = "peek"
            def fit(self, data, val_fn):
                data.split("test")
            def score(self, users, histories):
                raise AssertionError
    """))
    with pytest.raises(RuntimeError, match="PermissionError"):
        run_one("synthetic", f"{f}:Peek")


def test_outside_model_file_runs_and_code_edits_make_new_records(tmp_path, workspace):
    f = tmp_path / "mine.py"
    shutil.copy(TEMPLATE, f)
    a = run_one("synthetic", f"{f}:MarkovChain")
    assert a["model"] == "markov" and a["test"]["hr@10"] > 0.9   # next = last + 1 is a pure transition rule
    f.write_text(f.read_text() + "\n# edited\n")
    b = run_one("synthetic", f"{f}:MarkovChain")
    assert b["code_hash"] != a["code_hash"] and b["config_hash"] != a["config_hash"]


def test_session_hides_test_until_one_finalize(tmp_path, workspace):
    evolve.create("s", "synthetic", max_trials=2)
    t1 = evolve.trial("s", "pop")
    t2 = evolve.trial("s", "itemknn")
    assert "test" not in t1["trial"] and t2["used"]["trials"] == 2
    rec_dir = workspace / "sessions" / "s" / "records"
    assert all(json.loads(p.read_text())["test"] is None for p in rec_dir.glob("*/*/*.json"))
    with pytest.raises(PermissionError, match="budget"):
        evolve.trial("s", "bpr")
    final = evolve.finalize("s", 2)
    assert final["test"]["hr@10"] > 0.5
    with pytest.raises(PermissionError, match="finalized"):
        evolve.finalize("s", 1)
    published = json.loads(next((workspace / "runs").glob("synthetic/itemknn/*.json")).read_text())
    assert published["evolve_session"]["name"] == "s" and published["test"] == final["test"]


def test_cli_bench_json(capsys, workspace):
    assert main(["bench", "--model", "pop", "--suite", "smoke", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    rows = out["leaderboard"]["synthetic (loo-2)"]
    assert out["model"] == "pop" and rows[0]["model"] == "pop" and "ndcg@10" in rows[0]


def test_cli_reports_errors_as_json(capsys, workspace):
    assert main(["bench", "--model", "nope", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["error"] == "KeyError"
