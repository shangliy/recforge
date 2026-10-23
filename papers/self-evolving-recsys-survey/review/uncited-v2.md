# Uncited refs.bib entries

**Method.** I extracted every `\cite*{...}` key from `draft/paper.tex` after stripping comments. The file was a working copy with uncommitted edits, last modified 2026-10-22 20:08. I compared those keys with the 178 entries in `refs.bib`, which was generated 10:32 the same day.

**Counts.**
- 154 distinct keys are cited.
- 43 refs.bib entries are never cited.
- 19 cited keys are missing from refs.bib:
  - 12 are already in the edited manual.bib, and refs.bib just needs regenerating: he2017ncf, wang2019ngcf, yuan2023morec, akiba2019optuna, gao2022kuairand, gao2022kuairec, sarwar2001itemknn, harper2015movielens, mcauley2015amazon, wu2020mind, hidasi2016gru4rec, rendle2009bpr.
  - 7 are undefined anywhere and are supplied in `new-manual.bib`: lindauer2020bestpractices, kapoor2024reforms, zhu2025abc, agarwal2021precipice, dodge2019showyourwork, kapoor2025agentsmatter, kohavi2020trustworthy.

**Classes.**
- **(A)** In-scope self-evolving recommender that the survey should mention: 10 entries.
- **(B)** Related work worth citing: 26 entries. Two of these are optional and can be dropped: `zhao2022recbole2` and `li2024autokaggle`.
- **(C)** Out of scope or leftover: 7 entries.

I classified every entry from its arXiv abstract. For RecPilot, EvoReason, AgenticRS-Architecture, Agent0 and RuleAgent I also checked the method section of the arXiv HTML. A ⚠ marks a borderline call.

---

## (A) In scope: should be mentioned

| Key | Level / signal | Where | Sentence to insert |
|---|---|---|---|
| `zhang2026agenticrs` | L2 code + features (industry), offline comparison on validation/replay data | §5.3 Code-level loops in industry, after Astar | "From the authors of Astar, AutoModel organises an industrial recommender as interacting evolution agents for models (AutoTrain), features (AutoFeature) and deployment and online experimentation (AutoPerf), and shows in a case study an AutoTrain module that reproduces published methods from the paper text and compares them offline against the production baseline~\cite{zhang2026agenticrs}." Author overlap with `hu2026astar` and `hu2026rethinking` was checked in refs.bib (Hu, Deng, Mu, Zhang, Wang, Zhang, Zeng). The evidence is a case study and is not audited. |
| `skrlj2025agent0` | L2 features (text-derived categorical features); oracle feedback tunes the extraction prompts | §5.3 industry, or a short "feature loops" sentence in §5.2 | "Agent0 coordinates LLM agents that propose which aspects of raw text to turn into categorical features for a recommender, and tunes its own extraction prompts through a feedback loop with a downstream oracle~\cite{skrlj2025agent0}." |
| `wang2025ruleagent` | L2 (training-data denoising rules); selection on a validation-set evaluator, test reported separately | §5.2 Code-level loops in the open, end of paragraph | "RuleAgent has a language agent propose rules for denoising implicit feedback, retrains the recommender with an unlearning shortcut (LossEraser) instead of from scratch, and keeps rules according to validation-set performance~\cite{wang2025ruleagent}." |
| `ou2026recpilot` | L4 memory/rubrics, S6 (user feedback during service, best-of-$n$ rubric optimisation) | §5.5 L4, memory/reflection sentence | "RecPilot replaces item lists with generated reports, and its report agent refines per-user rubrics and experience memories from ongoing user feedback through best-of-$n$ optimisation~\cite{ou2026recpilot}." |
| `cai2024afl` | L4 policy, S6 (recommendation agent and user agent refine each other) | §5.5 L4, next to CoARS | "An agentic feedback loop lets a recommendation agent and a user agent refine each other's inferences over rounds, and reports that the loop does not amplify popularity or position bias~\cite{cai2024afl}." |
| `wang2024re2llm` | L4 memory (reflection-built hint base) + trained hint-retrieval policy; feedback from task labels | §5.5 L4, memory/reflection sentence | "Re2LLM has the LLM reflect on its recommendation errors to build a knowledge base of corrective hints, and trains a lightweight retrieval agent with task feedback to choose which hints to show~\cite{wang2024re2llm}." |
| `liu2023recprompt` | L4 prompts, iterative prompt optimiser | §5.5 L4, next to Spotify (prompt-level) | "RecPrompt pairs an LLM news recommender with a prompt optimiser that iteratively rewrites the recommendation prompt by bootstrapping~\cite{liu2023recprompt}, an earlier instance of the prompt-level loop that Spotify runs with a coding agent." |
| `wang2025srlf` | L4 reflection, S6 ("assess–validate–reflect" cycle) ⚠ | §5.5 L4, memory/reflection list | "SRLF runs a set-wise assess–validate–reflect cycle in which an LLM agent judges whole item sets against a user profile and revises its understanding~\cite{wang2025srlf}." ⚠ The abstract frames it as user-behaviour simulation, and whether the reflected state persists across rounds is not stated. Check before adding it to the taxonomy table. |
| `zhuang2026evoreason` | L4 weights (also touches L3 generative); S6, with the primitive library and teacher updated from the student's own on-policy outcomes; Kuaishou, with online results | §5.5 L4, weight-level sentence after OneRec | "EvoReason distils reasoning into latent tokens for a generative recommender, and updates its library of reasoning primitives and its teacher according to the student's on-policy outcomes~\cite{zhuang2026evoreason}." ⚠ This is a training method with a closed loop, not a keep/discard loop over candidates. It fits the "weights" row of L4, not L2/L3. |
| `ishida2026qdrec` | ⚠ Outputs, not the system. Quality–diversity archive of (item, hypothesis) recommendations; candidates enter if novel or better than their nearest neighbour | §5.5 L4 closing sentence, or Background "LLM program evolution" | "QD-Rec carries open-ended quality–diversity search into recommendation for decisions, evolving an archive of items paired with natural-language hypotheses in which a candidate is kept if it is novel or beats its nearest neighbour~\cite{ishida2026qdrec}; the evolved object is the recommendation set itself rather than the recommender." It is listed under (A) because it is the closest recommendation analogue of FunSearch-style archives. If the strict definition in §2 is applied, it is (B) Background. |

