---
name: open-sangam-status
description: Use when working in the open-sangam repository — the Sangam-era Tamil literature reader, its corpus pipeline, or the சங்க அவை (Sangam Avai) agent assembly. Helps you find the current phase and horizon before proposing scope, and avoid re-scraping or re-translating work already tracked.
---

Open Sangam turns archaic web archives of Sangam-era poetry into a layered learning platform — "Duolingo for Ancient Literature." The critical path is **corpus data → knowledge graph → reader + agents**: richer, verified data unlocks nearly everything downstream, so most useful work traces back to the corpus pipeline in `backend/python/`.

## Phase status

| Phase | Scope | Status |
|---|---|---|
| 1 — Data scraping & normalization | 18 poems → OKF datapackage | ✅ Complete — 2,552 verses |
| 2 — AI English translation + human verification | Gemini 2.5 Flash via OpenRouter, nightly | 🔄 In progress — 0% English so far, pipeline live |
| 3 — Library of Sangam reader (MVP) | React/Vite frontend | 🔄 In progress |
| 4 — Community contribution layer | Scholar-reviewed edits | ⬜ Pending |

Translation runs in three size-ordered phases (smallest first, so quality problems surface early): Phase 1 the Ten Idylls (~380 verses), Phase 2 the shorter anthologies (~472 verses), Phase 3 the large anthologies (~1,700 verses). Every draft lands `verified: false` until a scholar reviews it — never treat AI output here as authoritative.

## Workflow

1. **Read `docs/ROADMAP.md` (vision + horizons) and `docs/PROJECT_TRACKER.md` (live status) before scoping anything** — the README's corpus tables are a snapshot, not the source of truth.
2. **Get live corpus figures from the tool, not the README**: `python -m ai.translate_with_gemini --status` from `backend/python/` — no API key needed, no writes.
3. **Never run the translator without `--dry-run` first** when testing a new selector or phase override — `--dry-run` resolves and lists the batch with zero API calls.
4. **Run the Sangam Avai agents from `agents/`, never from `agents/avai/`.** ADK resolves agents relative to the parent directory; running from inside `avai/` is the single most common setup failure, per the repo's own README warning.
5. **Respect the phase order in `data-governance.md`.** A `--force` re-translate or a `--poem` override that jumps ahead of the current phase should be a deliberate, reviewed choice, not a default habit.
6. **For frontend work, check `docs/data-collection-plan.md` and open GitHub issues before building new UI against assumed-missing data** — Ainkurunooru and Poruṉarāṟṟuppaṭai were previously gaps but are now in the corpus; treat them as needing verification, not scraping.

## Next actions, by horizon

**Horizon 1 (now, Q3 2026):**
1. Finish Agents M1 — replace the 3-case smoke test with a formal `adk eval` evalset (~10 cases, repeat-aware) for ஔவையார் Avvaiyar.
2. Corpus Phase C — parse colophons into structured `author`/`patron`/`turai`/`speaker` fields; backfill `tinai: unknown`; auto-seed `poets.json`/`patrons.json`.
3. Data-quality pass on Ainkurunooru and Poruṉarāṟṟuppaṭai — verify, don't re-scrape.
4. Frontend quick wins: modal close-button a11y, wiring 3D scenes to real verse data, Library layout/animation polish.
5. Correct remaining Firebase-Hosting → Cloudflare-Pages references in architecture docs.

**Horizon 2 (next, Q4 2026):**
1. Agents M2 — the poet swarm: Tholkappiyar (scenario extraction), Kapilar (poem recreation), Paranar (imagery + pluggable image backend), Nakkirar (convener + peer-mesh routing evals).

## Anti-patterns

- **Trusting the README's corpus percentages** instead of running `--status` — they're a point-in-time snapshot and go stale the moment the nightly job runs again.
- **Running `adk run avai` from inside `agents/avai/`** — resolves no agents and produces a confusing empty-registry error instead of a clear message.
- **Re-scraping poems already marked complete** because a stat looked wrong, instead of running the normalizer's verification pass on the existing data.
- **Skipping the phase order with `--poem`** as a default workflow — phases are ordered smallest-first specifically so translation quality problems are caught before they propagate to the large anthologies.
- **Treating an unverified English draft as citable** in agent responses or docs — every draft is `verified: false` until scholar review per `docs/data-governance.md`.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture, `tamil-content-writing` and `tamil-transliteration` for the urai/English layering work, and `rag-pipeline-design` for the corpus → knowledge-graph → retrieval path the Sangam Avai agents depend on.
