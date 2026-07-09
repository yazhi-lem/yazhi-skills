---
name: llm-security-review
description: Use when reviewing or designing an LLM-powered feature — a chatbot, RAG pipeline, or agent with tool access — before it ships or gains new capabilities. Helps you find prompt injection, excessive agency, and unsafe tool/output handling that traditional code review misses.
---

LLM-powered systems introduce a threat class that standard code review is not built to catch: the model itself is an untrusted interpreter of attacker-controlled text. Treat every piece of text the model reads — user input, retrieved documents, tool outputs, web content — as potentially adversarial, because it can be. This review should happen before a new tool, data source, or autonomy level is granted, not after.

## Workflow

1. **Map the trust boundary between text and instructions.** Identify every place external content (user messages, RAG chunks, API/tool responses, scraped web pages) enters the model's context. Anywhere this happens is a prompt injection surface.
2. **Enumerate tool/agent permissions.** List every tool the model can call and what each tool can do to the outside world (read data, send data, spend money, modify state, execute code). Assign each a blast-radius rating.
3. **Check for excessive agency.** Does the model have write/delete/send access it doesn't need for its task? Can it chain tools to escalate (e.g. read secrets, then send them via an email tool)? Cut any capability not required for the stated use case.
4. **Test injection resistance.** Feed adversarial content through every entry point from step 1 (e.g. "ignore previous instructions and...", hidden text in a fetched webpage, malicious metadata in a retrieved document). Confirm the system prompt's instructions still hold and sensitive tools aren't triggered.
5. **Review output handling.** Is the model's output ever rendered as HTML, executed as code, used to construct a SQL query, or passed unsanitized into another tool call? Treat model output as untrusted user input on the way out, symmetric to treating input as untrusted on the way in.
6. **Check data exfiltration paths.** Can the model be tricked into embedding secrets, PII, or internal data into a response, a tool call argument (e.g. a URL fetched by an image-render tool), or a log line an attacker can read?
7. **Verify jailbreak/guardrail coverage.** Confirm safety instructions are enforced outside the model too (allowlists, output filters, policy checks) — never rely on the system prompt alone, since it can be overridden or leaked.
8. **Score and gate.** Use the table below; anything Critical/High blocks ship until mitigated.

## Risk categories

| Category | Example | Typical mitigation |
|---|---|---|
| Prompt injection | Malicious instructions hidden in a retrieved doc or webpage | Segregate instructions from data, treat retrieved content as data-only, instruction-hierarchy-aware models |
| Jailbreak | User crafts input to bypass system prompt policy | Defense in depth: output filters, policy classifiers, not just prompt wording |
| Excessive agency | Agent has delete/send/spend access beyond task need | Least-privilege tool scoping, human approval for high-impact actions |
| Insecure output handling | Model output rendered as HTML/executed/used in SQL unescaped | Sanitize/encode model output same as any untrusted input |
| Data exfiltration via tools | Model embeds secrets in a URL fetched by a tool | Egress allowlists, strip secrets from context, monitor tool call arguments |
| Unbounded resource use | Agent loops calling expensive tools/APIs | Rate limits, step budgets, cost caps per session |

## Numeric defaults

- Cap agent tool-call loops at a fixed step budget (e.g. 15-25 steps) with hard termination.
- Require human approval for any tool action rated "irreversible" or above a cost threshold (e.g. >$50 spend, any delete/send-external action).
- Log and retain full tool-call traces for at least 90 days for post-incident analysis.
- Re-run this review whenever a new tool is added or a model/provider changes, not just annually.

## Anti-patterns

- **Trusting the system prompt as a security boundary.** It's a strong suggestion to the model, not an access control; enforce restrictions outside the model too.
- **Granting broad tool scopes "to be safe for future use."** Unused permissions are pure attack surface; scope tools to exactly what the current task needs.
- **Sanitizing input but not output.** Model output rendered downstream is just as dangerous as unsanitized user input.
- **Testing only with polite adversarial prompts.** Real attackers use obfuscation, encoding, multi-turn setup, and content hidden in tool results — test those too.
- **Skipping review because "it's just a chatbot."** Any model with RAG or tool access has a real blast radius even without obvious "agent" framing.

Findings about the surrounding trust boundaries belong in `threat-modeling`. Non-LLM code paths (API handlers, auth checks) around the agent go through `secure-code-review`. Any API keys or credentials the agent's tools use go through `secrets-management`. A confirmed successful injection or exfiltration triggers `incident-response`.
