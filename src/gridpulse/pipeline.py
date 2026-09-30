"""End-to-end run for one scenario directory."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .changes import detect_changes, detect_stale_references
from .evidence import refresh_freshness
from .extract import extract_all
from .inference import HeuristicProposer, Proposer, apply_proposals
from .ingest import ingest_paths, scenario_files
from .investigation import Bundle, investigate
from .model import FindingKind
from .review import ReviewQueue
from .store import Store


@dataclass
class Result:
    store: Store
    queue: ReviewQueue
    bundles: list[Bundle]
    rejected_proposals: list


def run(scenario_dir: Path, proposer: Proposer | None = None, folders=None,
        store: Store | None = None) -> Result:
    store = store or Store()
    files = scenario_files(Path(scenario_dir), folders) if folders else \
        scenario_files(Path(scenario_dir))
    ingest_paths(store, files)
    extract_all(store)
    refresh_freshness(store)
    detect_changes(store)
    detect_stale_references(store)
    proposer = proposer or HeuristicProposer()
    _, rejected = apply_proposals(store, proposer.propose(store), proposer.name)
    queue = ReviewQueue(store)
    queue.enqueue_detected()
    bundles = [investigate(store, f) for f in list(store.findings.values())
               if f.kind == FindingKind.CHANGE]
    return Result(store, queue, bundles, rejected)
