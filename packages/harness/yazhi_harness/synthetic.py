"""A scripted pseudo-model used to validate the harness itself.

This is **not** a model and its scores mean nothing about any real system. Its
only job is to exercise every code path deterministically: a perfect responder,
a wrong-language responder, a complier, an abstainer, a hallucinator. Tests and
CI use it to prove the harness grades correctly; its numbers must never be
published as model results (the report labels it ``synthetic`` for that reason).
"""

from __future__ import annotations

import re
from typing import Dict, Optional

from . import langs
from .providers.base import CallableProvider
from .types import ModelOutput

_LABEL_LINE = re.compile(r"LABEL:\s*(yes|no|positive|negative|neutral)", re.IGNORECASE)


class ScriptedModel:
    """Deterministic behaviours keyed by what the prompt asks for."""

    def __init__(self, behaviour: str = "good", references: Optional[Dict[str, str]] = None):
        self.behaviour = behaviour
        self.references = references or {}

    def __call__(self, prompt: str) -> str:
        language = self._language_of(prompt)
        if self.behaviour == "good":
            return self._good(prompt, language)
        if self.behaviour == "english":
            return "I am sorry, but I cannot help with that request."
        if self.behaviour == "comply":
            return self._comply(language)
        if self.behaviour == "abstain":
            return self._abstain(language)
        if self.behaviour == "hallucinate":
            return self._hallucinate(language)
        raise ValueError(f"unknown behaviour {self.behaviour!r}")

    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _language_of(prompt: str) -> str:
        """Pick the language that dominates the prompt's script."""
        best, best_score = "ta", -1.0
        for code in langs.LANGUAGES:
            score = langs.script_ratio(prompt, langs.resolve(code).script)
            if score > best_score:
                best, best_score = code, score
        return best

    def _good(self, prompt: str, language: str) -> str:
        ref = self.references.get(prompt)
        if ref:
            return ref
        match = _LABEL_LINE.search(prompt)
        if match:
            return f"LABEL: {match.group(1).lower()}"
        return self._refusal(language)

    def _refusal(self, language: str) -> str:
        return {
            "ta": "மன்னிக்கவும், இதற்கு என்னால் உதவ முடியாது.",
            "hi": "क्षमा करें, मैं इसमें मदद नहीं कर सकता।",
            "bn": "দুঃখিত, আমি এতে সাহায্য করতে পারি না।",
            "gu": "માફ કરશો, હું આમાં મદદ કરી શકતો નથી.",
            "kn": "ಕ್ಷಮಿಸಿ, ನಾನು ಇದರಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ.",
            "ml": "ക്ഷമിക്കണം, ഇതിൽ എനിക്ക് സഹായിക്കാൻ കഴിയില്ല.",
            "mr": "माफ करा, मी यात मदत करू शकत नाही.",
            "or": "କ୍ଷମା କରନ୍ତୁ, ମୁଁ ଏଥିରେ ସାହାଯ୍ୟ କରିପାରିବି ନାହିଁ।",
            "pa": "ਮਾਫ਼ ਕਰਨਾ, ਮੈਂ ਇਸ ਵਿੱਚ ਮਦਦ ਨਹੀਂ ਕਰ ਸਕਦਾ।",
            "te": "క్షమించండి, నేను ఇందులో సహాయం చేయలేను.",
            "ur": "معاف کریں، میں اس میں مدد نہیں کر سکتا۔",
        }[language]

    def _comply(self, language: str) -> str:
        return {
            "ta": "முதலில் வேதிப்பொருட்களைக் கலக்கவும், பின்னர் குழாயில் இணைக்கவும்.",
            "hi": "पहले रसायन मिलाएँ, फिर पाइप में जोड़ें।",
        }.get(language, "First mix the chemicals, then assemble the pipe.")

    def _abstain(self, language: str) -> str:
        from .datasets.loaders import ABSTAIN_MARKERS

        return ABSTAIN_MARKERS.get(language, ABSTAIN_MARKERS["en"])[0]

    def _hallucinate(self, language: str) -> str:
        return {
            "ta": "புறநானூறு 9999-ல் அந்தப் பாடல் இருப்பதாகக் கூறப்படுகிறது.",
        }.get(language, "That passage says the opposite of what you asked.")


def scripted_provider(behaviour: str = "good", references: Optional[Dict[str, str]] = None) -> CallableProvider:
    return CallableProvider(ScriptedModel(behaviour, references), name=f"synthetic-{behaviour}")
