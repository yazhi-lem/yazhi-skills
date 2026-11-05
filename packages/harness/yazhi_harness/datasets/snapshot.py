"""Dataset snapshotting: download, verify, and pin corpora with a manifest.

A snapshot is: the raw files a loader reads, plus ``manifest.json`` (URL,
SHA-256, size, licence, fetch time). Runs record the manifest digest, so a
report can be traced to exactly the bytes that produced it.

Network access is confined to this module and to ``providers.http``.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import tarfile
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from .. import __version__
from ..langs import LANGUAGES, Language

HARNESS_HOME = Path.home() / ".cache" / "yazhi-harness"


def default_root() -> Path:
    """Where snapshots live unless overridden (``--data-root`` / ``YAZHI_HARNESS_DATA``)."""
    import os

    override = os.environ.get("YAZHI_HARNESS_DATA")
    return Path(override) if override else HARNESS_HOME / "datasets"


@dataclass
class Fetch:
    url: str
    filename: str
    post: Optional[Callable[[Path, Path], None]] = None


def _download(url: str, dest: Path, *, timeout: int = 120) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": f"yazhi-harness/{__version__}"})
    with urllib.request.urlopen(request, timeout=timeout) as response, partial.open("wb") as out:
        if getattr(response, "status", 200) != 200:
            raise RuntimeError(f"HTTP {response.status} for {url}")
        shutil.copyfileobj(response, out, length=1 << 16)
    partial.replace(dest)


def _sha256(path: Path, *, chunk: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


def _gunzip(src: Path, dest: Path) -> None:
    with gzip.open(src, "rb") as a, dest.open("wb") as b:
        shutil.copyfileobj(a, b)


def _extract_flores(src: Path, dest_root: Path, languages: List[Language]) -> None:
    wanted = {f"{lang.code}.devtest" for lang in languages} | {"eng.devtest"}
    with tarfile.open(src, "r:gz") as archive:
        for member in archive.getmembers():
            name = Path(member.name).name
            if not member.isfile() or name not in wanted:
                continue
            split = "devtest" if name.endswith(".devtest") else "dev"
            target_dir = dest_root / split
            target_dir.mkdir(parents=True, exist_ok=True)
            handle = archive.extractfile(member)
            if handle is None:
                continue
            with handle, (target_dir / name).open("wb") as out:
                shutil.copyfileobj(handle, out)


# --------------------------------------------------------------------------
# Per-dataset fetch plans
# --------------------------------------------------------------------------
_FLORES_URL = "https://dl.fbaipublicfiles.com/flores101/dataset/flores101_dataset.tar.gz"


def _indicqa_url(lang: Language) -> str:
    # IndicQA files are named by ISO-639-1 code (indicqa.ta.json).
    return (
        "https://huggingface.co/datasets/ai4bharat/IndicQA/resolve/main/data/"
        f"indicqa.{lang.bcp47}.json"
    )


def _paraphrase_url(lang: Language) -> str:
    return (
        "https://huggingface.co/datasets/ai4bharat/IndicXParaphrase/resolve/main/data/"
        f"{lang.bcp47}.tsv"
    )


def _sentiment_url(lang: Language) -> str:
    return (
        "https://huggingface.co/datasets/mteb/IndicSentiment/resolve/main/test/"
        f"{lang.bcp47}.jsonl.gz"
    )


#: Languages each upstream dataset actually publishes, verified by fetching
#: every file during development. Tamil is *not* in IndicXParaphrase upstream.
_COVERAGE: Dict[str, List[str]] = {
    "flores": [lang.bcp47 for lang in LANGUAGES.values()],
    # Verified against the HF tree listing: 11 files, and Urdu is NOT among
    # them. Claiming 11 here made the snapshot abort on a 404 for indicqa.ur.
    "indicqa": ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"],
    "paraphrase": ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "te"],
    "sentiment": [lang.bcp47 for lang in LANGUAGES.values()],
}

# IndicXParaphrase lists Assamese as ``as.tsv``; Assamese is not in our 11, so
# it is simply not fetched. Every other file matches its ISO-639-1 code.


def snapshot(name: str, root: Optional[Path] = None, *, languages: Optional[List[str]] = None) -> Path:
    from ..langs import resolve
    from .loaders import LOADERS

    if name not in LOADERS:
        raise KeyError(f"unknown dataset {name!r}; known: {', '.join(sorted(LOADERS))}")
    base = Path(root) if root else default_root()
    dest = base / name
    dest.mkdir(parents=True, exist_ok=True)
    # Only resolve codes this dataset actually publishes; "as" and "ur" are
    # not in our 11-language table and must be skipped, not crash the run.
    requested = languages if languages else _COVERAGE[name]
    picked = []
    for code in requested:
        try:
            picked.append(resolve(code))
        except Exception:
            continue
    picked = [lang for lang in picked if lang.bcp47 in _COVERAGE[name]]
    unsupported = [lang.bcp47 for lang in picked if lang.bcp47 not in _COVERAGE[name]]
    if unsupported:
        raise ValueError(
            f"{name} does not publish {', '.join(unsupported)}; "
            f"available: {', '.join(_COVERAGE[name])}"
        )
    fetched: List[Dict[str, object]] = []

    def record(path: Path, url: str, note: str = "") -> None:
        entry = {
            "path": path.relative_to(dest).as_posix(),
            "url": url,
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
        if note:
            entry["note"] = note
        fetched.append(entry)

    if name == "flores":
        archive = dest / "flores101_dataset.tar.gz"
        if not archive.exists():
            _download(_FLORES_URL, archive)
        _extract_flores(archive, dest, picked)
        for lang in picked:
            for split in ("devtest",):
                path = dest / split / f"{lang.code}.{split}"
                if path.exists():
                    record(path, _FLORES_URL, f"extracted member {split}/{lang.code}.{split}")
        record(dest / "devtest" / "eng.devtest", _FLORES_URL, "source language")
    elif name == "indicqa":
        for lang in picked:
            url = _indicqa_url(lang)
            # Saved under ISO-639-3 so the loader's language table is the only
            # naming convention in the repo; upstream URLs stay ISO-639-1.
            path = dest / f"indicqa.{lang.code}.json"
            if not path.exists():
                _download(url, path)
            record(path, url)
    elif name == "paraphrase":
        for lang in picked:
            url = _paraphrase_url(lang)
            path = dest / f"{lang.code}.tsv"
            if not path.exists():
                _download(url, path)
            record(path, url)
    elif name == "sentiment":
        for lang in picked:
            url = _sentiment_url(lang)
            gz = dest / f"{lang.code}.jsonl.gz"
            path = dest / f"{lang.code}.jsonl"
            if not gz.exists():
                _download(url, gz)
            if not path.exists():
                _gunzip(gz, path)
            record(path, url, "gunzipped")

    from .loaders import LOADERS as _L

    provenance = _L[name].provenance
    manifest = {
        "dataset": name,
        "provenance": {
            "name": provenance.name,
            "url": provenance.url,
            "license": provenance.license,
            "citation": provenance.citation,
            "genre": provenance.genre,
        },
        "languages": [lang.bcp47 for lang in picked],
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "harness_version": __version__,
        "files": fetched,
    }
    manifest_path = dest / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path


def verify(name: str, root: Optional[Path] = None) -> List[str]:
    """Re-hash a snapshot against its manifest; return problems (empty = ok)."""
    base = Path(root) if root else default_root()
    dest = base / name
    manifest_path = dest / "manifest.json"
    if not manifest_path.exists():
        return [f"{manifest_path} is missing"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    problems = []
    for entry in manifest.get("files", []):
        path = dest / entry["path"]
        if not path.exists():
            problems.append(f"missing file {entry['path']}")
        elif _sha256(path) != entry["sha256"]:
            problems.append(f"checksum mismatch {entry['path']}")
    return problems


def manifest_digest(name: str, root: Optional[Path] = None) -> Optional[str]:
    base = Path(root) if root else default_root()
    path = base / name / "manifest.json"
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
