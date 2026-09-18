---
name: security-posture-health-check
description: Use when running a periodic security review of an already-shipped system — a quarterly audit, a pre-funding/compliance due-diligence pass, or picking up ownership of a codebase someone else built. Helps you assess overall security health with a repeatable scorecard instead of an unstructured "looks fine to me" pass that misses slow-accumulating debt.
---

A one-time security review (`threat-modeling` at design time, `secure-code-review` per PR) doesn't catch what accumulates *between* reviews: dependencies that quietly go unpatched, access grants nobody revoked after someone left, logging that silently stopped firing months ago. A security health check is a periodic, scored pass across the whole system to catch this drift before it becomes an incident — the point isn't finding a single critical bug, it's measuring whether the system's overall security posture is improving, flat, or decaying.

## Health scorecard

| Dimension | Green | Yellow | Red |
|---|---|---|---|
| Dependency freshness | All deps patched within 30 days of a critical CVE | Some patched within 90 days | Known critical CVEs unpatched 90+ days |
| Access review | Access reviewed quarterly, offboarding revokes same-day | Reviewed annually | No review process; ex-employees/contractors still have access |
| Secrets hygiene | All secrets in a vault, rotated on schedule | Some plaintext env vars, no rotation schedule | Secrets in source control or shared documents |
| Logging & alerting | Auth failures, privilege escalation, and data exports are logged and alerted | Logged but not alerted on | Not logged — an incident would be invisible until reported externally |
| Patch/update cadence | OS, runtime, and framework versions current within one major version | One version behind | Multiple major versions behind or end-of-life |
| Security debt backlog | Findings tracked, triaged, and closed within SLA | Tracked but no SLA, backlog grows | Findings live in old tickets/Slack threads, no tracking system |

## Workflow

1. **Score each dimension independently** rather than producing one overall "security score" — a system can be excellent on secrets hygiene and terrible on access review, and averaging those hides the actionable signal.
2. **Pull real data, not impressions**: run `npm audit`/`pip-audit`/equivalent for dependency freshness, pull the actual IAM/access list for the access review row, grep for hardcoded credentials for secrets hygiene — a health check based on asking the team "is this fine?" reproduces whatever blind spot let the issue accumulate in the first place.
3. **Check offboarding specifically, not just current access.** Pull the list of people who left or changed roles in the last review period and confirm every one of their access grants was revoked the same day, not "eventually."
4. **Verify alerting fires, don't just check that logging exists.** A system that logs auth failures to a file nobody reads is functionally the same as not logging at all — trigger a test event and confirm a human gets notified.
5. **Track every finding to closure with an SLA by severity** (e.g., critical: 7 days, high: 30 days, medium: 90 days) — an untracked finding in a chat thread has a near-zero chance of getting fixed once the conversation moves on.
6. **Compare this review's scorecard to the last one.** The trend (improving, flat, decaying) matters more than the absolute score at any single point in time — a system stuck at "yellow" for three consecutive quarters is a process failure even if nothing is currently on fire.
7. **Set the review cadence to match the system's change rate and risk**: quarterly for actively-developed systems handling sensitive data, semi-annually for stable low-risk internal tools — and put the next review on the calendar before this one ends, since "we'll do it again sometime" reliably means "we won't."
8. **Escalate any red-dimension finding immediately**, don't wait for the report to be finalized — a health check that surfaces a critical unpatched CVE should trigger action that day, not sit in a document until the quarterly readout meeting.

## Anti-patterns

- **Producing a single averaged security score** — masks a critical red dimension behind several green ones and gives false reassurance to whoever reads only the headline number.
- **Basing the review on team self-report instead of pulled data** — "we rotate secrets regularly" is not evidence; the actual rotation timestamps in the vault are.
- **Checking that access review happens without verifying offboarding specifically** — a quarterly access review that never catches an ex-contractor's still-active API key is not actually doing its job.
- **Confirming logs exist without confirming alerts fire** — undetected logging is indistinguishable from no logging at all when it matters, during an actual incident.
- **Letting findings sit untracked between review cycles** — a health check with no follow-through mechanism becomes a quarterly ritual that documents the same unfixed issues every time instead of driving them to closure.

Cross-reference `environment-security-hardening` for the infrastructure-layer checks this scorecard pulls from, `secrets-management` for the rotation/vault practices behind the secrets-hygiene row, and `incident-response` for what happens when a red finding turns out to already be an active compromise.
