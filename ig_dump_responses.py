"""
Passive feed dumper: saves EVERY feed/timeline response (unmodified) to its own
JSON file so you accumulate samples. Does not alter the feed.

Run:  mitmdump -s ~/research/instagram/ig_dump_responses.py
Then browse/refresh the home feed.
Output: ~/research/instagram/sample_data/responses/<NN>_<ts>.json
        each = {endpoint, captured_at, paginated, n_docs, complete_doc, all_docs}
"""
import os, json, time
from mitmproxy import http, ctx

OUTDIR = os.path.expanduser("~/research/instagram/sample_data/responses")
os.makedirs(OUTDIR, exist_ok=True)
_seq = [0]

def split_docs(text):
    docs, dec, i, L = [], json.JSONDecoder(), 0, len(text)
    while i < L:
        while i < L and text[i] in " \r\n\t": i += 1
        if i >= L: break
        try: o, e = dec.raw_decode(text, i)
        except Exception: break
        docs.append(o); i = e
    return docs

def _paginated(flow):
    try:
        if flow.request.urlencoded_form.get("max_id"): return True
    except Exception: pass
    return "max_id" in (flow.request.get_text(strict=False) or "")

def response(flow: http.HTTPFlow):
    if "instagram.com" not in flow.request.pretty_host: return
    if "feed/timeline" not in flow.request.path: return
    raw = flow.response.get_text(strict=False) or ""
    docs = split_docs(raw)
    complete = max((d for d in docs if isinstance(d, dict)),
                   key=lambda d: len(d.get("feed_items") or []), default={})
    _seq[0] += 1
    fn = os.path.join(OUTDIR, f"{_seq[0]:02d}_{int(time.time())}.json")
    json.dump({"endpoint": flow.request.path.split("?")[0],
               "captured_at": round(time.time(), 1),
               "paginated": _paginated(flow),
               "n_docs": len(docs),
               "complete_doc": complete,
               "all_docs": docs},
              open(fn, "w"), indent=2)
    ctx.log.info(f"[dump] #{_seq[0]} {len(complete.get('feed_items') or [])} feed_items "
                 f"paginated={_paginated(flow)} -> {os.path.basename(fn)}")
