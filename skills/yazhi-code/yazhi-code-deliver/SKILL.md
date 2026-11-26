---
name: yazhi-code-deliver
description: Use when a merged yazhi-code change must reach a client or release channel — package it, deploy it, verify it in the target environment, and close the feedback loop. Helps you move from "merged" to "working for the user" without skipping rollback or localization checks; internal releases use org-release.
---

# Yazhi Code — Deliver to the Client

Merge is not delivery. This skill covers the last leg of the pipeline: turning reviewed code into a working change in the environment the user actually touches, then closing the loop with evidence. It owns the client-facing path; `org-release` owns internal release gates and `deployment-runbook` owns the customer-site procedure.

## Workflow

1. **Confirm the delivered outcome matches the original frame.** Re-read the one-sentence outcome from `yazhi-code-frame`. If the client sees a different result than the frame promised, stop and fix the frame or the code before packaging.
2. **Choose the delivery surface.** Name the exact artifact the client receives: a store build, a web deploy, a model checkpoint, a CLI release, or a customer-environment change. Each surface has a different rollback and verification step; do not treat them as interchangeable.
3. **Run the release and deployment gates for that surface.** Use `org-release` for internal sign-off, `deployment-runbook` for customer sites, and `poc-to-production` when the change is leaving a demo environment. Record which gate was used and who approved it.
4. **Verify in the target environment, not locally.** Check the observable outcome, one regression path, and the Tamil/child-safety strings if the change is user-facing. Local proof from `yazhi-code-handoff` is necessary but not sufficient.
5. **Prepare the rollback before announcing.** Keep the previous artifact retrievable, know the exact command or switch that restores it, and state the condition that triggers a rollback. A release without a tested rollback is a gamble.
6. **Close the loop with the client.** Send a short note: what changed, what was verified, what is deliberately out of scope, and where to report a problem. For customer engagements, follow `stakeholder-reporting`; for product users, keep the same four parts in the release notes.
7. **Watch the first feedback window.** For service changes, check `model-monitoring` or the service's own health signals for one full cycle before calling delivery done. Feed any mismatch back into `yazhi-code-frame` as a new, small frame — never by silently widening the shipped change.

## Delivery surface checks

| Surface | Must verify | Rollback owner |
|---|---|---|
| Store / mobile build | Install path, launch path, Tamil strings, store metadata | `org-release` + store console |
| Web deploy | Route health, one regression flow, backend contract | `org-release` + host rollback |
| Customer environment | Pre-flight, data safety, sign-off, support handoff | `deployment-runbook`, `fde-support-escalation` |
| Model checkpoint | Eval gate, fertility/purity claims, serving path | `model-monitoring`, `llm-evaluation` |
| CLI / library release | Install, help text, exit codes, one user script | `cli-tool-design` |

## Anti-patterns

- **Calling a merge a release.** Code on `main` is not a working client; verify in the target environment before saying it shipped.
- **Announcing before rollback is known.** The first hour after delivery is when a bad artifact is easiest to replace; searching for the rollback command then wastes it.
- **Reusing local proof as client proof.** A passing test suite says nothing about the customer's SSO, fonts, or data shape; run the target-environment check.
- **Silent scope growth after delivery.** Fixing a new request inside the shipped change breaks the frame and the handoff record; open a new frame instead.
- **Dropping Tamil or child-safety checks at the last mile.** The pipeline is only as strong as the final string the user sees; re-check what `yazhi-code-design` called out.
- **No feedback window.** Delivery without a monitored first cycle turns user-reported breakage into the first signal, when it should be the second.

Map to: `yazhi-code-handoff` (input), `org-release`, `deployment-runbook`, `poc-to-production`, `stakeholder-reporting`, and back to `yazhi-code-frame` for follow-up work.
