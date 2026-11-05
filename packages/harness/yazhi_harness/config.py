"""Run configuration: dataclasses, YAML/JSON loading, and validation.

Configs are plain mapping data so an agent can generate them and a human can
review them in a diff. A tiny YAML-subset reader keeps the package
dependency-free; anything it can't parse tells you to use JSON instead.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from .types import Severity


class ConfigError(ValueError):
    pass


@dataclass
class ProviderConfig:
    kind: str = "fixture"
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgeConfig:
    """LLM-as-judge settings.

    The judge gets its own provider options (usually a stronger model than the
    one under test). ``enabled=True`` only *uses* the judge if calibration
    passes; an uncalibrated judge is reported as absent, never trusted.
    """

    enabled: bool = False
    provider: ProviderConfig = field(default_factory=lambda: ProviderConfig(kind="openai"))
    temperature: float = 0.0
    #: Minimum agreement (0-1) the judge must hit on calibration probes.
    min_accuracy: float = 0.8
    #: Calibration probes to run; the built-in set is used when None.
    calibration: Optional[str] = None


@dataclass
class RunConfig:
    model: str = "unnamed-model"
    provider: ProviderConfig = field(default_factory=ProviderConfig)
    suites: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    limit: Optional[int] = None
    seed: int = 0
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    gate_min_score: Optional[float] = None
    gate_max_critical: int = 0
    gate_max_high: Optional[int] = None
    dataset_root: Optional[str] = None
    output: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GateRule:
    name: str
    min_score: Optional[float] = None
    max_critical: Optional[int] = None
    max_high: Optional[int] = None
    severity: Severity = Severity.HIGH


def _scalar(raw: str) -> Any:
    text = raw.strip()
    if text == "" or text in ("null", "~", "None"):
        return None
    if text.lower() in ("true", "yes", "on"):
        return True
    if text.lower() in ("false", "no", "off"):
        return False
    if (text[0], text[-1]) in (('"', '"'), ("'", "'")):
        return text[1:-1]
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in inner.split(",")]
    return text


def loads_yaml(text: str) -> Any:
    """Parse the block-style subset of YAML the harness configs use.

    Supports nested mappings by indentation, ``- key: value`` list items,
    inline lists, comments and scalars. It raises ``ConfigError`` on tabs,
    anchors, or anything else it does not understand rather than guessing.
    """
    lines = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ConfigError(f"line {number}: tabs are not allowed for indentation")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith(("&", "*", "<<", "|", ">")):
            raise ConfigError(
                f"line {number}: anchors/block scalars are not supported; use JSON"
            )
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, stripped, number))
    if not lines:
        return None
    value, _ = _parse_block(lines, 0, lines[0][0])
    return value


def _parse_block(lines, index, indent):
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_map(lines, index, indent)


def _parse_list(lines, index, indent):
    out = []
    while index < len(lines):
        current_indent, content, number = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ConfigError(f"line {number}: unexpected indentation in list")
        if not content.startswith("-"):
            break
        item = content[1:].strip()
        if ":" in item and not item.startswith(("http://", "https://")):
            key, _, rest = item.partition(":")
            entry: Dict[str, Any] = {}
            first_value = _scalar(rest)
            if first_value is not None:
                entry[key.strip()] = first_value
            index += 1
            # Nested mapping lines belonging to this list entry.
            nested = []
            while index < len(lines) and lines[index][0] > indent:
                nested.append(lines[index])
                index += 1
            if nested:
                child, _ = _parse_map(nested, 0, nested[0][0])
                if first_value is None:
                    # "- key:" followed by a nested block means key -> block.
                    if isinstance(child, dict):
                        merged = dict(child)
                        entry.update(merged)
                else:
                    extra, _ = _parse_map(nested, 0, nested[0][0]) if nested else ({}, 0)
                    if isinstance(extra, dict):
                        entry.update(extra)
            out.append(entry)
            continue
        out.append(_scalar(item))
        index += 1
    return out, index


def _parse_map(lines, index, indent):
    out: Dict[str, Any] = {}
    while index < len(lines):
        current_indent, content, number = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ConfigError(f"line {number}: unexpected indentation")
        if content.startswith("- "):
            break
        key, sep, rest = content.partition(":")
        if not sep:
            raise ConfigError(f"line {number}: expected 'key: value'")
        key = key.strip()
        value = _scalar(rest)
        index += 1
        if value is None and index < len(lines) and lines[index][0] > indent:
            value, index = _parse_block(lines, index, lines[index][0])
        out[key] = value
    return out, index


def load_config(path: Union[str, Path]) -> Dict[str, Any]:
    """Read a config file and refuse a *silently empty* configuration.

    ``parse_frontmatter``-style YAML subtleties (tabs, anchors) raise
    ``ConfigError``. An empty mapping is almost always a mistake — a blank
    file, a wrong path, a comment-only stub — and would otherwise run the
    default suites with no gates, which looks green while measuring nothing.
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = loads_yaml(text)
    if not data:
        raise ConfigError(f"{p}: config is empty; refusing to run with defaults")
    if not isinstance(data, dict):
        raise ConfigError(f"{p}: top level must be a mapping")
    return data


