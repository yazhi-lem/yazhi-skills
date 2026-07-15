---
name: tamil-swaram-notation
description: Use when digitizing, rendering, or generating Carnatic music notation written in Tamil script — swaram lines in a paattu book, a notation editor, or a music-learning app — and you need the seven swara letters, octave dots, and duration marks to survive as searchable text instead of becoming images. Helps you encode ஸ ரி க ம ப த நி notation in Unicode without breaking the letters' own vowel signs.
---

Carnatic notation in Tamil sources writes the seven swaras (சப்த ஸ்வரம்) as Tamil letters — ஸ ரி க ம ப த நி — decorated with octave dots above/below and duration punctuation. Tamil music theory also has its own older seven-note names (ஏழிசை, attested from the Silappatikaram tradition). The digital trap: the decorations have no dedicated Unicode characters, so naive digitization either flattens the notation (losing octave/duration, making it wrong) or renders it as images (losing search and accessibility). Done carefully, plain Unicode text can carry the whole system.

## Workflow

1. **Encode swara letters as ordinary Tamil text.** Use the Grantha ஸ (U+0BB8) for sa — the common printed convention — or ச consistently if matching a source that uses it; never mix the two in one corpus, since they are different code points and break search.
2. **Mark octaves with combining dots:** U+0307 (combining dot above) for மேல் ஸ்தாயி (higher octave), U+0323 (combining dot below) for மந்திர ஸ்தாயி (lower octave), attached after the *complete* swara letter — ரி + U+0307, i.e., after the vowel sign ி, not between ர and ி. Verify your font stack actually positions these on Tamil bases; many Tamil fonts place them badly, so test before committing to the scheme (font checks per `tamil-localization`).
3. **Encode duration with the source's punctuation convention:** the swara letter alone is one unit (mātrā); `,` extends one unit; `;` extends two. Keep them as literal ASCII comma/semicolon — they're part of the notation, not prose punctuation, so exempt notation lines from typographic "smart punctuation" processing.
4. **Mark swara variants with following digits** (ரி2, க1) or subscripts if the source distinguishes them — store the digit adjacent to the letter, never inside the letter's code-point sequence.
5. **Keep tala structure as text:** beat separators `|` and cycle end `||` on the swara line, with the sahitya (lyric) line aligned beneath in a separate text line — don't merge swara and lyric into one string.
6. **Validate round-trips:** notation text must survive NFC normalization, copy-paste, and grapheme segmentation (`tamil-text-processing`) with dots still attached to the right swaras.

## The seven swaras in Tamil

| Swara | Tamil notation letter | Ancient Tamil name (ஏழிசை) | Western analogue |
|---|---|---|---|
| Sa (ஷட்ஜம்) | ஸ (or ச) | குரல் (kural) | do |
| Ri (ரிஷபம்) | ரி | துத்தம் (tuttam) | re |
| Ga (காந்தாரம்) | க | கைக்கிளை (kaikkiḷai) | mi |
| Ma (மத்யமம்) | ம | உழை (uḻai) | fa |
| Pa (பஞ்சமம்) | ப | இளி (iḷi) | sol |
| Da (தைவதம்) | த | விளரி (viḷari) | la |
| Ni (நிஷாதம்) | நி | தாரம் (tāram) | ti |

Example line (Mayamalavagowla arohanam): `ஸ ரி க ம ப த நி ஸ̇` — the final ஸ̇ carries U+0307 for the upper-octave sa.

## Anti-patterns / common failure modes

- **Digitizing notation pages as images** — loses search, transposition tooling, screen-reader access, and any hope of programmatic analysis; the notation is representable as text.
- **Dropping octave dots because "the font looks odd"** — ஸ and ஸ̇ are different notes; fix the font stack instead of silently changing the music.
- **Inserting combining dots inside the akshara** (ர + U+0307 + ி) — breaks grapheme segmentation and renders the dot on the wrong element; dots go after the complete cluster.
- **Mixing ஸ and ச for sa within one corpus** — text search for a phrase fails on half the documents; pick one and record the convention.
- **Letting smart-quote/punctuation normalizers touch notation lines** — `,` and `;` are durations; a "typography cleanup" pass that converts or strips them corrupts rhythm.

For the Grantha letters used here see `tamil-aksharas`; for why the vowel-sign structure of ரி and நி matters when attaching marks see `tamil-swaram-vowels`; for font verification see `tamil-localization`.
