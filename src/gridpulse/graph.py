"""Typed dependency traversal (architecture §9–§10). Not a scheduling engine.

Propagation matrix (§10.3, D-035 initial): which relationship types carry which change kind, and in
which direction impact flows. REJECTED relationships are never traversed.
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import Dependency, DepType, RelConfidence, Validation
from .store import Store

OUT, IN = "out", "in"
PROPAGATION = {
    "DATE": [(DepType.PRECEDES, OUT), (DepType.CONTRIBUTES_TO, OUT)],
    "TEXT": [(DepType.REFERENCES, IN), (DepType.SPECIFIES, OUT), (DepType.VERIFIES, IN),
             (DepType.CONTRIBUTES_TO, OUT)],
}


@dataclass
class Hop:
    dep: Dependency
    reached: str


@dataclass
class Path:
    hops: list[Hop]

    @property
    def end(self) -> str:
        return self.hops[-1].reached

    @property
    def inferred(self) -> bool:
        return any(h.dep.confidence == RelConfidence.INFERRED for h in self.hops)

    @property
    def unvalidated(self) -> bool:
        return any(h.dep.validation != Validation.CONFIRMED for h in self.hops)


def traverse(store: Store, starts: list[str], change_kind: str, attribute: str = "",
             max_depth: int = 6) -> list[Path]:
    """All shortest paths from the start entities. `attribute` restricts the first hop of
    attribute-scoped relationships (e.g. a reference to 'clause 5.3')."""
    rules = PROPAGATION[change_kind]
    frontier = [(s, []) for s in starts]
    seen = set(starts)
    paths = []
    for _ in range(max_depth):
        nxt = []
        for node, hops in frontier:
            for d in store.dependencies.values():
                if d.validation == Validation.REJECTED:
                    continue
                for dep_type, direction in rules:
                    if d.type != dep_type:
                        continue
                    here, there = (d.source, d.target) if direction == OUT else (d.target, d.source)
                    if here != node or there in seen:
                        continue
                    if not hops and attribute and d.source_attribute \
                            and d.source_attribute != attribute:
                        continue
                    new = hops + [Hop(d, there)]
                    seen.add(there)
                    paths.append(Path(new))
                    nxt.append((there, new))
        frontier = nxt
    return paths
