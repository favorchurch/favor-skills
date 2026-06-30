# attendees

Count how many people are **registered or checked in** for any event. Checks Favor Event Tickets (the ticketing source of truth) first, then falls back to Fluro for non-ticketed or internal events.

---

## What it does

1. Confirms Favor Event Tickets is connected.
2. Looks up the event by name and reports the **registered/ticket count**.
3. If the event isn't a ticketed one (count 0 or not found), falls back to **Fluro** RSVP forms, then physical check-ins.
4. Reports the count with its **source** clearly labeled, prioritizing registrations over check-ins.

Full logic in [`SKILL.md`](SKILL.md).

---

## Prerequisites

Each requirement is a **capability bucket** — any listed tool satisfies it.

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Event Tickets Access** | Required | Favor Event Tickets MCP | The skill explains it needs the ticketing connection and asks you to run `mcp oauth login favor-event-tickets`, then waits. It won't guess a count. |
| **Fluro Access** | Optional (fallback) | Fluro for Favor Church MCP | Only used for non-ticketed/internal events. If absent, the skill warns those can't be checked and reports what Event Tickets returns. |

---

## How to use it

- **Slash command:** `/attendees <event name>`
- **Plain language:** "how many signed up for X?", "headcount for Y?", "how many are coming to Z?"

---

## Recipes

| Recipe | What it does |
|---|---|
| `/attendees favor conference 2026` | Registered-attendee count for Favor Conference 2026 via ticket registrations. |
| `/attendees worship conference` | Resolves a partial name and reports the ticket count. |
| *"How many RSVP'd for the prayer night?"* | Falls back to Fluro RSVP forms for a non-ticketed event. |
| *"How many actually checked in to Favor Conference?"* | Uses Fluro check-ins for physical attendance specifically. |
| *"Compare registrations vs check-ins for Favor Conference 2026."* | Reports both numbers with sources and notes the difference. |

---

## Notes

- **Registrations > check-ins.** Check-ins only reflect who physically showed up, not who registered.
- For paid/free ticketed events, Favor Event Tickets is authoritative. For small groups and internal events, Fluro is more likely to have the data.
- On an auth error mid-run, the skill stops and tells you which login to refresh (see Error Handling in `SKILL.md`).

See the [root README](../../README.md) for install prompts and the full skills catalog.
