---
name: yazhi-code-refactor
description: Use when changing code structure without intending to change behavior — extracting a helper, moving a boundary, removing duplication, or renaming across a repository. Helps you keep behavior constant with characterization checks and small reviewable steps; feature work goes to yazhi-code-implement.
---

# Behavior-Preserving Refactor

A refactor earns its place only when the code becomes easier to change and behavior stays the same. This skill owns that narrow contract. It is not a vector for feature work, and it does not repeat the general small-diff culture in `org-healthy-code`; it adds the specific checks that make "no behavior change" a claim you can defend.

## Workflow

1. **Write the invariant before the plan.** State the behavior that must not change: outputs, error shapes, latency class, call order, or external contract. If the request cannot name an invariant, it is not a refactor — use `yazhi-code-frame` and implement a change.
2. **Add a characterization check first.** Capture current behavior with the repo's own test command: one representative input, one error path, one edge case. It must pass before the refactor and after each step; an untested behavior cannot be preserved.
3. **Choose the smallest structural boundary.** Extract one function, rename one symbol, or move one module. Prefer the seam the repo already owns — a shared core over a UI layer, a constants module over copy-pasted values, or a named contract between repos. Do not introduce a new architecture to make a small edit prettier.
4. **Work in mechanical steps with checkpoints.** Each step is a single transformation: move, rename, or extract — never move plus change. Commit or stash between steps so a fork or rollback restores a known state. Pi's plan-mode `[DONE:n]` markers are a good progress record for a longer chain.
5. **Keep the diff boring.** No new flags, no new network calls, no "while I am here" fix. If a bug is discovered mid-refactor, stop and record a separate `yazhi-code-debug` or `yazhi-code-improve` frame. Mixing behavior change into a refactor is what makes review untrustworthy.
6. **Compare before and after mechanically.** Run the same commands from step 2, then check generated artifacts and cross-repo consumers if the symbol is public. For localized identifiers or strings, keep the exact code points — do not "clean up" glyphs during a rename.
7. **Hand off with the invariant named.** The PR description says what structure changed, what did not, which checks were run, and what follow-up was deliberately left out. Follow `yazhi-code-handoff` for the cold diff read.

## Refactor decision table

| Request | Refactor? | Owner |
|---|---|---|
| Duplicate logic in two layers with one source of truth | Yes — keep one owner | `yazhi-code-refactor` + the owning repo docs |
| Same duplication plus a new requirement | No — frame the behavior change | `yazhi-code-frame` |
| Dead code that code still cites | No — audit first | `org-repo-audit`, `org-plan-reset-recovery` |
| Test naming or style cleanup only | No — convention fix | `yazhi-code-standards` |
| New shared capability across repos | No — ownership decision | `org-service-boundaries`, `org-cross-repo-change` |

## Anti-patterns

- **Refactoring without a characterization check.** There is no way to tell a preserved behavior from a silent regression.
- **Renaming and rewiring in one commit.** Reviewers cannot separate mechanical change from behavior change, so the 48-hour gate becomes a rubber stamp.
- **"While I am here" bug fixes.** They belong in their own frame; otherwise the refactor's invariant is a lie.
- **Changing localized text during a rename.** Code-point or register changes are content work, not structural work; use the language skill separately.
- **Skipping downstream consumers.** A renamed public symbol without a contract check breaks another repo while this one stays green.

Map to: `yazhi-code-standards` (style authority), `yazhi-code-implement` (behavior changes), `yazhi-code-debug` (newly found bugs), `org-impactful-pr` (honest description).