## (B) Related work worth citing

| Key | Where | Sentence to insert |
|---|---|---|
| `hu2026rethinking` | §1 Introduction or §4 Taxonomy (as a blueprint) | "A recent blueprint proposes promoting pipeline modules to agents only when they form a closed, independently evaluable loop with an evolvable decision space, and distinguishes RL-style evolution in defined action spaces from LLM generation and selection of architectures and training schemes in open design spaces~\cite{hu2026rethinking}." |
| `maragheh2025future` | §5.5 L4 intro or §8 Open Problems ("Circularity at the policy level") | "Maragheh and Deldjoo define agentic recommenders as stateful agents that observe, plan, call tools and verify, and in a controlled pilot find multi-agent pipelines not uniformly better than a single-shot baseline~\cite{maragheh2025future}, a reminder that L4 gains need controlled baselines." |
| `huang2025multimodalagentic` | §5.5 L4 intro | "Perspective papers on LLM-based agentic recommenders list lifelong personalisation, controllability and evaluation in dynamic settings as open questions~\cite{huang2025multimodalagentic,maragheh2025future}." |
| `chen2026covemem` | §5.5 L4, after the memory list (contrast) | "CoVeMem instead replaces the rewritten text memory with frozen collaborative-filtering states that the LLM reads as soft tokens and learns to use by gradient training~\cite{chen2026covemem}, which removes the per-interaction LLM rewrite that memory-evolving agents rely on." |
| `lin2026lion` | §2 Scope ("Inclusion"/exclusions): boundary case for the term | "We exclude continual-learning methods that call themselves self-evolving but have no proposer or selection step, such as LION's sparse key–value memory for adapting a generative recommender to streaming preferences~\cite{lin2026lion}." |
| `liu2026bianque` | §5.3 industry, "Adjacent loops" sentence | "...and an operations agent for Kuaishou's search engine evolves its skills and event memory from on-call engineers' corrections~\cite{liu2026bianque}." (Its object is the operations agent, not the recommender.) |
| `liu2025dgdpo` | §5.5 L4, simulators sentence | "...user simulators whose profiles are iteratively diagnosed and refined, and co-evolve with the recommender over multi-round interaction~\cite{liu2025dgdpo}." |
| `shang2025agentrecbench` | §5.5 L4, benchmarks sentence | "...AgentRecBench, an interactive textual simulator with classic, evolving-interest and cold-start scenarios~\cite{shang2025agentrecbench}..." |
| `srikanth2026aide2` | §5.6 Meta | "Outside recommendation, AIDE$^2$ edits its own research-agent code, keeps changes that perform best on hidden evaluations, and shows that the gains transfer to four held-out benchmarks~\cite{srikanth2026aide2}. Separating selection tasks from held-out tasks is what meta-evolving recommenders lack." |
| `wong2025confucius` | §3 Background, harness-optimisation clause | "...and recent work optimises the agent harness itself~\cite{lou2026autoharness,lee2026metaharness,xu2026harness2}, including a meta-agent that builds, tests and refines coding agents~\cite{wong2025confucius}." |
| `schmidgall2025agentlab` | §3 Background, ML-engineering agents list | Add to the list: "...Agent Laboratory~\cite{schmidgall2025agentlab}..." |
| `trirat2024automlagent` | §3 Background, ML-engineering agents list | "...AutoML-Agent~\cite{trirat2024automlagent}..." |
| `guo2024dsagent` | §3 Background, ML-engineering agents list | "...DS-Agent~\cite{guo2024dsagent}..." |
| `li2024autokaggle` | §3 Background, ML-engineering agents list (optional) | "...AutoKaggle~\cite{li2024autokaggle}..." |
| `huang2023mlagentbench` | §3 Background (benchmarks sentence) | "MLAgentBench reports success rates falling from 100% on older datasets to 0% on Kaggle tasks created after the models' training~\cite{huang2023mlagentbench}, a warning for loops evaluated on public recommendation data." |
| `wijk2024rebench` | §6 Audit/§7 Protocol (R6 budget) or Background | "RE-Bench shows that the ranking of agents against human experts reverses as the time budget grows~\cite{wijk2024rebench}, so a single end-of-budget number can mislead." |
| `liu2024agenthpo` | §5.1 L1 or §7 R5 (null control) | "LLM-driven hyperparameter optimisation~\cite{zhang2023llmhpo,liu2024agenthpo} is the general-ML form of L1, and it is compared against Bayesian optimisation or random search, the null control we ask for in R5." |
| `zhang2023llmhpo` | same as above | (same sentence) Optional note: Zhang et al. treat model code as a hyperparameter, which is a step toward L2. |
| `jawahar2024llmpp` | §8 Open Problems, "Proxies for expensive candidates" | "LLMs can also serve as the proxy, predicting a candidate architecture's performance before training~\cite{jawahar2024llmpp}." |
| `wang2020autorec` | §3 Background, search-space AutoML | "...and AutoRec packages model search and tuning for deep recommenders as an AutoML library~\cite{wang2020autorec}." (It is a library/platform. The inclusion rule excludes general HPO libraries, but this one is recommender-specific; your call.) |
| `fan2023movielens` | §3 Background, Evaluation methodology | "Even the dominant dataset is a weak proxy: MovieLens interactions are shaped by the platform's own onboarding and recommendations~\cite{fan2023movielens}." |
| `zhao2022recbole2` | §3 Background, libraries (optional, next to RecBole) | "...RecBole~\cite{zhao2021recbole,zhao2022recbole2}..." |
| `zhou2026mofa` | §5.1 L1 or §5.3 industry, as a non-loop contrast | "LLM reasoning also selects features for industrial models directly from definitions, importance scores and correlations~\cite{zhou2026mofa}; without an evaluation-driven keep step it falls outside our definition." |
| `thakur2026feature` / `barlier2026feature` / `hao2026lattearena` | §5.3 adjacent loops (feature engineering) and §8 budget-normalised comparison | "Adjacent work evolves features for tabular and recommendation models: an error-driven loop turns AUC ranking inversions into feedback for an LLM feature generator~\cite{barlier2026feature}, a planner-guided agent writes feature code for recommendation models with human checkpoints~\cite{thakur2026feature}, and LATTEArena benchmarks LLM feature-engineering methods on cost as well as accuracy~\cite{hao2026lattearena}, the kind of cost-aware comparison we call for." |

