"""Provider abstraction, structured output, the AI trust boundary, tracing and provider switching
(milestone §1–§11). No network and no API key: the real provider is exercised with a fake client."""
import json
import tempfile
import unittest
from pathlib import Path

from gridpulse.inference import (apply_change_links, apply_entity_links, apply_proposals)
from gridpulse.ingest import ingest_file
from gridpulse.model import (Entity, EntityKind, Provenance, RelConfidence, Validation)
from gridpulse.store import Store
from gridpulse import prompts
from gridpulse.providers import (AnthropicProvider, ChangeLinkProposal, Citation,
                                 DependencyProposal, EntityLinkProposal, MissingConfigError,
                                 MockProvider, ProviderError, from_env)
from gridpulse.providers import anthropic_provider as ap
from gridpulse.model import DepType

DOC = """# Timing Note

| | |
|---|---|
| Document no. | KMB-NOTE-001 Rev 1 |
| Date | 1 March 2026 |

Commissioning shall commence once all HV equipment is installed.
The Main unit is delivered to site first.
"""


def tiny_store():
    store = Store()
    tmp = Path(tempfile.mkdtemp())
    p = tmp / "note.md"
    p.write_text(DOC)
    v = ingest_file(store, p)
    store.add_entity(Entity("A-01", EntityKind.ACTIVITY, "Install main unit"))
    store.add_entity(Entity("A-02", EntityKind.ACTIVITY, "Commissioning"))
    return store, v


def line_with(v, needle):
    return next(i for i, l in enumerate(v.lines, 1) if needle in l)


# --- fake Anthropic client (no network) -----------------------------------------------------

class _Block:
    def __init__(self, text):
        self.type, self.text = "text", text


class _Usage:
    def __init__(self, i, o):
        self.input_tokens, self.output_tokens = i, o


class _Resp:
    def __init__(self, text, stop_reason="end_turn"):
        self.content = [_Block(text)]
        self.usage = _Usage(1200, 340)
        self.stop_reason = stop_reason
        self.model = "claude-opus-5-5"


class _Messages:
    def __init__(self, resp_or_exc):
        self._r = resp_or_exc

    def create(self, **kwargs):
        if isinstance(self._r, Exception):
            raise self._r
        return self._r


class FakeClient:
    def __init__(self, text, stop_reason="end_turn", exc=None):
        self.messages = _Messages(exc if exc else _Resp(text, stop_reason))


class MockProviderTests(unittest.TestCase):
    def test_conforms_and_records_one_trace_per_operation(self):
        store, _ = tiny_store()
        p = MockProvider()
        self.assertEqual(p.propose_entity_links(store), [])       # no aliases yet
        self.assertEqual(len(store.ai_invocations), 1)
        p.interpret_change_links(store)
        p.propose_dependencies(store)
        self.assertEqual([i.operation for i in store.ai_invocations],
                         ["entity_links", "change_links", "dependencies"])
        for inv in store.ai_invocations:
            self.assertEqual(inv.provider, "mock-stand-in-v0")
            self.assertEqual(inv.prompt_version, "v1")            # prompt version recorded
            self.assertTrue(inv.input_versions)


class ProviderSwitchingTests(unittest.TestCase):
    def test_default_is_mock(self):
        self.assertIsInstance(from_env({}), MockProvider)

    def test_env_selects_mock(self):
        self.assertIsInstance(from_env({"GRIDPULSE_LLM_PROVIDER": "mock"}), MockProvider)

    def test_env_selects_anthropic_but_needs_key(self):
        with self.assertRaises(MissingConfigError):
            from_env({"GRIDPULSE_LLM_PROVIDER": "anthropic"})       # no ANTHROPIC_API_KEY

    def test_unknown_provider_fails_clearly(self):
        with self.assertRaises(MissingConfigError):
            from_env({"GRIDPULSE_LLM_PROVIDER": "gpt"})


class MissingConfigTests(unittest.TestCase):
    def test_anthropic_without_key_or_client(self):
        with self.assertRaises(MissingConfigError):
            AnthropicProvider(api_key=None)

    def test_model_is_configurable(self):
        prov = AnthropicProvider(model="claude-sonnet-5-5", client=FakeClient("{}"))
        self.assertEqual(prov.model, "claude-sonnet-5-5")


