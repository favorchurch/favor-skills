# Linked Favor Church 2026 design system - extracted guidance

The user-supplied Claude artifact is titled "Favor Church 2026". These design rules were extracted from its publicly shared rendered artifact on 2026-10-13. The complete project file table, font binaries, assets, and implementation source were not exported, so treat this as an evidenced semantic extraction, not a byte-for-byte migration. See [source-provenance.md](source-provenance.md) for precedence and refresh rules.

## Overall visual direction

"Warm, human and handmade" and "flat print on paper, ink type, one or two loud brand colours" are the governing motifs.

- Stack full-bleed, flat brand-tone bands vertically. Do not add gradients by default.
- Leave generous paper areas. Use **one accent color per section** rather than every accent in every section.
- Express texture with grain, photocopy, specks, paper and dust overlays. Keep live text and controls readable.
- Make designs feel welcoming, informal, and editorial rather than corporate-glossy.
- Use minimal motion: color transition `160ms cubic-bezier(0.2, 0.7, 0.2, 1)` as the default. No bouncing or decorative entrance animations.

## Five core colors

| Artifact name | Value | Guidance |
| --- | --- | --- |
| `fv-ink` | `#121411` | ink, body and display text |
| `fv-paper` | `#FEF1E8` | single official cream/paper ground |
| `fv-orange` | `#F45500` | energetic first accent |
| `fv-blue` | `#007FAE` | secondary bright accent |
| `fv-yellow` | `#FFB42A` | bright supporting accent |

Source-presented pairings: ink on paper/orange/yellow; paper on ink/blue. However, independent WCAG contrast calculation shows paper-on-blue is about **4.08:1**, insufficient for normal-size AA text (4.5:1), though sufficient for large text (3:1). Use large display type on that pairing or an accessible darker blue text-surface adaptation for smaller type. Avoid white-on-orange for normal text. The additional semantic colors from the dashboard repository belong in product/UI data applications, not as replacements for the five brand hues.

## Layout measures

- Broad container: **1200px** max-width.
- Narrow reading/content container: **760px** max-width.
- Outer gutters: **24px** as a starting point, reducing only for small viewport practicality.
- Spacing system: multiples of **4px**.
- Section vertical padding: **64px**, reduced to **32px** in the documented medium/compact responsive treatment.
- Prefer stacked bands and comfortable negative space. Avoid assuming these container measures must be imposed on existing complex admin applications.

## Language, punctuation, and UI labeling

- Tone: friendly and direct, like a peer; warm, plain-spoken, hospitable.
- Use concrete invitation and reassurance: "Coffee is on us." rather than a vague claim.
- Avoid insider jargon on public-facing surfaces when clear everyday language exists.
- **Lowercase** for public-site titles, buttons, pills, nav links and eyebrows.
- Keep titles short and end them with a period. Where using the artifact's `Heading`, `Hero`, or `Section` components, use their `period` behavior instead of manually typing a duplicate full stop.
- Body text uses ordinary sentence case. Preserve proper nouns, accessibility labels, official event titles, and existing product terms when needed.
- Button labels: verb-first, usually 2-3 words: `plan a visit`, `watch live`, `save my seat`, `give online`.

Apply these rules especially to public-site, campaign, and experience contexts. For a dense internal system, do not sacrifice conventional clarity, screen-reader naming, or domain terminology solely to enforce decorative casing.

## Type specimens and roles

These sizes are **observed artifact specimens**, not a universal responsive type scale to paste into every app.

| Family | Observed sample | Role |
| --- | --- | --- |
| Favorvetica Bold | `84px / 0.92`, tracking `-0.035em` | hero display |
| Favor Headline Regular | `64px / 1` | condensed poster/date blocks |
| Helvetica Neue Regular / Arial fallback | `16px / 1.5` | body copy |
| Favor Sans Regular/Bold | `28px / 1.5` | branded sans display and support |
| Perfectly Nineties | `40px / 1.1` | scripture/serif moment |
| PP Right Grotesk Mono | `24px / 1.45` | mono display/date |
| PP Right Grotesk Mono | `14px / 1.45` | meta, dates, eyebrows |
| Shines Paws | `34px / 1.1` | handmade attribution/tagline |
| Maows Hand | `34px / 1.1` | handwritten caps |
| Marked | `34px / 1.1` | stamped accent |
| Favor Folk | `34px / 1.1` | folk expressive accent |
| Favor Cutout | `34px / 1.1` | cutout display accent |
| Folkies Vantage Script | `34px / 1.1` | script accent |

Favor's dashboard code also uses Favor Sans for UI/body in some products. For a new broad-brand or public experience, prioritize the artifact's Helvetica Neue/Arial utility copy; for an existing product, preserve its established Favor Sans typography contract unless the user requests migration.

**Asset rule:** These names specify typography roles only. The skill contains no font files. Do not redistribute or forge a proprietary font.

## Named component vocabulary

The extracted artifact lists 18 component families:

`Button`, `Card`, `EventCard`, `Footer`, `Heading`, `Hero`, `Logo`, `NavBar`, `Quote`, `Section`, `SermonCard`, `Shape`, `Sticker`, `Surface`, `Tag`, `Text`, `TextField`, `TypeWall`.

Known behavior from rendered guidance:

- `Button`: solid, outline, ghost; size/icon variants and disabled state. Verbal labels stay short and action-led.
- `Heading`, `Hero`, `Section`: handle optional trailing-period behavior in their original design components.
- `EventCard`, `SermonCard`, `Card`: subject-specific and generic content groupings.
- `NavBar`, `Footer`: site-level navigation and closing wayfinding.
- `Quote`: scripture, quotations and testimonials, keeping source legible.
- `Tag`, `Sticker`: categories and handmade visual punctuators; treat functional statuses separately.
- `Logo`: official Favor/ministry marks, not generative logo approximations.
- `Shape`: ornamental shapes. The artifact names 11 guide shapes: `globe`, `rounded-column`, `scribble-01` to `scribble-03`, `smiley-01` and `smiley-02`, `squiggly`, `waves`, `wavy-01` and `wavy-02`.
- `Surface`, `Text`, `TextField`, `TypeWall`: layout/type/input and brand specimen primitives.

Do not invent component props or claim the original JSX implementation is bundled. Recreate visual behavior in the user's existing framework, or retrieve approved component source if available.

## Logos and assets

The artifact describes **12 official ministry marks**. Single-color marks can be recolored with CSS masks, but only from authorized source assets. Do not manufacture the missing 12 marks, claim they are present in this package, or distribute proprietary files. Use the approved current asset library/repository when accessible.

## What is exact versus inferred

- **Observed:** the five hues, listed families, component names, philosophy, lowercase labels, title periods, container/gutter/spacing values, minimal motion, no-gradients direction, action wording, texture categories.
- **Inferred/adapted:** framework-specific markup, exact spacing values beyond the stated grid, component prop APIs other than `period`, and product-specific data UI rules. These must be verified against the actual application or full design-system export before being called official.
