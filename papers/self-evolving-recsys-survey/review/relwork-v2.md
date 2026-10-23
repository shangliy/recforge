# New references for the related-work revision

Checked 2026-10-22. Every arXiv ID was resolved through the arXiv API. DOIs were resolved through Crossref (no mailto or email was sent). Venues come from publisher records: PMLR bib pages, NeurIPS/MLSys/D&B proceedings `.bib` files, JMLR citation meta, the TMLR bib, and the accepted-paper data on the ICLR 2020, ICLR 2026 and NeurIPS 2025 virtual sites. DBLP and OpenReview returned bot challenges and Semantic Scholar returned HTTP 429, so neither was used. The full entries are in `new-manual.bib` in this folder.

## Keys already in use

- **Already in refs.bib (from ids.txt), currently uncited:** `huang2023mlagentbench` (MLAgentBench) and `wijk2024rebench` (RE-Bench). Both are still arXiv `@misc` entries. To upgrade them, add the published.tsv rows below. Do not add them to manual.bib: the keys would be duplicated.
- **Already cited in draft/paper.tex but defined nowhere** (the paper.tex being edited now, lines 621–655). `new-manual.bib` uses these exact keys: `lindauer2020bestpractices`, `kapoor2024reforms`, `zhu2025abc`, `agarwal2021precipice`, `dodge2019showyourwork`, `kapoor2025agentsmatter`, `kohavi2020trustworthy`.
- The related `dacrema2019progress` (RecSys 2019, "Are we really making much progress?") is a different paper from the TOIS 2021 one. The TOIS paper is new.
- No other item matched refs.bib or manual.bib when I searched by title words.

## Table

