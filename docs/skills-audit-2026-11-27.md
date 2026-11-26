# Skills audit — 2026-11-27

Status: proposed · Owner: Vajra · Verified: 2026-11-27 against `main`
Scope: Hard review of all 99 skills, the catalog, validators, installer, and bundles.

> Update after `git fetch`: `origin/main` added `yazhi-code-frame`, `yazhi-code-implement`, and `yazhi-code-handoff` (commit `a121f72`); `origin/fix/yazhi-code-required-tables` added the tables their validator needed. Those were integrated, then the pipeline was extended with `yazhi-code-design`, `yazhi-code-deliver`, `yazhi-code-standards` (best practices distilled from Google engineering/style guides and public agent skills), and `design/visual-design`. It was then extended with five Pi-harness-aware support skills (`orient`, `debug`, `refactor`, `maintain`, `improve`). Then `yazhi-purpose` (purpose gate + three-axis review) and the evolving `indic/` side-collection were added, along with `collections/` maps. `styleguide-status` was then retired (rules in `google-style-adoption`, sync date in `yazhi-org-status`). The baseline below is the original 99-skill audit; the current catalog is 117 skills.

## Verdict

The repo is mechanically clean and semantically messy.

`validate_skills.py` reported **0 errors, 0 warnings** before this review, and every generated artifact was fresh. That result is misleading. The validator checks shape (frontmatter, table, three numbered steps, three anti-pattern bullets, README/index/manifest presence) but not truth, routing, or authority. The catalog is a flat list of 99 names in 13 categories with no task-first or audience-first entry point. Developers get a decent set; designers get fragments; "commons" gets fourteen skills aimed at a ~12-year-old and nothing for an ordinary adult user.

This is not a duplicate-files problem: **no two `SKILL.md` files are byte-identical**, and the longest shared 8-token passage between any two skills is 16 tokens (dated retirement boilerplate). The real problems are overlapping triggers, duplicated policy claims, stale facts, and several hundred lines of near-identical scaffolding that make 99 names feel like 99 choices when there are really about a dozen decisions.

Do not mass-delete skills. Narrow the triggers, name one owner per topic, and add a front door.

## Severity 1 — fixed in this pass

| Finding | Evidence | Fix |
|---|---|---|
| Test-naming convention contradicted itself | `tools/google-style-adoption` said `yazhi-api` uses `<module>_tests.py`; the repo's own `CONTEXT.md`/`README.md` say `<module>_test.py`. `styleguide-status` said the correct thing. `repos/adhan-status` claimed `test_*.py` is not collected, while adhan's `pyproject.toml` collects `*_tests.py`, `test_*.py`, and `*_test.py`. | Corrected both skills to name each repo's convention and removed the false "silent skip" claim. |
| Dead category reference | `org/yazhi-org-status` ended with "the `eco/` skills"; no `eco/` category exists (org was renamed). The validator missed it because it only checks `` `see`/`per` `` lines. | Changed to `org/`. |
| Fixed bug still taught as current | `tamil/tamil-purity-scoring` describes PR #130's Grantha fix, then lists "using the code's Grantha set without ஶ" as a live anti-pattern. | Replaced with a "do not compare pre-#130 numbers" anti-pattern. |
| Doc-header contracts disagreed | `tools/technical-documentation` requires `Status/Owner/Verified/Scope`; `org/org-doc-authoring` omitted `Scope` from every color's header. Both also duplicated owner/link/archive rules. | Aligned the color table with `Scope` and made `technical-documentation` the explicit owner of base headers, placement, and link checks. |
| Stale generated-file docstring | `scripts/build_skill_bundle.py` said the collection ships "51 skill bodies"; it ships 99. | Reworded to "every skill body". |
| Trigger narrowing, Phase 1 partial | Eight high-collision descriptions still invited the same sentence. | Narrowed `social-content-master`, `social-caption-writing`, `reel-script-generation`, `secure-code-review`, `technical-documentation`, `org-doc-authoring`, `yazhi-daily-rhythm`, and `yazhi-ops` with explicit "use X instead" boundaries. |

## Severity 1 — still open

