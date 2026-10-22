"""Kuaishou OpenOneRec / RecIF-Bench user behaviour (Hugging Face `OpenOneRec/OpenOneRec-RecIF`, Apache-2.0).

`onerec_bench_release.parquet` has one row per user (`uid`) with chronological per-domain lists. We use two
domains, each a separate dataset:

- `kuai-video`: `hist_video_pid` followed by `target_video_pid`. A view counts as an interaction when it is a
  long view, like, follow or forward and the user did not mark it not-interested. The flags are aligned with
  the id lists; plain views are dropped because most short-video exposures are not a preference signal.
- `kuai-goods`: `hist_goods_pid` followed by `target_goods_pid` (browsed products; no flags are released).

The release has no timestamps, so sequence position is the time. The release's own `split` column and target
lists are ignored: loo-2 holds out each user's last two items itself. Item text is the `caption` from
`pid2caption.parquet` (5.9 GB) when that file is present; video and goods ids are separate id spaces, so only
`kuai-video` gets captions. `kuai-video-50k` is a fixed 50k-user sample (seed 0) for runs that do not fit the
full data in memory.

The dataset is gated: accept its terms on huggingface.co with your account, then put a token in `HF_TOKEN` or
`~/.cache/huggingface/token`. Files are read in record batches, never whole.
"""
from __future__ import annotations

import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from .schema import SeqData, build

REPO = "OpenOneRec/OpenOneRec-RecIF"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/main"
MAIN, CAPTIONS = "onerec_bench_release.parquet", "pid2caption.parquet"
POSITIVE = ("hist_video_longview", "hist_video_like", "hist_video_follow", "hist_video_forward")
SAMPLES = {"kuai-video-50k": ("kuai-video", 50_000)}


def _token() -> Optional[str]:
    if os.environ.get("HF_TOKEN"):
        return os.environ["HF_TOKEN"]
    path = Path.home() / ".cache" / "huggingface" / "token"
    return path.read_text().strip() if path.exists() else None


def _ensure(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(f"{BASE}/{path.name}")
    if _token():
        req.add_header("Authorization", f"Bearer {_token()}")
    tmp = path.with_suffix(".part")
    try:
        with urllib.request.urlopen(req) as r, open(tmp, "wb") as f:
            while chunk := r.read(1 << 24):
                f.write(chunk)
    except urllib.error.HTTPError as e:
        tmp.unlink(missing_ok=True)
        if e.code in (401, 403):
            raise PermissionError(f"{REPO} is gated: accept its terms at https://huggingface.co/datasets/{REPO} "
                                  f"and set HF_TOKEN, or place {path.name} in {path.parent}") from e
        raise
    tmp.rename(path)


def _video_rows(batch) -> Dict[int, List[int]]:
    cols = {c: batch.column(c).to_pylist() for c in ("uid", "hist_video_pid", "target_video_pid",
                                                      "hist_video_not_interested", *POSITIVE)}
    out = {}
    for i, uid in enumerate(cols["uid"]):
        pids = cols["hist_video_pid"][i] or []
        flags = [cols[c][i] or [0] * len(pids) for c in POSITIVE]
        bad = cols["hist_video_not_interested"][i] or [0] * len(pids)
        keep = [p for j, p in enumerate(pids) if any(f[j] for f in flags) and not bad[j]]
        out[uid] = keep + list(cols["target_video_pid"][i] or [])
    return out


def _goods_rows(batch) -> Dict[int, List[int]]:
    uids, hist, tgt = (batch.column(c).to_pylist() for c in ("uid", "hist_goods_pid", "target_goods_pid"))
    return {u: list(h or []) + list(t or []) for u, h, t in zip(uids, hist, tgt)}


def _captions(path: Path, items: set) -> Dict[int, str]:
    import pyarrow.parquet as pq
    out = {}
    for batch in pq.ParquetFile(path).iter_batches(batch_size=200_000, columns=["pid", "caption"]):
        for p, c in zip(batch.column("pid").to_pylist(), batch.column("caption").to_pylist()):
            if p in items and c:
                out[p] = c
    return out


def build_openonerec(raw: Path, name: str) -> SeqData:
    import pyarrow.parquet as pq
    domain, n_sample = SAMPLES.get(name, (name, None))
    _ensure(raw / MAIN)
    if domain == "kuai-video":
        cols = ["uid", "hist_video_pid", "target_video_pid", "hist_video_not_interested", *POSITIVE]
        rows = _video_rows
    elif domain == "kuai-goods":
        cols, rows = ["uid", "hist_goods_pid", "target_goods_pid"], _goods_rows
    else:
        raise KeyError(name)
    f = pq.ParquetFile(raw / MAIN)
    keep = None
    if n_sample:
        uids = np.concatenate([b.column("uid").to_numpy() for b in f.iter_batches(columns=["uid"])])
        rng = np.random.default_rng(0)
        keep = set(rng.choice(np.sort(uids), size=min(n_sample, len(uids)), replace=False).tolist())
    user_items: Dict[int, List[int]] = {}
    for batch in f.iter_batches(batch_size=4096, columns=cols):
        for uid, seq in rows(batch).items():
            if keep is None or uid in keep:
                user_items[uid] = seq
    meta = {}
    if domain == "kuai-video" and (raw / CAPTIONS).exists():
        meta["title"] = _captions(raw / CAPTIONS, {p for s in user_items.values() for p in s})
    feedback = ("long view, like, follow or forward, not marked not-interested" if domain == "kuai-video"
                else "browsed products")
    return build(name, user_items, meta,
                 {"source": f"{BASE}/{MAIN}", "license": "Apache-2.0", "feedback": feedback,
                  "order": "release order (no timestamps)",
                  **({"sample": f"{n_sample} users, seed 0"} if n_sample else {})})
