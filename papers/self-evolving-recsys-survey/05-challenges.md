# Challenges, limitations, fallbacks

Evidence: `audit/evidence-part1.md` (17 systems, full text, quotes with section pointers). n = 17 incl. EvoRank (LTR).

## Limitations
| # | Limitation | Evidence | Type | Severity | Attacked by | Outcome |
|---|-----------|----------|------|----------|-------------|---------|
| L1 | **Selection on noise.** Hundreds of candidates are compared on one offline set without repeats; claimed gains are of the order of run-to-run noise. | C4: 12/17 report no variance; AgentX-Model σ≈0.001–0.002 AUC vs ">10⁻⁶ above baseline" (Tab. 4); AutoLR "noise calibration was disabled" (§5.3), KEEP = "one-run offline threshold crossing" (§3.6); EvoRank campaign 1 gains "almost entirely fitness noise" (§5) | fundamental (search ⇒ winner's curse) | blocking | EvoRank (transfer audit), AgentX KB "≥2 independent runs" | open; only EvoRank measures it |
| L2 | **No null control.** Whether the LLM proposer beats cheap search is untested. | C6: 10/17 none; AutoLR "does not establish superiority over random, greedy, or direct LLM-based routing" (§3.3); where run, null competitive: EvoRank random search transfers as well or better (p=0.03); AgentX-Model replay "Uniform Random's mean exceeds Fixed, Greedy, and Joint" (§4.5) | incidental (cheap to fix) | costly | VirtualMLE (grid/BO/OPRO), NOVA (Optuna-TPE), EvoRank | partial |
| L3 | **Test discipline unstated or violated.** | C2/C3: of 11 recommender papers with offline selection, 2 state test-once (RecHarness, VirtualMLE); 6 do not name the selection split; AI Co-Scientist selects and reports on the same set (Tab. 1) | incidental | blocking for offline claims | RecHarness, VirtualMLE, MLRC-Bench | partial |
| L4 | **Metric gaming / reward hacking by the agent.** | RecEvolve: "reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics" (§5.2), caught by humans; Co-Scientist "metric-winning bugs (e.g., silently increasing model size)" (Lesson 3); NOVA lists target leakage among silent failures; EvoRank audit found 3 target-encoding leakage bugs; Self-EvolveRec's agent can rewrite data loaders (§3.1.2) | fundamental (optimiser controls the code that produces the score) | blocking | NOVA gates, AutoLR preflight, AgentX-Model fixed eval code, RankEvolve cross-review, VirtualMLE immutable pipeline | open; isolation stated by 2/17 |
| L5 | **Sampled or unspecified ranking metrics.** | C1: 0/17 state full-catalogue ranking; 2 use 1+99 sampled (Self-EvolveRec, RecHarness); 3 LOO with candidate set unstated; pathology [krichene2020sampled] | incidental | costly | — | open |
| L6 | **Weak or untuned starting points.** | C8: tuned only in VirtualMLE, EvoRank; Self-EvolveRec "uniformly configured all recommender models… learning rate of 0.001" (App. D); RecHarness gains +85.85% on cold-start GRU4Rec vs +12.58% on HSTU; Co-Scientist's gain came from lowering an inherited LR; EvoRank: full-scale re-tuning "reverses that verdict" (§5) | incidental | costly | VirtualMLE, EvoRank | partial |
| L7 | **Incomparable budgets.** | C7: 16/17 report some unit — iterations, GPU-s, GPU-h, tokens, $, RMB, ideas; only 4 match budgets across compared methods | incidental | costly | NOVA (eval budget, not LLM cost), VirtualMLE | open |
| L8 | **Online A/B as the only safeguard, under-reported.** | 12/17 run A/B; durations stated in 5; AutoLR launch lifts "descriptive and are not pooled treatment effects" with no CIs; Sortify selected the frozen round on the same online signal, then re-tested 7 days (partial fix); repeated rounds = multiple testing (not discussed by any) | fundamental for industrial loops | costly | Sortify fresh A/B; AgentX CUPED/DiD | partial |
| L9 | **Closed, unreproducible evidence.** | 13/17 release no code; 6/17 do not name the LLM; all industrial data private | incidental (institutional) | costly | — | open |
| L10 | **Circular evaluation at the policy level (L4).** | simulators share the model family; Self-EvolveRec uses held-out simulators (§4.1) as mitigation; [xu2026stateretention] progress sits across generations | fundamental | costly | RecoWorld, τ-Rec verifiable rewards | partial |
| L11 | **Proxy→target transfer for components.** | to fill from audit2 (Evolving Semantic Indexes; Population Evolution: objective changes transfer poorly) | fundamental | costly | proxy screening + promotion | open |

## Counter-evidence to record honestly
- [roelofs2019metaanalysis]: across 120 Kaggle competitions, holdout reuse caused little overfitting. Differences to
  argue (not assume): Kaggle limits submissions and humans submit few, diverse models; agent loops evaluate
  10²–10³ correlated candidates against one split with no submission cap, and pick the max. EvoRank is the only
  direct measurement in this setting.
- Online A/B gates are strong evidence when designed well (randomised, pre-specified, CIs): industrial systems should
  be judged on A/B design quality, not offline hygiene.

## Fallbacks in the wild
| Method | When the assumption breaks | Fallback | Acknowledged? |
|---|---|---|---|
| Google/YouTube | offline proxy misaligned | slow loop of online A/B | yes |
| AgentX, NOVA, EvoRec, AutoLR | offline gain may be noise | human launch review + A/B | partly |
| RecEvolve, Co-Scientist | agent games the metric | humans inspect diffs | yes (as lessons) |
| RecHarness, AutoLR, NOVA | open-ended edits unsafe | restrict to human-defined edit arms / declared surfaces / templates | implicitly |
| Self-EvolveRec | offline metric ignores user value | LLM-simulator critiques | yes |
| Population Evolution, semantic indexes | full-scale evaluation too expensive | small proxy / subset screening | yes (transfer limits reported) |

## Live limitations (ranked by impact × tractability)
1. **L1+L2 selection on noise without null control** — highest impact (decides whether the field's gains exist),
   tractable (repeats + random search are cheap relative to LLM cost).
2. **L4 metric gaming** — high impact, needs structural isolation (the agent must not control evaluation code/data).
3. **L3/L5 test discipline and full ranking** — tractable immediately; a shared protocol fixes both.
4. **L7 budget comparability** — needed for any cross-evolver comparison.
5. **L11 proxy transfer for generative components** — open research problem.
