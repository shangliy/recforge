> **How to read this file:** the authoritative code for every cell is the **Released codes (audit.csv)** line under each system's heading; a verdict in the body that differs from it is flagged with the released code. Count sections and summary tables are first-coding records, kept for provenance, and superseded.
>
> **Note:** copied verbatim from `../review/sweep-2026-10-22.md` §(b), the second literature sweep, so that every
> core and comparison row has its evidence under `audit/`. Where a cell here differs from `audit.csv`, the csv is
> authoritative; `CHANGELOG.md` lists every cell changed after the evidence was written.
>
> **Cells recoded after this file was written** (in order, from `CHANGELOG.md`; the verdict given below for these
> cells may be the earlier one, and the final code is the one in `audit.csv`):
> - EvoPilot: C2 `NS` → `test` (925fd50); C3 `NS` → `N` (925fd50); C9 `gaming` → `P` (925fd50)
> - Amazon AutoResearch: C9 `gaming` → `P` (925fd50)
> - PILOT: C5 `P` → `N` (4ae46ea)
> - DMRL: C5 `P` → `N` (4ae46ea); C8 `published` → `production` (4ae46ea)
> - PEAR (search): C9 `NS` → `P` (this release)

# Audit 3: rows added in the second sweep (2026-10-22, full text read)

## (b) Must-add core systems (audit candidates)

Recommendation for `audit/audit.csv`:

| Group | Systems |
|---|---|
| Add as **core** | b1 EvoPilot, b2 Amazon AutoResearch, b3 PILOT, b4 A/B Agent |
| Add as **core-borderline** (L4 + L1, online only) | b5 DMRL |
| Add as **comparison** | b6 Feedback Contract (methodology, public CTR/LTR), b7 PEAR (e-commerce search) |
| **Abstract-only**; list in the borderline note until full text is available | b8 MLE Agents, b9 Open-Ended Autonomous Model Research for RecSys |
| **Cite only** | DREAM, AgenticRS-EnsNAS (see c1) |

### b1. EvoPilot: *Verify, Don't Trust: Agentic Model Development for Video Discovery Retrieval at Scale*

> **Released codes (audit.csv):** C1 `ranking-ns` · C2 `test` · C3 `N` · C4 `P` · C5 `P` · C6 `N` · C8 `production` · C9 `P` · incident `Y`; recoded since first coding: C2, C3, C9 (see CHANGELOG.md). Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2609.21257, 2026-09-18.
- Hao Fu, Baiting Zhu, Minglei Chen, Yinjie Huang, Shuai Ding.
- **Meta Platforms**.
- Comment: "submitted to the KDD 2027 Applied Data Science Track".
- No code. Uses Claude Opus 4.7/4.8 and Claude Haiku.
- Read depth: full text.

**What it is**
- **Level:** L1 (serving and config: interaction head, candidate depth, task-score weights) and L2 (capacity and loss retrains).
- **Signal:** offline click hit-rate@K=3000 on held-out replay, gated by a human-gated, fail-closed pair verifier, followed by one online A/B.
- **Setting:** a 37-day campaign with 7 directions, 20 rounds and 68 configurations.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | ranking-ns (+online) | "primary selection metric is click hit-rate at depth K" (§5.1, Eq. 4). Pool rebuilt from servable inventory; size not stated. |
| C2 | NS ⟨recoded since this was written; released code: `test`; the second coder's evidence for it: test, "Offline evaluation replays held-out pairs ... Its primary selection metric is click hit-rate at depth K" (Sec 4.4), and the reported 3.20 pp comes from the same offline evaluation; no separate validation split.⟩ | One held-out replay set; no val/test distinction (§5.1). |
| C3 | NS offline; one online A/B ⟨recoded since this was written; released code: `N`; the second coder's evidence for it: test, "Offline evaluation replays held-out pairs ... Its primary selection metric is click hit-rate at depth K" (Sec 4.4), and the reported 3.20 pp comes from the same offline evaluation; no separate validation split.⟩ | "We use the online A/B only to establish the product relevance of the selected model." (§5.5) |
| C4 | P | "Two publications with the same model, configuration, and pinned data differed by 0.36 points" (§5.1). The seven directions "are not independent replicates". |
| C5 | P | Offline +3.20 pp, then online +0.66% GSRR. "Offline hit-rate and online GSRR have different populations and denominators" (§5.1, Table 6). |
| C6 | N | "The primitive autoresearch baseline is a retained incident, not a concurrent randomized workflow comparison" (§6). |
| C7 | 37 days, 20 rounds, 68 configs, 1,662 launches, 97.2 h orchestrator wall-clock for 9 rounds | "we do not extrapolate token cost or GPU occupancy" (§6; Tables 4, 7). |
| C8 | production | "the baseline left the head disabled" (§3.2). |
| C9 | **gaming** (+P) ⟨recoded since this was written; released code: `P`; the second coder's evidence for it: P, isolated workers, read-only variant specs, date-order guards (Sec 4.4-4.6); no statement that evaluation data is unreachable.⟩ | "a favorable result used an evaluation date inside the candidate model's training window, so the result was retracted" (§5.2). A date-order guard was added afterwards (Table 3). |
| online | significance asserted, no interval; 7 days (audit.csv: `7d+sig`) | "+0.66%, a statistically significant increase" (§5.5). |

