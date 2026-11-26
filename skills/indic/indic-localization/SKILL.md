---
name: indic-localization
description: Use when adapting a UI for more than one Indian language — fonts, shaping, text expansion, plurals, numbers, dates, and keyboard input. Helps you avoid layouts that only work in English or one script; Tamil-specific font and string rules belong to tamil-localization.
---

# Indic Localization

A localized UI is a layout and input problem before it is a translation problem. This skill owns the cross-language surface rules for Indian locales. `tamil-localization` owns Tamil-specific fonts, glyphs, and number/date formats.

## Workflow

1. **Inventory the surfaces.** List every string, number, date, currency, sort order, input field, and error message that changes by locale. Hidden plural strings and validation errors are the usual omissions.
2. **Check font coverage and shaping for every script.** A font must contain the required code points and shape conjuncts correctly. Test with real long strings, not placeholder labels; a tofu box is a release blocker.
3. **Budget for text expansion and height.** Indic strings can be shorter or longer than English and may need extra line height for dependent vowels and marks. Use flexible containers and test at 200% zoom.
4. **Use locale-aware formats.** Numbers, dates, currency, and plural rules come from the locale, not from a hand-written format string. Indian digit grouping and calendar conventions differ from US/EU defaults.
5. **Support input, not just display.** Decide which keyboard/IME each language needs, how romanized input is accepted, and how backspace deletes a grapheme cluster. Route Tamil input to `tamil-input-methods`.
6. **Make sorting and search locale-aware.** Code-point order is not dictionary order. Decide collation per locale, and normalize at index time while keeping the raw string for display.
7. **Verify on the shipped build.** Run the same screenshot and interaction checks against the release artifact, with a native reviewer for each locale. Record the result per locale; one pass does not certify all.

## Localization matrix

| Surface | Default rule | Test case |
|---|---|---|
| Fonts | Full coverage + conjunct shaping | Longest real string per script |
| Layout | Flexible width/height, no fixed truncation | 200% zoom + longest label |
| Numbers/dates | Locale data, not hardcoded format | Indian grouping and local calendar |
| Plurals | Locale plural rules | Zero/one/few/many where applicable |
| Input | IME or romanized path per language | Backspace on a conjunct |
| Search | Locale collation, normalized index | Two equivalent spellings |

## Anti-patterns

- **Designing only for English and hoping strings fit.** Conjunct height and text expansion break fixed-height controls.
- **Assuming one font covers all scripts.** Coverage tables lie about shaping; render real strings.
- **Hardcoding date/number formats.** Locale data exists for a reason; hand-written formats drift.
- **Treating transliteration as input support.** Users need a real IME path and grapheme-safe editing.
- **Checking one locale and calling it localized.** Each language needs its own evidence and reviewer.

Map to: `tamil-localization`, `tamil-input-methods`, `indic-script-fundamentals`, `indic-transliteration`, `yazhi-review`.
