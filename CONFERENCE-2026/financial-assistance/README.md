# financial-assistance

Process Favor Church conference **financial assistance requests** end to end: read the **Rock** connection board, compute exact discounts from live ticket prices, update the tracker sheet, assign coupon codes, draft emails from the event's sender, then send and close cards — only after your go-signal.

> **Fluro is retired.** This skill talks to Rock only.

---

## What it does

- **Phase 1 — Intake:** reads cards in the *New Requests* lane on `MNL | Financial Assistance Requests`, joins each to its Rock form submission, saves a CSV.
- **Clarification:** routes incomplete/invalid requests to *Clarification Needed* with reasons.
- **Phase 2 — Prices:** reads live ticket prices and computes `discount = ticket cost − amount they can pay` (exact, never rounded to a tier).
- **Phase 3–4 — Tracker & coupons:** updates `REQUESTS` and draws the exact-tier coupon from the event's normalized coupon tab, marking it used.
- **Phase 5–7 — Email & close:** drafts HTML emails (standout coupon block) **from the event's sender**, then, after approval, sends, ticks `Sent`, and moves cards to *Email & Coupon Sent*.

Full phases and the verification checklist are in [`SKILL.md`](SKILL.md).

---

## Fixed systems

| | |
|---|---|
| Environment | **prod — `rock.favor.church`** |
| Connection Type | `4` — `MNL \| Financial Assistance Requests` |
| Form | WorkflowType `58` — `MNL Financial Assistance Request` |
| Spreadsheet | *Conferences - Financial Assistance 2026* |
| Config | the `CONFIG` tab — event → opportunity → tabs → sender |

**Senders are per-event.** `conferences@favor.church` is the default; Echo Conference 2026 sends from `echo@favor.church`. The skill resolves this from `CONFIG` and the template tab — never hardcoded.

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Rock access** | Required | Rock MCP · Rock REST (`rock-favor`) | The board and submissions live in Rock. |
| **Google Sheets** | Required | Composio `GOOGLESHEETS_*` · `gws` · Sheets MCP | `CONFIG`, `REQUESTS` and coupon tabs. |
| **Gmail send-as** | Required for emails | Gmail MCP/CLI with send-as | Won't create wrong-sender drafts — gives you setup steps + ready text instead. |
| **Event Tickets** | Required for live prices (has fallback) | Favor Event Tickets MCP · *fallback:* the event page | Falls back to the page URL on `CONFIG`. |
| `speak-like-favor` | Recommended | the skill | Keeps coupon emails on-brand. |

---

## How to use it

- **Slash command:** `/financial-assistance <check | process> <event>`
- **Plain language:** "review the new financial aid requests", "process the Echo assistance applications", "assign coupons for EC26".

| Recipe | What it does |
|---|---|
| `/financial-assistance check EC26` | Dry run — reads new cards, computes discounts, reports. No writes. |
| `/financial-assistance process new requests` | Full pipeline up to drafts; sends only after your go-signal. |
| *"Which requests need clarification?"* | Lists cards with missing/invalid data and the reason for each. |
| *"Assign coupons and draft, but don't send."* | Updates the tracker, allocates exact-tier coupons, drafts — stops at the checkpoint. |
| *"Go ahead and send."* | Sends from the event's sender, verifies, ticks `Sent`, moves cards. |

---

## Notes

- **Two records per applicant.** The *submission* carries the answers; the *ConnectionRequest* carries the lane. The skill reads both and joins them.
- **Card attributes are currently empty** — WT58 doesn't copy answers onto the card yet, so the skill reads the submission. It re-checks this each run.
- **Never guesses** the applicant, event, price, sender, coupon tier, or sent status.
- **Exact discounts only** — if the precise tier doesn't exist, it's a clarification, not a round-up.
- `Sent` is ticked only after a verified send.

See the [root README](../../README.md) for install prompts and the full skills catalog.
