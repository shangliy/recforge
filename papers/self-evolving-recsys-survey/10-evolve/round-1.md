# Round 1: adversarial review of `draft/paper.tex`

Reviewers: (A) senior RecSys PC member, (B) industrial ML lead whose system is audited, (C) reproducibility and statistics reviewer.
Inputs: `draft/paper.tex`, `audit/audit.csv`, `audit/summarize.py`, `audit/evidence-part{1,2}.md`, `05-challenges.md`, the recforge source tree, and the arXiv HTML of 12 papers plus the Roelofs et al. NeurIPS PDF, fetched 2026-10-21.
The paper was not edited.

---

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
| 1 | **Population Evolution C2 = test, C3 = N** (F2, abstract "two select on test data") | **Wrong / unfair.** The quoted sentence is about **baseline calibration on the two transfer targets** (KuaiVideo, VK-LSVD), not candidate selection: "Each recommendation target uses one baseline-calibrated configuration shared by the reference and every candidate … Baseline hyperparameter and training-duration selection use the released test split" (App. F.1; Table 30 caption). Source-search fitness is R_rank on the last-item target of *source* instances. Promotion uses separate peer instances and KuaiRand-27K. Full-target outcomes are "withheld from proposal context". The paper cuts the quote so that it reads as candidate selection on test. | arXiv 2610.05950 HTML | C2 → NS (source split not stated; reporting is on different instances). C3 → P. C9 → P (full-target outcomes withheld from the proposer). Abstract and F2 become "one selects candidates on its test leaderboard (RankEvolve), and one calibrates the shared baseline configuration of its transfer targets on their test split (Population Evolution)". |
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

## Part 2. Review

### Scorecard (1–5)

| Criterion | Score | One-line reason |
|---|---|---|
| Novelty vs existing surveys | **4** | No existing survey covers agent-driven evolution of recommender code. The audit with released verbatim evidence is new and valuable. The taxonomy is a modest contribution. |
| Correctness | **3** | Counts reproduce exactly from the CSV. However, ~9 coding cells disagree with the full text, and 5 factual sentences are wrong. Two of them (PE "selects on test", RecEvolve "in-batch") feed headline numbers in the abstract. |
| Fairness to audited authors | **2** | Industrial systems are counted against offline criteria the Threats section says should not apply. PE's disclosed baseline calibration is presented as test-set selection. AutoLR's self-identified "KEEP ratchet" is presented as a survey finding. A-MLE's disclosed failure list is counted as gaming. Several "not stated" cells read as defects in headings ("Test-once is rare", "Nobody repeats"). |
| Clarity | **4** | Tight, well organised, good tables. The 12-column audit table needs a legend for P per criterion, since P means different things in C4, C5 and C6. |
| Completeness of coverage | **3** | Meta REA appears in the taxonomy and intro, but it is neither audited nor listed as borderline, and it is a blog post. Policy Discovery (2607.27789, which has a random-selection control) was read but is used only in L3. The search covers arXiv only, with no ACM DL, KDD/RecSys 2026 proceedings or industry-blog sweep, although industrial loops are often first described in blogs. |
| Usefulness of the reporting standard | **4** | R1–R9 are concrete and checkable. Weaknesses: R4's "≥3 seeds" cannot estimate a spread; R5's "random search over the same edit space" is undefined for open-ended code edits; R9 lacks a correction rule for many online rounds and pre-registration of the final confirmation test. |

### Top 8 weaknesses, ordered by severity, with exact fixes

**W1. Population Evolution is miscoded as selecting on test, and this is in the abstract.** (Abstract; §6 F2, F3; Table 3; audit.csv.)
The quoted sentence covers shared baseline calibration on the two transfer targets. The draft truncates the quote to make it look like candidate selection on test.
Fix: recode PE as C2 = NS, C3 = P, C9 = P and rerun `summarize.py`.
- Abstract: "… eight do not say which data split makes the decision, one selects candidates on its test leaderboard, and three state …".
- F2: replace the PE sentence with "Population Evolution calibrates the shared baseline configuration of its transfer targets on their released test split and says so (App. F.1); its candidates are selected on source instances and reported on others."

