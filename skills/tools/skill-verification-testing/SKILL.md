---
name: skill-verification-testing
description: Use when a skill in this repo produces a self-reported verdict — "passed", "compliant", "no issues found", "on-brand", "no vulnerabilities" — and that verdict needs to be trusted before acting on it. Also use when authoring a new skill that will produce any pass/fail judgment, to build in verification from the start rather than adding it after a false verdict is discovered in production use.
---

# Skill Verification Testing

## Purpose

Any skill that ends in a self-reported verdict can produce a confident,
well-formatted "PASS" without the underlying check actually having been
run — not through deception, but because writing a plausible verdict is
often easier than doing the analysis it claims to summarize. This skill
gives a repeatable method for (a) auditing an existing skill's verdicts
against real evidence, and (b) designing new verdict-producing skills so
this failure is structurally harder to produce.

This applies repo-wide. Any skill whose SKILL.md contains language like
"confirm," "validate," "check," "review," or "ensure" followed by a
pass/fail-style output is in scope — not just skills in one category.

## Workflow

1. Identify verdict-producing skills by scanning for PASS/FAIL outputs without evidence.
2. Run an adversarial test using a deliberately constructed failing case.
3. Retrofit the skill to require an evidence worksheet before any verdict.
4. Spot-check the skill periodically in production.
5. Record the audit using the standard output format.

## Step 1 — Identify verdict-producing skills

Scan a skill's SKILL.md for output formats that include a status field
(PASS/FAIL, "compliant"/"non-compliant", "no issues found", a score, a
checkmark). If the skill's output includes a verdict but no requirement
to show the evidence behind it, it is at risk of this failure mode.

| Repo example | Verdict it produces | Currently requires evidence shown? |
|---|---|---|
| `content-quality-review` | PASS/FAIL per check | Yes, after the Step 5 fix |
| `secure-code-review` | Vulnerability found / clear | Check against skill body |
| `threat-modeling` | Threats enumerated | Check against skill body |
| `data-residency-compliance` | Auditable posture produced | Check against skill body |

## Step 2 — The adversarial test

To audit any verdict-producing skill, don't ask it to review real content.
Instead, feed it a case **deliberately constructed to fail**, and see if
it catches it:

- For `secure-code-review`: submit a diff with an obvious SQL injection and see if it's flagged, not just skimmed
- For `threat-modeling`: submit a design with an unauthenticated admin endpoint and check if it surfaces as a threat
- For `content-quality-review`: submit copy that repeats the same opener across platforms and check if it's actually caught (this exact test already found a real gap in this repo — see the skill's own changelog/history)

If the skill returns "PASS" or "no issues" on a case built to fail, the
verdict is not trustworthy yet — the skill needs the Step 3 fix below.

## Step 3 — Require an evidence worksheet before any verdict

Retrofit (or author from the start) the skill so it cannot output a
verdict without first producing a worksheet that:
- Quotes the specific thing being checked, not a paraphrase
- States the exact criterion being applied to it
- Reaches a verdict for that one item before moving to the next

A verdict without a preceding worksheet should be treated as "the check
did not happen," regardless of what the final status field says. This
mirrors the fix already applied to `content-quality-review` in this repo
— use it as the reference pattern.

## Step 4 — Spot-check in production, not just at build time

Passing the adversarial test once does not mean the skill will always
show its work. Periodically re-run Step 2 on skills already in active
use — a skill that showed its worksheet during testing can still lapse
back into bare verdicts under different phrasing or a longer task. This
is a recurring check, not a one-time certification.

## Step 5 — Output format for an audit

```
SKILL AUDITED: <name>
ADVERSARIAL CASE USED: <what was fed in, and what it was designed to fail on>
VERDICT RETURNED: <what the skill said>
EVIDENCE SHOWN: <yes, with worksheet / no, bare verdict only>
RESULT: <trustworthy / needs Step 3 fix, with reasoning>
```

## Common failure modes

- **Testing with real, passable content only**: auditing a skill using
  content that should genuinely pass never reveals whether it can catch a
  failure — the adversarial case must be built to fail.
- **Treating a good worksheet format as proof it's real**: a skill can
  learn to produce a convincing-looking worksheet without the underlying
  evidence being accurate. Spot-check the worksheet's claims against the
  actual content, not just its presence.
- **One-time certification**: verifying a skill once at launch and never
  re-checking it, missing later drift back into bare-verdict behavior.
- **Assuming this only applies to "review" skills**: any skill with an
  implicit judgment — a "recommended" tag, a risk score, a completion
  checkmark — carries the same risk, even without the word "review" in
  its name.
