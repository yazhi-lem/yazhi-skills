---
name: yazhi-harness
description: Use when you need to measure an Indian-language model's actual capability across Tamil, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Telugu and Urdu — before a release, after a fine-tune, or when someone claims a model "works well in Tamil" without numbers. Runs the model-agnostic Yazhi Harness (translation, reading comprehension, sentiment, paraphrase) and produces a report with per-language pass rates, confidence intervals and honest coverage gaps.
---

"Works in Tamil" is a claim, not a measurement. Small changes to a prompt, a tokenizer or a quantisation level move Indic-language quality unpredictably, and English benchmarks hide it entirely. The Yazhi Harness grades capability per language against professionally created corpora, so a regression in Kannada cannot be averaged away by an improvement in Hindi.

## Workflow

1. **Snapshot the corpora once.** Run `python3 -m yazhi_harness.cli snapshot --all` (~200 MB). It records a SHA-256 manifest per dataset; re-check with `snapshot flores --verify` so upstream drift never silently re-baselines your numbers.
2. **Point the harness at whatever serves the model.** Any OpenAI-compatible endpoint works (`llama-server`, vLLM, Ollama `/v1`, yazhi-api). Set `provider.base_url` and `provider.model` in a config, or pass `--base-url`.
3. **Pick suites that match your claim.** `flores` (translation), `qa` (reading comprehension incl. no-answer rows), `sentiment` (3-way), `paraphrase` (sentence-pair judgement). Do not run all four if you only need to gate one product surface — each costs calls.
4. **Set `limit` and `seed`.** 20 cases per language is ~220 calls per suite; below ~30 per language the confidence interval is wider than the differences you're trying to detect.
5. **Run and read the report**, not just the exit code: pass rate, mean, 95% Wilson interval, and a "Failures" block naming each failing case with its reason.
6. **Record known gaps.** IndicQA has no Urdu file; IndicXParaphrase has neither Tamil nor Urdu. The report prints missing languages per suite — quote that list instead of claiming "11 languages" for a 9-language run.
7. **Gate in CI** with `gate_min_score` and watch for the `provider_errors` violation: above 10% failed calls the numbers are infrastructure noise, not signal.

## Suites and what each proves

| Suite | Task | Scorer | Licence | Languages |
|---|---|---|---|---|
| `flores` | Translate English → target | char-F1 + script check | CC-BY-SA-4.0 | all 11 |
| `qa` | Answer from a passage | normalised exact match | CC-BY-4.0 | 10 (no Urdu) |
| `sentiment` | positive/negative/neutral | label match | CC0 | all 11 |
| `paraphrase` | same meaning, yes/no | label match | undeclared — local only | 9 (no Tamil/Urdu) |

## Interpreting scores

| Signal | Meaning | Action |
|---|---|---|
| High `script_ratio`, low score | Wrote the right language, wrong content | Model-quality issue, not a plumbing bug |
| Low `script_ratio` | Answered in English/romanised text | Language-fidelity failure; check system prompt |
| `skip` outcomes | Reference unusable (mis-aligned row) | Investigate the snapshot, never count as pass |
| `provider_errors` gate | Endpoint down or too slow | Fix infra before reading any score |
| Wide CI at n=20 | Cannot distinguish 5-point gaps | Raise `limit` before claiming a win |

## Anti-patterns

- **Reporting one aggregate number across 11 languages.** A 70% average can hide Tamil at 95% and Urdu at 30%; per-language rows are the deliverable.
- **Comparing runs at different `limit`/`seed` values.** Sampling differences look like model improvements. Pin both in the config and commit it.
- **Using the synthetic `ScriptedModel` numbers as results.** It exists to test the harness; its scores say nothing about any model.
- **Treating a `skip` as a pass.** A row the scorer could not grade is a hole in the evidence, not a success.
- **Publishing IndicXParaphrase slices.** It declares no licence; evaluate locally and cite the dataset instead.

Pair this with `aram-harness` before shipping anything safety-sensitive, and see `llm-evaluation` for the statistical reasoning behind the intervals and `model-monitoring` for tracking drift after release.
