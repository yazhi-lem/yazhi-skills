---
name: org-ethos
description: Use when a decision, doc, PR, or release needs a values check — child safety, data residency, language accuracy, or whether work belongs in the private chamber or the public one. Helps you apply the five gates and the standard of care instead of rediscovering them per project.
---

The rules are not a values statement pinned to a wall; they are gates. They are enforced in code and review: uncited answers are blocked, data-residency law is a launch gate, and every product carries a one-command rollback. Care is the second axis — how we treat each other and the reader — and the private/public chamber is the third — where a piece of work lives. This skill owns the values; the working skills apply them.

## The five gates

| Rule | Binding meaning | Gate it enforces |
|---|---|---|
| No claim without a source | If a source cannot be shown, say "I don't know" | Any answer whose section is not matched to stored source text is blocked |
| Data stays home | No foreign cloud or foreign AI API in production; citizen data never leaves the required jurisdiction | Data-residency law is a launch gate, not a nice-to-have |
| Think, then act | No system-changing action without a plan, an approved runbook, and a human confirm | One-command rollback on every product |
| Children first | No child uses the product before counsel sign-off and verified parental consent; collect the minimum data | A documented child-safety red-team before exposure |
| Ship what we said | Mark drafts as drafts, flag every inference, never present a plan as done | Status labels and PR evidence |

**Care** is measurable: native-speaker review of every user-visible localized string before it ships, a second human reviewer on every PR within 48 hours, review comments that critique the diff and not the person, and accessibility checked rather than assumed. An unreviewed string and a 48-hour-plus PR are both defects, not style preferences.

**Private and public chambers.** Keep internal configs, unfinished research, private keys, and prototypes in the private chamber; keep releases, public docs, and FLOSS-licensed libraries in the public one. Moving work between them is a deliberate promotion, never a push.

## Workflow

1. **Name which gate the work touches** before designing anything. Most work touches one or two; "all of them" means the scope is not yet understood.
2. **Check the data path first.** If the change sends citizen data, child data, or prompts to a foreign cloud or API, it fails the data gate and cannot ship as designed — redesign or get explicit owner sign-off and document it.
3. **Check the child gate.** Anything reachable by a child needs counsel sign-off, verified parental consent, and a documented red-team result before exposure. This gate is not deferrable to "after launch".
4. **Demand the source.** For any claim in a doc, PR, or model answer, name the citation. If there is none, write "I don't know" rather than a plausible sentence.
5. **Confirm the chamber.** New work starts private; promote to public only after review by the owning roles and a human. Never copy private keys, internal configs, or unfinished research into a public repo.
6. **Attach the plan and the rollback.** For anything that changes a running system, write the runbook and the one-command rollback before executing, and require a human confirm.
7. **Label the status honestly.** Draft, inference, and plan are three different words; using "done" for any of them breaks the ship-what-we-said gate and poisons the next reader's trust.

## Anti-patterns

- **Treating the rules as branding.** Printing "no claim without a source" in a README while the model invents citations is worse than silence — the gate is the code path, not the sentence.
- **Sending prompts to a foreign API "for a quick test".** One request from a laptop can put regulated data on someone else's server; the data gate has no staging exemption.
- **Shipping a localized string without native review.** Machine-fluent text that a native speaker finds wrong is a reputational cost, and it is the most common care failure.
- **Pushing from the private chamber to the public one directly.** Bypasses the review gates and has leaked private keys and internal configs into public history.
- **Calling a plan "done".** The most common honesty breach; a plan marked done stops getting reviewed while the work continues.
- **Deferring the child gate to "after launch".** Counsel sign-off and a documented red-team are preconditions; a launch without them is a launch we cannot defend.

For doc-level application see `org-doc-authoring`; for code-level see `org-healthy-code`; for PR-level see `org-impactful-pr`; for release gates see `org-release`; for model-facing risk see `llm-security-review`.
