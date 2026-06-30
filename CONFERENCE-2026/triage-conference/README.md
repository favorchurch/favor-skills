# triage-conference

Triage the **conferences@favor.church** inbox: fetch unread mail, answer each message accurately from the conference knowledge base, draft Favor-voice replies, and surface the right Favor Event Tickets / Fluro actions.

---

## What it does

A 4-phase pipeline:

1. **Fetch & summarize** unread mail and show a triage table.
2. **Classify & answer** each email against `references/conference-kb.md` (never invents event facts).
3. **Draft replies** in Favor voice, as HTML, with correct dates, links, and the right team closing.
4. **Take/suggest actions** — resend tickets, fix wrong emails, update kids guardian records, tag Favor DNA contacts in Fluro.

Full pipeline in [`SKILL.md`](SKILL.md); event facts in [`references/conference-kb.md`](references/conference-kb.md).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Gmail Draft Access** (conferences mailbox) | Required | Gmail MCP · Composio Gmail · `gws` (with read scope) | Can't fetch or draft without it; the skill stops and asks you to connect the conferences Gmail. |
| **Conference KB** (`references/conference-kb.md`) | Required | the bundled file | If absent, the skill stops rather than answering event facts from memory. |
| **Event Tickets Access** | Required for actions | Favor Event Tickets MCP | You can still summarize and draft (Phases 1–3); ticket resends/lookups need this connected. |
| **Fluro Access** | Optional | Fluro for Favor Church MCP | Only for tagging contacts (e.g. Favor DNA proof). If absent, the reply is drafted and tagging is noted as pending. |
| `speak-like-favor` | Recommended | the skill | Keeps every draft on-brand. |

---

## How to use it

- **Slash command:** `/triage-conference`
- **Plain language:** "check the conference inbox", "what's in conferences@favor.church?", "any new registrations to handle?"

---

## Recipes

| Recipe | What it does |
|---|---|
| `/triage-conference` | Full run: fetch unread, classify, draft replies, suggest/take ticket actions. |
| *"Just summarize the conference inbox, don't draft anything yet."* | Phase 1 only — the triage table. |
| *"Someone didn't get their QR ticket — resend it and reply."* | Resends via Favor Event Tickets and drafts a "check inbox and spam" reply. |
| *"This person wants to change their kid's guardian."* | Updates the kids attendee record in Favor Event Tickets and CCs kids@favor.church on the reply. |
| *"They sent Favor DNA proof — acknowledge and tag them."* | Drafts the acknowledgement and tags the Fluro contact with 🎓 Favor DNA. |

---

## Notes

- **Live facts beat the FAQ doc.** The KB notes where the public doc is stale (e.g. transfer deadline is June 26, not June 2).
- Drafts are created for review — it shows each one before/after saving.
- Skips automated/system mail unless it needs action.

See the [root README](../../README.md) for install prompts and the full skills catalog.
