# ticket-transfer

End-to-end workflow for processing **MNL ticket transfer requests** from the Fluro kanban — from pulling new requests, to looking up attendee records, to performing the transfer, to drafting confirmation emails. Built around a **go-signal**: nothing is written until you confirm.

---

## What it does

1. Fetches **new and pending** cards from the `mnlTicketTransfers` Fluro kanban.
2. Pulls full submission details (transferer, requester, transferee, proof of payment) from the linked interaction record.
3. Looks up both parties in Favor Event Tickets and flags edge cases (transferee already has a ticket, transferer not found, etc.).
4. Presents an action plan and **waits for your go-signal**.
5. Performs the attendee updates, verifies them, moves the kanban cards, and drafts completion/inquiry emails from `conferences@favor.church`.

Full step-by-step in [`SKILL.md`](SKILL.md).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Fluro Access** | Required | Fluro for Favor Church MCP | The requests live on the kanban; the skill stops and asks you to connect Fluro. |
| **Event Tickets Access** | Required | Favor Event Tickets MCP | Needed to look up and update attendee records; the skill asks you to connect it. |
| **Gmail Draft Access** | Required for the email step | Gmail MCP · Composio Gmail · `gws` · any send-as-capable Gmail tool | Steps 1–6 still run; if no Gmail tool is connected, the skill does the transfers and hands you ready-to-paste email text instead of blocking. |
| `speak-like-favor` | Recommended | the skill | Keeps email drafts on-brand. |

---

## How to use it

- **Slash command:** `/ticket-transfer`
- **Plain language:** "process the ticket transfers", "check the transfer kanban", "any new ticket transfer requests?"

---

## Recipes

| Recipe | What it does |
|---|---|
| `/ticket-transfer` | Pulls all new + pending requests, shows the lookup table, and proposes an action plan (no writes yet). |
| *"Process the ticket transfers, but show me the plan first."* | Same — stops at the go-signal for your review. |
| *"Go ahead with transfers 1 and 3 only."* | Performs just the approved transfers, verifies them, and moves those cards. |
| *"Draft the completion emails for the transfers we just did."* | Creates the confirmation drafts (To requester, CC transferee/transferer) for review. |
| *"This transferee already has a ticket — what do we do?"* | Flags it, keeps the card pending, and drafts an inquiry email instead of transferring. |

---

## Notes

- **Nothing is written before your go-signal.** Review the action plan first.
- Proof-of-payment links require you to be logged into Fluro in your browser.
- Always uses the process card `_id` (not the submission item `_id`) when moving kanban cards.

See the [root README](../../README.md) for install prompts and the full skills catalog.
