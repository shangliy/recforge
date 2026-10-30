#!/usr/bin/env python3
"""Write evidence-released.md: one row per coded cell, with the released code from audit.csv and the one piece of
evidence that supports it now.

    python3 evidence_released.py      # run after annotate_evidence.py; safe to rerun

The evidence files keep the first coding's verdicts, with recoded cells flagged in place (annotate_evidence.py). This
file reads them and keeps only the current layer: for a cell that was not recoded, the quote and pointer written at
first coding; for a recoded cell, the second coder's returned note where the released code is that coder's, otherwise
a pointer to the file where the recode is argued. audit.csv stays authoritative; this file is a view of it.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ["evidence-part1.md", "evidence-part2.md", "evidence-part3.md"]
CRIT = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9"]
MARK = "⟨recoded since this was written; released code: "
LEAD = re.compile(r"⟨superseded verdict, released code `[^`]*`; see end of line⟩ ?")

rows = {r["key"]: r for r in csv.DictReader(open(HERE / "audit.csv"))}

# Credited cells whose recode flag carries only a pointer: the quote from the file that argues the recode.
QUOTE = {
    ("patel2026evorank", "c9"): 'Frozen data preparation; label statistics only through helpers "with leakage guards built in"; '
        'the audit caught three target-encoding leakage bugs (Sec 5). Recoded from `Y+caught` when that value was dropped '
        '(CHANGELOG.md).',
    ("peng2026population", "c6"): '"Baseline HPO tunes the unmodified starting implementation separately for each instance '
        'before evolutionary search"; "CMA-ES sampling in Optuna ... with LLM-proposed configurations added after warm-up" '
        '(App. A.7); every local gain is measured against this tuned reference (second-coder/reconciliation.md).',
    ("peng2026population", "c8"): '"The starting code, model capacity, data, evaluator, and prescribed epochs or step count '
        'remain fixed during calibration" (App. A.7); ranking has no validation split (App. A.1) '
        '(second-coder/reconciliation.md).',
    ("chen2026rankevolve", "c9"): '"Define the failure set F_T = {u : rank_u(i_n) > 10} ... computing F_S only re-runs the '
        'frozen model with a different ignore_last_n argument" (App. H.1): the agent computes per-user ranks on the held-out '
        'test item and writes and runs evaluation variants (App. H.4), so the loop has test access '
        '(second-coder/reconciliation.md).',
    ("wang2026pear", "c9"): '"Before any candidate is exposed to real-user traffic, the proposed change and supporting '
        'evidence undergo human review and require explicit human confirmation" (Sec 9); "The search space is currently '
        'restricted to strategy-level parameters" (Sec 8) (verification-pass-3.md).',
}

# Credited cells whose first-coding note paraphrased the paper: verbatim quotes added on 29 October 2026, each
# matched against the coded arXiv version (quotes-added.json). They are put before the note.
ADDED = {(e["key"], e["crit"]): "; ".join(f'"{x["text"]}" ({x["loc"]})' for x in e["quotes"])
         for e in __import__("json").load(open(HERE / "quotes-added.json"))}


def sections():
    """Yield (key, file, body lines) for every system section, matched to audit.csv by arXiv id as in
    annotate_evidence.py."""
    for name in FILES:
        lines = (HERE / name).read_text().splitlines()
        heads = [i for i, l in enumerate(lines) if re.match(r"#{2,3} ", l)]
        for h in heads:
            end = next((i for i in range(h + 1, len(lines)) if re.match(r"#{2,3} ", lines[i])), len(lines))
            window = "\n".join([lines[h]] + [l for l in lines[h + 1:min(end, h + 15)] if re.search(r"arXiv \d{4}\.", l)])
            for r in rows.values():
                if r["version"].split("v")[0] in window:
                    yield r["key"], name, lines[h + 1:end]
                    break


def cell(body, c):
    """The current evidence for criterion c in a section, or None."""
    C = c.upper()
    for line in body:
        if line.startswith("> **Released codes"):
            continue
        if line.startswith(f"| {C} | "):  # table form (evidence-part3.md)
            cells = line.split(" | ")
            text = " | ".join(cells[2:]).rstrip(" |")
            if MARK in cells[1]:
                return current(cells[1], c, multi=False)
            return clean(text)
        m = re.search(r"\*\*" + C + r"\b[^*]*\*\*", line)
        if m and line.startswith("- "):
            if MARK in line:
                multi = len(re.findall(r"\*\*C\d\b[^*]*\*\*", line)) > 1
                got = current(line, c, multi)
                if got:
                    return got
            seg = line[m.end():]
            nxt = re.search(r"\*\*C\d\b[^*]*\*\*", seg)
            seg = seg[:nxt.start()] if nxt else seg
            return clean(seg)
    return None


def current(line, c, multi):
    """The supporting text carried by the recode flag for criterion c."""
    for flag in re.findall(re.escape(MARK) + r"(`[^`]*`[^⟩]*)⟩", line):
        if multi and f" for {c.upper()}" not in flag.split(";")[0]:
            continue
        sup = flag.split("; ", 1)[1] if "; " in flag else ""
        sup = re.sub(r"^the second coder's evidence for it: ", "second coder: ", sup)
        return clean(sup)
    return None


def clean(s):
    s = re.sub(r"\s*" + re.escape(MARK) + r"[^⟩]*⟩", "", s)
    s = LEAD.sub("", s).strip()
    return s.replace("|", "/").strip(" .") + "."


out = ["# Released codes with their current evidence", "",
       "Generated by `evidence_released.py` from `audit.csv` and the three evidence files; do not edit. One row per "
       "coded cell of the 27 core loops and 7 comparison points. The code is the released one (`audit.csv`). The "
       "evidence is the first coding's quote and pointer where the cell was not recoded, the second coder's returned "
       "note where a recoded cell follows that coder, and otherwise a pointer to the file that argues the recode. "
       "The evidence files keep the full history; this file keeps only the current layer.", ""]
seen, missing, pointer, credited_pointer, unquoted, credited, tuned = set(), [], [], [], [], 0, 0
for key, name, body in sections():
    if key in seen:  # RecEvolve is written up twice; the first write-up is used
        continue
    seen.add(key)
    r = rows[key]
    out += [f"## {r['system']} (`{key}`, {r['set']}; source: `{name}`)", "", "| Criterion | Released code | Evidence |",
            "|---|---|---|"]
    for c in CRIT:
        ev = QUOTE.get((key, c)) or cell(body, c)
        if (key, c) in ADDED:
            ev = ADDED[(key, c)] + ". Note: " + (ev or "")
        code = r[c]
        credited += code in ("Y", "P")
        tuned += code == "tuned"
        if not ev:
            missing.append((key, c))
            ev = "(no line in the evidence file; see CHANGELOG.md)"
        elif "argued in second-coder/reconciliation.md" in ev:
            pointer.append((key, c))
            if code in ("Y", "P"):
                credited_pointer.append((key, c))
        if code in ("Y", "P", "tuned") and not re.search(r'["\u201c\u201d]', ev):
            unquoted.append((key, c))
        out.append(f"| {c.upper()} | `{code}` | {ev} |")
    out.append("")
absent = sorted(k for k, r in rows.items() if r["set"] in ("core", "comparison") and k not in seen)
out.insert(4, f"Coverage: {len(seen)} systems; {len(seen) * len(CRIT)} cells, {credited} of them credited (`Y` or `P`; the {tuned} C8 cells coded `tuned`, which count as yes, are quoted too); "
              f"{len(pointer)} cells carry a pointer instead of a quote ({len(credited_pointer)} of them credited); {len(unquoted)} credited cells have no quoted text; {len(missing)} cells have no line in the "
              f"evidence files{'; systems without a section: ' + ', '.join(absent) if absent else ''}.\n")
(HERE / "evidence-released.md").write_text("\n".join(out) + "\n")
print(f"{len(seen)} systems, credited {credited}, pointer {len(pointer)}, missing {len(missing)}, absent {absent}")
for k, c in missing:
    print("missing", k, c)
for k, c in unquoted:
    print("unquoted", k, c, rows[k][c])
for k, c in pointer:
    print("pointer", k, c, rows[k][c])
