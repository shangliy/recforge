# Methodology landscape: a taxonomy of self-evolving recommenders

Sources read in full: the 17 systems in `audit/evidence-part1.md` (2026-10-21); the rest in `audit/evidence-part2.md`.

## Two axes
**Axis 1 — the evolved object (what changes):**
| Level | Object | Examples |
|---|---|---|
| L0 search space | a point in a human-written space | AutoFIS, NASRec, AutoEmb, AutoLossGen |
| L1 configuration | hyperparameters, fusion weights, budgets, thresholds | VirtualMLE, Sortify, CORAL, AgenticRecTune, SR-Agent |
| L2 code | model/loss/training/feature code | Self-EvolveRec, RecHarness, Google/YouTube, EvoRec, NOVA, AgentX(-Model), AutoLR, RecEvolve, Co-Scientist, Auto-RecSys, EvoSkillRec, RankEvolve, Population Evolution |
| L3 component of a generative recommender | semantic-ID construction, item vocabularies, decoding | Evolving Semantic Indexes, AgenticTagger, self-improving tokenization |
| L4 policy of an agentic recommender | prompts, memory, skills, LLM weights | RecMind, AgentCF(++), SAGER, RecNet, AtomRec, OneRec IPA, SPRec, Rec-R1, CoARS, RSIR |
| meta | the evolver itself | AgentX SGPO, Astar (learned direction proposer), Auto-RecSys playbooks, EvoRec skills |

**Axis 2 — the selection signal (what decides which change survives):**
| Signal | Examples | Main risk |
|---|---|---|
| S1 offline validation, separate test | RecHarness, VirtualMLE, Self-EvolveRec, EvoRank | adaptive overfitting of the validation set; sampled-metric artefacts |
| S2 offline held-out set also used for reporting | AI Co-Scientist (explicit), AgentX-Model best-of-rounds | selection bias reported as gain |
| S3 offline, split not stated | EvoRec, NOVA, AutoLR, Auto-RecSys, RecEvolve | unknown |
| S4 proxy model | Evolving Semantic Indexes (1M-param proxy), Population Evolution (small-subset screening) | proxy→target transfer |
| S5 online A/B | AgentX, CORAL, AgenticRecTune, Sortify, GEARS; second stage of most industrial systems | multiple testing across rounds; short windows; peeking |
| S6 self-generated (reflection, simulator, own samples) | L4 systems, RecoWorld, Self-EvolveRec's simulator critiques | circularity |

The cross-product is sparse: L2 systems use S1/S3/S5; L4 systems use S6; L3 uses S4. The taxonomy figure (Fig. 1)
places every system in this grid.

## Anatomy of an L1/L2 loop (shared mechanism)
1. **Proposer.** LLM(s) write a hypothesis + edit. Variants: bandit over edit arms (RecHarness: Thompson routing over
   human-defined arms, "jump-basin" arms), island/MAP-Elites (OpenEvolve-based Self-EvolveRec), research agent +
   coding agent (EvoRec, AgentX-Model, Auto-RecSys), council review (AutoLR), multi-model consensus (Co-Scientist:
   GPT-5.2 + Gemini 3 Pro + Claude Opus 4.5 vote), learned proposer (Astar, 8B).
2. **Verifier / gate before training.** Semantic-validity checks and forbidden patterns (NOVA, rejects target leakage
   among "silent failures"), engineering whitelists (AgentX), preflight that evaluation logic is unmodified (AutoLR),
   fixed platform evaluation code (AgentX-Model), cross-agent review (RankEvolve).
3. **Evaluator.** Offline training + metric; cost per trial from minutes (VirtualMLE) to hundreds of GPU-hours
   (Auto-RecSys).
4. **Memory.** Experiment logs, distilled skills (EvoRec, AgenticRecTune), cognition summaries transferable across
   datasets (VirtualMLE), knowledge bases requiring ≥2 independent runs (AgentX).
5. **Selection / promotion.** Best-val incumbent (RecHarness), KEEP ratchet into the trunk (AutoLR), best round per
   experiment (AgentX-Model), A/B significance + guardrails (AgentX, NOVA, EvoRec).
6. **Online gate.** 12/17 audited systems run A/B tests; durations 6 days–3 weeks where stated.

## Comparison (L1/L2, audited)
| System | Level | Proposer | Selection | Gate | Budget unit | Open |
|---|---|---|---|---|---|---|
| Self-EvolveRec | L2 | OpenEvolve/DeepEvolve-style + diagnosis tool + simulator critiques | val (sampled) | — | 21 iters / tokens | yes |
| RecHarness | L2 (arms) | Thompson routing | val (sampled), test once | isolated workspace | 43,200 GPU-s | yes |
| VirtualMLE | L1 | execute–reflect–memory | val, test once, test hidden | immutable data pipeline | trials, $ | yes |
| Google/YouTube | L1+L2 | Gemini personas | val loss → A/B | — | $20k / 6 months | no |
| EvoRec | L2 + skills | research + code agents | not stated → A/B | — | 50 iters | no |
| NOVA | L2 | verification-aware harness | offline AUC (split not stated) → A/B | validity checks | ≤10 rounds, ~$29/task | no |
| AgentX / -Model | L2 + meta | research lineages | A/B / best round AUC | whitelist, fixed eval code | 636 exps, 97.5M tokens (replay) | no |
| AutoLR | L1+L2 | council + explore/exploit | one-run KEEP | preflight | 1,586 evals, RMB 3–4/iter | no |
| RecEvolve | L2 | autonomous research loop | not stated | humans caught reward hack | 41 runs, 2 days | no |
| AI Co-Scientist | L2 | multi-LLM vote | held-out = report set | — | ~1,650 H20-h | no |
(L3/L4 rows and audit2 systems to be added.)

## Practical realities the papers bury
- Edit spaces are often human-curated (RecHarness arms, AutoLR declared edit surface, NOVA templates): "code-level"
  frequently means code inside a narrow, pre-approved region — closer to L0/L1 than the framing suggests.
- Run-to-run noise is comparable to claimed gains: AgentX-Model reports σ ≈ 0.001–0.002 AUC while counting any gain
  >10⁻⁶ as "above baseline"; AutoLR's KEEP threshold 10⁻³ ≈ the IQR of its deltas with noise calibration disabled.
- Baselines: Self-EvolveRec uses untuned shared hyperparameters; RecHarness "cold-start" templates (GRU4Rec avg HR@10
  0.2685); the largest headline gains are over these weak starts (+85.85% on GRU4Rec vs +12.58% on HSTU).
- 6/17 do not name the LLM; 13/17 release no code.

## Where recforge sits
Not a new evolver: an evaluation substrate for L1/L2 (and later L3) evolvers — selection signal S1 with the test
sealed by process separation (train-view API; file-system isolation not yet built), full-ranking metrics, equal-budget
random-search null, val→test gap per session. It occupies the "evaluation protocol" column that no row above fills
completely.
