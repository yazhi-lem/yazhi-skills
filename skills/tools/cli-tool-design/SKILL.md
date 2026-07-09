---
name: cli-tool-design
description: Use when designing or reviewing a command-line tool's interface — flags, defaults, output modes, exit codes, and help text — before or while implementing it. Helps you produce a CLI that's predictable for humans and scriptable for automation (including LLM agents shelling out to it).
---

A CLI has two audiences at once — a human typing interactively and a script (or agent) parsing output — and most bad CLIs pick one and break the other. Design for both from the start: consistent flags, a machine-readable output mode, and exit codes that mean something.

## Workflow

1. **Draft the noun-verb shape first.** Prefer `tool noun verb` (`tool user create`) over a flat verb soup once you have more than ~6 subcommands; keep it flat below that.
2. **Pick flag names from the standard vocabulary** before inventing new ones: `--output/-o`, `--format/-f`, `--verbose/-v`, `--quiet/-q`, `--dry-run`, `--force/-y`, `--config/-c`, `--help/-h`, `--version`. Reuse, don't reinvent.
3. **Set safe defaults.** The no-flags invocation should be the common case and should not be destructive. Anything irreversible (delete, overwrite, push) requires an explicit flag or interactive confirmation, bypassable with `--force`/`-y` for scripts.
4. **Add `--dry-run` to every command with side effects.** It should print exactly what would happen in the same format as the real run's summary, not a vague description.
5. **Support two output modes.** Human mode: colored, aligned, summarized. `--json` (or `--format=json`) mode: stable schema, no color, no progress bars, safe for piping to `jq`. Never mix log lines into stdout when `--json` is set — logs go to stderr.
6. **Map exit codes deliberately** (table below) rather than always returning 0 or 1. Scripts and agents branch on these.
7. **Write help text with an example in the first 5 lines.** `--help` output order: one-line summary, usage line, 1-2 examples, then flags. Flag descriptions state the default value inline (`--timeout <secs>  request timeout (default: 30)`).
8. **Make repeat invocations idempotent** where the underlying operation allows it — running the same create command twice should either no-op or give a clear "already exists" exit code, not a stack trace.

## Exit code convention

| Code | Meaning | Example |
|---|---|---|
| 0 | Success | Operation completed as requested |
| 1 | General/expected failure | Validation error, resource not found |
| 2 | Usage error | Bad flags, missing required argument |
| 3-63 | Reserved for tool-specific conditions | e.g. 3 = "already exists", 4 = "conflict" |
| 124 | Timeout | Long-running op exceeded `--timeout` |
| 130 | Interrupted (SIGINT) | User pressed Ctrl-C |

Defaults worth adopting unless you have a reason not to: 30s network timeout, 3 retries with exponential backoff, page size 50 for `list` commands, and human-readable output unless stdout is detected as non-tty (then auto-switch to a plain/machine mode).

## Anti-patterns

- **Flags that change meaning by context.** `-f` meaning "file" in one subcommand and "force" in another — pick one meaning per short flag across the whole tool.
- **Silent destructive defaults.** `tool clean` deleting untracked files with no confirmation and no `--dry-run` — this is how users lose work.
- **Progress bars or color codes leaking into `--json` output.** Breaks every downstream parser; keep stdout pure data in machine mode.
- **Required positional arguments with no sensible default and no prompt.** If a value is truly required, either prompt interactively (tty) or fail fast with a clear usage error (non-tty) — don't hang.
- **Version-locked help text.** Help that goes stale relative to actual flag behavior; generate `--help` from the same flag definitions the parser uses, never hand-maintain a separate copy.

CLIs are increasingly invoked by agents as well as humans — the `--json` mode and precise exit codes matter as much as, or more than, the human UX. See `mcp-server-development` if you're instead exposing the same functionality as MCP tools rather than a CLI, and `api-design` if there's a backend API underneath the CLI that needs its own versioning discipline.