class StructuredOutputParsingTests(unittest.TestCase):
    def test_valid_dependency_output(self):
        data = {"proposals": [{"type": "PRECEDES", "source": "A-01", "target": "A-02",
                               "reasoning": "x", "citations": [
                    {"doc_id": "D", "version_no": 1, "line_start": 1, "line_end": 1,
                     "quote": "q"}]}]}
        props = ap.parse_dependencies(data)
        self.assertEqual((props[0].type, props[0].source), (DepType.PRECEDES, "A-01"))

    def test_malformed_output_raises(self):
        for bad in ({"foo": 1}, [], "nope", {"proposals": "not a list"}):
            with self.assertRaises(ProviderError):
                ap.parse_dependencies(bad)

    def test_unknown_relationship_type_dropped(self):
        data = {"proposals": [{"type": "TELEPORTS", "source": "A-01", "target": "A-02",
                               "reasoning": "x", "citations": []}]}
        self.assertEqual(ap.parse_dependencies(data), [])

    def test_model_cannot_set_validation_or_confidence(self):
        # extra keys the model might return are ignored — the backend owns those states
        data = {"proposals": [{"type": "PRECEDES", "source": "A-01", "target": "A-02",
                               "reasoning": "x", "validation": "CONFIRMED",
                               "confidence": "EXPLICIT", "level": 3, "citations": []}]}
        p = ap.parse_dependencies(data)[0]
        self.assertFalse(hasattr(p, "validation"))
        self.assertFalse(hasattr(p, "confidence"))


class RealProviderWithFakeClientTests(unittest.TestCase):
    def _dep_json(self, v, line):
        return json.dumps({"proposals": [
            {"type": "PRECEDES", "source": "A-01", "target": "A-02", "reasoning": "supported",
             "citations": [{"doc_id": v.doc_id, "version_no": v.version_no,
                            "line_start": line, "line_end": line,
                            "quote": "Commissioning shall commence once all HV equipment"}],
             "validation": "CONFIRMED"}]})   # model tries to confirm; backend must ignore

    def test_end_to_end_dependency_stays_unvalidated_with_trace(self):
        store, v = tiny_store()
        line = line_with(v, "Commissioning shall commence")
        prov = AnthropicProvider(client=FakeClient(self._dep_json(v, line)))
        props = prov.propose_dependencies(store)
        inv = store.ai_invocations[-1]
        self.assertEqual(inv.provider, "anthropic")
        self.assertEqual(inv.model, "claude-opus-5-5")
        self.assertEqual(inv.prompt_template, "dependency_inference")
        self.assertEqual((inv.input_tokens, inv.output_tokens), (1200, 340))
        self.assertAlmostEqual(inv.cost_usd, 1200 / 1e6 * 4 + 340 / 1e6 * 20, places=6)
        self.assertIsNotNone(inv.latency_ms)
        acc, rej = apply_proposals(store, props, prov.name, invocation=inv)
        self.assertEqual(len(acc), 1)
        self.assertEqual(acc[0].validation, Validation.UNVALIDATED)      # not CONFIRMED
        self.assertEqual(acc[0].confidence, RelConfidence.INFERRED)
        self.assertEqual(acc[0].provenance, [Provenance.AI_INFERRED])

    def test_fabricated_evidence_is_rejected(self):
        store, v = tiny_store()
        bad = json.dumps({"proposals": [
            {"type": "PRECEDES", "source": "A-01", "target": "A-02", "reasoning": "made up",
             "citations": [{"doc_id": v.doc_id, "version_no": v.version_no, "line_start": 1,
                            "line_end": 1, "quote": "this text does not exist anywhere"}]}]})
        prov = AnthropicProvider(client=FakeClient(bad))
        acc, rej = apply_proposals(store, prov.propose_dependencies(store), prov.name)
        self.assertEqual(len(acc), 0)
        self.assertEqual(rej[0][1], "citation could not be verified")

    def test_malformed_model_output_raises_and_is_traced(self):
        store, _ = tiny_store()
        prov = AnthropicProvider(client=FakeClient("this is not json"))
        with self.assertRaises(ProviderError):
            prov.propose_dependencies(store)
        self.assertTrue(store.ai_invocations[-1].error)             # error traced, no secrets

    def test_refusal_raises(self):
        store, _ = tiny_store()
        prov = AnthropicProvider(client=FakeClient("{}", stop_reason="refusal"))
        with self.assertRaises(ProviderError):
            prov.propose_dependencies(store)

    def test_sdk_exception_becomes_provider_error(self):
        store, _ = tiny_store()
        prov = AnthropicProvider(client=FakeClient("", exc=RuntimeError("boom")))
        with self.assertRaises(ProviderError):
            prov.propose_dependencies(store)


