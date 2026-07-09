---
name: fine-tuning-workflow
description: Use when considering fine-tuning a model for a task, or when a fine-tuning run has finished and you need to know if it actually helped without breaking other capabilities. Helps you decide if fine-tuning is warranted and run the data prep, training, and regression-check workflow correctly.
---

Fine-tuning is the most expensive, slowest, and highest-risk lever for improving LLM behavior — it should be the last thing you reach for, not the first. Most "we need to fine-tune" situations are solved faster and more cheaply by better prompts or retrieval; reach for fine-tuning only when those provably hit a ceiling.

## Workflow

1. **Rule out prompt/RAG first.** Spend real effort on `prompt-engineering` (few-shot, structure, CoT) and `rag-pipeline-design` (if the task needs external knowledge) and measure with `llm-evaluation`. Fine-tune only if the eval plateau is a formatting/style/latency/cost problem that prompting can't fix — e.g., you need consistent structured output at high volume with lower per-call latency and no room for a long system prompt.
2. **Confirm the task is stable and high-volume.** Fine-tuning pays off for narrow, repeated tasks (classification, structured extraction, house style/tone) run thousands+ of times, not for a task whose requirements are still shifting weekly.
3. **Collect and clean training data.** Aim for at least 200-500 high-quality examples as an absolute floor for lightweight fine-tunes (LoRA/adapter-style), 1000+ for more ambitious behavior changes. Quality over quantity: deduplicate, remove contradictory labels, and balance classes/scenarios — a few hundred clean examples beat several thousand noisy ones.
4. **Split train/eval properly.** Hold out 10-20% as an eval split that is never touched during training, and keep it representative of production distribution, not just the easy cases. Also keep a separate untouched "regression" set of general-capability tasks (see step 6).
5. **Start with the lightest-weight method that could work**: LoRA/adapter fine-tuning or a hosted fine-tuning API before full-parameter fine-tuning — cheaper, faster, and far less prone to catastrophic forgetting.
6. **Guard against catastrophic forgetting.** Fine-tuning on a narrow dataset can silently degrade unrelated capabilities (general instruction-following, safety behavior, other tasks the model previously handled). Before and after training, run the model against a general-capability regression suite, not just your target-task eval.
7. **Evaluate post-fine-tune on three axes**: task metric improvement (did it get better at the target task?), regression suite (did anything break?), and held-out eval set performance vs. the base model + best prompt (is it actually beating a well-engineered prompt?). Use the same methodology as `llm-evaluation`.
8. **Ship with a rollback path.** Keep the base model + prompt as a fallback route, and version the fine-tuned model artifact/checkpoint just like a prompt version.
9. **Monitor post-deployment** for drift as real traffic diverges from training data distribution — see `model-monitoring`.

## Fine-tune vs. alternatives

| Approach | Best for | Cost/effort | Risk |
|---|---|---|---|
| Prompt engineering | Most tasks, fast iteration | Low | Low |
| RAG | Tasks needing external/current knowledge | Medium | Low-medium |
| LoRA/adapter fine-tune | Narrow, high-volume, stable task; style/format control | Medium | Medium (forgetting, needs eval) |
| Full fine-tune | Deep behavior change, when adapters plateau | High | High (forgetting, cost, retraining cadence) |

## Defaults

- Minimum training examples: 200-500 (adapter-style), 1000+ (deeper behavior change)
- Train/eval split: 80/20 or 90/10, eval set representative of production traffic
- Separate general-capability regression suite: 50-100 examples spanning unrelated tasks
- Re-run full eval + regression suite after every training run, not just the first one
- Keep base-model-plus-prompt as a documented fallback for at least one release cycle

## Anti-patterns

- **Fine-tuning before exhausting prompting and RAG.** It's slower to iterate, costs more, and risks forgetting — validate the ceiling first.
- **Training on a small, unvetted dataset scraped together quickly.** Noisy or contradictory labels teach the model inconsistent behavior; clean and dedupe before training.
- **Skipping the general-capability regression suite.** A model that improved on your target task but lost instruction-following or safety behavior elsewhere is a net loss you won't see without testing for it.
- **Evaluating only on the fine-tuning eval split.** That split shares distributional quirks with training data; also test against fresh, truly held-out production-like examples.
- **No rollback plan.** Treat the fine-tuned model as a deployable artifact with a version and a fallback, exactly like a prompt or code release.
