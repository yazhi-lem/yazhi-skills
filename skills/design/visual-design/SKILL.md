---
name: visual-design
description: Use when designing or reviewing a screen, component, or visual asset and you need concrete decisions on hierarchy, spacing, typography, color/contrast, and interaction states. Helps you ship a layout that reads at real sizes instead of relying on taste; for Tamil glyph shaping use tamil-localization.
---

# Visual Design Foundations

Good visual design is a set of testable decisions, not a matter of taste. This skill gives enough structure for a developer, designer, or founder to make those decisions explicitly and review them against the same defaults. It does not own Tamil glyph behavior, product copy, or brand voice — those have their own owners.

## Workflow

1. **Name the job of the screen before choosing anything visual.** Write one sentence: what should the user notice first, and what action should they take? If two things compete for first place, the layout cannot fix that ambiguity.
2. **Set the hierarchy in one pass.** Choose one primary element, one supporting element, and everything else as context. Give the primary element the largest contrast gap, not merely the largest font.
3. **Pick a spacing scale and apply it everywhere.** Use a 4 px base with 8/16/24/32/48 px steps. A screen that uses 7, 11, and 13 px gaps arbitrarily reads as unfinished even when every individual gap looks fine.
4. **Constrain type and color.** Use at most two type families, three sizes per screen, and one accent color. Check body text against WCAG AA (4.5:1; 3:1 for large text) before shipping a palette.
5. **Define every state, not just the happy one.** For each interactive element, specify default, hover, focus, pressed, disabled, loading, and error. Focus and error states are where accessibility and trust are won or lost.
6. **Review at real sizes and real content.** Check the narrowest supported width, the longest expected Tamil and English string, and a 200% zoom pass. Do not approve a design that only works with short placeholder text.
7. **Hand off decisions, not screenshots alone.** Record the spacing scale, type sizes, color tokens, and state rules beside the component so implementation can match them without guessing.

## Decision defaults

| Decision | Default | Failure it prevents |
|---|---|---|
| Hierarchy | One primary action per screen | Competing CTAs that dilute response |
| Spacing | 4 px base; 8/16/24/32/48 steps | Arbitrary gaps that make layout feel noisy |
| Type | Two families, three sizes per screen | A visual vocabulary nobody can reuse |
| Color | One accent; AA contrast for text | Decorative palettes that fail readability |
| States | Seven states enumerated per control | Broken keyboard and error paths |
| Content | Longest Tamil/English string tested | Layout breakage after localization |

## Anti-patterns

- **Decorating before hierarchy is set.** Gradients, shadows, and cards cannot rescue a screen where every element claims equal importance.
- **Using color as the only signal.** Error, selection, and required states need text or shape too; color-blind users and high-contrast modes drop the signal.
- **Designing only the default state.** A control with no focus or error treatment forces developers to invent one under deadline, usually inconsistently.
- **Approving placeholder-length copy.** "Submit" fits; the actual Tamil label plus a validation message does not. Test with real strings, per `tamil-localization`.
- **Treating accessibility as a final audit.** Contrast, focus order, and hit targets are layout decisions; retrofitting them costs more than setting them at step 4.
- **Mixing brand voice into layout.** Keep tone decisions in the repo's brand-voice-reference.md and `tone-of-voice-application`; this skill owns structure, not wording.

Follow `tamil-localization` for Tamil fonts, glyph shaping, and number/date formats, `age-appropriate-explaining` for kid-facing density, and `yazhi-code-design` when these decisions must become an implementation plan.
