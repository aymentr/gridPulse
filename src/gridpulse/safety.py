"""Determination-boundary guard (architecture I-6, D-005).

Generated text is checked before release. The system may state facts, calculations and potential
exposure; it may never assert a Level 3 engineering, contractual or project conclusion.
"""
from __future__ import annotations

import re


class UnsafeConclusionError(Exception):
    pass


FORBIDDEN = [
    r"\bwill (?:be )?(?:delayed|slip|slips|fail|miss)\b",
    r"\bwill not (?:meet|pass|comply|be met)\b",
    r"\bmust (?:be )?(?:notif|redesign|redone|redo|resubmit|revise|update)\w*",
    r"\b(?:is|are) (?:non-?compliant|wrong|incorrect)\b",
    r"\bnon-?compliant\b",
    r"\bcannot proceed\b",
    r"\b(?:is|was) (?:triggered|violated)\b",
    r"\bdelay(?:ed)? by \d+",
]
_RX = [re.compile(p, re.I) for p in FORBIDDEN]


def violations(text: str) -> list[str]:
    return [m.group(0) for rx in _RX for m in rx.finditer(text)]


def check(text: str) -> str:
    found = violations(text)
    if found:
        raise UnsafeConclusionError(f"unsupported Level 3 wording: {found}")
    return text
