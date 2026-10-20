"""Leaderboard: aggregate result records over seeds into one Markdown table per dataset."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import numpy as np

from .run import RUNS_DIR

COLUMNS = ("hr@10", "ndcg@10", "hr@20", "ndcg@20", "mrr")


def collect(runs_dir: Path = RUNS_DIR) -> List[Dict]:
    return [json.loads(p.read_text()) for p in sorted(runs_dir.glob("*/*/*.json"))]


def leaderboard(records: List[Dict], split: str = "test", sort_by: str = "ndcg@10") -> str:
    groups = defaultdict(list)
    for r in records:
        groups[(r["dataset"], r["protocol"], r["model"], r["config_hash"])].append(r)
    by_dataset = defaultdict(list)
    for (ds, proto, model, h), rs in groups.items():
        row = {"model": model, "hash": h, "seeds": len(rs),
               "fit_min": np.mean([r["fit_seconds"] for r in rs]) / 60}
        for c in COLUMNS:
            v = np.array([r[split][c] for r in rs])
            row[c] = (v.mean(), v.std(ddof=1) if len(v) > 1 else 0.0)
        by_dataset[(ds, proto)].append(row)

    out = []
    for (ds, proto), rows in sorted(by_dataset.items()):
        rows.sort(key=lambda r: -r[sort_by][0])
        out.append(f"### {ds} ({split}, protocol {proto})\n")
        out.append("| model | config | seeds | " + " | ".join(COLUMNS) + " | fit (min) |")
        out.append("|---|---|---|" + "---|" * len(COLUMNS) + "---|")
        for r in rows:
            cells = [f"{m:.4f} ± {s:.4f}" if r["seeds"] > 1 else f"{m:.4f}" for m, s in (r[c] for c in COLUMNS)]
            out.append(f"| {r['model']} | {r['hash']} | {r['seeds']} | " + " | ".join(cells) + f" | {r['fit_min']:.1f} |")
        out.append("")
    return "\n".join(out)
