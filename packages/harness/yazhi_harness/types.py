"""Core data types shared by every harness, runner, and scorer.

The harness is deliberately model-agnostic: a *case* is language-tagged data,
an *output* is whatever a provider returned, and a *result* is the graded
verdict. Nothing in this module imports a model library.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence


class Severity(str, Enum):
    """How much a failure matters. Ordered low -> critical."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def rank(self) -> int:
        return _SEVERITY_ORDER.index(self)

    def __lt__(self, other: "Severity") -> bool:  # type: ignore[override]
        return self.rank < other.rank


_SEVERITY_ORDER: List[str] = [
    Severity.INFO.value,
    Severity.LOW.value,
    Severity.MEDIUM.value,
    Severity.HIGH.value,
    Severity.CRITICAL.value,
]


def max_severity(values: Iterable[Severity], default: Severity = Severity.INFO) -> Severity:
    values = list(values)
    return max(values, key=lambda s: s.rank) if values else default


class Outcome(str, Enum):
    """Outcome of one graded case."""

    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"  # provider failure, not a model-quality signal
    SKIP = "skip"  # scorer could not judge (e.g. missing reference)


@dataclass(frozen=True)
class Case:
    """One unit of evaluation: a prompt in one language with optional references.

    ``metadata`` carries anything a scorer needs (context passage, gold label,
    expected behaviour); keys used by the built-in scorers are documented in
    each scorer module.
    """

    id: str
    language: str  # BCP-47-ish tag, e.g. "ta", "hi", "kn-IN"
    prompt: str
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    severity: Severity = Severity.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def base_language(self) -> str:
        """``ta`` from ``ta`` or ``ta-IN``."""
        return self.language.split("-")[0].lower()

    def fingerprint(self) -> str:
        """Stable hash over the things that define the case's identity."""
        payload = json.dumps(
            {
                "id": self.id,
                "language": self.language,
                "prompt": self.prompt,
                "references": self.references,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass
class ModelOutput:
    """A provider's answer to one case."""

    text: str
    latency_ms: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class SampleResult:
    """A graded case."""

    case_id: str
    language: str
    tags: List[str]
    severity: str
    prompt: str
    response: str
    outcome: Outcome
    score: float  # 0.0-1.0, higher is better
    scorer: str
    output_metas: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    latency_ms: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None


@dataclass
class SuiteResult:
    """All graded cases for one suite, plus its metadata."""

    suite: str
    model: str
    results: List[SampleResult]
    language: str = "all"
    scored_by: str = ""
    dataset_license: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.results)


@dataclass
class GateViolation:
    gate: str
    message: str
    severity: Severity = Severity.HIGH


@dataclass
class RunReport:
    """The complete, reproducible record of one harness run."""

    model: str
    provider: str
    suites: List[SuiteResult]
    created_at: str
    duration_sec: float
    harness_version: str
    config_digest: str
    gate_violations: List[GateViolation] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not self.gate_violations

    def exit_code(self) -> int:
        """0 = clean, 1 = CRITICAL violation, 2 = non-critical violation."""
        if not self.gate_violations:
            return 0
        if any(v.severity is Severity.CRITICAL for v in self.gate_violations):
            return 1
        return 2


def _plain(obj: Any) -> Any:
    """Recursively convert dataclasses/enums into JSON-serialisable values."""
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [_plain(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _plain(v) for k, v in asdict(obj).items()}
    return obj


def to_jsonable(obj: Any) -> Any:
    return _plain(obj)


def digest(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(_plain(obj), ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def score_percent(seq: Sequence[float]) -> float:
    return 100.0 * sum(seq) / len(seq) if seq else 0.0
