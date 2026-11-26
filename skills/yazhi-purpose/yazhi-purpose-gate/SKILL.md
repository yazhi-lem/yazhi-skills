---
name: yazhi-purpose-gate
description: Use when deciding whether a proposed Yazhi feature fits our purpose — sovereign, Tamil-native, and open by default — before it is framed or reviewed. Helps you prove those three defaults with evidence instead of slogans; the merge-time three-axis check is yazhi-review.
---

# Yazhi Purpose Gate

Yazhi features are not neutral. They either reduce or increase dependence on foreign clouds, English-first interfaces, and closed vendors. This gate turns three claims — sovereign, native, open by default — into questions with evidence. It sits before `yazhi-code-frame`; `yazhi-review` checks the same claims again at merge time with code and language evidence. `org-ethos` owns the underlying values; this skill owns the feature-fit decision.

## Workflow

1. **State the feature in one sentence and name the user.** If the user is a child, a Tamil speaker, or a regulated customer, say so now — those facts change the gates. Do not proceed with "everyone" as the user.
2. **Prove the sovereign path.** Show where data and prompts go by default. No foreign cloud, foreign AI API, or license-check callback on the default path; self-hostable/open weights where a model is involved. Use `data-residency-compliance`, `sovereign-cloud-architecture`, and `open-model-selection` for the detailed checks. Record the gateway exception explicitly if one is requested — a waiver needs an owner and a reason, not silence.
3. **Prove the native path.** Name the Tamil strings, input method, font/shaping, and number/date formats the feature touches. Every user-visible Tamil string gets a native-speaker review; every glyph or input behavior routes to `tamil-localization` or `tamil-input-methods`. "English now, Tamil later" is a debt to record in the frame, not a default to accept.
4. **Prove the open path.** Choose the FLOSS license, name the public artifact (library, docs, demo, model card), and confirm the core path works without a proprietary service. Work belongs in புறம் unless it contains keys, child personal data, unfinished research, or a founder gate — those stay in அகம் until promoted. `org-ethos` owns the chamber rule; this skill records which one applies.
5. **Check the hard gates before design.** Child-facing features need counsel sign-off and verified parental consent; system-changing features need a plan and tested rollback. If either gate is missing, stop and hand the work to `org-release` / `org-ethos` rather than designing around it.
6. **Write a short purpose note.** Table below, one line per default with evidence and a pass/fail/waiver marker, plus the named owner of any exception. Hand the note to `yazhi-code-frame` as a constraint; do not treat it as approval to ship.

## Purpose gate table

| Default | Evidence required | Fails when |
|---|---|---|
| Sovereign | Default data path, model license, hosting owner | Foreign API on the default path; no self-host route |
| Native | Tamil strings/input/fonts reviewed by a native speaker | English-only UI with no plan; machine-fluent Tamil unreviewed |
| Open | License, public artifact, no proprietary core dependency | Closed demo with no source path; private-by-default work |
| Child-safe | Counsel sign-off, consent path, red-team score | Any child-facing surface without the preconditions |
| Reversible | Runbook and one-command rollback | A deploy with no tested undo |

## Anti-patterns

- **Calling something sovereign because it runs on "our" server.** Sovereignty includes jurisdiction, model license, and vendor lock-in, not just hosting location.
- **Tamil as a translation ticket.** Treating language work as post-launch copy ignores glyphs, input, layout, and register.
- **Open by accident.** Publishing a demo without a license or a reusable artifact is neither open nor reusable.
- **Hiding a waiver in chat.** A foreign API exception or private chamber decision needs an owner and a written reason in the repo.
- **Gating after implementation.** Discovering a residency or child-safety blocker in review wastes the whole build.

Map to: `yazhi-code-frame` (constraints), `yazhi-review` (merge-time check), `org-ethos` (values), `org-release` (hard gates), `yazhi-org-status` (repo context).
