---
name: secrets-management
description: Use when adding, storing, rotating, or auditing credentials, API keys, or tokens anywhere in a codebase or infrastructure — before committing config, when provisioning a new service integration, or when a leak is suspected. Helps you keep secrets out of source control and scoped to least privilege.
---

Secrets that leak into source control, logs, or overly broad IAM roles are one of the most common and most preventable causes of breaches. The rule is simple to state and easy to violate under deadline pressure: secrets live in a secrets manager or injected environment, never in a repository, and every credential is scoped to the minimum it needs.

## Workflow

1. **Never commit secrets, ever.** Before committing config, env files, or infra-as-code, scan the diff for anything that looks like a key, token, password, or connection string. Use a pre-commit secret scanner (e.g. gitleaks, trufflehog) as an enforced hook, not an optional suggestion.
2. **Choose the right storage tier.** Use the decision table below — don't default to plain environment variables for anything beyond local dev.
3. **Scope every credential to least privilege.** A service should get a key that can do exactly what it needs (e.g. read-only on one bucket) and nothing else. Avoid account-wide or admin-level keys for automated services.
4. **Set a rotation cadence per secret class** (see table) and automate it — manual rotation reliably gets skipped.
5. **Separate secrets by environment.** Dev, staging, and prod must never share a credential. A leak in staging should not compromise prod.
6. **Audit for secrets already in git history.** Run a history scanner (gitleaks with `--log-opts`, trufflehog filesystem+git mode) on the full history, not just HEAD, at least quarterly and before any repo goes public.
7. **If a secret leaks: revoke first, then investigate.** Rotate/revoke the exposed credential immediately — do not wait to understand the blast radius first. Then hand off to `incident-response` for containment and postmortem.
8. **Purge from history only after rotation.** Rewriting git history (filter-repo/BFG) to remove a leaked secret is cleanup, not containment — the old value must be treated as permanently compromised regardless of history rewriting, since forks/clones may already have it.

## Storage tier decision table

| Use case | Recommended storage | Notes |
|---|---|---|
| Local developer secrets | `.env` file, gitignored, never committed | Use `.env.example` with placeholder values only |
| CI/CD pipeline secrets | Platform secrets store (GitHub Actions secrets, etc.) | Never echo secrets in build logs |
| Production app runtime secrets | Dedicated secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) | Inject at runtime, not baked into images |
| Service-to-service auth | Short-lived tokens / workload identity (OIDC, IAM roles) | Prefer no long-lived static credential at all |
| Third-party API keys | Secrets manager with per-service scoping | One key per integration, not shared across services |

## Rotation cadence defaults

| Secret class | Default rotation period | Trigger for immediate rotation |
|---|---|---|
| Cloud provider root/admin credentials | 90 days | Any suspected exposure |
| Service API keys | 90-180 days | Employee offboarding with access, vendor breach notice |
| Database credentials | 90 days | Schema/access change, suspected leak |
| CI/CD tokens | 180 days | Any leak in build logs or public repo |
| Signing/encryption keys | Per compliance requirement (often 1 year), with overlap period for old key validity | Any suspected compromise |

## Anti-patterns

- **Committing a secret "temporarily" to unblock a build.** Git history is forever; treat any committed secret as leaked the moment it's pushed, even if deleted in the next commit.
- **Using one shared API key across all environments.** Collapses blast radius boundaries — a staging leak becomes a prod incident.
- **Long-lived, broadly-scoped cloud credentials for automation.** Prefer short-lived, narrowly-scoped tokens (workload identity) over static admin keys.
- **Rotating on paper but not in practice.** A documented rotation policy nobody automates is a false sense of security; wire rotation into tooling, not a calendar reminder.
- **Investigating before revoking on a suspected leak.** Every minute a known-leaked credential stays live is exposure; revoke/rotate immediately, investigate in parallel.

Secrets uncovered during a `secure-code-review` or `llm-security-review` pass should be triaged here. Secret-handling boundaries should be identified during `threat-modeling`. A confirmed leak escalates to `incident-response`.