### No audience front door

The README catalog is grouped by implementation category (`agentic`, `fde`, `gtm`, `repos`, …). A developer looking for "review this PR" has to read 13 category blurbs and guess between `org-impactful-pr`, `secure-code-review`, `pr-loophole-review`, `org-healthy-code`, and `codebase-vulnerability-audit`. A designer has no category at all; Tamil design guidance is scattered through `tamil-localization`, `tamil-content-writing`, `tamil-numerals-symbols`, and `tone-of-voice-application`. A non-technical adult has no route except fourteen child-focused life skills.

Added [`docs/choose-a-skill.md`](./choose-a-skill.md) as a task/audience front door. Next step: link it prominently from the README and `skills/README.md`, and add `audience`/`task` tags to `skills.json` so tools can filter without string-matching descriptions.

### Trigger collisions

These pairs/sets will fire on the same sentence. The bodies cross-reference each other well, but the model still has to pick one before it reads the references.

| Cluster | Colliding skills | Recommended boundary |
|---|---|---|
| Social batch vs. format | `social-content-master` vs. `social-caption-writing` / `reel-script-generation` / `content-repurposing` | Master only for multi-piece or long-form-to-many-platform requests; single-format requests go direct. |
| Security review | `secure-code-review`, `pr-loophole-review`, `codebase-vulnerability-audit`, `security-posture-health-check` | Diff → first; suspected bypass → second; legacy whole-codebase → third; recurring scorecard → fourth. Put this sentence in each description. |
| Docs | `org-doc-authoring` vs. `technical-documentation` | Color/promotion vs. file contract. Now explicit in both bodies; still needs description-level separation. |
| Status | `yazhi-org-status` vs. six `repos/*-status` | Ecosystem map vs. in-repo work. Read one status skill, never all seven. |
| Tamil writing | `tamil-content-writing`, `tamil-tani-tamil`, `tamil-technical-terms`, `tamil-social-content` | Natural copy / purity register / glossary decision / social adaptation. |
| Tamil script reference | `tamil-aksharas`, `tamil-swaram-vowels`, `tamil-text-processing`, `tamil-transliteration` | Inventory vs. vowels vs. string operations vs. romanization. |
| Operating rhythm | `yazhi-daily-rhythm` vs. `yazhi-ops` | Detailed day vs. cadence/escalation. Their bodies are the closest pair in the repo (cosine ≈0.88 on body terms). |
| Kid learning | `age-appropriate-explaining` vs. the other 13 `yazh-life` skills | Only 6 of 13 siblings reference the base calibration skill; the rest re-derive "pitch it at a 12-year-old". Make it a one-line cross-reference everywhere. |
| Deployment/incident | `org-release`, `deployment-runbook`, `fde-support-escalation`, `incident-response` | Internal release / customer deployment / customer support / security compromise. |

## Severity 2 — consistency debt

1. **Word budget is not enforced.** `skill-authoring` says 400–700 words; `technical-documentation` says skills are 700 words; the validator allows 350–850. **25 of 99 skills exceed 700 words** (max 848: `pr-loophole-review`). A warning was added to the validator, but CI runs non-strict, so it does not fail. Either trim those 25 or make 850 the written contract.
2. **Status claims are dated but not owned consistently.** `yazhi-org-status` has a `verified 2026-11-21` snapshot; `adhan-status`, `illakiya-status`, and `open-sangam-status` have dates; `styleguide-status` says "as of this writing" with only an undated "last synced 2025-11-13"; `yazhi-dev-status` has mixed dates. There is no machine-checkable `Status/Owner/Verified` rule for skills themselves.
3. **Body structure is not uniform.** 90 skills use an `Anti-patterns` / `Common failure modes` heading, but social-media skills use `Step N — …` headings instead of `Workflow`, and the `repos/` skills have an extra `Next actions` section. That is acceptable variation in principle, but it is undocumented, so contributors copy whichever sample they saw last.
4. **The validator's anti-pattern check is textual, not semantic.** Three bullets of any content pass; a heading that mentions "failure mode" in prose can satisfy it. Cross-reference checks only fire on lines containing "see" or "per" and in backticks — which is why `eco/` survived until a human read the last line.
5. **The contract forbids metadata that would help discovery.** Frontmatter is deliberately two keys for portability. Good. But that means `skills.json` carries only `name/category/description/path`; there is no `audience`, `task`, `requires`, or `supersedes` field, and no way for tools to filter by role. Add metadata in a generated catalog, not in `SKILL.md`.
6. **Generated delivery creates the appearance of duplication.** `dist/` holds one collection bundle plus **99 per-skill `.skill` archives** (400 KB total; repo 6.7 MB). They are reproducible and CI-checked, so they are not a correctness problem, but they double the number of "things" users see. Document one primary install path per host and mark `dist/` clearly as generated (the README mostly does; `skills/README.md` does not).

