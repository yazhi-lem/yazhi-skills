---
name: anbu-ops
description: Use when running a consultation across FDE personas, onboarding a new node or agent into the monorepo, or reconciling task state that has drifted between journals and trackers. Helps you keep one authoritative record of decisions and a clean onboarding checklist instead of knowledge scattered across chat logs and half-updated task files.
---

Anbu is the operations layer for a workspace staffed by multiple agents and personas. The failure that costs real time: the same decision recorded three ways, none of them the one a new contributor reads. One authoritative log beats three optimistic ones.

## Workflow

1. **Open the consult with metadata.** Date, initiator, participating domains (SWE, Security, SRE, Data), and the decision to be made. A consult without a single question becomes a meeting.
2. **Ask each domain one scoped question.** Send the same brief with a domain-specific ask; unspecific broadcasts return overlapping answers you then have to reconcile.
3. **Record the outcome once** in `senai/agency/Consults.md` — decision, rationale, owner, date. Chat threads are not the system of record.
4. **Convert outcomes into actions** with an owner and a due date; an action with no owner is a wish.
5. **Onboard a node or agent against a checklist**, not from memory: credentials provisioned, base files present, skill module packaged, first health check green.
6. **Reconcile task state weekly.** Diff `src/data/tasks.md` against journal entries (`memory/YYYY-MM-DD.md`) and fix drift in the tracker, not the journal.
7. **Summarise monthly** into a single page: shipped, slipped, blocked, decided.

## Onboarding checklist

| Step | Artifact | Pass condition |
|---|---|---|
| Profile validated | `Team_Roster.md` | Role and domain stated |
| Credentials | SSH key / token store | Key works, token scoped |
| Base files | `senai/` tree | All referenced files resolve |
| Skill packaged | `dist/skills/<name>.skill` | One root `SKILL.md` |
| First health check | Node service port | Responds within 5s |

## Defaults

- Consult cadence: weekly per domain, ad hoc for launch-critical decisions.
- Every decision gets an owner and a date; review unreviewed actions after 7 days.
- One journal entry per working day, summarized monthly — not per task.

## Anti-patterns

- **Decisions living only in chat.** They vanish from the record and get re-litigated; write them to `Consults.md`.
- **Broadcasting a vague consult to every persona.** You get overlapping answers and spend more time reconciling than deciding.
- **Journals and task tracker both treated as source of truth.** They drift within a week; pick the tracker and summarise the journal.
- **Onboarding from memory.** Missing a credential step surfaces days later as an unexplained auth failure.
- **Actions without owners.** Unowned work silently expires.

For the standing task list see `yazhi-org-status`, for deploy steps see `deployment-runbook`, and for the capability bar new personas need see `skill-authoring`.
