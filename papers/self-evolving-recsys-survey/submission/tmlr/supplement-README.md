# Supplementary material: index

Where each table, figure and number of the paper comes from. Run the commands from `audit/`.

| Paper item | Source data | How it is produced |
|---|---|---|
| Audit table (per-loop codes), summary figure, all F1--F9 counts | `audit.csv` | `python3 summarize.py` prints the counts; `--tex FILE` writes the table rows, `--fig FILE` the figure |
| Taxonomy x outcomes table, retrospective proxy table of the checklist, sensitivity table (counts under each coding) | `audit.csv`, `design.csv`, `second-coder/` | `python3 summarize.py --tables DIR` |
| Headline-count table (value columns) and F8 lift range | `audit.csv`, `f8-lifts.md` | `python3 summarize.py --headline` (the judgement-based sets are named in the script; the agreement column comes from `kappa.py` and `online_agreement.py`) |
| Design table | `design.csv` | assembled by hand from `design.csv` and `design-evidence.md` |
| Inter-coder agreement (kappa, AC1, disagreements) | `second-coder/coder1-prereconciliation.csv`, `second-coder/returned/` | `python3 second-coder/kappa.py --first second-coder/coder1-prereconciliation.csv second-coder/returned/coder2.csv second-coder/returned/coder2-part2.csv` (add `--exclude-visible` for the variant without visible cells); checksums in `second-coder/README.md` |
| Online-gate re-coding agreement | `second-coder/online-gates-*.csv` | `python3 second-coder/online_agreement.py --first second-coder/online-gates-coder1-preadjudication.csv` (the paper's 88/95) |
| Evidence for every cell | `evidence-part1.md`--`evidence-part3.md`, `evidence-online-gates.md`, `design-evidence.md` | quotes and section pointers |
| Cell-level changes since first coding | `CHANGELOG.md` | generated from the repository history by `changelog.py` (history withheld for review) |
| Search log, hit counts, flow table | `../review/sweep-2026-10-22.md` | per-query table |
| Recall check | `recall-check.md` | matching needs the manuscript sources, not included |
| Bibliography and repository checks | `../review/ref-check.md`, `../review/refcheck-fixlog.md` | results only; rerunning needs the manuscript sources, not included |

**Not reproducible from this package alone:** the matching step of the recall check, the bibliography and repository checks, and `changelog.py` (it reads the withheld history). Their outputs are included; every other number in the paper can be recomputed with the commands above.

Coding conventions and the codebook: `audit/README.md`. Where an evidence file and `audit.csv` differ, `audit.csv` is authoritative.
