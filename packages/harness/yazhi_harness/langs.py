"""The 11 Indian languages the harness starts with, and script arithmetic.

The language inventory is imported by the data loaders, the Araṃ constitution,
the report aggregation and the ``script`` scorers, so it lives in one place.
Adding a language means adding one row here plus a corpus file to a loader.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Unicode blocks per script, inclusive. Tamil covers U+0B80-U+0BFF and so on;
# the extra ranges catch vedic/extender marks that appear in real text.
SCRIPT_RANGES: Dict[str, List[Tuple[int, int]]] = {
    "tamil": [(0x0B80, 0x0BFF)],
    "devanagari": [(0x0900, 0x097F), (0xA8E0, 0xA8FF)],
    "bengali": [(0x0980, 0x09FF)],
    "gurmukhi": [(0x0A00, 0x0A7F)],
    "gujarati": [(0x0A80, 0x0AFF)],
    "oriya": [(0x0B00, 0x0B7F)],
    "telugu": [(0x0C00, 0x0C7F)],
    "kannada": [(0x0C80, 0x0CFF)],
    "malayalam": [(0x0D00, 0x0D7F)],
    "arabic": [(0x0600, 0x06FF), (0x0750, 0x077F), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)],
    # Latin-1 Supplement letter ranges skip U+00D7 (x) and U+00F7 (/), and the
    # block starts at U+00C0 because U+00A0-U+00BF are Latin-1 punctuation
    # (U+00B0 degree sign, U+00B7 middle dot) that Indic text uses inline.
    "latin": [
        (0x0041, 0x005A),
        (0x0061, 0x007A),
        (0x00C0, 0x00D6),
        (0x00D8, 0x00F6),
        (0x00F8, 0x024F),
    ],
}


@dataclass(frozen=True)
class Language:
    code: str  # ISO 639-3, what the corpora and tokenizers use
    bcp47: str  # what APIs and metadata use
    english: str
    native: str
    script: str

    @property
    def label(self) -> str:
        return f"{self.english.title()} ({self.native})"


LANGUAGES: Dict[str, Language] = {
    lang.bcp47: lang
    for lang in [
        Language("tam", "ta", "Tamil", "தமிழ்", "tamil"),
        Language("hin", "hi", "Hindi", "हिन्दी", "devanagari"),
        Language("ben", "bn", "Bengali", "বাংলা", "bengali"),
        Language("guj", "gu", "Gujarati", "ગુજરાતી", "gujarati"),
        Language("kan", "kn", "Kannada", "ಕನ್ನಡ", "kannada"),
        Language("mal", "ml", "Malayalam", "മലയാളം", "malayalam"),
        Language("mar", "mr", "Marathi", "मराठी", "devanagari"),
        Language("ory", "or", "Odia", "ଓଡ଼ିଆ", "oriya"),
        Language("pan", "pa", "Punjabi", "ਪੰਜਾਬੀ", "gurmukhi"),
        Language("tel", "te", "Telugu", "తెలుగు", "telugu"),
        Language("urd", "ur", "Urdu", "اردو", "arabic"),
    ]
}

#: bcp47 -> ISO-639-3, for corpora that name languages in ISO-639-3.
BY_ISO3: Dict[str, Language] = {lang.code: lang for lang in LANGUAGES.values()}
#: English names, lower-case, for loaders whose columns use prose names.
BY_NAME: Dict[str, Language] = {lang.english.lower(): lang for lang in LANGUAGES.values()}

#: Languages whose script is shared with another language in the inventory.
#: A script-ratio check cannot separate these, so ``pure_script`` treats them
#: as "not contaminated" (see ``script.script_ratio`` docs).
SHARED_SCRIPTS = ("devanagari",)  # Hindi and Marathi

DEFAULT_LANGUAGE = "ta"


class UnknownLanguage(KeyError):
    pass


def resolve(code: str) -> Language:
    """Accept ``ta``, ``ta-IN``, ``tam``, ``Tamil`` or ``tamil``."""
    key = code.strip()
    if key in LANGUAGES:
        return LANGUAGES[key]
    base = key.split("-")[0].split("_")[0].lower()
    if base in LANGUAGES:
        return LANGUAGES[base]
    if base in BY_ISO3:
        return BY_ISO3[base]
    if base in BY_NAME:
        return BY_NAME[base]
    raise UnknownLanguage(
        f"unknown language {code!r}; known: {', '.join(sorted(LANGUAGES))}"
    )


def try_resolve(code: Optional[str]) -> Optional[Language]:
    if not code:
        return None
    try:
        return resolve(code)
    except UnknownLanguage:
        return None


def script_of(code: str) -> str:
    return resolve(code).script


def is_in_script(char: str, script: str) -> bool:
    cp = ord(char)
    return any(lo <= cp <= hi for lo, hi in SCRIPT_RANGES[script])


def _is_letter_or_mark(char: str) -> bool:
    category = unicodedata.category(char)
    return category[0] in ("L", "M")


def script_ratio(text: str, script: str) -> float:
    """Share of letter/mark characters that belong to ``script``.

    Digits, punctuation, whitespace and symbols are ignored, so a Tamil answer
    with a few English proper nouns scores high but a Latin-dominant answer
    scores low. Combining vowel signs count as letters (they are ``Mn``),
    which is why ``str.isalpha()`` is not used.
    """
    relevant = [c for c in text if _is_letter_or_mark(c)]
    if not relevant:
        return 0.0
    return sum(1 for c in relevant if is_in_script(c, script)) / len(relevant)


def foreign_script_ratio(text: str, script: str) -> float:
    """Share of letters that belong to *any other* script in the inventory.

    Latin is included, which is what catches Tanglish leakage in Tamil text.
    Scripts outside the inventory (Cyrillic, Han, ...) are ignored.
    """
    relevant = [c for c in text if _is_letter_or_mark(c)]
    if not relevant:
        return 0.0
    foreign = 0
    for c in relevant:
        for other, ranges in SCRIPT_RANGES.items():
            if other == script:
                continue
            if any(lo <= ord(c) <= hi for lo, hi in ranges):
                foreign += 1
                break
    return foreign / len(relevant)


SCRIPT_MEMBERS: Dict[str, List[str]] = {}
for _lang in LANGUAGES.values():
    SCRIPT_MEMBERS.setdefault(_lang.script, []).append(_lang.bcp47)
