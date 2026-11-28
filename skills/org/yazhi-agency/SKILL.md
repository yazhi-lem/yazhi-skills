---
name: yazhi-agency
description: Use when delegating a task to one or more Yazhi agents, or when a request spans several domains and needs routing. Helps you pick the right agent, sequence the handoffs, and avoid dispatching a read-only auditor to patch code.
---

A roster is not an org. Nine named agents produce nothing until work is routed to one of them with a clear owner, a bounded task, and a definition of done. This skill is the routing layer: it decides *who* acts, in *what order*, and what the handoff must contain so the next agent does not re-derive the context.

## The roster

| Agent | Use when | Writes? |
|---|---|---|
| `vajra` | The task is vague, architectural, or spans agents | no |
| `thozhar` | Application code, tests, builds, packaging | yes |
| `arivu` | Corpus, ETL, schemas, dataset cleaning | yes |
| `uyir` | Services, units, logs, backups, mesh | yes |
| `kaaval` | Secrets, permissions, CVEs, PR loopholes | no |
| `kanaku` | Market, pricing, positioning, pitch docs | docs only |
| `oviya` | UI, tokens, Tamil layout, accessibility | yes |
| `anbu` | Roster, briefs, onboarding, doc drift | docs only |
| `agam` | Offline personal tooling, local vaults | yes |

## Routing workflow

1. **Classify the request** into one primary domain. If two domains are equally primary, the task is not ready — split it.
2. **Check the owner.** One agent owns the task end to end. Other agents are consulted, not co-owners.
3. **Choose the mode.** Single for one issue, parallel for independent issues, chain when step two needs step one's output.
4. **Write the task** with the target path, the constraint, and the done condition. A task that says "improve auth" is not a task.
5. **Respect the read-only boundary.** `vajra` and `kaaval` investigate and report. If the task needs a patch, the chain is `kaaval` → `thozhar`.
6. **Verify before closing.** Read the agent's verification command and result, not just its summary.

## Dispatch modes

| Mode | Shape | Use |
|---|---|---|
| single | `{ agent, task }` | one issue, one owner |
| parallel | `{ tasks: [...] }` | independent issues; max 8 tasks, 4 concurrent |
| chain | `{ chain: [...] }` | sequential, `{previous}` carries the output |

## Handoff contract

Every dispatched task states four things: the **goal** in one sentence, the **first file** to read, the **boundary** (what not to touch), and the **done condition** (the command or artifact that proves it). Missing any one of these is why agents return plausible-sounding work that cannot be merged.

## Chain patterns

- **Unknown scope:** `vajra` (plan) → `thozhar` (implement) → `kaaval` (review).
- **New surface:** `oviya` (tokens) → `thozhar` (build) → `uyir` (deploy).
- **Data change:** `arivu` (pipeline) → `thozhar` (code) → `uyir` (storage).
- **Docs drift:** `anbu` (find drift) → `vajra` (decide) → `anbu` (fix).

## Anti-patterns

- **Dispatching the auditor to patch.** `kaaval` and `vajra` have no write tools by design; asking them to fix what they found produces a refusal or, worse, a fabricated diff. Chain to `thozhar` instead.
- **Parallelising dependent work.** Two agents editing the same files race and lose changes. Parallel is for independent issues only; use a chain when step two reads step one.
- **Task without a first file.** The agent burns its context rediscovering the repo. Name the entry point.
- **No done condition.** "Make it better" returns an essay. Name the test, build, or artifact.
- **Co-ownership.** Two owners means neither verifies. One owner, explicit consults.
- **Dispatching without reading the result.** The usage and verification block is the signal; a confident summary with a failed command is a failed task.

For repo-level sequencing, see `org-issue-triage` and `org-cross-repo-change`. For the reliability and security procedures the agents apply, see `agentic-reliability` and `agentic-security`.
