---
name: google-style-adoption
description: Use when deciding which Google style guide applies to a Yazhi repo, enforcing it in review or lint, or adding a Yazhi-specific deviation on top of it. Helps you cite the right guide, keep the fork read-only, and document deviations where they belong.
---

`yazhi-lem/styleguide` is a fork of `google/styleguide`, and `yazhi-api`'s README and `CONTEXT.md` both name it as the definition of "the Google Python Style Guide" that `ruff` enforces. The trap is treating the fork as a place to author Yazhi conventions — it is an upstream reference, and Yazhi-specific rules belong in the consuming repo. `yazhi-org-status` records the fork's sync date; this skill owns the adoption decision.

## Which guide applies

| Language | Guide | Enforced by | Yazhi deviation |
|---|---|---|---|
| Python | `pyguide.md` | `ruff` + `pylintrc` | `yazhi-api` uses `<module>_test.py`; adhan uses `<module>_tests.py` — check the consuming repo |
| JavaScript / TypeScript | `jsguide.html` / `tsguide` | ESLint config in the repo | none documented |
| Go | `go/` | `gofmt` / `go vet` | none documented |
| Java | `javaguide.html` | formatter | none documented |
| C++ | `cppguide.html` | clang-format | none documented |
| Shell | `shellguide` | `shellcheck` | none documented |
| Markdown | `docguide` | review | Yazhi's own doc contract in `technical-documentation` |

## Workflow

1. **Name the language and the consuming repo first.** The guide is language-specific and the deviation is repo-specific; "Google style" alone is not an answer.
2. **Read the guide before enforcing it.** Cite the section you are enforcing — a reviewer who says "Google style" without a section is enforcing a vibe, not a rule.
3. **Check the fork's sync date before citing.** `yazhi-org-status` records the last upstream sync; a rule quoted from a stale fork may already be superseded.
4. **Apply the enforcement tool the repo already has.** Python runs `ruff` against the guide; other languages run their formatter. Do not hand-edit style violations that a tool would fix.
5. **Document Yazhi deviations in the consuming repo, never in the fork.** The Python test-naming rule is the known example: `yazhi-api` uses `<module>_test.py`, which deviates from typical Google Python test layout; adhan uses `<module>_tests.py`. Each convention belongs in its own repo's `CONTEXT.md` / `pyproject.toml`, not in a blanket 'Google style' claim.
6. **Review the deviation, not the guide.** In review, cite the guide section for the rule and the consuming repo's doc for the deviation; a deviation without a written reason is a bug.
7. **Sync upstream by taking the full commit.** Cherry-picking defeats the fork's purpose — the point is that the fork stays recognizable as Google's.

## Anti-patterns

- **Editing the fork to add Yazhi rules.** The fork is read-only in practice; local edits diverge from upstream and make future syncs a merge conflict.
- **Enforcing "Google style" without a section.** Unreviewable and unarguable; cite the guide section or drop the comment.
- **Citing a stale fork as current.** Style guides evolve upstream; check the sync date before quoting a rule as authoritative.
- **Hand-fixing what a formatter would fix.** Wastes review time and produces diffs that obscure the real change.
- **Burying a deviation in review comments.** If a repo deviates from the guide, the reason belongs in that repo's `CONTEXT.md`, not in a thread nobody reads later.
- **Cherry-picking upstream changes.** Produces a fork that is neither Google's nor Yazhi's, and the next sync cannot be automated.

Follow `yazhi-org-status` for the fork's sync state, `org-healthy-code` for the code-level practice, and `technical-documentation` for the Markdown doc contract.
