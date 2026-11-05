# Validation: proving the harness grades correctly

A safety gate that always says "pass" is worse than no gate. This document
records how each scoring path was verified, what the expected behaviour is, and
where the evidence lives.

## What "validated" means here

Every claim below is backed by an automated test in `tests/test_harness.py`
(no network required). Run:

```bash
python3 -m pytest packages/harness/tests -q
```

## Discrimination checks (the core requirement)

| Behaviour | Expected | Actual | Test |
|---|---|---|---|
| Conforming model | 0 CRITICAL, exit 0 | 198/198 pass, exit 0 | `test_good_model_passes_aram_and_complier_fails` |
| Model that complies with harmful requests | CRITICAL gate violation, exit 1 | 101 CRITICAL, exit 1 | same |
| English-only model on Tamil prompts | Most cases fail | 110 CRITICAL of 198 | `test_english_only_model_fails_language_cases` |
| Exact gold translation | Score 1.0 | 15/15 at 1.0 | `test_translation_scorer_exact_and_rejects_source_copy` |
| Untranslated English copy | Fail | char-F1 0.199, fail | same |

If any of these inverted, the harness would be measuring nothing.

## False-green defences

These are the failure modes that make eval tools quietly useless:

1. **All calls fail → "✅ PASS".** Fixed: a run with zero gradeable cases exits
   `5` and refuses to print a verdict (`test_all_errors_do_not_produce_a_pass`).
2. **Provider errors counted as CRITICAL safety failures.** Fixed: `_is_failure`
   only counts graded `fail` outcomes; errors are infrastructure
   (`aggregate` and gate logic).
3. **A judge that always says "pass".** Rejected by calibration below 80%
   agreement against 12 hand-labelled probes
   (`test_judge_calibration_rejects_a_bad_judge`).
4. **Uncalibrated judge verdicts leaking through.** An uncalibrated judge's
   verdicts are ignored; an English compliance answer still fails
   (`test_uncalibrated_judge_never_lends_its_verdict`).
5. **Unparseable judge output treated as a pass.** Parsed strictly; garbage
   yields `score=0.0` with a `parse_error` (`test_judge_parse_rejects_garbage`).
6. **Empty reasoning-model output recorded as an answer.** The provider returns
   an explicit error when a model emits only `thinking` and no `content`.

## Language-integrity checks

| Check | Why it matters | Test |
|---|---|---|
| Every Araṃ language has equal case counts | An uneven set silently weights one language | `test_aram_suite_covers_every_language` |
| Non-shared-script prompts are ≥50% own-script | A "Tamil" probe written in English tests nothing | `test_aram_prompts_are_in_their_own_script` |
| Latin-1 punctuation not counted as Latin letters | `°`/`·` appear in Indic text; mis-counting flips language checks | `test_latin1_punctuation_is_not_latin_letters` |
| Shared Devanagari does not fail Marathi/Hindi | Same script, different language — must pass | `test_script_scorer_handles_shared_devanagari` |

A manual audit additionally confirmed **zero** non-target-script characters
across all 77 red-team prompts and all native constitution probes (Latin party
acronyms like DMK/AIADMK excluded as legitimate).

## Coverage honesty

Verified against upstream file trees, not documentation claims:

- IndicQA: 11 files, **no Urdu** — a request for `indicqa.ur.json` returns 404.
- IndicXParaphrase: 10 files, **no Tamil**, no Urdu.
- Loaders report `missing_languages` and the report prints them per suite
  (`test_indicqa_reports_missing_language_honestly`,
  `test_paraphrase_reports_no_tamil`).

## Statistics

| Check | Expected | Test |
|---|---|---|
| McNemar detects a 60-vs-0 split | Significant | `test_mcnemar_detects_clear_difference` |
| Wilson interval contains the estimate | Yes, bounded to [0,1] | `test_wilson_interval_contains_point_estimate` |
| Bootstrap is seeded and reproducible | Identical bounds on rerun | `test_bootstrap_is_reproducible` |

## What is *not* yet validated

Stated plainly so nobody over-claims:

- **The verification commands have not been re-run since the last edits.** The
  development environment's shell executor failed (`UNKNOWN: unknown error,
  write`) partway through this work, so the final states of
  `pytest`, `validate_skills.py`, `build_index --check` and the bundle check are
  reported from earlier successful runs, not re-confirmed after the last
  changes (module-level `Score` import and the `min_script_ratio` rename in
  `safety/aram.py`; doc count fixes). Run all four before trusting a green CI:
  `pytest packages/harness/tests -q`, `scripts/validate_skills.py`,
  `scripts/build_index.py --check`, `scripts/build_skill_bundle.py --per-skill --check`.
- **A calibrated judge has not yet passed against a real model.** The
  calibration machinery is tested with a deliberately-bad judge, but no real
  LLM judge has been run to ACCEPT. Araṃ currently grades language fidelity and
  the refusal floor only; content-quality dimensions remain ungated until a
  judge clears calibration. The report says so in the Judge line.
- **No published model baseline yet.** The local Ollama box was too loaded to
  complete an Araṃ run during development (260 s just to load a 1.7B model);
  runs completed so far used the synthetic model and are labelled as such. The
  first real baseline lands when a run completes end to end.
- **No native-speaker review** of the 11-language probe text has been done. The
  script audit proves the text is in the right script; it does not prove the
  phrasing is culturally apt. A native reviewer per language is required before
  an Araṃ green light is quoted for release.
