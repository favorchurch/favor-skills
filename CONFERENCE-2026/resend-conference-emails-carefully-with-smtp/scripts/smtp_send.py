#!/usr/bin/env python3
"""Resumable, paced, THREADED SMTP-relay sender for conference ticket "bumps".

Sends a short personalized reply per CSV bump row so the recipient's original
QR/ticket email resurfaces at the top of their inbox. Threads via In-Reply-To /
References = the original RFC822 Message-Id (carried in the CSV).

  python3 smtp_send.py --status     # progress counts, no send
  python3 smtp_send.py --dry-run    # preview first 5 built messages, no send
  python3 smtp_send.py --limit 25   # send next 25 unsent (WARM-UP)
  python3 smtp_send.py              # send all remaining (paced); resumes automatically

Resume authority: the append-only state JSONL. Re-running after a crash skips
every key already recorded 'sent'. Idempotent; safe to re-run.

CONFIG via env (defaults target Favor Conference 2026):
  BUMP_CSV        recipient CSV (cols: bump_action, recipient_email, recipient_name,
                  security_code, gmail_thread_id, gmail_message_id, rfc822_message_id)
  BUMP_STATE      state JSONL (default: <csv>.state.jsonl)
  BUMP_SUBJECT    reply subject (keep the "Re: <original subject>")
  BUMP_FROM_NAME / BUMP_FROM_ADDR
  BUMP_SMTP_USER / BUMP_SMTP_PASS   SMTP relay creds (app password)
  BUMP_DELAY (3.0) / BUMP_JITTER (1.5) / BUMP_DAILY_CAP (8000)
"""
import csv, json, os, sys, time, ssl, smtplib, argparse, random
from email.message import EmailMessage
from datetime import datetime, timezone

CSV_PATH   = os.environ.get("BUMP_CSV", "FC26_qr_bump_list_20260629.csv")
STATE_PATH = os.environ.get("BUMP_STATE", CSV_PATH.rsplit(".", 1)[0] + "_state.jsonl")
LOG_PATH   = os.environ.get("BUMP_LOG", CSV_PATH.rsplit(".", 1)[0] + "_run.log")
SUBJECT    = os.environ.get("BUMP_SUBJECT", "Re: Your QR TICKETS for Favor Conference 2026 are here!")
FROM_NAME  = os.environ.get("BUMP_FROM_NAME", "Favor Church")
FROM_ADDR  = os.environ.get("BUMP_FROM_ADDR", "conferences@favor.church")
SMTP_HOST  = os.environ.get("BUMP_SMTP_HOST", "smtp-relay.gmail.com")
SMTP_PORT  = int(os.environ.get("BUMP_SMTP_PORT", "587"))
SMTP_USER  = os.environ.get("BUMP_SMTP_USER", FROM_ADDR)
SMTP_PASS  = os.environ.get("BUMP_SMTP_PASS")

DELAY_SECONDS = float(os.environ.get("BUMP_DELAY", "3.0"))
JITTER        = float(os.environ.get("BUMP_JITTER", "1.5"))
DAILY_CAP     = int(os.environ.get("BUMP_DAILY_CAP", "8000"))
MAX_RETRY     = 3


MAP_URL  = "https://www.google.com/maps/search/?api=1&query=Filoil+EcoOil+Centre+San+Juan"
CONF_URL = "https://favor.church/conference"

def body_for(name):
    """Return (plain_text, html_body). EDIT per event, in your brand/church voice."""
    first = (name or "").strip().split(" ")[0] or "there"
    plain = (f"Hi {first}! Favor Conference 2026 (July 2-4) is almost here. "
             f"We've bumped your QR ticket back to the top, so it's right here in this thread. "
             f"See you at Filoil Centre, San Juan in a few days! \U0001F64C\n"
             f"Conference: {CONF_URL}\n"
             f"Map: {MAP_URL}\n\n"
             f"Much love,\nFavor Conference Team")
    html = (f"<p>Hi {first}! <a href=\"{CONF_URL}\">Favor Conference 2026</a> (July 2-4) is almost here. "
            f"We've bumped your QR ticket back to the top, so it's right here in this thread. "
            f"See you at <a href=\"{MAP_URL}\">Filoil Centre, San Juan</a> in a few days! \U0001F64C</p>"
            f"<p>Much love,<br>Favor Conference Team</p>")
    return plain, html


