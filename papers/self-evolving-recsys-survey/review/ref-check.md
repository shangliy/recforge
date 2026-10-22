# Reference and claim check: `draft/paper.tex` + `refs.bib`

Checked 2026-10-22. Nothing in `refs.bib`, `manual.bib` or `paper.tex` was edited.

**Line numbers.** `paper.tex`, `refs.bib` and `manual.bib` changed while this review was running (09:55: figures added and a new citation `yang2026ideationgoodhart`). All line numbers below refer to the snapshot taken at 10:00 (665 lines, md5 `23722565c24143ccc7c74eeb54f0630b`; copy at `/tmp/claude-1000/-home-shawnyang-Documents-2026-agent-newsroom/30ea0f8c-b5c4-4bcd-83b5-845d76320543/scratchpad/paper.snapshot.tex`). Each claim row also quotes the current text, so it can be found again with grep.

**Scripts** (all in `review/`, run from the survey root):

| Script | What it does |
|---|---|
| `bibparse.py` | brace-aware BibTeX parser |
| `check_bib.py` | finds cited/uncited/missing keys, duplicates and malformed fields; writes `bib_static.json` |
| `fetch_meta.py` | queries the arXiv API in batches of ≤50 with 3 s between calls; writes `meta.json` |
| `fetch_s2_batch.py` | one Semantic Scholar batch POST (the per-paper endpoint returned HTTP 429 continuously) |
| `fetch_crossref.py` | looks up the DOI, or else an exact title, in Crossref |
| `compare_meta.py` | compares bib fields with the arXiv record; writes `meta_report.json` |
| `upgrades.py` | builds the published-version table; writes `upgrades.md` |

**Claim checks.** Every sentence that carries a `\cite` was checked against the full text: arXiv HTML for all audited systems and comparison points, the arXiv HTML or PDF for surveys and any sentence with a number, a quote or a strong claim, and the abstract for the remaining L4 and background citations. Per-paper working notes with more quotes are in the scratchpad (`claims/A.md` … `claims/E.md`).

---

## 1. Summary counts

### Bibliography (Part 1)

**Entries.**
- `refs.bib` has 155 entries: 148 arXiv entries plus 7 manual entries. At the start there were 154; `yang2026ideationgoodhart` was added at 09:55.
- 112 keys are cited in `paper.tex`.
- Cite keys missing from `refs.bib`: **0**.
- Entries never cited: **43** (list in §2c).
- Duplicate keys: **0**.
- Duplicate works under two keys: **0**. I checked by eprint, DOI and normalised title. Related but distinct works:
  - `beel2025autoreclab` (position paper) vs `baumgart2026autoreclab` (demo).
  - `deng2025onerec`, `zhou2025onerectech` and `zhou2025openonerec` (three distinct reports).

**arXiv entries against the arXiv API.**
- Title, full author list and year agree for all 148: **0 mismatches**.
- Two titles were hand-edited for TeX (`Harness$^2$`, `$\tau$-Rec`). Both are correct.

**Metadata errors.**
- **4 in non-arXiv entries**: `meta2026rea` (wrong title); `romeraparedes2023funsearch` (truncated author list, wrong URL, missing volume/pages/DOI); `krichene2020sampled` and `roelofs2019metaanalysis` (missing fields; they cause the 6 BibTeX warnings).
- **2 optional title notes** on arXiv entries (§2a).

**Malformed BibTeX.**
- Unescaped `& % _ #`: **0**.
- Unbalanced braces: **0**.
- Every title is double-braced (`{{...}}`), so acronym capitalisation (LLM, CTR, HSTU, OneRec, BERT4Rec, …) is preserved in all of them.
- **10 entries** have raw UTF-8 letters in author names. They compile with `inputenc`/`T1`, but they should be TeX-escaped for ACM TAPS: `novikov2025alphaevolve` (Ngân Vũ), `nam2025mlestar` (Sercan Ö. Arık), `lou2026autoharness`, `hidasi2023flaws` (Balázs Hidasi, Ádám Czapp), `anelli2021elliot`, `chan2024mlebench`, `palumbo2026spotify`, `skrlj2025agent0`, `koralewski2026promptpack`, `zhou2026mofa`.

**Published versions.**
- **59** arXiv entries have a published version with a Crossref record; **39 of these are cited**.
- **10 more cited entries** have a venue confirmed only by the arXiv comment or Semantic Scholar.
- That makes **49 cited arXiv entries** that should cite the published version. See §3.

### Claims (Part 2)

**Sentences or table cells checked:** about 260, covering 101 cited works plus the meta blog. Every source was reached.

**Results:**

| Verdict | Count | Meaning |
|---|---|---|
| **Errors** | **24** (5 table/taxonomy T-1–T-5, 19 text C-1–C-19) | Wrong, unsupported by the cited source, or a quote that is not verbatim. |
| **Imprecise** | **35** (T-7–T-10, I-1–I-32) | Supported in substance, but a number, scope or qualifier differs from the source. |
| **Internal inconsistencies** | **3** (T-6, X-1, X-2) | Text, table and CSV disagree. |
| OK | The rest | |

The errors include **one structural error**: the audit table embedded in `paper.tex` is stale in 13 rows.

**Round-1 rechecks:**
- Of the 9 fixes, 7 are correctly reflected in the text.
- **#1 (Population Evolution)** and **#9/#5 (codes)** were fixed in `audit.csv`/`audit_rows.tex` but **not in the table printed in `paper.tex`**.
- **#2 (RecEvolve in-batch)** was fixed in F1 but **not in the intro**, at line 88.
- Round-1's EvoRank recommendation ("code EvoRank's three caught leakage bugs") rests on a misreading of the source. See C-3.

---

## 2. Metadata errors and exact fixes

### 2a. Field errors

