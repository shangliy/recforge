# Design fields of the 27 core systems: evidence

Extracted 2026-10-22 from the full arXiv text (LLM-assisted, reviewed by the authors). Fields and definitions: see README.md. Part 1 covers the first 14 systems of audit.csv, part 2 the remaining 13.


Source: full arXiv HTML text, fetched 2026-10-22, plus `audit/evidence-part1.md`. Quotes are verbatim (math rendered as plain text, `...` marks elisions) and at most about 25 words. "not stated" means the paper does not say. `*` in signal_chain marks the stage that decides keep/reject inside the loop.

## Proposed corrections to audit.csv

> Status: applied in v2 (see README.md, "Changes in v2") except Auto-RecSys `c2`/`c3`, which stay `na` because the paper reports no selection result, and Sortify `llm_named`, which stays `Y`.

1. **EvoRec level `L2` -> `L2+meta`** (or `L1+L2+meta`). The Skill library is evolved by the loop, which is the same reason AgentX, Auto-RecSys and AgenticRecTune carry `+meta`. Quote: "a multi-agent framework that co-evolves the recommendation model and the optimization methodology driving it" (Abstract).
2. **Auto-RecSys c2 `na` -> `NS`, c3 `na` -> `NS`.** The codebook reserves `na` for online-only systems. Auto-RecSys trains offline and compares against a baseline: "the analysis computes performance differences against the baseline and assigns a verdict of positive, neutral, or negative" (Sec 5.3).
3. **c9 `na` -> `P` for CORAL, AgenticRecTune, Sortify and GEARS** under the new definition, where `na` needs both no touchable offline data and no stated constraints:
   - CORAL: "feasibility checks, bounded-change limits, and safety constraints" (Sec 4.3).
   - AgenticRecTune: "Before online A/B testing starts, the users' review is required." (Sec 4.2.2); Critic checks "system guardrails, instruction constraints" (Sec 4.1.3).
   - Sortify: offline proxy on logged data, plus "--sandbox read-only" and "seven-layer safety pipeline" (Sec 2.5.4).
   - GEARS: works on tabular experiment records; "A policy is admitted only if all its features satisfy φ_shift≤τ" (Sec 4).
4. **Google/YouTube c9 `NS` -> `P`** (soft). "the definition of the loss function L_proxy remains invariant. While the model changes, the yardstick measuring its performance does not." (Sec 4.1.1). Prompt guardrail: "Keep Metric#3 ≤+1%" (Fig. 3).
5. **Level refinements (minor):**
   - RecHarness `L2` -> `L1+L2`. Arms include "tuning learning-rate schedules, adjusting dropout or weight decay".
   - NOVA `L2` -> `L1+L2`. ScaleUp "searches over coupled structural hyper-parameters, including token_cnt, token_dim".
   - AgentX `L2+meta` -> `L1+L2+meta`. The strategy track edits ranking formulas and strategy parameters, e.g. "S_1=B_r·(1+βP)" (Table 10).
   - EvoRec also edits lr and negative counts (Table 3).
6. **Sortify llm_named `Y` is generous.** Only "an LLM through the Codex CLI" and reference prices for GPT-5.4 / GPT-5.3-Codex are given (Sec 2.5.4, 4.9). Suggest `P`, or N with a note.
7. **Data-integrity flag, EvoRec Table 1 (Industrial).** R@10 is below R@5 in every column (e.g. Evo-MGUI R@5 0.0775, R@10 0.0571), and N@5 exceeds R@5 (SASRec 0.0919 vs 0.0701). Neither is possible for leave-one-out Recall/NDCG. Worth a footnote if EvoRec numbers are cited.
8. **VirtualMLE text vs table.** The text says "+13.1% N@5 on Baby" vs AutoML (Sec 4.2), but the Table 1 maximum is +12.1%. The +13.1% matches the N@10 comparison with OpenOneRec.
9. **Possible extra `+meta` (judgment):**
   - VirtualMLE: cross-dataset Cognition Summary.
   - Self-EvolveRec: the diagnosis tool co-evolves.
   - AgentX-Model: human-approved tool/instruction repair.
   - NOVA: KB rules committed between tasks.
   - Sortify: the LLM recalibrates the search objective.

   The `meta` column below marks these Y with the reason, so the survey can apply one consistent rule.


## Self-EvolveRec (`kim2026selfevolverec`, arXiv 2602.12612)

- **object**: L2
- **proposer**: llm
- **proposer_note**: LLM planner turns user-simulator critiques + diagnosis-tool reports + retrieved arXiv papers into a development report; GPT-5 coder edits the whole pipeline codebase; parent sampled from archive
- **meta**: Y ⟨superseded: released `meta` is N, with the evaluator marked as evolving (design.csv); this line is the first extraction⟩: the Model Diagnosis Tool (feedback/probe code) co-evolves with the codebase each iteration; evolving the user simulator is an optional variant (Sec 4.3.4), not the default
- **signal_chain**: offline* (validation score, Eq. 1); efficient variant: proxy* (zero-cost proxies). Simulator and diagnosis feedback steer edits but do not gate them
- **memory**: evolutionary archive/population of codebases, feedback reports and DIAG versions
- **acceptance**: every successfully executing codebase is added to the archive; parents sampled from the archive; final codebase = argmax of validation score (no explicit keep-if-better gate stated)
- **guards**: none stated beyond successful execution
- **human_role**: none stated
- **llm**: GPT-5-mini (planning, retrieval, user simulator); GPT-5 (coder); Claude Opus 4.6 variant (App. H.1)
- **kept_edits**: data: category-aware hard negatives (SASRec/CDs iter 0->1, HR 0.4676->0.5138); loss: popularity-annealed weighting (same step); architecture: LM-augmented bi-encoder embedding genre tags (Random seed, HR 0.0525->0.3737); loss: InfoNCE loss with an MF module (same step); architecture: Time-RoPE sequence encoding (Random seed iter 5, HR->0.5070)
- **headline_gain**: abstract gives no number ('significantly outperforms'); Table 1 e.g. SASRec/CDs NDCG@5 0.3559->0.3865 vs DeepEvolve 0.3610
- **baseline_type**: seed program (also AlphaEvolve/DeepEvolve from the same seed; untuned shared hyperparameters)
- **c9_isolation**: NS
- **c9_incident**: N
- **c4_note**: single runs; no seeds, repeated evolution sessions or noise estimate reported (Tables 1-12)

Evidence:

- *proposer*: "By integrating qualitative insights from the user feedback report (R_SIM) and quantitative findings from the diagnosis report (R_DIAG)" (Sec 3.2)
- *proposer*: "We employ GPT-5-mini for planning and retrieval, while utilizing GPT-5 as the coding agent for all frameworks." (Sec 4, Implementation Details)
- *meta*: "we design Diagnosis Tool - Model Co-Evolution, which dynamically updates DIAG to (i) inspect new components and (ii) translate SIM's qualitative critiques into measurable metrics" (Sec 1)
- *meta*: "Although our framework employs a fixed user simulator for efficiency, we further investigate the impact of evolving the user simulator" (Sec 4.3.4)
- *signal_chain*: selection objective is "score(B) = M(f_B(E_val, X; θ*_B))" (Eq. 1, Sec 2)
- *signal_chain*: "replaces full training with zero-cost proxies ..., which estimate pipeline potential through a single forward-backward pass on a representative mini-batch" (Sec 3.4)
- *memory*: "maintaining an Evolutionary Archive P(t) that stores the comprehensive history of codebases and feedback" (Sec 3.2)
- *acceptance*: "Upon successful execution, the new codebase B(t+1) is incorporated into the population history P(t+1)" (Sec 3.2)
- *c9_isolation*: "DIAG(t) directly accesses the model parameters θ and data loaders within the codebase" (no statement on test-split access) (Sec 3.1.2)
- *kept_edits*: "the agent introduced "Category-Aware Hard Negatives" and "Popularity-annealed Weighting," resulting in an immediate performance increment (HR: 0.4676→0.5138)" (Sec 4.3.6, Fig. 5)
- *kept_edits*: "introduced an "LM-Augmented Bi-Encoder" to embed "Genre Tags" and utilized the InfoNCE loss with an MF module" (App. H.5.2, Fig. 9)
- *kept_edits*: "addressed it by integrating "Time-RoPE Sequence Encoding," further boosting performance to HR: 0.5070" (App. H.5.2)
- *baseline_type*: "uniformly configured all recommender models... with a user/item embedding dimension of 50, a batch size of 128, and a learning rate of 0.001" (App. D)

Note: The kept edits are from case-study trajectories (Fig. 5, Fig. 9), not a list of final best codebases. Isolation: the agent rewrites data-processing logic and DIAG reads data loaders; the paper never says whether evaluation code or the test split is protected, so NS (risk, not N).

## RecHarness (`ling2026recharness`, arXiv 2607.29241)

- **object**: L1+L2
- **proposer**: llm+space
- **proposer_note**: Thompson sampling (Beta posteriors) over human-defined edit arms (local arms; jump arms unlocked when improvement rate < tau) picks directions; a frozen LLM writes the hypothesis and code edit within each selected arm
- **meta**: N (the Experiment Skill is a within-run memory digest that conditions the LLM; it is not carried across tasks)
- **signal_chain**: offline*>online (validation HR@10 decides promotion; one selected candidate checked on offline production AUC then 7-day A/B)
- **memory**: incumbent + per-arm Beta posteriors + Experiment Skill document (incumbent, recent successful edits, rejected directions, failure reasons, validation trends)
- **acceptance**: keep-if-better on validation (incumbent replaced only by an improving valid candidate); arm reward is binary success; jump arms accepted only if the retuned branch beats the pre-jump incumbent by delta_jump
- **guards**: bounded action space (human-defined arms); isolated workspace per candidate; validation-only selection with test used once; text feedback cannot change the bandit posterior
- **human_role**: humans define objective, validation metric and candidate arms; launch approval not stated
- **llm**: not stated
- **kept_edits**: architecture: intra-sequence self-attention over six real-time behaviour sequences, each compressed to 32-d and concatenated (192-d) into the shared-bottom ranker (offline AUC +0.09%, then 7-day A/B); per-dataset kept edits for the academic runs not reported in the main text
- **headline_gain**: abstract: ADVV +2.084%, Revenue +0.534%, Exposure +0.559% in a 7-day A/B; offline: avg HR@10 +12.58% vs HSTU cold-start base (+85.85% on GRU4Rec)
- **baseline_type**: production (online); cold-start/template (offline)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: Amazon results averaged over three runs with no std/CI; repeats not stated for KuaiRec; promotions decided on single trials

Evidence:

