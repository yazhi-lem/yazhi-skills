---
name: deployment-runbook
description: Use when you're about to deploy a system into a customer's environment — especially production — and need a written, repeatable procedure rather than tribal knowledge in your head. Helps you structure pre-flight checks, rollback steps, and sign-off gates so a deployment doesn't depend on you personally being awake and reachable.
---

Forward-deployed engineers often deploy into environments they don't fully control, using access that's temporary, on a schedule set by the customer's change window rather than their own convenience. A deployment that only exists as steps in your head fails the moment you're unreachable, or fails silently because nobody agreed in advance what "rolled back successfully" means. A runbook converts a risky, person-dependent event into a checklist anyone on the team can execute or audit.

## Workflow

1. **Draft the runbook at least 3 business days before the deployment window**, not the night before. Circulate it to the customer's technical approver and your own team for review.
2. **Write pre-flight checks as pass/fail items**, not prose. Each item should have an owner and a way to verify it (a command to run, a dashboard to check), not just "confirm X is fine."
3. **Define the rollback trigger explicitly before deployment starts.** Write the exact error-rate or latency threshold that triggers rollback, not "if something looks wrong." Ambiguous triggers cause hesitation exactly when speed matters.
4. **Script the rollback, don't improvise it.** Rollback should be a tested, single command or short sequence, ideally rehearsed in staging. If rollback takes longer to figure out than the deployment itself, you don't have a real rollback plan.
5. **Set a deployment window with a hard stop.** Default to a 2-hour window with a decision point at the 90-minute mark: if not fully validated by then, roll back rather than pushing past the window into an unplanned extension.
6. **Name the escalation path with real humans and channels**, not roles. "Escalate to on-call" is not a plan; "page Jane via PagerDuty, then Slack #customer-incident, then call the customer's IT liaison at this number" is.
7. **Require sign-off gates at each phase transition**: pre-flight complete, deployment complete, validation complete, rollback-window closed. Each gate needs a named approver, not just a checkbox you tick yourself.
8. **Run a post-deployment validation pass** against the success criteria defined during `poc-to-production` hardening — health checks, smoke tests, and a live dashboard check — before declaring the gate closed.
9. **File the completed runbook with timestamps and actual approvers** as the record of what happened; reuse it as the basis for the next deployment's draft and for `stakeholder-reporting` status updates.

## Runbook structure

| Section | Contents | Owner |
|---|---|---|
| Pre-flight checks | Access verified, backups taken, dependencies confirmed, customer notified | Deploying engineer |
| Deployment steps | Ordered, numbered commands/actions, expected output for each | Deploying engineer |
| Validation steps | Smoke tests, health checks, dashboard thresholds to confirm | Deploying engineer + customer technical contact |
| Rollback plan | Trigger conditions, rollback command sequence, expected recovery time | Deploying engineer |
| Escalation path | Named contacts, channels, and order of escalation | Engagement lead |
| Sign-off gates | Named approver per phase, timestamp of approval | Customer technical approver |

## Anti-patterns

- **Tribal-knowledge deployment.** Running the deployment from memory or a personal scratch file instead of a shared, reviewed document — a single point of failure if the deploying engineer is unavailable mid-incident.
- **Vague rollback triggers.** "Roll back if it looks bad" invites debate mid-incident instead of action; define the numeric threshold in advance.
- **Untested rollback.** Writing a rollback plan that has never actually been executed in staging — the first real run of it happens during a live incident, which is the worst possible time to discover it doesn't work.
- **No hard stop on the deployment window.** Letting a deployment run indefinitely "until it's fixed" instead of rolling back at a pre-agreed decision point, turning a contained issue into an extended outage.
- **Self-approved sign-off gates.** The deploying engineer marking their own gates complete with no independent approver, which removes the check that gates exist to provide.
