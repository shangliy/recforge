# Third verification pass: fact check of the second-sweep rows

- **Date:** 2026-10-27.
- **Scope:** the seven rows added in the second sweep, which the earlier passes did not cover: `fu2026evopilot`
  (EvoPilot), `chandran2026autoresearch` (Amazon AutoResearch), `pilot2026` (PILOT), `jiang2026abagent` (A/B Agent),
  `zhang2026dmrl` (DMRL), `yao2026feedbackcontract` (Feedback Contract) and `wang2026pear` (PEAR). For each row, every
  coded column of `audit.csv` (level, meta, evaluator, c1–c9, incident, online, ab_role, ab_rounds, ab_duration, ab_ci,
  ab_correction, ab_confirm, code, llm_named) was checked, and every sentence of `draft/paper.tex` that cites one of
  these keys.
- **Method:** an LLM agent read the arXiv full text of the version listed in `audit.csv` (2609.21257v1, 2609.30541v1,
  2608.18637v2, 2608.04625v1, 2609.02170v1, 2610.28798v1, 2609.35031v1) and checked (a) that each quote in
  `evidence-part3.md` and `evidence-online-gates.md` appears verbatim (whitespace, hyphenation, LaTeX escapes such as
  `\%`, `\times`, `\pm`, `{\sim}` and math symbols such as `\mathcal{V}` ignored), and (b) that the source supports the
  code under the codebook in `audit/README.md`. The authors reviewed the result.
- **Verdicts:** `supported`; `quote not found`; `code not supported`; `ambiguous` (the code is defensible but the text
  admits another reading).

`c7` is free text and not scored; it was read for accuracy only and is not counted as a cell.

## 1. Per-row checks

### 1.1 EvoPilot (`fu2026evopilot`, 2609.21257v1)

| column | code | verdict | note |
|---|---|---|---|
| level | L1+L2 | supported | Serving/config edits (interaction head, candidate depth, task-score weights) and capacity/loss retrains across the seven directions (§5, Table 4). |
| meta | N | supported | The incident catalog stays "advisory until a lesson is encoded as an executable check" (§6); the domain skill is versioned by people. No loop step rewrites the proposer's instructions, tools or weights. |
| evaluator | N | ambiguous | §5.2 records "the aggregate metric changed meaning" (evaluator revision drift), but this was an external metric-aggregation change caught as a failure, not a designed change of the loop's evaluator. `N` is defensible under the codebook's "the loop's evaluator ... changes during the run"; the codebook does not say whether unplanned infrastructure revisions count. |
| c1 | ranking-ns | supported | "Offline evaluation replays held-out pairs against one candidate pool" (§5.1); hit-rate at K=3000; the pool size is not stated (§3.2, §5.1). |
| c2 | test | supported | One held-out replay set both selects and reports; e.g. the click-only blend and the 6k depth are chosen on it (§5.4). |
| c3 | N | supported | Same replay set used for selection and reporting (§5.1, §5.4). |
| c4 | P | supported | "Two publications with the same model, configuration, and pinned data differed by 0.36 points" (§5.1): a run-to-run noise estimate, no repeated session. |
| c5 | P | supported | Offline selection followed by an online A/B on a different population (§5.5, Table 6): "Offline hit-rate and online GSRR have different populations and denominators" (§5.1). |
| c6 | N | supported | "The primitive autoresearch baseline is a retained incident, not a concurrent randomized workflow comparison" (§6). |
| c8 | production | supported | "the baseline left the head disabled" (§3.2). |
| c9 | P | supported | Human-gated, fail-closed pair verifier (§4); a date-order guard added after the leakage incident (Table 3). No statement that the agent cannot reach test data, so not `Y`. |
| incident | Y | supported | "a favorable result used an evaluation date inside the candidate model's training window, so the result was retracted" (§5.2). |
| online | 7d+sig | supported | Seven-day A/B; "+0.66\%, a statistically significant increase" (§5.5, verbatim modulo `\%`). |
| ab_role | confirm | supported | "It is separate from both the preceding 37-day agentic campaign and the randomized online experiment"; "The online A/B is a separate downstream endpoint" (§5.5). |
| ab_rounds | 1 | supported | One online A/B (§5.5, Table 6). |
| ab_duration | Y | supported | Seven days stated (§5.5). |
| ab_ci | Y | supported | Significance asserted ("statistically significant increase", §5.5); no interval or p-value, which the `online` code records as `sig`. |
| ab_correction | na | supported | `confirm` row. |
| ab_confirm | Y | supported | The A/B is separate from the selecting campaign (quotes under ab_role). |
| code | N | supported | No repository or release statement found. |
| llm_named | Y | supported | Claude Opus 4.7/4.8 and Claude Haiku (§5.1). |

