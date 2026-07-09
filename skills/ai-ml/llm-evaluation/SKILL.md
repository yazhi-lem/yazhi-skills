---
name: llm-evaluation
description: Use when you need to know whether a prompt, model, or pipeline change actually made things better, or when you're shipping LLM-backed features without any regression safety net. Helps you build eval sets and choose evaluation methods that produce trustworthy, statistically defensible signal.
---

"It looks better to me" is not an evaluation. LLM systems change behavior unpredictably with small prompt or model tweaks, so you need a repeatable eval set and a method (automated, human, or LLM-as-judge) matched to what you're actually measuring, plus enough samples to trust the result.

## Workflow

1. **Build a labeled eval set before you need one.** Pull 50-200 real (or realistic) input examples covering: common cases, known edge cases, and past failure modes. Store expected outputs or grading criteria, not just inputs — an eval set without ground truth is just a demo script.
2. **Segment the eval set by category** (e.g., "factual lookup," "multi-turn," "refusal cases") so a regression in one slice doesn't get diluted by improvement in another.
3. **Pick your evaluation method per metric** — see table. Don't default to LLM-as-judge for everything; it's convenient but adds its own noise and cost.
4. **For automated metrics**, use exact-match/regex for structured outputs, embedding similarity or ROUGE for loose paraphrase tasks, and custom assertions (JSON schema valid, contains citation, no PII) for pipeline correctness.
5. **For LLM-as-judge**, use a strong, fixed judge model, a rubric with explicit criteria (not "rate 1-10 quality"), and pairwise comparison (A vs B) over absolute scoring when possible — pairwise is more reliable than absolute Likert scores.
6. **Reserve human review** for a 10-20% audit sample and for anything safety- or compliance-sensitive; LLM judges systematically miss subtle factual errors and can share blind spots with the model being judged.
7. **Run regression tests on every prompt or model change**, not just at release time — treat the eval set like a test suite in CI. See `prompt-engineering` for versioning the prompts you're testing.
8. **Check statistical significance before declaring a win.** With n=50-100 and a binary pass/fail metric, a 5-point percentage swing is often noise. Use a bootstrap confidence interval or a paired test (e.g., McNemar's for paired binary outcomes) rather than eyeballing two percentages.
9. **Track eval results over time per prompt/model version** so drift and regressions are visible at a glance — feed this into `model-monitoring` for the production-facing half of the same problem.

## Method comparison

| Method | Cost | Speed | Best for | Weakness |
|---|---|---|---|---|
| Automated (exact/regex/schema) | Low | Fast | Structured output, deterministic tasks | Can't judge nuance, tone, correctness of prose |
| Embedding/statistical similarity | Low | Fast | Paraphrase/semantic closeness | Weak correlation with factual correctness |
| LLM-as-judge | Medium | Medium | Open-ended quality, style, relevance | Judge bias, cost, needs its own validation |
| Human review | High | Slow | Ground truth, safety, subtle correctness | Doesn't scale, slow feedback loop |

## Defaults

- Minimum eval set size before trusting a percentage: 50 examples; 100+ for anything with more than 2-3 outcome classes
- Human audit sample: 10-20% of automated/LLM-judge results, higher for new metrics until validated against human judgment
- Judge model temperature: 0 (deterministic grading)
- Significance threshold: treat differences under ~5 points as noise at n=50 unless a proper significance test says otherwise
- Re-run eval set on every prompt/model/retrieval change — not optional, not "just this once"

## Anti-patterns

- **Eyeballing a handful of outputs and calling it evaluated.** Five good-looking examples tell you nothing about the long tail; use the full eval set.
- **Using the same model as both generator and judge without validation.** Self-preference bias inflates scores; validate judge agreement against human labels first, or use a different/stronger model as judge.
- **Absolute 1-10 scoring instead of pairwise comparison.** Absolute LLM scores cluster and drift; pairwise A/B comparisons are far more stable and reproducible.
- **Declaring victory on small-sample percentage differences.** A jump from 82% to 85% on 50 examples is frequently within noise — run the significance check.
- **Letting the eval set go stale.** An eval set that never gets new failure cases added stops catching new regressions; treat it as a living artifact, not a one-time deliverable.
