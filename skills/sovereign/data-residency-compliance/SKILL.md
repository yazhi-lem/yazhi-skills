---
name: data-residency-compliance
description: Use when a project must keep data within a specific jurisdiction (GDPR, India's DPDP Act, sector rules) or a government/regulated-industry customer asks where data lives and who can access it. Helps you map data flows, pick applicable regimes, and produce an auditable residency posture.
---

Regulators and enterprise customers increasingly require proof — not just promises — that personal or sensitive data never leaves an approved jurisdiction, that access is logged, and that foreign subpoenas cannot reach it via a subprocessor. Getting this wrong blocks deals, triggers fines (GDPR: up to 4% global revenue; DPDP Act: up to INR 250 crore), and forces expensive re-architecture after the fact. Treat residency as a design constraint from day one, not a compliance checkbox added later.

## Workflow

1. **Inventory data flows.** List every place personal/sensitive data is created, stored, processed, cached, logged, or backed up — including third-party APIs (analytics, LLM providers, email, CDN, error tracking). Diagram the flow; do not skip logs, backups, and support tooling.
2. **Classify the data.** Tag each flow as personal data, sensitive personal data (health, biometric, financial, religious/caste under DPDP), or non-personal. Classification drives which regime applies and how strict controls must be.
3. **Identify applicable regimes** using the table below. A single product can be subject to several simultaneously (e.g., EU users under GDPR + India users under DPDP).
4. **Map legal basis and cross-border transfer mechanism** for each flow that crosses a border (SCCs, adequacy decision, DPDP's notified-country list, explicit consent).
5. **Pin storage and processing to region.** Configure cloud regions, database read replicas, and backup targets explicitly — never rely on provider defaults. Verify LLM/AI vendor endpoints don't silently route through out-of-region infrastructure (see `airgapped-llm-deployment` and `open-model-selection` if in-region inference isn't available).
6. **Build the audit trail.** Every access to regulated data needs an immutable log (who, what, when, legal basis). Retain logs 1-7 years depending on regime; default to 3 years unless a sector rule states otherwise.
7. **Interrogate vendors before signing.** Use the due-diligence questions below on every subprocessor.
8. **Re-run the inventory** on a fixed cadence (quarterly minimum) and whenever a new vendor, feature, or region is added.

## Regime comparison

| Regime | Scope | Cross-border transfer | Breach notification | Max penalty |
|---|---|---|---|---|
| GDPR (EU) | Any EU resident's personal data | SCCs, adequacy decision, or BCRs | 72 hours to regulator | 4% global revenue or €20M |
| India DPDP Act 2023 | Digital personal data of India-located persons | Allowed except to govt-blacklisted countries | "As soon as possible" (rules pending) | INR 250 crore |
| HIPAA (US health) | PHI | Business Associate Agreement required | 60 days | $1.5M/year per violation category |
| PCI-DSS | Cardholder data | Tokenization/segmentation required | Per acquirer contract | Fines + loss of processing rights |
| Sector rules (e.g., RBI, finance) | Financial records | Often mandates in-country storage only | Regulator-specific | Varies, can include license revocation |

## Vendor due-diligence questions

- Which physical regions/data centers store and process our data, including backups and disaster recovery?
- Do you use subprocessors outside the agreed region? Provide the current subprocessor list and change-notification SLA.
- Can you contractually commit to data-in-region with no admin access from outside the jurisdiction?
- What law enforcement/government access requests have you received, and what is your challenge policy?
- Do you support customer-managed encryption keys (see `secrets-management`) so you cannot be compelled to decrypt?
- What audit certifications do you hold (ISO 27001, SOC 2, in-country equivalents) and can we get the report?

## Anti-patterns

- **Trusting the provider's "default region" setting** — many services silently replicate metadata, logs, or ML features to a global control plane outside the chosen region.
- **Treating consent as a substitute for a transfer mechanism** — under GDPR and DPDP, consent alone rarely legalizes a systemic cross-border architecture; you still need SCCs or an adequacy basis.
- **Logging PII into observability/error-tracking tools** hosted outside the approved region — this is the most common accidental leak.
- **Skipping backups and DR sites in the inventory** — a compliant primary region with an out-of-region backup still violates residency.
- **One-time compliance review** — new features and vendors drift out of compliance silently; without periodic re-audit (step 8) you find out during a customer's security questionnaire or a breach, not before.

Cross-reference `sovereign-cloud-architecture` for infrastructure-level isolation and `secrets-management` for key-control patterns that keep encryption keys out of foreign-jurisdiction reach.
