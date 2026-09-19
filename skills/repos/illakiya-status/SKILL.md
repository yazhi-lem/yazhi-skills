---
name: illakiya-status
description: Use when working in the illakiya repository — the Rust + Kotlin native Tamil Android keyboard — on the layout engine, dictionary, sandhi rules, or the IME UI. Helps you extend the existing engine instead of duplicating logic that already exists across the Rust/Kotlin boundary.
---

Illakiya (இலக்கியம், "literature") is a native Tamil keyboard for Android: a Rust core (`libillakiya`) exposed to Kotlin/Compose via a UniFFI bridge. It implements the PM0100 layout — phonetically grouped per the *Tholkaappiyam* — covering all 247 Tamil characters (12 vowels, 18 consonants, 216 uyirmei combinations, plus ஃ aytham), with swipe-up for nedil (long vowels) and a from-scratch sandhi (word-joining) engine. It's the sibling project to `adhan` for Tamil-script handling — one does model tokenization, the other does keyboard input, and both encode the same Tholkaappiyam-derived character classification independently.

## Status at a glance

| Layer | File(s) | Status |
|---|---|---|
| Layout | `core-rust/src/layout.rs` | ✅ Complete — 216 uyirmei combos |
| Character classifier | `core-rust/src/tamil.rs` | ✅ Complete — Vallinam/Mellinam/Idaiyinam/Uyir |
| Dictionary | `core-rust/src/dictionary.rs` | ✅ 836 words, Trie-based, <5ms lookup — expansion in progress |
| Sandhi engine | `core-rust/src/sandhi.rs` | ✅ 6 Tholkaappiyam Punarchi rules with confidence scoring |
| State machine | `core-rust/src/engine.rs` | ✅ Complete — 379 lines, ties dictionary + sandhi together |
| Android IME | `android/` (Kotlin/Compose) | ✅ Structure complete — `IllakiyaIME`, `KeyboardView`, `SettingsActivity` |
| ONNX sandhi disambiguation | — | 📋 Not started |
| Tanglish mode | — | 📋 Not started |

## Workflow

1. **Read `docs/tasks.md` (dev log with Next Actions) and `docs/PLAN.md` (phase completion) before starting** — both are actively maintained and more current than the README's feature list.
2. **Put new Tamil-classification logic in `core-rust/`, never duplicate it in Kotlin.** The whole point of the UniFFI split is one classifier; a parallel Kotlin implementation of Vallinam/Mellinam rules would drift from the Rust source of truth.
3. **Run `cargo test` in `core-rust/` before touching the Android layer** — it's the first item in the repo's own Next Actions list and validates the engine independent of the Android build.
4. **Grow the dictionary via the existing sources table in the README**, not a new ad hoc word list — Swadesh+Common, Sangam Corpus, Modern Tamil, Verbs, Grammar, Tanglish, Tech, Literary, Body & Nature, and Corpus Frequent are the tracked categories; add words under the right one.
5. **Keep all data embedded via `include_str!`** — the "zero filesystem" design goal means no runtime file reads for dictionary or layout data; don't introduce a loose asset file as a shortcut.
6. **Build and test with `./scripts/build-apk.sh`**, requiring Android SDK + NDK + Rust — don't hand-assemble the cross-compilation steps; the script already handles the 4-ABI build.
7. **Check `docs/BRIDGE.md`** before changing the UniFFI interface (`illakiya.udl`) — it documents the full architecture, data flow, and performance targets the bridge is designed against.

## Next actions

1. `cargo test` — validate all Rust modules compile and pass (currently first on the repo's own list).
2. Expand the dictionary past 836 words toward 1,000+, prioritizing Sangam literature vocabulary.
3. ONNX integration for sandhi ambiguity resolution — currently rule-based only.
4. User dictionary persistence via SQLite (currently in-memory/session-only).
5. Tanglish mode — mixed Tamil-English detection, not yet started.

## Anti-patterns

- **Re-implementing Vallinam/Mellinam/Idaiyinam classification in Kotlin** instead of calling into the Rust core — creates two sources of truth for the same Tholkaappiyam rules.
- **Adding a dictionary word without categorizing it** into one of the tracked source buckets — breaks the provenance the README's dictionary-sources table depends on.
- **Introducing a runtime file read for layout or dictionary data** — violates the "zero filesystem, all data via `include_str!`" design goal that keeps the keyboard fast and dependency-free.
- **Changing `illakiya.udl` without updating `docs/BRIDGE.md`** — the bridge spec is the only place the Kotlin/Rust contract is documented end-to-end; drift here breaks builds silently until someone hits the mismatch at runtime.
- **Skipping `cargo test` before an Android build** — Rust-side regressions surface much more slowly and confusingly once wrapped in the UniFFI/JNA layer.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture, `adhan-status` for the sibling Tamil-script model work, and `tamil-input-methods` for general keyboard/IME design guidance (Tamil99, phonetic input, auto-pulli).
