# Choose a skill

Status: current · Owner: Vajra · Verified: 2026-11-27
Scope: A task-first front door for the 117 skills in this repo.

The full catalog is ordered by category. This page is ordered by **who is asking** and **what they are trying to do**. Pick one primary skill; follow its cross-references only when it names another skill. If two skills seem to fit, the narrower trigger wins.

## Yazhi maintainers and operators

| Task | Start here | Then, only if needed |
|---|---|---|
| Orient in the ecosystem | [`yazhi-org-status`](../skills/org/yazhi-org-status/SKILL.md) | The matching `repos/*-status` skill |
| Decide values, privacy, publication chamber | [`org-ethos`](../skills/org/org-ethos/SKILL.md) | `org-service-boundaries` |
| Run the day / week / month / quarter | [`yazhi-daily-rhythm`](../skills/org/yazhi-daily-rhythm/SKILL.md) or [`yazhi-ops`](../skills/org/yazhi-ops/SKILL.md) | `org-plan-reset-recovery` when old plans resurface |
| Write or retire a doc | [`technical-documentation`](../skills/tools/technical-documentation/SKILL.md) | [`org-doc-authoring`](../skills/org/org-doc-authoring/SKILL.md) for the green/blue/orange decision |
| Open or review a PR | [`org-impactful-pr`](../skills/org/org-impactful-pr/SKILL.md) | `org-healthy-code`, `secure-code-review` |
| Ship a release | [`org-release`](../skills/org/org-release/SKILL.md) | `deployment-runbook` for customer sites |
| Clean up stale docs/tasks/issues | [`org-repo-audit`](../skills/org/org-repo-audit/SKILL.md) (files) or [`org-issue-triage`](../skills/org/org-issue-triage/SKILL.md) (issues/PRs) | `org-plan-reset-recovery` for authority |
| Change something across repos | [`org-cross-repo-change`](../skills/org/org-cross-repo-change/SKILL.md) | `org-service-boundaries` for ownership |

Rules of thumb: `yazhi-org-status` is a dated map, not the source of truth — each repo's `README.md` / `docs/README.md` is. `repos/*-status` skills are for working *inside* that repo; do not load all six.

## Developers

| Task | Start here | Boundary |
|---|---|---|
| Design an API, CLI, or MCP surface | [`api-design`](../skills/tools/api-design/SKILL.md), [`cli-tool-design`](../skills/tools/cli-tool-design/SKILL.md), [`mcp-server-development`](../skills/tools/mcp-server-development/SKILL.md) | One interface at a time |
| Review a normal PR diff | [`secure-code-review`](../skills/security/secure-code-review/SKILL.md) | Use `pr-loophole-review` only when a control looks bypassed; `codebase-vulnerability-audit` is for whole-codebase sweeps |
| Design a trust boundary | [`threat-modeling`](../skills/security/threat-modeling/SKILL.md) | `secure-design-patterns` for the code shape; `llm-security-review` for LLM/agent features |
| Build an unattended agent | [`agentic-reliability`](../skills/agentic/agentic-reliability/SKILL.md) + [`agentic-security`](../skills/agentic/agentic-security/SKILL.md) | `gui-agent-design` only for screenshot/coordinate control |
| Build LLM features | [`prompt-engineering`](../skills/ai-ml/prompt-engineering/SKILL.md), [`rag-pipeline-design`](../skills/ai-ml/rag-pipeline-design/SKILL.md), [`llm-evaluation`](../skills/ai-ml/llm-evaluation/SKILL.md), [`model-monitoring`](../skills/ai-ml/model-monitoring/SKILL.md) | Pick the stage you are in; `fine-tuning-workflow` is for training decisions |
| Handle Tamil strings or input | [`tamil-text-processing`](../skills/tamil/tamil-text-processing/SKILL.md) for code; [`tamil-input-methods`](../skills/tamil/tamil-input-methods/SKILL.md) for keyboards; [`tamil-morphology-nlp`](../skills/tamil/tamil-morphology-nlp/SKILL.md) for search/NLP | `tamil-aksharas` / `tamil-swaram-vowels` are reference inventories, not workflows |
| Deploy to a customer | [`poc-to-production`](../skills/fde/poc-to-production/SKILL.md) → [`deployment-runbook`](../skills/fde/deployment-runbook/SKILL.md) | `fde-support-escalation` / `incident-response` after go-live |
| Work in a specific repo | `adhan-status`, `illakiya-status`, `open-sangam-status`, `yazhi-dev-status`, `yazh-unity-status` | Read that repo's docs first |

## Designers and content people

There is no dedicated visual-design skill yet — the nearest reliable guidance is split across these:

| Task | Start here | Notes |
|---|---|---|
| Tamil UI copy, fonts, layout, dates/numbers | [`tamil-localization`](../skills/tamil/tamil-localization/SKILL.md) | Font shaping and layout breakage live here |
| Natural Tamil copy / register | [`tamil-content-writing`](../skills/tamil/tamil-content-writing/SKILL.md), [`tamil-tani-tamil`](../skills/tamil/tamil-tani-tamil/SKILL.md), [`tamil-technical-terms`](../skills/tamil/tamil-technical-terms/SKILL.md) | One writing decision per string; do not load all three |
| Brand voice | [`tone-of-voice-application`](../skills/social-media/tone-of-voice-application/SKILL.md) + [`../brand-voice-reference.md`](../brand-voice-reference.md) | The reference overrides the skill's default voice |
| Social assets | [`social-content-master`](../skills/social-media/social-content-master/SKILL.md) only for multi-piece batches | Single caption → `social-caption-writing`; single reel → `reel-script-generation`; Tamil → `tamil-social-content` |
| Kid-facing UI/copy | [`age-appropriate-explaining`](../skills/yazh-life/age-appropriate-explaining/SKILL.md) | Safety escalation rules stay in `online-safety` / `first-aid-and-emergencies` |

