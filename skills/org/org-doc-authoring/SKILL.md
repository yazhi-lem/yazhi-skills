---
name: org-doc-authoring
description: Use when writing a new Yazhi doc and you need to pick its color — green for living state, blue for a frozen contract, orange for provisional work — and set its promotion path. Helps you stop three-way drift; file placement, size, and archive rules belong to technical-documentation.
---

Yazhi docs fail when a draft, a contract, and a status page all look the same on the page. Color is the fix: it tells a reader how much authority a doc has before they read a word. Green describes the present and changes in place; blue is frozen and changes only by version; orange is provisional and must expire. `technical-documentation` owns the file contract and archive rules; this skill owns the color decision and the promotion path between colors.

## The three colors

| Color | Meaning | Header | Lifetime | Typical kinds |
|---|---|---|---|---|
| Green | Living — describes how things are now | `Status: current`, `Owner:`, `Scope:`, `Verified: YYYY-MM-DD + commit` | Updated in place; re-verify on every change | Current state, runbooks, guides, READMEs |
| Blue | Frozen — a contract or record | `Status: frozen`, `Version:`, `Owner:`, `Scope:`, `Verified:` | Immutable once published; supersede, never edit | Architecture contracts, ADRs, versioned references, evidence reports |
| Orange | Provisional — in flight | `Status: draft`, `Expires: YYYY-MM-DD`, `Owner:`, `Scope:` | Time-boxed; must be promoted or archived by the expiry | Spikes, experiments, known-issues, pre-decision explorations |

## Promotion path

1. **Orange → Green** when the work becomes current reality: rewrite as living state, drop the expiry, add `Verified`. The draft is deleted, not left beside the promoted doc.
2. **Orange → Blue** when the exploration settles into a contract or decision: add a version, make it immutable, and record the decision that froze it.
3. **Green → Blue** when a status page stops changing and becomes a reference: freeze it with a version and point green docs at it.
4. **Any → Archive** when superseded: compress to `archives/YYYY-MM-DD-digest.md`, delete from `docs/`, fix inbound links in the same PR.

## Workflow

1. **Ask what the reader needs to do with the doc.** Change behavior now → green. Implement against it → blue. Decide whether to proceed → orange. No answer means the doc is not ready to be written.
2. **Check for an existing owner first.** `technical-documentation` owns the search order (`README.md`, `CONTEXT.md`, docs index, `archives/`); update the owner instead of adding a second source of truth.
3. **Write the header before the body.** `technical-documentation` owns the base fields (`Status`, `Owner`, `Verified`, `Scope`); color adds `Version` for blue or `Expires` for orange. An unclassified header will be trusted wrongly.
4. **Set the orange expiry to a real date** — default 14 days for a spike, 30 for a known-issues page — and put the promotion decision in the doc's first paragraph so the expiry owner knows what to do.
5. **Keep blue immutable.** If a frozen contract needs a change, publish a new version and mark the old one `superseded by vN` in the archive; editing a blue doc in place breaks every code comment that cites its section.
6. **Place by kind and register it.** `technical-documentation` owns the directory map and `docs/README.md` row; add the color to that row in the same change.
7. **Verify links and color mechanically.** `technical-documentation` owns link/header checks; this skill adds one check: no orange doc past its expiry without a promotion decision.

## Anti-patterns

- **Coloring everything green.** A draft marked `Status: current` is the single most expensive doc defect in Yazhi — it looks authoritative and is wrong within a week.
- **Editing a blue doc in place.** Silently invalidates code comments and ADR citations; supersede with a new version instead.
- **Orange docs with no expiry.** A "temporary" spike note from six months ago is indistinguishable from a decision; the expiry date is the whole mechanism.
- **Leaving the promoted draft beside the promoted doc.** Two documents, one topic, guaranteed disagreement within a month.
- **Choosing a color by aesthetics.** Color is an authority level, not a theme; picking by look means readers cannot infer which doc to trust.
- **Skipping the `docs/README.md` row.** An unregistered doc is invisible until someone finds it by grep and treats it as current.

Follow `technical-documentation` for size budgets, header fields, and archive rules; follow `org-ethos` for the source and chamber rules; use `org-repo-audit` to find docs that were never colored; use `org-plan-reset-recovery` before promoting a doc that came from a retired plan.
