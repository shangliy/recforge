"""Train and rank in a separate process; the parent keeps the targets.

The child receives only the train view (seq[:-2] per user). During fit, each
val_fn() call sends the model's ranked lists for the validation histories and
gets back NDCG@10. After fit, the parent sends the test histories (which end
with the validation item) and their timestamps, and receives the final lists.

This stops model code from reading targets through the API. It does not stop
code that opens the raw data files itself; for untrusted agents, run recforge
inside a container that mounts only the train view (see docs/AGENTS.md).
"""
from __future__ import annotations

import multiprocessing as mp
import os
import tempfile
import traceback
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np

from .data.schema import SeqData
from .eval import metrics_from_lists, rank_lists


def _child(conn, spec: str, cfg: Dict, seed: int, device: str, view_path: str, val_users: Optional[int]) -> None:
    try:
        from .models import get
        from .run import set_seed
        set_seed(seed)
        frac = os.environ.get("RECFORGE_GPU_FRAC")
        if frac and device.startswith("cuda"):
            import torch
            # Hard cap for shared GPUs: past it this process gets an OOM error instead of starving others.
            torch.cuda.set_per_process_memory_fraction(float(frac), torch.device(device))
        data = SeqData.load(Path(view_path))
        model = get(spec)(cfg, seed, device)
        users = np.arange(data.n_users)
        check = users if val_users is None or val_users >= data.n_users else \
            np.sort(np.random.default_rng(0).choice(data.n_users, val_users, replace=False))

        def val_fn() -> float:
            conn.send(("val", check, rank_lists(model, check, [data.seqs[i] for i in check], data.n_items,
                                                [data.times[i] for i in check])))
            return conn.recv()

        info = model.fit(data, val_fn)
        conn.send(("fit_done", info, rank_lists(model, users, data.seqs, data.n_items, data.times)))
        test_hist, test_times = conn.recv()
        conn.send(("test", rank_lists(model, users, test_hist, data.n_items, test_times)))
    except BaseException:
        conn.send(("error", traceback.format_exc()))
    finally:
        conn.close()


def train_and_rank(spec: str, cfg: Dict, seed: int, device: str, data: SeqData,
                   val_users: Optional[int] = None) -> Tuple[Dict, np.ndarray, np.ndarray]:
    """(fit info, val lists, test lists) for every user, in user order."""
    _, val_t = data.split("val")
    test_h, _, test_times = data.split_with_times("test")
    ctx = mp.get_context("spawn")
    parent, child = ctx.Pipe()
    with tempfile.TemporaryDirectory() as tmp:
        view_path = Path(tmp) / "train_view.npz"
        data.train_view().save(view_path)
        proc = ctx.Process(target=_child, args=(child, spec, cfg, seed, device, str(view_path), val_users))
        proc.start()
        child.close()
        try:
            while True:
                try:
                    msg = parent.recv()
                except EOFError:
                    raise RuntimeError(f"model process exited (code {proc.exitcode}) without a result") from None
                if msg[0] == "val":
                    parent.send(metrics_from_lists(msg[2], val_t[msg[1]])["ndcg@10"])
                elif msg[0] == "fit_done":
                    info, val_lists = msg[1], msg[2]
                    parent.send((test_h, test_times))
                elif msg[0] == "test":
                    test_lists = msg[1]
                    break
                elif msg[0] == "error":
                    raise RuntimeError("model process failed:\n" + msg[1])
        finally:
            proc.join(timeout=30)
            if proc.is_alive():
                proc.kill()
    return info, val_lists, test_lists
