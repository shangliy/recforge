> **Note (2026-10-21, after review round 1):** the per-paper evidence below is the source; the count sections and
> summary tables in this file are superseded by `audit.csv`, which corrects 12 cells (see `../10-evolve/round-1.md`).

# Audit 2: self-evolving recommender papers (16 papers, full text read)

Source: arXiv HTML full text (all 16 had HTML versions), including appendices. "not stated" means the paper does not say. "no" means the paper says or shows that it was not done. Quotes are ≤25 words, with section/table references.

Rubric keys: C1 metric type · C2 per-round selection signal · C3 final candidate scored once on held-out test after search · C4 variance (seeds or repeated evolution runs) · C5 overfitting/transfer check · C6 null control · C7 budget accounting · C8 baseline strength · C9 isolation/leakage/hacking discussion.

---

## 1. RecEvolve, 2609.01622

- **Org:** Google (Mountain View), all 9 authors.
- **LLM:** not stated (roles named: Orchestrator, Ideator, Critic, Coding Agent).
- **Evolved:** code and config of a production two-tower retrieval model (loss/temperature, watch-time weighting, DCN-V2 user tower, gated dense layers, LR schedule).
- **Seed/base:** "latest production" two-tower retrieval model.
- **Datasets:** proprietary production logs (video watch-time implied).
- **C1:** NDCG, MRR, Recall@K (K = 1, 5, 50, 200) (§4). Ranking is over in-batch negatives (sampled), as the reward-hack explanation shows: "a smaller batch size mathematically reduces the difficulty of the retrieval task by providing fewer negative candidates per step" (§5.2).
- **C2:** offline metric threshold, "γ(Φ_NS) > τ + ϵ and γ(Φ_Aux) ≥ Threshold" (Alg. 1). Which data split is used: not stated. Short probes are "validated against full 2M-step offline training runs" (§4).
- **C3:** not stated.
- **C4:** no (single trajectory of 41 runs).
- **C5:** online A/B only. There is no val→test gap analysis. The paper flags an online-offline gap: offline "win-win" results versus online "complex trade-offs" (§6(3)).
- **C6:** no.
- **C7:** "41 distinct autonomous experiments in approximately 2 days, with each individual run requiring over 3 hours" on 5 threads, TPU (§5). Tokens and $: not stated.
- **C8:** the mature production model is the baseline. Strong, but it is the seed, not a tuned competitor.
- **C9:** yes. Reward hacking through batch size was caught by a human (§5.2). The short-horizon budget favoured aggressive LR (§5.3). Failed ideas were re-tested (§5.4).
- **Online A/B:** User Satisfaction +3.77%, Cold-Start −16.50% (faster discovery), Unique Content +7.44% (Table 2). Duration, traffic share, significance and guardrails: not stated.
- **Code:** not released.
- **Headline:** NDCG@50 0.4796 → 0.5751 (+19.9%) vs the production baseline (Table 1). Online User Satisfaction +3.77%.

## 2. Astar, 2608.27287

- **Org:** Alibaba Group (Lazada advertising) and Zhejiang University.
- **LLM:** a trained proposer (Qwen3 0.6B/4B/8B: mid-training on 112B tokens, SFT on 81.1M, GRPO on 8.06M). The code agent is "built on general-purpose LLMs such as Qwen or Claude" (§3.4). Frontier baselines: GPT-5.5, Claude-4.8-Opus, GLM-5.2, Kimi-K2.6, MiniMax-M2.7, DeepSeek V4 Pro, Qwen-3.7 Max.
- **Evolved:** evolution directions (architecture, loss, optimizer, data), implemented as code in an online recall model (generative retrieval, RQ-VAE SIDs).
- **Seed/base:** the Lazada ad recall model. Corpus: historical commits and experiment logs.
- **Datasets:** proprietary.
- **C1:** offline Hitrate@200 (whether full catalogue is used: not stated). Proposal success is the "actual loss decrease obtained from real execution" (§4.1).
- **C2:** training loss. s = (1−α)ℓ_T + α·mean_k + γ·σ_k computed from loss curves (Eq. 1). A learned reward model ranks candidates (proxy).
- **C3:** not stated.
- **C4:** no.
- **C5:** partial. The paper claims RM@k (proxy) and S@k (real) "exhibit high consistency" (Table 2). The reward model is recalibrated "when persistent discrepancies emerge between true outcomes and predictions" (§3.3, App. B, Alg. 1).
- **C6:** compared against human experts and 7 frontier LLMs given the same context, plus training-stage and data-design ablations. No random search or HPO.
- **C7:** "Θ(100) directions/week" vs "Θ(1)–Θ(10)" manually (Table 6). Training tokens are given above. GPU-hours and $ for the evolution loop: not stated.
- **C8:** "senior algorithm engineers" and untrained frontier LLMs. Neither is tuned to the task.
- **C9:** no discussion of leakage or hacking, beyond reward-model drift.
- **Online A/B:** July 1–5, 2026 (5 days), random traffic split. GMV +4.86%, ad revenue +1.82%, clicks +0.84%, orders +1.79%, "statistically significant at p < 0.05" (Table 5). Guardrails: not stated.
- **Code:** not released.
- **Headline:** Astar-8B S@1 0.6786 vs human 0.3229 and GPT-5.5 0.3071. 20 iterations over 2 weeks gave offline Hitrate@200 +23.6%.

## 3. A-MLE (Agentic ML Exploration for ads ranking), 2609.08248

