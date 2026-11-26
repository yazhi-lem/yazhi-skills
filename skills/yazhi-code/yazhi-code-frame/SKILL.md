---
name: yazhi-code-frame
description: Use when starting a new piece of work or turning a vague idea into a clear, buildable intent. Helps you write the one-sentence outcome, explicit out-of-scope, and the main risk so implementation stays small and reviewable.
---

# Yazhi Code — Frame the Work

A clear frame is the fastest way to avoid rework. This skill turns an idea into a short, shared statement of intent that another developer (or an AI assistant) can act on without extra context. It owns the framing step; implementation and handoff live in the sibling skills.

## Workflow

1. **Write the one-sentence outcome.**  
   Complete: “When this is done, <specific observable thing> will be true.”  
   If you cannot finish the sentence, the work is not ready to start.

2. **List what is explicitly out of scope.**  
   Name the two or three things a reasonable person might assume are included but are not. This prevents scope creep later.

3. **Name the main risk.**  
   State the one or two things most likely to make this take longer or fail. Prefer concrete risks (“the existing parser does not expose this node type”) over vague ones (“it might be hard”).

4. **Check related skills before designing.**  
   - If the change touches shared contracts or multiple repos, read `org-cross-repo-change`.  
   - If it adds a new capability, confirm ownership with `org-service-boundaries`.  
   - If the work is large enough to affect the day, note it in `yazhi-daily-rhythm`.  
   - Once the frame is stable, pass it to `yazhi-code-design` for the smallest technical plan.

5. **Stop when the frame is shareable.**  
   You can explain the change to another developer in under a minute, and the outcome sentence is stable.

## Output shape

```
Outcome: <one sentence>
Out of scope: <bullet list>
Main risk: <one or two sentences>
Related skills checked: <names or “none”>
```

## Frame quality check

| Field | Ready to start when | Not ready when |
| --- | --- | --- |
| Outcome | One observable behaviour someone else could test | Uses words like “improve”, “clean up”, or “support” |
| Out of scope | Two or three named exclusions a reasonable person would expect | “Nothing, it is small” |
| Main risk | Names the concrete blocker and the fallback | “It might be hard” |
| Related skills | At least one checked, or an explicit “none” | Not looked at yet |

## Anti-patterns

- **Starting to code before the outcome sentence exists.** The first implementation usually solves the wrong problem.
- **“We’ll figure out scope as we go.”** Turns a small change into an open-ended exploration that is hard to review.
- **Listing every possible risk.** Only the ones that change the approach matter at this stage.
- **Skipping the related-skill check.** A cross-repo change framed in isolation creates contract drift that `org-impactful-pr` cannot fix later.

Map to: `yazhi-code-design` (turns the frame into a plan), `yazhi-code-implement`, `yazhi-code-handoff`, `yazhi-code-deliver` (reaches the client), `org-healthy-code` (keeps the diff small), `org-impactful-pr`, `yazhi-daily-rhythm`, `org-cross-repo-change`, `org-service-boundaries`.
