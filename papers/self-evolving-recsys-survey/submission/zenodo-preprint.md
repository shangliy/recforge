# Zenodo preprint record: fields to fill

Upload at https://zenodo.org/uploads/new (logged in). The record becomes permanent once published.

| Field | Value |
|---|---|
| Files | `draft/paper.pdf` (download: https://shangliy.github.io/recforge/survey/paper.pdf) |
| Do you already have a DOI? | **No** (Zenodo assigns one) |
| Resource type | **Publication → Preprint** |
| Title | Self-Evolving Recommender Systems: A Survey and an Evaluation Audit |
| Publication date | 2026-10-22 |
| Creator 1 | Yang, Shanglin; affiliation: Independent Researcher; role: (leave default) |
| Creator 2 | Shi, Zhan; affiliation: Santa Clara University |
| Description | the abstract below |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Keywords | recommender systems; LLM agents; self-evolving systems; AutoML; program evolution; evaluation; reproducibility |
| Language | English |
| Version | v1 |
| Related works | **Is supplemented by** → DOI `10.5281/zenodo.23574306` (resource type: Software) |
| Related works | **Is supplemented by** → URL `https://github.com/shangliy/recforge/tree/master/papers/self-evolving-recsys-survey/audit` (Dataset) |
| Related works | **Is documented by** is not needed |
| Publisher | Zenodo (default) |
| Communities | optional; skip |

Description (paste as plain text):

In 2026 a new kind of recommender research appeared: large language model (LLM) agents that propose changes to a recommender's configuration or source code, train the changed model, and keep what the evaluation says is better. Within ten months, more than thirty such systems were reported, from open-source research harnesses to production loops at Google, Meta, Amazon, Alibaba, Kuaishou, Tencent and NetEase. This survey organises them, together with search-space AutoML and the agentic recommenders that update their own memory or weights, along two axes: what the loop changes and which signal decides whether a change survives. Because a self-evolving system is only as good as the signal it selects on, we then audit how 27 configuration- and code-level recommender systems are evaluated, coding each paper's full text against nine criteria. Three of the 27 evaluate with full-catalogue ranking. Of the 17 that select candidates offline, nine do not say which data split makes the decision, two select on the data they report, and three state that the test set was used once. None reports its headline result with the spread over repeated evolution sessions, and none runs an equal-budget random search over its own edit space; the few studies that measure transfer to held-out data find that part of the selected gain, sometimes most of it, does not survive. Four systems report that their agent inflated the metric or leaked the target, caught by a human or by monitoring rather than by the acceptance rule. We distil these findings into a reporting standard and describe recforge, an open benchmark under development that implements the API side of a sealed-test, full-ranking, equal-budget protocol.
