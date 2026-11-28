---
name: tamil-purity-scoring
description: Use when measuring how pure a Tamil text or corpus is — scoring model output, filtering a pretraining corpus, or verifying a "pure Tamil" claim in a report. Helps you use a character formula and a token classifier honestly, and avoid the remaining gap that makes both overstate vocabulary purity.
---

A corpus pipeline usually ships two purity measurements: a character formula for Grantha and Latin contamination, and a token classifier for pure / mixed / non-Tamil / special tokens. Both are Tamil-specific — they count Grantha letters and script runs, not vocabulary — so neither is a general "is this pure Tamil" test. This skill owns how to score and how to report the number honestly.

A past formula fix changed the Grantha set and the denominator. **Numbers from before a formula change are not comparable to numbers after it.**

## What each metric actually measures

| Metric | Formula / rule | Denominator | Blind spot |
|---|---|---|---|
| Character formula | `(tamil_letters − grantha_letters) / all_letters` | **All letters** (`isalpha`) | Cannot see vocabulary: a Sanskrit stem in Tamil letters scores 1.0 |
| Breakdown helper | Returns the three counts plus the ratio | — | Same vocabulary limit; use it to separate "no Grantha" from "no Latin" |
| Grantha set | The five Grantha consonants plus their conjuncts | — | A wrong set silently changes every score; version it |
| Token classifier | Per-token: pure / mixed / non-Tamil / special | **All tokens** | Token-level, not document-level; a doc can be "pure" and still ungrammatical |
| Sanskrit stems | Not measured at all | — | தர்மம், சந்தோஷம், பிரச்சனை are pure Tamil letters but borrowed words |

## Workflow

1. **Decide the question first** — "is this sentence pure Tamil?" and "what share of this corpus is pure Tamil?" use different tools. A sentence score from the character formula is not a corpus percentage.
2. **Check which version of the metric you are quoting.** Record the Grantha set and denominator; a number produced before a formula fix is not comparable with one produced after.
3. **Read the breakdown, not just the ratio.** Report "Grantha-free" and "no Latin script" as two claims, because the ratio alone cannot separate them.
4. **For corpora, use the token classifier** and report the four classes. State the sample size, the sampling method, and the threshold used for a clean subset.
5. **State the threshold and the sample.** A purity number without its threshold and sample size is not comparable to another run.
6. **Score the thing you will ship.** A model's purity on classical couplets does not predict its purity on a product UI string; score the actual output distribution.
7. **Report the gap, not just the number.** "94.2% Grantha-free; 31% of tokens contain Latin script" is honest; "94% pure Tamil" is not.

## Anti-patterns

- **Quoting "pure Tamil" from the character formula alone.** It measures script, not vocabulary — a Sanskrit stem in Tamil letters scores 1.0, and a report claiming purity is wrong.
- **Quoting pre-fix purity numbers as current.** A changed Grantha set or denominator makes old and new scores incomparable.
- **Confusing token-level and document-level purity.** A document made of 95% pure tokens can be 40% mixed documents; the two numbers answer different questions.
- **Comparing runs with different thresholds.** A 0.95 threshold and a 0.80 threshold produce different "pure" corpora; always cite the threshold.
- **Scoring a sample and calling it the corpus.** Say it is a sample, or run the full corpus.
- **Treating a high score as grammatical correctness.** Purity measures letters and scripts, not syntax; pure vocabulary over English word order still scores high.
- **Treating Grantha-free as தனித்தமிழ்.** A sentence of pure Tamil letters built from Sanskrit stems (தர்மம், சந்தோஷம்) scores 1.0 and is not pure Tamil.

Follow `tamil-tani-tamil` for the writing decision this measures, `tamil-aksharas` for the Grantha inventory, and `tamil-morphology-nlp` for corpus tokenization.
