---
name: thozhan-dev
description: Use when shipping an offline-first Yazhi interface — a Flutter APK for a low-spec Android device, a Rust/Dioxus desktop or web widget, or a local predictive Tamil keyboard that must run with no network. Helps you keep storage local, the first frame fast, and keystrokes off any remote server.
---

Thozhan builds the surfaces users touch on devices with limited RAM, intermittent power and no reliable network. Every decision favours local data and a fast first frame over feature richness.

## Workflow

1. **Set the budget before coding.** Target device RAM, APK size ceiling and cold-start time — for the reference low-end Android, APK under 30 MB and cold start under 2.5 s are realistic goals.
2. **Design the storage first.** Choose Isar or SQLite by query pattern (Isar for object graphs, SQLite for relational/aggregate queries) and define the schema before UI work; retrofitting local persistence is the most expensive change.
3. **Make offline the default path, sync the exception.** Every write succeeds locally and queues; a network call is never on the critical path of a tap.
4. **Build the shell lean.** Dark-theme primitives from `oviya-design`, one sans plus one mono font, no heavy icon fonts, deferred or stripped debug tooling in release builds.
5. **Ship Tamil input locally.** Bundle a trie over the base dictionary (`tamil_base.json`); predict from memory, with keys never leaving the device.
6. **Measure on the device**, not the emulator — cold start, first input latency, and RSS after ten minutes of use.
7. **Verify the offline path by turning the radio off** for a full session; most offline bugs only appear there.

## Storage choice

| Need | Use | Why |
|---|---|---|
| Object graph, fast reactive reads | Isar | Indexed objects, change streams |
| Relational queries, aggregates | SQLite | JOINs, small footprint |
| Read-only word list | Bundled trie (JSON → memory-mapped) | No query engine at all |
| Small settings | `shared_preferences` / key-value | Trivial writes |

## Defaults

- APK ≤ 30 MB; cold start ≤ 2.5 s; first keystroke response ≤ 100 ms.
- Predictive dictionary: top ~50k Tamil words, trie built at build time, not at first launch.
- No analytics SDK in the release build unless explicitly justified.

## Anti-patterns

- **Network on the critical path.** A tap that waits for the server fails exactly where the product is deployed.
- **Building the trie at first launch.** Users see a multi-second stall on a slow device; build at compile time.
- **Using the emulator as the performance target.** Emulator timings hide the memory ceiling of the real device.
- **Ignoring APK size until release.** Storage-constrained users uninstall rather than wait; check the size every build.
- **Sending keystrokes or dictionaries to a server.** It breaks the privacy promise and the offline promise at once.

For the design tokens this UI consumes see `oviya-design`, for Tamil input mechanics see `tamil-input-methods`, and for the dictionary content see `tamil-text-processing`.
