"""Command line.

    python -m recforge data ml1m                          build/cache a dataset and print its stats
    python -m recforge run ml1m sasrec --seeds 1,2,3 --device cuda --set dim=128
    python -m recforge board [--split val]                print the leaderboard
"""
from __future__ import annotations

import argparse
import ast
import json
import sys

from .board import collect, leaderboard


def _parse_set(items):
    out = {}
    for it in items or []:
        k, _, v = it.partition("=")
        try:
            out[k] = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            out[k] = v
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="recforge")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("data", help="build and describe a dataset")
    d.add_argument("dataset")

    r = sub.add_parser("run", help="train and evaluate a model")
    r.add_argument("dataset")
    r.add_argument("models", help="comma-separated, e.g. pop,itemknn,sasrec")
    r.add_argument("--seeds", default="1")
    r.add_argument("--device", default="cpu")
    r.add_argument("--set", action="append", metavar="KEY=VALUE", help="config override, repeatable")
    r.add_argument("--val-users", type=int, default=None, help="subsample users for early-stopping checks")
    r.add_argument("--force", action="store_true")

    b = sub.add_parser("board", help="print the leaderboard")
    b.add_argument("--split", default="test", choices=["val", "test"])
    b.add_argument("--sort", default="ndcg@10")

    a = p.parse_args(argv)
    if a.cmd == "data":
        from .data import load
        data = load(a.dataset)
        print(json.dumps({"name": data.name, **data.stats(), **data.info}, indent=1))
    elif a.cmd == "run":
        from .run import run_one
        overrides, models = _parse_set(a.set), a.models.split(",")
        if overrides and len(models) > 1:
            p.error("--set applies to one model; run models separately to override their configs")
        for model in models:
            for seed in (int(s) for s in a.seeds.split(",")):
                rec = run_one(a.dataset, model, overrides, seed, a.device, force=a.force, val_users=a.val_users)
                t = rec["test"]
                print(f"{a.dataset} {model} s{seed} [{rec['config_hash']}]  test hr@10={t['hr@10']:.4f} "
                      f"ndcg@10={t['ndcg@10']:.4f}  fit {rec['fit_seconds']:.0f}s", flush=True)
    elif a.cmd == "board":
        print(leaderboard(collect(), a.split, a.sort))
    return 0


if __name__ == "__main__":
    sys.exit(main())
