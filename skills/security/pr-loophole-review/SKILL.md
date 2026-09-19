---
name: pr-loophole-review
description: Use when reviewing a specific pull request for a deliberately or carelessly introduced security bypass — an unfamiliar contributor's PR, a "quick fix" that touches auth or validation, or any diff where something about the change feels like it's working around a control rather than through it. Helps you spot a loophole hidden in a plausible-looking diff instead of trusting that a passing test suite means the change is safe.
---

`secure-code-review` checks a diff against known vulnerability classes (injection, broken authz, unsafe deserialization). This skill is narrower and adversarial: it assumes the diff might contain a change that *looks* like a reasonable fix but actually weakens or bypasses an existing control, whether by mistake or on purpose — a real, recurring category in both open-source supply-chain incidents and internal "fast-tracked" fixes under deadline pressure.

## Loophole shapes to check for

| Shape | Example | Why it's easy to miss |
|---|---|---|
| Widened default | `if strict: validate()` added where validation used to always run | Reads as a new feature (configurability), not a downgrade |
| Auth check moved or reordered | Authorization check moved after a side-effecting operation instead of before | Diff looks like a refactor; the security implication is in the ordering, not any single line |
| New early return | `if debug_mode: return mock_response` added before an auth check | Looks like harmless test scaffolding; the condition to reach it may be broader than intended |
| Weakened comparison | `==` changed to a fuzzy/prefix match on a token or password check | Passes existing tests if they only test the exact-match case |
| Silent exception swallowing | A new `try/except: pass` wraps a security check that used to propagate a failure | An error in the check now fails open instead of failing closed |
| Dependency swap | A pinned dependency version bumped to a new major version, or replaced with a similarly-named package | Reviewers check the diff of application code, not the transitive dependency tree |

## Workflow

1. **Read the diff for intent before reading it for correctness.** Ask "what would this change let someone do that they couldn't do before," not just "does this code run correctly" — a loophole is, by definition, code that works exactly as written while doing something the reviewer wouldn't have approved if asked directly.
2. **Treat any change that touches an existing `if`/`try`/early-return around a security check as high-scrutiny**, even if the PR's stated purpose is unrelated (a "fix flaky test" PR that also adjusts an auth conditional is a mismatch worth asking about directly).
3. **Check whether the change makes a control conditional that used to be unconditional** — a new flag, environment check, or debug mode that can skip validation/auth is the single most common loophole shape; confirm the condition can never evaluate true in production.
4. **Verify exception handling fails closed, not open.** A `try/except` added around a permission check that returns `True` (or otherwise proceeds) on any exception converts every future bug in that check into an authorization bypass.
5. **Diff the actual comparison logic character by character** when a PR touches a token, password, or signature check — `==` vs. a substring/prefix match, or a timing-unsafe comparison replacing a timing-safe one, are both easy to miss in a quick skim.
6. **For a dependency change, check what actually changed in the dependency**, not just the version number in the lockfile diff — a bumped transitive dependency can introduce new maintainers, new install scripts, or new network calls that a version-number-only review would never catch.
7. **Be more skeptical of a PR from an unfamiliar or first-time contributor that touches auth, validation, or CI configuration**, especially if the stated purpose (a typo fix, a "cleanup") doesn't match the security-relevant scope of the actual diff — this mismatch is the single strongest signal in real supply-chain-attack post-mortems.
8. **Ask the author to explain the security-relevant part of the diff in their own words** if anything above raises a question — a legitimate change has a clear, specific answer; a request that gets a vague or evasive answer, or gets quietly withdrawn, has told you something.
9. **When in doubt, request the change be split** so the security-relevant part can be reviewed on its own, separate from an unrelated refactor or cleanup that's bundled in the same PR to reduce scrutiny.

## Anti-patterns

- **Approving because the test suite passes** — tests validate the behavior someone thought to write a test for; a loophole is specifically the behavior nobody wrote a test to forbid.
- **Reviewing a large PR only at the diff-stat summary level** — a security-relevant three-line change hidden inside a 400-line "refactor" PR is a well-known technique for getting a loophole past a reviewer skimming for the stated purpose.
- **Trusting a version bump in a lockfile without checking what changed** — the actual risk lives in the dependency's new code, not in the version string.
- **Treating "it's just a debug flag" as automatically low-risk** — the question is never whether the flag is *labeled* safe, it's whether it's reachable in production and what it disables when set.
- **Skipping extra scrutiny for external or first-time contributors** out of politeness — the review bar should be about the diff's security-relevant scope, not about avoiding an awkward conversation; ask the clarifying question.

Cross-reference `secure-code-review` for the broader per-PR vulnerability-class checklist this skill sits alongside, `codebase-vulnerability-audit` for finding this same class of issue after it's already merged, and `secure-design-patterns` for the chokepoint/fail-safe-default patterns that make a loophole harder to introduce in the first place.
