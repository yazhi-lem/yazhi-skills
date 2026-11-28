---
name: org-cross-repo-change
description: Use when one change must land in two or more repositories — a proto/API contract, shared language logic, a data schema, or a doc contract — and merge order matters. Helps you sequence producers before consumers and keep every repo buildable after each merge.
---

Products split across repos are joined at a few narrow contracts: the service's gRPC surface, the model's tokenizer interface, the app's input engine, and the shared docs/skills contracts. A change that crosses one of those seams needs an order, or the first merge breaks the other repo until a follow-up lands. This skill owns that ordering; per-repo conventions stay in each repo's docs.

## Contract map

| Contract | Producer | Consumers | Merge order |
|---|---|---|---|
| gRPC service / proto change | `<service-repo>` | `<client-repo>`, `<site-repo>`, `<app-repo>` | Compatible additive change first, clients second, remove old field last |
| Model or tokenizer interface | `<model-repo>` | `<service-repo>`, `<client-repo>` | Publish interface + version, then update callers, then switch default |
| Language layout / rules / dictionary | `<app-repo>` | `<client-repo>`, `<site-repo>` | Core change, then web/mobile consumers |
| Corpus / domain pipeline | `<content-repo>` | `<service-repo>`, `<site-repo>` | Pipeline output schema, then ingestion, then UI |
| Docs or skill contract | `<skills-repo>` | every repo | Agree contract, then migrate docs in one repo at a time |

## Workflow

1. **Name the contract and its owner repo** before writing code. If you cannot say which repo produces the contract, the change is not scoped yet — read the two repos' docs indexes first.
2. **List every consumer explicitly**, including private/local repos and the shared skill catalog. Search for the old field, function, or doc path across all repos instead of relying on memory.
3. **Make the producer change backward-compatible when possible** — add a field, keep the old one, default the new behavior off. A compatible change lets producers and consumers merge in either order; use that to avoid coordinated downtime.
4. **Sequence PRs so each merge leaves both repos working.** Where compatibility is impossible, merge the consumer's tolerance for both versions *first*, then the producer change, then cleanup. Record the PR order in each PR description.
5. **Verify at each step with the consumer's own checks**, not just the producer's tests — run the client build/integration test against the new contract, and confirm no repo is left importing a path that only exists on a branch.
6. **Update the owning docs in the same PR as the contract** — `docs/README.md`, `CONTEXT.md`, or the skill contract — and regenerate derived artifacts when the skills repo is involved.
7. **Close the loop after all merges** by removing the temporary compatibility shim in a separate PR and noting the final contract version in the owning docs.

## Anti-patterns

- **Merging the breaking change first** and promising to fix consumers "in the next PR" — leaves the ecosystem broken for anyone who pulls in between.
- **Assuming a private repo is not a consumer.** A private service can still be central; breaking its contract silently breaks every client.
- **Changing a contract without updating its owning doc.** Code and docs then disagree, and the next agent follows the stale doc.
- **Duplicating language logic in a client "temporarily"** instead of extending the owning core — two implementations of the same rules drift within one release.
- **Reordering merges without recording why.** Future maintainers cannot tell which compatibility shim is safe to remove; each PR should state the contract version it targets.

For API-level compatibility details see `api-design`; for the doc-side rules see `technical-documentation`; for boundary ownership see `org-service-boundaries`; for recovery when a change revives a retired plan see `org-plan-reset-recovery`.
