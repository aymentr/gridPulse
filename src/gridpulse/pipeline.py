"""End-to-end run for one scenario directory.

    DOCUMENTS → extraction → LLM PROPOSAL → deterministic validation → REVIEW QUEUE → …

The LLM (provider) proposes entity links, change-identity links and dependencies. The deterministic
layer verifies every citation, owns change/conflict detection and calculation, and routes findings
to human review. Runs offline by default (MockProvider); a real provider is selected via the
environment (GRIDPULSE_LLM_PROVIDER) or passed in.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .changes import detect_changes, detect_stale_references
from .evidence import refresh_freshness
from .extract import extract_all
from .inference import apply_change_links, apply_entity_links, apply_proposals
from .ingest import ingest_paths, scenario_files
from .investigation import Bundle, investigate
from .model import FindingKind
from .providers.base import LLMProvider, from_env
from .review import ReviewQueue
from .store import Store


@dataclass
class Result:
    store: Store
    queue: ReviewQueue
    bundles: list[Bundle]
    rejected_proposals: list
    provider: str = ""
    rejected_entity_links: list = field(default_factory=list)
    rejected_change_links: list = field(default_factory=list)


def run(scenario_dir, provider: LLMProvider | None = None, proposer=None, folders=None,
        store: Store | None = None) -> Result:
    store = store or Store()
    files = scenario_files(Path(scenario_dir), folders) if folders else \
        scenario_files(Path(scenario_dir))
    ingest_paths(store, files)
    extract_all(store)                                  # deterministic structured import
    refresh_freshness(store)

    provider = provider or from_env()

    # Entity resolution (§5): LLM proposes free-text → entity links; backend verifies + records.
    links = provider.propose_entity_links(store)
    _, rej_entity = apply_entity_links(store, links, provider.name,
                                       invocation=_last(store))

    detect_changes(store)                               # deterministic value comparison (§6)
    detect_stale_references(store)

    # Semantic change interpretation (§6): claim-identity links corroborated against detection.
    clinks = provider.interpret_change_links(store)
    _, rej_change = apply_change_links(store, clinks, provider.name, invocation=_last(store))

    # Dependency inference (§7): the AI capability. `proposer` kept for backward compatibility.
    if proposer is not None:
        dep_proposals, dep_name, inv = proposer.propose(store), proposer.name, None
    else:
        dep_proposals, dep_name, inv = (provider.propose_dependencies(store),
                                        provider.name, _last(store))
    _, rejected = apply_proposals(store, dep_proposals, dep_name, invocation=inv)

    queue = ReviewQueue(store)
    queue.enqueue_detected()
    bundles = [investigate(store, f) for f in list(store.findings.values())
               if f.kind == FindingKind.CHANGE]
    return Result(store, queue, bundles, rejected, provider=provider.name,
                  rejected_entity_links=rej_entity, rejected_change_links=rej_change)


def _last(store: Store):
    """The AIInvocation just recorded by a provider operation, if any."""
    return store.ai_invocations[-1] if store.ai_invocations else None