**W2. F7 and the abstract overstate gaming and "the loop does not notice".** (Abstract; §6 F7; Conclusion.)
A-MLE is not gaming. RankEvolve's leaderboard monitoring surfaced its leaks, the authors say so, and the multi-position inflation was reasoned out before it was reported. The CSV codes one comparison point, while the text says two.
Fix:
- Abstract: "Two systems report that their agent inflated the metric or leaked the target; in the clearest case a human caught it."
- F7 title: "Agents find shortcuts in the evaluation; humans and monitoring, not the acceptance rule, catch them."
- Move A-MLE to a sentence on agent reliability.
- Align the comparison count with the CSV, or code EvoRank's caught leaks as a separate value (`caught`).

**W3. "Not stated" is turned into "not done" in headings and in industrial counts, which contradicts the paper's own Threats §9.**
- F3 title "Test-once is rare" → "Test-once is rarely stated."
- F4 title "Nobody repeats the evolution" is wrong (Google runs 6 independent sessions with CIs) → "No headline result comes with its spread over repeated sessions."
- Conclusion: "test-once and repeated sessions are rare" → "… are rarely reported."
- RecHarness C8 → NS. EvoSkillRec C8 → P.
- Code C2/C3 as `na` for systems that make no offline claim (Auto-RecSys), and give the offline denominators with and without online-gated systems.
- Add one sentence to §6, Audited set: "For the 15 systems with online gates we read offline criteria as describing the screen, not the launch decision; their launch evidence is assessed under R9."

**W4. The transfer evidence is overstated.** (Abstract; F5 title; "Does selection really overfit?"; Conclusion.)
- EvoSkillRec's selected P1 *does* retain its gains.
- EvoRank's second campaign keeps ~70%.
- PE keeps 2 of 3, and its main result is improved transfer.
- "losses on transfer of a size comparable to the reported gains" is never quantified.

Fix:
- Abstract: "the few studies that measure transfer find that part of the selected gain, sometimes most of it, does not survive."
- F5 title: "Where transfer is measured, selected gains shrink, sometimes to zero."
- Delete "of a size comparable to the reported gains", or add a small table with gain at selection vs gain at transfer for EvoSkillRec, PE, EvoRank and GR indexes.

**W5. recforge claims go beyond what the code and repository support.** (§1 contribution 4; §3 Audit procedure; §7 recforge.)
- (a) "the evidence file is released with recforge": `papers/` is **untracked** in git and absent from `origin/master`, so nothing is released yet.
- (b) "A sealed test enforced by process separation": the sealed test metrics of every trial are written as `sessions/<name>/records/*.sealed` JSON under `RECFORGE_HOME` (`run.py` l.101–102). The `cli-agent` evolver runs Claude Code or Codex with `RECFORGE_HOME` set and full file-system access (`evolvers/cli_agent.py` l.65–75). The agent can therefore read every trial's test score and edit `session.json` (budget used, `final`). The draft discloses only the raw-data hole.
- (c) "Evolvers on equal terms" and "an open benchmark that implements its … protocol" (abstract) imply exercised evolvers, but the draft reports no evolver run, and the OpenEvolve adapter has never run end to end.

Fix: commit and push `audit/` before submission, or change the text to "will be released".
Replace the sealed-test bullet with: "*A sealed test at the API level.* Method code runs in its own process and receives only a training view … Sealed scores and session state are ordinary files, so an agent with file-system access can read test scores or alter the budget; until the planned container mode, the seal holds only against agents that use the API."
Abstract: "describe recforge, an open benchmark under development that implements the API side of its sealed-test, full-ranking, equal-budget protocol."

