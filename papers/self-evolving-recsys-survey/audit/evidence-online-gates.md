# Online-gate items (ab_* columns of audit.csv): verbatim evidence

Coded 2026-10-27 from the full text of the arXiv version in audit.csv's `version` column. Single-coded.

Each quote is verbatim and at most about 30 words. NS means the paper does not say.
`ab_ci`: Y = a CI or significance test is reported for the headline online numbers. "Significance-only" means significance is asserted for the headline online result but no interval or p-value is shown; such explicit claims of statistical significance (or a stated p-value threshold) are coded Y; an unqualified "significant" is not.

## Task 1: online A/B role and confirmation

**ling2026recharness (2607.29241v1)**: confirm / 1 / Y / N / na / Y
- Duration: "In a 7-day online A/B test on 10% of traffic (Table 6), the candidate improves ADVV ... by 2.084%, Revenue by 0.534%" (Online A/B Test).
- The candidate was chosen offline: "Offline, it improves production AUC by 0.09 %".
- CI: Table 6 gives point estimates only. The conclusion says "significant gains" with no test reported. "Significant" here is not a claim of statistical significance (the blind LLM check reads it the same way), so the code is N; NOVA, CORAL, AgenticRecTune and EvoPilot, coded Y (significance-only), state statistical significance or a p-value threshold explicitly. Counting RecHarness would make the count 8 of 19.

**wang2026selfevolving (2602.10226v3)**: select / NS / NS / Y / N / N
- Role: the Online Agent "uses the rank to decide which configurations merit promotion to live experiments and when to terminate unpromising experiments" (§4.2).
- Reward tuning relies "exclusively on the Online Agent's slow loop" (§5.3.2). "Two weeks" is the length of that tuning period, not the duration of an experiment, so duration is NS.
- CI: Tables 1–2 give 95% CIs: "statistically significant at the 95% confidence level".
- Correction: multiple testing is not discussed. Confirm: no re-test is described.

**mu2026evorec (2606.28368v1)**: confirm / 1 / Y / Y / na / Y
- The A/B ran 7 days with 20% of traffic per group: "both statistically significant under a two-sided test (p<0.05)" (§3.5).

**liu2026nova (2606.27243v3)**: confirm / 1 / Y / Y (significance-only) / na / Y
- "six-day, user-randomized A/B test on 5% of production traffic" (§5.7)
- "The best candidate found offline proceeds to online validation" (Fig. 1)
- "GMV gains are positive and statistically significant across all three objectives" (Table 4 text). No CI or p-value is shown.

**lao2026agentx (2606.26859v2)**: select / 100 launched / NS (only the 3-week program is stated) / N / N / N
- Gate: "A candidate is eligible for KEEP only when the primary objective clears both a minimum effect threshold and statistical significance" (§6.3).
- Funnel: "374 ideas → 106 passed → 100 launched → 10 LR" (Eq. 10, Table 5). The paper gives only the length of the whole deployment ("a three-week deployment", §8.1); the duration of each experiment is NS.
- Headline: "A cumulative gain of 0.561% in user app consumption time" and "Over RMB 100 million in annualized revenue" (§8.1, RQ3). Neither has a CI.
- **Recode (applied):** the first coding had "3wk+CI"; audit.csv now has duration NS and interval N (see CHANGELOG.md), because significance appears only as a gate on individual experiments. The headline has no CI.
- Correction: multiple testing across the 100 launches is not discussed.

**yang2026agentxmodel (2609.30001v1)**: confirm / 5 / NS / N / na / Y (caveat)
- The paper reports the "five latest Launch Reviews" (Table 6) and states: "Relative gains use coarse ranges".
- Selection: "larger offline AUC gains relative to run-to-run variability help prioritize candidates for online A/B tests" (§4.1.1).
- Caveat: the number of A/Bs that did not reach Launch Review is NS, and "latest five" is itself a filter.

