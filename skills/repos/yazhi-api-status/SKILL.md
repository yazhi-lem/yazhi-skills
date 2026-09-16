---
name: yazhi-api-status
description: Use when working in the yazhi-api repository — adding an endpoint, a domain, an agent, or reviewing a PR against it. Helps you place new code in the right layer, respect the model-agnostic boundary, and avoid rebuilding work already scheduled in the Pilot/Launch roadmap.
---

`yazhi-api` is the central gRPC orchestrator for the whole Yazhi ecosystem — agents, IAM/Circle, retrieval, memory, and skills all route through it, but it never loads a model. Version 1.13.0 has the gRPC transport, IAM/Circle provisioning, two domain ingestion pipelines (legal, education), and the `YazhiAgent` framework in place. Two hard dates gate scope: **Pilot** (Oct 2026 — gRPC protocol freeze, Circle IAM/zero-trust tokens, core agent postures, installer CLI) and **Launch** (Dec 2026 — distributed ingestion, zero-cloud telemetry, Rust FFI bridges).

## Layer map

| Directory | What goes there | What never goes there |
|---|---|---|
| `services/` | Thin gRPC servicers; `.proto` is the contract | Business logic |
| `core/` | `pipeline.py` (orchestration), `router.py` (model + prompt selection) | Endpoint code |
| `domains/` | Per-domain schemas, disclaimers, ingestion, one package each | Cross-domain logic |
| `agents/` | `YazhiAgent` personas, goals, tool access | Guardian agents (see `guards/`) |
| `guards/` | Guardians bound to one child — consent gate, safety gate, the bond | Anything reached outside `Guardhouse.serve()` |
| `auth/` | API keys, JWT, IAM, Circle provisioning | Anything importable from `core/` |
| `scripts/` | Operational CLIs, run directly | Package imports |

## Workflow

1. **Read `CONTEXT.md` and `NEXT_ACTION.md` before touching anything** — they carry the live known-constraints list and the Pilot/Launch checklist; this skill summarizes them but they are ground truth.
2. **Never import or bundle model weights.** Adhan, Yazh, and future models are external services the pipeline calls — this is the one rule every contributor doc repeats.
3. **Before adding a new domain, land on `YazhiContext` first**, not the three currently-diverging context implementations (`core/pipeline.py`, `agents/common/context.py`, `domains/core/agents.py`) — building against the old pattern is the top-listed anti-pattern in `docs/API_AUDIT_AND_ROADMAP.md`.
4. **Reach a guardian only through `Guardhouse.serve()`.** Every other path skips the parental-consent gate and the safety gate on both sides of the model.
5. **Run `pytest -q` (775 tests) and `python scripts/ruff_baseline.py`** before opening a PR — the latter fails only on *new* ruff findings against the ~1,350-entry `.ruff-baseline.json`, so a blanket `ruff check --fix` will churn unrelated legacy code.
6. **Update `docs/` alongside any architectural change** and mirror new runtime deps from `pyproject.toml` into `requirements.txt` (`scripts/check_requirements_sync.py` enforces this).
7. **Never push this code to public GitHub** — Git-over-SSH only, per the repo's own contributor rules; the repo is private for a reason.

## Known constraints (fix with a migration, not a workaround)

- IAM state lives in module-level dicts (`auth/iam.py`) and is lost on restart — migrating onto `data/schema.sql` is an open Phase 1 item.
- `api_keys` has a CHECK constraint that predates the `core` and `governance` domains, so keys can't be issued for them yet; this is why 3 tests fail on a clean checkout (`iam_test.py`, `api_keys_test.py`, `apikeys_handler_test.py`) — they are the constraint, not a regression.
- `ChromaVectorStore` needs `chromadb`, which isn't declared in `pyproject.toml` — any agent with `vector_enabled: true` fails at `initialize()` until it's added behind an extra.
- `endpoints/legal.py` is deliberately disconnected pending a `LegalSearch` gRPC servicer.

## Next actions, in order

1. Land `core/context.py` (`YazhiContext`) and migrate the pipeline + agent framework onto it.
2. Act on `docs/DATA_QUALITY.md` — chiefly the 5,595 legal records with placeholder provenance.
3. Build data layers for `governance` (zero ingestion, zero retriever) and `health` (retriever exists, corpus empty).
4. Move the IAM store onto `data/schema.sql`.
5. Wire a third and fourth agent (`vaathi`, then `annachi`/`uzhavu`) past the `kural`/`kanaku` reference implementations.

## Anti-patterns

- **Building a new domain against the old context pattern** instead of waiting for `YazhiContext` — creates a fourth divergent implementation to unify later.
- **Treating the ruff baseline as a target to clear in one PR** — it can only shrink, never grow; a giant reformat PR is not the intended path.
- **Issuing API keys for `core` or `governance`** by loosening the CHECK constraint ad hoc instead of via a real migration.
- **Adding vector search silently** without declaring `chromadb`, leaving it inert at runtime with no error surfaced until `initialize()`.
- **Pushing to a public mirror or personal fork over HTTPS** — sovereignty and access control both depend on SSH-only distribution.

Cross-reference `yazhi-org-status` for how this repo fits the rest of the ecosystem, `sovereign-cloud-architecture` for the zero-cloud posture, and `secrets-management` for Circle/IAM credential handling.
