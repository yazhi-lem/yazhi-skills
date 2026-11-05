# Yazhi Harness · Araṃ Harness

Multilingual evaluation for Indian-language AI. Two harnesses, one engine.

| | Yazhi Harness | Araṃ Harness |
|---|---|---|
| Question | Can the model *do* the task in this language? | Does it behave *rightly* in this language? |
| Suites | `flores`, `qa`, `sentiment`, `paraphrase` | `aram` |
| Cases | 55,551 across 11 languages | 198 across 11 languages (18 each) |
| Grading | Deterministic scorers | Deterministic floor + calibrated LLM judge |
| Gate | optional `gate_min_score` | `gate_max_critical: 0` by default |

Araṃ (அறம், "right conduct") generalises the Tamil-only Aram Harness in
`repos/adhan` to all 11 Indian languages and decouples it from any single model
class. Nothing in this package imports a model library: a provider adapter turns
a prompt into text, and everything else is harness.

## Quick start (offline, no model)

```bash
cd packages/harness
python3 -m yazhi_harness.cli list
python3 -m yazhi_harness.cli run --provider sample --suite sample --model demo
python3 -m pytest tests -q          # no network needed
```

## Evaluate a real model

Any OpenAI-compatible endpoint works — `llama-server`, vLLM, Ollama `/v1`, or
yazhi-api:

```bash
python3 -m yazhi_harness.cli run \
  --provider openai --base-url http://127.0.0.1:11434/v1 --model qwen3:1.7b \
  --suite aram --language ta --language hi --language kn \
  --output reports/aram.md
```

Exit codes: `0` pass · `1` CRITICAL gate violation · `3` config error ·
`4` judge rejected by calibration · `5` nothing gradeable (provider down).

## Datasets

```bash
python3 -m yazhi_harness.cli snapshot --all      # ~200 MB, one time
python3 -m yazhi_harness.cli snapshot flores --verify
```

Snapshots are SHA-256 pinned; every report records the manifest digest. See
[docs/LICENSES.md](docs/LICENSES.md) — **two upstreams declare no licence**, and
the harness never commits or redistributes their text.

Reviewed coverage (verified against upstream file trees, not assumed):

| Suite | Languages | Gap |
|---|---|---|
| `flores` | 11 | none |
| `qa` (IndicQA) | 10 | no Urdu upstream |
| `sentiment` | 11 | none |
| `paraphrase` | 9 | no Tamil, no Urdu |

## Design decisions that make the numbers defensible

1. **Errors are never passes.** A provider failure is `error`, not `pass`; above
   10% failed calls a `provider_errors` violation fires regardless of gates. A run
   with no gradeable case exits `5` instead of reporting "✅ PASS".
2. **The judge must earn trust.** It is graded against 12 hand-labelled probes;
   below the agreement bar its verdicts are ignored and the report says so.
   Unparseable judge output (temp 0, strict JSON) is an error, never a pass.
3. **Language is a rubric condition, not an assumption.** An English refusal to a
   Tamil prompt fails, which is the most common real-world failure.
4. **Coverage gaps are printed, not averaged away.** A suite that grades 9
   languages says so; it never claims 11.
5. **Severity ≠ outcome.** `CRITICAL` marks how much a failure matters; provider
   errors are infrastructure and never counted as safety failures.
6. **Synthetic numbers are labelled synthetic.** `yazhi_harness.synthetic` exists
   only to test the harness — see `docs/VALIDATION.md`.

## Architecture

```
yazhi_harness/
  types.py        Case, ModelOutput, SampleResult, RunReport, Severity
  langs.py        11 languages, script ranges, script-ratio arithmetic
  config.py       YAML/JSON config, gates, judge config
  suites.py       suite registry + Araṃ case expansion
  runner.py       config -> provider -> scores -> gates -> report
  report.py       Markdown / JSON / CI summary
  stats.py        Wilson + bootstrap CIs, McNemar, power
  scorers/        script_ratio, translation, exact_match, label, refusal, regex
  safety/         constitution, red_team, judge (+calibration), aram scorer
  datasets/       loaders + snapshot/verify
  providers/      sample, fixture, openai-compatible (stdlib urllib)
  synthetic.py    scripted pseudo-model for testing only
```

## Adding a language

1. Add a row to `langs.LANGUAGES` (and its script range if new).
2. Add native probes for each intent in `safety/constitution.py`.
3. Add refusal markers and red-team prompt text in the language.
4. Add dataset coverage in `datasets/snapshot.py::_COVERAGE`.
5. Run `python3 -m pytest tests -q`; `test_aram_suite_covers_every_language`
   and `test_aram_prompts_are_in_their_own_script` will fail until the set is
   complete — deliberately.

## Adding a provider

Implement `generate(prompt) -> ModelOutput` and register it in
`providers.build_provider`. Return `ModelOutput(text="", error=...)` on failure
rather than raising; the runner also catches exceptions, but explicit errors
carry better diagnostics.

## Limitations (read before quoting a number)

- Tamil, Hindi and the other nine are covered by **different quantities** of
  real data; FLORES is 1,012 sentences, so per-language translation CIs are
  ±3 points at n=1,012 and far wider at the `limit: 20` default.
- Araṃ content-quality dimensions (tone, cultural nuance) are only graded when a
  calibrated judge is configured. Without one, Araṃ grades **language fidelity
  and the refusal floor only**, and the report states exactly that.
- The SuiteRenderer has 9 intents per language; regional political sensitivity
  varies within a language, and native review is still required before trusting
  a green Araṃ result for release.
- No dataset here measures long-context or multi-turn behaviour.
