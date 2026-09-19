---
name: yazh-kutty-status
description: Use when asked to start, scope, or resume work in the yazh-kutty repository — a 30K-vocabulary Tamil model for kids. Helps you confirm scope and avoid duplicating adhan's own nano-tier model before writing a first line of code into an empty repository.
---

`yazh-kutty` is described, org-wide, as "a 30K Tamil Model trained for kids with limited vocabulary in Tamil." As of this writing the repository is **empty** — zero size, no commits beyond repo creation, no code, no docs. Every other Yazhi model repo (`adhan`) has already gone through phased scaffolding, roadmap, and CI setup before writing model code; `yazh-kutty` has none of that yet. Treat any work item here as "define scope," not "continue existing work" — there is no existing work to continue.

## What actually exists today

| Artifact | State |
|---|---|
| Source code | None |
| Documentation | None beyond the one-line GitHub description |
| CI/CD | None |
| Relationship to `adhan` | Undefined — `adhan`'s own roadmap already targets a small, edge-deployable "light" launch tier (`adhan-nano`), which may or may not be the same effort as `yazh-kutty` |
| Relationship to `yazh-unity`'s "Yazh 30K" model | Undefined — `yazh-unity`'s README references an on-device "Yazh 30K" ONNX model that may be this project's deliverable, a placeholder name, or a separate artifact entirely |

## Workflow

1. **Before writing any code, resolve the `adhan`-overlap question with the founder.** `adhan`'s `ROADMAP_JAX_SLM.md` already plans a small, launch-ready SLM (`adhan-nano`) using the same swaram-token architecture; a 30K-vocabulary kids' model could be a constrained variant of that same model rather than a separate architecture. Confirm which before scaffolding a new training pipeline.
2. **Check whether `yazh-unity`'s "Yazh 30K, on-device ONNX via Barracuda" reference is this repository's deliverable.** If so, the actual requirements (latency <50ms, ONNX export, Barracuda compatibility, COPPA-relevant content constraints) come from `yazh-unity`'s docs, not from a blank slate.
3. **If genuinely a separate effort, scaffold it the way `adhan` was scaffolded**: Phase 0 (foundation), Phase A (CI/CD) before any model code, per the pattern in `adhan`'s own roadmap — don't skip straight to training code in an unstructured repo.
4. **Apply the same non-negotiables as every other Yazhi model repo**: no cloud dependency by default, sovereign/local-first training and inference, content and vocabulary constraints suitable for children (COPPA-equivalent posture, matching `yazh-unity`'s existing compliance docs).
5. **Name the vocabulary constraint precisely before training anything.** "30K vocabulary" needs a defined source list (age-appropriate corpus, curated word list, or a filtered slice of `adhan`'s own corpus) — pick one and document it before collecting data.
6. **Write the roadmap and README first**, mirroring `adhan`'s structure (`ROADMAP_JAX_SLM.md`-style phase plan, `docs/ARCHITECTURE_*.md`), so contributors don't hit an empty repo with no orientation the way this skill's own research did.

## Next actions

1. Founder decision: is `yazh-kutty` a constrained variant of `adhan-nano`, the same model referenced as "Yazh 30K" in `yazh-unity`, or a genuinely separate model?
2. Once scoped, write a roadmap document before any training code, following `adhan`'s Phase 0/A pattern.
3. Define the 30K-word vocabulary source explicitly — don't proceed with an implicit or undocumented word list.
4. If distinct from `adhan`, decide whether it reuses `adhan`'s swaram tokenizer or needs its own — reusing avoids a second from-scratch Tamil tokenizer effort.

## Anti-patterns

- **Starting training code before resolving the `adhan-nano` / "Yazh 30K" overlap** — risks building a second small Tamil model in parallel with one that may already cover this need.
- **Assuming "for kids" only means smaller vocabulary** — content safety, age-appropriateness, and COPPA-equivalent constraints (already documented for `yazh-unity`) matter as much as vocabulary size for a model aimed at children.
- **Building a second from-scratch Tamil tokenizer** instead of reusing `adhan`'s swaram tokenizer, when nothing about a smaller vocabulary requires a different tokenization scheme.
- **Treating the empty repository as a blank check for architecture choices** without confirming scope with the founder first — this is the one Yazhi repo where the next contributor has the least existing constraint to anchor to, which makes an unscoped start the most expensive mistake to walk back.

Cross-reference `yazhi-org-status` for the ecosystem-wide picture, `adhan-status` for the swaram-tokenizer and nano-tier training pipeline this likely builds on, and `yazh-unity-status` for the "Yazh 30K" on-device model reference.
