---
name: tamil-swaram-vowels
description: Use when handling Tamil vowels (swaram / உயிரெழுத்து) in code or content — validating input sequences, building keyboards or IMEs, debugging a vowel sign that renders on the "wrong" side of its consonant, or deciding whether to emit an independent vowel letter or a dependent sign. Helps you encode vowels in correct logical order and distinguish the two glyph families that write the same twelve sounds.
---

Tamil writes its twelve vowel sounds (ஸ்வரம், natively உயிரெழுத்து — "life letters") with **two distinct glyph families**: independent vowel letters used word-initially, and dependent vowel signs (matras) attached to a consonant everywhere else. The same sound /i/ is the standalone glyph இ in இலை but the sign ி in மி. Confusing the two families — or assuming glyphs appear in memory in the order they appear on screen — is the root cause of most Tamil vowel bugs: ெ ே ை visually render to the *left* of the consonant they logically follow, and ொ ோ ௌ split into two pieces that wrap around it.

## Workflow

1. **Pick the glyph family by position, not by sound.** Word-initial vowel → independent letter (அ ஆ இ …). Vowel after a consonant → dependent sign (ா ி ீ …). An independent vowel letter directly after a consonant (e.g., க followed by இ) is invalid Tamil orthography, not an alternate spelling of கி.
2. **Always encode logical order: consonant first, vowel sign second** — even for left-side signs. கெ is stored as க U+0B95 + ெ U+0BC6; the shaping engine performs the visual reordering. Never "pre-reorder" in the string to match what you see.
3. **Treat two-part signs as one code point.** ொ ோ ௌ each occupy a single code point (U+0BCA–U+0BCC) even though they render as a left piece plus a right piece. Do not decompose them into ெ + ா manually; if you receive decomposed input, normalize (NFC) before comparing.
4. **Remember the inherent vowel.** A bare consonant letter (க) already carries /a/ — there is no visible sign for அ after a consonant. The pulli ் (U+0BCD) *removes* the inherent vowel to give the pure consonant க்.
5. **Validate sequences with a rule, not a list:** `[consonant] ( ் | vowel-sign )?` and independent vowels/aytham only at positions not immediately following a consonant. Reject two consecutive vowel signs and a vowel sign with no base.
6. **Test rendering with all four placement geometries** (right, left, below/ligated, split) plus aytham ஃ before signing off a font or UI — see `tamil-localization` for the shaping checklist.

## The 12 swaram: independent letters and their signs

| Sound (ISO 15919) | Independent letter | Code point | Dependent sign (on க) | Sign code point | Length | Sign placement |
|---|---|---|---|---|---|---|
| a | அ | U+0B85 | க (inherent, no sign) | — | kuril (short) | — |
| ā | ஆ | U+0B86 | கா | U+0BBE | nedil (long) | right |
| i | இ | U+0B87 | கி | U+0BBF | kuril | right |
| ī | ஈ | U+0B88 | கீ | U+0BC0 | nedil | right |
| u | உ | U+0B89 | கு | U+0BC1 | kuril | ligated/below (shape varies per consonant) |
| ū | ஊ | U+0B8A | கூ | U+0BC2 | nedil | ligated/below |
| e | எ | U+0B8E | கெ | U+0BC6 | kuril | **left** of consonant |
| ē | ஏ | U+0B8F | கே | U+0BC7 | nedil | **left** |
| ai | ஐ | U+0B90 | கை | U+0BC8 | nedil (diphthong) | **left** |
| o | ஒ | U+0B92 | கொ | U+0BCA | kuril | **two-part split** (wraps consonant) |
| ō | ஓ | U+0B93 | கோ | U+0BCB | nedil | **two-part split** |
| au | ஔ | U+0B94 | கௌ | U+0BCC | nedil (diphthong) | **two-part split** |

Related marks: pulli ் (U+0BCD, vowel killer), aytham ஃ (U+0B83, the thirteenth "dependent" sound, a standalone glyph as in அஃது), and the au length mark ௗ (U+0BD7, appears in decomposed/legacy data).

Kuril/nedil (short/long) is phonemic — கடி "bite" vs காடி "vinegar" — so transliteration and search folding must decide explicitly whether to preserve it (see `tamil-transliteration`).

## Anti-patterns / common failure modes

- **Storing visual order for left-side signs** (ெ before க in memory because it looks that way) — produces strings no conformant renderer or collator handles correctly; logical order is always consonant-then-sign.
- **Emitting an independent vowel after a consonant** (க + இ intending கி) — common IME/keyboard bug; renders as two separate letters and breaks search.
- **Manually decomposing split signs** (ொ → ெ + ா) or counting them as two characters — they are single code points; only NFC-normalize, never hand-assemble.
- **Forgetting the inherent /a/** — mapping "ka" to க + some sign, or stripping ் as if it were a vowel sign, corrupts the syllable structure.
- **Truncating between consonant and sign** — inherits every failure in `tamil-text-processing`; a stranded ி or ெ renders as a floating mark.

For the full letter grid these vowels generate, see `tamil-aksharas`; for cluster-safe string operations, `tamil-text-processing`; for font/shaping verification, `tamil-localization`.
