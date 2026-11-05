"""Provider construction from config, plus the built-in demo corpus.

The bundled ``sample`` data lets a fresh clone run the whole pipeline with no
network and no model:

    python3 -m yazhi_harness.cli run --model demo --provider sample --suite sample
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .base import CallableProvider, FixtureProvider, Provider, ProviderError, run_cases
from .openai import OpenAICompatibleProvider

#: packages/harness/data/sample  (providers/ -> yazhi_harness/ -> harness/)
SAMPLE_DIR = Path(__file__).resolve().parents[2] / "data" / "sample"


class _SampleProvider(FixtureProvider):
    """Recorded responses shipped with the package (deliberately imperfect)."""

    name = "sample"

    def __init__(self) -> None:
        super().__init__(SAMPLE_DIR / "sample_responses.json")


_OPENAI_KEYS = {"temperature", "max_tokens", "timeout", "system_prompt", "api_key_env", "api_key", "think"}


def build_provider(kind: str, options: Dict[str, Any]) -> Provider:
    """Construct a provider from ``provider.kind`` plus its options."""
    kind = kind.strip().lower()
    if kind == "sample":
        return _SampleProvider()
    if kind == "fixture":
        path = options.get("path")
        if not path:
            raise ProviderError("fixture provider needs 'path'")
        return FixtureProvider(path)
    if kind in ("openai", "openai-compatible", "llamacpp", "vllm"):
        passthrough = {k: v for k, v in options.items() if k in _OPENAI_KEYS}
        return OpenAICompatibleProvider(
            base_url=options.get("base_url") or "http://127.0.0.1:8080/v1",
            model=options.get("model") or "local",
            extra_body=options.get("extra_body") or {},
            **passthrough,
        )
    raise ProviderError(f"unknown provider {kind!r}; known: sample, fixture, openai")


__all__ = [
    "CallableProvider",
    "FixtureProvider",
    "OpenAICompatibleProvider",
    "Provider",
    "ProviderError",
    "SAMPLE_DIR",
    "build_provider",
    "run_cases",
]
