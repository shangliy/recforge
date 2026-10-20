# recforge for agents

This page is the whole interface a coding agent needs to benchmark a recommender method or to evolve one.
Every command prints one JSON document with `--json`; failures print `{"error": ..., "message": ...}` and exit 1.

## 1. Write a method

```bash
recforge new my_method.py          # a working template (first-order Markov chain)
```

A method is one Python file with a class that subclasses `recforge.models.base.Recommender`:

| member | contract |
|---|---|
| `name` | unique string; becomes the leaderboard row name |
| `DEFAULTS` | dict of every setting; `--set key=value` overrides, unknown keys are rejected |
| `fit(data, val_fn) -> dict` | `data` is a train view: `data.train_seqs()` (per-user item ids in time order, 1..`data.n_items`, 0 = pad), `data.item_meta` (e.g. `title`), `data.n_users`. `val_fn()` returns validation NDCG@10 of the model as it is now. Leave the model in its best-validation state. Return anything worth logging. |
| `score(users, histories)` | `(len(users), n_items + 1)` array or tensor, higher is better. `users` index the train view; `histories[i]` is that user's items so far. History items and padding are removed for you. |
| `self.cfg`, `self.seed`, `self.device` | resolved config, seed, `cpu` / `cuda:N` |

The source file's hash is part of every result key, so an edited file is always a new result.

## 2. Benchmark it

```bash
recforge suites --json
recforge bench --model my_method.py:MyModel --suite smoke --json                 # runs end to end? (CPU, seconds)
recforge bench --model my_method.py:MyModel --suite ml1m --device cuda --json    # 3 seeds, with the leaderboard
recforge bench --model my_method.py:MyModel --suite ml1m --set dim=128 --json
```

The output's `leaderboard` places the method among every stored result for those datasets.

## 3. Evolve it under a budget

```bash
recforge session create run7 --dataset ml1m --max-trials 30 --max-minutes 240 --json
recforge session trial run7 --model my_method.py:MyModel --set lr=3e-3 --note "hypothesis" --device cuda --json
recforge session status run7 --json
recforge session finalize run7 --trial 12 --json      # test metrics, once; the session is closed
```

Rules enforced by recforge, not by the prompt:
- a trial returns validation metrics only; test metrics are sealed when it runs
- a trial is refused once the trial count or GPU-minute budget is spent
- finalize reveals the test metrics of exactly one trial, and the session accepts nothing afterwards
- the finalized trial joins the main leaderboard with its session (budget used, trial id) attached

Write the reasoning for each trial in `--note`; it is kept in the session file and is the evolve trail.

## Protocol (`loo-2`)

Leave-one-out per user (last item test, second-to-last validation). Full catalogue ranking: the model's top 100
per user, history removed; HR and NDCG at 10 and 20, MRR@100. Results from different protocol versions are never
put in one table.

## What isolation does and does not cover

Model code runs in its own process and receives only the train view, so the API cannot hand it a validation or
test target, and asking for one raises `PermissionError`. It does not stop code that opens the raw data files
under `data/` itself. For an agent you do not trust, run recforge in a container whose model process sees only
the train view; that mode is planned, not built.
