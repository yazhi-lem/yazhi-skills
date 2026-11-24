# skills/

Status: current · Verified: 2026-11-20

Canonical skill catalog for yazhi-lem. Layout: `skills/<category>/<skill-name>/SKILL.md`.

| Category | Covers |
|---|---|
| `ai-ml/`, `sovereign/`, `security/` | Model, deployment and security technique |
| `agentic/` | Agents that run unattended: reliability (idempotency, bounded loops) and security (prompt injection, least privilege) |
| `tamil/`, `yazh-life/`, `social-media/` | Tamil language and audience work |
| `fde/`, `gtm/` | Customer engagements, support, and go-to-market |
| `org/` | Internal ways of working: ethos, doc colors, healthy code, PRs, releases, operating rhythm, and cross-repo workflows |
| `repos/` | Per-repo status skills (one per public repo) |
| `tools/` | `skill-authoring` (contract), `technical-documentation` (doc contract), Google style adoption, API/CLI/MCP design |

Contribution rules live in
[`tools/skill-authoring/SKILL.md`](tools/skill-authoring/SKILL.md); new docs
follow [`tools/technical-documentation/SKILL.md`](tools/technical-documentation/SKILL.md).
After any SKILL.md change, regenerate `skills.json`, `.claude-plugin/plugin.json`
and `dist/` bundles, then run `scripts/validate_skills.py`.
