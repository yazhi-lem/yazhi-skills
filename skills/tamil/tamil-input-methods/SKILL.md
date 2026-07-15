---
name: tamil-input-methods
description: Use when building or configuring a way for users to type Tamil — a keyboard layout, IME, mobile keyboard, or transliteration input field — or debugging why typed keystrokes produce wrong or unrenderable letter sequences. Helps you pick between Tamil99, phonetic, and predictive input models and get the cluster-level editing behaviors (auto-pulli, backspace, reordering) right.
---

Typing Tamil is not "one key per letter": 247+ letters must be produced from ~30 keys, so every Tamil input method is a small state machine that composes aksharas from keystrokes. The three dominant models — the Tamil99 standard layout, phonetic/Tanglish transliteration, and predictive mobile keyboards — make different trade-offs, and all of them live or die on the same editing details: when the pulli is inserted automatically, whether an independent vowel or a vowel sign is emitted, and what backspace deletes. Getting these wrong produces invalid sequences that render as floating marks and poison downstream search.

## Workflow

1. **Pick the input model for the audience.** Tamil99 for users who already type Tamil (government standard, one consonant + one vowel key per akshara); phonetic/Tanglish for the large population that thinks in romanized spelling (`tamil-transliteration` owns the ambiguity handling); predictive/hybrid for mobile, layered on either.
2. **Emit logical-order Unicode, always.** Keystrokes may arrive in any UX order, but the buffer must end up consonant → sign (see `tamil-swaram-vowels`); never insert pre-shaped visual-order sequences.
3. **Implement vowel-key context sensitivity.** The same vowel key produces the independent letter (இ) at a word/syllable start and the dependent sign (ி) after a consonant. This one rule is the core of Tamil99: க key then இ key yields கி, not கஇ.
4. **Implement auto-pulli correctly (Tamil99 rule).** Two consonant keys in a row insert ் between them automatically — typing க க yields க்க (the first becomes mei). Provide the documented escape for genuine consonant-consonant-without-pulli sequences, and *don't* apply auto-pulli in phonetic mode, where "ka" already resolves the vowel.
5. **Decide backspace granularity deliberately and consistently:** delete one code point (lets users fix a wrong vowel sign without retyping the consonant — the common convention) or one whole grapheme cluster (simpler mental model, matches selection behavior). Mixing the two across text fields in one product is the bug users report most.
6. **Validate the composed buffer on every keystroke** with the structural rules (no orphan signs, no double signs, no independent vowel directly after a consonant) and block or auto-correct invalid states rather than committing them.
7. **Test the editing matrix before shipping:** type/delete/retype each of the four sign geometries (right, ligated, left, split), auto-pulli chains (க்க, ற்ற), Grantha letters (ஜ, ஸ்ரீ), and mixed Tamil-Latin input.

## Input model comparison

| Model | Example: typing தமிழ் | Strength | Weakness |
|---|---|---|---|
| Tamil99 (standard layout) | த ம இ ழ ஃ→pulli key* | Fast for trained users; deterministic; govt. standard | Learning curve; needs physical/visual layout |
| Phonetic / Tanglish | `thamizh` → தமிழ் | Zero learning curve for romanized typists | Ambiguous (`l` → ல/ள/ழ); needs candidate ranking |
| InScript (pan-Indic) | Indic-standard positions | Consistency across Indian scripts | Rarely known by Tamil-only users |
| Predictive mobile | partial input + suggestions | Speed on soft keyboards | Needs frequency lexicon; fails on names/rare words |

\*Tamil99 assigns vowels to the left hand, consonants to the right, and derives mei via auto-pulli or the pulli key.

## Anti-patterns / common failure modes

- **Emitting independent vowels after consonants** (கஇ for கி) — the classic naive-IME bug; renders as two letters and never matches correctly-typed text in search.
- **Applying auto-pulli in phonetic mode** — "ka" becomes க்அ or க்க-style garbage; auto-pulli is a Tamil99-layout rule, not a universal one.
- **Backspace deleting whole clusters in one field and code points in another** — users lose trust in editing; pick one granularity product-wide.
- **Committing invalid intermediate states to the text field** instead of holding them in a composition buffer — autocomplete, spell-check, and undo all record the garbage states.
- **Testing only with கா-style right-side vowels** — left-side (கெ) and split (கொ) signs exercise the reordering logic where composition bugs actually live.

For the sign inventory and ordering rules see `tamil-swaram-vowels`; for the full letter grid a layout must reach see `tamil-aksharas`; for Tanglish→Tamil candidate ranking see `tamil-transliteration`.
