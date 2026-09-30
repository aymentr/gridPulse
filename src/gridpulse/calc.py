"""Deterministic calculations (architecture §5.3). No scheduling engine, float or critical path."""
from __future__ import annotations

import re

from .model import Calculation, Claim
from .store import Store


def _record(store: Store, operation, inputs, result, unit, note="") -> Calculation:
    c = Calculation(id=store.next_id("CALC"), operation=operation, inputs=inputs, result=result,
                    unit=unit, note=note)
    store.calculations[c.id] = c
    store.log("calculation", calculation=c.id, operation=operation, result=str(result))
    return c


def calendar_days(store: Store, a: Claim, b: Claim, label_a: str, label_b: str) -> Calculation:
    """(b − a) in calendar days, from two DATE claims."""
    if a.value.kind != "DATE" or b.value.kind != "DATE":
        raise ValueError("calendar_days requires DATE claims")
    return _record(
        store, f"calendar_days({label_b} − {label_a})",
        [{"label": label_a, "value": a.value.value.isoformat(), "claim_id": a.id},
         {"label": label_b, "value": b.value.value.isoformat(), "claim_id": b.id}],
        (b.value.value - a.value.value).days, "calendar days",
        note="Comparison of evidenced dates only; not float and not a forecast.")


_RANGE = re.compile(r"(?:across|from) (?P<lo>\d+) ?% to (?P<hi>\d+) ?%")


def percent_range(text: str) -> tuple[int, int] | None:
    m = _RANGE.search(text)
    return (int(m.group("lo")), int(m.group("hi"))) if m else None


def range_gap(store: Store, stated: Claim, required: Claim, label_s: str, label_r: str,
              note: str) -> Calculation | None:
    """Portion of the required range not covered by the stated range, as written."""
    rs, rr = percent_range(stated.value.value), percent_range(required.value.value)
    if not rs or not rr:
        return None
    gaps = []
    if rr[0] < rs[0]:
        gaps.append((rr[0], min(rs[0], rr[1])))
    if rr[1] > rs[1]:
        gaps.append((max(rs[1], rr[0]), rr[1]))
    result = ", ".join(f"{a}–{b} %" for a, b in gaps) if gaps else "none"
    return _record(
        store, f"uncovered_portion({label_r} range, {label_s} range)",
        [{"label": label_s, "value": f"{rs[0]}–{rs[1]} %", "claim_id": stated.id},
         {"label": label_r, "value": f"{rr[0]}–{rr[1]} %", "claim_id": required.id}],
        result, "percent of active power (as stated)", note=note)


def points_below(store: Store, points: Claim, stated: Claim, label_p: str, label_s: str,
                 note: str) -> Calculation | None:
    rs = percent_range(stated.value.value)
    if not rs or points.value.kind != "LIST":
        return None
    below = [p for p in points.value.value if p < rs[0]]
    return _record(
        store, f"points_below_lower_bound({label_p}, {label_s})",
        [{"label": label_p, "value": points.value.value, "claim_id": points.id},
         {"label": label_s, "value": f"{rs[0]}–{rs[1]} %", "claim_id": stated.id}],
        below, "percent", note=note)
