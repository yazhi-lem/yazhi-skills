---
name: google-style-adoption
description: Use when deciding which Google style guide applies to a repository, enforcing it in review or lint, or documenting a local deviation. Helps you cite the right guide, keep the upstream fork read-only, and put deviations where the consuming repo can find them.
---

A shared style-guide fork is an upstream reference, not a place to author local conventions. The trap is treating the fork as policy: local rules belong in the consuming repo, and a rule quoted from a stale fork may already be superseded upstream. This skill owns the adoption decision and the deviation record.

## Which guide applies

| Language | Guide | Enforced by | Local deviation |
|---|---|---|---|
| Python | `pyguide.md` | `ruff` + `pylintrc` | Record test naming and lint exceptions in the repo |
| JavaScript / TypeScript | `jsguide.html` / `tsguide` | The repo's ESLint config | Record any rule disabled for a reason |
| Go | `go/` | `gofmt` / `go vet` | Record any generated-code exception |
| Java | `javaguide.html` | Formatter | Record any framework-specific exception |
| C++ | `cppguide.html` | clang-format | Record any platform-specific exception |
| Shell | `shellguide` | `shellcheck` | Record any shell-dialect exception |
| Markdown | `docguide` | Review | The repo's own doc contract in `technical-documentation` |

## Workflow

1. **Name the language and the consuming repo first.** The guide is language-specific and the deviation is repo-specific; "Google style" alone is not an answer.
2. **Read the guide before enforcing it.** Cite the section you are enforcing — a reviewer who says "Google style" without a section is enforcing a vibe, not a rule.
3. **Check the fork's sync date before citing.** A rule quoted from a stale fork may already be superseded; link the upstream commit or the sync record.
4. **Apply the enforcement tool the repo already has.** Python runs `ruff` against the guide; other languages run their formatter. Do not hand-edit style violations that a tool would fix.
5. **Document local deviations in the consuming repo, never in the fork.** Put the rule, the reason, and the owner in `CONTRIBUTING.md`, `CONTEXT.md`, or the linter config. A deviation without a written reason is a bug.
6. **Review the deviation, not the guide.** In review, cite the guide section for the rule and the consuming repo's doc for the deviation.
7. **Sync upstream by taking the full commit.** Cherry-picking defeats the fork's purpose — the point is that the fork stays recognizable as upstream.

## Anti-patterns

- **Editing the fork to add local rules.** The fork is read-only in practice; local edits diverge from upstream and make future syncs a merge conflict.
- **Enforcing "Google style" without a section.** Unreviewable and unarguable; cite the guide section or drop the comment.
- **Citing a stale fork as current.** Style guides evolve upstream; check the sync date before quoting a rule as authoritative.
- **Hand-fixing what a formatter would fix.** Wastes review time and produces diffs that obscure the real change.
- **Burying a deviation in review comments.** If a repo deviates from the guide, the reason belongs in that repo's docs, not in a thread nobody reads later.
- **Cherry-picking upstream changes.** Produces a fork that is neither upstream nor local, and the next sync cannot be automated.

Follow `org-healthy-code` for the code-level practice and `technical-documentation` for the Markdown doc contract.
