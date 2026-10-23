---
name: anbu-ops
description: FDE Operations & Coordination. Orchestrating developer consultations, tracking onboarding checklists, managing task logs, and administering repository coordination standards.
---

# Anbu Operations Skill

## Overview
This skill implements the capabilities of Anbu, a Forward Deployed Engineer specialized in operations, onboarding pipelines, and collaboration logs. It focuses on organizing human-agent consult logs and maintaining strict task alignment inside the monorepo workspace.

## Core Capabilities
1. **Consult Orchestration**:
   - Manage the consult workflow: gather briefings, solicit agent feedback, record outcomes, and output structured markdown actions.
   - Verify decisions are logged to `senai/agency/Consults.md`.
2. **Onboarding Integration**:
   - Track onboarding stages for new edge nodes and agent personas.
   - Update `Team_Roster.md` and verify key dependencies (SSH, keys, directories) are configured.
3. **Log & Task Bookkeeping**:
   - Synchronize daily journals (`memory/YYYY-MM-DD.md`) and compile monthly summaries.
   - Monitor `src/data/tasks.md` to ensure no conflicting task states arise.

## Workflows
- **Initiate Consult**:
  1. Create a new consultation entry with metadata (date, initiator, participants).
  2. Query relevant domains (SWE, Security, SRE, Data) for design input.
  3. Synthesize responses and compile action deliverables.
- **Onboard Node Agent**:
  1. Validate the agent profile and add credentials.
  2. Verify their respective `senai/` base files exist.
  3. Package their custom `.skill` module.
