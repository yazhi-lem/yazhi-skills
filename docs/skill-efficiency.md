# Skill efficiency guide

Status: current · Owner: Vajra · Verified: 2026-11-27
Scope: How to keep a skill short enough to load, specific enough to route, and durable enough to trust.

A skill is prompt context, not documentation. Every extra paragraph competes with the task the agent is trying to do. The contract in [`skill-authoring`](../skills/tools/skill-authoring/SKILL.md) is mandatory; this guide is the efficiency layer on top of it.

## The five rules

1. **One trigger, one outcome, one boundary.** The `description` says when to load the skill, what it produces, and which neighbouring skill owns the overlapping case. If two skills fire on the same sentence without a boundary, fix the descriptions before adding content.
2. **Stay under 700 words.** `validate_skills.py` warns above 700 and errors only outside 350–850. Use a table for lookup data, numbered steps for procedure, and a cross-reference for anything another skill already owns.
3. **Write for a cold reader.** The model sees the description at startup and the body only after a match. The first two sentences must explain why this matters now; the workflow must be executable without the conversation that led here.
4. **Date every status claim.** A phase, version, blocker, or sync date needs `verified YYYY-MM-DD` and a owning doc. Otherwise link to the repo's current index instead of copying the snapshot.
5. **Keep frontmatter portable.** Only `name` and `description`. Audience/task tags belong in generated catalogs, not in `SKILL.md`.

## Drift control

| Signal | Fix |
|---|---|
| Two skills with near-identical workflow steps | Name one owner; the other links to it |
| Body over 700 words | Move reference tables to the owning skill or a dated repo doc |
| Description starts with a topic label | Rewrite as "Use when [recognizable situation]" |
| Anti-patterns are generic | Replace with named failures and the reason they bite |
| Cross-reference to a dead skill/category | Update the link and add a validator check if it escaped CI |
| Status table without a verified date | Link to the source index, or date it with an owner |

## Backlog from the 2026-11-27 audit

The validator now surfaces **25 skills above 700 words** as warnings. They are not errors because deleting procedural detail without an owner is worse than a long skill. Reduce them one at a time: choose the longest, move its reference material to the owning skill, run `validate_skills.py`, and regenerate bundles in the same PR. `--strict` becomes a CI gate only when that count reaches zero.

See [`skills-audit-2026-11-27.md`](./skills-audit-2026-11-27.md) for the overlap map and [`choose-a-skill.md`](./choose-a-skill.md) for the audience front doors.
