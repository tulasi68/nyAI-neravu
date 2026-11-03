"""Tests for the AI–People's Court synthetic workflow state machine.

These tests validate workflow guards and safety attestations, not legal accuracy.
Run: python -m unittest discover -s tests -v
"""
import unittest

from app.peoples_court import (
    CaseCreate, CaseCategory, DraftPackage, DraftSubmission,
    PanelReviewCreate, ReviewVerdict, ObjectionCreate, ObjectionSeverity,
    ObjectionResponse, JudicialDetermination, InMemoryCaseStore,
)


def case_request(**overrides):
    data = dict(
        case_number="DEMO-1", title="Fictional A v B", category=CaseCategory.CIVIL,
        jurisdiction_note="Synthetic jurisdiction note", party_a_label="Fictional A",
        party_b_label="Fictional B", issue_summary="Fictional dispute only",
        evidence=[], synthetic_data_attestation=True,
    )
    data.update(overrides)
    return CaseCreate(**data)


def draft_request():
    return DraftSubmission(
        submitted_by_role="demo_operator",
        package=DraftPackage(
            draft_text="DRAFT ONLY — NOT A JUDICIAL DECISION. Synthetic draft.",
            issues_considered=["Synthetic issue"], authorities=[],
            limitations=["No real law or case data used"],
            source_coverage_note="Synthetic sample only; source verification not performed.",
            human_review_required=True,
        ),
    )


class PeoplesCourtWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.store = InMemoryCaseStore()
        self.case = self.store.create(case_request())

    def test_requires_synthetic_attestation(self):
        with self.assertRaises(ValueError):
            case_request(synthetic_data_attestation=False)

    def test_draft_enters_panel_review_and_cannot_skip_human_review(self):
        case = self.store.submit_draft(self.case.id, draft_request())
        self.assertEqual(case.status.value, "panel_review")
        bad = draft_request()
        bad.package.human_review_required = False
        with self.assertRaises(ValueError):
            self.store.submit_draft(self.case.id, bad)

    def test_duplicate_reviewer_is_rejected(self):
        self.store.submit_draft(self.case.id, draft_request())
        review = PanelReviewCreate(
            reviewer_id="reviewer-1", verdict=ReviewVerdict.AGREE,
            fairness_check=True, contrary_evidence_check=True,
            source_traceability_check=True, comments="Reviewed fictional record.",
        )
        self.store.review(self.case.id, review)
        with self.assertRaises(ValueError):
            self.store.review(self.case.id, review)

    def test_objection_routes_case_to_judicial_review_when_material(self):
        self.store.submit_draft(self.case.id, draft_request())
        obj_case = self.store.object(self.case.id, ObjectionCreate(
            reviewer_id="reviewer-1", issue="Missing fictional reply",
            explanation="The supplied draft does not discuss the reply.",
            severity=ObjectionSeverity.MATERIAL, affected_references=["Ex.D1"],
        ))
        self.assertEqual(obj_case.status.value, "objections_pending")
        obj_id = obj_case.objections[0]["objection_id"]
        after = self.store.respond(self.case.id, obj_id, ObjectionResponse(
            response="Cannot verify from current synthetic record.",
            disposition="unresolved", unresolved=True,
        ), "demo_ai_advisory")
        self.assertEqual(after.status.value, "judicial_review")

    def test_cannot_record_determination_before_judicial_review(self):
        with self.assertRaises(ValueError):
            self.store.determine(self.case.id, JudicialDetermination(
                judicial_officer_id="officer-1", outcome_reference="DEMO-ORDER-1",
                reasons="A sufficiently long fictional reason for this test.",
                reviewed_original_record=True, considered_panel_dissent=True,
                confirms_independent_judgment=True,
            ))

    def test_determination_requires_independent_review_attestations(self):
        self.store.submit_draft(self.case.id, draft_request())
        self.store.review(self.case.id, PanelReviewCreate(
            reviewer_id="reviewer-1", verdict=ReviewVerdict.OBJECT,
            fairness_check=False, contrary_evidence_check=True,
            source_traceability_check=True, comments="Synthetic concern.",
        ))
        self.store.request_judicial_review(self.case.id, "demo_operator")
        with self.assertRaises(ValueError):
            self.store.determine(self.case.id, JudicialDetermination(
                judicial_officer_id="officer-1", outcome_reference="DEMO-ORDER-1",
                reasons="A sufficiently long fictional reason for this test.",
                reviewed_original_record=True, considered_panel_dissent=False,
                confirms_independent_judgment=True,
            ))

    def test_audit_events_are_recorded(self):
        case = self.store.get(self.case.id)
        self.assertTrue(case.audit)
        self.assertEqual(case.audit[0].event_type, "case_created")
        self.assertIn("SYNTHETIC DEMO ONLY", " ".join(case.warnings))


if __name__ == "__main__":
    unittest.main()
