"""Command line. Every command takes --json for machine-readable output (one JSON document on stdout).

    recforge suites                                     list benchmark suites
    recforge bench --model sasrec --suite ml1m --device cuda [--baselines]
    recforge bench --model my_model.py:MyModel --suite smoke
    recforge new my_model.py                            copy the model template
    recforge run ml1m sasrec --seeds 1,2,3 --set dim=128
    recforge board [--split val]
    recforge data ml1m

    recforge session create NAME --dataset ml1m --max-trials 20 --max-minutes 120
    recforge session trial NAME --model my_model.py:MyModel --set lr=0.003 --note "why"
    recforge session status NAME
    recforge session finalize NAME --trial 7
"""
from __future__ import annotations

import argparse
import ast
import json
import shutil
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "templates" / "model_template.py"


def _parse_set(items):
    out = {}
    for it in items or []:
        k, _, v = it.partition("=")
        try:
            out[k] = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            out[k] = v
    return out


def _common(p, device=True):
    p.add_argument("--json", action="store_true", help="print one JSON document")
    if device:
        p.add_argument("--device", default="cpu", help="cpu, cuda or cuda:N")
        p.add_argument("--val-users", type=int, default=None, help="subsample users for early-stopping checks")


def _parser():
    p = argparse.ArgumentParser(prog="recforge")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("suites", help="list benchmark suites")
    _common(s, device=False)

    b = sub.add_parser("bench", help="run a method on a suite and show it among the baselines")
    b.add_argument("--model", required=True, help="built-in name or path/to/file.py:ClassName")
    b.add_argument("--suite", default="smoke")
    b.add_argument("--set", action="append", metavar="KEY=VALUE")
    b.add_argument("--baselines", action="store_true", help="also run the built-in baselines on this suite")
    _common(b)

    n = sub.add_parser("new", help="write a model template to start from")
    n.add_argument("path")

    r = sub.add_parser("run", help="train and evaluate models on one dataset")
    r.add_argument("dataset")
    r.add_argument("models", help="comma-separated specs")
    r.add_argument("--seeds", default="1")
    r.add_argument("--set", action="append", metavar="KEY=VALUE")
    r.add_argument("--force", action="store_true")
    _common(r)

    bo = sub.add_parser("board", help="print the leaderboard")
    bo.add_argument("--split", default="test", choices=["val", "test"])
    _common(bo, device=False)

    d = sub.add_parser("data", help="build and describe a dataset")
    d.add_argument("dataset")
    _common(d, device=False)

    se = sub.add_parser("session", help="budgeted evolve session: validation during search, test once")
    ssub = se.add_subparsers(dest="action", required=True)
    c = ssub.add_parser("create")
    c.add_argument("name")
    c.add_argument("--dataset", required=True)
    c.add_argument("--max-trials", type=int, default=20)
    c.add_argument("--max-minutes", type=float, default=120.0)
    c.add_argument("--seed", type=int, default=1)
    _common(c, device=False)
    t = ssub.add_parser("trial")
    t.add_argument("name")
    t.add_argument("--model", required=True)
    t.add_argument("--set", action="append", metavar="KEY=VALUE")
    t.add_argument("--note", default="")
    _common(t)
    st = ssub.add_parser("status")
    st.add_argument("name")
    _common(st, device=False)
    f = ssub.add_parser("finalize")
    f.add_argument("name")
    f.add_argument("--trial", type=int, required=True)
    _common(f, device=False)
    return p


def _emit(a, obj, text: str) -> None:
    print(json.dumps(obj, indent=1) if a.json else text, flush=True)


def main(argv=None) -> int:
    p = _parser()
    a = p.parse_args(argv)
    log = (lambda m: print(m, file=sys.stderr, flush=True)) if getattr(a, "json", False) else print
    try:
        return _dispatch(p, a, log)
    except (KeyError, ValueError, TypeError, FileNotFoundError, FileExistsError, PermissionError, RuntimeError) as e:
        msg = e.args[0] if e.args else str(e)
        if getattr(a, "json", False):
            print(json.dumps({"error": type(e).__name__, "message": str(msg)}))
        else:
            print(f"error: {msg}", file=sys.stderr)
        return 1


def _dispatch(p, a, log) -> int:
    from .board import aggregate, collect, to_markdown

    if a.cmd == "suites":
        from .bench import BASELINES, SUITES
        _emit(a, {"suites": SUITES, "baselines": BASELINES},
              "\n".join(f"{k:9} {v['datasets']} seeds {v['seeds']}  {v['about']}" for k, v in SUITES.items()))
    elif a.cmd == "bench":
        from .bench import run_suite
        res = run_suite(a.model, a.suite, a.device, _parse_set(a.set), a.baselines, a.val_users, log)
        _emit(a, res, to_markdown(res["leaderboard"]))
    elif a.cmd == "new":
        dst = Path(a.path)
        if dst.exists():
            raise FileExistsError(f"{dst} exists")
        shutil.copy(TEMPLATE, dst)
        print(f"wrote {dst}; try: python -m recforge bench --model {dst}:MarkovChain --suite smoke")
    elif a.cmd == "run":
        from .run import run_one
        overrides, specs = _parse_set(a.set), a.models.split(",")
        if overrides and len(specs) > 1:
            p.error("--set applies to one model; run models separately to override their configs")
        recs = []
        for spec in specs:
            for seed in (int(s) for s in a.seeds.split(",")):
                rec = run_one(a.dataset, spec, overrides, seed, a.device, force=a.force, val_users=a.val_users)
                recs.append(rec)
                log(f"{a.dataset} {rec['model']} s{seed} [{rec['config_hash']}]  test ndcg@10="
                    f"{rec['test']['ndcg@10']:.4f} hr@10={rec['test']['hr@10']:.4f}  {rec['seconds']:.0f}s")
        if a.json:
            print(json.dumps(recs, indent=1))
    elif a.cmd == "board":
        table = aggregate(collect(), a.split)
        _emit(a, table, to_markdown(table, a.split))
    elif a.cmd == "data":
        from .data import load
        data = load(a.dataset)
        info = {"name": data.name, **data.stats(), **data.info}
        _emit(a, info, json.dumps(info, indent=1))
    elif a.cmd == "session":
        from . import evolve
        if a.action == "create":
            s = evolve.create(a.name, a.dataset, a.max_trials, a.max_minutes, a.seed)
            _emit(a, s, f"session {a.name}: {a.dataset}, budget {s['budget']}")
        elif a.action == "trial":
            r = evolve.trial(a.name, a.model, _parse_set(a.set), a.device, a.val_users, a.note)
            v = r["trial"]["val"]
            _emit(a, r, f"trial {r['trial']['id']} [{r['trial']['config_hash']}] val ndcg@10={v['ndcg@10']:.4f} "
                        f"hr@10={v['hr@10']:.4f}; used {r['used']} of {r['budget']}")
        elif a.action == "status":
            s = evolve.load(a.name)
            lines = [f"session {a.name}: {s['dataset']}, used {s['used']} of {s['budget']}, final {s['final']}"]
            lines += [f"  {t['id']:3} {t['model']:12} val ndcg@10={t['val']['ndcg@10']:.4f}  {t['note']}"
                      for t in s["trials"]]
            _emit(a, s, "\n".join(lines))
        elif a.action == "finalize":
            r = evolve.finalize(a.name, a.trial)
            _emit(a, r, f"session {a.name} final trial {a.trial}: test {json.dumps(r['test'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
