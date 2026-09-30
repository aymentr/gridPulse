"""Component tests: entities, change/conflict detection, dependencies, graph, calculations,
inference boundary, review queue, safety guard. Uses the frozen scenario source documents only
(never ground truth)."""
import unittest
from datetime import date
from pathlib import Path

from gridpulse.cli import STANDARD_A
from gridpulse.entities import normalize_tag, resolve
from gridpulse.graph import traverse
from gridpulse.inference import Citation, DependencyProposal, apply_proposals
from gridpulse.model import (DepType, FindingKind, FindingStatus, Provenance, RelConfidence,
                             Validation)
from gridpulse.pipeline import run
from gridpulse.review import ReviewError, ReviewQueue
from gridpulse import safety

ROOT = Path(__file__).resolve().parents[1]
SCN_A = ROOT / "validation" / "scenario-a-transformer"
SCN_B = ROOT / "validation" / "scenario-b-pcs"


def run_a():
    return run(SCN_A, folders=STANDARD_A)


def dep(store, source, target, type_=DepType.PRECEDES):
    found = [d for d in store.dependencies.values()
             if d.source == source and d.target == target and d.type == type_]
    return found[0] if found else None


class EntityResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = run_a().store

    def test_tx01_aliases_resolve(self):
        for text in ("TX-01", "Main transformer (T1)", "Main power transformer",
                     "132/33 kV main power transformer, 120 MVA ONAN/ONAF, with OLTC"):
            self.assertEqual(resolve(self.s, text)[0], "TX-01", text)

    def test_aux_transformer_not_merged(self):
        self.assertEqual(resolve(self.s, "Auxiliary transformer")[0], "AUX-TX-02")
        self.assertNotIn("TX-01", {a.entity_id for a in self.s.aliases
                                   if "auxiliary" in a.alias.lower()})
        self.assertNotIn("AUX-TX-02", {a.entity_id for a in self.s.aliases
                                       if a.alias == "Main transformer (T1)"})

    def test_ambiguous_generic_name_not_resolved(self):
        self.assertIsNone(resolve(self.s, "transformer"))

    def test_aux_delivery_not_attached_to_tx01(self):
        tx = self.s.claims_for("TX-01", "delivery_date")
        aux = self.s.claims_for("AUX-TX-02", "delivery_date")
        self.assertTrue(tx and aux)
        self.assertTrue(all(c.value.value == date(2027, 1, 12) for c in aux))
        self.assertIn(date(2027, 2, 2), {c.value.value for c in tx})

    def test_tag_range_normalisation(self):
        self.assertEqual(normalize_tag("PCS-01 … PCS-28"), "PCS-01…PCS-28")
        self.assertEqual(normalize_tag("PCS-01…28"), "PCS-01…PCS-28")


class ChangeAndConflictTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = run_a().store

    def test_delivery_change_detected(self):
        chs = [c for c in self.s.changes.values()
               if c.subject == "TX-01" and c.attribute == "delivery_date"]
        self.assertEqual(len(chs), 1)
        old, new = self.s.claims[chs[0].old_claim], self.s.claims[chs[0].new_claim]
        self.assertEqual((old.value.value, new.value.value), (date(2027, 1, 12), date(2027, 2, 2)))
        self.assertEqual(self.s.claim_version(new).doc_id, "KMB-EPC-PR-0012")

    def test_no_change_for_unchanged_aux_transformer(self):
        self.assertFalse([c for c in self.s.changes.values() if c.subject == "AUX-TX-02"])

    def test_schedule_vs_report_conflict_detected(self):
        cfs = [c for c in self.s.conflicts.values()
               if c.subject == "TX-01" and c.attribute == "delivery_date"]
        self.assertEqual(len(cfs), 1)
        docs = {self.s.claim_version(self.s.claims[i]).doc_id: self.s.claims[i].value.value
                for i in cfs[0].claim_ids}
        self.assertEqual(docs, {"KMB-EPC-SCH-U12": date(2027, 1, 12),
                                "KMB-EPC-PR-0012": date(2027, 2, 2)})
        self.assertTrue(any(f.kind == FindingKind.CONFLICT for f in self.s.findings.values()))

    def test_every_claim_has_verified_evidence(self):
        for c in self.s.claims.values():
            self.assertTrue(c.evidence_ids, c.id)
            self.assertTrue(all(self.s.evidence[e].verified for e in c.evidence_ids), c.id)
            self.assertEqual(c.validation, Validation.UNVALIDATED)


