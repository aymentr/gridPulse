"""Deterministic extraction of claims, entities, aliases and explicit relationships.

STAND-IN: these parsers read the structures used by the synthetic document formats (Markdown
tables, numbered clauses, CSV schedule exports). They stand in for the AI-assisted extraction stage
and will not generalise to real project documents. Every output is UNVALIDATED and cited.
"""
from __future__ import annotations

import csv
import re

from .dates import parse_date
from .entities import known_tags_in, normalize_tag, tags_in
from .evidence import cite
from .model import (Claim, ClaimValue, Dependency, DepType, DocumentVersion, Entity, EntityAlias,
                    EntityKind, Level, Location, Provenance, RelConfidence, Validation)
from .store import Store

CHECKPOINT_PHRASES = {  # phrase in source text → neutral checkpoint name (D-033)
    "grid compliance milestone": "GRID COMPLIANCE CHECKPOINT",
}


# --- helpers ----------------------------------------------------------------------------------

def section_at(version: DocumentVersion, line_no: int) -> str:
    for i in range(line_no - 1, -1, -1):
        if version.lines[i].startswith("#"):
            return version.lines[i].lstrip("# ").strip()
    return ""


def evidence_for(store: Store, v: DocumentVersion, line_start: int, quote: str,
                 line_end: int | None = None):
    loc = Location(v.doc_id, v.version_no, line_start, line_end or line_start,
                   section_at(v, line_start))
    return cite(store, loc, quote)


def md_tables(v: DocumentVersion):
    """Yield (header, rows) where rows = [(line_no, cells)]; key-value tables are skipped."""
    i, n = 0, len(v.lines)
    while i < n:
        if v.lines[i].startswith("|") and i + 1 < n and re.match(r"^\|[-| ]+\|$", v.lines[i + 1]):
            header = [c.strip() for c in v.lines[i].strip().strip("|").split("|")]
            rows, j = [], i + 2
            while j < n and v.lines[j].startswith("|"):
                rows.append((j + 1, [c.strip() for c in v.lines[j].strip().strip("|").split("|")]))
                j += 1
            if any(header):
                yield header, rows
            i = j
        else:
            i += 1


def _col(header, *names):
    for idx, h in enumerate(header):
        if any(n.lower() == h.lower() for n in names):
            return idx
    return None


def new_claim(store, subject, attribute, value: ClaimValue, evidence, provenance,
              qualifier="", meta=None) -> Claim:
    return store.add_claim(Claim(
        id=store.next_id("CL"), subject=subject, attribute=attribute, value=value,
        level=Level.FACT, provenance=[provenance], evidence_ids=[evidence.id],
        validation=Validation.UNVALIDATED, evidence_confidence=evidence.confidence,
        created_at=store.clock(), qualifier=qualifier, meta=meta or {}))


def add_explicit_dependency(store, dep_type, source, target, evidence, provenance,
                            source_attribute="", meta=None) -> Dependency:
    """Explicit relationships from sources: EXPLICIT · UNVALIDATED (D-027, D-049)."""
    for d in store.dependencies.values():
        if (d.type, d.source, d.target, d.source_attribute) == (dep_type, source, target,
                                                                source_attribute) \
                and d.confidence == RelConfidence.EXPLICIT:
            if evidence.id not in d.evidence_ids:
                d.evidence_ids.append(evidence.id)
            return d
    dep = Dependency(id=store.next_id("DEP"), type=dep_type, source=source, target=target,
                     confidence=RelConfidence.EXPLICIT, validation=Validation.UNVALIDATED,
                     provenance=[provenance], evidence_ids=[evidence.id],
                     created_at=store.clock(), source_attribute=source_attribute, meta=meta or {})
    store.dependencies[dep.id] = dep
    store.log("dependency.created", dependency=dep.id, type=dep_type.value, source=source,
              target=target, confidence="EXPLICIT", validation="UNVALIDATED")
    return dep


# --- extractors -------------------------------------------------------------------------------

def extract_document_entities(store: Store) -> None:
    for doc in store.documents.values():
        store.add_entity(Entity(doc.doc_id, EntityKind.DOCUMENT_ARTIFACT, doc.title))


