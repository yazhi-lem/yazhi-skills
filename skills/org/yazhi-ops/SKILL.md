---
name: yazhi-ops
description: Use when setting or running Yazhi's operating cadence — the daily digest, weekly review, monthly gate, and quarterly reset — or when work is slipping and you need to know which ritual was skipped. Helps you run the rhythm as a system instead of improvising each week.
---

Yazhi runs on a cadence, not a backlog. The cadence is four loops — daily, weekly, monthly, quarterly — each with one owner, one artefact, and one gate. Capitol is the read model over Linear and GitHub, so a number means the same thing on the console, in the Slack digest, and in the `/capitol` command. When work slips, the question is never "who is slow" but "which loop was skipped". This skill owns the loops; `yazhi-daily-rhythm` owns the engineer's day inside them.

## The four loops

| Loop | When | Owner | Artefact | Gate |
|---|---|---|---|---|
| Daily | 08:45 IST, Mon–Sat | Rotating duty engineer | Slack digest (status, overdue, this week, PRs) | PRs older than 24h flagged |
| Weekly | Monday 10:00 IST | Guild master | Week brief: 3 headlines, 3 questions, owners | PRs older than 48h blocked |
| Monthly | First Monday | Guild master + counsel | Launch gate review, quest close | Store credentials, child safety |
| Quarterly | Start of quarter | Founders | Reset or continue; retire dated plans | Plan-reset note in `docs/` |

## Daily loop

1. **Read the digest, not the backlog.** The digest has four blocks: status, overdue, what lands this week, and PRs with a warning marker. Read those four; everything else is optional.
2. **Clear the ageing PRs first.** Anything over 24h gets a review or a comment today; the 48h limit is a hard gate, not a target.
3. **Check your own overdue items.** Overdue means a due date passed — not "I have not started". A moved due date is honest; a silent one is not.
4. **Protect one deep block.** No meetings, no digest, no Slack in the deep block; the daily loop is 30 minutes, the deep block is the rest.
5. **Close the day by updating status, not by reporting.** Move the Linear issue to its real state and leave a one-line note on what changed. A status update is a fact; a standup sentence is a story.

## Weekly loop

1. **Write the week brief as three headlines and three questions** — not a task list. Headlines say what lands; questions say what is still unknown. A week with no questions is a week with no learning.
2. **Assign one owner per headline.** Shared ownership is no ownership; the brief names a person, not a team.
3. **Review the 48h gate.** Count PRs older than 48h; a non-zero count is the week's first fix, before any new work.
4. **Check the Tamil review queue.** Every user-visible Tamil string needs a native reviewer; the queue is a gate, not a backlog.
5. **Re-derive the dates from the repos, not from memory.** Read `docs/README.md` and `CONTEXT.md`; a date that only exists in a chat message is not a date.

## Monthly and quarterly

1. **Monthly: run the launch gate review.** For each launch in the next 30 days, check the four gates — store credentials, child safety, DPDP residency, and the tested rollback. A launch without all four is not a launch.
2. **Monthly: close the quests.** Quests that did not complete get a reason and a decision — carry, cut, or rewrite — not a silent rollover.
3. **Quarterly: decide reset or continue.** If direction changed, write the retirement note and archive the old plan (`org-plan-reset-recovery`); if not, restate the same plan with new dates.
4. **Quarterly: audit the cadence itself.** Which loop was skipped most? A skipped loop is a design problem, not a discipline problem.

## Escalation ladder

| Situation | Escalate to | Within |
|---|---|---|
| PR blocked on a review | Duty engineer | same day |
| Build or CI broken on main | Duty engineer | 1 hour |
| Gate cannot pass (credentials, counsel) | Guild master | same day |
| Customer-facing outage | Guild master + founder | 15 minutes |
| Direction or scope question | Founder | next weekly |

## Anti-patterns

- **Running the digest as a status report.** The digest is a triage input; reading it aloud in a meeting wastes the one block that should be spent on work.
- **Skipping the 48h gate "just this week".** The gate is the only thing that stops review debt compounding; one skipped week becomes a month of rubber-stamps.
- **Weekly briefs as task lists.** A list of tasks hides the questions; the questions are what the week is for.
- **Monthly gates run from memory.** Read the repo's `docs/README.md` and `CONTEXT.md`; a gate checked against a stale snapshot is not checked.
- **Quarterly reset without a retirement note.** The old plan resurfaces in an issue and someone acts on it (`org-plan-reset-recovery`).
- **No duty rotation.** One person always reads the digest, so the cadence dies when they are away.

For the engineer's hour-by-hour day see `yazhi-daily-rhythm`; for the PR contract see `org-impactful-pr`; for the gates see `org-ethos` and `org-release`; for the repo state see `yazhi-org-status`.
