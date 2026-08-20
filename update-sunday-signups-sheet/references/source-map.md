# Source Map — CIW / SIGNUPS

## Fixed Sheet

- Spreadsheet ID: `1bUdcidjNrdxC4fyqgqIxWfQ3N6YvFDXY2gpQFts_Vzs`
- Tab: `CIW / SIGNUPS`  ·  gid/sheetId: `2040871883`
- Headers in row 2 (frozen 2 rows). Column A = weekly Sunday dates; data starts row 3.

## Columns (row 2 headers carry the source hyperlinks)

| Col | Header | Source system | Identifier |
|-----|--------|---------------|------------|
| B | ATTENDEES | manual / headcount | — |
| C | CHINESE | manual | — |
| D | HANDS RAISED | manual | — |
| E | CONNECT | **Rock** | workflow type `26` Sign up for a Connect Group! |
| F | SERVE | **Rock** | workflow type `49` Volunteer to Serve |
| G | BUILD | Rock | workflow types `34` BUILD ONLINE, `71` BUILD ONLINE - Saturday |
| H | FAVOR DNA | Rock | workflow types `30` Favor DNA, `61` Favor DNA - Saturday |
| I | BUILD (course) | Rock(?) | Fluro `buildCourseRegistrationForm` (defunct); Rock `Build` (type 45). Out of default scope. |
| J | NPN | Fluro (defunct) | interaction `newPeopleNightRsvp`. Out of default scope. |

Default scope = E–H only. **All four E–H source from Rock RMS only.** Fluro has been decommissioned — do not query it or attempt any dedup/union step. (CONNECT/SERVE migrated in the July 2026 cutover; BUILD/FDNA in June 2026; residual Fluro confirmed at 0 as of the 2026-08-03 run.) See the one-shot helper `scripts/signups-week-count.py`.

## Rock (all four: CONNECT 26, SERVE 49, BUILD 34/71, FAVOR DNA 30/61)

- Use the **prod** read-only MCP: `claude.ai Rock MCP (Read-only)` = `rock.favor.church`, Rock v17.7, Asia/Manila. Requires OAuth — if not connected, user runs `/mcp` → "claude.ai Rock MCP (Read-only)" → browser sign-in.
  - ⚠️ A second server, **`Rock-Preview`**, may also be connected with no auth — it is a **stale/wrong backend** (returns 0 for these workflow-type counts). Do not use it. Confirm you're on prod: `count WorkflowTypeId eq 34` for a recent week is non-zero.
  - ⚠️ Confirm type IDs with `rock_workflow action: workflowTypes` (authoritative). Do **not** trust `rock_lookup quickSearch` for workflowType IDs — it has returned id 42 ("New People") for "BUILD ONLINE". The authoritative list confirms 34/71/30/61 below.
- `rock_entity` `action: count`, `model: workflows`, OData **v1** syntax (the MCP falls back to REST v1):
  `WorkflowTypeId eq 34 and CreatedDateTime ge datetime'2026-06-15T12:00:00' and CreatedDateTime lt datetime'2026-06-22T12:00:00'`
- BUILD = count(34) + count(71).  FAVOR DNA = count(30) + count(61).  CONNECT = type 26.  SERVE = type 49.
- Each workflow instance = one signup form submission. BUILD/FDNA are all `Status="Completed"` and (harmlessly) named `"New Form"`. SERVE (49) rows stay `Status="Active"`. CONNECT (26) real rows are named with the registrant (`"MNL | Juan Dela Cruz"`).
- **Junk filter = exclude `Status=="Delivery Failed"` ONLY.** CONNECT accrues empty Delivery-Failed rows (17 in the 2026-07-12 week). ⚠️ Never filter by `Name=="New Form"` — that zeroes BUILD/FDNA (they're all named "New Form"). Include archived connect signups (`connectPortalArchived==True`).
- **Manila-only**: campus Id 1=MNL, 2=BNE, 3=SEL, 4=Global. These six form types are Manila-scoped (verified: no BNE/SEL initiators). Forms have no campus field; person `PrimaryCampusId` is mostly null → do NOT filter by person campus.
- **Rock REST API** (for CONNECT junk-filtering, attribute detail, or when the MCP falls short — MCP can't read workflow AttributeValues [404] & ignores `$sort`): key/url in `~/Git/connect.favor.church/.env.production` (`ROCK_API_KEY`, `ROCK_API_URL`), header `Authorization-Token`. (This repo was formerly named `favor-connect-portal`; if the path moves again, search `~/Git` for `.env.production` containing `ROCK_API_KEY`.) `GET /api/Workflows?$filter=WorkflowTypeId eq N and CreatedDateTime ge datetime'…' and CreatedDateTime lt datetime'…'&$select=Id,Name,Status,CreatedDateTime&$top=1000`. WAF **403s** on default `Python-urllib` UA (send a curl UA) and on `%27`-encoded quotes (keep `'` `:` `,` literal). Attrs: `GET /api/Workflows/{id}?loadAttributes=simple`. Alias→campus: `GET /api/People/GetByPersonAliasId/{aliasId}`.
- **Exclude**: `Build` (45 → maps to column I), and automation workflows `Update FDNA/BUILD Group` (59/62/68/69/72/73), `BUILD GRADUATION` (75).
- Connection type "MNL | Grow | Build & FDNA" (id 2) is the downstream pipeline, **not** the raw signup count.

## Write (Sheets API v4)

- Token: `gcloud auth application-default print-access-token`; header `x-goog-user-project: gen-lang-client-0705704834` (or `$GOOGLE_CLOUD_QUOTA_PROJECT`).
- `PUT .../values/'CIW / SIGNUPS'!E{row}:H{row}?valueInputOption=USER_ENTERED` with `{"values":[[connect,serve,build,fdna]]}`.
- Read links: `GET .../{id}?ranges=...&includeGridData=true&fields=sheets(data(rowData(values(formattedValue,hyperlink,userEnteredFormat/textFormat/link))))`.

## Validation note

The Monday-noon PH window was validated against the prior week (Jun 8→15 vs the Jun 14 row): Fluro SERVE reproduced exactly (15) and Rock-era BUILD closely. Historical G/H values predate the Fluro→Rock migration, so do not expect exact continuity across the 2026-06-14/15 boundary. As of the 2026-08-03 run, Fluro is fully decommissioned and residual counts confirmed at 0 — Rock-only going forward (e.g. week of Jul 27–Aug 3: CONNECT 40, SERVE 14, BUILD 10, FAVOR DNA 20, all Rock, no Fluro residual).