def extract_equipment_lists(store: Store, v: DocumentVersion) -> None:
    for header, rows in md_tables(v):
        tag_i, desc_i, cls_i = _col(header, "Tag"), _col(header, "Description"), \
            _col(header, "Voltage class")
        if None in (tag_i, desc_i, cls_i):
            continue
        for line_no, cells in rows:
            for tag in [normalize_tag(t) for t in cells[tag_i].split(",")]:
                store.add_entity(Entity(tag, EntityKind.EQUIPMENT, cells[desc_i]))
                ev = evidence_for(store, v, line_no, cells[tag_i])
                store.add_alias(EntityAlias(tag, cells[desc_i],
                                            f"description in same row as tag ({v.doc_id})", ev.id))
                new_claim(store, tag, "voltage_class", ClaimValue("TEXT", cells[cls_i]),
                          evidence_for(store, v, line_no, cells[cls_i]),
                          Provenance.DOCUMENT_DERIVED)
                new_claim(store, tag, "description", ClaimValue("TEXT", cells[desc_i]),
                          evidence_for(store, v, line_no, cells[desc_i]),
                          Provenance.DOCUMENT_DERIVED)


def extract_schedule(store: Store, v: DocumentVersion) -> None:
    start = next((i for i, l in enumerate(v.lines) if l.startswith("Activity ID,")), None)
    if start is None:
        return
    reader = csv.DictReader(v.lines[start:])
    for offset, row in enumerate(reader, start=1):
        line_no = start + 1 + offset
        raw = v.lines[line_no - 1]
        act, name = row["Activity ID"], row["Activity Name"]
        store.add_entity(Entity(act, EntityKind.ACTIVITY, name))
        ev = evidence_for(store, v, line_no, raw)
        store.add_alias(EntityAlias(act, name, f"activity name in {v.doc_id}", ev.id))
        dates = {k: parse_date(row[k]) for k in ("Start", "Finish") if row.get(k)}
        for key, attr in (("Start", "planned_start"), ("Finish", "planned_finish")):
            if dates.get(key):
                new_claim(store, act, attr, ClaimValue("DATE", dates[key], text=row[key]), ev,
                          Provenance.SCHEDULE_DERIVED)
        # Activity names that carry an equipment tag give the equipment's dated attributes.
        for tag in known_tags_in(store, name):
            lname = name.lower()
            if "delivery" in lname and dates.get("Finish"):
                new_claim(store, tag, "delivery_date",
                          ClaimValue("DATE", dates["Finish"], text=row["Finish"]), ev,
                          Provenance.SCHEDULE_DERIVED, meta={"activity": act})
            if "installation" in lname and dates.get("Start"):
                new_claim(store, tag, "installation_start",
                          ClaimValue("DATE", dates["Start"], text=row["Start"]), ev,
                          Provenance.SCHEDULE_DERIVED, meta={"activity": act})
                store.entities[act].name = name
        for pred in re.findall(r"(A\d{4})\s*FS", row.get("Predecessors", "")):
            store.add_entity(Entity(pred, EntityKind.ACTIVITY, pred))
            add_explicit_dependency(store, DepType.PRECEDES, pred, act, ev,
                                    Provenance.SCHEDULE_DERIVED)


_DELIVERY_IN_STATUS = re.compile(r"delivery date of ([^.]+?\d{4})", re.I)


def extract_procurement_tables(store: Store, v: DocumentVersion) -> None:
    for header, rows in md_tables(v):
        item_i, tag_i = _col(header, "Item"), _col(header, "Tag / ref")
        status_i, plan_i = _col(header, "Status"), _col(header, "Planned delivery to site")
        if None in (item_i, tag_i, status_i, plan_i):
            continue
        for line_no, cells in rows:
            tags = [t for t in (normalize_tag(x) for x in cells[tag_i].split(","))
                    if t in store.entities]
            if len(tags) != 1:
                continue                                  # no single identifiable subject
            tag = tags[0]
            ev_alias = evidence_for(store, v, line_no, cells[item_i])
            store.add_alias(EntityAlias(tag, cells[item_i],
                                        f"item name in same row as tag ({v.doc_id})", ev_alias.id))
            planned = parse_date(cells[plan_i])
            if planned:
                ev = evidence_for(store, v, line_no, cells[plan_i])
                new_claim(store, tag, "delivery_date",
                          ClaimValue("DATE", planned, text=cells[plan_i]), ev,
                          Provenance.DOCUMENT_DERIVED, qualifier=f"status: {cells[status_i]}")
                continue
            m = _DELIVERY_IN_STATUS.search(cells[status_i])
            if m and parse_date(m.group(1)):
                ev = evidence_for(store, v, line_no, m.group(0))
                new_claim(store, tag, "delivery_date",
                          ClaimValue("DATE", parse_date(m.group(1)), text=m.group(1)), ev,
                          Provenance.DOCUMENT_DERIVED, qualifier=f"reported: {cells[status_i]}")


