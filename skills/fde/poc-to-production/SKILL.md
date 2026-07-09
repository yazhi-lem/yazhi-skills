---
name: poc-to-production
description: Use when a customer POC has proven the concept works and stakeholders are asking "when can this go live?" Helps you decide what must change before a demo-quality prototype can carry real production traffic and real business risk.
---

A POC is optimized to prove a concept fast under a compressed timeline, usually with hardcoded credentials, no retries, and a happy-path-only demo script. Forward-deployed engineers are the ones who get asked to make that same code carry real customer traffic in weeks, and the gap between "it worked in the demo" and "it survives production" is where most FDE engagements go over budget or over deadline. Treat this as a distinct phase with its own gate, not a continuation of POC momentum.

## Workflow

1. **Run a go/no-go review before touching hardening work.** Cap the POC phase at 4 weeks by default (extend only with explicit stakeholder sign-off). At the review, score the POC against the readiness matrix below; anything below "partial" on a required row blocks production planning.
2. **Rewrite error handling first.** Every external call (API, DB, queue) needs explicit timeout, retry-with-backoff, and a defined failure mode (fail closed vs. degrade). POC code that silently swallows exceptions is the #1 source of production incidents in customer environments.
3. **Add observability before adding features.** Structured logs with request IDs, a health-check endpoint, and at minimum three dashboards: request volume, error rate, latency (p50/p95/p99). If you can't answer "is it healthy right now" in under 30 seconds, it's not production-ready.
4. **Load-test against realistic volume**, not demo volume. Get the customer's actual peak traffic numbers (or a documented estimate) during discovery — see `customer-discovery` — and test at 2x that number before committing to a launch date.
5. **Run a security review.** Secrets out of code and into a vault/secret manager, least-privilege service accounts, input validation on every external-facing endpoint, dependency vulnerability scan. Loop in the customer's security team early; see `enterprise-integration` for how access and review cycles typically work.
6. **Define and document handoff criteria** before you build them, not after. Write down what "done" means for support transition — who's on call, what the escalation path is, what counts as an SLA breach.
7. **Stage the rollout.** Shadow traffic or a small percentage canary before 100% cutover; never flip a customer's production traffic in one step. Pair this step with `deployment-runbook` for the actual cutover sequence.
8. **Report the hardening plan and timeline to stakeholders** as a distinct milestone, using `stakeholder-reporting` cadence, so the customer understands why "it already works" still needs weeks of hardening.

## POC-to-production readiness matrix

| Dimension | POC-acceptable | Production-required | Typical gap effort |
|---|---|---|---|
| Error handling | Try/catch, log and continue | Retry with backoff, circuit breaker, defined failure mode | 3-5 days |
| Observability | Console logs | Structured logs, metrics, alerting, dashboards | 3-5 days |
| Scaling | Single instance, manual restart | Autoscaling or documented capacity ceiling, load-tested at 2x peak | 1-2 weeks |
| Security | Hardcoded/local secrets, broad permissions | Secrets manager, least privilege, reviewed by customer security | 1-2 weeks |
| Data handling | Sample/synthetic data | Validated against real data edge cases, PII handling confirmed | 3-7 days |
| Support handoff | None | On-call rotation, escalation doc, runbook | 2-4 days |

## Anti-patterns

- **Demo code ships as-is.** Treating "the POC worked in the meeting" as equivalent to "it's ready." Demos are scripted happy paths; production traffic is not.
- **Hardening without a load test.** Adding retries and logging but never testing at realistic volume — the first real incident becomes the load test, in front of the customer.
- **No go/no-go gate.** Sliding from POC into production work without a checkpoint means nobody explicitly approved the added scope or timeline, which surfaces later as a stakeholder trust problem.
- **Security review as an afterthought.** Scheduling the customer security review after the build is "done" — findings then force a redesign under deadline pressure instead of shaping the build.
- **Undefined handoff.** Reaching launch day without an agreed on-call and escalation plan, leaving the FDE as the permanent single point of failure for support.
