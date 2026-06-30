# resend-conference-emails-carefully-with-smtp

Safely **bulk-resurface ticket (QR) emails** to many attendees by sending personalized, threaded replies ("bumps") that pop the original ticket email back to the top of each inbox. Built to be careful: validated, deduped, warmed up, and resumable so a crash never double-sends.

> ⚠️ This skill sends **real email to real attendees**. It treats every missing prerequisite as a hard stop and requires explicit go-ahead for the full send.

---

## What it does

1. Pulls **active attendees** from Favor Event Tickets (who currently holds a valid ticket).
2. Enumerates **sent ticket emails** and **bounces** from the mailbox.
3. Builds a recipient list: most-recent send per ticket, active, non-bounced, carrying the RFC822 `Message-Id` needed for threading.
4. **Verifies** thread IDs against the live mailbox.
5. Sends carefully: `--dry-run` → `--limit 25` warm-up → full paced, resumable send via SMTP relay.

Full gates, scripts, and threading details in [`SKILL.md`](SKILL.md). Helper scripts live in [`scripts/`](scripts/).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Event Tickets Access** | Required | Favor Event Tickets MCP | Source of truth for valid ticket holders; can't validate recipients without it. |
| **Gmail Read Access** (shared mailbox) | Required | Composio Gmail (aliased) · `gws` (read scope) · Gmail MCP | Needed to enumerate sent emails and bounces. |
| **Workspace SMTP Relay** | Required to send | Google Workspace SMTP relay + app password (`BUMP_SMTP_USER`/`BUMP_SMTP_PASS`) | Without it you can validate and dry-run but **must not** send. |
| **Shell & Python** | Required | a terminal with Python 3 | All validation/send scripts are Python. |
| Human go-ahead | Required gate | you | Warm up ~25 first; full batch only after you confirm. |

---

## How to use it

- **Slash command:** `/resend-conference-emails-carefully-with-smtp <event>`
- **Plain language:** "bump the QR tickets", "resend ticket emails to everyone", "remind all registrants before the event".

---

## Recipes

| Recipe | What it does |
|---|---|
| `/resend-conference-emails-carefully-with-smtp bump the QR tickets for FC26` | Full careful pipeline through validation, then pauses for warm-up confirmation. |
| *"Build the recipient list and verify it, but don't send."* | Runs steps 1–5 only — gives you a validated CSV. |
| *"Do the 25-email warm-up."* | `smtp_send.py --limit 25` — confirm threading + inbox placement. |
| *"Send the rest."* | Resumes the full paced send (skips already-sent rows). |
| *"What's the send status / how many are left?"* | `smtp_send.py --status`. |

---

## When NOT to use it

- A handful of recipients → just reply manually.
- People with **no existing ticket email** → send a *fresh* ticket via the ticketing system's resend, not this skill.

---

## Notes

- The append-only state file makes the send **idempotent and resumable** by any agent.
- Bumps use a short **plain-text** body (no links/images) for best inbox placement.
- Edit `scripts/smtp_send.py:body_for()` to your event's wording before sending.

See the [root README](../../README.md) for install prompts and the full skills catalog.
