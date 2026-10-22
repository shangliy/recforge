> **Note (2026-10-21, after review round 1):** the per-paper evidence below is the source; the count sections and
> summary tables in this file are superseded by `audit.csv`, which corrects 12 cells (see `../10-evolve/round-1.md`).

# Audit: self-evolving recommender systems (code/config level)

Source: full text of each paper (arXiv HTML; PDF for 2508.07407), read 2026-10-21. Versions: whatever arXiv served on that date (e.g., 2603.27765v3, 2507.21046v4, 2508.07407v2, 2502.10050v1, 2607.04433v1).
Conventions: "not stated" means the paper does not say. "no" means the paper reports or does something that answers the question negatively. Quotes are verbatim and at most 25 words, with a section or table pointer. "n/a" means the criterion does not apply, for example an offline test split in an online-only system.

---

## 1. 2602.12612 Self-EvolveRec

- **Org:** KAIST (8 authors) + Microsoft (1). **LLM:** GPT-5-mini for planning/retrieval/user simulator, GPT-5 as coder; Claude Opus 4.6 variant (App. H.1). **Evolved:** code. The entire pipeline codebase (architecture, loss, data processing), co-evolved with a diagnosis tool. **Seeds:** NCF, NGCF, SASRec, MoRec; also Random and NCF+NGCF+SASRec ensemble (Sec 4.3.1). **Datasets:** Amazon CDs, Electronics, Office; MovieLens (6,040 users, i.e., ML-1M).
- **C1 metric:** sampled. "Each test item is paired with 99 randomly sampled non-interacted items." NDCG@5/HR@5 (Sec 4, Evaluation Protocol).
- **C2 selection:** validation. Eq. 1 scores codebases on E_val: "score(B) = M(f_B(E_val, X, θ*_B))" (Sec 2).
- **C3 test once:** not stated. Table 4 "Peak indicates the iteration number of the best performance", and Fig. 5b tracks performance "across iterations" without naming the split.
- **C4 variance:** no. Single numbers; seeds or repeated evolution runs are never mentioned (Tables 1–12).
- **C5 overfit check:** no val→test gap. Partial held-out transfer for the simulator: evaluation users are "unseen by SIM during evolution" and PUB uses a different persona scheme (Sec 4.1).
- **C6 null control:** partial. NAS baselines (AutoFIS, NASRec, AutoLossGen, DNS-Rec), but not budget-matched: "search epochs to 5 for AutoFIS and 1 for NASRec" (App. D). LLM baselines AlphaEvolve (via OpenEvolve) and DeepEvolve run under a fixed 5M-token budget (App. H.2.4). No random search or HPO.
- **C7 budget:** "maximum evolution iterations to 21" (App. D); about 19m21s per iteration (Table 9); 5M-token budget experiment (Table 10); one A6000.
- **C8 baselines:** untuned shared settings: "uniformly configured all recommender models… embedding dimension of 50, a batch size of 128, and a learning rate of 0.001" (App. D).
- **C9 isolation:** not stated. Risk: the diagnosis tool "directly accesses the model parameters θ and data loaders within the codebase" (Sec 3.1.2), and the agent may rewrite data-processing logic.
- **Online A/B:** none. "fully validating user-centric improvements ultimately requires real-world A/B testing, which we leave for future" (Sec 5).
- **Code:** https://github.com/Sein-Kim/self_evolverec
- **Headline:** SASRec/CDs NDCG@5 0.3559→0.3865 vs DeepEvolve 0.3610; NGCF/MovieLens 0.1824→0.3588 (Table 1).

## 2. 2607.29241 RecHarness

- **Org:** Georgia Institute of Technology + Kuaishou Technology. **LLM:** not stated ("ϕ denotes the frozen LLM used for code generation"; details deferred to a Supplement that is not in the HTML). **Evolved:** code edits inside human-defined "edit arms" (LR schedule, dropout, layers/heads, pooling, features, loss; jump arms for structural changes). **Base models:** GRU4Rec, BERT4Rec, NextItNet, SASRec, HSTU (Amazon); D2Q, TPM, GR (KuaiRec). **Datasets:** Amazon Reviews Movies, Scientific, Electronics, CDs; KuaiRec.
- **C1:** sampled. "Each evaluation set contains one positive item and 99 sampled negatives" (Metrics). KuaiRec uses XAUC/MAE.
- **C2:** validation. "RecHarness uses only validation feedback for candidate selection, routing updates, and version promotion" (Search protocol).
- **C3:** yes. "The test set is used only once after search for final evaluation" (Search protocol).
- **C4:** 3 runs. "averaged over three runs" (Table 3 caption). No std or CI reported; repeats are not stated for KuaiRec (Table 4).
- **C5:** no quantitative val→test gap. Qualitative only: "w/o Bandit finds useful local edits but generalizes worse" (Ablation).
- **C6:** partial. Ablation "TR w/ Random replaces Thompson Routing… with uniform random arms selection" (the LLM still writes the edits) under the same GPU budget. Optuna is cited but not compared.
- **C7:** "For every model, we set a total GPU-time budget of 43,200 s"; 4 parallel trials per round; about 48 trials (Table 5).
- **C8:** "Base denotes the cold-start baseline"; also compared with "Paper", i.e., reported numbers from Kim et al. 2025 and Ma et al. 2026. Base tuning is not described, and the GRU4Rec base is weak (avg HR@10 0.2685).
- **C9:** "Each candidate runs in an isolated workspace" (Trial execution). Whether the agent can reach test labels is not discussed.
- **Online A/B:** "7-day online A/B test on 10% of traffic" in short-video ads: ADVV +2.084%, Revenue +0.534%, Exposure +0.559% (Table 6); offline AUC +0.09%. Guardrails and significance not stated.
- **Code:** https://github.com/6lyc/RecHarness
- **Headline:** avg HR@10 "+85.85% on the weaker GRU4Rec baseline and by 12.58% on the stronger HSTU baseline" vs cold-start base.

## 3. 2602.10226 Self-Evolving RS (Google/YouTube)

