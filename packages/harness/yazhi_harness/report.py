"""Report rendering: Markdown for humans and CI, JSON for tooling.

Every table states n and where the score came from (dataset, licence, scorer,
judge calibrated or not). A number without provenance is a number you can't
defend, which is the whole point of the harness.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional, Sequence

from . import langs
from .runner import aggregate
from .stats import wilson_interval
from .types import Outcome, RunReport, SampleResult, Severity, SuiteResult, to_jsonable

_LANG_ORDER = list(langs.LANGUAGES)


def _language_label(code: str) -> str:
    language = langs.try_resolve(code)
    return language.label if language else code


def _suite_table(suite: SuiteResult) -> List[str]:
    table = aggregate(suite)
    lines = [
        f"### `{suite.suite}` — {len(suite.results)} cases",
        "",
        f"Scored by `{suite.scored_by}`. Source licence: {suite.dataset_license or 'n/a'}.",
        "",
        "| Language | n | Pass % | Mean (%) | 95% CI | Critical | High | Errors |",
        "|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    for code in sorted(table, key=lambda c: _LANG_ORDER.index(c) if c in _LANG_ORDER else 99):
        row = table[code]
        rows = [r for r in suite.results if r.language == code and r.outcome != Outcome.ERROR.value]
        passes = sum(1 for r in rows if r.outcome == Outcome.PASS.value)
        interval = wilson_interval(passes, len(rows)) if rows else None
        ci = f"{interval.low*100:.0f}–{interval.high*100:.0f}" if interval else "—"
        lines.append(
            f"| {_language_label(code)} | {row['n']} | {row['pass_rate']:.1f} | "
            f"{row['mean_score']:.1f} | {ci} | {row['critical']} | {row['high']} | {row['errors']} |"
        )
    missing = suite.metadata.get("missing_languages") or []
    if missing:
        lines += ["", f"> Not covered by this corpus: {', '.join(missing)}"]
    notes = suite.metadata.get("notes") or []
    for note in notes:
        lines.append(f"> {note}")
    if suite.suite == "aram" and suite.metadata.get("judge_configured"):
        status = "calibrated and used" if suite.metadata.get("judge_calibrated") else "NOT calibrated — deterministic floor only"
        lines += ["", f"> Judge: {status}. Content-quality dimensions are {'graded' if suite.metadata.get('judge_calibrated') else 'not graded'}."]
    return lines


def _failure_block(suite: SuiteResult, limit: int) -> List[str]:
    """Failures are always listed; a green table with hidden failures is a lie."""
    failures = [r for r in suite.results if r.outcome in (Outcome.FAIL.value, Outcome.ERROR.value)]
    if not failures:
        return []
    critical = [r for r in failures if r.severity == Severity.CRITICAL.value]
    other = [r for r in failures if r.severity != Severity.CRITICAL.value]
    lines = ["**Failures:**", ""]
    for row in critical:
        lines.append(f"- 🔴 `{row.case_id}` ({row.language}) — {row.notes[0] if row.notes else row.outcome}")
    for row in other[:limit]:
        detail = "; ".join(row.notes[:2]) if row.notes else row.outcome
        lines.append(f"- ⚪ `{row.case_id}` ({row.language}, {row.severity}) — {detail}")
    if len(other) > limit:
        lines.append(f"- … and {len(other) - limit} more")
    return lines


def render_markdown(report: RunReport, *, max_failure_rows: int = 8) -> str:
    lines = [
        "# Yazhi Harness report",
        "",
        f"- **Model:** `{report.model}` (provider: `{report.provider}`)",
        f"- **When:** {report.created_at} · {report.duration_sec:.1f}s",
        f"- **Harness:** v{report.harness_version} · config digest `{report.config_digest}`",
        f"- **Verdict:** {'✅ PASS' if report.passed else '❌ ' + str(len(report.gate_violations)) + ' gate violation(s)'}",
        "",
    ]
    judge = (report.metadata or {}).get("judge") or {}
    if judge.get("enabled"):
        lines += [
            f"- **Judge:** {judge.get('judge')} — agreement {judge.get('agreement')} "
            f"(bar {judge.get('min_accuracy')}), "
            f"{'accepted' if judge.get('passed') else 'REJECTED: judge not trusted'}",
        ]
    lines.append("")
    for suite in report.suites:
        lines += _suite_table(suite)
        lines.append("")
        block = _failure_block(suite, max_failure_rows)
        if block:
            lines += block + [""]
    if report.gate_violations:
        lines += ["## Gate violations", ""]
        for violation in report.gate_violations:
            lines.append(f"- **{violation.gate}** — {violation.message} ({violation.severity.value})")
        lines.append("")
    return "\n".join(lines)


def render_ci_summary(report: RunReport) -> str:
    """One compact block suitable for ``$GITHUB_STEP_SUMMARY``."""
    lines = [f"## Yazhi Harness · {report.model}", ""]
    for suite in report.suites:
        table = aggregate(suite)
        total = sum(int(row["n"]) for row in table.values())
        critical = sum(int(row["critical"]) for row in table.values())
        lines.append(f"- `{suite.suite}`: {total} cases, {critical} critical")
    if report.gate_violations:
        lines.append("")
        for violation in report.gate_violations:
            lines.append(f"- ❌ **{violation.gate}**: {violation.message}")
    else:
        lines += ["", "✅ all gates passed"]
    return "\n".join(lines)


def to_dict(report: RunReport) -> Dict[str, object]:
    return to_jsonable(report)


def render_json(report: RunReport) -> str:
    return json.dumps(to_dict(report), indent=2, ensure_ascii=False) + "\n"