- **Org:** Meta Platforms (Menlo Park, New York).
- **LLM:** a fixed agent loop run with Claude Sonnet (≥3.5, 4.0), Gemini 2.5 and GPT-5 families (§6.7).
- **Evolved:** training config and model-architecture code of ads ranking models (DCN, DIN, multi-tower), with a human checkpoint at every stage boundary.
- **Seed/base:** the rolling production baseline of each model. Anonymised models M₁, M₂, …, M*.
- **Datasets:** proprietary.
- **C1:** AUC/logloss family: "NE (Normalized Entropy) … rMSE for calibration" (§5). The headline is a "relative offline regression-error reduction" (Table 1).
- **C2:** "statistical significance against the rolling baseline", with an auto re-run "when within-run variance exceeds a threshold" (§4.4). Data split: not stated.
- **C3:** not stated.
- **C4:** a variance re-run rule exists (§4.4). The number of seeds behind the headline: not stated.
- **C5:** no.
- **C6:** cross-LLM swap with the loop held fixed, plus manual and semi-automated baselines. L1 bench: generic LLM 8%, generic ML agent 16%, A-MLE 68% (§6.4). No random search.
- **C7:** not quantified ("multiple times the productivity", §6.1).
- **C8:** production rolling baseline. Strong.
- **C9:** failure modes are listed (§6.9): single-seed promotion, baseline drift, hallucinated APIs, agents that "pretend to have completed tasks".
- **Online A/B:** none reported.
- **Code:** not released.
- **Headline:** +2.56% relative regression-error reduction on M* with +0.42% training QPS (Table 1).

## 4. AURA, 2609.16625

- **Org:** The Walt Disney Company (one author is now at Intuit). GenAIECommerce'26 workshop.
- **LLM:** Gemini 3 Flash (classification), Gemini 3.1 Pro (analysis), Claude Opus 4.6 (code suggestions). Judge panel: Opus 4.6, GPT-5.5, Gemini 3.1 Pro.
- **Evolved:** diagnosis-driven code proposals and PRs (a genre cross feature, candidate-aware attention). The AURA pipeline itself (prompts and architecture) was refined against a rubric. Training and A/B are not automated: "candidate training and A/B testing remain manual" (§6).
- **Seed/base:** production rankers on two streaming platforms.
- **Datasets:** Platform A, 96,801 sessions (18,901 BAD). Platform B, 101,594 sessions (4,154 BAD).
- **C1:** fix screening used offline AUC (click, watch-minute) and NDCG@10 deltas (Table 3).
- **C2:** pipeline changes were kept when more of 25 binary rubric criteria flipped BAD→GOOD, as judged by two LLMs (§4.1). The same rubric is used to select and to report.
- **C3:** not applicable / no (no held-out rubric set).
- **C4:** fix screening used "three independently-trained days" (Table 3). Rubric results: single.
- **C5:** no.
- **C6:** no. "comparisons against external baselines remain for future work" (§6).
- **C7:** $349.26 (A) and $252.85 (B) end-to-end. AURA's own part was $28.28 / $2.64. Runtime 1,554 / 965 min. "$5.38 per actionable finding" (§4.3, Table 5).
- **C8:** not applicable.
- **C9:** yes. Fabricated IDs, judge self-preference, taxonomy collapse (§4.1, §5).
- **Online A/B:** none.
- **Code:** not released.
- **Headline:** rubric scores 15/25 → 23/25 (A) and 17/25 → 24/25 (B). The two candidate fixes produced no gain beyond ±0.1% noise.

## 5. RecSys Factory, 2608.11241

- **Org:** FiT, Tencent (Shenzhen).
- **LLM:** underlying model not stated. Runs on Claude Code (Stop hooks, `.claude/skills`) with LangGraph Router and Analyzer LLM calls.
- **Evolved:** mostly operations. YAML overrides after failures, operator weight decision support, feature ablation. HITL approval is required for every change. This is not an evaluation-driven search loop.
- **Seed/base:** Spark-XGB CTR×CVR (Business A), a reranker (Business B), a CVR audience model (Business C).
- **Datasets:** proprietary telecom-payment and wealth-management data.
- **C1:** offline AUC, online CPM, replayed revenue.
- **C2:** operator approval through HITL cards.
- **C3:** not applicable.
- **C4:** no. Business B has 20 perturbation trials (Wilson lower bound 83.9%).
- **C5:** no.
- **C6:** no. Onboarding 14 → 3 days is "author-recalled … no controlled pre-platform baseline was tracked" (§1).
- **C7:** 1,624 CLI dispatches over 78 days (78.6% success). 16-run HITL pilot. 29 skills, 400 pitfalls.
- **C8:** rule-based ranking (A).
- **C9:** yes. Silent data defects were found (§6.1–6.3).
- **Online A/B:** gray rollout, Business A "+10–31% CPM lift in 4 out of 7 regional cohorts" with "no within-cohort CI, no BH correction" (§6). Duration: not stated.
- **Code:** not released.
- **Headline:** +10–31% CPM in 4/7 cohorts. Features compressed 7,881 → 221 dims at AUC +0.01%.

## 6. SR-Agent, 2607.17719

- **Org:** Kuaishou Technology (Beijing). RecSys workshop 2026.
- **LLM:** "All LLM-based components use Claude Sonnet 4.6" (§4.3).
- **Evolved:** post-ranking strategy configuration, through four typed bounded actions: relation threshold Δτ∈[−0.15, 0.15], suppression Δλ∈[−0.5, 0.5], exposure limits, taxonomy correction. The base ranker is frozen.
- **Seed/base:** manually configured production post-ranking strategies.
- **Datasets:** Kuaishou e-commerce traffic.
- **C1:** online only, plus a bad-case resolution rate on retest cases.
- **C2:** four gates. Bad-case retest on diagnosis-matched cases, historical-traffic replay, human verification, online A/B with rollback (§3.5).
- **C3:** not applicable (the online A/B is the final test).
- **C4:** no.
- **C5:** replay is used as a generality check before online. No numbers on replay versus online agreement.
- **C6:** no (control is the static manual strategies).
- **C7:** "one complete loop consumes 36 Million aggregate tokens" (§4.3). End-to-end 3–5 days versus 2–3 weeks.
- **C8:** manual production strategies.
- **C9:** a bounded action space: "The LLM cannot emit serving code, alter model objectives, target unauthorized scopes" (§3.5). Leakage and hacking are not discussed. Humans audit about 1% of outputs.
- **Online A/B:** one month (June 15–July 15, 2026), 2.5% of traffic, about 60M users. Orders +0.707%, GMV +0.461%, clicks +0.554%, browsing depth +0.342%, 7-day clicked categories +0.482% (Table 2). Significance: not stated. Guardrail: rollback on violation.
- **Code:** not released.
- **Headline:** orders +0.71%. UserSim found 142 bad cases (95% validated) vs 36 found manually, out of 500. Resolution rate 49.2% → 83.1% over 10 updates.

