---
name: triage-conference
description: >
  Triage unread emails at conferences@favor.church, draft smart replies, and surface Favor Event Tickets action items.
  Use this skill whenever Rico asks to "triage conferences", "check conference emails", "what's in conferences@favor.church",
  "conference inbox", "any new registrations?", or asks for a conference email + event action summary. Also trigger when
  the user says /triage-conference or mentions catching up on conference communications. Always run the full pipeline:
  fetch unread → summarize → answer FAQs from the knowledge base → draft replies → suggest Favor Events next steps.
---

# triage-conference

Triage unread emails at conferences@favor.church, draft contextual replies that answer attendees' questions accurately, and surface next-step suggestions using Favor Event Tickets and Fluro data.

---

## Prerequisites

Each requirement below is a **capability bucket** — any one of the listed tools satisfies it. Run this preflight before triaging. If a **Required** bucket has no connected tool, explain what it is, why this skill needs it, and how to connect one of the options, then **stop and ask the user to set it up** before continuing — never invent inbox contents or event facts.

| Capability | Type | Satisfied by (any one) | If missing |
|---|---|---|---|
| **Gmail Draft Access** (on the `conferences@favor.church` mailbox) | Required | Gmail MCP (`search_threads`, `get_thread`, `create_draft`) · Composio Gmail (`GMAIL_*`) · `gws` CLI (if its OAuth has read scope) | Phases 1 (fetch unread) and 3 (draft replies) cannot run without it. Ask the user to connect the conferences Gmail, then wait. |
| **Conference KB** (`references/conference-kb.md`, bundled) | Required | the file shipped alongside this skill | Source of truth for event facts and FAQ answers. If not present, stop and ask — do not answer from memory. |
| **Event Tickets Access** (`attendees`, `orders`, `events`) | Required for Phase 4 actions | Favor Event Tickets MCP | Needed to resend tickets, check registrations, and fix wrong emails. If missing, you can still summarize and draft (Phases 1–3); warn that no ticket actions can be taken and ask to connect it for those. |
| **Fluro Access** (`item`, `update`) | Optional (conditional) | Fluro for Favor Church MCP | Only needed when an email requires tagging a contact (e.g. Favor DNA proof). If missing, draft the reply and note the tagging step is pending a Fluro connection. |
| `speak-like-favor` skill | Recommended | the `speak-like-favor` skill | Keeps every draft in Favor voice. If absent, apply the voice/HTML rules inlined in Phase 3. |

---

## Overview

This skill runs a 4-phase pipeline:

1. **Fetch & Summarize** — Search Gmail for unread messages to `conferences@favor.church`
2. **Classify & Answer** — Match each email to a known FAQ scenario and pull the correct answer from the knowledge base
3. **Draft Replies** — Create Gmail drafts in Favor voice for each email that warrants a reply
4. **Take/Suggest Actions** — Cross-reference Favor Event Tickets + Fluro to resend tickets, tag contacts, update records, and recommend follow-ups

**Always answer using the knowledge base in `references/conference-kb.md`. Never invent event facts.** If the KB does not cover something, say so and flag it for Rico rather than guessing.

---

## Phase 1: Fetch Unread Emails

Use the Gmail search tool with the query:

```
to:conferences@favor.church is:unread
```

- Set page size to 20–50 (paginate if more).
- For each result, fetch the full thread to get the body and any attachments.
- Extract: sender, subject, thread ID, body, date.
- Skip automated system mail (invoices, "Here's your ticket", "New ticket booking request", Fluro form-submission notices) unless they need action — note them as "no reply needed".

**Display a triage table:**

| # | From | Subject | Date | Scenario | Summary |
|---|------|---------|------|----------|---------|

---

## Phase 2: Classify & Answer from the Knowledge Base

Read `references/conference-kb.md` and match each email to a scenario in §3 of that file. Common recurring scenarios:

