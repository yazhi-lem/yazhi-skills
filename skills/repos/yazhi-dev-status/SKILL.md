---
name: yazhi-dev-status
description: Use when working in the yazhi-dev repository — the yazhi.dev marketing/community site and its /chat demo. Helps you keep the chat UI's backend contract intact and avoid re-designing a site that already went through one full visual pivot.
---

This is Yazhi's public-facing community site (yazhi.dev), a Next.js app whose job is to explain the ecosystem — Adhan, Open Sangam, Yazh — to visitors, plus a working `/chat` demo that proxies real conversations through `yazhi-api` (see `yazhi-api-status` for that service). The site already went through one complete visual pivot: v1 was a cyberpunk/neon theme (archived at `previous-designs/v1-cyberpunk/`), replaced in July 2026 with an immersive, scroll-driven Sangam-era 3D open-world experience (`src/three/`: `ThinaiWorld`, `Terrain`, `SangamObjects`, `CameraRig`, one procedural heightfield zone for each tinai). `INDEX.md` is a still-current design brief for a further "high-contrast dark mode" iteration — read it as intent, not as what's already built.

## Status at a glance

| Surface | State |
|---|---|
| Marketing site (3D open-world) | ✅ Shipped 2026-07-08 — 5 procedural tinai zones, scroll-driven camera |
| Marketing site (v1 cyberpunk) | Archived at `previous-designs/v1-cyberpunk/`, not deleted |
| `/chat` demo | Working — agents bound to Gemini or ChatGPT personas, but replies stream through `yazhi-api`, never directly from the browser |
| `INDEX.md` design brief | Describes a further redesign direction (neon/holographic dark mode) — not yet built |
| Backend integration | OpenAI-compatible Chat Completions + SSE, single integration point at `src/lib/chat/backend.ts` |

## Workflow

1. **Never call an LLM provider directly from the browser.** `/chat` is explicitly designed so replies stream through the `yazhi-api` backend — copy `.env.example` to `.env` and set `YAZHI_API_URL` (and optionally `YAZHI_API_KEY`, `YAZHI_CHAT_PATH`) rather than adding a client-side API key.
2. **Treat `src/lib/chat/backend.ts` as the one integration point** for the chat contract (OpenAI-compatible Chat Completions, SSE streaming) — don't duplicate request/response shaping elsewhere in the app.
3. **Check `previous-designs/v1-cyberpunk/ARCHIVE_README.md` before discarding a v1 pattern** — it documents the design philosophy and patterns explicitly kept for potential reuse, not dead code to delete.
4. **Read `INDEX.md` as the target for the next visual iteration, not the current state.** It describes three core sections (Adhan digital-data-stream, Open Sangam digital-Madurai-construct, Yazh connected-node-network) that may not exist yet in the live 3D-open-world build.
5. **Before adding a new agent persona to `/chat`**, check `src/lib/chat/agents.ts` for the existing provider-binding pattern (fixed to Gemini or ChatGPT, each with its own persona/system prompt) rather than inventing a new binding mechanism.
6. **Remember sessions/messages persist only in browser `localStorage`** — there's no server-side chat history; don't build a feature that assumes durable server-side conversation state without adding it first.
7. **This repo's `AGENTS.md` flags a breaking-changes warning for its Next.js version** — read `node_modules/next/dist/docs/` for the installed version's actual API before assuming training-data-era Next.js conventions apply.

## Next actions

1. Decide whether `INDEX.md`'s further redesign direction (neon/holographic dark mode) is still the target after the July 2026 3D-open-world ship, or superseded by it.
2. Until `YAZHI_API_URL` is configured, `/chat` shows a "not configured" notice by design — confirm this is set in every deployment environment rather than treating it as a bug.
3. Consider whether chat history should move from `localStorage`-only to a server-backed store if multi-device continuity becomes a requirement.

## Anti-patterns

- **Wiring `/chat` to call Gemini or OpenAI directly from client code** — defeats the entire point of routing through `yazhi-api`, and would leak API keys to the browser.
- **Deleting `previous-designs/v1-cyberpunk/`** as "old code" — it's a deliberately preserved design reference, not dead weight.
- **Building against `INDEX.md` as if it describes the current site** — it's a design brief; verify against the actual `src/three/` components for what's live today.
- **Assuming standard Next.js API/conventions from training data** without checking `node_modules/next/dist/docs/` first — `AGENTS.md` exists specifically because this version has breaking changes from what most training data reflects.
- **Adding server-side chat persistence silently** without updating the privacy/data-handling story — today's `localStorage`-only design is a stated choice, not an oversight.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture and `yazhi-api-status` for the backend contract `/chat` depends on.
