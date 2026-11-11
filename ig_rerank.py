"""
Single-response re-ranker

For each feed/timeline response, reorders that response's feed_items in place and
tags each unit with [POS k/N].

Ranking (env RANK): "reverse" (default) or "shuffle"
Run:  RANK=reverse mitmdump -s ~/research/instagram/ig_rerank_single.py
"""
import os, json, random
from mitmproxy import http, ctx

RANK = os.environ.get("RANK", "reverse")

def split_docs(text):
    docs, dec, i, L = [], json.JSONDecoder(), 0, len(text)
    while i < L:
        while i < L and text[i] in " \r\n\t": i += 1
        if i >= L: break
        try: o, e = dec.raw_decode(text, i)
        except Exception: break
        docs.append(o); i = e
    return docs

def rank_sorted(items):
    if RANK == "shuffle":
        r = list(items); random.shuffle(r); return r
    return list(reversed(items))  # reverse (default)

def tag(it, k, n):
    marker = f"[POS {k}/{n}] "
    def strip(t): return t.split("] ", 1)[-1] if isinstance(t, str) and t.startswith("[POS ") else (t or "")
    def stamp(m):
        if not isinstance(m, dict): return
        if isinstance(m.get("caption"), dict):
            m["caption"]["text"] = marker + strip(m["caption"].get("text"))
        if isinstance(m.get("ad_title"), str):
            m["ad_title"] = marker + strip(m["ad_title"])
    stamp(it.get("media_or_ad"))
    su = it.get("suggested_users")
    if isinstance(su, dict) and isinstance(su.get("title"), str):
        su["title"] = marker + strip(su["title"])
    es = it.get("explore_story")
    if isinstance(es, dict):
        stamp(es.get("media_or_ad"))

def response(flow: http.HTTPFlow):
    if "instagram.com" not in flow.request.pretty_host: return
    if "feed/timeline" not in flow.request.path: return
    raw = flow.response.get_text(strict=False) or ""
    docs = split_docs(raw)
    comp = max((d for d in docs if isinstance(d, dict)),
               key=lambda d: len(d.get("feed_items") or []), default=None)
    if comp is None: return
    items = comp.get("feed_items") or []
    if not items: return
    ordered = rank_sorted(items)
    n = len(ordered)
    for k, it in enumerate(ordered, start=1):
        tag(it, k, n)
    comp["feed_items"] = ordered
    comp["num_results"] = n
    flow.response.set_text(json.dumps(comp))   # single doc; app accepts it
    ctx.log.info(f"[single] reranked {n} units in-place (rank={RANK})")