- Didn't receive ticket / QR → resend + "check inbox and spam".
- "Is my order confirmation my ticket?" → clarify order confirmation vs separate QR tickets.
- Wrong/bounced email → correct in Favor Event Tickets, resend.
- Ticket transfer request → point to `favor.church/tickettransfer`; transferable **until June 26**.
- Financial assistance → `favor.church/financialaid`, deadline **June 26**; multi-ticket requests need Ps Dawn & Kim approval.
- Serving / Open Access volunteer → `favor.church/serveatconference`.
- Sponsorship → `sponsorships@favor.church`.
- Kids questions (helper/yaya, check-in, pickup times) → see KB §5.
- **Kids guardian update request → update the attendee record in FET + CC kids@favor.church (see Phase 4).**
- Open Access / BTS / pastors sessions → see KB §6.
- General FAQs (parking, venue, food, merch, baggage, accommodations, livestream, lost wristband, PWD/senior/deaf) → KB §7–9.
- **Favor DNA proof/screenshot → reply AND tag the Fluro contact (see Phase 4).**

> **Deadline note:** the Conference FAQs doc still says transfers close "June 2" — that is stale. The operative deadline is **June 26** (live ticket emails + Rico's replies). Use June 26.

---

## Phase 3: Draft Replies (Favor voice)

For each email that needs a reply, draft a warm, accurate reply, then save it as a Gmail draft.

**Always apply the `speak-like-favor` skill** to every draft. Key rules:

- Open with `Hey, [Name]!`
- Warm, casual, clear, encouraging — no Christianese, no corporate stiffness.
- **No em dashes** (use commas, colons, parentheses). Don't start sentences with "And". Oxford commas.
- Dates/times in Favor format: `July 2`, `6PM`, `9:30PM` (no `:00`, no space before AM/PM).
- Currency with `₱`. Visible link text lowercase with no `https://`/`www`, e.g. `favor.church/tickettransfer`.
- **Draft as HTML, no markdown.** Use `<strong>`, `<ul><li>`, `<p>` — never `**` or `-` bullet characters. Bold key dates, deadlines, links, and action items.
- **Make links clickable:** wrap every link in `<a href="https://full-url">visible text</a>` (clean visible text, full URL in the href). See the `speak-like-favor` Email Rendering section.
- Keep it concise (3–5 sentences) unless clarification is needed.
- Close with:

  ```
  Much love,
  Favor Conference Team
  ```

  Use the specific event team name (e.g. "Business Breakfast Team") when triaging a different event — derive it from the event, never a generic fallback.

**Tooling:** create drafts with Composio `GMAIL_CREATE_EMAIL_DRAFT` on the conferences Gmail connection. Params: `recipient_email`, `extra_recipients`/`cc` (arrays), `subject` (with "Re: "), `thread_id` (threads correctly), `body`, and `is_html: true` for HTML. (`gws` can also create drafts, but its OAuth often lacks Gmail read scope, so it can't fetch the inbox.) Caveats learned in practice: `GMAIL_LIST_DRAFTS`/search lag on indexing and under-report — confirm a draft exists with `GMAIL_GET_DRAFT` by id, not the list. `GMAIL_UPDATE_DRAFT` often fails on thread-reply drafts ("Message not a draft"); to fix one, `GMAIL_DELETE_DRAFT` then recreate it.

**CC rules:**
- If the email was forwarded from another Favor inbox (e.g. `info@favor.church`), CC that inbox so they know it's handled. CC all Favor addresses already on the thread.
- **Kids guardian update emails: always CC `kids@favor.church`** so the Kids team is in the loop.

**Show each draft inline** for review before/after saving.

---

## Phase 4: Take & Suggest Actions (Favor Event Tickets + Fluro)

### Favor Event Tickets

| Email type | Action |
|------------|--------|
| Needs ticket resent | `attendees { action: "resend", attendee_id }` |
| Check if registered | `attendees { action: "query", event_query, search: "<email>" }` |
| Count for an event | `attendees { action: "count", event_query }` |
| Wrong email / update | `attendees { action: "update", attendee_id, ... }` then resend |
| Order issue | `orders { action: "attendees", order_id }` |
| Unknown event name | `events { action: "search", search: "<name>" }` |

### Kids guardian update → update the attendee record

When someone emails requesting a guardian change for their child's ticket (e.g. "I can't attend, my mother will be bringing my kid"):

1. Query attendees by the sender's email with `include_ticket_fields: true` to find both the adult and kids attendees on the order. The kids attendee record will have fields like `parents-guardians-first-name`, `parents-guardians-last-name`, `parents-guardians-gender`, `parents-guardians-mobile`.
2. Update the kids attendee record with the new guardian's details:
   ```
   attendees { action: "update", attendee_id: <kids_attendee_id>, information: {
     "parents-guardians-first-name": "<new first name>",
     "parents-guardians-last-name": "<new last name>"
   }, dry_run: false }
   ```
3. If the sender didn't provide the new guardian's mobile number, note it in the reply and ask for it.
4. Draft the reply (Phase 3) — **CC `kids@favor.church`** — confirming the update, noting that the guardian will need the **Parent Code (Ticket ID)** from the ticket confirmation email at kids check-in.
5. **Note:** The guardian data lives entirely in Favor Event Tickets. There is no separate Fluro form submission for kids conference registrations — don't spend time searching Fluro for one.

### Favor DNA proof → tag the contact in Fluro

When someone sends proof/screenshot that they completed **Favor DNA**:

1. Draft the acknowledgement reply (Phase 3).
2. Find their Fluro contact by name/email (`item { action: "query", body: { _type: "contact", ... } }`).
3. Tag the contact with the graduate tag **🎓 Favor DNA**, Fluro tag `_id` **`6824574fea78c50036f1b7a4`** (definition `equipping`).
   - Do **not** use the plain "Favor DNA" tag `687641e7d93dae0036d7e48c` (that's the in-progress tag).
   - PATCH the contact via the Fluro `update` tool, adding the tag id to the existing `tags` array (preserve current tags).
4. Confirm the tag was applied before marking the email handled.

### Output format per email:

```
📌 Email #1 — [Subject]   (Scenario: missing ticket)
  Draft saved ✅
  Actions taken / suggested:
  • Resent QR ticket to [email] → attendees { action: "resend", attendee_id: ... }
  • [Favor DNA] Tagged contact with 🎓 Favor DNA in Fluro ✅
  • [Guardian update] Updated kids attendee #XXXXX: guardian → [New Guardian Name] ✅
```

---

## Full Output Summary

```
📬 Triage Complete
  - X unread emails found
  - Y drafts saved
  - Z actions taken (resends, tags, corrections, guardian updates)
  - W action items suggested
```

---

## Edge Cases

- **No unread emails:** "No unread emails at conferences@favor.church right now. 🎉"
- **No reply needed** (notification, bounce, auto-reply, system mail): skip drafting, note it.
- **ID/attachment with no context:** ask what it's in reference to before acting.
- **Multiple emails from same sender:** group and draft one consolidated reply.
- **KB doesn't cover the question:** don't guess. Draft a holding reply and flag it for Rico to confirm the answer.
- **FAQ doc vs live facts conflict:** trust live facts (e.g. transfer deadline June 26, not June 2).
- **Kids guardian update — mobile number missing:** update the name fields anyway, then ask for the mobile in the reply draft.

---

## Compatible Tools

- Gmail MCP — `search_threads`, `get_thread`, `create_draft`, `label_thread`
- Favor Event Tickets — `attendees` (`count`, `query`, `update`, `resend`), `orders` (`attendees`), `events` (`search`, `list`)
- Fluro — `item` (`query`, `get`), `update` (`update` for tagging contacts)

## References

- `references/conference-kb.md` — conference knowledge base (event facts, pricing, FAQs, scenario→answer map, Favor DNA tagging). Read it at the start of every triage run.
