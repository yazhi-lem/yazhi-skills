"""Yazhi Harness — multilingual evaluation for Indian-language AI.

    python3 -m yazhi_harness.cli run --config examples/aram-quick.yaml

Two harnesses ship together:

* **Yazhi Harness** — capability evaluation (translation, QA, classification)
  across 11 Indian languages, model-agnostic via provider adapters.
* **Araṃ Harness** — cultural-safety and alignment evaluation: 12
  constitutional principles, in-language refusal, citation honesty, and an
  LLM judge that is only trusted once calibrated.

Import ``yazhi_harness`` for programmatic use; nothing here imports a model
library, so it runs on a laptop with no GPU and no network.
"""

from __future__ import annotations

__version__ = "1.0.0"

from .config import ConfigError, JudgeConfig, ProviderConfig, RunConfig, load_config, run_config_from_dict
from .langs import LANGUAGES, Language, resolve
from .report import render_json, render_markdown, to_dict
from .runner import run
from .suites import SUITES, cases_for
from .types import Case, ModelOutput, RunReport, SampleResult, Severity, SuiteResult

__all__ = [
    "Case",
    "ConfigError",
    "JudgeConfig",
    "LANGUAGES",
    "Language",
    "ModelOutput",
    "ProviderConfig",
    "RunConfig",
    "RunReport",
    "SUITES",
    "SampleResult",
    "Severity",
    "SuiteResult",
    "__version__",
    "cases_for",
    "load_config",
    "render_json",
    "render_markdown",
    "resolve",
    "run",
    "run_config_from_dict",
    "to_dict",
]
