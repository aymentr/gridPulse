"""Offline, deterministic provider (milestone §1: MockProvider).

MockProvider lets the whole pipeline and the entire test-suite run with no API call and no API key.
Its proposals are derived deterministically from the store:
- dependencies come from the rule-based HeuristicProposer stand-in;
- entity links mirror the free-text mentions already evidenced in the documents;
- change links name the claim pairs behind each deterministically-detected change.

It is a STAND-IN. Its output is not evidence that GridPulse can extract or infer with an AI model;
it exists so the deterministic control layer can be exercised without a provider.
"""
from __future__ import annotations

from dataclasses import asdict

from .. import prompts
from ..inference import HeuristicProposer, _cite_from_evidence
from ..store import Store
from .base import (AIInvocation, ChangeLinkProposal, DependencyProposal, EntityLinkProposal,
                   LLMProvider, latest_version_keys, record_invocation)

MODEL = "mock-v0"


def _prompt_version(name: str) -> str:
    try:
        return prompts.prompt_version(name)
    except KeyError:
        return "v0"


class MockProvider(LLMProvider):
    name = "mock-stand-in-v0"
    model = MODEL

    def __init__(self):
        self._heuristic = HeuristicProposer()

    def _trace(self, store: Store, operation: str, prompt_name: str, output) -> AIInvocation:
        return record_invocation(
            store, provider=self.name, model=self.model, operation=operation,
            prompt_template=prompt_name, prompt_version=_prompt_version(prompt_name),
            input_versions=latest_version_keys(store), output=output,
            latency_ms=0.0, input_tokens=None, output_tokens=None, cost_usd=None)

    def propose_entity_links(self, store: Store) -> list[EntityLinkProposal]:
        out = []
        seen = set()
        for a in store.aliases:
            if a.evidence_id is None or a.alias == a.entity_id:
                continue
            key = (a.entity_id, a.alias.lower())
            if key in seen:
                continue
            seen.add(key)
            out.append(EntityLinkProposal(
                mention=a.alias, entity_id=a.entity_id,
                reasoning=(f"'{a.alias}' is used in the documents to refer to {a.entity_id} "
                           f"({a.basis})."),
                citation=_cite_from_evidence(store, a.evidence_id)))
        self._trace(store, "entity_links", "entity_resolution",
                    [{"mention": p.mention, "entity_id": p.entity_id} for p in out])
        return out

    def interpret_change_links(self, store: Store) -> list[ChangeLinkProposal]:
        out = []
        for ch in store.changes.values():
            out.append(ChangeLinkProposal(
                subject=ch.subject, attribute=ch.attribute,
                claim_ids=[ch.old_claim, ch.new_claim],
                reasoning=(f"The earlier and later statements of {ch.subject} {ch.attribute} are "
                           f"worded differently but describe the same underlying claim.")))
        self._trace(store, "change_links", "change_interpretation",
                    [asdict(p) for p in out])
        return out

    def propose_dependencies(self, store: Store) -> list[DependencyProposal]:
        proposals = self._heuristic.propose(store)
        self._trace(store, "dependencies", "dependency_inference",
                    [{"type": p.type.value, "source": p.source, "target": p.target,
                      "source_attribute": p.source_attribute} for p in proposals])
        return proposals