_CLAUSE = re.compile(r"^(?P<num>\d+\.\d+)\s+(?:\*\*(?P<title>[^*]+?)\.?\*\*)?\s*(?P<body>.*)$")


def _block(v: DocumentVersion, line_no: int) -> tuple[str, int]:
    """Text from line_no until the next blank line; returns (text, end_line)."""
    parts, j = [], line_no
    while j <= len(v.lines) and v.lines[j - 1].strip():
        parts.append(v.lines[j - 1].strip())
        j += 1
    return " ".join(parts), j - 1


def spec_subject(store: Store, v: DocumentVersion) -> str:
    for line in v.lines[:20]:
        m = re.match(r"^\|\s*Equipment\s*\|\s*(?P<v>[^|]+)\|", line)
        if m:
            for tag in tags_in(m.group("v")):
                if tag in store.entities:
                    return tag
    return v.doc_id


def extract_spec_clauses(store: Store, v: DocumentVersion) -> None:
    if "-SPC-" not in v.doc_id:
        return
    subject = spec_subject(store, v)
    for i, line in enumerate(v.lines, start=1):
        m = _CLAUSE.match(line)
        if m:
            text, end = _block(v, i)
            ev = evidence_for(store, v, i, text, end)
            new_claim(store, subject, f"clause {m.group('num')}",
                      ClaimValue("TEXT", re.sub(r"\*\*", "", text)), ev,
                      Provenance.DOCUMENT_DERIVED,
                      meta={"doc_id": v.doc_id, "clause": m.group("num"),
                            "title": (m.group("title") or "").strip()})
    for header, rows in md_tables(v):
        c_i, r_i = _col(header, "Clause"), _col(header, "Requirement")
        if None in (c_i, r_i):
            continue
        for line_no, cells in rows:
            ev = evidence_for(store, v, line_no, cells[r_i])
            new_claim(store, subject, f"clause {cells[c_i]}", ClaimValue("TEXT", cells[r_i]), ev,
                      Provenance.DOCUMENT_DERIVED,
                      meta={"doc_id": v.doc_id, "clause": cells[c_i], "title": ""})


_REQ = re.compile(r"^\*\*(?P<id>R-\d+) (?P<title>[^*]+?)\.\*\*\s*(?P<body>.*)$")


def extract_requirements(store: Store, v: DocumentVersion) -> None:
    for i, line in enumerate(v.lines, start=1):
        m = _REQ.match(line)
        if not m:
            continue
        text, end = _block(v, i)
        rid = m.group("id")
        store.add_entity(Entity(rid, EntityKind.REQUIREMENT, m.group("title")))
        ev = evidence_for(store, v, i, text, end)
        store.add_alias(EntityAlias(rid, m.group("title"), f"requirement title ({v.doc_id})",
                                    ev.id))
        new_claim(store, rid, "text", ClaimValue("TEXT", re.sub(r"\*\*", "", text)), ev,
                  Provenance.DOCUMENT_DERIVED,
                  meta={"doc_id": v.doc_id, "title": m.group("title")})


_REF = re.compile(r"(?P<doc>KMB(?:-[A-Z0-9]+)+),? (?P<rev>(?:Rev|Issue) \d+)"
                  r"(?:, clause (?P<cl>\d+\.\d+))?")


