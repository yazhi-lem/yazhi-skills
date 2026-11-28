---
name: yazhi-review
description: Use when reviewing a change before merge or release and you need one verdict across security, code, and Tamil language, plus sovereign/native/open evidence. Helps you route each axis to its owning skill and return a single pass/fail note; early feature-fit belongs to yazhi-purpose-gate.
---

# Review — Security, Code, Language

Review is one verdict, not three contradictory conversations. This skill runs a final pass across security, code craft, and language, then checks that the feature still fits sovereign/native/open defaults. It orchestrates existing owners; it does not replace `secure-code-review`, `yazhi-code-standards`, or the Tamil domain skills. `yazhi-purpose-gate` owns the earlier feature-fit decision.

## Workflow

1. **Fix the review scope.** Record repo, commit range, user-facing surfaces, data paths, and the reviewer date. A review without a range becomes a conversation about the branch in general.
2. **Require the purpose note.** If `yazhi-purpose-gate` has not produced a sovereign/native/open note for this change, stop and produce one. A merge-time review is the wrong place to discover a residency or child-safety blocker.
3. **Security axis — route, do not improvise.** For an ordinary diff use `secure-code-review`; for LLM/agent paths add `llm-security-review`; for a control that looks bypassed use `pr-loophole-review`; for credentials use `secrets-management`. Record each finding with severity and owner. A suspected active exploit leaves this flow for `incident-response`.
4. **Code axis — check the proof, not the vibe.** Apply `yazhi-code-standards` and `org-healthy-code`: one outcome, small diff, no foreign call on the default path, typed errors, and a named command with a result. Use `yazhi-code-handoff` for the cold diff read and `org-impactful-pr` for the honest description. "Tests pass" without the command is not evidence.
5. **Language axis — require native evidence.** For every user-visible Tamil string, confirm a native-speaker review; route layout/font/input to `tamil-localization` or `tamil-input-methods`, natural copy to `tamil-content-writing`, purity claims to `tamil-purity-scoring`. Machine-fluent Tamil with no named reviewer is a finding, not a nit.
6. **Re-check the three defaults.** Sovereign: no foreign API on the default path and model license/self-host route named. Native: Tamil strings and glyph behavior reviewed. Open: FLOSS license and public artifact named, or an explicit அகம் reason recorded per `org-ethos`. A waiver needs an owner and a date.
7. **Return one verdict.** Use the table below. Any block must name the single owner and the exact note/PR that resolves it. Do not silently expand scope while reviewing; open a new `yazhi-code-frame` for that.

## Review verdict

| Axis | Pass evidence | Block condition |
|---|---|---|
| Purpose | Dated purpose note with no unresolved waiver | Missing note; undisclosed foreign default; child gate absent |
| Security | Routed skill findings closed or owned with severity | Critical/high finding unowned; credential in diff |
| Code | Small diff, named check, honest description | Unreviewable diff; no runnable proof; silent fallback |
| Language | Native reviewer named per string; glyph/input checked | Unreviewed Tamil; broken shaping; invented purity claim |
| Openness | License + public artifact, or documented அகம் reason | Closed core path with no reason or owner |

## Anti-patterns

- **One reviewer claiming all three axes without opening the owner skills.** Security and Tamil each need their own checklist; a general impression is not a pass.
- **Treating green CI as a security verdict.** Tests cover the behavior someone wrote a test for, not the bypass nobody wrote a test to forbid.
- **Waiving a Tamil review under deadline.** Deadline pressure is exactly when an unreviewed string becomes public.
- **Hiding a residency or license exception in chat.** A waiver without an owner and date is a silent breach of the purpose gate.
- **Expanding the change during review.** New work belongs in a new frame; otherwise the review target moves and the verdict becomes meaningless.
- **Returning three verdicts instead of one.** Authors need one decision and one next action, not a committee summary.

Map to: `yazhi-purpose-gate` (input note), `org-ethos` (chamber and values), `yazhi-code-standards`, `secure-code-review`, `tamil-content-writing`, `org-release` (release gates), `yazhi-code-handoff` (merge path).
