# TechRxiv submission package

Prepared 2026-10-22. **The submitting author (Shanglin Yang) uploads this; Claude does not submit.**

## Before you upload
1. TechRxiv's stated policy on survey articles could not be read automatically (its site blocks bots). A third-party
   directory lists its accepted content level as "Research only". Check the author guidelines at
   https://www.techrxiv.org/ (or ask its support) that a survey with an original audit is in scope. The paper's audit
   (coded data, codebook, verbatim evidence) is original research and can be named as the main contribution in the
   submission form.
2. A TechRxiv posting cannot be deleted later, only marked withdrawn.
3. Check that the journal you plan to submit to (e.g. ACM TORS) allows a prior preprint; ACM's policy generally does.

## Files
- Manuscript: `../draft/paper.pdf` (14 pages; PDF metadata has title, authors and keywords)
- Optional supplementary link: https://github.com/shangliy/recforge/tree/master/papers/self-evolving-recsys-survey/audit

## Form fields
- **Title:** Self-Evolving Recommender Systems: A Survey and an Evaluation Audit
- **Authors:**
  1. Shanglin Yang, Independent Researcher, kudoysl@gmail.com (submitting author; add your ORCID if you have one)
  2. Zhan Shi, Santa Clara University, ashi2@scu.edu
- **Subject category:** Computing and Processing
- **Keywords:** recommender systems; LLM agents; self-evolving systems; AutoML; program evolution; evaluation;
  reproducibility
- **License:** CC BY 4.0 (most permissive; keeps journal options open)
- **Funding:** none
- **Competing interests:** The authors develop recforge, the open benchmark described in Section 7.
- **Data availability:** The audit data file, codebook and evidence are released at
  https://github.com/shangliy/recforge (MIT license).
- **Abstract:**

In 2026 a new kind of recommender research appeared: large language model (LLM) agents that propose changes to a recommender's configuration or source code, train the changed model, and keep what the evaluation says is better. Within ten months, more than thirty such systems were reported, from open-source research harnesses to production loops at Google, Meta, Amazon, Alibaba, Kuaishou, Tencent and NetEase. This survey organises them, together with search-space AutoML and the agentic recommenders that update their own memory or weights, along two axes: what the loop changes and which signal decides whether a change survives. Because a self-evolving system is only as good as the signal it selects on, we then audit how 27 configuration- and code-level recommender systems are evaluated, coding each paper's full text against nine criteria. Three of the 27 evaluate with full-catalogue ranking. Of the 17 that select candidates offline, nine do not say which data split makes the decision, two select on the data they report, and three state that the test set was used once. None reports its headline result with the spread over repeated evolution sessions, and none runs an equal-budget random search over its own edit space; the few studies that measure transfer to held-out data find that part of the selected gain, sometimes most of it, does not survive. Four systems report that their agent inflated the metric or leaked the target, caught by a human or by monitoring rather than by the acceptance rule. We distil these findings into a reporting standard and describe recforge, an open benchmark under development that implements the API side of a sealed-test, full-ranking, equal-budget protocol.
