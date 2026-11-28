# skills/

Status: current · Verified: 2026-11-28

Canonical skill catalog for this repository. Layout: `skills/<category>/<skill-name>/SKILL.md`.

Not sure which one to use? [`docs/choose-a-skill.md`](../docs/choose-a-skill.md) routes by task/audience; [`docs/skills-audit-2026-11-27.md`](../docs/skills-audit-2026-11-27.md) explains the current overlap and consolidation plan.

| Category | Covers |
|---|---|
| `ai-ml/`, `sovereign/`, `security/` | Model, deployment and security technique |
| `agentic/` | Agents that run unattended: reliability (idempotency, bounded loops) and security (prompt injection, least privilege) |
| `tamil/`, `yazh-life/`, `social-media/` | Tamil language and audience work |
| `fde/`, `gtm/` | Customer engagements, support, and go-to-market |
| `org/` | Internal ways of working: ethos, doc colors, healthy code, PRs, releases, operating rhythm, contributor session init, daily work status, and cross-repo workflows |
| `tools/` | `skill-authoring` (contract), `technical-documentation` (doc contract), Google style adoption, API/CLI/MCP design |
| `design/` | `visual-design` — hierarchy, spacing, type, contrast, states, real-content checks |
| `yazhi-code/` | Idea-to-client pipeline (`orient` → `frame` → `design` → `implement` → `handoff` → `deliver`), shared `standards`, and support loop (`debug`, `refactor`, `prune`, `maintain`, `writeup`, `action`, `improve`) |
| `yazhi-purpose/` | `purpose-gate` (sovereign, Tamil-native, open by default) and `yazhi-review` (security/code/language verdict) |
| `indic/` | Evolving multilingual/multicultural skills: scripts, transliteration, content, localization, cultural register |

Contribution rules live in
[`tools/skill-authoring/SKILL.md`](tools/skill-authoring/SKILL.md); new docs
follow [`tools/technical-documentation/SKILL.md`](tools/technical-documentation/SKILL.md).
After any SKILL.md change, regenerate `skills.json`, `.claude-plugin/plugin.json`
and `dist/` bundles, then run `scripts/validate_skills.py`.
