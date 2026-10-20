# recforge

One protocol to train, evaluate, compare and evolve recommenders — classic, generative (TIGER / HSTU /
OneRec) and LLM-based — with a demo product on top. Design, protocol rules and roadmap: [docs/DESIGN.md](docs/DESIGN.md).

Status: **M0**. Data layer, model contract, four baselines, full-ranking evaluation, result records and leaderboard.

## Quick start

```bash
python -m venv --system-site-packages .venv && .venv/bin/pip install -e .   # needs numpy, pandas, scipy, torch
.venv/bin/python -m pytest -q                                               # synthetic-data tests, CPU, seconds

python -m recforge data ml1m                                  # downloads if data/raw/ml-1m is missing
python -m recforge run ml1m pop,itemknn
python -m recforge run ml1m sasrec --seeds 1,2,3 --device cuda --set dim=128
python -m recforge board
```

`RECFORGE_RAW` points at an existing raw-data directory (`ml-1m/`, `mind/{train,dev}/`).

## Adding a model

Subclass `recforge.models.base.Recommender`, set `name` and `DEFAULTS`, implement `fit(data, val_fn)` and
`score(users, histories)`, and register it in `recforge/models/__init__.py`. `fit` must leave the model in its
best-validation state; it never sees test targets.

## Datasets

| name | source | sequence |
|---|---|---|
| `ml1m` | MovieLens-1M | all ratings as implicit feedback, by timestamp |
| `mind` | MIND-small (train + dev) | pre-window click history, then impression clicks by time |
| `synthetic` | generated | next item = last + 1; for tests |

## Results

Every run writes `runs/<dataset>/<model>/<config-hash>-s<seed>.json`; `python -m recforge board` builds the
table from those files only.
