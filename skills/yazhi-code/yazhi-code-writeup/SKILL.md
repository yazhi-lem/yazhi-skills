---
name: yazhi-code-writeup
description: Use when drafting or creating a GitHub issue or pull request for any repository, including from Pi via `/yazhi-issue` or `/yazhi-pr`. Helps you write a contentful, evidence-backed body with acceptance criteria, scope, test plan, and honest status; the PR body contract stays with `org-impactful-pr`.
---

An empty issue or a PR that says "fix stuff" costs more review time than it saves. A contentful write-up is a small contract: what is wrong, why it matters, what will be true when done, and how to verify it. This skill owns drafting and creating issues and PRs across repositories; `org-impactful-pr` owns the PR body contract, and this skill adds the issue contract, duplicate check, and Pi flow.

## Issue contract

| Section | Required content | Reject when |
|---|---|---|
| Title | Imperative, one outcome, searchable, 72 characters or fewer | "Bug", "Improvement", "Misc" |
| Problem | Current behavior, affected user, reproduction or evidence | "It does not work" |
| Outcome | What will be true when done; testable acceptance criteria | "Make it better" |
| Scope | In scope, out of scope, affected repos | No boundary |
| Evidence | Logs, command output, screenshot, file and line, links | No evidence |
| Plan | Smallest next step, owner, dependencies | Unbounded list |
| Done | Verification command or observable result | "Tested" |

For a PR, use the six sections in `org-impactful-pr` — what changed, why, evidence, contract impact, status, and gaps — then add the linked issue, exact test plan, and risk or rollback note. Do not restate the diff. For user-visible localized text, name the native review in the body.

## Workflow

1. **Choose the artifact.** If the invocation starts with `issue` or `pr`, that is the mode. An issue is for a problem not implemented; a PR for a change on a branch. A non-trivial PR without an issue needs a one-line reason.
2. **Search before writing.** Run `gh issue list --search`, `gh pr list --search`, and check the docs index. Link the canonical item; do not create a near-duplicate.
3. **Gather evidence.** Command and output, expected vs actual, reproduction steps, file and line, a UI screenshot, or a source-of-truth link. No evidence, not ready to create.
4. **Use the repo's template.** Check `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, and `CONTRIBUTING.md`; fill it rather than inventing a format. Follow `yazhi-code-standards` for titles and prose, and `org-healthy-code` for scope.
5. **Write one outcome with falsifiable criteria.** Every checklist item must be something a reviewer can run or observe. Two unrelated outcomes mean two issues or PRs.
6. **Set metadata honestly.** Labels only if they exist; route owner with `yazhi-agency`; assign only after confirmation. Mark a PR draft if not ready; never claim done with gaps.
7. **Preview and confirm.** In Pi, `/yazhi-issue` and `/yazhi-pr` queue this skill with the mode and prompt in the editor. Edit, submit, and review the drafted body before creation. No confirmation channel means stop after preview.
8. **Create with a file, then verify.** Use `gh issue create --title <quoted> --body-file <file>` or `gh pr create --base main --head <branch> --title <quoted> --body-file <file>`; never concatenate untrusted text. Open the URL and check rendering, links, labels, and linked issue.

## Pi creation flow

`/yazhi-issue <prompt>` and `/yazhi-pr <prompt>` both queue `/skill:yazhi-code-writeup`, with `issue` or `pr` as the first word. Write the body to `/tmp/yazhi-body.md`, read it back, and create only after approval. The skill never creates, posts, or assigns on its own.

## Anti-patterns

- **Title-only issue.** No reproduction, no acceptance criteria, so nobody can act without an interview.
- **A PR body that restates the diff.** The reviewer learns what changed but not why it matters or what proves it works.
- **Template placeholders left in.** `TODO`, `<!-- describe -->`, and empty sections look finished when they are not.
- **Acceptance criteria that cannot fail.** "Works well" is not a check; name the command or observable result.
- **Creating without a preview or via shell interpolation.** Untrusted text can break the command; use a file and confirm.

For the PR contract see `org-impactful-pr`; for the handoff before a PR see `yazhi-code-handoff`; for routing see `yazhi-agency`; for close/keep decisions see `org-issue-triage`; for Markdown structure see `technical-documentation`.
