# Founder Refresher & Next Actions — yazhi-skills

> **Milestone Expectations:**
> - 🎯 **October 2026:** Pilot Release — Complete Core Agent Skills Catalog for Sangam Literature, Data Scraping & API Automation
> - 🚀 **December 2026:** Public Launch — Open Skill Marketplace & Distributed Execution Engine for Community-contributed Tamil AI Skills

---

## 1. Executive Summary & Philosophy

`yazhi-skills` maintains the standardized catalog of procedural skills powering autonomous agents across Yazhi. Built upon the portable Agent Skills format, skills define actionable, verified checklists for LLM tool use.

---

## 2. October 2026 Pilot Scope

- [ ] **Core Skillset Validation:**
  - Standardize and test core skills: `skill-authoring`, `sangam-transcription`, `adhan-corpus-curation`, `yazhi-api-client`.
- [ ] **Build & Bundle Automation:**
  - Automated validation (`scripts/validate_skills.py`), bundle generation, and index synchronization in CI.
- [ ] **Plugin Packaging:**
  - Seamless Claude Code / Hermes / OpenCode plugin distribution setup.

---

## 3. December 2026 Launch Scope

- [ ] **Community Skill Registry:**
  - Public skill marketplace with automated quality scoring and sandboxed test execution.
- [ ] **Multilingual & Domain Skills:**
  - Specialized skills for Tamil governance (Nyayam), educational math (Kanaku), and administrative services (Sevai).

---

## 4. Immediate Next Actions

1. Run skill build scripts (`python3 scripts/build_index.py && python3 scripts/validate_skills.py`).
2. Verify YAML frontmatter syntax and trigger descriptions across all category skill files.
3. Clean up deprecated or prototype skill definitions.