- **Org:** Google Inc. (YouTube). **LLM:** Gemini 2.5 Pro (Gemini 2.5 Flash ablation). **Evolved:** config plus code deltas: optimizer and hyperparameters, architecture code ("Θ(10) lines of a component's code within Θ(1000)-line model definition"), reward logic (Sec 4.1.1). **Base:** production value-based RL ranking DNN on the YouTube watch page. **Datasets:** production logs.
- **C1:** loss/proxy plus online. Offline proxy is loss (compute_loss) or "long-watch correlation" (compute_eval); north-star online metrics. No ranking-accuracy metric.
- **C2:** offline "validation loss values are comparable" (Sec 4.1.1, optimizer persona). The Online Agent ranks candidates using online metrics to pick A/B arms (Sec 4.2).
- **C3:** not stated (offline). Online A/B is the final arbiter.
- **C4:** ablation only: "Results are averaged over 6 independent runs exploring 70 ideas each" (Sec 5.4, Table 4 with CIs). Online headline results come from single experiments with 95% CIs.
- **C5:** no val/test gap. Transfer to a second surface "with a completely different feature schema" (L5, Table 2).
- **C6:** no HPO or Vizier baseline. The comparison is against historical human launches: "outperformed 64% of launches generated using the traditional, manual approach" (Sec 5.1).
- **C7:** "LLM token costs were approximately $20,000 over a six-month period" (Sec 5.5.2); throughput Θ(100)/week (Table 5).
- **C8:** production human-engineered model. Claims to "surpass hand-tuned baselines" (Sec 1).
- **C9:** not stated.
- **Online A/B:** YouTube-level and surface-level north-star metrics with 95% CIs (Tables 1–2). Prompt guardrail "Keep Metric#3 ≤ +1%" (Fig. 3). Durations not stated.
- **Code:** not released.
- **Headline:** e.g., Gated Path +0.06% YouTube-level / +0.14% surface; Wide&Deep +1.10% surface-level (Table 2); training time 8× faster (Sec 5.2.2).

## 4. 2606.28368 EvoRec

- **Org:** Alibaba International Digital Commerce Group. **LLM:** Claude Opus 4.6 for all four agents. A Qwen3.7-MAX reproduction "yields consistent conclusions", with no numbers (Sec 3.1.3). **Evolved:** code (hyperparameters, sampling, loss, architecture; Table 3) plus a Skill library. **Base:** MGUI (ID-based), REG4Rec (generative). **Datasets:** Amazon Books; an industrial SE-Asian e-commerce dataset (2.95B interactions).
- **C1:** not stated. "We adopt leave-one-out evaluation and report Recall@5/10… and NDCG@5/10" (Sec 3.1.1). Candidate set and negatives unspecified.
- **C2:** not stated. Memory stores "metric_(t) the offline evaluation metric vector" (Sec 2.4); split unnamed.
- **C3:** not stated. **C4:** no (single numbers, Tables 1–2). **C5:** no.
- **C6:** partial. "AutoML (He et al., 2021), applied to each base model… as Auto-MGUI and Auto-REG" (Sec 3.1.2). The cited work is a survey, and the method and budget are unspecified.
- **C7:** "T_(max) = 50" iterations, early stop after k=10, 4×A100 (Sec 3.1.3). No tokens, $, or time.
- **C8:** "Training hyperparameters for both base models follow their original papers" (Sec 3.1.3). Baseline tuning not described.
- **C9:** not stated.
- **Online A/B:** 7 days, 20% of users per arm, control = production MGUI: revenue +1.85%, CTR +1.02%, "two-sided test (p < 0.05)" (Sec 3.5). Guardrails not stated.
- **Code:** not released.
- **Headline:** "up to 5.54%" relative N@10 over the strongest baseline (Books: 0.0381 vs MGUI 0.0361).

## 5. 2606.03221 VirtualMLE

- **Org:** Tsinghua University SIGS + BUPT. **LLM:** GPT-5.4 (robustness runs with Kimi 2.6 and DeepSeek V4 Pro, Table 4). **Evolved:** config: hyperparameters plus "selected architectural switches"/structural choices (Sec 1). **Base:** SASRec, HSTU. **Datasets:** Amazon-2014 Baby, Beauty, Pet.
- **C1:** not stated. "split each dataset according to the leave-one-out protocol. We report Recall@K and NDCG@K" (Sec 4.1). Negatives unspecified.
- **C2:** validation. "All tuning decisions are made exclusively on the validation set" (Sec 3.1); "final model is always selected by validation NDCG@10" (Sec 4.1).
- **C3:** yes. "Only the final configuration selected on the validation set is evaluated on the test set" (Sec 3.1).
- **C4:** 3 runs. "results are averaged over three independent runs" (Sec 4.1). No std.
- **C5:** partial. Validation N@10 (Table 2, e.g., SASRec/Baby 0.0394) and test N@10 (Table 1, 0.0321) are both reported, but the authors say they are "not directly comparable" (Sec 4.4 footnote). Cross-dataset transfer of the Cognition Summary: 28→10 trials (Fig. 2).
- **C6:** yes. Grid Search ("enumerates all 729 configurations"), Bayesian Opt. ("runs for 500 trials"), and OPRO with the same LLM and action interface; "search budget is configured to favor the baselines" (Sec 4.1).
- **C7:** trials to best validation score: 17–32 vs BO 163–464 (Table 2); LLM cost $1.5–4.8 per session (Table 4).
- **C8:** AutoML-tuned SASRec/HSTU as above. For generative baselines they "follow the experimental setup reported in (Zhou et al., 2026)" (possibly copied numbers; not stated).
- **C9:** yes. "The test set is completely hidden from the agent during exploration, and the data preparation pipeline is immutable" (Sec 3.1).
- **Online A/B:** none.
- **Code:** https://github.com/cst20/VirtualMLE-is-all-you-need-to-Recommend (linked as "here" in the abstract).
- **Headline:** up to +12.1% N@5 over the best baseline (HSTU/Baby); "average relative gain of 29.9%–31.9% over vanilla SASRec" (Sec 4.2).

