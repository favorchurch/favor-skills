# Applying Favor across media and products

The same system should feel like Favor everywhere without forcing identical chrome. Choose composition and expression according to the job.

## Operate: staff/admin, RSVP, Rock, check-in

**Primary goal:** make the next action obvious, reliable, and fast.

- Masthead: clear task title, campus/event context, short section kicker.
- Controls: one primary action, calm secondary actions, obvious disabled states.
- Work surface: mostly white forms, tables and grouped rows with quiet rules.
- Filters: visible selected values, clearable filters, no hidden irreversible state.
- Feedback: recovery actions for errors, concise confirmation for success, confirmation before destructive behavior.
- Branding: signature background, Favor type hierarchy, one accent motif at most in dense working areas.
- Mobile: replace tall filter rails with sheets/disclosures; convert broad tables to prioritized columns or expandable records.

Example: a Sunday RSVP volunteer count panel should show the count and scope first, make editable overrides explicit, expose missing source data distinctly from zero, and never require hover to see the exact value.

## Insight: dashboards, executive reports, statistics

**Primary goal:** let the viewer understand the true signal and its limitations.

- Lead with a meaningful question, comparison or KPI, not a gallery of unrelated charts.
- Show exact values, labels, units, period, denominator or scope.
- Keep chart colors semantically stable within a report, with the same category order across views.
- Use a thin editorial frame and white plot surfaces; avoid texture in plotting areas.
- Make pending/unknown/missing distinct from zero. Put healthy/warning words next to colors.
- Prefer a table for exact lookup; bars for category comparison; line for trend; a single KPI for one number; funnels only for meaningful stages.
- Mobile: switch visual form rather than shrinking chart labels until unreadable.

Example: Rock executive dashboards can be atmospheric in the masthead but strict in numbers, legends, filters, and detail disclosures.

## Experience: public websites, Bible, community and ticketing flows

**Primary goal:** make the journey legible, welcoming, and memorable.

- Allow expressive hero scale, fuller motif compositions, images and intentional negative space.
- Distinguish orientation, content, action and reassurance using type size and rhythm.
- Place key call-to-action where the user expects it; avoid confusing decorative buttons.
- Keep registration, personal detail, payment and check-in controls quiet and accessible.
- Make empty, offline, pending and permission states human-readable.
- Use rich motion only when it supports context and obeys reduced-motion preferences.

Example: a Bible reading experience may have expressive on-boarding but the reading/focus state should limit ornament and prioritize text.

## Campaign: invitations, social, event posters, slides, one-pagers

**Primary goal:** land a memorable message at the intended consumption size.

1. Define one primary headline and one action/message.
2. Establish a high-contrast typographic silhouette before secondary details.
3. Pair intentional motif/art direction with the correct event identity; do not indiscriminately reuse ministry-specific creative assets.
4. Use texture as atmosphere while keeping essential dates/locations legible.
5. Preserve safe margins and text hierarchy for crops and mobile viewing.
6. Use genuine Favor logos or official event marks only from authorized assets; otherwise use a clearly marked text placeholder.
7. For decks, keep repeated grids and section identity consistent; shift scale according to projected-view readability, not just desktop-preview appearance.

Export clean variants when requested: hero, square, story, slide; preserve editability where the chosen medium supports it. Avoid generic floating mockups where the user requested the underlying design asset.

## Playful: kids, youth, celebration

- Favor Folk, Shines Paws, smileys, cutouts, scallops, scribbles can carry more visual energy.
- Keep instructions, sign-up details, child/parent information and safety actions in a readable utility typeface.
- Reserve the highest visual complexity for expressive noninteractive areas.
- Make success joyful without hiding next steps or creating motion sensitivity.

## Cross-platform component grammar

Adapt these components to the current codebase instead of insisting on literal component names:

- `Shell` / background and outer gutter
- `Masthead` / title + action + context
- `SectionHeading` / eyebrow + title + support copy
- `Card` or ruled grouping / heading + body + optional footer
- `Metric` / value + unit + time/scope
- `FilterBar` / explicit active filters and clear affordance
- `StatePanel` / loading, zero, missing, error, unauthorized, offline, success
- `DataTable` / exact lookup with mobile variant
- `ChartFrame` / legend, units, exact-value labels, source
- `Dialog` / close, escape, focus and mobile-scroll behavior

This is a design grammar, not a new dependency or library. If the app already has equivalent primitives, style them instead.

## Three meaningful design options

When asked for 3-5 concepts, change at least two structural dimensions across options (navigation, density, hierarchy, data representation, hero composition, mobile strategy), rather than presenting near-identical color variants. Describe each option's best fit and trade-off. For example:

- **Editorial command center:** strong masthead, featured statistic, stacked focus panels, clear action rail.
- **Compact operations board:** prioritized rows, dense but clean data, compact filters and direct actions.
- **Card-first mobile:** one useful number or decision per card, progressive disclosure, minimal navigation.

Choose the recommended direction based on the task, not personal aesthetics. All concepts still use the same underlying Favor tokens and behavior quality.

## Copy and communication fit

Favor visual identity does not dictate copy tone on its own. When task includes church-facing wording or event details, use authorized naming, campus terminology, service times, date formats, and links; consult any available Favor-specific communication conventions rather than inventing new ones.