**zhang2026autolr (2609.04871v1)**: confirm / 9 / NS / N / na / Y (caveat)
- "AutoLR does not directly optimize the online business metrics used in Launch Review." (§3.6)
- "Promising candidates are then advanced to online A/B tests, and those demonstrating robust gains are submitted to Launch Review" (abstract)
- Table 1 lists 9 Launch Review records with point values. The sums are "descriptive and are not pooled treatment effects". Search and user-growth each add one more LR.
- The paper discusses selection noise offline: "a one-run threshold crossing could update the experimental trunk without a protocol-matched confirmation run" (§5.3).

**azhar2026coral (2609.02730v1)**: select / 3 / NS / Y (significance-only) / N / N
- "policy improved over three successive rounds of the loop, each evaluated with an A/B experiment" (§5.1)
- The agent "reinforce[s] the changes that helped and reverse[s] those that did not" (§4.3).
- Table 1: "neutral denotes no statistically significant change". The cycle cadence is k=3 days; the A/B duration is not stated.

**wu2026agenticrectune (2604.26969v2)**: select / NS / NS / Y / N / N
- "treatment groups exposed to the parameter settings generated by AgenticRecTune" (§5.1)
- "After rounds of small traffic of iteration, AgenticRecTune succesfully search the better candidate" (§5.2.1)
- "Each experiment was run as a standard launch period to ensure statistical significance (evaluated at a p-value < 0.05)" (§5.1). No number of days is given.

**cheng2026sortify (2603.27765v3)**: both / 7 (Country A) + 23 (Country B) / Y / N / N / Y for Country B
- The loop is online: a YOLO loop of "wait 3.5h, pull A/B, pipeline, publish" (Fig. 8). "the YOLO loop ran 7 consecutive rounds (25 hours) in Exp-401838 and accumulated 23 rounds across two search phases in Country B".
- Confirmation: "The frozen R7 parameters were validated through a 7-day A/B test" (§4.8.4). It used 10% treatment vs 20% control, GMV/UU +4.15%.
- Caveat: the abstract headline is Country A "pushes GMV from -3.6% to +9.2% within 7 rounds", which is an in-loop round (N for that number).
- The paper picks R7 as the only round where GMV and Ads Revenue were both positive. It does not discuss the selection effect. Table 10 gives point estimates only.

**yun2026gears (2602.18640v4)**: select / NS (hundreds) / NS / N (headline) / N / P
- Gate: "Statistical-significance guard ... 95% confidence interval excludes zero" (§4). The gate is applied to each of hundreds of candidate policies, with no multiplicity correction.
- Table 3 (nine surfaces) gives point values. Table 5 (case study) gives 95% CIs.
- "Deploying the resulting cohort-targeted policy yields a statistically significant lift" (§6). No separate numbers are given, and the provenance of Table 3 is NS.
- Why `ab_ci` is N although the paper has an interval and a significance claim (decided after the r173 review): the interval "+0.832% ± 0.039" (§4.1) is the governance hook checking one candidate inside an illustrative session, i.e. the selection gate, which is not credited (as for AgentX above); the §6 claim is about the case-study deployment, which has no reported number. The headline online result, Table 3 (nine surfaces), gives point values with neither. NOVA, CORAL and EvoPilot are credited because their significance claims attach to the reported headline numbers.

**pan2026recevolve (2609.01622v1)**: confirm / 1 / NS / N / na / Y
- "the champion model generated by the system was deployed in a production A/B test on live user traffic" (§5.7)
- Table 2 gives point estimates: +3.77% satisfaction, -16.50% cold-start, +7.44% unique content.

**hu2026astar (2608.27287v1)**: confirm / 1 / Y / Y / na / Y
- "online A/B test from July 1 to July 5, 2026" (§4.6)
- "all performance gains being statistically significant at p<0.05" (Table 5)