## (C) Out of scope / leftover

| Key | Reason |
|---|---|
| `wang2023recmind` | LLM recommender agent with self-inspiring planning within an episode; no self-improvement loop (excluded under §2). |
| `huang2023interecagent` | Conversational, tool-using LLM recommender; no improvement loop (excluded). |
| `wang2024macrec` | Multi-agent recommendation framework (SIGIR demo); its Reflector acts within a task, with no evolution across rounds. |
| `xu2025iagent` | User-side protective agent; a different paradigm with no evolving recommender. |
| `huang2025recbenchplus` | Benchmark for LLM recommendation assistants without self-improvement. Cite only if the L4 benchmark list is expanded. |
| `koralewski2026promptpack` | Cost scaling of a single-call LLM annotation agent through batching; no proposer or selection loop. |
| `song2019autoint` | AutoInt is a self-attentive CTR model, not AutoML (the name is misleading). Leftover. |

## The nine entries you asked about

| Key | Class | One line |
|---|---|---|
| `ishida2026qdrec` | A ⚠ (or B) | Quality–diversity evolution of an archive of item+hypothesis recommendations; it evolves outputs, not the recommender. |
| `lin2026lion` | B (scope boundary) | Continual adaptation with sparse KV memory; "self-evolving" in name only, with no proposer or selection. |
| `zhuang2026evoreason` | A ⚠ (L4 weights) | Closed-loop co-evolution of reasoning primitives/teacher with student outcomes; Kuaishou, with online results. |
| `chen2026covemem` | B (L4 contrast) | Trained vector memory instead of LLM-rewritten text memory; no self-improvement loop. |
| `ou2026recpilot` | A (L4 memory, S6) | Report agent self-evolves per-user rubrics and memories from user feedback (best-of-$n$). |
| `liu2026bianque` | B (adjacent industrial loop) | Skill and memory self-evolution of an operations agent for search/rec/ads engines at Kuaishou. |
| `zhang2026agenticrs` | A (L2 industry) | AutoModel: AutoTrain/AutoFeature/AutoPerf evolution agents; case study of paper-driven model reproduction with offline comparison. |
| `hu2026rethinking` | B (blueprint for intro/taxonomy) | Position paper for self-evolving agentic recommenders: module-to-agent criteria, RL vs. LLM generate-and-select, inner/outer rewards. |
| `maragheh2025future` | B (L4 intro / open problems) | Definitions and formalism for multi-agent recommenders; a pilot shows single-shot is often Pareto-efficient. |
