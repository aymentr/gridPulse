"""Provider-agnostic LLM boundary (milestone §1–§3, §9).

    documents → LLM PROPOSAL → deterministic validation → REVIEW QUEUE → human confirmation

The LLM only ever PROPOSES. It cannot create confirmed facts, confirmed dependencies, validated
state or Level-3 determinations: the proposal schemas below carry no validation/confidence/level
field the model can set, and the deterministic apply-layer (see gridpulse.inference) owns those.

Every real invocation is traced (provider, model, prompt version, input versions, output, tokens,
latency) via `AIInvocation`. No secrets are ever stored in a trace.
"""
from __future__ import annotations

import abc
import os
from dataclasses import dataclass, field

from ..model import DepType
from ..store import Store


# --- structured proposal schemas (milestone §3) ---------------------------------------------
# None of these carry validation / confidence / level. Those are the backend's to assign.

@dataclass(frozen=True)
class Citation:
    doc_id: str
    version_no: int
    line_start: int
    line_end: int
    quote: str


@dataclass
class DependencyProposal:
    type: DepType
    source: str
    target: str
    reasoning: str
    citations: list[Citation] = field(default_factory=list)
    source_attribute: str = ""


@dataclass
class EntityLinkProposal:
    """A free-text mention → an existing canonical entity id (entity resolution, §5)."""
    mention: str
    entity_id: str
    reasoning: str
    citation: Citation | None = None


@dataclass
class ChangeLinkProposal:
    """Two differently-worded claims judged to be the same underlying claim (§6).

    Carries no values and no computed difference: value comparison stays deterministic.
    """
    subject: str
    attribute: str
    claim_ids: list[str]
    reasoning: str


# --- AI invocation trace (milestone §9) -----------------------------------------------------

@dataclass
class AIInvocation:
    id: str
    provider: str
    model: str
    operation: str
    prompt_template: str
    prompt_version: str
    input_versions: list[str]
    timestamp: str
    output: object = None            # raw structured output (never secrets)
    evidence_refs: list[str] = field(default_factory=list)
    accepted: int = 0
    rejected: int = 0
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None
    error: str = ""


def record_invocation(store: Store, **kw) -> AIInvocation:
    inv = AIInvocation(id=store.next_id("AI"), timestamp=store.clock().isoformat(), **kw)
    store.ai_invocations.append(inv)
    store.log("ai.invocation", invocation=inv.id, provider=inv.provider, model=inv.model,
              operation=inv.operation, prompt=f"{inv.prompt_template}:{inv.prompt_version}",
              latency_ms=inv.latency_ms, tokens=inv.output_tokens)
    return inv


# --- context builders (shared by real providers) --------------------------------------------

def latest_version_keys(store: Store) -> list[str]:
    return sorted(v.key for v in store.all_latest_versions())


def numbered_context(store: Store) -> str:
    """Every latest document version with 1-based line numbers, so the model can cite exactly."""
    parts = []
    for v in sorted(store.all_latest_versions(), key=lambda v: v.doc_id):
        head = (f"### {v.doc_id} {v.revision_label} "
                f"(doc_id={v.doc_id}, version_no={v.version_no})")
        body = "\n".join(f"{i}: {line}" for i, line in enumerate(v.lines, start=1))
        parts.append(f"{head}\n{body}")
    return "\n\n".join(parts)


def entity_catalogue(store: Store) -> str:
    rows = [f"- {e.id} | {e.kind.value} | {e.name}"
            for e in sorted(store.entities.values(), key=lambda e: e.id)]
    return "\n".join(rows)


def claim_catalogue(store: Store) -> str:
    rows = []
    for c in sorted(store.claims.values(), key=lambda c: c.id):
        v = store.claim_version(c)
        src = f"{v.doc_id} {v.revision_label}" if v else "?"
        val = c.value.value
        rows.append(f"- {c.id} | {c.subject} | {c.attribute} | {val} | {src}")
    return "\n".join(rows)


# --- provider interface (milestone §1) ------------------------------------------------------

class LLMProvider(abc.ABC):
    """Every operation records exactly one AIInvocation on the store and returns proposals.

    The pipeline verifies and applies the proposals deterministically; nothing here writes trusted
    or validated state.
    """
    name: str = "base"
    model: str = ""

    @abc.abstractmethod
    def propose_entity_links(self, store: Store) -> list[EntityLinkProposal]:
        ...

    @abc.abstractmethod
    def interpret_change_links(self, store: Store) -> list[ChangeLinkProposal]:
        ...

    @abc.abstractmethod
    def propose_dependencies(self, store: Store) -> list[DependencyProposal]:
        ...


# --- configuration and selection (milestone §2) ---------------------------------------------

class ProviderError(Exception):
    """A real provider failed at call or parse time (never leaks secrets)."""


class MissingConfigError(ProviderError):
    """The selected provider is missing required configuration (e.g. API key)."""


ENV_PROVIDER = "GRIDPULSE_LLM_PROVIDER"
ENV_MODEL = "GRIDPULSE_LLM_MODEL"


def from_env(env: dict | None = None) -> LLMProvider:
    """Select a provider from the environment. Defaults to the offline MockProvider so the
    deterministic pipeline and test-suite never need an API key. If a real provider is selected but
    its configuration is missing, this raises MissingConfigError with a clear message."""
    env = os.environ if env is None else env
    name = (env.get(ENV_PROVIDER) or "mock").strip().lower()
    model = env.get(ENV_MODEL) or None
    if name in ("mock", "", "none", "offline"):
        from .mock import MockProvider
        return MockProvider()
    if name in ("anthropic", "claude"):
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider(model=model, api_key=env.get("ANTHROPIC_API_KEY"))
    raise MissingConfigError(
        f"unknown {ENV_PROVIDER}={name!r}; supported: 'mock', 'anthropic'")
