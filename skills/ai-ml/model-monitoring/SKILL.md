---
name: model-monitoring
description: Use when an LLM-backed feature is live in production and you need to know it's working — not just that it returns 200s, but that latency, cost, and answer quality stay within bounds and you find out about drift before users complain. Helps you set up the metrics, alerting thresholds, and feedback loops specific to LLM systems.
---

Standard uptime monitoring tells you nothing about whether an LLM system's answers are still good — a service can be fast, cheap, and confidently wrong. LLM monitoring needs its own signals: latency and cost per call, output-quality drift, hallucination indicators, and a feedback loop that routes real failures back into your eval set.

## Workflow

1. **Instrument the basics per call**: latency (time-to-first-token and total), input/output token counts, cost, model/prompt version, and a request ID that ties back to logs. Without prompt/model version tagging, you can't attribute a quality change to a specific rollout.
2. **Track cost at the granularity you can act on** — per feature, per user tier, per prompt version — not just a single account-wide dollar figure. A single verbose prompt change can silently 3x spend.
3. **Set latency SLOs per interaction type**: e.g., p95 time-to-first-token under 1-2s for chat, and a hard timeout (10-30s typical) with graceful degradation for batch/agentic calls. Alert on p95/p99, not just averages — averages hide the tail that users actually feel.
4. **Sample production outputs for quality monitoring.** Continuously score a random 1-5% sample (or 100% for low-volume systems) with the same automated/LLM-judge methodology from `llm-evaluation`, and track the score as a time series, not a one-off audit.
5. **Watch for output-quality drift**, not just absolute score drops: rising refusal rate, shrinking/lengthening output length, format-validation failure rate, and increasing rate of "I don't know" or hedging language are all early signals before user complaints show up.
6. **Build hallucination-detection signals appropriate to the system**: for RAG, track citation/groundedness (does the answer's claims map back to retrieved context?); for general generation, spot-check factual claims against a reference set or use a groundedness-focused LLM judge. No single signal is definitive — combine 2-3.
7. **Close the feedback loop.** Route user-flagged bad responses, low-score sampled outputs, and support escalations into a queue that periodically feeds new hard cases back into the eval set (`llm-evaluation`) and, if patterns emerge, prompt fixes (`prompt-engineering`) or fine-tuning data (`fine-tuning-workflow`).
8. **Set alert thresholds that page a human**, not just dashboards nobody looks at: e.g., error rate >2% over 5 min, p95 latency >2x SLO for 10 min, quality-sample score drop >10 points week-over-week, cost >150% of trailing 7-day average.
9. **Review dashboards on a cadence**, not only when paged — weekly for quality/cost trends, since drift is often too gradual to trigger a hard alert threshold.

## Signals to monitor

| Signal | What it catches | Typical threshold |
|---|---|---|
| p95/p99 latency | Slow provider, prompt bloat, retrieval slowness | p95 < 1-2s (chat), SLO-specific for batch |
| Cost per request/feature | Prompt bloat, runaway token usage, retries | Alert at >150% of 7-day rolling average |
| Refusal / hedge rate | Prompt regression, model swap side effects | Alert on >2x baseline week-over-week |
| Output-format validity rate | Silent breakage in structured-output tasks | Alert if <98% valid (schema-critical paths) |
| Sampled quality score | General quality drift | Alert on >10 point drop vs. trailing baseline |
| Groundedness/citation rate (RAG) | Hallucination against retrieved context | Alert if <90% of claims traceable to context |
| User feedback / flag rate | Real-world dissatisfaction | Alert on sustained rate increase, not single spikes |

## Defaults

- Quality sampling rate: 1-5% of production traffic (100% if volume is low, e.g., <1k calls/day)
- Alert on error rate: >2% over a 5-minute window
- Alert on latency: p95 exceeds SLO by 2x for 10+ minutes
- Alert on cost: >150% of trailing 7-day rolling average
- Feedback loop cadence: weekly triage of flagged/low-score outputs into the eval set

## Anti-patterns

- **Monitoring only HTTP status codes and uptime.** A 200 response with a hallucinated or malformed answer looks identical to a good one at the infra layer.
- **Alerting on averages instead of percentiles.** Average latency can look fine while a meaningful slice of users hit multi-second stalls.
- **No prompt/model version tags on logs.** When quality shifts, you need to know which version caused it — untagged logs make root-causing a rollout regression nearly impossible.
- **Treating the quality sample as a one-time audit.** Quality drift is gradual; without a continuous time series you'll only notice after it's been bad for weeks.
- **Collecting feedback but never routing it anywhere.** Flagged bad outputs that don't feed back into the eval set (`llm-evaluation`) or prompt iteration (`prompt-engineering`) are wasted signal.
