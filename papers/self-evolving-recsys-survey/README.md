# Self-Evolving Recommender Systems: A Survey and an Evaluation Audit

Shanglin Yang, Zhan Shi. Draft, 2026-10-22.

- `draft/paper.pdf`: the paper. Build: `cd draft && pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper`.
- `audit/audit.csv`: the coded audit (22 core systems plus 5 comparison systems, criteria C1–C9; codebook in `audit/README.md`).
  `python3 audit/summarize.py` regenerates the counts and `draft/audit_rows.tex`.
- `audit/evidence-part*.md`: per-paper quotes with section pointers behind each code. Counts in these files are
  superseded by `audit.csv`.
- `refs.bib`: bibliography. Rebuild with `python3 arxiv2bib.py ids.txt manual.bib > refs.bib && python3 published.py refs.bib`:
  arXiv entries come from the arXiv API, `published.py` swaps in the published venue, pages and DOI from `published.tsv`
  (checked against Crossref) and TeX-escapes author names.
- `review/`: the second adversarial review (`ref-check.md`: every cited sentence checked against its source) and its scripts.
- `audit/summarize.py --tex draft/audit_rows.tex --paper draft/paper.tex --fig draft/figs/audit_bars.tex` regenerates
  the audit table inside the paper and Figure 3 from `audit.csv`.
- `01-*.md` … `07-*.md`, `10-evolve/`: research notes and the adversarial review round.
  Stages 08–09 are empty: this is a survey with no new experiments.

Corrections to the audit are welcome as issues or pull requests that cite the paper and section.
