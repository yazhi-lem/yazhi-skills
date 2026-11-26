# Collections

Status: current · Owner: Vajra · Verified: 2026-11-27
Scope: Logical split of the skill catalog by audience and domain.

The canonical package layout stays `skills/<category>/<skill-name>/SKILL.md` — that is what Claude, Pi, the plugin manifest, installer, and bundles all read. This directory adds a second, human-facing tree: curated maps that answer "which skills do I need today?" without forcing readers through every category.

| Collection | Guide | Primary audience |
|---|---|---|
| Yazhi operating system | [`yazhi.md`](./yazhi.md) | Maintainers, agents, release owners |
| Engineering | [`engineering.md`](./engineering.md) | Developers, reviewers, FDE |
| Expression | [`expression.md`](./expression.md) | Designers, social/content, GTM |
| Commons | [`commons.md`](./commons.md) | Families, learners, everyday users |
| Indic & multicultural | [`indic.md`](./indic.md) | Tamil/Indic product and language work |

Rules for this tree:

- Collection files are **maps only**. The skill body owns the procedure; a collection never restates it.
- Add a row here when a new audience path emerges, not when a single skill is added.
- Links point to canonical `SKILL.md` paths; never copy a skill into `collections/`.
- Update both the collection map and `docs/choose-a-skill.md` when routing changes.

See [`docs/choose-a-skill.md`](../docs/choose-a-skill.md) for the short task-first front door and [`docs/skills-audit-2026-11-27.md`](../docs/skills-audit-2026-11-27.md) for why overlap is controlled by boundaries rather than deletion.
