---
name: org-healthy-code
description: Use when writing or reviewing code in a Yazhi repo and the change risks becoming unreviewable — a 2,000-line diff, a silent fallback, a test that asserts nothing, or a shortcut that sends data to a foreign API. Helps you keep diffs small, local-first, and honest so the 48-hour review gate actually works.
---

Yazhi's review gate is a second human within 48 hours, and it only works if the diff is reviewable. Healthy code here means four things: small enough to read, local-first by default, tested with assertions that can fail, and honest about what it does not do. `org-ethos` owns the values; this skill owns the code-level practice.

## The four habits

| Habit | Concrete default | Failure it prevents |
|---|---|---|
| Small diffs | ≤400 changed lines per PR; split by layer, not by file | Reviewers approve by skimming and miss the real change |
| Local-first | No network call on the default path; opt-in behind a flag | தற்சார்பு breach from a "convenience" API |
| Honest tests | Every test asserts a value; the overfit/sanity gate runs before long jobs | Green CI on a wiring bug that burns hours |
| Explicit failure | Raise with a typed error; never a bare `except: pass` | Silent fallback that hides data loss |

## Workflow

1. **Read the repo's own conventions first** — `CONTEXT.md` for yazhi-api, `docs/DEV.md` for adhan, the Rust core docs for illakiya. Yazhi repos differ on test naming and config: adhan collects `<module>_tests.py`, not `test_*.py`, so a correctly-written test can silently never run.
2. **Split the change by layer before writing it.** One PR for the contract, one for the implementation, one for the wiring. A 2,000-line PR that mixes all three cannot be reviewed in 48 hours and will be rubber-stamped.
3. **Keep the default path offline.** Add any network or model call behind an explicit flag with a documented fallback. If a feature cannot work offline, say so in the PR instead of quietly calling a foreign endpoint.
4. **Write the failing test first, then make it pass.** A test that asserts nothing, or asserts only that no exception was raised, is worse than no test — it certifies the bug. For long jobs, run the sanity gate (`--overfit-batch` in adhan) before the full run.
5. **Fail loudly and specifically.** Raise a typed error with the offending value; a swallowed exception in an ingestion pipeline looks like success and loses data.
6. **Check the boundary you are touching.** If the change crosses a repo contract, read `org-cross-repo-change` first; if it adds a capability, confirm the owner with `org-service-boundaries`.
7. **Leave the code easier to change than you found it** — delete the dead branch you had to read around, but do not bundle unrelated refactors into the same PR; that is what makes a small diff look large.

## Anti-patterns

- **The "temporary" network call.** A foreign API key added "just for the demo" is a தற்சார்பு breach with a production path; it survives because nobody owns removing it.
- **A test that only checks for no exception.** Certifies broken behavior and blocks the next person from finding the real bug.
- **`except Exception: pass` in a pipeline.** Turns a data-loss bug into a green run; the corpus quietly loses rows.
- **Mixing a refactor with a behavior change.** Reviewer cannot tell which line changed behavior, so the 48-hour gate becomes a formality.
- **Naming a test `test_*.py` in adhan.** Silently not collected by that repo's pytest convention; the suite is green and the test never ran.
- **Training on a GPU-only config on a CPU box.** The nano CPU config and the default configs are not interchangeable; the run fails hours in or produces garbage.

Follow `org-ethos` for the அறம் gates; `org-impactful-pr` for the PR that carries this code; `org-cross-repo-change` for contract changes; `org-service-boundaries` for where a capability belongs; `llm-security-review` for model-facing risk.
