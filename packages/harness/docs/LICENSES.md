# Dataset licensing and provenance

The harness ships **no** third-party text. Datasets are fetched by
`python3 -m yazhi_harness.cli snapshot`, which records the URL, SHA-256 and byte
size of every file in a `manifest.json`. Derived slices are never committed.

Licensing was verified against each dataset's card on 2025-11-05. Two upstreams
declare no licence, which is why the harness refuses to redistribute their text.

| Suite | Upstream | Licence | Redistributable | Notes |
|---|---|---|---|---|
| `flores` | [FLORES-101 devtest](https://github.com/facebookresearch/flores) | **CC-BY-SA-4.0** | Yes, with attribution + share-alike | 1,012 human-translated sentences, aligned across 11 Indian languages + English. Share-alike applies to derived datasets, not to your model weights. |
| `qa` | [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | **CC-BY-4.0** | Yes, with attribution | SQuAD-style Wikipedia QA. Includes genuine no-answer questions — the useful part for hallucination testing. **No Urdu file upstream.** |
| `sentiment` | [mteb/IndicSentiment](https://huggingface.co/datasets/mteb/IndicSentiment) (mirror of ai4bharat) | **CC0-1.0** | Yes, unrestricted | Product-review 3-way classification. All 11 languages. |
| `paraphrase` | [ai4bharat/IndicXParaphrase](https://huggingface.co/datasets/ai4bharat/IndicXParaphrase) | **none declared** | Fetch only | ⚠️ No licence file and no card statement. The harness fetches it locally and **does not** commit or redistribute its text. Treat results as research-only until AI4Bharat clarifies. **No Tamil or Urdu file.** |

## Coverage gaps you must not paper over

Verified by listing each upstream's file tree, not assumed from the paper:

- **IndicQA** publishes 11 files and **none for Urdu** (`indicqa.ur.json` is a 404).
- **IndicXParaphrase** publishes 10 files: `as bn gu hi kn ml mr or pa te` — **no Tamil**, no Urdu. Assamese (`as`) is not one of our 11 languages, so 9 usable.
- **FLORES-101** and **IndicSentiment** cover all 11.

The report prints each suite's missing languages in its own section. A suite
that silently grades 9 languages while calling itself "11-language" is the kind
of number this harness exists to prevent.

## Attribution text for published results

When you publish a report produced by these datasets, include:

> Evaluated on FLORES-101 (CC-BY-SA-4.0, Goyal et al. 2021), IndicQA
> (CC-BY-4.0, Doddapaneni et al. 2023), IndicSentiment (CC0, AI4Bharat), and
> IndicXParaphrase (AI4Bharat; licence undeclared).

## Why not IN22 / Samanantar

`ai4bharat/IN22-Gen` is gated and needs an authenticated token; `Samanantar` has
its own restrictive terms. Neither can be snapshotted by an agent without
credentials, so FLORES is the defensible choice for a reproducible default.

## Reproducing a snapshot

```bash
python3 -m yazhi_harness.cli snapshot --all              # ~200 MB into ~/.cache/yazhi-harness/datasets
python3 -m yazhi_harness.cli snapshot flores --verify     # re-hash and confirm nothing drifted
```

If an upstream changes a file, `--verify` reports the mismatch rather than
silently re-baselining your results.