def extract_references(store: Store, v: DocumentVersion) -> None:
    """Explicit document references in prose (tables such as registers are excluded)."""
    prose = [(i, l) for i, l in enumerate(v.lines, start=1) if l.strip() and not l.startswith("|")]
    joined, starts = "", []
    for i, l in prose:
        starts.append((len(joined), i))
        joined += l.strip() + " "

    def line_at(pos):
        return max(ln for off, ln in starts if off <= pos)

    for m in _REF.finditer(joined):
        cited = m.group("doc")
        if cited == v.doc_id:
            continue
        store.add_entity(Entity(cited, EntityKind.DOCUMENT_ARTIFACT, cited))
        a, b = line_at(m.start()), line_at(m.end() - 1)
        ev = evidence_for(store, v, a, m.group(0), b)
        clause = m.group("cl") or ""
        add_explicit_dependency(
            store, DepType.REFERENCES, v.doc_id, cited, ev, Provenance.DOCUMENT_DERIVED,
            source_attribute=f"clause {clause}" if clause else "",
            meta={"cited_revision": m.group("rev"), "clause": clause})


_POINTS = re.compile(r"levels of (?P<list>(?:\d+ ?%,? (?:and )?)+)")


def extract_tests(store: Store, v: DocumentVersion) -> None:
    tests = []
    for header, rows in md_tables(v):
        t_i, r_i = _col(header, "Test"), _col(header, "Requirement verified")
        title_i = _col(header, "Title")
        if None in (t_i, r_i):
            continue
        for line_no, cells in rows:
            tid = cells[t_i]
            store.add_entity(Entity(tid, EntityKind.TEST, cells[title_i] if title_i is not None
                                    else tid))
            tests.append(tid)
            req = re.fullmatch(r"R-\d+", cells[r_i])
            if req and req.group(0) in store.entities:
                ev = evidence_for(store, v, line_no, f"{tid} | {cells[title_i]} | {cells[r_i]}")
                add_explicit_dependency(store, DepType.VERIFIES, tid, req.group(0), ev,
                                        Provenance.DOCUMENT_DERIVED)
    for i, line in enumerate(v.lines, start=1):
        m = re.search(r"Acceptance of (?P<a>[A-Z]+-\d+) to (?P<b>[A-Z]+-\d+)", line)
        if m:
            text, end = _block(v, i)
            for phrase, gate in CHECKPOINT_PHRASES.items():
                if phrase in text.lower():
                    store.add_entity(Entity(gate, EntityKind.GATE, gate))
                    pre, a = m.group("a").rsplit("-", 1)
                    b = m.group("b").rsplit("-", 1)[1]
                    ev = evidence_for(store, v, i, text, end)
                    for n in range(int(a), int(b) + 1):
                        tid = f"{pre}-{n:0{len(a)}d}"
                        if tid in store.entities:
                            add_explicit_dependency(store, DepType.CONTRIBUTES_TO, tid, gate, ev,
                                                    Provenance.DOCUMENT_DERIVED)
        h = re.match(r"^#+ .*?(?P<tid>[A-Z]+-\d+)\b", line)
        if h and h.group("tid") in tests:
            current = h.group("tid")
            for j in range(i + 1, min(i + 12, len(v.lines) + 1)):
                text, end = _block(v, j)
                pm = _POINTS.search(text)
                if pm:
                    pts = [int(x) for x in re.findall(r"(\d+) ?%", pm.group("list"))]
                    ev = evidence_for(store, v, j, pm.group(0).strip(), end)
                    new_claim(store, current, "test_points_active_power_percent",
                              ClaimValue("LIST", pts, unit="%", text=pm.group(0).strip()), ev,
                              Provenance.DOCUMENT_DERIVED)
                    break


def extract_all(store: Store) -> None:
    """Ordered passes: identifiers first, then the documents that refer to them."""
    all_versions = [v for vs in store.versions.values() for v in vs]
    extract_document_entities(store)
    for v in all_versions:
        extract_equipment_lists(store, v)
    for v in all_versions:
        extract_requirements(store, v)
    for v in all_versions:
        extract_schedule(store, v)
        extract_procurement_tables(store, v)
        extract_spec_clauses(store, v)
        extract_references(store, v)
    for v in all_versions:
        extract_tests(store, v)
    store.log("extraction.complete", claims=len(store.claims),
              dependencies=len(store.dependencies), entities=len(store.entities))
