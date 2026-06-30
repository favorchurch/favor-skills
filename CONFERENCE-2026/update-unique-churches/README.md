# update-unique-churches

Keep the **"Church Count (Normalized)"** tab of the conference attendance Google Sheet current by folding **new MASTERLIST signups** into the existing normalized list — incrementally, not a full rebuild — and recomputing the unique-church count.

---

## What it does

- **Incremental, not rebuild:** every raw church string already folded in is recorded in the row's "Merged variants" column. Only strings *not yet* captured need judgment.
- The bundled `church_recount.py` does the deterministic work (extraction, matching, recount, payload assembly); the AI supplies the judgment (classify new strings, confirm merges, decide pruning).
- Counts are recomputed for the whole table, so **cancellations (counts go down)** and additions both register.
- Writes back the data region, banner, the 30+ tab, the Cities tab, and a dated Update Log row.

Full workflow, normalization rules, and gotchas in [`SKILL.md`](SKILL.md).

---

## Prerequisites

| Capability | Type | Satisfied by | If missing |
|---|---|---|---|
| **Google Sheets Access** (as `rico@favor.church`) | Required | Composio CLI with the `googlesheets` toolkit (the commands assume Composio `GOOGLESHEETS_*`) | Confirm with `composio whoami`; the skill asks you to authenticate if not connected. |
| **Shell & Python** | Required | a terminal with Python 3 + the bundled `church_recount.py` | The recount runs in the script; it won't hand-recount. |
| **Web search / fetch** | Optional | any web tool | Verifies ambiguous or higher-count new churches; if unavailable they're marked `Unverified`. |

---

## How to use it

- **Slash command:** `/update-unique-churches`
- **Plain language:** "recount the unique churches", "add new churches from the masterlist", "how many unique churches now?"

---

## Recipes

| Recipe | What it does |
|---|---|
| `/update-unique-churches` | Folds new signups into the normalized tab, recomputes, and writes back. |
| *"How many unique churches do we have now?"* | Runs the analyze step and reports the count + net change without writing. |
| *"Add the new churches from the masterlist and show me your judgment calls."* | Classifies uncaptured strings (existing/new/drop) and surfaces the ones worth auditing. |
| *"A church dropped to 0 — is that a bug?"* | Probes the MASTERLIST; usually a real cancellation, not an error. |
| *"Strip the campus parentheticals from the old rows."* | Applies the `strip_parens` transform to legacy rows and auto-merges duplicates. |

---

## Notes

- **`H1`/`E1` are live formulas** — the skill only writes the data region and other tabs, never those cells.
- Identity = **brand + the church's own campus city**, not the attendee's residence.
- A sibling `unique-churches` skill is **stale** — prefer this one.

See the [root README](../../README.md) for install prompts and the full skills catalog.
