---
name: update-sunday-signups-sheet
description: Update weekly ministry signup counts (CONNECT, SERVE, BUILD, FAVOR DNA) in the CIW / SIGNUPS tab. All four now source from Rock RMS workflow types (CONNECT 26, SERVE 49, BUILD 34/71, FAVOR DNA 30/61); CONNECT & SERVE also aggregate any residual Fluro submissions during the 2026 cutover (deduped by timestamp). Trigger when asked to update Sunday signups, CIW signups, weekly signups, or columns E–H of the CIW sheet.
---

# Update CIW / SIGNUPS Weekly Signups

## Scope

Update the weekly signup counts in one fixed tab:

- Spreadsheet: `1bUdcidjNrdxC4fyqgqIxWfQ3N6YvFDXY2gpQFts_Vzs` ("FAVOR SUNDAY LIVE HEADCOUNTS")
- Tab: `CIW / SIGNUPS`
- gid / sheetId: `2040871883`
- Columns updated: **E–H** (the signup counts) for the current week's row, plus **A** (the Sunday date) when that cell is blank.

Never edit other tabs or columns (`B/C/D` headcount, `I/J`) unless the user explicitly changes scope.

Before each run, read:
- `references/source-map.md` — column→source mapping, Fluro definitions, Rock workflow type IDs, write mechanics.
- `references/learned-nuances.md` — corrections from previous runs.

## Column → source map (driven by row-2 hyperlinks)

Row 2 holds headers whose cells carry hyperlinks to each ministry's signup query. Always re-read these links first (they are the source of truth) — definitions or systems can change.

| Col | Header | Live source |
|-----|--------|-------------|
| E | CONNECT | **Rock** workflow type `26` (Sign up for a Connect Group!) ∪ residual Fluro `mnlSignUpForAConnectGroup` |
| F | SERVE | **Rock** workflow type `49` (Volunteer to Serve) ∪ residual Fluro `signUpToServe` |
| G | BUILD | **Rock** workflow types `34` (BUILD ONLINE) + `71` (BUILD ONLINE - Saturday) |
| H | FAVOR DNA | **Rock** workflow types `30` (Favor DNA) + `61` (Favor DNA - Saturday) |

**All four signups now live in Rock RMS.** BUILD/FAVOR DNA migrated 2026-06-14 (Fluro `mnlBuildOnline`/`mnlFavorDna` dead since). CONNECT/SERVE migrated in the **July 2026 cutover** (Rock CONNECT type 26 live from 2026-06-03; Rock SERVE type 49 first submissions 2026-07-12). Rock is the go-forward source of truth for all four.

**Cutover aggregation (CONNECT & SERVE only).** During the transition, connect/serve signups may appear in Fluro *and/or* Rock. They must be a **deduped union**, not a sum:
- **CONNECT** — Fluro `mnlSignUpForAConnectGroup` is **mirrored** into Rock (identical submission timestamps: Fluro `created` UTC == Rock `CreatedDateTime` Manila to the second). Take the union — matching timestamps are the *same* signup counted once. (2026-07-05 week: Rock 21 == Fluro 21, all matched → 21. 2026-07-12 week: Rock 32 + 2 Fluro-only = 34.)
- **SERVE** — Fluro `signUpToServe` and Rock type 49 are **disjoint** (different people, no timestamp matches) → the union is effectively their sum. (2026-07-05 week: Rock 0 + Fluro 7 = 7. 2026-07-12 week: Rock 6 + Fluro 13 = 19.)
- As the cutover completes, Fluro CONNECT/SERVE should trend to 0; keep aggregating until they're reliably empty, then Rock-only.

**Manila-only.** Rock is now multi-campus (Manila=1, Brisbane=2, Seoul=3). These six form types (26, 49, 34, 71, 30, 61) are **Manila-scoped** — other campuses use separate form types (e.g. 24 BNE youth, 39 BNE kids). Verified: no Brisbane/Seoul initiators appear in these types. The forms carry **no campus field**, and initiators' `PrimaryCampusId` is mostly null, so do **not** try to filter by person campus — just count the Manila form types.

## Weekly Rule

Asia/Manila time, **Monday 12:00 PM rollover** (same convention as `update-tech-dashboard-live-signups`).

