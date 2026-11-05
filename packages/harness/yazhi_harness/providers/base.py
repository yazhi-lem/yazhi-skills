"""Providers: anything that turns a prompt into text.

The harness never imports a model library. A provider is a small adapter, so
the same suite runs against a local JAX checkpoint, a served OpenAI-compatible
endpoint, or a recorded fixture without changing a single case file.

Built-in kinds: ``fixture`` (offline), ``openai`` (any OpenAI-compatible
``/chat/completions`` endpoint), ``sample`` (the shipped demo responses).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, runtime_checkable

from ..types import ModelOutput


@runtime_checkable
class Provider(Protocol):
    name: str

    def generate(self, prompt: str) -> ModelOutput: ...


class ProviderError(RuntimeError):
    pass


def run_cases(provider: Provider, prompts: Sequence[str]) -> List[ModelOutput]:
    """Call ``provider.generate`` on each prompt, timing each call."""
    outputs: List[ModelOutput] = []
    for prompt in prompts:
        start = time.perf_counter()
        try:
            output = provider.generate(prompt)
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            outputs.append(ModelOutput(text="", error=f"{type(exc).__name__}: {exc}"))
            continue
        if output.latency_ms is None:
            output.latency_ms = (time.perf_counter() - start) * 1000.0
        outputs.append(output)
    return outputs


class FixtureProvider:
    """Replays recorded outputs keyed by prompt (or by case fingerprint).

    Used for deterministic tests and for re-scoring a recorded run without
    re-calling a model. A missing prompt is an explicit error, never empty text.
    """

    name = "fixture"

    def __init__(self, path: str | Path) -> None:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        responses = payload.get("responses") or payload
        if isinstance(responses, list):
            # Accept [{"id": ..., "prompt": ..., "response": ...}] as well.
            self._by_prompt = {
                row["prompt"]: row.get("response", "") for row in responses if "prompt" in row
            }
        elif isinstance(responses, dict):
            self._by_prompt = {str(k): str(v) for k, v in responses.items()}
        else:
            raise ProviderError(f"{path}: expected a mapping or list of responses")

    def generate(self, prompt: str) -> ModelOutput:
        if prompt not in self._by_prompt:
            return ModelOutput(text="", error="fixture has no recorded response for this prompt")
        return ModelOutput(text=self._by_prompt[prompt])


class CallableProvider:
    """Adapt any ``fn(prompt) -> str`` (a model, a mock, another API)."""

    name = "callable"

    def __init__(self, fn: Callable[[str], str], name: Optional[str] = None) -> None:
        self._fn = fn
        if name:
            self.name = name

    def generate(self, prompt: str) -> ModelOutput:
        text = self._fn(prompt)
        if not isinstance(text, str):
            raise ProviderError(f"provider returned {type(text).__name__}, expected str")
        return ModelOutput(text=text)
