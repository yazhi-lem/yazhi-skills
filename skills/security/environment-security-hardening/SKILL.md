---
name: environment-security-hardening
description: Use when provisioning or auditing an environment — a container image, a cloud account, CI/CD runners, or a dev/staging/prod config — for vulnerabilities that live outside the application code itself. Helps you catch exposed services, stale dependencies, over-broad IAM, and leaked environment variables that a code-only review never looks at.
---

Most application-layer reviews (`secure-code-review`, `secure-design-patterns`) assume the environment the code runs in is already sound — but a perfectly reviewed codebase deployed on a container running as root, with an unpatched base image, in a security group open to `0.0.0.0/0`, is still compromised on day one. Environment vulnerabilities are the ones no amount of code review catches, because they live in Dockerfiles, IaC, CI config, and cloud console settings, not in the application's source tree.

## Environment attack surface

| Layer | What to check | Common finding |
|---|---|---|
| Container image | Base image CVEs, running user, image provenance | Running as root; base image months out of date; unpinned `:latest` tag |
| Dependencies | Known-CVE packages, transitive deps, license/supply-chain risk | A direct dependency is fine but pulls in a vulnerable transitive package |
| Cloud/IaC config | Security groups, public storage buckets, IAM policy scope | A storage bucket or database left publicly readable; a security group open on all ports |
| CI/CD pipeline | Secrets exposure in logs, runner permissions, third-party action trust | A workflow prints an env var to logs; a CI token with write access to every repo in the org |
| Environment variables / config | Secrets in plaintext env vars vs. a vault, `.env` files committed | Production credentials in a `.env.example` that got filled in and committed by accident |
| Network | Exposed ports, missing segmentation between environments | A staging database reachable from the public internet because segmentation wasn't part of the provisioning checklist |

## Workflow

1. **Scan container images and dependencies for known CVEs before every deploy**, not just at initial setup — pin base image versions explicitly (never `:latest`) and re-scan on a schedule, since new CVEs get disclosed against images that haven't changed.
2. **Run containers as a non-root user by default.** A root-user container escape has full host access; a non-root container escape is contained to that user's limited privileges — set `USER` explicitly in every Dockerfile.
3. **Audit IAM/cloud permissions against actual usage, not against what was convenient to grant.** A service role with `*:*` because nobody had time to scope it is a standing invitation for a small compromise to become a full-account breach — review and tighten quarterly at minimum.
4. **Check that CI/CD secrets never appear in build logs** — a `printenv`, a verbose debug flag, or an uncaught error stack trace can leak a secret into a log that's readable by anyone with repo access, even if the secret itself is stored correctly.
5. **Verify network segmentation between dev/staging/prod.** Staging should not have production credentials, and production should not be reachable from a developer's laptop without going through the same controls a real client would.
6. **Confirm no `.env` file, credentials file, or cloud config with real secrets is committed to source control** — cross-reference `secrets-management` for rotation once a leak is found, but the environment-hardening pass is what should catch it before it ships.
7. **Pin third-party CI actions/plugins to a commit SHA, not a mutable tag**, and review what permissions they request — a compromised or malicious update to a widely-used CI action is a real, repeatedly-exploited supply-chain vector.
8. **Set a re-scan cadence** (weekly for CVE scans, quarterly for IAM/network review) and track findings to closure — a one-time hardening pass decays the moment a new base image CVE is disclosed or a new IAM role is added ad hoc.

## Anti-patterns

- **Using `:latest` or an unpinned base image tag** — makes builds non-reproducible and means a "safe" image today can silently become vulnerable tomorrow with no code change to review.
- **Granting a CI/CD token or service role broad org-wide or account-wide scope** "so it doesn't break" instead of scoping it to the specific repos/resources it needs — the most common way a single compromised pipeline becomes a full-organization incident.
- **Treating a security group or storage bucket's default (often permissive) setting as intentional** — cloud provider defaults are frequently permissive-by-default, and inheriting them without review is an unforced error, not a considered choice.
- **Skipping re-scans after initial setup** — an environment hardened once at launch and never revisited accumulates drift (new CVEs, new IAM grants, config changes) that nobody catches until an incident.
- **Debug/verbose logging left enabled in production or CI**, printing environment variables or request bodies that may contain secrets — convenient during an outage, and a standing leak the rest of the time.

Cross-reference `secure-design-patterns` for least-privilege service-credential scoping, `secrets-management` for what to do once a leaked credential is found, and `security-posture-health-check` for turning this into a recurring audit rather than a one-time pass.
