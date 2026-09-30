import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from gridpulse.evidence import cite, reverify
from gridpulse.ingest import BenchmarkIsolationError, ingest_file
from gridpulse.model import EvidenceConfidence, Location
from gridpulse.store import Store

DOC_V1 = """# Test Spec

| | |
|---|---|
| Document no. | KMB-TEST-001 Rev 1 |
| Date | 1 March 2026 |

5.3 **Capability.** Range 0 % to 100 %.
"""
DOC_V2 = DOC_V1.replace("Rev 1", "Rev 2").replace("1 March", "1 June").replace("0 % to", "20 % to")


class DocumentVersionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.store = Store()

    def _write(self, name, text):
        p = self.tmp / name
        p.write_text(text)
        return p

    def test_new_version_preserved_and_old_accessible(self):
        v1 = ingest_file(self.store, self._write("a.md", DOC_V1))
        v2 = ingest_file(self.store, self._write("b.md", DOC_V2))
        self.assertEqual(v1.doc_id, "KMB-TEST-001")
        self.assertEqual([v.version_no for v in self.store.versions["KMB-TEST-001"]], [1, 2])
        self.assertEqual(self.store.latest_version("KMB-TEST-001").revision_label, "Rev 2")
        self.assertIn("0 % to 100 %", "\n".join(self.store.version("KMB-TEST-001", 1).lines))
        self.assertIs(v2, self.store.version("KMB-TEST-001", 2))

    def test_reingest_same_content_is_idempotent(self):
        p = self._write("a.md", DOC_V1)
        ingest_file(self.store, p)
        ingest_file(self.store, p)
        self.assertEqual(len(self.store.versions["KMB-TEST-001"]), 1)

    def test_version_is_immutable(self):
        v1 = ingest_file(self.store, self._write("a.md", DOC_V1))
        with self.assertRaises(FrozenInstanceError):
            v1.lines = ("tampered",)

    def test_ground_truth_is_refused(self):
        gt = self.tmp / "ground-truth"
        gt.mkdir()
        with self.assertRaises(BenchmarkIsolationError):
            ingest_file(self.store, self._write("ground-truth/GROUND_TRUTH.md", "x"))
        with self.assertRaises(BenchmarkIsolationError):
            ingest_file(self.store, self._write("investigation-bundle.md", "x"))


class CitationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.store = Store()
        p = self.tmp / "a.md"
        p.write_text(DOC_V1)
        self.v = ingest_file(self.store, p)

    def test_valid_citation_accepted(self):
        ev = cite(self.store, Location("KMB-TEST-001", 1, 8, 8), "Range 0 % to 100 %")
        self.assertTrue(ev.verified)
        self.assertEqual(ev.confidence, EvidenceConfidence.HIGH)

    def test_citation_with_wrong_quote_is_downgraded(self):
        ev = cite(self.store, Location("KMB-TEST-001", 1, 8, 8), "Range 20 % to 100 %")
        self.assertFalse(ev.verified)
        self.assertEqual(ev.confidence, EvidenceConfidence.LOW)

    def test_citation_to_missing_location_is_downgraded(self):
        self.assertFalse(cite(self.store, Location("KMB-TEST-001", 1, 99, 99), "Range").verified)
        self.assertFalse(cite(self.store, Location("KMB-TEST-001", 7, 8, 8), "Range").verified)
        self.assertFalse(cite(self.store, Location("NO-SUCH-DOC", 1, 1, 1), "Range").verified)

    def test_reverify_is_deterministic(self):
        ev = cite(self.store, Location("KMB-TEST-001", 1, 8, 8), "Capability")
        self.assertTrue(reverify(self.store, ev.id))


if __name__ == "__main__":
    unittest.main()