- `currentCutoff` = most recent Monday 12:00 PM that has already passed.
- Reporting window = **[currentCutoff − 7 days, currentCutoff)**.
- The row to fill is the most recent data row — its `A` date is the Sunday inside the window. `A` and the `B/C/D` headcount columns are often still blank on a Monday (the CIW team fills them later); the row may be **entirely empty**. That's fine — write `E:H` regardless (signup columns are independent of the headcount columns), and fill `A` with the Sunday date if blank. Confirm `E:H` are empty before writing.
- Column `A` format is `Mon DD YYYY`, zero-padded day (e.g. `Jun 28 2026`). The Sunday in the window = `currentCutoff − 1 day`.

Use `scripts/week-window.mjs` to compute the window.

## Workflow

1. **Snapshot.** Read `A1:N2` (headers) and the last ~15 data rows (`A165:N185` area) with `valueRenderOption=FORMATTED_VALUE`. Identify the target row (latest, `E:H` blank). Re-read row-2 links with `includeGridData` + `userEnteredFormat/textFormat/link` to confirm the per-column source.

2. **Compute counts for the window** (recompute live; counts drift through the day). All four counts now come from Rock; CONNECT/SERVE additionally union any residual Fluro. **Easiest path: `scripts/signups-week-count.py`** computes all four (Rock counts + Fluro union, deduped by timestamp) for a given window in one shot. Manual mechanics:
   - **Rock (all four)** — count workflow rows per type in the window. Two ways:
     - *MCP* (`rock_entity`, `action: count`, `model: workflows`, prod read-only) with OData v1 `where`:
       `WorkflowTypeId eq 34 and CreatedDateTime ge datetime'<startISO>' and CreatedDateTime lt datetime'<endISO>'`. Good for BUILD/FAVOR DNA (clean, all `Completed`).
     - *REST API* (needed for CONNECT — see junk-filter below — and any attribute-level detail): prod Rock API key at `~/Git/favor-connect-portal/.env.production` (`ROCK_API_KEY`; header `Authorization-Token`), `GET https://rock.favor.church/api/Workflows?$filter=...&$select=Id,Name,Status,CreatedDateTime&$top=500`. Rock `CreatedDateTime` is already Asia/Manila.
       - ⚠️ **WAF gotchas:** the API rejects the default `Python-urllib` User-Agent (403) and percent-encoded single-quotes (`%27` → 403). Send a browser/curl `User-Agent` and keep `'`, `:` , `,` **literal** in the query string. The read-only MCP **cannot** read workflow AttributeValues (404) and **ignores `$sort`** — use the REST key for attribute/registrant detail; use `where`-filtered `count`/`search` (order-independent) for counting.
     - Sums: BUILD = type 34 + 71; FAVOR DNA = type 30 + 61 (Saturday variants 71/61 are usually 0). CONNECT = type 26; SERVE = type 49.
     - **Junk filter = `Status == "Delivery Failed"` only.** Type 26 accrues failed submissions with `Status = "Delivery Failed"`, named `"New Form"`, no `Person`/`connectGroup` (a batch of 17 hit the 2026-07-12 week). Exclude **only** `Status == "Delivery Failed"`. ⚠️ Do **not** filter on `Name == "New Form"`: BUILD (34) and FAVOR DNA (30) workflows are *all* legitimately named `"New Form"` — filtering by name zeroes them. (Real CONNECT rows are named e.g. `"MNL | Juan Dela Cruz"`; SERVE rows are `"New Volunteer to Serve"`, `Status = "Active"` since they don't auto-complete.) Per Rico: **include archived** connect signups (`connectPortalArchived == True` are still real — do not drop them; the Delivery-Failed filter already leaves them in).
   - **Fluro residual union (CONNECT & SERVE)** — Fluro REST `POST https://api.fluro.io/content/_query?limit=5000&simple=false` (token `FLURO_TOKEN` from `~/.env`). Body `{"_type":"interaction","definition":"<def>","status":{"$in":["active","draft","archived"]}}` (defs: `mnlSignUpForAConnectGroup`, `signUpToServe`). Filter `created` (UTC) into the Manila window. **Dedupe against Rock by timestamp:** convert Fluro `created`+8h and Rock `CreatedDateTime` to a per-second key; a Fluro row whose second matches a Rock row is the *same* signup (skip it). CONNECT total = Rock-valid + Fluro-only; SERVE total = Rock + Fluro-only. (Fluro response is ~70 MB — Node's `fetch` handles it; Python `urllib` may `IncompleteRead`, so fetch Fluro in Node, e.g. `scripts/fluro-week-count.mjs`, or dump timestamps to a file.)
     - **Use the right Rock server.** The session may expose two MCP servers: **`Rock MCP (Read-only)`** = prod `rock.favor.church` (correct; requires OAuth) and **`Rock-Preview`** = a stale/wrong backend that returns 0. If only Preview is connected, ask the user to run `/mcp` → **"claude.ai Rock MCP (Read-only)"** → browser sign-in. Sanity-check: `count WorkflowTypeId eq 34` for a recent week is non-zero. (The REST API key always hits prod.)
     - **Verify type IDs against ground truth, not `quickSearch`.** `rock_lookup quickSearch` is unreliable (misreported BUILD ONLINE as id 42 = actually "New People"). Use `rock_workflow action: workflowTypes` for the authoritative list: 34 BUILD ONLINE, 71 BUILD ONLINE - Saturday, 30 Favor DNA, 61 Favor DNA - Saturday, 26 Sign up for a Connect Group!, 49 Volunteer to Serve.
     - **Validate before trusting.** Re-run the prior week's window and reproduce the previous row's values (e.g. [Jun-15 12:00, Jun-22 12:00) → type 34 = 21, type 30 = 37, matching row 179's BUILD 21 / FAVOR DNA 37).

3. **Write E:H** via Sheets API v4 `values.update` (`valueInputOption=USER_ENTERED`), range `'CIW / SIGNUPS'!E{row}:H{row}`, values `[[connect, serve, build, fdna]]`. Use the `gcloud auth application-default print-access-token` ADC token + `x-goog-user-project` header. E:H are plain values — no formulas to preserve. Helper: `scripts/sheets-write-range.mjs`. **Also write `A{row}`** with the Sunday date (`Mon DD YYYY`) if that cell is blank — separate write to `'CIW / SIGNUPS'!A{row}`.

4. **Verify.** Read back `A{row}:H{row}` (FORMATTED_VALUE); confirm `A` (date) and `E–H` (counts) landed and that `B/C/D` are untouched. Spot-check one Rock count (`rock_entity search`) and one Fluro count.

5. **Improve.** Append corrections/mappings to `references/learned-nuances.md`.

## Link re-point (all four E2:H2 → Rock DataViews)

E2:H2 now point at Rock **DataViews** (the analog of the old Fluro filtered-list links), page 145:
- CONNECT (E2) → `…/page/145?DataViewId=28` (workflow type 26)
- SERVE (F2) → `…/page/145?DataViewId=29` (workflow type 49)
- BUILD (G2) → `…/page/145?DataViewId=22` (workflow types 34 + 71)
- FAVOR DNA (H2) → `…/page/145?DataViewId=23` (workflow types 30 + 61)

All four created 2026-06/07 and don't normally need re-creating. (DataViews filter by workflow type **all-time**, not by week — a "click to see the signups" reference; the weekly number lives in the cell.) To recreate/maintain a DataView, use the prod **Rock API key** at `~/Git/favor-connect-portal/.env.production` (`ROCK_API_KEY`; header `Authorization-Token: <key>` against `https://rock.favor.church/api`). Do not read that repo — only the env file. The read-only MCP cannot write DataViews.

Recipe (per DataView): POST `DataViewFilters` root `{"ExpressionType":2}` (GroupAny/OR) → POST child `DataViewFilters` `{"ExpressionType":0,"ParentId":<root>,"EntityTypeId":121,"Selection":"[\"Property_WorkflowTypeId\",\"1\",\"<typeId>\"]"}` (121 = PropertyFilter, `1` = EqualTo) → POST `DataViews` `{"Name":...,"EntityTypeId":113,"CategoryId":131,"DataViewFilterId":<root>}` (113 = Workflow, 131 = "Foundational Views" category) → PATCH each filter `{"DataViewId":<dv>}`. DataView detail page = `145`; URL `…/page/145?DataViewId=<dv>`.

To re-point the sheet links: Sheets `batchUpdate` → `updateCells` on `G2:H2` with `fields:"userEnteredFormat.textFormat.link"` and `userEnteredFormat.textFormat.link.uri` set (preserves cell text + other formatting).

## Helper Scripts

Node 18+.

- `scripts/week-window.mjs` — print the Monday-noon Asia/Manila window (`startISO`, `endISO`).
- `scripts/fluro-week-count.mjs --definition <def>` — count Fluro interactions in the window. Defaults to the **live** Monday-noon window (computed, same logic as `week-window.mjs`); pass `--start`/`--end` only to override. (Earlier versions had a stale hardcoded default that silently returned the prior week.)
- `scripts/rock-week-count.md` — the exact `rock_entity` MCP calls for BUILD / FAVOR DNA.
- `scripts/sheets-write-range.mjs --range "'CIW / SIGNUPS'!E179:H179" --values "19,10,21,37"` — write via Sheets API + ADC.
