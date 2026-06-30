# speak-like-favor

The Favor Church Manila voice. Use it to **draft, edit, or QA** any church communication — emails, SMS, captions, invitations, web copy, announcements, volunteer updates — so it sounds warm, clear, and unmistakably Favor.

This is the core skill. Many of the conference skills lean on it to keep their email drafts on-brand.

---

## What it does

- **Drafts** new copy in Favor voice (warm, casual, confident, no Christianese).
- **Edits** existing copy to fit the voice and shorten it.
- **QAs** copy against Favor's mechanical rules: no em dashes, no `fam`, Oxford commas, `₱` currency, clean lowercase links, Favor date/time format (`July 2`, `6PM`, `9:30PM`), correct ministry capitalization, and lowercase pronouns for God/Jesus/Holy Spirit.
- Applies the right **email formatting** (scannable, bolded labels, `Much love,` closing with the right team name).

The full rule set lives in [`SKILL.md`](SKILL.md) and the extended standards in [`references/qa-guidelines.md`](references/qa-guidelines.md).

---

## Prerequisites

**None.** Pure writing and QA guidance — works in any AI assistant, web or terminal, with no MCP servers, CLI tools, or credentials. (If you ask it to actually *send* or *publish* the copy, that delivery step belongs to another skill or tool.)

---

## How to use it

- **Slash command:** `/speak-like-favor` (where installed as a command), or
- **Plain language:** just ask — "make this sound like Favor", "QA this email", "write an invite for…".

---

## Recipes

| Recipe | What it does |
|---|---|
| *"Draft a reminder email for Favor Conference in our voice."* | Produces a warm, on-brand email with correct dates, links, and the `Much love,` closing. |
| *"QA this announcement"* (paste copy) | Flags em dashes, wrong date/time format, `https://`/`www` in links, capitalization slips, and currency. |
| *"Rewrite this SMS to sound less stiff."* | Tightens and warms up the copy while keeping it short. |
| *"Write an invite: Worship Night, Favor Studio, July 5, 7PM."* | Formats the invitation block in Favor's date/venue style. |
| *"Check this caption — does it follow our God/Jesus pronoun rule?"* | Verifies theological references and lowercase pronouns. |

---

## Notes

- It will use placeholders like `[Date]`, `[Time]`, `[Venue]`, `[Link]` rather than block on missing details.
- For event details, it follows Favor's invitation order (day, date, time, then venue).

See the [root README](../README.md) for install prompts and the full skills catalog.
