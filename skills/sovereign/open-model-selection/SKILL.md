---
name: open-model-selection
description: Use when choosing an LLM for a sovereignty-sensitive deployment — government, regulated industry, or any org that cannot depend on a foreign vendor's API — and open-weight self-hosting is on the table. Helps you evaluate license terms, provenance, and the real performance/ops tradeoff against proprietary APIs.
---

Sovereignty requirements often rule out proprietary hosted APIs outright: the model provider is a foreign entity subject to another jurisdiction's laws, the API requires sending data outside the country, or the vendor can unilaterally change terms or cut access. Open-weight models let an organization control inference location, audit behavior, and avoid vendor lock-in — but they shift real cost and risk onto the org's own infrastructure and ML-ops team. Choosing the wrong model or license here is expensive to reverse once integrated.

## Workflow

1. **Confirm the sovereignty driver first.** Is it data residency (data can't leave the country), vendor jurisdiction risk (provider is subject to a foreign government's compulsion), air-gap requirement (`airgapped-llm-deployment`), or cost at scale? The driver determines how strict the model selection needs to be — e.g., air-gap rules out anything requiring a license-check callback.
2. **Shortlist candidates by task fit**, not just leaderboard rank — check for domain/language coverage (e.g., regional language support if not English-only).
3. **Read the actual license, not the marketing page.** Confirm: commercial use allowed, redistribution/self-hosting allowed, no usage-report-back clause, no field-of-use restriction that conflicts with the deployment (e.g., government/defense-use exclusions exist in some "open" licenses).
4. **Check provenance.** Does the model card disclose training data sources, or at least data categories and geographic origin? For regulated deployments, undisclosed provenance is itself a risk — you cannot represent to an auditor what you cannot verify.
5. **Verify weight availability and format.** Full weights (not API-only "open" models) in safetensors format, with a permissive download path — required for both self-hosting and air-gapped export.
6. **Benchmark against the proprietary alternative on your own eval set**, not public leaderboards alone — gap varies heavily by task and language.
7. **Cost the self-hosting burden honestly**: GPU capacity, inference-serving engineering, monitoring, and update/patch cycle (see `airgapped-llm-deployment` for the offline case). Compare against proprietary API pricing at expected volume.
8. **Decide and document** the choice with the license, provenance summary, and benchmark numbers attached — this becomes the audit artifact for `data-residency-compliance` reviews.

## Licensing and provenance comparison

| Factor | Fully open (Apache-2.0/MIT weights) | "Open-weight" with usage restrictions (e.g., Llama-style) | Proprietary API-only |
|---|---|---|---|
| Self-host/air-gap capable | Yes | Usually yes, check field-of-use clause | No |
| Commercial/government use | Unrestricted | Sometimes restricted above a user/revenue threshold or for defense use | Per vendor contract |
| Training data disclosure | Varies, check model card | Varies, check model card | Almost never |
| Modification/fine-tune rights | Yes | Usually yes | No |
| Jurisdiction exposure | None (self-hosted) | None (self-hosted) | Vendor's home country |

## Numeric defaults

- Require model card provenance disclosure covering at least data category and geography — reject "trained on a large internet corpus" with no further detail for any government-facing deployment.
- Budget GPU capacity for self-hosting at roughly 1.2-1.5x the raw model memory footprint (weights + KV cache headroom) before committing to a sizing decision.
- Re-benchmark quarterly, or immediately after any fine-tune, against the same eval set to catch regression.

## Anti-patterns

- **Equating "open-weight" with "open-source"** — many open-weight licenses restrict commercial scale, government, or military use; read the actual license text every time, don't assume from the name.
- **Selecting purely by public leaderboard score** — leaderboards rarely reflect your language, domain, or safety requirements; always run your own eval.
- **Ignoring the ops burden** — self-hosting an LLM well requires GPU capacity planning, serving-engine expertise, and a patch cadence; underestimating this is the most common reason sovereign deployments stall post-launch.
- **Downloading weights from unofficial mirrors** — verify checksums against the publisher's official repo to avoid tampered weights, especially before air-gapped export.
- **Choosing a model with no committed maintenance/security-patch path** — an abandoned open model becomes a liability once vulnerabilities in the serving stack or model itself surface.

Cross-reference `airgapped-llm-deployment` for packaging the chosen model into a disconnected environment, `sovereign-cloud-architecture` for where the self-hosted inference runs, and `secure-code-review` when auditing any fine-tuning or serving code before production.