Evidence-file note (not a coded cell): the reliability quote "the control realized (3000,3000) while the treatment
realized (3000,600)" in `evidence-part3.md` b1 is a paraphrase. §5.3 reads "the control realized K_eff=3000 while the
treatment realized K_eff=600" (math rendering). All other EvoPilot quotes were found.

### 1.2 Amazon AutoResearch (`chandran2026autoresearch`, 2609.30541v1)

| column | code | verdict | note |
|---|---|---|---|
| level | L1+L2+L3 | supported | System B tunes semantic-ID tokenizer configurations (L1, L3); System A rewrites training code (L2) (§II-A, §II-B). |
| meta | N | supported | Algorithm 1 updates `program.md` with scores and summaries, but "The evaluator and program.md are immutable to the agents" (Fig. 1); System B memory is maintained by people. Persisted memory of outcomes alone is `N` under the codebook. |
| evaluator | N | ambiguous | Between runs, people added an `n_levels` guardrail and a tertiary usability metric after the codebook-size gaming (§III-E); the coherence weights are "fixed across all System B runs". The agent cannot change the evaluator, but the objective did change during the twelve-week campaign by human action. `N` holds if "the loop's evaluator" means changes made by the loop; the codebook does not settle this. |
| c1 | full | supported | FAISS IVF+Flat retrieval of the top 6 over the catalog (§II-A). Caveat already noted in the paper: the index covered about 17% of items until the text-only fallback (§V-B). |
| c2 | test | supported | Keep rule on the Evaluator score (Algorithm 1); "The trajectory in Figure 2 reports Recall@6 on the held-out evaluation set" (§V-B), the same set used to keep modifications. |
| c3 | N | supported | The headline is the trajectory's peak on the selection set: "The peak (6.90%, iter-12) is a 1.82 \times lift over the hand-tuned baseline" (§IV-B). |
| c4 | P | supported | One model re-evaluated "on 11 distinct customer-purchase dates; ... mean 6.18% \pm 0.28 pp" (§V-E); no repeated session. |
| c5 | P | supported | Same 11-date re-evaluation plus a full-scale re-test for System B (§V-E). |
| c6 | N | supported | Configuration-level AutoResearch is an LLM arm, not a non-LLM search (§V-A). |
| c8 | tuned | supported | "The hand-tuned baseline ... is the product of four engineer-weeks of manual work" (§II-A). |
| c9 | P | supported | "The evaluator and program.md are immutable to the agents" (Fig. 1); "the agent can read the evaluator's output but cannot change its code" (§V-E). |
| incident | Y | supported | "the agent discovered that maximizing codebook size trivially improves weighted coherence" (§III-E). |
| online | none | supported | "We report this as an offline study; an online pilot of the embeddings is underway" (§V-A). |
| ab_role ... ab_confirm (6 cells) | na | supported | No online experiment. |
| code | N | supported | Proprietary data; no repository. |
| llm_named | Y | supported | claude-sonnet-4-6 and claude-opus-4-6 via Bedrock. |

