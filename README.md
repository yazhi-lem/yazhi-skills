# yazhi-skills
Curated list of skills powering Yazhi

See [NEXT_ACTION.md](./NEXT_ACTION.md) for the roadmap, **October 2026 Pilot**, and **December 2026 Launch** deliverables.

Each skill lives at `skills/<category>/<skill-name>/SKILL.md` and follows a common contract: YAML frontmatter with a `name` (matching its directory) and a `description` starting with "Use when...", followed by a procedural, checklist-driven body. See [`skill-authoring`](skills/tools/skill-authoring/SKILL.md) for the contribution guide.

This is the portable [Agent Skills](https://code.claude.com/docs/en/skills) format, so the same files work in Claude Code, Claude Desktop, and any other tool that reads `SKILL.md`. See [Install](#install) for how to import them.

## Install

### Claude Code (plugin, recommended)

```
/plugin marketplace add yazhi-lem/yazhi-skills
/plugin install yazhi-skills@yazhi-skills
```

All 79 skills load namespaced as `yazhi-skills:<name>` — Claude picks them up automatically when relevant, or you invoke one directly with `/yazhi-skills:tamil-aksharas`. Update later with `/plugin marketplace update yazhi-skills`.

Non-interactively:

```bash
claude plugin marketplace add yazhi-lem/yazhi-skills
claude plugin install yazhi-skills@yazhi-skills
```

### Any tool that reads a skills directory

`install.sh` flattens the category tree into one directory of `<skill-name>/SKILL.md`, which is what Claude Desktop, `~/.claude/skills`, and most third-party agents expect:

```bash
git clone https://github.com/yazhi-lem/yazhi-skills.git
cd yazhi-skills

./install.sh                          # all skills -> ~/.claude/skills (symlinks)
./install.sh -c yazh-life -c tamil    # only those categories
./install.sh --project --mode copy    # vendor into ./.claude/skills of your project
./install.sh --dest ~/my-agent/skills --mode copy
./install.sh --list                   # see what's available
./install.sh --dry-run                # change nothing, print the plan
```

Symlinks (the default) mean `git pull` updates every installed skill; `--mode copy` vendors a fixed snapshot.

### Pre-packaged `.skill` bundles

A `.skill` file is a zip archive containing **exactly one `SKILL.md`, at its root** — the shape Claude accepts for an uploaded skill. Two are built into [`dist/`](dist) and committed, so they can be downloaded straight from GitHub without cloning:

| File | Contains | Use it for |
| --- | --- | --- |
| [`dist/yazhi-skills.skill`](dist/yazhi-skills.skill) | A generated router `SKILL.md` at the root, plus all 79 skills as reference files under `references/<category>/<name>.md` | Importing the whole collection as one skill |
| `dist/skills/<name>.skill` | One skill, its own `SKILL.md` at the archive root, and nothing else | Importing a single skill on its own |

The collection bundle's root `SKILL.md` is a router, not a copy: it carries a trigger line and bundled path per skill, and instructs the reader to open the matching file before acting. That keeps the index small while the full procedural detail stays in the 79 reference files.

Those 79 files are deliberately renamed away from `SKILL.md` on the way in. Shipping them at their repo paths would put 80 `SKILL.md` files in one archive, which is not a valid skill — the builder asserts the one-`SKILL.md` invariant, and CI re-checks it on every bundle.

Rebuild them after changing any skill:

```bash
python3 scripts/build_skill_bundle.py --per-skill   # rewrite dist/
python3 scripts/build_skill_bundle.py --check       # CI: fail if stale
```

Archives are byte-for-byte reproducible — fixed timestamps and sorted entries — so an unchanged skill produces an unchanged bundle and `--check` only fires on real drift.

### Programmatic use

[`skills.json`](skills.json) is a generated index of every skill — name, category, description, and repo-relative path — for tools that want to load or filter them without walking the tree:

```bash
jq -r '.skills[] | select(.category == "yazh-life") | .path' skills.json
```

Regenerate it (and the plugin manifest's skill paths) after adding a skill:

```bash
python3 scripts/build_index.py      # rewrite skills.json + .claude-plugin/plugin.json
python3 scripts/validate_skills.py  # check every SKILL.md against the repo contract
```

## Catalog (79 skills)

### Go-To-Market (gtm)

| Skill | Covers |
| --- | --- |
| [`positioning-and-messaging`](skills/gtm/positioning-and-messaging/SKILL.md) | Writing a positioning statement and messaging hierarchy before launch copy |
| [`pricing-strategy`](skills/gtm/pricing-strategy/SKILL.md) | Choosing a pricing model and metric, and setting/changing tiers |
| [`launch-planning`](skills/gtm/launch-planning/SKILL.md) | Tiering a launch and sequencing announcements across channels |
| [`sales-enablement`](skills/gtm/sales-enablement/SKILL.md) | Battlecards, objection handling, and certifying reps on a new pitch |
| [`channel-and-partnerships`](skills/gtm/channel-and-partnerships/SKILL.md) | Evaluating resellers, integrations, marketplaces, and co-marketing deals |

### Organization (org)

| Skill | Covers |
| --- | --- |
| [`yazhi-org-status`](skills/org/yazhi-org-status/SKILL.md) | Current status, vision, and next actions across all nine yazhi-lem repos |

### Repositories (repos)

One skill per yazhi-lem repository — its own layer map, workflow, next actions, and anti-patterns.

| Skill | Covers |
| --- | --- |
| [`yazhi-api-status`](skills/repos/yazhi-api-status/SKILL.md) | The central gRPC orchestrator: layer map, Pilot/Launch roadmap, known constraints |
| [`adhan-status`](skills/repos/adhan-status/SKILL.md) | The from-scratch Tamil SLM: JAX/Flax training phases, swaram tokenizer |
| [`open-sangam-status`](skills/repos/open-sangam-status/SKILL.md) | Sangam-era literature reader + agent assembly: corpus phases, translation pipeline |
| [`yazh-unity-status`](skills/repos/yazh-unity-status/SKILL.md) | The AR/XR Tamil pet app: endless-runner pivot, on-device inference, store blockers |
| [`illakiya-status`](skills/repos/illakiya-status/SKILL.md) | The Rust + Kotlin Tamil Android keyboard: layout, dictionary, sandhi engine |
| [`capitol-status`](skills/repos/capitol-status/SKILL.md) | The internal AI/ML ops console: recognizing UI scaffold vs. real backend |
| [`yazh-kutty-status`](skills/repos/yazh-kutty-status/SKILL.md) | The 30K-vocabulary kids' Tamil model: scoping an empty repository |
| [`yazhi-dev-status`](skills/repos/yazhi-dev-status/SKILL.md) | The yazhi.dev site and `/chat` demo: backend contract, design history |
| [`styleguide-status`](skills/repos/styleguide-status/SKILL.md) | The google/styleguide fork: when (not) to edit it |

### Forward-Deployed Engineering (fde)

| Skill | Covers |
| --- | --- |
| [`customer-discovery`](skills/fde/customer-discovery/SKILL.md) | Turning a vague customer ask into a scoped, buildable problem statement |
| [`poc-to-production`](skills/fde/poc-to-production/SKILL.md) | Hardening a proven POC to carry real production traffic and risk |
| [`deployment-runbook`](skills/fde/deployment-runbook/SKILL.md) | Repeatable pre-flight, rollback, and sign-off procedure for customer deployments |
| [`enterprise-integration`](skills/fde/enterprise-integration/SKILL.md) | Integrating with customer SSO, data pipelines, legacy APIs, and IT access processes |
| [`stakeholder-reporting`](skills/fde/stakeholder-reporting/SKILL.md) | Reporting cadence and format for technical and non-technical stakeholders |

### AI/ML (ai-ml)

| Skill | Covers |
| --- | --- |
| [`rag-pipeline-design`](skills/ai-ml/rag-pipeline-design/SKILL.md) | Designing chunking, embedding, retrieval, and reranking stages independently |
| [`llm-evaluation`](skills/ai-ml/llm-evaluation/SKILL.md) | Building eval sets and choosing statistically defensible evaluation methods |
| [`prompt-engineering`](skills/ai-ml/prompt-engineering/SKILL.md) | Structuring, versioning, and systematically iterating on prompts |
| [`fine-tuning-workflow`](skills/ai-ml/fine-tuning-workflow/SKILL.md) | Deciding whether to fine-tune and running data prep/training/regression checks |
| [`model-monitoring`](skills/ai-ml/model-monitoring/SKILL.md) | Production metrics, alerting thresholds, and feedback loops for LLM systems |

### Sovereign (sovereign)

| Skill | Covers |
| --- | --- |
| [`data-residency-compliance`](skills/sovereign/data-residency-compliance/SKILL.md) | Mapping data flows and producing an auditable residency posture |
| [`airgapped-llm-deployment`](skills/sovereign/airgapped-llm-deployment/SKILL.md) | Packaging models and serving inference in fully disconnected environments |
| [`open-model-selection`](skills/sovereign/open-model-selection/SKILL.md) | Evaluating open-weight models for license, provenance, and ops tradeoffs |
| [`sovereign-cloud-architecture`](skills/sovereign/sovereign-cloud-architecture/SKILL.md) | Multi-region isolation, local key control, and cloud exit strategy |

### Security (security)

| Skill | Covers |
| --- | --- |
| [`threat-modeling`](skills/security/threat-modeling/SKILL.md) | Enumerating and prioritizing threats before a system ships |
| [`secure-design-patterns`](skills/security/secure-design-patterns/SKILL.md) | Chokepoint auth, fail-safe defaults, and least privilege in code structure |
| [`llm-security-review`](skills/security/llm-security-review/SKILL.md) | Finding prompt injection, excessive agency, and unsafe tool/output handling |
| [`secure-code-review`](skills/security/secure-code-review/SKILL.md) | Catching injection, broken authz, and unsafe dependency changes pre-merge |
| [`pr-loophole-review`](skills/security/pr-loophole-review/SKILL.md) | Spotting a deliberately or carelessly introduced bypass hidden in one PR |
| [`codebase-vulnerability-audit`](skills/security/codebase-vulnerability-audit/SKILL.md) | Sweeping an entire existing codebase for dead auth checks and forgotten backdoors |
| [`environment-security-hardening`](skills/security/environment-security-hardening/SKILL.md) | Container, cloud/IaC, CI/CD, and network vulnerabilities outside the app code |
| [`security-posture-health-check`](skills/security/security-posture-health-check/SKILL.md) | A recurring scorecard for patching, access review, and logging coverage |
| [`secrets-management`](skills/security/secrets-management/SKILL.md) | Keeping credentials out of source control and scoped to least privilege |
| [`incident-response`](skills/security/incident-response/SKILL.md) | Classifying severity, containment, and blameless postmortems |

### Tamil (tamil)

| Skill | Covers |
| --- | --- |
| [`tamil-text-processing`](skills/tamil/tamil-text-processing/SKILL.md) | Handling Tamil strings at the grapheme-cluster level, not the code-unit level |
| [`tamil-transliteration`](skills/tamil/tamil-transliteration/SKILL.md) | Converting between Tamil script and Latin/"Tanglish" romanization |
| [`tamil-localization`](skills/tamil/tamil-localization/SKILL.md) | Adapting UI text, layout, fonts, and formatting for Tamil-speaking users |
| [`tamil-content-writing`](skills/tamil/tamil-content-writing/SKILL.md) | Writing natural, idiomatic Tamil copy instead of literal translation |
| [`tamil-swaram-vowels`](skills/tamil/tamil-swaram-vowels/SKILL.md) | The 12 vowels (swaram/உயிரெழுத்து): independent glyphs, dependent signs, and encoding order |
| [`tamil-aksharas`](skills/tamil/tamil-aksharas/SKILL.md) | The full 247-letter inventory: uyir, mei, uyirmei, aytham, Grantha, and numerals |
| [`tamil-numerals-symbols`](skills/tamil/tamil-numerals-symbols/SKILL.md) | Native numerals (௦–௲) and clerical symbols: when to use them and how they compose |
| [`tamil-legacy-encodings`](skills/tamil/tamil-legacy-encodings/SKILL.md) | Detecting and migrating TSCII/TAB/Bamini-era text to Unicode without corruption |
| [`tamil-input-methods`](skills/tamil/tamil-input-methods/SKILL.md) | Keyboard/IME design: Tamil99, phonetic input, auto-pulli, and backspace behavior |
| [`tamil-swaram-notation`](skills/tamil/tamil-swaram-notation/SKILL.md) | Encoding Carnatic swaram notation (ஸ ரி க ம ப த நி) as searchable Unicode text |
| [`tamil-morphology-nlp`](skills/tamil/tamil-morphology-nlp/SKILL.md) | Agglutinative morphology, sandhi, and lemma-level matching for NLP and search |

### Computer Use (computer-use)

| Skill | Covers |
| --- | --- |
| [`browser-automation`](skills/computer-use/browser-automation/SKILL.md) | Robust selectors, wait strategies, and verification for browser-driving agents |
| [`gui-agent-design`](skills/computer-use/gui-agent-design/SKILL.md) | Perceive-decide-act loop design, grounding, and guardrails for GUI control |
| [`desktop-workflow-automation`](skills/computer-use/desktop-workflow-automation/SKILL.md) | Automating multi-app desktop workflows so they're resumable after crashes |

### Tools (tools)

| Skill | Covers |
| --- | --- |
| [`mcp-server-development`](skills/tools/mcp-server-development/SKILL.md) | Designing MCP tools, resources, and prompts an LLM client calls reliably |
| [`cli-tool-design`](skills/tools/cli-tool-design/SKILL.md) | Flags, defaults, output modes, exit codes, and help text for CLIs |
| [`api-design`](skills/tools/api-design/SKILL.md) | Resource naming, versioning, pagination, and backward compatibility |
| [`skill-authoring`](skills/tools/skill-authoring/SKILL.md) | The frontmatter contract and quality bar for SKILL.md files in this repo |

### Yazh Life Skills (yazh-life)

Life skills pitched at a ~12-year-old — how to help one learn, decide, stay safe, and look after themselves. Written as guidance for the assistant doing the helping, not as material to read aloud to a kid.

| Skill | Covers |
| --- | --- |
| [`age-appropriate-explaining`](skills/yazh-life/age-appropriate-explaining/SKILL.md) | Pitching vocabulary, length, and analogies at a 12-year-old without dumbing down |
| [`homework-coaching`](skills/yazh-life/homework-coaching/SKILL.md) | The hint ladder: coaching to the answer instead of handing it over |
| [`study-and-memory`](skills/yazh-life/study-and-memory/SKILL.md) | Retrieval practice and spacing in place of re-reading and highlighting |
| [`time-and-planning`](skills/yazh-life/time-and-planning/SKILL.md) | A visible week, next-actions, and buffers before the deadline |
| [`speaking-and-presenting`](skills/yazh-life/speaking-and-presenting/SKILL.md) | Structure, rehearsal, and nerves for a class presentation |
| [`first-coding-steps`](skills/yazh-life/first-coding-steps/SKILL.md) | First projects, reading error messages, and debugging as a habit |
| [`science-projects`](skills/yazh-life/science-projects/SKILL.md) | Turning curiosity into a fair test with controls, repeats, and real safety rules |
| [`spotting-misinformation`](skills/yazh-life/spotting-misinformation/SKILL.md) | A 30-second source check, lateral reading, and why AI answers aren't sources |
| [`online-safety`](skills/yazh-life/online-safety/SKILL.md) | What never to share, grooming and scam patterns, cyberbullying, account setup |
| [`money-basics`](skills/yazh-life/money-basics/SKILL.md) | Save/spend/give split, trade-off arithmetic, and how free games monetise kids |
| [`feelings-and-friendship`](skills/yazh-life/feelings-and-friendship/SKILL.md) | Naming feelings, repair and apology scripts, and when to escalate to an adult |
| [`healthy-habits`](skills/yazh-life/healthy-habits/SKILL.md) | Concrete sleep, food, movement, and screen numbers for this age |
| [`kitchen-and-home-basics`](skills/yazh-life/kitchen-and-home-basics/SKILL.md) | A cooking and chores skill ladder with the hazard stated before the step |
| [`first-aid-and-emergencies`](skills/yazh-life/first-aid-and-emergencies/SKILL.md) | The short list a kid can execute under stress, and when to call for help |

### Social Media (social-media)

| Skill | Covers |
| --- | --- |
| [`social-content-master`](skills/social-media/social-content-master/SKILL.md) | Generating ready-to-publish posts, captions, and reel/short-form video scripts |
| [`tone-of-voice-application`](skills/social-media/tone-of-voice-application/SKILL.md) | Applying a brand's tone rules consistently and gracefully falling back to defaults |
| [`social-caption-writing`](skills/social-media/social-caption-writing/SKILL.md) | Drafting publish-ready social captions with platform-specific constraints |
| [`reel-script-generation`](skills/social-media/reel-script-generation/SKILL.md) | Scripting timestamped short-form videos with visual cues and on-screen text |
| [`content-repurposing`](skills/social-media/content-repurposing/SKILL.md) | Repurposing long-form assets into multiple platform-native social posts |
| [`hashtag-and-platform-strategy`](skills/social-media/hashtag-and-platform-strategy/SKILL.md) | Finalizing hashtags and posting notes for social media copy |
| [`content-quality-review`](skills/social-media/content-quality-review/SKILL.md) | Catching repetition, generic phrasing, and weak hooks before final output |
| [`tamil-social-content`](skills/social-media/tamil-social-content/SKILL.md) | Adapting social media content into idiomatic Tamil, avoiding literal translations |

## Contributing

1. Read [`skill-authoring`](skills/tools/skill-authoring/SKILL.md) — it is the contribution guide.
2. Add `skills/<category>/<skill-name>/SKILL.md`. The directory name and frontmatter `name` must match.
3. Add a row to the catalog above.
4. Run the full build and check:

```bash
python3 scripts/build_index.py
python3 scripts/build_skill_bundle.py --per-skill
python3 scripts/validate_skills.py
```

Commit the regenerated `skills.json`, `.claude-plugin/plugin.json`, and `dist/` alongside the skill itself — CI fails if any of them is stale.

New categories also need a title in `CATEGORY_TITLES` in [`scripts/lib_skills.py`](scripts/lib_skills.py).
