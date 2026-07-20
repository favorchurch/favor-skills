# Rock weekly count (BUILD, FAVOR DNA) via read-only MCP

Use the **prod** read-only Rock MCP: `claude.ai Rock MCP (Read-only)` (`rock.favor.church`). NOT `Rock-Preview` (stale backend → returns 0). If only Preview is connected, have the user authenticate via `/mcp`.
Confirm IDs with `rock_workflow action: workflowTypes` (authoritative), not `rock_lookup quickSearch` (unreliable for workflowType IDs).
For each workflow type, call `rock_entity` with `action: "count"`, `model: "workflows"`, OData **v1** `where`:

```
WorkflowTypeId eq <ID> and CreatedDateTime ge datetime'<startISO>' and CreatedDateTime lt datetime'<endISO>'
```

where `<startISO>`/`<endISO>` come from `week-window.mjs` (e.g. `2026-06-15T12:00:00` / `2026-06-22T12:00:00`).

- **BUILD (col G)** = count(`WorkflowTypeId eq 34`) + count(`WorkflowTypeId eq 71`)
- **FAVOR DNA (col H)** = count(`WorkflowTypeId eq 30`) + count(`WorkflowTypeId eq 61`)

Notes:
- Use `ge`/`lt` and `datetime'...'` (NOT `>=` / `DateTime(...)` — that 400s on REST v1).
- `CreatedDateTime` is Asia/Manila server time, so the window strings need no tz conversion.
- Verify with `action: "search"`, `select: "Id,Name,Status,CreatedDateTime,InitiatorPersonAliasId"`, `sort: "CreatedDateTime desc"` — each row should be a distinct person's "New Form" / Completed instance.
- Exclude type 45 (Build → column I) and automation workflows (59/62/68/69/72/73/75).
