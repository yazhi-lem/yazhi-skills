---
name: kanaku-biz
description: Use when pricing a self-hosted or offline Yazhi product, designing a P2P barter or mutual-aid transaction format, or sanity-checking unit economics under a hard resource cap. Helps you keep an ownership-respecting pricing model (one-time purchase, no SaaS lock-in) and barter payloads small enough to actually travel over BLE mesh.
---

Kanaku handles the commercial layer for products sold to communities that cannot assume a cloud, a credit card, or continuous connectivity. Pricing that assumes recurring revenue and always-online payment is a product that will not work where Yazhi deploys.

## Workflow

1. **Start from the resource ceiling, not the market.** Establish device cost, storage cap, and connectivity budget first; unit economics are downstream of whether the hardware fits the price.
2. **Cost the build honestly** — BOM, assembly, packaging, and the fraction of support time per unit; a ₹4,000 device with 2 hours of support is a loss.
3. **Choose the transaction model deliberately**: one-time purchase (default), sliding scale for students, or barter for community exchange — and write down why.
4. **Design barter payloads to fit the transport.** A BLE advertisement is roughly 31 bytes; a mesh gossip packet a few hundred. If the schema does not fit, split it.
5. **Make offline payment a first-class path** — cash handover, voucher, or offline-signed receipt, with reconciliation on next sync.
6. **Compute break-even and state the assumption** (units per month, support hours); an unstated assumption is an untested one.
7. **Re-check after any hardware change.** A ₹500 BOM shift flips whether the model closes.

## Model comparison

| Model | Cash pattern | Works offline | Lock-in risk | Best for |
|---|---|---|---|---|
| One-time licence | Single payment | Yes | None | Device bundles, local deployments |
| Sliding scale | Tiered one-time | Yes | None | Students, community groups |
| Barter / mutual aid | In-kind | Yes (mesh) | None | Village exchange networks |
| Subscription | Recurring | No | High | Only where network + billing exist |

## Defaults

- Price at 2.5–3× BOM before support is costed; below 2× there is no support margin.
- Barter payload ceiling: 512 bytes including signature and integrity hash.
- Reserve 10–15% of revenue for support and returns.

## Anti-patterns

- **Assuming SaaS revenue for an offline device.** Without recurring connectivity there is no recurring payment, and billing churn destroys the relationship.
- **Pricing below BOM to win adoption.** You cannot fund support, and the first hardware failure becomes a public one.
- **A barter schema that only fits over HTTP.** Mesh and BLE transports will reject it exactly where it is needed.
- **Unstated break-even assumptions.** The number looks defensible until the first real cost arrives.
- **Treating TAM/SAM/SOM as the decision.** For these deployments, unit margin at realistic volume is the deciding number.

For the user research behind price sensitivity see `customer-discovery`, for the deployment cost side see `deployment-runbook`, and for offline storage constraints see `thozhan-dev`.
