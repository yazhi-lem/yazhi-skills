---
name: org-cross-repo-change
description: Use when one change must land in two or more Yazhi repositories — a proto/API contract, shared Tamil logic, a data schema, or a doc contract — and merge order matters. Helps you sequence producers before consumers and keep every repo buildable after each merge.
---

Yazhi products are separate repos joined at a few narrow contracts: yazhi-api's gRPC surface, Adhan's tokenizer/model interface, Illakiya's input engine, and the shared docs/skills contracts. A change that crosses one of those seams needs an order, or the first merge breaks the other repo until a follow-up lands. This skill owns that ordering; per-repo conventions stay with the status skills.

## Contract map

| Contract | Producer | Consumers | Merge order |
|---|---|---|---|
| gRPC service / proto change | `yazhi-api` | `yazh-unity`, `yazhi-dev`, `illakiya` | Compatible additive change first, clients second, remove old field last |
| Model or tokenizer interface | `adhan` | `yazhi-api`, `yazh-unity` | Publish interface + version, then update callers, then switch default |
| Tamil layout / sandhi / dictionary | `illakiya` | `yazh-unity`, `yazhi-dev` | Core Rust change, then web/mobile consumers |
| Corpus / Avai pipeline | `open-sangam` | `yazhi-api`, `yazhi-dev` | Pipeline output schema, then ingestion, then UI |
| Docs or skill contract | `yazhi-skills` | every repo | Agree contract, then migrate docs in one repo at a time |

## Workflow

1. **Name the contract and its owner repo** before writing code. If you cannot say which repo produces the contract, the change is not scoped yet — stop and read `yazhi-org-status` and the two relevant status skills.
2. **List every consumer explicitly**, including private/local repos and the shared skill catalog. Search for the old field, function, or doc path across all repos instead of relying on memory.
3. **Make the producer change backward-compatible when possible** — add a field, keep the old one, default the new behavior off. A compatible change lets producers and consumers merge in either order; use that to avoid coordinated downtime.
4. **Sequence PRs so each merge leaves both repos working.** Where compatibility is impossible, merge the consumer's tolerance for both versions *first*, then the producer change, then cleanup. Record the PR order in each PR description.
5. **Verify at each step with the consumer's own checks**, not just the producer's tests — run the client build/integration test against the new contract, and confirm no repo is left importing a path that only exists on a branch.
6. **Update the owning docs in the same PR as the contract** — `docs/README.md`, `CONTEXT.md`, or the skill contract — and regenerate derived artifacts (`skills.json`, bundles) when `yazhi-skills` is involved.
7. **Close the loop after all merges** by removing the temporary compatibility shim in a separate PR and noting the final contract version in the status docs.

## Anti-patterns

- **Merging the breaking change first** and promising to fix consumers "in the next PR" — leaves the ecosystem broken for anyone who pulls in between.
- **Assuming a private repo is not a consumer.** `yazhi-api` is private but central; breaking its contract silently breaks every client.
- **Changing a contract without updating its owning doc.** Code and docs then disagree, and the next agent follows the stale doc.
- **Duplicating Tamil logic in a client "temporarily"** instead of extending the owning core — two implementations of sandhi or grapheme rules drift within one release.
- **Reordering merges without recording why.** Future maintainers cannot tell which compatibility shim is safe to remove; each PR should state the contract version it targets.

For API-level compatibility details see `api-design`; for the doc-side rules see `technical-documentation`; for boundary ownership see `org-service-boundaries`; for recovery when a change revives a retired plan see `org-plan-reset-recovery`.
