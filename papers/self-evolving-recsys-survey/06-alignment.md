# Alignment: survey claim vs limitations

## Matrix
| Limitation | Addressed by the survey? | How | Evidence in the paper |
|---|---|---|---|
| L1 selection on noise | direct (diagnosis) | audit C4/C5 + EvoRank, AgentX-Model noise figures | audit table; quoted figures |
| L2 no null control | direct (diagnosis + protocol) | audit C6; recommends equal-budget random search; recforge `random` evolver | audit; recforge |
| L3 test discipline | direct | audit C2/C3; sealed-test protocol | audit; recforge sessions |
| L4 metric gaming | direct (diagnosis), partial (remedy) | collects all reported incidents; isolation requirement; recforge train-view API (file-system isolation not built — say so) | quotes |
| L5 sampled metrics | direct | audit C1; full-ranking requirement | audit |
| L6 weak baselines | partial | audit C8; recommendation; recforge reproduced HSTU/SASRec baselines | audit |
| L7 budgets | partial | proposes a reporting card (trials, GPU-time, tokens/$) | proposal only |
| L8 online A/B | partial | separate A/B-quality criteria (duration, CIs, pre-registration, multiple rounds) | audit |
| L9 closed evidence | no (institutional) | catalogue of what is open | catalogue |
| L10/L11 | partial | discussed as open problems | cited papers |

## Subsumption check
- Searched: litsearch survey queries (02-related-work), WebSearch "survey self-evolving recommender 2026", citation
  graph of 2026 systems; full reads of the four nearest surveys (audit.md §Survey overlap).
- Closest: [lin2026roadmap] (agentic-RS roadmap, Jul 2026) — touches "agent as engineer" in one clause citing two
  papers; [gao2025selfevolvingsurvey], [fang2025selfevolvingsurvey] — self-evolving agents evolve their own components;
  [peng2025agentsurvey] — agent as recommender/simulator.
- Subsumes? **No.** None catalogues L1/L2 recommender evolution, and none audits evaluation practice.

## Diagnosis
Survey with an empirical (audit) core. The novelty risk is timing (the area is months old; another survey may appear),
not overlap. Mitigation: post to arXiv soon; keep the audit table versioned in the repo so it can be updated.

## Sharpened claim
For **LLM-driven evolution of recommender configuration and code (L1/L2)**, a **systematic audit on nine evaluation
criteria** shows that **selection on noise, missing null controls and unstated test discipline (L1–L3)** leave the
field unable to tell real gains from selection artefacts — 0/17 full-catalogue ranking, 2/11 test-once, 3/17 null
controls (competitive where run) — and specifies the **shared protocol** that would fix it, instantiated in recforge.

## Decision
keep, sharpened (no change of direction; no user confirmation needed by the skill's rule).
Dropped: claim 4 (self-evolution does not beat tuned baselines) — would need experiments, out of scope.
