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
| Self-EvolveRec (KAIST, Microsoft) | 2026 | model code (seeds NCF, NGCF, SASRec, MoRec), plus a co-evolving diagnosis tool | validation NDCG/HR, LLM user-simulator critiques, diagnosis tool | test held out; ranks against 99 sampled negatives; step cap only | [2602.12612](https://arxiv.org/abs/2602.12612) P | [Sein-Kim/self_evolverec](https://github.com/Sein-Kim/self_evolverec) C, none |
| RecHarness (Kuaishou, Georgia Tech) | 2026 | architecture, objective and training code; a bandit picks the edit direction | validation HR@10 only | test scored once; 43,200 GPU-second budget; backbones include HSTU; ranks against 99 sampled negatives | [2607.29241](https://arxiv.org/abs/2607.29241) P | [6lyc/RecHarness](https://github.com/6lyc/RecHarness) C, MIT |
| VirtualMLE (Tsinghua, BUPT) | 2026 | hyperparameters and training config of SASRec and HSTU; memory reused across datasets | per-trial outcomes | not discussed in the abstract | [2606.03221](https://arxiv.org/abs/2606.03221) P | [cst20/VirtualMLE-is-all-you-need-to-Recommend](https://github.com/cst20/VirtualMLE-is-all-you-need-to-Recommend) C (linked from the abstract), none |

| EvoSkillRec (CityU HK, Kuaishou, XJTU) | 2026 | architectures as typed "skill genomes" plus LLM-written modules promoted into a skill library | validation AUC | test used for reporting only; single evolution runs; only 1 of 5 validation-Pareto candidates kept its gains on test | [2609.34552](https://arxiv.org/abs/2609.34552) P | [Xiaopengli1/EvoSkill-Rec](https://github.com/Xiaopengli1/EvoSkill-Rec) (from the paper; license not checked) |
| RankEvolve (Meta) | 2026 | HSTU configs and code, Claude Code and Codex reviewing each other; ExecML-HSTU benchmark | full-test NDCG@10 leaderboard | full-catalogue ranking, but selects on test; documents three leakage incidents found in agent edits | [2609.39551](https://arxiv.org/abs/2609.39551) P | promised |
| Population Evolution (Meta) | 2026 | model and training code; several searches share evidence; RMD-Bench | source fitness, promotion to larger scale | full-catalogue ranking; transfer failures reported; baselines calibrated on the test split (disclosed) | [2610.05950](https://arxiv.org/abs/2610.05950) P | promised |
| AgentLTV | 2026 | lifetime-value pipeline programs (MCTS then island evolution) | Pareto multi-metric score | split not stated | [2602.21634](https://arxiv.org/abs/2602.21634) P | [wuchaowei123/AgentLTV](https://github.com/wuchaowei123/AgentLTV) C, none |
| AutoRecLab (Siegen, Göttingen) | 2026 | recommender experiment code from a natural-language description (automates experiments, does not evolve a model) | LLM-judged requirement coverage | n/a | [2609.21863](https://arxiv.org/abs/2609.21863) P | [ISG-Siegen/AutoRecLab](https://github.com/ISG-Siegen/AutoRecLab) C, MIT |

### Industrial, no code released

| system | org | year | evolves | feedback | paper |
|---|---|---|---|---|---|
| Self-Evolving Recommendation System | Google / YouTube | 2026 (RecSys) | code and config diffs of a production ranker: optimizer, architecture, reward logic | offline validation loss, then online A/B | [2602.10226](https://arxiv.org/abs/2602.10226) P |
| EvoRec | Alibaba | 2026 | model code; skills distilled from experiment memory | offline Recall/NDCG; online A/B; HSTU, TIGER and Cobra used as baselines | [2606.28368](https://arxiv.org/abs/2606.28368) P |
| NOVA | Tencent | 2026 | architecture code of an ads ranker | validity checks, a fixed offline evaluation budget, A/B | [2606.27243](https://arxiv.org/abs/2606.27243) P |
| AgentX | deployed at Kuaishou (no affiliation line) | 2026 | production code; the agents themselves | online A/B with guardrails | [2606.26859](https://arxiv.org/abs/2606.26859) P |
| AgentX-Model | deployed at Kuaishou | 2026 | model code in research lineages | offline AUC, calibration, A/B | [2609.30001](https://arxiv.org/abs/2609.30001) P |
| Auto-RecSys | Meta | 2026 | research ideas and execution playbooks | experiment outcomes | [2609.10922](https://arxiv.org/abs/2609.10922) P |
| AutoLR | NetEase | 2026 | code patches and configs under a limited trial budget | offline results, then a launch-review gate | [2609.04871](https://arxiv.org/abs/2609.04871) P |
| CORAL | Meta | 2026 (RecSys OARS workshop) | retrieval, ranking and serving configuration | live A/B | [2609.02730](https://arxiv.org/abs/2609.02730) P |
| AgenticRecTune | Google | 2026 | multi-stage pipeline configuration; a skill hub | online A/B | [2604.26969](https://arxiv.org/abs/2604.26969) P |
| Sortify | Shopee | 2026 | ranking fusion weights | online GMV / revenue | [2603.27765](https://arxiv.org/abs/2603.27765) P |
| GEARS | Meta | 2026 | ranking policy parameters | experiment results; checks against overfitting short-term signals | [2602.18640](https://arxiv.org/abs/2602.18640) P |
| AI Co-Scientist for search ranking | Trip.com, UCLA | 2026 | ranking architecture and training code, human in the loop | offline metrics; single-run statistics flagged as a limitation | [2603.22376](https://arxiv.org/abs/2603.22376) P |
| AgenticRS-Architecture | overlaps with EvoRec authors | 2026 | models, features and resources (design paper) | not specified | [2603.26085](https://arxiv.org/abs/2603.26085) P |
| RecEvolve | Google | 2026 | code and config of a production two-tower retrieval model | offline metrics, then A/B; its agent inflated in-batch metrics by shrinking the batch size, caught by a human | [2609.01622](https://arxiv.org/abs/2609.01622) P |
| Astar | Alibaba (Lazada), Zhejiang U. | 2026 | an 8B model trained on commit history proposes evolution directions | training-loss outcomes, learned reward model; 5-day A/B | [2608.27287](https://arxiv.org/abs/2608.27287) P |
| A-MLE | Meta | 2026 | config and architecture code of ads-ranking models, human checkpoints | significance vs a rolling baseline | [2609.08248](https://arxiv.org/abs/2609.08248) P |
| SR-Agent | Kuaishou | 2026 | post-ranking strategy configuration through four bounded actions | bad-case retest, replay, one-month A/B | [2607.17719](https://arxiv.org/abs/2607.17719) P |
| From Trajectories to Evidence | Kuaishou | 2026 | paper-derived module adaptations to a production ranker; auditable records | per-round AUC; reports that 22 of 30 trajectories end below an earlier best | [2608.05235](https://arxiv.org/abs/2608.05235) P |
| RecSys Factory | Tencent | 2026 | Claude-Code-based platform bounded to typed decision points (operations more than evolution) | human approval cards | [2608.11241](https://arxiv.org/abs/2608.11241) P |
| AURA | Walt Disney Company | 2026 | log-driven diagnosis and code proposals (stops at pull requests) | LLM-judged rubric | [2609.16625](https://arxiv.org/abs/2609.16625) P |
| Spotify conversational agent | Spotify | 2026 | prompts and logic of a conversational recommender, edited by a coding agent | LLM judge on synthetic conversations, then A/B | [2609.30297](https://arxiv.org/abs/2609.30297) P |
| Rethinking Recommendation Paradigms | Alibaba (EvoRec authors) | 2026 | blueprint for self-evolving agentic modules | layered rewards | [2603.26100](https://arxiv.org/abs/2603.26100) P |
| Ranking Engineer Agent (REA) | Meta | 2026 | ads ranking code and configs | experiment metrics; GPU cost approved up front | [engineering blog](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) |
| Planning in constrained agent topology | affiliation not confirmed | 2026 | feature-engineering code | downstream metrics, human input | [2601.10820](https://arxiv.org/abs/2601.10820) P |
| LLMs as feature engineers | affiliation not confirmed | 2026 | LLM-extracted features for CTR models | offline information gain; small gains reported honestly | [2609.21894](https://arxiv.org/abs/2609.21894) P |

### Closely related

| work | why it matters | paper |
|---|---|---|
| EvoRank (learning to rank, not recommendation) | Its held-out transfer audit found that most of the first campaign's gains were fitness noise. This is the clearest evidence that evolution loops overfit their selection data. The authors say code will be released; none was found. | [2609.22196](https://arxiv.org/abs/2609.22196) P |
| From AutoRecSys to AutoRecLab (Beel et al.) | A position paper calling for autonomous recsys research labs, with shared benchmarks and provenance | [2510.18104](https://arxiv.org/abs/2510.18104) P |
| RankEvolve for lexical retrieval (SIGIR '26 short) | LLM evolution of BM25/QL ranking programs; evaluated on 16 held-out datasets | [2602.16932](https://arxiv.org/abs/2602.16932) P, code [fangchenli/ranking-evolved](https://github.com/fangchenli/ranking-evolved) |
| WPP AlphaEvolve case study | Reports up to 7% on a recommendation score. A blog post; only search snippets were read | [blog](https://cms.research.wpp.com/?p=577) ? |

### Components of generative recommenders

| work | evolves | feedback | paper | code |
|---|---|---|---|---|
| Evolving Semantic Indexes for Generative Retrieval (Santa Clara U., Coupang) | semantic-ID construction, collisions, decoding, training objective | 1M-parameter proxy decoder; proxy-target agreement holds for indexes (ρ = 0.90) but inverts when the objective changes | [2610.28568](https://arxiv.org/abs/2610.28568) P | none found |
| AgenticTagger | hierarchical item-descriptor vocabulary used as tokens | annotator LLMs | [2602.05945](https://arxiv.org/abs/2602.05945) P | none found |
| Self-improving item tokenization | the recommender reassigns its own item tokens | its training signal | [2412.17171](https://arxiv.org/abs/2412.17171) P | none found |
| Feedback-grounded policy discovery (Kuaishou) | natural-language policies distilled into a semantic-ID generator | similarity reward on training data; 7-day A/B | [2607.27789](https://arxiv.org/abs/2607.27789) P | none found |

### LLM feature engineering and data rules

| work | evolves | paper |
|---|---|---|
| Agent0 | multi-value features discovered from text | [2507.18993](https://arxiv.org/abs/2507.18993) P |
| PromptPack | batched LLM annotation of ad creatives for CTR features | [2607.20528](https://arxiv.org/abs/2607.20528) P |
| MoFA | LLM feature selection and interaction discovery | [2603.24979](https://arxiv.org/abs/2603.24979) P |
| RuleAgent | denoising rules over training-loss patterns | [2503.23374](https://arxiv.org/abs/2503.23374) P |
| LATTEArena | benchmark of LLM tabular feature engineering (not recsys) | [2606.09004](https://arxiv.org/abs/2606.09004) P |

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
| SAGER | per-user natural-language policy skills | [2604.14972](https://arxiv.org/abs/2604.14972) P | no official code |
| RecNet | preference-propagation modules optimised with textual gradients | [2601.21609](https://arxiv.org/abs/2601.21609) P | none found |
| AtomRec | atomic, linked user and item memories | [2609.04882](https://arxiv.org/abs/2609.04882) P | none found |
| AMEM4Rec / STEAM / MARS | cross-user, community and belief-state memories | [2602.08837](https://arxiv.org/abs/2602.08837), [2601.16872](https://arxiv.org/abs/2601.16872), [2605.14401](https://arxiv.org/abs/2605.14401) P | none found |
| MemRec | collaborative memory graph | [2601.08816](https://arxiv.org/abs/2601.08816) P | [rutgerswiselab/MemRec](https://github.com/rutgerswiselab/MemRec) C, none |
| AgentCF++ | dual-layer cross-domain memory | [2502.13843](https://arxiv.org/abs/2502.13843) P | [jhliu0807/AgentCF-plus](https://github.com/jhliu0807/AgentCF-plus) C, none |
| AFL | recommender and user agents refine each other | [2410.20027](https://arxiv.org/abs/2410.20027) P | [Lanyu0303/AFL](https://github.com/Lanyu0303/AFL) C, MIT |
| CoARS | co-evolving recommender and user agents by RL | [2604.10029](https://arxiv.org/abs/2604.10029) P | none found |
| RSIR / DA-RSIR / state retention | recursive self-training on filtered synthetic sequences | [2602.15659](https://arxiv.org/abs/2602.15659), [2610.04302](https://arxiv.org/abs/2610.04302), [2610.07105](https://arxiv.org/abs/2610.07105) P | [USTC-StarTeam/RSIR](https://github.com/USTC-StarTeam/RSIR) C, none; [Jinfeng-Xu/RecRSI](https://github.com/Jinfeng-Xu/RecRSI) C, MIT |
| LION | self-evolving memory layer for generative recommenders | [2609.15598](https://arxiv.org/abs/2609.15598) P | [JazyJiang/Self-Evolving-Memory-for-Generative-Recommendation](https://github.com/JazyJiang/Self-Evolving-Memory-for-Generative-Recommendation) C, MIT |
| QD-Rec (Sakana AI) | quality-diversity archive of recommendations | [2610.23470](https://arxiv.org/abs/2610.23470) P | [SakanaAI/QD-Rec](https://github.com/SakanaAI/QD-Rec) C, Apache-2.0 |
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
| RecoWorld (WWW '26 HCRS workshop) | [2509.10397](https://arxiv.org/abs/2509.10397) P | none found |
| τ-Rec, verifiable agentic-recommender benchmark | [2606.10156](https://arxiv.org/abs/2606.10156) P | [nbharaths/tau-rec](https://github.com/nbharaths/tau-rec) C |
| RecRM-Bench, reward models for agentic recommenders | [2605.11874](https://arxiv.org/abs/2605.11874) P | HF dataset (per abstract) |
| RecBench+ (LLM recommendation assistants) | [2503.09382](https://arxiv.org/abs/2503.09382) P | [jiani-huang/RecBenchPlus](https://github.com/jiani-huang/RecBenchPlus) C, none |

### ML-engineering agent benchmarks

| benchmark | recommendation tasks | how test data is handled | paper | code |
|---|---|---|---|---|
| MLE-bench (OpenAI) | one: H&M fashion recommendations | the grader holds the private test set; the agent builds its own validation split | [2410.07095](https://arxiv.org/abs/2410.07095) P | [openai/mle-bench](https://github.com/openai/mle-bench) C |
| MLRC-Bench | one: KDD Cup 2023 next-product recommendation | agents see only the dev split; the best dev snapshot is scored on test once | [2504.09702](https://arxiv.org/abs/2504.09702) P | [yunx-z/MLRC-Bench](https://github.com/yunx-z/MLRC-Bench) C, MIT |
| MLGym (Meta) | none | `validate` returns test-set metrics and can be called repeatedly | [2502.14499](https://arxiv.org/abs/2502.14499) P | [facebookresearch/MLGym](https://github.com/facebookresearch/MLGym) C |
| MLAgentBench | none (task list not re-checked) | | [2310.03302](https://arxiv.org/abs/2310.03302) P | [snap-stanford/MLAgentBench](https://github.com/snap-stanford/MLAgentBench) C, MIT |
| RE-Bench (METR) | none (task list not re-checked) | agents compared with humans at matched time budgets | [2411.15114](https://arxiv.org/abs/2411.15114) P | [METR/RE-Bench](https://github.com/METR/RE-Bench) C |

### Surveys and roadmaps (none covers code-level evolution of recommenders)

| survey | paper |
|---|---|
| Autonomous Information Seeking: A Roadmap for Agentic Recommender Systems (mentions "agent as engineer" in one clause) | [2607.04433](https://arxiv.org/abs/2607.04433) P |
| A Survey on LLM-powered Agents for Recommender Systems | [2502.10050](https://arxiv.org/abs/2502.10050) P |
| A Survey of LLM Empowered Agents for Recommendation and Search | [2503.05659](https://arxiv.org/abs/2503.05659) P |
| A Survey of Foundation Model-Powered Recommender Systems | [2504.16420](https://arxiv.org/abs/2504.16420) P |
| The Future is Agentic (multi-agent recommender perspective) | [2507.02097](https://arxiv.org/abs/2507.02097) P |
| Towards Agentic Recommender Systems in the Era of Multimodal LLMs | [2503.16734](https://arxiv.org/abs/2503.16734) P |
| A Survey of Self-Evolving Agents (general; no recommender code evolution) | [2507.21046](https://arxiv.org/abs/2507.21046) P |
| A Comprehensive Survey of Self-Evolving AI Agents (general; never mentions recommendation) | [2508.07407](https://arxiv.org/abs/2508.07407) P |