**W6. Several attributions and citations are wrong.** (§1, §3, §6.)
- "112" → "120" Kaggle competitions (twice).
- [gao2025] does mention recommendation (#13).
- "no such benchmark exists yet" contradicts RMD-Bench and ExecML-HSTU (#14).
- AgentX-Model is not affiliated with Kuaishou in its text (1b #9).
- RecEvolve's evaluation candidate set is not stated (1b #2).
- Astar is not leave-one-out (1b #3).
- AutoLR named the KEEP ratchet itself (#10).
- AutoLR does discuss multiple testing (#11).
- The chronology in §1 is misordered (#25).

Fix: apply the per-row fixes in 1c.

**W7. A single coder with no reliability estimate, and evidence files that disagree with the data.** (§3 Audit procedure; §9 Coding.)
Reviewer C: this round found ~9 miscoded cells among ~200, about 4–5%, and they cluster in the cells that drive the abstract (C2, C9). The evidence files contain superseded counts that contradict the CSV.
Fix:
- Have a second coder recode a random 30% of rows (at least all C1, C2 and C9 cells) and report Cohen's κ per criterion.
- Regenerate or delete the stale count sections in `evidence-part1/2.md`.
- Add a per-cell `evidence_ref` column to `audit.csv` so that every cell links to one quote.
- §9: "A second coder recoded N rows; agreement was κ = … ; disagreements were resolved by …".

**W8. The reporting standard is under-specified where the statistics matter.** (§7 Table 4.)
- R4 with 3 sessions gives a range, not a spread. Ask for "≥5 sessions, or report every session's final test score; give the median and range".
- R5: define the null for open-ended code edits, e.g. "random search over the same configuration or edit-arm space, or an LLM proposer whose candidates are accepted at random (no selection feedback), at equal trial and GPU budget".
- R9: add "a correction or false-discovery rule across rounds, and a fresh pre-registered confirmation experiment for the final candidate (as Sortify does)".
- R6: include proposer-training cost (Astar's 112B-token mid-training) when the proposer is learned.
- Taxonomy: move Astar to S4. Mark EvoRank and the AI Co-Scientist visibly as comparison points in Table 2, which is titled "self-evolving recommender systems". Explain why Meta REA, a blog post, appears in the taxonomy but not in the audit or the borderline list.

### Sentences that overclaim

1. Abstract: "none compares against random search" → "over its own edit space at equal budget".
2. Abstract and F5: "much of the selected gain does not survive" (W4).
3. Abstract: "Three systems report that their agent gamed the metric or leaked the target" (W2).
4. Abstract: "describe recforge, an open benchmark that implements its sealed-test … protocol" (W5).
5. §1: "no such benchmark exists yet" (#14).
6. §1: surveys of self-evolving agents "do not discuss recommendation" (#13).
7. F1: "RecEvolve's metric is computed against in-batch negatives" (1b #2).
8. F4 title: "Nobody repeats the evolution" (1b #11).
9. F7 title: "the loop does not notice" (#7).
10. Online gates: "none discusses multiple testing" (#11).
11. "Does selection really overfit?": "losses on transfer of a size comparable to the reported gains" (W4).
12. §7: "most of the problems are not hard to fix" and Conclusion "None of this is hard to report". These sit uneasily with §7's own admission that R4 multiplies industrial cost; say "most are cheap to report".
13. §7 recforge: "A sealed test enforced by process separation" (W5b).

### "Not stated" treated as "not done"

- F3 heading, F4 heading and the Conclusion wording (W3).
- RecHarness C8 shown as N where the evidence says "not described" (1b #7). EvoSkillRec C8 is the same (1b #8).
- Auto-RecSys: counted among "eight do not say which split" although it makes no offline claim (1b #10).
- The industrial C9 = NS cells (EvoRec, NOVA, AgentX, Google, Astar, Auto-RecSys) are summarised in F7 as "eight are silent" under a heading asserting the loop does not notice. NOVA and AgentX in fact describe gates or whitelists (1b #5).

### recforge claims the paper cannot back

- "the evidence file is released with recforge" (§3). Not committed or pushed.
- "sealed test enforced by process separation" (§7). Holds at the API level only; sealed scores and session state are readable and writable on disk by the `cli-agent` evolver.
- "Evolvers on equal terms … Each run reports the validation-to-test gap". The code exists (commit c68d568), but the paper reports no run and the OpenEvolve adapter is untested end to end. Say "implemented; not yet exercised in this paper".
- Abstract and contribution 4: "an open benchmark that implements its … equal-budget protocol". It is open (the GitHub repo answers 200). "Implements" should be qualified as in W5.

Backed by code, with no change needed: full-catalogue ranking with history removed, HR/NDCG@10/20 and MRR@100 (`eval.py`); a `PermissionError` for validation or test targets in the train view (`data/schema.py`); `finalize` reveals exactly one trial and closes the session (`evolve.py`); a random-search evolver (`evolvers/random_search.py`); the listed models and datasets (README).

### Minor

- Table 3 caption "S99" is wrong for in-batch metrics. Rename it to "Sampled".
- C4 = P lumps together three things: repeats without spread, repeats in ablation only, and a re-run rule. Split it, or define P per criterion in the caption.
- The "Twelve of 22 report some LLM cost" count includes token counts. Write "tokens or cost".
- The "about thirty such systems" count should be made explicit, e.g. 22 audited + 4 borderline + REA + Policy Discovery + 2 L3.
