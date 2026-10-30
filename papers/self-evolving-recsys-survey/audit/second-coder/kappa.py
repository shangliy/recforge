#!/usr/bin/env python3
"""Agreement between the first coding (audit.csv) and the second coder's sheets.

    python3 kappa.py [--first coder1-prereconciliation.csv] [--exclude-visible] [--offline] coder2.csv [coder2-part2.csv ...]

--offline restricts the agreement to the 16 offline-selecting loops of the released coding, the stratum on which
F1-F6 and F8 are stated (the full run includes cells both coders mark not applicable for online-selecting loops).

--first defaults to ../audit.csv (the reconciled coding). The pre-reconciliation figures the paper reports come from
--first coder1-prereconciliation.csv, the first coder's sheet as committed before reconciliation (git 925fd50).

Prints, per criterion and pooled: raw agreement, Cohen's kappa with a 95% bootstrap interval (resampling systems),
and Gwet's AC1, which is robust to skewed marginals. Lists every disagreement and prints the confusion matrix of
each criterion so the two coders can reconcile against the paper text. Report the values from before reconciliation.
"""
import csv
import random
import sys
sys.dont_write_bytecode = True  # leave no __pycache__ in the released folder
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["c1", "c2", "c3", "c4", "c5", "c6", "c8", "c9", "incident"]
# first-coding values printed in the codebook file (../README.md, "Changes in v2") when the second batch was sent;
# --exclude-visible drops these cells
VISIBLE = {("chen2026rankevolve", "c9"), ("pan2026recevolve", "c9"), ("fu2026evopilot", "c9"),
           ("chandran2026autoresearch", "c9"), ("azhar2026coral", "c9"), ("wu2026agenticrectune", "c9"),
           ("cheng2026sortify", "c9"), ("yun2026gears", "c9"), ("wang2026selfevolving", "c9"),
           ("fu2026evopilot", "c2"), ("fu2026evopilot", "c3"), ("peng2026population", "c2"), ("peng2026population", "c8"),
           # the same file named the four rows that now carry incident = Y
           ("chen2026rankevolve", "incident"), ("pan2026recevolve", "incident"), ("fu2026evopilot", "incident"),
           ("chandran2026autoresearch", "incident")}


def norm(v):
    return v.strip().lower()


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    if len(ca) < 2 or len(cb) < 2:  # a coder used one label throughout: kappa is not estimable
        return po, float("nan")
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


def strat_kappa(by_crit):
    """Pooled agreement with chance agreement computed within each criterion (cell-weighted), so that criteria with
    different label sets do not lower the chance term as they do when all labels share one marginal distribution."""
    n = sum(len(p) for p in by_crit)
    po = sum(a == b for p in by_crit for a, b in p) / n
    pe = 0.0
    for p in by_crit:
        ca, cb = Counter(a for a, _ in p), Counter(b for _, b in p)
        pe += sum(ca[k] * cb[k] for k in ca) / len(p)
    pe /= n
    return (po - pe) / (1 - pe)


def boot_strat(by_sys, reps=2000, seed=0):
    """Bootstrap the stratified kappa by resampling systems; by_sys[i] is a list of (criterion, a, b)."""
    rng = random.Random(seed)
    crits = sorted({c for s in by_sys for c, _, _ in s})
    vals = []
    for _ in range(reps):
        sample = [rng.choice(by_sys) for _ in by_sys]
        groups = [[(a, b) for s in sample for c2, a, b in s if c2 == c] for c in crits]
        vals.append(strat_kappa([g for g in groups if g]))
    vals = sorted(v for v in vals if v == v)
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def boot_kappa(pairs, reps=2000, seed=0):
    rng = random.Random(seed)
    vals = sorted(k for k in (kappa([rng.choice(pairs) for _ in pairs])[1] for _ in range(reps)) if k == k)
    if not vals:
        return float("nan"), float("nan")
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def main():
    args = sys.argv[1:]
    if not args or {"-h", "--help"} & set(args):
        sys.exit(__doc__)
    first_path = HERE.parent / "audit.csv"
    skip = set()
    if "--exclude-visible" in args:
        skip, args = VISIBLE, [a for a in args if a != "--exclude-visible"]
    offline_only = "--offline" in args
    args = [a for a in args if a != "--offline"]
    if args[:1] == ["--first"]:
        first_path, args = Path(args[1]), args[2:]
    if not args:
        sys.exit(__doc__)
    first = {r["key"]: r for r in csv.DictReader(open(first_path))}
    second = [r for f in args for r in csv.DictReader(open(f)) if any(r.get(c, "").strip() for c in COLS[:8])]
    if offline_only:  # the 16 offline-selecting loops of the released coding, the stratum F1-F6 and F8 are stated on
        released = {r["key"]: r for r in csv.DictReader(open(HERE.parent / "audit.csv"))}
        second = [r for r in second if released[r["key"]]["c2"].strip() not in ("online", "na")]
    cols = [c for c in COLS if all(r.get(c, "").strip() for r in second)]
    pooled, disagreements, matrices, by_crit, kappas = [], [], {}, [], []
    by_sys = {r["key"]: [] for r in second}
    print(f"{len(second)} systems\n\ncriterion  agree  kappa  95% CI          AC1")
    for c in cols:
        rows = [r for r in second if (r["key"], c) not in skip]
        pairs = [(norm(first[r["key"]][c]), norm(r[c])) for r in rows]
        pooled += pairs
        by_crit.append(pairs)
        for r, (a, b) in zip(rows, pairs):
            by_sys[r["key"]].append((c, a, b))
        po, k = kappa(pairs)
        kappas.append(k)
        lo, hi = boot_kappa(pairs)
        print(f"{c:9}  {po:5.2f}  {k:5.2f}  [{lo:5.2f}, {hi:5.2f}]  {ac1(pairs):5.2f}")
        disagreements += [(r["system"], c, a, b) for r, (a, b) in zip(rows, pairs) if a != b]
        matrices[c] = Counter(pairs)
    po, k = kappa(pooled)
    print(f"{'pooled':9}  {po:5.2f}  {k:5.2f}  {'':16}  {ac1(pooled):5.2f}")
    applicable = [(a, b) for a, b in pooled if not (a == b == "na")]  # drop cells both coders mark not applicable
    po, k = kappa(applicable)
    print(f"{'pooled*':9}  {po:5.2f}  {k:5.2f}  {'':16}  {ac1(applicable):5.2f}  (* without na/na cells, n={len(applicable)})")
    lo, hi = boot_strat(list(by_sys.values()))
    print(f"{'stratified':9}  {'':5}  {strat_kappa(by_crit):5.2f}  [{lo:5.2f}, {hi:5.2f}]  (chance agreement within each criterion)")
    est = [k for k in kappas if k == k]  # skip criteria whose kappa is not estimable
    print(f"{'mean':9}  {'':5}  {sum(est) / len(est):5.2f}  (unweighted mean of per-column kappa over {len(est)} "
          f"estimable columns, the criteria and the incident flag; range {min(est):.2f}-{max(est):.2f})\n")
    for system, c, a, b in disagreements:
        print(f"  {system}: {c} first={a} second={b}")
    print("\nconfusion (first, second): count")
    for c, m in matrices.items():
        print(f"  {c}: " + ", ".join(f"({a},{b}):{n}" for (a, b), n in sorted(m.items())))


if __name__ == "__main__":
    main()
