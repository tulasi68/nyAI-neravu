"""Safety and regression tests for the structured judgment draft composer.

Run from the repository root:
    python -m unittest discover -s tests -v

These tests check composition and safety labels, not legal correctness.
"""
import unittest

from app.judgment_drafter import EvidenceItem, Issue, JudgmentRequest, Submission, build_draft


class JudgmentDraftComposerTests(unittest.TestCase):
    def test_empty_request_is_explicitly_a_draft_and_flags_missing_inputs(self):
        result = build_draft(JudgmentRequest())

        self.assertEqual(result["status"], "draft_for_human_review")
        self.assertIn("NOT A JUDICIAL DECISION", result["draft_label"])
        self.assertIn("Court name", result["missing_information"])
        self.assertIn("Verified authorities", result["missing_information"])
        self.assertIn("[NOT SUPPLIED", result["draft"])
        self.assertIn("A judge or authorised legal reviewer", " ".join(result["safeguards"]))

    def test_missing_evidence_is_not_invented(self):
        result = build_draft(JudgmentRequest(case_number="TEST/1"))

        self.assertIn("[Evidence not supplied; do not infer exhibits or witnesses.]", result["draft"])
        self.assertNotIn("Ex.P1:", result["draft"])

    def test_supplied_evidence_reference_and_excerpt_are_preserved(self):
        request = JudgmentRequest(
            case_number="TEST/2",
            evidence=[
                EvidenceItem(
                    reference="Ex.P7",
                    description="Bank return memo",
                    record_excerpt="Return reason transcribed from supplied sample",
                )
            ],
        )

        result = build_draft(request)

        self.assertIn("Ex.P7: Bank return memo", result["draft"])
        self.assertIn("Return reason transcribed from supplied sample", result["draft"])

    def test_issue_analysis_requires_independent_judicial_review(self):
        request = JudgmentRequest(
            issues=[
                Issue(
                    question="Whether the statutory requirements are established?",
                    applicable_law="Reviewer-supplied test, pending independent verification",
                    analysis="Assess both supporting and contrary evidence.",
                    record_references=["Ex.P1", "Ex.D1"],
                )
            ]
        )

        result = build_draft(request)

        self.assertIn("Record references: Ex.P1, Ex.D1", result["draft"])
        self.assertIn("Judicial review required", result["draft"])
        self.assertIn("independent determination", result["draft"].lower())

    def test_party_submissions_are_attributed_to_the_named_party(self):
        request = JudgmentRequest(
            submissions=[Submission(party="Defence", text="Submission from fictional test record")]
        )

        result = build_draft(request)

        self.assertIn("7.1. Defence: Submission from fictional test record", result["draft"])

    def test_empty_disposition_is_not_filled_with_an_outcome(self):
        result = build_draft(JudgmentRequest())

        self.assertIn("[NO DISPOSITION SUPPLIED; the court must decide independently.]", result["draft"])
        self.assertIn("[Insert only directions supported by findings independently reached by the court.]", result["draft"])


if __name__ == "__main__":
    unittest.main()
