"""Scorer protocol and result type.

A scorer turns ``(Case, ModelOutput)`` into a ``Score``. Scorers are pure and
deterministic by default so a run is reproducible; the LLM judge is the one
opt-in exception and is labelled as such in every report.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Protocol, runtime_checkable

from ..types import Case, ModelOutput


@dataclass
class Score:
    value: float  # 0.0-1.0
    outcome: str  # "pass" | "fail" | "skip" | "error"
    notes: List[str] = field(default_factory=list)
    details: Dict[str, object] = field(default_factory=dict)
    #: Optional severity override for this specific sample (e.g. a CRITICAL
    #: red-team case that failed is CRITICAL). Defaults to the case severity.
    severity: str | None = None


@runtime_checkable
class Scorer(Protocol):
    name: str

    def score(self, case: Case, output: ModelOutput) -> Score: ...


class ScorerError(Exception):
    pass


def clamp(value: float) -> float:
    return 0.0 if value < 0.0 else 1.0 if value > 1.0 else float(value)


def dims(*args: float) -> float:
    """Character-level F1 (multiset) — the SQuAD-style overlap measure.

    Used for QA answers where the expected answer is a short span and word
    tokenisation is unreliable for agglutinative Indic scripts.
    """
    from collections import Counter

    for text in args:
        if not isinstance(text, str):
            raise ScorerError("dims() expects strings")
    left, right = (Counter(t) for t in args)
    overlap = sum((left & right).values())
    if overlap == 0:
        return 0.0
    precision = overlap / sum(left.values())
    recall = overlap / sum(right.values())
    return 2 * precision * recall / (precision + recall)
