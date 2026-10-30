# TMLR submission (anonymized)

TMLR accepts surveys (it awards a Survey Certification), reviews on OpenReview, has no deadline and no page limit,
and allows a public preprint, so the Zenodo record does not conflict with double-blind review. Acceptance counts as
peer review, after which the survey also meets arXiv's rule for review articles.

## Build

```bash
python3 make_tmlr.py                     # draft/paper.tex -> main.tex, refs.bib -> refs-anon.bib
pdflatex main; bibtex main; pdflatex main; pdflatex main
```

`draft/paper.tex` stays the only source: rerun the script after any edit. It switches to the TMLR class and
author-year citations, hides the authors, rewrites the one first-person self-citation in the third person, sets the
audit table in landscape, and replaces the two GitHub links that name the authors with anonymous-repository links.
`tmlr.sty`, `tmlr.bst` and `fancyhdr.sty` are copied unchanged from
https://github.com/JmlrOrg/tmlr-style-file (Apache-2.0).

## Before submitting

1. Upload `supplement.zip` (written by `make_tmlr.py`, refused if it contains an identifying string) as the
   supplementary material. The PDF has no repository links: the audit-data footnote points at the supplement, and
   the authors' own ideation-harness citation is dropped.
2. Check the PDF: `pdfinfo main.pdf` shows no author, and
   `pdftotext main.pdf - | grep -iE "shangliy|Shanglin|Zhan Shi|Independent Researcher|Santa Clara|@[a-z0-9-]+\.(com|edu)"` prints nothing.
3. Both authors need OpenReview profiles. The submitting author fills in the form: title, abstract, keywords,
   PDF, and two to three suggested action editors from the TMLR editor list whose areas include recommender
   systems, AutoML or LLM agents.
4. In the submission form or cover letter, say that a non-anonymous preprint exists (Preprints.org
   10.20944/preprints202610.2336.v2) without linking it from the PDF.
5. The main text is longer than 12 pages, so TMLR's standard short review timeline does not apply; expect a
   longer review.

After acceptance: `\usepackage[accepted]{tmlr}`, real authors, real links, then post to arXiv.
