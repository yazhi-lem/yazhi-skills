---
name: yazhi-code-debug
description: Use when a Yazhi repo's build, test, or runtime behavior is wrong and the cause is unknown — reproduce, isolate, fix, and add a regression check. Helps you debug in small checkpoints instead of rewriting code blindly; security compromise goes to incident-response.
---

# Yazhi Code — Debug in Small Checkpoints

Debugging is a search problem, not a license to edit everything. This skill owns the unknown-cause loop for ordinary code failures: reproduce, narrow, instrument, fix one cause, and prove it stays fixed. A suspected exploit, leak, or compromised credential is not a debug task — hand it to `incident-response` immediately.

## Workflow

1. **Capture the exact failure before touching code.** Record the command, exit code, relevant log lines, repo, commit, and environment. If output is long, save it to a file from the tool and quote only the decisive lines; a truncated terminal tail is not a reproduction.
2. **Checkpoint the workspace.** Commit or stash unrelated work before instrumenting. Pi's checkpoint pattern stashes at turn start so a fork can restore code state; do the same with git when a slice begins. Never debug on top of unexplained dirty state.
3. **Make the failure repeatable and minimal.** Reduce to one command, one test, or one input. If the failure disappears, the environment or the input was the variable — write that down before changing code.
4. **Narrow by halves, not by hunches.** Bisect the input, the config, or the commit range. Use read-only exploration first; only edit when you can state which boundary you are testing. Batch independent searches and inspect only the excerpts that change the hypothesis.
5. **Instrument at the boundary.** Add the smallest log, assertion, or typed error that distinguishes the competing hypotheses. Keep it local; remove or promote it into a real test in the same slice. A debug print left in shared code is a new bug.
6. **Fix one cause and add the regression check.** The check must fail on the old behavior and pass on the new one ("Tests pass" with no command is not proof). Follow `yazhi-code-standards` for error paths and `org-healthy-code` for honest tests.
7. **Write the recovery note and stop.** Record symptom, root cause, changed files, command that now passes, and what you deliberately did not change. After a long session, that note is what survives compaction; a chat recap does not.

## Debug evidence table

| Stage | Evidence to keep | Bad shortcut |
|---|---|---|
| Reproduce | Command, exit code, commit, environment | "It failed earlier" |
| Isolate | Minimal input or test that still fails | Editing five files at once |
| Hypothesis | Two competing explanations and what distinguishes them | "Probably the cache" |
| Fix | One changed boundary plus a failing-then-passing check | Rewriting the module |
| Handoff | Changed files and verification command | Leaving instrumentation in place |

## Anti-patterns

- **Editing before reproducing.** The change that "seems related" usually hides the real variable and leaves two bugs.
- **Trusting the last 50 lines of a log.** The cause is often in the omitted head; save full output and quote selectively.
- **Bisecting by comment-out.** Removing code blindly changes behavior and creates a second unknown; change one boundary at a time.
- **A regression test that only checks no exception.** It certifies the broken path ran, not that the right result came back.
- **Debugging a security signal as a normal bug.** An active credential leak or exploitation follows `incident-response`, with containment before diagnosis.
- **Carrying debug instrumentation into the PR.** It belongs in the fix commit as a real assertion or nowhere.

Map to: `yazhi-code-implement` (if the fix grows into a feature), `yazhi-code-handoff` (verification evidence), `fde-support-escalation` (customer-site failures), `model-monitoring` (production LLM drift).
