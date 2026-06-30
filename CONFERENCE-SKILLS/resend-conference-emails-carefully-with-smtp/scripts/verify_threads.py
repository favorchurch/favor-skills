#!/usr/bin/env python3
"""Independent inbox double-check: re-query a spread of the CSV's gmail_thread_ids
against the live mailbox (via Composio) and confirm each is live AND mapped to the
right recipient + ticket subject. Expect 100% OK before sending.

  BUMP_CSV=recipient_bump_list.csv VERIFY_SUBJECT='Your QR TICKETS for Favor Conference 2026 are here' \
  SAMPLE=16 python3 verify_threads.py
"""
import csv, json, subprocess, os

CSV_PATH = os.environ.get("BUMP_CSV", "FC26_qr_bump_list_20260629.csv")
SUBJECT  = os.environ.get("VERIFY_SUBJECT", "Your QR TICKETS for Favor Conference 2026 are here")
SUBJECT_KEY = os.environ.get("VERIFY_SUBJECT_KEY", "QR TICKETS")
SAMPLE = int(os.environ.get("SAMPLE", "16"))


def fetch(q):
    p = subprocess.run(['composio', 'execute', 'GMAIL_FETCH_EMAILS', '-d',
                        json.dumps({'query': q, 'max_results': 15, 'verbose': False})],
                       capture_output=True, text=True)
    d = json.loads(p.stdout, strict=False)
    ofp = d.get('outputFilePath') or (d.get('data', {}) or {}).get('outputFilePath')
    if ofp and os.path.exists(ofp):
        dat = (json.load(open(ofp), strict=False).get('data', {}) or {})
    else:
        dat = d.get('data', {}) or {}
    return dat.get('messages') or []


rows = [x for x in csv.DictReader(open(CSV_PATH)) if x['bump_action'] == 'bump_recent_send']
n = len(rows)
idx = sorted(set(list(range(3)) + list(range(max(0, n - 3), n)) + list(range(5, n, max(1, n // 10)))[:SAMPLE - 6]))
sample = [rows[i] for i in idx]
ok = bad = 0
print(f'verifying {len(sample)} of {n} bump threads via Composio re-query...\n')
for r in sample:
    em = r['recipient_email']; tid = r['gmail_thread_id']
    msgs = fetch(f'in:sent to:{em} subject:"{SUBJECT}"')
    tids = {m.get('threadId') for m in msgs}
    st = 'OK' if tid in tids else ('NO_MATCH' if msgs else 'EMPTY')
    ok += (st == 'OK'); bad += (st != 'OK')
    print(f'{st:9} date={r["latest_send_date_utc"][:10]} to={em} csv_tid={tid} live={len(tids)}')
print(f'\nVERIFY: {ok} OK / {bad} problems of {len(sample)}')
