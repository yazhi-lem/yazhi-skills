---
name: yazhi-work-start
description: Use when an individual contributor starts a session and needs their identity, repository, and task focus settled before touching code. Reads the Plane tracker and repository metadata to produce one start brief and one first move; it does not edit code or change tracker state.
---

Memory costs an hour to re-derive who you are, what you own, and which task is due. This skill is the session init: it resolves the contributor against Plane, picks one task and one repo, and writes a brief the rest of the chain can execute. Plane is the task source of truth; this skill reads it, never writes it.

## What Plane owns

| Source | Plane object | Used for |
|---|---|---|
| Person | Member (email, display name, ID) | Identity |
| Open work | Issue (state, assignee, target date, priority) | Today's task |
| Projects | Project (identifier, name, lead) | Repo mapping |
| Cycles | Cycle (name, start and end) | Weekly focus, if current |
| Code | GitHub PRs/issues or local repo | Authored PRs and review queue |
| Freshness | Issue `updated_at` or last webhook | Stale-data warning |

## Workflow

1. **Resolve the contributor.** Use an explicit email or member ID first. Otherwise match `git config user.email` and `gh api user --jq .login` against Plane members. If identities disagree, list candidates and ask; never guess.
2. **Check tracker freshness.** Read the newest issue `updated_at` or the last webhook time. If it is older than 24h, mark `tracker: stale` and fall back to GitHub and repo docs.
3. **Pull the person's queue.** Read Plane projects, then their issues; keep state groups `backlog`, `unstarted`, `started`, and `triage`. Overdue is a target date before today. Add open authored PRs, plus repo PRs with no review over 48h old.
4. **Map to one surface.** Use the task's project to resolve the repo mapping and the checkout path. Run `git status --short`, `git branch --show-current`, and `git rev-parse --short HEAD`. For non-code work, set `repo: none` and name the artifact.
5. **Choose one task.** Priority: overdue urgent/high issue, then current cycle, then 48h review breach, then recent repo issue. If two tie, show three and ask. No task means `task: none`; do not invent work.
6. **Write the brief.** Save `docs/reports/work-start/YYYY-MM-DD-<slug>.md` with the fields below, IST date, commit, and `tracker: live|stale`.
7. **Load only the first context.** Read the repo's `README.md`, `CONTEXT.md` or `docs/README.md`, and the first file named by the task. Run the smallest build/test gate if cheap; no long jobs. Full map: `yazhi-code-orient`.
8. **Hand off.** Code goes to `yazhi-code-frame` or `yazhi-code-implement`; review goes to `yazhi-work-status` or `yazhi-code-action`; unclear scope: `yazhi-code-frame`. Do not edit code or write to Plane; do those in the normal tools.

## Start brief

| Field | Content |
|---|---|
| Person | Member ID, display name, email, focus |
| Task | One issue ID, title, source, target date, priority |
| Why today | Overdue, due, review SLA, or blocker |
| Surface | Repo, branch, HEAD, clean/dirty; or `none` + artifact |
| Done when | Issue acceptance criterion or tracker checklist |
| First file | Path and why it is first |
| First command | Smallest build or test command |
| Review queue | PRs in the person's repos past 48h |
| Provenance | IST date, `tracker: live|stale`, last update |
| Out of scope | What not to touch |

## Plane reads

```bash
: "${PLANE_BASE_URL:=https://api.plane.so}"
: "${PLANE_WORKSPACE:?set PLANE_WORKSPACE}"
: "${PLANE_API_TOKEN:?set PLANE_API_TOKEN}"
curl -fsS -H "X-API-Key: $PLANE_API_TOKEN" \
  "$PLANE_BASE_URL/api/v1/workspaces/$PLANE_WORKSPACE/projects/"
```

For each project, read `/projects/<id>/issues/`; useful fields: `id`, `name`, `state` (resolve its group), `assignees`, `target_date`, `priority`, and `updated_at`.

## Anti-patterns

- **Guessing the person from a name.** Two contributors can share a name; show candidates and ask.
- **Treating a stale tracker as live.** If Plane has not synced in 24h, say so and use the repo docs.
- **Opening every repo.** Init picks one surface; cloning every repo is not init.
- **Starting with code.** Brief and first file come before edits; implementation is `yazhi-code-implement`.
- **Writing to Plane from the init pass.** Task state changes belong in the normal tracker flow, not a side channel.
- **Inventing a task when Plane has none.** `task: none` is valid; ask for direction.

For the repo map see `yazhi-code-orient`; for framing see `yazhi-code-frame`; for the cross-repo queue see `yazhi-work-status`; for GitHub actions see `yazhi-code-action`; for routing see `yazhi-agency`.
