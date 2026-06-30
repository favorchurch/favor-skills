# export-attendees

Export the full attendee list from **Favor Event Tickets** and paste it (values only) into the matching **Google Sheets masterlist**, then stamp the "Last Updated" cell.

---

## What it does

1. Gets a short-lived CSV download URL from Favor Event Tickets.
2. Downloads the CSV (with a browser User-Agent — the signed URL 403s default agents).
3. Finds the masterlist sheet and reads its header row.
4. Matches columns by name (keeps existing column positions; new CSV columns go to the right; never overwrites sheet-only columns).
5. Pastes all rows in 300-row chunks (paced to stay under rate limits) in the Composio remote workbench.
6. Updates the "Last Updated" timestamp (Manila time) and reports a summary.

Full workflow + the Worship Conference 2026 sheet specifics in [`SKILL.md`](SKILL.md).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Event Tickets Access** | Required | Favor Event Tickets MCP | Source of the CSV; the skill asks you to connect it. |
| **Google Sheets Access** | Required | Composio `GOOGLESHEETS_*` (the flow uses the Composio Remote Workbench for the paste) | Needed to locate the masterlist and write values. |
| **Shell & Python** | Required | a terminal with `bash`, `curl`, Python 3 | The signed CSV URL must be `curl`ed promptly (expires ~15 min). |

---

## How to use it

- **Slash command:** `/export-attendees <event name>`
- **Plain language:** "sync the attendee list to the sheet", "update the masterlist with attendees", "paste the CSV to the masterlist".

---

## Recipes

| Recipe | What it does |
|---|---|
| `/export-attendees worship conference 2026` | Exports the full CSV into the masterlist and stamps "Last Updated". |
| *"Update the attendee sheet for Favor Conference."* | Resolves the event, finds the masterlist, pastes values. |
| *"Export the attendees again."* / *"Re-export."* | Re-runs against the same sheet + event discussed earlier. |
| *"Sync the list, but tell me about any new columns first."* | Reports column matches/new columns before pasting. |
| *"How many rows did we just write, and how many were cancelled?"* | Reports total rows, completed vs cancelled counts, and the timestamp set. |

---

## Notes

- **Cancelled rows are kept intentionally** — they're not filtered out.
- New CSV columns are appended to the right; existing column positions never shift.
- The full CSV is processed in the remote workbench, not loaded into the AI's context.

See the [root README](../../README.md) for install prompts and the full skills catalog.
