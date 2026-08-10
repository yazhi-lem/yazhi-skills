#!/usr/bin/env python3
"""Regenerate skills.json (the machine-readable index) and the plugin manifest's
`skills` paths from what is actually on disk.

Usage:
    python3 scripts/build_index.py           # write the files
    python3 scripts/build_index.py --check    # fail if they are out of date

skills.json is what non-Claude tools read: one flat array of every skill with
its name, category, description, and repo-relative path to the SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib_skills import (  # noqa: E402
    REPO_ROOT,
    categories,
    discover,
    title_for,
)

INDEX_PATH = REPO_ROOT / "skills.json"
MANIFEST_PATH = REPO_ROOT / ".claude-plugin" / "plugin.json"


def build_index() -> dict:
    skills = discover()
    cats = categories(skills)
    return {
        "name": "yazhi-skills",
        "description": "Curated Agent Skills powering Yazhi.",
        "repository": "https://github.com/yazhi-lem/yazhi-skills",
        "license": "GPL-3.0-or-later",
        "skillFormat": "SKILL.md with YAML frontmatter (name, description)",
        "generatedBy": "scripts/build_index.py — do not edit by hand",
        "count": len(skills),
        "categories": [
            {
                "id": cat,
                "title": title_for(cat),
                "path": f"skills/{cat}",
                "count": sum(1 for s in skills if s.category == cat),
            }
            for cat in cats
        ],
        "skills": [
            {
                "name": s.name,
                "category": s.category,
                "path": s.rel_path,
                "description": s.description,
            }
            for s in sorted(skills, key=lambda s: (cats.index(s.category), s.name))
        ],
    }


def build_manifest_skills() -> list[str]:
    return [f"./skills/{cat}/" for cat in sorted({s.category for s in discover()})]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the generated files are out of date",
    )
    args = parser.parse_args()

    index_text = json.dumps(build_index(), indent=2, ensure_ascii=False) + "\n"

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["skills"] = build_manifest_skills()
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    targets = [(INDEX_PATH, index_text), (MANIFEST_PATH, manifest_text)]

    if args.check:
        stale = [
            p.relative_to(REPO_ROOT).as_posix()
            for p, text in targets
            if not p.exists() or p.read_text(encoding="utf-8") != text
        ]
        if stale:
            print(
                "out of date: " + ", ".join(stale) + "\n"
                "run: python3 scripts/build_index.py",
                file=sys.stderr,
            )
            return 1
        print("generated files are up to date")
        return 0

    for path, text in targets:
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
