---
name: favor-design-system
description: Apply the Favor Church 2026 visual design system to create, critique, revise, prototype, or implement on-brand interfaces and visual assets. Use whenever the user says "Favor Design System", "make it look like Favor", "Favor Church brand", or asks for Favor-aligned web/apps, dashboards, admin tools, mobile views, UI components, event graphics, one-pagers, social creatives, charts, decks, or design reviews. Establish canonical colors, typography roles, texture and icon treatment, layout patterns, responsive behavior, and accessibility; respect existing application code and current source assets. Do not use for unrelated brands or tasks involving only prose unless visual styling is requested.
---

# Favor Design System

Make work recognizably Favor Church while keeping it functional, accessible, and fit for its audience. This is a reusable design decision system, not a command to make every screen look like a dashboard or to color generic UI orange.

## Source of truth

1. Read [claude-artifact.md](references/claude-artifact.md) for the linked design system's observed visual rules, layout dimensions, typography and components.
2. Read [brand-core.md](references/brand-core.md) for repo-verified tokens, asset policies, and context-specific extensions.
3. For layouts, prototypes, art direction, or visual assets, consult [application-patterns.md](references/application-patterns.md).
4. For implemented web/app UI or audits, consult [implementation-qa.md](references/implementation-qa.md).
5. For provenance and refresh, consult [source-provenance.md](references/source-provenance.md).
6. Reuse `assets/favor-tokens.json` for portable tokens and `assets/favor-starter.css` only as a starter where the project has no established style layer.

The linked Claude artifact is titled `Favor Church 2026`. Its rendered metadata exposed specific design-system rules, although a complete file/component export was not available. These rules and the canonical `favorchurch/rock-dashboards` tokens were checked on 2026-10-13. Do not claim this skill contains the original proprietary fonts, full asset library, or original component source.

## Decision process

1. Identify the deliverable: critique, design specification, visual prototype, rendered creative, presentation, existing-code implementation, or design-system extension.
2. Identify the context:
   - **Operate**: staff/admin portals, check-in, data entry, system controls. Clarity and error prevention dominate.
   - **Insight**: reports, charts, executive dashboards, metrics. Exact values and comparisons dominate.
   - **Experience**: public-facing websites, event registration, Bible/community apps. Emotion and journey can be more expressive.
   - **Campaign**: social posts, invites, event visuals, decks, posters. Bold typography, texture, and motifs can lead.
   - **Playful**: Kids, youth, celebrations. More expressive graphic vocabulary; controls stay readable.
3. Inspect the actual input first: screenshot, existing site, repository, deck, brief, or source asset. Distinguish confirmed brand assets from inferences. If the user provides an existing design-system export, prioritize it and document conflicts.
4. Use Favor brand tokens semantically. Select type roles before sizes and layout structure before decoration. Never invent official colors, fonts, logos, or component names.
5. Preserve the user's intended medium and stack. A React page stays React; an editable deck remains a deck; a graphic request yields a graphic, not an unsolicited code mockup.
6. Solve desktop and mobile deliberately. Specify or implement critical states and interactions, not only the default static view.
7. Review visual quality, functional affordances, contrast, accessibility, asset provenance, and output requirements before delivering.

## Visual invariants

- Ground the system in paper `#FEF1E8`, ink `#121411`, orange `#F45500`, blue `#007FAE`, and yellow `#FFB42A`; use white surfaces only where the context calls for clear utility/data areas.
- For broad-brand/public work, use one accent color per section, full-bleed flat brand-tone bands and generous paper areas. Avoid gradients.
- Typography is role-based: Favorvetica for true display moments, Favor Headline for condensed poster/date impact, Helvetica Neue/Arial for public body, PP Right Grotesk Mono for dates/meta, Perfectly Nineties for scripture; Favor Sans remains a valid project-specific UI face.
- The artifact specifies lowercase public titles/buttons/nav/pills/eyebrows, short title lines ending in a period, sentence-case body, and brief verb-first actions. Preserve proper nouns and clarity.
- Favor's handmade motifs (bursts, waves, scallops, scribbles, sparks, flowers, stars) add personality. Never substitute a decorative motif for a functional icon whose meaning must be obvious.
- Prefer editorial composition, tangible paper/print texture, clear rules, warmth, and intentional contrast over generic shadow-heavy SaaS gloss. Use minimal color transitions (~160ms) rather than bounces or decorative entrance animation.
- Keep textures around or behind expressive sections; never under dense tables, charts, or tiny text.
- Distinguish unknown/missing from a true zero; status meaning must survive without color.
- Keep primary actions obvious, controls usable, touch targets generous, and focus visible. Do not ship decorative-looking dead controls.
- Use approved assets from the project or canonical repository. Never embed or redistribute proprietary Favor font binaries from a connected repo in a packaged skill.

## Task branches

### Create or redesign

State the surface's job in one sentence. Determine audience, hierarchy, key actions, density, and viewing environment. Establish a coherent composition with Favor tokens and typography. Apply at most one or two strong motifs to operational pages; allow more expression in campaigns. Show multiple approaches only when requested or clearly valuable, differentiating **structure** rather than merely shifting colors. Present a recommended option and explain its trade-offs.

### Prototype

Make the result sufficiently faithful for a meaningful design decision: realistic sample copy, actual expected value formats, named states, clear interactions, and deliberate mobile behavior. If requested functionality is not supported by the output medium, say what is a simulation. When possible, compare mobile and desktop variants using the same components and tokens.

### Implement

Inspect the existing codebase and component system. Reuse current design primitives. Centralize variables, avoid raw hex values in every component, preserve data/auth boundaries, and implement responsive behavior from the smallest viewport. Respect existing dependency and routing choices. Verify using tests and visual review when tools permit; report what was and was not verified.

### Critique or audit

Report specific problems and fixes in priority order: usability/accessibility, content and data semantics, structural hierarchy, Favor alignment, optional flourishes. Do not present mere personal taste as an invariant. When the user requests a fix, implement it if the applicable tools and access are available.

### Brand graphics or slides

Select the correct campaign/context treatment, establish one clear primary message, favor hierarchy/contrast over decorative accumulation, and use authentic logos/imagery only when provided or accessible. Keep body copy readable at the final consumption size. For editing work, preserve editability where requested. If actual logo or font assets are unavailable, use a clearly identified placeholder or safe text treatment rather than fabricated marks.

## Deliverable contract

Give a usable result in the requested format, not just an aesthetic description. For design specs, include responsive hierarchy, components, key states, tokens, and behavior. For code, deliver working source and report verification. For reviews, tie each finding to the actual artifact and recommended repair. Mention material unknowns, especially asset and source limitations, without derailing straightforward work.
