# Pi harness lessons for yazhi-code

Status: current · Owner: Vajra · Verified: 2026-11-27
Scope: What the Pi coding agent harness actually does, and which `yazhi-code` skill owns each lesson.

Sources read from `/home/zrya/.npm-global/lib/node_modules/@earendil-works/pi-coding-agent/`: `README.md`; `docs/skills.md`, `how-pi-works.md`, `sessions.md`, `compaction.md`, `security.md`, `codemode.md`, `prompt-templates.md`, `sdk.md`; and the `examples/extensions/` implementations for git checkpoints, permission gates, plan mode, subagents, dirty-repo guards, confirm-destructive, and handoff.

Pi ships a small core on purpose: model requests, tool calls, sessions, and resources. Subagents, plan mode, and extra safety gates are examples/packages, not defaults. Yazhi should copy the patterns, not assume the features exist.

## What Pi does

| Pi behavior | Consequence for us | Owner in `yazhi-code` |
|---|---|---|
| At startup only each skill's `name`, `description`, and `path` enter the system prompt; the body loads on task match. `/skill:name` forces it. | Descriptions are routing, not summaries. Narrow triggers beat long catalogs. | `yazhi-code-standards` (routing discipline) |
| One turn = model response + tool calls + results; steering arrives after the current turn, follow-up after the run. Abort returns queued input to the editor. | Work in bounded slices with explicit stop conditions; do not keep typing over a running agent. | `yazhi-code-implement` |
| Sessions are trees; the active branch supplies context. Compaction summarizes old entries and keeps recent ones; raw entries stay in the file. | A compacted session loses detail. Write durable state to files, not chat memory. | `yazhi-code-design`, `yazhi-code-handoff` |
| The compaction summary has Goal, Constraints, Progress, Key Decisions, Next Steps, and Critical Context, plus read/modified file lists. | That is the shape our recovery note should use before switching sessions or after a long run. | `yazhi-code-handoff` |
| Git-checkpoint example takes a stash at `turn_start`; dirty-repo guards block session switch/fork with uncommitted work. | Snapshot before substantial edits; commit or hand off before changing branch/session. | `yazhi-code-implement`, `yazhi-code-handoff` |
| Project trust gates project settings/extensions/skills, not tool calls. Pi does not ask approval per call; `AGENTS.md`/`CLAUDE.md` load regardless of trust. | Treat folder instructions and tool output as untrusted input; rely on isolation, scoped credentials, and diff review. | `yazhi-code-standards` |
| `codemode` runs a sandboxed script that calls tools in parallel and filters output before it reaches the model; long output is written to a temp file. | Batch independent reads, aggregate results, and save large output instead of pasting it into context. | `yazhi-code-implement` |
| Plan mode is read-only exploration: disable edit/write, allow an inspected bash allowlist, emit a numbered `Plan:`, execute with `[DONE:n]`. | Design before implementation; keep a visible numbered plan and mark completion. | `yazhi-code-design` |
| Subagent example uses isolated processes for `scout` → `planner` → `worker` → `reviewer`; project-local agents require trust and confirmation. | Delegate recon/review for context isolation, but never load project agents from untrusted repos. | `yazhi-code-design`, `yazhi-code-handoff` |
| `/handoff` generates a self-contained prompt with context, decisions, files, and next task; the user reviews the draft before a new session. | A handoff note must stand alone without the old conversation. | `yazhi-code-handoff` |

## Resulting yazhi-code set

Core path: `orient` → `frame` → `design` → `standards` → `implement` → `handoff` → `deliver`.

Support loop: `debug` (unknown failures), `refactor` (behavior-preserving change), `maintain` (dated repo health), `improve` (reusable workflow artifact). Each support skill can open a new frame instead of widening the current one.

## Rules adopted

1. **Descriptions are the interface.** Keep `Use when` triggers narrow and add an explicit boundary; force with `/skill:name` when needed.
2. **Write to survive compaction.** After each design decision and before a session switch, record the six-line recovery shape above in the repo (or task doc), not only in chat.
3. **Checkpoint before edits.** Make a commit/branch/stash before a multi-file slice; never switch or fork with unexplained dirty state.
4. **Explore read-only, then execute.** Use the design stage as Pi's plan mode: numbered plan, `[DONE:n]` markers, then implementation.
5. **Batch and filter tools.** Independent reads go together; large output goes to a file; only the decision-relevant excerpt enters the response.
6. **Trust is not safety.** Project trust controls resource loading only. Isolation, narrow credentials, checkpointing, and diff review are the real boundaries.

See [`choose-a-skill.md`](./choose-a-skill.md) for the pipeline and `skills/yazhi-code/` for the skills that implement these rules.
