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
eval     full ranking, history masked, pessimistic ties; HR / NDCG @10, @20, MRR
run      one (dataset, model, config, seed) -> one immutable JSON record (config hash, protocol, commit)
board    records -> per-dataset table, mean ± std over seeds
evolve/  (M2) agent edits a model under a budget; scored on val, test hidden; its own leaderboard
serve/   (M3) a chosen record's model behind an HTTP API, with per-vertical candidate filters
```

`score(users, histories)` is deliberately sequence-in, scores-out. ID models ignore `histories`, sequential and
generative models ignore `users`, and an LLM reranker reads `item_meta` for the history. Generative models that
decode item tokens (TIGER, OneRec) implement `score` by beam search and give the beam's items their sequence
log-probability and every other item -inf, so ranking metrics stay defined over the full catalogue.

## Protocol rules (version `loo-1`)

1. Leave-one-out: last item test, second-to-last validation, the rest train. Same for every dataset.
2. Full ranking over the whole catalogue. No sampled-negative metrics.
3. Items in the user's history are removed from the ranking.
4. Early stopping and model selection use validation only. Test is computed once, after fit.
5. A record is never overwritten; a changed config is a new hash. Changing any rule bumps `PROTOCOL_VERSION`,
   and rows from different versions are never put in one table.

## Model roadmap

| milestone | models |
|---|---|
| M0 (done) | Pop, ItemKNN, BPR-MF, SASRec |
| M1 | TIGER (RQ-VAE semantic IDs on item text + seq2seq), HSTU, OneRec-style decoder with preference alignment, BERT4Rec |
| later | LLM zero-shot reranker over item_meta, semantic-ID variants (the 2026 reproducibility questions) |

Each M1 model must first reproduce its paper's ML-1M or Amazon number under its own protocol, then be run under
`loo-1`. Both numbers go in the model's docstring.

## Evolve track (M2)

Harness²-style loop: an agent proposes a change (config, or code inside the model file), the runner trains it,
the agent sees validation metrics only, and adopted changes plus their evidence go to an experience file.

Leakage rules, enforced by the runner rather than by prompt:
- the agent process cannot read test targets (evaluation runs in a separate process that returns val metrics)
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