class DependencyTests(unittest.TestCase):
    def test_explicit_schedule_dependency(self):
        s = run_a().store
        d = dep(s, "A1000", "A1010")
        self.assertIsNotNone(d)
        self.assertEqual((d.confidence, d.validation), (RelConfidence.EXPLICIT,
                                                        Validation.UNVALIDATED))
        self.assertEqual(d.provenance, [Provenance.SCHEDULE_DERIVED])

    def test_schedule_has_no_stated_install_to_hv_link(self):
        s = run(SCN_A, folders=STANDARD_A, proposer=_NoProposals()).store
        self.assertIsNone(dep(s, "A1010", "A1100"))

    def test_inferred_dependency_stays_unvalidated(self):
        s = run_a().store
        d = dep(s, "A1010", "A1100")
        self.assertEqual((d.confidence, d.validation), (RelConfidence.INFERRED,
                                                        Validation.UNVALIDATED))
        self.assertEqual(d.provenance, [Provenance.AI_INFERRED])
        self.assertTrue(d.proposer and d.reasoning and d.evidence_ids)

    def test_rejected_dependency_not_traversed(self):
        r = run_a()
        s, q = r.store, r.queue
        before = {p.end for p in traverse(s, ["TX-01", "A1000"], "DATE")}
        self.assertIn("A1100", before)
        q.add_reviewer("rev-1", ["Commissioning Engineer"])
        f = next(f for f in s.findings.values() if f.kind == FindingKind.DEPENDENCY
                 and s.dependencies[f.ref_id].target == "A1100")
        q.reject(f.id, "rev-1", "Commissioning Engineer", "test rationale")
        self.assertEqual(s.dependencies[f.ref_id].validation, Validation.REJECTED)
        after = {p.end for p in traverse(s, ["TX-01", "A1000"], "DATE")}
        self.assertIn("A1010", after)
        self.assertNotIn("A1100", after)
        self.assertNotIn("A1300", after)


class _NoProposals:
    name = "none"

    def propose(self, store):
        return []


class CalculationTests(unittest.TestCase):
    def test_3_18_21_day_calculations(self):
        s = run_a().store
        results = {c.result for c in s.calculations.values() if c.unit == "calendar days"}
        self.assertTrue({3, 18, 21} <= results, results)
        for c in s.calculations.values():
            self.assertTrue(all(i["claim_id"] in s.claims for i in c.inputs))

    def test_range_gap_and_points_below(self):
        s = run(SCN_B).store
        ops = {c.operation.split("(")[0]: c.result for c in s.calculations.values()}
        self.assertEqual(ops.get("uncovered_portion"), "0–20 %")
        self.assertEqual(ops.get("points_below_lower_bound"), [0, 10])


class InferenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.s = run(SCN_A, folders=STANDARD_A, proposer=_NoProposals()).store
        v = self.s.latest_version("KMB-EPC-SCH-U12")
        self.v = v
        self.line = next(i for i, l in enumerate(v.lines, 1) if "A1100" in l)

    def _proposal(self, quote, line=None):
        return DependencyProposal(DepType.PRECEDES, "A1010", "A1100", "test",
                                  [Citation(self.v.doc_id, self.v.version_no,
                                            line or self.line, line or self.line, quote)])

    def test_unverifiable_citation_rejected(self):
        acc, rej = apply_proposals(self.s, [self._proposal("text that is not there")], "t")
        self.assertEqual(acc, [])
        self.assertEqual(rej[0][1], "citation could not be verified")
        self.assertIsNone(dep(self.s, "A1010", "A1100"))

    def test_missing_citation_and_unknown_entity_rejected(self):
        p = DependencyProposal(DepType.PRECEDES, "A1010", "A1100", "test", [])
        q = DependencyProposal(DepType.PRECEDES, "A1010", "NOPE-99", "test",
                               self._proposal("A1100").citations)
        _, rej = apply_proposals(self.s, [p, q], "t")
        self.assertEqual([r for _, r in rej], ["no citations", "unknown entity"])

    def test_accepted_proposal_is_inferred_unvalidated(self):
        acc, _ = apply_proposals(self.s, [self._proposal("A1100")], "t")
        self.assertEqual(len(acc), 1)
        d = acc[0]
        self.assertEqual((d.confidence, d.validation), (RelConfidence.INFERRED,
                                                        Validation.UNVALIDATED))


