# Favor Church AI Skills 🚀

A friendly, non-coder guide to installing and using **Favor Church AI Skills**.

These "skills" are custom instructions, guidelines, and workflows. They teach AI assistants (like Claude, Gemini, Cursor, ChatGPT, and Codex) how to write, format, and perform church operations exactly according to Favor Church Manila standards.

---

## ⚡ Instant Install via AI Assistant (Recommended)

If you are using a terminal-enabled AI assistant (like **Claude Code**, **Gemini CLI / Antigravity**, **Cursor**, or **Windsurf**), you don't need to run any terminal commands yourself!

Just **copy the prompt below** and paste it directly into your AI's chat box:

```text
I want to install the Favor Church AI skills as plugins/skills in my AI agent environment.
Please execute the following steps:
1. Clone the repository `https://github.com/favorchurch/favor-skills.git` to `~/Git/favor-skills` (create or update the directory if needed).
2. Install the skills (`speak-like-favor` and `attendees` folders) by copying them into the appropriate global and/or workspace-level folders for my assistant:
   - If you are Gemini CLI / Antigravity: Copy them to `~/.gemini/skills/` (global) and/or `.agents/skills/` (workspace).
   - If you are Claude Code: Copy them to `~/.claude/skills/` (global) and/or `.agents/skills/` (workspace).
   - If you are Cursor / Windsurf: Copy them to `.agents/skills/` in the workspace, or generate a `.cursorrules` file using the rules from `speak-like-favor/SKILL.md` in the workspace root.
3. Verify that the files are properly copied.
Please check if you have command execution or file system capabilities. If you do, go ahead and install these skills now!
```

---

## 💬 Use in Web AIs (ChatGPT, Claude.ai, Gemini Web)

If you are using web-based AI assistants (which cannot run commands or install plugins), you can copy and paste the rules below directly into your AI's **Custom Instructions**, **System Prompt**, or **Project Knowledge**.

### 1. Speak Like Favor Voice Rules
*(Teaches the AI our writing tone, date formats, and capitalization guidelines)*
<details>
<summary><b>Click to expand "Speak Like Favor" prompt</b></summary>

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

### 2. Event Attendee Count Workflow
*(Teaches the AI how to lookup attendee numbers)*
<details>
<summary><b>Click to expand "Attendees" workflow prompt</b></summary>

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

---

## 🛠️ Manual Installation (For Coder / Terminal Users)

If you prefer to install these files yourself via the command line:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:favorchurch/favor-skills.git ~/Git/favor-skills
   ```
2. **For Global installation (Gemini CLI / Antigravity):**
   ```bash
   mkdir -p ~/.gemini/skills
   cp -r ~/Git/favor-skills/speak-like-favor ~/Git/favor-skills/attendees ~/.gemini/skills/
   ```
3. **For Global installation (Claude Code):**
   ```bash
   mkdir -p ~/.claude/skills
   cp -r ~/Git/favor-skills/speak-like-favor ~/Git/favor-skills/attendees ~/.claude/skills/
   ```
4. **For Workspace installation (inside a specific project):**
   ```bash
   mkdir -p .agents/skills
   cp -r ~/Git/favor-skills/speak-like-favor ~/Git/favor-skills/attendees .agents/skills/
   ```

---

## 📂 Repository Layout

```text
favor-skills/
├── README.md                       # This file
├── speak-like-favor/
│   ├── SKILL.md                    # Voice & Tone Guidelines
│   ├── references/
│   │   └── qa-guidelines.md        # Extended QA standards
│   └── agents/
│       └── openai.yaml             # ChatGPT/Codex integration rules
└── attendees/
    └── SKILL.md                    # Attendee count workflow logic
```

---

## ⚙️ Configuration & Credentials

The repository itself does not store any credentials. However, some skills require specific credentials to run:

- **`speak-like-favor`**: No external connections needed.
- **`attendees`**: Requires access to the **Favor Event Tickets** and **Fluro** MCP servers.
  - The AI will prompt you to run `mcp oauth login favor-event-tickets` or `mcp oauth login fluro-mcp` if authentication is missing or expired.

---

## 🤝 Contributing

1. Create a branch from `main` (e.g. `feature/update-rules`).
2. Make your edits to the relevant `SKILL.md` (these are the single sources of truth).
3. If you change a skill's behavior, remember to also update the copy-paste prompt in this `README.md`.
4. Submit a Pull Request.
