---
name: rag-pipeline-design
description: Use when building or debugging a retrieval-augmented generation system and answers are missing context, hallucinating, or retrieval feels like guesswork. Helps you design chunking, embedding, retrieval, and reranking stages that can be evaluated and tuned independently.
---

RAG quality is really two separate problems wearing one trenchcoat: retrieval quality (did we find the right passages?) and generation quality (did the model use them well?). Most "the RAG answers are bad" complaints are actually retrieval failures, so design and evaluate each stage separately before touching prompts.

## Workflow

1. **Chunk with structure, not just size.** Start with 300-500 token chunks and 10-15% overlap for prose; use 800-1200 tokens for dense technical docs where context matters more than precision. Prefer splitting on headings/paragraphs over fixed-width windows — a chunk that cuts a sentence in half is a retrieval landmine.
2. **Attach metadata at chunk time.** Source, section title, timestamp, and doc ID enable filtering and citation later. Don't bolt this on after the fact.
3. **Pick an embedding model deliberately.** See table below. Default to a strong general-purpose model (e.g., an OpenAI `text-embedding-3-large`-class or a top MTEB open model) unless you have domain-specific data to justify fine-tuning one.
4. **Choose retrieval mode.** Start with hybrid (dense + BM25/sparse) — pure dense retrieval misses exact-match terms (IDs, error codes, names) that sparse retrieval nails. Fuse with reciprocal rank fusion (RRF), not naive score averaging (scales differ).
5. **Rerank top-k.** Retrieve 20-50 candidates with the cheap retriever, then rerank down to 3-8 with a cross-encoder (e.g., `bge-reranker`, Cohere Rerank). This is the single highest-leverage step most pipelines skip.
6. **Budget the context window explicitly.** Decide a token budget for retrieved context (e.g., 2-4k tokens) before you build the prompt template, and truncate/prioritize by rerank score, not insertion order.
7. **Evaluate retrieval in isolation** using recall@k and MRR against a labeled query→relevant-chunk set (see `llm-evaluation` for how to build that set). Don't only look at final answer quality — you can't tell if a bad answer came from bad retrieval or bad generation without this.
8. **Only then tune the generation prompt** (structure, instructions to cite sources, refusal-on-no-context behavior) — see `prompt-engineering`.
9. **Wire up production monitoring** for retrieval latency, empty-result rate, and citation-groundedness once live — see `model-monitoring`.

## Retrieval mode comparison

| Mode | Strengths | Weaknesses | Use when |
|---|---|---|---|
| Dense only | Semantic/paraphrase matches | Misses exact IDs, rare terms | Conversational, paraphrase-heavy queries |
| Sparse (BM25) | Exact match, cheap, interpretable | No semantic generalization | Logs, code, structured docs |
| Hybrid (dense+sparse+RRF) | Best of both, robust | Extra infra, tuning fusion weights | Default for most production RAG |
| Hybrid + reranker | Highest precision at top-k | Added latency (50-200ms) | Anything answer-quality-sensitive |

## Defaults

- Chunk size: 300-500 tokens (prose), 800-1200 (technical/code)
- Overlap: 10-15%
- Retrieve-then-rerank: retrieve 20-50, keep 3-8
- Context budget: 2-4k tokens of retrieved text, leaving headroom for system prompt + few-shot + generation
- Retrieval eval set: minimum 50-100 labeled queries before trusting recall@k numbers

## Anti-patterns

- **Tuning the prompt to fix a retrieval problem.** If the right chunk was never retrieved, no amount of prompt engineering recovers it. Check recall@k first.
- **One-size chunk size for all document types.** A 500-token chunk that's perfect for a blog post will fragment a legal clause or code function. Segment by content type.
- **Naive score-fusion across dense and sparse.** Cosine similarity and BM25 scores live on different scales; averaging them silently favors one retriever. Use RRF or a learned fusion.
- **No reranking step.** Top-k-by-embedding-similarity alone consistently underperforms retrieve-then-rerank in production benchmarks; skipping it is leaving free accuracy on the table.
- **Evaluating only end-to-end answer quality.** Without separating retrieval and generation metrics, debugging is guesswork — see `llm-evaluation` for building the separated eval harness.
