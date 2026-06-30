#!/usr/bin/env python3
"""Collect failed-delivery recipient addresses from mailer-daemon notices -> bounced.txt
   OUTDIR=. python3 fetch_bounces.py
"""
import json, subprocess, sys, os, re, time, html

OUTDIR = os.environ.get("OUTDIR", ".")
QUERY  = os.environ.get("BOUNCE_QUERY", "from:mailer-daemon")
OUT    = os.path.join(OUTDIR, os.environ.get("BOUNCED_TXT", "bounced.txt"))
OWN_DOMAIN = os.environ.get("OWN_DOMAIN", "favor.church")
EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
DROP = (OWN_DOMAIN, 'mailer-daemon', 'googlemail.com', 'google.com', 'gmail-noreply')


def fetch(payload):
    return subprocess.run(['composio', 'execute', 'GMAIL_FETCH_EMAILS', '-d', json.dumps(payload)],
                          capture_output=True, text=True)


def extract(d):
    ofp = d.get('outputFilePath') or (d.get('data', {}) or {}).get('outputFilePath')
    inline = (d.get('data', {}) or {}).get('messages')
    if inline is None and ofp and os.path.exists(ofp):
        fd = json.load(open(ofp), strict=False); dat = fd.get('data', {}) or {}
    else:
        dat = d.get('data', {}) or {}
    return (dat.get('messages') or []), dat.get('nextPageToken')


bounced = set(); token = None; page = 0; total = 0
while True:
    page += 1
    payload = {'query': QUERY, 'max_results': 100, 'verbose': False}
    if token:
        payload['page_token'] = token
    p = fetch(payload)
    if p.returncode != 0 or not p.stdout.strip():
        sys.stderr.write(f'page {page}: CLI fail {p.stderr[:200]}\n'); break
    d = json.loads(p.stdout, strict=False)
    if not d.get('successful'):
        sys.stderr.write(f'page {page}: err {d.get("error")}\n'); break
    msgs, token = extract(d); total += len(msgs)
    for m in msgs:
        snip = html.unescape(((m.get('preview') or {}).get('body')) or m.get('messageText') or '')
        subj = m.get('subject') or ''
        if not re.search(r"delivery|undeliver|couldn.?t be delivered|failed|wasn.?t delivered|Address not found|Delivery Status", snip + subj, re.I):
            continue
        for e in EMAIL.findall(snip):
            el = e.lower()
            if any(d_ in el for d_ in DROP):
                continue
            bounced.add(el)
    sys.stderr.write(f'page {page}: msgs={len(msgs)} bounced={len(bounced)} next={"Y" if token else "N"}\n'); sys.stderr.flush()
    if not token:
        break
    if page > 100:
        break
    time.sleep(0.2)

with open(OUT, 'w') as f:
    for e in sorted(bounced):
        f.write(e + '\n')
print(f'DONE mailer-daemon msgs scanned={total} distinct bounced={len(bounced)} -> {OUT}')
