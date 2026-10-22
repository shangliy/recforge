# Related work (landscape for the survey)

Corpus: `refs.bib` (154 entries; every arXiv entry generated from the arXiv API, titles checked by eye 2026-10-21).
Sources: the curated catalogue `docs/related-work.md` (first sweep, ~75 entries, repos checked via GitHub API),
a second sweep `sweep-2026-10-21.md` (+56, abstracts only), litsearch runs below, and the bibliographies of
RecHarness, EvoRec, AgentX-Model, RecEvolve and the agentic-RS roadmap.

## Queries run
| Query | Source(s) | Kept |
|-------|-----------|------|
| self-evolving recommender system LLM agent (2025+) | litsearch (arXiv, OpenAlex, S2) | EvoRec, RecHarness; rest noise |
| LLM agent automated recommender model optimization code | litsearch | few; generic agent papers dominate |
| agentic harness recommender architecture evolution | litsearch | NOVA |
| LLM-driven NAS click-through rate | litsearch | none new |
| autonomous research agent recommendation model iteration industrial | litsearch | none new |
| survey LLM-based agents recommender / agentic RS / self-evolving agents / generative rec / AutoML agents / AI-scientist recsys | litsearch | 6 surveys (below) + AutoRecLab position |
| survey "self-evolving" recommender 2026 | WebSearch extended | RecEvolve, SAGER, RecNet, AtomRec, roadmap 2607.04433 |
| ~30 arXiv full-text phrasings + company names + citation-graph walk | sweep agent | 56 additions |

Generic search engines return mostly unrelated "agent for X" papers; the citation graph of the 2026 systems was the
productive source. Lesson for the methods section of the paper: describe the search protocol honestly
(seed set + backward/forward snowballing + keyword sweep), with the cut-off date 2026-10-21.

## Landscape
### Cluster A — Search-space AutoML for recommenders (2019–2024)
- **Approach:** differentiable / evolutionary / RL search over a predefined space (interaction blocks, embedding
  dims, architectures, losses).
- **Representative:** [song2020autoctr], [liu2020autofis], [zhao2020autoemb], [zhang2023nasrec], [zhang2024dnsrec],
  [li2022autolossgen]; survey [zheng2022automl].
- **Core assumption:** the good design is inside a space a human wrote.
- **Ceiling:** cannot propose an operation outside the space; evaluation mostly validation logloss/AUC on Criteo-type
  data, so the selection-hygiene problem is mild (few, cheap, low-variance evaluations).

### Cluster B — Generic LLM program evolution and ML-engineering agents (2023–2026)
- **Approach:** an LLM proposes code edits; an automatic evaluator scores them; an archive/tree/bandit chooses what
  to expand.
- **Representative:** [romeraparedes2023funsearch], [novikov2025alphaevolve], [openevolve], [lange2025shinka],
  [liu2025deepevolve], [jiang2025aide], [nam2025mlestar], [yang2025rdagent], harness optimisation
  [lou2026autoharness], [lee2026metaharness], [xu2026harness2]; benchmarks [chan2024mlebench], [nathani2025mlgym],
  [zhang2025mlrcbench], [wijk2024rebench].
- **Core assumption:** the evaluator is a faithful, cheap, unhackable fitness.
- **Ceiling:** at most one recsys task per benchmark (H&M in MLE-bench; KDD Cup 2023 in MLRC-Bench); MLGym exposes
  test metrics through `validate`. Recsys evaluators are none of cheap, faithful or unhackable.

### Cluster C — Code- and configuration-level self-evolving recommenders (2026)
- **Approach:** cluster B transplanted onto a recommender codebase, plus recsys-specific structure (domain skills,
  verification gates, memory of failed edits, online A/B as the final judge).
- **Academic/open:** [kim2026selfevolverec], [ling2026recharness], [cao2026virtualmle], [baumgart2026autoreclab],
  [chen2026rankevolve] (HSTU, multi-agent review), [li2026evoskillrec], [peng2026population] (with RMD-Bench).
- **Industrial/closed:** [wang2026selfevolving] (Google/YouTube), [meta2026rea], [mu2026evorec] + [hu2026astar]
  (Alibaba), [lao2026agentx] + [yang2026agentxmodel] + [zhuang2026trajectories], [liu2026nova], [li2026autorecsys],
  [zhang2026autolr] (NetEase), [azhar2026coral], [wu2026agenticrectune], [cheng2026sortify], [yun2026gears],
  [pan2026recevolve], [gao2026amle], [kim2026aura], [ao2026recsysfactory] (Tencent), [yang2026sragent] (Kuaishou),
  [wu2026agentltv], [wu2026coscientist]; adjacent IR [nian2026rankevolveir], [patel2026evorank].
- **Core assumption:** the offline evaluator (or the A/B test) is a trustworthy selection signal for hundreds of
  agent-generated candidates.
- **Ceiling:** to be established by the audit (stage 05). Early signals: RecEvolve's agent found reward-hacking
  shortcuts in the evaluation protocol; RankEvolve targets silent leakage defects in agent edits; AgentX's
  "trajectories to evidence" reports non-monotonic trajectories; EvoRank's held-out audit found campaign gains to be
  mostly fitness noise; Population Evolution and Evolving Semantic Indexes report proxy→target transfer failures for
  objective changes.

