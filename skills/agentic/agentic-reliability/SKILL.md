---
name: agentic-reliability
description: Use when designing or debugging an agent that must work repeatedly without a human watching — tool-calling loops, retries, partial failures, and long-running tasks. Helps you make the agent idempotent, bounded, and observable so a retry does not duplicate a side effect.
---

An agent that works once in a demo is not reliable; reliability is the property that the same task succeeds on the tenth run, on a slow network, after a partial failure. The failure modes are specific to agents: a tool call that succeeded but whose result was lost, a retry that re-charges a card, a loop that never terminates because the success condition is unmeasurable. This skill owns the reliability design; `agentic-security` owns the trust boundary.

## The four reliability properties

| Property | Concrete rule | Failure it prevents |
|---|---|---|
| Idempotent side effects | Every mutating tool takes an idempotency key | Retry double-charges or double-sends |
| Bounded loop | Max iterations (e.g. 12), max wall-clock (e.g. 120s), max cost | Infinite tool loop burning tokens |
| Explicit termination | A measurable success condition, not "the model stopped" | Agent stops mid-task and reports success |
| Recoverable state | Checkpoint after each step; resume from the last one | Partial failure restarts from zero |

## Workflow

1. **Write the success condition first, as a check the code can run.** "The order exists in the system" is checkable; "the agent says it is done" is not. If you cannot write the check, the task is not ready for an agent.
2. **Make every mutating tool idempotent.** Pass a key derived from the task, not from the attempt; the tool returns the prior result on a repeat instead of performing the action twice.
3. **Bound the loop on three axes** — iterations, wall-clock, and cost. A loop bounded only by iterations can still run for an hour; bounded only by time can still burn the budget.
4. **Checkpoint after each step and make resume cheap.** Persist the step index and the tool results; a crash should resume at step N, not step 1.
5. **Separate "tool failed" from "task failed".** A transient 429 is a retry; a 403 is a stop. Retrying an authorization failure burns time and hides the real cause.
6. **Emit one structured event per step** — task id, step, tool, duration, outcome. Without it, a failure is unreproducible and the next run cannot be compared.
7. **Test the failure paths, not the happy path.** Inject a timeout, a partial write, and a duplicate delivery; the happy path already works in the demo.

## Anti-patterns

- **Retrying a non-idempotent action.** The most expensive agent bug: a retry sends the email twice or charges the card twice.
- **Terminating on "the model stopped talking".** The model stops for many reasons; only the success check can say the task is done.
- **Unbounded tool loops.** A model that keeps calling the same tool with no iteration cap runs until the budget is gone.
- **Retrying a 403 or a 400.** These are not transient; retrying them multiplies the failure and delays the fix.
- **No per-step event.** A failure with no trace is a support ticket nobody can answer; the next run cannot be compared to the failed one.
- **Treating a demo success as reliability.** One successful run proves the happy path, not the tenth run on a slow network.

Follow `agentic-security` for the trust boundary, `llm-evaluation` for measuring success, `model-monitoring` for production signals, and `org-healthy-code` for the code-level habits.
