# recforge

One protocol to benchmark and evolve recommenders — classic, generative (TIGER / HSTU / OneRec) and LLM-based.
Bring a method as one Python file, run one command, get its place on the leaderboard. Agents use the same
commands with `--json`, and evolve sessions give them a budget and validation-only feedback.

- Agent / method interface: [docs/AGENTS.md](docs/AGENTS.md)
- Design, protocol rules, roadmap: [docs/DESIGN.md](docs/DESIGN.md)
- Survey of self-evolving recommenders: [docs/SURVEY.md](docs/SURVEY.md), catalogue in [docs/related-work.md](docs/related-work.md)

## Quick start

```bash
git clone https://github.com/shangliy/recforge.git && cd recforge
python -m venv .venv && .venv/bin/pip install -e .        # numpy, pandas, scipy, torch
.venv/bin/python -m pytest -q                             # CPU, under a minute

recforge new my_method.py
recforge bench --model my_method.py:MarkovChain --suite smoke --baselines
recforge bench --model my_method.py:MarkovChain --suite ml1m --device cuda   # downloads MovieLens-1M once
recforge board
```

Workspace: `RECFORGE_HOME` (default: the checkout) holds `data/`, `runs/` and `sessions/`.
`RECFORGE_RAW` points at existing raw data (`ml-1m/`, `mind/{train,dev}/`) to skip downloads.

## Built-in models and datasets

| models | `pop`, `itemknn`, `bpr`, `sasrec`, `hstu` (generative, Meta), `tiger` (semantic IDs + T5, Google); OneRec-style next |
|---|---|
| datasets | `ml1m` (MovieLens-1M), `beauty` / `sports` / `toys` (Amazon 2014 5-core), `mind` (MIND-small news), `synthetic` (tests) |
| presets | `--preset hstu-repo` (SASRec, HSTU), `--preset hstu-repo-large` (HSTU): the published configs |
| suites | `smoke` (synthetic), `ml1m` (3 seeds), `standard` (ml1m + mind, 3 seeds) |

Every run writes `runs/<dataset>/<model>/<config-hash>-s<seed>.json` with the model's source hash, config,
protocol version and commit; the leaderboard is built from those files only.
