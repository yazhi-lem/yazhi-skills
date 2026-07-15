---
name: tamil-numerals-symbols
description: Use when deciding how to render numbers, dates, or units in Tamil content — or when a design, archive, or classical text calls for the native Tamil numeral glyphs and clerical symbols. Helps you choose between Western and Tamil digits correctly, use the traditional multiplicative numerals without inventing fake positional forms, and verify font coverage for the symbol block.
---

Tamil has a complete native numeral system and a set of clerical symbols (day, month, year, rupee, debit, credit) encoded in Unicode — but modern Tamil text almost never uses them, and the traditional system is **not positional-decimal**, so mechanically substituting ௧௦ for "10" produces something no historical document ever contained. Getting this right means knowing both when to use the native glyphs (rarely, deliberately) and how the traditional system actually composes numbers when you do.

## Workflow

1. **Default to Western Arabic digits (0–9) for all modern content** — UI, prices, dates, phone numbers. Native readers expect "10 நிமிடம்", not "௧௦ நிமிடம்"; Tamil digits in a modern interface read as decorative affectation or an over-eager localization bug (see `tamil-localization`).
2. **Reserve Tamil numerals for deliberate contexts:** classical/religious text editions, traditional almanacs (பஞ்சாங்கம்), decorative or heritage design, and scholarly reproduction of manuscripts or ledger archives.
3. **Compose traditional numbers multiplicatively, not positionally.** The historical system has no zero: 10, 100, 1000 are their own glyphs (௰ ௱ ௲), and numbers chain digit×unit + remainder. 2026 is ௨௲௨௰௬ (2×1000, 2×10, 6) — *not* ௨௦௨௬. Positional use of ௦–௯ (௨௦௨௬) is a modern convention; pick one system per document and label which you're using.
4. **Use the clerical symbols only with their conventional meanings** (table below) — they come from accounting and almanac practice, not general typography.
5. **Check font coverage separately for U+0BE6–U+0BFA.** Many otherwise complete Tamil fonts omit the symbol range (௳–௺); render the full block and look for tofu before shipping (coverage workflow in `tamil-aksharas`).
6. **Never auto-convert digits in either direction** during transliteration or localization passes — preserve what the source used (`tamil-transliteration` covers why).

## Glyph reference (U+0BE6–U+0BFA)

| Glyph | Code point | Meaning |
|---|---|---|
| ௦ ௧ ௨ ௩ ௪ ௫ ௬ ௭ ௮ ௯ | U+0BE6–U+0BEF | digits 0–9 (௦ is a modern addition; the traditional system had no zero) |
| ௰ | U+0BF0 | ten |
| ௱ | U+0BF1 | hundred |
| ௲ | U+0BF2 | thousand |
| ௳ | U+0BF3 | day sign (நாள்) |
| ௴ | U+0BF4 | month sign (மாதம்) |
| ௵ | U+0BF5 | year sign (வருடம்) |
| ௶ | U+0BF6 | debit sign (பற்று) |
| ௷ | U+0BF7 | credit sign (வரவு) |
| ௸ | U+0BF8 | "as above" ditto sign |
| ௹ | U+0BF9 | rupee sign |
| ௺ | U+0BFA | number sign (எண்) |

Worked traditional examples: 40 = ௪௰ (4×10); 555 = ௫௱௫௰௫; 1998 = ௲௯௱௯௰௮.

## Anti-patterns / common failure modes

- **Positional strings passed off as traditional numerals** (௧௯௯௮ for 1998 in a "classical" design) — historically wrong; the traditional form is ௲௯௱௯௰௮, and mixing systems within one text reads as machine-generated.
- **"Helpful" digit conversion in a localization pass** — converting 10 → ௧௦ everywhere makes modern UI look wrong to every native reader; digits are a register choice, not a translation.
- **Assuming font support because Tamil letters render** — the numeral/symbol range is the most commonly omitted part of the block; test it explicitly.
- **Using ௹ as a general currency symbol** — modern Indian content uses ₹ (U+20B9); ௹ belongs to historical ledger reproduction only.
- **Parsing Tamil numerals with a positional-decimal parser** — ௪௰ is 40, not 410 or 4·10 concatenated; a traditional-system parser must handle multiplicative chaining.

For the letter (non-numeral) inventory see `tamil-aksharas`; for date/number *formatting* conventions (lakh/crore grouping, DD/MM/YYYY) see `tamil-localization`.