def key_for(row):
    return (row.get("security_code") or row.get("gmail_message_id") or row["recipient_email"]).strip()


def load_sent_keys():
    sent = set()
    if os.path.exists(STATE_PATH):
        for line in open(STATE_PATH):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("status") == "sent":
                sent.add(rec.get("key"))
    return sent


def append_state(rec):
    rec["ts"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_PATH, "a") as f:
        f.write(json.dumps(rec) + "\n")


def log(msg):
    line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def load_rows():
    with open(CSV_PATH, newline="") as f:
        return [r for r in csv.DictReader(f) if r["bump_action"] == "bump_recent_send"]


def build_message(row):
    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"] = row["recipient_email"]
    msg["Subject"] = SUBJECT
    mid = (row.get("rfc822_message_id") or "").strip()
    if mid:
        msg["In-Reply-To"] = mid
        msg["References"] = mid
    plain, html = body_for(row.get("recipient_name"))
    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")
    return msg


def cmd_status():
    rows = load_rows(); sent = load_sent_keys()
    done = sum(1 for r in rows if key_for(r) in sent)
    failed = 0
    if os.path.exists(STATE_PATH):
        for line in open(STATE_PATH):
            line = line.strip()
            if line and json.loads(line).get("status") == "failed":
                failed += 1
    print(f"bump rows: {len(rows)} | sent: {done} | remaining: {len(rows)-done} | failed-attempts logged: {failed}")


def connect(ctx):
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
    s.starttls(context=ctx)
    s.login(SMTP_USER, SMTP_PASS)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if args.status:
        return cmd_status()

    rows = load_rows()
    sent = load_sent_keys()
    todo = [r for r in rows if key_for(r) not in sent]
    todo.sort(key=lambda r: r.get("latest_send_date_utc", ""))  # OLDEST original send first
    if args.limit:
        todo = todo[:args.limit]
    log(f"start: {len(rows)} total bump rows | {len(rows)-len([r for r in rows if key_for(r) not in sent])} already sent | {len(todo)} to process this run")

    if args.dry_run:
        for r in todo[:5]:
            m = build_message(r)
            plain, html = body_for(r.get("recipient_name"))
            print("----")
            print(f"To: {m['To']}\nIn-Reply-To: {m['In-Reply-To']}\n\n{plain}\n[html alternative has map link: {'href' in html}]")
        log(f"dry-run only: would send {len(todo)} messages")
        return

    if not SMTP_PASS:
        log("ERROR: BUMP_SMTP_PASS not set (source your .bump_env)"); sys.exit(1)

    ctx = ssl.create_default_context()
    server = connect(ctx)
    sent_this_run = 0
    consecutive_fail = 0
    try:
        for i, r in enumerate(todo, 1):
            if sent_this_run >= DAILY_CAP:
                log(f"daily cap {DAILY_CAP} reached — stop; re-run to resume"); break
            if consecutive_fail >= 10:
                log("ABORT: 10 consecutive failures (possible block/throttle). Investigate before resuming."); break
            k = key_for(r)
            msg = build_message(r)
            ok = False; err = None
            for attempt in range(1, MAX_RETRY + 1):
                try:
                    server.send_message(msg); ok = True; break
                except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError):
                    try:
                        server = connect(ctx)
                    except Exception as e:
                        err = f"reconnect failed: {e}"; time.sleep(5)
                except smtplib.SMTPRecipientsRefused as e:
                    err = f"recipient refused: {e}"; break
                except smtplib.SMTPException as e:
                    err = str(e); time.sleep(2 * attempt)
            if ok:
                append_state({"key": k, "email": r["recipient_email"], "status": "sent", "thread_id": r.get("gmail_thread_id", "")})
                sent_this_run += 1; consecutive_fail = 0
                if i % 50 == 0:
                    log(f"progress: {i}/{len(todo)} this run | {sent_this_run} sent")
            else:
                append_state({"key": k, "email": r["recipient_email"], "status": "failed", "error": err})
                log(f"FAILED {r['recipient_email']}: {err}"); consecutive_fail += 1
            time.sleep(DELAY_SECONDS + random.uniform(0, JITTER))
    finally:
        try:
            server.quit()
        except Exception:
            pass
    log(f"run complete: {sent_this_run} sent this run")


if __name__ == "__main__":
    main()
