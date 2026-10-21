"""TIGER (Rajput et al., NeurIPS 2023, "Recommender Systems with Generative Retrieval").

1. Item text -> Sentence-T5 embedding (768-d) from item_meta fields (title, brand, categories, price, ...).
2. RQ-VAE: encoder 768-512-256-128-32 (ReLU), 3 residual codebooks of 256 x 32, beta 0.25, k-means init on
   the first batch, Adagrad lr 0.4, batch 1024, 20k epochs. Items sharing a 3-code prefix get a 4th code
   0, 1, ... in id order; others get 0.
3. T5 encoder-decoder (4 + 4 layers, 6 heads of 64, d_model 128, MLP 1024, ReLU, dropout 0.1). Input: a
   hashed user token (2000 buckets) then the codes of the last 20 history items; output: the 4 codes of the
   next item. Batch 256, lr 0.01 for 10k steps then inverse square root decay, 200k steps (Adafactor, the
   T5X default; the paper names T5X but not the optimizer).
4. score(): beam search constrained to existing semantic IDs, so every beam is a real item. Beam items get
   their sequence log-probability; all other items -inf.

Paper (Table 1), Amazon Beauty: Recall@5 0.0454, NDCG@5 0.0321, Recall@10 0.0648, NDCG@10 0.0384, under the
same leave-one-out split as loo-2. Differences here: the paper does not remove history items from the ranking
(recforge does, for every model), and this T5 has 4.8M parameters where the paper reports about 13M.

text_encoder="random" replaces text embeddings with fixed random vectors (the paper's Random ID ablation);
the tests use it because the synthetic dataset has no text.
"""
from __future__ import annotations

import hashlib
import warnings
from typing import Dict, List

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .base import EarlyStopper, Recommender

PAD, EOS, OFFSET = 0, 1, 2
TEXT_FIELDS = ("title", "brand", "categories", "price", "genres", "category", "subcategory")


# ---- 1. item text embeddings ------------------------------------------------------------------------------

def item_texts(item_meta: Dict[str, list], n_items: int) -> List[str]:
    fields = [f for f in TEXT_FIELDS if f in item_meta]
    out = []
    for i in range(1, n_items + 1):
        parts = [f"{f}: {item_meta[f][i]}" for f in fields if item_meta[f][i] not in (None, "")]
        out.append("; ".join(parts) or f"item {i}")
    return out


