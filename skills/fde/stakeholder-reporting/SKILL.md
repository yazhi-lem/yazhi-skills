---
name: stakeholder-reporting
description: Use when you need to keep both technical and non-technical customer stakeholders informed of progress, risk, and blockers throughout an engagement without either burying them in detail or blindsiding them with a late surprise. Helps you set a reporting cadence and format that builds trust and surfaces risk early without triggering unnecessary alarm.
---

Forward-deployed engineers report to an audience split between engineers who want specifics and executives who want a one-line status — get the format wrong for either and you either lose their attention or lose their confidence. Because FDE work happens inside someone else's timeline and budget, silence is read as risk: a stakeholder who hasn't heard from you in two weeks assumes the worst, even if the work is on track. Reporting is a deliberate, structured part of the job, not overhead around it.

## Workflow

1. **Set the cadence in the kickoff, not after the first problem.** Default cadence: a written async update weekly, plus a live sync every two weeks for engagements over a month; for engagements under 4 weeks (e.g., a `poc-to-production` sprint), a written update every 2-3 business days.
2. **Split the audience explicitly.** Produce two views from the same underlying status: a technical appendix (logs, metrics, specific blockers) for engineers, and a one-paragraph executive summary (status, risk level, decision needed) for non-technical sponsors. Don't make executives read through technical detail to find the one line that matters to them.
3. **Use a consistent status template every time.** Predictability lets stakeholders scan in seconds instead of re-reading structure each time. See the template table below.
4. **Report risk as soon as you see it trending, not once it's a blocker.** A risk flagged early with a mitigation plan reads as competence; the same risk revealed only once it's blocking reads as a surprise and damages trust.
5. **Separate "risk" from "alarm" in language.** State the risk, its likelihood, its impact, and what you're doing about it — never state a risk without a next action attached, since an unattached risk statement reads as helplessness.
6. **Escalate through the stakeholder map you built in discovery**, not around it. Route technical risk to the technical approver and business/timeline risk to the economic buyer — see `customer-discovery` for how that map was built — rather than broadcasting every issue to everyone.
7. **Close the loop on every open item.** Every status update should reference the previous update's open items with an explicit resolved/still-open/escalated status — items that silently disappear erode trust fast.
8. **Tie major status changes to a runbook or milestone event.** Deployment day updates should reference the `deployment-runbook` sign-off gates directly, so stakeholders see status tied to concrete, auditable checkpoints rather than your subjective read.

## Status report template

| Section | Audience | Content | Length target |
|---|---|---|---|
| Executive summary | Economic buyer, sponsor | Overall status (green/yellow/red), one risk if any, one decision needed if any | 3-4 sentences |
| Progress this period | Both | What shipped/validated against the plan | 3-5 bullets |
| Risks and blockers | Both, routed by type | Risk, likelihood, impact, mitigation owner and next action | 1 row per risk |
| Technical detail | Technical approver, daily users | Metrics, logs, specific implementation notes | As needed, appendix |
| Next period plan | Both | What's planned, what decision or access is needed from the customer | 3-5 bullets |

## Anti-patterns

- **Silence between updates.** Going quiet for two-plus weeks because "there's nothing to report yet" — silence is interpreted as risk regardless of intent; send a short update even when progress is incremental.
- **One-size-fits-all reports.** Sending the same dense technical document to an executive sponsor and an engineer — the executive skims past the one line they needed and disengages from future updates.
- **Burying risk in a wall of green status.** Listing a real risk as a minor bullet in an otherwise all-green report so it doesn't get noticed until it's already a blocker — flag it with visible severity the first time you see it trending.
- **Alarmist escalation.** Reporting every minor uncertainty as a red-status crisis — this trains stakeholders to tune out your reports, so real emergencies get the same muted response as routine noise.
- **Status without a next action.** Reporting "X is blocked" with no owner or mitigation step attached, leaving the stakeholder to wonder whether you're on top of it or just observing it.