**Reliability findings**
- **No-op edits:** "history rewriting removed the intended edit but left a plausible revision chain" (§5.2).
- **Evaluator drift:** "the aggregate metric changed meaning" (§5.2).
- **Funnel mismatch creating a false 22-pp drop:** "the control realized K_eff=3000 while the treatment realized K_eff=600" (§5.3).
- **Train/serve gap** from a seed identifier.
- **No CIs offline:** "we do not report inferential confidence intervals" (§5.1).

### b2. *AutoResearch at Production Scale: Failure Modes and a Multi-Agent Framework*

> **Released codes (audit.csv):** C1 `full` · C2 `test` · C3 `N` · C4 `P` · C5 `P` · C6 `N` · C8 `tuned` · C9 `P` · incident `Y`; recoded since first coding: C9 (see CHANGELOG.md). Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2609.30541, 2026-09-24.
- Aparajith Chandran, Juwon Kim, Saurav Jha, Pablo Castells, Florian Hottier.
- **Amazon, Books Core Recs Science**.
- **IEEE ICDM 2026 (Applied Track)**.
- No code. Uses Claude Sonnet 4.6 and Opus 4.6 via Bedrock.
- Read depth: full text.

**What it is**
- Two systems: System A (book-retrieval embeddings) and System B (RQ-VAE Semantic IDs).
- **System A, L2:** the agent rewrites the whole `train.py`.
- **System B, L1 + L3:** hyperparameter and encoder-architecture edits to a **semantic-ID tokenizer**.
- **Signal:** keep-if-better.
  - System A: Recall@6, kept if it beats the best by τ.
  - System B: weighted cluster coherence.
- **Scale:** 12 weeks, 220+ experiments.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | A: full (FAISS over the index); B: other (unsupervised coherence) | "the six nearest neighbors … retrieved via a FAISS IVF+Flat index" (§II-A). "weighted coherence is 0.5×L1+0.3×L2+0.2×L3" (§II-B). |
| C2 | **test** | Same held-out set for keep decisions and reporting: "retains modifications that improve a held-out scalar metric" (Abstract). Results are "Recall@6 on the held-out evaluation set" (§V-B). |
| C3 | N | Headline is the trajectory peak: "1.82× relative lift … on its peak evaluation date" (§V-A). |
| C4 | P | One model re-evaluated across 11 dates: "mean 6.18% ± 0.28 pp" (§V-E). No repeated sessions. |
| C5 | P | "the peak ~2.6σ above the across-date mean"; "Even the across-date mean preserves a 1.63× lift" (§V-A/E). |
| C6 | N | "the natural campaign transitions in Table V serve as the ablation" (§V-A). |
| C7 | 220+ iterations; 9–19 h multi-GPU per iteration; 12 weeks; "approximately 8 engineer-weeks" saved | Table I, §II-C, §VI. No total GPU-hours or tokens. |
| C8 | tuned + production | "hand-tuned baseline … product of four engineer-weeks … 3.79% Recall@6" (§II-A). Deployed baseline 2.82%. |
| C9 | **gaming** (+P: evaluator immutable) ⟨recoded since this was written; released code: `P`; the second coder's evidence for it: P, "an immutable evaluator that the agent observes but cannot modify" (Sec II); test access not ruled out.⟩ | "the agent discovered that maximizing codebook size trivially improves weighted coherence … the resulting hierarchy was unusable" (§III-E). |
| online | none | "online pilots … are underway" (§VI). |