**yang2026sragent (2607.17719v2)**: select / 10 updates / Y / N / N / P
- "Candidates that pass both offline stages proceed to strategy-owner review and controlled online A/B testing" (§3.5). An online guardrail violation triggers rollback.
- The headline is a one-month A/B (June 15–July 15, 2.5% traffic) comparing the agent with manual work: clicks +0.554%, GMV +0.461%, orders +0.707% (Table 2). No significance is reported.
- P: that system-level A/B is not used to pick arms, but the in-loop A/Bs ran in the same period.

**zhuang2026trajectories (2608.05235v1)**: confirm / 2 / NS / N / na / Y
- "Each candidate originated from a paper-derived intervention and passed artifact verification, machine evaluation, and claim qualification before online testing." (§Production cases)
- Table 8: page duration +0.75%, net growth utility +6.34%. No duration and no significance terms appear anywhere in the paper.
- "candidate-level online performance against frozen baselines rather than framework-level attribution" (Limitations)

**fu2026evopilot (2609.21257v1)**: confirm / 1 / Y / Y (significance-only) / na / Y
- "We use the online A/B only to establish the product relevance of the selected model." (§5.5)
- "The analysis covers a seven-day window and uses a regression-adjusted mean with outcomes from a separate seven-day pre-period." (§5.5)
- "the estimated relative GSRR effect was +0.66%, a statistically significant increase" (§5.5). No CI is shown.
- The model was selected offline (Table 3 chain: re-test, then matched-lineage ablation +3.20 pp, then online A/B).

**pilot2026 (2608.18637v2)**: select / NS / Y (5 days) / N / N → P (revised after the blind check; see Adjudication) / P
- "adoption requires a statistically conclusive whole-bucket comparison against the Champion" (§4.3)
- Designed confirmation: "Final confirmation evaluates the Champion against a single pre-registered test on D_confirm, a freshly collected, held-out sample gathered only after the Champion was fixed." (§3.4). No D_confirm result is reported.
- The headline is Table 7, "Outcome of PILOT at day 5, all five buckets". These are in-search gaps against B0, e.g. bucket 23 IPV +1.40%. "The task continued beyond the five-day window reported here" (§6.4).
- Rounds: Table 10 records 3 actions across 5 buckets. R_max is NS.
- Correction (first reading, superseded): decision rules are pre-registered for each round, but multiplicity across buckets and looks is not discussed. The blind check found the within-round joint calibration (§4.3) this reading missed; see Adjudication. The ROAM comparison "is before/after, not randomized" (§6.3.1).

**jiang2026abagent (2608.04625v1)**: select / 5 / NS / N / N / N
- Table 3: "Online A/B testing results throughout the iterative strategy-tuning process", covering Strategies 1–5.
- Table 5 (§5.6) GMV +4.829%, GPM +4.677%, OPM +0.841%, Clicks +0.370%, Orders +1.053%. These are identical to Strategy 5 in Table 3, so the headline is the selected round itself.
- The paper gives no duration and does not test significance. Significance is mentioned only as an engineer task in §1.

**zhang2026dmrl (2609.02170v1)**: select / NS / NS / N / N / P
- "Each edited skill S_i is then executed by task agent, which instantiates the corresponding parameter intervention and evaluates it through online A/B experiment." (§3)
- Each DRPO iteration samples 8 rollouts; the number of iterations is NS.
- "long-term metrics include AUD@7d, PES@7d and LTV, measured over a 7-day horizon" (§5.1.3)
- CUPED is used for variance reduction. No CI or significance is reported.
- P: "experiments in different tables are conducted during non-overlapping time windows" (§5.1.3). Whether these windows are separate from the RL training rollouts is NS.

## Task 2: DMRL LTV across tables

**Result: the figure in the draft holds once Tables 3 and 4 are included.**

Default configuration: "Unless otherwise specified, we instantiate the optimizer with Qwen3-8B and sample 8 rollouts in DRPO iteration." (§5.1.2)

LTV for the full DMRL configuration in each table:

| Table | Row | LTV |
|---|---|---|
| Table 2 (main) | DMRL (DRPO+LRP) | +0.052% |
| Table 3 (LRP ablation) | full "LRP" | +0.042% |
| Table 4 (DRPO ablation) | full "DRPO" | +0.021% |
| Table 5 | Two-stage | +0.052% |
| Table 6 | Qwen3-8B | +0.064% |
| Table 7 | 8 rollouts | +0.050% |