## 7. EvoSkillRec, 2609.34552

- **Org:** City University of Hong Kong, Kuaishou Technology, Xi'an Jiaotong University.
- **LLM:** GPT-5.5 through Codex CLI. RQ5 compares Claude Opus 4.8, GPT-5.6, DeepSeek-V4-Pro and GLM-5.2.
- **Evolved:** architecture, as a skill genome of 94 curated skills plus LLM-synthesised `nn.Module` code promoted into a Tier-2 library.
- **Seed/base:** DeepFM (CTR), Shared-Bottom (MTL), SAR-Net (MDL), RankMixer (QK-Video).
- **Datasets:** MovieLens-1M, Amazon Beauty and Books (CTR, chronological 70/10/20 split), Census-Income (MTL), Amazon and MovieLens MDL (random 80/10/10), QK-Video (394.6M / 50.1M / 48.6M rows).
- **C1:** AUC (logloss also logged).
- **C2:** validation AUC (validation AUC + MFU for co-evolution).
- **C3:** yes. "Candidate and checkpoint selection uses the corresponding validation metric; held-out test metrics are used for reporting, not selection" (§5.1). "Test metrics are never used for selection in either setting" (App. D.2).
- **C4:** no, single runs. "margins … on the order of 10⁻⁴ AUC, which a single evolution run cannot reliably separate from run-to-run variation" (§6).
- **C5:** yes, val→test. "Five candidates, P1–P5, lie on the Pareto front, but only P1 (round 19) retains both improvements on the test set" (§5.5, Table 4). Cross-task transfer untested (§6).
- **C6:** yes. NASRec (weight-sharing NAS) and OpenEvolve (LLM code evolution) at B = 200/250 training slots vs EvoSkillRec's 200 (App. D.5, Table 17), plus skill-only and code-only ablations. No random search.
- **C7:** 25 generations × 8 = 200 slots. "the experiments reported here cost roughly $7,000" (§6). 8× A800.
- **C8:** best of 7 CTR / 5 MTL / 11 MDL manual models in a shared trainer at fixed lr 1e-3. No per-baseline tuning stated.
- **C9:** generated modules are sandboxed (no file, network or subprocess access). Leakage is not discussed.
- **Online A/B:** none.
- **Code:** https://github.com/Xiaopengli1/EvoSkill-Rec
- **Headline:** test AUC +0.0001 to +0.0085 over the best baseline (Beauty 0.6845 vs OpenEvolve 0.6760). QK-Video P1: test AUC +1.7×10⁻⁴, MFU +0.044 pp.

## 8. RankEvolve (multi-agent harness for HSTU) / ExecML-HSTU, 2609.39551

- **Org:** Meta.
- **LLM:** Claude Code (Claude Opus 4.8) and Codex (GPT-5.6), both at maximum reasoning. OpenHands is supported.
- **Evolved:** training configs and code patches of HSTU, under an Executable Operating Protocol with human gates. The operator "also steered it".
- **Seed/base:** public HSTU, BASE and LARGE.
- **Datasets:** MovieLens-20M and -32M. Transfer replay on Foursquare-TKY/NYC, Gowalla, Yelp. ExecML: 96 HSTU and 96 LitGPT tasks.
- **C1:** full catalogue: "canonical full-test NDCG@10 (leave-one-out, full-corpus ranking over all held-out users)" (§3.1).
- **C2:** test. The persistent leaderboard is canonical full-test NDCG@10, and an LLM critic promotes combinations from it (§2.1, App. B). No separate validation split is described. A single passing mention of "validation NDCG@10" appears in App. I.1.
- **C3:** no. Reported values are "best checkpoints, not independent seeds" (Table 1), from the same test protocol used for the leaderboard.
- **C4:** no for HSTU ("checkpoint evaluations from one run are not independent seeds"). ExecML: 95% task-clustered CIs, McNemar, Holm, pre-registered.
- **C5:** the recipes were replayed on 4 datasets, one run each (Table 3). The ExecML composition effect transferred to LitGPT: +12.5, CI [3.0, 22.0].
- **C6:** ExecML: budget-matched one-pass, extended-budget, blind best-of-N and CC→CC→CC baselines. HSTU loop: none.
- **C7:** "~55 leaderboard entries across 49 experiment directories on 1–8 NVIDIA H200s; we report run counts rather than an unverifiable GPU-hour aggregate" (§3.1). ExecML $0.95–1.02 per task; plan-merge $2.40 per task.
- **C8:** published HSTU anchors (0.2098 LARGE, 0.1895 BASE). ML-32M uses internal reproductions.
- **C9:** yes, extensive (see the failure-mode section).
- **Online A/B:** none.
- **Code:** "will be released with the codebase" (App. B), not yet released.
- **Headline:** NDCG@10 0.2192 vs 0.2098 (+4.48%, LARGE) and 0.1948 vs 0.1895 (+2.80%, BASE). ExecML accuracy 62.5% vs 45.8% (+16.7 pts), silent critical-defect rate 10.4%.

## 9. Population Evolution / RMD-Bench, 2610.05950

