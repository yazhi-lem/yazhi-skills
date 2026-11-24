---
name: tamil-tani-tamil
description: Use when writing Tamil copy that should be தனித்தமிழ் — replacing வடமொழி (Sanskrit) loanwords, Grantha letters, and English code-switching with native Tamil while keeping the sentence grammatical. Helps you pick the right native word per term and avoid the calque phrasing that makes translated Tamil obvious.
---

தனித்தமிழ் (tani-tamil, "pure Tamil") is the movement associated with Maraimalai Adigal and பாரதிதாசன்: write Tamil with Tamil words, not Sanskrit borrowings. In practice it is not a blanket ban — it is a per-term decision about வடமொழி loanwords (தர்மம், யுத்தம், சந்தோஷம்), Grantha letters (ஜ ஶ ஷ ஸ ஹ), and English code-switching. Adhan's Aram harness tests it as "Linguistic Purity" and Illakiya's writing prompt states the rule directly. This skill owns the Tamil-specific decision; `tamil-purity-scoring` owns the measurement.

## The three substitutions that actually matter

| Pattern | Common borrowing | தனித்தமிழ் form | Note |
|---|---|---|---|
| Sanskrit abstract noun | தர்மம் | அறம் | The flagship case — Yazhi's own five rules use அறம் |
| Sanskrit abstract noun | சந்தோஷம் | மகிழ்ச்சி | Both are understood; மகிழ்ச்சி is the native register |
| Sanskrit abstract noun | பிரச்சனை | சிக்கல் | பிரச்சனை is colloquial; சிக்கல் reads as edited Tamil |
| Sanskrit abstract noun | யுத்தம் | போர் | Same for சமாதானம் → அமைதி |
| Sanskrit abstract noun | சுதந்திரம் | விடுதலை | விடுதலை is the modern political register |
| Grantha-letter word | ஜனம், ஷரீரம், ஸ்தலம் | மக்கள், உடல், இடம் | Removing the Grantha letter removes the loan |
| Grantha-letter word | ஹாஸ்பிடல் | மருத்துவமனை | Loan kept in speech, native in writing |
| English code-switch | "meeting-க்கு வர்றீங்களா" | கூட்டத்திற்கு வருகிறீர்களா | Replace the English noun, keep Tamil grammar |

## The Tamil-specific traps

1. **Sanskrit sandhi breaks Tamil sandhi.** வடமொழி compounds follow Sanskrit rules (e.g. ராஜ + ரிஷி → ராஜரிஷி), so a borrowed word often refuses the வல்லினம் doubling and புணர்ச்சி that native Tamil requires. If you swap a Sanskrit noun into a Tamil sentence, re-check the புணர்ச்சி at the join instead of assuming the original sentence still parses.
2. **The -ம் / -த்துவம் / -தை suffixes carry Sanskrit grammar.** Words like மவுனம், தைரியம், சுதந்திரம் are Sanskrit stems wearing Tamil endings. Replacing the noun often means rebuilding the sentence, not swapping one word.
3. **Grantha letters are the tell.** ஜ ஶ ஷ ஸ ஹ and க்ஷ do not occur in native Tamil words. Any of them in a "pure" sentence means a loan is still present — find it before claiming the text is தனித்தமிழ்.
4. **Register decides whether the loan is wrong.** கூட்டம் is native and everyday; ஹாஸ்பிடல் is a loan that speech keeps. Writing ஹாஸ்பிடல் in a product UI is a defect; writing it in dialogue is not.

## Workflow

1. **Fix the register first.** Formal/literary (செந்தமிழ்) demands near-pure Tamil; casual speech tolerates loans. Decide before hunting for words.
2. **Scan for the three markers** — Grantha letters, Sanskrit stems ending in -ம்/-த்துவம், and Latin-script English nouns. Each hit is a candidate, not automatically a defect.
3. **Swap with the substitution table above**, then rebuild the sentence. If the swap leaves the verb agreeing with a different noun, rewrite the clause.
4. **Re-check புணர்ச்சி and வல்லினம்** at every join you touched; borrowed nouns rarely trigger the doubling native Tamil expects.
5. **Keep proper nouns and brands.** யாழி, Adhan, Illakiya, and Firebase are names, not loanwords — never translate them.
6. **Have a native speaker read the result aloud.** A sentence can be pure and still wrong; the ear catches what the word list cannot.
7. **Record the decision** in the glossary owned by `tamil-technical-terms` so the next document does not re-litigate it.

## Anti-patterns

- **Purging every loan regardless of register.** Replacing everyday speech words makes dialogue stiff and unnatural — தனித்தமிழ் is a writing standard, not a ban on how people talk.
- **Swapping the noun and leaving the Sanskrit sentence shape.** The commonest failure: pure vocabulary inside a translated clause structure, which native readers still clock as translation.
- **Missing the Grantha letter.** ஜ, ஷ, ஸ, ஹ, ஶ, க்ஷ in a supposedly pure line means the claim is false — scan before asserting.
- **Translating brand and product names.** யாழி stays யாழி; renaming it breaks search, docs, and the store listing.
- **Treating தனித்தமிழ் as anti-Sanskrit politics.** The goal is clearer Tamil for the reader, not a purity score; a sentence that reads worse after the swap should be reverted.
- **Asserting purity without a measurement.** "Pure Tamil" is a claim; `tamil-purity-scoring` turns it into a number, and the two shipped measures both overstate it.

For the word list see `tamil-technical-terms`; for the numbers see `tamil-purity-scoring`; for register and general copy quality see `tamil-content-writing`; for the model's own purity gate see `org-ethos` and `adhan-status`.
