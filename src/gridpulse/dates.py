"""Deterministic date parsing for the formats used in project documents."""
from __future__ import annotations

import datetime as dt
import re

_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

# "2 February 2027", "12 Jan 2027", "February 2, 2027", "20-Nov-2026", "12-Jan-27"
DATE_RE = re.compile(
    r"\b(?P<d1>\d{1,2})[ -](?P<m1>[A-Za-z]{3,9})[ -](?P<y1>\d{2,4})\b"
    r"|\b(?P<m2>[A-Za-z]{3,9}) (?P<d2>\d{1,2}), (?P<y2>\d{4})\b")


def _year(y: str) -> int:
    n = int(y)
    return n + 2000 if n < 100 else n


def _build(day: str, month: str, year: str) -> dt.date | None:
    m = _MONTHS.get(month[:3].lower())
    if m is None:
        return None
    try:
        return dt.date(_year(year), m, int(day))
    except ValueError:
        return None


def find_dates(text: str) -> list[tuple[dt.date, str]]:
    """All dates in text, in order, with the exact matched substring."""
    out = []
    for m in DATE_RE.finditer(text):
        if m.group("d1"):
            d = _build(m.group("d1"), m.group("m1"), m.group("y1"))
        else:
            d = _build(m.group("d2"), m.group("m2"), m.group("y2"))
        if d is not None:
            out.append((d, m.group(0)))
    return out


def parse_date(text: str) -> dt.date | None:
    found = find_dates(text)
    return found[0][0] if found else None
