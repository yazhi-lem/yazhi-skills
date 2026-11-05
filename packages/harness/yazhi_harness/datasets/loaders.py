"""Dataset loaders: parse corpora into language-tagged ``Case`` objects.

Every loader records provenance (name, URL, licence, revision) and reports
which languages it actually covers. Loaders raise ``DatasetUnavailable`` with
a message naming the snapshot command when a corpus file is missing — they
never emit a fake or empty language silently, because an empty language
column in a results table reads as "scored" to a human skimming it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from .. import langs
from ..types import Case, Severity


class DatasetUnavailable(RuntimeError):
    def __init__(self, name: str, detail: str) -> None:
        super().__init__(
            f"dataset {name!r} is not available: {detail}\n"
            f"run: python3 -m yazhi_harness.cli snapshot {name} "
            f"(or point --data-root at an existing snapshot)"
        )


@dataclass(frozen=True)
class Provenance:
    name: str
    url: str
    license: str
    citation: str
    genre: str
    revision: str = ""


@dataclass
class CaseSet:
    """Cases from one corpus, restricted to a language selection."""

    provenance: Provenance
    cases: List[Case]
    languages: List[str]
    missing_languages: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _pick_languages(requested: Optional[Sequence[str]]) -> List[langs.Language]:
    if not requested:
        return list(langs.LANGUAGES.values())
    picked = [langs.resolve(code) for code in requested]
    seen, out = set(), []
    for lang in picked:
        if lang.bcp47 not in seen:
            seen.add(lang.bcp47)
            out.append(lang)
    return out


class DatasetLoader:
    name: str = ""
    provenance: Provenance

    def __init__(self, root: Optional[Path] = None) -> None:
        """``root`` is the *datasets* root; each dataset lives in ``root/<name>``.

        ``snapshot()`` and the loaders must agree on this layout, so the
        subdirectory is appended in both paths: a caller passing
        ``--data-root X`` gets ``X/flores``, ``X/indicqa``, and so on.
        """
        from . import default_root

        base = Path(root) if root else default_root()
        self.root = base / self.name

    def available(self) -> bool:
        raise NotImplementedError

    def load(
        self,
        languages: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
        seed: int = 0,
    ) -> CaseSet:
        raise NotImplementedError

    def _require(self, path: Path) -> Path:
        if not path.exists():
            raise DatasetUnavailable(self.name, f"{path} is missing")
        return path


# --------------------------------------------------------------------------
# FLORES-101 — professional parallel translation, 11 Indic languages + English
# --------------------------------------------------------------------------
_FLORES_ISO3_NOTE = "FLORES uses ISO-639-3 codes (tam, hin, ...)"


class FloresLoader(DatasetLoader):
    """``devtest`` split: 1,012 sentences, human-translated, multilingually aligned.

    Prompt: translate the English source into the target language.
    """

    name = "flores"
    provenance = Provenance(
        name="FLORES-101 devtest",
        url="https://github.com/facebookresearch/flores",
        license="CC-BY-SA-4.0",
        citation=(
            "Goyal et al. 2021, The FLORES-101 Evaluation Benchmark for "
            "Low-Resource and Multilingual Machine Translation"
        ),
        genre="wikipedia-news (domain: general knowledge)",
        revision="flores101_dataset",
    )

    def _file(self, iso3: str, split: str) -> Path:
        return self.root / split / f"{iso3}.{split}"

    def available(self) -> bool:
        return self._file("eng", "devtest").exists()

    def load(self, languages=None, limit=None, seed=0) -> CaseSet:
        import random

        self._require(self._file("eng", "devtest"))
        split = "devtest"
        with self._file("eng", split).open(encoding="utf-8") as handle:
            english = [_norm(line) for line in handle]
        total = len(english)
        picked = _pick_languages(languages)
        indices = list(range(total))
        if limit is not None and limit < total:
            random.Random(seed).shuffle(indices)
            indices = sorted(indices[:limit])
        cases: List[Case] = []
        missing: List[str] = []
        for lang in picked:
            path = self._file(lang.code, split)
            if not path.exists():
                missing.append(lang.bcp47)
                continue
            with path.open(encoding="utf-8") as handle:
                target = [_norm(line) for line in handle]
            if len(target) != total:
                raise DatasetUnavailable(
                    self.name,
                    f"{path} has {len(target)} lines, English has {total} "
                    f"({_FLORES_ISO3_NOTE}); re-snapshot",
                )
            for i in indices:
                if not target[i]:
                    continue
                cases.append(
                    Case(
                        id=f"flores-{lang.code}-{i:04d}",
                        language=lang.bcp47,
                        prompt=(
                            f"Translate the following English sentence into "
                            f"{lang.english} ({lang.native}). Output only the translation.\n\n"
                            f"{english[i]}"
                        ),
                        references=[target[i]],
                        tags=["translation", self.provenance.genre],
                        severity=Severity.MEDIUM,
                        metadata={"source": "flores-101", "source_text": english[i], "row": i},
                    )
                )
        return CaseSet(
            provenance=self.provenance,
            cases=cases,
            languages=[p.bcp47 for p in picked if p.bcp47 not in missing],
            missing_languages=missing,
            notes=[_FLORES_ISO3_NOTE],
        )


# ---------------------------------------------------------------------------
# IndicQA — native-language extractive QA (Tamil by default; 11 in total)
# ---------------------------------------------------------------------------

#: Phrases a model may use to decline an unanswerable question, per language.
#: Kept to multi-word or unambiguous markers; bare "இல்லை"/"no" are excluded
#: because they appear inside correct answers ("இல்லை என்று கூறினார்").
ABSTAIN_MARKERS: Dict[str, List[str]] = {
    "tam": ["கொடுக்கப்பட்டுள்ள விவரத்தில்", "தகவல் இல்லை", "குறிப்பிடப்படவில்லை", "இல்லை என்று கூற முடியாது", "பதில் இல்லை"],
    "hin": ["जानकारी नहीं है", "उपलब्ध नहीं है", "उल्लेख नहीं"],
    "ben": ["তথ্য নেই", "তথ্য পাওয়া যায় না", "উল্লেখ নেই"],
    "guj": ["માહિતી નથી", "માહિતી ઉપલબ્ધ નથી"],
    "kan": ["ಮಾಹಿತಿ ಇಲ್ಲ", "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ"],
    "mal": ["വിവരം ഇല്ല", "വിവരം ലഭ്യമല്ല"],
    "mar": ["माहिती नाही", "माहिती उपलब्ध नाही"],
    "ory": ["ସୂଚନା ନାହିଁ", "ତଥ୍ୟ ନାହିଁ"],
    "pan": ["ਜਾਣਕਾਰੀ ਨਹੀਂ", "ਜਾਣਕਾਰੀ ਉਪਲਬਧ ਨਹੀਂ"],
    "tel": ["సమాచారం లేదు", "సమాచారం అందుబాటులో లేదు"],
    "urd": ["معلومات نہیں", "معلومات دستیاب نہیں"],
    "en": ["information not available", "not mentioned", "cannot be answered"],
}


class IndicQALoader(DatasetLoader):
    """Native-language reading comprehension with genuine no-answer questions.

    Tamil questions are native (median length 44 chars, QAs per article 7);
    the other languages use the same schema. Unanswerable rows
    (``category == "NO"``) test calibrated abstention instead of guessing.
    """

    name = "indicqa"
    provenance = Provenance(
        name="IndicQA",
        url="https://huggingface.co/datasets/ai4bharat/IndicQA",
        license="CC-BY-4.0",
        citation="Doddapaneni et al. 2023, IndicQA (AI4Bharat)",
        genre="wikipedia reading comprehension",
    )
    max_context_chars = 4000  # keep prompts inside small on-device contexts

    def _file(self, iso3: str) -> Path:
        return self.root / f"indicqa.{iso3}.json"

    def available(self) -> bool:
        return self._file("tam").exists()

    def load(self, languages=None, limit=None, seed=0) -> CaseSet:
        import random

        self._require(self._file("tam"))
        picked = _pick_languages(languages)
        rng = random.Random(seed)
        cases: List[Case] = []
        missing: List[str] = []
        for lang in picked:
            path = self._file(lang.code)
            if not path.exists():
                missing.append(lang.bcp47)
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            rows = []
            for article in payload.get("data", []):
                for paragraph in article.get("paragraphs", []):
                    context = _norm(paragraph.get("context", ""))
                    if len(context) > self.max_context_chars:
                        continue  # skip rather than truncate the evidence away
                    for qa in paragraph.get("qas", []):
                        answers = [a.get("text", "") for a in qa.get("answers", [])]
                        answers = [a for a in (_norm(x) for x in answers) if a]
                        category = qa.get("category", "SHORT")
                        rows.append((qa, context, answers, category))
            if limit is not None and limit < len(rows):
                rows = sorted(rng.sample(rows, limit), key=lambda r: r[0].get("id", 0))
            for qa, context, answers, category in rows:
                answerable = category != "NO"
                cases.append(
                    Case(
                        id=f"indicqa-{lang.code}-{qa.get('id')}",
                        language=lang.bcp47,
                        prompt=(
                            f"Read the passage and answer the question in "
                            f"{lang.english}. If the answer is not in the passage, say it "
                            f"is not given.\n\nPassage:\n{context}\n\n"
                            f"Question: {_norm(qa.get('question', ''))}\nAnswer:"
                        ),
                        references=answers,
                        tags=["qa", "unanswerable" if not answerable else "answerable"],
                        severity=Severity.MEDIUM,
                        metadata={
                            "answerable": answerable,
                            "abstain": ABSTAIN_MARKERS.get(lang.code, ABSTAIN_MARKERS["en"]),
                            "category": category,
                        },
                    )
                )
        return CaseSet(
            provenance=self.provenance,
            cases=cases,
            languages=[p.bcp47 for p in picked if p.bcp47 not in missing],
            missing_languages=missing,
            notes=["contexts over 4,000 chars are skipped to keep prompts in small contexts"],
        )


# ---------------------------------------------------------------------------
# IndicXParaphrase — native sentence-level paraphrase pairs (10 languages)
# ---------------------------------------------------------------------------
class ParaphraseLoader(DatasetLoader):
    """Two native sentences, 1: paraphrases, 0: not.

    The task is a binary judgement, which a label scorer can grade exactly —
    no reference generation needed.
    """

    name = "paraphrase"
    provenance = Provenance(
        name="IndicXParaphrase",
        url="https://huggingface.co/datasets/ai4bharat/IndicXParaphrase",
        license="NO-ASSERTED-LICENSE (evaluate locally; do not redistribute rows)",
        citation="AI4Bharat, IndicXParaphrase",
        genre="sentence pairs",
    )

    def _file(self, iso3: str) -> Path:
        return self.root / f"{iso3}.tsv"

    def available(self) -> bool:
        return self._file("hin").exists()

    def load(self, languages=None, limit=None, seed=0) -> CaseSet:
        import csv
        import random

        self._require(self._file("hin"))
        picked = _pick_languages(languages)
        rng = random.Random(seed)
        cases: List[Case] = []
        missing: List[str] = []
        for lang in picked:
            path = self._file(lang.code)
            if not path.exists():
                missing.append(lang.bcp47)
                continue
            with path.open(encoding="utf-8") as handle:
                rows = [
                    r for r in csv.DictReader(handle, delimiter="\t")
                    if r.get("sentence1") and r.get("sentence2")
                ]
            if limit is not None and limit < len(rows):
                rows = rng.sample(rows, limit)
            for i, row in enumerate(rows):
                label = "yes" if str(row.get("label", "1")).strip() == "1" else "no"
                cases.append(
                    Case(
                        id=f"paraphrase-{lang.code}-{i:04d}",
                        language=lang.bcp47,
                        prompt=(
                            f"Are the two {lang.english} sentences below paraphrases of "
                            f"each other? Answer with a label line exactly as "
                            f"'LABEL: yes' or 'LABEL: no'.\n\n"
                            f"Sentence 1: {_norm(row['sentence1'])}\n"
                            f"Sentence 2: {_norm(row['sentence2'])}"
                        ),
                        tags=["paraphrase"],
                        severity=Severity.LOW,
                        metadata={
                            "label": label,
                            "aliases": {"yes": "ஆம்", "no": "இல்லை"},
                        },
                    )
                )
        notes = ["IndicXParaphrase has no Tamil file upstream; Tamil is reported as missing"]
        return CaseSet(
            provenance=self.provenance,
            cases=cases,
            languages=[p.bcp47 for p in picked if p.bcp47 not in missing],
            missing_languages=missing,
            notes=notes,
        )


# ---------------------------------------------------------------------------
# IndicSentiment — CC0 n-way-parallel sentiment (13 languages)
# ---------------------------------------------------------------------------
_SENTIMENT_ALIASES = {"positive": "நேர்மறை", "negative": "எதிர்மறை", "neutral": "நடுநிலை"}


class SentimentLoader(DatasetLoader):
    name = "sentiment"
    provenance = Provenance(
        name="IndicSentiment (MTEB mirror)",
        url="https://huggingface.co/datasets/mteb/IndicSentiment",
        license="CC0-1.0",
        citation="Doddapaneni et al. 2023, IndicSentiment (AI4Bharat); MTEB mirror",
        genre="product reviews",
    )

    def _file(self, iso3: str) -> Path:
        return self.root / f"{iso3}.jsonl"

    def available(self) -> bool:
        return self._file("tam").exists()

    def load(self, languages=None, limit=None, seed=0) -> CaseSet:
        import random

        self._require(self._file("tam"))
        picked = _pick_languages(languages)
        rng = random.Random(seed)
        cases: List[Case] = []
        missing: List[str] = []
        for lang in picked:
            path = self._file(lang.code)
            if not path.exists():
                missing.append(lang.bcp47)
                continue
            rows = []
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
            if limit is not None and limit < len(rows):
                rows = rng.sample(rows, limit)
            for i, row in enumerate(rows):
                text = _norm(row.get("INDIC REVIEW") or row.get("text") or "")
                label = str(row.get("LABEL") or row.get("label") or "").strip().lower()
                if not text or label not in _SENTIMENT_ALIASES:
                    continue
                cases.append(
                    Case(
                        id=f"sentiment-{lang.code}-{i:04d}",
                        language=lang.bcp47,
                        prompt=(
                            f"Classify the sentiment of this {lang.english} review as "
                            f"positive, negative or neutral. Reply with exactly one "
                            f"label line: 'LABEL: <label>'.\n\nReview: {text}"
                        ),
                        tags=["sentiment", str(row.get("CATEGORY", "")).lower()],
                        severity=Severity.LOW,
                        metadata={"label": label, "aliases": _SENTIMENT_ALIASES},
                    )
                )
        return CaseSet(
            provenance=self.provenance,
            cases=cases,
            languages=[p.bcp47 for p in picked if p.bcp47 not in missing],
            missing_languages=missing,
        )


LOADERS: Dict[str, type[DatasetLoader]] = {
    "flores": FloresLoader,
    "indicqa": IndicQALoader,
    "paraphrase": ParaphraseLoader,
    "sentiment": SentimentLoader,
}


def load(name: str, root=None, languages=None, limit=None, seed=0) -> CaseSet:
    if name not in LOADERS:
        raise KeyError(f"unknown dataset {name!r}; known: {', '.join(sorted(LOADERS))}")
    return LOADERS[name](root).load(languages=languages, limit=limit, seed=seed)
