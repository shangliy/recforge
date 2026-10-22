# Benchmarks & evaluation (survey version)

For a survey this stage maps *how the surveyed systems are evaluated* and what a shared benchmark would need. No
numbers here are ours; per-paper datasets/metrics come from the audits (`audit/evidence-part1.md`, `audit/evidence-part2.md`) at
stage 05.

## Evaluation settings in use
| Setting | Measures | Used by (examples) | Metric(s) | Protocol | Access |
|---------|----------|--------------------|-----------|----------|--------|
| Leave-last-out sequential rec, sampled ranking (1+99) | next-item ranking vs random negatives | [kim2026selfevolverec], [ling2026recharness] | HR/NDCG@k | per-paper | public (Amazon, MovieLens) |
| Leave-one-out, full ranking | next-item ranking over the catalogue | [mu2026evorec] (to confirm), [chen2026rankevolve] ML-20M (to confirm), recforge `loo-2` | HR/NDCG/MRR | per-paper / recforge | public |
| CTR prediction | pointwise click probability | cluster A; [li2026evoskillrec] | AUC, logloss | standardised by BARS/FuxiCTR [zhu2022bars], [zhu2021fuxictr] | Criteo/Avazu public |
| Industrial offline | proprietary logs | Google, Meta, AgentX, NOVA, EvoRec, Astar, RecEvolve, ... | AUC, calibration, NDCG, Hitrate@200 | private | none |
| Online A/B | live users | nearly all industrial systems | GMV, orders, watch time, satisfaction | private | none |
| User simulators | simulated satisfaction | [zhang2023agent4rec], [liu2025recoworld], Self-EvolveRec evaluation | LLM-judged | per-paper | open code |
| MLE agent benchmarks | agent engineering on Kaggle-like tasks | [chan2024mlebench] (H&M), [zhang2025mlrcbench] (KDD Cup 2023) | task metric | standardised, grader-held test | public |
| In-paper agent benchmarks | execution accuracy of agent edits; discovery under compute | ExecML-HSTU [chen2026rankevolve], RMD-Bench [peng2026population] | execution accuracy; ranking/watch-time gain | new, not yet adopted | no code found |

## Metric pathologies
- Sampled HR/NDCG (1+99): inconsistent with exact metrics, can reverse rankings [krichene2020sampled]. An evolution
  loop optimising it may learn to beat random negatives rather than rank the catalogue (hypothesis, untested).
- Leave-one-out without a global timeline leaks the future [ji2020leakage]; the splitting choice changes rankings
  [meng2020splitting].
- AUC on industrial data: small offline gains often do not transfer online (the motivation of Sortify and of Google's
  fast/slow loops; quotes pending audit).
- One validation set reused for hundreds of agent trials: adaptive overfitting [dwork2015reusable], [blum2015ladder].
  Counter-evidence: human holdout reuse on Kaggle overfits little [roelofs2019metaanalysis]. Direct evidence for an
  LLM loop: [patel2026evorank].
- Weak baselines: tuned simple models beat many neural methods [dacrema2019progress], [rendle2020ncf]; a loss change
  alone reorders SASRec and BERT4Rec [klenitskiy2023dross].

## Blind spots of current practice
- No benchmark compares evolvers with each other under an equal budget on the same recsys tasks.
- No benchmark measures selection overfitting (val→test gap of the selected candidate, spread over repeated runs).
- No benchmark enforces the test seal against agent code. MLE-bench and MLRC-Bench withhold files; recforge withholds
  targets through the train-view API but not yet through the file system.
- Generative-recommender components (tokeniser, decoding, losses) have no shared evolution task.

## What a shared benchmark needs (input to the survey's Section 7)
- Primary: full-ranking sequential tasks with public data and a reproduced baseline (ML-1M; Amazon Beauty for TIGER;
  a large industrial-flavoured set such as Kuaishou OpenOneRec [zhou2025openonerec]).
- Secondary: CTR under BARS/FuxiCTR protocols.
- Baselines: tuned SASRec/HSTU/TIGER; an equal-budget random search; at least two LLM evolvers (e.g. OpenEvolve-based,
  RecHarness).
- Reported per session: budget used (trials, GPU time, tokens/$), validation and test of the selected candidate, the
  gap, and the spread across at least 3 repeated sessions.
- recforge [recforge] provides the protocol, sealed sessions, a null baseline and adapters. It has no evolver results
  yet, and the survey must say so.
