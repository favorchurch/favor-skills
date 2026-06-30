# Favor Church AI Skills 🚀

A friendly, non-coder guide to installing and using **Favor Church AI Skills**.

These "skills" are custom instructions, guidelines, and workflows. They teach AI assistants (like Claude, Gemini, Cursor, ChatGPT, and Codex) how to write, format, and perform church operations exactly according to Favor Church Manila standards.

---

## ⚡ Install via AI Assistant

Paste a prompt directly into your AI's chat. The prompts below work in three tiers — **pick the section that matches your environment.**

---

### Prompts to Install Favor Skills

Paste into any terminal-capable AI (Claude Code, Gemini CLI, Cursor, Windsurf, or a cloud instance).

#### Install Core Skill (`speak-like-favor`)

```text
Install the "speak-like-favor" folder from https://github.com/favorchurch/favor-skills into my AI agent's global skills directory, then confirm SKILL.md is present.
```

#### Install All Conference Skills

```text
Install every folder inside CONFERENCE-2026/ from https://github.com/favorchurch/favor-skills into my AI agent's global skills directory, then list the installed skill names to confirm. After installing, check each skill's Prerequisites and tell me which skills still need an MCP connection or tool I haven't set up yet. Don't block the install, just list what's missing so I know what to connect.
```

#### Uninstall All Conference Skills

```text
Remove all Favor Church conference skills from my AI agent's global skills directory.

Delete these folders:
  attendees, ticket-transfer, triage-conference, financial-assistance,
  export-attendees, resend-conference-emails-carefully-with-smtp, update-unique-churches

From:
  - Claude Code / Claude CLI: ~/.claude/skills/
  - Gemini CLI / Antigravity: ~/.gemini/skills/
  - Cursor / Windsurf: .agents/skills/ in the current workspace

List remaining skill folders after deletion to confirm.
```

---

### Install Individual Skills

Paste directly into any AI — web or terminal. Works in Claude.ai Projects and ChatGPT with browsing as persistent instructions.

