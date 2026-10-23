# Second-coder reliability check

**v2:** the second coder codes all 27 core systems: `sheet.csv` (10, sent first) and `sheet2.csv` (the other 17). The
v2 codebook separates C9 (isolation design) from `incident` (gaming or leakage reported); add the `incident` column to
the first sheet as well. Run `python3 kappa.py coder2.csv coder2-part2.csv`.

The audit in the paper was coded by one person. This folder holds the check a reviewer will ask for: a second
coder independently codes a random sample of the core systems, and we report agreement (Cohen's kappa) per
criterion in the paper's limitations paragraph.

1. `python3 sample.py` writes `sheet.csv`: 10 core systems drawn with a fixed seed.
2. Send the second coder `CODER-GUIDE.md` and a copy of the sheet named `coder2.csv` (nothing else). They fill C1-C6, C8 and C9 from the full text of each paper
   (arXiv link in the sheet; read the appendices too), using only the codebook in `../README.md`. Do **not** open
   `audit.csv`, `../evidence-part*.md` or the paper's Table 3 until the sheet is done. Put a short quote and
   section pointer for each non-obvious cell in `notes`.
3. `python3 kappa.py coder2.csv` prints agreement and kappa per criterion and pooled, and every disagreement.
4. Reconcile disagreements against the paper text. Record the pre-reconciliation kappa in the paper; change
   `audit.csv` only where the reconciliation shows the first coding was wrong, and note the change in `../README.md`.

C7 (budget units) is free text and is not scored.
