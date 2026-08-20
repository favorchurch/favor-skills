# Learned Nuances — CIW / SIGNUPS

Append dated discoveries after each run. Keep entries short, factual, reusable.

## 2026-08-10

- Filled **row 186 (Sun Aug 09)**: CONNECT 30, SERVE 19, BUILD 23, FAVOR DNA 28. Row was entirely empty; wrote A="Aug 09 2026" and E:H.
- **`scripts/signups-week-count.py` failed in a sandboxed `env -i` shell** (SSL cert verify failed — stripped-env urllib lost the system CA bundle) and `scripts/week-window.mjs` needed an explicit clean PATH (the default shell's `node` is an nvm-wrapped function that chokes under `env -i`, printing `_load_nvm: command not found` and eventually hitting `FUNCNEST`). Workaround: run `env -i PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin" node ...` for the window script, and fall back to the MCP `rock_entity count` path entirely (skip the Python REST helper) rather than fighting the sandboxed SSL context.
- **MCP `rock_entity count` where-clause syntax**: plain `==`/`&&` LINQ-style with `DateTime(y,m,d,h,mi,s)` constructors worked directly, e.g. `WorkflowTypeId == 34 && CreatedDateTime >= DateTime(2026,8,3,12,0,0) && CreatedDateTime < DateTime(2026,8,10,12,0,0)`. No need for OData `datetime'...'` literal syntax this run.
- One of six count calls (type 49 SERVE) hit a transient Cloudflare 502 (`origin_bad_gateway`); an immediate identical retry succeeded. Consistent with the 2026-07-27 note that transient MCP failures should just be retried once, not treated as a dead end.
- No Delivery-Failed junk in CONNECT (26) this week — raw count == filtered count == 30. Saturday variants (71 BUILD, 61 FDNA) were both 0.
- **Sheets API v4 write via curl**: do NOT combine `-G` (which forces `-d`/`--data-urlencode` onto the query string) with a JSON `-d` body in the same call — it corrupts the request ("Cannot bind query parameter"). Build the `valueInputOption=USER_ENTERED` query string directly in the URL, write the JSON body to a scratch file, and send it with `--data-binary @file` (no `-G`). Use `-G`+`--data-urlencode` only for GET reads.

## 2026-08-03 — Fluro decommissioned; Rock-only going forward

- Filled **row 185 (Sun Aug 02)**: CONNECT 40, SERVE 14, BUILD 10, FAVOR DNA 20. Row was entirely empty; wrote A="Aug 02 2026" and E:H.
- **Rico confirmed Fluro has now been fully decommissioned.** Removed the Fluro union/dedup step from `SKILL.md`, `references/source-map.md`, and `scripts/signups-week-count.py` — all four columns are Rock-only, no more per-week Fluro-residual check needed. `scripts/fluro-week-count.mjs` is retired (kept only for historical reference).
- **The `favor-connect-portal` repo (source of the Rock API key/env) has been renamed to `connect.favor.church`** at `~/Git/connect.favor.church/.env.production`. All references in this skill updated. If it moves again, search `~/Git` for `.env.production` containing `ROCK_API_KEY`.

## 2026-06-22

- First run of this skill. Filled row 179 (week Sun 2026-06-21): CONNECT 19, SERVE 10, BUILD 21, FAVOR DNA 37.
- BUILD & FAVOR DNA migrated Fluro → Rock. Fluro `mnlBuildOnline` / `mnlFavorDna` last submissions 2026-06-14, then 0. Live source is now Rock workflow types: BUILD ONLINE (34) + Saturday (71); Favor DNA (30) + Saturday (61). Saturday variants were 0 this week.
- Window validated: Mon-noon PH [Jun-15 12:00, Jun-22 12:00). Prior week (Jun 8→15) reproduced the Jun-14 row's SERVE exactly (15) and BUILD closely — confirms the boundary.
- Rock `rock_entity count` falls back to REST v1; must use OData v1 (`ge`/`lt`/`datetime'...'`).
- Each Rock workflow instance = one signup (distinct InitiatorPersonAliasId, "New Form", Completed).
- Link re-point DONE: created Rock DataViews via prod API key (`~/Git/favor-connect-portal/.env.production` → `ROCK_API_KEY`, header `Authorization-Token`). BUILD → DataView 22, FAVOR DNA → DataView 23; G2/H2 now link to `https://rock.favor.church/page/145?DataViewId=22|23`. Integer property filters encode as `["Property_WorkflowTypeId","1","<id>"]` (1=EqualTo); copy encoding from existing filters when unsure. DataView filter tree: POST root (ExpressionType 2=OR), POST children (EntityTypeId 121), POST DataView (EntityTypeId 113 Workflow, CategoryId 131), then PATCH DataViewId onto each filter. Read-only MCP can't write — must use the API key.
- The DataViews filter by workflow type only (all-time), not the weekly window — they're a "see the signups" reference; the weekly number lives in the sheet. A rolling date filter can be added later (date EntityField selection like `["Property_CreatedDateTime","256","CURRENT:-7"]`, unverified).
- The deprecated `rock-cli` skill was removed this session; use the Rock MCP instead.

## 2026-06-29

- Filled row 180 (week Sun 2026-06-28): CONNECT 8, SERVE 7, BUILD 6, FAVOR DNA 33. Saturday variants (71/61) were 0.
- Target row was entirely empty (B/C/D not yet filled by the CIW headcount team — normal on a Monday). Wrote E:H anyway; signup columns are independent of the manual headcount columns. Row 179 = prior week (Jun 21), already filled.
- **`scripts/fluro-week-count.mjs` has a STALE hardcoded default window (`2026-06-15`/`2026-06-22`).** Always pass `--start`/`--end` from `week-window.mjs` explicitly, or you'll silently get the prior week. (CONNECT 19 / SERVE 10 with no args = last week's numbers, not this week's.)
- **TWO Rock MCP servers are visible this session — pick carefully:**
  - `Rock-Preview` (no auth, always connected) returned a STALE/WRONG backend: `count WorkflowTypeId eq 34` = 0, search ignored `sort`, data appeared to cap in April, and its `quickSearch` claimed BUILD ONLINE = type 42. **Do not use it for these counts.**
  - `Rock MCP (Read-only)` (prod `rock.favor.church`) requires OAuth — user must run `/mcp` → select "claude.ai Rock MCP (Read-only)" → complete browser sign-in. This is the correct prod source.
- **`rock_lookup quickSearch` (kind workflowType) is UNRELIABLE for type IDs** — even on prod it returned id 42 for "BUILD ONLINE" (42 is actually "New People"). Use `rock_workflow action: workflowTypes` (authoritative ID↔name list) to confirm IDs instead. That list confirmed the skill's mapping: 34 BUILD ONLINE, 71 BUILD ONLINE - Saturday, 30 Favor DNA, 61 Favor DNA - Saturday.
- Query validated against prior week on prod: type 34 = 21 and type 30 = 37 for [Jun-15 12:00, Jun-22 12:00) — exactly matching row 179's recorded BUILD 21 / FAVOR DNA 37.

## 2026-07-13 — CONNECT & SERVE migrated Fluro → Rock (all four now in Rock)

- Filled **row 181 (Sun Jul 05)**: CONNECT 21, SERVE 7, BUILD 13, FAVOR DNA 18. **Row 182 (Sun Jul 12)**: CONNECT 34, SERVE 19, BUILD 19, FAVOR DNA 27. B/C/D already filled by CIW team — left untouched; A dates already present.
- **New Rock workflow types**: CONNECT = **26** "Sign up for a Connect Group!" (live from 2026-06-03); SERVE = **49** "Volunteer to Serve" (first submissions 2026-07-12). Confirmed via `rock_workflow action: workflowTypes`. Other connect-ish types (52 Connect Groups, 63 Connect, 55 Start a Connect, 76 Host A Connect) were 0 in-window — not the signup form. Do not confuse.
- **Fluro/Rock overlap resolved by TIMESTAMP matching** (Fluro `created` UTC +8h == Rock `CreatedDateTime` Manila, to the second → same signup):
  - CONNECT is **mirrored** into Rock. Jul05: Rock 21 == Fluro 21, all 21 timestamps matched → union 21 (NOT 42). Jul12: Rock 32 valid + 2 Fluro-only = 34 (only 1 of 3 Fluro matched). ⇒ take the deduped **union**, never the sum.
  - SERVE is **disjoint** (0 timestamp matches). Jul05: Rock 0 + Fluro 7 = 7. Jul12: Rock 6 + Fluro 13 = 19. ⇒ union == sum here.
  - Cutover is tapering: Fluro CONNECT dropped 21→3 across the two weeks. Keep aggregating until Fluro reliably hits 0, then go Rock-only.
- **CONNECT junk**: type 26 had 17 `Status="Delivery Failed"` empty rows (Name "New Form", no Person/connectGroup) clustered 2026-07-12 10:30–13:36 (a form glitch). Filter = **exclude `Status=="Delivery Failed"` ONLY**. ⚠️ BUILD (34) & FDNA (30) workflows are *all* legitimately named **"New Form"** — filtering by Name zeroes them (learned the hard way; the helper had this bug). SERVE rows are "New Volunteer to Serve", `Status="Active"` (never auto-complete).
- The user's rule: **count archived connect signups too** (`connectPortalArchived==True` are real). The Delivery-Failed-only filter already keeps them.
- **Manila-only**: Rock is now multi-campus (campus Id 1=Manila/MNL, 2=Brisbane, 3=Seoul, 4=Global). These six form types are Manila-scoped; verified **no BNE/SEL initiators** appear. Forms have **no campus field**; person `PrimaryCampusId` is mostly null (e.g. a clearly-Manila serve signup had null). ⇒ do NOT filter by person campus — just count the Manila form types.
- **Rock REST API** (needed beyond the MCP — MCP can't read workflow AttributeValues [404] and ignores `$sort`): key at `~/Git/favor-connect-portal/.env.production` (`ROCK_API_KEY`, `ROCK_API_URL`), header `Authorization-Token`. WAF **403s** on (a) default `Python-urllib` User-Agent → send a curl UA; (b) `%27`-encoded single quotes → keep `'` `:` `,` literal in the query string. Alias→person campus via `GET /api/People/GetByPersonAliasId/{aliasId}`. Workflow form attrs via `GET /api/Workflows/{id}?loadAttributes=simple` (Person guid, connectGroup, connectPortalArchived, Status).
- Fluro `_query` response is ~70 MB; Python `urllib` `IncompleteRead`s — fetch Fluro in **Node** (`fetch` handles it) or dump timestamps to a file.
- New one-shot helper: **`scripts/signups-week-count.py [--start … --end …]`** → all four counts (Rock + deduped Fluro union) as JSON incl. `row_values_EH`. Validated: reproduces both rows above.

## 2026-07-27

- Filled **row 184 (Sun Jul 26)**: CONNECT 33, SERVE 25, BUILD 28, FAVOR DNA 20. A/B/D already present (A="Jul 26 2026", B=1267, D=10); C left blank for CIW team; E:H confirmed empty before write.
- **`scripts/signups-week-count.py` timed out** on the Rock REST call this run (90s timeout hit) — fell back to the MCP `rock_entity count`/`search` path fully manually. Don't assume the helper always completes; have the manual fallback ready.
- **`claude.ai Rock for Favor Church` MCP (readwrite mode) intermittently 403'd** ("blocked by a firewall/security service") on the first call for 4 of 6 workflow-type count queries, while 2 succeeded — pure transience, not tied to a specific type. Simple immediate retry of the exact same call succeeded every time. Don't abandon the query on one 403; retry once.
- Workflow type 26 display name has changed from "MNL Sign up for a Connect Group!" (as of 2026-07-13) to **"GLB Sign up for a Connect Group!"** — same ID (26), same form, just re-labeled (Global?) in Rock's admin. Don't be thrown off by the name; the ID mapping (26=CONNECT, 49=SERVE, 34/71=BUILD, 30/61=FAVOR DNA) is still authoritative — verify via `rock_workflow workflowTypes` if in doubt.
- **Saturday variants (BUILD 71, FDNA 61) were non-trivial this week** (8 each) after being ~0 for weeks — both mostly `Status="Active"` (not "Completed" like their weekday counterparts) but no `Delivery Failed` junk and no "New Form" naming anomaly. Per the standing junk rule (exclude `Status=="Delivery Failed"` only), these count as-is. Don't assume Saturday = 0; check every week.
- Type 26 (CONNECT) junk this week: 37 raw rows, 4 `Status=="Delivery Failed"` (ids 5354, 5364, 5422, 5441) → valid 33. Type 49 (SERVE), 34 (BUILD), 30/61 (FDNA) had zero Delivery-Failed junk.
- Fluro residual: CONNECT (`mnlSignUpForAConnectGroup`) = 0 in-window (cutover fully tapered, 3rd week running). SERVE (`signUpToServe`) = 1 in-window (`2026-07-26T08:35:28Z`, title "MNL | Volunteer to Serve") with **no matching Rock timestamp** among the 24 Rock SERVE rows → confirmed Fluro-only/disjoint per the standing rule → SERVE total = 24 + 1 = 25.

## 2026-07-20

- Filled **row 183 (Sun Jul 19)**: CONNECT 30, SERVE 18, BUILD 27, FAVOR DNA 14. Row was entirely empty (A blank too — wrote `Jul 19 2026`); B/C/D left blank for CIW team.
- **Fluro residual finally hit 0 for both CONNECT and SERVE this week** — the tapering predicted on 2026-07-13 has completed. All four columns are now effectively Rock-only; keep checking Fluro each week but expect 0 going forward.
- Row-2 header links unchanged (E→DataView 28, F→29, G→22, H→23) — re-verified, no re-point needed.
- Spot-checked via `rock_entity count` MCP (LINQ-style `where`, not OData — the tool now accepts `WorkflowTypeId eq 34 and CreatedDateTime ge datetime'...'` directly and still works): type 34 = 22, type 49 = 18 (both matched script). Type 26 raw/unfiltered = 31 vs script's 30 (post Delivery-Failed exclusion) — consistent, 1 junk row excluded.
- **Header links re-pointed to Rock (all four).** Created Rock DataViews (same recipe as BUILD/FDNA, prod API key): CONNECT (type 26) → **DataView 28**, SERVE (type 49) → **DataView 29**. Re-pointed E2 → `…/page/145?DataViewId=28`, F2 → `…?DataViewId=29` via Sheets `batchUpdate`→`updateCells` on `E2:F2` with `fields:"userEnteredFormat.textFormat.link"` (preserves cell text/format). G2=22, H2=23 unchanged. Single-type DataViews still use a root OR filter (ExpressionType 2) + one child (`["Property_WorkflowTypeId","1","<id>"]`, EntityTypeId 121), then PATCH `DataViewId` onto both filters — mirror the BUILD template (filter 125→126/127). NB: Rock REST `batchUpdate`/heredocs — write JSON to a file and `curl --data @file` (zsh mangled an inline heredoc with a `GID` var).
