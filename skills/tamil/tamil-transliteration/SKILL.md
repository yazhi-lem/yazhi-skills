---
name: tamil-transliteration
description: Use when converting Tamil script to Latin characters (or back) — for search indexing, URL slugs, voice/SMS input normalization, or supporting "Tanglish" user input. Helps you pick the right romanization scheme and handle the many-to-one ambiguity that makes reverse transliteration lossy.
---

Transliteration between Tamil (U+0B80–U+0BFF) and Latin script is not one operation but several, each with different goals: a formal, reversible academic scheme (ISO 15919), a phonetic approximation for search/pronunciation, and the informal "Tanglish" spelling real users type in chat and SMS. These schemes disagree with each other, and going Latin-to-Tamil is inherently ambiguous because Tamil's ~18 consonants and limited vowel-length distinctions collapse many possible Latin spellings onto the same intended word — you cannot build a lossless reverse mapping without added context or a dictionary/language model.

## Workflow

1. **Decide direction and reversibility requirement first.** Tamil→Latin for display/search is easy and mostly deterministic. Latin→Tamil (e.g., converting "Tanglish" user input to native script) is ambiguous and needs a ranked-candidate approach, not a single deterministic function.
2. **Pick a scheme matched to the use case**, not the most "correct" one — see table. Mixing schemes within one product (e.g., ISO 15919 in URLs but ad-hoc phonetics in search) causes inconsistent lookups.
3. **For Tamil→Latin (forward), map at the cluster level**, not the code point level — a consonant+vowel-sign cluster like மி must map to one syllable unit (`mi`), not to `m` followed by a separate vowel-sign transliteration that could misorder.
4. **For Latin→Tamil (reverse/"Tanglish" input), generate candidate sets, not a single answer.** "eppadi" could be spelled எப்படி; "zh" digraphs (used for ழ) versus plain "l" (often substituted for ள or ழ by casual typists) create systematic ambiguity — maintain a substitution-rule table and rank candidates by frequency/dictionary match rather than picking one deterministically.
5. **Normalize before comparing/searching.** Strip vowel-length distinctions, fold `zh`/`z`/`l` variants, and fold aspirated/unaspirated consonant spellings (`th`/`t`, `dh`/`d`) into a canonical search key so "தமிழ்" typed as "tamil," "thamil," or "thamizh" all resolve to the same record.
6. **Handle mixed-script and numerals explicitly.** Tamil has its own numeral forms (Tamil digits, U+0BE6–U+0BEF) that are rarely used in modern digital text — most Tamil content uses Western Arabic numerals inline (e.g., "10 நிமிடம்"). Don't assume a string is pure-script; detect and preserve embedded Latin words/brand names/numbers rather than attempting to transliterate them.
7. **Validate round-trips on a test set of real ambiguous words** before shipping any reverse-transliteration feature — check that common Tanglish spellings for high-frequency words resolve correctly.

## Scheme comparison

| Scheme | Purpose | Example for வணக்கம் | Reversible? |
|---|---|---|---|
| ISO 15919 | Academic/library standard, diacritics encode exact phonemes | vaṇakkam | Yes, near-lossless |
| IAST-style / Madras Lexicon | Linguistic scholarship | vaṇakkam (similar) | Yes |
| Simplified ASCII (search/URL slugs) | No diacritics, ASCII-only | vanakkam | No — loses retroflex vs. dental distinction |
| Tanglish (user-generated, chat/SMS) | Fast informal typing | vanakkam / vannakam / vanaikkam | No — many spellings per word, ambiguous both ways |

## Ambiguity example

The Latin string "kali" could map to கலி, காலி ("empty," long a), or களி (retroflex ள, different word/meaning) — a plain consonant-by-consonant reverse map cannot disambiguate; distinguishing dental ல, retroflex ள, and alveolar ழ all commonly collapse to "l" or "zh" in casual typing. Treat reverse transliteration as a ranking/search problem, not a function.

## Anti-patterns / common failure modes

- **Building a single deterministic Latin→Tamil function** and expecting correct round-trips — the mapping is inherently many-to-one; ship candidate ranking or a lookup dictionary instead.
- **Mapping consonant and vowel-sign code points independently** instead of at the syllable-cluster level, which can produce transliterations with vowels in the wrong order relative to how Tamil script visually (but not logically) reorders some vowel signs before the consonant.
- **Ignoring retroflex/dental/alveolar distinctions** (ல் vs ள் vs ழ்) by collapsing them all to "l" in forward transliteration when the output needs to be reversible or search-precise — fine for casual display, wrong for anything requiring disambiguation.
- **Assuming all digits in Tamil text are Tamil numerals** — most real-world Tamil content uses Western Arabic digits; a transliteration pass that "helpfully" converts 10 → Tamil numeral glyphs will look wrong to native readers, who rarely use the Tamil numeral system.
- **Not normalizing before search matching**, so "தமிழ்" indexed as "tamil" fails to match a user query typed "thamizh" — apply the same folding rules on both index and query sides.

See `tamil-text-processing` for cluster-boundary mechanics needed to transliterate correctly, and `tamil-localization` for when transliterated slugs/labels appear in UI.
