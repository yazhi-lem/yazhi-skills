---
name: tamil-legacy-encodings
description: Use when ingesting Tamil text from pre-Unicode sources — old news archives, government documents, DTP files, or web pages that render as gibberish Latin characters unless a specific font (Bamini, TSCII, TAB) is installed. Helps you detect which legacy encoding you have, convert it to Unicode without corrupting visual-order vowel signs, and validate the migration.
---

Decades of Tamil digital text predate Unicode adoption and live in mutually incompatible legacy encodings — standards like TSCII and TAB/TAM, and pure **font-hack encodings** like Bamini where the file is "Latin" bytes that only look like Tamil when a specific font maps those bytes to Tamil glyphs. Copy the text, change the font, or feed it to any modern tool and you get gibberish like `jkpo;` (Bamini for தமிழ்). Migrating this data is a solved problem *if* you identify the encoding correctly and handle the visual-to-logical order conversion; done naively it silently produces plausible-looking but corrupted Tamil.

## Workflow

1. **Detect before converting.** Legacy Tamil files usually declare nothing useful. Signals: a hard font dependency (Bamini/STMZH/Amudham named in the document or CSS) means font-hack; bytes in the 0x80–0xFF range with Tamil-looking rendering under "TSCII" fonts means TSCII; pure ASCII that renders as Tamil only under one font is a glyph-mapped hack. Build a frequency-based detector — each encoding has telltale high-frequency byte pairs (e.g., Bamini's `jkp` for தமி) — rather than trusting metadata.
2. **Convert with a per-encoding mapping table, not char-by-char intuition.** Use maintained converters/tables (TSCII↔Unicode is formally specified; Bamini/TAB tables exist in open-source converter projects) and treat multi-byte glyph sequences as units — legacy encodings encode *glyphs*, so one Unicode letter may be 1–3 legacy bytes and vice versa.
3. **Reorder visual to logical.** This is the step naive converters botch: legacy encodings store text in **visual order** — left-side vowel signs physically precede the consonant (Bamini stores ெ-shape *before* க-shape for கெ), and split vowels are stored as two separate glyph pieces. Unicode requires logical order (consonant first) with single code points for split signs (see `tamil-swaram-vowels`). Conversion must merge the pieces and swap the order.
4. **Normalize to NFC and validate structurally.** After conversion, run NFC, then reject or flag any output containing: a vowel sign with no preceding consonant, two consecutive vowel signs, or an independent vowel immediately after a consonant — each indicates a mapping or reordering bug.
5. **Spot-check with a bilingual sample set.** Convert a page with known content (a masthead, a dated article) and have the result read by a native reader or diffed against a known-good Unicode copy; corrupted conversions often remain superficially readable.
6. **Store only Unicode going forward** and keep the original bytes archived with the detected encoding recorded — re-conversion with a fixed table is cheap; recovering a lost original is not.

## Encoding landscape

| Encoding | Type | Era/where found | Detection hint |
|---|---|---|---|
| TSCII | 8-bit standard (Tamil in 0x80–0xFF, ASCII intact) | Mailing lists, early web, Tamil Nadu govt. | Mixed ASCII + high bytes; TSCII-declared fonts |
| TAB / TAM | 8-bit standards (predecessors to TSCII) | Early Tamil Nadu government documents | Similar to TSCII but incompatible tables |
| Bamini, STMZH, Amudham, … | Font-hack (glyphs mapped onto ASCII/Latin) | DTP, newspapers, typed documents, subtitles | Pure ASCII gibberish (`jkpo;`) readable only in that font |
| TACE16 | 16-bit, one code point per akshara | Tamil Nadu govt. proposal, niche archives | 2-byte units outside Unicode Tamil block |

## Anti-patterns / common failure modes

- **Guessing the encoding from one file and batch-converting an archive** — archives mix encodings across years and authors; detect per document.
- **Converting glyphs 1:1 without visual→logical reordering** — output renders identically at first glance but has ெ stored before its consonant: search, collation, and any downstream processing (`tamil-text-processing`) silently break.
- **Losing split vowel signs** — legacy கொ is two glyph pieces; mapping each piece independently yields க + ெ + ா instead of க + ொ (U+0BCA), which NFC does *not* fully repair.
- **Trusting HTML `charset` or file metadata** — font-hack pages declare `iso-8859-1` or `windows-1252` because the bytes *are* Latin; only the font makes them Tamil.
- **Discarding originals after conversion** — every mapping-table bug found later becomes unfixable data loss.

For the structural validation rules see `tamil-swaram-vowels` and `tamil-aksharas`; for post-migration string handling see `tamil-text-processing`.
