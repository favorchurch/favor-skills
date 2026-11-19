# Favor Church 2026 brand core

This is a portable, sourced snapshot. The bundled tokens are verified against the current `favorchurch/rock-dashboards` brand files on 2026-10-13; the linked Claude design system's rules were partially extracted from its shared rendering. The full original file table and proprietary assets were not obtainable. Never describe the snapshot as an exact source export.

## Palette and meaning

| Name / semantic role | Hex | Treatment |
| --- | --- | --- |
| Cream / page ground | `#FEF1E8` | signature warm page background |
| Near-black / ink | `#121411` | headlines, most body text, high-emphasis rules |
| White / surface | `#FFFFFF` | clean cards, forms, charts, print backgrounds |
| Orange / brand accent | `#F45500` | brand energy, select hero accents and visual focus |
| Blue / secondary | `#007FAE` | linked, navigational, or distinct action family |
| Gold / third accent | `#FFB42A` | select supporting decorative/data accents |
| Muted ink | `#625F59` | secondary text, captions and subdued metadata |
| Rule | `#DED8D1` | quiet borders, divisions and table separators |
| Soft orange | `#FFE2D2` | supportive accent fill |
| Soft blue | `#D8F1F5` | supportive secondary fill |
| Focus | `#005EB8` | keyboard focus ring |
| Positive | `#34735A` | success/healthy feedback, paired with words |
| Warning | `#A65B00` | caution, paired with words |
| Chart plum | `#79547A` | categorical series |
| Chart sage | `#62806B` | categorical series |
| Chart gray | `#A7A29C` | categorical series |

A separate, more conservative executive theme has used `#C23F00` as orange text and `#00647F` as blue text to improve contrast. These are contextual darkened adaptations, not replacements for the canonical palette. Recheck contrast on the actual surface: primary text generally needs 4.5:1 and meaningful non-text icons and boundaries 3:1. Do not use color alone to communicate status.

## Typography by job

| Family | Role | Guidance |
| --- | --- | --- |
| Favorvetica (Regular, Bold) | display | hero lines, big section anchors, large numeric statements |
| Favor Headline | editorial accent | distinct short headlines; use sparingly |
| Favor Sans (Regular, Bold) | utility | interfaces, forms, labels, body, captions, section identifiers |
| Favor Folk | expressive | event/ministry identity, limited accent text |
| Favor Cutout | decorative | large, short decorative words or visual cut-outs only |
| Shines Paws | kids/playful | youth and kids celebratory moments |
| Maows Hand | handwritten | annotation or accent, not dense content |
| MARKED | stamp/label | stamp-like decorative treatments |

The linked design artifact adds Helvetica Neue/Arial for public body, PP Right Grotesk Mono for meta/date, Perfectly Nineties for scripture and Folkies Vantage Script for expressive script. Read `claude-artifact.md` before picking exact faces for public/brand work. Use no more display types than the composition needs. On dense operational screens, one display role plus Favor Sans is often enough. For UI copy, prefer high legibility over expressive type. For changing numbers use tabular numerals where supported.

**Font rights:** Do not redistribute or expose Favor proprietary font binaries. When a Favor project already includes authorized fonts, reference those in that codebase. Otherwise use `"Favorvetica", Arial, sans-serif` for display and `"Favor Sans", Arial, sans-serif` for utility with actual fallback rendering explicitly acknowledged. Never pretend a generic typeface is the licensed original.

## Iconography

The canonical `design/assets/icons/` catalog includes:

- Bursts, sparks, stars, asterisks, flowers
- Scalloped circles, wavy badges, squiggles, scribbles
- Waves, smileys, globe, rounded column

Use those hand-made forms for identity and section rhythm, not save/delete/navigation semantics. Functional controls should retain conventional icons with readable labels or accessible names. SVG assets should usually inherit color through `currentColor`. Prefer existing approved project icon assets over newly approximated brand motifs.

## Texture and physicality

| Category | Approximate blend and opacity | Typical placement |
| --- | --- | --- |
| Photocopy | multiply/screen, 8-20% | expressive hero/event segments |
| Noise grain | screen, 5-12% | subtle warmth over cream |
| Dust and scratches | screen, 6-15% | expressive editorial atmosphere |
| Paper | multiply, 10-30% | masthead and spacious campaign areas |

Avoid covering dense tables, charts, small navigation labels, or vital buttons with visible texture. Evaluate its effect on contrast and readability rather than mechanically using the top of an opacity range. Favor is tactile and editorial; it is not blurry glassmorphism, universal soft shadows, or default enterprise SaaS chrome.

## Structural signatures

- Cream canvas + white work surfaces + legible near-black type.
- Explicit horizontal rules and editorial sections rather than shadow-heavy card stacks.
- Small uppercase eyebrow labels for metadata when they help hierarchy.
- Large, deliberate hero/type moment and restrained decorative punctuation.
- Moderate corners or intentional square geometry, depending on context; do not enforce a radius where one is not tokenized.
- Blue distinguishes navigation/secondary controls; orange identifies selected primary moments.
- Strong contrasts between canvas, surface, text, actions, and states.
- Typography, spacing and hierarchy make the page Favor before decorative stickers do.

## Misuse to prevent

- Splashing orange on every component instead of creating hierarchy.
- Overusing several expressive fonts in one operational surface.
- Introducing invented brand swatches, logo variants, icons, or proprietary font substitutes as official.
- Confusing expressive campaign graphics with routine administration.
- Using texture inside charts and behind long body paragraphs.
- Reproducing fake figures in a dashboard without marking them sample/demo.
- Treating zero and unknown as interchangeable.
- Stretching desktop data views onto narrow phones without hierarchy changes.

## Source URLs

- [Canonical source directory](https://github.com/favorchurch/rock-dashboards/tree/main/design)
- [Brand token file](https://github.com/favorchurch/rock-dashboards/blob/main/design/tokens/brand-2026.json)
- [Design README](https://github.com/favorchurch/rock-dashboards/blob/main/design/README.md)