class TrustBoundaryTests(unittest.TestCase):
    def test_level3_reasoning_rejected_for_every_proposal_type(self):
        store, v = tiny_store()
        line = line_with(v, "Commissioning shall commence")
        cit = Citation(v.doc_id, v.version_no, line, line,
                       "Commissioning shall commence once all HV equipment")
        dep = DependencyProposal(DepType.PRECEDES, "A-01", "A-02",
                                 "Energization will be delayed", [cit])
        acc, rej = apply_proposals(store, [dep], "t")
        self.assertEqual(len(acc), 0)
        self.assertEqual(rej[0][1], "level-3 wording in reasoning")

        el = EntityLinkProposal("Main unit", "A-01", "the plant is non-compliant", cit)
        acc, rej = apply_entity_links(store, [el], "t")
        self.assertEqual((len(acc), rej[0][1]), (0, "level-3 wording in reasoning"))

    def test_entity_link_recorded_as_unvalidated_alias(self):
        store, v = tiny_store()
        line = line_with(v, "Main unit")
        el = EntityLinkProposal("Main unit", "A-01", "refers to the main unit activity",
                                Citation(v.doc_id, v.version_no, line, line, "The Main unit"))
        acc, rej = apply_entity_links(store, [el], "t")
        self.assertEqual((len(acc), len(rej)), (1, 0))
        alias = [a for a in store.aliases if a.alias == "Main unit"][0]
        self.assertEqual((alias.entity_id, alias.validation), ("A-01", Validation.UNVALIDATED))

    def test_entity_link_refuses_to_merge_two_entities(self):
        store, v = tiny_store()
        # propose that canonical entity "A-02" is actually "A-01" — a merge; must be refused
        el = EntityLinkProposal("A-02", "A-01", "same thing", None)
        acc, rej = apply_entity_links(store, [el], "t")
        self.assertEqual(len(acc), 0)
        self.assertEqual(rej[0][1], "refusing to merge two canonical entities")

    def test_entity_link_unverifiable_citation_rejected(self):
        store, v = tiny_store()
        el = EntityLinkProposal("Main unit", "A-01", "ok",
                                Citation(v.doc_id, v.version_no, 1, 1, "not present here"))
        acc, rej = apply_entity_links(store, [el], "t")
        self.assertEqual((len(acc), rej[0][1]), (0, "citation could not be verified"))

    def test_entity_link_unknown_entity_rejected(self):
        store, v = tiny_store()
        el = EntityLinkProposal("Main unit", "NOPE", "ok", None)
        acc, rej = apply_entity_links(store, [el], "t")
        self.assertEqual((len(acc), rej[0][1]), (0, "unknown entity"))

    def test_change_link_needs_deterministic_corroboration(self):
        # no changes detected in the tiny store → any change link is rejected, none fabricated
        store, _ = tiny_store()
        cl = ChangeLinkProposal("A-01", "delivery_date", ["CL-0001", "CL-0002"], "same claim")
        acc, rej = apply_change_links(store, [cl], "t")
        self.assertEqual(len(acc), 0)
        self.assertEqual(len(store.changes), 0)                     # backend owns change creation


class PromptVersioningTests(unittest.TestCase):
    def test_templates_exist_and_are_versioned(self):
        for name in ("entity_resolution", "change_interpretation", "dependency_inference"):
            text, version = prompts.get_prompt(name)
            self.assertTrue(text.strip())
            self.assertEqual(version, "v1")

    def test_missing_template_raises(self):
        with self.assertRaises(KeyError):
            prompts.get_prompt("no_such_template")


if __name__ == "__main__":
    unittest.main()