## 6. 2606.27243 NOVA

- **Org:** Tencent Inc. **LLM:** "All LLM-dependent stages use Claude Sonnet 4.6", with a ranking ensemble of GPT, Claude Opus, Gemini, Kimi ("latest production versions") (Sec 5.2, 4.3.2). **Evolved:** architecture code: computation graph, feature configuration, structural hyperparameters (Sec 3). **Base:** production RankMixer-style pCVR backbone; L3 tasks port TokenMixer-Large/MixFormer. **Datasets:** industrial ads, one month, billion-scale, >1,000 feature fields.
- **C1:** AUC. "baseline-relative AUC gain in percentage points"; AUC-positive ≥0.10 pp; primary metric is the effective pass rate EPR (Sec 5.2).
- **C2:** not stated (split). Selection is "the best observed offline metric" J_offline (Sec 3). GMV/bias are "validation metrics rather than search objectives".
- **C3:** not stated.
- **C4:** 20 tasks per setting (N_iter ≤200), aggregated into rates. No seeds or CIs on the rates.
- **C5:** no.
- **C6:** yes (L2 only). Optuna-TPE under the "same maximum offline-evaluation budget"; "LLM inference cost is not matched" (Sec 5.3). Also OpenHands/ReAct/R&D-Agent with the same skills.
- **C7:** R_max = 10 rounds, K = 4 candidates, ≤1 offline evaluation per round (Sec 5.2). About $29 of Claude API per task (sum of Table 5 stages).
- **C8:** "All coding-agent baselines receive the same reusable skills"; R&D-Agent is a "budget-matched adaptation"; the human reference is "retrospective… not budget matched".
- **C9:** agent access is not discussed. "target leakage" is listed among the semantic silent failures to reject (Sec 1).
- **Online A/B:** "six-day, user-randomized A/B test on 5% of production traffic": GMV +1.25/+1.70/+2.02% ("statistically significant"), absolute pCVR bias −58.8/−66.7/−37.3% (Table 4). The task template has a guard margin ε (App. A.3.1).
- **Code:** not released ("we do not release it verbatim"; mechanism-level artifacts only).
- **Headline:** EPR 53.3% (L2) / 51.7% (L3) vs R&D-Agent 29.2% / 28.3% (Table 1).

## 7. 2606.26859 AgentX

- **Org:** "AgentX Team" (alphabetical author list, App. A). No affiliation line; deployed on the Kuaishou App. **LLM:** not stated. **Evolved:** production strategy code (C++/DSL ranking formulas); model architecture (paper reproduction, module ablation, cross-paper composition); agent harness prompts (SGPO). **Base:** production main-feed and life-service ranking; RankMixer for the model track. **Datasets:** Kuaishou production; KuaiRand, Taobao, Amazon, ML-1M (App. B); industrial ads (B.3).
- **C1:** strategy track is online A/B only; model track uses offline AUC (Tables 13–15).
- **C2:** online A/B: "eligible for KEEP only when the primary objective clears both a minimum effect threshold and statistical significance" plus guardrail veto (Sec 6.3). For the model track, the split behind "Beats baseline (public datasets)" is not stated (Table 9). SGPO edits are admitted by a paired-replay LLM-judge score (Sec 7.1).
- **C3:** not stated.
- **C4:** no for headline numbers. The KB requires "evidence from at least two independent runs" (Sec 7.2).
- **C5:** partial. Public→industrial transfer of modules; "the ranking is not strictly preserved" (App. B.3).
- **C6:** no. The comparison is against "a single algorithm engineer under the traditional manual-iteration workflow" (Table 8).
- **C7:** 3 workers × 3 weeks, 374 ideas → 10 launchable results (Table 5); model study 214 dispatched experiments (Table 9). No tokens, $, or GPU figures.
- **C8:** public-data baseline is the production model "simplified only to fit the public-dataset feature schema" (Sec 8.2). Tuning not described.
- **C9:** not discussed. "Parameter changes must pass an engineering whitelist" (Sec 6.2).
- **Online A/B:** 3-week deployment; main feed "0.561% in user app consumption time"; life service "over RMB 100 million in annualized revenue" (Sec 8.1). CUPED/DiD, canary release, guardrail veto. Model track: 22 A/Bs → 5 positive → 2 launches (+0.865% live-stream duration).
- **Code:** not released.
- **Headline:** "8× concurrency and 3.7× business value over a manual engineer" (abstract).

## 8. 2609.30001 AgentX-Model

- **Org:** not stated in the HTML (author list only; successor of AgentX). **LLM:** "privately deployed GLM-5.2" (Research Agent on Pi runtime, Model Agent on Claude Code); GLM-5.3 for replay/assessment (Sec 4.1.1). **Evolved:** model code (feature interactions, routing, backbones, task towers, losses) via Reproduce/Follow-up/Composition/Diagnose; human-approved tool/instruction repair (App. B.2). **Base:** business baselines, Scenarios A–E. **Datasets:** unnamed production settings.
- **C1:** AUC (plus PCOC calibration); online A/B.
- **C2:** not stated (split). Each experiment's result is its best round, "b_i = max_r AUC_(i,r)" (Eq. 3), and later work continues from it. Calibration is reported as "test PCOC" (Sec 4.3.3).
- **C3:** not stated. Best-of-rounds selection on the same reported measurement; no separate final test is described.
- **C4:** partial. "With the random seed fixed, repeated executions yield pooled within-implementation AUC standard deviations of 0.002208, 0.001010, and 0.001099" (Sec 4.1). Yet an experiment counts as above baseline if it exceeds it "by more than 10⁻⁶" (Table 4 caption). Scenario D's best gain (+0.001776) is under 2σ.
- **C5:** no val/test gap. Cross-setting Knowledge Transfer (Table 9; largest gain 0.000789).
- **C6:** partial, in historical replay only: "Uniform Random's mean exceeds Fixed, Greedy, and Joint" in Scenario A (Sec 4.5). No null control for the production gains.
- **C7:** 636 experiments over about 25 days; proposal median 33.6 min (Table 3); replay "97.5 million metered tokens", ~430 min for 36 agent runs.
- **C8:** production business baselines.
- **C9:** partial. "The Model Agent modifies model code, while evaluation uses fixed code provided by the platform" (Sec 4.1.1); "The test split and acceptance rules remain outside the repair agent's control" (App. B.2).
- **Online A/B:** five latest launch reviews: acquisition efficiency 10–15%, target-segment ad spend 15–20%, watch time 0.3–0.8% (Table 6, "coarse ranges"). Duration and guardrails not stated.
- **Code:** not released.
- **Headline:** "560 of 636 completed model-changing experiments recorded AUC above their business baselines"; Scenario A best ΔAUC +0.023669 (Table 4).

