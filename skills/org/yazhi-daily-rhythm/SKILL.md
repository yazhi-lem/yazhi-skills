---
name: yazhi-daily-rhythm
description: Use when starting an engineering day or when a day has gone sideways and you need the hour-by-hour recovery. Gives the four blocks, three boundaries, and close checks; for weekly/monthly cadence or escalation use yazhi-ops instead.
---

An engineering day has four blocks and three boundaries. The boundaries are the only places you change context. Most lost days are not lazy days — they are days where a block was never protected. This is the day-level companion to `yazhi-ops`, which owns the weekly and monthly loops.

## The day (IST)

| Block | Window | What happens | Hard rule |
|---|---|---|---|
| Digest | 08:45–09:15 | Read the chat digest, clear ageing PRs, set one outcome | No deep work until the 48h queue is known |
| Deep work | 09:15–13:00 | One task, one repo, notifications off | No chat, no "quick" review |
| Review window | 14:00–15:30 | PRs, Tamil strings, anything blocking someone else | Reviewing is work, not a break |
| Close | 17:30–18:00 | Update status, note what changed, set tomorrow's first move | Status is a fact, not a summary |

## The digest block (30 minutes)

1. **Read the four digest blocks in order** — status, overdue, what lands this week, PRs with a warning. Do not open the full backlog first.
2. **List PRs older than 24h and 48h.** The 24h list is today's review queue; the 48h list is a gate breach and goes first.
3. **Check your own overdue items and either move the date or do the work.** A passed due date without a decision is the one status always wrong.
4. **Write one outcome** — one sentence. "Finish the tokenizer eval" is an outcome; "work on the model repo" is not.
5. **Stop at 30 minutes.** Longer means you are reading the backlog instead of the digest.

## The deep block (3h45m)

1. **Pick one task and open one repo.** Multi-repo work is a weekly-scale decision; switching repos mid-block is the most expensive context change there is.
2. **Turn off chat and the digest.** The 48h gate is already known; a second check mid-block is procrastination.
3. **Work in the smallest reviewable unit** — one PR's worth. A 400-line diff is the target (`org-healthy-code`).
4. **Leave a checkpoint at the halfway mark** — a commit, a note, or a failing test.
5. **Stop at the boundary, even mid-task.** Carrying over silently is how the close loses its meaning.

## The review window (90 minutes)

1. **Review the 48h breaches first**, then the 24h queue. A review is a decision: approve, request changes, or ask a question — never "LGTM" without reading the diff.
2. **Check the Tamil strings.** Any user-visible Tamil needs a native reviewer; flag it rather than approving on the author's word.
3. **Check the PR body against the contract** — what changed, evidence, gaps, contract impact (`org-impactful-pr`).
4. **Leave one actionable comment per review.** "Looks good" teaches nothing; "this changes the error contract, update the doc" is a review.
5. **Do not start your own work here.** A review that becomes a code change is a context switch with no boundary.

## The close block (30 minutes)

1. **Move every touched Plane issue to its real state.** In progress, blocked, done — not "still in progress" because the day ended.
2. **Write one line on what changed** in the issue or PR. Tomorrow's digest reads this line.
3. **Set tomorrow's first move** — the exact task and repo, so the digest starts with a decision already made.
4. **Flag anything needing escalation** via the ladder in `yazhi-ops`; a blocker raised at close is a day lost, one raised at the review window is a day saved.
5. **Stop.** The close is 30 minutes, not an extra work block.

## Recovery when the day goes sideways

1. **Name the block that was lost** — digest, deep, review, or close. A day without a close is a day without a tomorrow.
2. **Re-run only the lost block** at the next slot; do not replay the whole day.
3. **If the digest was lost**, run it now — the 48h queue cannot wait.
4. **If the deep block was lost**, protect the next one and shrink the outcome to one reviewable unit.
5. **If the close was lost**, spend five minutes tomorrow writing yesterday's close from the commit log.

## Anti-patterns

- **Skipping the digest because "I know what I'm doing".** It finds the 48h breaches you did not know about.
- **Extending deep work into the review window.** That window is the only slot where other people's work moves.
- **Reviewing without reading.** "LGTM" on a 400-line diff is the rubber-stamp the 48h gate exists to prevent.
- **Closing with a status that is not true.** "In progress" on a task you did not touch makes the next digest useless.
- **Carrying a whole day's plan into tomorrow.** Shrink the outcome instead of stacking two days.
- **Running the day in chat.** A day spent in chat has no block and no boundary.

For the weekly and monthly loops see `yazhi-ops`; for the cross-repo queue see `yazhi-work-status`; for the PR contract see `org-impactful-pr`; for code habits see `org-healthy-code`; for the gates see `org-ethos`.
