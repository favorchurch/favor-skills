#!/usr/bin/env python3
"""Paginate Composio GMAIL_FETCH_EMAILS over all Sent ticket-delivery emails -> sent_all.jsonl

  PAGE=100 QR_QUERY='in:sent subject:"..."' OUTDIR=. python3 fetch_sent.py

Robust to: shell quoting (argv), Composio offload-to-file (top-level outputFilePath;
messages + nextPageToken live in the file's .data), and per-page timeouts (auto-halves
the page size and retries). Don't trust resultSizeEstimate — paginate to exhaustion.
"""
import json, subprocess, sys, os, time

OUTDIR = os.environ.get("OUTDIR", ".")
QUERY  = os.environ.get("QR_QUERY", 'in:sent subject:"Your QR TICKETS for Favor Conference 2026 are here"')
PAGE   = int(os.environ.get("PAGE", "100"))
OUT    = os.path.join(OUTDIR, os.environ.get("SENT_JSONL", "sent_all.jsonl"))


def fetch(payload):
    return subprocess.run(['composio', 'execute', 'GMAIL_FETCH_EMAILS', '-d', json.dumps(payload)],
                          capture_output=True, text=True)


def extract(d):
    ofp = d.get('outputFilePath') or (d.get('data', {}) or {}).get('outputFilePath')
    inline = (d.get('data', {}) or {}).get('messages')
    if inline is None and ofp and os.path.exists(ofp):
        fd = json.load(open(ofp), strict=False)
        dat = fd.get('data', {}) or {}
    else:
        dat = d.get('data', {}) or {}
    return (dat.get('messages') or []), dat.get('nextPageToken')


out = open(OUT, 'w')
token = None; page = 0; total = 0; size = PAGE
while True:
    page += 1
    payload = {'query': QUERY, 'max_results': size, 'verbose': False}
    if token:
        payload['page_token'] = token
    t0 = time.time(); p = fetch(payload); dt = time.time() - t0
    if p.returncode != 0 or not p.stdout.strip():
        sys.stderr.write(f'page {page}: CLI fail rc={p.returncode} err={p.stderr[:200]}\n'); break
    try:
        d = json.loads(p.stdout, strict=False)
    except Exception as e:
        sys.stderr.write(f'page {page}: JSON err {e} out[:200]={p.stdout[:200]!r}\n'); break
    if not d.get('successful'):
        if 'timed out' in str(d.get('error', '')).lower() and size > 25:
            size = max(25, size // 2); page -= 1
            sys.stderr.write(f'  timeout -> retry same page at size {size}\n'); continue
        sys.stderr.write(f'page {page}: not successful err={d.get("error")}\n'); break
    msgs, token = extract(d)
    for m in msgs:
        out.write(json.dumps(m) + '\n')
    total += len(msgs)
    sys.stderr.write(f'page {page}: +{len(msgs)} total={total} {dt:.1f}s size={size} next={"Y" if token else "N"}\n'); sys.stderr.flush()
    if not token:
        break
    if page > 400:
        sys.stderr.write('SAFETY CAP\n'); break
    time.sleep(0.2)
out.close()
print('DONE total messages =', total, '->', OUT)
