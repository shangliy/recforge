# Second-coder reliability check

The scored criteria (C1-C6, C8, C9 and `incident`) of all 27 core systems were coded twice, not fully independently (see below): once by the first coder from LLM-extracted quotes,
not a full reading (`audit.csv`, as it stood before reconciliation: `coder1-prereconciliation.csv`)
and once by a second coder (statement identical to the paper's Appendix B: "By the second coder's own account, the papers were read by hand without an LLM, and neither an earlier version of the survey's audit table nor the draft's findings had been seen before the sheets were returned; whether the coder opened any other first-coding file (the sheet, the quote files or the evidence files, all in the shared repository) was not asked and is not recorded, and 17 first-coding cells were visible in the codebook file the guide pointed to." The guide did not ask the coder to avoid LLMs); the guide asked the coder not to open the first coding's sheet, which was in the shared repository (the codebook it was pointed to showed 17 first-coding
values; see below and `kappa.py --exclude-visible`). The second coder had not read the survey draft's findings before
returning the sheets; coding time was not recorded (the guide suggested about 20–30 minutes per paper; both returned sheets were in the repository within about 20 hours of the first batch being sent).

Files:

- `CODER-GUIDE.md`: the guide the second coder received, with the codebook in `../README.md`. It is kept as sent, so its paper counts and table and figure numbers ("10 papers", "Table 3 or Figure 3") refer to the draft and first batch of that time; the audit table is now Table 6.
- `sheet.csv`, `sheet2.csv`: the blank sheets sent to the second coder (10 systems drawn with `sample.py`, seed
  20261022, sent first, then the other 17; the core list has not changed since the draw, so the same 10 keys come out
  of the released `audit.csv`; the script reads `refs.bib`, not in this package, only to fill the arXiv column, and leaves it empty without it). `sheet.csv` predates the split of C9 into isolation and reported incidents and so has
  no `incident` column; the guide was revised to add it before the second batch was sent, and both returned sheets
  contain it. The guide's opening still says "eight criteria" and "10 papers" from that first version (its table lists the eight
  scored criteria plus `incident`, and the second batch added 17 papers), and its "Table 3 or Figure 3" are the audit
  table and figure as numbered in the draft of that time.
- `returned/coder2.csv`, `returned/coder2-part2.csv`: the second coder's returned sheets, unedited. (One pointer in them is off by a subsection: RankEvolve-HSTU's multi-position leakage quote is in App. H.4 of the coded version, which has no App. H.5; the notes cite H.5.)
- `coder1-prereconciliation.csv`: the first coding of the same cells before any reconciliation. One value is outside the codebook: Population Evolution's c3 is `P` (the first coder's reading that the test split calibrated only the baseline); `kappa.py` treats it as its own category, and it is one of the 38 disagreements (the released code is `N`).
- `coder1-at-kit.csv`: the first coding as it stood when each batch was sent. The first ten systems (`sheet.csv`) went
  out on the afternoon of 2026-10-22; an internal review then changed Population Evolution c2 and c8, which are set back
  here. The other 17 (`sheet2.csv`) went out with the frozen coding that evening, so their cells equal
  `coder1-prereconciliation.csv` (EvoPilot's c2 and c3 were changed before that batch was sent). `kappa.py --first
  coder1-at-kit.csv returned/coder2.csv returned/coder2-part2.csv` gives pooled kappa 0.81, as for the frozen sheet.
- The codebook file the second coder was pointed to (`../README.md`, section "Changes in v2" at the time) listed 17
  first-coding values when the second batch was sent: c9 for RankEvolve-HSTU, RecEvolve, EvoPilot, Amazon AutoResearch,
  CORAL, AgenticRecTune, Sortify, GEARS and Google/YouTube; EvoPilot c2, c3; Population Evolution c2, c8; and
  `incident` = Y for RankEvolve-HSTU, RecEvolve, EvoPilot and Amazon AutoResearch (an earlier version of this note and
  of `kappa.py` counted 13 and missed these four). `kappa.py --exclude-visible` leaves these cells out; pooled kappa
  stays 0.81, stratified kappa is 0.69, and incident kappa is not estimable (no agreed incident remains).
- `kappa.py` also prints a stratified kappa (chance agreement within each criterion, cell-weighted; 0.71, bootstrap
  interval over systems 0.60-0.79) and the unweighted mean of the per-criterion values (0.71); the pooled 0.81 treats
  all labels as one set, which lowers the chance term because the criteria use different labels.
- `kappa.py --offline` restricts the comparison to the 16 offline-selecting loops of the released coding, on which
  F1-F6 are stated: stratified kappa 0.68 (0.55-0.77), C2 0.90, C3 0.70, C4 0.87, C5 0.25, C6 0.54, C8 0.56. The
  27-loop figures are higher partly because both coders mark the offline criteria not applicable for online loops.
- `disagreements.csv`, `reconciliation.md`: every disagreement and how it was resolved against the paper text.
- `online-gates-check.csv`: a blind LLM re-coding of the single-coded online-gate fields (`ab_*` in `audit.csv`);
  a consistency check, not a human coding (see `../evidence-online-gates.md`).
- `online-gates-coder1-preadjudication.csv`: the first coding of the online-gate fields before adjudication against
  that check (it differs from `audit.csv` in PILOT `ab_correction`, N then P, DMRL `ab_duration`, Y then NS, and AgentX
  `ab_duration`, Y then NS).
- `online_agreement.py`: agreement on the online-gate fields, per item, over all 19 loops with an online experiment
  and over the 10 online-selecting loops. `ab_rounds` is free text and is not compared.

Agreement figures reported in the paper (before reconciliation):

    python3 kappa.py --first coder1-prereconciliation.csv returned/coder2.csv returned/coder2-part2.csv

prints raw agreement, Cohen's kappa with a bootstrap interval and Gwet's AC1 per criterion and pooled, the pooled
values without cells both coders marked not applicable, every disagreement and the confusion matrices. Without
`--first` the script compares against the reconciled `../audit.csv`.

Online-gate agreement reported in the paper (88 of 95 cells before adjudication):

    python3 online_agreement.py --first online-gates-coder1-preadjudication.csv   # the paper's figures (88/95, kappa 0.86 stratified by item, confirmation alone 0.65, pooled 0.91; applicable cells 79/86). Without --first it compares against the adjudicated coding

C7 (budget units) is free text and is not scored. Design fields (`design.csv`) and kept edits are
single-coded; the strata follow from the double-coded C2. Both points are as the paper's threats section states.

## Provenance of the agreement inputs

SHA-256 checksums of the three files the reported kappa is computed from, and the repository commits they match
(times are commit times, local time of the repository):

| file | SHA-256 | matches |
|---|---|---|
| `coder1-prereconciliation.csv` | `d89468be1d65e9d1ccc8034cc7e8210313281d7a786a45c0a07d44e4904d8423` | `audit/audit.csv` as committed in 925fd50, 22 October 20:37, byte for byte |
| `returned/coder2.csv` | `bd1c8141bccc53003dabb3104eed9b746476f78f6f1fb278fecaa560674d3473` | first committed in 4ae46ea, 23 October 11:04, unchanged since |
| `returned/coder2-part2.csv` | `eb9f590843f8250531e0750dfd8122814b68a9040408340f5bb4011779b6fb05` | first committed in 4ae46ea, 23 October 11:04, unchanged since |

Check with `sha256sum coder1-prereconciliation.csv returned/coder2*.csv`. The checksums show that the released files
are the committed ones; that the second coder's sheets were not edited before the 23 October commit rests on the
authors' account, as the paper says.