Evidence-file note: "~8 engineer-weeks" (c7 free text) paraphrases "We estimate AutoResearch saved approximately 8
engineer-weeks across both systems" (§VI). All other quotes were found modulo LaTeX rendering.

### 1.3 PILOT (`pilot2026`, 2608.18637v2)

| column | code | verdict | note |
|---|---|---|---|
| level | L1 | supported | Ranking-objective weights per user segment chosen from a "rule-generated legal-command envelope" (Abstract, §2). |
| meta | Y | supported | The Memory Curator "asynchronously distills experiment outcomes into strategy-level domain knowledge and provenance-tracked methodology" (Abstract); Methodology Experience entries are pulled into the next task at playbook assembly (§3.1), changing the Manager's operating instructions. |
| evaluator | N | supported | Decision criteria are "Pre-registered" (§4.3); no change during the run. |
| c1 | online | supported | All headline numbers are online IPV/transaction lifts (Abstract, §6.2). |
| c2 | online | supported | Promote/reject/continue verdicts on online bucket results (§4.3). |
| c3 | na | supported | Online-selecting loop. |
| c4 | N | supported | One five-day deployment; no repeated session or noise estimate of the loop. |
| c5 | N | supported | Confirmation is designed ("a single pre-registered test on D_confirm ... The test runs once", §3.4) but no result is reported. |
| c6 | N | supported | ROAM is itself an LLM agent (§6.1); the 2x2 ablation is "Planned" (§6.3.1). |
| c8 | production | supported | "Five experiment buckets (21–25) run challenger configurations against a fixed baseline group (B0)" (§6.1). |
| c9 | P | supported | "a deterministic Manager Guard generates a legal-command envelope ... and the Manager selects only from this envelope (bounded)" (§2). |
| incident | N | supported | None reported. |
| online | 5d | supported | "We report the first five days." (§6.1). |
| ab_role | select | supported | Verdicts per round on bucket results (§4.3). |
| ab_rounds | NS | supported | Rounds per bucket not enumerated; Table 7 gives only per-bucket status ("retuned once", "untouched", "one structural pivot"). |
| ab_duration | Y | supported | Five days reported, seven-day window (§6.1). |
| ab_ci | N | supported | Table 7 gives point estimates only; the one 95% interval is an illustrative S1 bundle entry, "The values in the Strategy Evidence entry are illustrative" (§5.3), not the headline. |
| ab_correction | P | supported | "statistical thresholds are jointly calibrated across the multi-arm comparison to control the overall error rate" within a round (§4.3), not across rounds. |
| ab_confirm | P | supported | Confirmation designed (§3.4), not reported. |
| code | N | supported | No repository found. |
| llm_named | N | supported | No model name in the text. |

Note (not a coded cell): the abstract's "+0.96% transaction count" is bucket 25; the best bucket by IPV (bucket 23)
has +0.95% (Table 7). The headline takes the per-metric maximum across buckets. `paper.tex` does not quote this
number.

### 1.4 A/B Agent (`jiang2026abagent`, 2608.04625v1)

