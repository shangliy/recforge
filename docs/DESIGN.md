# recforge design

## Goal

One protocol under which classic recommenders, generative recommenders (TIGER, HSTU, OneRec-style) and
LLM-based recommenders are trained, evaluated and compared, under which coding agents can evolve them, and
from which a winning model can be served in a working demo (news, agent-written content, local stores).

What exists already and what this adds:

| layer | existing work | gap recforge targets |
|---|---|---|
| classic | RecBole, Microsoft Recommenders | no generative models |
| generative | MiniOneRec, OpenOneRec (RecIF-Bench), Meta generative-recommenders (HSTU) | each repo has its own split and metrics, so TIGER / HSTU / OneRec numbers are not comparable |
| self-evolving | RecHarness, EvoRec, YouTube self-evolving recsys, AgentX | systems in papers; no shared benchmark for comparing the agents themselves |
| demo | none of the above | a served model on real catalogues (MIND news, Agent Newsroom posts, OSM stores) |

## Layers and contracts

```
data/    SeqData: per-user chronological item sequences, ids 1..n, 0 = pad, no repeats; item_meta for text/geo
models/  Recommender.fit(data, val_fn) -> info ; Recommender.score(users, histories) -> (B, n_items + 1)
worker   model code in its own process with the train view only; returns ranked top-100 lists per user
eval     judge side holds targets: HR / NDCG @10, @20, MRR@100 from the lists
run      one (dataset, model spec, source hash, config, seed) -> one immutable JSON record
bench    suites (smoke, ml1m, standard): one command, fixed datasets and seeds, result placed among baselines
evolve   budgeted sessions: trials see validation only, test sealed, one finalize
serve/   (M3) a chosen record's model behind an HTTP API, with per-vertical candidate filters
```

`score(users, histories)` is deliberately sequence-in, scores-out. ID models ignore `histories`, sequential and
generative models ignore `users`, and an LLM reranker reads `item_meta` for the history. Generative models that
decode item tokens (TIGER, OneRec) implement `score` by beam search and give the beam's items their sequence
log-probability and every other item -inf, so ranking metrics stay defined over the full catalogue.

## Protocol rules (version `loo-2`)

1. Leave-one-out: last item test, second-to-last validation, the rest train. Same for every dataset.
2. Full ranking over the whole catalogue; the model commits to a top-100 list. No sampled-negative metrics.
3. Items in the user's history are removed from the ranking.
   (`loo-1` ranked inside the judge with pessimistic ties and full MRR; `loo-2` moved ranking to the model side.)
4. Early stopping and model selection use validation only. Test is computed once, after fit.
5. A record is never overwritten; a changed config is a new hash. Changing any rule bumps `PROTOCOL_VERSION`,
   and rows from different versions are never put in one table.

## Model roadmap

| milestone | models |
|---|---|
| M0 (done) | Pop, ItemKNN, BPR-MF, SASRec |
| M1 (in progress) | HSTU and TIGER implemented; OneRec-style decoder with preference alignment, BERT4Rec next |
| later | LLM zero-shot reranker over item_meta, semantic-ID variants (the 2026 reproducibility questions) |

Each M1 model must first reproduce its paper's ML-1M or Amazon number under its own protocol, then be run under
`loo-2`. Both numbers go in the model's docstring.

## Evolve track (sessions built; agent loop is M2)

Harness²-style loop: an agent proposes a change (config, or code inside the model file), the runner trains it,
the agent sees validation metrics only, and adopted changes plus their evidence go to an experience file.

Leakage rules, enforced by the runner rather than by prompt (see docs/AGENTS.md for what is and is not covered):
- model code gets the train view only, in its own process; targets stay with the judge
- every training counts against a stated budget (GPU-minutes and number of trainings), reported with the result
- the final candidate is scored on test exactly once
- an evolve result is a record like any other, plus the full edit trail

Separate leaderboard: best test metric reached per budget, by agent, on fixed datasets and fixed seed models.

## Demo (M3)

Train on public logs, serve on a live catalogue:
- news: MIND-trained model, candidates from current news items
- agent content: Agent Newsroom posts as candidates (content ids and text from its API)
- local stores: OSM places from LocalScout; needs a geo-aware candidate filter before ranking

Agent Newsroom has no reader interaction logs, so its vertical is cold-start by construction; the demo must say so.