## 9. 2609.10922 Auto-RecSys

- **Org:** Meta (one author also UIUC). **LLM:** not stated. **Evolved:** per-idea model code/config (embedding strategies, gating, auxiliary losses, features) plus model playbooks (execution knowledge). **Base:** "several industry-scale recommendation models" (unnamed). **Datasets:** internal, unnamed.
- **C1:** not stated. "the analysis computes performance differences against the baseline and assigns a verdict of positive, neutral, or negative" (Sec 5.3). No model-quality numbers are reported.
- **C2:** not stated. "All ideas on the same model share a common baseline with aligned training date ranges, ensuring fair A/B comparison" (Sec 5.2).
- **C3:** not stated. **C4:** no. **C5:** no. **C6:** no (qualitative comparison with the manual process).
- **C7:** 31 iterations on one model, 46 sessions; "a single training job may consume hundreds of GPU-hours" (Sec 6). No token or $ figures.
- **C8:** n/a (production baseline; it shifts at iteration 21).
- **C9:** not stated. Human checkpoints exist in interactive mode. "Auto-RecSys currently accepts playbook updates unconditionally based on agent judgment" (Sec 9).
- **Online A/B:** none reported.
- **Code:** not released.
- **Headline:** operational only: major fixes per iteration "from 4.0 to 0.5" across 31 iterations (Sec 10). No accuracy gain claimed.

## 10. 2609.04871 AutoLR

- **Org:** NetEase, Inc. (DASHEN app). **LLM:** Claude Opus-class, then migrated to "a mixed DeepSeek-V4-Pro/Flash stack" (abstract). **Evolved:** model and config code on a declared edit surface (sequence modeling, expert routing, feature interaction, gating, task weighting, regularization, training strategy) (Sec 3.3). **Base:** production DASHEN rankers (two feeds). **Datasets:** internal.
- **C1:** other/unspecified. "click- and watch-time-related offline metrics are combined into a scalar proxy" plus protected guardrail metrics (Sec 3.6).
- **C2:** offline scalar delta vs the active trunk under a "fixed offline evaluation contract". The split is not stated. KEEP is a single run: "The E1 suffix marks a one-run offline threshold crossing rather than a confirmed effect" (Sec 3.6).
- **C3:** not stated. KEEP rewrites the trunk used for later comparisons (the "KEEP ratchet").
- **C4:** no. "noise calibration was disabled in the audited configuration" (Sec 5.3); the archive "lacks… broad fixed-snapshot repeats" (Sec 6.2).
- **C5:** no measurement. Adaptive overfitting is discussed explicitly (Sec 2.3), and the reference floor 10⁻³ is about the IQR of the deltas (1.2×10⁻³, Table 2).
- **C6:** no. "it does not establish superiority over random, greedy, or direct LLM-based routing under a matched trial budget" (Sec 3.3).
- **C7:** 1,586 completed evaluations; "LLM API cost of RMB 3–4 per iteration, excluding model-training compute" (abstract).
- **C8:** production trunk.
- **C9:** partial. Preflight verifies "frozen objectives or evaluation logic are not modified" (Sec 3.5); "the training and evaluation pipeline remains fixed" (Sec 4.1).
- **Online A/B:** nine Launch Reviews of engineer-selected candidates. Summed lifts +5.75% penetration, +10.83% consumption time, +5.55% VV, "descriptive and are not pooled treatment effects" (abstract). No CIs (Sec 6.2). Human-gated.
- **Code:** not released.
- **Headline:** 1,586 evaluations and 9 positive Launch Reviews; identifies the KEEP-ratchet failure mode.

## 11. 2609.02730 CORAL

- **Org:** Meta AI. **LLM:** not stated ("a general-purpose LLM"; cost at "representative frontier-LLM pricing"). **Evolved:** config/policy. Retrieval-budget multipliers per source; per-segment serving treatment from a discrete menu. No code changes. **Base:** live production recommenders on "two large-scale social platforms". **Datasets:** live traffic.
- **C1:** online A/B only (watch time, sessions; serving cost).
- **C2:** online. "its effect is measured with an A/B experiment whose result is written back to memory" (Sec 4.3), with a cadence of k = 3 days.
- **C3:** n/a. **C4:** no seeds; A/B significance only ("'neutral' denotes no statistically significant change", Table 1). **C5:** no.
- **C6:** no (no bandit, BO, or random-allocation baseline).
- **C7:** k = 3 days, memory m = 3 cycles; about 10 calls per cycle, ~1.5k input / ~2.5k output tokens per call, "estimated… the pipelines do not log token usage" (Table 2); "tens of U.S. dollars" per deployment (Sec 6).
- **C8:** production allocations "typically hand-set and seldom revised" (Sec 5.1).
- **C9:** n/a (no offline labels). Guardrails: "feasibility checks, bounded-change limits, and safety constraints"; a constrained optimizer enforces the budget (Sec 4.3).
- **Online A/B:** video service rounds R1–R3. Deployed configuration: sessions +0.16%, watch time +0.15% (largest market +0.77%); new low-signal users +0.23% sessions. Second surface: serving savings of "millions of USD" annualized, +44% in round 2, engagement "statistically unchanged". Per-test durations not stated.
- **Code:** not released.
- **Headline:** +0.16% sessions and +0.15% watch time at no extra serving cost.

## 12. 2604.26969 AgenticRecTune

