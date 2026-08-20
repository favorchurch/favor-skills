---
name: financial-assistance
description: Use when processing Favor Church financial assistance requests from Rock — reading the MNL | Financial Assistance Requests connection board, calculating discounts, assigning coupon codes, updating the tracker Sheet, drafting and sending coupon emails from the event's sender, and moving kanban cards. Triggers on "financial assistance", "assistance requests", "coupon codes", "financial aid", "EC26 requests", "Echo assistance".
---

# Financial Assistance (Rock)

## Overview

Process Favor Church conference financial assistance requests end to end: read the **Rock** connection board, calculate exact discounts from live ticket prices and applicant pay amounts, update the tracker Sheet, assign coupon codes, draft emails **from the sender that event uses**, then send and close cards only after the user gives the go-signal.

Core rule: never guess the applicant, event, ticket price, sender, coupon tier, or sent status. Verify each live system before writing.

> **Fluro is retired.** There is no Fluro board, no `mnlFinancialAssistanceRequests` process, and no Fluro link anywhere in this workflow. If a tab, note, or older instruction mentions Fluro, it is stale — the Rock connection board is the only source.

## Fixed Systems

| System | Value |
| --- | --- |
| Environment | **PROD — `rock.favor.church`** (announce this on every Rock call, read or write) |
| Connection Type | `4` — `MNL \| Financial Assistance Requests` |
| Form (WorkflowType) | `58` — `MNL Financial Assistance Request` |
| Kanban board | `https://rock.favor.church/connections` |
| Spreadsheet | `1gWT7fB-TWRQwIHrlxpAjBo7scHBbIqlAcxSyUdmt9So` ("Conferences - Financial Assistance 2026") |
| Config tab | `CONFIG` — **read this first, every run** |
| Tracker tab | `REQUESTS` unless the user specifies otherwise |
| Default sender | `conferences@favor.church` |
| No-browser rule | Do not use Chrome, browser automation, or manual web UI control for processing |

### The CONFIG tab is the source of truth

Never hardcode an event, opportunity id, sender, or tab name. Read `CONFIG!A2:K` and resolve per event:

| Column | Meaning |
| --- | --- |
| `Event Code` | e.g. `EC26` |
| `Event Name` | e.g. `Echo Conference 2026` |
| `Status` | `ACTIVE` / `ARCHIVED` / `DEFAULT` |
| `Rock Opportunity ID` | the ConnectionOpportunity this event's cards live on |
| `Coupon Tab` / `Template Tab` | which tabs to read |
| `Sender (FROM)` / `CC` | who the email comes from |
| `Event Page URL` | for live ticket prices when the Tickets MCP is down |

Resolution rules:

1. Match the submission's event to a row with `Status = ACTIVE`.
2. Sender = that row's `Sender (FROM)`, **overridden by** the `FROM` value on the event's template tab if the two disagree — and when they disagree, say so and ask before sending.
3. If no row matches, fall back to the `DEFAULT` row's sender (`conferences@favor.church`) and **tell the user** you fell back.
4. Never send from a sender that does not appear on `CONFIG`.
5. Rows marked `ARCHIVED` are historical only — never assign coupons from an archived tab.

Current state: `EC26` → opportunity `9`, tabs `EC26-Coupons` / `EC26-Template`, sender **`echo@favor.church`**. `FC26`, `HS26`, `WOR26` are archived (tabs renamed `ARCHIVE — …` and hidden).

### Kanban lanes (ConnectionStatus ids)

| Id | Lane | Use |
| --- | --- | --- |
| `14` | New Requests | Intake source (default lane for every submission) |
| `15` | Clarification Needed | Invalid / missing data |
| `16` | Email & Coupon Sent | Only after a verified send |
| `17` | No Coupon | Only if the user decides no coupon |
| `18` | Event Finished | Not part of normal processing |

## Prerequisites

Each requirement is a **capability bucket** — any one listed tool satisfies it. Run this preflight before any phase. If a **Required** bucket has no connected tool, explain what it is, why the skill needs it, and how to connect it, then **stop and ask** — never guess a price, coupon, or sender to work around a missing tool.

