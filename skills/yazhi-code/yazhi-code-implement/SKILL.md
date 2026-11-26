---
name: yazhi-code-implement
description: Use when implementing a framed change in small working slices, especially when using an AI coding assistant. Helps you keep the tree runnable, verify each slice locally, and write prompts that produce usable results on the first or second try.
---

# Yazhi Code — Implement in Working Slices

Implementation stays fast when each step leaves the code in a working state and the AI is given tight, constrained prompts. This skill owns the coding loop; framing and final handoff are in the sibling skills.

## Workflow

1. **Confirm the frame is still valid.**  
   Re-read the one-sentence outcome. If it has shifted, update it before writing more code.

2. **Choose the smallest slice that proves the intent.**  
   Take the boundary and test strategy from `yazhi-code-design`. Prefer extending existing code over new structure; the slice should compile and run.

3. **Use AI for drafting, not for ownership.**  
   Give the model the outcome, the relevant existing code, and explicit constraints. Ask for the smallest change that could work. Always read and run the result yourself.

4. **Verify the slice before continuing.**  
   Confirm previous behavior still holds and the new behavior is present. Update tests or other local proof in the same pass. See `yazhi-code-standards` for naming, error, and style defaults, and `org-healthy-code` for honest tests and small diffs.

5. **Repeat until the outcome is met.**  
   Stop when the one-sentence outcome is true. Do not expand the change.

## Working in a tool loop

Pi runs turns of model output plus tool calls; steering arrives between turns, follow-up after the run. Work with that shape:

1. **Checkpoint before edits.** Commit, branch, or stash before a multi-file slice; Pi's own checkpoint example takes a stash at `turn_start`.
2. **Batch independent reads.** Use parallel tools or a sandboxed script for `read`/`grep`/`find`; write large output to a file and return only the decision-relevant excerpt.
3. **Write the recovery note.** After each slice, record outcome, constraints, done/in-progress/blocked, decisions, next step, critical context, and modified files. Compaction keeps that summary, not every tool result.
4. **Stop cleanly.** When the slice is verified, stop. A queued follow-up is a new frame, not hidden scope.

## Prompting techniques that reduce rework

| Element | What to include | Example phrasing |
| --- | --- | --- |
| Intent | The one-sentence outcome | “When done, the parser returns the new node type without changing existing nodes.” |
| Constraints | Style, patterns, what to avoid | “Match the existing error style. Do not add network calls.” |
| Context | Only the relevant existing code or error | Paste the function or the failing test output. |
| Output shape | Diff, full function, or changed lines only | “Show only the changed function.” |
| Verification | How you will check it | “I will run the existing test suite plus one new assertion.” |

Useful patterns:
- “Given this existing function, add X while keeping current behavior. Show only the changed function.”
- “Write the minimal failing test first, then the smallest change that makes it pass.”
- “List three approaches that touch the fewest files. Implement the preferred one.”

## Anti-patterns

- **Letting the model decide the approach.** You own the design; the model drafts the implementation.
- **Accepting a large generated diff without reading it.** Creates unreviewable changes that break `org-healthy-code`.
- **Continuing after a slice leaves the tree non-runnable.** The next slice becomes harder to verify.
- **Prompting with the entire file when only one function matters.** Increases noise and incorrect edits.
- **Committing code you do not understand.** Violates the ownership rule and makes later review slower.

Map to: `yazhi-code-frame` (the outcome), `yazhi-code-design` (the plan), `yazhi-code-standards` (craft rules), `yazhi-code-handoff` (local proof and PR), `org-healthy-code` (small diffs, honest tests, local-first), `agentic-reliability` (bounded steps), `org-impactful-pr`.
