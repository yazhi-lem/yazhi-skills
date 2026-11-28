# Yazhi Pi extension

Status: current · Owner: Vajra · Verified: 2026-11-28
Scope: A thin Pi harness adapter for the `yazhi-purpose` and `yazhi-code` skills.

This extension does not auto-commit, auto-push, replace tools, or change model settings. It adds five commands and three conservative gates that follow Pi's own examples (`git-checkpoint`, `permission-gate`, `protected-paths`, `dirty-repo-guard`).

## Commands

| Command | Queued skill | Use when |
|---|---|---|
| `/yazhi-start` | `/skill:yazhi-work-start` | Resolving your Plane member, task focus, repo, and first move |
| `/yazhi-purpose` | `/skill:yazhi-purpose-gate` | Deciding if a feature is sovereign, Tamil-native, and open by default |
| `/yazhi-review` | `/skill:yazhi-review` | Final security / code / language verdict before merge or release |
| `/yazhi-issue` | `/skill:yazhi-code-writeup issue` | Draft a contentful, evidence-backed GitHub issue |
| `/yazhi-pr` | `/skill:yazhi-code-writeup pr` | Draft a contentful PR with scope, evidence, and test plan |

Arguments pass through: `/yazhi-review PR 123` queues `/skill:yazhi-review PR 123`, and `/yazhi-pr fix the sandhi join` queues `/skill:yazhi-code-writeup pr fix the sandhi join`. The prompt is placed in the editor for review; submit it to load the skill. Commands require interactive mode.

## Gates

- **Dangerous bash** — `rm -rf`, `sudo`, forced `git push`, `chmod/chown 777`, `shutdown/reboot/mkfs`. Confirm in TUI; block in non-interactive mode.
- **Protected paths** — writes/edits containing `.env`, `.git/`, `node_modules/`, `.ssh/`, `id_rsa`, or `credentials` are blocked.
- **Dirty repo** — switching or forking a session with uncommitted changes asks for confirmation; non-interactive runs are cancelled.

Project trust is separate: enabling this extension does not make a project's own skills, agents, or extensions safe. Review them before granting trust.

## Install

User-level (all projects):

```bash
mkdir -p ~/.pi/agent/extensions
ln -s "$PWD/extensions/yazhi" ~/.pi/agent/extensions/yazhi
```

Or load once:

```bash
pi -e "$PWD/extensions/yazhi/index.ts"
```

Project-local:

```bash
mkdir -p .pi/extensions
ln -s "$PWD/extensions/yazhi" .pi/extensions/yazhi
```

Project-local extensions load only after project trust is granted. Run `/reload` after installing during an active session.

No npm dependencies: Pi loads TypeScript extensions through jiti. The only import is Pi's own type/event API.
