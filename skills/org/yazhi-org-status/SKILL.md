---
name: yazhi-org-status
description: Use when starting work in any yazhi-lem repository, planning cross-repo work, or briefing someone (human or agent) on where the Yazhi ecosystem stands. Helps you orient quickly to the current status, vision, and near-term priorities of each project instead of re-deriving them from scratch by reading nine repos.
---

Yazhi is a sovereign, zero-cloud Tamil-first AI ecosystem spanning nine repositories under `github.com/yazhi-lem`, built around one non-negotiable rule: no model weights, no cloud dependency, no external API keys by default. Every product traces back to the same nervous system (`yazhi-api`) and the same underlying model family (Adhan/Yazh). An agent dropped into one of these repos without this context re-derives the ecosystem shape from grep, which wastes a session rediscovering what a one-page briefing already answers.

## The nine repos

| Repo | Purpose | Stack | Status |
|---|---|---|---|
| `yazhi-api` | Central gRPC orchestrator: agents, IAM/Circle, RAG, memory, skills | Python 3.11, gRPC, SQLite | v1.13.0 — gRPC transport, IAM/Circle, two ingestion pipelines live; Pilot Oct 2026, Launch Dec 2026 |
| `adhan` | From-scratch Tamil SLM: swaram-token tokenizer, JAX/Flax training | Python, JAX/Flax, MLflow | Phase 0 + A done; Phase 3 (pretrain `adhan-nano`) in progress |
| `open-sangam` | Sangam-era Tamil literature reader + AI agent assembly (சங்க அவை) | React/Vite, Firebase, Gemini via OpenRouter | Phase 1 (scrape/normalize) done — 18 poems, 2,552 verses; Phase 2 (English translation) drafting nightly; Phase 3 (reader) in progress |
| `yazh-unity` | AR/XR Tamil pet app, on-device ONNX inference | Unity 6, C#, Barracuda | Production-ready code; blocked on Play Store / App Store signing credentials (founder gate) |
| `illakiya` | Native Tamil (PM0100/Tholkaappiyam) Android keyboard | Rust core + Kotlin/Compose via UniFFI | Working 836-word dictionary + sandhi engine; pre-1.0 |
| `capitol` | Internal AI/ML ops + people console: annotation, agents, models | Next.js 16, React 19, TypeScript | Early scaffold — console/annotation/audit/people pages stubbed, no backend wired |
| `yazh-kutty` | 30K-vocabulary Tamil model for kids | — | Named, empty repo — not started |
| `yazhi-dev` | yazhi.dev community site + `/chat` demo | Next.js, Framer Motion | Chat UI streams through `yazhi-api`; immersive-site redesign at design-doc stage |
| `styleguide` | Fork of Google's style guides | — | Reference only — `yazhi-api`'s Python style is enforced against this |

## Vision

Sovereign, air-gap-capable Tamil AI: a child, or anyone, should be able to talk, learn, and read in Tamil — natively, not through translation — on infrastructure nobody outside the organization can be compelled to hand over. `yazhi-api` never touches model weights, so Adhan, Yazh, or a future model can sit behind it interchangeably; `open-sangam` and `illakiya` supply the literary corpus and native input method the models are trained and reasoned over; `yazh-unity`, `yazh-kutty`, and `yazhi-dev` are the surfaces a family actually touches.

## Workflow

1. **Read the repo's own context file first** — `CONTEXT.md` / `NEXT_ACTION.md` (`yazhi-api`), `ROADMAP_JAX_SLM.md` (`adhan`), `docs/ROADMAP.md` + `docs/PROJECT_TRACKER.md` (`open-sangam`). This skill is the map, not the territory — it goes stale the moment a phase closes.
2. **Check the milestone dates before proposing scope.** `yazhi-api` has two hard dates: Pilot (Oct 2026 — gRPC protocol freeze, Circle IAM, core agent postures, installer CLI) and Launch (Dec 2026 — distributed ingestion, zero-cloud telemetry, Rust FFI bridges). Flag work serving neither instead of silently absorbing it.
3. **Never add a model or model weight into `yazhi-api`.** It calls Adhan/Yazh as external services, by design.
4. **For Tamil-text work, check the domain skill first** — `tamil-text-processing`, `tamil-aksharas`, `tamil-morphology-nlp` — before reinventing the swaram/akshara handling `adhan` and `illakiya` already implement.
5. **Treat `yazh-unity` and `yazh-kutty` as founder-gated.** The former is blocked purely on signing credentials, not engineering. The latter has no code yet; confirm scope before starting.
6. **Refresh this table** when a repo's phase, version, or blocker changes, so the next session doesn't re-clone nine repos to relearn the same status lines.

## Next course of action, by repo (most urgent first)

1. `open-sangam` — close Agents M1 (ஔவையார் Avvaiyar eval set, due 2026-08-31), parse colophon metadata (Corpus Phase C), keep the nightly English-translation pipeline running Phase 1 → 3.
2. `yazhi-api` — land `core/context.py` (`YazhiContext`) before new domain work; fix the `api_keys` CHECK-constraint migration (3 known-failing tests); build data layers for the empty `governance` and `health` domains.
3. `adhan` — finish Phase 3 pretraining of `adhan-nano`, then Phase 4 Tamil-specific eval probes.
4. `yazh-unity` — unblock signing credentials (Play Store + App Store); everything else is done.
5. `illakiya` — grow the dictionary past 836 words and widen sandhi rule coverage.
6. `capitol` — decide whether this ships at all before wiring a backend; today it is UI scaffold only.
7. `yazh-kutty` — scope and start, or fold into `adhan`'s nano tier if redundant.

## Anti-patterns

- **Building a new domain agent against the old context pattern.** `yazhi-api` has three divergent context implementations mid-unification; a fourth compounds the exact problem `YazhiContext` exists to fix.
- **Treating a founder-gated blocker as an engineering task.** `yazh-unity`'s only blocker is a signing key/certificate; refactoring its build pipeline doesn't move the launch date.
- **Assuming "public repo" means "push freely."** `yazhi-api` is private, and its own contributor rules say never push Yazhi code to public GitHub over HTTPS — Git-over-SSH only.
- **Overriding the ruff baseline wholesale.** `yazhi-api` carries roughly 1,350 pre-existing lint findings on purpose (`.ruff-baseline.json`); run `scripts/ruff_baseline.py`, not a blanket `ruff check --fix`.
- **Re-deriving corpus stats by hand.** `open-sangam`'s README numbers are a snapshot from 2026-08-04; use `python -m ai.translate_with_gemini --status` for the current figures instead.

Cross-reference `sovereign-cloud-architecture` and `airgapped-llm-deployment` for the infrastructure posture behind "zero-cloud by default," `fine-tuning-workflow` for `adhan`'s pretraining loop, and `tamil-text-processing` / `tamil-aksharas` for the swaram/akshara-level handling shared by `adhan` and `illakiya`.
