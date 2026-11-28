---
name: yazhi-code-orient
description: Use when entering an unfamiliar repository or task and you need a read-only map before framing any change. Helps you find the current source of truth, build gates, conventions, and trust boundaries; for contributor and task setup use `yazhi-work-start` first.
---

# Orient Before Framing

Working from memory is how work drifts. This skill is the read-only reconnaissance pass before `yazhi-code-frame`: find what owns the truth in this repo, what commands prove code still works, and what must not be touched. It produces a short map, not a status snapshot or a cleanup report.

## Workflow

1. **Fix the scope to one repo and one task.** Name the repository and the question you are trying to answer. If the task spans repos, hand the contract question to `org-cross-repo-change` and `org-service-boundaries` before continuing.
2. **Read the status owner, not a remembered snapshot.** Open `README.md`, `CONTEXT.md`, and `docs/README.md` in that order. Treat any repo map or status note as dated orientation; if a plan or hard date is not linked from the current index, check `org-plan-reset-recovery` before acting on it.
3. **Find the build and proof gates.** Locate the test command, formatter/linter, generated artifacts, and the smallest sanity check. A service repo may need a unit test and an integration check; an app repo may need a platform build; a model repo may need a small sanity batch before a long run. Record the exact commands, not "run tests".
4. **Map the boundary of the change.** Identify the module or source of truth that owns the behavior: a core library over a UI layer, a shared schema over its clients, or a contract between repos. Note any language, child-facing, or data-residency constraint that will need a domain skill later.
5. **Check the harness surface.** Read `AGENTS.md` / `CLAUDE.md`, project configuration, and skill descriptions that apply. Project resources load only after trust; context files load regardless. Do not execute unfamiliar project agents or extensions just because they exist. See `yazhi-code-standards` for the trust rule.
6. **Batch the reads and write the map.** Group independent `read`/`grep`/`find` calls; save large output to a file and return only the decision-relevant excerpt. Produce a six-line note: repo, source of truth, gates, boundary, risks, and the next frame. Hand it to `yazhi-code-frame`, then stop.

## Orientation map

| Field | What to capture | Failure it prevents |
|---|---|---|
| Source of truth | Current doc index and owner | Acting on a retired roadmap |
| Gates | Exact commands and sanity checks | Discovering the real test gate after the edit |
| Boundary | Owning module, contract, or platform seam | Duplicating logic across layers or repos |
| Constraints | Language, child safety, data residency, local-first | Finding a gate at review time instead of design time |
| Harness | Context files, project trust, relevant skills | Loading untrusted project resources silently |
| Next frame | One outcome sentence candidate | Starting implementation without a frame |

## Anti-patterns

- **Cloning every repo to answer one question.** Read the current index first; broad recon buries the decision in stale detail.
- **Treating a status note as live status.** It has a verified date; the repo docs own the truth.
- **Guessing the test command.** A passed command from a sibling repo proves nothing about this one.
- **Executing project agents before trust.** Project-local agents and extensions are repo-controlled code, not harmless context.
- **Turning recon into a refactor.** This pass is read-only; write the map and hand off, do not "fix what you found".

Map to: `yazhi-work-start` (person, task, and repo init before this pass), `yazhi-code-frame` (next stage), `yazhi-code-design` (boundary detail), `yazhi-code-standards` (trust and tool discipline), `org-repo-audit` (only for a separate stale-doc audit).
