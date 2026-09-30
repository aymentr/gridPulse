"""Impact investigation → investigation bundle (architecture §10, §13; D-037 section structure).

The bundle is a structured investigation, not a verdict. All text passes the safety guard.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import safety
from .calc import calendar_days, points_below, range_gap
from .graph import Path, traverse
from .model import (Claim, DepType, EntityKind, Finding, FindingKind, RelConfidence, Validation)
from .store import Store

CHECKPOINT_KEYWORDS = [                       # entity-name keyword → neutral checkpoint (D-033)
    ("grid compliance", "GRID COMPLIANCE CHECKPOINT"),
    ("energization", "ENERGIZATION CHECKPOINT"),
    ("commissioning", "COMMISSIONING CHECKPOINT"),
    ("installation", "CONSTRUCTION CHECKPOINT"),
    ("delivery", "PROCUREMENT CHECKPOINT"),
]
ROLE = {                                      # simple routing table (D-008 recommendation B)
    "date": "Project Controls",
    "sequence": "Commissioning Engineer",
    "technical": "Electrical/Grid Engineer",
    "document": "EPC technical lead",
}


@dataclass
class Bundle:
    finding_id: str
    title: str
    validated: list[str] = field(default_factory=list)
    observed: list[str] = field(default_factory=list)
    inferred: list[str] = field(default_factory=list)
    calculations: list[str] = field(default_factory=list)
    exposures: list[str] = field(default_factory=list)
    human_validation: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    uncertainty: list[str] = field(default_factory=list)
    non_conclusions: list[str] = field(default_factory=list)
    impacts: list[dict] = field(default_factory=list)

    def to_markdown(self) -> str:
        def sec(title, items, empty="None."):
            body = "\n".join(f"- {i}" for i in items) if items else f"- {empty}"
            return f"### {title}\n{body}\n"
        md = (f"## Investigation {self.finding_id}: {self.title}\n\n"
              "Pre-review investigation output. Not an engineering or project determination.\n\n"
              + sec("VALIDATED INFORMATION", self.validated,
                    "None — no human review has occurred.")
              + sec("OBSERVED INFORMATION", self.observed)
              + sec("INFERRED RELATIONSHIPS", self.inferred)
              + sec("DETERMINISTIC CALCULATIONS", self.calculations)
              + sec("POTENTIAL EXPOSURES", self.exposures)
              + sec("HUMAN VALIDATION REQUIRED", self.human_validation)
              + sec("UNCERTAINTY", self.uncertainty)
              + sec("NOT ESTABLISHED BY THIS INVESTIGATION", self.non_conclusions)
              + sec("EVIDENCE", self.evidence))
        return safety.check(md)

    def to_dict(self) -> dict:
        safety.check(self.to_markdown())
        return {k: v for k, v in self.__dict__.items()}


def _name(store: Store, eid: str) -> str:
    e = store.entities.get(eid)
    return f"{eid} ({e.name})" if e and e.name and e.name != eid else eid


def _checkpoint(store: Store, eid: str) -> str:
    e = store.entities[eid]
    if e.kind == EntityKind.GATE:
        return e.name
    if e.kind == EntityKind.DOCUMENT_ARTIFACT and "-SPC-" in eid:
        return "ENGINEERING CHECKPOINT"
    text = e.name.lower()
    return next((cp for kw, cp in CHECKPOINT_KEYWORDS if kw in text), "")


def _dep_label(store: Store, d) -> str:
    prov = "/".join(p.value for p in d.provenance)
    attr = f" [{d.source_attribute}]" if d.source_attribute else ""
    proposer = f" (proposer: {d.proposer})" if d.proposer else ""
    return (f"{_name(store, d.source)}{attr} —{d.type.value}→ {_name(store, d.target)} · "
            f"{d.confidence.value} · {d.validation.value} · {prov}{proposer}")


def _ev(store: Store, eid: str) -> str:
    e = store.evidence[eid]
    flag = "" if e.verified else " [UNVERIFIED]"
    fresh = "" if e.freshness.value == "CURRENT" else f" [{e.freshness.value}]"
    return f"{eid}: {e.location.describe()} — \"{e.quote[:160]}\"{flag}{fresh}"


def _claim_line(store: Store, c: Claim) -> str:
    v = store.claim_version(c)
    val = c.value.value.strftime("%d %b %Y") if c.value.kind == "DATE" else c.value.value
    q = f" ({c.qualifier})" if c.qualifier else ""
    return (f"{_name(store, c.subject)} · {c.attribute} = {val}{q} — source {v.doc_id} "
            f"{v.revision_label}".rstrip() + f" · {c.validation.value} · evidence "
            f"{c.evidence_confidence.value} [{', '.join(c.evidence_ids)}]")


def _latest(store: Store, subject: str, attribute: str) -> Claim | None:
    cs = store.claims_for(subject, attribute)
    if not cs:
        return None
    return sorted(cs, key=lambda c: (store.claim_version(c).source_date or 0,
                                     store.claim_version(c).version_no))[-1]


def investigate(store: Store, finding: Finding) -> Bundle:
    if finding.kind != FindingKind.CHANGE:
        raise ValueError("investigations start from a CHANGE finding")
    ch = store.changes[finding.ref_id]
    old, new = store.claims[ch.old_claim], store.claims[ch.new_claim]
    b = Bundle(finding.id, finding.summary)
    evidence_ids = set(old.evidence_ids + new.evidence_ids)

    b.observed += [f"Earlier observation: {_claim_line(store, old)}",
                   f"Later observation: {_claim_line(store, new)}"]
    b.validated += [f"{_claim_line(store, c)}" for c in (old, new)
                    if c.validation == Validation.CONFIRMED]

    # related conflicts and stale references
    for cf in store.conflicts.values():
        if cf.subject == ch.subject and cf.attribute == ch.attribute:
            cs = [store.claims[i] for i in cf.claim_ids]
            b.observed.append("Source divergence: " + "; ".join(_claim_line(store, c) for c in cs))
            evidence_ids.update(e for c in cs for e in c.evidence_ids)
            b.human_validation.append(
                f"Which source reflects the current plan for {ch.subject} {ch.attribute}? "
                f"— {ROLE['date']}")
            b.uncertainty.append("The supplied sources disagree; no source has been selected "
                                 "as authoritative.")

    kind = new.value.kind if new.value.kind in ("DATE", "TEXT") else "TEXT"
    starts, attribute = [ch.subject], ""
    if kind == "DATE":
        starts += [c.meta["activity"] for c in store.claims_for(ch.subject, ch.attribute)
                   if c.meta.get("activity")]
    else:
        doc_id = new.meta.get("doc_id")
        if doc_id:
            starts.append(doc_id)
        attribute = ch.attribute
        for f in store.findings.values():
            if f.kind == FindingKind.STALE_EVIDENCE:
                d = store.dependencies[f.ref_id]
                if d.target == doc_id and d.source_attribute in ("", attribute):
                    b.observed.append(f"Stale reference: {f.summary}")
                    evidence_ids.update(f.evidence_ids)
                    b.human_validation.append(
                        f"Is {d.source} to be reviewed against the latest revision of "
                        f"{d.target}? — {ROLE['document']}")
    paths = traverse(store, sorted(set(starts)), kind, attribute)

    for p in paths:
        _record_path(store, b, p, evidence_ids)
    _calculations(store, b, ch, old, new, paths, kind)

    if kind == "DATE":
        b.uncertainty.append("Float, installation duration and resequencing options are not "
                             "evidenced in the supplied documents.")
    if any(p.inferred for p in paths):
        b.uncertainty.append("One or more impact paths include an INFERRED · UNVALIDATED "
                             "relationship; downstream items on those paths are potential only.")
    if not paths:
        b.uncertainty.append("No relationship from the changed item to other project "
                             "information was identified in the supplied documents.")
        b.human_validation.append(f"Does the change to {ch.subject} {ch.attribute} affect other "
                                  f"project information? — {ROLE['technical']}")
    b.non_conclusions += [
        "No determination is made about whether any milestone or checkpoint date changes.",
        "No determination is made about compliance with any requirement or about any test result.",
        "No determination is made about which source is correct, or about any party's intent.",
        "No determination is made about contractual, notification or engineering obligations.",
    ]
    b.evidence = [_ev(store, e) for e in sorted(evidence_ids)]
    b.to_markdown()                                   # safety check before release
    store.log("investigation.bundle", finding=finding.id, impacts=len(b.impacts))
    return b


def _record_path(store: Store, b: Bundle, p: Path, evidence_ids: set) -> None:
    for h in p.hops:
        evidence_ids.update(h.dep.evidence_ids)
        if h.dep.confidence == RelConfidence.INFERRED:
            line = _dep_label(store, h.dep) + (f" — reasoning: {h.dep.reasoning}"
                                               if h.dep.reasoning else "")
            if line not in b.inferred:
                b.inferred.append(line)
                role = ROLE["sequence"] if h.dep.type == DepType.PRECEDES else ROLE["technical"]
                b.human_validation.append(
                    f"Confirm or reject the inferred relationship {h.dep.source} "
                    f"{h.dep.type.value} {h.dep.target} — {role}")
        else:
            line = "Explicit relationship: " + _dep_label(store, h.dep)
            if line not in b.observed:
                b.observed.append(line)
    cp = _checkpoint(store, p.end)
    path_text = " → ".join([p.hops[0].dep.source if p.hops[0].reached == p.hops[0].dep.target
                            else p.hops[0].dep.target] + [h.reached for h in p.hops])
    status = "inferred path" if p.inferred else "explicit path"
    exposure = (f"Potential impact identified: {_name(store, p.end)}"
                + (f" ({cp})" if cp else "") + f" via {path_text} [{status}, unvalidated]. "
                "Expert validation required.")
    b.exposures.append(exposure)
    b.impacts.append({"entity": p.end, "checkpoint": cp, "path": path_text,
                      "inferred": p.inferred, "unvalidated": p.unvalidated,
                      "dependencies": [h.dep.id for h in p.hops]})


def _calculations(store: Store, b: Bundle, ch, old: Claim, new: Claim, paths, kind) -> None:
    def show(c):
        ins = ", ".join(f"{i['label']} = {i['value']} [{i['claim_id']}]" for i in c.inputs)
        b.calculations.append(f"{c.operation}: {c.result} {c.unit} — inputs: {ins}. {c.note}")

    if kind == "DATE":
        for c in store.calculations.values():
            if {i["claim_id"] for i in c.inputs} == {old.id, new.id}:
                show(c)
        direct = [p for p in paths if len(p.hops) == 1 and p.hops[0].dep.type == DepType.PRECEDES]
        sched = [c for c in store.claims_for(ch.subject, ch.attribute) if c.meta.get("activity")]
        sched = sorted(sched, key=lambda c: store.claim_version(c).source_date or 0)[-1:] \
            if sched else []
        for p in direct:
            succ_start = _latest(store, p.end, "planned_start")
            if not succ_start:
                continue
            for base in sched:
                show(calendar_days(store, base, succ_start,
                                   f"{ch.attribute} (schedule)", f"{p.end} planned start"))
            show(calendar_days(store, succ_start, new,
                               f"{p.end} planned start", f"{ch.attribute} (latest report)"))
    else:
        for p in paths:
            end = store.entities[p.end]
            if end.kind == EntityKind.REQUIREMENT:
                req = _latest(store, p.end, "text")
                c = range_gap(store, new, req, f"{ch.subject} {ch.attribute}", p.end,
                              "Stated ranges compared as written; they may be stated at "
                              "different measurement points or on different bases.")
                if c:
                    show(c)
            if end.kind == EntityKind.TEST:
                pts = _latest(store, p.end, "test_points_active_power_percent")
                if pts:
                    c = points_below(store, pts, new, f"{p.end} test points",
                                     f"{ch.subject} {ch.attribute}",
                                     "Values compared as written; bases may differ.")
                    if c:
                        show(c)
