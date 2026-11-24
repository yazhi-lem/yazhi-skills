---
name: org-ethos
description: Use when a Yazhi decision, doc, PR, or release needs a values check — child safety, data residency, Tamil cultural accuracy, or whether work belongs in the private அகம் chamber or the public புறம் one. Helps you apply the five அறம் rules and the அன்பு standard of care instead of rediscovering them per project.
---

Yazhi's rules are not a values statement pinned to a wall; they are gates. The five அறம் rules come from the Aram harness (adhan's `docs/behaviour/ARAM_HARNESS.md`, seeded into Capitol's `ARAM_RULES`), and they are enforced in code: Nyaya blocks uncited answers, DPDP Act 2023 is a launch gate, and every product carries a one-command rollback. அன்பு (anbu) is the second axis — how we treat each other and the reader — and அகம்/புறம் (agam/puram) is the third — which chamber a piece of work lives in. This skill owns the values; the working skills apply them.

## The five அறம் rules

| Rule | Binding meaning | Gate it enforces |
|---|---|---|
| மெய்ப்பொருள் — no claim without a source | If a source cannot be shown, say "தெரியவில்லை / I don't know" | Nyaya blocks any answer whose section is not matched to stored Act text |
| தற்சார்பு — data stays home | No foreign cloud or foreign AI API in production; Indian citizen data never leaves India | DPDP Act 2023 is a launch gate, not a nice-to-have |
| எண்ணித் துணிக — think, then act | No system-changing action without a plan, an approved runbook and a human confirm | One-command rollback on every product |
| குழந்தை காப்பு — children first | No child uses Yazh before counsel sign-off and verified parental consent; first name and age band only | Kid red-team ≥98% before exposure |
| சொல்லிய வண்ணம் செயல் — ship what we said | Mark drafts as drafts, flag every inference, never present a plan as done | Status labels and PR evidence |

**அன்பு (anbu)** — the standard of care: native-speaker review of every Tamil string before it ships, a second human reviewer on every PR within 48 hours, review comments that critique the diff and not the person, and accessibility checked rather than assumed. Care is measurable: an unreviewed Tamil string and a 48-hour-plus PR are both defects, not style preferences.

**அகம் / புறம் (agam / puram)** — the two chambers from `docs/SOP_GIT_ARCHITECTURE.md`. அகம் is the private chamber: `agam-y` on self-hosted Forgejo, holding internal configs, unfinished research, private keys, and prototypes. புறம் is the public square: `puram-y` on GitHub, holding releases, public docs, and FLOSS-licensed libraries. Moving work from one to the other is a deliberate promotion, never a push.

## Workflow

1. **Name which rule the work touches** before designing anything. Most Yazhi work touches one or two; "all of them" means the scope is not yet understood.
2. **Check the data path first.** If the change sends citizen data, child data, or prompts to a foreign cloud or API, it fails தற்சார்பு and cannot ship as designed — redesign or get explicit founder sign-off and document it.
3. **Check the child gate.** Anything reachable by a child needs counsel sign-off, verified parental consent, and a kid red-team score ≥98% before exposure. This gate is not deferrable to "after launch".
4. **Demand the source.** For any claim in a doc, PR, or model answer, name the citation. If there is none, write "தெரியவில்லை" rather than a plausible sentence.
5. **Confirm the chamber.** New work starts in அகம்; promote to புறம் only after review by agents (Vajra/Kaaval/Thozhan) and a human. Never copy private keys, internal configs, or unfinished research into a public repo.
6. **Attach the plan and the rollback.** For anything that changes a running system, write the runbook and the one-command rollback before executing, and require a human confirm.
7. **Label the status honestly.** Draft, inference, and plan are three different words; using "done" for any of them breaks சொல்லிய வண்ணம் செயல் and poisons the next reader's trust.

## Anti-patterns

- **Treating அறம் as branding.** Printing "no claim without a source" in a README while the model invents verse numbers is worse than silence — the gate is the code path, not the sentence.
- **Sending prompts to a foreign API "for a quick test".** One request from a laptop can put child data on someone else's server; தற்சார்பு has no staging exemption.
- **Shipping a Tamil string without native review.** Machine-fluent Tamil that a native speaker finds wrong is a reputational cost paid by the whole ecosystem, and it is the most common அன்பு failure.
- **Pushing from அகம் to புறம் directly.** Bypasses the review gates and has leaked private keys and internal configs into public history.
- **Calling a plan "done".** The most common சொல்லிய வண்ணம் செயல் breach; a plan marked done stops getting reviewed while the work continues.
- **Deferring the child gate to "after launch".** Counsel sign-off and ≥98% kid red-team are preconditions; a launch without them is a launch we cannot defend.

For doc-level application see `org-doc-authoring`; for code-level see `org-healthy-code`; for PR-level see `org-impactful-pr`; for release gates see `org-release`; for the full test suite see `adhan-status` and `llm-security-review`.
