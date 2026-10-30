# Backward-citation recall check: self-evolving recsys survey

Date: 2026-10-27, after the 2026-10-22 search cut-off; the cited works predate the citing core papers, all of which were posted by the cut-off. Survey: `draft/paper.tex`. Corpus: the 27 rows with `set=core` in `audit/audit.csv`.

## Method

- **Papers checked: 27 of 27 core papers.** 22 came from the cached text. 5 were fetched from arxiv.org/html: 2606.03221 VirtualMLE, 2609.10922 Auto-RecSys, 2609.39551 RankEvolve-HSTU, 2610.05950 Population Evolution and 2609.30541 Amazon AutoResearch.
- For each paper, the related-work section was read and every 2025–2026 entry was pulled from its reference list.
- Each entry was matched by arXiv id and title against the survey's `refs.bib`, `manual.bib` and the `\cite` keys in paper.tex. These three files are not in the anonymous supplement, so the matching step cannot be rerun from it; the outcome for every entry is listed below.
- A cited work counts as **qualifying** if it plausibly meets inclusion criterion (i). That means an LLM or agent loop that proposes changes to a recommender's or ranker's config, features, code or components, and keeps or rejects them after evaluation, dated 2025–2026.
- Categories:
  - (a) core row
  - (b) comparison row
  - (c) named elsewhere in paper.tex: borderline, uncoded, not audited, or adjacent
  - (d) absent from paper.tex
- The (d) candidates were checked against their arXiv abstracts using the export.arxiv.org API.

## Qualifying cited systems

| # | System (arXiv) | Cat. | Cited by (audited core papers) |
|---|---|---|---|
| 1 | Self-EvolveRec (2602.12612) | a | AgenticRecTune, AgentX, SR-Agent, EvoSkillRec, RankEvolve-HSTU |
| 2 | Google/YouTube self-evolving recsys (2602.10226) | a | most core papers (≥15) |
| 3 | AgenticRecTune (2604.26969) | a | AgentX, NOVA, Trajectories, PILOT, DMRL, AutoLR |
| 4 | AgentX (2606.26859) | a | SR-Agent, RecHarness, PILOT, CORAL, AutoLR, AgentX-Model |
| 5 | NOVA (2606.27243) | a | RecHarness, Trajectories, PILOT, CORAL, AutoLR, AgentX-Model |
| 6 | EvoRec (2606.28368) | a | RecHarness, PILOT |
| 7 | Sortify (2603.27765) | a | VirtualMLE, EvoRec, RecHarness, PILOT |
| 8 | GEARS (2602.18640) | a | VirtualMLE, RecHarness |
| 9 | RecHarness (2607.29241) | a | AutoLR, AgentX-Model |
| 10 | PILOT (2608.18637) | a | AutoLR |
| 11 | CORAL (2609.02730) | a | AgentX-Model |
| 12 | Auto-RecSys (2609.10922) | a | AgentX-Model |
| 13 | AutoLR (2609.04871) | a | AgentX-Model |
| 14 | Trajectories (2608.05235) | a | AgentX-Model |
| 15 | RecEvolve (2609.01622) | a | AgentX-Model |
| 16 | Astar (2608.27287) | a | AgentX-Model |
| 17 | RankEvolve-IR (2602.16932) | b | RankEvolve-HSTU |
| 18 | Meta REA (blog, `meta2026rea`) | c (not audited) | NOVA, AutoLR, RankEvolve-HSTU |
| 19 | RecSys Factory (2608.11241) | c (borderline) | AgentX-Model |
| 20 | AutoRecLab (2609.21863) | c (borderline) | AgentX-Model |
| 21 | AgenticTagger (2602.05945) | c (uncoded) | AgenticRecTune, PILOT |
| 22 | AutoModel / AgenticRS-Architecture (2603.26085) | c (uncoded) | PILOT |
| 23 | MoFA, LLM-driven constraint-aware feature selection (2603.24979) | d (borderline) | CORAL |
| 24 | DualAgent-Rec, LLMs as orchestrators (2601.19121) | d (borderline, likely out) | AgenticRecTune |

