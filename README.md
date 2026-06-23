# Favor Church AI Skills (`favor-skills`)

A collection of **AI Agent Skills** used by Favor Church Manila. Each skill is a set of
custom instructions, workflows, and rules that guide AI assistants (Gemini CLI, Claude Code,
ChatGPT, Codex, Cursor, etc.) to perform tasks in line with Favor Church standards.

This repository contains **no application code** — there is nothing to build, compile, or
deploy as a service. Every skill is plain Markdown (`SKILL.md`) plus optional reference and
agent-config files. "Installing" a skill means copying its folder into an AI assistant's
skills directory, or pasting its instructions into a chat.

---

## 📋 Available skills

| Skill folder | What it does |
| :--- | :--- |
| **[`speak-like-favor`](speak-like-favor)** | Voice, copywriting tone, mechanical rules, formatting, dates/venues/capitalization conventions, and QA guidelines for drafting and editing Favor Church communications. |
| **[`attendees`](attendees)** | Workflow for counting registered or checked-in attendees for an event — checks Favor Event Tickets (WordPress/WooCommerce) first, then Fluro as a fallback. |

---

## 🧰 Tech stack

There is no runtime, package manager, or test suite. The repo is content for AI agents:

- **Format** — the [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) convention:
  each skill is a folder with a `SKILL.md` whose YAML frontmatter declares `name` and
  `description`, followed by Markdown instructions. This format is read by Claude Code,
  Gemini CLI, Codex, and similar agentic tools.
- **Languages** — Markdown (skill instructions and references) and YAML (per-agent config).
- **External services referenced by the skills** (the skills tell the agent to call these;
  the repo itself does not bundle or configure them):
  - **Favor Event Tickets MCP** — a WordPress/WooCommerce-backed MCP server. Tool:
    `mcp_favor-event-tickets_event_attendee_count`.
  - **Fluro MCP** — Favor's church-management platform. Tools:
    `mcp_fluro-mcp_attendee_rsvp`, `mcp_fluro-mcp_event_checkins`.
  - **Google Docs** — the upstream source of record for the QA guidelines (linked inside
    `speak-like-favor/references/qa-guidelines.md`).

---

## 🗂️ Repository layout

```text
favor-skills/
├── README.md                       # This file
├── speak-like-favor/
│   ├── SKILL.md                    # Main skill: Favor voice, formatting, mechanical rules
│   ├── references/
│   │   └── qa-guidelines.md        # Fuller QA standards, loaded on demand for deep QA passes
│   └── agents/
│       └── openai.yaml             # ChatGPT/Codex/API/Atlas interface + invocation policy
└── attendees/
    └── SKILL.md                    # Attendee-count workflow (Favor Event Tickets → Fluro)
```

Each top-level folder is one self-contained skill. `references/` holds material that the
skill loads only when needed (progressive disclosure), keeping the main `SKILL.md` lean.
`agents/` holds platform-specific configuration for assistants that support it.

---

## 🚀 Local install (command line)

To use these skills with agentic CLI assistants (Gemini CLI, Claude Code, etc.), install them
globally for your user or scoped to a single workspace.

### 1. Clone the repository

```bash
git clone git@github.com:favorchurch/favor-skills.git ~/Git/favor-skills
```

### 2. Install globally

Copy the skill folders into your global agent skills directory:

```bash
# Create the directory if it does not exist (example path: Gemini CLI)
mkdir -p ~/.gemini/skills

# Copy the skills
cp -r ~/Git/favor-skills/speak-like-favor ~/Git/favor-skills/attendees ~/.gemini/skills/
```

> The destination path depends on your assistant. Gemini CLI uses `~/.gemini/skills`;
> other tools use their own skills directory (e.g. `~/.claude/skills` for Claude Code).
> Adjust the target path to match the assistant you use.

### 3. Install for a single workspace

To make the skills active only inside one project, copy them into that project's local
skills directory instead:

