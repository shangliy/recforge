"""Leaderboard: aggregate result records over seeds into one table per dataset."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


COLUMNS = ("hr@10", "ndcg@10", "hr@20", "ndcg@20", "mrr@100")


def collect(runs_dir: Optional[Path] = None) -> List[Dict]:
    from . import run
    runs_dir = run.RUNS_DIR if runs_dir is None else runs_dir
    return [json.loads(p.read_text()) for p in sorted(runs_dir.glob("*/*/*.json"))]


def aggregate(records: List[Dict], split: str = "test", datasets: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
    """{dataset: [row, ...]} with one row per (model, config hash), mean and std over seeds, best first by NDCG@10."""
    groups = defaultdict(list)
    for r in records:
        if r.get(split) is None or (datasets and r["dataset"] not in datasets):
            continue
        groups[(r["dataset"], r["protocol"], r["model"], r["config_hash"])].append(r)
    out = defaultdict(list)
    for (ds, proto, model, h), rs in groups.items():
        row = {"model": model, "config_hash": h, "protocol": proto, "seeds": sorted(r["seed"] for r in rs),
               "minutes": round(float(np.mean([r["seconds"] for r in rs])) / 60, 2)}
        for c in COLUMNS:
            v = np.array([r[split].get(c, np.nan) for r in rs])
            row[c] = {"mean": round(float(v.mean()), 5), "std": round(float(v.std(ddof=1)) if len(v) > 1 else 0.0, 5)}
        out[f"{ds} ({proto})"].append(row)
    for rows in out.values():
        rows.sort(key=lambda r: -r["ndcg@10"]["mean"])
    return dict(sorted(out.items()))


def to_markdown(table: Dict[str, List[Dict]], split: str = "test") -> str:
    out = []
    for ds, rows in table.items():
        out.append(f"### {ds}, {split}\n")
        out.append("| model | config | seeds | " + " | ".join(COLUMNS) + " | min/run |")
        out.append("|---|---|---|" + "---|" * len(COLUMNS) + "---|")
        for r in rows:
            n = len(r["seeds"])
            cells = [f"{r[c]['mean']:.4f} ± {r[c]['std']:.4f}" if n > 1 else f"{r[c]['mean']:.4f}" for c in COLUMNS]
            out.append(f"| {r['model']} | {r['config_hash']} | {n} | " + " | ".join(cells) + f" | {r['minutes']:.1f} |")
        out.append("")
    return "\n".join(out)