- **Org:** Google (Mountain View). **LLM:** Gemini 3 Pro (ablations Gemini 3 Flash, Gemini 1.5 Pro; Table 2). **Evolved:** system-level config (fusion weights, thresholds) in pre-ranking, ranking, and re-ranking. No model code. **Base:** production Google Discover configurations. **Datasets:** live traffic.
- **C1:** online A/B only (anonymized "Engagement Metric 1/2", "Diversity Metric").
- **C2:** online. The Online Agent gathers "the final performance metrics (e.g., the North Star metrics and statistical significance)" (Sec 4.2.3). Memory keeps a Pareto "top performers" pool (Sec 4.3.2).
- **C3:** n/a. **C4:** no (p<0.05 per A/B). **C5:** no.
- **C6:** no. Grid search is mentioned only rhetorically ("more efficiently than traditional grid search methods", Sec 5.2.2). The only strategy ablation is single-agent vs actor-critic (Table 3).
- **C7:** not stated (only "rounds of small traffic of iteration").
- **C8:** control is "the existing tuned configurations on the production" (Sec 5.1).
- **C9:** n/a. "Before online A/B testing starts, the users' review is required" (Sec 4.2.2).
- **Online A/B:** "standard launch period to ensure statistical significance (evaluated at a p-value < 0.05)" (Sec 5.1); duration not stated. Secondary-metric floors b_j appear in the formulation (Sec 3).
- **Code:** not released.
- **Headline:** pre-ranking +0.75% / +0.90% engagement; re-ranking diversity +3.43% (Table 1). The model ablation text says "diversity task in the pre-ranking stage", but the Table 2 caption says re-ranking (internal inconsistency).

## 13. 2603.27765 Sortify

- **Org:** Shopee ("All authors are from Shopee"). **LLM:** an OpenAI model "through the Codex CLI's exec subcommand"; cost quoted at GPT-5.4 / GPT-5.3-Codex prices; the exact model is not named (Sec 2.5.4, 4.9). **Evolved:** config. The LLM adjusts framework knobs (transfer intercept |Δβ| ≤ 0.1, penalty multiplier ∈ [0.5, 2]); Optuna TPE searches the 7-dimensional sorting-formula weights. **Base:** production sorting formula (product detail page), Country A/B. **Datasets:** live traffic.
- **C1:** online A/B (GMV, Orders, Ads Revenue) plus the offline "Influence Share" proxy (not a ranking-accuracy metric).
- **C2:** online A/B per ~3.5 h window. In Country B, R7 was frozen as "the only round where GMV and Ads Revenue were simultaneously positive" (Sec 4.8.2), i.e., selected on the same online signal.
- **C3:** partially yes. The frozen parameters were re-tested in a fresh "7-day A/B test (03-15 to 03-22… 10% treatment vs. 20% control)" before rollout (Sec 4.8.4).
- **C4:** no. The Country A peak came from "a low-traffic early morning window (∼12K impressions)" (Sec 4.3.1). No CIs.
- **C5:** offline→online proxy gap reported (I_gmv +18.2% vs GMV −3.6%; +41.6% vs +9.2%; Table 5). This is not a val/test gap.
- **C6:** no. Optuna is the inner search; there is no Optuna-only or LMS-only (no-LLM) ablation.
- **C7:** "5,000 trials", 25 workers, ~4 h cycle, "6.25–12.5 CPU-hours per round", 1 LLM call per round costing ~$0.03–0.10 (Sec 4.9); 30 rounds in total.
- **C8:** manual loop of "1–2 human-hours per optimization round" (Sec 4.9).
- **C9:** n/a. LLM runs "--sandbox read-only"; a seven-layer output safety pipeline with hard clamps (Sec 2.5.4).
- **Online A/B:** Country A, 7 rounds / 25 h: GMV −3.6%→+9.2%, Orders +12.5%; Advertiser Value negative R3–R7 (Table 4). Country B 7-day A/B: GMV/UU +4.15%, Ads Revenue +3.58%, then rollout (Table 10). Constraints include I_order degradation ≤5%, eCPM, ads top-10 rate.
- **Code:** not released (cites the predecessor repo github.com/yinsn/ParaDance).
- **Headline:** +4.15% GMV/UU, +3.58% Ads Revenue (Country B).

## 14. 2602.18640 GEARS

- **Org:** Meta (Menlo Park). **LLM:** Claude Sonnet 4.6. **Evolved:** policy. Segment→treatment personalization policies selected from GAS heterogeneous-treatment-effect candidates. Skills are static, "read-only resources"; no model code changes. **Base:** GAS candidate policies. **Datasets:** 20 internal online experiments (~0.5B users each) → 100-instruction benchmark.
- **C1:** benchmark nDCG@1/3/5, Prec@k, Recall@k over candidate *policy* lists vs deterministic ground truth (not item recommendation). Production reports online metric lifts.
- **C2:** online experiment data. Policies are chosen on HTE estimates from the same randomized experiment, behind a "Statistical-significance guard… 95% confidence interval excludes zero" (Sec 4).
- **C3:** not stated. **C4:** no seeds; CIs on production metrics (e.g., "+0.832% ± 0.039", Sec 4.1).
- **C5:** partial. "backtest results indicate that the metrics improvement… remains consistent over a period of one month" (Fig. 5), for one policy.
- **C6:** no non-LLM selection baseline. Baselines are prompting methods: Naive, CoT, Self-Consistency, Self-Refine, Code-as-Action (Table 1).
- **C7:** "approximately 3.9K input tokens and 35.8K output tokens, costing roughly $3.75 per run"; ~$1,500/year (Sec 5.5).
- **C8:** same LLM across all prompting baselines; no tuning discussion.
- **C9:** n/a / not stated.
- **Online A/B:** nine Meta surfaces, Metric 1 lifts 0.011–0.14% (Table 3). Duration and significance per surface not stated.
- **Code:** not released.
- **Headline:** 0.94 nDCG@1 vs 0.77 for Code-as-Action (Table 1).

## 15. 2603.22376 AI Co-Scientist for production search ranking

