# Next Actions: yazhi-skills (Q4 2026)

> This file mirrors the Yazhi Q4 2026 launch plan as of **8 Oct 2026**.

## Where this repo sits in the Q4 plan

- **No Q4 2026 milestone or dated item** targets yazhi-skills. The repo is mapped to **Yazhi Academy** and **Yazhi Media**
  (Federal **Circle**) as "skills and learning content (@yazhi.skills)".
- The closest link is the **FDE Foundry** (Yazhi Academy's Forward Deployed Engineering apprenticeship). The `skills/fde/` set
  (customer-discovery, poc-to-production, deployment-runbook, enterprise-integration, stakeholder-reporting) matches that
  curriculum's subject, but whether these skills are part of the cohort-2 curriculum is **unclear**.
- The previous version of this file set an **October "pilot"** (core skill validation, CI bundling, plugin packaging) and a
  **December "public launch"** (community skill marketplace; Nyayam / Kanaku / Sevai domain skills). Neither date is part of
  the Q4 plan, so they are listed below as undated backlog.

## Academy dates this repo could support

| Date | Academy milestone |
|---|---|
| 20 Nov 2026 | Cohort-2 selection rubric and intake size |
| 25 Nov 2026 | Programme page (structure only) and cohort-1 capstone showcase |
| **1 Dec 2026** | Cohort-2 applications open |

## Undated backlog

- Validate core skills and keep the index and bundles rebuilt in CI (`scripts/build_index.py`, `scripts/validate_skills.py`).
- Plugin packaging (Claude Code / Hermes / OpenCode).
- Community skill registry and domain skills (Nyayam, Kanaku, Sevai). These need a planned, dated item before they are scheduled.
- Review open PR [#9](https://github.com/yazhi-lem/yazhi-skills/pull/9) (skill-verification-testing, from 19 Sep).

## Possible next step

If the FDE skills become part of the cohort-2 curriculum, map `skills/fde/` to the FDE Foundry curriculum weeks so this repo
has a dated reason to change.
