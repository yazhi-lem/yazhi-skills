"""OpenAI-compatible chat provider — plain ``urllib``, no SDK.

Works against llama.cpp's ``llama-server``, vLLM, Ollama (``/v1``), LM Studio,
Sarvam/OpenRouter/OpenAI gateways, or yazhi-api: anything that serves
``POST {base_url}/chat/completions``. Keeping it dependency-free matters for
air-gapped sovereign deployments, where installing an SDK is not an option.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .base import ProviderError
from ..types import ModelOutput

DEFAULT_TIMEOUT = 120
DEFAULT_MAX_TOKENS = 256


class OpenAICompatibleProvider:
    name = "openai"

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: Optional[str] = None,
        *,
        api_key_env: str = "YAZHI_HARNESS_API_KEY",
        temperature: float = 0.0,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        timeout: float = DEFAULT_TIMEOUT,
        system_prompt: Optional[str] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        think: Optional[bool] = None,
    ) -> None:
        if not base_url:
            raise ProviderError("openai provider needs base_url")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key or os.environ.get(api_key_env, "")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.system_prompt = system_prompt
        self.extra_body = extra_body or {}
        # Ollama honours top-level ``think``; vLLM/llama.cpp use
        # ``chat_template_kwargs.enable_thinking``. Send only when asked so
        # non-reasoning endpoints are unaffected.
        self.think = think

    def _payload(self, prompt: str) -> Dict[str, Any]:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        body: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        # Providers that reject unknown keys (some strict gateways) can be
        # driven without extras; everything else gets them.
        if self.think is not None:
            body["think"] = self.think
            body.setdefault("chat_template_kwargs", {})["enable_thinking"] = self.think
        body.update(self.extra_body)
        return body

    def generate(self, prompt: str) -> ModelOutput:
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(self._payload(prompt), ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "yazhi-harness"},
            method="POST",
        )
        if self.api_key:
            request.add_header("Authorization", f"Bearer {self.api_key}")
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:300]
            return ModelOutput(text="", error=f"HTTP {exc.code}: {detail}")
        except (urllib.error.URLError, TimeoutError) as exc:
            return ModelOutput(text="", error=f"connection failed: {exc}")
        latency = (time.perf_counter() - start) * 1000.0
        try:
            choice = payload["choices"][0]
            message = choice.get("message", {})
            text = message.get("content") or choice.get("text") or ""
            # Reasoning models (Qwen3, DeepSeek, R1) may put the whole answer in
            # a separate field and leave `content` empty — or spend the entire
            # token budget thinking and emit nothing. Keep the trace for
            # debugging, and never report an empty answer as a real response.
            reasoning = (
                message.get("reasoning_content")
                or message.get("reasoning")
                or payload.get("thinking")
                or ""
            )
        except (KeyError, IndexError, AttributeError) as exc:
            return ModelOutput(text="", error=f"unexpected response shape: {exc}", raw=payload or {})
        if not text and reasoning:
            return ModelOutput(
                text="",
                latency_ms=latency,
                raw={"model": payload.get("model"), "finish_reason": choice.get("finish_reason"),
                     "reasoning_omitted": True},
                error=(
                    "model emitted only reasoning and no answer (finish_reason="
                    f"{choice.get('finish_reason')}); increase max_tokens or disable thinking"
                ),
            )
        usage = payload.get("usage") or {}
        return ModelOutput(
            text=text,
            latency_ms=latency,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            raw={
                "model": payload.get("model"),
                "finish_reason": choice.get("finish_reason"),
                "reasoning_preview": reasoning[:500] if reasoning else None,
            },
        )
