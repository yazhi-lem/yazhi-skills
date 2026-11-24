---
name: fde-data-migration
description: Use when moving a customer's data into or out of the system — initial load, environment promotion, or a schema change on live data. Helps you make the migration reversible, verifiable, and safe to run twice without corrupting or duplicating records.
---

A data migration is the highest-risk routine operation in a customer deployment: it is irreversible in practice, it runs against real records, and it is hard to test without the real data. The three questions that prevent most damage are: can I run it twice, can I prove it worked, and can I undo it. This skill owns the migration; `deployment-runbook` owns the environment it runs in.

## Migration types

| Type | Risk | Reversible? | Precondition |
|---|---|---|---|
| Initial load | Duplicate records on rerun | Yes, if idempotent | Empty target or a stable key |
| Schema change | Data loss on column drop | Only with a backup | Backup verified restorable |
| Environment promotion | Config drift | Yes | Same schema in both |
| Customer export / offboarding | Incomplete or leaked data | N/A | Recipient allowlist |
| Live backfill | Long lock, partial writes | Yes, if batched | Batch key + checkpoint |

## Workflow

1. **Write the target state and the count first.** "Table `orders` holds 48,213 rows matching the source" is checkable; "the data is migrated" is not. Counts, not narratives, are the evidence.
2. **Make the load idempotent.** Use a natural key or an upsert; a rerun after a partial failure must not duplicate rows. Test the rerun before the first real run.
3. **Take and verify a backup before any destructive step.** A backup nobody has restored is a hope; restore it to a scratch database and count the rows.
4. **Run in batches with a checkpoint.** Record the last committed batch key; a failure resumes at the next batch instead of restarting the load.
5. **Validate with three checks** — row counts, a checksum or sampled field comparison, and a spot-check of the records the customer will see first. Two of three is not verification.
6. **Respect the residency rule.** Customer data does not leave the approved environment; for an export, use the recipient allowlist and confirm the destination with the customer in writing.
7. **Keep the rollback script next to the migration script** and run it once on a copy. An untested rollback is not a rollback.

## Anti-patterns

- **Running a non-idempotent load twice.** The classic duplication bug; the second run doubles the rows and the customer sees every order twice.
- **Dropping a column without a verified backup.** The data is gone and the "backup" was never restored, so nobody knows if it works.
- **Migrating without a count.** "It ran" is not evidence; without the target count, a partial load looks like success.
- **Loading in one transaction.** A failure at 95% rolls back everything and the window is lost; batches with checkpoints resume.
- **Exporting without an allowlist.** The single worst residency failure — customer data leaves the approved environment and nobody can say where it went.
- **Testing only on sample data.** Production data has the nulls, the duplicates, and the odd encoding that the sample did not.

Follow `deployment-runbook` for the environment baseline, `org-ethos` for the தற்சார்பு residency gate, `secure-code-review` for the ingestion code, and `org-release` when the migration is part of a release.