- **Org:** Trip.com Group + UCLA. **LLM:** GPT-5.2, Gemini Pro 3, Claude Opus 4.5 (majority-vote consensus); single LLM for coding. **Evolved:** model code (transformer layout, slot-type/temporal embeddings) and LR schedules. **Base:** V2 human-designed transformer (V1 = mean-pool + DCN + MoE). **Datasets:** production hotel search logs (5 of 200+ sequence slots).
- **C1:** AUC. ℳ is the "average of 6 AUC metrics… over 7 days of unseen data" (Sec 3.2.6).
- **C2:** that same held-out ℳ. "computes Δℳ against the previous best and proceeds accordingly" for keep/revert (Sec 3.2.6).
- **C3:** no. Table 1 reports the same ℳ that drove keep/revert; there is no separate final test.
- **C4:** no. "All entries are single best runs without repeated seeds or confidence intervals" (Table 1 caption).
- **C5:** no.
- **C6:** no. "We cannot refute this without a parallel human-only arm" (Sec 4.2, compute-substitution).
- **C7:** "∼1,650 vs. ∼150 H20-hours"; ~1 extra week of wall-clock (Sec 1).
- **C8:** human-designed V2 with inherited LR 5×10⁻⁵. The V3.2 gain came from lowering the LR, which suggests the baseline LR was not re-tuned for the new architecture.
- **C9:** not stated. The paper reports "metric-winning bugs (e.g., silently increasing model size)" (Lesson 3).
- **Online A/B:** none for V3.5 alone: "we make no online claim for V3.5 in isolation" (Sec 4.3).
- **Code:** not released.
- **Headline:** +0.083 (AUC×100) from the AI loop on top of the human +0.118; combined +0.201 vs V1.

## 16. 2609.01622 RecEvolve

- **Org:** Google (Mountain View). **LLM:** not stated. **Evolved:** model code/config: learnable temperature, watch-time-weighted contrastive loss, DCN-V2 user tower, gated dense layers, cosine LR, batch size. **Base:** "mature large-scale production Two-Tower retrieval model". **Datasets:** production (unnamed); TPU clusters.
- **C1:** not stated (candidate set). "NDCG, MRR, and Recall @ K (K = 1, 5, 50, 200)" (Sec 4).
- **C2:** not stated. Algorithm 1 keeps a candidate if γ(Φ_NS) > τ + ε, computed by an "evaluation suite"; Fig. 4 refers to "continuous validation convergence".
- **C3:** not stated. **C4:** no. **C5:** no.
- **C6:** no.
- **C7:** "41 distinct autonomous experiments in approximately 2 days… each individual run requiring over 3 hours"; 5 threads; 2M-step runs (Sec 4–5).
- **C8:** production model.
- **C9:** not stated, and evidently not enforced. "reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics" (Sec 5.2), caught by humans.
- **Online A/B:** "User Satisfaction +3.77%", Cold-Start −16.50% (faster), Unique Content +7.44% (Table 2). Duration, significance, and guardrails not stated.
- **Code:** not released.
- **Headline:** NDCG@50 0.4796→0.5751 (+19.9%) (Table 1).

## 17. 2609.22196 EvoRank (learning-to-rank; comparison point)

- **Org:** University of Maryland + Independent Researcher. **LLM:** not stated (SkyDiscover / AdaEvolve engine, "one LLM call per iteration"). **Evolved:** code in EVOLVE-BLOCKs. Campaign 1: the LambdaMART gradient (loss); campaign 2: feature code plus pipeline spec (models, losses, ensemble). **Base:** XGBoost rank:ndcg. **Datasets:** Expedia ICDM 2013 (9.9M impressions, 399k queries), 70/15/15 split by query.
- **C1:** per-query full-list NDCG@10/@38, booking NDCG, pooled revenue. This is learning-to-rank over the shown list; no negative sampling.
- **C2:** selection fold. "a small fitness fold of 8k training queries… scored on the fold's held-back validation queries" (Sec 3.3).
- **C3:** yes. The transfer audit is "re-scoring every checkpoint's selected program on 60k held-out queries"; Kaggle hidden test "one shot each, no leaderboard iteration" (Sec 3.4, 5).
- **C4:** 3 independent runs per condition plus a 10,000-sample paired query bootstrap. The authors add that "Three runs… suffice for the paired-bootstrap headline… but not to characterize the variance of the search itself" (Sec 6).
- **C5:** yes, explicit. Val vs Test in Table 1 and Fig. 4. Campaign 1 gains "were almost entirely fitness noise"; "roughly 70 percent of selection-fold gains survive" in campaign 2.
- **C6:** yes. "equal-budget random-search controls" (random search transferred as well or better in campaign 1, p = 0.03); Optuna-tuned baseline; "equal tuning on both sides" (Sec 3.4).
- **C7:** "50 iterations (about ten dollars)" per run; 5–40 s per evaluation.
- **C8:** strong. "LambdaMART (XGBoost rank:ndcg) with 40 Optuna trials", re-tuned at every training size. Full-scale re-tuning "reverses that verdict" until capacity is matched (Sec 5).
- **C9:** yes. Frozen data preparation; label statistics only through helpers "with leakage guards built in"; the audit caught three target-encoding leakage bugs (Sec 5).
- **Online A/B:** none ("audited for transfer, not for online effects").
- **Code:** https://github.com/shabazpatel/evorank
- **Headline:** +0.0057 NDCG@10 (95% CI [0.0041, 0.0073]) vs Optuna-tuned LambdaMART on 60k held-out queries; Kaggle private NDCG@38 0.5196 (top 6%).

---

## Summary table

Legend: Y = yes / stated; N = no; NS = not stated; P = partial; n/a = not applicable. C1: S99 = sampled with 99 negatives; LOO-NS = leave-one-out ranking with the candidate protocol unstated; AUC = AUC or loss proxy; ON = online A/B primary; LTR = full per-query list; ? = no metric stated.

