import os
from pathlib import Path

import pytest

from recforge import evolve, run

# subprocesses (python -m recforge ...) import this checkout too, not another installed copy
_ROOT = str(Path(__file__).resolve().parents[1])
os.environ["PYTHONPATH"] = os.pathsep.join(p for p in (_ROOT, os.environ.get("PYTHONPATH")) if p)


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    """Isolated runs/ and sessions/ directories for one test."""
    monkeypatch.setattr(run, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(evolve, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(evolve, "SESSIONS_DIR", tmp_path / "sessions")
    return tmp_path
