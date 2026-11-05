---
name: oviya-design
description: Use when defining or auditing the visual identity of a Yazhi app — building the Sangam Earth dark palette, exporting shared CSS custom properties, or pruning ad-hoc styles that drifted from the theme. Helps you keep one token source across web and mobile while staying readable on low-power, small screens.
---

Oviya owns visual identity: a dark, terracotta-and-forest palette (Sangam Earth) exported as tokens rather than scattered hex values. The failure that compounds: every screen hard-codes its own colours, so one palette change means an archaeology project across the codebase.

## Workflow

1. **Audit the current casing first.** Grep for raw colour literals (`#[0-9a-f]{3,6}`, `rgb(`) outside the theme file; each hit is a future inconsistency.
2. **Define tokens in HSL**, because hue/saturation/lightness are what you actually adjust for a new tiṇai colourway; hex-only palettes force you to guess.
3. **Name by role, not by colour.** `--surface`, `--surface-raised`, `--accent`, `--text-muted` survive a palette change; `--terracotta-500` does not.
4. **Check contrast before shipping.** Body text at least 4.5:1 against its surface, large text 3:1 (WCAG AA). A beautiful dark palette that fails contrast is unreadable outdoors, which is where these devices are used.
5. **Export one source** — `src/styles/theme.css` with custom properties — and generate the Flutter theme map from it rather than maintaining both by hand.
6. **Prune on every UI pass.** Replace redundant style attributes with token references; delete tokens nothing uses.
7. **Keep assets minimal.** Inline SVGs under 2 KB; no icon font larger than the screens that use it.

## Token roles

| Token | Purpose | Constraint |
|---|---|---|
| `--surface` | Base background | Dark, low-luminance |
| `--surface-raised` | Cards, sheets | ≥ 6% lighter than surface |
| `--accent` | Primary action | ≥ 4.5:1 on surface |
| `--text-primary` | Body copy | ≥ 4.5:1 on surface |
| `--text-muted` | Secondary | ≥ 3:1, not for body |
| `--border` | Boundaries | Visible but non-competing |

## Defaults

- Fonts: one sans (Inter/Outfit) plus one monospace; two weights maximum to cut payload.
- Spacing scale: 4 / 8 / 12 / 16 / 24 / 32 px only.
- Dark mode as default; light mode derived from the same roles, never hand-tuned.

## Anti-patterns

- **Colour literals outside the theme file.** They drift within a release and break palette changes.
- **Naming tokens after pigment.** `--forest-green` becomes a lie the moment the palette moves.
- **Skipping contrast checks on a dark palette.** Muted text on dark backgrounds is where accessibility silently fails.
- **Maintaining CSS and Flutter themes separately.** They diverge in days; generate one from the other.
- **Shipping a heavy icon font.** It often outweighs the app's own assets on a low-storage device.

For Tamil typeface coverage and rendering checks see `tamil-localization`, for the mobile shell these tokens feed see `thozhan-dev`, and for what a new skill must look like see `skill-authoring`.