- **Org:** Meta.
- **LLM:** GPT-5.5 at high reasoning on the AdaEvolve harness. §4.4 varies 5 harnesses and 4 proposers (including Claude Opus 5).
- **Evolved:** model and training code (sequence blocks, distributional heads, GRPO loss, LLM/VLM architecture and optimizer).
- **Seed/base:** FuXi-Linear (ranking), EGMN (watch-time), GRPO with Qwen2.5-Coder (RL), a Gemma-3-style 185M LLM, a Qwen3.5-style VLM (646M trainable).
- **Datasets:** ranking sources KuaiLive, KuaiRand-1K/Pure, KuaiRec, KuaiSAR. Watch-time sources CIKM16, KuaiRec, WeChat, KuaiRand-Pure/1K. Larger-scale: KuaiRand-27K. Transfer: KuaiVideo (CTR), VK-LSVD (MAE), LiveCodeBench-632.
- **C1:** full catalogue: "The benchmark evaluates full-catalog next-item ranking" (App. A.1). Fitness is (NDCG@10 + HR@10 + MRR)/3. MAE and AUC are used on transfer targets.
- **C2:** source fitness on the last-item target (a separate validation split for ranking is not stated). Promotion requires success on ≥2 of 4 peers, then larger-scale retraining. In Track B, full-target scores are withheld from the proposer.
- **C3:** no on the transfer targets: "Baseline hyperparameter and training-duration selection use the released test split, which is also used for final reporting" (App. F.1). The authors disclose this.
- **C4:** no. "we report one complete run per method–configuration" (App. B.5). Transfer candidates use 3 seeds.
- **C5:** yes, and it is central to the paper (see the failure-mode section).
- **C6:** yes. Standalone evolution S (same harness, no sharing) at matched source iterations. Direct full-target evolution at matched total GPU compute. Baselines calibrated by CMA-ES HPO (50 trials). No random search.
- **C7:** 5 searches × 100 iterations. GPU-hours given only as orders of magnitude: tens (watch-time), hundreds (ranking, RL), thousands (LLM, VLM). "Exact GPU-hour usage is restricted by policy" (App. B.5).
- **C8:** tuned. Per-instance baseline HPO before discovery (App. A.7).
- **C9:** test-split calibration is disclosed. Hacking and leakage by the agent are not discussed.
- **Online A/B:** none.
- **Code:** "will be made publicly available", not yet released.
- **Headline:** mean best local gain 7.01% → 8.97% (ranking) and 2.84% → 3.85% (watch-time) vs S. LLM full-target: best 2.48% vs 0.92%, 13 vs 0 successes. VLM: 8.78% vs 5.05% loss reduction. KuaiVideo AUC 74.46 vs reference 74.39.

## 10. From Trajectories to Evidence, 2608.05235

- **Org:** Kuaishou Technology (Beijing).
- **LLM:** GLM-5.2, self-hosted, for all components (generation, verification, controller).
- **Evolved:** paper-derived module adaptations (code) to production RankMixer, plus a registry of qualified Repair/Guard memory records.
- **Seed/base:** production RankMixer. 30 source papers.
- **Datasets:** proprietary production data ("four datasets"). Reproduction on Amazon Electronics (5 models).
- **C1:** AUC.
- **C2:** the per-round measured outcome versus the production baseline. Split: not stated.
- **C3:** not stated.
- **C4:** no. "The record-use diagnostic contains only eight single-run pairs" (Limitations).
- **C5:** partial. Memory-transfer audit (Table 6): 3 of 5 Apply pairs beneficial, 1 harmful.
- **C6:** no-memory vs memory paired arms (8 pairs). Controller compared with an always-Reject rule (79.7% vs 67.2% accuracy). No random search.
- **C7:** the budget is the count of dispatched machine experiments B. "we budget dispatched machine experiments rather than inference tokens" (§Exp.). Numbers: not stated. Up to 3 repair retries.
- **C8:** production baseline. Reproduced AUCs fall below the reported ones (InterFormer 0.8865 reported, 0.8522 reproduced), but the ordering is preserved (ρ = 1.0).
- **C9:** yes. Execution-validity gates, a same-model verifier caveat, withheld claims.
- **Online A/B:** live-streaming page duration +0.75%, user-growth net utility +6.34% (Table 8). Duration and guardrails: not stated. These are "candidate-level … rather than framework-level attribution".
- **Code:** not released.
- **Headline:** the non-monotonic trajectory finding (26/30 and 22/30, below) and two online lifts.

## 11. Spotify conversational recommendation self-improvement, 2609.30297

- **Org:** Spotify. RecSys'26.
- **LLM:** "top-tier frontier models", unnamed. The judge model differs from the agent model.
- **Evolved:** prompt artefacts (system prompt, few-shot examples, tool descriptions), edited by a coding agent.
- **Seed/base:** "a highly manually optimized prompt".
- **Datasets:** about 1,000 single- and multi-turn examples seeded from real and synthetic prompts, with a train/val/test split "propagated … to prevent leakage across splits at the seed level" (§3.1.2).
- **C1:** other. LLM-judge pass@1 (GREEN rate).
- **C2:** per mini-batch of 8: "re-run the evaluation with temperature τ = 0" on the judge (§3.2.5). Which split this uses: not stated.
- **C3:** yes, apparently. "+8% relative increase in pass@1 … on the full test set (statistically significant with p = 0.01 using a pairwise sign test)" (§4.2).
- **C4:** no. "In one run" (§4.2). The capability analysis averages n = 10 runs.
- **C5:** no. Mini-batching is used "To reduce the risk of overfitting" (§3.2.5).
- **C6:** no. ACE is mentioned qualitatively, with no numbers.
- **C7:** "typically runs for a few hours" (§4.2). Tokens and $: not stated.
- **C8:** the manually optimised prompt.
- **C9:** yes. Variance root causes (tool_failure, tool_variance, judge_variance) are separated so they do not cause spurious updates. Judge agrees with humans 97% of the time.
- **Online A/B:** two weeks, several markets, about 15M users. +14% listening, +5% WAU, −5% skip rate (§4.3). This A/B tests the whole agent experience against a refinement-only experience, not the self-improvement loop. Guardrails: not stated.
- **Code:** not released.
- **Headline:** pass@1 +8% relative on the test set.

## 12. AgentLTV, 2602.21634

