#!/usr/bin/env python3
"""Agreement between the first coding (audit.csv) and the second coder's sheet.

    python3 kappa.py coder2.csv

Prints raw agreement and Cohen's kappa per criterion and pooled, and lists every disagreement
so the two coders can reconcile them against the paper text.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9"]


def norm(v):
    return v.strip().lower()


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    first = {r["key"]: r for r in csv.DictReader(open(HERE.parent / "audit.csv"))}
    second = [r for r in csv.DictReader(open(sys.argv[1])) if any(r[c].strip() for c in COLS)]
    pooled, disagreements = [], []
    print(f"{len(second)} systems\n\ncriterion  agree  kappa")
    for c in COLS:
        pairs = [(norm(first[r["key"]][c]), norm(r[c])) for r in second]
        pooled += pairs
        po, k = kappa(pairs)
        print(f"{c:9}  {po:5.2f}  {k:5.2f}")
        disagreements += [(r["system"], c, a, b) for r, (a, b) in zip(second, pairs) if a != b]
    po, k = kappa(pooled)
    print(f"{'pooled':9}  {po:5.2f}  {k:5.2f}\n")
    for system, c, a, b in disagreements:
        print(f"  {system}: {c} first={a} second={b}")


if __name__ == "__main__":
    main()