| Key | Problem | Source checked | Exact fix |
|---|---|---|---|
| `meta2026rea` | **Title wrong.** The bib has "…: An Autonomous AI System Accelerating Meta Ads Ranking Innovation". | Page `<title>`/`og:title` at the cited URL. Date 17 Mar 2026 and URL confirmed. | `title = {{Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta's Ads Ranking Innovation}}` |
| `romeraparedes2023funsearch` | **Problems:** author list truncated with `and others`; `url` points to GitHub, not the paper; volume, number, pages and DOI missing; BibTeX warns about missing number/volume/pages. | Crossref 10.1038/s41586-023-06924-6 | `author = {Bernardino Romera-Paredes and Mohammadamin Barekatain and Alexander Novikov and Matej Balog and M. Pawan Kumar and Emilien Dupont and Francisco J. R. Ruiz and Jordan S. Ellenberg and Pengming Wang and Omar Fawzi and Pushmeet Kohli and Alhussein Fawzi}, journal = {Nature}, volume = {625}, number = {7995}, pages = {468--475}, year = {2024}, doi = {10.1038/s41586-023-06924-6}, url = {https://doi.org/10.1038/s41586-023-06924-6}`. Published online 14 Dec 2023; issue dated 18 Jan 2024. Either year is defensible, but keep `romeraparedes2023` only if you keep 2023. |
| `krichene2020sampled` | Pages, publisher and DOI missing. BibTeX warns: empty publisher, empty address, no pages. | Crossref 10.1145/3394486.3403226 (title and both authors match) | Add `pages = {1748--1757}, publisher = {ACM}, address = {New York, NY, USA}, doi = {10.1145/3394486.3403226}`. Optionally `url = {https://doi.org/10.1145/3394486.3403226}`. |
| `roelofs2019metaanalysis` | Volume and publisher missing (BibTeX warnings); the URL is a legacy redirect. | NeurIPS proceedings page and official BibTeX (title and 7 authors match) | `booktitle = {Advances in Neural Information Processing Systems}, volume = {32}, publisher = {Curran Associates, Inc.}, year = {2019}, url = {https://proceedings.neurips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html}`. The official BibTeX has `pages = {}`, so no page range can be verified. Leave pages out and accept the ACM-style warning. |
| `li2026autorecsys` (optional) | The arXiv metadata title, which matches the bib, ends "…Recommender System". The PDF/HTML title says "…Recommender Systems". | arXiv API v1 vs HTML | Optional: keep the arXiv record title, or use the paper's own title. Not an error against the arXiv record. |
| `mu2026evorec` (optional) | arXiv metadata says "Self Evolving"; the paper's title says "Self-Evolving". | arXiv API v1 vs HTML | Optional: `{{EvoRec: Self-Evolving Agentic Recommender Systems}}` |

**Entries verified with no field error:**
- `openevolve`: repo answers HTTP 200 at github.com/algorithmicsuperintelligence/openevolve.
- `recforge`: HTTP 200.
- `yang2026ideationgoodhart`: repo answers HTTP 200. Its claim in the text is wrong; see C-7.

### 2b. Non-ASCII author names (formatting; compiles today)

Replace with TeX escapes for ACM submission:
- `Ngân Vũ` → `Ng{\^a}n V{\~u}`
- `Sercan Ö. Arık` → `Sercan {\"O}. Ar{\i}k`
- `Balázs Hidasi and Ádám Czapp` → `Bal{\'a}zs Hidasi and {\'A}d{\'a}m Czapp`
- The others in the same way.

### 2c. Uncited entries (43)

Delete these, or cite them. They are harmless for `bibtex`, since only cited entries are printed.

`zhang2026agenticrs, thakur2026feature, barlier2026feature, song2019autoint, wang2020autorec, jawahar2024llmpp, schmidgall2025agentlab, wong2025confucius, liu2024agenthpo, zhang2023llmhpo, trirat2024automlagent, guo2024dsagent, li2024autokaggle, wang2023recmind, huang2023interecagent, liu2023recprompt, wang2024re2llm, xu2025iagent, rendle2019sampled, fan2023movielens, zhao2022recbole2, shang2025agentrecbench, huang2025recbenchplus, huang2023mlagentbench, wijk2024rebench, sun2019bert4rec, hu2026rethinking, liu2026bianque, chen2026covemem, cai2024afl, wang2025srlf, liu2025dgdpo, zhuang2026evoreason, ou2026recpilot, lin2026lion, ishida2026qdrec, skrlj2025agent0, koralewski2026promptpack, zhou2026mofa, wang2025ruleagent, hao2026lattearena, maragheh2025future, huang2025multimodalagentic`

Some of these could support existing sentences:
- `rendle2019sampled`: the timeline figure's 2019 "Sampled-metric critique" box has no 2019 citation in the text.
- `sun2019bert4rec`: line 201 names BERT4Rec without citing it.

---

## 3. Published-version upgrades (cited entries)

Confirmed by Crossref DOI, or by exact title match where marked. Convert `@misc` to `@inproceedings`/`@article` with these values. The year is the publication year, which differs from the arXiv year in several cases. The full table, including the uncited entries, is in `review/upgrades.md`.

