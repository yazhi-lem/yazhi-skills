"""Command line: ``python3 -m yazhi_harness.cli <command>``.

Commands map to the moments an evaluation happens:

  run        score a model on suites and write a report (exit code = gate)
  calibrate  measure judge-vs-human agreement before trusting a judge
  snapshot   fetch + verify datasets into a pinned local copy
  list       show suites, languages and what is available offline
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__, langs
from .config import ConfigError, load_config, run_config_from_dict
from .datasets import LOADERS, default_root, manifest_digest, snapshot, verify
from .report import render_ci_summary, render_json, render_markdown
from .safety.calibration import calibration_probes
from .safety.judge import LanguageAwareJudge, calibrate
from .suites import SUITES


def _build_config(args) -> "object":
    from .config import ProviderConfig

    data = {}
    if args.config:
        data.update(load_config(args.config))
    if args.provider:
        data["provider"] = {"kind": args.provider}
    if args.base_url:
        provider = dict(data.get("provider") or {"kind": "openai"})
        provider["base_url"] = args.base_url
        data["provider"] = provider
    if args.model:
        data["model"] = args.model
        if data.get("provider"):
            data["provider"] = {**data["provider"], "model": args.model}
    if args.suite:
        data["suites"] = args.suite
    if args.language:
        data["languages"] = args.language
    if args.limit is not None:
        data["limit"] = args.limit
    if args.no_judge:
        data["judge"] = {"enabled": False}
    if args.data_root:
        data["dataset_root"] = args.data_root
    if args.min_score is not None:
        data["gate_min_score"] = args.min_score
    if not data:
        raise ConfigError("nothing to run: pass --suite (and maybe --provider)")
    if "provider" not in data:
        data["provider"] = {"kind": "sample"}
    config = run_config_from_dict(data)
    if not config.suites:
        config.suites = ["sample"]
    return config


def _cmd_run(args) -> int:
    from .runner import run as run_suites

    try:
        config = _build_config(args)
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 3
    report = run_suites(config)
    graded = sum(1 for s in report.suites for r in s.results if r.outcome in ("pass", "fail"))
    if graded == 0:
        print(
            "error: no case could be graded (every provider call failed); "
            "refusing to report a verdict — check the provider/endpoint",
            file=sys.stderr,
        )
        return 5
    markdown = render_markdown(report)
    out = Path(args.output) if args.output else (Path(config.output) if config.output else None)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.suffix.lower() == ".json":
            out.write_text(render_json(report), encoding="utf-8")
        else:
            out.write_text(markdown + "\n", encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    print(markdown)
    return report.exit_code()


def _cmd_calibrate(args) -> int:
    from .providers import build_provider

    options = {"base_url": args.base_url} if args.base_url else {}
    if args.model:
        options["model"] = args.model
    provider = build_provider(args.provider or "openai", options)
    judge = LanguageAwareJudge(provider)
    result = calibrate(judge, calibration_probes(), min_accuracy=args.min_accuracy)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    print(
        f"\nagreement {result.agreement:.2f} ({result.n} probes), bar {args.min_accuracy} "
        f"-> {'ACCEPT' if result.passed else 'REJECT'}",
        file=sys.stderr,
    )
    return 0 if result.passed else 4


def _cmd_snapshot(args) -> int:
    aliases = {"qa": "indicqa"}
    requested = [aliases.get(n, n) for n in (args.dataset or [])]
    names: List[str] = requested or (list(LOADERS) if args.all else [])
    if not names:
        print("pass a dataset name or --all", file=sys.stderr)
        return 3
    for name in names:
        if args.verify:
            problems = verify(name, args.data_root)
            status = "ok" if not problems else "; ".join(problems)
            print(f"{name}: {status}")
            continue
        languages = args.language or None
        path = snapshot(name, args.data_root, languages=languages)
        digest = manifest_digest(name, args.data_root)
        print(f"{name}: wrote {path} (manifest {digest})")
    return 0


def _cmd_list(args) -> int:
    root = args.data_root or default_root()
    print(f"yazhi-harness {__version__}")
    print(f"data root: {root}\n")
    print("suites:")
    for name, suite in sorted(SUITES.items()):
        available = "ready" if suite.available(root) else "needs snapshot"
        judge = " +judge" if suite.needs_judge else ""
        print(f"  {name:12s} {available:14s}{judge}  {suite.description}")
    print("\nlanguages:")
    for code, language in langs.LANGUAGES.items():
        print(f"  {code:3s} {language.code:4s} {language.label} [{language.script}]")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yazhi-harness",
        description="Multilingual evaluation for Indian-language AI (Yazhi + Araṃ harnesses).",
    )
    parser.add_argument("--version", action="version", version=f"yazhi-harness {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="score a model and write a report")
    run_p.add_argument("--config", help="YAML or JSON run config")
    run_p.add_argument("--provider", help="provider kind: sample, fixture, openai")
    run_p.add_argument("--base-url", help="OpenAI-compatible base URL, e.g. http://127.0.0.1:8080/v1")
    run_p.add_argument("--model", help="model name (provider + report label)")
    run_p.add_argument("--suite", action="append", help="suite name (repeatable)")
    run_p.add_argument("--language", action="append", help="language code (repeatable)")
    run_p.add_argument("--limit", type=int, help="max cases per language")
    run_p.add_argument("--data-root", help="dataset snapshot root")
    run_p.add_argument("--min-score", type=float, help="gate: mean score below this fails")
    run_p.add_argument("--no-judge", action="store_true", help="disable the LLM judge")
    run_p.add_argument("--output", help="report path (.md or .json)")
    run_p.set_defaults(func=_cmd_run)

    cal_p = sub.add_parser("calibrate", help="measure judge agreement before trusting it")
    cal_p.add_argument("--provider", default="openai")
    cal_p.add_argument("--base-url")
    cal_p.add_argument("--model")
    cal_p.add_argument("--min-accuracy", type=float, default=0.8)
    cal_p.set_defaults(func=_cmd_calibrate)

    snap_p = sub.add_parser("snapshot", help="download and pin datasets")
    snap_p.add_argument("dataset", nargs="*", help="dataset names: " + ", ".join(LOADERS))
    snap_p.add_argument("--all", action="store_true", help="every dataset")
    snap_p.add_argument("--language", action="append", help="limit to these languages")
    snap_p.add_argument("--data-root")
    snap_p.add_argument("--verify", action="store_true", help="re-hash an existing snapshot")
    snap_p.set_defaults(func=_cmd_snapshot)

    list_p = sub.add_parser("list", help="show suites, languages and dataset availability")
    list_p.add_argument("--data-root")
    list_p.set_defaults(func=_cmd_list)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
