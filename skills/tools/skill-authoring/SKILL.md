---
name: skill-authoring
description: Use when writing a new SKILL.md file for this repository, or reviewing one submitted in a PR. Helps you meet the frontmatter contract, hit the body quality bar, and place the file correctly so an agent actually finds and trusts it at trigger time.
---

This is the contribution guide for the whole repo, encoded as a skill so it's discoverable the same way every other skill is. A skill file exists to change agent behavior at a specific trigger moment — if a reader can't tell from the frontmatter alone when to invoke it, the skill has already failed its main job.

## Repo layout convention

Every skill lives at `skills/<category>/<skill-name>/SKILL.md`. The directory name is the source of truth for identity — `name` in the frontmatter must equal the directory name, in kebab-case, exactly. No `index.md`, no `README.md` alongside it; the SKILL.md is the whole unit.

## Frontmatter contract

1. **`name`** — kebab-case, must exactly match the immediate parent directory name. `skills/tools/api-design/SKILL.md` → `name: api-design`. A mismatch here is an automatic reject; tooling that resolves skills by directory will silently break.
2. **`description`** — must start with the literal words "Use when" followed by a concrete, recognizable trigger scenario, not a topic label. Then one more sentence on what the skill helps produce or avoid.
   - Bad: `description: Helps with API design.` (topic label, no trigger)
   - Good: `description: Use when designing a new REST or RPC API surface, or reviewing an existing one for consistency. Helps you avoid the breaking-change and inconsistency traps...`
3. Nothing else is required in frontmatter — don't add fields speculatively.

## Body quality bar

1. **Open with 2-3 sentences of framing** — why this matters, not what it is. Skip encyclopedic throat-clearing ("APIs are interfaces that...").
2. **Include a numbered workflow or checklist** with concrete, sequenced steps — not a bag of unordered tips. Steps should be things an agent can actually execute or check off.
3. **Include at least one table** where there's tabular information (exit codes, error shapes, primitive selection) — tables compress better than prose for reference lookups.
4. **Prefer concrete numeric defaults over vague advice.** "Use a reasonable timeout" is not actionable; "30s default timeout, 3 retries with exponential backoff" is.
5. **Include an "Anti-patterns" or "Common failure modes" section** with 3-5 specific, named failures and *why* each one bites — not generic "avoid bad code" filler.
6. **Cross-reference sibling skills by name in backticks** instead of duplicating their content. If two skills would otherwise repeat the same guidance, one should own it and the other should link to it.
7. **Target 400-700 words** for the body. Long enough to be procedural, short enough that an agent reads the whole thing at trigger time instead of skimming.

## Review checklist for a new skill PR

| Check | How to verify |
|---|---|
| Frontmatter parses | YAML between `---` markers is valid, exactly two keys: `name`, `description` |
| `name` matches directory | Compare `name:` value to the parent directory's basename, char for char |
| Description is a real trigger | Starts with "Use when" + a scenario an agent would recognize mid-task, not a one-line topic summary |
| Body has a workflow/checklist | At least one numbered list of concrete steps present |
| Body has a table | At least one Markdown table present |
| Concrete over vague | Skim for at least one numeric default or specific example; reject descriptions like "use good judgment" with nothing to anchor it |
| Anti-patterns section exists | 3-5 named failure modes, each with a one-clause reason |
| Cross-references are valid | Any skill name in backticks corresponds to an actual `skills/<category>/<name>/` directory in this repo |
| Word count sane | Roughly 400-700 words; flag if wildly over (encyclopedic) or under (stub) |
| No stray files | Just `SKILL.md` in the directory — no README/index alongside it |

## Common failure modes

- **Description as topic label instead of trigger.** "Covers CLI design" tells an agent nothing about *when* to reach for it — always phrase as "Use when [doing X]."
- **Name/directory drift.** Renaming the directory without updating `name:`, or vice versa — breaks lookup silently since nothing errors until something tries to resolve it.
- **Generic essay body.** Paragraphs of platitudes with no numbers, no checklist, no table — reads like a blog post, not something an agent can execute against.
- **Duplicating a sibling skill's content** instead of cross-referencing it — creates two sources of truth that drift apart over time.
- **Missing anti-patterns section**, or one filled with vague entries like "don't write bad code" instead of named, specific failures with a reason.

See `mcp-server-development`, `cli-tool-design`, and `api-design` in this same category as worked examples of the structure this skill describes.
