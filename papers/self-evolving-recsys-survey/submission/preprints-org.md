# Preprints.org submission: fields to fill

Submit at https://www.preprints.org (log in, "Submit"). Preprints.org lists *Review* among its accepted article
types, screens each submission, and assigns a Crossref DOI. It is run by MDPI; posting there does not commit the
paper to an MDPI journal.

| Field | Value |
|---|---|
| Article type | **Review** |
| Subject | Computer Science and Mathematics → Information Systems (alternative: Artificial Intelligence and Machine Learning) |
| Title | Self-Evolving Recommender Systems: A Survey and an Evaluation Audit |
| Authors | Shanglin Yang (Independent Researcher, USA); Zhan Shi (Santa Clara University, Santa Clara, CA, USA) |
| Corresponding author | whoever submits; give that author's email in the form only |
| Abstract | same as `zenodo-preprint.md` (272 words) |
| Keywords | recommender systems; LLM agents; self-evolving systems; AutoML; program evolution; evaluation; reproducibility |
| File | `draft/paper.pdf` (the ACM version with authors, not the anonymized TMLR file) |
| Licence | CC BY 4.0 |
| Funding | None |
| Conflict of interest | The authors built recforge, the open benchmark described in Section 7. |
| Data availability | Audit data and per-cell evidence: https://github.com/shangliy/recforge/tree/master/papers/self-evolving-recsys-survey/audit |

## Note to the editors (paste into the comments box)

> This review was previously deposited on Zenodo (DOI 10.5281/zenodo.23575788) and is not published in, or under
> review at, a peer-reviewed venue other than [leave blank, or: Transactions on Machine Learning Research, which
> permits preprints]. We would like the Preprints.org version to be linked to the Zenodo record.

I could not open Preprints.org's author instructions to confirm how it treats a paper already on Zenodo (the page
refused automated access). The note discloses the Zenodo deposit up front; if screening objects, the Zenodo DOI
remains the citable record.

## After it is posted

Posted 2026-10-23 as DOI 10.20944/preprints202610.2336.v1 (https://www.preprints.org/manuscript/202610.2336/v1).
Version 2 posted as DOI 10.20944/preprints202610.2336.v2 (https://www.preprints.org/manuscript/202610.2336/v2);
it is now the canonical DOI in `README.md`, `CITATION.cff`, `site/` and the BibTeX, with Zenodo as an alternate.


- Add the Preprints.org DOI to `site/index.html` (a link, not `citation_doi`; keep the Zenodo DOI as the
  canonical one so citations do not split), `CITATION.cff` (`identifiers`) and the Zenodo record's related works
  ("Is identical to").
- If TMLR later accepts the paper, add the journal DOI to the Preprints.org record so it links to the published
  version.
