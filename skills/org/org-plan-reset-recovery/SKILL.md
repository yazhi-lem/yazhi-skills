---
name: org-plan-reset-recovery
description: Use when an old roadmap, dated issue, or archived plan resurfaces after a Yazhi strategy reset and someone is about to act on it. Helps you verify what is current, cite the retirement source, and avoid resurrecting plans the founders deliberately cleared.
---

Yazhi has reset direction more than once (most recently around 2026-11-20/21), and old plans survive in issues, archived docs, local clones, and agent memory. They are convincing because they are detailed and often have hard dates. This skill owns the "is this still current?" check before scope is set. It does not decide strategy; it decides which source has authority today and how to retire the rest without losing history.

## Source authority

| Source | Authority | How to use it |
|---|---|---|
| Repo `README.md` + `docs/README.md` (`Status/Owner/Verified`) | Current for that repo | Read first; the verified date is part of the claim |
| `CONTEXT.md` in `yazhi-api` | Current for central service constraints | Overrides older architecture notes |
| `archives/` and retired-plan banners | History only | Cite as "why we stopped"; never as a task list |
| Dated roadmap or `NEXT_ACTION.md` | Superseded unless linked from a current index | Verify before acting |
| Old session notes / issue import | Hint only | Re-check against the current repo state |

## Workflow

1. **Identify the claim that is about to drive work** — a phase number, a launch date, a model choice, or a "next action" — and quote it verbatim. Vague suspicion is not enough to overturn a plan.
2. **Read the current index in the affected repo** (`docs/README.md`, then `CONTEXT.md` where present). If the claim is not linked there, treat it as historical unless the index explicitly defers to it.
3. **Check for a reset note or archive entry** and record where and when the plan was retired. A dated retirement beats a dated plan; cite the source in the issue or PR that would have acted on the old plan.
4. **Look for a replacement, not just a rejection.** Most resets keep the goal and drop the date, the model, or the sequencing. Rewrite the surviving intent in current language rather than closing everything as obsolete.
5. **Update or close the artifact explicitly** — comment on the issue with the retirement source, rewrite its title/body if the work still matters, or close it with a category reason per `org-issue-triage`. Do not leave a "superseded" banner on a live doc; archive it per `technical-documentation`.
6. **Refresh the current index if it is itself stale.** If the docs index still links the retired plan, fix the index in the same change so the next reader does not repeat the mistake.
7. **Record what changed in the decision**, including the date and the repos checked, in the PR/issue that would have implemented the old plan. Future resets need the same trail.

## Anti-patterns

- **Treating detail as authority.** A 40-row roadmap with exit criteria can still be dead; authority comes from the current index and reset notes.
- **Resurrecting a retired model or stack "just for a quick test."** The Adhan PyTorch/LoRA pipeline and old API V2 plans were deliberately retired; rebuilding them forks project direction.
- **Deleting the archive to clean up.** Archives are the evidence that a reset happened; keep a compressed copy and link to it from the current docs.
- **Silently ignoring an old issue.** Someone will act on it in a later session; close or rewrite it with the retirement source instead.
- **Declaring a reset from memory.** Verify against the repo's docs and git history first — an assumed reset can retire real work.

For the stale-file classification see `org-repo-audit`; for issue-level decisions see `org-issue-triage`; for the ecosystem map see `yazhi-org-status`; for archive and header rules see `technical-documentation`.
