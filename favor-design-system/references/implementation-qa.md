# Implementation and QA for Favor-aligned UI

## Before coding

1. Inspect the existing framework, component library, styling strategy, navigation and app states.
2. Determine which context applies (operate, insight, experience, campaign, playful).
3. If the actual Favor design source, existing stylesheet or approved asset manifest is accessible, read it first. Do not add a second competing design token layer by accident.
4. Prefer the linked artifact's public-facing composition conventions for new public/site work. Favor dashboards may use stricter, product-specific UI variants.
5. Keep existing authorization, data processing and business logic intact. Styling is not permission to widen access or move protected data to the client.

## Mapping tokens

Use semantic CSS variables. The optional `assets/favor-starter.css` demonstrates a minimal interoperable layer. Map its vars to existing Tailwind, CSS Modules, Sass, React, Vue, or plain CSS rather than replacing the project's entire design system.

For exact brand work, the five core variables are:

```css
--fv-ink: #121411;
--fv-paper: #fef1e8;
--fv-orange: #f45500;
--fv-blue: #007fae;
--fv-yellow: #ffb42a;
```

Supporting UI/dashboards can use `--fv-surface`, `--fv-rule`, `--fv-muted`, `--fv-focus` and semantic states. Keep raw hex definitions central.

## Interactions and states

Explicitly cover applicable states: loading, ready, zero/none, unknown/missing, pending, filtered-empty, error, unauthorized, offline/degraded, success and destructive-confirmation.

- A clickable-looking affordance must have a real action. Otherwise render it disabled or non-interactive with an explanation.
- Clearly differentiate unknown (`not available`) from actual zero (`0`).
- Prefer native links, buttons, inputs and selects; ensure visible labels and keyboard semantics.
- Modal/sheet: explicit close control, Escape support, managed focus, working internal scroll, no hidden bottom actions.
- Active filter and scope must be visible; clearing filters should be straightforward.
- Reduce animation when `prefers-reduced-motion` is active. The brand default is a subtle 160ms color transition, not bouncy entrance effects.

## Typography and color validation

- Use licensed Favor faces only from authorized project assets. When absent, gracefully fall back rather than claiming visual equivalence.
- Keep public titles short/lowercase/period-ended when appropriate; body copy sentence-case. Preserve actual content semantics and proper names.
- Check contrast on actual backgrounds (normally at least 4.5:1 for body text, 3:1 for large text/UI boundaries).
- The artifact's paper-on-blue color pairing is only about 4.08:1, so it is not safe for ordinary small text without adjustment.
- Use ink on orange instead of white on orange for body-sized primary buttons when practical.
- Decorative script/cutout font is never the default for form instructions, charts, error messages or legal text.

## Mobile and accessibility verification

Test at a narrow phone width (about 390 CSS px, and 320px where feasible), a middle viewport (~768-1024px), and a wide desktop. Verify:

- No accidental page-level horizontal overflow.
- Buttons/forms remain comfortably targetable (44x44 CSS px for primary touch actions where practical).
- Long campus names, service times, currency figures and numbers wrap or truncate intentionally.
- Heading hierarchy, contrast, focus order and screen reader names remain correct.
- Tables become prioritized rows/details or deliberately scrollable tables with preserved column context.
- Charts have exact readable numbers/labels, not hover-only values; data categories stay stable.
- Keyboard-only interaction, dialog close/return focus, scroll locks and error recovery work.
- Status semantics remain clear with color removed.
- Texture does not impair reading or chart interpretation.
- Print/export captures required text without clipping.

## Code review checklist

- [ ] Matches the selected Favor context and existing stack
- [ ] Uses the actual brand token source (or documents a verified fallback)
- [ ] No fabricated font binaries, official marks, or unlicensed assets
- [ ] Correct source-precedence and no accidental token duplicates
- [ ] Brand typography, lowercase labels, and punctuation used appropriately
- [ ] No gradients or unnecessary motion in default broad-brand surfaces
- [ ] One meaningful accent per section; paper/ink remains foundational
- [ ] Major states and interactions behave as advertised
- [ ] Contrast, keyboard, reduced-motion and mobile verified
- [ ] Screenshots at representative widths checked when browser tools exist
- [ ] Changed files and tests are summarized, with unverified areas disclosed

## Expected outputs by task

- **Design specification:** page hierarchy, component structure, responsive layouts, 5 core tokens, typography roles, asset needs, state matrix, acceptance criteria.
- **Prototype:** realistic visible content, interactions that work or are explicitly marked simulated, both mobile/desktop treatment where relevant.
- **Implementation:** working source within the current app and verification notes; no unrelated architecture rewrite.
- **Review:** concrete screen-anchored findings, severity, fix path and distinction between required correction versus optional brand expression.
- **Graphic/deck:** final visual deliverable at the requested dimensions/editability with intentional hierarchy and licensing disclosures as needed.
