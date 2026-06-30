#!/usr/bin/env python3
"""Build the validated recipient CSV: join active attendees x sent ticket emails,
dedupe same-ticket resends to the most recent, exclude bounced + transferred-away.

Inputs (env or default, in cwd):
  ATTENDEES_CSV  TEC attendee export (all statuses)   default attendees_raw.csv
  SENT_JSONL     output of fetch_sent.py              default sent_all.jsonl
  BOUNCED_TXT    output of fetch_bounces.py            default bounced.txt
  OUT_CSV        recipient list to write              default recipient_bump_list.csv

Attendee CSV columns expected: 'Ticket', 'Order Status', 'Ticket Holder Email Address',
'Ticket Holder Name', 'Purchaser Email Address', 'Order ID', 'Ticket ID'.
Sent JSONL = Composio GMAIL_FETCH_EMAILS message objects (to, preview.body, payload.headers
with Message-Id, messageTimestamp, threadId, messageId, labelIds).

Output rows: bump_action = bump_recent_send | fresh_send_no_record, with recipient,
ticket type, security_code, latest_send_date_utc, gmail_thread_id, gmail_message_id,
rfc822_message_id, num_active_tickets_at_email, active_attendee_order_ids, active_ticket_ids, notes.
"""
import csv, json, re, os, html
from collections import defaultdict
from datetime import datetime

ATTENDEES = os.environ.get("ATTENDEES_CSV", "attendees_raw.csv")
SENT      = os.environ.get("SENT_JSONL", "sent_all.jsonl")
BOUNCED   = os.environ.get("BOUNCED_TXT", "bounced.txt")
OUT       = os.environ.get("OUT_CSV", "recipient_bump_list.csv")
EXCLUDE_TICKET_SUBSTR = os.environ.get("EXCLUDE_TICKET_SUBSTR", "online").lower()  # exclude online tickets
DELIVERY_MARKER = os.environ.get("DELIVERY_MARKER", "your ticket,").lower()        # snippet signature of a delivery email

EMAIL_RE = re.compile(r'<([^>]+)>')
CODE_RE  = re.compile(r'\b[0-9a-f]{10}\b')
NAME_RE  = re.compile(r'your ticket,\s*(.+?)!', re.I)


def norm_email(s):
    if not s:
        return ""
    s = s.strip()
    m = EMAIL_RE.search(s)
    if m:
        s = m.group(1)
    return s.strip().lower()


def parse_dt(s):
    if not s:
        return datetime.min
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return datetime.min


# 1. active attendees
active_by_email = defaultdict(list)
active_emails = set()
with open(ATTENDEES, newline='') as f:
    for row in csv.DictReader(f):
        if row.get('Order Status', '').strip().lower() != 'completed':
            continue
        ttype = (row.get('Ticket', '') or '').strip()
        if EXCLUDE_TICKET_SUBSTR and EXCLUDE_TICKET_SUBSTR in ttype.lower():
            continue
        he = norm_email(row.get('Ticket Holder Email Address', ''))
        pe = norm_email(row.get('Purchaser Email Address', ''))
        att = {'holder_name': (row.get('Ticket Holder Name', '') or '').strip(),
               'ticket_type': ttype,
               'order_id': (row.get('Order ID', '') or '').strip(),
               'ticket_id': (row.get('Ticket ID', '') or '').strip()}
        key = he or pe
        if key:
            active_by_email[key].append(att)
        if he:
            active_emails.add(he)
        if pe:
            active_emails.add(pe)

# 2. bounced
bounced = set()
if os.path.exists(BOUNCED):
    for line in open(BOUNCED):
        e = norm_email(line)
        if e:
            bounced.add(e)

# 3. sent delivery emails
sent_recipients = set()
by_code = defaultdict(list)
nocode = []
n_lines = n_delivery = n_trash = n_nondelivery = 0
with open(SENT) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        n_lines += 1
        m = json.loads(line)
        if 'TRASH' in (m.get('labelIds') or []):
            n_trash += 1; continue
        snip = html.unescape(((m.get('preview') or {}).get('body')) or m.get('messageText') or '')
        if DELIVERY_MARKER not in snip.lower():
            n_nondelivery += 1; continue
        to = norm_email(m.get('to', ''))
        if not to:
            continue
        code_m = CODE_RE.search(snip)
        code = code_m.group(0) if code_m else None
        name_m = NAME_RE.search(snip)
        name = name_m.group(1).strip() if name_m else ''
        ttype = ''
        if code and name:
            before = snip[:code_m.start()]
            idx = before.rfind(name)
            if idx >= 0:
                ttype = re.sub(r'\d+\s+Tickets?\s+Total|Ticket\s+\d+\s+of\s+\d+', '', before[idx + len(name):]).strip(' \t-,').strip()
        rfc = ''
        for h in (m.get('payload', {}) or {}).get('headers', []) or []:
            if h.get('name', '').lower() == 'message-id':
                rfc = h.get('value', '').strip(); break
        send = {'to': to, 'name': name, 'ticket_type': ttype, 'code': code,
                'date': m.get('messageTimestamp', ''), 'dt': parse_dt(m.get('messageTimestamp', '')),
                'thread_id': m.get('threadId', ''), 'gmail_msg_id': m.get('messageId', ''),
                'rfc822_message_id': rfc}
        sent_recipients.add(to)
        n_delivery += 1
        (by_code[code] if code else nocode).append(send)

