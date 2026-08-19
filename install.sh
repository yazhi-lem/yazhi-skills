#!/usr/bin/env bash
# Install yazhi-skills into any tool that reads a flat directory of
# <skill-name>/SKILL.md — Claude Code, Claude Desktop, or your own agent.
#
# Claude Code users can instead install this repo as a plugin:
#   /plugin marketplace add yazhi-lem/yazhi-skills
#   /plugin install yazhi-skills@yazhi-skills
# See README.md. This script exists for everything that isn't a plugin host.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_ROOT/skills"

DEST="${HOME}/.claude/skills"
MODE="symlink"
CATEGORIES=()
FORCE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [options]

Options:
  -d, --dest DIR       Install into DIR (default: ~/.claude/skills)
  -p, --project        Shorthand for --dest ./.claude/skills
  -c, --category NAME  Install only this category (repeatable).
                       One of: ai-ml computer-use fde security sovereign
                               tamil tools yazh-life
  -m, --mode MODE      symlink (default) or copy
  -f, --force          Overwrite existing entries with the same name
  -n, --dry-run        Print what would happen, change nothing
  -l, --list           List available skills and exit
  -h, --help           Show this help

Examples:
  ./install.sh                              # all skills, symlinked into ~/.claude/skills
  ./install.sh -c yazh-life -c tamil        # just those two categories
  ./install.sh --project --mode copy        # vendor into this repo's .claude/skills
  ./install.sh --dest ~/my-agent/skills -m copy
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    -d|--dest)     DEST="$2"; shift 2 ;;
    -p|--project)  DEST="$PWD/.claude/skills"; shift ;;
    -c|--category) CATEGORIES+=("$2"); shift 2 ;;
    -m|--mode)     MODE="$2"; shift 2 ;;
    -f|--force)    FORCE=1; shift ;;
    -n|--dry-run)  DRY_RUN=1; shift ;;
    -l|--list)
      for f in "$SRC"/*/*/SKILL.md; do
        d="$(dirname "$f")"
        printf '%-14s %s\n' "$(basename "$(dirname "$d")")" "$(basename "$d")"
      done
      exit 0 ;;
    -h|--help)     usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$MODE" in
  symlink|copy) ;;
  *) echo "--mode must be 'symlink' or 'copy', got '$MODE'" >&2; exit 2 ;;
esac

if [ "${#CATEGORIES[@]}" -eq 0 ]; then
  for d in "$SRC"/*/; do CATEGORIES+=("$(basename "$d")"); done
fi

for cat in "${CATEGORIES[@]}"; do
  if [ ! -d "$SRC/$cat" ]; then
    echo "no such category: $cat (see ./install.sh --list)" >&2
    exit 2
  fi
done

[ "$DRY_RUN" -eq 1 ] || mkdir -p "$DEST"

installed=0
skipped=0

for cat in "${CATEGORIES[@]}"; do
  for skill_dir in "$SRC/$cat"/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    name="$(basename "$skill_dir")"
    target="$DEST/$name"

    if [ -e "$target" ] || [ -L "$target" ]; then
      if [ "$FORCE" -eq 1 ]; then
        [ "$DRY_RUN" -eq 1 ] || rm -rf "$target"
      else
        echo "skip   $name (already exists; use --force to replace)"
        skipped=$((skipped + 1))
        continue
      fi
    fi

    if [ "$DRY_RUN" -eq 1 ]; then
      echo "would $MODE $cat/$name -> $target"
    elif [ "$MODE" = "symlink" ]; then
      ln -s "${skill_dir%/}" "$target"
    else
      cp -R "${skill_dir%/}" "$target"
    fi
    installed=$((installed + 1))
  done
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo "dry run: $installed skill(s) would be installed into $DEST"
else
  echo "installed $installed skill(s) into $DEST ($MODE), skipped $skipped"
  echo "restart your agent, or run /reload-plugins in Claude Code, to pick them up."
fi
