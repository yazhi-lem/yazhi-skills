---
name: yazhi-dev-status
description: Use when working in the yazhi-dev repository — the yazhi.dev marketing/community site and its /chat demo. Helps you keep the chat UI's backend contract intact and avoid re-designing a site that already went through one full visual pivot.
---

This is Yazhi's public-facing community site (yazhi.dev), a Next.js app whose job is to explain the ecosystem — Adhan, Open Sangam, Yazh — to visitors, plus a `/chat` demo that proxies conversations through yazhi-api. The site went through one complete visual pivot: the v1 cyberpunk theme was removed on 2026-10-27 and survives in git history (see [archives/README.md](https://github.com/yazhi-lem/yazhi-dev/blob/main/archives/README.md)), replaced in July 2026 with an immersive, scroll-driven Sangam-era 3D experience (`src/three/`). The old `INDEX.md` design brief was retired at the same time; [`docs/README.md`](https://github.com/yazhi-lem/yazhi-dev/blob/main/docs/README.md) is the current doc index.

## Status at a glance

| Surface | State |
|---|---|
| Marketing site (3D open-world) | ✅ Shipped 2026-07-08 — 5 procedural tinai zones, scroll-driven camera |
| Marketing site (v1 cyberpunk) | Removed 2026-10-27; recoverable from git history |
| `/chat` demo | Working — agents bound to Gemini or ChatGPT personas, but replies stream through `yazhi-api`, never directly from the browser |
| `INDEX.md` design brief | Retired 2026-10-27; do not treat as a live target |
| Backend integration | OpenAI-compatible Chat Completions + SSE, single integration point at `src/lib/chat/backend.ts` |

## Workflow

1. **Never call an LLM provider directly from the browser.** `/chat` is explicitly designed so replies stream through the `yazhi-api` backend — copy `.env.example` to `.env` and set `YAZHI_API_URL` (and optionally `YAZHI_API_KEY`, `YAZHI_CHAT_PATH`) rather than adding a client-side API key.
2. **Treat `src/lib/chat/backend.ts` as the one integration point** for the chat contract (OpenAI-compatible Chat Completions, SSE streaming) — don't duplicate request/response shaping elsewhere in the app.
3. **Check `archives/2026-10-27-docs-digest.md` before reviving a v1 pattern** — it records what was deliberately retired and why.
4. **Read `docs/SITE.md` for the live 3D world and design tokens.** The old `INDEX.md` brief described a further dark-mode iteration; it was retired and is not a current target.
5. **Before adding a new agent persona to `/chat`**, check `src/lib/chat/agents.ts` for the existing provider-binding pattern (fixed to Gemini or ChatGPT, each with its own persona/system prompt) rather than inventing a new binding mechanism.
6. **Remember sessions/messages persist only in browser `localStorage`** — there's no server-side chat history; don't build a feature that assumes durable server-side conversation state without adding it first.
7. **This repo's `AGENTS.md` flags a breaking-changes warning for its Next.js version** — read `node_modules/next/dist/docs/` for the installed version's actual API before assuming training-data-era Next.js conventions apply.

## Next actions

1. Confirm the current visual direction against `docs/SITE.md` and `src/three/` — the retired `INDEX.md` brief is not a planning input.
2. Until `YAZHI_API_URL` is configured, `/chat` shows a "not configured" notice by design — confirm this is set in every deployment environment rather than treating it as a bug.
3. Consider whether chat history should move from `localStorage`-only to a server-backed store if multi-device continuity becomes a requirement.

## Anti-patterns

- **Wiring `/chat` to call Gemini or OpenAI directly from client code** — defeats the entire point of routing through `yazhi-api`, and would leak API keys to the browser.
- **Reviving retired design docs as current briefs.** `INDEX.md` and `previous-designs/` were removed deliberately; use git history, not the live tree.
- **Building against retired design docs as if they describe the current site** — verify against `docs/SITE.md` and `src/three/` for what's live today.
- **Assuming standard Next.js API/conventions from training data** without checking `node_modules/next/dist/docs/` first — `AGENTS.md` exists specifically because this version has breaking changes from what most training data reflects.
- **Adding server-side chat persistence silently** without updating the privacy/data-handling story — today's `localStorage`-only design is a stated choice, not an oversight.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture, including the `yazhi-api` backend that `/chat` depends on.