| column | code | verdict | note |
|---|---|---|---|
| level | L1 | supported | "After adjusting the objective weights and decision thresholds" (§5.4); strategy parameter configurations (§3.3). |
| meta | N | supported | The experience tree stores outcomes ("validated outcomes are distilled back into the strategy experience tree", §4); memory of outcomes only. |
| evaluator | N | supported | Utility U(v) (Eq. 8) fixed. |
| c1 | online | supported | Headline "4.829% increase in GMV" online (Abstract, §5.6). The offline LLM-judge scores (§5.2) rate strategy text, not the recommender. |
| c2 | online | supported | "the agent performs local search around its promising parameter range" on online A/B rounds (§3.3). |
| c3 | na | supported | Online-selecting. |
| c4 | N | supported | One trajectory. |
| c5 | N | supported | Table 5 (§5.6) repeats Strategy 5 of the selecting rounds (Table 3); no separate check. |
| c6 | N | supported | Baselines are LLMs and RAG agents (§5.2). |
| c8 | production | supported | "The root represents the production baseline or initial strategy" (§3.3); an expert-designed strategy is also compared (§5.3). |
| c9 | P | supported | "rule-based validators check formatting, numerical ranges, parameter types, and configuration consistency, while agent and human reviewers assess safety" (§4). |
| incident | N | supported | None reported. |
| online | yes | supported | No duration or interval for the headline. |
| ab_role | select | supported | §3.3, §5.3. |
| ab_rounds | 5 | supported | Strategies 1–5 (Table 3, §5.3). |
| ab_duration | NS | supported | "experiment duration" is extracted as an input (§3.3) but no duration is reported. |
| ab_ci | N | supported | Confidence weights ρ_j are used internally (Eq. 5); no interval or test on the headline. |
| ab_correction | N | supported | None. |
| ab_confirm | N | supported | Table 5's GMV, GPM, OPM, clicks and orders equal Strategy 5 in Table 3 (Table 5 adds CVR +0.578%). |
| code | N | supported | No repository. |
| llm_named | Y | supported | "GLM-5.1 serves as the foundation model" (§4). |

### 1.5 DMRL (`zhang2026dmrl`, 2609.02170v1)

| column | code | verdict | note |
|---|---|---|---|
| level | L1 | supported | The frozen task agent adjusts "advertising AB parameters in real time" (§1); "restricted to a predefined whitelist of parameters and permissible value ranges" (§5.1.2). |
| meta | Y | supported | The upper-level optimizer (Qwen3-8B) is trained with DRPO and rewrites the skill document that the task agent loads each round (§3, §5.1.2). |
| evaluator | N | supported | The Long-term Reward Predictor is trained before the loop (Algorithm, Phases I–III); no change during the run is described. |
| c1 | online | supported | Headline LTV lifts are online (Abstract, Tables 2–7). |
| c2 | online | supported | "The environment returns short-term outcomes and treatment–control comparison signals" from the online experimentation environment (§5.1.2). |
| c3 | na | supported | Online-selecting. |
| c4 | N | supported | No repeated session with spread. |
| c5 | N | supported | Each table is its own window; "All conclusions are restricted to within-table comparisons" (§5.1.3); no held-out check of a selected candidate. |
| c6 | N | supported | HPO appears only as motivation (§1); baselines are LLM skill optimizers (SAGE, SkillOpt, SKILLRL). |
| c8 | production | supported | The control group runs the production configuration (§5.1.3). |
| c9 | P | supported | "To mitigate operational risks, the Task Agent is restricted to a predefined whitelist of parameters and permissible value ranges" (§5.1.2). |
| incident | N | supported | The memory bank uses only matured outcomes, "preventing temporal information leakage" (§5.1.1): a design, not an incident. |
| online | yes | supported | No interval or significance test; CUPED variance reduction only (§5.1.3). |
| ab_role | select | supported | DRPO rollouts are scored on online treatment–control signals (§5.1.2). |
| ab_rounds | NS | supported | "sample 8 rollouts in DRPO iteration" (§5.1.2); number of online rounds not stated. |
| ab_duration | NS | ambiguous | "7-day cumulative metric mitigates the impact of short-term fluctuations" (§5.1.3). The adjudication read this as a metric horizon, not an experiment length (paper.tex appendix says so); a reader could take it as a stated minimum duration. `NS` is the conservative reading. |
| ab_ci | N | supported | No intervals or p-values in Tables 2–7. |
| ab_correction | N | supported | None. |
| ab_confirm | P | supported | "experiments in different tables are conducted during non-overlapping time windows" (§5.1.3), but the text does not say whether these windows are separate from the training rollouts. |
| code | N | supported | No repository. |
| llm_named | Y | supported | "we instantiate the optimizer with Qwen3-8B ... we employ OpenAI Codex as the frozen Task Agent, using GPT-5.5 as its underlying model" (§5.1.2). |

