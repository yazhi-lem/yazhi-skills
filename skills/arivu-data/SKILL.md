---
name: arivu-data
description: FDE Data & AI. Data pipeline scraping, Project Madurai parsing, GGUF quantization, and dataset pre-training formats for offline AI models.
---

# Arivu Data Skill

## Overview
This skill implements the capabilities of Arivu, a Forward Deployed Engineer specialized in data intelligence, scraping, and LLM data compilation. It focuses on harvesting, cleaning, and preparing high-quality Tamil linguistic corpus files (e.g., Tolkappiyam, Sangam Literature) for model pre-training and fine-tuning.

## Core Capabilities
1. **Sovereign Text Ingestion**:
   - Write custom Python scrapers targeting classical archives (e.g., Project Madurai) without relying on bloated scraping frameworks.
   - Clean raw UTF-8 text files by removing markup, editor notes, and encoding artifacts.
2. **LLM Pre-training Pipelines**:
   - Parse classical grammar rules into structured ChatML formatting.
   - Segment text datasets into high-density tokens for continuous pre-training (CPT).
3. **Edge AI Optimization**:
   - Quantize model checkpoints to GGUF format using `llama.cpp` tools.
   - Benchmark model inference speed and memory footprints on edge hardware.

## Workflows
- **Ingest & Sanitize Corpus**:
  1. Fetch raw text data via stream-based Python requests.
  2. Apply regex filters to remove editorial annotations and non-text characters.
  3. Validate UTF-8 compliance and write to local SQLite database or compressed text file.
- **Quantization Pipeline**:
  1. Convert PyTorch/Safetensors weights to GGUF format.
  2. Run quantization (e.g., Q4_K_M or Q8_0) to fit RAM ceilings.
