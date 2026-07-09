---
name: threat-modeling
description: Use when designing a new system, feature, or trust boundary before any code ships — e.g. adding a new API, integrating a third party, or changing auth flow. Helps you systematically enumerate threats, prioritize them by likelihood x impact, and turn them into concrete design changes or tracked risks.
---

Threat modeling is a design-time activity, not a post-incident checklist. Do it before the first line of implementation code is written, whenever a system gains a new trust boundary, data flow, or privilege level. Retrofitting a threat model after ship is strictly worse: mitigations become expensive refactors instead of cheap design decisions, and you inherit whatever assumptions got baked in.

## When to threat-model

Trigger a session whenever any of these happen: a new service or API is designed, a system crosses a new trust boundary (new external integration, new user role, new network zone), sensitive data (PII, credentials, payment info) is introduced or moved, or an existing model is more than ~6 months old and the system changed materially. Do not wait for a security review gate at the end of a project — by then the cost of fixing a structural flaw is 10-100x higher.

## Workflow

1. **Draw the data flow diagram.** Identify every process, data store, external entity, and the data flows between them. Be concrete — name the actual services and databases, not "the backend."
2. **Mark trust boundaries.** Anywhere data crosses from one privilege level, network zone, or ownership domain to another (browser to API, API to DB, service to third-party vendor) is a boundary. List every boundary explicitly.
3. **Enumerate assets.** What is worth attacking — credentials, PII, payment data, model weights, internal APIs, admin privileges? Rank each by business impact if compromised.
4. **Apply STRIDE per boundary.** For each trust boundary, ask whether Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, or Elevation of privilege is possible. Use the table below as a prompt, not a checklist to blindly fill in.
5. **Score by likelihood x impact.** Use a 1-5 scale for each; multiply for a priority score. Anything above 15 blocks ship; 8-15 needs a documented mitigation or accepted-risk sign-off; below 8 can be tracked as backlog.
6. **Decide a mitigation per finding.** Mitigate, transfer (e.g. push to a managed service with better guarantees), accept (with named owner and expiry date), or avoid (remove the feature/flow entirely).
7. **Record and revisit.** Store the model next to the design doc. Re-run step 4-6 whenever the design changes meaningfully.

## STRIDE quick reference

| Category | Question to ask | Typical mitigation |
|---|---|---|
| Spoofing | Can an attacker impersonate a user, service, or device? | Strong auth (mTLS, signed tokens), identity verification |
| Tampering | Can data or code be modified in transit or at rest without detection? | Integrity checks, signatures, immutable audit logs |
| Repudiation | Can an actor deny having performed an action? | Signed, tamper-evident audit trails with timestamps |
| Information disclosure | Can data be read by someone without authorization? | Encryption, least-privilege access, output filtering |
| Denial of service | Can the system be made unavailable? | Rate limiting, quotas, circuit breakers, autoscaling |
| Elevation of privilege | Can an actor gain more access than granted? | Authz checks at every boundary, least privilege by default |

## Anti-patterns

- **Threat-modeling after ship.** Turns design fixes into production incidents and expensive rewrites; do it before implementation starts.
- **Modeling the happy path only.** A diagram with no failure edges or malicious-actor edges isn't a threat model, it's an architecture diagram.
- **Treating STRIDE as a form to fill mechanically.** Categories that don't apply to a boundary should be skipped explicitly ("N/A — no data written here"), not padded with filler findings.
- **No owner or expiry on accepted risks.** An "accepted risk" with no name and no revisit date is a permanent, silently decaying vulnerability.
- **Skipping re-review on change.** A threat model for v1 of an API doesn't cover v2's new admin endpoint; treat significant redesigns as new trigger events.

Findings that involve LLM components (agents, tool-calling, RAG) should be handed to `llm-security-review` for deeper analysis. Findings that require code-level verification feed into `secure-code-review`. Any credential or key flows uncovered here should be checked against `secrets-management`. If a modeled threat materializes, follow `incident-response`.