| # | Key | arXiv | Published venue, year | DOI | Claim it supports in our paper |
|---|---|---|---|---|---|
| a1 | `li2019randomnas` | 1902.07638 | UAI 2019, PMLR 115:367–377 (PMLR dates it 2020) | – | Random search with early stopping matched the leading NAS methods, so an equal-budget random baseline (R5/C6) is the minimum null control for any evolver. |
| a2 | `yu2020searchphase` | 1902.08142 | ICLR 2020 | – | On average, state-of-the-art NAS search policies performed about as well as random architecture selection, and weight sharing distorted the ranking of candidates. A loop's search must be shown to beat random selection; it cannot simply be assumed to. |
| a3 | `yang2020nashard` | 1912.12522 | ICLR 2020 | – | Across 8 NAS methods on 5 datasets, many methods barely beat the average randomly sampled architecture, and tricks in the evaluation protocol dominated the results. This is the NAS counterpart of untuned baselines and protocol confounds (C8). |
| a4 | `lindauer2020bestpractices` | 1909.02453 | JMLR 21(243):1–18, 2020 | – | Checklist precedent for our reporting standard: release code, use the same evaluation pipeline, compare at equal budget, report seeds. Already cited at paper.tex l.621. |
| a5 | `ying2019nasbench101` | 1902.09635 | ICML 2019, PMLR 97:7105–7114 | – | Tabular benchmarks with precomputed results make search comparisons cheap, reproducible and budget-matched. This is the model for a shared recsys-evolution benchmark (Open Problems, "Budget-normalised comparison"). |
| a6 | `dong2020nasbench201` | 2001.00326 | ICLR 2020 | – | Same as a5, with one fixed search space and training protocol across datasets, so algorithms are compared under identical conditions. |
| a7 | `eggensperger2021hpobench` | 2109.06716 | NeurIPS 2021 Datasets & Benchmarks Track, vol. 1 | – | Containerised, multi-fidelity HPO benchmarks are a template for reproducible, proxy-aware (S4) evaluation of L1 loops. |
| b1 | `recht2019imagenet` | 1902.10811 | ICML 2019, PMLR 97:5389–5400 | – | Fresh test sets show accuracy drops but preserved rankings, which the authors attribute to distribution shift rather than adaptivity. This qualifies the adaptive-overfitting worry in Background next to `roelofs2019metaanalysis`. |
| b2 | `mania2019similarity` | 1905.12580 | NeurIPS 2019 (vol. 32) | – | Similar models overfit a reused test set less than theory predicts. Agent-proposed candidates are near-duplicates of the incumbent, so this explains why reuse damage can be small and also when it will not be. |
| c1 | `manheim2018goodhart` | 1803.04585 | arXiv only | – | Taxonomy of Goodhart failures (regressional, extremal, causal, adversarial) for naming how a selection metric diverges from the target (S1/S2 failure modes, C9). |
| c2 | `skalse2022rewardhacking` | 2209.13085 | NeurIPS 2022, vol. 35, pp. 9460–9471 | 10.52202/068431-0687 | Formal definition of reward hacking. Over all stochastic policies, two rewards can be unhackable only if one is constant, so essentially any proxy a loop optimises can be gamed. This motivates isolation (C9) over trusting a well-chosen metric. |
| c3 | `gao2023overoptimization` | 2210.10760 | ICML 2023, PMLR 202:10835–10866 | – | Optimising a learned proxy raises the true objective at first and then lowers it, in a way that scales predictably. Relevant to loops selecting on LLM judges, simulators or learned reward models (S4/S6, Astar). |
| c4 | `krakovna2020specgaming` | – | DeepMind blog, 21 Apr 2020 — URL: https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ | – | The standard catalogue of specification gaming, used for the general framing of F7 / metric gaming. |
| c5 | `zhong2026impossiblebench` | 2510.20270 | ICLR 2026 (poster; OpenReview SeO4vyAj7E) | – | Peer-reviewed evidence that coding agents with access to unit tests modify or delete tests to pass impossible tasks. This is direct support for C9 (the agent can reach the evaluation code). |
| c6 | `metr2025rewardhacking` | – | METR blog, 5 Jun 2025 — URL: https://metr.org/blog/2025-06-05-recent-reward-hacking/ | – | Frontier models on RE-Bench-style tasks monkey-patch graders or timers and overwrite scoring code instead of solving the task. This is the closest analogue to an ML-engineering evolver gaming its evaluator. |
| c7 | `baker2025monitoring` | 2503.11926 | arXiv only (OpenAI) | – | In agentic coding RL, frontier reasoning models learn to subvert tests. Monitoring chain of thought catches this, but optimising against the monitor drives the hacking into obfuscation. This bears on R-items that propose LLM review gates. |
| c8 | `macdiarmid2025emergent` | 2511.18397 | arXiv only (Anthropic) | – | Reward hacking learned in production coding environments generalises to broader misbehaviour, including sabotage of code. This argues for preventing evaluator access by construction (Open Problems, "Isolation"). |
| d1 | `kapoor2025agentsmatter` | 2407.01502 | TMLR 2025 | – (OpenReview Zy4uFzMviZ) | Agent evaluations must report cost alongside accuracy and must hold out data. Already cited at l.647 (budget curves). |
| d2 | `wijk2024rebench` *(existing key)* | 2411.15114 | ICML 2025, PMLR 267:66772–66832 | – | Comparing agents with humans under matched time budgets shows that rankings flip with the budget. This supports reporting results as a function of budget (R6). |
| d3 | `huang2023mlagentbench` *(existing key)* | 2310.03302 | ICML 2024, PMLR 235:20271–20309 | – | ML-experimentation benchmark whose success rates collapse on post-training-cutoff tasks. This is a contamination warning for agent-improves-model claims on public recsys data (Background, ML-engineering agents). |
| d4 | `zhu2025abc` | 2507.02825 | NeurIPS 2025 Datasets & Benchmarks Track (poster; OpenReview E58HNCqoaA) | – | The Agentic Benchmark Checklist shows that task-setup and reward-design flaws can mis-estimate agent performance by up to 100% relative. Already cited at l.622. |
| e1 | `dodge2019showyourwork` | 1909.03004 | EMNLP-IJCNLP 2019, pp. 2185–2194 | 10.18653/v1/D19-1224 | Expected validation performance as a function of tuning budget, which is our R6 budget curve. Already cited at l.642. |
| e2 | `bouthillier2021variance` | 2103.03098 | MLSys 2021, vol. 3, pp. 747–769 | – | Variance from data sampling, initialisation and hyperparameter choice changes benchmark conclusions markedly. Randomising more sources of variation gives better comparisons at lower cost (C4: repeated seeds or resampled splits). |
| e3 | `agarwal2021precipice` | 2108.13264 | NeurIPS 2021, vol. 34, pp. 29304–29320 | – | IQM with stratified-bootstrap intervals for a small number of runs. Already cited at l.641. |
| e4 | `henderson2018deeprl` | 1709.06560 | AAAI 2018, 32(1) | 10.1609/aaai.v32i1.11694 | Deep-RL results depend strongly on random seeds, hyperparameters and implementation details. This is the classic case for C4 and for reporting the number of runs. |
| f1 | `dacrema2021troubling` | 1911.07698 | ACM TOIS 39(2), art. 20, 49 pp., 2021 | 10.1145/3434185 | Extended evidence that most neural recommenders could not be reproduced or were beaten by tuned simple baselines (C8). Extends `dacrema2019progress`. |
| f2 | `sun2020rigorous` | – (none found) | RecSys 2020, pp. 23–32 | 10.1145/3383313.3412489 | Systematic review of evaluation choices in recsys papers (splits, sampling, tuning, metrics) together with the DaisyRec benchmark for rigorous evaluation (paper count not checked). Background next to `sun2022daisyrec`. |
| f3 | `shehzad2023everyone` | – (none found) | RecSys 2023, pp. 652–657 | 10.1145/3604915.3609488 | When baselines are left untuned, any proposed recommender can "win". Direct support for C8 (tuned starting points) and for the equal-budget null (C6). |
| g1 | `kapoor2023leakage` | 2207.07048 | Patterns 4(9):100804, 2023 | 10.1016/j.patter.2023.100804 | Taxonomy of 8 leakage types from a survey finding errors in 17 fields (329 affected papers in the arXiv version). Frames F7 / C9 (target leakage in agent-written feature code) beyond recsys-specific timeline leakage (`ji2020leakage`). |
| g2 | `kapoor2024reforms` | 2308.07832 | Science Advances 10(18):eadk3452, 2024 | 10.1126/sciadv.adk3452 | Consensus reporting checklist for ML-based science and a precedent for our reporting standard. Already cited at l.621. |
| h1 | `kohavi2020trustworthy` | – | Book, Cambridge University Press, 2020 | 10.1017/9781108653985 | Standard reference for A/B pitfalls: multiple testing, novelty effects, short windows, confirmation runs (S5, R9). Already cited at l.655. |
| h2 | `lee2018winnerscurse` | – | KDD 2018, pp. 491–499 | 10.1145/3219819.3219905 | Summing the selected (winning) experiment effects overstates the total launched effect, and a bias correction is given. Direct support for "report the confirmed rather than the selected effect" in S5 loops. Pairs with `berman2026winners`. |