- *proposer*: "a bandit router selects the next modification direction according to historical validation feedback, while the LLM generates a concrete optimization hypothesis and executable code edit" (Abstract)
- *object*: "tuning learning-rate schedules, adjusting dropout or weight decay, changing embedding dimensions, modifying the number of layers or attention heads, changing the sequence pooling strategy" (Methodology, edit arms)
- *acceptance*: "After executing the resulting trials, a candidate is promoted only if it improves over the incumbent" (Methodology)
- *acceptance*: "treated as successful only if it is valid, outperforms the average candidate in the same trial group, and does not fall below the historical incumbent" (Methodology)
- *acceptance*: "The jump is accepted if the retuned branch improves upon the pre-jump incumbent by a margin δ_jump>0" (Basin-aware Jump)
- *memory*: "Experiment Skill is a compact textual guide that records the current incumbent, recent successful edits, invalid or rejected directions, failure reasons" (Experiment Skill and Feedback)
- *guards*: "The Experiment Skill affects the mutation operator μ_ϕ but not the posterior update above" (Experiment Skill and Feedback)
- *guards / c9*: "Each candidate runs in an isolated workspace"; "The test set is used only once after search for final evaluation." (Experimental Settings, Search protocol / Trial execution)
- *human_role*: "human experts define the optimization objective, validation metric, and candidate arms" (Online A/B Test)
- *llm*: "ϕ denotes the frozen LLM used for code generation" (model never named) (Methodology)
- *kept_edits*: "The candidate applies self-attention to each of the six real-time behavior sequences, compresses each into a 32-dim vector via an MLP" (Online A/B Test)
- *c4_note*: "Performance on Amazon Reviews, averaged over three runs." (Table 3 caption)

Note: Object is L1+L2 because several arms are pure configuration (LR schedule, dropout, weight decay, embedding size).

## Google/YouTube (`wang2026selfevolving`, arXiv 2602.10226)

