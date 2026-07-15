---
name: tamil-localization
description: Use when adapting a UI, product, or app for Tamil-speaking users — translating interface strings, laying out text, choosing fonts, or formatting dates/numbers. Helps you avoid the layout breakage, font-rendering failures, and grammatically broken output that literal string-substitution localization causes for Tamil.
---

Localizing into Tamil is not a find-and-replace of English strings — Tamil is agglutinative with subject-object-verb order, expands considerably in character count versus English, and requires a font stack that correctly shapes conjunct consonants and vowel-sign reordering. Treating Tamil like a drop-in replacement for English in fixed-width buttons, string-concatenation templates, or Latin-only fonts produces clipped text, mojibake-looking glyphs (boxes/broken ligatures), and sentences no native speaker would consider grammatical.

## Workflow

1. **Budget 30-60% more horizontal/vertical space than the English source.** Tamil words and especially conjuncts/compound letters render wider than the Latin equivalent; short English labels ("Save," "Submit") often expand disproportionately ("சேமி" is short, but "Save Changes" → "மாற்றங்களை சேமிக்கவும்" is much longer per character). Design fixed-width buttons/nav items with this margin, or use flexible/auto-sizing containers.
2. **Verify the font stack actually shapes Tamil correctly.** Confirm the font has a Tamil OpenType table with proper GSUB/GPOS rules for conjunct formation and vowel-sign reordering (e.g., in க + ி → கி, the vowel sign visually appears to the *left* of the consonant despite being encoded after it in memory — this reordering must be handled by the shaping engine, not assumed to be visual order in source). Fonts without Tamil support render fallback boxes or Latin-only glyphs; system default fonts on older devices are a common failure point.
3. **Never build sentences by concatenating translated word fragments around a variable.** `"{name} உள்நுழைந்தார்"` breaks when name-dependent case/honorific markers or word order need to shift; use full sentence templates with placeholders positioned per Tamil grammar, and get separate templates for pluralization/gender/honorific variants rather than trying to reuse one skeleton.
4. **Respect SOV order and postpositions, not English's SVO + prepositions.** "Click here to continue" is not word-for-word "இங்கே கிளிக் தொடர" — Tamil localizers write the verb last and restructure clause order; a literal calque reads as broken or comically formal/wrong.
5. **Format dates, numbers, and currency per Tamil/India locale conventions**, not by translating English format strings. Use `Intl.DateTimeFormat('ta-IN')` / `Intl.NumberFormat('ta-IN')` rather than hardcoding a date pattern — day-month-year ordering, and Indian digit grouping (lakh/crore, e.g., 10,00,000 not 1,000,000) differ from US conventions even when Western Arabic digits are used (Tamil numeral glyphs are rarely used in modern UI).
6. **Test truncation and line-wrap with real translated strings**, not lorem-ipsum placeholders — string-processing bugs from `tamil-text-processing` (cutting mid-grapheme-cluster) surface exactly here, in ellipsis/truncation logic applied to translated labels.
7. **Have a native reviewer check register and naturalness** before shipping — see `tamil-content-writing` for what "natural" means concretely.

## Key considerations at a glance

| Concern | English default | Tamil requirement |
|---|---|---|
| String length | Baseline | +30-60% typical expansion |
| Word order | SVO | SOV, verb-final |
| Grammar structure | Isolating (mostly fixed words) | Agglutinative (suffixes stack: case, plural, tense) |
| Font requirement | Any Latin font | Font must include Tamil OpenType shaping (GSUB/GPOS) |
| Number format | 1,000,000 | 10,00,000 (lakh/crore grouping) |
| Date order (common) | MM/DD/YYYY | DD/MM/YYYY, often with Tamil month names in formal contexts |
| Pluralization | Singular/plural suffix | Often no plural marking required on nouns; don't assume an English-style plural template maps 1:1 |

## Glyph behaviors a Tamil font must shape correctly

Test each of these five geometries with the specific font file before shipping — a font can pass four and still break the fifth:

| Behavior | Marks | Example (base க) | What failure looks like |
|---|---|---|---|
| Right-side vowel sign | ா ி ீ | கா, கி, கீ | sign detached or overlapping |
| Ligated/below sign (shape varies per consonant) | ு ூ | கு vs டு vs று | generic hook instead of the consonant-specific ligature |
| Left-side reordered sign | ெ ே ை | கெ (encoded க+ெ) | sign renders *after* the consonant |
| Two-part split sign | ொ ோ ௌ | கொ (one code point, two pieces) | only one half renders, or halves misplaced |
| Pulli and conjuncts | ், க்ஷ, ஸ்ரீ | க், க்ஷ, ஸ்ரீ | dot missing/floating; conjunct renders as separate letters |

The complete sign inventory with code points is in `tamil-swaram-vowels`; the full 247-letter grid for coverage testing is in `tamil-aksharas`.

## Anti-patterns / common failure modes

- **Fixed-width UI elements sized only for English text length** — Tamil labels get clipped or wrap awkwardly; always test with actual translated strings, not the English source length.
- **Shipping without verifying font Tamil-glyph coverage** — many "supports all languages" fonts silently fall back to tofu boxes or unshaped/reordered glyphs for Tamil conjuncts; check the specific font file, don't trust the family name.
- **Literal/calque translation via a single interpolation template reused across languages** — English `"{count} items selected"` structure imposed on Tamil produces ungrammatical or unnatural output; Tamil needs its own sentence structure, not slot-filling into an English skeleton.
- **Assuming Tamil UI numerals/dates match Western formatting conventions** — Indian digit grouping and DD/MM/YYYY ordering differ from US defaults even without script differences.
- **Truncating localized strings with code-unit-based ellipsis logic** — inherits every pitfall from `tamil-text-processing`; a truncated label can end mid-conjunct and render broken.

For the string-manipulation mechanics behind safe truncation and sorting, see `tamil-text-processing`; for romanized fallbacks/slugs, see `tamil-transliteration`; for writing idiomatic copy rather than literal translation, see `tamil-content-writing`; for the glyph and letter inventories behind the shaping table, see `tamil-swaram-vowels` and `tamil-aksharas`.