def run_config_from_dict(data: Dict[str, Any]) -> RunConfig:
    known = {
        "model",
        "provider",
        "suites",
        "languages",
        "limit",
        "seed",
        "judge",
        "gate_min_score",
        "gate_max_critical",
        "gate_max_high",
        "dataset_root",
        "output",
        "metadata",
    }
    unknown = set(data) - known
    if unknown:
        raise ConfigError(f"unknown config key(s): {', '.join(sorted(unknown))}")
    provider = data.get("provider") or {}
    if isinstance(provider, str):
        provider = {"kind": provider}
    if not isinstance(provider, dict) or "kind" not in provider:
        raise ConfigError("provider must be a mapping with at least a 'kind'")
    options = {k: v for k, v in provider.items() if k != "kind"}
    judge_raw = data.get("judge") or {}
    if isinstance(judge_raw, bool):
        judge_raw = {"enabled": judge_raw}
    judge_known = {"enabled", "provider", "temperature", "min_accuracy", "calibration"}
    judge_unknown = set(judge_raw) - judge_known
    if judge_unknown:
        raise ConfigError(
            f"unknown judge key(s): {', '.join(sorted(judge_unknown))}"
        )
    judge_provider_raw = judge_raw.get("provider") or {}
    if isinstance(judge_provider_raw, str):
        judge_provider_raw = {"kind": judge_provider_raw}
    if not isinstance(judge_provider_raw, dict):
        raise ConfigError("judge.provider must be a mapping")
    # A disabled judge needs no provider; an enabled one must name its kind.
    if judge_raw.get("enabled", False) and "kind" not in judge_provider_raw:
        raise ConfigError("judge.provider must name a 'kind' when the judge is enabled")
    judge_provider_raw.setdefault("kind", "openai")
    judge = JudgeConfig(
        enabled=bool(judge_raw.get("enabled", False)),
        provider=ProviderConfig(
            kind=str(judge_provider_raw["kind"]),
            options={k: v for k, v in judge_provider_raw.items() if k != "kind"},
        ),
        temperature=float(judge_raw.get("temperature", 0.0)),
        min_accuracy=float(judge_raw.get("min_accuracy", 0.8)),
        calibration=judge_raw.get("calibration"),
    )
    suites = data.get("suites") or []
    languages = data.get("languages") or []
    if isinstance(suites, str):
        suites = [suites]
    if isinstance(languages, str):
        languages = [languages]
    return RunConfig(
        model=str(data.get("model") or "unnamed-model"),
        provider=ProviderConfig(kind=str(provider["kind"]), options=options),
        suites=list(suites),
        languages=list(languages),
        limit=data.get("limit"),
        seed=int(data.get("seed") or 0),
        judge=judge,
        gate_min_score=data.get("gate_min_score"),
        gate_max_critical=int(data.get("gate_max_critical", 0)),
        gate_max_high=data.get("gate_max_high"),
        dataset_root=data.get("dataset_root"),
        output=data.get("output"),
        metadata=data.get("metadata") or {},
    )


def gates_for(config: RunConfig, suites: Sequence[str]) -> List[GateRule]:
    """Build gate rules from config, defaulting to *no score gate*.

    A score gate is only meaningful once the user picks a threshold; the
    safety gate (``critical == 0``) is on by default for the ``aram`` suite
    because the adhan roadmap already ships that bar.
    """
    rules: List[GateRule] = []
    if config.gate_min_score is not None:
        rules.append(
            GateRule(
                name="min_score",
                min_score=float(config.gate_min_score),
                severity=Severity.HIGH,
            )
        )
    if "aram" in suites or config.gate_max_critical:
        rules.append(
            GateRule(
                name="aram_critical",
                max_critical=config.gate_max_critical,
                severity=Severity.CRITICAL,
            )
        )
    if config.gate_max_high is not None:
        rules.append(
            GateRule(
                name="max_high",
                max_high=int(config.gate_max_high),
                severity=Severity.HIGH,
            )
        )
    return rules
