# update-sunday-signups-sheet

Update the weekly **CONNECT / SERVE / BUILD / FAVOR DNA** signup counts in the `CIW / SIGNUPS` tab of the "FAVOR SUNDAY LIVE HEADCOUNTS" Google Sheet.

All four counts now source from **Rock RMS** workflow types. CONNECT and SERVE additionally union any residual Fluro submissions during the 2026 Fluro→Rock cutover, deduped by submission timestamp so overlapping signups aren't double-counted.

---

## What it does

- Computes the current Monday-noon (Asia/Manila) reporting window and finds the target row (most recent Sunday, columns E–H still blank).
- Counts Rock RMS workflow submissions per ministry (CONNECT=type 26, SERVE=type 49, BUILD=types 34+71, FAVOR DNA=types 30+61), excluding `Status == "Delivery Failed"` junk rows.
- During the Fluro→Rock cutover, also counts residual Fluro `mnlSignUpForAConnectGroup` / `signUpToServe` submissions and dedupes them against Rock by matching timestamps.
- Writes columns **E–H** (and **A**, the Sunday date, if blank) via the Sheets API — never touches the manual `B/C/D` headcount columns or columns `I/J`.
- Verifies the write by reading the row back.

The full rule set — column→source mapping, Rock workflow type IDs, WAF gotchas, and write mechanics — lives in [`SKILL.md`](SKILL.md) and [`references/source-map.md`](references/source-map.md). Corrections and discoveries from each run are logged in [`references/learned-nuances.md`](references/learned-nuances.md).

---

## Prerequisites

- **Rock RMS Access** — read-only MCP (`rock.favor.church` prod) for counting workflow submissions, or the prod Rock REST API key for attribute-level detail / junk filtering.
- **Fluro Access** — REST token, for the residual CONNECT/SERVE union during the cutover window. Expected to trend to zero as the migration completes.
- **Google Sheets Access** — via `gcloud auth application-default` (ADC) + a quota project header, to read/write the target tab.
- **Shell & Python/Node** — the helper scripts (`scripts/`) are Python and Node 18+.

---

## How to use it

- **Slash command:** `/update-sunday-signups-sheet` (where installed as a command), or
- **Plain language:** "update Sunday signups", "update the CIW signup counts", "fill in this week's CONNECT/SERVE/BUILD/FAVOR DNA numbers".

## Recipes

| Recipe | What it does |
|---|---|
| *"Update the CIW signups sheet."* | Computes the current week's window, counts all four ministries, writes E–H (and A if blank), and verifies the write. |
| *"What were last week's Rock signup counts?"* | Runs `scripts/signups-week-count.py` with an explicit `--start`/`--end` window without writing to the sheet. |
| *"Did the Fluro→Rock cutover finish for CONNECT/SERVE?"* | Checks whether the Fluro residual count has reached zero for the current window. |

---

## Notes

- Row-2 headers carry hyperlinks to Rock DataViews (the source-of-truth links) — the skill re-reads these each run rather than trusting a cached mapping, since definitions or systems can change.
- Rock is multi-campus; the six workflow types here are Manila-only. Do not filter by person campus — filter by workflow type.
- Two Rock MCP servers may be visible in a session — only the prod, OAuth-gated one returns correct counts; a stale preview server silently returns zero.

See the [root README](../README.md) for install prompts and the full skills catalog.
