#!/usr/bin/env python3
"""Put the released codes from audit.csv at the top of each system's section in the evidence files.

    python3 annotate_evidence.py      # rewrites evidence-part{1,2,3}.md in place; safe to rerun

The evidence files keep the verdict and quote written at first coding, and some verdicts were changed later
(verification passes, internal review, reconciliation). This adds, under each system's heading, one line with the
final code of every criterion and the cells changed since first coding, and flags each body line of a recoded cell
with its released code, so a superseded verdict is not taken for the released one. Where the released code is the
second coder's, the flag carries that coder's returned note for the cell as its supporting quote; otherwise it points
to second-coder/reconciliation.md (reconciliation recodes) or verification-pass-1.md (earlier recodes).
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ["evidence-part1.md", "evidence-part2.md", "evidence-part3.md"]
COLS = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9", "incident"]
TAG = "> **Released codes (audit.csv)"

rows = {r["key"]: r for r in csv.DictReader(open(HERE / "audit.csv"))}
changed = {}
for line in (HERE / "CHANGELOG.md").read_text().splitlines():
    if m := re.match(r"- `([^`]+)` \(.*\) (c\d|incident): `", line):
        changed.setdefault(m.group(1), set()).add(m.group(2))


def note(r):
    codes = " · ".join(f"{c.upper() if c != 'incident' else 'incident'} `{r[c]}`" for c in COLS)
    rec = sorted(changed.get(r["key"], ()))
    tail = (f"; recoded since first coding: {', '.join(c.upper() for c in rec)} (see CHANGELOG.md)" if rec else "")
    return (f"{TAG}:** {codes}{tail}. Where a verdict below differs, this code is the released one; such verdicts are "
            "flagged, including changes made before the changelog starts.")


MARK = " ⟨recoded since this was written; released code: "
LEAD = "⟨superseded verdict, released code "  # put before the old verdict so it is not read as the released one

# the second coder's returned notes, split per criterion, give the supporting quote for a recoded cell whose released
# code is the second coder's; the other recoded cells are argued in second-coder/reconciliation.md
SEG = re.compile(r"(?:^|(?<=\. )|(?<=\.\) )|(?<=\.\" ))((?:c\d|incident)(?:/(?:c\d|incident))*): ")
second = {}
for f in ("coder2.csv", "coder2-part2.csv"):
    for r2 in csv.DictReader(open(HERE / "second-coder" / "returned" / f)):
        notes = (r2.get("notes") or "").strip()
        parts = SEG.split(notes)
        segs = {}
        for i in range(1, len(parts) - 1, 2):
            for c in parts[i].split("/"):
                segs[c] = parts[i + 1].strip()
        second[r2["key"]] = ({c: (r2.get(c) or "").strip() for c in COLS}, segs)


def support(r, c):
    codes, segs = second.get(r["key"], ({}, {}))
    if codes.get(c, "").lower() == r[c].lower() and segs.get(c):
        return "; the second coder's evidence for it: " + segs[c].replace("⟩", ")")
    return "; argued in second-coder/reconciliation.md or verification-pass-1.md"
BULLET = re.compile(r"^- \*\*(C\d)\b[^*]*\*\*")
ROW = re.compile(r"^\| (C\d) \| ")


# the verdict a bullet opens with, for the criteria coded Y / P / N / NS / na; a verdict that disagrees with the released
# code is flagged even when the change predates the changelog
VERDICT = [("not stated", "NS"), ("not discussed", "NS"), ("not applicable", "na"), ("partial", "P"), ("yes", "Y"),
           ("no", "N")]


def verdict(line):
    body = re.sub(r"^- \*\*C\d\b[^*]*\*\*\s*", "", line).lower()
    for word, code in VERDICT:
        if re.match(re.escape(word) + r"\b", body):
            return code
    if re.match(r"[^.]* is not (discussed|stated)\b", body):
        return "NS"
    return None


def mark(line, r, rec):
    """Flag a criterion line (bullet or table row) whose cell was recoded after the evidence was written, or whose
    opening verdict differs from the released code."""
    line = re.sub(re.escape(MARK) + r"`[^`]*`[^⟩]*⟩", "", line)
    line = re.sub(re.escape(LEAD) + r"`[^`]*`; see end of line⟩ ", "", line)
    m = BULLET.match(line)
    if m:
        c = m.group(1).lower()
        v = verdict(line)
        if c in r and r[c] in ("Y", "P", "N", "NS", "na") and v and v != r[c]:
            rec = rec | {c}
    if m:
        # a bullet can carry several criteria inline ("**C3:** not stated. **C5:** no."); flag each recoded one
        cs = [c.lower() for c in re.findall(r"\*\*(C\d)\b[^*]*\*\*", line)]
        flagged = [c for c in dict.fromkeys(cs) if c in rec and c in r]
        for c in flagged:
            line = re.sub(r"(\*\*" + c.upper() + r"\b[^*]*\*\*\s*)", lambda g: g.group(1) + LEAD + f"`{r[c]}`; see end of line⟩ ",
                          line, count=1)
        if flagged:
            return line.rstrip() + "".join(MARK + f"`{r[c]}` for {c.upper()}{support(r, c)}⟩" if len(cs) > 1
                                           else MARK + f"`{r[c]}`{support(r, c)}⟩" for c in flagged)
    m = ROW.match(line)
    if m and m.group(1).lower() in rec:
        cells = line.split(" | ")
        c = m.group(1).lower()
        cells[1] += MARK + f"`{r[c]}`{support(r, c)}⟩"
        return " | ".join(cells)
    return line


for name in FILES:
    path = HERE / name
    # drop a previous run's line together with the blank line inserted before it
    lines = path.read_text().replace("\n\n" + TAG, "\n" + TAG).splitlines()
    lines = [l for l in lines if not l.startswith(TAG)]
    heads = [i for i, l in enumerate(lines) if re.match(r"#{2,3} ", l)]
    inserts = []
    for h in heads:
        # the system's arXiv id is in the heading, or in an "arXiv <id>" line just below it
        end = next((i for i in range(h + 1, len(lines)) if re.match(r"#{2,3} ", lines[i])), len(lines))
        window = "\n".join([lines[h]] + [l for l in lines[h + 1:min(end, h + 15)] if re.search(r"arXiv \d{4}\.", l)])
        for r in rows.values():
            if r["version"].split("v")[0] in window:
                inserts.append((h, note(r), r))
                break
    for h, text, r in sorted(inserts, reverse=True, key=lambda t: t[0]):
        end = next((i for i in range(h + 1, len(lines)) if re.match(r"#{2,3} ", lines[i])), len(lines))
        rec = changed.get(r["key"], set())
        lines[h + 1:end] = [mark(l, r, rec) for l in lines[h + 1:end]]
        lines[h + 1:h + 1] = ["", text]
    path.write_text(re.sub(r"\n{3,}", "\n\n", "\n".join(lines) + "\n"))
    print(name, len(inserts), "sections annotated")
