"""Tests for conservative synthetic case-record traceability analysis."""
import unittest

from app.case_analysis import AnalysisRequest, RecordSource, RecordClaim, PartyPosition, analyze_record


class CaseAnalysisTests(unittest.TestCase):
    def request(self, **overrides):
        data = dict(
            synthetic_data_attestation=True,
            case_number="DEMO-TRACE-1",
            case_category="civil",
            issues=["Whether the agreement was signed"],
            sources=[
                RecordSource(reference="Ex.P1", description="Fictional agreement",
                             text="Both parties signed the written agreement."),
                RecordSource(reference="Ex.D1", description="Fictional reply",
                             text="The respondent denies signing the agreement."),
            ],
            party_positions=[
                PartyPosition(party_label="Claimant A", position="Agreement signed", references=["Ex.P1"]),
                PartyPosition(party_label="Respondent B", position="Signature denied", references=["Ex.D1"]),
            ],
            claims=[
                RecordClaim(claim_id="C1", side="Claimant A",
                            claim_text="Both parties signed the agreement", cited_references=["Ex.P1"]),
                RecordClaim(claim_id="C2", side="Respondent B",
                            claim_text="Respondent did not sign", cited_references=["MISSING"]),
            ],
        )
        data.update(overrides)
        return AnalysisRequest(**data)

    def test_report_is_non_outcome_and_human_review_only(self):
        report = analyze_record(self.request())
        self.assertTrue(report["synthetic_only"])
        self.assertTrue(report["no_outcome_predicted"])
        self.assertTrue(report["human_review_required"])
        self.assertEqual(report["status"], "source_traceability_report_for_human_review")

    def test_unknown_citation_is_flagged(self):
        report = analyze_record(self.request())
        row = next(c for c in report["claim_traceability"] if c["claim_id"] == "C2")
        self.assertEqual(row["unknown_references"], ["MISSING"])
        self.assertEqual(report["completeness_flags"]["claims_with_unknown_references"][0]["claim_id"], "C2")

    def test_issue_map_is_candidate_only(self):
        report = analyze_record(self.request())
        self.assertTrue(report["issue_source_map"][0]["source_found"])
        self.assertIn("does not establish evidentiary support", report["issue_source_map"][0]["candidate_sources"][0]["review_note"])

    def test_rejects_non_synthetic_record(self):
        with self.assertRaises(ValueError):
            self.request(synthetic_data_attestation=False)

    def test_duplicate_source_reference_rejected(self):
        with self.assertRaises(ValueError):
            self.request(sources=[
                RecordSource(reference="X", description="one", text="fictional one"),
                RecordSource(reference="X", description="two", text="fictional two"),
            ])

    def test_claim_without_citation_is_flagged(self):
        req = self.request(claims=[RecordClaim(claim_id="C3", side="Neutral",
                                               claim_text="A procedural event happened")])
        report = analyze_record(req)
        self.assertEqual(report["completeness_flags"]["claims_without_citations"], ["C3"])


if __name__ == "__main__":
    unittest.main()
