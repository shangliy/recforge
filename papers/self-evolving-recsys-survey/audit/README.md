# Evaluation audit of self-evolving recommender systems

Data behind Section 6 and Table 3 of the survey. Coded 2026-10-21 from the full text (arXiv HTML or PDF, with
appendices) of each paper, in the version arXiv served on that date.

- `audit.csv`: one row per system; the paper's table and every count are generated from it by `summarize.py`.
- `evidence-part1.md`, `evidence-part2.md`: per-paper rubric with verbatim quotes (at most 25 words) and section or
  table pointers for every coded cell.

## Codebook
| column | values |
|---|---|
| set | `core` (recommendation, L1/L2 loop with evaluation-driven selection) or `comparison` (outside recommendation) |
| c1 metric | `full` full-catalogue ranking; `sampled` ranking against sampled or in-batch negatives; `ranking-ns` ranking with the candidate set not stated; `auc` AUC/logloss/loss proxy; `online` online only; `none` no usable metric stated; `other` |
| c2 selection | `val`, `test`, `trainloss`, `online`, `NS` (not stated) |
| c3 test once | `Y`, `N`, `NS`, `na` (online-only systems) |
| c4 repeats | `Y` repeated evolution sessions with spread; `P` repeats without spread, or ablation-only repeats, or a re-run rule; `N` |
| c5 gap | `Y` explicit selection-vs-held-out check of the selected candidates; `P` partial transfer evidence; `N` |
| c6 null | `Y` non-LLM search (random, grid, BO, HPO, NAS) at equal or favourable budget; `P` partial (unmatched budget, LLM still proposing, replay only); `N` |
| c7 budget | units reported |
| c8 baselines | `tuned`, `untuned`, `production`, `published`, `seed`, `NS`, `P` |
| c9 isolation | `Y` agent cannot reach test data, stated; `P` part of the loop constrained; `gaming` gaming or leakage by the loop reported; `NS`; `na`; `N` |
| online | `none`, or duration / `CI` (significance reported) / `yes` |

"Not stated" means the paper does not say; it does not mean the practice was absent. Corrections are welcome as
issues or pull requests with a quote from the paper.

## Borderline systems read but not counted
RecSys Factory (2608.11241, operations platform, human approval of every change), AutoRecLab (2609.21863, experiment
generation), AURA (2609.16625, stops at pull requests), Spotify (2609.30297, prompt-level L4 loop). Their evidence is in
`evidence-part2.md`.

## Rows added 2026-10-22

EvoPilot, Amazon AutoResearch, PILOT, A/B Agent, DMRL (core) and Feedback Contract, PEAR (comparison) were coded
from the full text in the second sweep; the per-cell quotes with section pointers are in
`../review/sweep-2026-10-22.md` §(b). C6 counts only non-LLM search; Feedback Contract's label-permuted no-signal task
is a "null task", which the codebook does not score.
