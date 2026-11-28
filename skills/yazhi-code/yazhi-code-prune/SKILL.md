---
name: yazhi-code-prune
description: Use when a repository has accumulated dead code, unused dependencies, duplicate helpers, stale flags, or oversized modules and you need a safe prune-and-refactor pass. Helps you prove what is unused, remove it in small reversible commits, measure the reduction, and hand the remaining structure to `yazhi-code-refactor`; feature work stays out.
---

Codebases grow by addition; removal is a separate discipline. A prune pass is not "delete what looks unused" — it is proving no live path needs a thing, removing it in a reversible step, and measuring the reduction. This skill owns the decision and the removal; `yazhi-code-refactor` owns the behavior-preserving restructuring that follows, and `yazhi-code-debug` owns any bug found on the way.

## Candidate table

| Candidate | Proof before removal | Default move |
|---|---|---|
| Dead function or export | Zero references in code, tests, configs, templates, docs; no dynamic or registry entrypoint; one release of deprecation for public API | Remove with a test |
| Unused dependency | Not imported by source, tests, or scripts; not required by build, plugin, or CLI entrypoint; lockfile clean | Remove, reinstall, build |
| Duplicate helper | Two implementations, same behavior, one owner named | Consolidate |
| Stale feature flag | Off by default, no live config enables it, telemetry confirms | Remove flag and dead branch |
| Oversized module | Over 500 lines or 20 functions, mixed responsibilities | Split after characterization |
| Commented-out code, stale TODO, or orphaned test | Git history or no code/CI reference; owner agrees | Delete; link an issue |

## Workflow

1. **Fix the baseline.** One repo, `HEAD`, date, and the exact build, test, and lint commands. Record line/file counts, dependency count, CI time, and bundle/binary size. No baseline, no measurable prune.
2. **Inventory mechanically, not by eye.** Search every symbol across code, tests, configs, templates, and docs. Use repo tools when present: `vulture`/`ruff` for Python, `cargo machete`/`clippy` for Rust, `knip`/`ts-prune` for TypeScript. Save the raw output.
3. **Classify each candidate** as `remove`, `deprecate`, `consolidate`, `split`, or `keep`; write the evidence and owner. Uncertain means `deprecate`, never delete.
4. **Pick one batch by reduction-to-risk.** One category per PR and at most 400 changed lines. Never mix dead-code removal, dependency removal, and restructuring in one PR.
5. **Prove safety before deleting.** Run the full gate; check dynamic imports, reflection, registries, string dispatch, templates, public API, and cross-repo consumers. For uncertain behavior, add a characterization check.
6. **Remove in reversible commits.** Dead code, then tests, then dependencies, then duplicates or splits. Each commit builds and passes the named gate. If a test fails, stop and route it to `yazhi-code-debug`; never delete the failing test.
7. **Measure after with the same commands.** Lines/files removed, dependencies removed, build/test time, bundle/binary size. If the delta is not a real reduction, revert or leave it out.
8. **Hand off with evidence.** The PR body states what was proven dead, what was not touched, verification commands, and the rollback commit. Remaining structure goes to `yazhi-code-refactor`; a recurring class becomes a lint or CI rule via `yazhi-code-improve`.

## Guardrails

| Do not prune | Why | Route |
|---|---|---|
| Public API, proto, or schema | Breaks consumers while the repo stays green | Deprecate and `org-cross-repo-change` |
| Database migrations or data | Irreversible and often the only history | Owner, backup, migration plan |
| Localized strings or legacy encodings | May be compatibility paths, not dead weight | The relevant language/encoding skill |
| A test with no replacement | Removes the only guard | Add characterization or sign-off |
| Generated files by hand | Drift from the source | Regenerate, then ignore |
| Code under a flag still in telemetry | Not provably dead | Wait or instrument |

## Anti-patterns

- **One `rg` hit as proof of death.** Dynamic imports, reflection, registries, and string dispatch do not show up; check entrypoints and runtime config.
- **Deleting a dependency used only by the build.** Import scans miss plugins, hooks, and CLI entrypoints; run the build after removal.
- **Mixing prune with behavior change.** The PR no longer proves "no behavior change"; split it.
- **Deleting a test to get green.** The failure is the signal; route it to `yazhi-code-debug` and fix the code.
- **Deleting legacy localized or encoding paths because they look unused.** They are often the compatibility surface for old data.

See `yazhi-code-refactor` for the structural half, `yazhi-code-maintain` for candidates, `org-healthy-code`/`yazhi-code-handoff` for the diff, and `org-cross-repo-change` for contracts.
