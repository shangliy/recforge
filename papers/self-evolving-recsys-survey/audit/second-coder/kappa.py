#!/usr/bin/env python3
"""Agreement between the first coding (audit.csv) and the second coder's sheets.

    python3 kappa.py coder2.csv [coder2-part2.csv ...]

Prints, per criterion and pooled: raw agreement, Cohen's kappa with a 95% bootstrap interval (resampling systems),
and Gwet's AC1, which is robust to skewed marginals. Lists every disagreement and prints the confusion matrix of
each criterion so the two coders can reconcile against the paper text. Report the values from before reconciliation.
"""
import csv
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9", "incident"]


def norm(v):
    return v.strip().lower()


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def ac1(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    cats = {x for p in pairs for x in p}
    if len(cats) < 2:
        return float("nan")
    pi = {k: (sum(a == k for a, _ in pairs) + sum(b == k for _, b in pairs)) / (2 * n) for k in cats}
    pe = sum(p * (1 - p) for p in pi.values()) / (len(cats) - 1)
    return (po - pe) / (1 - pe)


def boot_kappa(pairs, reps=2000, seed=0):
    rng = random.Random(seed)
    vals = sorted(k for k in (kappa([rng.choice(pairs) for _ in pairs])[1] for _ in range(reps)) if k == k)
    if not vals:
        return float("nan"), float("nan")
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def main():
    first = {r["key"]: r for r in csv.DictReader(open(HERE.parent / "audit.csv"))}
    second = [r for f in sys.argv[1:] for r in csv.DictReader(open(f)) if any(r.get(c, "").strip() for c in COLS[:8])]
    cols = [c for c in COLS if all(r.get(c, "").strip() for r in second)]
    pooled, disagreements, matrices = [], [], {}
    print(f"{len(second)} systems\n\ncriterion  agree  kappa  95% CI          AC1")
    for c in cols:
        pairs = [(norm(first[r["key"]][c]), norm(r[c])) for r in second]
        pooled += pairs
        po, k = kappa(pairs)
        lo, hi = boot_kappa(pairs)
        print(f"{c:9}  {po:5.2f}  {k:5.2f}  [{lo:5.2f}, {hi:5.2f}]  {ac1(pairs):5.2f}")
        disagreements += [(r["system"], c, a, b) for r, (a, b) in zip(second, pairs) if a != b]
        matrices[c] = Counter(pairs)
    po, k = kappa(pooled)
    print(f"{'pooled':9}  {po:5.2f}  {k:5.2f}  {'':16}  {ac1(pooled):5.2f}\n")
    for system, c, a, b in disagreements:
        print(f"  {system}: {c} first={a} second={b}")
    print("\nconfusion (first, second): count")
    for c, m in matrices.items():
        print(f"  {c}: " + ", ".join(f"({a},{b}):{n}" for (a, b), n in sorted(m.items())))


if __name__ == "__main__":
    main()
