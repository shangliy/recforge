#!/usr/bin/env python3
"""Draw the reliability sample and write a blank coding sheet for the second coder.

    python3 sample.py [OUT]      # -> OUT (default sample-sheet.csv; 10 core systems, fixed seed)

The released sheet.csv is not overwritten unless it is named as OUT.

The seed is fixed so the sample is reproducible and chosen before any second coding is seen.
"""
import csv
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED, N = 20261022, 10
COLS = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9"]


def arxiv_ids():
    """key -> arXiv id from the bibliography (eprint field or arxiv.org URL)."""
    ids, key = {}, None
    bib = HERE.parents[1] / "refs.bib"
    if not bib.exists():  # the supplement ships without the bibliography; the arXiv column is then left empty
        return ids
    for line in bib.read_text().splitlines():
        if m := re.match(r"@\w+\{([^,]+),", line):
            key = m.group(1)
        elif key and (m := re.search(r"(?:eprint\s*=\s*\{|arxiv\.org/abs/)(\d{4}\.\d{4,5})", line)):
            ids.setdefault(key, m.group(1))
    return ids


def main():
    rows = [r for r in csv.DictReader(open(HERE.parent / "audit.csv")) if r["set"] == "core"]
    sample = sorted(random.Random(SEED).sample(rows, N), key=lambda r: r["key"])
    ids = arxiv_ids()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sample-sheet.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "system", "arxiv"] + COLS + ["notes"])
        for r in sample:
            w.writerow([r["key"], r["system"], ids.get(r["key"], "")] + [""] * len(COLS) + [""])
    print(f"wrote {out.name} with {N} systems (seed {SEED})")


if __name__ == "__main__":
    main()
