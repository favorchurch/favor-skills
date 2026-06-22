---
name: attendees
description: Count registered or checked-in attendees for an event using Favor Event Tickets (WordPress/WooCommerce) or Fluro. Use when asked about attendee counts, RSVPs, registrations, headcount, or event attendance.
---

# Attendees Skill

Count attendees for any event by checking Favor Event Tickets (WordPress/WooCommerce) first, then Fluro as a fallback.

## Workflow

### Step 1 — Authenticate Favor Event Tickets first

- If the Favor Event Tickets MCP session is not authenticated, stop and prompt the user to run `mcp oauth login favor-event-tickets`.
- Do not continue to Fluro until Favor Event Tickets has been authenticated.

### Step 2 — Check Favor Event Tickets (WordPress)

Use `mcp_favor-event-tickets_event_attendee_count` with the event name or partial title as `event_query`.

- If the event is found and returns a count → **report it and stop**.
- If an authentication error occurs at this stage, stop and prompt the user to run `mcp oauth login favor-event-tickets`. Re-authorization must be done via the CLI's built-in OAuth flow, not another skill.
- If the result is 0 or the event is not found (and no auth error) → proceed to Step 3.

```
mcp_favor-event-tickets_event_attendee_count
  event_query: "<user's event name>"
```

### Step 3 — Check Fluro (fallback)

Try `mcp_fluro-mcp_attendee_rsvp` first (it checks forms, guestlists, and mailing lists):

```
mcp_fluro-mcp_attendee_rsvp
  search: "<user's event name>"
```

- If `attendee_rsvp` returns a count → **report it and stop**.
- If `attendee_rsvp` returns 0 or no match, and you have a Fluro event ID, fall back to `mcp_fluro-mcp_event_checkins` for physical check-in counts.

### Step 4 — Reporting

Present results clearly:

- State the event name as resolved/matched.
- Show the attendee count with the source (e.g., "via ticket registrations" or "via RSVP form" or "via check-ins").
- If counts came from multiple sources, show each separately and note any differences.
- If nothing is found in either system, say so clearly and suggest the user double-check the event name.

## Notes

- **Prioritize RSVP/registration counts over check-in counts** — check-ins only reflect who physically attended, not total registered.
- If the user asks specifically about check-ins or physical attendance, use `event_checkins` directly.
- For ticket-based events (paid or free tickets via WooCommerce), Favor Event Tickets is the authoritative source.
- For small groups, prayer events, or internal church events, Fluro is more likely to have the data.

## Error Handling

### Authentication Errors

If you encounter an authentication error (e.g., `401 Unauthorized`, `Invalid token`, or `Authentication failed`) from any MCP tool:

- **For Fluro (`fluro-mcp`):** 
  - If the error occurs, prompt the user to run `mcp oauth login fluro-mcp`. 
  - **Do not** attempt to fix this via another skill (like `fluro-auth`); the underlying MCP session must be re-authorized via the CLI's built-in OAuth flow.
- **For Favor Event Tickets:**
  - Prompt the user to run `mcp oauth login favor-event-tickets` to refresh the session.
  - This is the required first step before falling back to Fluro.
- **General:**
  - If an MCP tool returns an auth error, do not silently fail. Report the error to the user and explain that re-authorization is required to continue.
