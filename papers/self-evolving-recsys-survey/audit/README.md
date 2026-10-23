# Evaluation audit of self-evolving recommender systems

Data behind Section 6 and Table 3 of the survey. Coded 2026-10-21 from the full text (arXiv HTML or PDF, with
appendices) of each paper, in the version arXiv served on that date.

- `audit.csv`: one row per system; the paper's table and every count are generated from it by `summarize.py`.
- `evidence-part1.md`, `evidence-part2.md`: per-paper rubric with verbatim quotes (at most 25 words) and section or
  table pointers for every coded cell.

## Codebook
| column | values |
|---|---|
| set | `core` (recommendation, L1–L3 loop with evaluation-driven selection) or `comparison` (outside recommendation) |
| level | evolved object: `L1` configuration, `L2` code, `L3` generative-recommender components (joined with `+`) |
| meta | `Y` the loop changes its proposer's instructions, tools, skills or weights and reuses them; `N` |
| c1 metric | `full` full-catalogue ranking; `sampled` ranking against sampled or in-batch negatives; `ranking-ns` ranking with the candidate set not stated; `auc` AUC/logloss/loss proxy; `online` online only; `none` no usable metric stated; `other` a non-recommendation metric |
| c2 selection | the data or signal that keeps or rejects candidates in the loop: `val`; `test` (the same data the results are reported on); `trainloss`; `online`; `NS` (not stated); `na` (no selection step: operational outcomes only) |
| c3 test once | `Y` stated; `N` selection data are the reported data, or test is reused; `P` partly; `NS`; `na` (online-selecting loops) |
| c4 repeats | `Y` repeated evolution sessions with spread; `P` repeats without spread, ablation-only repeats, a re-run rule, or a run-to-run noise estimate of single models without repeating a session; `N` |
| c5 gap | `Y` explicit selection-vs-held-out check of the selected candidates; `P` partial transfer evidence (another dataset, scale, period or population); `N` |
| c6 null | `Y` non-LLM search (random, grid, BO, HPO, NAS) at equal or favourable budget; `P` partial (unmatched budget, LLM still proposing, replay only); `N` |
| c7 budget | units reported (free text, not scored) |
| c8 baselines | `tuned` (stated); `P` partly tuned, or tuned on the test split; `untuned`; `production`; `published`; `seed`; `NS` |
| c9 isolation | design, regardless of incidents: `Y` stated that the agent cannot reach test data or labels; `P` part of the loop constrained (fixed evaluation code, gates, whitelists, sandboxing, bounded actions); `N` the agent can reach test data; `NS`; `na` online-only loop with no offline data or evaluation code the agent could touch and no stated constraints |
| incident | `Y` the paper reports gaming, metric inflation, leakage or a metric-winning bug produced by the loop; `N` |
| online | `none`, or what is reported: duration (`7d`, `3wk`, `1mo`), `CI` or `sig` (confidence intervals or significance), `yes` (an online experiment without either) |
| code | `Y` released; `promised`; `N` |
| llm_named | `Y` the LLM is named; `N` |

Strata used in the paper: offline-selecting loops (`c2` not in `online`, `na`; 17), online-selecting loops (`c2` =
`online`; 9) and one loop with operational outcomes only (`c2` = `na`). All counts, Table 3 and Figure 3 are generated
by `summarize.py`.

"Not stated" means the paper does not say; it does not mean the practice was absent. Corrections are welcome as
issues or pull requests with a quote from the paper.

## Borderline systems read but not counted
RecSys Factory (2608.11241, operations platform, human approval of every change), AutoRecLab (2609.21863, experiment
generation), AURA (2609.16625, stops at pull requests), Spotify (2609.30297, prompt-level L4 loop). Their evidence is in
`evidence-part2.md`.

## Reconciliation with the second coder (2026-10-23)

