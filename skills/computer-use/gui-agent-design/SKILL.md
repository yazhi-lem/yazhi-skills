---
name: gui-agent-design
description: Use when designing the perceive-decide-act loop for an agent that controls arbitrary GUIs via screenshots, coordinates, or an accessibility tree rather than a fixed API. Helps you choose a grounding strategy, define a safe action space, and add guardrails before the agent can click/type/scroll on real screens.
---

GUI agents differ from scripted browser automation in one key way: the target UI is not known in advance, so the agent must ground a natural-language goal ("close the dialog") into a concrete coordinate or element reference at runtime. This means every loop iteration carries genuine uncertainty about what's on screen and what an action will do, so the design must budget for misgrounding and irreversible mistakes.

## Workflow

1. **Perceive**: capture a screenshot and, if available, an accessibility tree snapshot in the same step. Prefer the a11y tree for grounding when the platform exposes one (web, native apps with proper labels); fall back to vision-based coordinate grounding only when it doesn't (canvas apps, games, legacy desktop UI).
2. **Ground the instruction**: map the requested action to a specific element or (x, y) point. Require a confidence/consistency check — e.g. ask the model to output both a bounding box and a short justification, and reject grounding results below a set confidence threshold (default: re-prompt or take a fresh screenshot if the model expresses uncertainty or if two independent grounding attempts disagree by >20px).
3. **Classify the action's risk tier** before executing (see table) and apply the matching guardrail.
4. **Act**: execute a single atomic action (one click, one keystroke sequence, one scroll). Never batch multiple destructive actions on one perception — re-observe between steps.
5. **Verify**: re-screenshot after every action and diff against the expected post-state (element appeared/disappeared, focus moved, text changed). Cap consecutive no-progress verifications at 3 before halting and escalating to the user.
6. **Escalate on ambiguity**: if the same screen state persists after 2 corrective attempts, or the target element cannot be found after 3 grounding attempts, stop and ask for clarification rather than guessing.

## Action space design options

| Design | Grounding needed | Pros | Cons |
|---|---|---|---|
| Coordinate clicks (x, y) | Vision-based bounding box | Works on any pixel-rendered UI | Brittle to resolution/DPI/theme changes |
| Accessibility-tree element refs | Role + name lookup | Stable across visual changes, faster | Unavailable on canvas/game UIs, some apps mislabel elements |
| Semantic action verbs (`click_button("Save")`) | Hybrid (tree lookup, vision fallback) | Most robust, self-documenting for logs | Requires an abstraction layer to implement |
| Keyboard-only macros | None (positional focus) | Deterministic, no grounding error | Only works when tab order/shortcuts are known and stable |

## Numeric defaults

- Screenshot cadence: after every action, plus one before the first action (baseline).
- Grounding confidence threshold: reject and retry below ~0.7 model-reported confidence, or on >20px disagreement between two grounding passes.
- Max retries per action: 3, then escalate.
- No-progress cutoff: 3 consecutive verifications with no observed state change halts the loop.
- Idle/hang timeout waiting for UI response: 8s before re-screenshotting.
- Destructive-action confirmation window: always pause for explicit approval before actions tagged high-risk (see below).

## Risk tiers and guardrails

| Tier | Examples | Guardrail |
|---|---|---|
| Safe | Scroll, read, hover, screenshot | Execute freely |
| Reversible | Open menu, type into a draft field, navigate | Execute, verify after |
| Destructive | Delete, submit payment, send message, overwrite file | Require explicit user confirmation or a dry-run preview before executing |
| Irreversible + high-blast-radius | Format/delete account, mass-send, deploy to prod | Refuse by default unless the user's instruction explicitly and unambiguously names this exact action |

## Anti-patterns

- **Acting on a stale screenshot** — perception and action must be tightly paired; a screenshot taken 5 actions ago no longer reflects reality.
- **Coordinate-only grounding with no accessibility-tree fallback** — small UI scaling or theme changes silently break every click.
- **No confirmation step before destructive actions** — a misgrounded click on "Delete" instead of "Duplicate" is unrecoverable without one.
- **Retrying the identical action on failure without re-perceiving** — if a click didn't work, the screen state changed or grounding was wrong; re-screenshot before retrying, don't repeat blindly.
- **Treating "no error thrown" as success** — GUI actions rarely raise exceptions; success must be confirmed visually or via the a11y tree, not assumed.

For browser-specific selector and wait strategies, see `browser-automation`. For chaining GUI actions with file-system and native-app steps in a longer workflow, see `desktop-workflow-automation`.