class ReviewQueueTests(unittest.TestCase):
    def setUp(self):
        r = run_a()
        self.s, self.q = r.store, r.queue
        self.q.add_reviewer("pc-1", ["Project Controls"])
        self.q.add_reviewer("ce-1", ["Commissioning Engineer"])
        self.dep_f = next(f for f in self.s.findings.values() if f.kind == FindingKind.DEPENDENCY)
        self.chg_f = next(f for f in self.s.findings.values() if f.kind == FindingKind.CHANGE)

    def test_all_findings_start_under_review(self):
        self.assertTrue(all(f.status == FindingStatus.UNDER_REVIEW
                            for f in self.s.findings.values()))

    def test_only_human_confirmation_confirms_inferred_dependency(self):
        d = self.s.dependencies[self.dep_f.ref_id]
        self.assertEqual(d.validation, Validation.UNVALIDATED)
        self.q.confirm(self.dep_f.id, "ce-1", "Commissioning Engineer", "ok")
        self.assertEqual(d.validation, Validation.CONFIRMED)
        self.assertEqual(d.confidence, RelConfidence.INFERRED)     # origin is preserved
        self.assertIn(Provenance.HUMAN_CONFIRMED, d.provenance)
        self.assertEqual(self.s.reviews[-1].reviewer_id, "ce-1")

    def test_unauthorized_reviewer_refused(self):
        with self.assertRaises(ReviewError):
            self.q.confirm(self.dep_f.id, "pc-1", "Commissioning Engineer")
        with self.assertRaises(ReviewError):
            self.q.confirm(self.dep_f.id, "someone", "Project Controls")
        self.assertEqual(self.s.dependencies[self.dep_f.ref_id].validation,
                         Validation.UNVALIDATED)

    def test_reject_requires_rationale(self):
        with self.assertRaises(ReviewError):
            self.q.reject(self.chg_f.id, "pc-1", "Project Controls", " ")

    def test_request_investigation_and_edit(self):
        self.q.request_investigation(self.chg_f.id, "pc-1", "Project Controls", "Which source?")
        self.assertEqual(self.chg_f.status, FindingStatus.INVESTIGATION_REQUESTED)
        old = self.chg_f.summary
        self.q.edit(self.chg_f.id, "pc-1", "Project Controls", "edited", "clarify")
        self.assertEqual((self.chg_f.summary, self.chg_f.revisions[-1]["summary"]),
                         ("edited", old))

    def test_confirm_change_confirms_new_claim_only(self):
        ch = self.s.changes[self.chg_f.ref_id]
        self.q.confirm(self.chg_f.id, "pc-1", "Project Controls")
        self.assertEqual(self.s.claims[ch.new_claim].validation, Validation.CONFIRMED)
        self.assertEqual(self.s.claims[ch.old_claim].validation, Validation.UNVALIDATED)
        with self.assertRaises(ReviewError):                       # closed findings stay closed
            self.q.reject(self.chg_f.id, "pc-1", "Project Controls", "late")


class SafetyGuardTests(unittest.TestCase):
    def test_level3_wording_rejected(self):
        for text in ("Energization will be delayed.", "HV commissioning will slip",
                     "PCS Rev 8 is non-compliant with R-12", "The PPC must be redesigned",
                     "The network operator must be notified", "The study must be redone",
                     "GC-04 will fail", "Energization is delayed by 21 days",
                     "The plant will not meet R-12"):
            with self.assertRaises(safety.UnsafeConclusionError, msg=text):
                safety.check(text)

    def test_neutral_wording_allowed(self):
        safety.check("Potential impact identified: A1100 (COMMISSIONING CHECKPOINT). "
                     "Expert validation required. 18 calendar days.")


if __name__ == "__main__":
    unittest.main()
