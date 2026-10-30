# First verification pass: fact check of the first coding

Part 1 (fact check) of the first adversarial verification pass, run by LLM agents on 2026-10-21 and reviewed by the
authors, before `audit.csv` was first committed. The 12 cell corrections it led to are listed in 1b; later changes are in
`CHANGELOG.md`. Counts and row names refer to the corpus and draft at that date (22 core systems), not to the paper.
Part 2 (a review of the draft's writing) is not released.

> **Superseded verdicts.** Some verdicts below were later reversed. In particular, Population Evolution C2 (→ `NS` here) was set back to `test` by internal review before the second coding, and its C3 (→ `P` here) is now `N`; see `CHANGELOG.md` for every later change. Where this file and `audit.csv` differ, `audit.csv` is authoritative.

## Part 1. Fact check

### 1a. Counts: text vs `audit.csv` (`python3 audit/summarize.py`)

The script's output and every number in the abstract, §6 and F1–F8 **agree**. The numbers match the data. The disagreements are between the data and the evidence (1b), and in a few places where the text says more than the CSV codes.

| Text claim | CSV / script | Status |
|---|---|---|
| 22 core, 16 offline, 6 online, 5 comparison | 22 / 16 / 6 (c2=online) / 5 | match |
| Abstract and F1: 2 full-catalogue | c1 full = 2 | match |
| F1: 3 sampled, 3 LOO-unstated, 6 AUC, 6 online, 2 none | 3 / 3 / 6 / 6 / 2 | match (but see 1b #3, #4) |
| Abstract and F2: 8 NS, 2 test; F2: 5 val, 1 trainloss | 8 / 2 / 5 / 1 | match (but see 1b #1) |
| Abstract and F3: 3 test-once, 2 opposite, 11 NS | 3 / 2 / 11 | match |
| F4: none with spread (C4=Y is 0) | Y = 0, P = 5 | match (F4 names 4 of the 5 P cells; AgentX-Model is the fifth) |
| F5: 2 core with explicit held-out check | c5 Y = 2 | match |
| F6: 3 Y, 9 P, 10 N | 3 / 9 / 10 | match |
| Abstract: "Three systems report that their agent gamed the metric or leaked the target" | c9 gaming = 3 (RecEvolve, A-MLE, RankEvolve) | match, but A-MLE should not be in it (1b #6) |
| **F7: "Three core systems and two comparison points report gaming or leakage"** | comparison c9 = gaming for **one** row (AI Co-Scientist). EvoRank is coded `Y` | **mismatch.** The text counts EvoRank, the CSV does not. Either code EvoRank's three caught leakage bugs as a separate value or say "one comparison point (and EvoRank's audit caught three leakage bugs)". |
| F7: 1 Y, 6 P, 8 NS | 1 / 6 / 8 | match |
| F8: 2 tuned, 12 LLM cost, 4 code, 2 promised, 5 LLM unnamed | 2 / 12 / 4 / 2 / 5 | match. Note that "LLM cost" counts token counts as cost, e.g. Self-EvolveRec's token budget and SR-Agent's 36M tokens. Say "LLM tokens or cost". |
| Online: 15 / 7 durations / 8 CI | 15 / 7 / 8 | match |

**Stale evidence summaries.** The evidence files no longer agree with the CSV. `evidence-part1.md` "Counts (n = 17)" says "0/17 state full-catalogue ranking" and "LLM not named: 6/17". It codes RecEvolve C1 = LOO-NS and C9 = N, and RecHarness C8 = NS. `audit/README.md` says the CSV is backed by these files. Either regenerate the count sections or mark them "superseded by audit.csv". Otherwise a reader who checks a cell finds two answers. `05-challenges.md` also carries the wrong "112 Kaggle competitions" figure (see 1c #12).

### 1b. Coding errors found by checking the CSV against evidence and full text

| # | Cell | Problem | Source checked | Fix |
|---|---|---|---|---|
| 1 | **Population Evolution C2 = test, C3 = N** (F2, abstract "two select on test data") | **Wrong / unfair.** The quoted sentence is about **baseline calibration on the two transfer targets** (KuaiVideo, VK-LSVD), not candidate selection: "Each recommendation target uses one baseline-calibrated configuration shared by the reference and every candidate … Baseline hyperparameter and training-duration selection use the released test split" (App. F.1; Table 30 caption). Source-search fitness is R_rank on the last-item target of *source* instances. Promotion uses separate peer instances and KuaiRand-27K. Full-target outcomes are "withheld from proposal context". The paper cuts the quote so that it reads as candidate selection on test. | arXiv 2610.05950 HTML | **Superseded: the released codes are C2 `test`, C3 `N` (internal review; see CHANGELOG.md).** C2 → NS (source split not stated; reporting is on different instances). C3 → P. C9 → P (full-target outcomes withheld from the proposer). Abstract and F2 become "one selects candidates on its test leaderboard (RankEvolve), and one calibrates the shared baseline configuration of its transfer targets on their test split (Population Evolution)". |
| 2 | **RecEvolve C1 = sampled ("in-batch")** (F1: "RecEvolve's metric is computed against in-batch negatives, as its own reward-hacking incident shows") | **Unsupported.** The paper names in-batch negatives only for *training* ("the Two-Tower model utilizes in-batch negative sampling"). It never states the evaluation candidate set. Inferring the evaluation set from the batch-size hack is plausible but remains an inference, and the text states it as fact. | arXiv 2609.01622 | C1 → ranking-ns. F1: "RecEvolve does not state its evaluation candidate set; that shrinking the batch inflated its metrics suggests in-batch negatives." Counts: sampled 2, candidate-set-unstated 4. |
| 3 | **Astar C1 = ranking-ns, rendered "LOO?"** (Table 3 caption, F1 "Three report leave-one-out ranking metrics") | **Wrong.** Astar reports offline Hitrate@200 on Lazada's recall model. The paper never mentions leave-one-out. | arXiv 2608.27287 | Rename the category "ranking metric, candidate set not stated" and drop "leave-one-out" from F1 and the caption. |
| 4 | **Astar taxonomy cell S2/S3** | **Wrong axis.** Astar selects on training-loss curves plus a learned reward model, which is S4 (proxy) by the paper's own definitions. | evidence-part2 #2 | Move Astar to S4. |
| 5 | **NOVA C9 = NS** | **Inconsistent with the paper's own text.** §5 says NOVA "adds verification gates that reject recommender-invalid edits such as target leakage", and §7 credits NOVA's gates with closing part of the isolation gap. NOVA lists target leakage among "semantic silent failures" that verification rejects. | arXiv 2606.27243 | C9 → P. The same applies to AgentX ("Parameter changes must pass an engineering whitelist") → P. |
| 6 | **A-MLE C9 = gaming** (abstract "three systems … gamed the metric or leaked the target") | **Miscategorised.** A-MLE reports promotion on a single seed and weaker models that "pretend to have completed tasks". These are procedural and honesty failures, not metric gaming or target leakage. It also says "the auto re-run rule materially reduced this", which means the loop did notice. | arXiv 2609.08248 §6.9 | C9 → P (re-run rule; failure modes reported). The abstract count becomes two (RecEvolve, RankEvolve). Discuss A-MLE under "agent reliability" in F7. |
| 7 | **RecHarness C8 = untuned (shown as N)** | **"Not stated" treated as "not done".** The evidence says "Base tuning is not described". The paper calls Base "the cold-start baseline". Its Table 3 also lists "Paper" (published) numbers, so the comparison is not only against an untuned base. | arXiv 2607.29241 Table 3 | C8 → NS. Keep F8's point about the gap between the base and published numbers (avg HR@10 0.2685 base vs 0.4990 published for GRU4Rec). That point is stronger than "untuned". |
| 8 | **EvoSkillRec C8 = untuned** | Borderline. The evidence says "fixed lr 1e-3. No per-baseline tuning stated". | evidence-part2 #7 | → P ("shared trainer, fixed lr; tuning not described"). |
| 9 | **AgentX-Model org = "Kuaishou (deployment)"** (intro and §5 attribute it to Kuaishou) | **Unsupported.** The HTML gives no affiliation and never mentions Kuaishou. The evidence file itself says "Org: not stated". | arXiv 2609.30001 | Write "AgentX-Model, a successor of the Kuaishou-deployed AgentX", or drop it from the Kuaishou list. |
| 10 | **Auto-RecSys counted among the 16 offline loops and the 8 "do not say"** | It makes no accuracy claim (operational metrics only) and reports no model-quality numbers. Threats says the paper does "not treat a missing offline test split as a defect when no offline claim is made", but the counts do exactly that. | evidence-part1 #9 | Code C2/C3 as `na` for systems with no offline claim, and report n = 15. |
| 11 | **Google C4 = P and F4 title "Nobody repeats the evolution"** | **Factually wrong title.** Google runs "6 independent runs exploring 70 ideas each" with CIs (Table 4). That is repeated evolution with spread, though only for an ablation. | arXiv 2602.10226 §5.4 | Title: "No headline result is reported with its spread over repeated evolution sessions." |

### 1c. Specific claims (12 required; 22 checked; 14 against the original source)

| # | Claim in paper | Verified against | Verdict | Fix |
|---|---|---|---|---|
| 1 | Population Evolution "states that 'baseline hyperparameter and training-duration selection use the released test split…'" and so "selects on test data" (F2) | arXiv 2610.05950 App. F.1 | **Quote correct, use wrong.** It concerns baseline calibration on transfer targets. | See 1b #1. |
| 2 | PE: candidate +10.66% on a peer dataset, −0.79% at larger scale; two of three keep gains (F5) | arXiv 2610.05950 §5.1 | correct | Add PE's main result for balance: larger-scale pass rate 18/60 vs 11/60 for standalone search. |
| 3 | RankEvolve: multi-position eval inflated NDCG@10 0.2192 → 0.2577 (F7) | arXiv 2609.39551 | correct ("0.2517/0.2577 at ignore_last_n = 1/2") | Give both values. Note that the authors reasoned it out as leakage, and their one measured run gave ≈0.2190. It was not reported as a gain. |
| 4 | RankEvolve: best pair 10.4% silent critical-defect rate, single Claude Code pass 35.4% (F7) | arXiv 2609.39551 Table 4, abstract | correct (HSTU column, "CC, one pass") | none |
| 5 | RankEvolve and PE "also come from Meta" | arXiv 2609.39551 (all four authors Meta), evidence for PE | correct | none |
| 6 | RankEvolve's leaderboard is canonical full-test NDCG@10 (F2) | arXiv 2609.39551 | correct | none |
| 7 | F7 heading "the loop does not notice" | arXiv 2609.39551 App. I.1: the genre and DPO bugs "surfaced … as anomalous metric trajectories … that the next reasoner call could read off the leaderboard and act on" | **contradicted** for RankEvolve. A-MLE's re-run rule also "materially reduced" single-seed promotion. | Retitle: "Agents find shortcuts in the evaluation; humans or monitoring, not the acceptance rule, catch them." |
| 8 | AgentX-Model σ "0.001–0.002 AUC" and >10⁻⁶ criterion (F4) | arXiv 2609.30001 §4.1, Table 4 | **slightly wrong**: 0.001010–0.002208 | "0.0010–0.0022". |
| 9 | AgentX-Model "Uniform Random's mean exceeds Fixed, Greedy, and Joint" (F6) | arXiv 2609.30001 §4.5 | quote correct. What is randomised is **experiment selection in replay**, not edits. | Say so in F6. It also weakens the abstract's "none compares against random search" (#20). |
| 10 | AutoLR: single-run KEEP, calibration disabled, "KEEP ratchet" (F4) | arXiv 2609.04871 §2.3, §3.6, §5.3 | correct, but **AutoLR coined the term** ("We call this stateful amplification mechanism the KEEP ratchet") and analysed it. The draft presents it as a flaw the survey found. | "AutoLR itself identifies this risk and names it the 'KEEP ratchet' (§2.3)." |
| 11 | "none discusses multiple testing across the many rounds a loop runs" (Online gates) | arXiv 2609.04871 §2.3 discusses adaptive reuse and cites reusable holdouts, the Ladder and online false-discovery control | **wrong** | "none corrects for multiple testing across rounds; AutoLR discusses the problem but does not apply a correction." |
| 12 | Roelofs et al.: "a meta-analysis of 112 Kaggle competitions" (§3 and §6) | NeurIPS 2019 PDF: "over one hundred … competitions"; "We surveyed 120 competitions" | **wrong** (112 does not appear) | "120 Kaggle competitions". Fix 05-challenges.md as well. |
| 13 | Surveys of self-evolving agents "do not discuss recommendation" (§1) | arXiv 2507.21046 §5.2.2: SOFT "enable[s] LLM-based recommender systems to learn from their own successful recommendation patterns" | **wrong for [gao2025]**; correct for [fang2025] (0 hits, per evidence) | "… and mention recommendation at most in passing (one paragraph on self-optimised fine-tuning in [gao2025]; none in [fang2025])". |
| 14 | "Beel et al. call for … benchmarks to evaluate them; no such benchmark exists yet" (§1) | The paper itself: PE "introduces RMD-Bench", RankEvolve "introduces ExecML-HSTU"; §3 cites MLRC-Bench's recommendation task | **self-contradicted** | "No shared benchmark yet enforces sealed test, full-ranking evaluation and equal-budget null controls across evolvers; RMD-Bench and ExecML-HSTU each fix one setting." |
| 15 | RecEvolve batch-size quote; "a human caught it and rolled it back" (F7) | arXiv 2609.01622 §5.2: "Upon human detection of this exploit, a rollback was executed" | correct | none |
| 16 | RecEvolve offline "win-win" vs online trade-offs (§7) | arXiv 2609.01622 §6 | correct | none |
| 17 | RecHarness +85.85% over GRU4Rec, +12.58% over HSTU; 43,200 GPU-s; five backbones; three runs (§5, F4, F8) | arXiv 2607.29241 and evidence-part1 #2 | correct | none |
| 18 | Google: ~$20,000 over six months; Gemini personas; validation loss then A/B (§5) | arXiv 2602.10226 §5.5.2 | correct | none |
| 19 | NOVA rejects target leakage via verification gates (§5) | arXiv 2606.27243 §1 | correct. This contradicts NOVA's C9 = NS. | See 1b #5. |
| 20 | Abstract "none compares against random search" | evidence: RecHarness random arm routing (LLM still edits), AgentX-Model random selection in replay | **overclaim as worded** | "none runs an equal-budget random search over its own edit space". |
| 21 | MLGym `validate` returns test-set metrics during the session (§3) | arXiv 2502.14499 Table 2: "validates the current submission file and returns the metrics on the test set" | correct | none |
| 22 | MLRC-Bench: next-product-recommendation task; dev split only, best dev snapshot scored once on hidden test (§3) | arXiv 2504.09702 §3.1, Table 1 (KDD Cup 2023) | correct | none |
| 23 | Astar trains an 8B model on an advertising system's commit history (§5) | arXiv 2608.27287 | correct (0.6B/4B/8B; Lazada) | none |
| 24 | AutoLR "reviews proposals by an LLM council under a limited trial budget" (§5) | arXiv 2609.04871: "Multi-Expert Proposal Council"; "allocates a limited trial budget" | correct in substance | Use the paper's name: "a multi-expert proposal council". |
| 25 | Intro chronology: Google, Self-EvolveRec and RecHarness came first, "and within months, systems followed" | arXiv IDs: RecHarness is 2607 (July). GEARS (2602), Sortify (2603) and AgenticRecTune (2604) came earlier. | **misordered** | Drop RecHarness from the "first" sentence or remove the time claim. |

**Fact-check failures: 9.**
- Wrong: #12, #13, #14, #11, #25.
- Unsupported: RecEvolve in-batch (1b #2), AgentX-Model = Kuaishou (1b #9).
- Misused quote: PE test split (#1).
- Contradicted by the source: F7 "loop does not notice" (#7).

Minor: #8, the Astar "LOO" label (1b #3), and #20 (overclaim).

---