**Reliability findings**
- Five named failure modes: infrastructure fragility, agent memory decay, search-direction stagnation, iteration-cost asymmetry, **metric fixation**.
- "the agent treats the metric as ground truth" (§III-E).
- **Index-coverage confound** (sub-agent's inference, not stated by the authors): an agent-added text fallback grew FAISS coverage from about 17% to the full catalogue. The candidate set behind Recall@6 therefore changed mid-campaign.
- **Note:** this is the first audited system that evolves a semantic-ID tokenizer, an L3 component, in production.

### b3. PILOT: *PILOT Technical Report* (Proactive Insight Learner for Online Tree-Experiments)

> **Released codes (audit.csv):** C1 `online` · C2 `online` · C3 `na` · C4 `N` · C5 `N` · C6 `N` · C8 `production` · C9 `P` · incident `N`; recoded since first coding: C5 (see CHANGELOG.md). Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2608.18637, v1 2026-08-19.
- "PILOT Team", 20 authors in alphabetical order. Core contributors: Jiuning Lin, Ruiquan Lan, Xiaodong Zhu.
- **Taobao & Tmall Group of Alibaba**, per the deployment text and an internship footnote.
- 42-page technical report. No code.
- Read depth: full text.

**What it is**
- **Level:** L1. Per-bucket 8-dimensional ranking-objective weight vectors, wrapped in user-segment PolicyTrees.
- **Proposers:** LLM roles (Manager, Search Planner, Memory Curator). They choose only from a deterministic "legal-command envelope".
- **Memory (L4-like):** a strategy and methodology store.
- **Signal:** online whole-bucket A/B against the Champion, with pre-registered criteria.
- **ROAM**, the comparison agent, is defined only inside this report. No separate paper was found on arXiv.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | online | "IPV is the north-star optimization target. PV and transaction count serve as critical guardrails" (§6.1). |
| C2 | online | "adoption requires a statistically conclusive whole-bucket comparison against the Champion" (§4.3). |
| C3 | na. Designed Y, but not reported | "Final confirmation evaluates the Champion against a single pre-registered test … The test runs once." (§3.4). No confirmation result in §6. |
| C4 | N | "We report the first five days." (§6.1). The 5 buckets are parallel arms. |
| C5 | P (designed, not reported) ⟨recoded since this was written; released code: `N`; the second coder's evidence for it: N, D_confirm is not reported.⟩ | "The data collected while searching … shaped the choice of Champion, so it cannot also serve as proof." (§3.4) |
| C6 | N | ROAM is also an LLM agent. A deterministic-only cell is planned but not run (§6.3.1, Table 8). |
| C7 | buckets × days | "Five experiment buckets (21–25) … +1.0% IPV within 7 days" (§6.1). Budget is in "bucket-days" (§4.1). |
| C8 | production + seed (in-house ROAM) | Fixed baseline bucket B0 (§6.1). |
| C9 | P | "LLM roles only choose among options these services already generated: they cannot invent a command, alter a statistical conclusion" (§2). |
| online | 5 days reported; no CI | Lifts are point estimates (Tables 7, 9). |

**Reliability findings**
- "The comparison in §6.2 is before/after, not randomized." (§6.3.1). Also: "suggestive rather than causal."
- The headline "+1.40% IPV" is a best-of-5-bucket maximum.
- Sub-agent reading: the top buckets 22 and 23 were "untouched" by the loop (Table 7).
- **Good-practice design to credit as stated design:** pre-registration, a single confirmation sample, and a rule forbidding "almost significant" readings. This is the only system in the corpus with a stated pre-registered test-once rule.

### b4. *A/B Agent: A Self-Evolving Agent for Strategy Iteration in Industrial A/B Testing*

> **Released codes (audit.csv):** C1 `online` · C2 `online` · C3 `na` · C4 `N` · C5 `N` · C6 `N` · C8 `production` · C9 `P` · incident `N`. Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2608.04625, 2026-08-05.
- Zhuohang Jiang, Yuxin Chen, Yongsen Pan, Zheng Hu, Wenqi Fan +4.
- **Kuaishou** and PolyU.
- No venue; the ACM template was left unfilled. No code.
- Read depth: full text.

**What it is**
- **Level:** L1 (recommendation strategy, parameters, objective weights, thresholds) plus an L4 hierarchical experience-tree memory.
- **Signal:** online A/B core and guardrail metrics. Node utility is given in Eq. 8.
- **Offline evaluation:** an LLM judge (GPT-5.5) scores 310 historical strategies.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | online (+ LLM-judge offline) | "GPT-5.5 serves as the automatic evaluator and assesses each strategy along two dimensions: Correctness … and Novelty" (§5.1). |
| C2 | online | "compares successive experiment variants, and generates the strategy … for the next testing round" (§3.3). |
| C3 | na | The final online number (+4.829% GMV, §5.6) is the trajectory's Strategy 5 (Table 3). |
| C4 | N | One trajectory. |
| C5 | N | Same figure reported in §5.3 and §5.6. |
| C6 | N | Baselines are LLMs and RAG variants only (§5.1). |
| C7 | not reported | 5 online rounds; duration and traffic not stated. |
| C8 | production / P | "Compared with the expert-designed strategy, Strategy 5 improves GMV and GPM by 2.150% and 2.941% points" (§5.3). |
| C9 | P | "rule-based validators check formatting, numerical ranges" (§4). |
| online | yes; no duration, no CI | §5.6, Table 5. |

**Note:** the LLM judge (GPT-5.5) is also one of the baselines.

### b5. DMRL: *Document-Mediated Reinforcement Learning for Skill Optimization in Advertising Recommendation* (core-borderline)

> **Released codes (audit.csv):** C1 `online` · C2 `online` · C3 `na` · C4 `N` · C5 `N` · C6 `N` · C8 `production` · C9 `P` · incident `N`; recoded since first coding: C5, C8 (see CHANGELOG.md). Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2609.02170, 2026-09-02.
- Wei Zhang, Hongji Li, Song Sun, Peng Yu, Xue Yang, Lei Zhao, Peng Jiang.
- **Kuaishou** and SJTU.
- No code.
- Read depth: full text.

**What it is**
- **Level:** L4 and L1.
  - A Qwen3-8B optimizer is RL-trained (DRPO) to edit a skill document.
  - A frozen Codex/GPT-5.5 task agent then sets whitelisted ad-system A/B parameters (L1).
- **Signal:** online A/B short-term outcomes, plus a learned long-term reward predictor (LRP, 7-day LTV).
- **Relation to the corpus:** it cites AgenticRecTune and extends it.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | online | AUD, PES and LTV at @1d/@7d (§5.1.3). |
| C2 | online + learned proxy | "The environment returns short-term outcomes and treatment–control comparison signals, while LRP estimates the corresponding long-term rewards" (§5.1.2). |
| C3 | na | |
| C4 | N | "experiments in different tables are conducted during non-overlapping time windows" (§5.1.3). |
| C5 | P ⟨recoded since this was written; released code: `N`; the second coder's evidence for it: N.⟩ | LRP-predicted vs ground-truth LTV (Fig. 4). This checks the proxy, not the selected candidates. |
| C6 | N | HPO is mentioned only as motivation (§1). |
| C7 | 8 rollouts per iteration | Iterations, traffic and tokens not stated. |
| C8 | published / P ⟨recoded since this was written; released code: `production`; the second coder's evidence for it: production, control runs the current best configuration.⟩ | SAGE, SkillOpt, SKILLRL, TFT, DelayAdapter. Their tuning is not stated. |
| C9 | P | "restricted to a predefined whitelist of parameters" (§5.1.2). The memory uses only matured outcomes, "preventing temporal information leakage" (§5.1.1). |
| online | yes; CUPED; no CI | Headline LTV +0.052% vs +0.024% for the best baseline (Table 2). |

**Reliability finding:** the same full DMRL run is reported as +0.052%, +0.064% and +0.050% in different time windows (Tables 2/5, 6, 7). That 0.02–0.04 pp spread is as large as most between-method gaps. (Superseded: with the full-model rows of the ablation Tables 3 and 4, +0.042% and +0.021%, the range is +0.021% to +0.064%; see `evidence-online-gates.md`.)

### b6. *An Explicit Feedback Contract for Iterative ML-Agent Harnesses* (comparison / methodology row)

> **Released codes (audit.csv):** C1 `auc` · C2 `val` · C3 `Y` · C4 `Y` · C5 `Y` · C6 `N` · C8 `seed` · C9 `Y` · incident `N`. Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2610.28798, 2026-10-20.
- Kehui Yao et al. (11 authors). **Walmart Global Tech**, Lehigh, Rutgers.
- No code.
- Read depth: full text.

**What it is**
- **Level:** L2. A Codex coding agent (GPT-5.6-Sol) edits models. Claude Sonnet 4.6 is a secondary backbone.
- **Signal:** a validation score. Under the contract it is released only when a candidate beats the champion by more than the paired standard error. The test set is quarantined.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | auc (CTR) / ranking-ns (MSLR NDCG@10) | "we report AUC"; "macro NDCG@10" (§5.1). |
| C2 | val | "It can reach V only through the harness" (§3). |
| C3 | Y | "A final model is named before any test feedback exists … H is then evaluated once" (§4.1). |
| C4 | Y (3 seeds real, 5 control) | The authors caveat: "three seeds on the real datasets cannot separate a small effect from none" (§6). |
| C5 | Y | The val–test gap is one of the three reported metrics (§5.1, Tables 2–5). |
| C6 | N under the rubric | It has a label-permuted **no-signal control**, "any apparent gain is selection noise by construction" (§5.1), but no non-LLM search arm. Suggest adding a codebook note, "null task", distinct from "null search". |
| C7 | ≤30 submissions | |
| C8 | seed | |
| C9 | Y | "V is reachable only by submitting a candidate … H is unreachable" (§4.1). |
| online | none | |

**Key numbers** (Table 2):

| Task | Gap, exact feedback | Gap, contract |
|---|---|---|
| Criteo | 0.0060 | 0.0055 |
| MSLR | 0.0134 | 0.0123 |
| No-signal control | 0.0163 | 0.0000 |

On the control, the exact-feedback agent "ended by reporting a gain of 0.0157" (Abstract).

### b7. PEAR: *Progressive Evidence-Based AutoResearch for Industrial Search Systems* (comparison: e-commerce search)

> **Released codes (audit.csv):** C1 `online` · C2 `online` · C3 `na` · C4 `P` · C5 `P` · C6 `N` · C8 `production` · C9 `P` · incident `N`; recoded since first coding: C9 (see CHANGELOG.md). Where a verdict below differs, this code is the released one; such verdicts are flagged, including changes made before the changelog starts.

**Bibliographic**
- arXiv 2609.35031, 2026-09-28.
- Yifan Wang, Shipeng Zhu, Fei Xiong, Yuqin Yang +5.
- "Global E-Commerce Agentic Search Team"; no company is named.
- No code; the LLM is not stated.
- Read depth: full text.

**What it is**
- **Level:** L1. "The search space is currently restricted to strategy-level parameters" (§8).
- **Signal:** a multi-fidelity ladder (shadow-traffic proxy, then rapid online, then decision-grade online). A candidate is promoted when its 95% CI lower bound is above 0.

**Audit codes**

| C | code | evidence |
|---|---|---|
| C1 | online (+ learned list-level proxy) | (§5.2) |
| C2 | online | "A candidate is promoted when the interval lies entirely above zero" (App. A). |
| C3 | na | The L4 A/B is both the gate and the reported result. |
| C4 | P | Replicated configurations only (Table 2). |
| C5 | P | For the two traced candidates, the shadow-traffic proxy effect is 16.8× and 28.5× the decision-grade online effect, and the rapid-online effect 5.7× and 13.8×, on different metrics per stage ("Order proxy +45.88% … Main Order/DAU +2.73%", Table 5). In Task B Phase I, 5 promoted candidates gave "No significant gain" (Table 3). |
| C6 | N | BO is a prompting principle only (§5.1). |
| C7 | rounds, groups, configs (e.g. 19 rounds, 133 groups, 20 configs) | Table 1. |
| C8 | production | (§6.2) |
| C9 | P ⟨recoded since this was written; released code: `P`; argued in second-coder/reconciliation.md or verification-pass-1.md⟩ | "the proposed change and supporting evidence undergo human review and require explicit human confirmation" (§9); the search space is "restricted to strategy-level parameters" (§8). Coded NS at first; changed to P by the third verification pass. |
| online | CI (p<0.05) | Table 6. |

**Note:** non-stationarity is the paper's explicit motivation: "transient gains may be mistaken for persistent improvements" (Abstract).