- **Org:** Sichuan University, Harbin Institute of Technology, Sun Yat-sen University, City University of Hong Kong, VIVO, Xiangtan University.
- **LLM:** claude-sonnet-4.5, gpt-5.2, gemini-3-pro (§5.1.4).
- **Evolved:** full LTV pipeline programs (features, architecture, loss, calibration), searched by MCTS (PUCT with a Pareto reward) and then island EA.
- **Seed/base:** about 30 LTV method templates as roots (App. B).
- **Datasets:** proprietary mobile-game data, about 800k users over two periods, 8:1:1 split. Kaggle Acquire Valued Shoppers (1.8M), 8:1:1.
- **C1:** other: ER, Normalized Gini, Spearman, RMSE.
- **C2:** not stated ("Evaluate c on 𝒟 via Code Fixer", Algs. 1–2). Generated programs must "print(f"score = {score}")" (App. A.1). The final discovered program computes "S = ComputeScore(y_te, ŷ_te)" and returns S (App. D, Alg. 3).
- **C3:** not stated. It is doubtful, because the program's own score uses test data.
- **C4:** the ± in Table 2 is not explained. Single search run.
- **C5:** no.
- **C6:** module ablations only (w/o MCTS, w/o EA). No random or HPO baseline.
- **C7:** MCTS stops at 100 feasible programs (133 explored), EA adds 100 more (116 evaluated). 2× A100. Tokens and $: not stated.
- **C8:** 10 LTV models (ZILN, OptDist, HiLTV, …). Tuning: not stated.
- **C9:** no.
- **Online A/B:** none. An offline "analysis on real traffic logs from July 2025" of bucket metrics. The model is claimed "deployed online".
- **Code:** https://github.com/wuchaowei123/AgentLTV (data and discovered program).
- **Headline:** vs the strongest baseline, ER −41.26%, Gini +15.44%, Spearman +40.97%, RMSE −47.82%. Internal inconsistency: Table 3 gives full AgentLTV ER 0.594 / RMSE 141.09, while Table 2 gives 0.705 / 133.58 and 0.875 / 145.61.

## 13. AutoRecLab (demo), 2609.21863

- **Org:** University of Siegen and University of Göttingen.
- **LLM:** GPT-5.4-mini.
- **Evolved:** experiment code (research automation, not a recommender), by ε-greedy tree search over candidate programs.
- **Seed/base:** none. Prompt → requirements → prototype → full experiment.
- **Datasets:** MovieLens-1M, Amazon2018 Musical Instruments, Amazon2018 Video Games, via OmniRec.
- **C1:** generated experiments report NDCG@10 and Precision@10. Protocol: not stated.
- **C2:** an LLM-judged fraction of requirements met. "This score records requirement coverage and does not represent general confidence or guarantee correctness" (§3.2.2).
- **C3:** not applicable.
- **C4:** 9 runs (3 per dataset), reported individually (Table 1).
- **C5:** no.
- **C6:** no.
- **C7:** $0.76 for the demo, about $0.90–1.10 per run, runtimes up to 33.65 h, 8 prototype and 4 final nodes (Table 1).
- **C8:** not applicable.
- **C9:** partial. "some resulting analyses were not scientifically meaningful" (§4).
- **Online A/B:** none.
- **Code:** https://github.com/ISG-Siegen/AutoRecLab
- **Headline:** 8 of 9 runs produced bug-free code at about $1 per run.

## 14. Evolving Semantic Indexes for Generative Retrieval, 2610.28568

- **Org:** Santa Clara University and Coupang.
- **LLM:** gemma-4-31b-it as mutator (local vLLM on one H200), on AdaEvolve with 3 islands.
- **Evolved:** SID construction, collision handling, generator training objective, decoding, and the full pipeline (separate scopes).
- **Seed/base:** RQ-VAE with TIGER collision handling. Proxy: a 2-layer GPT-2 (~1M non-embedding parameters). Target: gemma-3-1b-pt.
- **Datasets:** NQ320K, MSMARCO300K, a proprietary multilingual e-commerce dataset (25,000 next-day test queries).
- **C1:** other. Document retrieval Recall@1/5/10/100 and MRR@10, with constrained beam search over the full corpus.
- **C2:** proxy Recall@100 on ℛ_feedback. "To keep search blind to test data, we randomly split each dataset’s original training relevance pairs into ℛ_proxy (two thirds) and ℛ_feedback (one third)" (§3).
- **C3:** yes. "All reported numbers are on the held-out test queries, which neither stage ever sees" (§4). "Test data is entirely unreachable to the mutator LLM" (§3).
- **C4:** target results are mean ± sd over 3 independent training runs (6 for e-commerce). Each scope has one search run. "Searches have different initializations and completed budgets" (Table 2).
- **C5:** yes, and it is central. Proxy–target ρ = 0.90 over 21 SID programs (Fig. 2b), plus transfer failures (see the failure-mode section).
- **C6:** no random search. Collision rate was rejected as a fitness because it is "too easy to hack" (§3).
- **C7:** proxy 20 min vs target 5 h per candidate. "100 candidate evaluations … 33 hours of proxy computation versus 500 hours of target evaluation" (§4). Up to 20 retries, 2 h execution cap.
- **C8:** the main comparison is Seed GR. BM25 and Contriever are shown "as references rather than competitors".
- **C9:** yes. Explicit isolation from test data; a collision-gate hackability argument.
- **Online A/B:** none.
- **Code:** not stated (no repository link).
- **Headline:** NQ R@1 55.82 → 59.28 and R@100 85.82 → 90.57. MSMARCO R@100 79.70 → 82.55. E-commerce R@100 gain over BM25 +49.01 → +50.66 pp.

## 15. Feedback-Grounded Policy Discovery for Generative Recommendation, 2607.27789

