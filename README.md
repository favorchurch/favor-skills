# Favor Church AI Skills (favor-skills)

This repository contains a collection of AI Agent Skills utilized by Favor Church Manila. These skills are custom instructions, workflows, and rules that guide AI assistants (Gemini CLI, Claude Code, ChatGPT, Cursor, etc.) to perform tasks following church standards.

---

## 📋 Table of Available Skills

| Skill Folder | Description |
| :--- | :--- |
| **[`speak-like-favor`](skills/speak-like-favor)** | Voice, copywriting tone, mechanical rules, formatting, and QA guidelines for drafting and editing Favor Church communications. |
| **[`attendees`](skills/attendees)** | Workflow for counting registered or checked-in attendees for events using WooCommerce/Favor Event Tickets or Fluro. |

---

## 🚀 Installation Instructions (Command Line)

To use these skills locally with agentic command-line assistants (such as Gemini CLI or Claude Code), you can install them globally or per-workspace.

### 1. Clone the repository
First, clone this repository to your local machine:
```bash
git clone git@github.com:favorchurch/favor-skills.git ~/Git/favor-skills
```

### 2. Install Globally
Copy the skills to your global agent configurations folder:
```bash
# Create the directory if it does not exist
mkdir -p ~/.gemini/skills

# Copy the skills
cp -r ~/Git/favor-skills/skills/* ~/.gemini/skills/
```

### 3. Install for a Specific Workspace
If you only want these skills active within a specific project folder, copy them to the local workspace customization directory:
```bash
# In your target project root:
mkdir -p .agents/skills

# Copy the skills
cp -r ~/Git/favor-skills/skills/* .agents/skills/
```

---

## 💬 How to Install / Ingest via Prompt (Web AI)

If you are using a web-based AI assistant (like Claude.ai, ChatGPT, or Gemini Web) and cannot use CLI-based skills, you can copy-paste the skill instructions directly into your prompt, custom instructions, or system rules.

Below are the direct markdown contents you can copy-paste:

### A. Speak Like Favor
> Use this when you want the AI to draft or QA copy in the Favor Church voice.
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
> Use this when you want the AI to understand how to check registration and check-in counts for Favor events.
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
