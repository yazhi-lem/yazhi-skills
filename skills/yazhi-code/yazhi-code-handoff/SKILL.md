---
name: yazhi-code-handoff
description: Use when a change is complete for its stated intent and you are ready to commit or share it for review. Helps you perform a cold local review, write an honest commit or PR description, and hand off work that another developer can continue without extra context.
---

# Yazhi Code — Local Proof and Handoff

The handoff is where speed is protected or lost. A clean local review and an honest description let the next person (or the 48-hour review gate) move quickly. This skill owns the final verification and sharing steps.

## Workflow

1. **Cold-read the full diff.**  
   Read it as if you did not write it. Look for unrelated changes, missing verification, and places where the intent is unclear.

2. **Run the checks that matter for this change.**  
   Prefer the smallest set that proves the outcome and protects existing behavior. Note what you ran and the result.

3. **Write the commit or PR description.**  
   State the intent (why) and the effect (what). Include how it was verified and any remaining open points. Follow `org-impactful-pr` for scope, evidence, and honest status.

4. **Confirm the handoff stands alone.**  
   Someone who has not seen the conversation can understand what was done, how it was checked, and what is still open.

5. **Integrate only after agreed checks pass.**  
   Address review substance without expanding scope unless the original intent was wrong.

## What each artifact must answer

| Artifact | Must answer | Fails review when |
| --- | --- | --- |
| Commit or PR title | What changed, in the imperative | “fix stuff”, “wip”, “updates” |
| Description | Why the change exists and what it affects | Only restates the diff |
| Verification | Which command or check ran, and its result | “Tests pass” with no named command |
| Open points | What is deliberately left for later | Follow-up debt left silent |

## Checklist before sharing

- [ ] Diff reviewed cold; no unrelated changes.
- [ ] Relevant local checks pass and are named in the description.
- [ ] Commit/PR message states intent and effect.
- [ ] Open points or follow-ups are listed.
- [ ] I can explain the change without the code open.
- [ ] Related skills consulted if needed (`org-healthy-code`, `org-impactful-pr`, `org-cross-repo-change`).

## Anti-patterns

- **“It works on my machine” with no named checks.** Leaves the reviewer to rediscover what was verified.
- **Including drive-by refactors in the same commit.** Makes the diff larger and the intent harder to see.
- **Vague commit messages (“fix stuff”, “wip”).** Forces the next person to reconstruct the reason from the code.
- **Deferring all verification to CI.** Slows the feedback loop and often hides local-only issues.
- **Expanding scope while addressing review comments.** Turns a focused change into an open-ended one.

Map to: `org-impactful-pr` (48-hour reviewable PRs with evidence), `org-healthy-code` (small, honest, local-first diffs), `yazhi-daily-rhythm` (close the day with clear status), `org-release` (if the change is on a release path), `yazhi-code-frame` and `yazhi-code-implement` (the earlier steps this handoff completes).
