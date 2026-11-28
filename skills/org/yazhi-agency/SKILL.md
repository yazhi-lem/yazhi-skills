---
name: yazhi-agency
description: Use when delegating a task to one or more specialist agents or roles, or when a request spans several domains and needs routing. Helps you pick the right owner, sequence the handoffs, and avoid dispatching a read-only auditor to patch code.
---

A roster is not an org. Nine roles produce nothing until work is routed to one of them with a clear owner, a bounded task, and a definition of done. This skill is the routing layer: it decides *who* acts, in *what order*, and what the handoff must contain so the next agent does not re-derive the context.

## The roster

| Role | Use when | Writes? |
|---|---|---|
| Coordinator | The task is vague, architectural, or spans roles | no |
| Developer | Application code, tests, builds, packaging | yes |
| Data | Corpus, ETL, schemas, dataset cleaning | yes |
| Operations | Services, units, logs, backups, mesh | yes |
| Security | Secrets, permissions, CVEs, PR loopholes | no |
| Business | Market, pricing, positioning, pitch docs | docs only |
| Design | UI, tokens, typography, accessibility | yes |
| Docs/Ops | Roster, briefs, onboarding, doc drift | docs only |
| Local/Offline | Offline personal tooling, local vaults | yes |

## Routing workflow

1. **Classify the request** into one primary domain. If two domains are equally primary, the task is not ready — split it.
2. **Check the owner.** One role owns the task end to end. Other roles are consulted, not co-owners.
3. **Choose the mode.** Single for one issue, parallel for independent issues, chain when step two needs step one's output.
4. **Write the task** with the target path, the constraint, and the done condition. A task that says "improve auth" is not a task.
5. **Respect the read-only boundary.** Coordinator and Security investigate and report. If the task needs a patch, the chain is Security → Developer.
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

- **Unknown scope:** Coordinator (plan) → Developer (implement) → Security (review).
- **New surface:** Design (tokens) → Developer (build) → Operations (deploy).
- **Data change:** Data (pipeline) → Developer (code) → Operations (storage).
- **Docs drift:** Docs/Ops (find drift) → Coordinator (decide) → Docs/Ops (fix).

## Anti-patterns

- **Dispatching the auditor to patch.** Coordinator and Security have no write tools by design; asking them to fix what they found produces a refusal or, worse, a fabricated diff. Chain to Developer instead.
- **Parallelising dependent work.** Two agents editing the same files race and lose changes. Parallel is for independent issues only; use a chain when step two reads step one.
- **Task without a first file.** The agent burns its context rediscovering the repo. Name the entry point.
- **No done condition.** "Make it better" returns an essay. Name the test, build, or artifact.
- **Co-ownership.** Two owners means neither verifies. One owner, explicit consults.
- **Dispatching without reading the result.** The usage and verification block is the signal; a confident summary with a failed command is a failed task.

For repo-level sequencing, see `org-issue-triage` and `org-cross-repo-change`. For the reliability and security procedures the roles apply, see `agentic-reliability` and `agentic-security`.
