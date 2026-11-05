---
name: arivu-data
description: Use when building or repairing a Tamil corpus pipeline — scraping Project Madurai and similar classical archives, cleaning OCR and encoding artefacts, or quantising a trained checkpoint to GGUF for an offline edge model. Helps you ship a reproducible dataset with provenance instead of a folder of half-cleaned text nobody can re-derive.
---

Arivu owns the path from raw classical text to a trainable, reproducible corpus, and the final step from checkpoint to edge-deployable weights. Two things bite: cleaned text whose provenance is lost (so a bad source cannot be removed later), and a quantisation that fits RAM but destroys Tamil quality.

## Workflow

1. **Fetch with the source URL recorded per document.** Write a manifest row (source URL, licence, fetch date) as you stream each file — retrofitting provenance after a 200 MB scrape is a rewrite.
2. **Record the licence before cleaning.** Project Madurai texts are public-domain Tamil literature, but a scraped aggregator may add claims; never let an unclear licence enter the corpus silently.
3. **Clean in a fixed order**: normalise UTF-8 (NFC), strip HTML/markup, remove editorial notes and page numbers, then collapse whitespace. Out-of-order cleaning breaks Tamil grapheme clusters — see `tamil-aksharas`.
4. **Filter by script, not by ASCII.** Drop documents whose Tamil-script ratio is below 0.8 rather than hand-checking thousands of files.
5. **Deduplicate by normalised hash** before splitting, or near-identical scrape revisions leak test text into training.
6. **Split by document, never by line.** Line-level splits put consecutive verses of one poem on both sides of the split.
7. **Quantise last, and re-run the eval.** Convert to GGUF, then re-measure with `yazhi-harness`; Q4_K_M that costs 8 points of Tamil translation accuracy is a regression, not an optimisation.

## Pipeline stages

| Stage | Tool | Output | Failure looked for |
|---|---|---|---|
| Ingest | `urllib`/`requests`, no framework | Raw files + manifest | Missing provenance |
| Clean | NFC normalise + regex | UTF-8 corpus | Broken aksharas |
| Filter | script-ratio check | Kept/dropped list | Tanglish contamination |
| Dedup | SHA-256 of normalised text | Unique docs | Test leakage |
| Pack | shard writer | `train.bin` / `val.bin` | Off-by-one shard loss |
| Quantise | `llama.cpp` | `Q4_K_M.gguf` | Quality regression |

## Defaults

- Script-ratio floor 0.8; document-level dedup; 99:1 train/val split by document.
- Quantisation candidates: Q4_K_M (default), Q8_0 when RAM allows, never below Q4 for Tamil output.
- Benchmark tokens/s and RSS on the actual target device, not the dev laptop.

## Anti-patterns

- **Cleaning before recording provenance.** You cannot remove a contaminated source you can no longer identify.
- **Regex filtering on ASCII assumptions.** Stripping "non-word" characters destroys Tamil vowel signs; treat the script as letters plus marks.
- **Deduplicating after the split.** Duplicate documents then appear in both train and test, inflating results.
- **Shipping quantised weights without re-evaluating.** The regression is invisible until a user hits it.
- **Trusting an uncleaned scrape as a corpus.** Editor notes and page numbers teach the model noise.

Run the finished model through `yazhi-harness` and `aram-harness` before release; for tokenizer-level design see `tamil-text-processing`, and for general training tradeoffs see `fine-tuning-workflow`.