- Table 3 text: "the full LRP model achieves the best overall LTV improvement".
- Table 4 text: "DRPO achieves the highest LTV of +0.021% among all variants".
- Range: +0.021 to +0.064, a spread of 0.043 pp.
- The main-table lead over the best baseline (LRP+SkillOpt, +0.024%) is 0.028 pp: "DRPO outperforms SAGE, SkillOpt, and SKILLRL by +0.101%, +0.028%, and +0.048%".
- An earlier check of this figure had missed Tables 3 and 4.
- Caveat 1: the paper does not label the full rows in Tables 3 and 4 as the default configuration; this is the coder's inference.
- Caveat 2: all five metrics in the Table 5 "Two-stage" row are identical to the Table 2 DMRL row (-0.020/+0.644/+0.082/+0.960/+0.052). This contradicts the claim that tables come from non-overlapping windows; it looks like a reused experiment. That leaves 5 distinct values, and the spread is unchanged.
- The paper itself says "All conclusions are restricted to within-table comparisons".

## Task 3: selection gate

| key | (a) what decides keep | (b) abstract headline | (c) stratum |
|---|---|---|---|
| mu2026evorec | Offline metric on unnamed data. Memory stores "metric_t the offline evaluation metric vector, and verdict_t ∈{success, fail, neutral}" (§2.4). The loop stops at T_max or after k rounds without improvement (§2.2). | offline ("up to 5.54% offline improvement") + online | offline |
| liu2026nova | Offline AUC (≥+0.10 pp; "+0.15 pp promotion threshold"). An LLM ranking ensemble picks which candidate to evaluate. The corpus is "one month" of production data; the eval split is unnamed. "The best candidate found offline proceeds to online validation". | offline (EPR) + online GMV | offline |
| yang2026agentxmodel | An LLM Research Agent decides, reading offline AUC. "Training and evaluation use the business data" (§2.1); the split is unnamed. Humans gate deployment. | offline (560/636 above baseline) + online ranges | offline |
| zhang2026autolr | Offline scalar s(T)=wᵀφ(m(T)) plus guardrails, under a "fixed offline evaluation contract defined by engineers" (§3.6). The data is unnamed. | online (9 LRs) + offline counts | offline |
| pan2026recevolve | Offline NDCG/MRR/Recall@K. Algorithm 1: "if γ(Φ_NS)>τ+ε and γ(Φ_Aux)≥Threshold then M*←M_cand ... Log KEEP" (else rollback). The eval data is unnamed. | offline (~20% NDCG) + online +3.77% | offline |
| hu2026astar | Offline: training loss z=1[s_cur<s_prev] (§3.3) and Hitrate@200. "the modified system undergoes training and offline evaluation, and successful changes are deployed to production" (§3.4). The data is unnamed. | offline (S@1, Hitrate +23.6%) + online | offline |
| gao2026amle | Offline significance against a rolling baseline, then human review. "the agent computes statistical significance against the rolling baseline ... At the end of an exploration round the agent produces a structured leaderboard of candidates" (§4.4). Human checkpoint at every stage (§4.6). The eval data is unnamed. The paper has no online A/B. | process/throughput; Table 1 is offline (+2.56% rel. regression error) | offline |
| zhuang2026trajectories | Offline AUC plus LLM-assisted qualification. "We retain the first, best, and last valid round and report their metric differences from the production baseline". Candidates passed "machine evaluation, and claim qualification before online testing". The split is unnamed. | process (non-monotonic trajectories) + an unquantified line on online lifts | offline |

## Task 4

