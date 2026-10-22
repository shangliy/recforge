# Self-evolving recommender systems: a survey

*October 2026. The entries, links and verification status are in [related-work.md](related-work.md).*

## 1. Scope

This survey covers systems that improve a recommender with little or no human work per step, focusing on
systems where an LLM agent proposes a change, the change is evaluated, and the result decides what to try next.
These systems differ in what they change:

| level | what changes | examples |
|---|---|---|
| search space | a choice inside a fixed design space | AutoFIS, NASRec, AutoEmb, AutoLossGen |
| configuration | hyperparameters, fusion weights, pipeline settings | VirtualMLE, CORAL, Sortify, AgenticRecTune |
| code | model, loss, training and feature code | Self-EvolveRec, RecHarness, EvoRec, Google/YouTube, NOVA, AgentX, Meta REA |
| policy | prompts, memory, or the weights of an LLM recommender | RecMind, AgentCF, MACRec, OneRec's preference alignment, SPRec, Rec-R1 |

"Self-evolving" is used for all four levels in the literature. Only the code level can find designs a human did
not foresee, and it is also the level where evaluation mistakes cost the most, because the agent controls nearly
everything that produces the number it is judged on.

## 2. How the field developed

**Before 2026: search spaces and policies.** AutoML for recommenders (surveyed by Zheng et al., 2022) searched
for interaction structures (AutoCTR, AutoFIS), embedding sizes (AutoEmb, AutoDim), whole architectures with
weight sharing (NASRec, DNS-Rec), and losses (AutoLossGen). Each method can only find designs its search space
contains. In parallel, LLM recommender agents (2023–2025) learned in context: RecMind plans per query, AgentCF and
MACRec update memories or reflect, and RecPrompt tunes prompts. OneRec, SPRec and Rec-R1 change model weights
with DPO or RL on their own outputs. None of these edits recommender source code.

**General program evolution matured first.** FunSearch (2023) and AlphaEvolve (2025) showed that an LLM
proposing code under an automatic evaluator can find new algorithms. Open implementations followed: OpenEvolve,
ShinkaEvolve, DeepEvolve. ML-engineering agents (AIDE, MLE-STAR, R&D-Agent, AI Scientist) and their benchmarks
(MLE-bench, MLAgentBench, RE-Bench, MLGym, MLRC-Bench) made "agent improves a model under a metric" a standard
task. These benchmarks contain at most one recommendation task each.

**2026: code-level recommender evolution.** All the systems in this group appeared within one year.

- *Academic and open source.*
  - Self-EvolveRec runs an AlphaEvolve-style loop over NCF, NGCF, SASRec and MoRec seeds. It adds directional
    feedback from an LLM user simulator and a diagnosis tool that evolves alongside the model.
  - RecHarness has a bandit choose the direction of each edit and evolves architecture, objective and training
    code for five sequential backbones, HSTU among them. It uses validation-only feedback and a GPU-second budget.
  - VirtualMLE tunes the configuration of SASRec and HSTU and keeps a memory that transfers across datasets.
- *Industrial and closed.*
  - Google reports an agent that writes code and config changes for YouTube rankers. It promotes changes through
    an offline loop on validation loss, then through online A/B tests.
  - Meta's REA, AgentX, AgentX-Model, NOVA, Auto-RecSys, AutoLR, AgenticRecTune and EvoRec follow the same pattern:
    LLM agents propose, offline metrics screen, online experiments decide.
  - No industrial system has released code.

Two kinds of paper frame the field. Beel et al.'s AutoRecLab position paper (2025) calls for shared
benchmarks and provenance for autonomous recommender research. EvoRank (2026, learning to rank) measured
what most papers do not: when the evolved pipelines were scored on 60k held-out queries, most of the first
campaign's gains turned out to be fitness noise.

## 3. A common anatomy

Most code-level systems share the same four parts, and they differ mainly in how they build each one:

1. **Proposer.** An LLM writes a hypothesis and a code edit. Systems add structure around it: a bandit over edit
   directions (RecHarness), islands or MAP-Elites archives (OpenEvolve-based), a research agent paired with a
   coding agent (EvoRec, AgentX-Model), or a council that reviews each proposal (AutoLR).
2. **Evaluator.** The edited model is trained and scored. Academic systems use offline ranking metrics.
   Industrial systems use offline proxies first and then live A/B tests.
3. **Memory.** Past trials are summarized for the proposer as an experiment log, distilled skills (EvoRec,
   AgenticRecTune), forbidden patterns (NOVA), or cross-dataset heuristics (VirtualMLE).
4. **Selection.** One trial becomes the incumbent and is reported. What data this decision uses is the most
   important property of the system and the least often described.

## 4. Open problems

**4.1 Sampled metrics as the objective.** Both open-source recommender-evolution systems select and report
with one target against 99 random negatives. Krichene and Rendle showed that sampled metrics can reverse model
rankings. When the agent's objective is the sampled metric, a loop can learn to separate targets from random
items rather than rank the catalogue. No paper checks whether evolved gains survive full ranking.

