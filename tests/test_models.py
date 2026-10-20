"""Every built-in model trains through the runner on the synthetic dataset, whose answer is known (next = last + 1)."""
import json

import pytest

from recforge.board import aggregate, collect, to_markdown
from recforge.run import run_one

FAST = {
    "pop": {},
    "itemknn": {},
    "bpr": {"epochs": 30, "batch_size": 512, "lr": 1e-2},
    "sasrec": {"epochs": 15, "max_len": 20, "dim": 32, "dropout": 0.1},
}
# Random guessing over 200 items gives HR@10 of about 0.05.
FLOOR = {"pop": 0.0, "itemknn": 0.5, "bpr": 0.08, "sasrec": 0.8}


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    runs = tmp_path_factory.mktemp("runs")
    return runs, {m: run_one("synthetic", m, cfg, seed=1, runs_dir=runs) for m, cfg in FAST.items()}


@pytest.mark.parametrize("model", list(FAST))
def test_model_clears_floor(records, model):
    assert records[1][model]["test"]["hr@10"] >= FLOOR[model], records[1][model]["test"]


def test_popularity_cannot_learn_the_rule(records):
    assert records[1]["pop"]["test"]["hr@10"] < 0.2


def test_record_is_reused_and_board_renders(records):
    runs, recs = records
    again = run_one("synthetic", "sasrec", FAST["sasrec"], seed=1, runs_dir=runs)
    assert again == json.loads(json.dumps(recs["sasrec"]))
    table = to_markdown(aggregate(collect(runs)))
    assert "| sasrec |" in table and table.index("| sasrec |") < table.index("| pop |")
