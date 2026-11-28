# Yazhi Pi Agents

The Yazhi roster as **Pi subagent definitions** — one markdown file per agent, with
YAML frontmatter. These are the runtime form of the roles described in
[`AGENTS.md`](../../../../AGENTS.md) and the briefs in `knowledge/`.

This directory is the single source of truth for the roster. Do not copy these files
by hand; install them as symlinks.

## Format

```markdown
---
name: thozhar
description: Use when implementing or refactoring application code ...
tools: read, bash, edit, write, grep, find, ls
---

System prompt for the agent.
```

- `name` — the name you pass to the `subagent` tool.
- `description` — shown to the model; start with "Use when…".
- `tools` — optional allowlist. Omit to inherit Pi's default tools.
- `model` — optional. **Omit it** so the agent inherits the dispatching session's
  model. Hard-coding a model id is how the OpenClaw cron job failed 177 times.

## Roster

| Agent | Role | Tools | Write? |
|---|---|---|---|
| `vajra` | Coordinator / architect / IAM audit | read, grep, find, ls, bash | no |
| `thozhar` | Software engineer | full | yes |
| `arivu` | Data / ETL / corpus | full | yes |
| `uyir` | Reliability / SRE / mesh | full | yes |
| `kaaval` | Security audit | read, grep, find, ls, bash | no |
| `kanaku` | Business / market | read, grep, find, ls, write | docs only |
| `oviya` | Design / UI-UX | read, grep, find, ls, edit, write | yes |
| `anbu` | Operations / onboarding | read, grep, find, ls, edit, write | docs only |
| `agam` | Sovereign local-first tooling | full | yes |

Read-only agents (`vajra`, `kaaval`) are deliberately denied write tools: they
investigate and report, they do not patch.

## Install

Pi does not ship a subagent feature. The `subagent` extension from Pi's own examples
provides it.

```bash
# 1. Install the subagent extension
mkdir -p ~/.pi/agent/extensions/subagent
cp "$(dirname "$(command -v pi)")/../lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/subagent/"{index.ts,agents.ts} \
  ~/.pi/agent/extensions/subagent/

# 2. Install the agents (symlinks to this directory)
./install.sh --pi-agents
```

Then restart `pi` or run `/reload`.

## Use

Ask the main agent:

```text
Use thozhar to add the sandhi rule tests to apps/<app>
Run kaaval and anbu in parallel: secret scan, then roster drift check
Use a chain: vajra plans the Circle IAM cutover, thozhar implements step 1
```

The `subagent` tool exposes three modes:

- **single** — `{ agent, task }`
- **parallel** — `{ tasks: [...] }` (max 8 tasks, 4 concurrent)
- **chain** — `{ chain: [...] }` with `{previous}` substitution

## Adding an agent

1. Add `agents/<name>.md` here.
2. Run `./install.sh --pi-agents --force`.
3. Add the row to the roster table above and to `AGENTS.md`.

Keep briefs pointing at paths that exist. `anbu`'s job is to catch it when they don't.