| Capability | Type | Satisfied by (any one) | If missing |
|---|---|---|---|
| **Rock access** | Required | `Rock_for_Favor_Church` MCP (`rock_form`, `rock_entity`, `rock_workflow`) · Rock REST via the `rock-favor` plugin's `rock_api.py` | The requests and the board live in Rock; without it there is nothing to intake or close. |
| **Google Sheets access** | Required | Composio (`GOOGLESHEETS_*`) · `gws` CLI · Sheets MCP | `CONFIG`, `REQUESTS` and the coupon tabs live in Sheets. |
| **Gmail send-as** | Required for Phases 5 & 7 | Gmail MCP/CLI with send-as · Composio Gmail with verified send-as · `gws` | Drafts must come from the event's sender. If no tool can enforce `From`, **do not create wrong-sender drafts** (see Sender Enforcement). |
| **Event Tickets access** | Required for live prices (has fallback) | `Favor_Event_Tickets` MCP · *fallback:* the `Event Page URL` on `CONFIG` | Used for live ticket prices. If both fail, ask the user for prices — never assume last year's. |
| `speak-like-favor` skill | Recommended | the `speak-like-favor` skill | Keeps coupon emails in Favor voice. If absent, apply the HTML rules inlined in Phase 5. |

Default to a **dry-run summary** if the user asks to "check", "review", or "process" without explicitly authorizing writes. Proceed with writes when they ask to update, draft, assign, move, send, or complete a phase.

## Reading a request: two sources, one applicant

Rock splits this data across two records. You need both.

| What you need | Where it lives | How to read it |
| --- | --- | --- |
| **The answers** (event, ticket type, amount able to pay, reason, church, pastor flag) | the **form submission** (workflow instance of WT58) | `rock_form action=listSubmissions workflowTypeId=58` (add `limit`/`offset`; `exportSubmissions` for bulk) |
| **The card / lane state** | the **ConnectionRequest** | `rock_entity action=search model=connectionrequests where='ConnectionOpportunityId == <id>'` |

**Known gap (as of 2026-08-14):** WT58's "Create Connection Request" action does not copy the answers onto the card, so the ConnectionRequest's own attributes (`SeniorPastor`, `Church`, `TicketType`, `AmountAbleToPay`, `Reason`) are **empty on every card**. Do not read them and do not treat blank as `0` — read the submission instead. Re-check this each run: if those attributes start coming back populated, the copy action has been configured and you may prefer them.

**Joining a submission to its card:**

1. Submission field `Requester` is a **person alias GUID** → resolve to a person (`rock_people`), then match `ConnectionRequest.PersonAliasId`.
2. Tie-break on time: the card is created within seconds of the submission's `completedDateTime`.
3. If one person has two cards on the same opportunity, that is a **duplicate ambiguity** — clarification, not a guess.

## Phase 1: Intake

1. Announce: *"Reading Rock prod (rock.favor.church)."*
2. Resolve the event and its opportunity id from `CONFIG`.
3. List cards on that opportunity in lane `14` (New Requests).
4. Pull submissions with `rock_form listSubmissions workflowTypeId=58` and join each card to its submission.
5. Extract per applicant: first/last name, email, phone, church, ticket type, amount able to pay, reason, event, **ConnectionRequest id**, **submission (workflow) id**.
6. Save all inspected New items to a CSV before writing Sheets, named `<EVENT-CODE>_financial_assistance_new_<YYYYMMDD>.csv` (e.g. `EC26_financial_assistance_new_20260814.csv`).

Do not move any card in this phase.

Skip and flag any submission where `SeniorPastor = Yes` — pastors' tickets are already free and that branch collects no ticket/amount fields, so there is nothing to price. As of 2026-08-14 the form hides its Submit button for that branch and points pastors at `echo@favor.church` instead, so these should be rare; if one still appears, report it separately for the user to handle by hand.

## Clarification Rules

Move a card to lane `15` (Clarification Needed) and report the reason when any of these are true:

| Issue | Why |
| --- | --- |
| Missing or invalid email | Cannot draft/send safely |
| Missing ticket type | Cannot determine ticket cost |
| Missing, non-numeric, or ambiguous pay amount | The amount they wrote is honored exactly |
| Pay amount greater than the live ticket cost | Discount would be negative |
| Event missing, archived, or mismatched | Wrong template/coupon risk |
| No matching template tab | Email cannot be generated faithfully |
| No unused coupon at the computed discount | Cannot honor the exact approved discount |
| Duplicate applicant / two cards for one person | Risk of assigning the wrong coupon |
| No submission joined to the card | Nothing to price — investigate before acting |

For clarification cards: do not add to the tracker, do not allocate a coupon, do not draft an email — unless the user explicitly decides the missing value.

## Phase 2: Live Ticket Prices

Preferred order:

1. `Favor_Event_Tickets` MCP for the event and ticket types.
2. The `Event Page URL` from `CONFIG` when the MCP is unavailable or timing out.
3. User-provided prices only if they explicitly confirm.

```text
amount_to_pay = exact numeric value from the applicant
discount      = live_ticket_cost(ticket_type) - amount_to_pay
```

