---
name: mcp-server-development
description: Use when building or reviewing a Model Context Protocol (MCP) server — designing its tools, resources, and prompts so an LLM client can call them reliably. Helps you pick the right primitive, write tool schemas an LLM will use correctly on the first try, and keep tool output small enough to not blow the context window.
---

MCP servers are consumed by an LLM, not a human developer, so the usual API design instincts need adjusting: names and descriptions are the interface, and every extra field in a response is tokens the model has to read and pay for on every turn. Treat the tool list as a prompt you're writing, not just a function signature.

## Workflow

1. **Inventory capabilities and sort into primitives.** Use the table below — most designs default to too many tools when a resource or prompt would do.
2. **Name tools as verb_noun, scoped and specific** (`create_issue`, not `issue` or `do_action`). Avoid overloading one tool with a `mode` or `action` enum parameter unless the operations are truly identical in shape — LLMs pick the wrong branch under ambiguity.
3. **Minimize required parameters.** Every required field is a chance for the model to hallucinate a value. Default optional params server-side; require only what has no sane default (2-4 required params is a good ceiling before you split the tool).
4. **Write descriptions like documentation, not a comment.** State what it does, when to use it vs. a sibling tool, and any non-obvious constraints (e.g., "id must come from `list_issues`, not a URL"). This is the single highest-leverage thing you can do for the skill's reliability.
5. **Design error responses to be self-correcting.** Return a short machine-readable error code plus one sentence telling the model what to do differently, not a stack trace.
6. **Cap output size explicitly.** Paginate list-returning tools (default page size 20-50), truncate long text fields with a note ("...output truncated, use offset=N"), and never return raw binary or full file contents by default — return a summary plus an id/handle to fetch more.
7. **Dry-run against a real client before shipping.** Watch which tool the model reaches for first; if it picks the wrong one repeatedly, the descriptions (not the model) are the bug.

## Primitive selection

| Primitive | Use when | Avoid when |
|---|---|---|
| Tool | The action has side effects, or the model must supply inputs to get a result | The data is static/browsable — that's a resource |
| Resource | Read-only content the model (or user) can browse/attach, addressable by URI | The content requires parameters to compute (use a tool instead) |
| Prompt | You want to hand the user/model a reusable, parameterized instruction template | You're tempted to use it to pass data — prompts aren't for payloads |

## Common failure modes

- **Chatty tool output.** Returning full JSON objects with every field (internal ids, timestamps, nulls) when the model asked a simple question. Trim response shape to what's decision-relevant; add a `verbose` flag for the rest.
- **Ambiguous near-duplicate tools.** `get_user` and `fetch_user` coexisting with subtly different behavior — the model can't tell them apart from names alone and will guess wrong under load.
- **Silent truncation.** Cutting output without telling the model it was cut; it will confidently answer from partial data. Always signal truncation explicitly.
- **Stack-trace errors.** Raw exceptions dumped into the tool result. The model can't act on `NullPointerException at line 42` — return `{"error": "missing_field", "hint": "provide 'due_date' as ISO-8601"}` instead.
- **Stateful hidden context.** Tools that depend on server-side session state the model can't see or reset lead to confusing failures; prefer explicit ids passed on every call.

For the CLI-facing equivalent of these concerns (flags, help text, exit codes), see `cli-tool-design`. For the wire-format and versioning concerns underneath a tool's HTTP backend, see `api-design`. If you're packaging this guidance itself as a skill file, see `skill-authoring`.
