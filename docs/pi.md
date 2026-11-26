# Using yazhi-skills with Pi

Status: current · Owner: Vajra · Verified: 2026-11-25 against `main`
Scope: How to install and invoke these skills in the Pi coding agent.

Every skill here is a plain directory containing `SKILL.md`, which is the
portable form Pi implements (the Agent Skills specification). Nothing in this
repo is Claude-specific: the `.claude-plugin/` manifest is only one install
path. This page covers the Pi path.

## Install

Three ways, in order of preference.

### 1. Installer (recommended)

```bash
git clone https://github.com/yazhi-lem/yazhi-skills
cd yazhi-skills

./install.sh --pi            # all skills -> ~/.pi/agent/skills
./install.sh --pi-project    # all skills -> ./.pi/skills (this repo only)
./install.sh --pi -c org     # just the org/ category
```

`--pi` symlinks by default; pass `--mode copy` to vendor the files instead.
After installing, restart `pi` or run `/reload`.

### 2. Point Pi at the checkout (no copying)

Add the skills directory to your Pi settings. User settings live in
`~/.pi/agent/settings.json`; project settings in `.pi/settings.json`.

```json
{
  "skills": ["~/Yazhi/repos/yazhi-lem/yazhi-skills/skills"]
}
```

Resource paths in user settings resolve from the agent directory and support
`~`; in project settings they resolve from the project `.pi` directory. Editing
the skill in the checkout takes effect on the next `/reload`.

### 3. Copy into a project

```bash
./install.sh --pi-project --mode copy
```

Commit `.pi/skills/` if the project should carry its own copy. Prefer
`--pi-project` without `--mode copy` when you want the skills to track the
checkout.

## Invoke

Pi advertises every skill's name and description in the system prompt and loads
the full instructions only when the task matches. You can force a skill:

```text
/skill:yazhi-daily-rhythm
/skill:yazhi-ops
/skill:org-impactful-pr
```

`enableSkillCommands` (default on) controls whether skills appear in command
discovery. Set `disable-model-invocation: true` in a skill's frontmatter to make
it command-only — not used here, because every skill in this repo is meant to be
selectable by the model.

## Yazhi extension

The repo ships a small [Yazhi extension](../extensions/yazhi/README.md) that queues `/skill:yazhi-code-orient`, `/skill:yazhi-purpose-gate`, and `/skill:yazhi-review` through `/yazhi-start`, `/yazhi-purpose`, and `/yazhi-review`. It also confirms dangerous shell commands, blocks writes to protected paths, and warns before switching sessions with uncommitted work.

```bash
mkdir -p ~/.pi/agent/extensions
ln -s "$PWD/extensions/yazhi" ~/.pi/agent/extensions/yazhi
```

Run `/reload` after installing. Project-local copies load only after project trust is granted; the extension does not make project agents or extensions safe.

## The daily rhythm in Pi

Two skills form the day loop and are designed to be invoked explicitly:

| Skill | When | What it gives you |
|---|---|---|
| `yazhi-daily-rhythm` | Start of day, or when a day goes sideways | Four blocks, three boundaries, the recovery path |
| `yazhi-ops` | Weekly review, monthly gate, or when work slips | The four loops and the escalation ladder |

A typical morning in Pi:

```text
/skill:yazhi-daily-rhythm
read the digest and set today's one outcome
```

Then work the deep block, and at the end of the day:

```text
/skill:yazhi-daily-rhythm
close the day: update status, set tomorrow's first move
```

## Notes and limits

- **Frontmatter stays two keys.** Every skill declares only `name` and
  `description`, so it loads in Pi, Claude Code, and any other Agent Skills host.
  Pi accepts extra portable fields (`license`, `compatibility`,
  `allowed-tools`), but the repo's validator rejects them to keep the contract
  uniform. Add a field only if you also relax `scripts/lib_skills.py`.
- **Name collisions keep the first discovered skill.** Pi warns on stderr and
  keeps the first one found. If you install both `--pi` and `--pi-project`, the
  project copy wins in that project.
- **`/reload` after editing.** Pi caches skill metadata at startup; a changed
  `SKILL.md` needs `/reload` before the new description is routed.
- **Project skills require trust.** Pi loads `.pi/skills/` only after project
  trust is granted; review unfamiliar skills before approving.
- **Bundles are not needed.** `dist/*.skill` archives are for hosts that import a
  single archive. Pi reads the directory tree directly, so install from
  `skills/` and ignore `dist/`.

See `README.md` for the Claude Code plugin path and the full catalog.
