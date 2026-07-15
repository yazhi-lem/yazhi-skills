---
name: tamil-aksharas
description: Use when you need the complete Tamil letter inventory (aksharas / அட்சரம், natively எழுத்து) — enumerating letters for a keyboard layout, font coverage test, education app, or collation routine, or deciding what counts as "one letter" in Tamil. Helps you generate the 247-letter grid from its 31 base glyphs instead of hardcoding it, and avoid shipping an "alphabet" that misses Grantha letters, aytham, or numerals.
---

The traditional Tamil syllabary (அரிச்சுவடி) is a closed, well-defined inventory of **247 letters**, every one of which a native reader treats as a single unit — an akshara — regardless of how many Unicode code points compose it. Tools that enumerate "the Tamil alphabet" from the Unicode block alone get this wrong in both directions: they list dependent signs and pulli as if they were letters, and they miss the 216 compound letters that exist only as consonant+sign sequences. Generate the inventory from its structure; never hardcode the grid.

## The 247-letter inventory

| Class | Native name | Count | Members | Composition in Unicode |
|---|---|---|---|---|
| Vowels | உயிர் (uyir, "life") | 12 | அ ஆ இ ஈ உ ஊ எ ஏ ஐ ஒ ஓ ஔ | 1 code point each (U+0B85–U+0B94) |
| Pure consonants | மெய் (mei, "body") | 18 | க் ங் ச் ஞ் ட் ண் த் ந் ப் ம் ய் ர் ல் வ் ழ் ள் ற் ன் | base consonant + pulli ் (2 code points) |
| Compound letters | உயிர்மெய் (uyirmei, "life+body") | 216 | 18 consonants × 12 vowels (க கா கி … ), see grid rule | base alone (inherent a) or base + vowel sign (1–2 code points) |
| Special | ஆய்தம் (aytham) | 1 | ஃ | U+0B83 |
| **Total** | | **247** | | |

## The 18 consonants by native class

Traditional order (வரிசை): க ங ச ஞ ட ண த ந ப ம ய ர ல வ ழ ள ற ன (U+0B95–U+0BB9, non-contiguous).

| Class | Meaning | Members | ISO 15919 |
|---|---|---|---|
| வல்லினம் (vallinam) | hard/stop | க ச ட த ப ற | k c ṭ t p ṟ |
| மெல்லினம் (mellinam) | soft/nasal | ங ஞ ண ந ம ன | ṅ ñ ṇ n m ṉ |
| இடையினம் (idaiyinam) | medium/approximant | ய ர ல வ ழ ள | y r l v ḻ ḷ |

## Workflow

1. **Generate uyirmei rows, don't enumerate them.** For each consonant C: the mei is C + ் ; the a-row akshara is C alone; the other 11 are C + the matching vowel sign (`tamil-swaram-vowels` has the sign table). Worked row for க: க் க கா கி கீ கு கூ கெ கே கை கொ கோ கௌ. 18 × 13 + 12 + 1 = 247.
2. **Decide up front whether "complete" includes Grantha.** Modern Tamil borrows six Grantha letters for loanwords: ஜ (U+0B9C), ஶ (U+0BB6), ஷ (U+0BB7), ஸ (U+0BB8), ஹ (U+0BB9), and the conjunct க்ஷ (க+்+ஷ); ஸ்ரீ (ஸ+்+ர+ீ) is a fixed ligature. Each Grantha consonant takes the full 13-form row too. Keyboards, fonts, and school apps that omit them can't type ஜூன் (June) or ஸ்ரீ.
3. **Count aksharas as grapheme clusters, never code points.** க் and கா are 2 code points but 1 akshara each; use a segmenter per `tamil-text-processing`.
4. **Collate in varisai order:** all uyir first (அ→ஔ), then aytham, then consonant rows in traditional order with each row's 13 forms ordered by vowel — `Intl.Collator('ta')`/ICU already implement this; don't sort by code point.
5. **Include numerals and symbols in font-coverage checks:** digits ௦–௯ (U+0BE6–U+0BEF), ௰ 10, ௱ 100, ௲ 1000 (U+0BF0–U+0BF2) — rare in modern text (see `tamil-transliteration`) but expected of a complete font.
6. **Round-trip test the generated grid:** render all 247 (+ Grantha rows), confirm no tofu, no stranded signs, and that NFC normalization leaves every akshara unchanged.

## Anti-patterns / common failure modes

- **Enumerating the Unicode block as "the alphabet"** — U+0B80–U+0BFF contains signs, marks, and symbols that are not letters, and cannot contain the 216 uyirmei, which exist only as sequences.
- **Hardcoding the 216-cell grid** — typo-prone and unverifiable; generate from 18 bases × 12 vowel forms and spot-check one row.
- **Counting code points as letters** — reports வணக்கம் as 7 letters instead of 5; every length/limit decision inherits this bug.
- **Omitting Grantha letters and aytham** from keyboards or coverage tests — real modern text (loanwords, names, ஸ்ரீ) becomes untypeable or unrenderable.
- **Sorting the grid by code point** — puts mei forms and vowel rows in an order no Tamil reader recognizes; use Tamil collation.

For the vowel signs that generate the grid columns, see `tamil-swaram-vowels`; for cluster-safe counting and slicing, `tamil-text-processing`; for romanizing the inventory, `tamil-transliteration`.
