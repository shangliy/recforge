# Idea: Self-evolving recommender systems — a survey

## Raw idea
User (2026-10-21): "可以把现在开源的已经有的 self-evolve 的推荐都放到这里，然后写一篇综述" … "我要写的是一个综述论文".
Choices: arXiv first (ACM two-column, ~12–20 pp), pure survey (no new experiments), recforge presented as the
companion open benchmark.

## Restatement
Survey the systems in which an automated proposer (mostly an LLM agent) changes a recommender — its search-space
choices, configuration, source code, or policy — under an evaluation loop; organise them by what is changed and
what signal selects among changes; and audit how they are evaluated.

## Context
- Problem: in 2026 about 15 code-level "self-evolving recommender" systems appeared within ten months, from
  academia (Self-EvolveRec, RecHarness, VirtualMLE) and industry (Google/YouTube, Meta REA, Alibaba EvoRec,
  AgentX, NOVA, NetEase AutoLR, ...). No survey covers them, and their results cannot be compared.
- Who is blocked: researchers who want to know which evolver works or whether reported gains are real;
  practitioners choosing a harness design.
- Why now: the area is new (first code-level system Feb 2026) and growing fast, and it inherits the recsys
  evaluation problems (sampled metrics, leakage, weak baselines) just as the optimiser — an agent running
  hundreds of trials — is best placed to exploit them.
- Venue: arXiv, ACM `acmart` sigconf two-column, 12–20 pages incl. refs. Later extension to TOIS / CSUR possible.
- Resources: literature only. recforge (github.com/shangliy/recforge) is cited as the companion benchmark; its
  existing features may be described, but this paper produces no new numbers.

## Claim candidates
| # | Claim | Ambition | Falsified if | Defensible? |
|---|-------|----------|--------------|-------------|
| 1 | We catalogue and classify self-evolving recommender work. | narrow | not falsifiable | yes, but it is a list, not a survey |
| 2 | A two-axis taxonomy (what is evolved × where the selection signal comes from) separates the field into families with distinct failure modes. | medium | families do not differ in failure modes, or many systems do not fit | yes |
| 3 | An evaluation audit of code- and configuration-level systems shows that their reported gains, as a body of evidence, are not yet shown to be real: most use sampled metrics or do not state which split drives selection, none reports a validation-to-test gap or an equal-budget random-search control, and no two share a protocol. | medium-high | a majority of audited systems report full-ranking metrics, validation-only selection, and a null control | **yes — primary** |
| 4 | Self-evolving recommenders do not yet beat well-tuned baselines. | high | needs experiments we chose not to run | no (out of scope) |

**Primary claim (3 + 2):** Self-evolving recommender systems can be organised by *what* the loop changes and *what
signal* selects among changes. Auditing the code- and configuration-level systems against eight evaluation
criteria shows that the field's evidence cannot yet distinguish genuine improvement from selection on noise,
sampled-metric artefacts, or weak baselines. A shared sealed-test, full-ranking, budget-accounted protocol is the
missing piece.

**Falsification condition:** this claim is wrong if, on the audited set, most systems already (a) use full-ranking
metrics, (b) select on validation only and touch test once, (c) report a val→test gap or seed spread, and (d) share
a protocol with at least one other system.

## Assumptions (attack surface)
1. The audit is fair to papers we did not read in full. — Mitigation: read the full text of every audited system;
   distinguish "not stated" from "absent"; invite corrections.
2. Online-A/B-gated industrial systems are not held to offline-hygiene criteria. — A/B tests are strong evidence;
   audit them on A/B criteria (duration, guardrails, multiple-testing) instead.
3. Selection overfitting is real at the trial counts used (20–600). — Evidence: EvoRank's transfer audit (LTR),
   adaptive data analysis, Kaggle leaderboard shake-ups. Needs citations.
4. Sampled metrics distort *evolution* outcomes, not only model comparisons. — Plausible from Krichene & Rendle;
   untested for evolution loops → stated as an open problem, not a finding.
5. recforge is not presented as validated evidence. — It has no evolver results yet; described as a proposed
   protocol plus tooling only.

## Scope
In: AutoML/NAS for recommenders (background); LLM agents that modify recommender configuration or code; agentic or
LLM recommenders whose policy, prompt, memory or weights improve through self-generated feedback (OneRec IPA,
SPRec, AgentCF, ...); general program-evolution and ML-engineering agents insofar as recsys systems build on them;
evaluation methodology.
Out: LLM-as-recommender without a self-improvement loop; conversational recommendation in general; online
learning / bandits as a field (mentioned only); hyperparameter-optimisation libraries.
Not claiming: that any system's numbers are wrong; that self-evolution does not work.

## Open questions for the user
- Author list and affiliation for the title block (placeholder until told).
- Whether recforge is named in the title/abstract or only in Section 7.
