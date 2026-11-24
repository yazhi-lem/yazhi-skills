---
name: yazhi-ops
description: Use when deciding what to do next in a Yazhi working week, running a daily or weekly review, or diagnosing why work is stalling. Helps you follow the operating rhythm — daily digest, 48-hour PR rule, weekly OKR check, monthly freeze — instead of re-deriving priorities from scratch.
---

Yazhi runs on a rhythm rather than a backlog: a daily digest, a 48-hour review rule, a weekly OKR check, a monthly freeze, and three review gates. Capitol is the operating surface — it mirrors Linear (the source of truth for the plan), GitHub PRs, and Slack, and flags anything past the 48-hour rule. This skill owns the cadence; the gates themselves live in `org-ethos` and the release gates in `org-release`.

## The rhythm

| Cadence | What happens | Where it lives | Failure it prevents |
|---|---|---|---|
| Daily | Slack digest: open PRs past 48h, overdue issues, due-this-week | Capitol → Slack digest | Work silently ageing |
| Daily | One review pass on PRs older than 48h | `Code · GitHub` view | Rubber-stamp merges after long waits |
| Weekly | OKR → project → issue progress check | `Overview` / `Projects` views | Plans drifting from the plan |
| Weekly | Native-speaker pass on new Tamil strings | Review queue | Untranslated or wrong Tamil shipping |
| Monthly | Freeze: quest board closes, launch gates re-checked | `Quests` / `Launches` | Scope creep past a gate |
| Per launch | Gate table: credentials, counsel, rollback | `Launches` view | Launching without a gate |

## Workflow

1. **Start the day from the digest, not from memory.** Read the open PRs past 48h and the overdue issues first; those are the commitments already made, and they outrank new work.
2. **Clear the 48-hour queue before taking new scope.** Every PR older than 48h without a review is a broken promise; Capitol flags it, and it is the cheapest thing to fix.
3. **Check the weekly OKR delta once, not continuously.** Compare done/overdue/due-this-week against the plan; a launch that disagrees with Linear shows a warning in Capitol rather than silently picking a date.
4. **Hold the three gates on every change** — technical review, native-speaker review for Tamil, and counsel for anything touching children or legal answers. A gate skipped is a defect, not a shortcut.
5. **Treat the monthly freeze as real.** The quest board closes and the launch line is re-checked; scope added after the freeze needs a founder decision, not a quiet commit.
6. **Promote from அகம் to புறம் deliberately.** Work leaves the private chamber only after the gates pass; the promotion is a reviewed change, not a push (`org-ethos`).
7. **Report the rhythm, not the activity.** A weekly note should say what moved, what is blocked, and what the next gate is — not what everyone did.

## Anti-patterns

- **Starting the week from a blank backlog.** Re-deriving priorities every Monday is how the same issue gets re-planned three times; the plan is Linear, mirrored in Capitol.
- **Letting the 48-hour rule slide.** PRs that sit a week get merged without real review, which is where the security and Tamil defects land.
- **Skipping the weekly OKR check because "we know where we are".** The delta is the only signal that a launch date is at risk; without it, the risk surfaces at the gate.
- **Quietly adding scope after the freeze.** The freeze exists because the gate needs a stable scope; a late commit invalidates the gate, not the freeze.
- **Treating the digest as status theatre.** A digest that lists everything teaches nobody what to do; it should list what is late and what needs a decision.
- **Confusing activity with progress.** "20 PRs merged" is not a rhythm signal; "the 48-hour queue is empty and the next gate is 3 days out" is.

For the values behind the gates see `org-ethos`; for release gates see `org-release`; for PR quality see `org-impactful-pr`; for what is current after a reset see `org-plan-reset-recovery`.