| Ticket Cost | Applicant Can Pay | Discount |
| --- | ---: | ---: |
| Adult `1000` | `100` | `900` |
| Student `250` | `100` | `150` |
| Adult `1000` | `0` | `1000` / full discount |

Never round to a nearby coupon tier. If the exact tier does not exist, it is clarification / no available coupon.

## Phase 3: Update REQUESTS

1. Read the `REQUESTS` headers first (row 3). **Infer columns by header name, never by fixed letter** — the tab has a code-generator widget sitting in the middle of the columns.
2. Current headers include: `DISCOUNT`, `Event`, `Ticket Type`, `Coupon Discount`, `Amount to Pay`, `First Name`, `Last Name`, `Email`, `Sent`, `Rock Request ID`, `Sender Used`, `Date Sent`.
3. Append rows only for non-clarification applicants.
4. Always fill `Rock Request ID` — it is the join key back to the board.
5. Leave `Sent` unchecked until the email is actually sent.

Re-read the inserted rows afterwards and confirm row count, names, emails, ticket types, pay amounts, discounts, coupon codes, and that `Sent` is still unchecked.

## Phase 4: Assign Coupons

The coupon tabs are **normalized — one row per coupon** (this replaced the old side-by-side tier blocks).

Headers (row 3): `Coupon Code` · `Discount (PHP)` · `Tier Label` · `Ticket Type Scope` · `Used?` · `Gave To` · `Email` · `Date Assigned` · `Rock Request ID` · `Notes`

1. Read the event's coupon tab from `CONFIG`.
2. For each applicant, filter to rows where `Discount (PHP)` **equals the exact computed discount** and `Ticket Type Scope` either is blank/`any` or includes their ticket type.
3. Take the **first** row where `Used?` is `FALSE` and `Gave To` is blank.
4. Write in that row: `Used? = TRUE`, `Gave To` = full name, `Email`, `Date Assigned` (Manila date), `Rock Request ID`.
5. Copy the coupon code back into the tracker row.

If the tab has **no codes at all** for the event, stop and tell the user the coupon pool is empty — do not borrow from an archived tab.

Re-read the edited coupon rows after writing. Never issue one code twice. Do not delete or restructure archived coupon tabs unless the user asks.

## Phase 5: Draft Emails

1. Read the event's template tab (e.g. `EC26-Template`).
2. Use its `FROM`, `SUBJECT`, `BODY`, `RECIPIENTS`, `CC`, `BCC` values. **`FROM` varies by event** — `conferences@favor.church` by default, `echo@favor.church` for Echo Conference 2026.
3. Replace placeholders: `NAME`, `(TicketType)`, `COUPON_CODE`, discount with `₱`, amount to pay with `₱`, `EMAIL_ADDRESS`.
4. Draft as **HTML** (`is_html: true`), never plain text with markdown. Apply `speak-like-favor` Email Rendering:
   - **Render the coupon code in a large, bold standout block**, regardless of the template:
     ```html
     <div style="font-size:34px;font-weight:bold;letter-spacing:3px;color:#E8740C;background:#FFF4E8;border:2px dashed #E8740C;border-radius:10px;padding:18px;text-align:center;margin:18px 0;font-family:monospace;">EC26-XXXX-900</div>
     ```
   - **Make every link clickable:** `<a href="https://favor.church/echo#tickets">favor.church/echo#tickets</a>`.
   - Bold names and amounts with `<strong>`; use `<ol>`/`<ul>` for steps, never `-`/`*` or `**`.
5. Footer must include the sending account's default signature. If that cannot be applied, check recent mail from that sender for its signature and copy it, telling the user you did so.
6. Create drafts only — never send without an explicit go-signal.

### Sender Enforcement

The sender is the event's `FROM`, resolved from `CONFIG` + the template tab.

Preferred order:

1. Gmail MCP/CLI method that supports send-as/from.
2. `gws` or Composio Gmail with a raw MIME `From:` header and verified send-as.
3. If no available tool can enforce `From`, **do not create wrong-sender drafts.** Give the user install/auth instructions plus ready-to-send subject/body/recipient text.

Never use browser automation or the user's Gmail UI to fix the sender.

After drafting, verify every draft: `From` matches the event's sender, `To`/`CC`/`BCC` match the template, subject contains the applicant's name, and the body carries the right coupon, discount, and amount to pay.

## Phase 6: Review Checkpoint

Before sending, report:

- applicants processed, and which event/opportunity
- cards moved to Clarification Needed, with reasons
- pastor-branch submissions skipped
- CSV path
- tracker row numbers
- coupon codes assigned
- **the sender resolved for this batch, and where it came from**
- draft ids / status and verification results

Do not send, tick `Sent`, or move cards until the user gives a go-signal.

