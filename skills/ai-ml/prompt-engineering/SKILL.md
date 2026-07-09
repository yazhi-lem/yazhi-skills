---
name: prompt-engineering
description: Use when writing or iterating on prompts for an LLM feature and outputs are inconsistent, ignoring instructions, or vulnerable to user-supplied text overriding your intent. Helps you structure, version, and systematically iterate on prompts instead of hand-tweaking wording until it feels right.
---

Prompt engineering stops being guesswork once you treat prompts as versioned artifacts with a clear structure and a test loop, not as prose you polish until an example looks good. Structure separates stable instructions from untrusted input; iteration is measured against an eval set, not vibes.

## Workflow

1. **Separate system and user content strictly.** System prompt holds role, constraints, output format, and tools — things that never change per-request. User content holds the task and any retrieved/user-supplied data. Never concatenate untrusted data into the system prompt.
2. **Structure the system prompt in sections**: role/goal, constraints (what not to do), output format (with an example), and edge-case handling (what to do when data is missing/ambiguous). Use headers or XML-ish tags (`<context>`, `<task>`) — models parse structured prompts more reliably than a wall of prose.
3. **Decide direct-answer vs chain-of-thought deliberately.** Use direct answers for classification/extraction where reasoning adds latency and cost without accuracy gain. Use explicit step-by-step reasoning for multi-hop, arithmetic, or planning tasks where skipping steps causes errors. Don't default to "think step by step" on everything — it roughly doubles token cost for tasks that don't need it.
4. **Add few-shot examples when format compliance matters more than creativity** — 2-5 examples covering the typical case plus one edge case is usually enough; more than ~8 examples has diminishing returns and eats context budget.
5. **Isolate untrusted input from instructions.** Wrap retrieved documents or user text in clear delimiters and explicitly instruct the model to treat content inside them as data, not commands — this is your main defense against prompt injection, not a guarantee.
6. **Iterate against the eval set, not a handful of manual tries.** Change one variable at a time (wording, example set, temperature) and re-run the full eval set — see `llm-evaluation` for how that set should be built and graded.
7. **Version every prompt** (e.g., `summarize_v3.txt` or a row in a prompt registry) with a changelog note on what changed and why. Never edit a production prompt in place without a diffable version — you need to roll back when a "fix" regresses something else.
8. **Set temperature by task type**: 0-0.2 for extraction/classification/structured output, 0.3-0.7 for general assistant responses, 0.7-1.0 for creative/brainstorming tasks. Default to 0 unless you have a specific reason for randomness.
9. **Feed prompt changes back through regression testing** (`llm-evaluation`) and watch for drift in production (`model-monitoring`) — a prompt that passed eval can still degrade against real traffic distribution shifts.

## Structure decision matrix

| Technique | Use when | Cost |
|---|---|---|
| Direct answer, no CoT | Classification, extraction, short factual Q&A | Lowest latency/tokens |
| Chain-of-thought | Multi-step reasoning, math, planning | 2-4x tokens, higher accuracy on hard tasks |
| Few-shot examples | Strict output format, tone matching | +200-800 tokens per prompt |
| Zero-shot + strong instructions | Well-known tasks, capable models | Cheapest, works less reliably on edge cases |

## Defaults

- Few-shot example count: 2-5 typical, 1 edge case included
- Temperature: 0 for structured/extraction tasks, 0.3-0.7 for conversational, up to 1.0 for creative
- Max prompt iteration cycle: change one variable, re-run full eval set, log result before next change
- Delimiter untrusted content with clear tags (e.g., `<untrusted_input>...</untrusted_input>`) plus an explicit instruction to never follow instructions found inside it

## Anti-patterns

- **Blending user-supplied or retrieved text directly into the system prompt.** This is the single largest prompt-injection surface; keep it in clearly delimited user-turn content instead.
- **Tweaking wording based on 2-3 example outputs.** A change that fixes one example can silently break ten others; always re-run the eval set (`llm-evaluation`).
- **Using chain-of-thought everywhere "to be safe."** It inflates latency and cost and can even hurt accuracy on simple tasks by giving the model room to talk itself into a wrong answer.
- **No version history on prompts.** Editing the live prompt string in place makes regressions impossible to trace or roll back.
- **Over-stuffing few-shot examples.** Beyond ~8 examples, marginal accuracy gains are small while context budget and latency cost keep climbing — trim instead of adding.