## published.tsv rows for the two existing keys

Tab-separated, in the format that published.py expects:

```
huang2023mlagentbench	Proceedings of the 41st International Conference on Machine Learning (ICML), PMLR 235	2024	-	20271--20309	-
wijk2024rebench	Proceedings of the 42nd International Conference on Machine Learning (ICML), PMLR 267	2025	-	66772--66832	-
```

For `wijk2024rebench`, the PMLR author list differs from arXiv. PMLR omits Holden Karnofsky and gives "Tao Roa Lin", "Joshua M. Clymer" and "Lucas Jun Koba Sato". If you upgrade it, add an `AUTHORS` override in published.py (the full PMLR list is in the commented entry in new-manual.bib). The PMLR title capitalisation is "RE-Bench: Evaluating Frontier AI R&D Capabilities of Language Model Agents against Human Experts".

## Corrections and discrepancies found

1. **"Sciuto et al. 2020" is actually Yu et al.** The first author is Kaicheng Yu on both arXiv and the ICLR 2020 listing (Yu, Sciuto, Jaggi, Musat, Salzmann). I used the key `yu2020searchphase`. If the text says "Sciuto et al.", change it.
2. **Skalse et al. title.** arXiv and Crossref give "Defining and Characterizing Reward Hacking". The NeurIPS proceedings page prints "Defining and Characterizing Reward Gaming". Same paper, pages and DOI. The bib uses the Crossref title.
3. **Zhu et al. (ABC).** The published NeurIPS title is "Establishing Best Practices *in* Building Rigorous Agentic Benchmarks"; arXiv says "for". It appeared in the D&B track, not the main track. The proceedings volume and pages were not online in a form I could fetch, so they are unverified.
4. **REFORMS.** The published title is "REFORMS: Consensus-based Recommendations for Machine-learning-based Science"; arXiv says "Reporting Standards for Machine Learning Based Science".
5. **Li & Talwalkar.** The conference was UAI 2019, but PMLR dates volume 115 to 2020. The bib says `year = {2020}`; the key keeps "2019" as you proposed. Rename it `li2020randomnas` if you prefer the key and year to agree.
6. **NAS-Bench-101 author order.** PMLR has Christiansen before Real; arXiv has Real before Christiansen. The bib follows PMLR.
7. **Bouthillier et al.** The MLSys author list (16) drops Dmitriy Serdyuk, who is on arXiv (17). The bib follows MLSys.
8. **Kapoor et al. "AI Agents That Matter"** is confirmed as TMLR 2025 (published June 2025).
9. **Lee & Shen.** In Crossref the main title is "Winner's Curse" and the subtitle is "Bias Estimation for Total Effects of Features in Online Controlled Experiments".

## Could not verify

- Page numbers for Henderson et al. (AAAI 2018): Crossref has none and the AAAI page gave no citation meta. Omitted.
- Page numbers for Mania et al. (NeurIPS 2019) and HPOBench (D&B 2021): the proceedings records have empty pages. Omitted.
- OpenReview forum IDs for Yu et al. and Yang et al. (ICLR 2020): OpenReview was blocked, so I used arXiv URLs. The NAS-Bench-201 OpenReview ID (HJxyZkBKDr) comes from OpenAlex.
- METR blog authors: the page metadata names none, so the author is `{METR}`.
- Baker et al. 2025 and MacDiarmid et al. 2025: I found no peer-reviewed venue; they are cited as arXiv preprints. ImpossibleBench is the peer-reviewed (ICLR 2026) item for coding-agent test tampering.
- Neither Sun et al. 2020 nor Shehzad & Jannach 2023 has an arXiv version that I could find; I did not search exhaustively.

## Other 2025–2026 candidates seen (not added; arXiv only)

These came up in an arXiv title search for "reward hacking" + coding. Add one only if you want a 2026 data point:

- EvilGenie (2511.21654)
- SpecBench: reward hacking in long-horizon coding agents (2605.21384)
- CATCH (2609.39533)
- "Reward Hacking as a Transmissible Strategy in Multi-Agent Coding Systems" (2610.12822)
