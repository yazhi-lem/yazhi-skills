#!/usr/bin/env python3
"""Validate every SKILL.md against the repo contract in skills/tools/skill-authoring.

Usage:
    python3 scripts/validate_skills.py [--strict]

Exit code 0 when there are no errors (warnings alone still pass, unless
--strict is given). Run it in CI and before opening a PR.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib_skills import (  # noqa: E402
    CATEGORY_TITLES,
    REPO_ROOT,
    SKILLS_ROOT,
    ParseError,
    discover,
    load_skill,
)

WORD_MIN, WORD_MAX = 350, 850
DESC_MAX = 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors"
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    def error(where: str, msg: str) -> None:
        errors.append(f"{where}: {msg}")

    def warn(where: str, msg: str) -> None:
        warnings.append(f"{where}: {msg}")

    # --- discovery ------------------------------------------------------
    skill_files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    if not skill_files:
        print("no skills found under skills/*/*/SKILL.md", file=sys.stderr)
        return 1

    skills = []
    for path in skill_files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            skills.append(load_skill(path))
        except (ParseError, UnicodeDecodeError) as exc:
            error(rel, str(exc))

    # Anything at the wrong depth would be invisible to the plugin loader.
    for stray in SKILLS_ROOT.glob("*/SKILL.md"):
        error(
            stray.relative_to(REPO_ROOT).as_posix(),
            "skill is one level too shallow; use skills/<category>/<name>/SKILL.md",
        )
    for stray in SKILLS_ROOT.glob("*/*/*/SKILL.md"):
        error(
            stray.relative_to(REPO_ROOT).as_posix(),
            "skill is one level too deep; use skills/<category>/<name>/SKILL.md",
        )

    names: dict[str, str] = {}

    for skill in skills:
        rel = skill.rel_path

        if skill.name != skill.dir_name:
            error(rel, f"name '{skill.name}' != directory '{skill.dir_name}'")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", skill.name):
            error(rel, f"name '{skill.name}' is not kebab-case")
        if skill.name in names:
            error(rel, f"duplicate skill name, also defined in {names[skill.name]}")
        else:
            names[skill.name] = rel

        if not skill.description.startswith("Use when"):
            error(rel, "description must start with 'Use when'")
        if len(skill.description) > DESC_MAX:
            error(rel, f"description is {len(skill.description)} chars (max {DESC_MAX})")
        if skill.description.count(".") < 2:
            warn(rel, "description looks like a single sentence; add what it helps with")

        if skill.category not in CATEGORY_TITLES:
            warn(
                rel,
                f"category '{skill.category}' has no title in scripts/lib_skills.py",
            )

        body = skill.body
        if not re.search(r"^\|.*\|.*$", body, re.M):
            error(rel, "body has no Markdown table")
        if not re.search(r"^\s*1\.\s+\S", body, re.M):
            error(rel, "body has no numbered workflow/checklist")
        if not re.search(r"^#+ .*(Anti-pattern|failure mode)", body, re.M | re.I):
            error(rel, "body has no 'Anti-patterns' / 'failure modes' section")
        if not re.search(r"\d", body):
            warn(rel, "body contains no numbers; prefer concrete defaults")

        words = skill.word_count
        if not WORD_MIN <= words <= WORD_MAX:
            warn(rel, f"body is {words} words (target {WORD_MIN}-{WORD_MAX})")

        # Cross-references in this repo always read "see `other-skill`" or
        # "per `other-skill`", and no skill name contains a digit. Both filters
        # keep inline technical terms (`data-testid`, `iso-8859-1`) out of the
        # check; a future skill name with a digit in it would be skipped here.
        for line in body.splitlines():
            if not re.search(r"\b(see|per)\b", line, re.I):
                continue
            for ref in set(re.findall(r"`([a-z]+(?:-[a-z]+)+)`", line)):
                if ref == skill.name or list(SKILLS_ROOT.glob(f"*/{ref}")):
                    continue
                warn(rel, f"cross-reference `{ref}` matches no skill directory")

        siblings = [p.name for p in skill.path.parent.iterdir() if p.name != "SKILL.md"]
        if siblings:
            warn(rel, f"extra files alongside SKILL.md: {', '.join(sorted(siblings))}")

    # --- repo-level invariants ------------------------------------------
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for skill in skills:
        if skill.rel_path not in readme:
            error("README.md", f"catalog is missing {skill.rel_path}")
    if f"## Catalog ({len(skills)} skills)" not in readme:
        error("README.md", f"catalog heading should read 'Catalog ({len(skills)} skills)'")

    manifest_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        declared = set(manifest.get("skills", []))
        expected = {f"./skills/{c}/" for c in sorted({s.category for s in skills})}
        for missing in sorted(expected - declared):
            error(".claude-plugin/plugin.json", f"'skills' is missing {missing}")
        for extra in sorted(declared - expected):
            error(".claude-plugin/plugin.json", f"'skills' lists unknown path {extra}")
    else:
        error(".claude-plugin/plugin.json", "manifest is missing")

    index_path = REPO_ROOT / "skills.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        indexed = {s["name"] for s in index.get("skills", [])}
        if indexed != set(names):
            error(
                "skills.json",
                "index is stale; regenerate with python3 scripts/build_index.py",
            )

    # --- report ----------------------------------------------------------
    for line in warnings:
        print(f"warning: {line}")
    for line in errors:
        print(f"error: {line}", file=sys.stderr)

    print(
        f"\nchecked {len(skills)} skills in "
        f"{len({s.category for s in skills})} categories: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
