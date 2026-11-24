---
name: fde-support-escalation
description: Use when a deployed customer system starts failing in production and you need to triage, contain, and escalate without losing the customer's trust. Helps you separate a support ticket from an incident and hand off with evidence instead of a narrative.
---

The transition from "the POC worked" to "the customer depends on it" is where support becomes an engineering function. A production failure at a customer site has three clocks running: containment (stop the damage), communication (tell the customer what is happening), and diagnosis (find the cause). Running them in the wrong order — diagnosing silently while the customer waits — is the most common way a technical fix still loses the account. This skill owns the support path; `incident-response` owns the security incident path.

## Triage classes

| Class | Signal | First action | Escalation |
|---|---|---|---|
| Support question | "How do I…" | Answer from docs | None |
| Bug | Wrong result, no outage | Reproduce, file with evidence | Engineering ticket |
| Degraded | Slow or partial | Contain, then diagnose | On-call |
| Outage | System down or data at risk | Contain first, communicate second | On-call + customer contact |
| Security incident | Suspected breach | Freeze and escalate | `incident-response` |

## Workflow

1. **Classify before acting.** A support question answered as an incident wastes the customer's and the on-call's time; an outage handled as a ticket delays containment.
2. **Contain first on anything degraded or worse.** Roll back, disable the failing path, or fail closed — the rollback command should already exist from the deployment runbook, not be invented under pressure.
3. **Communicate on a clock, not on progress.** Say what is known, what is not, and when the next update is, even if the update is "no change". Silence reads as incompetence; a scheduled "still working" reads as control.
4. **Capture evidence before you fix.** Logs, the request that failed, the customer's environment, and the timestamps. A fix without evidence cannot be verified and will recur.
5. **Separate the customer's narrative from the system's record.** The customer reports the symptom; the logs report the cause. Use both, but diagnose from the logs.
6. **Escalate with a written handoff** — class, timeline, containment already taken, evidence links, and the open question. An escalation that starts with "it's broken" makes the on-call redo the triage.
7. **Close with a cause and a prevention**, not just a fix. Update the runbook, add the check that would have caught it, and tell the customer what changed.

## Anti-patterns

- **Diagnosing silently while the customer waits.** The technical fix lands, the trust does not; communicate on a clock from the first minute.
- **Fixing before containing.** A restart that loses the evidence and leaves the failure in place; contain first, then diagnose.
- **Escalating without evidence.** The on-call redoes the triage and the customer waits twice as long.
- **Treating every report as an incident.** Burns the on-call's attention and makes real outages slower to escalate.
- **Closing on "it works now".** No cause, no prevention, and the same failure returns next month.
- **Improvising a rollback during an outage.** The one-command rollback is part of the deployment runbook; discovering it does not exist at 2am is the failure.

Follow `deployment-runbook` for the rollback and environment baseline, `incident-response` for security incidents, `stakeholder-reporting` for the customer-facing update, and `org-ethos` for the எண்ணித் துணிக human-confirm gate.