Table values confirmed: full DMRL LTV +0.052 (Table 2), +0.042 (Table 3), +0.021 (Table 4), +0.052 (Table 5,
identical to Table 2), +0.064 (Table 6), +0.050 (Table 7); best baseline in Table 2 LRP+SkillOpt +0.024. Quotes with
LaTeX escapes ("DRPO achieves the highest LTV of +0.021\% among all variants", §5.3.2; "DRPO outperforms SAGE,
SkillOpt, and SKILLRL by +0.101\%, +0.028\%, and +0.048\%", §5.2; "Each edited skill S_{i}", §3) were found.

### 1.6 Feedback Contract (`yao2026feedbackcontract`, 2610.28798v1; comparison)

| column | code | verdict | note |
|---|---|---|---|
| level | L2 | supported | Agents develop models "by editing code, running experiments" (Abstract). |
| meta | na | supported | Comparison row. |
| evaluator | na | supported | Comparison row. |
| c1 | auc | supported | "we report AUC" (Criteo, §5.1). MSLR uses "macro NDCG@10" (§5.1), so the row mixes AUC and a ranking metric; `auc` follows the Criteo headline. |
| c2 | val | supported | "It can reach \mathcal{V} only through the harness, which keeps the labels" (§3). |
| c3 | Y | supported | "A final model is named before any test feedback exists ... \mathcal{H} is then evaluated once" (§4.1, C4). |
| c4 | Y | supported | "We run three independent attack seeds for Criteo and MSLR and five for the no-signal control" (§5.1); Table 2 reports mean ± SE. Authors' caveat: "three seeds on the real datasets cannot separate a small effect from none" (§6). |
| c5 | Y | supported | The validation–test gap is the primary metric (§5.1, Tables 2–5). |
| c6 | N | supported | The label-permuted control ("any apparent gain is selection noise by construction", §5.1) is a null task, not a non-LLM search arm. |
| c8 | seed | supported | Comparisons are against the provided base models (hashed logistic regression, HistGradientBoostingRegressor base ranker, base rate on the control; §5.1); no separate tuned baseline. |
| c9 | Y | supported | "\mathcal{V} is reachable only by submitting a candidate ... \mathcal{H} is unreachable while the agent iterates" (§4.1, C1). |
| incident | N | supported | The inflated gain under exact feedback is the designed experimental outcome, and the authors state "Neither agent was gaming anything" (§5.2). |
| online | none | supported | Public offline datasets only. |
| ab_role ... ab_confirm (6 cells) | na | supported | No online experiment. |
| code | N | supported | No repository found. |
| llm_named | Y | supported | "GPT-5.6-Sol (Codex)" and "Claude Sonnet 4.6" (Table 5, §5.5). |

Table 2 gaps confirmed: Criteo 0.0060 (exact) vs 0.0055 (contract); MSLR 0.0134 vs 0.0123; no-signal 0.0163 vs
0.0000; all runs under "a maximum of 30 submissions". All evidence quotes were found once `\mathcal{V}` and
`\mathcal{H}` are read as V and H.

### 1.7 PEAR (`wang2026pear`, 2609.35031v1; comparison)

| column | code | verdict | note |
|---|---|---|---|
| level | L1 | supported | "The search space is currently restricted to strategy-level parameters" (§8). |
| meta | na | supported | Comparison row. |
| evaluator | na | supported | Comparison row. |
| c1 | online | supported | Headline: strategies "significantly increased Main Order/DAU by 2.7336% and 3.2957%" (Abstract). |
| c2 | online | supported | Last gate among several promoted candidates is decision-grade online evaluation; "A candidate is promoted when the interval lies entirely above zero" (App. A). |
| c3 | na | supported | Online-selecting. |
| c4 | P | supported | Candidate generation includes interventions that "replicate previous observations" (§5.1); Table 2 traces replication; no repeated session with spread. |
| c5 | P | supported | Two candidates tracked across L2/L3/L4 (Table 5): "Order proxy +45.88\%", "Observed order +15.48\%", "Main Order/DAU +2.73\%" (candidate A); +61.64% / +29.76% / +2.16% (candidate B). Task B Phase I: 5 promoted, L4 outcome "No significant gain" (Table 3). |
| c6 | N | supported | Bayesian optimisation is a prompting principle: the principles "guide qualitative reasoning about observed effects and uncertainty rather than specifying a" BO algorithm (§5.1). |
| c8 | production | supported | "the deployed baseline is G=(2,1)" (§6.2). |
| c9 | NS | code not supported | The paper states constraints on the loop: each task runs "within a predefined objective and intervention scope" (§1, §4), the search space is "restricted to strategy-level parameters" (§8), and "Before any candidate is exposed to real-user traffic, the proposed change and supporting evidence undergo human review and require explicit human confirmation; automated promotion within the Verifier Ladder cannot independently initiate such exposure" (§9). Under the codebook (`P`: gates, bounded actions) and for consistency with PILOT, A/B Agent and DMRL (all `P` on whitelists, validators or reviewer gates), the code should be `P`. |
| incident | N | supported | None reported. |
| online | CI | supported | "dark-green boldface indicates statistical significance at p<0.05" (Table 6). Strictly this is a significance test, which the codebook lists together with CI. |
| ab_role ... ab_confirm (6 cells) | na | supported | Comparison rows are not coded on ab_* (all seven comparison rows are `na`). |
| code | N | supported | No repository. |
| llm_named | N | supported | No model name in the text. |

Evidence-file note: `evidence-part3.md` b7 C5 says proxy effects were "inflated about 3× and 13–28×". From Table 5,
the shadow-traffic proxy (L2) is 16.8× (A) and 28.5× (B) the decision-grade effect (L4); rapid online (L3) is 5.7× and
13.8× L4; L2 is 3.0× and 2.1× L3. The "3×" is L2 vs L3, not vs L4, and the three metrics differ (order proxy, observed
orders, Main Order/DAU). All PEAR quotes were found (the Table 5 percentages modulo `\%`).

## 2. Sentences in `draft/paper.tex`

| line(s) | sentence (abridged) | verdict | note |
|---|---|---|---|
| 114–116 | A concurrent controlled study on CTR and LTR data shows exact validation feedback lets a coding agent overfit the validation split, and a feedback contract with a quarantined test set removes the spurious gain on a no-signal task (Feedback Contract). | supported | Table 2: gap 0.0163 → 0.0000 on the control; positive gaps on Criteo and MSLR. |
| 165–169 | Comparison points include e-commerce search strategy (PEAR) and a controlled study of agent feedback on public CTR and LTR data (Feedback Contract). | supported | Criteo and MSLR-WEB10K (§5.1). |
| 392–409 | Taxonomy table: A/B Agent and PEAR in L1/LLM; PILOT^m and DMRL^m; EvoPilot (L2), Amazon AutoResearch (L3), Feedback Contract (L2, comparison). | supported | Matches `level`/`meta` in `audit.csv`. |
| 436–440 | PILOT has LLM roles choose ranking-objective weights for user segments from a legal-command envelope generated by deterministic services; A/B Agent iterates strategy parameters across online rounds with a hierarchical experience tree; DMRL trains a small LLM with RL to rewrite the skill document an ad-tuning agent follows. | supported | PILOT Abstract, §2; A/B Agent §3.3; DMRL §5.1.2 (Qwen3-8B, DRPO). |
| 441–443 | An e-commerce search loop adds a multi-fidelity ladder from shadow-traffic proxies to decision-grade online tests (PEAR). | supported | §5.2. |
| 485–487 | EvoPilot runs a 37-day campaign of agent-proposed configuration and retraining changes behind a fail-closed verifier and catalogues its failures. | supported | §4, §5, Table 4. |
| 487–489 | Amazon's AutoResearch rewrites the training code of a book-retrieval model and tunes a semantic-ID tokenizer in a twelve-week campaign of more than 220 experiments. | supported | "twelve-week campaign" (§V-A); "220+ agent-d[riven experiments]" (§VI); §II-C. |
| 503–505 | Amazon's AutoResearch is the first audited production loop that edits a semantic-ID tokenizer, and the first in which the agent gamed a tokenizer metric. | ambiguous | Gaming supported (§III-E). "Production loop" reads as deployed, but the paper reports "an offline study" with an online pilot "underway" (§V-A); it describes production-scale systems. Suggested wording: "the first audited production-scale loop". |
| 538–542 | PILOT carries methodology across experiments; DMRL trains a small LLM to rewrite the skill document. | supported | PILOT Abstract ("provenance-tracked methodology"), §3.1; DMRL §5.1.2. |
| 631 | Agents introduced hard negatives (incl. Amazon). | supported | "hard-negative contrastive learning [24, 25, 26]" (§V-A). |
| 713–717, 725–726 | Audit-table rows for the seven systems. | supported, except PEAR c9 | Each cell matches `audit.csv`. PEAR's c9 `\ns` would become `\pa` under the proposed correction. |
| 737 | A text-only fallback "expanded catalog coverage by 5.8$\times$" (Amazon). | supported | Abstract. |
| 746–748 | Amazon "retains modifications that improve a held-out scalar metric" and headlines the trajectory's peak; EvoPilot selects and reports on one held-out replay set. | supported | Amazon Abstract, §IV-B; EvoPilot §5.1, §5.4. |
| 772–773 | EvoPilot reruns on pinned data "differed by 0.36 points"; Amazon re-evaluates one model across 11 dates ("6.18% ± 0.28 pp"). | supported | EvoPilot §5.1; Amazon §V-E (`\pm`). |
| 792 | Amazon's 1.82× peak is "~2.6σ above the across-date mean" of 1.63×. | supported | §V-A ("{\sim} 2.6 \sigma", "Even the across-date mean preserves a 1.63 \times lift"). |
| 796–798 | In an e-commerce search loop, effects on a shadow-traffic proxy were several to tens of times larger than in decision-grade online experiments, and five promoted candidates showed no significant gain (PEAR). | ambiguous | Second clause supported (Table 3, Phase I: 5 promoted, "No significant gain"). For the first clause, shadow-traffic (L2) vs decision-grade (L4) is 16.8× and 28.5× for the two candidates in Table 5, so "several" fits only the rapid-online stage (5.7×); the metrics also differ by stage. Suggested wording: "effects on a shadow-traffic proxy were 17 and 29 times the decision-grade online effects for the two candidates traced (on different metrics)". |
| 800–802 | On a label-permuted task, a coding agent given exact validation scores "ended by reporting a gain of 0.0157" (Feedback Contract). | supported | Abstract; §5.2 ("Exact ends with a reported gain of 0.0157"). |
| 851–854 | EvoPilot leakage quote ("... model's training window, so the result was retracted"); the paper does not say whether the agent or a person chose the date, or what caught it. | supported | §5.2; no attribution found. |
| 854–856 | In Amazon's semantic-ID loop, "the agent discovered that maximizing codebook size trivially improves weighted coherence"; human QA between runs caught it. | supported | §III-E; "human QA between runs diagnosed metric fixation early on" (§IV-E). |
| 893 | A/B Agent's headline GMV lift repeats the numbers of its fifth strategy round. | supported | Table 5 vs Table 3, Strategy 5 (+4.829% GMV, +4.677% GPM). |
| 900–904 | PILOT designs its final confirmation as "a single pre-registered test" that "runs once", because "the data collected while searching ... cannot also serve as proof", but the report does not include it; its headline compares the best of five buckets before and after, "not randomized". | supported | §3.4; §6.1 (five buckets); §6.3.1 ("The comparison in §6.2 is before/after, not randomized"). |
| 904–905 | DMRL does not say whether its comparison windows are separate from its training rollouts. | supported | §5.1.2–§5.1.3. |
| 905–909 | DMRL's full configuration appears in six tables in "non-overlapping time windows", LTV +0.021% to +0.064% (five distinct values; one table repeats the main table), spread 0.043 pp, larger than its 0.028-point lead; authors restrict conclusions to within-table comparisons. | supported | Values in 1.5: distinct {0.021, 0.042, 0.050, 0.052, 0.064}; 0.064 − 0.021 = 0.043; 0.052 − 0.024 = 0.028; "All conclusions are restricted to within-table comparisons" (§5.1.3). |
| 1104–1109 | DMRL duration changed to not stated because its seven days are a metric horizon; PILOT's joint calibration within a round credited as partial correction. | supported | DMRL §5.1.3; PILOT §4.3. |

## 3. Summary

- **Cells checked:** 147 (7 rows × 21 coded columns; `c7` read but not scored).
  - supported: 143
  - ambiguous: 3 (EvoPilot `evaluator`, Amazon `evaluator`, DMRL `ab_duration`)
  - code not supported: 1 (PEAR `c9`)
  - quote not found: 0 (two evidence-file quotes are paraphrases of text that is present: EvoPilot "(3000,3000) ... (3000,600)" and Amazon "~8 engineer-weeks"; neither backs a coded cell)
- **Sentences checked:** 24 sentence groups in `draft/paper.tex`: 22 supported, 2 ambiguous (lines 503–505, 796–798).

### Proposed corrections

1. `audit.csv`, `wang2026pear`, `c9`: `NS` → `P` (quote: §9, "Before any candidate is exposed to real-user traffic, the
   proposed change and supporting evidence undergo human review and require explicit human confirmation"; §8, "The
   search space is currently restricted to strategy-level parameters"). Update `evidence-part3.md` b7 C9 and regenerate
   the audit table with `summarize.py` (paper.tex line 726, `\ns` → `\pa`).
2. `paper.tex` lines 796–797 (PEAR): replace "several to tens of times larger" with the stage-specific ratios (shadow
   proxy 17× and 29× the decision-grade effect for the two candidates, on different metrics), or say "more than ten
   times larger".
3. `paper.tex` line 504 (Amazon): "first audited production loop" → "first audited production-scale loop", since the
   paper reports an offline study.
4. `evidence-part3.md` b7 C5: correct "inflated about 3× and 13–28×" to the Table 5 ratios (L2/L4 16.8× and 28.5×;
   L3/L4 5.7× and 13.8×).
5. `evidence-part3.md` b1 and b2: mark the two paraphrases as paraphrases or replace them with the verbatim text
   ("the control realized K_eff=3000 while the treatment realized K_eff=600", §5.3; "approximately 8 engineer-weeks",
   §VI).
6. Optional, codebook: state whether `evaluator` = `Y` covers changes to the objective made by people or infrastructure
   during a run (Amazon's added `n_levels` guardrail and usability metric; EvoPilot's metric-aggregation change), or
   only changes made by the loop. Under the current reading both stay `N`.

## Corrections applied after author review

- `wang2026pear` `c9`: NS → P (audit.csv and evidence-part3.md b7). PEAR is a comparison point, so no core count changes.
- evidence-part3.md b7 C5: the stage ratios are restated from Table 5 (16.8× and 28.5× shadow proxy vs decision-grade;
  5.7× and 13.8× rapid online vs decision-grade).
- evidence-part3.md b1 and b2: the two paraphrased quotes are replaced by the verbatim text.
- paper.tex: PEAR's proxy inflation is stated as 17 and 29 times for the two traced candidates, on different metrics per
  stage; Amazon AutoResearch is described as a production-scale loop (the paper reports an offline study with an online
  pilot underway).
- The three ambiguous `evaluator` / `ab_duration` cells are kept as coded.
