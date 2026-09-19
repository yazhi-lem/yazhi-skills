---
name: secure-design-patterns
description: Use when designing a module, service, or API's internal structure — choosing how auth checks, input validation, and privilege boundaries are arranged in code — after threat modeling has named the risks but before implementation starts. Helps you pick concrete, proven design patterns instead of ad hoc placement of security checks that later drift out of sync with the code they're meant to protect.
---

`threat-modeling` tells you *what* can go wrong and *which* trust boundaries matter; this skill is about *how to structure code* so the mitigation actually holds once five other engineers have touched the file. Most real-world breaches trace back not to an exotic exploit but to a security check that existed once, in one place, and got bypassed by a new code path nobody wired it into — a design failure, not a missing-feature failure.

## Pattern selection by concern

| Concern | Pattern | What it prevents |
|---|---|---|
| Authorization checked in multiple places | Complete mediation — one chokepoint every request passes through | A new route/handler that forgets to call the auth check |
| Broad default access | Fail-safe defaults — deny unless explicitly allowed | A missing permission entry silently granting access instead of blocking it |
| One compromised component exposes everything | Defense in depth — redundant, independent layers (network, app, data) | A single control failure becoming a full breach |
| Overprivileged services/users | Least privilege — grant only what's needed, scoped and time-boxed | Lateral movement after a single credential or service is compromised |
| Security logic mixed into business logic | Separation of concerns — auth/validation as middleware or a dedicated layer, not inline | Security checks silently skipped when business logic is refactored |
| Hidden bypass paths | No security through obscurity — assume the design is known, security must hold anyway | Reliance on an attacker "not finding" an unlisted endpoint or unminified secret |

## Workflow

1. **Start from the threat model's trust boundaries**, not from a blank page — each boundary crossing (client→API, service→service, user→admin) needs an explicit, named enforcement point before you write the handler.
2. **Put every authorization check behind one chokepoint per boundary** (a middleware, a decorator, a gateway policy) rather than repeating `if user.role == 'admin'` inline across handlers — a chokepoint is auditable in one place; scattered checks require re-verifying every call site on every change.
3. **Default new routes, fields, and feature flags to denied/off/private**, and require an explicit opt-in to expose them — a forgotten `public: true` is far more common, and far more dangerous, than a forgotten `public: false`.
4. **Validate at the trust boundary, not deep inside business logic.** Input crossing from an untrusted caller (HTTP body, message queue payload, file upload) gets validated at the entry point; code three calls deep should be able to trust its inputs came from a already-validated boundary, or the validation strategy has failed its purpose.
5. **Scope every service credential and API key to the minimum it needs**, time-boxed where the platform supports it (short-lived tokens over long-lived keys) — cross-reference `secrets-management` for the storage/rotation half of this.
6. **Never rely on an endpoint being "unlisted" or a parameter being "undocumented" as its security control** — if the only thing stopping access is that nobody's found it yet, add a real check before shipping, not after someone does.
7. **Write the negative test alongside the feature**: a test that asserts the unauthorized path is rejected, not just that the authorized path succeeds — a suite with only happy-path coverage won't catch a chokepoint bypass introduced later.
8. **Re-review the design when a new code path is added to an existing boundary** (a new admin route, a new webhook receiver) — confirm it routes through the existing chokepoint rather than reimplementing its own check.

## Anti-patterns

- **Copy-pasting an authorization check into a new handler** instead of routing through the shared chokepoint — works today, silently drifts out of sync the next time the check's logic changes in one place but not the other.
- **Defaulting a new feature flag, field, or route to public/enabled** "to make development easier," planning to lock it down before ship — this step gets skipped under deadline pressure far more often than it gets remembered.
- **Validating input in the UI/client only** and trusting the server-side handler doesn't need to re-check — any client-side validation is a UX nicety, not a security boundary, since the client is never trusted infrastructure.
- **Granting a service account broad admin-equivalent scope** "for now" because scoping it precisely takes more setup time — this is the single most common root cause of a small compromise turning into a full-environment breach.
- **Treating an obscure URL, undocumented parameter, or unminified-but-unlinked admin panel as sufficiently protected** — obscurity buys time against casual discovery, not against a targeted attacker or an automated scanner.

Cross-reference `threat-modeling` for identifying which boundaries need these patterns in the first place, `secure-code-review` for verifying a diff actually implements them correctly, and `secrets-management` for the credential-scoping half of least privilege.