| # | Paper | Evolves | C1 metric | C2 selection signal | C3 test once | C4 variance | C5 gap/transfer | C6 null control | C7 budget reported | C8 baselines tuned | C9 isolation | Online A/B | Code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Self-EvolveRec | code | S99 | val (Eq.1) | NS | N | P (held-out simulator) | P (NAS, unmatched) | iters, time, tokens | N (fixed shared HPs) | NS (agent edits loaders) | none | Y |
| 2 | RecHarness | code (arms) | S99 | val | Y | 3 runs, no std | N | P (random arm routing) | GPU-s 43,200 | NS (cold-start base) | P (isolated workspace) | 7d, 10% | Y |
| 3 | Google/YouTube | config + code deltas | AUC (loss) + ON | val loss + online | NS | ablation only (6 runs) | P (2nd surface) | N | $20k / 6 mo | prod. baseline | NS | yes, CIs | N |
| 4 | EvoRec | code | LOO-NS | NS | NS | N | N | P (unspecified AutoML) | 50 iters | "original papers" | NS | 7d, 20% | N |
| 5 | VirtualMLE | config (+switches) | LOO-NS | val | Y | 3 runs, no std | P (val & test both shown) | Y (Grid 729, BO 500, OPRO) | trials, $ | Y (AutoML-tuned) | Y | none | Y |
| 6 | NOVA | code (architecture) | AUC | NS | NS | 20 tasks, no CI | N | Y (Optuna-TPE, L2) | rounds, $/task | same skills | NS | 6d, 5% | N |
| 7 | AgentX | code + strategy + prompts | ON (+AUC) | online A/B | NS | N | P (public→industrial) | N (vs engineer) | ideas/weeks | NS | NS | 3 wk | N |
| 8 | AgentX-Model | code | AUC | NS (best round) | NS | P (std reported, ignored) | N | P (replay only) | experiments, tokens | prod. baseline | P (fixed eval code) | 5 LRs | N |
| 9 | Auto-RecSys | code/config | ? | NS | NS | N | N | N | iterations | n/a | NS | none | N |
| 10 | AutoLR | code/config | ? (scalar proxy) | NS (one-run KEEP) | NS | N (calibration off) | N | N (explicitly) | evals, RMB/iter | prod. trunk | P (frozen eval) | 9 LRs, no CIs | N |
| 11 | CORAL | config/policy | ON | online A/B | n/a | N | N | N | calls, tokens | hand-set prod. | n/a | yes | N |
| 12 | AgenticRecTune | config | ON | online A/B | n/a | N | N | N | NS | prod. tuned | n/a | yes (p<.05) | N |
| 13 | Sortify | config | ON + proxy | online A/B | P (fresh 7d A/B) | N | P (offline→online) | N | trials, CPU-h, $ | manual loop | n/a | 7d | N |
| 14 | GEARS | policy | ON (+benchmark nDCG) | online experiment data | NS | N (CIs only) | P (1-month backtest) | N | tokens, $ | prompting only | n/a | 9 surfaces | N |
| 15 | AI Co-Scientist | code + LR | AUC | held-out eval = report set | N | N (single runs) | N | N | GPU-h | P (inherited LR) | NS (bugs noted) | none | N |
| 16 | RecEvolve | code/config | LOO-NS (NDCG/MRR) | NS | NS | N | N | N | runs, hours | prod. | N (reward hack found) | yes | N |
| 17 | EvoRank (LTR) | code | LTR | val (fitness fold) | Y | 3 runs + bootstrap | Y | Y (random search, Optuna) | iters, $ | Y (Optuna 40) | Y | none | Y |

### Counts (n = 17; 16 if EvoRank is excluded)