```bash
# Run from your target project root:
mkdir -p .agents/skills
cp -r ~/Git/favor-skills/speak-like-favor ~/Git/favor-skills/attendees .agents/skills/
```

---

## ⚙️ Configuration

The repo itself needs **no environment variables or secrets**. Configuration matters only
when a skill drives an external tool:

| Skill | Requirement | How to satisfy it |
| :--- | :--- | :--- |
| `attendees` | An authenticated **Favor Event Tickets** MCP session | Run `mcp oauth login favor-event-tickets` (the skill prompts for this if the session is missing or returns an auth error). |
| `attendees` | An authenticated **Fluro** MCP session (fallback path) | Run `mcp oauth login fluro-mcp`. Re-authorization must go through the CLI's built-in OAuth flow, not another skill. |
| `speak-like-favor` | None | Pure instruction skill — no external calls. |

`speak-like-favor/agents/openai.yaml` configures how OpenAI-family assistants (ChatGPT,
Codex, the API, and Atlas) surface and auto-invoke the skill. See the inline comments in that
file for what each field controls.

---

## ✅ Validation

There is no automated test suite. A skill is "valid" when:

- Its `SKILL.md` starts with YAML frontmatter containing a `name` and a `description`.
- The instructions are accurate and the referenced tools / commands exist.

To sanity-check after editing, confirm the frontmatter parses and that any tool names or
`mcp oauth login` commands still match the live MCP servers. The most reliable validation is
to load the skill into an assistant and run it against a real request.

---

## 📦 Deployment

"Deployment" here means **distribution**, not a server release:

- **CLI assistants** — re-run the install steps above (copy the folders into the assistant's
  skills directory) whenever the skills change. There is no build step.
