---
name: org-repo-audit
description: Use when auditing docs, task files, or configuration across multiple yazhi-lem repositories for stale, duplicate, or unhealthy content and the team wants a reduction plan before any edits. Helps you produce a dated, evidence-backed inventory and proposal instead of deleting a live source of truth.
---

Cross-repo audits fail in two opposite ways: the report is a vague "docs are bloated" complaint, or someone starts deleting files before anyone has agreed what is canonical. This skill owns the *report-only* audit pass across Yazhi repos. It turns a sprawl of READMEs, docs indexes, `NEXT_ACTION.md`/`factory/` remnants, and duplicate guides into a classification with an explicit owner and a proposed action per item. Read-only by default: act only when the requester says to act.

## What to inventory

| Artifact | Healthy signal | Stale/unhealthy signal | Canonical owner |
|---|---|---|---|
| `docs/README.md` | `Status/Owner/Verified` header, current links | No verified date, links to `archives/` as if live | Per-repo docs index |
| Root `README.md` | Matches docs index and code | Describes a retired model, stack, or launch date | Repo README |
| Task artifacts (`NEXT_ACTION.md`, `factory/`) | Absent or archived | Dated task lists presented as current plans | `CONTEXT.md` / docs index |
| Roadmaps and plans | One current plan, dated | Two plans disagreeing, or hard dates after a reset | `docs/README.md` + `CONTEXT.md` |
| Duplicate guides | One doc owns a topic | Two docs restate the same procedure with different numbers | The doc cited by code |

## Workflow

1. **Fix scope and date in the output header** — list the repos and commit SHAs inspected, the audit date, and whether the pass is report-only. Without that, findings age into rumor.
2. **Inventory, do not sample.** Walk the repos in scope and collect every candidate file, including files hidden under `docs/`, `.yazhi/skills/`, and root task artifacts. Record path, last-touched date, and the line that makes it look stale.
3. **Classify each item** as *current*, *stale*, *duplicate*, or *retired-but-cited*. Use 60 days without an update as the default stale threshold, but treat a post-reset date (see `org-plan-reset-recovery`) as stale immediately regardless of age.
4. **Check citations before proposing removal.** Search code and live docs for section references — a doc with zero readers is safe to retire; a doc cited by an IAM or data-architecture section must be retired together with its citations.
5. **Estimate savings concretely.** Report bytes/line counts per item and a total proposed reduction; "we can cut a lot" is not a decision-grade proposal. Flag consolidation targets (one doc owning a topic) separately from deletions.
6. **Return a proposal table** with columns: repo, path, class, evidence, proposed action, and verification command. Do not edit anything unless the request explicitly authorizes changes; if it does, apply one repo at a time and re-run the verification command per repo.
7. **Hand off the durable rule, not just the cleanup** — if the sprawl came from a missing ownership rule, add it to `technical-documentation` rather than re-explaining it in each PR.

## Anti-patterns

- **Deleting first, asking later.** Removes a doc that a code comment still cites and turns an audit into an incident.
- **Counting lines instead of checking authority.** A short stale roadmap outranks a long current index if the former still drives work; verify ownership before ranking by size.
- **Using a single staleness threshold for everything.** A 60-day-old API guide may be current; a one-day-old plan dated before a strategy reset is not.
- **Reporting duplicates without naming the winner.** Two docs with no chosen owner get both edited and drift again within a week.
- **Re-deriving repo state from memory or old session notes.** Read each repo's current `README.md`, `docs/README.md`, and `CONTEXT.md`; the previous session's snapshot is a hint, not evidence.

For the classification of issues and PRs rather than files see `org-issue-triage`; for what counts as current after a reset see `org-plan-reset-recovery`; for the doc header and archive rules see `technical-documentation`; for the repo map see `yazhi-org-status`.
