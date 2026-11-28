---
name: org-issue-triage
description: Use when validating open issues and PRs across repositories after a strategy reset — aged planning imports, duplicate titles, hard dates, or PRs claiming to close issues. Helps you decide close, keep, or rewrite with evidence without silently discarding contributor work.
---

A planning import can leave a repo with dozens of open issues that no longer describe any current plan, while real work sits in PRs that "close" issues they never actually fix. This skill owns the *validation* pass: for each issue or PR, decide whether it is actionable today, needs a rewrite, or should be closed with a reason. The default is to close stale planning artifacts, not to close work a contributor is still doing.

## Decision table

| Signal | Default action | Evidence required before closing |
|---|---|---|
| Open >60 days, zero comments, bulk-import label or date | Close as stale | No open PR references it and no current doc lists it |
| Hard date in body after a plan reset | Close or rewrite without the date | Check `archives/` and the current docs index first |
| Duplicate/near-duplicate title | Keep the newer or more detailed one; close the other with a link | Compare bodies, not just titles |
| Open PR claims to close it but PR is blocked | Keep the issue open; comment with the blocker | Read the PR's checks and conflicts, not its description alone |
| External author, recent activity | Keep; ask a clarifying question instead | Never close on age alone when someone is actively engaged |

## Workflow

1. **Snapshot the queue before judging it.** Record repo, number, title, author, created/updated dates, labels, comment count, and linked PRs for every open item in scope. A triage decision without a dated snapshot is unreviewable.
2. **Cross-check PR claims mechanically.** For every "closes #N" in an open or merged PR, verify the PR is actually merged or at least passing checks and free of conflicts. A claimed close in a blocked PR is not a closed issue.
3. **Apply the decision table in the order shown**, strongest keep-signal first. Recent external activity outranks age; a live implementation outranks a stale title.
4. **Check the current plan before closing on stale dates.** Look at the repo's `README.md`, `docs/README.md`, and `CONTEXT.md`, then `org-plan-reset-recovery` for retired plans. An issue that matches a current priority is not stale just because it was imported months ago.
5. **Prefer rewrite over close for actionable work with a bad title or date.** Edit the title/body to match current language, keep the issue number and history, and note the change in a comment.
6. **Close in batches with one reason per batch** — e.g. "superseded by the 2026-11-20 plan reset; see docs/README.md" — so authors can appeal a category, not chase individual silences.
7. **Report the numbers** — total reviewed, closed by reason, rewritten, kept with blockers, and any external items left untouched. Include the snapshot date and the repos covered.

## Anti-patterns

- **Mass-closing by age alone.** Deletes live work and external contributions; age is a signal to inspect, not a verdict.
- **Trusting "closes #N" in a PR description.** A blocked or abandoned PR can claim an issue for months while the issue stays open — verify merge state and checks.
- **Deduplicating by title only.** Two similar titles can be genuinely different scopes; compare bodies and acceptance criteria first.
- **Closing an issue whose hard date passed but whose goal is still in the current plan.** Rewrite the date away instead of dropping the work.
- **Silent triage.** Closing without a category-level reason leaves authors unable to tell a deliberate reset from neglect; always comment with the source of truth.

For the file-side equivalent see `org-repo-audit`; for the GitHub write pass that executes these decisions see `yazhi-code-action`; for deciding what is current after a reset see `org-plan-reset-recovery`; for cross-repo sequencing once an issue becomes work see `org-cross-repo-change`.
