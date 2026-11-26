---
name: adhan-status
description: Use when working in the adhan repository — the from-scratch Tamil small language model — whether on the tokenizer, the JAX training loop, corpus scraping, or evaluation. Helps you place work in the current phase instead of resuming a pipeline the project already retired.
---

Adhan is Yazhi's Tamil-first language model, built from scratch rather than fine-tuned: `swaram` (uyir–mey / akshara) tokens as the atomic unit, agglutination-aware modeling, trained in JAX/Flax and tracked with MLflow, targeting a small, edge-deployable release. The legacy PyTorch pipeline (Gemma LoRA fine-tuning, XLM-RoBERTa MLM, `sangam_gpt`) has been **removed** — the project now stands entirely on the from-scratch JAX SLM plus the Phase 2 data-collection pipeline. Any reference to LoRA, Gemma, or `sangam_gpt` in an old branch or issue is describing a retired approach.

## Roadmap phases

| Phase | Scope | Status |
|---|---|---|
| 0 — Foundation & scaffolding | Repo structure, base tooling | ✅ Done |
| A — CI/CD | Pipelines, packaging | ✅ Done |
| 1 — Tokenizer to production | Swaram tokenizer hardening | 🚧 In progress |
| 2 — Corpus at pretraining scale | `src/data_scraper/` collection + HF export | 🚧 In progress |
| 3 — Pretrain `adhan-nano` | JAX/Flax training, CPU-first | 🚧 In progress |
| 4 — Evaluation & Tamil-specific probes | `adhan_slm.eval.run_eval` | 📋 Next |
| 5 — Instruct/chat alignment (light) | Post-pretrain tuning | 📋 Planned |
| 6 — Compress & ship light | Launch `adhan-nano` v0.1 | 🚀 Launch target |
| 7 — Scale up | Post-launch | 📋 Planned |

## Workflow

1. **Read [`docs/README.md`](https://github.com/yazhi-lem/adhan/blob/main/docs/README.md) for the current phase** before writing code. The old week-by-week `ROADMAP_JAX_SLM.md` was retired on 2026-11-21; the README and docs index are now the status owners.
2. **Test the tokenizer with no JAX installed first**: `PYTHONPATH=src python -m adhan_slm.tokenizer.swaram_tokenizer "<text>"` — this is the fastest sanity check and needs zero heavy deps.
3. **Prefer the CPU training path unless you have CUDA 12 on Linux.** `pip install -e ".[dev,jax,tamil-nlp]"` gets a working CPU stack on macOS/Windows/CI; only add `jax-gpu` when you actually have the hardware.
4. **Sanity-gate any training change with `--overfit-batch` before a real run** — one batch, loss must collapse — per `docs/training/CPU_TRAINING.md`. Skipping this wastes a full training budget on a wiring bug.
5. **Use `scripts/prepare_slm_corpus.py` to freeze the tokenizer and pack shards** before training; don't hand-roll corpus prep — vocab size (12,000 default) and sequence length (1,024 default) are baked into the frozen tokenizer.
6. **Keep tests at `<module>_tests.py`, one file per module under test** — this is a repo-specific convention, distinct from the singular `<module>_test.py` form used in the yazhi-api repo.
7. **Run `python scripts/run_scraper.py --strategy modern --max-records 80000`** for corpus builds; check `src/data_scraper/merge_corpora.py` before writing a new merge step — one already exists.

## Next actions

1. Finish Phase 3: pretrain `adhan-nano` end-to-end on the CPU nano config (`adhan_slm_nano_cpu.yaml`) with gradient accumulation.
2. Move into Phase 4 — Tamil-specific eval probes via `adhan_slm.eval.run_eval`.
3. Track progress against the repo README and `docs/README.md`, not memory; retired trackers were removed on 2026-11-21 and survive only in git history.
4. Keep `src/core/` shared constants as the single source for anything used across tokenizer, training, and eval — don't reintroduce per-module copies.

## Anti-patterns

- **Reviving the removed PyTorch/LoRA/Gemma pipeline** for a "quick fine-tune" — it was deliberately deleted in favor of the from-scratch JAX approach; resurrecting it forks the project's direction.
- **Skipping the `--overfit-batch` sanity gate** before a full training run — a silent wiring bug (bad loss masking, wrong shard order) burns hours of CPU/GPU time before surfacing.
- **Hand-writing a new corpus merge script** instead of extending `src/data_scraper/merge_corpora.py` — duplicates logic that already handles the merge contract.
- **Training against a GPU-only config on a CPU box** (or vice versa) without checking the config file's `--device` flag — the nano CPU config and default configs are not interchangeable.
- **Treating `test_*.py` as a silent skip.** This repo's pytest config collects `*_tests.py`, `test_*.py` and `*_test.py`; the convention is `<module>_tests.py` for colocated module tests, but a `test_*.py` file still runs. The failure is convention drift, not non-collection.

Cross-reference `yazhi-org-status` for how Adhan fits the rest of the ecosystem, `fine-tuning-workflow` for general pretrain/fine-tune tradeoffs, and `illakiya-status` for the sibling swaram/akshara-level Tamil-input work.
