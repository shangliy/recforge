#!/usr/bin/env python3
"""Agreement on the online-gate items between the first coding and the blind LLM re-coding (online-gates-check.csv).

    python3 online_agreement.py [--first online-gates-coder1-preadjudication.csv]

--first defaults to ../audit.csv (the adjudicated coding). ab_rounds is free text and is not compared. Prints the
agreement per item, over all 19 loops with an online experiment and over the 10 online-selecting loops, and lists
every disagreement, with Cohen's kappa per item, stratified by item (chance agreement within each item, the paper's
convention), and pooled over all cells and over the cells not both marked not applicable.
"""
import csv
import sys
sys.dont_write_bytecode = True  # leave no __pycache__ in the released folder
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # kappa.py sits next to this script

from kappa import kappa, strat_kappa  # noqa: E402
COLS = ["ab_role", "ab_duration", "ab_ci", "ab_correction", "ab_confirm"]


def main():
    args = sys.argv[1:]
    if {"-h", "--help"} & set(args):
        sys.exit(__doc__)
    first_path = HERE.parent / "audit.csv"
    if "--first" in args:
        first_path = Path(args[args.index("--first") + 1])
    print(f"first coding: {first_path.name} (the paper's 88/95 and 79/86 use online-gates-coder1-preadjudication.csv)\n")
    first = {r["key"]: r for r in csv.DictReader(open(first_path))}
    audit = {r["key"]: r for r in csv.DictReader(open(HERE.parent / "audit.csv"))}
    check = {r["key"]: r for r in csv.DictReader(open(HERE / "online-gates-check.csv"))}
    online = {k for k, r in audit.items() if r["c2"] == "online" and r["set"] == "core"}
    total, pooled, by_item = [0, 0], [], {}
    print("item           all loops   online-selecting  kappa")
    for c in COLS:
        pairs = {k: (first[k][c].strip().lower(), check[k][c].strip().lower()) for k in check}
        n_all = sum(a == b for a, b in pairs.values())
        n_on = sum(pairs[k][0] == pairs[k][1] for k in pairs if k in online)
        total[0] += n_all
        total[1] += len(pairs)
        pooled += pairs.values()
        by_item[c] = list(pairs.values())
        k = kappa(by_item[c])[1]
        print(f"{c:14} {n_all:3}/{len(pairs):<6} {n_on:3}/{len(online & set(pairs)):<13} {k:.2f}")
    applicable = [(a, b) for a, b in pooled if not (a == b == "na")]
    print(f"{'stratified':14} {total[0]:3}/{total[1]}  kappa {strat_kappa(list(by_item.values())):.2f}")
    print(f"{'pooled':14} {total[0]:3}/{total[1]}  kappa {kappa(pooled)[1]:.2f}")
    print(f"{'applicable':14} {sum(a == b for a, b in applicable):3}/{len(applicable)}  kappa {kappa(applicable)[1]:.2f}\n")
    for k in check:
        for c in COLS:
            a, b = first[k][c].strip(), check[k][c].strip()
            if a.lower() != b.lower():
                print(f"  {audit[k]['system']}: {c} first={a} check={b}")


if __name__ == "__main__":
    main()
