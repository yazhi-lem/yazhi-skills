---
name: yazhi-work-status
description: Use when starting a work day, preparing the digest, or asking what is open and what needs attention across all repos. Produces a dated PR/issue queue with a ten-minute light review on relevance, quality, testing, readability, and size, plus a JSON handoff for `yazhi-code-action`; the scan itself never posts, labels, or merges.
---

Most daily status reports are either a raw `gh` dump or a vibe summary. This skill owns the read-only daily pass across all repositories: a dated queue, a short review of each open PR and issue, and a JSON handoff for `yazhi-code-action`. It never writes to GitHub.

## The five review axes

A light review is a triage opinion, not an approval. Spend at most 10 minutes per item and decide what deserves a full review today. At more than 400 changed lines or 20 files, stop reading hunks and recommend a split; green CI answers none of the axes by itself.

| Axis | Pass | Fail |
|---|---|---|
| Relevance | Current issue or plan; not a duplicate | Orphan branch, retired plan, duplicate title |
| Quality | Contentful body: problem, outcome, evidence, acceptance criteria; explicit errors; local-first; no obvious security flag | Empty template, no reproduction, silent fallback, foreign API |
| Testing | Named command and result; assertion can fail; CI green | "Tested locally", assertion-free test, red CI |
| Readability | One outcome; names explain why; readable cold | Drive-by refactor, mixed layers, magic |
| Size | At most 400 changed lines and 20 files | Over either: triage scope only, request a split |

## Workflow

1. **Freeze the snapshot.** Record the IST time, `gh auth status`, rate-limit reset, repos in scope, and each repo's default-branch `HEAD`; together they form the `run_id`.
2. **Pull the whole queue mechanically.** Run one `gh pr list` and one `gh issue list` per repo with `--state open --limit 100 --json` and the fields that decide the queue: `number,title,author,createdAt,updatedAt,isDraft,additions,deletions,changedFiles,reviewDecision,mergeable,statusCheckRollup,labels,url` (issues need a subset). Save the raw output; if a repo is inaccessible, record it in `not_reviewed`.
3. **Rank before reading.** 48h+ PRs first, then red CI, conflicts, and external authors waiting; then 24h PRs; then issues. Age is `createdAt`, not `updatedAt`; a bot bump is not activity.
4. **Review each item against the five axes.** Read the body, the diff stat, then only the hunks that decide the verdict: auth, input, data, money, Tamil, config. For issues, check problem, outcome, and evidence; for PRs, check the `org-impactful-pr` contract. Use `gh pr diff` for named files.
5. **Write one evidence-backed comment per concern, or none.** Cite the file and line, command and result, or URL. Redact secrets and private URLs at capture; the report is shared.
6. **Assign the next action and owner.** Choose from `review`, `request-changes`, `ask`, `label`, `split`, `close`, `assign`, `escalate`, or `none`; route with `yazhi-agency`; mark whether it needs confirmation. Do not perform it.
7. **Emit both artifacts and stop.** Write `YYYY-MM-DD.md` and `YYYY-MM-DD.json` under the workspace `docs/reports/work-status/`. If the timebox expires, mark the rest `not-reviewed`; an honest partial queue beats a guessed complete one.

## Report shape

| Section | Content |
|---|---|
| Top of queue | 48h breaches, red CI, conflicts, external authors waiting |
| Repo scoreboard | Open PRs, 24h/48h counts, open issues, stale issues |
| Per item | Key, five verdicts, severity, next action, owner |
| Bottom | What was not reviewed and why |

## Handoff contract

The JSON carries `run_id`; each item carries `key` (`repo#number`), `kind` (`pr` or `issue`), `url`, `severity`, the five `verdicts`, `comments[]` (`body`, `evidence`, optional `path`/`line`), `next_actions[]` (`action`, `detail`, `owner`, `confirmation`), and `not_reviewed[]`. The Markdown is the human summary.

## Anti-patterns

- **Reviewing everything.** A daily pass that reads every diff becomes a full review and misses the 48h breach; rank first, then timebox.
- **Using `updatedAt` as age.** A bot label bump makes a 90-day PR look new; use `createdAt`.
- **Marking an unread axis as pass.** `not-reviewed` is honest; a guessed pass becomes a false approval in the action step.
- **Posting from the scan.** Once the scan writes to GitHub it is no longer read-only or re-runnable; `yazhi-code-action` owns writes.

See `yazhi-work-start` for a single contributor's session init, `yazhi-daily-rhythm` for the day, `org-impactful-pr` for the PR contract, `org-issue-triage` for close/keep, `org-healthy-code` for size and tests, and `secure-code-review` for a deep pass.
