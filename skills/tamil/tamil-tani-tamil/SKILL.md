---
name: tamil-tani-tamil
description: Use when writing or reviewing Tamil copy that should read as தனித்தமிழ் (pure Tamil) — product UI, model responses, marketing, or documentation — and the text currently leans on Sanskrit loanwords, Grantha letters, or English code-mixing. Helps you decide per term whether to use a native coinage, a loanword, or the English word, and keep that choice consistent.
---

தனித்தமிழ் (tani-tamil, "pure Tamil") is the position that Tamil should be written in its own words and letters rather than borrowed ones. It is not a ban on all borrowing — it is a decision procedure applied term by term. Adhan's Aram harness treats it as a testable property (Linguistic Purity: "Tamil-only when requested, no Tanglish leakage"), and Illakiya's writing prompts set the same standard: prefer a common Tamil word where a natural one exists, keep brand names in Tamil script. This skill owns the writing decision; `tamil-purity-scoring` owns the measurement.

## The three-way decision per term

| Option | Use when | Example |
|---|---|---|
| Native Tamil word or coinage | A natural Tamil word exists or the concept is everyday | கணினி (computer), கைப்பேசி (mobile), மின்னஞ்சல் (email) |
| Loanword in Tamil script | The word is fully nativized and understood by every reader | பஸ், டீ, ரயில் — spoken-register, not formal writing |
| English in Latin script | Brand, product, or API name that must not be translated | `Yazhi`, `Firebase`, `gRPC`, `ONNX` |

The default for formal and product copy is the native word. The default for casual/social copy is whatever the audience actually reads — see `tamil-social-content` for the code-mixing decision.

## Workflow

1. **Name the register before editing.** Formal written Tamil (letters, articles, official use) is near-pure; spoken/casual Tamil tolerates loanwords and Tanglish. Choosing the register first prevents "fixing" text that was never meant to be formal.
2. **List every borrowed term in the text** — Sanskrit-derived (தர்மம், ராஜா, லோகம்), Grantha-letter words (ஜூன், ஸ்ரீ, ஷாப்), and English code-mixed words (AI, server, login). You cannot decide per term without the list.
3. **Apply the three-way table to each term.** Prefer the native word when one exists; keep the loanword when it is fully nativized in the target register; keep the English word only for brands and API names.
4. **Check the Grantha letters.** A word using ஜ ஶ ஷ ஸ ஹ or the க்ஷ / ஸ்ரீ forms is by definition not pure Tamil. Either substitute a native word or accept the loanword knowingly — never leave it in by accident.
5. **Write the replacement, not just the flag.** "Avoid loanwords" is not an edit. Produce the native term and confirm a native speaker accepts it in that sentence; a correct word in the wrong sentence still reads as translated.
6. **Keep the glossary consistent.** Record each decision in the project's terminology table (see `tamil-technical-terms`) so the next screen does not say லாகின் where this one says உள்நுழை.
7. **Re-read for calque grammar.** Sentence-by-sentence translation from English produces grammatically valid but unnatural Tamil. Pure vocabulary over English syntax is still not தனித்தமிழ்; rewrite the sentence in Tamil word order.

## Anti-patterns

- **Purity as a lexical ban.** Replacing every loanword with an obscure coinage nobody uses makes the text correct and unreadable; the goal is natural Tamil, not a word-list score.
- **Translating brand and API names.** `Yazhi`, `Firebase`, `gRPC` stay as they are, written in Tamil script where the sentence needs it; translating them breaks search and support.
- **Fixing vocabulary while leaving English syntax.** The most common failure — the words are Tamil, the sentence is English, and native readers clock it instantly.
- **Inconsistent register across one product.** உள்நுழை on one screen and லாகின் on the next reads as unreviewed and breaks search.
- **Leaving Grantha letters in "pure" text.** ஜூன் or ஸ்ரீ in copy claimed to be தனித்தமிழ் fails the purity check on its face; substitute or accept the loanword explicitly.
- **Skipping native-speaker review.** A fluent-sounding machine Tamil that a native reader finds wrong costs more than the loanword it replaced.

Follow `tamil-content-writing` for the drafting standard and register table, `tamil-technical-terms` for coinage and glossary, `tamil-purity-scoring` for measuring, and `tamil-localization` for UI strings.