def item_embeddings(data, encoder: str, device: str, seed: int) -> np.ndarray:
    """(n_items, D) float32, cached on disk by encoder and text content."""
    if encoder == "random":
        return np.random.default_rng(seed).standard_normal((data.n_items, 768)).astype(np.float32)
    texts = item_texts(data.item_meta, data.n_items)
    if not any(f in data.item_meta for f in TEXT_FIELDS):
        raise ValueError(f"dataset {data.name!r} has no item text; use text_encoder='random'")
    from ..data import CACHE_DIR
    key = hashlib.sha1((encoder + "\n" + "\n".join(texts)).encode()).hexdigest()[:12]
    path = CACHE_DIR / "emb" / f"{data.name}-{key}.npy"
    if path.exists():
        return np.load(path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from sentence_transformers import SentenceTransformer
        st = SentenceTransformer(encoder, device=device)
        emb = st.encode(texts, batch_size=256, convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    del st
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, emb)
    return emb


# ---- 2. RQ-VAE --------------------------------------------------------------------------------------------

def _mlp(dims: List[int]) -> nn.Sequential:
    layers = []
    for a, b in zip(dims[:-1], dims[1:]):
        layers += [nn.Linear(a, b), nn.ReLU()]
    return nn.Sequential(*layers[:-1])


def _kmeans(x: torch.Tensor, k: int, iters: int, gen: torch.Generator) -> torch.Tensor:
    """k centres; when x has fewer than k points, extra centres start at sampled points (and may stay empty)."""
    start = torch.randperm(len(x), generator=gen)[:k] if len(x) >= k else torch.randint(len(x), (k,), generator=gen)
    c = x[start.to(x.device)].clone()
    for _ in range(iters):
        assign = torch.cdist(x, c).argmin(1)
        counts = torch.bincount(assign, minlength=k).float()
        sums = torch.zeros_like(c).index_add_(0, assign, x)
        c = torch.where(counts[:, None] > 0, sums / counts.clamp(min=1)[:, None], c)
    return c


class RQVAE(nn.Module):
    def __init__(self, in_dim: int, hidden: List[int], latent: int, levels: int, codebook: int, beta: float):
        super().__init__()
        self.beta = beta
        self.enc = _mlp([in_dim, *hidden, latent])
        self.dec = _mlp([latent, *reversed(hidden), in_dim])
        self.books = nn.ModuleList(nn.Embedding(codebook, latent) for _ in range(levels))

    def quantize(self, z: torch.Tensor):
        r, zq, loss, codes = z, torch.zeros_like(z), z.new_zeros(()), []
        for book in self.books:
            c = torch.cdist(r, book.weight).argmin(1)
            e = book(c)
            loss = loss + ((r.detach() - e) ** 2).sum(-1).mean() + self.beta * ((r - e.detach()) ** 2).sum(-1).mean()
            zq, r = zq + e, r - e.detach()
            codes.append(c)
        return z + (zq - z).detach(), torch.stack(codes, 1), loss

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        zq, _, qloss = self.quantize(self.enc(x))
        return ((self.dec(zq) - x) ** 2).sum(-1).mean() + qloss

    @torch.no_grad()
    def init_codebooks(self, x: torch.Tensor, gen: torch.Generator) -> None:
        r = self.enc(x)
        for book in self.books:
            book.weight.copy_(_kmeans(r, book.num_embeddings, 20, gen))
            r = r - book.weight[torch.cdist(r, book.weight).argmin(1)]


def semantic_ids(emb: np.ndarray, c: Dict, seed: int, device: str) -> tuple[np.ndarray, Dict]:
    """(n_items + 1, levels + 1) codes, row 0 unused, plus stats."""
    gen = torch.Generator().manual_seed(seed)
    x = torch.as_tensor(emb, device=device)
    rq = RQVAE(x.shape[1], c["rq_hidden"], c["rq_latent"], c["rq_levels"], c["rq_codebook"], c["rq_beta"]).to(device)
    rq.init_codebooks(x[torch.randperm(len(x), generator=gen)[:c["rq_batch"]].to(device)], gen)
    opt = torch.optim.Adagrad(rq.parameters(), lr=c["rq_lr"])
    for _ in range(c["rq_epochs"]):
        for idx in torch.randperm(len(x), generator=gen).split(c["rq_batch"]):
            loss = rq(x[idx.to(device)])
            opt.zero_grad()
            loss.backward()
            opt.step()
    rq.eval()
    with torch.no_grad():
        codes = rq.quantize(rq.enc(x))[1].cpu().numpy()
    last = np.zeros(len(codes), dtype=np.int64)
    seen: Dict[tuple, int] = {}
    for i, row in enumerate(map(tuple, codes)):
        last[i] = seen.get(row, 0)
        seen[row] = last[i] + 1
    full = np.concatenate([codes, last[:, None]], 1)
    stats = {"rq_final_loss": round(float(loss.detach()), 5), "unique_prefixes": len(seen),
             "max_collisions": int(last.max()) + 1,
             "codebook_usage": [round(len(np.unique(codes[:, l])) / c["rq_codebook"], 3) for l in range(codes.shape[1])]}
    return np.concatenate([np.zeros((1, full.shape[1]), dtype=np.int64), full]), stats


# ---- 3-4. generative retrieval ----------------------------------------------------------------------------

class PrefixIndex:
    """Which next code is valid after each prefix, and which item a full code tuple is."""

    def __init__(self, codes: np.ndarray, sizes: List[int], device: str):
        self.sizes, self.device = sizes, device
        items = torch.as_tensor(codes[1:], device=device)
        n = len(items)
        self.masks, self.keys = [], []
        key = torch.zeros(n, dtype=torch.long, device=device)
        for t, k in enumerate(sizes):
            uniq, row = torch.unique(key, return_inverse=True)
            m = torch.zeros(len(uniq), k, dtype=torch.bool, device=device)
            m[row, items[:, t]] = True
            self.keys.append(uniq)
            self.masks.append(m)
            key = key * k + items[:, t]
        order = key.argsort()
        self.full_keys, self.full_items = key[order], order + 1

    @staticmethod
    def _find(sorted_keys: torch.Tensor, key: torch.Tensor):
        pos = torch.searchsorted(sorted_keys, key).clamp(max=len(sorted_keys) - 1)
        return pos, sorted_keys[pos] == key

    def allowed(self, t: int, prefix_key: torch.Tensor) -> torch.Tensor:
        """(N, sizes[t]) valid next codes; an unknown prefix (a dead beam) allows none."""
        pos, found = self._find(self.keys[t], prefix_key)
        return self.masks[t][pos] & found[:, None]

    def items(self, full_key: torch.Tensor) -> torch.Tensor:
        """Item id per full code tuple; 0 where no item has it."""
        pos, found = self._find(self.full_keys, full_key)
        return torch.where(found, self.full_items[pos], 0)


class TIGER(Recommender):
    name = "tiger"
    DEFAULTS = {"text_encoder": "sentence-transformers/sentence-t5-base",
                "rq_hidden": [512, 256, 128], "rq_latent": 32, "rq_levels": 3, "rq_codebook": 256, "rq_beta": 0.25,
                "rq_lr": 0.4, "rq_batch": 1024, "rq_epochs": 20000,
                "d_model": 128, "d_kv": 64, "d_ff": 1024, "heads": 6, "layers": 4, "dropout": 0.1,
                "user_buckets": 2000, "max_items": 20,
                "steps": 200000, "batch_size": 256, "lr": 0.01, "warmup_steps": 10000,
                "eval_every": 5000, "patience": 10, "beam": 30}

    # token layout: PAD, EOS, then one block per code level, then user buckets
    def _layout(self, codes: np.ndarray) -> None:
        self.sizes = [self.cfg["rq_codebook"]] * self.cfg["rq_levels"] + [max(self.cfg["rq_codebook"], int(codes[:, -1].max()) + 1)]
        self.level_off = np.cumsum([OFFSET] + self.sizes[:-1])
        self.user_off = OFFSET + sum(self.sizes)
        self.vocab = self.user_off + self.cfg["user_buckets"]
        self.tokens = torch.as_tensor(codes + self.level_off[None, :], dtype=torch.long)   # (n_items + 1, 4)
        self.tokens[0] = PAD

    def _user_token(self, users: np.ndarray) -> torch.Tensor:
        return torch.as_tensor(self.user_off + (users.astype(np.int64) * 2654435761) % self.cfg["user_buckets"])

    def _encode_inputs(self, users: np.ndarray, histories: List[np.ndarray]):
        m = self.cfg["max_items"]
        rows = [torch.cat([self._user_token(np.array([u])), self.tokens[h[-m:]].reshape(-1), torch.tensor([EOS])])
                for u, h in zip(users, histories)]
        ids = nn.utils.rnn.pad_sequence(rows, batch_first=True, padding_value=PAD)
        return ids.to(self.device), (ids != PAD).to(self.device)

    def fit(self, data, val_fn):
        c = self.cfg
        emb = item_embeddings(data, c["text_encoder"], self.device, self.seed)
        codes, info = semantic_ids(emb, c, self.seed, self.device)
        self._layout(codes)
        self.index = PrefixIndex(codes, self.sizes, self.device)

        from transformers import T5Config, T5ForConditionalGeneration
        from transformers.optimization import Adafactor
        cfg = T5Config(vocab_size=self.vocab, d_model=c["d_model"], d_kv=c["d_kv"], d_ff=c["d_ff"],
                       num_layers=c["layers"], num_decoder_layers=c["layers"], num_heads=c["heads"],
                       dropout_rate=c["dropout"], feed_forward_proj="relu", pad_token_id=PAD, eos_token_id=EOS,
                       decoder_start_token_id=PAD)
        torch.manual_seed(self.seed)
        self.net = T5ForConditionalGeneration(cfg).to(self.device)
        info["params"] = sum(p.numel() for p in self.net.parameters())

        users, hists, targets = [], [], []
        for u, s in enumerate(data.train_seqs()):
            for t in range(1, len(s)):
                users.append(u)
                hists.append(s[max(0, t - c["max_items"]):t])
                targets.append(s[t])
        users, targets = np.array(users), np.array(targets)
        info["train_examples"] = len(targets)

        opt = Adafactor(self.net.parameters(), lr=c["lr"], scale_parameter=False, relative_step=False,
                        warmup_init=False)
        sched = torch.optim.lr_scheduler.LambdaLR(
            opt, lambda s: min(1.0, (c["warmup_steps"] / max(s, 1)) ** 0.5))
        gen = torch.Generator().manual_seed(self.seed)
        stopper = EarlyStopper(self.net, c["patience"])
        step = 0
        while step < c["steps"] and not stopper.stop():
            for idx in torch.randperm(len(targets), generator=gen).split(c["batch_size"]):
                self.net.train()
                idx = idx.numpy()
                ids, mask = self._encode_inputs(users[idx], [hists[i] for i in idx])
                labels = self.tokens[targets[idx]].to(self.device)
                loss = self.net(input_ids=ids, attention_mask=mask, labels=labels).loss
                opt.zero_grad()
                loss.backward()
                opt.step()
                sched.step()
                step += 1
                if step % c["eval_every"] == 0 or step == c["steps"]:
                    stopper.update(val_fn())
                    if stopper.stop() or step >= c["steps"]:
                        break
        info.update(stopper.restore())
        info["steps"] = step
        return info

    @torch.no_grad()
    def score(self, users, histories, batch: int = 128):
        from transformers.modeling_outputs import BaseModelOutput
        self.net.eval()
        n_items = len(self.tokens) - 1
        out = torch.full((len(users), n_items + 1), -torch.inf)
        for lo in range(0, len(users), batch):
            ids, mask = self._encode_inputs(users[lo:lo + batch], histories[lo:lo + batch])
            enc = self.net.encoder(input_ids=ids, attention_mask=mask).last_hidden_state
            b = len(ids)
            scores = torch.zeros(b, 1, device=self.device)
            keys = torch.zeros(b, 1, dtype=torch.long, device=self.device)
            dec = torch.full((b, 1, 1), PAD, dtype=torch.long, device=self.device)
            for t, k in enumerate(self.sizes):
                w = dec.shape[1]
                logits = self.net(encoder_outputs=BaseModelOutput(last_hidden_state=enc.repeat_interleave(w, 0)),
                                  attention_mask=mask.repeat_interleave(w, 0),
                                  decoder_input_ids=dec.reshape(b * w, -1)).logits[:, -1]
                off = int(self.level_off[t])
                logp = F.log_softmax(logits, -1)[:, off:off + k]
                logp = logp.masked_fill(~self.index.allowed(t, keys.reshape(-1)), -torch.inf).view(b, w, k)
                total = (scores[:, :, None] + logp).view(b, w * k)
                scores, flat = total.topk(min(self.cfg["beam"], w * k), dim=1)
                parent, code = flat // k, flat % k
                keys = keys.gather(1, parent) * k + code
                dec = torch.cat([dec.gather(1, parent[:, :, None].expand(-1, -1, dec.shape[2])),
                                 (code + off)[:, :, None]], 2)
            items = self.index.items(keys.reshape(-1)).view(b, -1)
            ok = torch.isfinite(scores) & (items > 0)
            rows = torch.arange(b, device=self.device)[:, None].expand_as(items)
            out[lo + rows[ok].cpu(), items[ok].cpu()] = scores[ok].cpu()
        return out
