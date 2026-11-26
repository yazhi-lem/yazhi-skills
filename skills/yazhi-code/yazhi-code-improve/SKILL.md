---
name: yazhi-code-improve
description: Use when recurring Yazhi friction should become a reusable improvement — a script, prompt template, skill, extension, or documented check in any repo. Helps you baseline the pain, choose the smallest artifact, and measure adoption; SKILL.md formatting belongs to skill-authoring.
---

# Yazhi Code — Improve the Workflow

An improvement is not "we should do that more carefully". It is a small reusable artifact that removes a repeated cost from a Yazhi workflow, with an owner and a way to tell whether it helped. This skill owns that loop across any repo. It defers the SKILL.md contract to `skill-authoring`, structural code changes to `yazhi-code-refactor`, and doc cleanup to `org-repo-audit`.

## Workflow

1. **Baseline the pain before proposing a fix.** Name the repeated task, how often it happens, who pays, and one measurable cost: minutes per run, number of manual steps, PRs blocked, or errors missed. A pain with no baseline cannot show improvement.
2. **Find the existing owner of the workflow.** Search `README.md`, `CONTEXT.md`, `docs/README.md`, prompt templates, and skill descriptions. If an artifact already covers 80% of the problem, improve it rather than adding a second one — this is the same anti-duplication rule as `technical-documentation`.
3. **Choose the smallest artifact that can carry the fix.** Use a prompt template for a reusable instruction with arguments; a skill for procedural guidance with references; a script for deterministic work; an extension for event-driven harness behavior. Prefer the lightest option that solves the case. Do not build a Pi extension when a two-line template suffices.
4. **Design for the harness boundary.** Project resources load only after trust; context files load regardless and are untrusted input. Put executable hooks in user-level or explicitly trusted project resources, declare dependencies, and keep credentials out of the artifact. See `yazhi-code-standards` and the repo's `docs/pi-harness-lessons.md`.
5. **Prove the improvement before adoption.** Run the old and new paths on the same task. Record the command, the result, and the delta against the baseline. For a skill or template, also check that its trigger is narrow enough to load when needed and not otherwise.
6. **Ship with an owner and an adoption path.** Name who maintains it, where it is installed (`~/.pi/agent/`, repo `.pi/`, plugin manifest, or package), and what existing docs link to it. Regenerate `skills.json`, the plugin manifest, and bundles when a skill changes; CI must stay clean.
7. **Review after one cycle, not at launch.** After a week or ten uses, compare against the baseline. If the artifact is unused or makes the task slower, retire it with a redirect instead of keeping another plausible file.

## Artifact selection

| Friction | Smallest artifact | Owner check |
|---|---|---|
| Same prompt typed with different arguments | Prompt template | Search `.pi/prompts/` and `~/.pi/agent/prompts/` first |
| Repeated procedure needing references | Skill | `skill-authoring` + `docs/choose-a-skill.md` |
| Deterministic local transformation | Script in an existing tool dir | `org-service-boundaries` for ownership |
| Event-driven check (tool call, turn start) | Pi extension | Trust and permission review before use |
| Recurring docs/task sprawl | Owner rule in `technical-documentation` | `org-repo-audit` for reduction plan |

## Anti-patterns

- **Improving without a baseline.** The new artifact feels better but nobody can say what it changed.
- **Adding a second skill for an existing workflow.** Two sources of truth drift apart within a month; update the owner.
- **Building an extension for a prompt-shaped problem.** Executable hooks carry trust and maintenance cost a template does not.
- **Trusting project-local automation by default.** Project agents and extensions are repo-controlled code; review before granting trust.
- **Launching without an owner.** An unowned improvement becomes the next stale artifact in the audit.
- **Keeping a failed experiment.** Retire it with a redirect row; silence leaves users guessing which one is current.

Map to: `yazhi-code-maintain` (source of candidates), `yazhi-code-frame` (implementation work), `skill-authoring` (SKILL.md contract), `technical-documentation` (doc owners), `choose-a-skill.md` (discovery).