A second author coded all 27 core systems independently (`second-coder/returned/`). Pre-reconciliation agreement:
pooled 0.84, Cohen's kappa 0.81, Gwet's AC1 0.84; kappa below 0.6 for c5 (0.30) and c8 (0.57). The 38 disagreements
and their resolutions are in `second-coder/reconciliation.md`; 31 cells changed in this file. Google/YouTube is now
online-selecting (c2 `online`), so the strata are 16 offline-selecting, 10 online-selecting, 1 operational.

Rules the reconciliation settled, to apply to new rows:
- c2 in a multi-stage loop: code the last gate that keeps or rejects among several candidates. A single online test of
  one already-selected candidate is c5 evidence, not selection.
- c1: the headline metric is the one behind the numbers in the abstract's headline claim; `online` only when every
  quantified gain there is online; `other` for any non-recommendation metric (fix steps, policy-selection nDCG);
  `none` only when no quantitative metric is given. A success rate defined on a recommendation metric (NOVA's EPR on
  AUC) is coded by that metric.
- c3: `N` when test scores are computed during the search or the reported number is by construction the best over
  rounds, even if the paper states they are not used for selection.
- c5: an online A/B of an offline-selected candidate, or a check on another dataset or scale, is `P`; `Y` is reserved
  for a same-task selection-vs-held-out comparison. A designed but unreported confirmation, or a check of a proxy rather
  than of the selected candidates, is `N`.
- c6: comparisons with humans, manual workflows, other LLMs or trivial decision rules are `N`.
- c8: `P` if tuned on the reported split; else `tuned`/`untuned` if tuning is stated (original-paper defaults are
  `untuned`); else the comparator's identity (`seed`, `production`, `published` only for numbers copied from papers).
- c9: `N` when the text shows the agent reading test labels or running test evaluation, whatever the process gates.
- incident: requires a documented instance; a risk the paper names (AutoLR's KEEP ratchet) is a note, not `Y`.

## Changes in v2 (2026-10-22, after review)

- `c9` no longer mixes design and incidents: the four core rows formerly coded `gaming` now carry their isolation
  design (RecEvolve `P`, RankEvolve-HSTU `N`, EvoPilot `P`, Amazon AutoResearch `P`) and `incident` = `Y`; AI
  Co-Scientist is `NS` + `Y`.
- EvoPilot `c2` NS → `test`, `c3` NS → `N`: one held-out replay set both selects and is reported (§5.1).
- Population Evolution `c2` NS → `test` (source-instance evaluation scores drive discovery and report local gains;
  transfer targets are withheld from the proposer) and `c8` tuned → `P` (baselines calibrated on the released test
  split, App. F.1).
- A/B Agent meta → N: only its experience tree of past outcomes is written back.
- `level` now holds the evolved object only, and meta-evolution has its own `meta` column (Y for 13 core systems,
  following the rule in design.csv: the loop changes its proposer's instructions, tools, skills or weights and reuses
  them). Object changes: EvoRec L2 → L1+L2, RecHarness and NOVA L2 → L1+L2, AgentX L2 → L1+L2, Amazon AutoResearch
  L2+L3 → L1+L2+L3 (their kept edits include configuration and strategy parameters).
- `c9` for CORAL, AgenticRecTune, Sortify and GEARS `na` → `P`, and Google/YouTube `NS` → `P`: each states
  constraints on the loop (bounded changes, critic and review gates, read-only sandboxes, a fixed scoring loss).
- Design fields for every core system (object, proposer, signal chain, memory, acceptance, guards, human role, LLM,
  kept edits, headline gain, baseline) are in `design.csv`, with evidence quotes in `design-evidence.md`.

## Rows added 2026-10-22

EvoPilot, Amazon AutoResearch, PILOT, A/B Agent, DMRL (core) and Feedback Contract, PEAR (comparison) were coded
from the full text in the second sweep; the per-cell quotes with section pointers are in
`../review/sweep-2026-10-22.md` §(b). C6 counts only non-LLM search; Feedback Contract's label-permuted no-signal task
is a "null task", which the codebook does not score.
