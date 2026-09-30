"""Real Claude provider (milestone §1, §2, §3, §9).

Uses the official Anthropic SDK. The model only ever returns STRUCTURED proposals (JSON schema);
the deterministic layer (gridpulse.inference) re-verifies every citation and owns all validation.
This module therefore contains no trust decisions — only the API call, structured-output parsing
and invocation tracing.

The SDK is imported lazily so the package (and the offline test-suite) works without it installed.
A `client` can be injected for testing without a network call or API key.
"""
from __future__ import annotations

import json
import time

from ..model import DepType
from .. import prompts
from ..store import Store
from .base import (Citation, ChangeLinkProposal, DependencyProposal, EntityLinkProposal,
                   LLMProvider, MissingConfigError, ProviderError, claim_catalogue,
                   entity_catalogue, latest_version_keys, numbered_context, record_invocation)

DEFAULT_MODEL = "claude-opus-5-5"                       # per Anthropic SDK guidance
MAX_TOKENS = 16000
_PRICES = {"claude-opus-5-5": (4.0, 20.0)}             # (input, output) USD per 1M tokens

_CITATION_SCHEMA = {
    "type": "object",
    "properties": {
        "doc_id": {"type": "string"}, "version_no": {"type": "integer"},
        "line_start": {"type": "integer"}, "line_end": {"type": "integer"},
        "quote": {"type": "string"}},
    "required": ["doc_id", "version_no", "line_start", "line_end", "quote"],
    "additionalProperties": False,
}
_DEP_SCHEMA = {
    "type": "object",
    "properties": {"proposals": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "type": {"type": "string"}, "source": {"type": "string"},
            "target": {"type": "string"}, "reasoning": {"type": "string"},
            "source_attribute": {"type": "string"},
            "citations": {"type": "array", "items": _CITATION_SCHEMA}},
        "required": ["type", "source", "target", "reasoning", "citations"],
        "additionalProperties": False}}},
    "required": ["proposals"], "additionalProperties": False,
}
_ENTITY_SCHEMA = {
    "type": "object",
    "properties": {"proposals": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "mention": {"type": "string"}, "entity_id": {"type": "string"},
            "reasoning": {"type": "string"}, "citation": _CITATION_SCHEMA},
        "required": ["mention", "entity_id", "reasoning", "citation"],
        "additionalProperties": False}}},
    "required": ["proposals"], "additionalProperties": False,
}
_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {"proposals": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "subject": {"type": "string"}, "attribute": {"type": "string"},
            "claim_ids": {"type": "array", "items": {"type": "string"}},
            "reasoning": {"type": "string"}},
        "required": ["subject", "attribute", "claim_ids", "reasoning"],
        "additionalProperties": False}}},
    "required": ["proposals"], "additionalProperties": False,
}


# --- pure parsers (testable without a client; ignore any extra keys the model returns, so the
#     model can never set validation/confidence/level — the backend owns those) ---------------

def _citation(d: dict) -> Citation:
    return Citation(str(d["doc_id"]), int(d["version_no"]), int(d["line_start"]),
                    int(d["line_end"]), str(d["quote"]))


def _proposals_list(data) -> list:
    if not isinstance(data, dict) or not isinstance(data.get("proposals"), list):
        raise ProviderError("malformed model output: expected an object with a 'proposals' list")
    return data["proposals"]


def parse_dependencies(data) -> list[DependencyProposal]:
    out = []
    for p in _proposals_list(data):
        try:
            dep_type = DepType(str(p["type"]).upper())
        except (KeyError, ValueError):
            continue                                    # unknown relationship type → drop
        try:
            cites = [_citation(c) for c in p.get("citations", [])]
            out.append(DependencyProposal(
                type=dep_type, source=str(p["source"]), target=str(p["target"]),
                reasoning=str(p.get("reasoning", "")), citations=cites,
                source_attribute=str(p.get("source_attribute", ""))))
        except (KeyError, TypeError, ValueError) as e:
            raise ProviderError(f"malformed dependency proposal: {e}") from e
    return out


def parse_entity_links(data) -> list[EntityLinkProposal]:
    out = []
    for p in _proposals_list(data):
        try:
            out.append(EntityLinkProposal(
                mention=str(p["mention"]), entity_id=str(p["entity_id"]),
                reasoning=str(p.get("reasoning", "")),
                citation=_citation(p["citation"]) if p.get("citation") else None))
        except (KeyError, TypeError, ValueError) as e:
            raise ProviderError(f"malformed entity-link proposal: {e}") from e
    return out


