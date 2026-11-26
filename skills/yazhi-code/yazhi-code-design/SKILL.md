---
name: yazhi-code-design
description: Use when a framed yazhi-code change needs an implementation design before code — module boundaries, data flow, interface shape, and test strategy. Helps you turn the outcome sentence into a small, reviewable plan; visual hierarchy belongs to visual-design and Tamil copy to tamil-localization.
---

# Yazhi Code — Design the Smallest Plan

A frame says what must be true. This skill decides the smallest structure that can make it true, before any code is written. It is the bridge between `yazhi-code-frame` and `yazhi-code-implement`; it does not replace the domain skills that own API, security, Tamil, or visual decisions.

## Workflow

1. **Restate the outcome and constraints from the frame.** If the one-sentence outcome has changed, go back to `yazhi-code-frame` before designing. Write down the hard constraints: repo ownership, local-first/no-weights rules, and any frozen contract the change must not break.
2. **Draw the boundary on existing code first.** Name the modules or files that will change and the ones that must stay untouched. Prefer extending an existing seam over adding a new service; if ownership is unclear, stop for `org-service-boundaries`.
3. **Choose one interface shape.** Decide whether the change is a function, an API endpoint, a CLI flag, or a UI state. Follow `api-design`, `cli-tool-design`, `mcp-server-development`, or `visual-design` for that shape rather than re-deriving their rules here.
4. **Describe the data flow in three lines.** Where does input enter, what transforms it, and where does the observable outcome appear? Include error paths; a design that only describes the happy path is not a plan.
5. **Name the proof before implementation.** Write the smallest test or check that would make the outcome false if the design is wrong. Link it to the slice plan in `yazhi-code-implement`, and check `secure-design-patterns` or `threat-modeling` when the boundary is a trust boundary.
6. **Check Tamil and audience decisions explicitly.** Any user-visible Tamil string goes through `tamil-localization` / `tamil-content-writing`; kid-facing screens go through `age-appropriate-explaining`. Mark these as design inputs, not later polish.
7. **Stop at a plan another developer can challenge.** The output is a short note: boundary, interface, data flow, proof, and the skills consulted — not a ticket backlog. Treat it as Pi's read-only plan mode: no edits until the numbered plan is agreed, then mark each step `[DONE:n]` as it completes.

## Decision record

| Decision | Write down | Owner skill |
|---|---|---|
| Boundary | Files/modules in and out; frozen contracts untouched | `org-service-boundaries`, `org-cross-repo-change` |
| Interface | One function, endpoint, flag, or UI state | `api-design`, `cli-tool-design`, `mcp-server-development`, `visual-design` |
| Data flow | Input → transform → observable outcome, plus error path | This skill |
| Proof | Smallest check that fails if the design is wrong | `org-healthy-code`, `llm-evaluation` where relevant |
| Audience | Tamil copy, kid-facing density, accessibility | `tamil-localization`, `age-appropriate-explaining` |

## Anti-patterns

- **Designing a new architecture for a small frame.** A one-sentence outcome rarely justifies a new service; reuse the existing seam first.
- **Letting the chosen AI tool pick the boundaries.** The model drafts slices; the developer owns the structure and the constraints.
- **Skipping the error path.** A plan that names only successful data flow leaves failure handling to whoever writes the code next.
- **Treating Tamil text as a translation task at the end.** Glyph shaping, string length, and register change layout and data models; decide them here.
- **Writing a plan with no falsifiable proof.** "Add tests" is not a strategy; name the assertion that would fail if the outcome were not met.
- **Expanding the frame during design.** If the plan needs a bigger outcome, return to `yazhi-code-frame` and get agreement before coding.

Map to: `yazhi-code-frame` (input), `yazhi-code-implement` (slices), `yazhi-code-handoff` (local proof), `yazhi-code-deliver` (client reality). For large unknown areas, an isolated `scout` → `planner` → `worker` → `reviewer` chain can keep recon and review out of the main context; only load project-local agents from trusted repos.
