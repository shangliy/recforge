# Refinement: contributions → evidence → falsifier (survey version)

## Contribution 1 — Scope and taxonomy
- **Challenge:** the term "self-evolving recommender" covers search-space AutoML, LLM code agents, generative-component
  search and agent memory updates; no survey separates them ([lin2026roadmap] covers one clause).
- **Solution:** two axes — evolved object (L0–L4 + meta) × selection signal (S1–S6); every surveyed system placed.
- **Evidence:** Table "taxonomy" with ~90 systems; Fig. 1 grid.
- **Falsified if:** many systems cannot be placed, or placement does not predict the evaluation risks in Sec. 6.

## Contribution 2 — Evaluation audit (the empirical core)
- **Challenge:** L1–L5 (stage 05).
- **Solution:** nine-criterion codebook (C1 metric … C9 isolation) applied to every L1/L2 system from full text, with
  verbatim evidence; codebook and per-paper evidence released in the repo.
- **Evidence:** audit table (17 + ~16 systems), counts, quoted failure incidents.
- **Falsified if:** a re-coder reading the same papers reaches materially different counts (we release evidence so this
  can be checked); or most systems satisfy C1–C6.

## Contribution 3 — Reporting standard and shared protocol
- **Challenge:** L6–L8, plus no shared benchmark.
- **Solution:** a reporting checklist (full ranking; selection split; test once; ≥3 repeated sessions; val→test gap;
  equal-budget null; budget card; isolation statement; A/B design) and its instantiation in recforge (what is built,
  what is not).
- **Falsified if:** the checklist cannot be met at reasonable cost — we estimate cost with published per-trial costs
  (e.g., VirtualMLE $1.5–4.8/session; EvoRank ~$10/run) rather than run experiments.

## Contribution 4 — Open problems
Proxy fidelity for generative components; isolation against metric gaming; budget-normalised comparison; circular
evaluation in policy-level loops; evolving the evolver (Astar, SGPO).

## Coverage check
| Contribution | Evidence | Falsifiable |
|---|---|---|
| C1 taxonomy | placement table | yes |
| C2 audit | per-paper evidence file | yes (re-coding) |
| C3 checklist + recforge | costs from papers; repo | yes |
| C4 open problems | citations | n/a (agenda) |

## Paper skeleton
- **Title candidates:**
  1. *Self-Evolving Recommender Systems: A Survey and an Evaluation Audit*
  2. *When Agents Engineer Recommenders: A Survey of Self-Evolving Recommender Systems and How They Are Evaluated*
  3. *Are Self-Evolving Recommenders Actually Improving? A Survey with an Evaluation Audit*
- Sections: 1 Intro · 2 Scope & method · 3 Background · 4 Taxonomy · 5 Systems by level · 6 Evaluation audit ·
  7 Reporting standard & shared protocol (recforge) · 8 Open problems · 9 Threats to validity · 10 Conclusion.
- Figures/tables: Fig 1 taxonomy grid; Fig 2 loop anatomy; Tab 1 survey comparison; Tab 2 systems catalogue;
  Tab 3 audit (main); Tab 4 failure incidents; Tab 5 reporting checklist.
- Abstract and intro: written in `draft/paper.tex`.

## Resource plan
Literature only; no GPU. Length target 14–18 pages acmart sigconf incl. references.