## Commons / learners / families

The `yazh-life` skills are written as guidance for the assistant helping a ~12-year-old, not as text to read aloud. Start with [`age-appropriate-explaining`](../skills/yazh-life/age-appropriate-explaining/SKILL.md) for tone, then pick the topic: homework, study, planning, speaking, first coding, science projects, money, feelings, habits, kitchen/home, online safety, misinformation, or emergencies. Emergency and abuse/safety questions override the normal teaching flow and escalate to a trusted adult immediately.

## Yazhi Code pipeline — idea to client

Use one stage at a time; each stage hands a short artifact to the next. Do not jump straight from frame to code when the change touches a UI, a shared contract, or a client environment.

| Stage | Skill | Output |
|---|---|---|
| 1. Frame | [`yazhi-code-frame`](../skills/yazhi-code/yazhi-code-frame/SKILL.md) | Outcome, out-of-scope, main risk |
| 2. Design | [`yazhi-code-design`](../skills/yazhi-code/yazhi-code-design/SKILL.md) | Boundary, interface, data flow, proof |
| 3. Implement | [`yazhi-code-implement`](../skills/yazhi-code/yazhi-code-implement/SKILL.md) | Small runnable slices |
| 4. Handoff | [`yazhi-code-handoff`](../skills/yazhi-code/yazhi-code-handoff/SKILL.md) | Cold-read diff, named checks, honest PR |
| 5. Deliver | [`yazhi-code-deliver`](../skills/yazhi-code/yazhi-code-deliver/SKILL.md) | Client-environment proof, rollback, feedback loop |

Stages 3 and 4 both consult [`yazhi-code-standards`](../skills/yazhi-code/yazhi-code-standards/SKILL.md) — the shared Google-leaning code/write/review/push checklist. Harness-specific patterns live in [`pi-harness-lessons.md`](./pi-harness-lessons.md). For visual decisions inside stage 2, use [`visual-design`](../skills/design/visual-design/SKILL.md); for Tamil glyph/layout details use `tamil-localization`.

## Yazhi Code support loop

The core pipeline handles a change from idea to client. These five skills handle the work around it in any Yazhi repo, and each can open a new frame rather than expanding the current one.

| Situation | Skill | What it produces |
|---|---|---|
| New repo or unfamiliar task | [`yazhi-code-orient`](../skills/yazhi-code/yazhi-code-orient/SKILL.md) | Read-only map: truth source, gates, boundary, risks |
| Build/test/runtime failure with unknown cause | [`yazhi-code-debug`](../skills/yazhi-code/yazhi-code-debug/SKILL.md) | Repro, root cause, regression check, recovery note |
| Structure change, behavior must stay the same | [`yazhi-code-refactor`](../skills/yazhi-code/yazhi-code-refactor/SKILL.md) | Characterization checks and small mechanical steps |
| Routine repo health between features | [`yazhi-code-maintain`](../skills/yazhi-code/yazhi-code-maintain/SKILL.md) | Dated health note with exactly one next improvement |
| Repeated friction worth automating | [`yazhi-code-improve`](../skills/yazhi-code/yazhi-code-improve/SKILL.md) | Small owned artifact with baseline and adoption path |

## Indic and multilingual work

The [`indic/` collection](../collections/indic.md) sits beside Tamil: [`indic-script-fundamentals`](../skills/indic/indic-script-fundamentals/SKILL.md) for cross-script text, [`indic-transliteration`](../skills/indic/indic-transliteration/SKILL.md) for romanization, [`indic-multilingual-content`](../skills/indic/indic-multilingual-content/SKILL.md) for copy, [`indic-localization`](../skills/indic/indic-localization/SKILL.md) for UI surfaces, and [`indic-cultural-context`](../skills/indic/indic-cultural-context/SKILL.md) for the living cultural register. Tamil-specific work stays in `tamil/`.

## Yazhi purpose and review

| Need | Skill | Boundary |
|---|---|---|
| Decide if a feature fits Yazhi before building it | [`yazhi-purpose-gate`](../skills/yazhi-purpose/yazhi-purpose-gate/SKILL.md) | Feature-fit gate; values themselves stay in `org-ethos` |
| One verdict before merge or release | [`yazhi-review`](../skills/yazhi-purpose/yazhi-review/SKILL.md) | Routes to security/code/language owners instead of duplicating their checks |

In Pi, the [Yazhi extension](../extensions/yazhi/README.md) adds `/yazhi-start`, `/yazhi-purpose`, and `/yazhi-review` to queue these skills.

## Collision rules

- **Social media:** `social-content-master` is the batch orchestrator. For one post or one script, use the format-specific skill directly.
- **Security:** `secure-code-review` for any PR diff; `pr-loophole-review` for a suspected bypass; `codebase-vulnerability-audit` for legacy code; `security-posture-health-check` for recurring scorecards.
- **Docs:** `technical-documentation` owns headers, placement, size, and archives; `org-doc-authoring` owns only green/blue/orange and promotion.
- **Status:** one repo status skill at a time, always subordinated to that repo's current docs.
- **Tamil:** reference inventories (`tamil-aksharas`, `tamil-swaram-vowels`, `tamil-numerals-symbols`) answer "what glyphs exist"; processing/writing skills answer "what should I do with them".

See [`skills-audit-2026-11-27.md`](./skills-audit-2026-11-27.md) for why these boundaries exist and what is still being consolidated.
