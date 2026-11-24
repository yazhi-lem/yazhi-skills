---
name: tamil-technical-terms
description: Use when rendering a technical concept in Tamil — UI strings, docs, model prompts, or a glossary — and you must decide between a native Tamil coinage, a transliterated loanword, or the English term in Latin script. Helps you reuse established Yazhi terms and coin new ones without inventing words nobody reads.
---

Illakiya's writing prompts already set the rule: prefer a common Tamil word where a natural one exists, and keep brand and product names in Tamil script. The hard part is not the rule, it is the per-term decision — and the cost of getting it wrong is inconsistency across screens and unsearchable help text. This skill owns the glossary and the coinage procedure; `tamil-tani-tamil` owns the writing standard.

## Established terms (use these)

| English | Tamil | Note |
|---|---|---|
| computer | கணினி | Established; do not use கம்ப்யூட்டர் in formal copy |
| email | மின்னஞ்சல் | Established compound (மின் + அஞ்சல்) |
| mobile / phone | கைப்பேசி | Established; கைத்தொலைபேசி in formal registers |
| meeting | கூட்டம் | Established |
| office | அலுவலகம் | Established |
| keyboard | விசைப்பலகை | Established; Illakiya's core term |
| language model | மொழி மாதிரி | Yazhi's own term; keep it stable |
| tokenizer | சொற்பிரிப்பான் | Descriptive coinage; keep it stable |
| server | சேவையகம் | Established in technical Tamil |
| dashboard | தகவல்பலகை | Coinage; confirm with native reviewer |
| login | உள்நுழைவு | Established; never லாகின் in formal copy |
| privacy | தனியுரிமை | Established in policy registers |

## The coinage procedure

1. **Search the glossary and the codebase first.** Illakiya's `web/server/prompts.ts`, Adhan's tokenizer docs, and `tamil-content-writing` all carry prior decisions. Reusing a term beats coining a better one.
2. **Prefer an existing Tamil word over a new coinage.** கணினி and மின்னஞ்சல் won because people already used them; a technically superior coinage nobody says is a loss.
3. **Coin by compounding known roots, not by inventing roots.** சொல் + பிரி + ப்பான் (tokenizer) is transparent; a Sanskrit-style abstract noun is not.
4. **Test the coinage in a real sentence, not in isolation.** A word that works in a glossary row can fail in a sentence where case endings and sandhi change its shape.
5. **Keep brand and API names in Latin script inside Tamil sentences.** `Yazhi`, `Firebase`, `gRPC`, `ONNX` stay as written; translating them breaks search and support.
6. **Record the decision in the glossary in the same change**, with the register it applies to (formal / product / casual). An unrecorded decision is re-litigated in the next PR.
7. **Apply the term consistently across the product.** One screen saying உள்நுழை and the next லாகின் is the failure this skill exists to prevent.

## Anti-patterns

- **Coinage by Sanskrit-style abstraction.** A newly minted Sanskritized noun reads as purer but is less Tamil than the everyday word it replaced — and defeats the point of தனித்தமிழ்.
- **Translating brand names.** Breaks search, support, and the model's own training signal; keep them in Latin script.
- **One term per screen.** Inconsistent terminology makes help text unsearchable and reads as unreviewed.
- **Skipping native-speaker review of a new coinage.** A coinage that is grammatical but connotes the wrong thing is worse than the loanword.
- **Recording the decision nowhere.** The next contributor re-decides, and the glossary never becomes authoritative.
- **Using a formal term in casual copy.** கைத்தொலைபேசி in an Instagram caption reads as a government notice; match the register.

Follow `tamil-tani-tamil` for the three-way decision and register, `tamil-content-writing` for the drafting standard, `tamil-localization` for UI strings and font/width constraints, and `tamil-purity-scoring` to verify Grantha-free output.
