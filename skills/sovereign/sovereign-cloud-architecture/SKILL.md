---
name: sovereign-cloud-architecture
description: Use when architecting infrastructure for a government, defense, or regulated customer that requires national/organizational control over data, keys, and operations — not just data-in-region but freedom from foreign-jurisdiction compulsion. Helps you design multi-region isolation, local key control, and a credible exit strategy.
---

Data residency alone doesn't guarantee sovereignty: a foreign-owned cloud provider operating a local region can still be legally compelled (e.g., US CLOUD Act) to hand over data or access regardless of where it's physically stored. True sovereign architecture controls the full stack — infrastructure ownership, key custody, subprocessor chain, and personnel jurisdiction — and is designed so the organization can leave a provider without catastrophic disruption. Government and regulated-industry procurement increasingly requires proof of this, not just a regional data center.

## Workflow

1. **Establish the sovereignty threat model.** Are you defending against foreign government compulsion, vendor lock-in, geopolitical disruption, or all three? This determines whether a hyperscaler's "sovereign region" offering suffices or a true national/local-operator cloud is required.
2. **Map every subprocessor in the stack** — compute, storage, DNS, CDN, monitoring/SaaS tools, support access — and flag any entity incorporated or headquartered outside the trusted jurisdiction. A single foreign subprocessor with data-plane access undermines the whole architecture.
3. **Design multi-region isolation.** Separate environments (prod/staging, or per-tenant for government customers) into isolated regions/accounts with no implicit trust between them; a breach or legal action in one must not expose the other.
4. **Put key management under local control.** Use customer- or nationally-controlled HSMs/KMS for encryption keys so the cloud provider cannot decrypt data even under compulsion (bring-your-own-key or hold-your-own-key models). Coordinate with `secrets-management` for day-to-day key handling practices.
5. **Restrict operational access by personnel jurisdiction.** Confirm support/SRE staff with data-plane access are within the trusted jurisdiction, or that access is mediated (just-in-time, logged, revocable) when it isn't.
6. **Architect for portability from day one.** Avoid provider-proprietary APIs where a standard equivalent exists (Kubernetes over proprietary PaaS, standard SQL over proprietary managed-database extensions) so workloads can be redeployed elsewhere.
7. **Write and test an exit plan.** Document data export procedure, expected export volume/time, and an alternate provider or on-prem target. Run a partial exit drill (export + restore a non-critical workload) at least annually.
8. **Continuously verify**, not just at signing — cloud providers' subprocessor lists and regional offerings change; re-run steps 2 and 5 at least twice a year.

## Deployment option comparison

| Option | Foreign jurisdiction exposure | Key control | Typical cost | Best for |
|---|---|---|---|---|
| National/local sovereign cloud operator | None | Full local control | Higher, less elastic | Government, defense, top-tier regulated |
| Hyperscaler "sovereign region" (local entity, local staff) | Reduced but not zero (parent entity risk) | Often BYOK available | Medium | Large regulated enterprise |
| Standard hyperscaler region, no sovereignty controls | Full | Provider-managed by default | Lowest | Non-sensitive workloads only |
| Fully on-prem / private data center | None | Full | Highest ops burden | Air-gapped or classified (see `airgapped-llm-deployment`) |

## Numeric defaults

- Target under 4 hours for a full encrypted data export to be technically retrievable on demand; longer indicates an exit-plan gap.
- Re-audit the subprocessor list at least every 6 months.
- Require key rotation on a maximum 90-day cycle for sovereign-controlled KMS/HSM keys.
- Run at least one exit/portability drill per year, covering a non-critical workload end-to-end.

## Anti-patterns

- **Conflating "data-in-region" with "sovereign"** — a foreign-owned provider's local region still exposes the org to that provider's home-country legal compulsion; verify actual corporate and legal structure, not just the data center's country.
- **Letting provider-proprietary services accumulate unchecked** — each proprietary API adopted (managed queue, proprietary auth, non-standard database extension) raises exit cost; track this as technical debt explicitly.
- **Leaving key management with the cloud provider** — without customer-held keys, "sovereign" claims are cosmetic; the provider can still be compelled to produce plaintext.
- **Never testing the exit plan** — an exit strategy that exists only as a document, untested, routinely fails when actually needed (contract disputes, sanctions, provider exit from the market).
- **Ignoring support-tier and monitoring subprocessors** — teams secure the primary data store but overlook that their APM/logging/support vendor has broad data-plane access from a foreign jurisdiction.

Cross-reference `data-residency-compliance` for the regulatory drivers behind these controls, `open-model-selection` and `airgapped-llm-deployment` for AI-specific workloads within a sovereign architecture, and `secrets-management` for the key-handling practices underpinning step 4.