### Cluster D — Component-level evolution for generative recommenders (2024–2026)
- **Approach:** search or self-improvement over semantic-ID tokenisers, item vocabularies, decoding, policies distilled
  into SID generators.
- **Representative:** [nian2026semanticindex], [xie2026agentictagger], [chen2024tokenization],
  [chen2026policydiscovery]; backbones [zhai2024hstu], [rajput2023tiger], [deng2025onerec], [zhou2025openonerec].
- **Core assumption:** a cheap proxy (small decoder, annotator LLM) ranks candidates like the full model.
- **Ceiling:** proxy fidelity (Spearman 0.90 in [nian2026semanticindex]) holds for index changes but not objective
  changes — evidence that the proxy is the bottleneck.

### Cluster E — Policy / memory / weight self-improvement of agentic recommenders (2023–2026)
- **Approach:** the recommender is an LLM agent (or LLM) that rewrites its memory, skills, prompts or weights from
  self-generated feedback (reflection, simulators, self-play, recursive self-training).
- **Representative:** reflection/memory [wang2023recmind], [zhang2024agentcf], [liu2025agentcfpp], [wang2024macrec],
  [tao2026sager], [li2026recnet], [hu2026atomrec], [nguyen2026amem4rec], [liao2026steam], [shen2026mars],
  [chen2026memrec]; prompts [liu2023recprompt], [palumbo2026spotify]; weights [deng2025onerec], [gao2024sprec],
  [lin2025recr1], [wang2026coars]; recursive self-improvement [zhang2026rsir], [hasan2026darsir],
  [xu2026stateretention]; open-ended [ishida2026qdrec]; environments [liu2025recoworld], [zhang2023agent4rec],
  [wang2023recagent].
- **Core assumption:** self-generated feedback (simulator, reflection, own samples) correlates with real user utility.
- **Ceiling:** circular evaluation — simulators often share the model family with the agent being improved
  (Self-EvolveRec mitigates with held-out simulators); recursive self-training can drift ([xu2026stateretention]
  shows progress can sit across generations rather than in the latest model).

### Cluster F — Evaluation methodology (the yardstick)
- [dacrema2019progress], [rendle2019sampled]/[krichene2020sampled], [ji2020leakage], [meng2020splitting],
  [hidasi2023flaws], [rendle2020ncf], [klenitskiy2023dross], [petrov2022bert4rec], [fan2023movielens],
  [sun2022daisyrec]; adaptive data analysis [dwork2015reusable], [blum2015ladder]; **counter-evidence**
  [roelofs2019metaanalysis] (little holdout overfitting across 120 Kaggle competitions).

## Nearest works (existing surveys) and our delta
| Key | Why close | Precise delta | Read depth |
|-----|-----------|---------------|------------|
| [lin2026roadmap] Autonomous Information Seeking: roadmap for agentic RS (Jul 2026) | most recent agentic-RS taxonomy | taxonomy by autonomy level (agent-assisted / as-recommender / as-simulator); per the sweep it does not treat code-evolving systems as a class. **To confirm with the audit agent's full read.** | abstract + refs |
| [peng2025agentsurvey], [zhang2025agentsearchsurvey], [huang2025fmsurvey] | LLM agents in recsys | 2025, predate every cluster-C system; cover the agent as recommender/simulator, not the agent as engineer of the recommender | abstract |
| [gao2025selfevolvingsurvey], [fang2025selfevolvingsurvey] | self-evolving agents in general | domain-agnostic; no recsys evaluation issues (sampled metrics, leakage, A/B) | abstract (audit agent reading) |
| [zheng2022automl] | AutoML for recommenders | pre-LLM; search-space methods only | known |
| [beel2025autoreclab] | call for autonomous recsys labs | a position paper; no catalogue, no audit | abstract |

## White space
- No survey of cluster C (code/config-level self-evolving recommenders) exists as of 2026-10-21 (searched: litsearch
  survey queries above; WebSearch "survey self-evolving recommender 2026"; sweep of 2026 bibliographies).
- No cross-system audit of evaluation practice in self-evolving recommenders exists.
- No shared benchmark: the closest are inside-paper suites (ExecML-HSTU, RMD-Bench) and general MLE benchmarks with ≤1
  recsys task.

## Timeline
- 2019–2024: search-space AutoML; LLM agents as recommenders/simulators (2023–).
- 2023–2025: general program evolution (FunSearch → AlphaEvolve → OpenEvolve/Shinka) and MLE agents/benchmarks.
- 2025: OneRec/SPRec/Rec-R1 make weight-level self-improvement mainstream in generative rec; AutoRecLab call.
- Feb 2026: first code-level systems (Google/YouTube 2602.10226, Self-EvolveRec 2602.12612, AgentLTV).
- Mar–Oct 2026: industrial wave (Meta REA, AgentX family, NOVA, EvoRec/Astar, AutoLR, RecSys Factory, SR-Agent,
  A-MLE, AURA, RecEvolve), open harnesses (RecHarness, RankEvolve), first component-level search over semantic IDs,
  first in-paper benchmarks; first papers about the *reliability* of these loops (RankEvolve, Trajectories→Evidence).
