---
name: launch-planning
description: Use when planning the rollout of a new product, major feature, or rebrand — deciding launch tier, sequencing announcements, and coordinating teams around a ship date. Helps you avoid the common failure of treating "launch" as a single press-release day instead of a staged sequence with its own success criteria.
---

A launch is a coordinated sequence across product readiness, messaging, channels, and internal enablement — not a single announcement moment. Most launches that "fizzle" didn't fail on messaging; they failed because a dependency (sales wasn't trained, docs weren't live, support didn't know the feature existed) broke on day one and nobody had planned for it.

## Launch tiers

| Tier | Scope | Typical lead time | Coordination needed |
|---|---|---|---|
| Tier 1 (major) | New product, new market, funding/brand milestone | 8-12 weeks | Cross-functional: PR, sales, support, exec comms, paid |
| Tier 2 (significant) | Major feature, meaningful pricing change | 3-6 weeks | Product marketing, sales enablement, docs, lightweight PR |
| Tier 3 (minor) | Incremental feature, small improvement | 1-2 weeks | Changelog, in-app notice, docs update |
| Tier 4 (silent) | Internal tooling, infra change, bug fix | 0 | Release notes only |

Picking the wrong tier is the most common launch-planning mistake in both directions: over-investing PR effort on a minor feature dilutes future launch credibility, and under-investing on a major shift leaves the market and even your own sales team unaware something changed.

## Workflow

1. **Assign a launch tier before planning anything else** — it determines lead time, budget, and which teams need to be in the room. Revisit the tier if scope changes mid-planning; a "minor" feature that turns into a new pricing model has become Tier 2.
2. **Build the plan backward from the ship date**, not forward from "when marketing is ready." List every dependency (docs, support macros, sales deck, legal review, translated assets) with an owner and a deadline at least 3-5 business days before launch day, so slippage has room to absorb without moving the date.
3. **Confirm product readiness with a go/no-go checklist**, not a verbal "should be fine": feature flag rollout plan, rollback path, monitoring/alerting live, known-issues list reviewed by support.
4. **Sequence the announcement across owned, earned, and paid channels deliberately** — owned (blog, changelog, email) goes live first or simultaneously; earned (press, analyst briefings) needs embargo coordination days to weeks ahead; paid amplification starts only once owned assets are confirmed live, not before.
5. **Train internal teams before the external announcement, not after.** Sales and support should never learn about a launch from a customer asking about it — run an internal enablement session at least 3-5 business days ahead, per `sales-enablement`.
6. **Define launch success metrics before launch day**, not retroactively — signups, activation rate, press mentions, or pipeline influenced, matched to the launch tier's actual goal. A Tier 3 feature shouldn't be judged by Tier 1 press-mention targets.
7. **Plan a 2-week post-launch check-in** to review the metrics against target and capture what broke in the dependency chain — this is where the next launch's checklist gets better.
8. **Have a rollback or mitigation plan for the top 2-3 likely failure modes** (a critical bug, a messaging misfire, a competitor counter-announcement) decided before launch day, not improvised live.

## Anti-patterns

- **Treating launch day as the finish line** instead of the start of a measurement window — the real signal (activation, retention, pipeline) shows up over the following weeks, not on day one.
- **Briefing press or partners under embargo without confirming your own internal teams are ready** — an embargo leak or an early customer question with no internal answer ready is entirely avoidable with correct sequencing.
- **Skipping the go/no-go checklist because "the team feels good about it"** — feature flags without a rollback plan, or docs published minutes before the announcement, are the actual cause of most launch-day fires.
- **Over-tiering a minor update** to justify a big push — burns PR/analyst goodwill and paid budget on something that won't sustain the attention, making the next real Tier 1 ask harder to fund.
- **Defining success metrics after the fact** to match whatever numbers came in — removes the ability to honestly assess whether the launch worked and improve the next one.

Cross-reference `positioning-and-messaging` for the messaging hierarchy a launch plan executes against, `sales-enablement` for the internal training this workflow depends on, and `channel-and-partnerships` for coordinating partner-dependent launch moments.
