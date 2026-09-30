"""End-to-end tests on the frozen benchmark scenarios.

The production pipeline never reads ground truth. These TESTS read only the "Forbidden conclusions"
section of each frozen GROUND_TRUTH.md, to check that no bundle states any of them. Expected
findings are asserted from the scenario source documents, not imported from ground truth.
"""
import re
import unittest
from pathlib import Path

from gridpulse import safety
from gridpulse.cli import STANDARD_A, main
from gridpulse.model import FindingKind, RelConfidence, Validation
from gridpulse.pipeline import run

ROOT = Path(__file__).resolve().parents[1]
SCN_A = ROOT / "validation" / "scenario-a-transformer"
SCN_B = ROOT / "validation" / "scenario-b-pcs"


def forbidden_conclusions(scenario: Path) -> list[str]:
    text = (scenario / "ground-truth" / "GROUND_TRUTH.md").read_text()
    section = text.split("## Forbidden conclusions", 1)[1].split("\n## ", 1)[0]
    return [l[2:].strip() for l in section.splitlines() if l.startswith("- ")]


def bundle_for(result, subject, attribute):
    for b in result.bundles:
        f = result.store.findings[b.finding_id]
        ch = result.store.changes[f.ref_id]
        if ch.subject == subject and ch.attribute == attribute:
            return b
    raise AssertionError(f"no bundle for {subject} {attribute}")


def all_text(result) -> str:
    return "\n".join(b.to_markdown() for b in result.bundles) + "\n" + "\n".join(
        f.summary for f in result.store.findings.values())


class _ForbiddenMixin:
    """Each forbidden conclusion: (a) its literal wording is absent, (b) a scenario-specific
    pattern for it is absent, (c) the whole output passes the safety guard."""
    scenario: Path
    PATTERNS: dict[str, list[str]]

    def check_forbidden(self, result):
        text = all_text(result)
        low = text.lower()
        self.assertEqual(safety.violations(text), [])
        bullets = forbidden_conclusions(self.scenario)
        self.assertEqual(len(bullets), len(self.PATTERNS), "forbidden list changed; update tests")
        for bullet, key in zip(bullets, self.PATTERNS):
            self.assertTrue(bullet.lower().startswith(key.lower()), (bullet, key))
            literal = re.sub(r"\s*\(.*?\)", "", bullet).lower()
            for part in literal.split(" / "):
                self.assertNotIn(part.strip(), low, bullet)
            for pat in self.PATTERNS[key]:
                self.assertIsNone(re.search(pat, text, re.I), (bullet, pat))


class ScenarioATests(_ForbiddenMixin, unittest.TestCase):
    scenario = SCN_A
    PATTERNS = {
        "Energization will be delayed": [r"energi[sz]ation[^.\n]{0,40}\b(will|is|be) (be )?delay",
                                         r"delay(ed)? by \d+"],
        "HV commissioning will slip": [r"commissioning[^.\n]{0,40}\bwill\b[^.\n]{0,20}slip"],
        "The schedule is wrong": [r"\b(schedule|report)\b[^.\n]{0,20}\b(is|was) (wrong|incorrect)"],
        "The EPC's statement": [r"\bmaintained\b[^.\n]{0,30}\b(false|untrue|incorrect)"],
        "Any statement about the EPC's or supplier's intent": [
            r"\b(intend|intention|intentional|deliberate|conceal|hid(e|ing)|mislead)"],
        "The installation → HV commissioning link": [
            r"Explicit relationship: A1010[^\n]*PRECEDES→ A1100",
            r"A1010[^\n]*PRECEDES→ A1100[^\n]*(CONFIRMED|EXPLICIT)"],
    }

    @classmethod
    def setUpClass(cls):
        cls.r = run(SCN_A, folders=STANDARD_A)
        cls.b = bundle_for(cls.r, "TX-01", "delivery_date")

    def test_ingests_sources_only(self):
        paths = [v.source_path for vs in self.r.store.versions.values() for v in vs]
        self.assertTrue(paths)
        for p in paths:
            self.assertNotIn("ground-truth", p)
            self.assertNotIn("investigation-bundle", p)
            self.assertNotIn("changed", Path(p).parts)          # standard run excludes variant

    def test_findings(self):
        kinds = {(f.kind, f.subject) for f in self.r.store.findings.values()}
        self.assertIn((FindingKind.CHANGE, "TX-01"), kinds)
        self.assertIn((FindingKind.CONFLICT, "TX-01"), kinds)
        self.assertFalse([k for k in kinds if k[1] == "AUX-TX-02"])

    def test_bundle_has_d037_sections(self):
        md = self.b.to_markdown()
        for sec in ("VALIDATED INFORMATION", "OBSERVED INFORMATION", "INFERRED RELATIONSHIPS",
                    "DETERMINISTIC CALCULATIONS", "POTENTIAL EXPOSURES",
                    "HUMAN VALIDATION REQUIRED", "EVIDENCE"):
            self.assertIn(f"### {sec}", md)
        self.assertNotRegex(md, r"\b(NOT )?READY\b")

    def test_bundle_content(self):
        md = self.b.to_markdown()
        self.assertIn("12 Jan 2027", md)
        self.assertIn("02 Feb 2027", md)
        self.assertIn("KMB-EPC-SCH-U12", md)
        for n in (3, 18, 21):
            self.assertRegex(md, rf": {n} calendar days")
        self.assertRegex(md, r"A1010[^\n]*PRECEDES→ A1100[^\n]*INFERRED · UNVALIDATED · "
                             r"AI_INFERRED")
        self.assertRegex(md, r"A1000[^\n]*PRECEDES→ A1010[^\n]*EXPLICIT · UNVALIDATED · "
                             r"SCHEDULE_DERIVED")
        ends = {i["entity"]: i for i in self.b.impacts}
        self.assertFalse(ends["A1010"]["inferred"])
        for e in ("A1100", "A1300"):
            self.assertTrue(ends[e]["inferred"] and ends[e]["unvalidated"])
        self.assertEqual(ends["A1300"]["checkpoint"], "ENERGIZATION CHECKPOINT")
        self.assertTrue(all(i["unvalidated"] for i in self.b.impacts))
        self.assertIn("Project Controls", md)

    def test_every_evidence_line_verified(self):
        self.assertTrue(self.b.evidence)
        self.assertFalse([e for e in self.b.evidence if "[UNVERIFIED]" in e])

    def test_nothing_confirmed_without_review(self):
        s = self.r.store
        self.assertFalse([c for c in s.claims.values() if c.validation != Validation.UNVALIDATED])
        self.assertFalse([d for d in s.dependencies.values()
                          if d.validation != Validation.UNVALIDATED])

    def test_forbidden_conclusions_absent(self):
        self.check_forbidden(self.r)

    def test_variant_run_with_supplier_letter(self):
        r = run(SCN_A)
        self.check_forbidden(r)
        self.assertTrue(any(f.kind == FindingKind.CHANGE and f.subject == "TX-01"
                            for f in r.store.findings.values()))


