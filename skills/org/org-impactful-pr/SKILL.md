---
name: org-impactful-pr
description: Use when opening or reviewing a pull request in a Yazhi repo and you want it to land within the 48-hour gate without rework — especially when the PR touches Tamil strings, child-facing code, or another repo's contract. Helps you write the scope, evidence, and honest status that a reviewer can verify instead of trust.
---

A PR in Yazhi is reviewed by a second human within 48 hours, and Capitol flags any open PR past that line. The gate only works if the PR states what it changes, what proves it works, and what it deliberately leaves undone. `org-healthy-code` owns the diff; this skill owns the write-up and the review path.

## The PR body contract

| Section | Content | Why a reviewer needs it |
|---|---|---|
| What changed | One sentence, behavior-level not file-level | Lets them decide whether to read at all |
| Why | The issue, the plan, or the incident | Distinguishes planned work from drive-by |
| Evidence | Command run, output, screenshot, or test name | Verification instead of trust |
| Contract impact | Which repo/proto/doc contract, and merge order | Prevents the broken-consumer merge |
| Status | `done` / `draft` / `plan only` — never ambiguous | சொல்லிய வண்ணம் செயல் |
| Gaps | What is not done and who owns it | Stops "done" from being a lie |

## Workflow

1. **State the scope in one behavior sentence** before writing code — "the keyboard now suggests sandhi-joined forms" beats "update Kotlin files". If the sentence needs "and", split the PR.
2. **Link the source of truth.** Issue, ADR, or runbook. If there is none, the PR is unexplained work and should be a draft until the plan exists.
3. **Attach evidence, not adjectives.** The command you ran and its output, the test name and its assertion, or the screenshot. "Tested locally" is not evidence.
4. **Flag Tamil strings for native review.** Every user-visible Tamil string needs a native-speaker pass before merge; list the reviewed strings in the PR so the reviewer does not have to hunt for them.
5. **Flag child-facing and data-moving changes.** Anything reachable by a child needs the குழந்தை காப்பு gate; anything sending data off-machine needs தற்சார்பு sign-off. Say so in the PR, not in a DM.
6. **Declare contract impact and merge order.** If the change touches a proto, schema, or doc contract, name the consumer repo and the order — see `org-cross-repo-change`. A silent breaking change is the most expensive PR defect in the ecosystem.
7. **Set the status honestly and keep it current.** Open as draft if the work is not finished; mark `done` only when the gaps section is empty. Update the status when the review changes the plan.

## Anti-patterns

- **A PR that "closes #N" while blocked.** The issue stays open, the claim rots, and triage later cannot tell what is real — verify merge state and checks before writing "closes".
- **Scope creep in the description.** Adding "also refactored X" makes the diff look large and the reviewer skim; split it.
- **No evidence section.** The 48-hour gate becomes a social gesture; reviewers approve what they did not verify.
- **Shipping a Tamil string without native review.** The most common அன்பு failure and the one users notice first.
- **Marking a PR done with known gaps.** Breaks சொல்லிய வண்ணம் செயல் and leaves the next reader to discover the gap in production.
- **Cross-repo change merged without the consumer.** Leaves the ecosystem broken for anyone who pulls in between; see the merge-order table in `org-cross-repo-change`.

Follow `org-healthy-code` for the diff itself; `org-ethos` for the அறம் and அன்பு gates; `org-issue-triage` when the PR closes an issue; `org-release` when the PR is part of a release; `technical-documentation` when the PR changes docs.
