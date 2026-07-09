---
name: customer-discovery
description: Use when starting an engagement with a new enterprise customer and you need to turn vague asks ("we want AI in our workflow") into a scoped, buildable problem statement before writing code. Helps you run a tight discovery process that surfaces real requirements, technical constraints, and the actual decision-makers, instead of building the wrong thing fast.
---

Forward-deployed engineers get pulled into a customer's environment before the problem is fully defined, often with a sales-driven narrative that doesn't match what the ground-floor users actually need. Skipping or rushing discovery is the single biggest predictor of a `poc-to-production` failure later, because rework at that stage costs 10x what it costs here. Discovery is not a courtesy meeting — it's risk reduction under a deadline.

## Workflow

1. **Timebox it.** Default to 3 days for a single-team engagement, up to 5 for multi-department rollouts. Longer discovery without a working prototype starts to look like stalling to the customer — commit to a date for a findings readout before you start.
2. **Separate stated wants from real needs.** Ask "what do you do today when this fails?" and "walk me through the last time this went wrong" instead of "what features do you want?" Stated wants are usually a competitor's feature list; real needs come from watching a workflow break.
3. **Map the stakeholders before the first meeting.** You need the economic buyer (signs off on budget), the technical approver (security/IT, can block deployment), and the daily user (will make or break adoption). If you only meet one of these in week one, treat that as a red flag, not a convenience.
4. **Inventory technical constraints early.** Data residency, auth system (SSO/SAML provider), network egress rules, existing data pipeline format, and approved deployment surface (VPC, on-prem, air-gapped). These determine architecture more than any feature request — see `enterprise-integration` for how to negotiate access once you know what's needed.
5. **Run a working-session, not a requirements interview.** Bring a whiteboard or shared doc and co-build a rough data flow diagram live with the customer. People correct a wrong diagram far more readily than they answer an abstract question.
6. **Write a one-page problem statement and get explicit sign-off.** Include: the workflow being changed, success metric, out-of-scope items, and constraints. Circulate to all three stakeholder types above and get a reply, not just silence, before scoping the POC.
7. **Convert findings into a POC plan** and hand off to `poc-to-production` scoping — discovery output should map directly onto the POC's acceptance criteria.

## Stakeholder elicitation matrix

| Stakeholder type | What they'll tell you | What to actually listen for | Common failure if skipped |
|---|---|---|---|
| Economic buyer | Business outcome, budget, timeline pressure | Real deadline vs. negotiable deadline | Scope creep with no one able to say no |
| Technical approver (IT/Security) | Compliance requirements, approved vendors | Hard blockers vs. preferences | POC works, prod deployment blocked for months |
| Daily user | Feature requests, pain points | The manual workaround they already use | Built system nobody adopts |
| Data owner | Data format, access policy | Undocumented data quality issues | Integration breaks on real data in week 2 |
| Integration/ops team | System landscape, uptime requirements | Existing incident patterns | Runbook gaps discovered during `deployment-runbook` |

## Anti-patterns

- **Discovery-by-deck.** Running discovery entirely through a slide presentation from the customer's champion, with no direct access to end users. You get the pitch, not the problem — insist on at least one session with actual users.
- **Unbounded discovery.** Letting discovery run past its timebox "to be thorough." It never converges on its own; more time produces more requirements, not more clarity. Force a decision point.
- **Skipping the technical approver.** Building a slick POC that the customer's security team rejects outright because it violates a constraint nobody mentioned. Get IT/security in the room in week one, not week four.
- **Treating the kickoff deck as the requirements doc.** Sales materials describe the aspiration, not the constraint set. Always re-derive requirements from direct observation.
- **No written sign-off.** Verbal alignment in a meeting evaporates the moment scope gets contested later. A one-page problem statement with a reply-confirmed sign-off is cheap insurance — use it to anchor `stakeholder-reporting` expectations from day one.