- **C1 metric:** 0/17 state full-catalogue ranking evaluation. 2 use sampled metrics with 99 negatives (Self-EvolveRec, RecHarness). 3 report LOO ranking metrics without stating the candidate set (EvoRec, VirtualMLE, RecEvolve). 4 use AUC or a loss proxy as the primary offline metric (Google, NOVA, AgentX-Model, Co-Scientist). 5 are online-A/B primary (AgentX, CORAL, AgenticRecTune, Sortify, GEARS). 2 state no usable metric (Auto-RecSys; AutoLR's unspecified scalar). 1 uses a full per-query LTR list (EvoRank).
- **C2 selection signal:** among the 12 papers with an offline accept/reject loop, 4 name a validation split explicitly (Self-EvolveRec, RecHarness, VirtualMLE, EvoRank); Google says "validation loss"; Co-Scientist selects on the held-out set it also reports; 6 do not state the split (EvoRec, NOVA, AgentX-Model, Auto-RecSys, AutoLR, RecEvolve). The other 5 select on online A/B.
- **C3 test exactly once:** 3/17 yes (RecHarness, VirtualMLE, EvoRank); 1 partial (Sortify, fresh 7-day A/B after the freeze); 1 explicit no (Co-Scientist); the rest not stated or n/a. **Of the 11 recommender papers with an offline selection loop (the 12 above minus EvoRank), only 2 state test-once (RecHarness, VirtualMLE).**
- **C4 variance on headline numbers:** 3/17 report repeated runs (RecHarness 3, VirtualMLE 3, EvoRank 3 plus bootstrap). None of the first two report std or CIs. 2 partial (Google: ablation only; AgentX-Model: reports run-to-run σ ≈ 0.001–0.002 AUC but counts any gain >10⁻⁶ as "above baseline"). 12 report none.
- **C5 val→test gap / transfer:** 1/17 reports an explicit selection-vs-held-out gap (EvoRank); 6 partial (Self-EvolveRec, VirtualMLE, Google, AgentX, Sortify, GEARS); 10 none.
- **C6 null control:** 3/17 have a real non-LLM search baseline (VirtualMLE: Grid/BO; NOVA: Optuna-TPE; EvoRank: equal-budget random search + Optuna). 4 partial (Self-EvolveRec NAS with unmatched budget; EvoRec unspecified "AutoML"; RecHarness random routing with LLM edits; AgentX-Model random/greedy in replay only). 10 none. Where tested properly, the null control was competitive: in EvoRank campaign 1, random search transferred as well or better (p = 0.03), and in AgentX-Model's Scenario A replay, Uniform Random beat the agent policies on mean best AUC.
- **C7 budget:** reported in some unit by 16/17 (AgenticRecTune reports none). Units are heterogeneous (iterations, GPU-seconds, GPU-hours, tokens, $, RMB, ideas), and only NOVA, Self-EvolveRec (tokens), VirtualMLE, and EvoRank match budgets across compared methods.
- **C8 baselines:** clearly tuned baselines only in VirtualMLE (Grid/BO-tuned) and EvoRank (Optuna, re-tuned per scale). Self-EvolveRec states untuned shared HPs; RecHarness starts from "cold-start" templates; industrial papers compare against production models (tuning n/a).
- **C9 isolation:** 2/17 state that the agent cannot see the test set or labels (VirtualMLE; EvoRank via leakage-guarded helpers). 3 partial (AgentX-Model fixed evaluation code; AutoLR frozen evaluation logic; RecHarness isolated workspace). 2 report actual metric gaming or leakage (RecEvolve batch-size reward hack; Co-Scientist "metric-winning bugs"). The rest are silent.
- **Online A/B:** 12/17 report online tests (Google, RecHarness, EvoRec, NOVA, AgentX, AgentX-Model, AutoLR, CORAL, AgenticRecTune, Sortify, GEARS, RecEvolve). Explicit significance or CIs: Google, EvoRec, NOVA, AgentX, AgenticRecTune, GEARS, CORAL (significance stated). Durations stated: RecHarness 7d, EvoRec 7d, NOVA 6d, AgentX 3 wk, Sortify 7d.
- **Code released:** 4/17 (Self-EvolveRec, RecHarness, VirtualMLE, EvoRank). All industrial systems are closed.
- **LLM not named:** 6/17 (RecHarness, AgentX, Auto-RecSys, CORAL, RecEvolve, EvoRank).

---

## Survey overlap (subsumption check)

### 2607.04433, "Autonomous Information Seeking: A Roadmap for Agentic Recommender Systems" (NUS, Poliba, RUC, USTC; v1)
- **Scope:** It builds a level-of-autonomy taxonomy around three paradigms: agent-assisted recommendation, agent-as-recommender (single- and multi-agent), and agent-as-user-simulator. It covers profile, memory, tool, workflow, and optimization components, and gives a long treatment of evaluation (LLM-as-judge, simulators, trace-level assessment). Its open challenges are lifelong user modeling, controllability, trust, privacy, and efficiency.
- **Code-level evolution of recommender models: not covered.** Its "Optimization and Adaptation" sections (4.2.5, 4.3.3) mean the agent refining its own reasoning or policy (self-reflection, DPO, distillation), not an agent changing a recommender's code or configuration. The only touch is one clause in the Sec. 3 task list: "leveraging agent as engineer to update the recommendation strategies lao2026agentx, wang2026self". The citation keys are unresolved in the text and correspond to AgentX (2606.26859) and Google 2602.10226. The bibliography also places 2602.10226 among the §4.3.3 multi-agent optimization citations. Self-EvolveRec, RecHarness, NOVA, EvoRec, and the others are absent. ("CORAL" in this survey is a different, retrieval-augmented recommender paper from KDD'24.)

### 2502.10050, "A Survey on LLM-powered Agents for Recommender Systems" (Tianjin Univ. + Du Xiaoman; v1, Feb 2025)
- **Scope:** It classifies methods as recommender-oriented (e.g., RecMind, MACRec), interaction-oriented (conversational, explainable), or simulation-oriented (Agent4Rec, AgentCF, RecAgent). It analyzes four agent modules (profile, memory, planning, action) and surveys datasets and evaluation metrics. Its future directions are architecture, evaluation, and security.
- **Code-level evolution of recommender models: not covered.** In every surveyed method the LLM agent is or serves the recommender. No AutoML, NAS, HPO, or agent-modifies-recommender-code work appears (Table 1 lists 23 methods, none of this type). It predates all 17 audited papers.

### 2507.21046, "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve…" (v4)
- **Scope:** It is a general survey of agents that evolve their own model, memory, tools, or architecture. It is organized by what to evolve, when (intra- vs inter-test-time), and how (reward-based, imitation, population/evolutionary), and covers evaluation goals (adaptivity, generalization, efficiency, safety). Its application domains are coding, GUI, finance, medical, and education.
- **Code-level evolution of recommender models: not covered.** Code self-modification appears only for the agent's *own* code or general algorithms (Darwin Gödel Machine, AlphaEvolve, Gödel Agent; Sec 3.4). ML engineering appears only as benchmarks (MLE-Bench). Recommendation appears twice: SOFT, self-optimized fine-tuning of an LLM-based recommender ("LLM-based recommender systems to learn from their own successful recommendation patterns", Sec 5.2), and a test-time-learning recommendation task. Neither is an agent evolving a recommender's code or configuration under an evaluation loop. None of the 17 audited papers is cited.

### 2508.07407, "A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems" (Glasgow, Sheffield, et al.; v2, Aug 2025)
- **Scope:** It proposes a feedback-loop framework (system inputs, agent system, environment, optimisers) and reviews optimization of foundation models, prompts, memory, tools, workflows, and multi-agent communication. Its domain-specific sections are biomedicine, programming, and finance (plus scientific research, games, computer use, and law). It closes with evaluation, safety ("Three Laws"), and ethics.
- **Code-level evolution of recommender models: not covered.** The full text contains zero occurrences of "recommend"/"recommender" (checked by full-text search of the PDF). The optimization target is always the agent system itself (prompts, workflows, topology), never an external recommender model. "AgentX" hits refer to EvoAgentX, the authors' own framework.

**Subsumption verdict:** none of the four surveys subsumes a survey on LLM-agent/automated-loop evolution of recommender configuration or code. The two RecSys-agent surveys treat the agent as the recommender, assistant, or simulator; the two self-evolving-agent surveys treat the agent's own components as the evolving object. Only the roadmap (2607.04433) acknowledges the "agent as engineer" direction, in one clause citing two papers.