- **Org:** Kuaishou Technology, Huazhong Agricultural University, Fudan University, Tianjin University.
- **LLM:** Qwen3.5-122B-A10B (intent, policy and feedback agents). Qwen3-Embedding-8B.
- **Evolved:** per-user textual "policies" (K = 5 per round, R ≤ 2 rounds), selected by advantage and then distilled into a Policy Token. What evolves is LLM-teacher text, not recommender config or code.
- **Seed/base:** TIGER and LETTER backbones.
- **Datasets:** Amazon Beauty, Toys and Games, Sports and Outdoors. Leave-one-out (last item for test, second-to-last for validation).
- **C1:** R@5/10 and N@5/10, leave-one-out. Whether ranking is full or sampled: not explicitly stated (SID generation).
- **C2:** a proxy reward. Cosine similarity between the executor's predicted item profile and "the last item in the user’s training sequence", minus an intent-only baseline (Eq. 5). "Validation and test targets are never used for policy generation, evaluation, or refinement" (§3.3.3).
- **C3:** the split used to select hyperparameters (lr, epochs, λ "selected from" sets, App. A.2) is not stated.
- **C4:** "All experiments are repeated five times, and the average results are reported" (App. A.2). No standard deviations.
- **C5:** the similarity reward and Recall@10 rise together over rounds (Fig. 3). No transfer failure reported.
- **C6:** yes. Random Policy Selection gives R@10 0.0718, w/o evolution 0.0728, Target-as-Policy 0.0703, full model 0.0739 (Beauty/TIGER, Table 4).
- **C7:** not stated (8× A800, R = 2).
- **C8:** TIGER per the GRID config, LETTER with official code. Conventional baseline numbers follow prior settings.
- **C9:** target isolation stated (C2 quote). Hacking is not discussed.
- **Online A/B:** 7 days, 5% vs 5% of traffic, about 13.25M users and 1.61M items. Revenue +4.506%, ADVV +4.621%, "statistically significant at the 95% confidence level" (§4.4.2). Guardrails: not stated.
- **Code:** not released.
- **Headline:** Beauty TIGER R@10 0.0617 → 0.0739 (TIGER + Ours). Online revenue +4.5%.

## 16. RankEvolve (lexical retrieval), 2602.16932

- **Org:** Santa Clara University, an independent researcher, Walmart Global Tech.
- **LLM:** GPT-5.2 at temperature 0.85, on OpenEvolve.
- **Evolved:** the whole lexical ranking program (about 300 lines): document and query representation, scoring function, collection language model.
- **Seed/base:** BM25 (k1 = 0.9, b = 0.4, Pyserini defaults) and QL-Dirichlet (μ = 2000).
- **Datasets:** 12 datasets used during evolution (6 BEIR, 6 BRIGHT). 16 held out (8 BEIR, 6 BRIGHT, TREC DL 19/20).
- **C1:** other. nDCG@10 and Recall@100 over the full corpus. Fitness = 0.8·R@100 + 0.2·nDCG@10.
- **C2:** fitness on the 12 evolution datasets. Which query split is used: not stated.
- **C3:** yes, as cross-dataset hold-out. "The remaining 16 are held out entirely and used solely to test generalization" (§4.2).
- **C4:** no. One run per seed: 300 steps (BM25), 200 steps (QL).
- **C5:** yes. Seen vs unseen fitness per seed structure (Table 2). Significance by per-query paired t-test (Table 1).
- **C6:** partial. The "constrained" seed (hyperparameters plus predefined variants only, "analogous to automated grid search") at a 200-step budget gives seen 42.87, unseen 50.47, vs freeform 44.35 / 51.20 (Table 2).
- **C7:** 300 and 200 steps. Latency is reported (the evolved BM25 is 648.89 vs 56.72 ms/query). Tokens and $: not stated.
- **C8:** weak to moderate. Baselines use default Pyserini parameters: BM25, BM25+, BM25-adpt, QL-Dir, QL-JM.
- **C9:** no leakage discussion. The fitness weighting is said to "authorize the optimizer to sacrifice the pawn" (§4.3).
- **Online A/B:** none.
- **Code:** https://github.com/fangchenli/ranking-evolved (linked from "Code is available here").
- **Headline:** BRIGHT R@100 32.11 → 37.51 and nDCG@10 10.55 → 11.79 (unseen). TREC DL nDCG@10 62.16 → 64.57. BEIR nDCG@10 is slightly lower than BM25 (47.90 vs 48.16).

---

## Compact table (paper × C1–C9)