**4.2 Which split drives the search.** RecHarness, Self-EvolveRec and MLRC-Bench restrict feedback to
validation and score the final choice on test once. Several other systems do not say which split drives
per-round decisions. MLGym's `validate` returns test metrics and can be called repeatedly. In AIDE-style
loops the agent writes its own validation split. Where a seal exists, it is a convention of the experiment
script, and nothing stops the agent's code from reading the test data.

**4.3 Overfitting the selection data.** An agent that runs hundreds of trials against one validation set will
find edits that fit that set. Apart from EvoRank, which is about learning to rank, no paper in this survey reports
the validation-to-test gap of the selected trial, the spread over repeated evolution sessions, or whether random
search with the same budget does as well.

**4.4 Budgets.** Budgets are counted as GPU-seconds (RecHarness), offline evaluations (NOVA), steps
(Self-EvolveRec), approved GPU estimates (Meta REA), or not at all. Almost no paper reports LLM tokens or cost,
so improvement per unit of compute cannot be compared across systems.

**4.5 No shared benchmark.** Each paper chooses its own datasets, splits, seeds, backbones and step limits.
Industrial results use private data and online metrics. A number from one paper cannot be compared with a
number from another, and nobody else can rerun the industrial results.

**4.6 Weak starting points.** Dacrema et al., Rendle et al., Petrov and Macdonald, and Klenitskiy and Vasilev
showed that well-tuned simple baselines, or a different loss alone, often erase reported progress. Evolution
papers mostly start from, and compare against, untuned seeds, so a reported gain can be ordinary tuning.

**4.7 Generative recommenders are barely covered.** HSTU appears as a backbone in RecHarness and VirtualMLE
(VirtualMLE tunes only its configuration). TIGER, HSTU and Cobra appear only as baselines in EvoRec. No open
system evolves the code of semantic-ID tokenizers, constrained decoding or generative-retrieval losses under
a controlled protocol.

**4.8 Circular evaluation at the policy level.** Policy-level agents are usually judged by LLM user
simulators or small candidate sets. The simulator is often from the same model family as the agent being
improved. Self-EvolveRec reduces this by evaluating with simulators the evolution loop never saw.

## 5. What recforge provides and what it does not yet

recforge is meant to be the shared, offline and rerunnable environment that §4.2–§4.5 call for. Built today:

| problem | recforge today |
|---|---|
| 4.1 sampled metrics | Every result ranks the full catalogue with history removed (HR, NDCG at 10 and 20, MRR@100). No sampled metric exists in the code. |
| 4.2 split hygiene | The model runs in a separate process that receives only the train view. Asking it for a validation or test target raises `PermissionError`. Evolve trials return validation metrics only. Test metrics are written sealed and revealed for exactly one trial at `finalize`, after which the session accepts nothing. |
| 4.4 budgets | Sessions have a trial limit and a minute limit, both enforced by recforge, and the session file keeps every trial with its note. |
| 4.5 shared benchmark | One protocol version (`loo-2`), fixed datasets and seeds, and result keys that contain the source hash of the method. Evolved and hand-written methods share one leaderboard. |
| 4.6 starting points | Pop, ItemKNN, BPR, SASRec, HSTU and TIGER ship as baselines. SASRec and HSTU reproduce the HSTU repository's ML-1M numbers within a few percent with `--preset hstu-repo`. |
| 4.7 generative models | HSTU and TIGER are built in, so they can be evolution seeds. |

Not built yet, in order of importance:

- **Real isolation.** The train view protects the API, not the file system: model code could open the raw
  files itself. A container mode that mounts only the train view is planned and is needed before running
  agents that are not trusted.
- **Overfitting measurements (4.3).** Each finalized session should report its validation-to-test gap, sessions
  should be repeatable over seeds, and a random-search or Optuna evolver with the same budget should run as the
  null baseline.
- **Cost accounting (4.4).** LLM tokens and dollars are not recorded; only trials and minutes are.
- **A timeline-aware split.** Leave-one-out ignores the global timeline, which Ji et al. show leaks future
  data. A temporal split should be offered next to `loo-2`.
- **More generative models.** An OneRec-style model with preference alignment is next.
- **Evolver adapters.** OpenEvolve, ShinkaEvolve, AIDE, RecHarness (MIT) and Self-EvolveRec (no license, so link
  only) could each drive a session through the same `--json` commands, which would make them comparable for the
  first time.

## 6. Suggested experiments

1. Take the selected trials of an evolution run and score them with sampled metrics and with full ranking. Check
   whether the order of the trials agrees (§4.1).
2. Run the same evolver for several sessions, one seed each, and report the mean and spread of the finalized
   test score and the validation-to-test gap (§4.3).
3. Compare an LLM evolver with random search over the same configuration space at an equal trial budget (§4.3,
   §4.6).
4. Seed sessions with HSTU and TIGER and restrict edits to the tokenizer, the decoding or the loss (§4.7).
