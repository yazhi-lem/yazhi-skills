---
name: pricing-strategy
description: Use when setting initial pricing for a new product, restructuring tiers, or deciding whether to change a pricing model (seat-based, usage-based, flat, freemium). Helps you anchor price to value delivered and buyer willingness-to-pay instead of defaulting to cost-plus or copying a competitor's sheet.
---

Pricing is a positioning decision, not just a finance one — it signals who the product is for and what it's worth, and it's one of the few GTM levers with immediate, direct P&L impact. Most early pricing mistakes aren't about the number being wrong; they're about picking the wrong pricing *model* (metric) for how the buyer perceives value, which no amount of number-tweaking later fixes.

## Pricing model fit

| Model | Best fit | Fails when |
|---|---|---|
| Flat / per-seat | Value scales with number of users | Value comes from usage intensity, not headcount — light and heavy users pay the same |
| Usage-based (API calls, compute, records) | Value scales with consumption; infra-heavy products | Buyer can't predict monthly cost, creates budgeting friction and finance pushback |
| Tiered (feature-gated) | Clear feature-value ladder across buyer segments | Gating the wrong feature into a higher tier blocks adoption of the core value prop |
| Freemium | Low-friction, high-volume, viral/network-effect products | Free tier cannibalizes paid if it already satisfies the core job-to-be-done |
| Per-outcome / value-based | High-value, measurable outcome (e.g., per-resolved-ticket) | Outcome is hard to attribute or measure cleanly; erodes trust if disputed |

## Workflow

1. **Identify the value metric before picking numbers** — the unit that scales with the value the buyer receives (seats, API calls, GB stored, resolved cases). Pricing on the wrong metric is the single hardest thing to fix later, because it requires migrating every existing customer's contract.
2. **Anchor to willingness-to-pay research, not cost-plus.** Run a Van Westendorp price-sensitivity survey or structured willingness-to-pay interviews with target-segment buyers before setting list price; cost-plus tells you the floor, not what the market will bear.
3. **Set 3 tiers, not 5+**, unless you have clear evidence of distinct buyer segments needing distinct feature sets. More tiers than segments creates decision paralysis and support overhead explaining the differences.
4. **Price the middle tier as the one you want most customers to choose** (the decoy-effect anchor), and make the top-tier ceiling high enough that it doesn't cap expansion revenue from your largest accounts.
5. **Build in at least 20-30% margin for discounting** before the number goes on a rate card — sales will negotiate, and a list price with no discount room forces either margin erosion or an uncomfortable "no" on reasonable asks.
6. **Grandfather existing customers explicitly when changing pricing**, and give 30-60 days notice minimum — a silent price change on renewal is the single fastest way to generate churn and public backlash.
7. **Instrument the value metric from day one**, even before charging for it, so a usage-based or outcome-based model has real historical data to price against instead of a guess.
8. **Revisit pricing at each major GTM inflection** — new segment, new competitor with a different model, or when expansion revenue stalls — rather than treating the original number as permanent.

## Anti-patterns

- **Copying a competitor's price sheet** without knowing their cost structure, funding runway, or which segment they're actually optimizing for — inherits their strategy without their context.
- **Pricing on a metric the buyer can't predict or control** (e.g., unpredictable usage spikes) — creates bill-shock, which drives churn even when the product delivers value.
- **Gating the core value proposition behind the top tier** — a buyer who can't experience the main benefit at an accessible price point never becomes an expansion candidate.
- **Changing pricing model and price simultaneously** — makes it impossible to tell which change caused a conversion or churn shift, and doubles the customer-communication burden.
- **Treating list price as fixed once set** — pricing is a hypothesis to test against conversion and expansion data, not a one-time decision to defend forever.

Cross-reference `positioning-and-messaging` for how price communicates value tier, `launch-planning` for sequencing a pricing change announcement, and `sales-enablement` for arming reps to defend price in a negotiation.
