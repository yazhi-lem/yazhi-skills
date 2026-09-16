---
name: capitol-status
description: Use when working in the capitol repository — the internal AI/ML ops and people-management console. Helps you recognize this is a UI mockup over hardcoded data, not a working backend, before building on top of state that doesn't actually exist yet.
---

Capitol is meant to be Yazhi's unified internal tool for AI/ML Ops and people management — annotation queues, agent/model monitoring, and audit — built as a Next.js 16 + React 19 app. Today it is an **early UI scaffold only**: every number on screen (win-rate, GPU%, queue throughput, agreement heat map, audit log) comes from `src/lib/data.ts` constants, not a live data source. There is no backend, no database, and no connection to `yazhi-api` yet, despite the dashboard's "● sovereign" badge and "0 external calls" audit claims being purely decorative at this stage.

## Status at a glance

| Area | Path | State |
|---|---|---|
| Dashboard shell | `src/app/page.tsx`, `src/app/mission/page.tsx` | UI complete, hardcoded data |
| Console (annotation/audit/models/people) | `src/app/console/*` | Pages exist, stubbed |
| Bench (personal QA, task queue) | `src/app/bench/*` | Pages exist, stubbed |
| Shared components | `src/components/{ui,layout,dashboard,bench}/` | Built — `ProgressBar`, `HeatMap`, `KPICard`, `SovereignBadge`, `ChatDock`, etc. |
| Data layer | `src/lib/data.ts` | Mock constants (`HEAT_CELLS`, `QUEUES`, `MODEL`, `AUDIT_LOG`) — no real source |
| Backend | — | Does not exist |

## Workflow

1. **Don't build against `src/lib/data.ts` as if it were live data.** Any feature that reads `MODEL.winRate`, `QUEUES`, or `AUDIT_LOG` today is reading a fixture, not a system — say so explicitly if asked whether a metric is "real."
2. **Decide the backend question before adding more frontend surface.** The repo currently has zero server-side code; before wiring another console page, confirm whether Capitol is meant to call `yazhi-api` directly (consistent with the rest of the ecosystem's architecture) or stand up its own service.
3. **Keep new UI consistent with the existing "sovereign console" visual language** — hand-drawn border-radius quads, hatch-pattern placeholders (`HatchBox`) for not-yet-wired charts, and the ⬡ CAPITOL command-bar pattern already established in `mission/page.tsx`.
4. **Use `HatchBox` for any chart or visualization that has no real data source yet**, rather than inventing fake numbers that look finished — it's the repo's own convention for marking "designed, not implemented."
5. **Route any people/annotation/model data model design through the same schema `yazhi-api`'s `auth/` (IAM/Circle) and `domains/` already define**, rather than inventing a parallel people/roles model for Capitol alone.
6. **Run `npm run lint` and `npm run build`** before proposing UI changes — there's no test suite yet, so these are the only automated checks in the repo.

## Next actions

1. Decide and document whether Capitol talks to `yazhi-api` (gRPC) or gets its own backend — this blocks every other next step.
2. Replace `src/lib/data.ts` with a real data source once that decision is made.
3. Wire the `console/annotation`, `console/audit`, `console/models`, and `console/people` pages to actual queues/models/people records.
4. Add a test suite — currently none exists beyond ESLint.

## Anti-patterns

- **Presenting the dashboard's numbers as live metrics** to a user or in a demo without disclosing they're hardcoded — the win-rate, GPU%, and audit entries are fixtures in `src/lib/data.ts`.
- **Adding a new console page without deciding the backend architecture first** — grows the UI surface area that will all need rewiring once a real data source exists.
- **Inventing a Capitol-specific people/roles schema** instead of reusing `yazhi-api`'s IAM/Circle model — creates two sources of truth for who's who across the ecosystem.
- **Faking chart data instead of using `HatchBox`** — makes an unimplemented feature look shipped, which is worse than an honest placeholder.
- **Treating the "0.1.0" package version or the polished UI as a signal of production-readiness** — the UI is ahead of the backend, not a reflection of overall project maturity.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture and `yazhi-api-status` for the IAM/Circle schema this project should likely reuse rather than duplicate.
