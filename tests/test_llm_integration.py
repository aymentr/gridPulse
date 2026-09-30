"""Integration: Scenario A and B end-to-end through the provider abstraction (milestone §11, K/L).

Runs with the offline MockProvider (K), with a NullProvider to prove the AI seam is real, and with
the real AnthropicProvider class driven by a fake client to prove the pipeline wiring works with a
real provider without a key (L; the model itself is not exercised — no credentials here)."""
import json
import unittest
from pathlib import Path

from gridpulse.cli import STANDARD_A
from gridpulse.model import FindingKind, RelConfidence, Validation
from gridpulse.pipeline import run
from gridpulse.providers import MockProvider
from gridpulse.providers.base import LLMProvider
from gridpulse import safety
from test_scenarios import all_text, forbidden_conclusions
from test_providers import FakeClient
from gridpulse.providers import AnthropicProvider

ROOT = Path(__file__).resolve().parents[1]
SCN_A = ROOT / "validation" / "scenario-a-transformer"
SCN_B = ROOT / "validation" / "scenario-b-pcs"


class NullProvider(LLMProvider):
    """A provider that proposes nothing — isolates the deterministic layer from the AI layer."""
    name = "null"
    model = ""

    def propose_entity_links(self, store):
        return []

    def interpret_change_links(self, store):
        return []

    def propose_dependencies(self, store):
        return []


def inferred(store):
    return {(d.source, d.target) for d in store.dependencies.values()
            if d.confidence == RelConfidence.INFERRED}


class MockProviderIntegrationTests(unittest.TestCase):
    def test_scenario_a_end_to_end(self):
        r = run(SCN_A, folders=STANDARD_A, provider=MockProvider())
        self.assertEqual(r.provider, "mock-stand-in-v0")
        self.assertIn(("A1010", "A1100"), inferred(r.store))            # inferred dependency
        self.assertTrue(any(f.kind == FindingKind.CHANGE and f.subject == "TX-01"
                            for f in r.store.findings.values()))
        self.assertTrue(any(f.kind == FindingKind.CONFLICT for f in r.store.findings.values()))
        self.assertEqual(len(r.store.ai_invocations), 3)
        self.assertEqual(safety.violations(all_text(r)), [])            # no forbidden output
        for bullet in forbidden_conclusions(SCN_A):
            head = bullet.split("(")[0].strip().lower()
            self.assertNotIn(head, all_text(r).lower())

    def test_scenario_b_end_to_end(self):
        r = run(SCN_B, provider=MockProvider())
        self.assertIn(("PCS-01…PCS-28", "R-12"), inferred(r.store))
        d = next(d for d in r.store.dependencies.values()
                 if d.source == "PCS-01…PCS-28" and d.target == "R-12")
        self.assertEqual((d.confidence, d.validation),
                         (RelConfidence.INFERRED, Validation.UNVALIDATED))
        self.assertEqual(len(r.store.ai_invocations), 3)
        self.assertEqual(safety.violations(all_text(r)), [])


class SeamIsRealTests(unittest.TestCase):
    def test_null_provider_removes_ai_layer_but_keeps_deterministic(self):
        r = run(SCN_A, folders=STANDARD_A, provider=NullProvider())
        # no inferred dependencies without the AI layer …
        self.assertEqual(inferred(r.store), set())
        # … but deterministic change + conflict detection is untouched
        self.assertTrue(any(f.kind == FindingKind.CHANGE for f in r.store.findings.values()))
        self.assertTrue(any(f.kind == FindingKind.CONFLICT for f in r.store.findings.values()))
        # explicit schedule dependencies still exist
        self.assertTrue(any(d.confidence == RelConfidence.EXPLICIT
                            for d in r.store.dependencies.values()))

    def test_mock_vs_null_differ_only_in_ai_proposals(self):
        mock = run(SCN_B, provider=MockProvider())
        null = run(SCN_B, provider=NullProvider())
        self.assertGreater(len(inferred(mock.store)), 0)
        self.assertEqual(inferred(null.store), set())
        self.assertEqual(len(mock.store.changes), len(null.store.changes))   # deterministic parity


class RealProviderWiringTests(unittest.TestCase):
    def test_pipeline_runs_with_anthropic_provider_via_fake_client(self):
        empty = json.dumps({"proposals": []})
        prov = AnthropicProvider(client=FakeClient(empty))
        r = run(SCN_A, folders=STANDARD_A, provider=prov)
        self.assertEqual(r.provider, "anthropic")
        self.assertEqual(len(r.store.ai_invocations), 3)
        self.assertTrue(all(i.provider == "anthropic" and i.model == "claude-opus-5-5"
                            for i in r.store.ai_invocations))
        # deterministic layer still produced the change and conflict
        self.assertTrue(any(f.kind == FindingKind.CHANGE for f in r.store.findings.values()))
        self.assertEqual(safety.violations(all_text(r)), [])


if __name__ == "__main__":
    unittest.main()
