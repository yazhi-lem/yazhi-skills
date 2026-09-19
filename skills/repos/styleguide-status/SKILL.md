---
name: styleguide-status
description: Use when asked to change, sync, or reference the styleguide repository — a fork of google/styleguide. Helps you recognize it as an upstream reference rather than a place to author new conventions, and route Yazhi-specific style decisions elsewhere.
---

`yazhi-lem/styleguide` is a **fork of `google/styleguide`**, last synced 2025-11-13. It hosts Google's language style guides (C++, C#, Go, AngularJS, Common Lisp, and more) exactly as upstream wrote them. Its only concrete, documented use inside the Yazhi ecosystem is normative: `yazhi-api`'s own README and `CONTEXT.md` both point to `github.com/yazhi-lem/styleguide` as the definition of "the Google Python Style Guide," which `ruff` enforces on new code. It is a reference dependency other repos cite, not a place where Yazhi-specific conventions live.

## What this repo is and isn't

| It is | It is not |
|---|---|
| A synced fork of `google/styleguide`, read-only in practice | A place to document Yazhi's own engineering standards |
| The named source for `yazhi-api`'s Python style enforcement | Actively diverging from upstream — no Yazhi-specific edits exist as of this writing |
| Useful to link to from any repo's contributor docs | A target for feature work, refactors, or new content |
| Occasionally due for an upstream sync | Owned content that needs review for correctness — Google owns the guidance itself |

## Workflow

1. **Default to not editing this repo.** If a style question comes up in `yazhi-api` or any other Yazhi repo, the answer is "what does `google/styleguide`'s relevant guide say," not "let's write our own section here."
2. **If Yazhi needs a style rule Google's guide doesn't cover** (e.g., the `<module>_test.py` colocated-test convention `yazhi-api` uses, which is a Yazhi-specific deviation from typical Google Python test layout), document that rule in the consuming repo's own `CONTEXT.md`/`README.md`, not by editing this fork.
3. **When syncing with upstream, take the full upstream commit, don't cherry-pick.** A fork that silently diverges from `google/styleguide` defeats its purpose as a stable, recognizable reference — anyone consulting it should get exactly what Google publishes.
4. **Check the fork's last-synced date before citing a language-specific rule as current** — style guides evolve upstream; a stale fork can quote outdated guidance without anyone realizing it's stale.
5. **Point new contributor docs at this fork's URL rather than google/styleguide directly** only when there's a specific reason (e.g., pinning to a known-synced version); otherwise linking straight to upstream avoids the sync-lag question entirely.
6. **Treat any local modification to a guide file as a red flag in review** — a diff against a `.html`/`.md` guide file in this repo almost certainly means someone edited Google's content directly instead of writing Yazhi-specific guidance in the right place.

## Next actions

1. Confirm whether the fork needs a fresh sync from `google/styleguide` — check the last-synced date (2025-11-13) against upstream's current state before the next time `yazhi-api`'s Python style is questioned in review.
2. If Yazhi accumulates enough repo-specific conventions layered on top of the Google guide (as `yazhi-api` already has, per `yazhi-api-status`, with its test-naming and `.ruff-baseline.json` policy), consider a dedicated Yazhi engineering-standards doc instead of scattered `CONTEXT.md` files.

## Anti-patterns

- **Editing a guide file in this fork to add a Yazhi-specific rule** — creates silent, undocumented drift from upstream that nobody expects when they clone `google/styleguide`-style guidance.
- **Citing this repo's content as current without checking the sync date** — a stale fork can quietly disagree with what Google currently recommends.
- **Cherry-picking partial upstream updates** instead of a full sync — leaves the fork in an inconsistent state that's harder to reason about than either "fully synced" or "not yet synced."
- **Treating this repo as the place to resolve a Yazhi-specific style question** (test naming, `.ruff-baseline.json` policy, directory layout) — those belong in the consuming repo's own contributor docs, as `yazhi-api` already does correctly.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture and `yazhi-api-status` for the one concrete place this fork is currently cited from.
