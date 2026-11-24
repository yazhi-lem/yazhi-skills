---
name: skill-authoring
description: Use when writing a new SKILL.md file for this repository, or reviewing one submitted in a PR. Helps you meet the frontmatter contract, hit the body quality bar, and place the file correctly so an agent actually finds and trusts it at trigger time.
---

This is the repo's contribution guide, encoded as a skill so it's discoverable like every other skill. A skill changes agent behavior at a specific trigger moment — if the frontmatter can't tell a reader when to invoke it, the skill has failed its main job.

## Repo layout convention

Every skill lives at `skills/<category>/<skill-name>/SKILL.md`. The directory name is the identity — `name` in the frontmatter must equal it, kebab-case. No `index.md` or `README.md` alongside; the SKILL.md is the whole unit.

## Frontmatter contract

1. **`name`** — kebab-case, must exactly match the parent directory name. `skills/tools/api-design/SKILL.md` → `name: api-design`. A mismatch is an automatic reject; tooling that resolves skills by directory breaks silently.
2. **`description`** — must start with the literal words "Use when" followed by a concrete, recognizable trigger scenario, not a topic label, then one more sentence on what it helps produce or avoid.
   - Bad: `description: Helps with API design.` (topic label, no trigger)
   - Good: `description: Use when designing a new REST or RPC API surface, or reviewing an existing one for consistency. Helps you avoid the breaking-change and inconsistency traps...`
3. Nothing else is required in frontmatter — don't add fields speculatively.

## Body quality bar

1. **Open with 2-3 sentences of framing** — why this matters, not what it is. Skip encyclopedic throat-clearing ("APIs are interfaces that...").
2. **Include a numbered workflow or checklist** with concrete, sequenced steps — not unordered tips. Steps should be things an agent can execute or check off.
3. **Include at least one table** where there's tabular information (exit codes, error shapes, primitive selection) — tables compress better than prose for lookups.
4. **Prefer concrete numeric defaults over vague advice.** "Use a reasonable timeout" is not actionable; "30s default timeout, 3 retries with exponential backoff" is.
5. **Include an "Anti-patterns" or "Common failure modes" section** with 3-5 specific, named failures and *why* each one bites — not generic "avoid bad code" filler.
6. **Cross-reference sibling skills by name in backticks** instead of duplicating them. If two skills would repeat the same guidance, one owns it and the other links to it.
7. **Target 400-700 words** (the validator allows 350-850) — long enough to be procedural, short enough to read whole at trigger time.
8. **Date any status-bearing claim and name its owner.** A repo phase, version, or blocker belongs in a skill only with a `verified YYYY-MM-DD` date and a pointer to the source of truth (`docs/README.md`, `CONTEXT.md`). Undated snapshots become fiction silently; see the `org/` skills for the workflows that expire them.

## Review checklist for a new skill PR

Run `python3 scripts/build_index.py && python3 scripts/validate_skills.py` first — it mechanises every row below that a script can check, plus `skills.json` and the plugin manifest. Review by hand only what it can't judge; the validator requires 3+ numbered steps and 3+ named anti-patterns, so stubs fail CI.

| Check | How to verify |
|---|---|
| Frontmatter parses | YAML between `---` markers is valid, exactly two keys: `name`, `description` |
| `name` matches directory | Compare `name:` value to the parent directory's basename, char for char |
| Description is a real trigger | Starts with "Use when" + a scenario an agent recognizes mid-task, not a topic summary |
| Body has a workflow/checklist | At least 3 numbered list items of concrete steps present |
| Body has a table | At least one Markdown table present |
| Concrete over vague | At least one numeric default or specific example; reject "use good judgment" with nothing to anchor it |
| Anti-patterns section exists | At least 3 named failure modes, each with a one-clause reason |
| Cross-references are valid | Any skill name in backticks corresponds to an actual `skills/<category>/<name>/` directory in this repo |
| Word count sane | Roughly 400-700 words; flag if wildly over (encyclopedic) or under (stub) |
| Status claims are dated | Any phase/version/blocker says when it was verified and cites the owning doc |
| No stray files | Just `SKILL.md` in the directory — no README/index alongside it |

## Common failure modes

- **Description as topic label instead of trigger.** "Covers CLI design" tells an agent nothing about *when* to reach for it — always phrase as "Use when [doing X]."
- **Name/directory drift.** Renaming the directory without updating `name:`, or vice versa — lookup breaks silently since nothing errors until resolution fails.
- **Generic essay body.** Platitudes with no numbers, checklist, or table — reads like a blog post, not something an agent can execute.
- **Duplicating a sibling skill's content** instead of cross-referencing it — two sources of truth that drift apart.
- **Missing anti-patterns section**, or one filled with vague entries like "don't write bad code" instead of named, specific failures with a reason.
- **Undated status snapshot.** A phase table with no verified date looks authoritative forever and quietly becomes wrong; date it and link the index that owns it.

See `mcp-server-development`, `cli-tool-design`, and `api-design` as worked examples; see `org-plan-reset-recovery` for how dated plans are retired.
