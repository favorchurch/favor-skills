---
name: resend-conference-emails-carefully-with-smtp
description: Use when re-sending, bumping, or resurfacing conference/event ticket (QR) emails to many attendees from a shared Gmail mailbox — before an event, after a delivery issue, or as a reminder. Triggers include "bump the QR tickets", "resend ticket emails to everyone", "remind all registrants", bulk threaded Gmail replies, and any attendee email blast that would exceed Gmail's ~2,000/day mailbox cap (needs SMTP relay).
---

# Resend Conference Emails Carefully (SMTP)

## Overview
Bulk-resurface attendees' existing ticket emails by sending **personalized, threaded replies** ("bumps") that pop the original QR email back to the top of each inbox — built to be **safe**: every recipient is validated against the ticketing system, resends/bounces/transfers are filtered out, and the send is paced, warmed up, and **resumable** so a crash never double-sends or loses its place.

**Core principle:** a bulk send to real attendees is hard to reverse — validate, dedupe, warm up, and make it resumable *before* you ever send the full batch.

## When to use
- "Bump / resend the QR tickets", "remind attendees", "resurface tickets before the event"
- A mail-delivery problem means many people need their ticket re-sent
- Any attendee blast larger than ~2,000 (Gmail mailbox/day cap → must use SMTP relay)

## When NOT to use
- A handful of recipients → just reply manually
- Recipients with NO existing ticket email (nothing to thread onto) → send a *fresh* ticket via the ticketing system's resend, not this skill

## The careful gates (do NOT skip)
1. **Validated recipient list** — cross-check every recipient against the ticketing system's *active/completed* attendees. Never send off the mailbox alone.
2. **Exclude** transferred-away tickets (recipient not in the active list) and bounced addresses (mailer-daemon history).
3. **Dedupe** resends to the single most-recent send per ticket (its security code).
4. **Resumable progress tracker** — append-only state file; re-running skips already-sent rows. ANY agent can resume.
5. **Warm-up first** — send ~25, confirm threading + inbox placement (not spam) + no bounces, THEN the rest.
6. **Explicit human go-ahead** for the full send. Use SMTP relay (not the Gmail API) for >2k/day.

## Connectors / prerequisites
- **Ticketing (active attendees):** Favor Event Tickets MCP (`attendees` count/csv/query). Source of truth for who currently holds a valid ticket. `csv` returns a short-lived `download_url` — curl it to a file.
- **Mailbox reads:** Composio CLI, gmail connection aliased to the shared mailbox (e.g. `conferences`). `GMAIL_FETCH_EMAILS` paginates; large pages offload to `outputFilePath` (read that file). `verbose:false` still returns headers (incl. `Message-Id`) + snippet.
- **Send:** Google Workspace **SMTP relay** (`smtp-relay.gmail.com:587`, ~10k/day). Requires Admin → Apps → Gmail → Routing → **SMTP relay service** enabled (require auth + TLS) and an **app password** for the mailbox. Export `BUMP_SMTP_USER` / `BUMP_SMTP_PASS` (e.g. via a gitignored `.bump_env`).
- **gws (optional, reads only):** its OAuth client's GCP project must grant the mailbox `serviceusage.services.use`, or `messages.get`/`threads.get` 403. Not needed if you read via Composio.

## Workflow
Set per-event config (env vars at the top of each script), then run in order. Scripts live in `scripts/`. Default config targets Favor Conference 2026; override via env.

**Before sending, edit `smtp_send.py:body_for()`** to your event's wording and voice — short, personalized, plain text, no links (best inbox placement).

1. **Active attendees** — Favor Event Tickets MCP `attendees csv` → curl the `download_url` → `attendees_raw.csv`. (Filtering to completed + non-online happens in step 4.)
2. **Enumerate sent ticket emails** — `python3 scripts/fetch_sent.py` (env `QR_QUERY`, `OUTDIR`) → `sent_all.jsonl`. Don't trust `resultSizeEstimate` (it returns a bogus ~201); paginate to exhaustion.
3. **Detect bounces** — `python3 scripts/fetch_bounces.py` → `bounced.txt`.
4. **Build recipient list** — `python3 scripts/build_recipient_list.py` → `<out>.csv`: bump rows (most-recent send per ticket, active, non-bounced, carrying RFC822 `Message-Id`) + fresh-send rows (active attendee with no record).
5. **Verify** — `python3 scripts/verify_threads.py` → re-query a sample of thread IDs against the live mailbox; confirm recipient + subject match. Expect 100% before sending.
6. **Send carefully** — `python3 scripts/smtp_send.py --dry-run` first: it prints ~5 sample messages; confirm each has a non-empty `In-Reply-To` header (threading), a personalized greeting, and a plain-text body, then a `would send N` line. Then `--limit 25` (warm-up; verify threading + inbox placement, not spam). Then `python3 scripts/smtp_send.py` (full, paced, resumable). `--status` for progress.
   - Note: `smtp_send.py` only sends the `bump_recent_send` rows. `fresh_send_no_record` rows have no original `Message-Id` to thread onto — resend those via the ticketing system's native resend instead, not this script.

## Resuming (any agent, after any interruption)
```bash
source .bump_env
python3 scripts/smtp_send.py --status   # remaining count
python3 scripts/smtp_send.py            # resumes; skips keys already 'sent'
```
The append-only state file (`*_state.jsonl`) is the single source of truth. Idempotent — safe to re-run; running again after completion sends nothing.

## Threading (why bumps land in the right thread)
Each reply sets `In-Reply-To` and `References` to the **original email's RFC822 `Message-Id`** (carried in the CSV). That is what makes Gmail thread the bump into the recipient's existing ticket conversation. Use a short **plain-text** body (no HTML/links/images) for best inbox placement.

## Common mistakes / red flags
- Trusting Gmail's `resultSizeEstimate` (bogus ~201) → under-enumerates. Paginate fully.
- Missing the RFC822 `Message-Id` → replies start a NEW thread instead of bumping.
- Full batch via Gmail API / `gws +reply` → hits the ~2k/day mailbox cap. Use SMTP relay for volume.
- Bumping the raw mailbox without cross-checking the ticketing system → spams transferred-away/cancelled holders.
- Empty body or heavy HTML → spam folder. Short, personalized, plain text.
- Combined "N Tickets Total" orders are one thread → one bump (you cannot bump a sub-ticket individually).
- Skipping the warm-up → a deliverability problem becomes thousands of problems.

## Scripts
- `scripts/fetch_sent.py` — paginate the mailbox for the ticket-email subject → JSONL (handles Composio offload + per-page timeout auto-halving).
- `scripts/fetch_bounces.py` — collect bounced recipient addresses from mailer-daemon notices.
- `scripts/build_recipient_list.py` — join attendees ⨯ sent, dedupe by security code, exclude bounced/transferred → bump + fresh-send CSV.
- `scripts/verify_threads.py` — independent inbox re-query to confirm thread IDs are live + correctly mapped.
- `scripts/smtp_send.py` — resumable, paced, threaded SMTP-relay sender with `--status` / `--dry-run` / `--limit`.

Each script reads config from env vars (with sensible defaults) and supports being pointed at any event's artifacts. Edit the personalized body in `smtp_send.py:body_for()` per event, in your church/brand voice.