Counts: a = 16, b = 1, c = 5, d = 2 (both borderline).

## Share of in-scope citation-network systems the screen found

This is a check within the citation network the screen itself drew on, run after the cut-off; it is not an independent recall estimate, and the paper reports recall as unmeasured.

- **Counting both (d) items as qualifying (lower bound):** 22 / 24 = **91.7%**. These counts describe the manuscript when the check was run; the two (d) systems were absent then and are now cited as borderline, so they are not evidence of a search miss in either version.
- **Counting MoFA only (the coder's judgement):** 22 / 23 = **95.7%**.
- **Counting neither (strict reading of the selection-rule criterion):** 22 / 22 = 100%.

## (d) judgements

- **2603.24979 MoFA (Zhou et al., Meta).** Borderline. An LLM proposes feature subsets and interaction terms for production ranking and value models. This is an L1/feature-level change, and it was validated in online experiments. However, the abstract describes a one-shot, reasoning-based selection with no automated keep/reject loop. MoFA was in `refs.bib` and `manual.bib` but not cited when this check was run; the paper now cites it in the recall check (§9) as one of the two absent systems.
- **2601.19121 DualAgent-Rec.** Probably does not qualify. An LLM coordinator splits the budget between an exploitation optimiser and an exploration optimiser that build constrained recommendation lists. It optimises the recommendations, not the recommender's config, code or components, which the survey's own scope excludes. It could still be mentioned as an exclusion example.

Cited (d) works checked and found **not qualifying**, because none targets a recommender:

| arXiv | Work | Cited by | Reason |
|---|---|---|---|
| 2601.04554 | "A/B Agent" user simulator (a different paper from the audited A/B Agent, 2608.04625) | AgentX, PILOT | A user simulator or evaluator, not a proposer |
| 2601.10657 | PACEvolve | AgenticRecTune, Population Evolution | General LLM evolutionary search |
| 2605.15871 | AIRA-Compose / AIRA-Design | Population Evolution | Agentic architecture search for language foundation models |
| 2608.08189 | Janus | Population Evolution | General algorithm–evaluator co-evolution |
| 2608.26530 | PILOT in the Loop (a different PILOT) | AgentX-Model | Live self-improvement of general agents |
| 2609.09646 | RobustSGPO | AgentX-Model | Harness evolution on the AgentX brainstorming workflow, not a recommender model |
| 2609.18094 | Agora | AgentX-Model | Collective auto-research on an LM weight-transfer task |
| 2609.14858 | Dream-RSI | AgentX-Model | General exploration-policy self-improvement |
| 2606.06473 | MLEvolve | AgentX, AgentX-Model | General MLE agent |
| 2502.18530 | IMPROVE | several | MLE agent for image-classification pipelines |

Other general ML/MLE agents in the reference lists, such as MLE-STAR, R&D-Agent, ML-Agent, AutoMind, ShinkaEvolve and AdaEvolve, fail for the same reason.

Agentic or LLM recommenders absent from the survey also appear in the lists. Examples: ChainRec 2602.10490, RecThinker 2603.09843, ReasonRec 2606.28357, RRCM 2605.07129, IDSS 2603.11399, and local-life agentic reasoning 2604.14051. None of these is a criterion-(i) loop. At most they are L4 or adjacent, so they are left out of the recall denominator.

Cited non-loop works that the survey already covers: hu2026rethinking 2603.26100 (cited by VirtualMLE and CORAL; CORAL's "Hu et al. 2026" is this blueprint, not Astar), RecPilot 2603.07605, MARS 2605.14401, SAGER, RecNet, AMEM4Rec, MemRec, AtomRec, AgentCF and RecoWorld.

## Caveats

- Reference parsing was heuristic. A few lists were only partly parsed, so a small number of citations may have been missed. The related-work prose was read as a cross-check.
- Sortify cites no 2025–26 loop work. Astar and Amazon AutoResearch cite no recommender loops.
- The citation graph is dense among the late-2026 papers. AgentX-Model alone cites 9 core rows, which inflates the overlap in (a).
- Most (a) hits come from core papers citing each other. This is a closed-world check: it cannot find loops that no core paper cites.