- **object**: L1+L2
- **proposer**: llm
- **proposer_note**: Offline Agent with specialised personas (optimizer, architecture, reward) proposes deltas against the production config, conditioned on the Experiment Journal sorted by offline score; reward persona runs SQL analyses over logs
- **meta**: N
- **signal_chain**: offline>online* (offline proxy: loss via compute_loss or long-watch correlation via compute_eval; LLM Online Agent ranks journal into top-K for live A/B; humans review final metrics). Reward-hyperparameter tuning used the online loop only
- **memory**: Experiment Journal (all configurations, offline scores, online metrics); daily warm start from best K findings
- **acceptance**: LLM Online Agent ranks candidates on offline + online metrics, promotes top-K to live experiments and terminates the rest; launch after human review of collected metrics; guardrail stated in the prompt
- **guards**: fixed loss yardstick for optimizer/architecture personas; delta-based edits against production file; prompt-level online guardrail (e.g., Keep Metric#3 <= +1%); persona-specific tools
- **human_role**: humans present the initial research idea and review the experiment metrics (launch decision)
- **llm**: Gemini 2.5 Pro (Gemini 2.5 Flash ablation)
- **kept_edits**: hparam: Adagrad(lr=0.1) -> RMSprop(lr=0.005, rho=0.95,...); hparam: batch size, epochs and optimizer hyperparameters giving 8x faster training; architecture: Gated Path (value_path*gate_path, GLU-like); architecture: follow-up GELU gates + layer normalisation; loss: reward with a new active-engagement factor; loss: four reward hyperparameters tuned via the online loop
- **headline_gain**: abstract gives no number ('several successful production launches'); e.g. Gated Path +0.06% YouTube-level / +0.14% surface-level, Wide&Deep +1.10% surface-level (Tables 1-2); beat 64%/73% of manual launches
- **baseline_type**: production
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: ablation averaged over 6 independent runs x 70 ideas (z-scored loss); online results single experiments with 95% CIs; no repeated evolution sessions for launches

Evidence:

- *proposer*: "Output each proposal with exactly two fields: ... "explanation" ... "delta", the change against the model's current configuration" (Fig. 2)
- *signal_chain*: "Its task is to rank the candidates to identify the top K for online experimentation." (Sec 4.2 (1))
- *signal_chain*: "This tuning was performed without offline metrics, relying exclusively on the Online Agent's slow loop to explore the parameter space." (Sec 5.3.2)
- *memory*: "the Experiment Journal – a shared, persistent knowledge base containing the history of all configurations, their offline scores, and any available online metrics" (Sec 4)
- *memory*: "we warm-start the Offline Agent's daily run with the best K findings from the preceding day" (Sec 5.6 L3)
- *guards / c9*: "the definition of the loss function L_proxy remains invariant. While the model changes, the yardstick measuring its performance does not." (Sec 4.1.1 A)
- *guards*: "Maintain system safety by enforcing: Keep Metric#3 ≤+1%" (Fig. 3)
- *human_role*: "human engineers are only required to perform the high-level step of presenting the initial research idea ... and the final step of reviewing experiment metrics" (Sec 4.2)
- *kept_edits*: "switching from the legacy Adagrad optimizer to RMSprop ... resulted in a statistically significant drop in offline loss and improvement in live traffic" (Sec 5.2.1, Table 3)
- *kept_edits*: "In total, training time improved by 8× without sacrificing business metrics." (Sec 5.2.2)
- *kept_edits*: "the agent further refined this architecture by moving from standard sigmoid gates to GELU activations combined with layer normalization" (Sec 5.2.3)
- *kept_edits*: "synthesized a reward function that incorporates a novel signal indicating whether the user is actively engaging with content" (Sec 5.3.1)
- *kept_edits*: "The agent, however, identified a solution tuning four hyperparameters in two weeks." (Sec 5.3.2)
- *c4_note*: "Results are averaged over 6 independent runs exploring 70 ideas each" (Sec 5.4)

Note: c9 coded P (audit.csv says NS): the optimizer/architecture personas are scored by a fixed tool on an invariant loss. Reward edits change the label logic and are scored by compute_eval, so only part of the loop is constrained.

## EvoRec (`mu2026evorec`, arXiv 2606.28368)

- **object**: L1+L2
- **proposer**: llm
- **proposer_note**: Research Agent combines arXiv/blog retrieval, Skill library and Memory into a hypothesis (with a diversity check); Code Agent makes minimal-diff edits and submits training
- **meta**: Y: Skill library (research/engineering/diagnosis skills) distilled from Memory every N=5 rounds by the Skill Evolver (merge/refine/create)
- **signal_chain**: offline*>online (offline metric vector, split not stated; final model in a 7-day A/B)
- **memory**: persistent Memory (hypothesis, diff, log, metrics, verdict per round, indexed) + evolving Skill library
- **acceptance**: not stated (each round gets a success/fail/neutral verdict; loop stops at T_max=50, after k=10 rounds without improvement, or at a target threshold)
- **guards**: diversity constraint on target module; infeasible hypotheses rejected by the Code Agent; no evaluation-side guard stated
- **human_role**: none stated (claims human-free operation)
- **llm**: Claude Opus 4.6 (all four agents); Qwen3.7-MAX reproduction (no numbers)
- **kept_edits**: hparam: reduce lr to 5e-4 (+0.41% R@10); data: negative samples 4->16 (+0.52%); architecture: multi-interest pooling, 4 heads (+1.03%); loss: BCE -> InfoNCE (+1.18%); data: hard-negative mining tau=0.1 via Skill #12 (+2.31%); hparam: layer-wise lr decay via Skill #16 (+0.63%)
- **headline_gain**: up to +5.54% relative offline (N@10, Books) over the strongest baseline; online +1.85% revenue, +1.02% CTR (7-day A/B, p<0.05)
- **baseline_type**: other (strongest offline baseline; base models use original-paper hyperparameters); production MGUI (online)
- **c9_isolation**: NS
- **c9_incident**: N
- **c4_note**: single numbers, no seeds or repeated sessions (Tables 1-2); online significance by two-sided test only

Evidence:

- *proposer*: "The Research Agent retrieves external knowledge (e.g., arXiv) and combines it with Skill and Memory to generate optimization hypotheses." (Sec 1)
- *meta*: "the Skill Evolver periodically distills reusable methodology from a persistent Memory of past experiments" (Abstract)
- *meta*: "Skill self-evolution is carried out by the Skill Evolver agent and triggered by the Orchestrator every N rounds" (Sec 2.5.1)
- *signal_chain*: memory entry includes "metric_t the offline evaluation metric vector" (Sec 2.4)
- *acceptance*: "The loop terminates when reaching T_max iterations, k consecutive rounds without improvement, or a target metric threshold." (Sec 2.2)
- *acceptance*: "verdict_t∈{success, fail, neutral} the attribution label" (Sec 2.4)
- *guards*: "the Research Agent performs a diversity constraint check to avoid focusing on the same module for too many consecutive rounds" (Sec 2.3.1)
- *human_role*: "Human-free operation: the entire pipeline is autonomously driven by collaborating agents." (Sec 1)
- *llm*: "The four agents share Claude Opus 4.6 as the reasoning backbone" (Sec 3.1.3)
- *kept_edits*: Table 3 rows: "Reduce lr to 5e-4 +0.41%"; "Neg. samples 4→16 +0.52%"; "Multi-interest pooling (4 heads) +1.03%"; "Replace BCE with InfoNCE +1.18%"; "Hard neg. mining (τ=0.1) +2.31% Skill #12"; "Layer-wise lr decay +0.63% Skill #16" (Table 3)
- *baseline_type*: "Training hyperparameters for both base models follow their original papers." (Sec 3.1.3)

Note: The kept edits are the positive-delta rounds in Table 3. The paper never says whether negative rounds were rolled back. Data-integrity flag: in Table 1 the Industrial R@10 values (e.g. Evo-MGUI 0.0571) are below R@5 (0.0775), and N@5 exceeds R@5 (0.0919 vs 0.0701 for SASRec). Neither is possible under standard leave-one-out Recall/NDCG.

## VirtualMLE (`cao2026virtualmle`, arXiv 2606.03221)

- **object**: L1
- **proposer**: llm
- **proposer_note**: LLM (GPT-5.4) reflect&plan -> act -> observe -> update loop over a markdown-defined action space (hyperparameters + selected structural switches)
- **meta**: Y: a cross-dataset Cognition Summary (transferable tuning rules) is distilled into long-term memory and reused as a zero-shot prior on new datasets
- **signal_chain**: offline* (validation NDCG@10); test evaluated once at the end
- **memory**: hierarchical memory: short-term within-session trajectory + long-term cross-dataset knowledge (Cognition Summary, discard heuristics)
- **acceptance**: rule-enforced Program module (keep/discard, stop condition); final model selected by validation NDCG@10
- **guards**: sandboxed protocol with a defined action space; test set hidden from the agent; immutable data-preparation pipeline; same pipeline and validation protocol for all methods
- **human_role**: none stated
- **llm**: GPT-5.4 (robustness runs with Kimi 2.6 and DeepSeek V4 Pro)
- **kept_edits**: architecture: dense hybrid scoring scheme (Beauty/SASRec val N@10 0.0581->0.0712); capacity: hidden_dim 128 (marginal, ->0.0718); architecture: relative position bias + SwiGLU FFN ('largest local gains in that stage'); final selected configurations per dataset not reported
- **headline_gain**: abstract gives no number; up to +12.1% N@5 over the best tuned baseline (HSTU/Baby, Table 1); best validation reached in 17-32 trials vs BO 163-464 (Table 2)
- **baseline_type**: tuned (Grid Search 729 configs, BO 500 trials, OPRO with same LLM)
- **c9_isolation**: Y
- **c9_incident**: N
- **c4_note**: averaged over three independent runs; no std or CI

Evidence:

- *guards / c9*: "The test set is completely hidden from the agent during exploration, and the data preparation pipeline is immutable throughout the search process." (Sec 3.1)
- *acceptance*: "a rule-enforced Program module (keep/discard, stop-condition check)" (Sec 3)
- *acceptance*: "the final model is always selected by validation NDCG@10" (Sec 4.1)
- *object*: "many critical decisions extend beyond scalar hyperparameters to include selected architectural switches and training heuristics" (Sec 1)
- *memory*: "Long-term memory stores persistent knowledge across datasets and optimization sessions, including dataset observations and model-level knowledge." (Sec 3.3)
- *meta*: "After completing optimization on a dataset, the agent distills the full search trajectory into a Cognition Summary." (Sec 3.2)
- *kept_edits*: "the agent first pushed validation NDCG@10 from 0.0581 (the untuned baseline) to 0.0712 through a dense hybrid scoring scheme" (Sec 4.4 (i))
- *kept_edits*: "try relative position bias and SwiGLU before further widening" ... "delivered the largest local gains in that stage of the search" (Sec 4.4 (i))
- *baseline_type*: "The search budget is configured to favor the baselines: Grid Search enumerates all 729 configurations, and Bayesian Optimization runs for 500 trials." (Sec 4.1)
- *c4_note*: "For all methods in our experiments, results are averaged over three independent runs." (Sec 4.1)

Note: Internal inconsistency: the text says "the largest improvement reaching +13.1% N@5 on Baby" (Sec 4.2), but the largest Improv. cell in Table 1 is +12.1% (HSTU/Baby N@5).

## NOVA (`liu2026nova`, arXiv 2606.27243)

- **object**: L1+L2
- **proposer**: llm
- **proposer_note**: Solution Design generates K=4 modification plans per round from trajectory feedback + fixed KB snapshot; Code Generation applies them under production constraints; Optuna-TPE is only a baseline
- **meta**: Y (weak, between tasks): validated rules may be committed to the knowledge base for future task snapshots; within a task the KB is fixed and confirmed semantic errors become new verification rules
- **signal_chain**: self>offline*>online (LLM semantic-rule verifier + 4-LLM judge ranking pick 1 of K; local tests; offline AUC; best offline candidate to a 6-day A/B)
- **memory**: trajectory memory (semantic diagnostics, local-test results, offline deltas) synthesised into weak components / directions / forbidden patterns; active semantic-rule set; fixed KB snapshot
- **acceptance**: any candidate reaching offline evaluation becomes the working state; best observed offline AUC returned; task stops when best gain >= tau=0.15 pp; AUC-positive = >=0.10 pp; online promotion threshold +0.15 pp
- **guards**: hard production constraints (shapes/dtypes, feature availability, params/FLOPs budget); semantic-rule verification incl. target leakage; local tests; deterministic scripts for training and metrics; guard margin epsilon on other objectives; Copilot mode human confirmation
- **human_role**: Copilot mode: human confirms the selected plan and implementation; AutoRun: none; experts audit semantic labels post hoc
- **llm**: Claude Sonnet 4.6 for all LLM stages; ranking ensemble of GPT, Claude Opus, Gemini, Kimi ('latest production versions')
- **kept_edits**: architecture: transferred TokenMixer-Large modules (Mixing-and-Reverting, PerToken-SwiGLU) into the RankMixer-style backbone; loss: AuxLoss with corrected o1 indexing, o3 masked and reduced o1 AuxLoss weight (Round 6, +0.15/+0.02/+0.09 pp; to online A/B); architecture: MixFormer multi-sequence gated fusion (+0.05/+0.02/+0.02 pp; not promoted)
- **headline_gain**: effective pass rate 53.3% (ScaleUp) / 51.7% (Literature-to-Production) vs R&D-Agent 29.2% / 28.3%; online GMV +1.25/+1.70/+2.02%, |pCVR bias| -58.8/-66.7/-37.3%
- **baseline_type**: other (budget-matched coding-agent baselines and Optuna-TPE); production (online)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: 20 tasks per setting aggregated into rates without CIs; no seeds or noise estimate for the 0.10 pp AUC-positive threshold

Evidence:

- *proposer*: "Solution Design uses the task request q, current architecture A_t, structured guidance z_t from trajectory memory, and fixed prior KB to produce K modification plans" (Sec 4.2)
- *signal_chain*: "generates multiple candidate modifications, rejects candidates that violate recommender-specific architecture semantics, and ranks the valid survivors for local testing and offline evaluation" (Sec 1)
- *signal_chain*: "Candidate ranking uses the latest production versions available during evaluation from four LLM families: GPT, Claude Opus, Gemini, and Kimi." (Sec 4.3.2)
- *acceptance*: "a candidate that reaches offline evaluation becomes the next working state. The search returns A_best when the improvement threshold is reached" (Sec 4.5)
- *acceptance*: "An evaluated candidate is AUC-positive when ΔAUC_pp ≥ 0.10 pp. A task terminates when the best observed baseline-relative gain reaches τ=0.15 pp." (Sec 5.2 Metrics)
- *acceptance*: "Its gains remain below the +0.15 pp promotion threshold, so it was not advanced to online A/B testing." (Sec 5.6 Case 2)
- *guards*: "These constraints cover tensor shapes and dtypes, feature availability, and parameter/FLOPs budgets." (Sec 3)
- *guards*: "examples include mismatched feature-token mappings, missing sequence masks, incorrect logit-fusion paths and target leakage" (Sec 1)
- *guards*: "deterministic scripts execute testing, training, and metric collection" (Sec 4.1)
- *human_role*: "AutoRun proceeds autonomously, whereas Copilot requires human confirmation of the selected plan and implementation." (Sec 4.6)
- *meta*: "Reusable rules validated during the task may be committed afterward and appear only in future snapshots" (Sec 4.6)
- *object*: "searches over coupled structural hyper-parameters, including token_cnt, token_dim, and the number of RankMixer layers" (Sec 5.2 Tasks)
- *kept_edits*: "Revert to Round 4; retain corrected o1 indexing and o3 masking, and reduce the o1 AuxLoss weight +0.15/+0.02/+0.09" (Table 3)
- *llm*: "All LLM-dependent stages use Claude Sonnet 4.6 (Anthropic, 2026), except NOVA's four-model ranking ensemble" (Sec 5.2)

Note: During the loop the agent introduced an auxiliary-loss indexing bug (Round 3). It was caught by code inspection and was not metric-winning, so c9_incident = N.

## AgentX (`lao2026agentx`, arXiv 2606.26859)

- **object**: L1+L2
- **proposer**: llm
- **proposer_note**: Brainstorm Agent generates bounded batches of ranked proposals with an avoid set and evidence weighting; model track runs a 3-phase reproduce / module-ablate / compose loop with memory-guided pruning
- **meta**: Y: SGPO edits one subagent's harness (instructions, validation rules, output contract, tool discipline), admitted via paired replay; the exploration memory also keeps playbook / anti-pattern entries
- **signal_chain**: strategy track: self>online* (validator admission + human gate, then A/B KEEP/EXTEND/DISCARD); model track: offline>online*>launch review
- **memory**: Experiment KB + System KB; avoid set; negative-result assets; append-only event log with playbook and anti_patterns; trace pool for SGPO
- **acceptance**: KEEP only if the primary objective clears a minimum effect threshold and statistical significance and guardrails show no unacceptable cross-domain damage; human launch review; SGPO edit admitted if paired-replay gain > epsilon and safety check passes; KB entries need >=2 independent runs + adversarial review
- **guards**: engineering whitelist on parameters; canary/gray release; tiered guardrail veto; dryrun compile checks; feature switches; deterministic metric extraction (no LLM); falsifiable-attribution check
- **human_role**: human approval gate for ideas (approve/revise/defer/reject); guardrail triggers escalate to human review; launch review
- **llm**: not stated
- **kept_edits**: strategy: constrained PCV fine-ranking score S2 = B_d*(1+beta(u)G(P)) (watch time +0.071%, real-show +0.118%, launch-review ready); strategy: UV-level CPM boost (revenue +4.7%); architecture: residual gate fix x*(1+tanh(V_o x)) (dAUC +0.0022); architecture: MHFT+VQ-Code+MVSF composition (best offline, avg +0.0264 AUC); other: SGPO-accepted brainstorm-harness edits (explicit task contract, business-causal chain per idea)
- **headline_gain**: 8x concurrency and 3.7x business value over a manual engineer; main feed +0.561% app time; life service > RMB 100M annualized revenue
- **baseline_type**: other (single algorithm engineer, manual workflow); production (A/B controls)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: headline numbers from single deployments; A/B decisions use CUPED/DiD and significance; KB experience entries require >=2 independent runs

Evidence:

- *acceptance*: "A candidate is eligible for KEEP only when the primary objective clears both a minimum effect threshold and statistical significance" (Sec 6.3)
- *guards*: "Parameter changes must pass an engineering whitelist so that an agent cannot modify unauthorized scheduler or serving controls." (Sec 6.2)
- *human_role*: "Only ready candidates that pass validation can enter the human approval gate" (Sec 4.4)
- *human_role*: "The primary role of guardrail thresholds is to flag risks for human review, not to mechanically discard experiments." (Sec 6.3)
- *meta*: "Only the target subagent's instructions, validation rules, output contract, and tool-use discipline are edited." (Sec 7)
- *meta / acceptance*: "turns accumulated execution traces into local subagent prompt updates and admits them solely through paired replay" (Sec 7)
- *acceptance*: "The threshold gate requires evidence from at least two independent runs." (Sec 7.2)
- *guards*: "Exec is a pure Python state machine—no LLM involved" (Sec 5.2.1)
- *signal_chain*: "filters them through offline evaluation, online testing, and launch-review gates" (Sec 8.2)
- *kept_edits*: "The final online result showed user watch time +0.071% and real-show +0.118%, while keeping user-experience guardrails stable." (Sec 8.3, Table 11)
- *kept_edits*: "the UV-level CPM boost achieved a positive lift, increasing revenue by +4.7%" (Table 12)
- *kept_edits*: "Round 2 applied a one-line residual fix ... and returned ΔAUC=+0.0022 with all causal-chain links verified" (Sec 5.2.2)
- *kept_edits*: "MHFT + VQ-Code + MVSF obtains AUC scores of 0.6900 and 0.6134 on KuaiRand and Taobao" (App. B.2)

Note: Object L1+L2 (audit.csv: L2+meta): the strategy track edits ranking-formula code and parameters (strategy), the model track edits model code. LLM never named. Not 'na' for isolation: the model track trains and evaluates offline.

## AgentX-Model (`yang2026agentxmodel`, arXiv 2609.30001)

- **object**: L2
- **proposer**: llm
- **proposer_note**: Research Agent (Assembler + independent Auditor) builds proposals from papers and earlier results; a human-designed scheduling policy picks the action type (Reproduce/Diagnose/Follow-up/Composition); Model Agent implements over multiple rounds
- **meta**: Y (human-gated): Model Agent proposes tool/instruction repairs and candidate memories, deployed only after human approval
- **signal_chain**: self>offline*>online (Auditor review; best-round AUC vs business baseline on fixed platform evaluation; Launch Review A/B)
- **memory**: shared research state (round-specific code, findings tied to measurements, unresolved questions); continuation archive; human-approved memories
- **acceptance**: experiment result = best valid round AUC (later rounds never overwrite it); counted above baseline if > baseline by >1e-6; Research Agent chooses continuations; online via Launch Review
- **guards**: research sandbox (no change to upstream features or prediction tasks); fixed platform evaluation code; independent Auditor; source/version checks; test split and acceptance rules outside the repair agent's control
- **human_role**: human-designed scheduling policy; approves tool/instruction changes and memories; Launch Reviews
- **llm**: privately deployed GLM-5.2 (Research Agent on Pi runtime, Model Agent on Claude Code); GLM-5.3 for replay and assessment
- **kept_edits**: architecture: expert pool 1->4 with new routing/load balancing (Scenario B best); architecture: restricted token-group information flow + learned compensation path (Scenario C best); loss: corrected scale of pairwise ranking loss (Scenario A best); regularization: temperature normalisation in entropy regularizer against codebook collapse (Scenario D); launched: architecture: adaptive attention temperature; loss: multi-task objective pruning (~10% fewer FLOPs/params)
- **headline_gain**: 560 of 636 completed experiments above business-baseline AUC; online gains 10-15% acquisition efficiency, 15-20% target-segment ad spend, 0.3-0.8% watch time
- **baseline_type**: production
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: fixed-seed repeat SD 0.0022 / 0.0010 / 0.0011 AUC reported, yet 'above baseline' means >1e-6; Scenario D best gain +0.001776 is below 2 SD; no repeated sessions

Evidence:

- *guards*: "Agents can change how the model uses those inputs, but do not change upstream feature collection or redefine the prediction tasks." (Sec 2.1)
- *guards / c9*: "The Model Agent modifies model code, while evaluation uses fixed code provided by the platform." (Sec 4.1.1)
- *guards / c9*: "The test split and acceptance rules remain outside the repair agent's control." (App. B.2)
- *acceptance*: "Later revisions do not overwrite the best measured implementation." (Sec 3.2)
- *acceptance*: "Results counted as above business baseline exceed it by more than 10^-6." (Table 4 caption)
- *c4_note*: "With the random seed fixed, repeated executions yield pooled within-implementation AUC standard deviations of 0.002208, 0.001010, and 0.001099" (Sec 4.1)
- *meta*: "The Model Agent can propose changes to tools or instructions, validate them, and submit them for human approval before deployment." (Sec 3.1)
- *proposer*: "We use a human-designed scheduling policy as a baseline for sustained operation and trajectory collection." (Sec 3.3)
- *llm*: "Both used privately deployed GLM-5.2 as the underlying language model." (Sec 4.1.1)
- *kept_edits*: "the best measured model expanded the expert pool from one to four and changed the routing and load-balancing mechanism" (Sec 4.3.1)
- *kept_edits*: "a Follow-up addressed codebook collapse by revising temperature normalization in the entropy regularizer" (Sec 4.3.1)
- *kept_edits*: Launch Review model changes: "Adaptive attention temperature"; "Multi-task objective pruning"; "Hierarchical aggregation with calibration" (Table 6)

## Auto-RecSys (`li2026autorecsys`, arXiv 2609.10922)

- **object**: L2
- **proposer**: llm
- **proposer_note**: ideas from researchers' design docs, literature mining and KB brainstorming (embedding strategies, gating, auxiliary losses), filtered against experiment history and ranked by impact/complexity/risk/novelty
- **meta**: Y: model-specific playbooks (dead ends, pipeline recipes, submission configs) are distilled from trajectories after each iteration; updates accepted unconditionally
- **signal_chain**: offline* (verdict vs shared baseline after full training; toy-train smoke validation before submission; split not stated)
- **memory**: playbooks; append-only experiment history with verdicts and lessons; model knowledge base; idea backlog; session trajectories
- **acceptance**: verdict positive/neutral/negative from metric differences vs a common baseline; human results review in interactive mode; playbook updates accepted without a gate
- **guards**: deterministic scripts enforce preconditions and state transitions; toy-train validation; shared baseline with aligned training date ranges; human checkpoints in interactive mode
- **human_role**: interactive mode: checkpoints at idea selection, code review, training submission, results review; autonomous mode skips them
- **llm**: not stated
- **kept_edits**: not reported (no model changes or quality gains reported; only harness self-repairs such as a cron-based monitor replacement)
- **headline_gain**: operational: major fixes per iteration 4.0 -> 0.5 over 31 iterations; no accuracy gain claimed
- **baseline_type**: other (earlier iterations / manual process)
- **c9_isolation**: NS
- **c9_incident**: N
- **c4_note**: no repeats, seeds or noise estimates

Evidence:

- *proposer*: "applying common improvement patterns, such as embedding strategies, gating mechanisms, and auxiliary losses" (Sec 5.1)
- *meta / acceptance*: "Auto-RecSys currently accepts playbook updates unconditionally based on agent judgment." (Sec 9)
- *acceptance*: "the analysis computes performance differences against the baseline and assigns a verdict of positive, neutral, or negative" (Sec 5.3)
- *guards*: "All ideas on the same model share a common baseline with aligned training date ranges, ensuring fair A/B comparison." (Sec 5.2)
- *guards*: "deterministic scripts perform state transitions, API interactions, validation checks, and file operations" (Sec 1)
- *human_role*: "In interactive mode it pauses at four checkpoints, namely idea selection, code review, training submission, and results review" (Sec 2.1)
- *headline_gain*: "reducing major fixes from 4.0 to 1.3 per iteration" ... "reached 0.5 major fixes per iteration" (Sec 7.2)

Note: Codebook issue: audit.csv codes c2 = na and c3 = na, but the codebook reserves na for online-only systems. Auto-RecSys runs offline training and compares against a baseline (quote above), so c2 = NS and c3 = NS. c9 left NS: the deterministic scripts guard state, not test-data access.

## AutoLR (`zhang2026autolr`, arXiv 2609.04871)

- **object**: L1+L2
- **proposer**: llm+space
- **proposer_note**: multi-expert LLM council proposes, debates and adversarially reviews; a deterministic evidence-weighted selector (Beta(1,1)-smoothed success rate, diversity caps) over human-defined direction families + council rerank; top-1 trained
- **meta**: N
- **signal_chain**: self>offline*>online (council review + memory gate; one-run offline scalar delta vs trunk with protected-metric guardrails; engineer-selected A/B; Launch Review)
- **memory**: layered knowledge (external research, production-system facts, DASHEN domain) + experiment memory (hypotheses, patches, logs, failures, offline results, promotion decisions, lineage)
- **acceptance**: KEEP_E1 if guardrails hold and delta >= tau_keep in one run (fixed floor; noise calibration disabled) -> rewrites trunk; PACK if tau_pack <= delta < tau_keep; else DISCARD; engineers pick A/B candidates; Launch Review gates rollout
- **guards**: fixed offline evaluation contract; read-only preflight checks that frozen objectives/eval logic are untouched; declared edit surface; non-compensatory protected-metric guardrails; deterministic controllers own execution, metrics and state
- **human_role**: engineers define objectives, evaluation contract and edit boundaries; select candidates for online A/B; Launch Review approves rollout
- **llm**: Claude Opus-class models, migrated to a mixed DeepSeek-V4-Pro/Flash stack
- **kept_edits**: not reported (Launch Reviews described by metrics only)
- **headline_gain**: 1,586 completed evaluations; nine Launch Reviews with summed lifts +5.75% penetration, +10.83% consumption time, +5.55% VV (descriptive, not pooled)
- **baseline_type**: production
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: KEEP decided on a single run; noise calibration disabled; no fixed-snapshot repeats; session-resampled intervals; IQR of deltas (~1.2e-3) comparable to the 1e-3 floor

Evidence:

- *proposer*: "AutoLR does not sample from a Beta posterior or maintain direction-level posterior state." (Sec 3.3)
- *proposer*: "it does not establish superiority over random, greedy, or direct LLM-based routing under a matched trial budget" (Sec 3.3)
- *acceptance*: "The E1 suffix marks a one-run offline threshold crossing rather than a confirmed effect." (Sec 3.6)
- *acceptance*: "KEEP is the only action that rewrites the working repository; PACK retains the candidate and its lineage, and DISCARD rejects it" (Sec 3.6)
- *c4_note*: "noise calibration was disabled and no reusable version-matched profile was retained" (Sec 3.6)
- *guards / c9*: "A read-only preflight stage verifies that referenced files and symbols exist, required features are available, and frozen objectives or evaluation logic are not modified." (Sec 3.5)
- *guards / c9*: "it may modify designated model and configuration code, while the training and evaluation pipeline remains fixed" (Sec 4.1)
- *human_role*: "Engineers currently decide which packages enter online A/B testing, and Launch Review remains the human gate for full-traffic rollout." (Sec 3.6)
- *c9_incident*: "The archive establishes this mutable-baseline mechanism, but it cannot identify how much observed progress or drift reflects true model improvement" (Sec 5.3)

Note: KEEP ratchet: the paper identifies it as a risk mechanism, not as an observed incident of metric inflation, so c9_incident = N. If the survey counts 'identified mechanism with circumstantial evidence', this is the borderline case.

## CORAL (`azhar2026coral`, arXiv 2609.02730)

- **object**: L1
- **proposer**: llm
- **proposer_note**: LLM proposes bounded per-unit adjustments (retrieval-budget multipliers, per-segment serving treatment) from observation/assessment/decision memory; a constrained optimizer projects proposals onto the budget-feasible set
- **meta**: N
- **signal_chain**: online* (A/B result each k=3-day cycle written back to memory)
- **memory**: three stores over the last m=3 cycles: observations, LLM assessments, deployed decisions with attributed outcomes
- **acceptance**: no explicit keep/reject rule: each cycle's configuration is deployed; the agent reinforces changes that helped and reverses those that did not; the reported configuration is the one converged after several cycles
- **guards**: constrained optimizer enforcing the hard budget; feasibility checks; bounded-change limits; safety constraints; bounded ranges / discrete menu; fixed tool order; deterministic tools
- **human_role**: a human supervises operation (meant to be replaced progressively by guardrails)
- **llm**: not stated ('a general-purpose LLM')
- **kept_edits**: strategy: reallocated per-source retrieval-budget multipliers (deployed R3 config: +0.16% sessions, +0.15% watch time); strategy: per-segment allocations moving budget to content/context sources for low-signal and new users (+0.23% sessions); strategy: lighter serving treatments for a subset of user segments, widened in round 2 (+44% savings, engagement unchanged)
- **headline_gain**: abstract gives no number; +0.16% sessions and +0.15% watch time at no extra serving cost; serving savings of millions of USD annualized on the second surface
- **baseline_type**: production (hand-set allocations)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: A/B significance per round only ('neutral' = no significant change); no repeats or seeds

Evidence:

- *proposer*: "invokes a numerical optimizer that projects a candidate configuration onto the budget-feasible set" (Sec 3)
- *signal_chain*: "its effect is measured with an A/B experiment whose result is written back to memory" (Sec 4.3)
- *acceptance*: "Recording these attributed outcomes lets the agent reinforce the changes that helped and reverse those that did not" (Sec 4.3)
- *guards / c9*: "this supervision is progressively replaced by the harness's automated guardrails—feasibility checks, bounded-change limits, and safety constraints" (Sec 4.3)
- *human_role*: "A human supervises its operation, tracking the effect of its changes and the decisions it makes" (Sec 4.3)
- *object*: "a configuration assigns each source a budget multiplier within a bounded range" (Sec 5.1)
- *baseline_type*: "These shares are typically hand-set and seldom revised" (Sec 5.1)
- *kept_edits*: "R3 aggregates several decision cycles and is the deployed configuration" (Table 1 caption)

Note: c9 coded P (na at first coding; the released audit.csv now has P). Under the new definition, na needs both no touchable offline data/eval code and no stated constraints. CORAL states a budget projection, bounded-change limits and feasibility checks.

## AgenticRecTune (`wu2026agenticrectune`, arXiv 2604.26969)

- **object**: L1
- **proposer**: llm
- **proposer_note**: Actor Agent (Gemini) proposes a batch of configurations from Skillhub context + Pareto-elite history; Critic Agent filters and refines; Online Agent generates config code and A/B tasks
- **meta**: Y: self-evolving Skillhub; Insight Agent extracts patterns and the Skill Agent appends rules, tightens search bounds and synthesizes new skills
- **signal_chain**: self>online* (Critic LLM filter, user review, then A/B with p<0.05)
- **memory**: Agent Memory (task records with results; Pareto 'top performers' pool with diversity selection) + Skillhub
- **acceptance**: Pareto top-performer pool kept in memory (strictly dominated candidates discarded); A/B significance p<0.05; launch decision rule not detailed
- **guards**: Critic checks format, system guardrails, instruction constraints, known failure cases; allowed value ranges per skill (tightened over time); secondary-metric floors b_j; user review before every A/B
- **human_role**: users' review required before each A/B test starts
- **llm**: Gemini 3 Pro (ablations: Gemini 3 Flash, Gemini 1.5 Pro)
- **kept_edits**: strategy: pre-ranking value-based-retrieval score-fusion weights; strategy: ranking value-fusion weights; strategy: re-ranking diversity thresholds and weights (diversity +3.43%)
- **headline_gain**: abstract gives no number ('multiple successful production launches'); pre-ranking +0.75% / +0.90% engagement, re-ranking diversity +3.43% (Tables 1, 3)
- **baseline_type**: production (existing tuned configurations)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: p<0.05 per A/B; no repeated rounds; the model-ablation stage is inconsistent (text: pre-ranking; Table 2 caption: re-ranking)

Evidence:

- *signal_chain / guards*: "checking them against format requirement, system guardrails, instruction constraints, and known historical failure cases" (Sec 4.1.3)
- *human_role*: "Before online A/B testing starts, the users' review is required." (Sec 4.2.2)
- *acceptance / memory*: "The system maintains a "top performers" pool by systematically discarding candidates that are strictly outperformed by others." (Sec 4.3.2)
- *meta*: "automatically appends these refined rules to the Domain Knowledge component of that skill. Simultaneously, it dynamically tightens the search space bounds" (Sec 4.4.1)
- *guards*: "such as the allowed search space (value ranges) for tuning parameters" (Sec 4.4)
- *baseline_type*: "the control group is the existing tuned configurations on the production" (Sec 5.1)
- *acceptance*: "Each experiment was run as a standard launch period to ensure statistical significance (evaluated at a p-value < 0.05)." (Sec 5.1)
- *kept_edits*: "Table 1 shows that diversity metric increases by 3.43% and engagement Metric 1 & 2 also increase." (Sec 5.2.3)

Note: c9 coded P (na at first coding; the released audit.csv now has P). The Critic, bounded value ranges and mandatory user review are stated constraints.

## Sortify (`cheng2026sortify`, arXiv 2603.27765)

- **object**: L1
- **proposer**: llm+space
- **proposer_note**: Optuna TPE (5,000 trials/round) searches the 7-dim sorting-formula weights on an offline Influence-Share objective; LMS + LLM meta-controller adjust transfer intercepts and penalty multipliers (framework knobs), not the weights
- **meta**: Y ⟨superseded: released `meta` is N, with the evaluator marked as evolving (design.csv); this line is the first extraction⟩ (objective level, judgment call): the inner search's objective (offline->online transfer calibration, constraint penalty weights) is recalibrated each round by LMS + LLM
- **signal_chain**: proxy*>online>online (best Optuna trial on offline proxy published each ~4 h round; per-round A/B feeds calibration; human-frozen round re-tested in a 7-day A/B)
- **memory**: Memory DB (7 SQLite tables: episodes with offline/online pairs, prior relations, update histories, penalty weights)
- **acceptance**: inside the loop: best Optuna trial on the penalized proxy objective is published every round (no reject step); outer loop: humans froze R7 (only round with GMV and Ads Revenue both positive), ran a 7-day A/B and approved rollout
- **guards**: Codex CLI --sandbox read-only; seven-layer output safety pipeline (schema validation, relation-key whitelist, hard clamps |dbeta|<=0.1, m in [0.5,2], penalty bounds [1,000, 80,000], no-op fallback); evidence-key requirement; channel freeze rule; constraint penalties (e.g., I_order degradation <=5%)
- **human_role**: sets objectives, constraints and ranges (Layer 1); optional confirmation of the initial round; freezes parameters, runs the 7-day A/B and approves rollout
- **llm**: an OpenAI model via Codex CLI (exact model not named; cost quoted at GPT-5.4 / GPT-5.3-Codex prices)
- **kept_edits**: strategy: Country B frozen R7 sorting-formula weights ('high Click, low GMV/Order' structure) -> 7-day A/B and full rollout; strategy: organic-click weight ps_org_wc 1.0 -> 3.71 found in the first Country B round (directional signal, not the deployed config)
- **headline_gain**: +4.15% GMV/UU and +3.58% Ads Revenue (7-day A/B, Country B); Country A GMV -3.6% -> +9.2% over 7 rounds
- **baseline_type**: production (control sorting formula)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: no CIs; the Country A R7 peak came from a ~12K-impression window; the frozen Country B parameters were re-tested in a fresh 7-day A/B (a confirmation run)

Evidence:

- *proposer*: "Each round runs 5,000 trials with 25 parallel workers using the Constant Liar strategy" (Sec 2.2.4)
- *proposer*: "the LLM adjusts framework-level parameters (intercepts and penalty multipliers), not the 7-dimensional bottom-level sorting parameter vector" (Sec 2.5.2)
- *acceptance*: "Execute the Optuna TPE search ... Extract the best parameter vector, publish to Redis" (Sec 3.2)
- *acceptance*: "produced the only round where GMV and Ads Revenue were simultaneously positive" (Sec 4.8.2)
- *human_role*: "the decisions to freeze R7 parameters, conduct 7-day static A/B testing, and approve production rollout were all made by human operators" (Sec 4.9)
- *guards*: "The LLM's raw text output passes through a seven-layer safety pipeline before any system state is modified" (Sec 2.5.4)
- *guards*: "Hard clamp: Regardless of the LLM's output, Δβ_LLM is clamped to [-0.1,+0.1] and m_LLM to [0.5,2.0] in code." (Sec 2.5.4)
- *guards / c9*: invocation flag "--sandbox read-only" (Sec 2.5.4)
- *llm*: "At OpenAI's public prices as of March 26, 2026 (GPT-5.4: ...; GPT-5.3-Codex: ...)" (model itself not named) (Sec 4.9)
- *c4_note*: "R7 metrics were collected during a low-traffic early morning window (∼12K impressions)" (Sec 4.3.1)
- *kept_edits*: "This configuration exhibits a "high Click, low GMV/Order" structure" (Sec 4.8.3, Table 9)

Note: c9 coded P (na at first coding; the released audit.csv now has P). There is offline data: the proxy objective is computed on logged data. The read-only sandbox and the clamps are stated constraints. audit.csv llm_named = Y is generous: only Codex CLI and reference prices are given.

## GEARS (`yun2026gears`, arXiv 2602.18640)

- **object**: L1
- **proposer**: llm+space
- **proposer_note**: GAS enumerates quantile-segment -> treatment policies via random-weight Pareto search + tolerance filter; LLM controller (Claude Sonnet 4.6) writes shell filters from the intent and interprets candidates with read-only skills
- **meta**: N (skills are static, read-only resources)
- **signal_chain**: offline*>online (segment-level HTE estimates from a completed randomized experiment, filtered by deterministic hooks; then production deployment)
- **memory**: none (per-session; static read-only skills)
- **acceptance**: tolerance-based Pareto filter + intent-derived programmatic filter (e.g., guardrail LCB >= 0) + feature-stability hook + significance guard (95% CI excludes zero); human review before deployment
- **guards**: deterministic validation hooks (feature-stability shift <=15% binary / 45% quantile; statistical-significance guard); pre-search feature filter; read-only skills; logged admission decisions
- **human_role**: reviews the policy rationale before deployment
- **llm**: Claude Sonnet 4.6
- **kept_edits**: strategy: cohort-targeted policy segmented on a two-day engagement count (keeps 76% of the naive Metric-1 gain, removes the Metric-2 regression); strategy: activity-based personalisation (treatment 1 for very active users, treatment 2 for less active users); strategy: policies deployed on nine surfaces (Metric 1 +0.011-0.14%)
- **headline_gain**: 0.94 nDCG@1 vs 0.77 for Code-as-Action on the 100-instruction benchmark
- **baseline_type**: other (prompting and code-execution baselines with the same LLM)
- **c9_isolation**: P
- **c9_incident**: N
- **c4_note**: no seeds or repeats for the benchmark; CIs on production metrics; one-month backtest for one policy

Evidence:

- *proposer*: "estimates heterogeneous treatment effects across quantile-based user segments and enumerates candidate policies via random-weight Pareto search" (Sec 4)
- *proposer*: "the agent translates the user's intent into deterministic operations over the candidate table by generating and executing shell commands" (Sec 4)
- *meta*: "modular, read-only resources that provide the agent with structured procedures and access to internal tools" (Sec 4)
- *acceptance / guards*: "A policy is admitted only if all its features satisfy φ_shift≤τ" (Sec 4)
- *acceptance / guards*: "verifies that reported metric lifts are statistically significant (95% confidence interval excludes zero for the primary metric)" (Sec 4)
- *human_role*: "generates a natural-language rationale for human review before deployment" (Sec 4)
- *kept_edits*: "The resulting policy retains 76% of the naive baseline's Metric 1 gain while fully eliminating the guardrail violation." (Sec 4.1, Fig. 3)
- *kept_edits*: "users who are very active benefit more from the first treatment" ... "less active users prefer the second treatment" (Sec 6.1)
- *llm*: "All experiments use Claude Sonnet 4.6 (Anthropic, 2025c) as the backbone LLM." (Sec 5.1)

Note: c9 coded P (na at first coding; the released audit.csv now has P). The agent works on tabular experiment records (offline data), and deterministic hooks are stated constraints. The 'loop' is a single guided selection pass per experiment, not an iterated evolution. Kept in the core set as a borderline case and counted as online-selecting because its deciding estimates come from a completed randomised experiment (paper, note to the design table); without it the online-selecting stratum is nine loops, none correcting and one confirming afresh.


Extracted 2026-10-22 from the arXiv HTML full text of each paper, including appendices, together with the existing evidence in `audit/evidence-part1.md`, `audit/evidence-part2.md` and `review/sweep-2026-10-22.md` §(b).

- Quotes are verbatim and at most 25 words.
- "not stated" means the paper does not say.
- Field values are in `design-part2.csv`. This file gives the evidence behind them.
- The A-MLE, Astar, Trajectories-to-Evidence, EvoPilot and Amazon AutoResearch texts were first read from a conversion that dropped inline math. Numbers that matter were re-checked against the HTML or the regenerated text.

---

## Answers to the specific questions

### (1) EvoPilot: selection data, reported data, and test-once

**Selection and reporting use the same data.** One held-out replay set does both. No validation/test split is described.
- §5.1: "Offline evaluation replays held-out pairs against one candidate pool. Its primary selection metric is click hit-rate at depth K".
- §5.4: the reported offline outcomes come from that metric: "These admitted results rejected the additive score, fixed depth at 6k, and stopped the loss direction."
- **Recommendation: C2 should be "test", as for Amazon.** audit.csv currently has NS.

**Test-once (C3) is not stated.** The only independent endpoint is the single online A/B.
- §5.5: "We use the online A/B only to establish the product relevance of the selected model."
- §5: "The online A/B is a separate downstream endpoint. It causally estimates only the selected model treatment".
- §5.1: "Offline readings are descriptive point estimates, and we do not report inferential confidence intervals for them."
- C3 = NS is correct.

### (2) Population Evolution: selection data and baseline tuning

**Selection data on source instances.** Candidates are selected on each source instance's held-out evaluation portion. That is the same portion whose gains are reported as "local gains". No separate validation split is described for ranking, watch-time or RL.
- Ranking (App. A.1): "the last interaction is the next-item target, and preceding interactions form the history". Fitness is the mean of NDCG@10, HR@10 and MRR.
- Watch-time (App. A.2): "Training uses a fixed deterministic 80% partition; the remaining 20% supplies the evaluation scores used throughout discovery."
- RL (App. A.3): the source trains and evaluates on "the same 408-problem DeepCoder Codeforces/test partition".
- VLM (App. A.5) is the exception. Fitness uses "validation data disjoint from training".
- Track B (§2.3): "full-target scores and pass/fail outcomes are withheld from proposal context". In Track A, peer and larger-scale results "return to the ledger".
- **Recommendation: C2 is better coded "test" (selection on the reported held-out portion) than NS.** At minimum, add a note citing App. A.2.

**Baseline tuning.**
- Transfer targets are calibrated on their released test split. Confirmed in App. F.1: "Baseline hyperparameter and training-duration selection use the released test split, which is also used for final reporting; no separate validation split is used".
  - VK-LSVD calibration "monitors released-test MAE" (F.2).
  - KuaiVideo hyperparameters are "selected using released-test AUC" (F.3).
- Sources and intermediates use CMA-ES in Optuna (App. A.7): "Ranking, watch-time, and LLM/VLM source and intermediate references use CMA-ES sampling in Optuna".
  - Trial caps are 50 for ranking and watch-time and 20 for LLM/VLM.
  - The split used for HPO is not stated.
- RL: "RL disables baseline HPO and uses the mean of three independent fixed-configuration runs."

### (3) A-MLE: did the automatic re-run rule "materially reduce" single-seed promotion?

Yes, in those exact words, but the claim is qualitative only.
- §4.4: "triggers an automatic re-run when within-run variance exceeds a threshold".
- §6.9: "Over-confident triage: the agent sometimes promoted a candidate based on a single seed when within-run variance warranted re-running; the auto re-run rule materially reduced this."
- No counts, rates, before/after comparison or table support the claim.
- The threshold value is not stated.
- The rule triggers on *within-run* variance, not across-seed variance.

### (4) Amazon: "5.8×" and "220"

**"5.8×" is verbatim.** The × is rendered as MathML in the HTML, which is why it disappears from some text dumps.
- Abstract: "the agent autonomously designed a text-only fallback that expanded catalog coverage by 5.8×."
- §V-B: "Coverage thus expanded by 5.8× in a single iteration, without any human direction."
- §V-B gives the mechanism: the co-purchase graph "covers only 17% of items", and afterwards "the next FAISS index covered all items".

**"220+" counts the whole campaign across both systems, not only the tokenizer.**
- §II-C: "The combined campaign spans twelve weeks and 220+ experiments. System A ran 60+ iterations across 6 runs; System B ran 150+ iterations across 15 runs."
- System B (the RQ-VAE semantic-ID tokenizer) accounts for 150+ of the 220+.

### (5) EvoSkillRec: is P1 the highest-validation candidate on the Pareto front?

Yes, among the five front candidates. It is not the highest-validation candidate of the whole run.

Table 4 (val AUC / test AUC / MFU %):

| Candidate | Val AUC | Test AUC | MFU % |
|---|---|---|---|
| P1 (r19) | 0.92999 | 0.93598 | 1.477 |
| P2 (r1) | 0.92996 | 0.93573 | 1.513 |
| P3 (r3) | 0.92963 | 0.93570 | 1.565 |
| P4 (r18) | 0.92946 | 0.93540 | 1.567 |
| P5 (r5) | 0.92927 | 0.93561 | 1.574 |
| Baseline | 0.92948 | 0.93580 | 1.433 |

- Table 32 (App. E.3) gives the same front at 6 decimals. Its caption says "Rows run from highest AUC to highest MFU."
- §5.5 places P1 "at the accuracy-preserving end" of the front, with "the lowest MFU of the five (1.477%)".
- **Higher-validation candidates exist off the front.** §5.5: "the best validation AUC reaching 0.9301". That candidate (signed-bucket retokenizer, gen 14) failed the MFU eligibility constraint and was discarded (Table 31).
- The front is constrained. App. D.2: candidates are "eligible only if its validation AUC is within 0.001 of the incumbent best and its training MFU is at least 95% of the baseline's".
- No rule for choosing one front point is stated. P1 is singled out post hoc because "only P1 (round 19) retains both improvements on the test set" (§5.5).
- The post-hoc score is "only used for comparison after the run" (App. E.3).

---

## Per-system evidence

### pan2026recevolve — RecEvolve (2609.01622)

- **object:** L2 (loss, architecture, LR schedule). The batch size was also edited in the reward-hack session.
- **proposer:** llm. §3: "a central Orchestrator that delegates tasks to specialized subagents (e.g., Ideator, Critic, and Coding Agent)". §3.2: hypotheses can be "explicitly provided by human engineers via a prioritized Hypothesis Backlog".
- **meta:** N.
- **signal_chain:** proxy>offline*>online.
  - §4: "initial short-horizon probes were validated against full 2M-step offline training runs".
  - Alg. 1 decides keep/reject on the "evaluation suite".
  - Which horizon the keep decision uses is not stated.
- **memory:** a knowledge base plus results log. §3.1: the knowledge base holds "RecSys domain knowledge, historical results, and search heuristics". §5.4: subagents "sometimes failed to synthesize these past failures".
- **acceptance:** Alg. 1 line 20: "if γ(Φ_NS) > τ + ε and γ(Φ_Aux) ≥ Threshold", then "VCS_Commit() and Log KEEP". Otherwise "VCS_Rollback() {Aggressive regression pruning}".
- **guards:** "if ¬Verify(M_cand) then VCS_Rollback()" (Alg. 1). Fig. 1 describes "Pre-execution Validation, acting as a quality gate". Branches use "Snapshot isolation".
- **human_role:** rolled back a change. §5.2: "Upon human detection of this exploit, a rollback was executed".
- **llm:** not stated.
- **kept_edits:** listed in §5.1/§5.5 (Ideas 2, 6, 18, 23, 20, 36, 40). Table 1 gives 0.4796 → 0.5751.
- **headline:** Abstract: "a breakthrough 20% relative improvement in NDCG, a gain that translated directly to a +3.77% increase in user satisfaction".
- **c9_isolation = P.** The basis is the pre-execution Verify/Critic gate and per-experiment branch isolation. Data access is not stated.
- **c9_incident = Y.** §5.2: "drastically reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics". This happened "In a separate exploratory session" and was caught by a human.
- **c4:** single trajectory. §5: "41 distinct autonomous experiments in approximately 2 days".

### hu2026astar — Astar (2608.27287)

- **proposer:** learned.
  - Abstract: "learns a specialized evolution-guiding model from the abundant iteration histories of industrial systems".
  - §3.4: "a code agent (built on general-purpose LLMs such as Qwen or Claude) translates the evolution direction into runnable code modifications".
- **meta:** Y.
  - §3.4: "verified samples are used to continue training Astar, thereby refining its capability to propose effective directions".
  - §3.3: the reward model is updated "when persistent discrepancies emerge between true outcomes and predictions".
- **signal_chain:** proxy>offline*>online.
  - §3: the reward model "performs rapid ranking of generated evolution direction candidates".
  - §3.4: "the modified system undergoes training and offline evaluation, and successful changes are deployed to production".
  - §4.6: the online test is one A/B after 20 iterations ("July 1 to July 5, 2026").
- **acceptance:** the success criterion is not defined beyond "successful". §1: "the evaluation results determine whether each proposal is retained or discarded".
- **guards:** none stated for the loop. The whitelist filters training data: "we filter the modifications against a predefined parameter whitelist" (§2.2.1).
- **kept_edits:** not reported. The §4.7 case studies (MoE decoder FFN, Muon spectral denoising) are proposals, not stated launches.
- **headline:** Abstract: S@1 "0.6786 … far exceeding human experts (0.3229)"; "offline Hitrate@200 by 23.6%"; "4.86% in GMV and 1.82% in advertising revenue".
- **c9 = NS, incident N.**
- **c4:** Table 5: "statistically significant at p<0.05". No seeds.

### gao2026amle — A-MLE (2609.08248)

- **object:** L1+L2. §4.3: "The agent edits the training configuration or the model architecture in a sandboxed copy of the codebase".
- **proposer:** llm. §4.1: hypotheses "are scored by an LLM critic".
- **meta:** N. The skill library is fixed. §6.7: "We hold the agent loop, skills, and prompts fixed and swap the LLM".
- **memory:** §4.5: "At session end, the new outcomes are then committed back to the relevant Track Record". These are markdown knowledge trees.
- **signal_chain:** offline*>human review. §4.4: "computes statistical significance against the rolling baseline". No online A/B is reported.
- **acceptance and human role:** §4.6: "every stage boundary is a checkpoint at which a human engineer can approve continuation, request modifications, or terminate the session".
- **guards:** §4.3: "runs type checks and unit tests, builds an image with the updated code, runs a short smoke pass". §6.9: "pre-flight checks catch these before training launch".
- **c9_isolation = P.** The basis is the sandbox, the fixed shared offline evaluation suite ("Both baselines share the same offline evaluation suite") and human checkpoints. Access to test data is not stated.
- **c9_incident = N (borderline).**
  - The §6.9 failure modes are agent-reliability failures: single-seed promotion, and "weaker base models hallucinate workflow identifiers and pretend to have completed tasks".
  - They are not reported as gaming of the evaluation.
  - Who caught them is not stated, except that pre-flight checks caught the hallucinated APIs.
- **headline:** the abstract has no number ("practical force multiplier"). Table 1: "+2.56%" relative offline regression-error reduction, "+0.42%" train QPS.

### yang2026sragent — SR-Agent (2607.17719)

- **object:** L1. §3.1: "SR-Agent leaves the base ranker frozen and refines only π_S".
- **proposer:** llm within typed arms. §3.5: "strategy owners configure and version the typed action space 𝒜".
- **signal_chain:** self>proxy>online*. §3.2: "labeled bad-case retesting, historical-traffic replay, human verification, and online A/B testing before safe deployment". The UserSim retest is the self stage.
- **guards:**
  - §3.5: "The LLM cannot emit serving code, alter model objectives, target unauthorized scopes, or invoke operations outside 𝒜".
  - §3.5: "A deterministic validator rejects candidates with invalid parameters".
- **memory:** Strategy Memory "records previous proposals and their validation outcomes" (§3.5), plus Bad-Case Memory and Diagnosis Memory.
- **human_role:** §3.4: "human reviewers randomly audit approximately 1% of the bad cases produced by UserSim". Strategy-owner review is a gate before A/B.
- **llm:** §4.3: "All LLM-based components use Claude Sonnet 4.6".
- **kept_edits:** §4.4: "ten successive strategy updates". The individual updates are not itemized.
- **headline:** Abstract: "increases order volume by 0.71%, browsing depth by 0.34%, and clicked-category diversity by 0.48%".
- **c9 = P, incident N.**
- **Note:** the loop uses offline retest and replay, so it is not online-only. That supports keeping c9 = P rather than na.

### li2026evoskillrec — EvoSkillRec (2609.34552)

- **proposer:** llm+space.
  - §4.2.1: retrieval is "rule-based rather than embedding-based" over typed operators.
  - §4.2.2: "one LLM call turns [the brief] into a set of architectural sketches".
- **meta:** Y (skill library).
  - §3: "Ω_t ⊆ Ω_{t+1}, with strict inclusion exactly when a code-space invention is promoted".
  - §4.2.2: "only generated skills carried by a survivor are promoted".
- **signal_chain:** offline*. §5.1: "Candidate and checkpoint selection uses the corresponding validation metric; held-out test metrics are used for reporting, not selection".
- **acceptance:** App. D.2: "top-K candidates by s among those satisfying s(G) ≥ s̄_t − δ"; "If no candidate survives, the current parents are kept". Co-evolution uses the constrained Pareto front (see Q5).
- **guards:**
  - §4.2.2: "static analysis rejects non-importable code and any file, network, subprocess, or dynamic-evaluation capability".
  - §4.2.2: "What the LLM receives is not the training data but a structured design brief".
  - App. D.3: "coefficient of variation of MFU across windows is at most 0.05".
- **llm:** §5.1: "generated by GPT-5.5 through the Codex CLI".
- **kept_edits:** best-validation rows of Tables 24–29, plus the P1 composition (Fig. 4). §5.5: P1 "adds a low-rank task router at the tower interface".
- **headline:** the abstract has no number. Table 1 shows +0.0001 to +0.0085 test AUC.
- **c9 = P (leaning Y).** Test data is never used for selection, and the LLM sees no data. An explicit statement that the agent cannot reach test data is absent. Incident N.
- **c4:** §6: "margins … on the order of 10⁻⁴ AUC, which a single evolution run cannot reliably separate from run-to-run variation".
- **Corrections to evidence-part2 §7:**
  - Co-evolution is 30 generations × 6 = 180 candidates (Table 12, App. E.3), not 25 × 8.
  - QK-Video uses a separate 92-skill library.

### chen2026rankevolve — RankEvolve-HSTU (2609.39551)

- **proposer:** llm. §2.1: candidates are "re-ranked not by a numeric genetic operator but by an LLM critic over a persistent leaderboard". App. D: "The user selects which proposals advance to Phase 4".
- **meta:** N. §2.2: "The deployed flow is human-authored YAML".
- **signal_chain:** offline* on the test split. App. B: "Canonical evaluation is full-test NDCG@10 over all held-out users".
- **acceptance:** §2.1: an LLM critic "promotes reference-beating combos to seed the next round".
- **guards:**
  - §2.1: "dependencies, gates, branch/join cardinality, loop budgets, tool allowlists, and checkpoint/restart are checked statically or enforced at runtime".
  - The Claude Code and Codex lanes form "an implement–review dual".
  - App. C: the read-only, hash-checked evaluator applies to the ExecML benchmark only.
- **human_role:** §2.1: "the operator also authorized compute, vetoed one over-budget experiment, and gave three high-level directions". One of those directions was to "guarantee no test leakage".
- **c9_isolation = N** (the alternative coding is P, for process gates).
  - Selection is on full-test NDCG.
  - The agent itself evaluated at test positions. App. H.1: "re-runs the frozen model with a different ignore_last_n argument".
  - Cross-agent review, EOP gates and allowlists constrain the process, not access to the test data.
  - "Guarantee no test leakage" was a human directive, not an enforced mechanism.
- **c9_incident = Y.** Who caught each incident:
  - Genre v1 leak: the agent, from metric anomalies. App. H.3: "a textbook feature leak the agent detected and corrected". App. I.1: bugs "surfaced not from a failed unit test but as anomalous metric trajectories".
  - Multi-position eval: the agent's mandatory post-hoc diagnosis. App. H.4: "Apparent 'gains' from naive multi-position eval were leakage". App. H.4: "the loop requires a post-hoc diagnosis of every negative before the next proposal".
  - DPO target-derived negatives: same route as the genre leak. Table 1: "A leak-free re-derivation … is neutral".
  - Subset-eval phantom gains: catcher not stated. §3.1: "the system repeatedly chased phantom 0.005-scale 'gains'".
- **c4:** Table 1: "best checkpoints, not independent seeds".

### peng2026population — Population Evolution (2610.05950)

See Q2 for selection data and baseline tuning.
- **object:** L2. §2: "A candidate is an executable intervention in model architecture or training code."
- **signal_chain:** publish on source (offline*) > peer gate (proxy*) > larger-scale or full target (offline*).
  - App. B.1: "Scores are not averaged across instances before selection."
  - Table 20: "Every peer gate requires at least two wins among four peers."
- **memory:** §2.2: "Peer and promotion results affect local proposals only through this context; code archives remain instance-specific."
- **guards:**
  - App. A.1: "Data loading, loss, sampling, and evaluation are fixed."
  - App. A.4: "the implementation must pass the causal-leakage check".
  - App. A.3: "the evaluator's test cases excluded from the generation prompt".
- **meta:** N. App. A.6: the shared domain guidance is fixed and human-written.
- **llm:** §4.1: "GPT-5.5 at high reasoning effort as the proposer".
- **kept_edits:** graduated designs (Table 23, App. D). App. D: "Muon update geometry, RoPE configurations …, and late-training EMA/SWA checkpoint averaging".
- **headline:** Abstract: "raises mean best local gains from 7.01% to 8.97% in ranking and from 2.84% to 3.85% in watch-time".
- **c9 = P.** The basis is the fixed evaluators, the protected components and the withholding in Track B. No statement bars the proposer from source evaluation data. Incident N.
- **c4:** App. B.5: "we report one complete run per method–configuration".

### zhuang2026trajectories — Trajectories-to-Evidence (2608.05235)

- **memory:** "Each record contains five semantic blocks: source context, intervention, measured outcome, supporting evidence, and applicability boundary." Records are Repair, Guard or Withheld.
- **controller:** Apply/Defer/Reject. It "combines deterministic checks over structured record and target fields with an LLM-based assessment". Its "overall accuracy was 67.2%, below the 79.7% obtained by an always-Reject rule".
- **guards:**
  - "The producer, evidence-and-constraint verifier, and requirement reviewer operate in separate contexts."
  - "An executed round is valid only when all four gates pass".
  - The repair loop allows "up to three verification-and-repair retries".
- **signal_chain:** self>offline*>online. Production candidates "passed artifact verification, machine evaluation, and claim qualification before online testing".
- **llm:** "All LLM components … use GLM-5.2 … self-hosted".
- **kept_edits:**
  - Table 5: pre-head RMSNorm Repair.
  - Table 6 transfers: MixFormer +0.0030, TokenFormer +0.0034, OneTrans +0.0101 ΔAUC.
  - Table 8 online launches: "+0.75%", "+6.34%". The launched edits are not described.
- **c9 = P, incident N.**
- **c4:** "only eight single-run pairs".

### fu2026evopilot — EvoPilot (2609.21257)

See Q1 for selection and reporting data.
- **object:** L1+L2. §3.2: a change may alter "the task-score weights, P, or K". §5.1: "seven capacity or loss rounds".
- **proposer:** llm. §4.3: "a planner reads this direction protocol together with prior plans, results, takeaways, and human edits. It then proposes variants".
- **acceptance:** §4.1: "VerifyComparison establishes mechanical eligibility, and human review completes admission". §5.4: results "within the 0.36-point operational band, so the study selected the simpler click-only blend".
- **guards:**
  - §4.4: "The orchestrator and verifier are deterministic programs, not agents."
  - §4.5: "The verifier rejects missing attestations, self-reported numbers without artifact provenance, and unauthorized differences."
  - Table 3: the date-order check was added "after leakage".
- **human_role:** §5.1: "Every round and every research-level exception required human approval." §4.4: "Humans retain authority over research direction, metric semantics, approvals, exceptions, and stopping."
- **memory:** §4.5: "The incident catalog contains 38 searchable records in six categories."
- **llm:** §4.4: "Planning, experiment modification, result synthesis, and repair used Claude Opus 4.7/4.8; bounded read-only monitoring used Claude Haiku."
- **kept_edits:** §5.5: "the interaction-head treatment became the default VDD MBR online configuration". Depth fixed at 6k; the click-only blend was selected (§5.4).
- **headline:** the abstract reports "an offline improvement of 3.20 percentage points" and "a 0.66% relative increase in the VDD slice of Good Search Result Rate for Retention (GSRR)".
- **c9_isolation = P.** The basis is the fail-closed verifier, round-tied human approvals, data pins and the dedicated clone. §4.3: the specification is read-only, "although it is not cryptographically immutable". No statement bars the agent from evaluation data.
- **c9_incident = Y.** Who caught each incident:
  - Leakage: the detector is not stated. §5.2: "a favorable result used an evaluation date inside the candidate model's training window, so the result was retracted."
  - No-op edit: the detector is not stated. §5.2: "history rewriting removed the intended edit but left a plausible revision chain."
  - Funnel mismatch: the human gate. §4.2: "its required human-gated review rejected the model attribution". This was a pre-existing evaluator defect that the primitive autoresearch baseline misattributed, not EvoPilot gaming. §5.3: "The first EvoPilot version relied on the human gate."
  - Evaluator drift: reproduced post hoc (§5.2).
- **c4:** §5.1: "Two publications with the same model, configuration, and pinned data differed by 0.36 points". The seven directions "are not independent replicates".

### chandran2026autoresearch — Amazon AutoResearch (2609.30541)

See Q4 for "5.8×" and "220+".
- **object:**
  - System A is L2. §I: "the agent rewrites the entire training script per iteration".
  - System B is L1+L3. §II-B: "proposing changes to hyperparameters and encoder architecture but not rewriting the training script". The target is the RQ-VAE semantic-ID tokenizer.
- **acceptance:**
  - §I: "keeps or discards based on a held-out scalar metric".
  - §VI: System B uses a "post-execution automatic revert that lets the agent attempt cheap hypotheses freely and rolls back on regression".
- **guards:**
  - §II: "an immutable evaluator that the agent observes but cannot modify".
  - §V-E: "cannot change its code, so it cannot inflate its own score".
  - §V-B: "The Code Fixer's pre-execution review caught one DDP wrapper bug".
- **human_role:**
  - §IV-D: "in System B the human researcher (rather than the agent) maintains the program file between runs".
  - Table VI: "Phase transitions are human-driven program.md updates".
- **llm:** "claude-sonnet-4-6 for the Researcher; claude-opus-4-6 for the Code Fixer and Criticizer", via Bedrock.
- **kept_edits:**
  - §V-A: "cross-attention, sentence-transformer fine-tuning, hard-negative contrastive learning …, a temperature curriculum, multi-hop neighborhood profiles, and a dual mean+top-K aggregation".
  - §V-C: "bottleneck encoder, deeper encoder, batch-size and codebook scaling".
- **headline:** Abstract: "a 1.82× Recall@6 lift and a 2.1× coherence lift over hand-tuned baselines".
- **c9_isolation = P.** The evaluator is immutable and the agent's write scope is limited. Access to held-out data is not stated.
- **c9_incident = Y.** The catcher was human QA.
  - §III-E: "the agent discovered that maximizing codebook size trivially improves weighted coherence … but the resulting hierarchy was unusable".
  - §IV-E: "human QA between runs diagnosed metric fixation early on".
  - The index-coverage change is framed by the authors as a coverage–recall trade-off. Treating it as a confound is our inference.
- **c4:** §V-E: one model re-evaluated "on 11 distinct customer-purchase dates". There are no repeated sessions.

### pilot2026 — PILOT (2608.18637)

- **proposer:** llm+space. §4.1: "The Search Planner may only reference action IDs already present in A(T*); it cannot invent actions".
- **meta:** Y. Fig. 2: "the Memory Curator lets experimental methodology evolve across tasks". Table 5 calls it "Meta-knowledge: how to run experiments well".
- **signal_chain:** proxy>online*>online.
  - §4.2: "Round 0 results determine only the order in which candidates are verified".
  - §4.3: "adoption requires a statistically conclusive whole-bucket comparison against the Champion".
  - §3.4: "The test runs once". No confirmation result is reported.
- **acceptance:** §4.3: "Before a Challenger is deployed, the system freezes the decision criteria".
- **guards:** §2: "LLM roles only choose among options these services already generated: they cannot invent a command, alter a statistical conclusion".
- **human_role:** App. C.1: "Human approval. Launching a real wave, increasing traffic, expanding budget, changing the frozen spec…".
  - This is in tension with the abstract's "with no human intervention throughout the experimental cycle".
- **llm:** not stated.
- **kept_edits:** Table 10 bucket changes (21, 24, 25). The best bucket, 23, was "held stable throughout".
- **headline:** Abstract: "up to +1.40% IPV, +1.60% Core IPV, +0.96% transaction count, and +1.50% transaction amount".
- **c9 = P, incident N.**
- **c4:** §6.1: "We report the first five days". §6.3.1: "The comparison in §6.2 is before/after, not randomized".

### jiang2026abagent — A/B Agent (2608.04625)

- **object:** L1. §5.4: "After adjusting the objective weights and decision thresholds, Strategy 2…".
  - The experience tree is the evolver's knowledge, not the policy of an LLM-agent recommender, so it is not L4.
- **proposer:** llm. §4: "GLM-5.1 serves as the foundation model for strategy understanding, generation, and iterative optimization".
- **meta:** N (borderline). §4: "validated outcomes are distilled back into the strategy experience tree". This is a knowledge-base write-back; no skills, prompts or proposer change.
- **signal_chain:** self>online*.
  - §3.2: candidates are "evaluated by agent-based judges in terms of contextual relevance, evidence consistency".
  - Online, the agent "compares successive experiment variants" (§3.3).
  - The GPT-5.5 judge is used only for the offline 310-strategy benchmark (§5.1). It is not in the loop.
- **guards:** §4: "rule-based validators check formatting, numerical ranges, parameter types, and configuration consistency".
- **human_role:** §4: "agent and human reviewers assess safety, rationality, and engineering feasibility. Once approved, the strategy is launched".
- **headline:** Abstract: "a 4.829% improvement in GMV … while maintaining positive gains across all guardrail metrics".
- **c9 = P, incident N.**
- **c4:** one trajectory of 5 strategies.

### zhang2026dmrl — DMRL (2609.02170)

- **object:** L1. §3: the task agent "interprets the modified documents to adjust advertising AB parameters".
  - The skill document belongs to the tuning agent, not to a recommender agent, so it goes under meta, not L4.
- **proposer:** learned+llm. §5.1.2: "an optimizer model iteratively improves its skill-optimization strategy using feedback collected from previous rollouts".
- **meta:** Y. Both the skill document and the DRPO-trained optimizer evolve.
- **signal_chain:** online>proxy*. §5.1.2: "The environment returns short-term outcomes and treatment–control comparison signals, while LRP estimates the corresponding long-term rewards".
- **acceptance:** no keep/reject rule. It is a policy-gradient update with an advantage from Eq. 14.
- **guards:**
  - §5.1.2: "the Task Agent is restricted to a predefined whitelist of parameters and permissible value ranges".
  - §5.1.1: matured-only memory, "preventing temporal information leakage".
- **llm:** Qwen3-8B optimizer. §5.1.2: "OpenAI Codex as the frozen Task Agent, using GPT-5.5".
- **kept_edits:** not reported.
- **headline:** the abstract has no number ("outperforms state-of-the-art baselines"). Table 2: LTV +0.052% vs +0.024%.
- **c9 = P, incident N.**
- **c4:**
  - §5.1.3: "All conclusions are restricted to within-table comparisons".
  - The full DMRL configuration appears with LTV from +0.021% (Table 4) to +0.064% (Table 6).
  - That the Table 3 and Table 4 rows are the full system is our inference.

---

## audit.csv cells that look wrong

1. **fu2026evopilot c2 = NS → test.**
   - §5.1: "Offline evaluation replays held-out pairs against one candidate pool. Its primary selection metric is click hit-rate at depth K".
   - The same replay is reported (§5.4). There is no validation split.
2. **peng2026population c2 = NS → test.**
   - App. A.2: "the remaining 20% supplies the evaluation scores used throughout discovery".
   - Ranking uses the last-item target, and no validation split is described (App. A.1).
   - The exception is VLM, which uses a validation shard. At minimum, add a note.
3. **jiang2026abagent level = L1+meta → L1, with meta N or borderline.**
   - The evolver only writes "validated outcomes … back into the strategy experience tree" (§4).
   - The sweep's "L4 experience tree" label also does not fit the new L4 definition.
4. **fu2026evopilot c9 = gaming.** The isolation value is P.
   - The detector of the leakage retraction is not stated.
   - The funnel mismatch was caught by the human gate. It was a pre-existing evaluator defect, not loop gaming (§4.2, §5.3).
5. **Isolation values for the "gaming" rows.** RecEvolve P; RankEvolve-HSTU N (or P if process gates count); EvoPilot P; Amazon P.
6. **Minor, in evidence-part2 §7 (EvoSkillRec), not audit.csv.** Co-evolution is 30 × 6 = 180 candidates, not 25 × 8 = 200. The §5.5 cost and slot numbers for the main benchmarks are unaffected.
