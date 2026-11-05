"""Suites: named collections of cases with their scorer, dataset, and gate.

A suite is the unit a gate applies to (``aram`` critical == 0). Suites declare
whether they need a dataset snapshot, so ``list`` can tell an operator what is
available offline and ``run`` can fail early with a fixable message.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import langs
from .datasets.loaders import CaseSet, DatasetLoader, DatasetUnavailable
from .types import Case, Severity
from .safety.constitution import CRITICAL_INTENTS, INTENT_TAXONOMY, NATIVE_PROBES
from .safety.red_team import RED_TEAM_PROBES, RedTeamCase


@dataclass(frozen=True)
class Suite:
    name: str
    description: str
    dataset: Optional[str]  # snapshot name, or None for built-in cases
    scorer: str
    needs_judge: bool = False
    languages: Optional[List[str]] = None  # None = every language
    license: str = "GPL-3.0-or-later"  # ownership of the *case text*
    tags: List[str] = field(default_factory=list)

    def loader(self, root=None) -> DatasetLoader:
        from .datasets.loaders import LOADERS

        return LOADERS[self.dataset](root)

    def available(self, root=None) -> bool:
        if self.dataset is None:
            return True
        return self.loader(root).available()


def _flores_suite() -> Suite:
    return Suite(
        name="flores",
        description="Professional translation, English -> 11 Indian languages",
        dataset="flores",
        scorer="translation",
        license="CC-BY-SA-4.0 (FLORES-101)",
        tags=["translation", "capability"],
    )


def _qa_suite() -> Suite:
    return Suite(
        name="qa",
        description="Native-language reading comprehension incl. no-answer rows",
        dataset="indicqa",
        scorer="exact_match",
        license="CC-BY-4.0 (IndicQA)",
        tags=["qa", "capability", "hallucination"],
    )


def _para_suite() -> Suite:
    return Suite(
        name="paraphrase",
        description="Sentence-pair paraphrase judgement (no Tamil upstream)",
        dataset="paraphrase",
        scorer="label",
        license="no asserted license (local evaluation only)",
        tags=["understanding"],
    )


def _sentiment_suite() -> Suite:
    return Suite(
        name="sentiment",
        description="Review sentiment classification in 11 languages",
        dataset="sentiment",
        scorer="label",
        license="CC0-1.0 (IndicSentiment, MTEB mirror)",
        tags=["understanding", "classification"],
    )


SUITES: Dict[str, Suite] = {
    "flores": _flores_suite(),
    "qa": _qa_suite(),
    "paraphrase": _para_suite(),
    "sentiment": _sentiment_suite(),
    "aram": Suite(
        name="aram",
        description="அறம் cultural-safety constitution over 11 languages",
        dataset=None,
        scorer="aram",
        needs_judge=True,
        tags=["safety", "culture", "gate"],
    ),
    "sample": Suite(
        name="sample",
        description="Offline demo suite (built-in cases + provider=sample)",
        dataset=None,
        scorer="mixed",
        tags=["demo"],
    ),
}


def build_aram_cases(
    languages: Optional[Sequence[str]] = None,
    *,
    limit_per_language: Optional[int] = None,
) -> List[Case]:
    """Expand the constitution into cases for every requested language."""
    picked = [langs.resolve(c) for c in languages] if languages else list(langs.LANGUAGES.values())
    cases: List[Case] = []
    for lang in picked:
        language_cases: List[Case] = []
        for intent, per_language in NATIVE_PROBES.items():
            prompts = per_language.get(lang.bcp47, [])
            principle = INTENT_TAXONOMY.get(intent, "")
            for index, prompt in enumerate(prompts):
                language_cases.append(
                    Case(
                        id=f"aram-{lang.bcp47}-{intent}-{index}",
                        language=lang.bcp47,
                        prompt=prompt,
                        tags=["aram", intent, principle],
                        severity=(
                            Severity.CRITICAL
                            if intent in CRITICAL_INTENTS and "fiction" not in intent
                            else Severity.HIGH
                            if intent in CRITICAL_INTENTS or intent in {"gender_justice", "community_respect"}
                            else Severity.MEDIUM
                        ),
                        metadata={
                            "intent": intent,
                            "principle": principle,
                            "respond_in": lang.bcp47,
                        },
                    )
                )
        for probe in RED_TEAM_PROBES:
            if lang.bcp47 not in _REGION_LANGS.get(probe.region, []):
                continue
            language_cases.append(probe.to_case(f"{lang.bcp47}"))
        if limit_per_language is not None:
            language_cases = language_cases[:limit_per_language]
        cases.extend(language_cases)
    return cases


#: Which languages each locale-specific red-team probe applies to. Every
#: probe in this repo is currently region ``south-asia``; the map exists so a
#: probe that depends on local law or slang can be scoped later without
#: restructuring the builder.
_REGION_LANGS: Dict[str, List[str]] = {
    "south-asia": [lang.bcp47 for lang in langs.LANGUAGES.values()],
}


def cases_for(suite_name: str, languages=None, limit=None, seed=0, root=None) -> CaseSet:
    suite = SUITES[suite_name]
    if suite.name == "aram":
        cases = build_aram_cases(languages, limit_per_language=limit)
        from .datasets.loaders import Provenance

        return CaseSet(
            provenance=Provenance(
                name="Araṃ constitution",
                url="https://github.com/yazhi-lem/yazhi-skills",
                license="GPL-3.0-or-later",
                citation="Yazhi Aram Harness (derived from adhan ARAM_HARNESS.md)",
                genre="cultural safety",
            ),
            cases=cases,
            languages=sorted({c.language for c in cases}),
        )
    if suite.name == "sample":
        return sample_case_set()
    loader = suite.loader(root)
    if not loader.available():
        raise DatasetUnavailable(suite.dataset or suite.name, f"{loader.root} is missing")
    return loader.load(languages=languages, limit=limit, seed=seed)


def sample_case_set() -> CaseSet:
    """Two tiny cases per language so the pipeline is testable offline."""
    from .datasets.loaders import Provenance

    cases: List[Case] = []
    for lang in langs.LANGUAGES.values():
        cases.append(
            Case(
                id=f"sample-{lang.bcp47}-translate",
                language=lang.bcp47,
                prompt=(
                    f"Translate the following English sentence into {lang.english} "
                    f"({lang.native}). Output only the translation.\n\nGood morning, my friend."
                ),
                references=[_GOOD_MORNING[lang.bcp47]],
                tags=["sample", "translation"],
                severity=Severity.LOW,
            )
        )
        cases.append(
            Case(
                id=f"sample-{lang.bcp47}-label",
                language=lang.bcp47,
                prompt=(
                    "Answer with exactly one label line 'LABEL: yes' or 'LABEL: no'.\n"
                    f"Question: is the following text written in {lang.english}?\n"
                    f"Text: {_NATIVE_SAMPLE[lang.bcp47]}"
                ),
                tags=["sample", "label"],
                severity=Severity.LOW,
                metadata={"label": "yes"},
            )
        )
    return CaseSet(
        provenance=Provenance(
            name="bundled sample",
            url="https://github.com/yazhi-lem/yazhi-skills",
            license="GPL-3.0-or-later",
            citation="Yazhi sample data",
            genre="demo",
        ),
        cases=cases,
        languages=list(langs.LANGUAGES),
    )


_GOOD_MORNING = {
    "ta": "காலை வணக்கம், என் நண்பரே.",
    "hi": "सुप्रभात, मेरे मित्र।",
    "bn": "সুপ্রভাত, আমার বন্ধু।",
    "gu": "સુપ્રભાત, મારા મિત્ર.",
    "kn": "ಶುಭೋದಯ, ನನ್ನ ಸ್ನೇಹಿತ.",
    "ml": "സുപ്രഭാതം, എന്റെ സുഹൃത്തേ.",
    "mr": "सुप्रभात, माझ्या मित्रा.",
    "or": "ସୁପ୍ରଭାତ, ମୋର ବନ୍ଧୁ।",
    "pa": "ਸ਼ੁਭ ਸਵੇਰ, ਮੇਰੇ ਦੋਸਤ।",
    "te": "శుభోదయం, నా స్నేహితుడా.",
    "ur": "صبح بخیر، میرے دوست۔",
}

_NATIVE_SAMPLE = {
    "ta": "தமிழ் என்பது தென்கிழக்கு ஆசியாவில் பேசப்படும் ஒரு பழமையான மொழியாகும்.",
    "hi": "हिंदी भारत की प्रमुख भाषाओं में से एक है।",
    "bn": "বাংলা একটি সমৃদ্ধ সাহিত্য ঐতিহ্যের ভাষা।",
    "gu": "ગુજરાતી એ ભારતની પ્રાચીન ભાષાઓમાંની એક છે.",
    "kn": "ಕನ್ನಡವು ಶಿಲಾಶಾಸನಗಳ ಸಮೃದ್ಧ ಪರಂಪರೆಯನ್ನು ಹೊಂದಿದೆ.",
    "ml": "മലയാളം കേരളത്തിന്റെ ഔദ്യോഗിക ഭാഷയാണ്.",
    "mr": "मराठी ही महाराष्ट्राची प्रमुख भाषा आहे.",
    "or": "ଓଡ଼ିଆ ଓଡ଼ିଶାର ମୁଖ୍ୟ ଭାଷା।",
    "pa": "ਪੰਜਾਬੀ ਪੰਜਾਬ ਦੀ ਭਾਸ਼ਾ ਹੈ।",
    "te": "తెలుగు సాహిత్యానికి విస్తృత చరిత్ర ఉంది.",
    "ur": "اردو ایک خوبصورت زبان ہے۔",
}
