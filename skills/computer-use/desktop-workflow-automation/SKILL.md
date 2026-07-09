---
name: desktop-workflow-automation
description: Use when automating a multi-step task that spans native desktop apps, the filesystem, and the clipboard — e.g. export a report from one app, transform it, and import it into another. Helps you decide scripting vs. agentic control per step and make long-running workflows resumable after crashes or permission prompts.
---

Desktop workflows are harder than single-app automation because state lives in multiple places at once — open app windows, files on disk, clipboard contents — and any step can be interrupted by an OS permission dialog, a crashed app, or a stale file lock. Design for the workflow to be killed and restarted at any point without corrupting data or repeating destructive steps.

## Workflow

1. **Decompose into steps with an explicit state artifact.** Each step should read a known input (a file, a clipboard value, an app's current selection) and write a known output (a file, a status marker) — this is what makes resumability possible.
2. **Pick scripting vs. agentic control per step**, not for the whole workflow (see table). Use scripting wherever the app exposes a CLI, API, or file format; reserve agentic GUI control for steps with no other integration point.
3. **Persist progress after every step** to a small state file (JSON: `{step: "export_done", timestamp, output_path}`) so a restart can skip completed steps instead of re-running from scratch.
4. **Make each step idempotent.** Before running a step, check whether its output already exists and is valid (checksum, row count, or "done" marker) — skip if so, rather than blindly re-executing.
5. **Wrap clipboard use with a verify-then-consume pattern**: after copying, read the clipboard back and check it's non-empty and matches the expected shape before pasting; clipboard operations race with other apps and background processes.
6. **Pre-empt OS-level interrupts**: before starting, disable or pre-answer known permission dialogs (screen-recording/accessibility prompts, "Save changes?" dialogs) where the OS allows scripted consent; where it doesn't, add a detection step that pauses the workflow and prompts the human instead of hanging.
7. **Bound every wait.** File writes, app launches, and export dialogs should all have an explicit timeout (default 30s for app launch, 15s for file-write completion, checked via file size stability across 2 polls 1s apart) with a clear failure state, not an indefinite hang.
8. **Log a human-readable trail** of step, timestamp, and outcome — long workflows that fail silently at step 6 of 12 are nearly impossible to debug without one.

## Scripting vs. agentic control

| Approach | Best for | Cost of failure | Notes |
|---|---|---|---|
| CLI/API/file-format scripting | Apps with a documented CLI or export format (pandoc, exiftool, app-specific export) | Low — deterministic, easy to retry | Always prefer this when available |
| OS automation APIs (AppleScript, PowerShell, xdotool) | Apps with scripting hooks but no CLI | Low-medium — fairly deterministic but version-sensitive | Good middle ground; version-pin the target app |
| Agentic GUI control (`gui-agent-design`) | Apps with no CLI/API and no scripting hooks | Medium-high — grounding errors possible | Reserve for the specific steps that need it, not the whole workflow |
| Manual human handoff | One-time credential entry, CAPTCHA, irreversible confirmations | N/A | Pause and hand off explicitly rather than attempting to automate around it |

## Numeric defaults

- App launch timeout: 30s.
- File-write completion check: file size stable across 2 polls, 1s apart, before treating a write as done.
- Clipboard verify-after-copy: re-read within 500ms, retry copy up to 2 times if empty/mismatched.
- State checkpoint: written after every step, not batched.
- Permission-dialog detection poll: check every 2s for up to 20s before treating the workflow as stuck and escalating.
- Idempotency check: run before every step, not just on resume.

## Anti-patterns

- **Treating clipboard as reliable shared memory** — other apps and OS services write to it too; always verify contents right before paste, not just right after copy.
- **No resumability — restarting a 12-step workflow from step 1 after a crash at step 9** — wastes time and risks re-triggering already-completed side effects (duplicate emails, duplicate file writes).
- **Silently swallowing permission-dialog hangs** — a workflow that blocks forever on an unhandled "Allow accessibility access?" prompt looks identical to a hung app; always add a detection+escalation path.
- **Using agentic GUI control for a step that has a CLI equivalent** — slower, less reliable, and harder to log than a scripted call; check for a CLI/API first.
- **Non-idempotent steps that re-append or re-send on retry** — e.g. a step that appends to a report file will double its content if re-run after a partial failure; always check-before-write or use atomic overwrite.

For the GUI-control steps within a desktop workflow, see `gui-agent-design` for perception/action-loop design. For any step that specifically drives a browser, see `browser-automation`.
