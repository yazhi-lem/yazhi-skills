---
name: yazh-unity-status
description: Use when working in the yazh-unity repository — the Tamil AR/XR pet app — on gameplay, the on-device Tamil inference engine, or release packaging. Helps you recognize that the code is production-ready and the actual blocker is credentials, not engineering.
---

Yazh XR Pet App is an AR pet the child chats with in Tamil (no translation layer — the pet thinks natively in Tamil via on-device ONNX inference). It pivoted in July 2026 from a survival-care loop to an endless runner: the pet runs through the five **tinai** landscapes of Sangam literature (குறிஞ்சி Kurinji, முல்லை Mullai, மருதம் Marutham, நெய்தல் Neithal, பாலை Palai) on an endless cycle, four pets each with a distinct ability (double jump, high jump, obstacle smash, collectible magnet), and runs still feed the pet's mood/bond via the `YazhLife` system between sessions.

## Status at a glance

| Aspect | State |
|---|---|
| Codebase | 2,485 lines of C# across 8+ systems; production-ready |
| AI model | Yazh 30K, on-device ONNX via Barracuda, <50ms latency |
| CI/CD | GitHub Actions builds a debug-signed APK on every push to `main`/`develop`; model-less by default (falls back to scripted Tamil dialogue without ONNX weights) |
| COPPA compliance | Documented in `docs/security/COPPA_COMPLIANCE.md` |
| Play Store | 🔴 Blocked — awaiting signing key (founder gate) |
| App Store | 🔴 Blocked — awaiting signing certificate (founder gate) |

## Workflow

1. **Check `docs/START_HERE.md` and `docs/SETUP.md` before any change** — they're written specifically for new contributors and cover the Unity 6 LTS setup this repo assumes.
2. **Recognize the blocker before proposing work.** Both stores are gated purely on signing credentials the founder controls — see `docs/deployment/PLAY_STORE_PLAN.md`. No amount of build-script or CI work unblocks this; don't spend a session there.
3. **Keep new gameplay work inside `Assets/Scripts/Runner/`** (the current endless-runner core loop) rather than extending the legacy `Gameplay/SurvivalSystem.cs`, which is now explicitly the legacy loop per the README's own labeling.
4. **Treat `Assets/Scripts/AI/YazhInferenceEngine.cs` as the only place ONNX inference is invoked** — verify model hashes against `docs/security/ONNX_HASH_VERIFICATION.md` before swapping a model file.
5. **Never commit real ONNX weights to a path CI builds from by default** — CI is model-less on purpose so unsigned test APKs keep shipping without bundling proprietary model weights.
6. **Update `docs/MODEL_STATUS.md` and `docs/COMPLETION_SUMMARY.md`** when a system's implementation status changes — these are the living trackers referenced from `docs/INDEX.md`.
7. **Route AR-specific changes through `Assets/Scripts/AR/ARSessionManager.cs`** — it owns the ARKit/ARCore lifecycle; don't start a session directly from gameplay code.

## Next actions

1. Founder: provide the Play Store signing key and App Store signing certificate — this is the only item blocking both store launches.
2. Engineering (non-blocking, can proceed in parallel): expand `docs/gameplay/ENDLESS_RUNNER_DESIGN.md` coverage — more terrain variety, additional pet abilities beyond the current four.
3. Keep `docs/LATENCY_BENCHMARK.md` current as the ONNX model or Barracuda version changes; <50ms is the target to protect.
4. Track the 3 open engineering issues in the repo (per the org-level status skill) — none are store-blocking.

## Anti-patterns

- **Proposing an engineering fix for a credentials blocker.** The Play Store and App Store gates are administrative (signing key/certificate), not code — refactoring the build pipeline doesn't move either launch date.
- **Bundling real ONNX model weights into a CI-triggered build path.** CI is deliberately model-less; the app must fall back to scripted dialogue without them.
- **Extending `SurvivalSystem.cs`** for new features — it's the pre-pivot legacy loop; new gameplay belongs in `Runner/`.
- **Skipping the ONNX hash check** when swapping a model file — `docs/security/ONNX_HASH_VERIFICATION.md` exists specifically to catch a tampered or mismatched model before it ships to a child's device.
- **Starting an AR session outside `ARSessionManager`** — bypasses the lifecycle management ARKit/ARCore both require and risks leaking a session across scene transitions.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture, `airgapped-llm-deployment` for on-device inference patterns, and `adhan-status` for the Yazh 30K model this app embeds.
