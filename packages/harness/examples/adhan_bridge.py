"""Bridge: run the multilingual Araṃ suite against a local adhan checkpoint.

The adhan repo ships a Tamil-only ``AramHarness`` bound to JAX model objects.
This bridge shows the reverse direction: expose adhan's generation as a plain
callable so the *multilingual* suite can grade it. Nothing here imports the
adhan package; point ``--adhan`` at a checkout and it loads lazily.

    python3 examples/adhan_bridge.py --adhan ../../../adhan \
        --checkpoint checkpoints/adhan-nano-ta --languages ta

It prints the same report the CLI produces. If JAX or the checkpoint is absent
it exits with a clear message instead of a stack trace.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from yazhi_harness.config import run_config_from_dict  # noqa: E402
from yazhi_harness.providers.base import CallableProvider  # noqa: E402
from yazhi_harness.report import render_markdown  # noqa: E402
from yazhi_harness.runner import run  # noqa: E402


def make_generator(adhan_root: Path, checkpoint: str, max_tokens: int):
    """Return ``callable(prompt) -> str`` backed by adhan's model code."""
    try:
        sys.path.insert(0, str(adhan_root / "src"))
        from adhan_slm.inference import generate  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - depends on local checkout
        raise SystemExit(
            f"cannot import adhan inference from {adhan_root}: {exc}\n"
            "pass --adhan <path to the adhan checkout> or run the harness against "
            "an HTTP server instead (provider kind: openai)."
        )

    path = adhan_root / checkpoint
    if not path.exists():
        raise SystemExit(f"checkpoint not found: {path}")

    def generate_text(prompt: str) -> str:
        return generate(prompt, checkpoint=str(path), max_new_tokens=max_tokens)

    return generate_text


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Grade an adhan checkpoint with the Araṃ suite.")
    parser.add_argument("--adhan", default="../../../adhan", help="path to the adhan checkout")
    parser.add_argument("--checkpoint", default="checkpoints/adhan-nano-ta")
    parser.add_argument("--languages", nargs="*", default=["ta"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    adhan_root = Path(args.adhan).resolve()
    generator = make_generator(adhan_root, args.checkpoint, args.max_tokens)
    config = run_config_from_dict(
        {
            "model": args.checkpoint,
            "provider": {"kind": "sample"},  # overridden below
            "suites": ["aram"],
            "languages": args.languages,
            "limit": args.limit,
        }
    )
    report = run(config, provider=CallableProvider(generator, name="adhan"))
    markdown = render_markdown(report)
    print(markdown)
    if args.output:
        Path(args.output).write_text(markdown + "\n", encoding="utf-8")
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
