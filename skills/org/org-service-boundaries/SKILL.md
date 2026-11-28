---
name: org-service-boundaries
description: Use when deciding where a new capability belongs across a multi-repo stack — service, model, app, content, client, or site — and a local-first or sovereignty constraint is at stake. Helps you keep model weights, external APIs, and language logic in their owning repos instead of duplicating them in a client.
---

A multi-repo stack is held together by a few hard constraints: no model weights or cloud dependency in the orchestrator by default, language-specific logic owned by the language repos, and clients that consume contracts rather than reimplement them. When a feature could live in several places, choosing by convenience creates a second source of truth and quietly breaks the local-first posture. This skill owns the placement decision; implementation details stay with the owning repo.

## Ownership map

| Capability | Owner | Why there | Do not put it in |
|---|---|---|---|
| Inference orchestration, agents, IAM, routing | `<service-repo>` (gRPC) | Central service, agent-native, local-first | Clients or model repos |
| Model weights, tokenizer, training, eval | `<model-repo>` | Model lifecycle and corpus belong together | The service repo (hard rule), mobile apps |
| Layouts, language rules, dictionaries, input engines | `<app-repo>` (core → UI) | One engine across input surfaces | UI layers or client apps |
| Corpus, translation pipeline, domain prompts | `<content-repo>` | Corpus and scholarly review flow | Service ingestion code |
| Gameplay, on-device runtime, store packaging | `<client-repo>` | Device lifecycle and store gates | The orchestrator |
| Site, community pages, demo surfaces | `<site-repo>` | Public surface consumes contracts | Backend service logic |
| Shared docs and skill contracts | `<skills-repo>` | One source of truth for agents | Every individual repo |

## Workflow

1. **State the requirement in one sentence, including the data it touches.** "Rewrite a child's message formally, on device" is placeable; "add AI" is not.
2. **Check the owning repo's constraint document before choosing a home.** No weights in the service, no external API keys or cloud dependencies by default, local network first. A design that needs one of those is a design that needs explicit sign-off, not a default.
3. **Find the owning repo in the table, then read its current docs and conventions.** A repo map or status note is orientation; the repo's `README.md` and `docs/README.md` are authoritative.
4. **Choose the narrowest seam.** Prefer a client calling an existing service method over adding a new backend capability; prefer extending the shared core over copying language logic into a UI or client.
5. **If the capability spans two owners, write the contract first** and sequence the work with `org-cross-repo-change` — the owner of the data or model defines the interface, consumers adapt.
6. **Name the failure mode you are avoiding in the PR description** — e.g. "weights stay in the model repo; the service calls it over gRPC" — so reviewers can verify the boundary rather than trusting intent.
7. **Update the owner's docs index when the boundary changes.** A new service or a new dependency is a status change, not just a code change.

## Anti-patterns

- **Loading a model in the service repo "temporarily" for a demo.** It breaks the central no-weights rule and turns a stateless orchestrator into a deployment that needs the model artifact.
- **Adding an external API key as the default path.** Sovereign deployments must work offline; keep any third-party call opt-in and behind a documented fallback.
- **Duplicating language or grapheme logic in a client.** The shared core already owns it; a second copy diverges on edge cases and fails tests differently.
- **Putting corpus review into the ingestion pipeline.** The content repo's review flow exists for a reason; bypassing it publishes unverified work.
- **Building a new domain agent against old context implementations.** The service repo already has divergent context paths; a fourth makes the eventual merge harder.

For contract sequencing see `org-cross-repo-change`; for offline deployment patterns see `airgapped-llm-deployment` and `sovereign-cloud-architecture`; for LLM-specific risks see `llm-security-review`.
