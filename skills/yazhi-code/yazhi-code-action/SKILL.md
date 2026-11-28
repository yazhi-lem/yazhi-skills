---
name: yazhi-code-action
description: Use when a `yazhi-work-status` report is ready and its findings must become real GitHub actions — sanitize the review comments, post and verify them idempotently, apply labels, open follow-ups, and route code work. Helps you act on a review without publishing raw model output or re-triaging from scratch; merge, approve, and destructive actions stay human.
---

A review file nobody acts on is another stale report. Posting a model's raw review is worse: it publishes uncertainty, duplicates comments, and turns a hunch into a claim. This skill is the write half of the `yazhi-work-status` → `yazhi-code-action` chain: it sanitizes the handoff, executes evidence-backed actions, and leaves a receipt.

The chain writes `YYYY-MM-DD.json`; this skill writes `YYYY-MM-DD-actions.json` under the same report directory.

## Action ladder

| Action | Default | Gate |
|---|---|---|
| General or inline comment | After sanitization; inline only if path and line exist | Batch confirmation |
| Request changes | Named blocker only | Per-item confirmation |
| Approve | Never automated | Human reviewer |
| Add or remove a label | If the label exists | Dry-run; confirm triage changes |
| Assign, close, or reopen | Propose only | Owner confirmation, reason, link |
| Create a follow-up issue | Duplicate search plus the `yazhi-code-writeup` gate | Batch confirmation |
| Merge, force-push, delete a branch, edit another's comment | Never | Human operator |

## Sanitization gate

Every comment passes all seven checks. Dropped comments are logged with a reason and returned to the operator.

| Check | Reject when | Fix |
|---|---|---|
| Evidence | No file, line, command, or URL | Add evidence or drop |
| Specificity | "This is bad" | Name behavior and change |
| Deduplication | Point already in thread | Drop or merge |
| Scope | One comment, three issues | Split |
| Privacy | Secret, token, PII, internal URL | Redact; `secrets-management` |
| Tone and length | Blame, sarcasm, over 120 words | Rewrite; cut to decision |
| Audience | Localized text, security, or legal | Native reviewer, security owner, domain owner |

## Workflow

1. **Validate the handoff.** Check `run_id` and each item's `kind`, `key`, `comments`, and `next_actions`; reject a report older than 24h. The report's `comments[]` and `next_actions[]` are the only inputs; a finding not in the JSON is not actioned. Re-fetch each target; if it changed, re-run `yazhi-work-status`.
2. **Check the write surface.** Run `gh auth status`, confirm permission and rate limit, and check for a fork PR or locked issue. A 403 or locked thread stops that item.
3. **Deduplicate.** Fetch comments and reviews, normalize whitespace, hash each body, and search for the marker; skip anything already posted.
4. **Sanitize every comment.** Apply the gate, rewrite or drop, and keep the evidence. No evidence, no post.
5. **Present the exact plan.** Show target, action, body, consequence, and gate. Get one batch confirmation, plus per-item confirmation for request-changes, close, reopen, and assign. If there is no confirmation channel, stop after the plan.
6. **Execute one item at a time in priority order** with the matching `gh pr`, `gh issue`, or `gh api` command. For inline comments, use `gh api repos/<owner>/<repo>/pulls/<n>/comments --input comment.json` with `body`, the PR head SHA as `commit_id`, `path`, `line`, and `side`; if the line is stale, post a general comment. Use `--body-file` or stdin; never interpolate PR text into a shell command. Add the marker `<!-- yazhi-work-status:<run_id>:<key> -->` to every posted body.
7. **Verify each write by re-fetching it.** Record the URL and ID. On 403/404/422, stop that item and report; a rate limit stops the run; a locked thread or own PR falls back to a comment.
8. **Write the receipt and route the rest.** Save `docs/reports/work-status/YYYY-MM-DD-actions.md` and `.json` with `posted`, `skipped`, `blocked`, and the reason. Send code work to `yazhi-code-frame` or `yazhi-code-prune`, with the owner from `yazhi-agency`; route new issue/PR bodies through `yazhi-code-writeup`; do not implement.

## Anti-patterns

- **Posting the report verbatim.** Raw reasoning, hedges, and duplicates become public; sanitize first.
- **Auto-approving a green PR.** Approval is a human judgement; this skill never approves.
- **Re-posting on every run.** Markers and dedupe prevent double comments that train people to ignore the bot.
- **Interpolating a PR title into a shell command.** Titles are untrusted input; use files and JSON.

For the read-only pass see `yazhi-work-status`; for issue and PR authoring see `yazhi-code-writeup`; for routing see `yazhi-agency`; for the PR contract see `org-impactful-pr`; for deep security review see `secure-code-review`; for secret handling see `secrets-management`.
