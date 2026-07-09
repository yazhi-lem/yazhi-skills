# yazhi-skills
Curated list of skills powering Yazhi

Each skill lives at `skills/<category>/<skill-name>/SKILL.md` and follows a common contract: YAML frontmatter with a `name` (matching its directory) and a `description` starting with "Use when...", followed by a procedural, checklist-driven body. See [`skill-authoring`](skills/tools/skill-authoring/SKILL.md) for the contribution guide.

## Catalog (30 skills)

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
| [`llm-security-review`](skills/security/llm-security-review/SKILL.md) | Finding prompt injection, excessive agency, and unsafe tool/output handling |
| [`secure-code-review`](skills/security/secure-code-review/SKILL.md) | Catching injection, broken authz, and unsafe dependency changes pre-merge |
| [`secrets-management`](skills/security/secrets-management/SKILL.md) | Keeping credentials out of source control and scoped to least privilege |
| [`incident-response`](skills/security/incident-response/SKILL.md) | Classifying severity, containment, and blameless postmortems |

### Tamil (tamil)

| Skill | Covers |
| --- | --- |
| [`tamil-text-processing`](skills/tamil/tamil-text-processing/SKILL.md) | Handling Tamil strings at the grapheme-cluster level, not the code-unit level |
| [`tamil-transliteration`](skills/tamil/tamil-transliteration/SKILL.md) | Converting between Tamil script and Latin/"Tanglish" romanization |
| [`tamil-localization`](skills/tamil/tamil-localization/SKILL.md) | Adapting UI text, layout, fonts, and formatting for Tamil-speaking users |
| [`tamil-content-writing`](skills/tamil/tamil-content-writing/SKILL.md) | Writing natural, idiomatic Tamil copy instead of literal translation |

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
