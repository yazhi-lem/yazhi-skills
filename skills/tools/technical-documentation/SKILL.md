---
name: technical-documentation
description: Use when writing, rewriting, reviewing, or retiring a Markdown doc in any yazhi-lem repository and you need the file contract — header, placement, size budget, link checks, archive rules. Enforces one structure; the green/blue/orange color decision belongs to org-doc-authoring.
---

Yazhi docs fail when they drift out of sync with the code or when three "current status" notes disagree. One short, dated doc per topic beats a pile of plausible snapshots. This skill applies to authored Markdown; generated corpus exports such as open-sangam's `obsidian-vault/` are data, not docs.

## Size budget

A doc that needs a table of contents to find its point is too long for the live tree. Default ceilings: status/current-state pages **2 KB**, runbooks **8 KB**, reference docs **15 KB**, ADRs **4 KB**, skills **700 words**. Anything larger is a book: archive it with a dated digest and leave a short current-status page that links to git history. Aspirational specs for unbuilt systems do not live in `docs/`.

## Workflow

1. **Name the job first.** Is this architecture, a how-to guide, a contract reference, an immutable decision, or evidence? If no category fits, it probably belongs in the repo README or an issue, not a new file.
2. **Look for an existing owner before creating anything.** Search the repo's `README.md`, `CONTEXT.md`, `docs/README.md`, and `archives/` for the same topic. Update the owner rather than adding a second source of truth.
3. **Use the header contract** on every authored doc: one H1, then `Status:`, `Owner:`, `Verified:` (date + commit or code path), and a one-sentence `Scope:`. Mark drafts as drafts; never leave "TBD after plan reset" in the live tree — archive the plan and write a current one-page status instead.
4. **Place it by kind:** `docs/architecture/`, `docs/guides/`, `docs/reference/`, `docs/decisions/`, `docs/reports/`. Use lowercase kebab-case for runbooks and guides; UPPER_SNAKE_CASE for topic/decision docs. Add one row to `docs/README.md` in the same change.
5. **Write current state once.** Put live status in `CONTEXT.md` or `docs/README.md`; other docs link to it. When a fact changes, edit that owner and every link stays valid. Never copy a status table into a second doc.
6. **Retire, don't annotate.** A superseded doc moves to `archives/YYYY-MM-DD-digest.md` as a compressed entry, is deleted from `docs/`, and all inbound links are fixed in the same PR. A "superseded" banner in a live doc is a failure, not a process.
7. **Verify mechanically.** Check relative links from the doc's own directory, confirm the H1/header, and make sure generated files carry a "generated — do not edit" banner. For Tamil text, use `tamil-content-writing` before calling a string final.

| Kind | Location | Rule |
|---|---|---|
| Product overview | `README.md` | ≤100 lines; links out, does not duplicate |
| Current state | `CONTEXT.md` / `docs/README.md` | Dated; one owner per repo |
| How-to / runbook | `docs/guides/` | Numbered steps + verification command |
| Contract | `docs/reference/` | Versioned; code pins it by section |
| Decision | `docs/decisions/` | Immutable; supersede with a new ADR |
| Evidence | `docs/reports/` | Generated/dated; never hand-edited |
| Retired doc | `archives/` | Compressed digest + fixed inbound links |

## Anti-patterns

- **Book as a doc.** A 100 KB spec for an unbuilt subsystem, or a 25-chapter plan with six-week deadlines, is not current documentation — archive it and keep a one-page status.
- **Status snapshot as a doc.** "Complete delivery", "current as of" and "7 scripts" claims rot immediately; point to a dated status owner instead.
- **Banner-managed obsolescence.** Leaving "superseded" text in the live tree makes readers guess which section is true.
- **Deleting a doc without fixing inbound links.** This is how the `factory/` cleanup broke 30 links across seven repos.
- **Treating generated output as authored docs.** Obsidian vault exports and eval reports drift when hand-edited.
- **Copying the same table into two repos.** Keep one canonical table and link to it, as `skill-authoring` requires for overlapping skills.

Follow `skill-authoring` for the file contract, and refresh `yazhi-org-status`, `adhan-status`, `illakiya-status`, and `yazh-unity-status` whenever a repo's status owner changes.
