---
name: tamil-content-writing
description: Use when drafting or reviewing original Tamil copy (marketing, product, documentation) rather than mechanically translating it, and the output needs to read as natural, idiomatic Tamil rather than an English sentence wearing Tamil words. Helps you choose the right register, avoid English-calque phrasing, and keep terminology consistent when working with translators.
---

Tamil has a well-documented diglossia: செந்தமிழ் (formal/literary) in writing, news, and official contexts, versus கொடுந்தமிழ்/பேச்சு தமிழ் (spoken/colloquial) in conversation and casual digital content. Pick a register deliberately and stick to it — and avoid sentence-by-sentence translation from English, which produces grammatically valid but unnatural "calque" Tamil native readers immediately clock as translated.

## Workflow

1. **Choose register before writing a sentence.** Formal documentation, legal/financial copy, and news use செந்தமிழ் conventions (literary verb forms, standard case markers, no colloquial contractions). Marketing copy, chat/support, and casual app UI often work better in a moderated spoken register with contracted verb forms. Mixing registers within one document reads as inconsistent, not friendly.
2. **Draft in Tamil directly for anything persuasive or idiomatic** (marketing taglines, error messages, onboarding copy) rather than translating a finished English draft — English rhetorical structures (short imperative sentences, wordplay, alliteration) often don't carry over, and translators end up either producing a stilted calque or having to rewrite from scratch anyway.
3. **When translation is unavoidable, translate meaning, not sentence structure.** Rewrite for Tamil's verb-final order and drop English-only constructs (passive voice, strings of prepositions) — a literal "Please click the button below to proceed" reads recognizably foreign.
4. **Build and enforce a terminology glossary for technical/product content.** Decide once whether to use a Tamil coinage, a transliterated loanword, or the English term left in Latin script for concepts like "login," "server," "cloud," "dashboard" — and apply that choice consistently. Inconsistent terminology (one screen says உள்நுழை, another says லாகின்) reads as unreviewed and confuses users searching help content. The established terms and the coinage procedure live in `tamil-technical-terms`; for pure-Tamil wording see `tamil-tani-tamil`.
5. **Route through a native reviewer/editor, not just a translator.** A translator can be fluent yet produce grammatically-correct-but-unnatural text; a reviewer asking "does a Tamil speaker actually write this way" catches calque phrasing, wrong register, and terminology drift that accuracy-only QA misses.
6. **Check compound/agglutinative word formation for correctness**, not just individual word choice — Tamil stacks case, number, and tense suffixes onto stems, and incorrect suffix combinations (common when writers think in English morphology) are a frequent, hard-to-spot error.
7. **Re-read final copy aloud (or have a reviewer do so) to catch awkward word order** — verb-final SOV sentences that were assembled by translating English SVO structure often "sound" wrong before a grammar-checker would flag them.

## Register comparison

| Aspect | செந்தமிழ் (formal/literary) | பேச்சு தமிழ் (colloquial/spoken) |
|---|---|---|
| Typical use | Docs, legal, news, official UI | Marketing, chat, casual app copy |
| Verb forms | Full literary conjugations | Contracted spoken forms |
| Pronouns | நீங்கள் (formal "you") | நீ / informal forms, context-dependent |
| Loanwords | Often Tamil-coined equivalents preferred | English loanwords common, often left in Latin script |
| Reader perception if mismatched | Colloquial in formal doc reads unprofessional | Overly formal in chat reads cold/robotic |

## Letter classes and sandhi (புணர்ச்சி)

Tamil letter classes (வல்லினம் hard க ச ட த ப ற, மெல்லினம் nasal, இடையினம் medium — full inventory in `tamil-aksharas`) drive a rule writers get wrong constantly: at word joins, a vallinam consonant often doubles (வல்லினம் மிகும்). மரம் + கிளை → மரக்கிளை; அதைக் கேட்டேன், not அதை கேட்டேன். Omitted or over-applied doubling is the most common spelling error in otherwise fluent copy — add it to the native-review checklist; spell-checkers miss it.

## Common English-calque mistakes

| English-influenced (avoid) | Natural Tamil pattern |
|---|---|
| Overusing passive voice constructions carried over from English | Prefer active, verb-final constructions natural to Tamil |
| Literal word-for-word idiom translation (idioms rarely map 1:1) | Find/use an equivalent Tamil idiom or drop the idiom and state plainly |
| Treating English sentence boundaries as fixed when translating | Tamil often merges or splits clauses differently; translate at paragraph, not sentence, granularity |
| Leaving English SVO order intact with Tamil words substituted in | Reorder to verb-final SOV |

## Anti-patterns / common failure modes

- **Sentence-by-sentence machine-style translation without a native editing pass** — produces grammatically parseable but instantly recognizable "translated" Tamil; always route through review.
- **Mixing formal and colloquial register in one piece** — inconsistent honorifics/verb forms (நீங்கள் in one line, நீ in the next) undermine trust in the content's polish.
- **Inconsistent technical terminology across a product surface** — pick one term per concept and enforce it via a shared glossary; don't let each translator/writer choose independently.
- **Ignoring agglutinative suffix correctness** — bolting the wrong case/plural suffix onto a borrowed or coined term produces a word that's technically parseable but marked as "off" by native readers.
- **Skipping a native-speaker review because the text "translated cleanly"** — clean translation and natural Tamil are different bars; only a native reviewer reliably catches the gap.

See `tamil-localization` for how register/terminology choices interact with UI space and formatting constraints, `tamil-transliteration` for decisions about when to romanize versus coin/borrow terms, `tamil-aksharas` for the letter classes behind the sandhi rules, and `tamil-text-processing` for safe programmatic handling of the Tamil strings this content produces.
