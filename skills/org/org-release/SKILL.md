---
name: org-release
description: Use when shipping a release — a store build, a service deploy, a model checkpoint, or a public doc set — and the think-then-act rule requires a plan, an approved runbook, and a human confirm before anything changes. Helps you gate the release on safety, data residency, and rollback instead of discovering a blocker at submission.
---

Our release rule is think, then act: no system-changing action without a plan, an approved runbook, and a human confirm, plus one-command rollback on every product. Store submissions add hard external gates, and a data-residency law is a launch gate for anything touching citizen data. This skill owns the release sequence; `org-ethos` owns the values behind it.

## Release gates

| Gate | Applies to | Pass condition | Who blocks it |
|---|---|---|---|
| Safety | Anything reachable by a child | Counsel sign-off + verified parental consent + a documented red-team result | Counsel, release owner |
| Data residency | Any product handling citizen data | No foreign cloud or API in production; data stays in the required jurisdiction | Release owner |
| Signing credentials | Mobile store builds | Store credentials issued and held by the release owner | Release owner |
| Rollback | Every deployable product | One-command rollback written and tested | Release owner |
| Localized strings | Any user-visible text | Native-speaker review recorded per string | Native reviewer |
| Second reviewer | Every PR in the release | Human review within 48 hours | Reviewer |
| Regulated claims | Legal, medical, or financial surfaces | Required expert sign-off recorded | Domain reviewer |

## Workflow

1. **Write the release plan as a green doc** (see `org-doc-authoring`) with the version, the exact commits, the gates in the table above, and the named human who confirms each. A release without a plan is a deploy, not a release.
2. **Check the gates before the build, not after.** Missing signing credentials or expert sign-off is a release-owner gate; discovering it at submission burns days.
3. **Freeze the scope.** Anything merged after the release branch is cut waits for the next release, unless it is a fix for a gate that just failed — and that fix gets its own review.
4. **Verify on the artifact you will ship**, not on `main`: run the test suite, the safety checks where applicable, and the localized-string review against the release build.
5. **Write and test the rollback first.** One command, tested on a staging copy, documented in the runbook. A rollback nobody has run is a hope.
6. **Get the human confirm.** Think-then-act requires an explicit human "go" per system-changing action; the agent proposes and verifies, the human confirms.
7. **Publish the release notes as a blue doc** — version, date, what changed, what is known-broken, and the rollback command — and update the owning docs index in the same change.

## Anti-patterns

- **Releasing without a tested rollback.** Turns a bad deploy into an outage measured in hours; the one-command rule exists precisely for this.
- **Treating data residency as a post-launch task.** It is a launch gate; a product that sends citizen data abroad cannot be "fixed next sprint".
- **Submitting with placeholder model or asset files.** A submission with placeholders fails review or ships a broken app.
- **Skipping the native-speaker pass under release pressure.** Deadline pressure is exactly when a bad localized string ships and becomes public.
- **Marking a release done while a gate is waived.** A waived gate is a documented decision with an owner and a date, not a silent omission.
- **Shipping the release branch without updating the docs index.** The next agent reads a stale version and proposes work against a contract that no longer exists.

Follow `org-ethos` for the value gates; `org-impactful-pr` for the PRs in the release; `org-cross-repo-change` when the release spans repos; `org-doc-authoring` for the plan and release notes; the owning repo's `docs/README.md` for per-repo blockers.
