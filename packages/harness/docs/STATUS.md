# Yazhi Harness + Araṃ Harness — handover status

The development environment's shell executor failed mid-task (`UNKNOWN: unknown
error, write` on every `bash` call, including with escalated sandbox
permissions, across the Lead and three separate teammate sessions). File
read/write still work, so the code and docs below are complete; the two items
that need a shell — the final verification re-run and the git commit — are
blocked. Everything below is what was actually done, what was verified, and
what is still open.

## What was delivered

### 1. `packages/harness/` — a working evaluation engine

Stdlib-only Python, no model library imported anywhere. Two harnesses on one
engine:

| Harness | Purpose | Suites | Cases |
|---|---|---|---|
| **Yazhi Harness** | Capability in 11 Indian languages | `flores`, `qa`, `sentiment`, `paraphrase` | 55,551 |
| **Araṃ Harness** | Cultural safety / alignment | `aram` | 198 (18 per language) |

Files: `types.py`, `langs.py`, `config.py`, `registry.py`, `suites.py`,
`runner.py`, `report.py`, `stats.py`, `synthetic.py`, `cli.py`,
`scorers/{base,text}.py`, `safety/{constitution,red_team,judge,aram,calibration}.py`,
`datasets/{loaders,snapshot}.py`, `providers/{base,openai}.py`, plus
`data/sample/sample_responses.json`, `tests/test_harness.py`,
`examples/{aram-quick.yaml,yazhi-multilingual.yaml,adhan_bridge.py}`,
`docs/{LICENSES.md,VALIDATION.md}`, `README.md`.

### 2. Two new skills in yazhi-skills

- `skills/ai-ml/yazhi-harness/SKILL.md` (588 words, validates)
- `skills/ai-ml/aram-harness/SKILL.md` (566 words, validates)

### 3. Eight pre-existing validator errors fixed

The 8 persona skills were sitting at `skills/<name>/SKILL.md` (one level too
shallow, 8 CI errors). Moved to `skills/fde/` via `git mv` and rewritten to meet
the skill contract (trigger-style descriptions, a table, named anti-patterns).
Validator went from **8 errors → 0 errors** across 86 skills.

### 4. Real datasets verified and snapshotted

Fetched into `/home/valav/Yazhi/.scratch/harness-data/` with SHA-256 manifests:
FLORES-101 (CC-BY-SA-4.0), IndicQA (CC-BY-4.0), IndicSentiment (CC0),
IndicXParaphrase (no licence declared → fetch-only, never redistributed).

## Decisions made and why

1. **Build new, don't fork adhan's `AramHarness`.** The existing one takes
   `model`/`params`/`tokenizer` in its constructor and is Tamil-only; generalising
   it meant forking. The new engine is model-agnostic by provider adapter and the
   adhan bridge (`examples/adhan_bridge.py`) grades adhan checkpoints with it.
2. **Datasets fetched, never committed.** Two upstreams have unclear licensing
   (IndicXParaphrase declares none); the repo is GPL-3.0-or-later. Snapshots are
   pinned by hash and produced on demand.
3. **Errors are never passes.** Provider failure → `error`, never `pass`; >10%
   error rate fires a `provider_errors` gate; a run with zero gradeable cases
   exits 5 with no verdict. This was found by an actual bug: an all-error run
   initially printed "✅ PASS".
4. **The judge must earn trust.** Calibrated against 12 hand-labelled probes;
   below 80% agreement its verdicts are ignored and the report says so. An
   uncalibrated judge cannot turn an English compliance answer into a pass.
5. **Coverage gaps printed, not averaged.** IndicQA has no Urdu upstream;
   IndicXParaphrase has no Tamil or Urdu. Verified against file trees, not docs.
6. **Reasoning-model output handled explicitly.** Qwen3 returned text only in a
   `thinking` field with empty `content`; the provider now errors clearly instead
   of recording a blank answer as a response.

## Verified vs unverified — read this before quoting anything

**Verified by actually running commands** (before the executor failed):

| Check | Result |
|---|---|
| `pytest packages/harness/tests -q` | passed, all green at the time it ran |
| `validate_skills.py` | 0 errors, 10 warnings (warnings pre-existing) |
| `build_index.py --check` | "generated files are up to date" |
| `build_skill_bundle.py --per-skill --check` | "87 bundle(s) up to date" |
| Loaders against real snapshots | 55,551 cases parsed; gaps reported correctly |
| Araṃ discrimination | good model 198/198 pass; complying 101 CRITICAL; English-only 110 CRITICAL |
| Translation scorer | exact refs 1.0; English source copy fails |
| Script audit | 0 non-target-script chars in 77 red-team prompts |

**Verified by reading the source only** (after the executor failed, the last two
edits were checked by hand rather than by running):

| Edit | Static check |
|---|---|
| Module-level `from ..scorers.base import Score` in `safety/aram.py` | All six `Score(...)` call sites in `score()` resolve; the annotation no longer needs a `# noqa`. |
| `min_tamil_ratio` → `min_script_ratio` | `_floor()` uses it language-agnostically; no other module passes the old keyword. |
| `runner.py` scorer path | Calls `scorer.score(case, output)` on the scorer protocol and handles its `Score`. |

**Not verified — requires a working shell:**

- The exact pytest count (37 vs 38 is unresolved; all hard-coded counts were
  removed from the docs rather than guessed).
- Any command after the last two source edits (the table above is a static
  check, not a run).
- The full end-to-end CLI demo against the real datasets.
- `git status` / the commit itself — the work is **not committed**.

## Known open items

1. **No real model baseline.** Ollama on this box was too loaded (260 s to load a
   1.7B model; load average 24 on 12 cores). `llama3.2-tamil` answered in 19 s and
   produced genuine Tamil, but echoed prompt instructions — the run was killed by
   the executor failure. A real baseline needs a working shell plus an idle box.
2. **No judge has passed calibration on a real model.** Araṃ currently grades
   language fidelity and the refusal floor only; content quality is ungated.
3. **No native-speaker review** of the 11-language probe text. Script correctness
   is proven; cultural aptness is not.
4. **Araṃ probe depth is 9 intents per language**, not 12 principles × 11. The
   constitution defines 12; the case builder produces 18 cases per language from
   them. Regional sensitivity within a language is not covered.

## Resume checklist (first thing to run when a shell works)

```bash
cd repos/yazhi-skills
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py 2>&1 | tail -3
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_index.py --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_skill_bundle.py --per-skill --check
cd packages/harness
YAZHI_HARNESS_DATA=/home/valav/Yazhi/.scratch/harness-data \
  PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q 2>&1 | tail -12
PYTHONDONTWRITEBYTECODE=1 python3 -m yazhi_harness.cli run --provider sample --suite sample --model demo
cd ../..
git status --short
```

Then commit and push (the message is stored in
[`COMMIT_MSG.txt`](COMMIT_MSG.txt), so this is one paste):

```bash
cd repos/yazhi-skills
git add -A
git commit -F packages/harness/docs/COMMIT_MSG.txt
git log --oneline -1
git push -u origin HEAD
```

The push goes to `git@github.com:yazhi-lem/yazhi-skills.git` (SSH). If it fails
for auth or network reasons, fix the credential — do not force-push or change
the remote.

Rebuild generated files first if any `--check` reports staleness:

```bash
python3 scripts/build_index.py && python3 scripts/build_skill_bundle.py --per-skill
```

Before pushing, confirm nothing unintended is in the commit:

```bash
git status --short
git show --stat --oneline HEAD | head -40
```

Nothing from `~/.scratch/harness-data` or `~/.cache/yazhi-harness` should
appear — datasets are fetched, never vendored.
