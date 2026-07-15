---
name: tamil-text-processing
description: Use when code manipulates Tamil strings — truncating, measuring length, sorting, indexing, or regex-matching text that contains Tamil script — and the output looks subtly wrong (broken glyphs, mis-sorted lists, off-by-one substrings). Helps you handle Tamil text at the grapheme-cluster level instead of the code-unit level so operations don't corrupt combining marks.
---

Tamil script is encoded in Unicode block U+0B80–U+0BFF, but a single "letter" a Tamil reader perceives — a grapheme cluster — is frequently built from multiple code points: a base consonant plus a vowel sign (matra) or a virama (pulli, U+0BCD) that suppresses the inherent vowel. Treating code points, UTF-16 code units, or bytes as if they were letters is the single biggest source of Tamil text bugs: truncation that splits a cluster renders as a dangling vowel sign or a stray dot, `.length` checks that wildly overcount visual width, and naive substring slicing that produces invalid, unrenderable sequences.

## Workflow

1. **Identify the unit you actually need.** Byte length (storage/network limits), UTF-16 code unit count (JS `.length`), Unicode code point count (`Array.from(str).length` / Python `len(str)`), and grapheme cluster count (what a user perceives as "characters") are four different numbers for the same Tamil string. Pick the one that matches the requirement — display truncation almost always means grapheme clusters, not code units.
2. **Use a grapheme segmenter for anything user-facing.** JS: `Intl.Segmenter('ta', { granularity: 'grapheme' })`. Python: the `grapheme` or `regex` (`\X`) packages, or ICU via `PyICU`. Never hand-roll cluster boundaries — combining rules are complex enough to get wrong on edge cases.
3. **Truncate/substring only at cluster boundaries.** Segment first, slice the cluster array, then rejoin — never slice the raw string by index.
4. **Sort with Tamil collation, not code point order.** Use `Intl.Collator('ta')` (JS) or ICU collation (`PyICU.Collator`), not `str.sort()`/`Array.sort()` default comparators, which sort by UTF-16 code unit and produce an order no Tamil reader would recognize.
5. **Write regex against clusters or use Unicode property escapes carefully.** `.` in most regex engines matches one code point, not one cluster — `மி.` can accidentally match only half of `மிழ்`. Use `\X` (PCRE/Perl/`regex` module) for cluster-aware matching, or explicitly quantify `\p{M}*` after base characters to absorb combining marks.
6. **Test with real multi-part clusters**, not just simple consonants — see table below — before shipping any string-manipulation code path.

## Grapheme clusters vs. code points vs. code units

| String | Visual letters (grapheme clusters) | Unicode code points | JS UTF-16 code units |
|---|---|---|---|
| `தமிழ்` (Tamil) | 4: த, மி, ழ், (ழ்=ழ+்) | 5: த, ம, ி, ழ, ் | 5 |
| `வணக்கம்` (hello) | 5: வ, ண, க், க, ம் | 7 | 7 |
| `ஸ்ரீ` (Sri, conjunct) | 1 cluster (ஸ்ரீ) or 2 depending on segmenter | 4: ஸ, ், ர, ீ | 4 |
| `க்ஷ` (ksha ligature) | 1 visual unit, 3 code points | 3: க, ், ஷ | 3 |

`மி` alone is a two-code-point sequence (ம U+0BAE + ி U+0BBF) that renders as one visual glyph — `"மி".length` is 2 in JS even though a reader sees one letter. `ழ்` (ழ + pulli U+0BCD) similarly is two code points rendering as one glyph with a dot below.

## Native letter classes and their code-point shapes

Every grapheme cluster you segment corresponds to one letter in Tamil's native classification — knowing the class tells you how many code points to expect:

| Native class | Example glyphs | Code points per letter |
|---|---|---|
| உயிர் (uyir) — 12 vowels | அ, ஈ, ஔ | 1 (U+0B85–U+0B94) |
| மெய் (mei) — 18 pure consonants | க், ழ், ன் | 2 (consonant + pulli U+0BCD) |
| உயிர்மெய் (uyirmei) — 216 compounds | க, கா, கொ | 1 (inherent a) or 2 (consonant + vowel sign) |
| ஆய்தம் (aytham) | ஃ | 1 (U+0B83) |

The full 247-letter inventory and how to generate it is in `tamil-aksharas`; the vowel-sign placement rules (including the left-side and split signs that make visual order differ from logical order) are in `tamil-swaram-vowels`.

## Anti-patterns / common failure modes

- **Truncating by code unit/point count** (`str.slice(0, 20)`, `str[:20]`): can cut a vowel sign or pulli off its base consonant, leaving an orphaned combining mark that renders as a floating dot or broken glyph, or that fails to round-trip when re-parsed.
- **Using `.length` as a proxy for "how many letters"** for UI constraints like input-field character limits — a 10-character Tamil word can report a code-unit length of 14+, causing premature truncation warnings or silently over-tight limits.
- **Default/locale-naive sort** (`Array.prototype.sort()`, Python's plain `sorted()`) on Tamil strings — sorts by code point, which does not match Tamil traditional alphabetical order (vowels, then consonants in a fixed sequence, with compound letters ordered by base consonant, not by the code point of the vowel sign attached). Always pass an `Intl.Collator('ta')` or ICU collator.
- **Regex `.` or `[^x]` assumed to match "one Tamil letter"** — it matches one code point and can split a cluster mid-match, corrupting replacements done with matched groups.
- **Reversing a string by code point** (`str.split('').reverse().join('')`) — breaks every multi-code-point cluster into disconnected, unrenderable fragments.

For romanizing this text see `tamil-transliteration`; for how truncation/length limits interact with UI space budgeting see `tamil-localization`; for writing the actual Tamil copy being processed see `tamil-content-writing`; for the letter inventory itself see `tamil-aksharas` and `tamil-swaram-vowels`.
