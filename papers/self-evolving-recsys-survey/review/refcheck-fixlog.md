# Ref-check fix log

Pass of 2026-10-26 over `review/ref-check.md` (2026-10-22). Each item was checked against the current `draft/paper.tex`, `audit/audit.csv` and `refs.bib`. Backups: `draft/paper_pre_refcheck.tex`, `*.pre_refcheck` (refs.bib, manual.bib, published.tsv, published.py, audit/audit.csv, draft/audit_rows.tex, draft/figs/audit_bars.tex, draft/figs/timeline.tex, submission/tmlr/make_tmlr.py, submission/tmlr/main.pdf).

Status counts: already fixed 106, fixed now 10, not applicable 5 (total 121; ref-check has no I-27).

audit.csv was not changed. `summarize.py` output is identical to the embedded table, audit_rows.tex and audit_bars.tex, and every count quoted in the text matches it. refs.bib was rebuilt per README (arxiv2bib.py + published.py; 48/48 published versions applied). The only change is the two optional titles.

| id | status | note |
|---|---|---|
| T-1 | already fixed | Embedded table between %BEGIN/END-AUDIT-ROWS is identical to `summarize.py` output from audit.csv (re-ran into scratch, no diff). |
| T-2 | already fixed | PE row has no Astar and C9 = P. C2/C3 are coded test/N, not NS/P as ref-check proposed. This was set in the two-coder reconciliation and fits I-18: PE selects and reports source-local gains on the same instances. F2/F3 describe it this way. |
| T-3 | already fixed | EvoRank C9 = Y, incident = N. The caption has no `\yes{}+G`. |
| T-4 | already fixed | The taxonomy no longer has signal columns. REA sits in L2 x LLM as "Meta REA (blog)", with no online claim. |
| T-5 | already fixed | AutoCTR and AutoLossGen carry the dagger (paper.tex l.323-325). |
| T-6 | already fixed | AutoLR is in the L2 row. Caption: multi-object loops appear in the row of their highest level. |
| T-7 | already fixed | "\emph{comparison:} Evolving Semantic Indexes" in the taxonomy. The L3 text says "a generative document-retrieval system that we treat as a comparison point". |
| T-8 | already fixed | "prompts and tool descriptions: ... Spotify". |
| T-9 | already fixed | EvoRank C1 = other. |
| T-10 | already fixed | audit.csv online values: NOVA 6d+sig, CORAL sig, AgenticRecTune sig. F9 says "nine report significance or confidence intervals", which matches summarize. |
| C-1 | already fixed | Intro: "inflated its proxy metrics by shrinking the batch size, and with it the number of in-batch negatives". |
| C-2 | already fixed | Intro: "won on the metric without a real improvement", with the verbatim co-scientist quote. "Five" = 4 core + 1 comparison, as in F7. |
| C-3 | already fixed | F7: "Four core loops and one comparison point". EvoRank appears only as a pre-search leakage audit (prevention). |
| C-4 | already fixed | The quote is now verbatim: ``improved $\mathcal{M}$ while being wrong (e.g., silently increasing model size)''. |
| C-5 | already fixed | "travel search ranking" / "travel-search co-scientist". No "hotel" left. |
| C-6 | already fixed | "a fresh online confirmation ..., as Sortify does with a seven-day re-test, ideally pre-registered". |
| C-7 | already fixed | "for two Claude models (Sonnet and Opus)". The text flags it as by one of us and not peer reviewed. |
| C-8 | already fixed | MACRec removed from the L4 text and taxonomy (wang2024macrec is now uncited). |
| C-9 | already fixed | Klenitskiy for the loss change; Petrov for longer training. |
| C-10 | already fixed | Hidasi is cited for sampled metrics and leakage. The split-choice clause cites only Meng et al. |
| C-11 | already fixed | The Kaggle submission-limit claim is gone. It now reads "without a resubmission cap~\cite{blum2015ladder}". |
| C-12 | already fixed | "DPO preference pairs mined at the held-out target position". |
| C-13 | already fixed | "would have inflated NDCG@10 from 0.2192 to 0.2517/0.2577". The wording on how it was caught is under C-14. |
| C-14 | fixed now | F7 (l.763-765) now says: "the genre and DPO bugs surfaced as anomalous trajectories on the leaderboard, the inflation was reasoned out as leakage in the diagnosis the loop requires for every negative result". Checked against 2609.39551 App. H.4 ("An argument rather than a sweep..."; "the loop requires a post-hoc diagnosis of every negative before the next proposal") and App. I.1. |
| C-15 | already fixed | "an operator's approval, not an evaluation, keeps or rejects each proposed override". Matches 2608.11241 §1/§4.2 (re-checked). Residual risk: the 196-round Stop-hook campaign's keep rule is deferred to a companion paper. |
| C-16 | already fixed | Moved to the borderline-systems sentence: "RecSys Factory's diagnostics uncovered a pre-existing upstream join bug". |
| C-17 | already fixed | "Evolving Semantic Indexes evolves TIGER-style semantic-ID components for document retrieval but releases no code; no open system yet does so for recommendation". |
| C-18 | already fixed | "Seven studies outside recommendation are included as comparison points", each with its domain named. |
| C-19 | already fixed | "only in passing, in two sentences that cite AgentX and the Google loop". |
| I-1 | already fixed | "... and others followed." |
| I-2 | already fixed | "RMD-Bench fixes protocols for cross-dataset and cross-scale discovery and ExecML-HSTU measures whether agents' edits execute correctly". |
| I-3 | already fixed | "embedding search, mostly for click-through-rate (CTR) prediction models". |
| I-4 | fixed now | l.204-205: "whole architectures with a weight-sharing supernet (NASRec), compact attention-based sequential models under resource constraints (DNS-Rec)". |
| I-5 | already fixed | "... on public CTR data, or standard rating and sequential benchmarks, with standard splits". |
| I-6 | fixed now | The L4 section was already fixed. The Background sentence (l.230-231) still had the old wording; it now reads "first by iterative DPO~\cite{deng2025onerec} and then by on-policy RL~\cite{zhou2025onerectech,zhou2025openonerec}". |
| I-7 | already fixed | Sortify: Optuna searches exchange rates; the LLM meta-controller recalibrates the transfer intercepts and penalties. |
| I-8 | already fixed | "screens candidates on peer datasets (and, for LLM and VLM targets, on small training subsets)". |
| I-9 | already fixed | "Most industrial systems share a two-stage design". |
| I-10 | already fixed | "promotes on validation loss (with a proxy metric for reward changes)". |
| I-11 | already fixed | "AgentX, deployed at Kuaishou, iterates online strategies and model research, and its successor AgentX-Model runs research lineages". |
| I-12 | already fixed | "can also sit in earlier generations, not only in the latest model". |
| I-13 | already fixed | "prompts, few-shot examples and tool descriptions with a coding agent, evaluated by an LLM judge on synthetic conversations". |
| I-14 | already fixed | "Simulated environments and benchmarks ... the user simulators Agent4Rec and RecAgent, and the verifiable $\tau$-Rec benchmark". |
| I-15 | already fixed | "a two-sentence mention of self-optimised fine-tuning and a recommendation task in a benchmark it describes". |
| I-16 | already fixed | F1: "99 sampled negatives". |
| I-17 | already fixed | F2: Astar's loss-decrease rule labels training data; the paper does not say what decides production iterations (C2 = NS). |
| I-18 | already fixed | F2: PE "selects on its source instances' evaluation scores and reports its local gains on them". |
| I-19 | already fixed | "six independent sessions with bracketed ranges, but only for an ablation". |
| I-20 | already fixed | F5: P1 has the highest validation score; "the paper states no rule for choosing a front point". |
| I-21 | fixed now | The scope (historical replay, Scenario A) was already stated. Added at l.729-730: "and no policy led consistently across scenarios". |
| I-22 | already fixed | F4: A-MLE's re-run rule "materially reduced" single-seed promotions. |
| I-23 | already fixed | F8: "the same fixed hyperparameters (embedding 50, batch 128, learning rate 0.001) without describing tuning them". |
| I-24 | already fixed | F9: "AutoLR's summed launch-review lifts". |
| I-25 | fixed now | F6 (l.723) now: "Optuna-TPE at a matched offline-evaluation budget but unmatched LLM cost, and only on its ScaleUp task, a search over structural hyperparameters". The previous text ("in its code-level setting") was wrong: 2606.27243 says Optuna-TPE is "applicable only to L2", NOVA's ScaleUp task over six structural hyperparameters. Verified in the arXiv HTML. |
| I-26 | already fixed | F5: "on a small sample of five programs". |
| I-28 | fixed now | figs/timeline.tex: RecEvolve moved from Sep to Jul (arXiv API v1 2026-07-20). I re-queried the arXiv API for every 2026 system in the figure; all other placements match their v1 month. EvoRank and RecSys Factory are still not in the figure (they are a comparison point and a borderline system). |
| I-29 | already fixed | AgentLTV C2 = test. |
| I-30 | fixed now | F7 already said "metric-winning bugs, metric inflation or leakage". The audit-table legend (l.603) now matches: "gaming, metric-winning bugs, metric inflation or leakage". |
| I-31 | fixed now | l.876: "about \$29 per task, or about \$22 with cached artifacts". Checked against 2606.27243 Table 5 (sums to 29.14 / 22.29). |
| I-32 | not applicable | The S6 signal columns are gone from the taxonomy. The L4 row says "Selected mostly on self-generated feedback", and §4.5 describes Rec-R1 as "RL against a recommender's metric". |
| I-33 | not applicable | Ref-check verdict: OK to keep the AgentCF dagger. |
| X-1 | already fixed | Resolved with T-1. Abstract: "Four loops report..."; incident = Y for 4 core rows. |
| X-2 | already fixed | F7: "three say nothing" matches C9 NS = 3 among offline-selecting loops (summarize). |
| B-meta2026rea | already fixed | The title matches ref-check's corrected title. |
| B-romeraparedes2023funsearch | already fixed | Full 12 authors, Nature 625(7995):468-475, 2024, DOI and DOI URL. The key still says 2023 while year = 2024; the key is never printed, so it is cosmetic. |
| B-krichene2020sampled | already fixed | pages, publisher, address and DOI present. |
| B-roelofs2019metaanalysis | already fixed | NeurIPS 32, Curran, proceedings URL; no pages (none verifiable). |
| B-utf8-authors | already fixed | published.py TeX-escapes author names. refs.bib has 0 non-ASCII characters. |
| B-li2026autorecsys (optional) | fixed now | Uses the paper's own title ("...Recommender Systems") via TITLES in published.py. |
| B-mu2026evorec (optional) | fixed now | "EvoRec: Self-Evolving Agentic Recommender Systems" via TITLES in published.py. |
| B-uncited (2c) | not applicable | BibTeX prints only cited entries. rendle2019sampled and sun2019bert4rec are now cited, as suggested. |
| P-audited-caution | already fixed | wang2026selfevolving and pan2026recevolve cite RecSys 2026 with note "The audit coded the arXiv version". |
| P-wang2026selfevolving | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-pan2026recevolve | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-palumbo2026spotify | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-baumgart2026autoreclab | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-narasimhan2026taurec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-nian2026rankevolveir | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-chen2026memrec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-liu2025recoworld | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhang2025agentsearchsurvey | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-peng2025agentsurvey | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-liu2025agentcfpp | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-gao2024sprec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-wang2023recagent | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-nam2025mlestar | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-toledo2025aira | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhang2025mlrcbench | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhang2024agentcf | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-wang2024macrec | already fixed | Published version (Crossref DOI) applied from published.tsv. Now uncited after the C-8 fix. |
| P-zhang2023agent4rec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhang2024dnsrec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhang2023nasrec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-ji2020leakage | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-sun2022daisyrec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zheng2022automl | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-hidasi2023flaws | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-klenitskiy2023dross | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-petrov2022bert4rec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-li2022autolossgen | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhu2022bars | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhao2021recbole | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhu2021fuxictr | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-anelli2021elliot | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhao2020autoemb | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-song2020autoctr | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-liu2020autofis | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-meng2020splitting | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-rendle2020ncf | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-dacrema2019progress | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-kang2018sasrec | already fixed | Published version (Crossref DOI) applied from published.tsv. |
| P-zhai2024hstu | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-rajput2023tiger | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-chan2024mlebench | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-lin2025recr1 | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-gao2025selfevolvingsurvey | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-zhang2026rsir | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-dwork2015reusable | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-blum2015ladder | already fixed | Venue applied before this pass, confirmed only by the arXiv comment or Semantic Scholar (no Crossref record). Kept; pages not verified. |
| P-azhar2026coral | not applicable | Workshop paper. Ref-check: may stay an arXiv citation. Left as @misc. |
| P-kim2026aura | not applicable | Workshop paper. Ref-check: may stay an arXiv citation. Left as @misc. |