- **Web assistants** (Claude.ai, ChatGPT, Gemini Web) — see
  [How to install / ingest via prompt](#-how-to-install--ingest-via-prompt-web-ai) below; the
  skill text is pasted directly into custom instructions or a system prompt.
- **OpenAI-family auto-invocation** — controlled by `speak-like-favor/agents/openai.yaml`.

---

## 🤝 Contributing — dev → production

1. Branch from `main` for any change (e.g. `docs/...`, `feat/...`, `fix/...`).
2. Edit the relevant `SKILL.md` (or its `references/` file). Treat each `SKILL.md` as the
   **single source of truth** for that skill's behavior.
3. Open a pull request against `main`. The repo lives at
   [`favorchurch/favor-skills`](https://github.com/favorchurch/favor-skills).
4. Once merged to `main`, the change reaches users when they re-clone or `git pull` and
   re-copy the skill folders into their assistant's skills directory (see
   [Local install](#-local-install-command-line)).

If you change a skill's behavior, update any copy of its instructions embedded below in this
README so the two do not drift.

---

## 💬 How to install / ingest via prompt (web AI)

If you use a web-based AI assistant (Claude.ai, ChatGPT, Gemini Web) and cannot load
CLI skills, copy the skill instructions directly into your prompt, custom instructions, or
system rules.

> The snippets below are a convenience copy for pasting into chat. The **canonical, complete**
> versions live in each skill's `SKILL.md`; if the two ever differ, the `SKILL.md` wins.

### A. Speak Like Favor
> Use this when you want the AI to draft or QA copy in the Favor Church voice. Full source:
> [`speak-like-favor/SKILL.md`](speak-like-favor/SKILL.md).
<details>
<summary><b>Click to expand "Speak Like Favor" System Prompt</b></summary>

```markdown
# Speak Like Favor Voice Guidelines

Draft, edit, or QA Favor Church Manila communication so it feels warm, clear, authentic, and easy for people to act on.

## Core Voice
Write like a friendly peer and helpful thought partner. Keep copy warm, human, and concise.
- Sound casual, clear, genuine, and encouraging.
- Avoid Christianese, stiff church jargon, preachy phrasing, and overly formal wording.
- Keep invitations confident and direct. Write "Join us!", not "Please join us!".
- Prefer simple phrasing over long sentences.

## Output Format
Default to scannable email-style formatting:
- Start warm: "Hey, [Name]!"
- Use short paragraphs and bolding for key labels, dates, deadlines, venues, and action items.
- Use bullets for lists, not hyphen lists.
- End emails with:
  Much love,
  [Team Name]

## Mechanical Rules
- Use English only.
- Never use the word "fam".
- Never use an em dash (—). Use a comma, colon, semicolon, period, or parentheses instead.
- Do not start sentences with "And".
- Use the Oxford comma: "read, think, and pray".
- Use numerals for web and digital copy.
- Use "₱" for currency, for example "₱100". Use "PHP" only when the peso sign is unavailable.
- Remove "https://", "http://", and "www" from visible links unless specifically required.
- Use lowercase links unless case-sensitive (e.g. favor.church/mnl).

## Dates and Times
- Use "Jan 1", never "Jan 1st" or "1st of Jan".
- Use the full month when space allows.
- Use "AM" and "PM" with no space: "7AM", "7:15PM". Do not write "7:00PM"; write "7PM".
- For invitations, use this order:
  [Day of week], [Month] [Day], [Time]
  [Venue Name]
  Example:
  Saturday, March 8, 10AM
  Favor Studio, Shangri-La Plaza

## Names and Capitalization
- Use "Church" for the universal body of believers, and "church" for a service, building, or organization.
- Use "Connect Group" on first mention. "Connect" is acceptable after.
- Capitalize official ministries: "Favor Kids", "Favor Girl", "Favor Men", "Favor Youth", "Favor Movement", "Favor Adults", "Favor Pro", "Favor Seasoned", "Favor Business", and "Favor College".
- Do not capitalize common group names unless directly addressing them: "Favor parents and guardians", "Favor leaders".
- Use "Ps" for Pastor, with no period (e.g., "Ps James").
- Use "PS." only for postscript.

## God and Theological References
- Use lowercase pronouns for God, Jesus, and the Holy Spirit: "he", "him", "his", "you".
- Use "gospel" for the good news of Jesus, "Gospel" when referring to a book of the Bible, "Word" for Jesus, and "word" for a message/teaching.

## Venues
Use full venue names:
- Favor Studio, Shangri-La Plaza
- Favor Care, Shangri-La Plaza
- Favor Office, Shangri-La Plaza
- ICS Church, Greenfield District
- Metrotent Convention Center
- PhilSports Arena, Pasig
- Podium Hall, 6F at The Podium, Ortigas
- The Study, 4F at The Podium, Ortigas
- Valle Verde 5 Clubhouse, Pasig
- Valle Verde Country Club, Pasig
- Ynares Sports Arena, Pasig
```
</details>

### B. Attendees
> Use this when you want the AI to understand how to check registration and check-in counts
> for Favor events. Full source: [`attendees/SKILL.md`](attendees/SKILL.md).
<details>
<summary><b>Click to expand "Attendees" Workflow Prompt</b></summary>

```markdown
# Attendees Skill Workflow

Count attendees for any event by checking WooCommerce tickets first, then Fluro as a fallback.

## Workflow Steps
1. **Authenticate WooCommerce first:** The AI should check if the WooCommerce tickets server session is authenticated.
2. **Check WooCommerce (WordPress):** Query WooCommerce for ticket registrations matching the event name. If a count is returned, report it.
3. **Check Fluro (fallback):** If WooCommerce yields no match, query Fluro forms, guestlists, and mailing lists for physical RSVPs or registrations.
4. **Physical Check-ins (secondary fallback):** If no registrations are found, check physical check-in logs for physical attendance numbers.

## Reporting Output
- State the event name matched.
- Show the attendee count with the source (e.g. "via ticket registrations" or "via check-ins").
- Differentiate between registrations (tickets/RSVPs) and check-ins (people who physically arrived).
```
</details>
