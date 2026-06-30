---
name: export-attendees
description: >
  Export attendee data from Favor Event Tickets (WordPress/WooCommerce) to a Google Sheets masterlist.
  Use this skill whenever the user wants to sync, export, update, or paste attendee/registration data
  from an event into a Google Sheet — even if phrased casually like "update the sheet with attendees",
  "sync the attendee list", "export attendees to Sheets", or "paste the CSV to the masterlist".
  Also triggers for follow-up commands like "do it again" or "re-export" when attendees were previously discussed.
---

# Export Attendees Skill

Exports the full attendee CSV from Favor Event Tickets and pastes it (values only) into the matching Google Sheets masterlist, then updates the "Last Updated" timestamp.

---

## Prerequisites

Each requirement below is a **capability bucket** — any one of the listed tools satisfies it. Run this preflight before exporting. If a **Required** bucket has no connected tool, explain what it is, why this skill needs it, and how to connect one of the options, then **stop and ask the user to set it up** before continuing — never paste partial or fabricated rows.

| Capability | Type | Satisfied by (any one) | If missing |
|---|---|---|---|
| **Event Tickets Access** (`attendees` with `action: "csv"`) | Required | Favor Event Tickets MCP | Source of the attendee CSV. Ask the user to connect it (e.g. `mcp oauth login favor-event-tickets`), then wait. |
| **Google Sheets Access** (+ Composio Remote Workbench for the paste) | Required | Composio `GOOGLESHEETS_*` (this skill's flow assumes the Composio workbench) | Needed to locate the masterlist and paste values in chunks. Ask the user to connect the `googlesheets` toolkit in Composio, then wait. |
| **Shell & Python** (bash + `curl` with a browser User-Agent) | Required | a terminal with `bash`, `curl`, and Python 3 | The signed CSV URL returns HTTP 403 to default User-Agents and expires in ~15 min. Without a shell, the CSV can't be downloaded. |

---

## Workflow

### Step 0 — Resolve the target event

Decide which event to export **before** anything else. Never assume a specific conference.

1. **If the user named an event** (this message or earlier in the conversation), use that as the `event_query` and skip to Step 1.

2. **If no event was named** (e.g. "sync the sheet", "update attendees", "do it again" with no prior event in context), auto-resolve the default to **the current conference** from the live event list — do NOT hardcode one:

   ```
   Favor Event Tickets:events
     action: "search"
     query: "conference"
     per_page: 50
   ```

   From the results, pick the **soonest upcoming conference**: the event with "conference" in its title whose `end_date` has **not yet passed** (`end_date` >= today, Asia/Manila UTC+8), choosing the one with the earliest `start_date`. That becomes the `event_query`.

   Worked example (today = 2026-06-30):
   - Favor Conference 2026 ends 2026-07-04 → not passed → **selected default**.
   - Worship Conference 2026 (ended 2026-04-18) and High School Conference 2026 (ended 2026-03-07) → past → skipped.
   - On/after 2026-07-05, Favor Conference 2026 is past, so the default rolls forward to the next conference whose end date hasn't passed (whatever it is — Worship/High School/Favor, soonest wins).

Announce the resolved event in your first reply (e.g. "No event specified — defaulting to the current conference: **Favor Conference 2026** (ends Jul 4, 2026)"), then continue **end-to-end without a confirmation prompt** — the only thing that pauses for confirmation is a missing sheet (Step 3).

### Step 1 — Get the CSV download URL

Use `Favor Event Tickets:attendees` with the event name. This returns a temporary download URL (expires in 15 minutes, per the response's `expires_in: 900` — still download promptly) and the total attendee count.

```
Favor Event Tickets:attendees
  action: "csv"
  event_query: "<resolved event from Step 0>"
```

Note the `total_attendees` from the response — this is the completed-tickets count for the final report.

### Step 2 — Download the CSV (bash)

```bash
curl -s "<download_url>" -o /tmp/attendees.csv
head -1 /tmp/attendees.csv   # capture header row only
wc -l /tmp/attendees.csv     # total row count
```

Only read the header row here — do NOT load all rows into context. The full data will be processed in the remote workbench.

### Step 3 — Find the Google Sheet

Use `GOOGLESHEETS_SEARCH_SPREADSHEETS` (via Composio) to locate the sheet by the **resolved event name** (e.g. "Favor Conference 2026"). Capture the `spreadsheet_id`.

Then use `GOOGLESHEETS_GET_SHEET_NAMES` to list all tabs — identify the one that looks like a masterlist (usually named "MASTERLIST" or similar).

- **Sheet found** → continue to Step 4 end-to-end, no confirmation needed.
- **No sheet matches the event name** → do NOT fall back to another conference's sheet or guess. Stop and ask the user to confirm creating a fresh masterlist (Step 3b). Proceed only after they say yes.

### Step 3b — Create the masterlist (only if none exists)

Run this **only** when Step 3 finds no sheet for the resolved event, and **only after the user confirms**.

Create a new spreadsheet titled `<Event Name> Attendees` (e.g. "Favor Conference 2026 Attendees") with a `MASTERLIST` tab, modeled on the most recent prior conference masterlist (see the cache table at the bottom) so downstream formulas/filters line up:

- **A1:** `Last Updated` label · **B1:** timestamp (written in Step 7)
- **Header row at row 4:** the CSV column names, in CSV order
- **Data starts at row 5**

Use `GOOGLESHEETS_CREATE_SPREADSHEET` (then write the A1 label + row-4 headers). Capture the new `spreadsheet_id` and continue to Step 4.

### Step 4 — Read sheet headers

Fetch rows 1–6 of the masterlist tab to locate:
- The **header row** (the row containing column names matching the CSV)
- The **"Last Updated"** cell (look for the label in column A; the timestamp value is in column B of the same row)
- The **first data row** (the row immediately after the header row)

Use `GOOGLESHEETS_BATCH_GET` with range `MASTERLIST!A1:Z6`.

Report to the user:
- Which row the headers are on (e.g., "Headers found at row 4")
- Which cell holds "Last Updated" (e.g., "Last Updated timestamp is at B1")
- Where data will be pasted (e.g., "Data will be pasted starting at row 5")

### Step 5 — Match columns (in Remote Workbench)

In the Composio remote workbench:

1. Parse the CSV header
2. Compare with sheet header row
3. **Column matching rules:**
   - Match by column name (case-insensitive, trim whitespace)
   - For columns that **exist in both**: keep the sheet's original column index — paste CSV data into that same column position
   - For columns **only in the CSV** (new): append them to the right of the last sheet column
   - For columns **only in the sheet** (missing from CSV): leave them blank / do not overwrite
4. Build a column mapping: `{csv_col_index: sheet_col_index}`

If the sheet header row has fewer columns than the CSV, note which new columns will be added and to which column letters.

### Step 6 — Paste data (in Remote Workbench)

Write the full data (all rows, including cancelled orders) to the sheet in chunks of 300 rows to avoid rate limits. Use `RAW` value input option. Sleep 1.2s between chunks.

```python
CHUNK = 300
for i in range(0, len(data_rows), CHUNK):
    chunk = data_rows[i:i+CHUNK]
    start_row = header_row + 1 + i
    end_row = start_row + len(chunk) - 1
    rng = f"'MASTERLIST'!A{start_row}:V{end_row}"  # adjust end col as needed
    run_composio_tool("GOOGLESHEETS_UPDATE_VALUES_BATCH", {
        "spreadsheet_id": SPREADSHEET_ID,
        "valueInputOption": "RAW",
        "data": [{"range": rng, "values": chunk}]
    })
    time.sleep(1.2)
```

### Step 7 — Update "Last Updated" timestamp

Update the timestamp cell (found in Step 4) with the current Manila time (UTC+8).

Format: `M/D/YYYY HH:MM:SS` — use `USER_ENTERED` so Sheets parses it as a date.

### Step 8 — Report

Summarize:
- Total rows in CSV (all statuses)
- Completed tickets count
- Cancelled tickets count
- Rows written to sheet
- Any column mismatches or new columns added
- Last Updated timestamp set

---

## Default event & per-event sheet cache

**The default event is resolved at runtime in Step 0** — the soonest conference whose end date hasn't passed. No conference below is a permanent default; the cache is only a shortcut for repeat exports.

Sheet coordinates are discovered dynamically in Steps 3–4. Add a row here once you confirm a new event's layout. The most recent filled row also serves as the template when creating a new masterlist (Step 3b).

| Event | Spreadsheet ID | Tab | Header row | Data starts | Last Updated | Columns |
|---|---|---|---|---|---|---|
| Favor Conference 2026 *(current default)* | _discover in Step 3_ | MASTERLIST | _discover_ | _discover_ | _discover_ | _discover_ |
| Worship Conference 2026 *(past — layout template)* | `1XtIpt-mRAvDbTQ5Q7EqlmkCXNh0REAfaZGv-FiuZDZU` | MASTERLIST | Row 4 (A4:V4) | Row 5 | A1 label → **B1** value | A–V (22); CSV adds `Purchase Date` as col W |

[Worship Conference 2026 Attendees sheet](https://docs.google.com/spreadsheets/d/1XtIpt-mRAvDbTQ5Q7EqlmkCXNh0REAfaZGv-FiuZDZU/edit) — reference for the masterlist layout.

---

## Notes & Gotchas

- **CSV token expires in 15 minutes** (`expires_in: 900`) — still download promptly after fetching the URL. Don't read the headers first and then re-fetch.
- **Programmatic download needs a browser User-Agent** — the signed URL returns HTTP 403 to default UAs (Cloudflare/WAF). Fetch with `curl -A "Mozilla/5.0 ..."` or equivalent.
- **Cancelled rows are included intentionally** — do not filter them out.
- **"Tickets are non-refundable" column** is mostly blank in the CSV — this is a known server-side data issue, not a paste error.
- **Rate limits:** Google Sheets allows ~60 writes/min. The 300-row chunk + 1.2s delay keeps writes safe.
- **Do not use token limit on CSV parsing** — process the full CSV only in the remote workbench, not in Claude's context window.
- **Column merge rule:** Never shift existing column positions. New CSV columns go to the right of the last sheet column.