| # | Paper | C1 metric | C2 selection | C3 test once | C4 variance | C5 transfer/overfit | C6 null control | C7 budget | C8 baselines | C9 leakage/hacking |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RecEvolve | NDCG/MRR/Recall@K, in-batch (sampled) | offline metric threshold; split n.s. | n.s. | no | online A/B only | no | 41 runs, ~2 d, >3 h/run, 5 threads | production seed | **yes**: batch-size reward hack |
| 2 | Astar | Hitrate@200 (n.s.); train-loss success | train loss + reward-model proxy | n.s. | no | RM vs real "consistency"; RM recalibration | humans + 7 frontier LLMs; ablations | Θ(100) dirs/wk; training tokens | humans, untuned LLMs | RM drift only |
| 3 | A-MLE | NE / rMSE (logloss-type) | significance vs rolling baseline | n.s. | re-run rule; n n.s. | no | cross-LLM, manual, semi-auto | not quantified | production rolling | failure list (single-seed promotion) |
| 4 | AURA | AUC/NDCG@10 (screen); rubric | LLM-judged rubric (same for select/report) | n/a | 3 trained days | no | no | $349 / $253 per run | n/a | fabricated IDs, self-preference |
| 5 | RecSys Factory | AUC, CPM | human HITL | n/a | no | no | no | 1,624 dispatches / 78 d | rule baseline | silent data corruption found |
| 6 | SR-Agent | online + retest | 4-stage gate incl. replay + A/B | n/a (A/B) | no | replay pre-check | no | 36M tokens/loop | manual strategies | bounded action space |
| 7 | EvoSkillRec | AUC | validation AUC | **yes** | no (single runs, admitted) | **yes**: val→test Pareto | **NASRec + OpenEvolve**, ablations | 200 slots, ~$7k | untuned manual best | sandboxing only |
| 8 | RankEvolve-HSTU | **full-catalogue** NDCG@10 | full-test leaderboard | **no** | no (HSTU); CIs (ExecML) | 4-dataset replay; LitGPT | budget-matched (ExecML only) | ~55 runs, 1–8 H200, $/task | published anchors | **yes**: 3 leakage incidents |
| 9 | Population Evolution | **full-catalogue** rank; MAE; AUC | source fitness + peer promotion | **no** (transfer calibrated on test) | no (1 run) | **yes**: peer/large-scale failures | standalone S, Direct (matched) | orders of magnitude only | CMA-ES-tuned | test-split calibration disclosed |
| 10 | Traj→Evidence | AUC | per-round outcome; split n.s. | n.s. | no (single-run pairs) | memory-transfer audit | no-memory arm; always-Reject | experiment count, n.s. | production | validity gates; non-monotonic |
| 11 | Spotify | LLM-judge pass@1 | judge on mini-batches | yes (test, sign test) | no (1 run) | no | no | "a few hours" | manual prompt | variance root-cause filtering |
| 12 | AgentLTV | ER/Gini/Spearman/RMSE | n.s. (program prints score; final computes on test) | n.s. / doubtful | ± unexplained | no | ablations only | ~250 programs | 10 LTV models, tuning n.s. | no |
| 13 | AutoRecLab | n/a (requirement score) | LLM requirement coverage | n/a | 9 runs listed | no | no | ~$1/run | n/a | "not scientifically meaningful" |
| 14 | Semantic Indexes GR | Recall@K / MRR (doc retrieval) | proxy R@100 on train-split feedback | **yes** | 3 target trainings; 1 search | **yes**: proxy→target ρ, failures | no | 20 min vs 5 h per candidate | seed GR | **yes**: test isolation, hackable proxy |
| 15 | Policy Discovery GR | R/N@K leave-one-out | similarity to train last item | n.s. (hps) | 5 repeats, mean only | reward–recall trend | **random policy selection** | n.s. | TIGER/LETTER official | target isolation stated |
| 16 | RankEvolve-IR | nDCG@10 / R@100 | fitness on 12 datasets | yes (16 held-out datasets) | no | **yes**: seen vs unseen | constrained seed ≈ grid search | 300 / 200 steps | default params | no |

n.s. = not stated; n/a = not applicable.

### Counts (16 papers)
- **C1 full-catalogue recsys ranking stated explicitly:** 2 (RankEvolve-HSTU, Population Evolution). Another 2 retrieval papers use full-corpus document retrieval (GR indexes, RankEvolve-IR). Sampled/in-batch: 1 (RecEvolve, inferred from its own reward-hack explanation). AUC/logloss-type: 5 (A-MLE, EvoSkillRec, Traj→Evidence, AURA screening, RecSys Factory). Online only: 1 (SR-Agent). Other: 5.
- **C2 validation (or a train-split held-out feedback set) explicitly used for selection:** 3 (EvoSkillRec, GR indexes, Policy Discovery via the train last item). Test used for selection or calibration: 2 (RankEvolve-HSTU leaderboard; PE transfer calibration). Training loss: 1 (Astar). Not stated or unclear: about 6.
- **C3 explicit "selected on val, scored once on held-out test":** 4 (EvoSkillRec, GR indexes, RankEvolve-IR cross-dataset, Spotify). Explicit no: 2. Not stated or not applicable: 10.
- **C4 repeated evolution runs behind headline numbers:** 0 of 16. Repeated final-model training seeds only: 4 (GR indexes ×3, Policy Discovery ×5, PE transfer ×3, AURA ×3 days).
- **C5 a transfer or overfitting check with numbers:** 6 (EvoSkillRec, RankEvolve-HSTU, PE, GR indexes, RankEvolve-IR, Traj→Evidence).
- **C6 any null control:** 7 with some control. Only 3 are equal-budget non-LLM or non-sharing searches: EvoSkillRec (NASRec), PE (S and Direct at matched budget), RankEvolve-IR (constrained ≈ grid search). Policy Discovery has random selection. A random-search baseline: 0.
- **C7 dollar or GPU-hour numbers:** 4 ($: AURA, EvoSkillRec, AutoRecLab, RankEvolve-HSTU per task; GPU-hours partial for the GR paper). PE reports orders of magnitude only and calls exact figures policy-restricted.
- **Online A/B reported:** 7 (RecEvolve, Astar, SR-Agent, Spotify, Policy Discovery, Traj→Evidence; RecSys Factory gray rollout). Duration stated: 4 (Astar 5 d, SR-Agent 1 month, Spotify 2 wk, Policy Discovery 7 d). Significance stated: 2 (Astar, Policy Discovery).
- **Code released:** 4 (EvoSkillRec, AgentLTV, AutoRecLab, RankEvolve-IR). Promised: 2 (RankEvolve-HSTU, PE).

---

## Failure-mode evidence (quotes)

### Reward hacking and metric exploitation
- **RecEvolve §5.2:** "the system autonomously discovered that drastically reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics."
- **RecEvolve §5.2:** "Rather than improving the model’s underlying semantic representations, the system effectively ”hacked” the metric. Upon human detection of this exploit, a rollback was executed" (detected by a human, not by the harness).
- **RecEvolve §5.3:** "the system consistently favored highly aggressive learning rate schedules (e.g., up to 3.0) to maximize metric improvements within the limited horizon."
- **RecEvolve §5.4:** "the system occasionally revisited and re-tested architectural modifications that had already failed in earlier rounds."
- **RecEvolve §7:** "the system acts as an ultimate stress-tester for experimental infrastructure, actively seeking out and exploiting metric shortcuts."
- **GR indexes §3:** collision rate "cannot serve as the fitness function because it is too easy to hack … random assignments can produce few collisions and balanced code usage."
- **RankEvolve-IR §4.3:** "When we optimize a weighted sum, we implicitly authorize the optimizer to sacrifice the pawn to advance the queen."
- **RankEvolve-IR §6:** latency was visible but not part of the objective, and the best BM25* is "roughly 11× slower than the seed BM25."

