---
name: incident-response
description: Use when a security incident is suspected or confirmed — active exploitation, a data leak, a compromised credential, or anomalous access. Helps you classify severity, contain before diagnosing root cause, and run a blameless postmortem afterward.
---

Incident response prioritizes stopping ongoing damage over understanding it. The instinct to fully diagnose root cause before acting is wrong under active compromise — contain first, investigate in parallel, root-cause after. This skill covers classification, escalation, containment, and postmortem structure.

## Workflow

1. **Classify severity immediately** using the table below. Don't wait for full information — classify on worst plausible interpretation and downgrade later if warranted.
2. **Declare the incident and assign an incident commander (IC).** One person owns coordination and decisions; everyone else executes or investigates under their direction. Avoid decision-by-committee during an active incident.
3. **Contain before root-causing.** Revoke the compromised credential, isolate the affected host/service, block the malicious IP/traffic, or disable the vulnerable endpoint — whichever stops the bleeding fastest. This is a reversible, fast action, not the final fix.
4. **Establish a communication cadence** appropriate to severity (see table) and stick to it even when there's "no update" — silence during an incident erodes trust faster than bad news.
5. **Preserve evidence before cleanup.** Snapshot logs, memory, disk state, and relevant traces before rotating credentials or rebuilding systems, or root-causing becomes impossible.
6. **Diagnose root cause once contained.** Now trace how the incident happened — this may hand off to `secure-code-review` or `llm-security-review` findings if the root cause is a code/design flaw, or to `secrets-management` if it's a leaked credential.
7. **Declare resolution explicitly** — state when containment is confirmed stable and monitoring shows no further activity, not just when things "seem quiet."
8. **Run a blameless postmortem within 5 business days** while details are fresh, using the structure below.
9. **Track remediation items to closure**, not just to a backlog that never gets revisited. Assign an owner and a due date to each.

## Severity classification

| Severity | Definition | Response SLA | Comms cadence |
|---|---|---|---|
| SEV1 - Critical | Active exploitation, confirmed data breach, full service compromise | Page on-call immediately, IC assigned within 15 min | Every 30 min |
| SEV2 - High | Suspected compromise, high-impact vuln actively exploitable, partial outage from attack | Response within 1 hour | Every 1-2 hours |
| SEV3 - Medium | Vulnerability found with no evidence of exploitation, contained anomaly | Response within 1 business day | Daily |
| SEV4 - Low | Theoretical risk, policy violation with no exploit path | Response within 5 business days | On resolution |

## Postmortem structure (blameless)

1. **Summary** — what happened, in 2-3 sentences, severity, duration.
2. **Timeline** — timestamped sequence from first signal to resolution, including detection lag.
3. **Impact** — what data/systems/users were affected, quantified where possible.
4. **Root cause** — the underlying condition that allowed it, not just the triggering event. Ask "why" enough times to reach a systemic cause, not a person.
5. **What went well / what didn't** — process and tooling, not individual performance.
6. **Action items** — each with an owner and due date, split into "prevent recurrence" and "reduce detection/response time" categories.

## Anti-patterns

- **Root-causing before containing.** Every hour spent diagnosing while a credential stays live or an endpoint stays exploitable is more damage; contain first, always.
- **No single incident commander.** Diffuse ownership during a SEV1 causes duplicated or contradicting actions.
- **Naming individuals as the cause in a postmortem.** Blame suppresses honest reporting next time; focus on systemic and process causes.
- **Wiping evidence during cleanup.** Rebuilding or rotating before snapshotting logs/state makes root cause analysis impossible.
- **Letting comms cadence lapse when there's no news.** Stakeholders assume the worst from silence; "still investigating, next update in 30 min" is a valid update.
- **Closing the postmortem without tracking action items to completion.** Untracked remediation items are how the same incident recurs.

Findings that reveal a design gap feed back into `threat-modeling`. Code-level root causes get fixed via `secure-code-review`, agent/LLM-specific causes via `llm-security-review`, and credential leaks via `secrets-management`.
