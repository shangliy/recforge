# Coding guide for the second coder

You will code 10 self-evolving recommender papers on eight criteria, from the full text only. The aim is to measure
how far two readers agree, so please work independently: do not open `audit.csv`, `evidence-part*.md`, the
paper's Table 3 or Figure 3 until you have returned the sheet, and do not discuss individual papers with the first
coder before then. Budget about 20–30 minutes per paper.

## How to work

1. Open each paper from the `arxiv` column of `coder2.csv` (https://arxiv.org/abs/ID; use the HTML or PDF and read
   the appendices: protocols are often there).
2. Find the **headline result**: the main improvement the abstract claims. Code the evidence behind that result,
   not a side experiment, unless the criterion says otherwise.
3. Fill one value per cell from the allowed values below, typed exactly as shown. When two values seem to fit, pick
   the one the rules point to and write why in `notes`.
4. For every cell that is not obvious, put a short quote (at most 25 words) and its section or table in `notes`,
   e.g. `c2: "only validation feedback for candidate selection" (Search protocol)`.

**"Not stated" (`NS`) is not "no" (`N`).** Use `NS` when the paper does not say; use `N` when the paper says or
shows something that answers the question negatively (for example, single numbers with no repeats anywhere are
`N` for C4, because the tables show it). Use `na` only when the criterion cannot apply.

## Criteria and allowed values

| | Question | Values |
|---|---|---|
| **c1** metric | What metric supports the headline result? | `full` ranking over the full item catalogue · `sampled` ranking against sampled or in-batch negatives (e.g. 1 positive + 99 negatives) · `ranking-ns` a ranking metric (HR, NDCG, Recall) but the candidate set is not stated · `auc` AUC, logloss, NE, MSE or another loss-type proxy · `online` the headline is only an online metric · `other` a metric that is not a recommendation metric (e.g. task success rate, rubric score) · `none` no usable metric stated |
| **c2** selection | Which data or signal decides whether a candidate is kept during the loop? | `val` a validation split · `test` the same split the results are reported on · `trainloss` training loss · `online` an online experiment decides · `NS` the paper does not say which split · `na` there is no selection step |
| **c3** test once | Is the finally selected candidate evaluated on a held-out test split once, after the search? | `Y` stated · `N` the test split is used during search or repeatedly · `P` partly (e.g. once for some experiments only) · `NS` · `na` online-only systems with no offline test |
| **c4** repeats | Are the headline numbers repeated over seeds or over whole evolution sessions? | `Y` repeated sessions **and** the spread (std, CI, range) is reported · `P` repeats without any spread, repeats only in an ablation, or only a rule to re-run noisy candidates · `N` single numbers |
| **c5** gap | Does the paper check that the selected gain holds outside the data it was selected on? | `Y` an explicit selection-vs-held-out comparison for the selected candidates (e.g. val score next to test score, or a val→test gap) · `P` partial transfer evidence (another dataset, unseen users, a later period, a qualitative remark) · `N` |
| **c6** null | Is there a non-LLM search baseline over the same space? | `Y` random search, grid, Bayesian optimisation, HPO or NAS at equal or more favourable budget for the baseline · `P` such a baseline with unmatched budget, or a "random" ablation where the LLM still proposes, or replay only · `N` none. A comparison against LLM-based evolvers does **not** count. |
| **c8** baselines | What is the starting point or main comparison? | `tuned` tuned (stated) · `untuned` shared default hyperparameters, or explicitly not tuned · `production` the production model · `published` numbers copied from earlier papers · `seed` the loop's own seed program · `P` partly tuned · `NS` |
| **c9** isolation | Can the agent reach test data or evaluation code, and is gaming discussed? | `Y` stated that the agent cannot reach test data or labels · `P` part of the loop constrained (fixed evaluation code, gates, whitelists, sandboxing) but test access not ruled out · `gaming` the paper reports that the loop itself gamed the metric, leaked the target or found a metric-winning bug (this value takes precedence) · `N` the agent can reach test data · `NS` · `na` |

## Return

Save as `coder2.csv` (keep the header and the `key` column unchanged) and send it back. Then the two coders
compare disagreements against the paper text. The first, independent sheet is what the paper reports as
agreement, so please do not edit it after seeing the first coding.
