---
name: enterprise-integration
description: Use when your system needs to connect to a customer's existing SSO/SAML provider, data pipeline, legacy API, or message queue, and you have to negotiate access through their IT/security process rather than just configuring it yourself. Helps you plan integration patterns and access requests so enterprise IT constraints don't become last-week surprises.
---

Forward-deployed engineers rarely control the systems they need to integrate with — customer IT owns the identity provider, the data warehouse, and the network, and every access request goes through a change process that runs on the customer's timeline, not yours. Underestimating how long enterprise access provisioning takes is one of the most common causes of slipped deadlines in FDE work, because it's a dependency you can't route around by working harder.

## Workflow

1. **Inventory every system you need to touch during discovery**, not after the build starts — see `customer-discovery`. For each: what's the interface (REST, SOAP, flat-file drop, message queue), who owns it, and what's the access request process.
2. **File access requests immediately, even before design is final.** Enterprise IT provisioning (service accounts, firewall rules, VPN access, SAML app registration) commonly takes 5-10 business days minimum; treat it as the critical path, not a background task.
3. **Default to the customer's existing identity provider for auth.** Don't stand up a parallel auth system unless explicitly required — implement SSO via SAML 2.0 or OIDC against their IdP (Okta, Azure AD, Ping, etc.), since a second login system is both a security red flag and an adoption blocker.
4. **Prefer pull over push for legacy data integration** where possible. Polling a legacy API or reading a scheduled file export is lower-risk than asking the customer to modify their system to push data to you — modifying legacy systems often requires their own change-control cycle.
5. **Negotiate the smallest viable access scope.** Ask for read-only and a specific dataset/queue before asking for broader access; over-asking slows down security review and rarely gets approved faster.
6. **Build an anti-corruption layer at the integration boundary.** Translate the customer's legacy data model into your own internal model at a single well-defined boundary, so their schema quirks and future changes don't leak through your whole system.
7. **Confirm message delivery semantics explicitly** for any queue integration (at-least-once vs. exactly-once, ordering guarantees) — don't assume; legacy queues frequently have surprising guarantees or none at all.
8. **Document every credential, endpoint, and access grant** in a single integration register as you go, so `deployment-runbook` pre-flight checks and support handoff aren't reconstructed from memory later.

## Integration pattern decision matrix

| Customer system type | Preferred pattern | Fallback if blocked | Typical access lead time |
|---|---|---|---|
| SSO/Identity (Okta, Azure AD, Ping) | SAML 2.0 / OIDC federation | Temporary local auth, flagged as tech debt | 5-10 business days |
| Data warehouse / lake | Scheduled read-only pull (JDBC/API) | Customer-managed export to shared storage | 3-7 business days |
| Legacy REST/SOAP API | Direct API call with service account | Vendor-provided adapter or middleware | 5-15 business days |
| Message queue (Kafka, MQ, IBM MQ) | Dedicated consumer group, least-privilege topic ACL | Scheduled batch export as interim | 5-10 business days |
| File-based legacy system | SFTP drop with defined schema and cadence | Manual export during POC, automate later | 3-5 business days |

## Anti-patterns

- **Designing before checking access constraints.** Building the integration architecture around an assumed API before confirming the customer's IT will grant that access, then redesigning under deadline pressure when it's denied.
- **Standing up a parallel login system.** Skipping SSO integration "for now" — it becomes permanent, fails security review at production time, and blocks the `poc-to-production` gate.
- **Requesting broad access "to be safe."** Asking for write access or full-database scope when read-only on one table would do; this triggers a slower, more scrutinized security review.
- **Assuming queue semantics.** Building on an assumed at-least-once or ordering guarantee without confirming it with the queue owner, leading to duplicate-processing or ordering bugs discovered in production.
- **No anti-corruption layer.** Letting the customer's legacy schema bleed directly into your core data model — every upstream schema change then requires changes throughout your system instead of at one boundary.
