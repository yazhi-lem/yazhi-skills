# docs/

Status: current · Owner: Anbu · Verified: 2026-11-20 against `main`

Documentation index for the yazhi-skills repository.

| Document | Covers |
|---|---|
| [`../README.md`](../README.md) | Install, catalog (102 skills), contribution workflow |
| [`pi.md`](./pi.md) | Installing and invoking the skills in the Pi coding agent |
| [`../brand-voice-reference.md`](../brand-voice-reference.md) | Brand tone-of-voice reference |
| [`../skills/README.md`](../skills/README.md) | Local skills structure and central catalog |
| [`../skills/tools/skill-authoring/SKILL.md`](../skills/tools/skill-authoring/SKILL.md) | The SKILL.md contract |
| [`../skills/tools/technical-documentation/SKILL.md`](../skills/tools/technical-documentation/SKILL.md) | Technical doc structure for yazhi-lem repos |

## Rules

- A skill's contract is owned by `skill-authoring`; do not duplicate it here.
- Internal ways of working (ethos, doc colors, healthy code, PRs, releases) and cross-repo workflows (audits, triage, contract sequencing, plan recovery, service boundaries) live in `skills/org/`; per-repo state stays in `skills/repos/`.
- Every SKILL.md change requires regenerated `skills.json`, plugin manifest and bundles.
- The skill contract is portable: frontmatter stays to `name` + `description` so the same files load in Claude Code, Pi, and any Agent Skills host. Host-specific instructions live in `README.md` and `pi.md`, not in SKILL.md.
