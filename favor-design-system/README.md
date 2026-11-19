# Favor Design System

Favor Church's reusable 2026 visual system for websites, dashboards, staff apps, event graphics, presentations, social posts, and design QA.

The skill adapts Favor's look to the job: functional internal tools stay practical; public experiences and campaigns can be more expressive. It includes sourced brand guidelines, portable tokens, styling, and implementation checks.

## Install

**Ask your terminal-capable AI agent:**

```text
Install the favor-design-system folder from https://github.com/favorchurch/favor-skills in my AI agent's global skills directory. Preserve SKILL.md and its agents/, assets/, and references/ folders. Confirm the skill is discoverable.
```

Alternatively, clone and copy the folder:

```bash
git clone https://github.com/favorchurch/favor-skills.git
mkdir -p ~/.claude/skills
cp -R favor-skills/favor-design-system ~/.claude/skills/
```

Use the configured skills directory of your assistant instead of `~/.claude/skills` when appropriate (for example `~/.agents/skills/` or a workspace `.agents/skills/`). In ChatGPT, upload/install the packaged skill using its Skills interface, if available. Web assistants without skills installation can follow [SKILL.md](SKILL.md) and load its referenced documents.

**Requirements:** No MCP connection is required to apply brand rules. To modify an existing app or inspect live visuals, give your agent appropriate screenshots, source code, or project access. The skill does not include proprietary Favor fonts or logos.

## Example prompts

- "Make this admin dashboard look like Favor, but preserve its data density."
- "Review this mobile layout against the Favor Design System."
- "Prototype a Favor-style event landing page with desktop and mobile layouts."
- "Use Favor visual language on this presentation without sacrificing readability."

## Contents

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Entry point, design workflow, and deliverable checklist |
| [agents/openai.yaml](agents/openai.yaml) | ChatGPT skill display metadata |
| [references/](references/) | Brand guidelines, contextual patterns, QA, source provenance |
| [assets/favor-tokens.json](assets/favor-tokens.json) | Portable design tokens |
| [assets/favor-starter.css](assets/favor-starter.css) | Optional starter CSS for projects without an established style layer |

**Provenance:** This is a sourced snapshot checked on October 13, 2026, not a complete export of the original Claude artifact. Read [source provenance](references/source-provenance.md) and prefer newer approved project assets if there is a conflict.

See the [full Favor Skills catalog](../README.md).
