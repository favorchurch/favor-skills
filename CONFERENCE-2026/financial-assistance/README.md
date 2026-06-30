# financial-assistance

Process Favor Church conference **financial assistance requests** end to end: read the Fluro kanban, compute exact discounts from live ticket prices, update the tracker sheet, assign coupon codes, draft emails from the correct sender, then send and close cards — only after your go-signal.

---

## What it does

- **Phase 1 — Intake:** reads `new` cards, pulls the linked submission, saves inspected items to a CSV.
- **Clarification:** routes incomplete/invalid requests to "Clarification Needed" with reasons.
- **Phase 2 — Prices:** reads live ticket prices and computes `discount = ticket cost − amount they can pay` (exact, never rounded to a coupon tier).
- **Phase 3–4 — Tracker & coupons:** updates the `REQUESTS` tab and assigns the exact-tier coupon, marking it used.
- **Phase 5–7 — Email & close:** drafts HTML emails (with a standout coupon block) from `conferences@favor.church`, then, after approval, sends and moves cards.

Full phases and verification checklist in [`SKILL.md`](SKILL.md).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Fluro Access** | Required | Fluro for Favor Church MCP | Requests live on the `mnlFinancialAssistanceRequests` board; the skill stops and asks you to connect Fluro. |
| **Google Sheets Access** | Required | Composio `GOOGLESHEETS_*` · `gws` · Sheets MCP | The tracker and coupon tabs live in Sheets. |
| **Gmail Draft Access** (send-as `conferences@favor.church`) | Required for emails | Gmail MCP/CLI with send-as · Composio Gmail with send-as · `gws` | If no tool can enforce the sender, the skill won't create wrong-sender drafts — it gives you setup steps + ready-to-send text. |
| **Event Tickets Access** | Required for live prices (has fallback) | Favor Event Tickets MCP · *fallback:* the public event page | If missing, it reads the official event page and tells you. |
| `speak-like-favor` | Recommended | the skill | Keeps coupon emails on-brand. |

---

## How to use it

- **Slash command:** `/financial-assistance <check | process> <event>`
- **Plain language:** "review the new financial aid requests", "process the assistance applications", "assign coupons for FC26".

---

## Recipes

| Recipe | What it does |
|---|---|
| `/financial-assistance check FC26` | Dry run — reads new requests, computes discounts, reports. No writes. |
| `/financial-assistance process new requests` | Full pipeline up to drafts; sends only after your go-signal. |
| *"Which requests need clarification?"* | Lists cards with missing/invalid email, ticket type, or pay amount and the reason for each. |
| *"Assign coupons and draft the emails, but don't send yet."* | Updates the tracker, allocates exact-tier coupons, and drafts — stops at the review checkpoint. |
| *"Go ahead and send the approved ones."* | Sends from `conferences@favor.church`, verifies, ticks `Sent`, and moves cards to "Email & Coupon Sent". |

---

## Notes

- **Never guesses** the applicant, event, price, sender, coupon tier, or sent status — every value is verified against a live system first.
- **Exact discounts only** — if the precise coupon tier doesn't exist, it's a clarification, not a round-up.
- `Sent` is ticked only after the message is actually verified as sent.

See the [root README](../../README.md) for install prompts and the full skills catalog.