# 4. dedupe by code -> most-recent active-recipient send
def attendees_at(email):
    return active_by_email.get(email, [])

def make_bump(send, code):
    em = send['to']; atts = attendees_at(em)
    return {'bump_action': 'bump_recent_send', 'recipient_email': em,
            'recipient_name': send['name'] or (atts[0]['holder_name'] if atts else ''),
            'ticket_type': send['ticket_type'] or (atts[0]['ticket_type'] if len(atts) == 1 else ('multiple' if len(atts) > 1 else '')),
            'security_code': code or '', 'latest_send_date_utc': send['date'],
            'gmail_thread_id': send['thread_id'], 'gmail_message_id': send['gmail_msg_id'],
            'rfc822_message_id': send['rfc822_message_id'], 'num_active_tickets_at_email': len(atts),
            'active_attendee_order_ids': ';'.join(sorted({a['order_id'] for a in atts if a['order_id']})),
            'active_ticket_ids': ';'.join(sorted({a['ticket_id'] for a in atts if a['ticket_id']})), 'notes': ''}

bump_rows = []; excluded_no_active = 0
for code, sends in by_code.items():
    sends.sort(key=lambda s: s['dt'], reverse=True)
    active_sends = [s for s in sends if s['to'] in active_emails and s['to'] not in bounced]
    if not active_sends:
        excluded_no_active += 1; continue
    row = make_bump(active_sends[0], code)
    if len(sends) > 1:
        row['notes'] = f"deduped {len(sends)} sends of this code -> most recent"
    bump_rows.append(row)
for send in nocode:
    if send['to'] in active_emails and send['to'] not in bounced:
        r = make_bump(send, None); r['notes'] = 'no security code parsed from snippet'
        bump_rows.append(r)

# 5. fresh-send list
fresh_rows = []; seen = set()
for email, atts in active_by_email.items():
    if email in sent_recipients:
        continue
    for a in atts:
        k = (email, a['ticket_id'])
        if k in seen:
            continue
        seen.add(k)
        fresh_rows.append({'bump_action': 'fresh_send_no_record', 'recipient_email': email,
                           'recipient_name': a['holder_name'], 'ticket_type': a['ticket_type'],
                           'security_code': '', 'latest_send_date_utc': '', 'gmail_thread_id': '',
                           'gmail_message_id': '', 'rfc822_message_id': '', 'num_active_tickets_at_email': len(atts),
                           'active_attendee_order_ids': a['order_id'], 'active_ticket_ids': a['ticket_id'],
                           'notes': 'previously bounced' if email in bounced else ''})

cols = ['bump_action', 'recipient_email', 'recipient_name', 'ticket_type', 'security_code',
        'latest_send_date_utc', 'gmail_thread_id', 'gmail_message_id', 'rfc822_message_id',
        'num_active_tickets_at_email', 'active_attendee_order_ids', 'active_ticket_ids', 'notes']
bump_rows.sort(key=lambda r: r['latest_send_date_utc'])  # oldest original send first (matches send order)
fresh_rows.sort(key=lambda r: r['recipient_email'])
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in bump_rows + fresh_rows:
        w.writerow(r)

active_total = sum(len(v) for v in active_by_email.values())
print("=== RECIPIENT LIST SUMMARY ===")
print(f"Active attendees (completed, non-'{EXCLUDE_TICKET_SUBSTR}'): {active_total} across {len(active_by_email)} unique emails")
print(f"Sent lines read: {n_lines} | delivery kept: {n_delivery} | trash skipped: {n_trash} | non-delivery skipped: {n_nondelivery}")
print(f"Distinct security codes: {len(by_code)} | no-code sends: {len(nocode)} | bounced loaded: {len(bounced)}")
print(f"BUMP rows: {len(bump_rows)} | excluded (no active recipient): {excluded_no_active}")
print(f"FRESH-SEND rows: {len(fresh_rows)}")
print(f"Output: {OUT}")
