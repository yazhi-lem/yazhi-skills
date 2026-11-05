"""Araṃ (அறம்) safety suite: constitution, red-team probes, judge.

Araṃ = righteousness/right conduct. The suite grades whether a model answers
in the caller's language, refuses harm in that language, keeps classical
citations honest, and stays neutral on caste, religion and politics.
"""

from .constitution import (
    CONSTITUTION,
    CRITICAL_INTENTS,
    INTENT_TAXONOMY,
    NATIVE_PROBES,
    Principle,
)
from .judge import JUDGE_RUBRIC, JudgeVerdict, LanguageAwareJudge, parse_judge_output
from .red_team import RED_TEAM_PROBES, RedTeamCase, red_team_for

__all__ = [
    "CONSTITUTION",
    "CRITICAL_INTENTS",
    "INTENT_TAXONOMY",
    "JUDGE_RUBRIC",
    "JudgeVerdict",
    "LanguageAwareJudge",
    "NATIVE_PROBES",
    "Principle",
    "RED_TEAM_PROBES",
    "RedTeamCase",
    "parse_judge_output",
    "red_team_for",
]
