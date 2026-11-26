---
name: indic-script-fundamentals
description: Use when code handles text in more than one Indic script — Devanagari, Bengali, Tamil, Telugu, Kannada, Malayalam, Gurmukhi, and others — and grapheme, encoding, or normalization bugs appear. Helps you treat clusters as units; Tamil-specific glyph work belongs to tamil-text-processing.
---

# Indic Script Fundamentals

Indic scripts share a logical model but differ in glyph shaping, combining marks, and legacy encodings. Bugs look like "wrong characters" while the bytes are correct. This skill owns the cross-script rules; `tamil-text-processing` and the other `tamil-*` skills own Tamil-specific detail.

## Workflow

1. **Name the script and the operation.** State whether the task is validation, truncation, sorting, search, rendering, or conversion. A rule that is safe for byte slicing in ASCII is unsafe for any Brahmi-derived script.
2. **Work at grapheme-cluster boundaries.** A user-perceived character can be a base consonant plus vowel sign, virama, and conjunct. Never slice by UTF-16 code units or Python bytes; use a Unicode grapheme library and test with a conjunct-heavy sample.
3. **Normalize deliberately, rarely.** Decide whether the pipeline uses NFC or NFD, document it, and apply it at the input boundary only. Normalizing after storage changes identifiers and breaks cached keys.
4. **Separate logical order from display order.** Store text in Unicode logical order. Let the font/shaping engine handle repositioning; do not reorder code points to make a screenshot look right.
5. **Detect legacy encodings before trusting text.** Pre-Unicode sources may be TSCII, ISCII, Bamini, or font-specific byte maps. Identify the encoding from metadata or byte patterns, convert once, and keep the original bytes for audit.
6. **Test with a script matrix.** Use at least one word with a conjunct, one with a dependent vowel, one with a combining mark above/below, and one mixed-script string. Run the same assertions for every supported script.
7. **Route script-specific work onward.** Tamil glyph inventory → `tamil-aksharas`; Tamil string operations → `tamil-text-processing`; transliteration → `indic-transliteration`; UI layout → `indic-localization`.

## Cross-script checklist

| Concern | Rule | Failure mode |
|---|---|---|
| Length / truncation | Count grapheme clusters | A cursor lands inside a conjunct |
| Storage | Unicode logical order, documented normalization | Display-order text breaks search and copy |
| Sorting | Locale-aware collation, not code-point order | Dictionary order looks random to readers |
| Search | Normalize at index time, keep raw source | Equivalent spellings miss each other |
| Legacy input | Detect, convert once, retain original | Irreversible mojibake after a second pass |
| Fonts | Verify shaping for every supported script | Tofu boxes or misplaced marks |

## Anti-patterns

- **Slicing by code units.** It splits clusters and produces characters a native reader cannot pronounce.
- **Assuming all Indic scripts share Tamil rules.** The family resemblance is real; the code point behavior is not identical.
- **Reordering code points to fix rendering.** That creates text that looks right in one font and is wrong everywhere else.
- **Normalizing on every read.** Repeated normalization changes stored keys and makes diffs untraceable.
- **Testing only with Hindi or only with Tamil.** A fix for one script often fails on another's conjunct or vowel sign.

Map to: `tamil-text-processing`, `tamil-aksharas`, `indic-transliteration`, `indic-localization`, `yazhi-review` (language axis).
