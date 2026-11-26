---
name: indic-transliteration
description: Use when converting between Indic scripts and Latin romanization, or between Indic scripts, for search, slugs, voice input, or user-generated "Hinglish/Tanglish" text. Helps you choose a scheme and keep ambiguity visible; Tamil-specific romanization belongs to tamil-transliteration.
---

# Indic Transliteration

Transliteration is a lossy mapping, not translation. The same Latin string can represent several Indic words, and the same Indic sound can be written several ways in Latin. This skill owns the cross-script decision; `tamil-transliteration` owns Tamil-specific schemes and glyph tables.

## Workflow

1. **Name the purpose before the scheme.** Search normalization, display, URL slugs, and voice input need different strictness. A slug may tolerate ambiguity; a legal name must be reversible.
2. **Choose one scheme per surface.** Use a published standard where one exists (ISO 15919 for scholarly work, ITRANS/HK for dev workflow), and record it beside the field or index. Do not switch schemes by language without a boundary.
3. **Keep the original script as the source of truth.** Store the original alongside the transliteration, and mark generated romanization as derived. A slug is never evidence of the correct spelling.
4. **Preserve ambiguity in search.** Index multiple plausible forms, rank exact script matches first, and show the original script in results. Do not silently pick one expansion of a Latin token.
5. **Handle scheme-specific collisions explicitly.** Long vs short vowels, aspirated vs unaspirated consonants, and schwa deletion are common loss points. Build a collision table for the scripts you support and test it.
6. **Treat mixed-script input as user intent.** "Tanglish" and "Hinglish" strings are code-mixing, not errors. Normalize for search, but do not rewrite user-visible text without consent.
7. **Hand off language-specific work.** Tamil glyph-to-ISO mapping → `tamil-transliteration`; multilingual copy adaptation → `indic-multilingual-content`; font/layout → `indic-localization`.

## Scheme decision table

| Purpose | Preferred scheme | Constraint |
|---|---|---|
| Scholarly citation | ISO 15919 | Preserve distinctions, accept longer strings |
| Search index | Published scheme + variants | Rank exact-script match above romanized |
| URL slug | ASCII-safe, short | Keep original for lookup; do not use as proof |
| Voice/SMS input | Lenient parser | Ask for confirmation on ambiguous tokens |
| Cross-script display | Standard mapping | Native-speaker review before shipping |

## Anti-patterns

- **Treating romanization as canonical.** It drops distinctions that matter to readers and to meaning.
- **One scheme for every language.** A scheme tuned for Devanagari can collapse distinctions in Tamil or Bengali.
- **Silent expansion of ambiguous words.** Guessing the intended script in a result list erases the user's choice.
- **Rewriting user text for neatness.** Code-mixing is normal; normalize behind the scenes only.
- **Testing only "hello world" examples.** Real failures live in vowel length, aspiration, and conjunct clusters.

Map to: `tamil-transliteration`, `indic-script-fundamentals`, `indic-multilingual-content`, `yazhi-review`.
