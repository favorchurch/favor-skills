# Source provenance and refresh rules

## What informed this skill

1. **Linked artifact:** [Favor Church 2026 Claude design system](https://claude.ai/artifact/6hm1bC4oKAzJ1v2YTpZACG?sk=6qmf2XsG0A6-Ev471ehnUA). Accessed 2026-10-13 as a public read-only artifact via structured rendered-page extraction. Its observed style directions, names, layout dimensions, type specimens and component vocabulary are documented in [claude-artifact.md](claude-artifact.md). The full `project/design-system.json` and component/asset files were *not* obtained and are *not* part of this package.
2. **Canonical Favor repository:** `favorchurch/rock-dashboards` `main`, specifically [design/tokens/brand-2026.json](https://github.com/favorchurch/rock-dashboards/blob/main/design/tokens/brand-2026.json) (file SHA `b9df39b43e8640ff5fc81cb20ad9b44120715d24`) and [design/README.md](https://github.com/favorchurch/rock-dashboards/blob/main/design/README.md) (SHA `b6f37beac3e2fdc122edc798eb4ece0ae9108064`) retrieved via an authorized GitHub connector on 2026-10-13.
3. **Favor dashboard design guidance:** a pre-existing reusable Favor dashboard system and its documented product adaptations. It adds operating/data QA norms, which are context-specific, not blanket replacements for the linked artifact's public-brand rules.

## Precedence for future work

- If user provides a more recent official design-system export or specific approved creative direction, use it to update the semantic rules and record the changed source.
- For *public-facing new design*, prefer the linked artifact's evidenced treatment where it is specific: lowercase UI, type roles, 1200px/760px grids, full-bleed flat bands, one accent, 160ms motion, no gradients.
- For existing apps, do not blindly overwrite an established project component/theme contract. Identify divergences, report intentional exceptions, and update only the scope requested.
- For detailed brand assets and licensing, prefer the current authorized Favor repository/asset library over synthetic icons, invented logos or fonts.
- For accessibility, actual measured contrast overrides a visually attractive pairing on small text.
- If two explicit approved sources conflict in the *same* scope and neither is clearly newer/authoritative, flag the choice rather than combining contradictory requirements unnoticed.

## Refresh workflow

1. Fetch the latest `design/README.md`, `design/tokens/brand-2026.json`, approved `design/decisions/`, active theme/stylesheet and relevant asset manifests in `favorchurch/rock-dashboards`.
2. Confirm which version of the linked Claude artifact is in use. If an export exists, read its file table and component source or tokens rather than relying on a rendered-page extraction.
3. Diff literal palette, font roles, component names, casing, dimensions, motion and asset rules.
4. Update `SKILL.md` instructions, the reference files and `assets/favor-tokens.json`; do not silently change source authority.
5. Validate and repackage the full skill.

## Licensing and security

The canonical repository holds Favor-owned/proprietary typefaces and approved icons. This skill includes **no font files**, no ministry logos and no proprietary image binaries; it uses their names, documented roles and authorized-source pointers. Never print secret GitHub tokens or signed asset URLs in deliverables. Do not redistribute licensed source assets outside authorized usage just because an app integration can access them.

## Known limits

- The Claude artifact's full design-system source, assets and executable component code were not provided for local packaging.
- The linked artifact's observed `Heading/Hero/Section` `period` feature is known, but complete component prop contracts are not. Do not invent them.
- Type specimen numbers are observed samples, not guaranteed universal responsive values.
- The portable CSS is a convenience starter, not an official drop-in replacement for the current website or Rock dashboard theme.
