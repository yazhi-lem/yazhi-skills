---
name: tamil-morphology-nlp
description: Use when building NLP or search features over Tamil text — tokenization, stemming, keyword search, NER, embeddings, or LLM pipelines — and results are poor because whitespace tokens don't match query terms or token counts explode. Helps you handle Tamil's agglutinative morphology and sandhi stem changes so matching works at the lemma level, not the surface-form level.
---

Tamil is heavily agglutinative: a single whitespace-delimited "word" routinely packs a stem plus plural, case, tense, person, and clitic suffixes — மரங்களுக்கு is மரம் (tree) + கள் (plural) + உக்கு (dative), with a sandhi change (ம் → ங்) at the join. English-style NLP assumptions — that whitespace tokens are lemmas, that a light stemmer suffices, that a word list covers the vocabulary — all fail here: the same lemma surfaces in dozens of inflected forms, and the stem itself mutates. Every retrieval and matching feature over Tamil must decide where it stands on morphology, explicitly.

## Workflow

1. **Never equate whitespace tokens with lemmas.** Treat each token as stem+suffixes; searching, deduplicating, or frequency-counting surface forms undercounts every lemma and misses most matches (வீடு, வீட்டை, வீட்டுக்கு, வீடுகள் are one lemma, four surface forms).
2. **Run a morphological analyzer, not a suffix-chopper.** Use an existing Tamil analyzer (Open-Tamil, ThamizhiMorph, or an Indic NLP suite) to lemmatize. Naive suffix stripping fails on sandhi: the oblique stem changes shape (மரம் → மரத்த-, வீடு → வீட்ட-), so removing உக்கு from வீட்டுக்கு still doesn't yield வீடு without an un-doubling rule.
3. **Index and query at the same normalization level.** Whatever pipeline (lemmatize → NFC → cluster-safe casefolding of embedded Latin) runs at index time must run identically on queries — asymmetry here is the top cause of "search finds nothing" bugs (same principle as the transliteration folding in `tamil-transliteration`).
4. **Budget LLM tokens at 3–5× the English count.** Tamil is 3 bytes/character in UTF-8 and most BPE vocabularies fragment it into byte-level pieces; a prompt or chunk-size budget tuned on English text overflows or truncates mid-akshara on Tamil. Measure with the actual tokenizer, and keep chunk boundaries on grapheme clusters (`tamil-text-processing`).
5. **Handle sandhi at word boundaries for compounds and colloquial text.** Compounds fuse with vallinam doubling (மரம் + கிளை → மரக்கிளை — rules in `tamil-content-writing`), and spoken-register text (`tamil-content-writing`'s பேச்சு தமிழ்) uses contracted verb forms formal analyzers may not know; test on the register you actually ingest.
6. **Evaluate on inflected queries, not dictionary forms.** Build the test set from real user queries/logs — mostly inflected — and score lemma-level recall, not exact-match.

## One lemma, many surface forms

| Surface form | Morphemes | Gloss |
|---|---|---|
| வீடு | வீடு | house (nominative) |
| வீட்டை | வீட்ட- + ஐ | house (accusative; oblique stem, doubled ட்) |
| வீட்டுக்கு | வீட்ட- + உக்கு | to the house (dative) |
| வீடுகள் | வீடு + கள் | houses |
| வீடுகளிலிருந்து | வீடு + கள் + இல் + இருந்து | from the houses |
| செய்கிறேன் | செய் + கிறு + ஏன் | I do (verb: stem + present + 1sg) |
| செய்யவில்லை | செய் + ய + வில்லை | did not do |

## Anti-patterns / common failure modes

- **Porter-style suffix stripping ported to Tamil** — without oblique-stem and sandhi reversal it produces non-words and merges distinct lemmas; use a real analyzer.
- **Exact-match or prefix-match keyword search on surface forms** — recall collapses because users type one inflection and documents contain others; lemmatize both sides.
- **Chunking/truncating by character or token count tuned for English** — splits aksharas and blows context budgets; count with the real tokenizer and cut at cluster boundaries.
- **Training/evaluating only on formal written Tamil** — colloquial and social-media text diverges in verb morphology and spelling; a formal-corpus model quietly degrades on it.
- **Treating embedded Latin/Tanglish tokens as noise** — real Tamil text is code-mixed; route romanized tokens through `tamil-transliteration` folding instead of dropping them.

For grapheme-safe mechanics see `tamil-text-processing`; for romanized/code-mixed input see `tamil-transliteration`; for the letter classes behind sandhi rules see `tamil-aksharas`.