def parse_change_links(data) -> list[ChangeLinkProposal]:
    out = []
    for p in _proposals_list(data):
        try:
            out.append(ChangeLinkProposal(
                subject=str(p["subject"]), attribute=str(p["attribute"]),
                claim_ids=[str(i) for i in p["claim_ids"]],
                reasoning=str(p.get("reasoning", ""))))
        except (KeyError, TypeError, ValueError) as e:
            raise ProviderError(f"malformed change-link proposal: {e}") from e
    return out


def _extract_text(resp) -> str:
    if getattr(resp, "stop_reason", None) == "refusal":
        raise ProviderError("model refused the request")
    parts = [b.text for b in getattr(resp, "content", []) if getattr(b, "type", None) == "text"]
    if not parts:
        raise ProviderError("model returned no text content")
    return "".join(parts)


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, model: str | None = None, api_key: str | None = None, client=None):
        self.model = model or DEFAULT_MODEL
        if client is not None:
            self._client = client
            return
        if not api_key:
            raise MissingConfigError(
                "the 'anthropic' provider requires ANTHROPIC_API_KEY (set GRIDPULSE_LLM_PROVIDER"
                "=mock to run offline)")
        try:
            import anthropic
        except ImportError as e:
            raise MissingConfigError(
                "the 'anthropic' package is not installed; `pip install anthropic` or set "
                "GRIDPULSE_LLM_PROVIDER=mock") from e
        self._client = anthropic.Anthropic(api_key=api_key)

    # --- provider operations ---------------------------------------------------------------
    def propose_dependencies(self, store: Store) -> list[DependencyProposal]:
        return self._invoke(store, "dependencies", "dependency_inference", _DEP_SCHEMA,
                            parse_dependencies, self._context(store))

    def propose_entity_links(self, store: Store) -> list[EntityLinkProposal]:
        return self._invoke(store, "entity_links", "entity_resolution", _ENTITY_SCHEMA,
                            parse_entity_links, self._context(store))

    def interpret_change_links(self, store: Store) -> list[ChangeLinkProposal]:
        ctx = (self._context(store) + "\n\n## Claim catalogue\n" + claim_catalogue(store))
        return self._invoke(store, "change_links", "change_interpretation", _CHANGE_SCHEMA,
                            parse_change_links, ctx)

    def _context(self, store: Store) -> str:
        return (f"## Entity catalogue\n{entity_catalogue(store)}\n\n"
                f"## Documents (line-numbered)\n{numbered_context(store)}")

    # --- one traced model call -------------------------------------------------------------
    def _invoke(self, store, operation, prompt_name, schema, parse_fn, user_content):
        system, version = prompts.get_prompt(prompt_name)
        started = time.perf_counter()
        error = ""
        raw = None
        try:
            resp = self._client.messages.create(
                model=self.model, max_tokens=MAX_TOKENS, system=system,
                thinking={"type": "adaptive"},
                output_config={"effort": "high",
                               "format": {"type": "json_schema", "name": operation,
                                          "schema": schema}},
                messages=[{"role": "user", "content": user_content}])
            text = _extract_text(resp)
            try:
                raw = json.loads(text)
            except json.JSONDecodeError as e:
                raise ProviderError(f"model output was not valid JSON: {e}") from e
            proposals = parse_fn(raw)
        except ProviderError as e:
            error = str(e)
            self._record(store, operation, prompt_name, version, None, started, None, error)
            raise
        except Exception as e:                              # SDK / network error; no secrets
            error = f"{type(e).__name__}: {e}"
            self._record(store, operation, prompt_name, version, None, started, None, error)
            raise ProviderError(f"anthropic call failed during {operation}: {error}") from e
        self._record(store, operation, prompt_name, version, raw, started, resp, "")
        return proposals

    def _record(self, store, operation, prompt_name, version, raw, started, resp, error):
        usage = getattr(resp, "usage", None)
        in_tok = getattr(usage, "input_tokens", None)
        out_tok = getattr(usage, "output_tokens", None)
        cost = None
        if in_tok is not None and out_tok is not None and self.model in _PRICES:
            pi, po = _PRICES[self.model]
            cost = round(in_tok / 1e6 * pi + out_tok / 1e6 * po, 6)
        record_invocation(
            store, provider=self.name, model=self.model, operation=operation,
            prompt_template=prompt_name, prompt_version=version,
            input_versions=latest_version_keys(store), output=raw,
            latency_ms=round((time.perf_counter() - started) * 1000, 2),
            input_tokens=in_tok, output_tokens=out_tok, cost_usd=cost, error=error)
