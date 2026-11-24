---
name: org-service-boundaries
description: Use when deciding where a new capability belongs in the Yazhi stack — yazhi-api, Adhan, Illakiya, open-sangam, or a client — and a sovereign or local-first constraint is at stake. Helps you keep model weights, external APIs, and Tamil NLP logic in their owning repos.
---

The Yazhi ecosystem is held together by a few hard constraints: no model weights or cloud dependency in the orchestrator by default, Tamil language work owned by the language repos, and clients that consume contracts rather than reimplement them. When a feature could live in several places, choosing by convenience creates a second source of truth and quietly breaks the sovereign posture. This skill owns the placement decision; implementation details stay with the owning status skill.

## Ownership map

| Capability | Owner | Why there | Do not put it in |
|---|---|---|---|
| Inference orchestration, agents, IAM, RAG routing | `yazhi-api` (private, gRPC) | Central service, agent-native, local-first | Clients or model repos |
| Model weights, tokenizer, training, eval | `adhan` | Model lifecycle and corpus belong together | `yazhi-api` (hard rule), mobile apps |
| Keyboard layouts, sandhi, dictionary, input engine | `illakiya` (Rust core → Kotlin) | One engine across input surfaces | Kotlin UI or client apps |
| Sangam corpus, translation pipeline, Avai prompt | `open-sangam` | Corpus and scholarly review flow | `yazhi-api` ingestion code |
| AR gameplay, on-device runtime, store packaging | `yazh-unity` | Device lifecycle and store gates | The orchestrator |
| Site, community pages, `/chat` demo | `yazhi-dev` | Public surface consumes contracts | Backend service logic |
| Shared docs/skill contracts | `yazhi-skills` | One source of truth for agents | Every individual repo |

## Workflow

1. **State the requirement in one sentence, including the data it touches.** "Rewrite a child's Tamil message formally, on device" is placeable; "add AI" is not.
2. **Check the constraint list in `yazhi-api/CONTEXT.md` before choosing a home.** No weights in the orchestrator, no external API keys or cloud dependencies by default, local network first. A design that needs one of those is a design that needs explicit sign-off, not a default.
3. **Find the owning repo in the table, then read its status skill** (`adhan-status`, `illakiya-status`, `open-sangam-status`, `yazh-unity-status`, `yazhi-dev-status`) for its current phase and conventions.
4. **Choose the narrowest seam.** Prefer a client calling an existing gRPC method over adding a new backend capability; prefer extending the Rust core over copying Tamil logic into Kotlin or Unity.
5. **If the capability spans two owners, write the contract first** and sequence the work with `org-cross-repo-change` — the owner of the data or model defines the interface, consumers adapt.
6. **Name the failure mode you are avoiding in the PR description** — e.g. "weights stay in Adhan; api calls it over gRPC" — so reviewers can verify the boundary rather than trusting intent.
7. **Update the owner's docs index and the ecosystem map when the boundary changes.** A new service or a new dependency is a status change, not just a code change.

## Anti-patterns

- **Loading a model in `yazhi-api` "temporarily" for a demo.** It breaks the central no-weights rule and turns a stateless orchestrator into a deployment that needs the model artifact.
- **Adding an external API key as the default path.** Sovereign deployments must work offline; keep any third-party call opt-in and behind a documented fallback.
- **Duplicating Tamil grapheme/sandhi logic in a client.** Illakiya's Rust core already owns it; a second copy diverges on edge cases and fails grapheme tests differently.
- **Putting corpus review into the ingestion pipeline.** open-sangam's `verified: false` scholar-review flow exists for a reason; bypassing it publishes unverified translations.
- **Building a new domain agent against old context implementations.** `yazhi-api` has several context paths mid-unification; a fourth makes the eventual merge harder.

For the repo map see `yazhi-org-status`; for contract sequencing see `org-cross-repo-change`; for offline deployment patterns see `airgapped-llm-deployment` and `sovereign-cloud-architecture`; for LLM-specific risks see `llm-security-review`.