## Severity 2 — gaps

- **Designers are underserved.** No skill covers visual hierarchy, color/contrast, typography selection, component states, or accessibility review. `tamil-localization` covers glyph/layout failure modes but not design process. Add 2–3 design-owned skills only after an owner is named; otherwise this becomes another pile of generic essays.
- **"Commons" is underserved.** The 14 `yazh-life` skills are all pitched at a ~12-year-old. There is no plain-language, adult-facing skill for everyday computer/AI questions, privacy basics, or "is this tool safe to use" outside `spotting-misinformation` and `online-safety`.
- **Private/local Yazhi work is partly invisible.** `yazhi-org-status` mentions `yazhi-api` and `capitol` as private with no skills, while the workspace also has `circle`, `yazhi-auth`, and local ops. The six `repos/*-status` skills cover only the public set. Decide deliberately: either add local/private status skills with no code details, or state that boundary in the README.
- **Status skills duplicate repo docs.** Each `*status` skill contains a phase table and "next actions" that can only age. Keep the stable workflow/traps in the skill; move the phase table behind a dated pointer to the repo's `docs/README.md`.

## Target structure

```text
Front door        docs/choose-a-skill.md + one router description in the collection bundle
    ↓
Owners            one canonical skill per topic (docs, security review, social, status, Tamil text)
    ↓
Specialists       narrow triggers, explicit "not when X, use Y" boundary in every description
    ↓
Generated         skills.json / plugin manifest / dist bundles / README catalog from one source
```

Proposed consolidation (do not do all at once):

1. **Phase 1 — narrow descriptions (no files deleted).** Done for 4 of the 9 clusters (social batch/format, security diff, docs, operating rhythm). Remaining: status, Tamil writing, Tamil reference, kid learning, deployment/incident.
2. **Phase 2 — retire or fold 4–6 low-value skills.** Candidates: `styleguide-status` (stable rule already in `google-style-adoption`, sync date already in `yazhi-org-status`); merge `yazhi-daily-rhythm` into a single `yazhi-ops` runbook section; merge `tamil-swaram-vowels` into `tamil-aksharas` as a vowel reference section; fold `content-quality-review` into the social batch checklist only if the batch orchestrator starts enforcing it. Each retirement needs a redirect row in the catalog.
3. **Phase 3 — audience/task metadata.** Add `catalog/meta.json` (or a mapping in `scripts/build_index.py`) with `audience: [yazhi, developer, designer, commons]` and `task:` tags; emit them into `skills.json` only. Keep `SKILL.md` frontmatter at two keys.
4. **Phase 4 — validator hardening.** Warn on a backticked path that names no category/repo/dir; require a dated `Verified:` for any skill containing a phase/version/blocker table; make `--strict` the CI gate only after the 25 long skills and all dead refs are cleaned up.

## Acceptance criteria for "done"

- `python3 scripts/validate_skills.py --strict` passes with 0 warnings.
- Every description has one trigger, one outcome, and one boundary ("use X instead when …").
- No skill carries a status snapshot without `verified YYYY-MM-DD` and a named owner doc.
- `docs/choose-a-skill.md` is linked from both READMEs and covers all four audiences.
- Every retired skill has a documented replacement; no dead category/reference remains.
- One owner is named for design and one for commons before new skills are added in those areas.