class ScenarioBTests(_ForbiddenMixin, unittest.TestCase):
    scenario = SCN_B
    PATTERNS = {
        "The plant / equipment will fail": [r"\bwill (not )?(fail|pass)\b",
                                            r"fail[^.\n]{0,20}grid compliance"],
        "PCS Rev 8 is non-compliant": [r"non-?compliant", r"\bdoes not (meet|comply)"],
        "The PPC must be redesigned": [r"\bredesign"],
        "The network operator must be notified": [r"\b(must|shall|needs? to) be notified",
                                                  r"R-30[^.\n]{0,30}\b(is|was) triggered"],
        "The protection study must be redone": [r"\bredone\b", r"\bredo\b"],
        "Updated simulation models must be submitted": [
            r"models?[^.\n]{0,30}\b(must|need to) be submitted", r"R-31[^.\n]{0,30}\bapplies"],
        "The PCS → R-12 link": [
            r"Explicit relationship: PCS[^\n]*→ R-12",
            r"PCS-01…PCS-28[^\n]*SPECIFIES→ R-12[^\n]*(CONFIRMED|EXPLICIT)"],
    }

    @classmethod
    def setUpClass(cls):
        cls.r = run(SCN_B)
        cls.b = bundle_for(cls.r, "PCS-01…PCS-28", "clause 5.3")

    def test_clause_changes_detected(self):
        attrs = {c.attribute for c in self.r.store.changes.values()
                 if c.subject == "PCS-01…PCS-28"}
        self.assertTrue({"clause 5.3", "clause 6.1", "clause 9.2"} <= attrs)

    def test_stale_ppc_reference(self):
        stale = [f for f in self.r.store.findings.values()
                 if f.kind == FindingKind.STALE_EVIDENCE]
        self.assertEqual(len(stale), 1)
        d = self.r.store.dependencies[stale[0].ref_id]
        self.assertEqual((d.source, d.target, d.source_attribute, d.meta["cited_revision"]),
                         ("KMB-EPC-SPC-PPC-002", "KMB-EPC-SPC-PCS-001", "clause 5.3", "Rev 7"))

    def test_pcs_to_r12_inferred_unvalidated(self):
        d = [d for d in self.r.store.dependencies.values()
             if d.source == "PCS-01…PCS-28" and d.target == "R-12"]
        self.assertEqual(len(d), 1)
        self.assertEqual((d[0].confidence, d[0].validation),
                         (RelConfidence.INFERRED, Validation.UNVALIDATED))

    def test_bundle_content(self):
        md = self.b.to_markdown()
        self.assertIn("0–20 %", md)
        self.assertIn("[0, 10]", md)
        self.assertIn("different measurement points", md)
        cps = {i["checkpoint"] for i in self.b.impacts}
        self.assertTrue({"GRID COMPLIANCE CHECKPOINT", "ENGINEERING CHECKPOINT"} <= cps)
        r12_paths = [i for i in self.b.impacts if "R-12" in i["path"]]
        self.assertTrue(r12_paths and all(i["inferred"] for i in r12_paths))

    def test_non_consequential_changes_not_routed_as_exposure(self):
        for subject, attr in (("KMB-EPC-SPC-BCN-003", "clause 6.3"),
                              ("PCS-01…PCS-28", "clause 9.2")):
            self.assertEqual(bundle_for(self.r, subject, attr).exposures, [])

    def test_forbidden_conclusions_absent(self):
        self.check_forbidden(self.r)


class IsolationTests(unittest.TestCase):
    def test_production_code_does_not_reference_benchmark_answers(self):
        src = ROOT / "src" / "gridpulse"
        for p in src.glob("*.py"):
            text = p.read_text()
            if p.name == "ingest.py":                  # the refusal list itself
                continue
            for word in ("GROUND_TRUTH", "ground-truth", "investigation-bundle", "scoring",
                         "A-GT", "B-GT"):
                self.assertNotIn(word, text, f"{p.name} mentions {word}")

    def test_cli_runs(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main(["run", str(SCN_A), "--standard-a"]), 0)
        self.assertIn("## Review queue", buf.getvalue())
        self.assertIn("not an AI model", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
