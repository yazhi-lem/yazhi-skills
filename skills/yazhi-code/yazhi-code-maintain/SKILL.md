---
name: yazhi-code-maintain
description: Use when running a routine health pass on one Yazhi repo — generated artifacts, CI, test gates, dated status docs, and toolchain drift — and you need a dated note with one next improvement. Helps you keep repos runnable between features; org cadence is yazhi-ops and security scoring is security-posture-health-check.
---

# Yazhi Code — Maintain One Repo

Repos rot between features: a generated index goes stale, a status page keeps a dead date, a test command silently stops being run. This skill owns the repeatable, read-mostly health pass for a single repo. It is narrower than `yazhi-ops` (the organization's cadence) and `security-posture-health-check` (security scoring), and it does not delete or rewrite docs — that is `org-repo-audit`.

## Workflow

1. **Fix the date, repo, and commit in the note.** Record the working directory, `git rev-parse --short HEAD`, and today's date before checking anything. An undated health note becomes rumor within a week.
2. **Run the repo's own gates, not a generic checklist.** Read `README.md`, `CONTEXT.md`, and `docs/README.md` for the declared commands. Run the smallest gate that proves the code still builds or tests, then the generated-artifact check if the repo has one. In `yazhi-skills` that means `build_index.py --check`, `build_skill_bundle.py --check`, and `validate_skills.py`.
3. **Check dates and owners, not just links.** For each current-state doc, verify `Status/Owner/Verified` and that linked plans are still in the live index. A 60-day-old guide can be current; a one-day-old plan dated before a reset is not. Use `org-plan-reset-recovery` when authority is unclear.
4. **Inspect drift in dependencies and toolchain.** Compare the declared runtime/tool versions with what CI actually uses, and look for a lockfile or generated file that changed without a source change. Do not upgrade anything in this pass — record the drift as a candidate improvement.
5. **Batch the mechanical checks.** Group independent reads and searches; save long command output to a file and quote the failing lines. This is the Pi `codemode` pattern: filter before the result reaches the model or the note.
6. **Write one dated health note.** Use the table below, name one owner for each red/amber row, and choose exactly one next improvement. More than one next step is a plan reset, not maintenance.
7. **Hand the improvement forward.** If the next step changes code structure, open a `yazhi-code-improve` or `yazhi-code-refactor` frame. If it is a security finding, use `security-posture-health-check` / `incident-response`. Do not silently fix it here.

## Health note shape

| Check | Healthy signal | Action when not |
|---|---|---|
| Build / test gate | Declared command passes, result named | Record command and failure; open a debug frame |
| Generated artifacts | `--check` or equivalent is clean | Regenerate in a separate PR with the source change |
| Current docs | Dated `Status/Owner/Verified`, live links | Flag owner; use `org-plan-reset-recovery` |
| Conventions | Formatter/linter clean; skill/index consistent | Point to `yazhi-code-standards` |
| Toolchain drift | Declared and CI versions match | One candidate improvement, no upgrade here |
| Tamil / child-facing strings | Native review and safety gate recorded | Route to `tamil-content-writing` / `org-release` |

## Anti-patterns

- **Running a generic checklist instead of the repo's gates.** A green command from a sibling repo proves nothing about this one.
- **Deleting a stale doc during a health pass.** The pass is read-mostly; `org-repo-audit` owns reduction with an agreed plan.
- **Averaging health into one score.** A green build does not cancel a red access review or an undated status page.
- **Upgrading dependencies "while checking".** Maintenance produces a candidate; implementation is a separate, reviewable change.
- **An undated note with no owner.** It will be quoted as current long after the repo has moved on.

Map to: `yazhi-code-orient` (first entry), `yazhi-code-improve` (next step), `org-repo-audit` (doc cleanup), `yazhi-ops` (cadence), `security-posture-health-check` (security).
