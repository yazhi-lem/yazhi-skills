---
name: yazhi-code-standards
description: Use when writing, refactoring, or reviewing Yazhi code before you push it, and you want one shared better-code standard instead of style-by-opinion. Helps you apply Google-leaning naming, error, test, and review rules; google-style-adoption owns which language guide applies.
---

# Yazhi Code — Better Code Standard

This is the craft checklist for `yazhi-code-implement`, `yazhi-code-handoff`, and ordinary development work. It turns best practices from Google engineering guidance and public agent skills into rules an agent or developer can apply in one pass. It defers guide choice to `google-style-adoption`, security to `secure-code-review`, and PR writing to `yazhi-code-handoff`.

## Workflow

1. **Let technical facts beat preference.** Before changing code, write the observable outcome and the exact check that proves it. If the only reason is "I prefer this shape", it is a style opinion, not a defect. Keep the skill trigger narrow: hosts like Pi load a body only after its description matches.
2. **Keep the change small and complete.** One outcome per diff, related tests in the same diff, and the tree still usable afterwards. Split refactors, generated code, and unrelated fixes into separate changes; a small change is reviewed more thoroughly and rolled back more easily.
3. **Use the repo's tools, not a substitute.** Run the formatter, linter, and test command the repo already declares. Cite the style-guide section when enforcing a rule; document a deviation in the consuming repo, never in a fork. See `google-style-adoption` for the guide map and `org-healthy-code` for Yazhi's small-diff rules.
4. **Write for the next reader.** Use clear, specific names; keep functions focused on one job; keep comments about *why*, not *what*. Avoid speculative abstractions for needs that do not exist yet. For Python, the Google guide's defaults are 4-space indent, 80-character lines, and no bare `except:`.
5. **Make failure paths explicit.** Prefer built-in exception types, narrow `try` blocks, and errors that name the bad value. Never swallow an error to keep a happy path green; security-relevant failures must fail closed and go to `secure-code-review` when a boundary is involved.
6. **Review every line before you push.** Check design, functionality, complexity, tests, naming, comments, style, and consistency in that order. Confirm the named checks, hand off through `yazhi-code-handoff`, recheck CI, and address only in-scope comments.

## Standard at a glance

| Area | Rule | Proof before push |
|---|---|---|
| Scope | One outcome, tests included | Diff explains itself in under a minute |
| Style | Guide section + repo tool | Formatter/linter clean; deviation documented |
| Names | Specific, consistent, no abbreviations that need a decoder | A new reader can predict a function from its name |
| Errors | Built-in types, narrow catches, fail closed | One failing case shows a useful message |
| Tests | Relevant unit + regression assertion | Named command passes locally |
| Review | Every line, facts over opinion | Checklist above completed, not skimmed |

## Sources and harness rules

| Source | Rule kept |
|---|---|
| Google Engineering Practices | One thing per change; what/why description; facts over preference |
| Google Python Style Guide | Lint, imports, exceptions, 80-char lines, 4-space indents |
| Public agent skills | Tools as black boxes; measurable acceptance; review states |
| Pi harness (`skills.md`, `security.md`) | Descriptions route; project trust is not tool safety; write state to survive compaction |
| `org-healthy-code`, `google-style-adoption` | Local-first, honest tests, guide ownership |

See the repo's `docs/pi-harness-lessons.md` for the mapping.

## Anti-patterns

- **Style by personal taste.** Arguing "I would write it this way" without citing the guide section turns review into preference theater.
- **Drive-by cleanup in a bug fix.** Unrelated formatting or refactors hide the real change and make rollback risky.
- **"Tests pass" with no command named.** A reviewer cannot reproduce a claim without the exact command and result.
- **Catch-all error handling.** A broad `except` or empty failure path converts future bugs into silent wrong answers.
- **Pushing before the cold read.** Reading your own diff immediately after writing it misses the assumptions you never stated.
- **Adding abstraction for a future that may not come.** Speculative layers cost more to understand than the repeated code they remove.
- **Treating project trust as tool safety.** Trust gates resource loading, not what an enabled tool can read or run.

Map to: `yazhi-code-design` (the proof), `yazhi-code-implement` (the slices), `secure-code-review` (security), `yazhi-code-handoff` (push gate), `yazhi-code-deliver` (client reality).
