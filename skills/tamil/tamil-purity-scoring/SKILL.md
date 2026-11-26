---
name: tamil-purity-scoring
description: Use when measuring how pure a Tamil text or corpus is — scoring model output, filtering a pretraining corpus, or verifying a "pure Tamil" claim in a report. Helps you use the real purity formula and token classifier, and avoid the remaining gap that makes both overstate vocabulary purity.
---

Adhan ships two purity measurements. `compute_pure_tamil_purity` in `adhan_slm/eval/thirukkural_eval.py` measures Grantha and Latin contamination; `scripts/pure_tamil_tokens.py` classifies corpus tokens as pure / mixed / non-tamil / special. Both are Tamil-specific — they count Grantha letters and script runs, not vocabulary — so neither is a general "is this pure Tamil" test. This skill owns how to score and how to report the number honestly.

Three bugs in the character formula were fixed in adhan PR #130: the Grantha set omitted ஶ, `set("ஜஷஸஹக்ஷ")` also captured க and the pulli (so every க counted as Grantha), and the denominator ignored Latin script. **Numbers from before that fix are not comparable to numbers after it.**

## What each metric actually measures

| Metric | Formula / rule | Denominator | Blind spot |
|---|---|---|---|
| `compute_pure_tamil_purity` | `(tamil_letters − grantha_letters) / all_letters` | **All letters** (`isalpha`) | Cannot see vocabulary: a Sanskrit stem in Tamil letters scores 1.0 |
| `compute_purity_breakdown` | returns the three counts plus the ratio | — | Same vocabulary limit; use it to separate "no Grantha" from "no Latin" |
| Grantha set in code | `set("ஜஷஸஹஶ")` — five consonants | — | Fixed in #130; க்ஷ and ஸ்ரீ are conjuncts of these, so they need no entry |
| `pure_tamil_tokens.py` | per-token: pure / mixed / non-tamil / special | **All tokens** | Token-level, not document-level; a doc can be "pure" and still ungrammatical |
| Sanskrit stems | not measured at all | — | தர்மம், சந்தோஷம், பிரச்சனை are pure Tamil letters but borrowed words |

## Workflow

1. **Decide the question first** — "is this sentence pure Tamil?" and "what share of this corpus is pure Tamil?" use different tools. A sentence score from the character formula is not a corpus percentage.
2. **Check which version of the metric you are quoting.** Since adhan #130 the Grantha set is the five consonants and the denominator is all letters. A number produced before that fix counts க as Grantha and ignores English — do not mix the two in one report.
3. **Read the breakdown, not just the ratio.** `compute_purity_breakdown` returns `tamil_letters`, `grantha_letters` and `other_letters`; report "Grantha-free" and "no Latin script" as two claims, because the ratio alone cannot separate them.
4. **For corpora, use the token classifier** (`python scripts/pure_tamil_tokens.py --corpus <dir> --docs 20000`) and report the four classes. Use `--min-doc-purity 0.95` when emitting a clean subset, and say which threshold you used.
5. **State the threshold and the sample.** Adhan's tokenizer gate is mean fertility < 1.15; the kid-safety gate is ≥98% red-team pass. A purity number without its threshold and sample size is not comparable to another run.
6. **Score the thing you will ship.** A model's purity on Thirukkural couplets does not predict its purity on a product UI string; score the actual output distribution.
7. **Report the gap, not just the number.** "94.2% Grantha-free; 31% of tokens contain Latin script" is honest; "94% pure Tamil" is not.

## Anti-patterns

- **Quoting "pure Tamil" from the character formula alone.** It measures script, not vocabulary — a Sanskrit stem in Tamil letters scores 1.0, and a report claiming purity is wrong.
- **Quoting pre-#130 purity numbers as current.** The old Grantha set omitted ஶ and counted க/pulli as Grantha; those scores are not comparable with post-fix numbers.
- **Confusing token-level and document-level purity.** A document made of 95% pure tokens can be 40% mixed documents; the two numbers answer different questions.
- **Comparing runs with different thresholds.** A 0.95 threshold and a 0.80 threshold produce different "pure" corpora; always cite the threshold.
- **Scoring a sample and calling it the corpus.** `--docs 20000` is a stride-derived sample; say so, or run `--all`.
- **Treating a high score as grammatical correctness.** Purity measures letters and scripts, not syntax; pure vocabulary over English word order still scores high.
- **Treating Grantha-free as தனித்தமிழ்.** A sentence of pure Tamil letters built from Sanskrit stems (தர்மம், சந்தோஷம்) scores 1.0 and is not pure Tamil; the metric measures script, not vocabulary.

Follow `tamil-tani-tamil` for the writing decision this measures, `tamil-aksharas` for the Grantha inventory, `tamil-morphology-nlp` for corpus tokenization, and `adhan-status` for the current tokenizer gates.
