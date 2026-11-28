# docs/

Status: current · Owner: Anbu · Verified: 2026-11-28 against `main`

Documentation index for the yazhi-skills repository.

| Document | Covers |
|---|---|
| [`../README.md`](../README.md) | Install, catalog (117 skills), contribution workflow |
| [`choose-a-skill.md`](./choose-a-skill.md) | Task/audience front door for maintainers, developers, designers, and commons |
| [`../collections/README.md`](../collections/README.md) | Human-facing split of the catalog by audience/domain |
| [`skill-efficiency.md`](./skill-efficiency.md) | Conciseness, routing, and status-claim rules for skills |
| [`skills-audit-2026-11-27.md`](./skills-audit-2026-11-27.md) | Hard review: duplicate triggers, stale facts, consistency debt, consolidation plan |
| [`pi.md`](./pi.md) | Installing and invoking the skills in the Pi coding agent |
| [`../extensions/yazhi/README.md`](../extensions/yazhi/README.md) | Yazhi Pi extension: `/yazhi-start`, `/yazhi-purpose`, `/yazhi-review`, `/yazhi-issue`, `/yazhi-pr`, and safety gates |
| [`pi-harness-lessons.md`](./pi-harness-lessons.md) | What the Pi harness does and how `yazhi-code` adopts its skill/session/checkpoint patterns |
| [`../brand-voice-reference.md`](../brand-voice-reference.md) | Brand tone-of-voice reference |
| [`../skills/README.md`](../skills/README.md) | Local skills structure and central catalog |
| [`../skills/tools/skill-authoring/SKILL.md`](../skills/tools/skill-authoring/SKILL.md) | The SKILL.md contract |
| [`../skills/tools/technical-documentation/SKILL.md`](../skills/tools/technical-documentation/SKILL.md) | Technical doc structure for repositories |

## Rules

- A skill's contract is owned by `skill-authoring`; do not duplicate it here.
- Internal ways of working (ethos, doc colors, healthy code, PRs, releases) and cross-repo workflows (daily work status, audits, triage, contract sequencing, plan recovery, service boundaries) live in `skills/org/`.
- Every SKILL.md change requires regenerated `skills.json`, plugin manifest and bundles.
- The skill contract is portable: frontmatter stays to `name` + `description` so the same files load in Claude Code, Pi, and any Agent Skills host. Host-specific instructions live in `README.md` and `pi.md`, not in SKILL.md.
