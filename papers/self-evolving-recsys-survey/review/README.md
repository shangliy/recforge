# review/

Reference and claim checks of the draft. Several of these files describe **earlier drafts**. Their line numbers, counts and
quoted text can differ from the current `draft/paper.tex`. Treat them as historical records; the current coding is in
`audit/audit.csv` and the cell-level history in `audit/CHANGELOG.md`.

| File | What it is | Status |
|---|---|---|
| `sweep-2026-10-22.md` | Search log of the second literature sweep (queries, hits, screening, capped queries) | current; the search log behind the paper's search protocol |
| `ref-check.md` | Report of the second verification pass (every cited sentence and table cell against its source, 2026-10-22) | historical: line numbers refer to a 665-line snapshot; all items, including T-1 (the stale embedded table, since replaced by `\input{audit_rows}`), are resolved in `refcheck-fixlog.md` |
| `refcheck-fixlog.md` | Item-by-item resolution of `ref-check.md` against the later draft | current as of 2026-10-26; later recoding is in `audit/CHANGELOG.md` |
| `upgrades.md`, `upgrades.py` | arXiv entries with a published version, and the script that lists them | current |
| `bib_static.json`, `meta.json`, `meta_report.json` | Outputs of the scripts below | snapshots |

## Scripts

Run them from the survey root. `check_bib.py`, `fetch_meta.py` and `compare_meta.py` read `refs.bib` and
`draft/paper.tex`, so they need the full repository; they do not run from the supplementary material alone.
`fetch_meta.py`, `fetch_crossref.py` and `fetch_s2_batch.py` query arXiv, Crossref and Semantic Scholar over the network.
`upgrades.py` needs only the JSON files in this folder.