| Key | Published in | Year | Vol(no) / pages | DOI | Note |
|---|---|---|---|---|---|
| **wang2026selfevolving** | Proc. 20th ACM RecSys | 2026 | 1462–1470 | 10.1145/3773078.3831919 | Audited core system |
| **pan2026recevolve** | Proc. 20th ACM RecSys | 2026 | 1437–1442 | 10.1145/3773078.3831898 | Audited core system |
| palumbo2026spotify | Proc. 20th ACM RecSys | 2026 | 994–1003 | 10.1145/3773078.3831910 | Published name "Benjamin Lacker" (arXiv: "Ben Lacker") |
| baumgart2026autoreclab | Proc. 20th ACM RecSys (Demo) | 2026 | 1790–1792 | 10.1145/3773078.3841273 | **Published title differs:** "AutoRecLab: An Autonomous Recommender Systems Lab" |
| narasimhan2026taurec | Proc. 20th ACM RecSys (Repro.) | 2026 | 915–919 | 10.1145/3773078.3831847 | |
| nian2026rankevolveir | Proc. 49th ACM SIGIR | 2026 | 4028–4033 | 10.1145/3805712.3809962 | |
| chen2026memrec | Proc. 64th ACL (Long) | 2026 | 44515–44544 | 10.18653/v1/2026.acl-long.2061 | Title match; author "Mingxuan Ju" (arXiv "Clark Mingxuan Ju") |
| liu2025recoworld | Companion Proc. ACM Web Conf. 2026 | 2026 | 650–659 | 10.1145/3774905.3794661 | |
| zhang2025agentsearchsurvey | ACM TOIS | 2026 | article 3842663 | 10.1145/3842663 | |
| peng2025agentsurvey | Findings of EMNLP 2025 | 2025 | 11574–11583 | 10.18653/v1/2025.findings-emnlp.620 | **Published version has 6 authors** (adds Jian Yang between Hua Huang and Qing Yang) |
| liu2025agentcfpp | Proc. 48th ACM SIGIR | 2025 | 2566–2571 | 10.1145/3726302.3730161 | |
| gao2024sprec | Proc. ACM Web Conf. 2025 | 2025 | 5075–5084 | 10.1145/3696410.3714524 | |
| wang2023recagent | ACM TOIS 43(2) | 2025 | 1–37 | 10.1145/3708985 | **Published title "User Behavior Simulation with Large Language Model-based Agents"; 15 authors** (adds Hao Sun; "Xin Zhao" = Wayne Xin Zhao) |
| nam2025mlestar | NeurIPS 38 | 2025 | 129290–129310 | 10.52202/085713-3889 | |
| toledo2025aira | NeurIPS 38 | 2025 | 39717–39756 | 10.52202/085713-1186 | |
| zhang2025mlrcbench | NeurIPS 38 (Datasets & Benchmarks) | 2025 | 100801–100845 | 10.52202/085713-3036 | |
| zhang2024agentcf | Proc. ACM Web Conf. 2024 | 2024 | 3679–3689 | 10.1145/3589334.3645537 | |
| wang2024macrec | Proc. 47th ACM SIGIR | 2024 | 2760–2764 | 10.1145/3626772.3657669 | |
| zhang2023agent4rec | Proc. 47th ACM SIGIR | 2024 | 1807–1817 | 10.1145/3626772.3657844 | |
| zhang2024dnsrec | Proc. 18th ACM RecSys | 2024 | 591–600 | 10.1145/3640457.3688117 | |
| zhang2023nasrec | Proc. ACM Web Conf. 2023 | 2023 | 1199–1207 | 10.1145/3543507.3583446 | |
| ji2020leakage | ACM TOIS 41(3) | 2023 | 1–27 (art. 75) | 10.1145/3569930 | Year 2023, not 2020 |
| sun2022daisyrec | IEEE TPAMI 45(7) | 2023 | 8206–8226 | 10.1109/TPAMI.2022.3231891 | |
| zheng2022automl | ACM TOIS | 2023 | article 3579355 | 10.1145/3579355 | |
| hidasi2023flaws | Proc. 17th ACM RecSys | 2023 | 848–855 | 10.1145/3604915.3608839 | |
| klenitskiy2023dross | Proc. 17th ACM RecSys | 2023 | 1120–1125 | 10.1145/3604915.3610644 | |
| petrov2022bert4rec | Proc. 16th ACM RecSys | 2022 | 436–447 | 10.1145/3523227.3548487 | |
| li2022autolossgen | Proc. 45th ACM SIGIR | 2022 | 1304–1315 | 10.1145/3477495.3531941 | |
| zhu2022bars | Proc. 45th ACM SIGIR | 2022 | 2912–2923 | 10.1145/3477495.3531723 | |
| zhao2021recbole | Proc. 30th ACM CIKM | 2021 | 4653–4664 | 10.1145/3459637.3482016 | |
| zhu2021fuxictr | Proc. 30th ACM CIKM | 2021 | 2759–2769 | 10.1145/3459637.3482486 | |
| anelli2021elliot | Proc. 44th ACM SIGIR | 2021 | 2405–2414 | 10.1145/3404835.3463245 | |
| zhao2020autoemb | 2021 IEEE ICDM | 2021 | 896–905 | 10.1109/ICDM51629.2021.00101 | Title match. **Published version has 10 authors:** Xiangyu Zhao, Haochen Liu, Wenqi Fan, Hui Liu, Jiliang Tang, Chong Wang, Ming Chen, Xudong Zheng, Xiaobing Liu, Xiwang Yang. Crossref misspells "Zhaok". |
| song2020autoctr | Proc. 26th ACM KDD | 2020 | 945–955 | 10.1145/3394486.3403137 | |
| liu2020autofis | Proc. 26th ACM KDD | 2020 | 2636–2645 | 10.1145/3394486.3403314 | |
| meng2020splitting | Proc. 14th ACM RecSys | 2020 | 681–686 | 10.1145/3383313.3418479 | |
| rendle2020ncf | Proc. 14th ACM RecSys | 2020 | 240–248 | 10.1145/3383313.3412488 | |
| dacrema2019progress | Proc. 13th ACM RecSys | 2019 | 101–109 | 10.1145/3298689.3347058 | |
| kang2018sasrec | IEEE ICDM 2018 | 2018 | 197–206 | 10.1109/ICDM.2018.00035 | |

**Venue confirmed only by the arXiv comment or Semantic Scholar** (no Crossref record; pages not verified):
- `zhai2024hstu` → ICML 2024 (PMLR 235).
- `rajput2023tiger` → NeurIPS 2023 (vol. 36).
- `chan2024mlebench` → ICLR 2025 (arXiv comment: "ICLR version").
- `lin2025recr1` → TMLR 2025.
- `gao2025selfevolvingsurvey` → TMLR, 01/2026.
- `zhang2026rsir` → ICML 2026 (accepted).
- `dwork2015reusable` → NeurIPS 2015 (vol. 28).
- `blum2015ladder` → ICML 2015, PMLR 37, pp. 1006–1014 (pages per Semantic Scholar).
- `azhar2026coral` → RecSys '26 OARS workshop.
- `kim2026aura` → GenAIECommerce'26 workshop at RecSys 2026.

Workshop papers may reasonably stay as arXiv citations.

**Caution for audited systems.** RecEvolve and the Google/YouTube loop now have RecSys 2026 versions. The audit coded the arXiv version (Threats §9 says so). Either cite the arXiv version explicitly as the coded version, or re-check the published text before switching.

---

## 4. Claim errors

Columns: line in the 10:00 snapshot | current text | what the source says (quote, section) | proposed text. **E** = error, **I** = imprecise, **X** = internal inconsistency.

### 4a. Audit table and taxonomy (structural)