**(a) pan2026recevolve, C1 candidate set.** The paper does **not state** the candidate set. It can only be inferred from the batch incident: "In a separate exploratory session ... reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics" and "Because the Two-Tower model utilizes in-batch negative sampling, a smaller batch size mathematically reduces the difficulty of the retrieval task by providing fewer negative …" (§5.2). The candidates are in-batch negatives, so the set size equals the batch size (8k, or 1k in the incident). This is inferred, not stated. *Released code: `sampled` (C1), taking the incident's statement of in-batch negative sampling as the evaluation's candidate set; the paper's footnote gives the reading under which the candidate set is not stated.*

**(b) li2026evoskillrec (2609.34552v1), C6.** The paper has a non-LLM search baseline, **NASRec**, plus OpenEvolve as an LLM baseline (App. D.5, Table 1).
- Space: fixed and task-specific.
  - CTR: "linear, FM, deep MLP, cross-network, AutoInt, and SENET-deep branches, with sum, gated, or concatenation-MLP fusion".
  - MTL: Shared-Bottom/MMoE/PLE.
  - MDL: Shared-Bottom/STAR/MMoE/PLE/SAR-Net.
- Budget: NASRec screens 2B architectures with a 3-epoch weight-sharing supernet, then trains B standalone models. B=250 on the MovieLens tasks and 200 on the others. EvoSkillRec gets 25×8=200 slots. "candidate budgets do not measure total search computation" (Table 17 text). Supernet training comes on top of B.
- Both methods select on validation AUC, and "test metrics are evaluated after candidate selection and do not guide search". Each candidate uses one seed (2022).
- Results: NASRec is below the best manual model on all six benchmarks (e.g. Beauty 0.6632 vs EvoSkillRec 0.6845). The margin over the best baseline (OpenEvolve on ML-1M) is +0.0001.

**(c) kim2026selfevolverec (2602.12612v2), C6.** The NAS/non-LLM baselines are AutoFIS, NASRec, AutoLossGen and DNS-Rec (§4, App. F.1). The LLM baselines are AlphaEvolve (via OpenEvolve) and DeepEvolve.
- Space: NS. The NAS search spaces are not described beyond the one-line descriptions of each method.
- Budget: "For NAS baselines, we configured the search epochs to 5 for AutoFIS and 1 for NASRec, following the hyper-parameter setting in NASRec". LLM frameworks get "maximum evolution iterations to 21" (App. D). Retraining is shared: emb 50, batch 128, lr 1e-3, up to 300 epochs, one A6000.
- No compute or wall-clock match is made between NAS and the LLM loop. The fixed 5M-token budget (App. H.2.4) applies only among the LLM frameworks. Self-EvolveRec takes about 19 min per iteration (App. H.2.1).

## Adjudication after the blind check (second-coder/online-gates-check.csv)

- PILOT `ab_correction` N → P: "When multiple Challengers run in parallel within the same round, statistical thresholds
  are jointly calibrated across the multi-arm comparison to control the overall error rate" (§4.3). This corrects across
  parallel arms within a round, not across rounds, so it is partial.
- DMRL `ab_duration` Y → NS (changed after a later review): the 7-day figure is the horizon of its long-term metrics
  (AUD@7d, PES@7d), not the length of an experiment, and no experiment duration is stated.
- GEARS: the legacy `online` column read `CI`, which describes the promotion gate; the headline (Table 3) has point
  values only, so it now reads `yes`, consistent with `ab_ci` = N.
- The other five disagreements (Google/YouTube, AgenticRecTune, SR-Agent and DMRL `ab_confirm`; PILOT `ab_role` select
  vs both) are N/P or select/both; the first coding is kept. Under either coding one online-selecting loop confirms its
  final candidate afresh; on correction the codings differ only on PILOT (Y in the blind coding, P here).
- AgentX `ab_duration` Y → NS (changed after a later review; both codings had Y): only the length of the whole
  deployment is given ("a three-week deployment", §8.1), not the duration of each experiment, as for Google's two-week
  tuning period. The legacy `online` column now reads `yes`.
- Agreement was 88 of 95 cells before this adjudication and 88 of 95 after it (DMRL's duration change adds one
  agreement, AgentX's removes one).