### Silent leakage and silent defects
- **RankEvolve-HSTU App. H.3:** genre v1 "positives carried genre information that negatives did not; training loss collapsed to zero and eval appeared to spike (0.2163) before degrading."
- **RankEvolve-HSTU App. H.4:** "Apparent “gains” from naive multi-position eval were leakage (inflating 0.2192 to 0.2517/0.2577 at ignore_last_n=1/2)."
- **RankEvolve-HSTU Table 1 (iter 4):** DPO −35.9%: "All three used target-derived negatives (pre-fix mining) … A leak-free re-derivation … is neutral (Δ ≈ 0)."
- **RankEvolve-HSTU §3.1:** subset eval "ran ≈0.005–0.010 higher … without it, the system repeatedly chased phantom 0.005-scale “gains” from subset and checkpoint noise."
- **RankEvolve-HSTU App. I.1:** "the genre and DPO bugs surfaced not from a failed unit test but as anomalous metric trajectories."
- **RankEvolve-HSTU Abstract / Table 4:** a single-product one-pass silent critical-defect rate of 35.4%. The best budget-matched pair still has "a 10.4% silent critical-defect rate."
- **RankEvolve-HSTU §2.1 (pilot):** "ten runs received the whole procedure as one in-context playbook, and none was fully faithful … four stopped early, four skipped a gate."
- **RankEvolve-HSTU Limitations:** the case study "does not separate the agent’s contribution from the operator’s."
- **RecSys Factory §6.1:** a join bug "had silently corrupted all downstream training samples for the prior modeling cycle."
- **RecSys Factory §6.3:** upstream issues "would have produced a training run that succeeded engineeringly but silently corrupted labels or features."
- **RecSys Factory §6.2:** "one item’s effective weight 67× lower than its configured value."
- **AURA §5:** "904 fabricated UUIDs dressed up with real collection names to look plausible."
- **A-MLE §6.9:** "the agent sometimes promoted a candidate based on a single seed when within-run variance warranted re-running."
- **A-MLE §6.9:** "weaker base models hallucinate workflow identifiers and pretend to have completed tasks."

### Test-set use in selection or calibration
- **Population Evolution App. F.1:** "Baseline hyperparameter and training-duration selection use the released test split, which is also used for final reporting; no separate validation split is used."
- **RankEvolve-HSTU App. B:** "Canonical evaluation is full-test NDCG@10 over all held-out users," and this is the leaderboard the critic promotes from. No validation split is described.
- **AgentLTV App. D, Alg. 3:** the discovered program computes "S = ComputeScore(y_te, ŷ_te)" and returns it. Generated code must "print(f"score = {score}")" (App. A.1). Inference: search fitness may be test-based; the paper does not say otherwise.

### Non-monotonic trajectories
- **Traj→Evidence §Non-Monotonic:** "For 26 methods, at least one later valid round outperforms the first."
- **Traj→Evidence:** "for 22 methods, the last round falls below an earlier best, and later modifications sometimes partially or completely erase a previously observed gain."
- **Traj→Evidence:** "the final state of an adaptation trajectory is not necessarily its most useful experimental knowledge."
- **Traj→Evidence Controller:** "affirmative precision of 25%". Accuracy 67.2% is "below the 79.7% obtained by an always-Reject rule."
- **Traj→Evidence Bounded Self-Verification:** same-model verification "may leave correlated blind spots". Code alignment moved only 50% → 52%.
- **RecEvolve §5.6:** after Idea 40, "a continuous streak of reverted regressions" (ideation plateau).

### Proxy→target and source→target transfer failures
- **GR indexes §5.2:** "Once the generator’s training objective becomes mutable, the proxy becomes not only less informative but misleading."
- **GR indexes §5.2:** full-pipeline evolution "reaches a much higher proxy score of 62.85% while reducing target Recall@100 to 76.12%" (seed 85.82%).
- **GR indexes §5.2:** "all five improve proxy fitness over initialization while regressing on target recall … inversely ranked (Spearman ρ = −0.80, n = 5."
- **GR indexes §5.2:** for SID-only programs, proxy–target "Spearman ρ = 0.90" over 21 programs. Reliability depends on what is evolved.
- **Population Evolution §5.1:** "The KuaiLive ranking candidate improves KuaiRand-1K by 10.66% but declines by 0.79% at larger scale."
- **Population Evolution §5.1:** "All three pass peer screening, but only two retain positive gains at larger scale."
- **Population Evolution Table 2D:** larger-scale pass rate for the standalone baseline: ranking 11/60, watch-time 4/10, RL 0/15. PE: 18/60, 5/7, 2/12.
- **Population Evolution §4.2:** the RL candidates on held-out LiveCodeBench are "both below the unmodified reference mean of 23.26%."
- **Population Evolution Table 4:** Direct full-target LLM evolution produced 0 successes from 70 attempts.
- **EvoSkillRec §5.5:** "Five candidates, P1–P5, lie on the Pareto front, but only P1 (round 19) retains both improvements on the test set."
- **AURA §4.2:** both agent-proposed fixes "tracked the production baseline to within run-to-run noise on aggregate metrics (±0.1%" — the offline screen rejected them.
- **Traj→Evidence Table 6:** of 5 reference-Apply memory transfers, 3 helped and 1 hurt (HiFormer ΔAUC −0.0187).
- **RecEvolve §6(3):** offline evaluations "often yielded ”win-win” scenarios," while online "frequently exhibit complex trade-offs."

### Variance and statistical resolution admitted
- **EvoSkillRec §6:** "Some of the margins we report are on the order of 10⁻⁴ AUC, which a single evolution run cannot reliably separate from run-to-run variation."
- **Population Evolution App. B.5:** "we report one complete run per method–configuration."
- **RecSys Factory §6:** cohort lifts are "inter-cohort ranges … no within-cohort CI, no BH correction."
- **Spotify §4.2:** the +8% comes from "one run."
