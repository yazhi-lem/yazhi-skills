---
name: airgapped-llm-deployment
description: Use when an LLM must run in a fully disconnected, classified, or restricted-network environment (defense, government, critical infrastructure, high-security enterprise) with no outbound internet access. Helps you package models, dependencies, and inference serving so the system works offline and can be patched safely over time.
---

Government, defense, and critical-infrastructure environments often mandate that no outbound network path exists at all — not "firewalled," but physically or logically air-gapped — because any connectivity is treated as an exfiltration or intrusion vector. Standard ML tooling assumes live internet access (pip installs, HF Hub downloads, telemetry, license checks), so every dependency must be deliberately vendored and verified before it crosses the gap. Missing this turns a "quick pip install" into weeks of blocked deployment.

## Workflow

1. **Select a model that can legally and technically be exported.** Confirm license terms permit offline/on-prem redistribution inside the secure enclave (see `open-model-selection` for licensing due diligence). Avoid models whose weights are only served via a gated API.
2. **Build a complete bill of materials (BOM).** List every artifact needed: model weights, tokenizer, config files, inference server binary/image, Python/CUDA runtime, OS packages, and any vector DB or RAG index. Nothing implicit — if it's not on the BOM, it doesn't cross the gap.
3. **Package on a connected staging system.** Download weights (safetensors preferred over pickle), pip-vendor all Python wheels (`pip download --no-deps` per pinned version), and build the container image with all deps baked in — no `pip install` at runtime.
4. **Checksum and sign everything.** Generate SHA-256 hashes for every artifact and sign the manifest. This is the control that proves nothing was tampered with in transit across the gap.
5. **Transfer via the approved one-way path** (write-once media, diode, or mediated transfer station) with the receiving side independently verifying checksums before use — never trust the transfer medium.
6. **Deploy with an offline-first inference server** (vLLM, TGI, llama.cpp, Triton — all runnable with `--offline`/no telemetry flags). Disable any built-in phone-home, update-check, or license-ping behavior explicitly; don't assume a flag is off by default.
7. **Validate in the isolated environment** against a held-out eval set before declaring production-ready — the staging environment's behavior is not guaranteed identical.
8. **Define the patch/update cadence.** Treat every future model or dependency update as a repeat of steps 2-6, not a live upgrade. Default to a quarterly re-certification cycle unless the threat model demands faster (e.g., CVE-driven ad hoc cycles).

## Deployment option comparison

| Option | Isolation level | Update friction | Best for |
|---|---|---|---|
| Full air gap (no physical network link) | Highest | Manual media transfer only | Classified/defense workloads |
| Logical air gap (isolated VLAN, one-way diode) | High | Scheduled diode transfer | Critical infrastructure, regulated finance |
| Restricted network (allowlisted egress only) | Medium | Controlled proxy pulls | Regulated enterprise, not classified |
| Sovereign cloud, no air gap | Lower | Normal CI/CD | Data-residency-only requirements (see `sovereign-cloud-architecture`) |

## Anti-patterns

- **Assuming "offline mode" flags disable all network calls** — many ML frameworks still attempt DNS lookups or telemetry pings on startup; verify with a packet capture in an isolated test network before trusting it.
- **Using pickle-based checkpoints** — arbitrary code execution risk on load; require safetensors or an equivalent verified format.
- **Skipping the staging checksum step** — without signed manifests, you cannot prove integrity to an auditor, which defeats the purpose of the air gap.
- **Treating the air-gapped system as "set and forget"** — unpatched CVEs in the inference stack accumulate silently; schedule re-certification even without connectivity.
- **Baking secrets or API keys into the container image "just in case a fallback is needed"** — any embedded credential is a latent connectivity path; keep the enclave genuinely disconnected and manage any required secrets per `secrets-management`.

Cross-reference `open-model-selection` for choosing a model whose license and weight format suit air-gapped export, and `data-residency-compliance` for the regulatory basis that often mandates this deployment mode.
