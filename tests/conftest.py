import pytest

from recforge import evolve, run


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    """Isolated runs/ and sessions/ directories for one test."""
    monkeypatch.setattr(run, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(evolve, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(evolve, "SESSIONS_DIR", tmp_path / "sessions")
    return tmp_path