> **Requirements column:** these are the *capabilities* a skill needs **to run**, not to install. Installing a skill never checks them. Each requirement is a **capability bucket** (e.g. "Gmail Draft Access"), and any one of several interchangeable tools can satisfy it — the [Configuration & Credentials](#️-configuration--credentials) section lists the tool options for each bucket. When you actually use a skill, it runs a quick preflight: if a **Required** capability has no connected tool, it explains what's missing and how to connect one, then pauses; **Optional** capabilities just produce a warning and the skill continues.

| Skill | Description | Requirements (capability buckets) | Prompt to paste |
|---|---|---|---|
| `speak-like-favor` | Favor Church Manila voice and tone — drafting, editing, and QA-ing emails, announcements, invitations, and church copy | None | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/speak-like-favor/SKILL.md and follow it as your active writing and voice guidelines for this conversation.` |
| `attendees` | Look up registered or checked-in attendee counts for any event via Favor Event Tickets or Fluro | **Event Tickets Access** (required) · **Fluro Access** (optional fallback) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/attendees/SKILL.md and follow it as your active skill instructions for looking up event attendee counts.` |
| `ticket-transfer` | End-to-end workflow for processing ticket transfer requests from the Fluro kanban, including attendee updates and confirmation emails | **Fluro Access** + **Event Tickets Access** (required) · **Gmail Draft Access** (required for emails) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/ticket-transfer/SKILL.md and follow it as your active skill instructions for handling ticket transfers.` |
| `triage-conference` | Triage the conferences@favor.church inbox, draft smart replies, and surface Favor Event Tickets action items | **Gmail Draft Access** + bundled KB (required) · **Event Tickets Access** (required for actions) · **Fluro Access** (optional) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/triage-conference/SKILL.md and follow it as your active skill instructions for conference attendee triage.` |
| `financial-assistance` | Process financial assistance applications — coupon assignment, request tracking, Gmail drafts, and Fluro kanban updates | **Fluro Access** + **Google Sheets Access** + **Gmail Draft Access** (send-as `conferences@favor.church`) (required) · **Event Tickets Access** (live prices, has fallback) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/financial-assistance/SKILL.md and follow it as your active skill instructions for handling financial assistance applications.` |
| `export-attendees` | Sync and export attendee data from Favor Event Tickets into a Google Sheets masterlist | **Event Tickets Access** + **Google Sheets Access** + **Shell & Python** (required) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/export-attendees/SKILL.md and follow it as your active skill instructions for exporting attendee lists.` |
| `resend-conference-emails-carefully-with-smtp` | Safely re-send or bulk-bump QR ticket emails to many attendees via SMTP relay without hitting Gmail's daily cap | **Event Tickets Access** + **Gmail Read Access** + **Workspace SMTP Relay** + **Shell & Python** (all required) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/resend-conference-emails-carefully-with-smtp/SKILL.md and follow it as your active skill instructions for safely resending conference emails via SMTP.` |
| `update-unique-churches` | Recount and update the unique churches represented in the conference attendance Google Sheet | **Google Sheets Access** + **Shell & Python** (required) · web search (optional) | `Fetch https://raw.githubusercontent.com/favorchurch/favor-skills/main/CONFERENCE-2026/update-unique-churches/SKILL.md and follow it as your active skill instructions for updating the unique churches count.` |

> Each skill folder also has its own **README.md** with a deeper usage guide and more recipes. Browse them in [`CONFERENCE-2026/`](CONFERENCE-2026/) and [`speak-like-favor/`](speak-like-favor/).

---

## 💬 Full Skill Content for Web AIs (Copy-Paste)

If your web AI cannot browse URLs, expand the sections below and paste the content directly.

### Speak Like Favor Voice Rules
*(Teaches the AI our writing tone, date formats, and capitalization guidelines)*
<details>
<summary><b>Click to expand</b></summary>

```markdown
# Speak Like Favor

Use this skill to draft, edit, or QA Favor Church Manila communication so it feels warm, clear, authentic, and easy for people to act on.

## Core Voice

Write like a friendly peer and helpful thought partner. Keep copy warm, human, and concise.

- Sound casual, clear, genuine, and encouraging.
- Avoid Christianese, stiff church jargon, preachy phrasing, and overly formal wording.
- Keep invitations confident and direct. Write `Join us!`, not `Please join us!`.
- Prefer simple phrasing over long sentences that do not connect.
- For visitors and public copy, make the message friendly, non-threatening, and easy to understand.
- For leaders and volunteers, sound clear, motivating, understanding, and team-oriented. Prefer `we` when it feels natural.
- For correction or sensitive copy, be truthful, patient, non-judgmental, and kind.

## Output Format

Default to scannable email-style formatting unless the user asks for another format.

- Start warm: `Hey, [Name]!`
- Use short paragraphs.
- Use bolding for key labels, dates, deadlines, venues, and action items.
- Use bullets for lists, not hyphen lists, unless a numbered sequence is clearer.
- End emails with:

```text
Much love,
XXX Team
```

Replace `XXX Team` with the relevant team, for example `Favor Conference Team`.

## Mechanical Rules

Apply these rules strictly when drafting or editing.

- Use English only.
- Never use the word `fam`.
- Never use an em dash. Use a comma, colon, semicolon, period, or parentheses instead.
- Do not start sentences with `And`.
- Use the Oxford comma: `read, think, and pray`.
- Use numerals for web and digital copy.
- Use `₱` for currency, for example `₱100`. Use `PHP` only when the peso sign is unavailable.
- Remove `https://`, `http://`, and `www` from visible links unless a platform specifically requires the full URL.
- Use lowercase links unless case-sensitive, for example `favor.church/mnl`.
- If a long public link will be used long-term, suggest a `favor.church` shortlink. For temporary internal links, `tinyurl.com` or `bit.ly` is acceptable.

## Dates and Times

Use Favor date and time formatting.

- Use `Jan 1`, never `Jan 1st` or `1st of Jan`.
- Use the full month when space allows.
- Use `AM` and `PM` with no space: `7AM`, `7:15PM`.
- Do not write `7:00PM`; write `7PM`.
- For invitations, use this order:

```text
Saturday, March 8, 10AM
Favor Studio, Shangri-La Plaza
```

## Names, Ministry Terms, and Capitalization

Apply Favor-specific terms carefully.

- Use `Church` for the universal body of believers.
- Use `church` for a service, building, or organization.
- Use `Connect Group` on first mention. `Connect` is acceptable after the first mention.
- Capitalize official ministries and communities: `Favor Kids`, `Favor Girl`, `Favor Men`, `Favor Youth`, `Favor Movement`, `Favor Adults`, `Favor Pro`, `Favor Seasoned`, `Favor Business`, and `Favor College`.
- Use `Favor Girl`, not `Favor Girls`, unless quoting existing approved copy that intentionally uses another form.
- Do not capitalize common group names unless directly addressing them: `Favor parents and guardians`, `Favor leaders`, `Connect Group leader`.
- When addressing groups directly, capitalization may be appropriate, for example `Hey, Connect Leaders!`.
- Use `Ps` for Pastor, with no period. When unsure, use the full title, for example `Pastors James and Kate Aiton`.
- Use `PS.` only for postscript.

## God, Jesus, Bible, and Theological References

Keep language clear and theologically careful without sounding heavy.

- Use lowercase pronouns for God, Jesus, and the Holy Spirit: `he`, `him`, `his`, `you`.
- If referring to God, Jesus, or the Holy Spirit in captions, use the name first, then lowercase pronouns after.
- Check basic theological accuracy. Do not refer to Jesus as the Father, or say the Father died for our sins.
- Use `gospel` for the good news of Jesus.
- Use `Gospel` when referring to a book of the Bible, for example `Gospel of John`.
- Use `Word` when referring to Jesus as the Word made flesh.
- Use `word` for a message, teaching, or spoken word from God.
- Bible references do not need parentheses. Examples: `Matt 10:28 NIV`, `Matthew 10:28 NIV`.

## Venues

Use full venue names.

- `Favor Studio, Shangri-La Plaza`
- `Favor Care, Shangri-La Plaza`
- `Favor Office, Shangri-La Plaza`
- `ICS Church, Greenfield District`
- `Metrotent Convention Center`
- `PhilSports Arena, Pasig`
- `Podium Hall, 6F at The Podium, Ortigas`
- `The Study, 4F at The Podium, Ortigas`
- `Valle Verde 5 Clubhouse, Pasig`
- `Valle Verde Country Club, Pasig`
- `Ynares Sports Arena, Pasig`

## Drafting Workflow

When creating or editing copy:

1. Identify the audience, channel, and action needed.
2. Apply Favor voice first, then shorten and clarify.
3. Check formatting, dates, times, links, venues, capitalization, currency, and theological references.
4. For emails, add the required `Much love,` team closing unless the user asks otherwise.
5. If key details are missing but the task can still be completed, use clear placeholders like `[Date]`, `[Time]`, `[Venue]`, and `[Link]` rather than blocking.
6. Before any tool calls for a multi-step task, send a short user-visible update that acknowledges the request and states the first step.

## QA Checklist

Before finalizing, scan for:

- No em dashes.
- No sentence starts with `And`.
- No use of `fam`.
- No unnecessary `please` in invitations.
- No Christianese or insider-only phrasing.
- Dates and times follow Favor format.
- Links have no `https://`, `http://`, or `www` in visible text.
- Venue names are complete.
- Official group names are capitalized correctly.
- God/Jesus/Holy Spirit pronouns are lowercase.
- Email closing uses `Much love,` and the right team name.
```

</details>

### Attendees Workflow
*(Teaches the AI how to look up attendee numbers)*
<details>
<summary><b>Click to expand</b></summary>

```markdown
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
```

</details>

---

## 🍳 Prompt Recipes

Each skill works two ways: type its **slash command** (e.g. `/attendees ...`) where skills are installed as commands (Claude Code, Codex, and similar), or just **ask in plain language** anywhere — the skill triggers on intent. The recipes below show the slash form; the italic plain-English version works too.

> Recipes only run the steps your connected tools allow. If a skill needs a capability you haven't connected yet (see the [Requirements column](#install-individual-skills)), it explains what's missing and how to connect it before doing anything risky.

### Single-skill recipes

| # | Recipe | What it does |
|---|---|---|
| 1 | `/attendees favor conference 2026` | Counts registered attendees for Favor Conference 2026 — checks Favor Event Tickets first, falls back to Fluro. |
| 2 | `/attendees worship night` *("how many RSVP'd for worship night?")* | Looks up an internal / non-ticketed event's RSVP or check-in count via Fluro. |
| 3 | `/triage-conference` *("check the conference inbox")* | Fetches unread mail at conferences@favor.church, matches each to the knowledge base, and drafts Favor-voice replies. |
| 4 | `/ticket-transfer` *("process the ticket transfers")* | Pulls new and pending transfer requests, matches attendee records, then (after your go-signal) updates tickets and drafts confirmation emails. |
| 5 | `/financial-assistance check FC26` *("review the new financial aid requests")* | Dry run: reads new requests, computes exact discounts from live ticket prices, and reports — no writes. |
| 6 | `/financial-assistance process new requests` | Full pipeline: updates the tracker, assigns exact-tier coupon codes, and drafts emails. Sends only after you approve. |
| 7 | `/export-attendees worship conference 2026` *("sync the attendee list to the sheet")* | Exports the full attendee CSV into the Google Sheets masterlist and stamps the "Last Updated" cell. |
| 8 | *"export the attendees again"* / *"re-export"* | Re-runs the last export against the same sheet and event. |
| 9 | `/update-unique-churches` *("recount the unique churches")* | Folds new MASTERLIST signups into the normalized church-count tab and recomputes — additions and cancellations both register. |
| 10 | *"how many unique churches do we have now?"* | Runs the recount's analyze step and reports the current unique count plus the net change. |
| 11 | `/resend-conference-emails-carefully-with-smtp bump the QR tickets for FC26` | Validates every recipient against active tickets, warms up ~25, then bulk-bumps ticket emails via SMTP relay. Resumable and safe. |
| 12 | *"draft a reminder email for Favor Conference in our voice"* | `speak-like-favor` writes a warm, on-brand email with correct dates, links, and closing. |
| 13 | *"QA this announcement"* (paste your copy) | `speak-like-favor` checks for em dashes, date and time format, link styling, capitalization, and currency. |

### Combo recipes (chaining skills)

| # | Recipe | What it does |
|---|---|---|
| 14 | *"Count Favor Conference 2026 attendees, then sync the full list to the masterlist."* | `attendees` for the headcount, then `export-attendees` to push every row into Sheets. |
| 15 | *"Triage the conference inbox, then bump everyone who never got their QR ticket before the event."* | `triage-conference` surfaces delivery issues, then `resend-conference-emails-carefully-with-smtp` resurfaces tickets safely. |
| 16 | *"Process the new financial aid requests and make sure the coupon emails sound like Favor."* | `financial-assistance` computes discounts and drafts, with `speak-like-favor` voice applied to every draft. |
| 17 | *"Run the ticket transfers, then re-check the Favor Conference headcount."* | `ticket-transfer` updates attendee records, then `attendees` confirms the count. |
| 18 | *"Sync the attendee masterlist, then recount the unique churches."* | `export-attendees` refreshes MASTERLIST, then `update-unique-churches` folds the new signups into the church count. |

---

## 🛠️ Manual Installation (Terminal Users)

**With git (recommended):**

```bash
git clone https://github.com/favorchurch/favor-skills.git /tmp/favor-skills

# Claude Code — core + all conference skills
mkdir -p ~/.claude/skills
cp -r /tmp/favor-skills/speak-like-favor ~/.claude/skills/
cp -r /tmp/favor-skills/CONFERENCE-2026/. ~/.claude/skills/

# Gemini CLI — core + all conference skills
mkdir -p ~/.gemini/skills
cp -r /tmp/favor-skills/speak-like-favor ~/.gemini/skills/
cp -r /tmp/favor-skills/CONFERENCE-2026/. ~/.gemini/skills/

# Workspace (Cursor / Windsurf / any project)
mkdir -p .agents/skills
cp -r /tmp/favor-skills/speak-like-favor .agents/skills/
cp -r /tmp/favor-skills/CONFERENCE-2026/. .agents/skills/
```

**Without git (curl + unzip):**

```bash
curl -L https://github.com/favorchurch/favor-skills/archive/refs/heads/main.zip \
     -o /tmp/favor-skills.zip
unzip -q -o /tmp/favor-skills.zip -d /tmp/favor-skills-extract

# Claude Code — core + all conference skills
mkdir -p ~/.claude/skills
cp -r /tmp/favor-skills-extract/favor-skills-main/speak-like-favor ~/.claude/skills/
cp -r /tmp/favor-skills-extract/favor-skills-main/CONFERENCE-2026/. ~/.claude/skills/
```


---

## 📂 Repository Layout

Every skill folder has a `SKILL.md` (the source of truth the AI follows) and a `README.md` (a human-friendly usage guide with recipes).

```text
favor-skills/
├── README.md                       # This file
├── speak-like-favor/
│   ├── SKILL.md                    # Voice & tone guidelines
│   ├── README.md                   # Usage guide + recipes
│   ├── references/
│   │   └── qa-guidelines.md        # Extended QA standards
│   └── agents/
│       └── openai.yaml             # ChatGPT/Codex integration rules
└── CONFERENCE-2026/                # Conference-specific operation skills
    ├── attendees/
    │   ├── SKILL.md                # Attendee count workflow logic
    │   ├── README.md               # Usage guide + recipes
    │   └── agents/
    │       └── openai.yaml         # ChatGPT/Codex integration rules
    ├── ticket-transfer/
    │   ├── SKILL.md                # Transfer tickets between attendees
    │   └── README.md
    ├── triage-conference/
    │   ├── SKILL.md                # Conference attendee triage workflow
    │   ├── README.md
    │   └── references/
    │       └── conference-kb.md    # Conference knowledge base
    ├── financial-assistance/
    │   ├── SKILL.md                # Financial assistance application handling
    │   └── README.md
    ├── export-attendees/
    │   ├── SKILL.md                # Export attendee lists to Sheets
    │   └── README.md
    ├── resend-conference-emails-carefully-with-smtp/
    │   ├── SKILL.md                # Safe bulk email re-send workflow
    │   ├── README.md
    │   └── scripts/                # Python SMTP helper scripts
    └── update-unique-churches/
        ├── SKILL.md                # Update unique church count tracker
        ├── README.md
        └── church_recount.py       # Church recount utility script
```

---

## ⚙️ Configuration & Credentials

This repo stores **no credentials**. Skills only need connections when you *run* them, not when you install them. Each requirement is a **capability bucket** — a thing the skill needs to do (like "draft an email") — and any one of several interchangeable tools can satisfy it. Connect whichever tool you already use.

### Capability buckets

| Capability bucket | What it's for | Satisfied by any one of |
|---|---|---|
| **Gmail Draft Access** | Read a Favor mailbox and create/send drafts (with the right sender, e.g. `conferences@favor.church`) | Gmail MCP · Composio Gmail (`GMAIL_*`) · `gws` CLI · any send-as-capable Gmail CLI/MCP |
| **Gmail Read Access** | Read/enumerate a mailbox (no sending) | Composio Gmail · `gws` CLI (with read scope) · Gmail MCP |
| **Event Tickets Access** | Read/update attendees, orders, tickets, and events (WordPress/WooCommerce) | Favor Event Tickets MCP *(for ticket prices only, the public event page is a manual fallback)* |
| **Fluro Access** | Read kanban boards, form submissions, and contacts; write tags and card moves | Fluro for Favor Church MCP |
| **Google Sheets Access** | Read and write spreadsheet values | Composio (`GOOGLESHEETS_*`) · `gws` CLI · Google Sheets MCP |
| **Workspace SMTP Relay** | Send high volumes of email past Gmail's daily API cap | Google Workspace SMTP relay (`smtp-relay.gmail.com:587`) + an app password |
| **Shell & Python** | Run helper scripts and download CSVs | A terminal with `bash`, `curl`, and Python 3 |

### Which skill needs what

| Skill | Required | Optional |
|---|---|---|
| `speak-like-favor` | — (none) | — |
| `attendees` | Event Tickets Access | Fluro Access (fallback) |
| `ticket-transfer` | Fluro Access · Event Tickets Access · Gmail Draft Access (for emails) | — |
| `triage-conference` | Gmail Draft Access · Event Tickets Access (for actions) | Fluro Access |
| `financial-assistance` | Fluro Access · Google Sheets Access · Gmail Draft Access | Event Tickets Access (has event-page fallback) |
| `export-attendees` | Event Tickets Access · Google Sheets Access · Shell & Python | — |
| `resend-conference-emails-carefully-with-smtp` | Event Tickets Access · Gmail Read Access · Workspace SMTP Relay · Shell & Python | — |
| `update-unique-churches` | Google Sheets Access · Shell & Python | Web search |

If a **Required** capability has no connected tool when you run a skill, the skill explains what's missing and how to connect one of the options, then pauses (it never fakes results). **Optional** capabilities just produce a heads-up and the skill keeps going. For MCP servers, the AI will typically prompt you to run something like `mcp oauth login favor-event-tickets` or `mcp oauth login fluro-mcp`.

---

## 🤝 Contributing

1. Create a branch from `main` (e.g. `feature/update-rules`).
2. Make your edits to the relevant `SKILL.md` (these are the single sources of truth).
3. If you change a skill's behavior, also update its folder `README.md`, the copy-paste prompt, and the Requirements/recipes in this `README.md`.
4. Submit a Pull Request.
