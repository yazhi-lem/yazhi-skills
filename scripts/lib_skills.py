"""Shared discovery + frontmatter parsing for the yazhi-skills repo.

Standard library only, Python 3.8+. No YAML dependency: SKILL.md frontmatter is
restricted to two flat string keys (`name`, `description`) by the repo contract,
so a small hand-rolled parser is both sufficient and dependency-free.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"

# Category id -> human-readable title used in README headings and skills.json.
CATEGORY_TITLES: Dict[str, str] = {
    "fde": "Forward-Deployed Engineering",
    "ai-ml": "AI/ML",
    "sovereign": "Sovereign",
    "security": "Security",
    "tamil": "Tamil",
    "computer-use": "Computer Use",
    "tools": "Tools",
    "yazh-life": "Yazh Life Skills",
    "social-media": "Social Media",
}

FRONTMATTER_KEYS = ("name", "description")


class Skill(NamedTuple):
    name: str
    category: str
    path: Path  # absolute path to SKILL.md
    description: str
    body: str

    @property
    def rel_path(self) -> str:
        return self.path.relative_to(REPO_ROOT).as_posix()

    @property
    def dir_name(self) -> str:
        return self.path.parent.name

    @property
    def word_count(self) -> int:
        return len(self.body.split())


class ParseError(Exception):
    pass


def parse_frontmatter(text: str) -> Dict[str, str]:
    """Parse a `---` delimited frontmatter block of flat `key: value` pairs.

    Values may wrap onto continuation lines (indented or not) the way YAML plain
    scalars do; they are joined with a single space.
    """
    if not text.startswith("---"):
        raise ParseError("file does not start with a '---' frontmatter marker")
    lines = text.split("\n")
    closing = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing = i
            break
    if closing is None:
        raise ParseError("frontmatter block is never closed with '---'")

    fields: Dict[str, str] = {}
    current: Optional[str] = None
    for raw in lines[1:closing]:
        if not raw.strip():
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if match and not raw.startswith((" ", "\t")):
            current = match.group(1)
            if current in fields:
                raise ParseError(f"duplicate frontmatter key: {current}")
            fields[current] = match.group(2).strip()
        elif current is not None:
            fields[current] = (fields[current] + " " + raw.strip()).strip()
        else:
            raise ParseError(f"cannot parse frontmatter line: {raw!r}")
    return fields


def load_skill(skill_md: Path) -> Skill:
    text = skill_md.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    for key in FRONTMATTER_KEYS:
        if key not in fields:
            raise ParseError(f"missing required frontmatter key: {key}")
    extra = sorted(set(fields) - set(FRONTMATTER_KEYS))
    if extra:
        raise ParseError(f"unexpected frontmatter key(s): {', '.join(extra)}")
    body = text.split("\n---", 1)[1].split("\n", 1)[1] if "\n---" in text else ""
    return Skill(
        name=fields["name"],
        category=skill_md.parent.parent.name,
        path=skill_md,
        description=fields["description"],
        body=body,
    )


def discover(skills_root: Path = SKILLS_ROOT) -> List[Skill]:
    """Return every skill under skills/<category>/<name>/SKILL.md, sorted."""
    found = sorted(skills_root.glob("*/*/SKILL.md"))
    return [load_skill(p) for p in found]


def categories(skills: List[Skill]) -> List[str]:
    """Category ids in a stable order: known ones first, then any new ones."""
    present = {s.category for s in skills}
    known = [c for c in CATEGORY_TITLES if c in present]
    return known + sorted(present - set(known))


def title_for(category: str) -> str:
    return CATEGORY_TITLES.get(category, category.replace("-", " ").title())
