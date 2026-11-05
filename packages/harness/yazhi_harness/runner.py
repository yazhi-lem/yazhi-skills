"""The runner: config -> provider -> suites -> scores -> report.

Ordering, seeding and truncation are all routed through here so a report can
state exactly what ran. Concurrency is intentionally absent: an on-device or
CPU-served model is the target, where parallel calls distort latency and
memory figures more than they buy time.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Sequence

from . import __version__, langs
from .config import RunConfig, gates_for
from .datasets import manifest_digest
from .datasets.loaders import DatasetUnavailable
from .providers import build_provider, run_cases
from .registry import RegistryError
from .safety.aram import AramScorer
from .safety.constitution import INTENT_TAXONOMY
from .safety.calibration import calibration_probes
from .safety.judge import LanguageAwareJudge, calibrate
from .scorers.base import Score, Scorer
from .scorers.text import get_scorer
from .suites import SUITES, Suite, cases_for
from .types import (
    Case,
    GateViolation,
    Outcome,
    RunReport,
    SampleResult,
    Severity,
    SuiteResult,
    digest,
    max_severity,
    score_percent,
)

#: Above this share of provider errors a suite's numbers mean nothing.
ERROR_RATE_CEILING = 0.10

#: Suite name -> scorer name. ``mixed`` and ``aram`` are handled specially.
SUITE_SCORERS: Dict[str, str] = {
    "flores": "translation",
    "qa": "exact_match",
    "sentiment": "label",
    "paraphrase": "label",
}

_TAG_SCORER = {"translation": "translation", "label": "label", "sample": "mixed"}


def _scorer_for_case(case: Case, suite: Suite, aram: AramScorer) -> Scorer:
    if suite.name == "aram" or "aram" in case.tags:
        return aram  # type: ignore[return-value]
    if suite.name == "sample":
        if "translation" in case.tags:
            return get_scorer("translation")
        if "label" in case.tags:
            return get_scorer("label")
        raise RegistryError(f"sample case {case.id} has no known task tag")
    return get_scorer(SUITE_SCORERS[suite.name])


def run_suite(
    suite: Suite,
    config: RunConfig,
    provider,
    *,
    aram_scorer: Optional[AramScorer] = None,
    judge_configured: bool = False,
) -> SuiteResult:
    languages = config.languages or None
    case_set = cases_for(
        suite.name,
        languages=languages,
        limit=config.limit,
        seed=config.seed,
        root=config.dataset_root,
    )
    if not case_set.cases:
        raise DatasetUnavailable(
            suite.name,
            "loaded zero cases (check --languages and --limit against the snapshot)",
        )
    aram = aram_scorer or AramScorer()
    scorers_by_case = [_scorer_for_case(c, suite, aram) for c in case_set.cases]
    # One provider call per distinct prompt; the same prompt is never billed twice.
    unique_prompts: List[str] = []
    index_of: Dict[str, int] = {}
    for case in case_set.cases:
        if case.prompt not in index_of:
            index_of[case.prompt] = len(unique_prompts)
            unique_prompts.append(case.prompt)
    outputs = run_cases(provider, unique_prompts)

    results: List[SampleResult] = []
    for case, scorer in zip(case_set.cases, scorers_by_case):
        output = outputs[index_of[case.prompt]]
        try:
            score = scorer.score(case, output)
        except Exception as exc:  # noqa: BLE001 - a scorer bug must not crash a run
            score = Score(0.0, "error", [f"scorer {scorer.name} raised {type(exc).__name__}: {exc}"])
        severity = score.severity or case.severity.value
        results.append(
            SampleResult(
                case_id=case.id,
                language=case.language,
                tags=list(case.tags),
                severity=severity,
                prompt=case.prompt,
                response=output.text[:2000],
                outcome=score.outcome,
                score=round(score.value, 4),
                scorer=scorer.name,
                output_metas=dict(score.details),
                notes=list(score.notes),
                latency_ms=output.latency_ms,
                prompt_tokens=output.prompt_tokens,
                completion_tokens=output.completion_tokens,
            )
        )

    missing = case_set.missing_languages
    metadata: Dict[str, object] = {
        "case_count": len(results),
        "unique_prompts": len(unique_prompts),
        "missing_languages": missing,
        "notes": case_set.notes,
        "judge_configured": judge_configured,
        "dataset_manifest": manifest_digest(suite.dataset, config.dataset_root)
        if suite.dataset
        else None,
        "genres": [case_set.provenance.genre],
    }
    if suite.name == "aram":
        metadata["judge_calibrated"] = bool(aram.judge_calibrated and aram.judge is not None)
    return SuiteResult(
        suite=suite.name,
        model=config.model,
        results=results,
        language=",".join(sorted({r.language for r in results})),
        scored_by=", ".join(sorted({r.scorer for r in results})),
        dataset_license=case_set.provenance.license,
        metadata=metadata,
    )


def _is_failure(row: SampleResult) -> bool:
    """A graded, actionable failure — never an infra error or an unjudgeable skip."""
    return row.outcome == Outcome.FAIL.value


def aggregate(suite_result: SuiteResult) -> Dict[str, Dict[str, object]]:
    """Per-language pass rate, mean score and severity counts."""
    by_language: Dict[str, List[SampleResult]] = {}
    for row in suite_result.results:
        by_language.setdefault(row.language, []).append(row)
    table: Dict[str, Dict[str, object]] = {}
    for language, rows in sorted(by_language.items()):
        scored = [r for r in rows if r.outcome != Outcome.ERROR.value]
        table[language] = {
            "n": len(rows),
            "scored": len(scored),
            "pass_rate": round(100.0 * sum(r.outcome == Outcome.PASS.value for r in scored) / max(len(scored), 1), 1),
            "mean_score": round(score_percent([r.score for r in scored]), 1),
            "errors": sum(r.outcome == Outcome.ERROR.value for r in rows),
            "skipped": sum(r.outcome == Outcome.SKIP.value for r in rows),
            "critical": sum(
                r.severity == Severity.CRITICAL.value and _is_failure(r) for r in rows
            ),
            "high": sum(r.severity == Severity.HIGH.value and _is_failure(r) for r in rows),
        }
    return table


def evaluate_gates(
    suites: Sequence[SuiteResult],
    config: RunConfig,
) -> List[GateViolation]:
    rules = gates_for(config, [s.suite for s in suites])
    violations: List[GateViolation] = []
    # Error-rate is checked unconditionally: if the provider is down, every
    # other number in the report is meaningless even when no score gate is set.
    for suite in suites:
        if not suite.results:
            continue
        error_rate = sum(r.outcome == Outcome.ERROR.value for r in suite.results) / len(suite.results)
        if error_rate > ERROR_RATE_CEILING:
            violations.append(
                GateViolation(
                    gate=f"provider_errors/{suite.suite}",
                    message=(
                        f"{error_rate:.0%} of calls failed at the provider level "
                        f"(ceiling {ERROR_RATE_CEILING:.0%}); results are not a model signal"
                    ),
                    severity=Severity.HIGH,
                )
            )
    for rule in rules:
        for suite in suites:
            rows = [r for r in suite.results if r.outcome != Outcome.ERROR.value]
            if rule.min_score is not None:
                mean = score_percent([r.score for r in rows]) / 100.0
                if mean < rule.min_score:
                    violations.append(
                        GateViolation(
                            gate=f"{rule.name}/{suite.suite}",
                            message=f"mean score {mean:.3f} < required {rule.min_score:.3f}",
                            severity=rule.severity,
                        )
                    )
            if rule.max_critical is not None:
                critical = sum(
                    r.severity == Severity.CRITICAL.value and _is_failure(r)
                    for r in suite.results
                )
                if critical > rule.max_critical:
                    violations.append(
                        GateViolation(
                            gate=f"{rule.name}/{suite.suite}",
                            message=f"{critical} CRITICAL failure(s) > allowed {rule.max_critical}",
                            severity=rule.severity,
                        )
                    )
            if rule.max_high is not None:
                high = sum(
                    r.severity == Severity.HIGH.value and _is_failure(r)
                    for r in suite.results
                )
                if high > rule.max_high:
                    violations.append(
                        GateViolation(
                            gate=f"{rule.name}/{suite.suite}",
                            message=f"{high} HIGH failure(s) > allowed {rule.max_high}",
                            severity=rule.severity,
                        )
                    )
    return violations


def _setup_judge(config: RunConfig, judge_provider) -> tuple[Optional[AramScorer], Dict[str, object]]:
    """Build and calibrate the judge; return a scorer plus its calibration record.

    The judge is only trusted when calibration agreement clears
    ``min_accuracy``. A failing or unavailable judge leaves the suite on its
    deterministic floor and the report says so explicitly.
    """
    if not config.judge.enabled or "aram" not in (config.suites or []):
        return AramScorer(), {"enabled": False}
    if judge_provider is None:
        judge_provider = build_provider(
            config.judge.provider.kind, config.judge.provider.options
        )
    judge = LanguageAwareJudge(judge_provider)
    calibration = calibrate(
        judge,
        calibration_probes(),
        min_accuracy=config.judge.min_accuracy,
        judge_name=config.judge.provider.kind,
    )
    record: Dict[str, object] = calibration.to_dict()
    if not calibration.passed:
        return AramScorer(judge=judge, judge_calibrated=False), record
    return AramScorer(judge=judge, judge_calibrated=True), record


def run(config: RunConfig, *, provider=None, judge_provider=None) -> RunReport:
    """Execute every configured suite and return the report."""
    started = time.perf_counter()
    suites = config.suites or ["sample"]
    unknown = [s for s in suites if s not in SUITES]
    if unknown:
        raise RegistryError(f"unknown suite(s) {unknown}; known: {', '.join(sorted(SUITES))}")
    injected = provider is not None
    if not injected and config.provider.kind == "sample" and set(suites) - {"sample", "aram"}:
        raise ValueError(
            "provider 'sample' only has recorded responses for the built-in suites; "
            "use a real provider for dataset suites"
        )
    if not injected:
        provider = build_provider(config.provider.kind, config.provider.options)

    aram_scorer, judge_record = _setup_judge(config, judge_provider)

    results: List[SuiteResult] = []
    for name in suites:
        results.append(
            run_suite(
                SUITES[name],
                config,
                provider,
                aram_scorer=aram_scorer,
                judge_configured=bool(config.judge.enabled) and name == "aram",
            )
        )

    report = RunReport(
        model=config.model,
        provider=config.provider.kind,
        suites=results,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        duration_sec=round(time.perf_counter() - started, 2),
        harness_version=__version__,
        config_digest=digest(config),
        gate_violations=evaluate_gates(results, config),
        metadata={
            "seed": config.seed,
            "limit": config.limit,
            "languages": config.languages,
            "judge": judge_record,
        },
    )
    return report
