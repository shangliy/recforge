# Related work: self-evolving and agent-driven recommender systems

A catalogue of work on improving recommenders automatically, with what each system changes, what feedback it
learns from, and whether its code is open. Read [SURVEY.md](SURVEY.md) for the analysis.

Checked on 2026-10-21. Tags:

- **P**: the paper (title, authors, arXiv ID) was confirmed against arXiv or the venue page.
- **C**: the repository was confirmed through the GitHub API. The license shown is the one GitHub reports. "none" means no license file was found, so reuse is not permitted by default.
- **?**: part of the entry could not be confirmed (the note says which part).

"Hygiene" records whether the paper discusses which split drives the search, sampled vs. full ranking, budgets,
or the gap between validation and test. For many 2026 preprints only the abstract was read, so "not discussed"
can understate the paper. Corrections are welcome as pull requests.

## 1. LLM agents that change recommender code or configuration

### Open source

| system | year | evolves | feedback | evaluation hygiene | paper | code |
|---|---|---|---|---|---|---|
| Self-EvolveRec | 2026 | model code (seeds NCF, NGCF, SASRec, MoRec), plus a co-evolving diagnosis tool | validation NDCG/HR, LLM user-simulator critiques, diagnosis tool | test held out; ranks against 99 sampled negatives; step cap only | [2602.12612](https://arxiv.org/abs/2602.12612) P | [Sein-Kim/self_evolverec](https://github.com/Sein-Kim/self_evolverec) C, none |
| RecHarness (Kuaishou, Georgia Tech) | 2026 | architecture, objective and training code; a bandit picks the edit direction | validation HR@10 only | test scored once; 43,200 GPU-second budget; backbones include HSTU; ranks against 99 sampled negatives | [2607.29241](https://arxiv.org/abs/2607.29241) P | [6lyc/RecHarness](https://github.com/6lyc/RecHarness) C, MIT |
| VirtualMLE | 2026 | hyperparameters and training config of SASRec and HSTU; memory reused across datasets | per-trial outcomes | not discussed in the abstract | [2606.03221](https://arxiv.org/abs/2606.03221) P | [cst20/VirtualMLE-is-all-you-need-to-Recommend](https://github.com/cst20/VirtualMLE-is-all-you-need-to-Recommend) ?, not confirmed official, none |

### Industrial, no code released

| system | org | year | evolves | feedback | paper |
|---|---|---|---|---|---|
| Self-Evolving Recommendation System | Google / YouTube | 2026 (RecSys) | code and config diffs of a production ranker: optimizer, architecture, reward logic | offline validation loss, then online A/B | [2602.10226](https://arxiv.org/abs/2602.10226) P |
| EvoRec | Alibaba | 2026 | model code; skills distilled from experiment memory | offline Recall/NDCG; online A/B; HSTU, TIGER and Cobra used as baselines | [2606.28368](https://arxiv.org/abs/2606.28368) P |
| NOVA | affiliation not confirmed | 2026 | architecture code of an ads ranker | validity checks, a fixed offline evaluation budget, A/B | [2606.27243](https://arxiv.org/abs/2606.27243) P |
| AgentX | affiliation not confirmed | 2026 | production code; the agents themselves | online A/B with guardrails | [2606.26859](https://arxiv.org/abs/2606.26859) P |
| AgentX-Model | affiliation not confirmed | 2026 | model code in research lineages | offline AUC, calibration, A/B | [2609.30001](https://arxiv.org/abs/2609.30001) P |
| Auto-RecSys | affiliation not confirmed | 2026 | research ideas and execution playbooks | experiment outcomes | [2609.10922](https://arxiv.org/abs/2609.10922) P |
| AutoLR | NetEase | 2026 | code patches and configs under a limited trial budget | offline results, then a launch-review gate | [2609.04871](https://arxiv.org/abs/2609.04871) P |
| CORAL | affiliation not confirmed | 2026 (RecSys OARS workshop) | retrieval, ranking and serving configuration | live A/B | [2609.02730](https://arxiv.org/abs/2609.02730) P |
| AgenticRecTune | affiliation not confirmed | 2026 | multi-stage pipeline configuration; a skill hub | online A/B | [2604.26969](https://arxiv.org/abs/2604.26969) P |
| Sortify | affiliation not confirmed | 2026 | ranking fusion weights | online GMV / revenue | [2603.27765](https://arxiv.org/abs/2603.27765) P |
| GEARS | affiliation not confirmed | 2026 | ranking policy parameters | experiment results; checks against overfitting short-term signals | [2602.18640](https://arxiv.org/abs/2602.18640) P |
| AI Co-Scientist for search ranking | online travel platform | 2026 | ranking architecture and training code, human in the loop | offline metrics; single-run statistics flagged as a limitation | [2603.22376](https://arxiv.org/abs/2603.22376) P |
| AgenticRS-Architecture | overlaps with EvoRec authors | 2026 | models, features and resources (design paper) | not specified | [2603.26085](https://arxiv.org/abs/2603.26085) P |
| Ranking Engineer Agent (REA) | Meta | 2026 | ads ranking code and configs | experiment metrics; GPU cost approved up front | [engineering blog](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) |
| Planning in constrained agent topology | affiliation not confirmed | 2026 | feature-engineering code | downstream metrics, human input | [2601.10820](https://arxiv.org/abs/2601.10820) P |
| LLMs as feature engineers | affiliation not confirmed | 2026 | LLM-extracted features for CTR models | offline information gain; small gains reported honestly | [2609.21894](https://arxiv.org/abs/2609.21894) P |

### Closely related

| work | why it matters | paper |
|---|---|---|
| EvoRank (learning to rank, not recommendation) | Its held-out transfer audit found that most of the first campaign's gains were fitness noise. This is the clearest evidence that evolution loops overfit their selection data. The authors say code will be released; none was found. | [2609.22196](https://arxiv.org/abs/2609.22196) P |
| From AutoRecSys to AutoRecLab (Beel et al.) | A position paper calling for autonomous recsys research labs, with shared benchmarks and provenance | [2510.18104](https://arxiv.org/abs/2510.18104) P |
| WPP AlphaEvolve case study | Reports up to 7% on a recommendation score. A blog post; only search snippets were read | [blog](https://cms.research.wpp.com/?p=577) ? |

## 2. Classic AutoML and NAS for recommenders (background)

| work | venue | searches over | paper | code |
|---|---|---|---|---|
| AutoCTR | KDD 2020 | interaction-block DAGs, by evolution | [2007.06434](https://arxiv.org/abs/2007.06434) P | none found |
| AutoFIS | KDD 2020 | feature-interaction mask (DARTS-style gates) | [2003.11235](https://arxiv.org/abs/2003.11235) P | [zhuchenxv/AutoFIS](https://github.com/zhuchenxv/AutoFIS) C, none |
| AutoEmb | 2020 | embedding dimensions in streaming recommendation | [2002.11252](https://arxiv.org/abs/2002.11252) P | not checked |
| AutoDim | 2020 | per-field embedding dimensions | [2006.14827](https://arxiv.org/abs/2006.14827) P | not checked |
| NASRec (Meta) | WWW 2023 | architectures, with weight sharing | [2207.07187](https://arxiv.org/abs/2207.07187) P | [facebookresearch/NasRec](https://github.com/facebookresearch/NasRec) C, Apache-2.0 |
| DNS-Rec | 2024 | sequential-recommender architectures | [2402.00390](https://arxiv.org/abs/2402.00390) P | not checked |
| AutoLossGen | SIGIR 2022 | loss functions, by RL | [2204.13160](https://arxiv.org/abs/2204.13160) P | not checked |
| AutoRec (AutoKeras-style) | RecSys 2020 demo | pipelines and hyperparameters | [2007.07224](https://arxiv.org/abs/2007.07224) P | [datamllab/AutoRec](https://github.com/datamllab/AutoRec) C, none |
| AutoML for Deep Recommender Systems (survey) | 2022 | survey | [2203.13922](https://arxiv.org/abs/2203.13922) P | |

## 3. General LLM program evolution and ML-engineering agents

None of these targets recommendation. Self-EvolveRec builds on OpenEvolve and DeepEvolve and uses them as
baselines. They are candidate evolvers to run against recforge sessions.

| system | org | evolves | paper | code |
|---|---|---|---|---|
| FunSearch | Google DeepMind | one function, island-based evolution | Nature 2023 | [google-deepmind/funsearch](https://github.com/google-deepmind/funsearch) C, Apache-2.0 |
| AlphaEvolve | Google DeepMind | whole files, by diffs | [2506.13131](https://arxiv.org/abs/2506.13131) P | early access only |
| OpenEvolve | community | code, MAP-Elites with islands | no paper | [algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve) C, Apache-2.0 |
| ShinkaEvolve | Sakana AI | code, with novelty rejection sampling | [2509.19349](https://arxiv.org/abs/2509.19349) P | [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) C, Apache-2.0 |
| DeepEvolve | Notre Dame, MIT-IBM | code, with deep research | [2510.06056](https://arxiv.org/abs/2510.06056) P | [liugangcode/deepevolve](https://github.com/liugangcode/deepevolve) C, none |
| AIDE | Weco AI | ML solution code, by tree search | [2502.13138](https://arxiv.org/abs/2502.13138) P | [WecoAI/aideml](https://github.com/WecoAI/aideml) C, MIT |
| MLE-STAR | Google Cloud, KAIST | code, with ablation-guided refinement | [2506.15692](https://arxiv.org/abs/2506.15692) P | not confirmed |
| AIRA | Meta | search policies and operators on MLE-bench | [2507.02554](https://arxiv.org/abs/2507.02554) P | not checked |
| R&D-Agent | Microsoft Research | code, with research and development agents | [2505.14738](https://arxiv.org/abs/2505.14738) P | [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) C, MIT |
| The AI Scientist / v2 | Sakana AI | experiments and papers | [2408.06292](https://arxiv.org/abs/2408.06292), [2504.08066](https://arxiv.org/abs/2504.08066) P | [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist), [-v2](https://github.com/SakanaAI/AI-Scientist-v2) C, custom license |
| Agent Laboratory | | research assistant agents | [2501.04227](https://arxiv.org/abs/2501.04227) P | [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) C, MIT |
| AutoML-Agent | | full AutoML pipelines | [2410.02958](https://arxiv.org/abs/2410.02958) P | [DeepAuto-AI/automl-agent](https://github.com/DeepAuto-AI/automl-agent) C, none |
| DS-Agent | | data-science code, case-based reasoning | [2402.17453](https://arxiv.org/abs/2402.17453) P | [guosyjlu/DS-Agent](https://github.com/guosyjlu/DS-Agent) C, none |
| AutoKaggle | | Kaggle pipelines | [2410.20424](https://arxiv.org/abs/2410.20424) P | [multimodal-art-projection/AutoKaggle](https://github.com/multimodal-art-projection/AutoKaggle) C, Apache-2.0 |
| AgentHPO | Tsinghua | hyperparameters | [2402.01881](https://arxiv.org/abs/2402.01881) P | [ssui-liu/AgentHPO](https://github.com/ssui-liu/AgentHPO) ?, not confirmed official |
| LLMs for HPO (Zhang et al.) | | hyperparameters | [2312.04528](https://arxiv.org/abs/2312.04528) P | not checked |
| AutoHarness | Google DeepMind | agent harness code | [2603.03329](https://arxiv.org/abs/2603.03329) P | none found |
| Meta-Harness | Stanford | harness and prompt code | [2603.28052](https://arxiv.org/abs/2603.28052) P | [stanford-iris-lab/meta-harness](https://github.com/stanford-iris-lab/meta-harness) C, MIT |
| Harness² | Google Cloud AI Research (from the author list) | per-task harnesses, by propose / probe / compose | [2610.14224](https://arxiv.org/abs/2610.14224) P | none found |
| Confucius Code Agent | Meta | agent scaffolding; the base of Meta REA | [2512.10398](https://arxiv.org/abs/2512.10398) P | [facebookresearch/cca-swebench](https://github.com/facebookresearch/cca-swebench) C, MIT, may cover only the SWE-bench code |

## 4. Recommender agents that evolve a policy, prompt, memory or weights (not code)

| system | evolves | paper | code |
|---|---|---|---|
| RecMind | per-query planning (self-inspiring) | [2308.14296](https://arxiv.org/abs/2308.14296) P | none found |
| InteRecAgent (MSRA) | tool-using policy with reflection | [2308.16505](https://arxiv.org/abs/2308.16505) P | [microsoft/RecAI](https://github.com/microsoft/RecAI) C, MIT |
| MACRec | multi-agent policy with a reflector | [2402.15235](https://arxiv.org/abs/2402.15235) P | [wzf2000/MACRec](https://github.com/wzf2000/MACRec) C, none |
| AgentCF | user and item agent memories, by reflection | [2310.09233](https://arxiv.org/abs/2310.09233) P | [RUCAIBox/AgentCF](https://github.com/RUCAIBox/AgentCF) C, Apache-2.0 |
| RecPrompt | news-recommendation prompts | [2312.10463](https://arxiv.org/abs/2312.10463) P | not checked |
| Re2LLM | a hint knowledge base built by reflection, plus an RL retrieval agent | [2403.16427](https://arxiv.org/abs/2403.16427) P | not checked |
| iAgent | user-side agent with dynamic memory | [2502.14662](https://arxiv.org/abs/2502.14662) P | [WujiangXu/iAgent](https://github.com/WujiangXu/iAgent) C, none |
| OneRec (Kuaishou) | weights, by iterative DPO on its own beam samples | [2502.18965](https://arxiv.org/abs/2502.18965), [2506.13695](https://arxiv.org/abs/2506.13695) P | [Kuaishou-OneRec/OpenOneRec](https://github.com/Kuaishou-OneRec/OpenOneRec) C, none; coverage of the DPO loop not checked |
| SPRec | weights, by self-play SFT + DPO | [2412.09243](https://arxiv.org/abs/2412.09243) P | [RegionCh/SPRec](https://github.com/RegionCh/SPRec) C, none |
| Rec-R1 | LLM weights, by RL against a recommender's metric | [2503.24289](https://arxiv.org/abs/2503.24289) P | [linjc16/Rec-R1](https://github.com/linjc16/Rec-R1) C, Apache-2.0 |
| Agent4Rec | user simulator (used as an evaluator) | [2310.10108](https://arxiv.org/abs/2310.10108) P | [LehengTHU/Agent4Rec](https://github.com/LehengTHU/Agent4Rec) C, MIT |
| RecAgent / YuLan-Rec | user-behavior simulation | [2306.02552](https://arxiv.org/abs/2306.02552) P | [RUC-GSAI/YuLan-Rec](https://github.com/RUC-GSAI/YuLan-Rec) C, MIT |

Generative backbones that the evolution systems use or compare against:

| model | paper | code |
|---|---|---|
| HSTU (Meta) | [2402.17152](https://arxiv.org/abs/2402.17152) P | [meta-recsys/generative-recommenders](https://github.com/meta-recsys/generative-recommenders) C, Apache-2.0 |
| TIGER (Google) | [2305.05065](https://arxiv.org/abs/2305.05065) P | no official code; [snap-research/GRID](https://github.com/snap-research/GRID) implements semantic-ID retrieval |

## 5. Evaluation protocol and benchmarks

### Recommender evaluation

| work | finding | paper | code |
|---|---|---|---|
| Dacrema et al., RecSys 2019 | tuned simple baselines beat most neural methods; some papers tuned on test | [1907.06902](https://arxiv.org/abs/1907.06902) P | [MaurizioFD/RecSys2019_DeepLearning_Evaluation](https://github.com/MaurizioFD/RecSys2019_DeepLearning_Evaluation) C, AGPL-3.0 |
| Krichene & Rendle, KDD 2020 | sampled metrics can reverse model rankings | [1912.02263](https://arxiv.org/abs/1912.02263) P (preprint) | |
| Ji et al., TOIS | leave-one-out that ignores the global timeline leaks future data | [2010.11060](https://arxiv.org/abs/2010.11060) P | |
| Meng et al., RecSys 2020 | splitting strategy changes rankings | [2007.13237](https://arxiv.org/abs/2007.13237) P | |
| Hidasi & Czapp, RecSys 2023 | four common evaluation flaws | [2307.14951](https://arxiv.org/abs/2307.14951) P | |
| Rendle et al., RecSys 2020 | NCF vs. MF revisited | [2005.09683](https://arxiv.org/abs/2005.09683) P | |
| Klenitskiy & Vasilev, RecSys 2023 | a loss change alone makes SASRec beat BERT4Rec | [2309.07602](https://arxiv.org/abs/2309.07602) P | |
| Petrov & Macdonald, RecSys 2022 | BERT4Rec replicability | [2207.07483](https://arxiv.org/abs/2207.07483) P | |
| Fan et al., TOIS | what MovieLens results mean | [2307.09985](https://arxiv.org/abs/2307.09985) P | |
| DaisyRec 2.0 (Sun et al.) | rigorous evaluation and fair comparison | [2206.10848](https://arxiv.org/abs/2206.10848) P | [recsys-benchmark/DaisyRec-v2.0](https://github.com/recsys-benchmark/DaisyRec-v2.0) C, MIT |

### Libraries and open benchmarks

| library | paper | code |
|---|---|---|
| RecBole | [2011.01731](https://arxiv.org/abs/2011.01731), [2206.07351](https://arxiv.org/abs/2206.07351) P | [RUCAIBox/RecBole](https://github.com/RUCAIBox/RecBole) C, MIT |
| Elliot | [2103.02590](https://arxiv.org/abs/2103.02590) P | [sisinflab/elliot](https://github.com/sisinflab/elliot) C, Apache-2.0 |
| BARS | [2205.09626](https://arxiv.org/abs/2205.09626) P | [reczoo/RecBench](https://github.com/reczoo/RecBench) C, Apache-2.0 |
| FuxiCTR | [2009.05794](https://arxiv.org/abs/2009.05794) P | [reczoo/FuxiCTR](https://github.com/reczoo/FuxiCTR) C, Apache-2.0 |
| AgentRecBench (agents as recommenders) | [2505.19623](https://arxiv.org/abs/2505.19623) P | official repo not found |
| RecBench+ (LLM recommendation assistants) | [2503.09382](https://arxiv.org/abs/2503.09382) P | [jiani-huang/RecBenchPlus](https://github.com/jiani-huang/RecBenchPlus) C, none |

### ML-engineering agent benchmarks

| benchmark | recommendation tasks | how test data is handled | paper | code |
|---|---|---|---|---|
| MLE-bench (OpenAI) | one: H&M fashion recommendations | the grader holds the private test set; the agent builds its own validation split | [2410.07095](https://arxiv.org/abs/2410.07095) P | [openai/mle-bench](https://github.com/openai/mle-bench) C |
| MLRC-Bench | one: KDD Cup 2023 next-product recommendation | agents see only the dev split; the best dev snapshot is scored on test once | [2504.09702](https://arxiv.org/abs/2504.09702) P | [yunx-z/MLRC-Bench](https://github.com/yunx-z/MLRC-Bench) C, MIT |
| MLGym (Meta) | none | `validate` returns test-set metrics and can be called repeatedly | [2502.14499](https://arxiv.org/abs/2502.14499) P | [facebookresearch/MLGym](https://github.com/facebookresearch/MLGym) C |
| MLAgentBench | none (task list not re-checked) | | [2310.03302](https://arxiv.org/abs/2310.03302) P | [snap-stanford/MLAgentBench](https://github.com/snap-stanford/MLAgentBench) C, MIT |
| RE-Bench (METR) | none (task list not re-checked) | agents compared with humans at matched time budgets | [2411.15114](https://arxiv.org/abs/2411.15114) P | [METR/RE-Bench](https://github.com/METR/RE-Bench) C |