| # | Line | Current | Source / evidence | Fix |
|---|---|---|---|---|
| T-1 **E** | 397–427 (`%BEGIN/END-AUDIT-ROWS`) | **The embedded table is stale.** 13 rows differ from `draft/audit_rows.tex` and `audit.csv`, which carry the round-1 fixes. As printed, it contradicts the abstract ("one selects on its test leaderboard"), F1 ("Four report ranking metrics without saying…"), F2, F3 and F7 ("two core systems… five say nothing"). | Every disputed cell was re-verified against the source, and every one supports the CSV. See the cell list below. | Replace the block with `\input{audit_rows}` (or paste `draft/audit_rows.tex`) after applying T-3. |
| T-2 **E** | 418 | `Population Evolution~\cite{peng2026population}, Astar~\cite{hu2026astar} & … & test & \no & … & \ns` | The PE paper never mentions Astar, and Astar has its own row (409). The PE row should read C2 = NS, C3 = P, C9 = P: "the implementation must pass the causal-leakage check, for a run to be valid" (2610.05950 App. A). | `Population Evolution~\cite{peng2026population} & L2 & Full & \ns & \pa & \no & \yes & \pa & \yes & \pa & \no & later \\`. The `Astar` next to PE at line 260 (taxonomy S4 column) is correct. |
| T-3 **E** | 389 (caption `\yes{}+G`), EvoRank row; CSV `Y+caught` | EvoRank C9 coded as isolation plus leakage "caught by an audit" (round-1 #F7). | 2609.22196 §3.4/§5: the three target-encoding bugs came from building the authors' own hand-built candidate for the headroom gate, "run before any LLM spend: one hand-built candidate must beat the fitness fold's noise floor"; "The audit caught each bug before any search depended on it." The loop did not produce them. | Code EvoRank C9 = `Y`. Drop `\yes{}+G` from the caption. |
| T-4 **E** | 261 | Meta REA (blog) placed in column **S5 online A/B (primary)** | The blog never mentions online/A-B/traffic. Its result is offline: "REA-driven iterations doubled average model accuracy over baseline across six models" (meta2026rea). | Move REA to S2/S3 (signal not stated), or mark "(blog; signal not stated)". |
| T-5 **E** | 252 | `AutoCTR~\cite{song2020autoctr}, AutoLossGen~\cite{li2022autolossgen}` without † | Official code exists at github.com/facebookresearch/AutoCTR (README names the KDD paper) and github.com/rutgerswiselab/AutoLossGen, which the abstract links: "Source code of the work is available at …". Both answer HTTP 200. | `AutoCTR\textsuperscript{\dag}~\cite{song2020autoctr}, AutoLossGen\textsuperscript{\dag}~\cite{li2022autolossgen}` |
| T-6 X | 253 vs 407 | AutoLR is in the L1 row of the taxonomy but coded L1+L2 in the audit | 2609.04871 §3.1: "π_t is the repository-grounded code patch implementing the proposal" | Add AutoLR to L2 × S2/S3 as well. |
| T-7 I | 262, 324 | Evolving Semantic Indexes appears in the L3 row with no "comparison" marker, under "Components of generative recommenders" | 2610.28568 §1: "Generative retrieval (GR) casts document retrieval as an autoregressive generation task". §6 counts it as a comparison point. | Add `\emph{comparison:}` in the taxonomy; at line 324 write "Evolving Semantic Indexes, a generative document-retrieval system we treat as a comparison point, runs …". |
| T-8 I | 266 | "prompts and logic: Spotify" | 2609.30297 §3.2: "a coding agent equipped with read–write access to the prompt artifacts (e.g., system prompt, few-shot examples, tool descriptions)" | "prompts and tool descriptions: Spotify" |
| T-9 I | EvoRank row C1 = Full | EvoRank re-ranks the shown list of hotels for each query (learning to rank). This is not full-catalogue ranking. | 2609.22196 §3 | Code C1 = `other` (or LTR). This does not change any core count. |
| T-10 I | `audit.csv` online column | NOVA, CORAL and AgenticRecTune are coded "CI" but report significance only, with no intervals. GEARS does report ± intervals. | NOVA §5.7 "statistically significant"; CORAL Table 1; AgenticRecTune §5.1 "p-value < 0.05" | Rename the value `sig`. The text's "eight report significance or confidence intervals" still holds. |

**Cells that differ between the T-1 table and the CSV.** The source supports the CSV in every case.

| System | Cell | Table in `paper.tex` | CSV | Source |
|---|---|---|---|---|
| Self-EvolveRec | C1 | S99 | Sampled | Undefined legend code |
| RecHarness | C1 | S99 | Sampled | Undefined legend code |
| RecHarness | C8 | \no | NS | Base tuning not described |
| EvoRec | C1 | LOO? | Rank? | |
| VirtualMLE | C1 | LOO? | Rank? | |
| Astar | C1 | LOO? | Rank? | 2608.27287 reports Hitrate@200 and never mentions leave-one-out |
| RecEvolve | C1 | S99 | Rank? | 2609.01622 never states the evaluation candidate set |
| NOVA | C9 | \ns | P | §1, target-leakage gate |
| AgentX | C9 | \ns | P | §6.2, "engineering whitelist" |
| Auto-RecSys | C2/C3 | \ns | \na | No offline claim |
| A-MLE | C9 | G | P | No inflation or leakage reported; sandboxed codebase |
| EvoSkillRec | C8 | \no | P | |
| Population Evolution | row | see T-2 | | |
| EvoRank | C9 | \yes | — | Plain `\yes` happens to be right (see T-3) |

### 4b. Text claims

| # | Line | Current text | Source says | Proposed text |
|---|---|---|---|---|
| C-1 **E** | 88 | "RecEvolve's agent inflated an in-batch-negative metric by shrinking the batch size" | 2609.01622 §5.2: "drastically reducing the batch size (from 8k down to 1k) artificially inflated proxy metrics. Because the Two-Tower model utilizes in-batch negative sampling…". The evaluation candidate set is never stated (round-1 #2; F1 at 435 already hedges). | "RecEvolve's agent inflated its proxy metrics by shrinking the batch size, and with it the number of in-batch negatives~\cite{pan2026recevolve}" |
| C-2 **E** | 87–90 | "The agent also controls the code that produces its score. Two of the systems … did exactly this: … an AI co-scientist … produced ``metric-winning bugs'' such as silently growing the model" | 2603.22376 §5, Lesson 3: "The agent occasionally produced implementations that improved ℳ while being wrong (e.g., silently increasing model size)". A model-capacity confound is not tampering with the scorer. | "…Two of the systems we read report that their agent won on the metric without a real improvement: RecEvolve's agent … and an AI co-scientist for search ranking produced implementations that ``improved ℳ while being wrong (e.g., silently increasing model size)''~\cite{wu2026coscientist}." |
| C-3 **E** | 488, 496–497 | "Two core systems and two comparison points report metric inflation or target leakage produced by the loop itself … EvoRank's audit caught three target-encoding leakage bugs" | See T-3: the bugs came from the hand-built headroom-gate candidate, "before any LLM spend", and "The audit caught each bug before any search depended on it" (2609.22196 §3.4, §5). | "Two core systems and one comparison point report …". Then: "EvoRank's pre-search audit caught three target-encoding leakage bugs in the authors' own hand-built candidate before any search used it~\cite{patel2026evorank}, an example of prevention." |
| C-4 **E** | 497–498 | "the search co-scientist produced ``metric-winning bugs (e.g., silently increasing model size)''" | **Not a verbatim quote.** It splices the heading "Lesson 3: metric-winning bugs make code audit non-optional." to the sentence "improved ℳ while being wrong (e.g., silently increasing model size)" (2603.22376 §5). | "the search co-scientist produced implementations that ``improved ℳ while being wrong (e.g., silently increasing model size)''~\cite{wu2026coscientist}" |
| C-5 **E** | 319, 445 | "A Trip.com co-scientist for **hotel** search ranking"; "the **hotel**-search co-scientist" | "hotel" appears 0 times in 2603.22376 (v1 and v2). Abstract: "production search-ranking system of a large online travel platform"; affiliation Trip.com Group. | "travel search ranking"; "the travel-search co-scientist" |
| C-6 **E** | 620 | "Combining the two with pre-registered online confirmation of the final candidate, as Sortify does" | 2603.27765 has no "pre-regist…" or "pre-specif…" anywhere. §5: "the decisions to freeze R7 parameters, conduct 7-day static A/B testing, and approve production rollout were all made by human operators". §4.8.4: 7-day A/B, "10% treatment vs. 20% control". Table 10 gives point differences only. | "Combining the two with a fresh online confirmation of the final candidate, as Sortify does with a seven-day re-test, ideally pre-registered, is a starting point." (R9 at line 549 does not mention Sortify and is fine.) |
| C-7 **E** | 353–357 | "…on two hypothesis spaces with measured ground truth and **for both Claude and GPT models**~\cite{yang2026ideationgoodhart}" | The cited repo's REPORT.md, claim A, covers "2 个公开空间 × 2 个生成模型" ("2 public spaces × 2 generation models") = **Sonnet and Opus**. Judge scores rose (Sonnet 7.5→8.2, Opus 8.2→8.9) and precision fell (Sonnet .79→.43, Opus .87→.28; HPOBench Sonnet .82→.43, Opus .90→.42). GPT models appear only in a preliminary prior-agreement probe (Q1), and §Threats says "先验面板只有 3 个 Claude 系模型" ("the prior panel contains only 3 Claude-family models"). | "…on two hypothesis spaces with measured ground truth and for two Claude models (Sonnet and Opus)~\cite{yang2026ideationgoodhart}". This is a self-citation to an unreviewed repo; consider saying so. |
| C-8 **E** | 335 | Memory and reflection methods update user and item agents "(AgentCF, AgentCF++, **MACRec**)" | 2402.15235 abstract: "Unlike existing work on using agents for user/item simulation, we aim to deploy multi-agents to tackle recommendation tasks directly"; roles are Manager, User/Item Analyst, Reflector, Searcher and Task Interpreter. §3.2.2: the Reflector steps in "when the Manager is about to perform the second or more runs on the same task input". Nothing persists across interactions. | Remove MACRec from the list (it is not self-improving), or add a separate clause: "MACRec adds a Reflector agent that critiques a manager agent's answer within a task~\cite{wang2024macrec}". |
| C-9 **E** | 201 | "a loss change alone can reorder SASRec and BERT4Rec~\cite{klenitskiy2023dross,petrov2022bert4rec}" | Petrov & Macdonald (2207.07483, abstract): the original results replicate "if training for a much longer amount of time (up to 30x)". The paper is about training length and implementations; it never changes the loss. Klenitskiy supports the clause. | "a loss change alone can reorder SASRec and BERT4Rec~\cite{klenitskiy2023dross}, and BERT4Rec's reported advantage depends on much longer training~\cite{petrov2022bert4rec}" |
| C-10 **E** | 203–205 | "and the split choice changes rankings~\cite{meng2020splitting, hidasi2023flaws}" | Hidasi & Czapp §2.3: leave-one-out and random splits "inherently enable information leaking through time". §2.4: "the bias introduced by negative sampling can change the ordering of models". The paper does not show split choice reordering models. | "…can reverse model rankings~\cite{krichene2020sampled,hidasi2023flaws}; leave-one-out splits … leak future information~\cite{ji2020leakage,hidasi2023flaws}, and the split choice changes rankings~\cite{meng2020splitting}." |
| C-11 **E** | 522 | "Kaggle limits submissions and teams submit few, diverse models" (follows the Roelofs citation) | Not in Roelofs, which partly contradicts it: the analysis keeps competitions "with at least 1,000 submissions" (§2.3), and "numerous practitioners repeatedly evaluated their progress against a holdout set" (abstract). Rate limits appear in Blum & Hardt: "limiting … the rate of re-submission". | "Kaggle caps the rate of resubmission~\cite{blum2015ladder}, and its leaderboards are probed by many teams with a wide range of model families~\cite{roelofs2019metaanalysis}, whereas an agent loop evaluates hundreds of correlated candidates …" |
| C-12 **E** | 492 | "and DPO negatives derived from the target" | 2609.39551 App. I.1: "one training-overlap flaw in the preference-pair mining (iter 4)". App. H.4 fix: "rejecting items mined only from internal positions, never the held-out target". The flaw is pairs mined at the held-out target position. | "and DPO preference pairs mined at the held-out target position (a training-overlap flaw)" |
| C-13 **E** | 491 | "a multi-position evaluation that inflated NDCG@10 from 0.2192 to 0.2577" | App. H.4: "Apparent 'gains' from naive multi-position eval were leakage (inflating 0.2192 to 0.2517/0.2577 at ignore_last_n=1/2). An argument rather than a sweep turned a tempting idea into a negative result; the one measured run agrees (≈0.2190…)". The value is incomplete, and the inflation was not something the loop produced and accepted. Round-1 #3 asked for both values. | "a naive multi-position evaluation that would have inflated NDCG@10 from 0.2192 to 0.2517/0.2577 (ignore_last_n = 1/2), which was reasoned out as leakage" |
| C-14 **E** | 492–493 | "These surfaced as anomalous trajectories on the leaderboard and were diagnosed before being reported as gains" | App. I.1: "the genre and DPO bugs surfaced not from a failed unit test but as anomalous metric trajectories". Only 2 of the 3 issues surfaced this way; the third was reasoned out (H.4). | "The genre and DPO bugs surfaced as anomalous trajectories on the leaderboard, the multi-position inflation was reasoned out, and none was reported as a gain, but …" |
| C-15 **E** | 369 | RecSys Factory "(an operations platform with human approval of every change)" | 2608.11241: the HITL approval card covers the ChatOps DAG's remediation overrides ("the Analyzer proposes an override, the operator decides", §1). It is "reported here from an 8-day 16-run pilot" (abstract). The same platform runs an autonomous loop that "self-triggers via the Claude Code Stop hook" (§3), "a 196-round campaign" (abstract). Code review is a team convention, "not as production hard gates" (§1). | "(an operations platform in which an operator approves the agent's proposed overrides through human-in-the-loop cards)" |
| C-16 **E** | 498–499 | Under F7 ("Agents find shortcuts"): "RecSys Factory found a join bug that ``silently corrupted all downstream training samples''" | The quote is verbatim, but the context is wrong. §6.1: "an upstream dimension table had multi-row entries … causing the LEFT JOIN to produce 2–3× row duplication. The bug had silently corrupted all downstream training samples for the prior modeling cycle." It was a pre-existing data bug that the platform's diagnostics uncovered, not an agent shortcut. | Move to a data-integrity sentence: "RecSys Factory's diagnostics uncovered a pre-existing upstream join bug that had ``silently corrupted all downstream training samples''". Keep AURA: "AURA's agent fabricated 904 session identifiers in its diagnostic stage". |
| C-17 **E** | 330 | "No open system yet evolves TIGER- or OneRec-style components under a shared protocol." | 2610.28568 §2.1: "Our seed program combines RQVAE-based SID construction with TIGER-style collision handling". The sentence holds only because that system releases no code and targets document retrieval. | "Evolving Semantic Indexes evolves TIGER-style semantic-ID components for document retrieval but releases no code; no open system yet does so for recommendation under a shared protocol." |
| C-18 **E** | 133 | "Search and ranking systems outside recommendation (learning to rank, lexical retrieval) are included as comparison points" | The audit has five comparison points (line 365: LTR, search ranking, lexical retrieval, generative document retrieval, LTV prediction). AgentLTV (2602.21634) is LTV prediction, which is neither search nor ranking. | "Systems outside recommendation (learning to rank, search ranking, lexical retrieval, generative document retrieval and lifetime-value prediction) are included as comparison points …" |
| C-19 **E** | 100–101 | the roadmap "mentions the ``agent as engineer'' direction in one clause~\cite{lin2026roadmap}" | 2607.04433 has two mentions: §3 Governance bullet, "leveraging agent as engineer to update the recommendation strategies"; and §3.3, "Optimization planning leverages LLM agents to automatically diagnose algorithm limitations and update the recommendation strategies/pipelines iteratively Lao et al. (2026); Wang et al. (2026a)". | "…mentions the ``agent as engineer'' direction only in passing, in two sentences that cite AgentX and the Google loop~\cite{lin2026roadmap}" |

#### Imprecise claims (scope, qualifier or number differs from the source)

| # | Line | Current | Source | Proposed |
|---|---|---|---|---|
| I-1 | 78–80 | "…within months, open harnesses such as RecHarness … and systems at Meta, …, NetEase and others." | Grammar: the round-1 edit left the clause with no verb. | "…and others followed." |
| I-2 | 103–104 | "RMD-Bench and ExecML-HSTU each fix one setting" | RMD-Bench spans "ranking, watch-time prediction, RL algorithm discovery, and LLM/VLM pretraining" (2610.05950 abstract). ExecML-HSTU scores whether agents' code edits execute correctly (2609.39551 §4); it does not compare evolvers. | "RMD-Bench fixes protocols for cross-dataset and cross-scale discovery and ExecML-HSTU measures whether agents' edits execute correctly, but no shared benchmark yet compares evolvers …" |
| I-3 | 72 | "embedding search for click-through-rate (CTR) models~\cite{…,zhao2020autoemb,…}" | AutoEmb is evaluated on "Movielens-20m, Movielens-latest and Netflix Prize data" with MSE and accuracy (§3.1), which is not CTR. | "…for recommendation models, mostly CTR prediction~\cite{…}" |
| I-4 | 177 | DNS-Rec among "whole architectures with weight sharing" | 2402.00390: "tailor compact network architectures for attention-based SRS models"; DARTS-style supernet pruning "in both depth and width dimensions" | "…whole architectures with a weight-sharing supernet (NASRec), compact attention-based sequential models under resource constraints (DNS-Rec)…" |
| I-5 | 179 | "Evaluation is mostly validation logloss or AUC on public CTR data" | True for 4 of the 7 methods cited (AutoCTR, AutoFIS, AutoDim, NASRec). AutoEmb uses ratings with MSE; DNS-Rec and AutoLossGen use ranking on ML/Amazon/Gowalla. | "…mostly validation logloss/AUC on public CTR data, or standard rating and sequential benchmarks, with fixed splits" |
| I-6 | 196 | OneRec "further aligned by iterative preference optimisation on its own samples~\cite{deng2025onerec,zhou2025onerectech,zhou2025openonerec}" | Only 2502.18965 uses iterative DPO on beam samples. The tech report uses on-policy RL ("Early Clipped GRPO", §2.4), and OpenOneRec uses GRPO (§5.3). | "…aligned on its own samples, first by iterative DPO~\cite{deng2025onerec} and then by on-policy RL~\cite{zhou2025onerectech,zhou2025openonerec}" |
| I-7 | 283 | Sortify "adjusts the exchange rates … with Optuna inside an LLM meta-controller" | §2.1: Optuna TPE is the inner layer (5,000 trials). The LLM adjusts "transfer function intercepts and penalty multipliers rather than low-level search parameters". | "Sortify searches the exchange rates of a sorting formula with Optuna, while an LLM meta-controller recalibrates the search's offline-to-online transfer intercepts and penalties" |
| I-8 | 299 | Population Evolution "screens candidates on small subsets" | Abstract: "For expensive targets, PE searches small training subsets". That is the LLM/VLM track; the recommendation track screens on peer datasets. | "screens candidates on peer datasets (and, for LLM/VLM targets, on small training subsets)" |
| I-9 | 305 | "Industrial systems share a two-stage design: … online experiments decide launches" | A-MLE and Auto-RecSys report no online experiment (2609.08248 results; 2609.10922 §4). | "Most industrial systems share …" |
| I-10 | 307 | Google "promotes on validation loss and then on north-star A/B metrics" | 2602.10226 §4.1.1: the reward persona "cannot use compute_loss. Instead, it relies on the compute_eval tool to calculate a proxy metric". | "promotes on validation loss (a correlation proxy for reward changes) and then on north-star A/B metrics" |
| I-11 | 315 | AgentX and AgentX-Model "run research lineages (reproduce, follow up, compose, diagnose)" | The four actions are AgentX-Model's (2609.30001 §3.2.1). AgentX (2606.26859) iterates online strategies, plus "reproduction, module ablation, and cross-paper composition". | "AgentX, deployed at Kuaishou, iterates online strategies and model research, and its successor AgentX-Model runs research lineages (reproduce, follow up, compose, diagnose) …" |
| I-12 | 343 | progress can sit in earlier generations "rather than the latest model" | 2610.07105 abstract: "progress may reside in relations between generations as well as in the latest model" | "…can also sit in earlier generations, not only in the latest model" |
| I-13 | 343–344 | Spotify improves "prompts and logic … evaluated on synthetic conversations" | §3.2 prompt artifacts (see T-8). Conversations are scored by an LLM judge (§3.1). | "…prompts, few-shot examples and tool descriptions with a coding agent, evaluated by an LLM judge on synthetic conversations" |
| I-14 | 345–346 | "Environments for training such agents include RecoWorld, Agent4Rec, RecAgent and … τ-Rec" | Agent4Rec is "a user simulator" for "collaborative filtering-based" recommenders. RecAgent is a user-behaviour "sandbox". τ-Rec is a benchmark with "verifiable rewards". Only RecoWorld is a training environment. | "Simulated environments and benchmarks for such agents include RecoWorld~\cite{…}, the user simulators Agent4Rec and RecAgent, and the verifiable τ-Rec benchmark" |
| I-15 | 97–99 | gao2025 has "one paragraph on self-optimised fine-tuning" | 2507.21046 §5.2.2 (SOFT, two sentences). Further passing mentions in §7.2.2 (movie-recommendation task in MemoryAgentBench) and §8.1. The round-1 fix is applied correctly. | "(a two-sentence mention of self-optimised fine-tuning, §5.2.2, and a recommendation task in a benchmark it describes, in~\cite{gao2025…})" |
| I-16 | 434 | "Self-EvolveRec and RecHarness pair each test item with 99 random negatives" | RecHarness: "one positive item and 99 sampled negatives"; it does not say "random". | "…with 99 sampled negatives (random in Self-EvolveRec)" |
| I-17 | 441 | "one selects on training loss and a learned reward model (Astar)" | 2608.27287 §3.2: the loss labels history and trains the reward model, which "ranks candidate directions". Deployment acceptance is "training and offline evaluation" (§3.4), with no split named. | "one ranks candidates with a reward model trained on loss-curve outcomes and accepts by loss decrease (Astar)" |
| I-18 | 443–444 | PE "selects candidates on source instances and reports on others" | PE also headlines source-local gains selected on the same instance: "raises mean best local gains from 7.01% to 8.97% in ranking" (§4.2). | "…selects candidates on source instances (no separate validation split is stated) and also reports transfer to others, but …" |
| I-19 | 453 | Google "runs six independent sessions with confidence intervals, but only for an ablation" | §5.4: "averaged over 6 independent runs"; Table 4 brackets (e.g. "−0.84 [−1.70,−0.01]") are never called confidence intervals; "interval" does not appear. | "…six independent sessions with bracketed ranges (Table 4), but only for an ablation" |
| I-20 | 465 | EvoSkillRec: "the candidate it selects is P1" | The paper reports all five front candidates and names none as selected. P1 has the highest validation AUC (0.92999) and is the one highlighted (App. E.3). | "P1, the front's highest-validation candidate, is also the one that keeps both gains" |
| I-21 | 483 | AgentX-Model: ``Uniform Random's mean exceeds Fixed, Greedy, and Joint'' | §4.5: "In Scenario A, Uniform Random's mean exceeds …"; "no allocation policy consistently led across them" | "…in Scenario A of AgentX-Model's historical replay … ``…'', and no policy led consistently across environments" |
| I-22 | 495 | A-MLE "promoted candidates on a single seed until a re-run rule reduced this" | §6.9: "the agent **sometimes** promoted a candidate based on a single seed when within-run variance warranted re-running; the auto re-run rule materially reduced this". The rule is part of the design (§4.4), not a later fix. | "A-MLE's agent sometimes promoted a candidate on a single seed, which its automatic re-run rule materially reduced" |
| I-23 | 508 | Self-EvolveRec configures all models "with the same untuned hyperparameters" | App. D: "we uniformly configured all recommender models … embedding dimension of 50, a batch size of 128, and a learning rate of 0.001". "Untuned" is not stated. | "…with the same fixed hyperparameters (embedding 50, batch 128, lr 0.001) and does not describe tuning them" |
| I-24 | 516 | AutoLR's "launch-review lifts are … ``descriptive and are not pooled treatment effects''" | Abstract: the values "sum arithmetically to +5.75% … These sums are descriptive and are not pooled treatment effects". The phrase refers to the sums. | "AutoLR's summed launch-review lifts are, in its own words, ``descriptive …''" |
| I-25 | 479 (F6) | NOVA vs Optuna-TPE "at an equal or favourable budget" | §5.3: "matched maximum offline-evaluation budget; LLM inference cost is not matched". Optuna covers six hyperparameters and is "applicable only to L2". | Add: "(matched evaluation budget, unmatched LLM cost; L2 task only)" |
| I-26 | 474 (F5) | Semantic Indexes "ρ = −0.80" | The authors add "n=5; too few programs for a significance claim". | Add "(n = 5)" |
| I-28 | Timeline figure (`figs/timeline.tex`) | RecEvolve placed in Sep 2026 by "month of first arXiv version" | arXiv v1 of 2609.01622 is dated 2026-07-20 (likewise EvoRank 2609.22196 v1 2026-08-30 and RecSys Factory 2608.11241 v1 2026-07-31; both are absent from the figure). | Either say "month of arXiv identifier (announcement)" or move RecEvolve to Jul. All other 23 placements match the v1 month. |
| I-29 | 426 (table) | AgentLTV row C2 = \ns | Evidence leans to test: the discovered program computes its score on test labels (2602.21634 App. D). | Consider C2 = test for AgentLTV (comparison set only; no core count changes). |
| I-30 | Abstract 41–42 / F7 | Co-scientist counted as "metric inflation or target leakage" (C9 = G) | A capacity confound (C-2). | Widen the G legend to "metric-winning bugs, inflation or leakage", or recode. |
| I-31 | 557 (cost) | NOVA "about \$29 per task" | Table 5 sums to $29.14; about $22 with cached artifacts. | Optional: "(about \$22 with cached artifacts)". |
| I-32 | 265 (taxonomy) | Rec-R1 under "L4 policy (S6) self-generated feedback" | Rec-R1's reward is NDCG from a fixed recommender's ground truth, which is external feedback. | Optional caption note. |
| I-33 | AgentCF † | † marks "open-source code verified" | The repo github.com/RUCAIBox/AgentCF exists (HTTP 200, contains code), but the paper does not link it. | OK to keep. Note that it was found under the lab organisation. |

#### Internal inconsistencies (besides T-1 and T-6)

- **X-1.** Abstract and F7 say "Two systems report … inflated the metric or leaked the target". The printed table shows three `G` cells among core systems (A-MLE included). This is fixed by T-1.
- **X-2.** F7 says "five say nothing". The printed table shows 7 `\ns` in C9 (NOVA and AgentX are stale). This is fixed by T-1.

### 4c. Verified correct (spot list of the high-risk sentences)

**Affiliations.** All company attributions in the abstract and intro hold:
- Google: Google/YouTube, RecEvolve, AgenticRecTune.
- Meta: REA, Auto-RecSys, A-MLE, CORAL, GEARS, RankEvolve (all four authors), Population Evolution (all eight).
- Alibaba: EvoRec; Astar, on the Lazada advertising platform.
- Kuaishou: AgentX (three-week Kuaishou deployment), SR-Agent, Trajectories.
- Tencent: NOVA, RecSys Factory.
- NetEase: AutoLR.
- Shopee: Sortify.
- AgentX-Model names no affiliation; "successor of AgentX" is correct.

**Numbers and quotes confirmed verbatim against the full text:**
- RecHarness: +85.85% / +12.58%, 43,200 GPU-s, five backbones, three runs without std, validation-only selection, test used once.
- VirtualMLE: hidden test, immutable pipeline, grid search (729) and BO (500) at a budget favourable to them, tuned baselines, $1.5–4.8 per session.
- EvoSkillRec: both quotes; five Pareto candidates; NASRec and OpenEvolve as controls.
- RankEvolve: canonical full-test NDCG@10 leaderboard; genre leak (training loss → 0, eval spike, "detected and corrected"); 10.4% / 35.4%.
- Population Evolution: +10.66% / −0.79%, 2 of 3 designs, 11/60 → 18/60, test-split baseline calibration (App. F.1).
- Google: about $20,000 over six months, Gemini personas, February 2026.
- RecEvolve: batch-size quote, human rollback, "win-win" quote.
- A-MLE: "pretend to have completed tasks".
- AgentX-Model: σ 0.0010–0.0022 AUC and the >10⁻⁶ rule.
- Trajectories: 22 of 30.
- AutoLR: KEEP ratchet (named by the authors), single-run promotion with calibration disabled, the "does not establish superiority…" quote, discusses multiple testing without a correction.
- NOVA: target-leakage gates, Optuna-TPE comparison, 6-day A/B.
- AURA: stops at pull requests; 904 fabricated identifiers.
- SR-Agent: four typed actions, one-month A/B.
- Sortify: frozen round chosen on the same online signal, 7-day re-test.
- EvoRank: "almost entirely fitness noise", 60k held-out queries, about 70% survival, random search p = 0.03, about $10 per 50 iterations.
- Semantic Indexes: ρ = 0.90, the "not only less informative but misleading" quote, ~1M-parameter proxy decoder.
- MLE-bench has exactly one recommendation competition (H&M) of 75, so "at most one" holds.
- MLRC-Bench: dev split only; best snapshot scored once on test.
- MLGym `validate` "returns the metrics on the test set".
- Roelofs: 120 competitions; the round-1 fix is correct.
- fang2025 has 0 hits for "recommend".
- Meta REA: "plans, launches and debugs … with up-front GPU budget approval".

---

## 5. Unverifiable or partly verified items

1. **DBLP** returned a bot-challenge page, so it was not used. Non-arXiv entries were verified through Crossref (DOI), the official NeurIPS proceedings page and BibTeX, and the GitHub/blog pages.
2. **`roelofs2019metaanalysis` pages.** The official NeurIPS BibTeX has an empty `pages` field, so no page range can be verified.
3. **Pages for ICML/NeurIPS/ICLR/TMLR upgrades without a Crossref record** (`zhai2024hstu`, `rajput2023tiger`, `chan2024mlebench`, `lin2025recr1`, `gao2025selfevolvingsurvey`, `zhang2026rsir`, `dwork2015reusable`): only the venue was confirmed, via the arXiv comment and Semantic Scholar. `blum2015ladder` pp. 1006–1014 comes from Semantic Scholar only.
4. **Semantic Scholar per-paper endpoint.** It returned HTTP 429 throughout, so the batch endpoint was used instead (148/148 found).
5. **arXiv API 429s.** Some claim-check sub-runs hit the limit and read authors and affiliations from the arXiv HTML author block instead. All 148 records were fetched by `fetch_meta.py` (`review/meta.json`).
6. **AutoLR C9 quote.** The preflight check that "frozen objectives or evaluation logic are not modified" was taken from `audit/evidence-part1.md` and not re-read in the source. AutoLR's other claims were re-read.
7. **`yang2026ideationgoodhart`.** It can be checked only against the authors' own repository (README.md, REPORT.md), which is not peer-reviewed. The pre-registration itself was not inspected.
8. **AgentCF code.** The repository was found by URL under the authors' lab. The paper does not link it (see I-33).