## Phase 7: Go-Signal Send And Close

1. Send the verified drafts from the event's sender.
2. Search sent mail and verify: count equals processed applicants, `from` is the required sender, each recipient got the expected subject and coupon.
3. Move only successfully sent cards to lane `16`:
   ```json
   {
     "tool": "rock_workflow",
     "action": "updateConnectionRequest",
     "connectionRequestId": 1024,
     "statusId": 16,
     "dryRun": false,
     "commit": true,
     "reason": "Coupon email sent and verified"
   }
   ```
   Use the **ConnectionRequest id**, not the workflow/submission id.
4. In `REQUESTS`, tick `Sent` and fill `Sender Used` and `Date Sent`.
5. Add a Sheets note on each `Sent` cell with the sent date and sender, Manila time:
   ```text
   Sent via echo@favor.church on Friday, August 14, 2026, 12:02PM
   ```

If an email fails, do not move that card or mark it sent. Report the applicant and reason.

## Email-Approved Requests (exception)

When a request is **approved directly over email** (e.g. handed off from `triage-conference`) and there is **no matching card on the board**, do not block:

- Skip the board intake and the lane move for that applicant. A missing card is expected here.
- Still assign the coupon from the coupon tab (Phase 4) and still add the full row to `REQUESTS` (Phase 3), including the code, so it is drawn and recorded exactly once. Leave `Rock Request ID` blank and note "email-approved" .
- Draft/send in the applicant's thread as usual, from the event's sender.
- Determine the discount from their stated pay amount. If it is not in the email, use the tier already issued to the same requester's group (check the tracker for their email), or ask. Never round.

Everything else — exact-discount math, one coupon per applicant, tracker recording, sender enforcement — still applies.

## Verification Checklist

| Area | Verify |
| --- | --- |
| Environment | Announced prod on every Rock call |
| CONFIG | Event resolved, opportunity id, tabs, sender — none hardcoded |
| Intake | Lane 14 only, submissions joined to cards, pastor branch flagged |
| Clarifications | Moved to lane 15, no coupon or draft allocated |
| CSV | Exists, row count matches items inspected |
| Prices | Source recorded, live costs used |
| REQUESTS | Rows appended by header name, `Rock Request ID` filled, `Sent` unchecked pre-send |
| Coupons | Exact tier, `Used?=TRUE`, `Gave To` + `Rock Request ID` written, code copied to tracker |
| Drafts | Event's sender, recipients, CC/BCC, subject, placeholders, HTML formatting |
| Sending | Sent search confirms exact count and sender |
| Closing | Only sent cards moved to lane 16; `Sent` ticked with date note |

## Common Mistakes

| Mistake | Correct behavior |
| --- | --- |
| Looking for a Fluro board | Fluro is retired; use the Rock connection board |
| Reading ticket type / amount off the ConnectionRequest | Those attributes are empty — read the form submission |
| Treating an empty card attribute as `0` | It means "not copied", not "zero" |
| Sending everything from `conferences@favor.church` | Resolve the sender per event from `CONFIG` (Echo 2026 = `echo@favor.church`) |
| Hardcoding the opportunity id or tab names | Read them from `CONFIG` each run |
| Assigning a coupon from an archived tab | Archived tabs are history only |
| Interpreting `YES`, `.`, blank, or text as `0` | Clarification needed |
| Using stale ticket prices | Verify live prices first |
| Rounding to the nearest coupon tier | Exact discount only |
| Creating drafts from `rico@favor.church` | Stop and set up sender-capable tooling |
| Marking `Sent` after creating a draft | Only after a verified send |
| Moving a card with the workflow/submission id | Use the ConnectionRequest id |
| Using the browser UI to fix the sender | Forbidden; use MCP/CLI or hand over manual drafts |

## Adding a New Event

When a new conference opens:

1. In Rock, create a **ConnectionOpportunity** under ConnectionType `4` and note its id.
2. **Clone WT58** and point the clone's `Event` workflow attribute default at the new opportunity. This is the agreed pattern (decided 2026-08-14): the form deliberately has **no visible Event field**, because Rock's Connection Opportunity picker is not reliably filtered to one connection type and a public picker could misfile a request onto another team's board. One form per event, routing fixed by the attribute default. Never point two live events at one form.
3. Add a row to `CONFIG`: event code, name, `ACTIVE`, opportunity id, coupon tab, template tab, sender, CC, event page URL.
4. Create `<CODE>-Coupons` (copy the EC26 header row) and `<CODE>-Template` (copy EC26-Template, change FROM / subject / body / event URL).
5. Flip the finished event's `CONFIG` row to `ARCHIVED`, rename its tabs `ARCHIVE — …` and hide them.
