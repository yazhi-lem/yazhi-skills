---
name: yazhi-org-status
description: Use when starting work in any yazhi-lem repository, planning cross-repo work, or briefing someone (human or agent) on where the Yazhi ecosystem stands. Helps you orient quickly to the current status, vision, and near-term priorities of each project without re-deriving them from eleven repos.
---

Yazhi is a sovereign, Tamil-first AI ecosystem built around one rule: no model weights, no cloud dependency, no external API keys by default. Every product traces back to the same orchestrator (`yazhi-api`) and model family (Adhan/Yazh). This skill is a map, not the territory — each repo's `README.md` and `docs/README.md` own its current state.

## The repos

Each public repo has a dedicated status skill with a fuller layer map and workflow. Read the table for orientation, that skill before touching code.

| Repo | Purpose | Status snapshot (verified 2026-11-21) | Detail |
|---|---|---|---|
| `yazhi-api` | gRPC orchestrator: agents, Circle IAM, RAG, memory | v1.13.0; transport, IAM and ingestion pipelines live. Planning was reset on 2026-11-21; status lives in `CONTEXT.md` and `docs/README.md` | private, no public skill |
| `adhan` | From-scratch Tamil SLM, Swaram tokenizer, JAX training | Tokenizer benchmark published; nano training/eval in progress. See `adhan/docs/README.md` | `adhan-status` |
| open-sangam | Sangam literature reader, corpus pipeline, சங்க அவை agent | Layered reader + corpus + Avai agent; README counts are a snapshot. See [docs/README.md](https://github.com/yazhi-lem/open-sangam/blob/main/docs/README.md) | `open-sangam-status` |
| `yazh-unity` | AR/XR Tamil pet app | Endless-runner pivot; bundled ONNX files are placeholders; store credentials founder-gated | `yazh-unity-status` |
| `illakiya` | Native Tamil keyboard + Sarvam-powered writing web app | Web app live; Rust/Kotlin core pre-1.0. See `illakiya/docs/README.md` | `illakiya-status` |
| yazhi-dev | Public community site + `/chat` demo | 3D site shipped; chat streams through yazhi-api. See [docs/README.md](https://github.com/yazhi-lem/yazhi-dev/blob/main/docs/README.md) | `yazhi-dev-status` |
| `capitol` | Local Linear/GitHub/Slack operator console | Live tooling with a 2026-10-03 data snapshot; see `capitol/README.md` | private |
| `styleguide` | Fork of Google style guides | Upstream reference, last synced 2025-11-13 — not Yazhi policy | `styleguide-status` |
| `yazhi-skills` | Shared skill catalog | 99 skills, including `technical-documentation` and the `org/` ways-of-working skills | — |
| `books`, `yazh-kutty` | Placeholder repos | No commits or code yet; founder-gated scope | — |

## Workflow

1. **Read the repo's own context file first** — `CONTEXT.md` / `README.md` / `docs/README.md`. The old `NEXT_ACTION.md`, `factory/*`, `ROADMAP_JAX_SLM.md`, `docs/ROADMAP.md` and `docs/PROJECT_TRACKER.md` were retired on 2026-11-21; do not relink to them.
2. **Check milestone dates before proposing scope.** Launch dates were cleared during the November replan; treat dated plans in `archives/` as history, not commitments.
3. **Never add a model or model weight to `yazhi-api`.** It calls Adhan/Yazh as external services by design.
4. **For Tamil-text work, check the domain skill first** — `tamil-text-processing`, `tamil-aksharas`, `tamil-morphology-nlp` — before reinventing what `adhan` and `illakiya` already implement.
5. **Treat `yazh-unity` as founder-gated for store launch**, but not for engineering: gameplay and docs work can proceed while signing credentials are awaited.
6. **Refresh this table** when a repo's phase, version or blocker changes, so the next session doesn't re-clone eleven repos to relearn the same lines.

## Durable next steps (verify in each repo before acting)

1. `adhan` — finish `adhan-nano` pretraining, then Tamil eval probes in `docs/behaviour/EVAL_TAMIL.md`.
2. `open-sangam` — keep the nightly translation pipeline phase-ordered and every draft `verified: false` until scholar review.
3. `yazhi-api` — respect the post-replan status in `CONTEXT.md`; do not resurrect the retired V2 plan.
4. `yazh-unity` — founder provides signing credentials; engineering keeps `docs/MODEL_STATUS.md` honest about placeholder weights.
5. `illakiya` — grow the dictionary and widen sandhi coverage from the Rust core, not in Kotlin.

## Anti-patterns

- **Building a new domain agent against the old context pattern.** `yazhi-api` has divergent context implementations mid-unification; a fourth compounds the problem.
- **Treating a founder-gated blocker as an engineering task.** Signing keys are not a build-script problem.
- **Assuming "public repo" means "push freely."** `yazhi-api` is private; use Git-over-SSH only.
- **Overriding the ruff baseline wholesale.** Run `scripts/ruff_baseline.py`, not `ruff check --fix`.
- **Re-deriving corpus stats by hand.** Run `python -m ai.translate_with_gemini --status` from `open-sangam/backend/python/`.

Cross-reference the per-repo skills above for detail below ecosystem level, the `eco/` skills for work that spans repos, `technical-documentation` for the shared doc contract, and `sovereign-cloud-architecture` / `airgapped-llm-deployment` for the zero-cloud posture.
