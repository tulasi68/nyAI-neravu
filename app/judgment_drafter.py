"""Structured judicial draft composer; this module never determines case outcomes."""
from typing import List, Optional
from pydantic import BaseModel, Field

class EvidenceItem(BaseModel):
    reference: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1, max_length=2000)
    record_excerpt: Optional[str] = Field(None, max_length=5000)

class Submission(BaseModel):
    party: str = Field(..., min_length=1, max_length=120)
    text: str = Field(..., min_length=1, max_length=8000)

class Issue(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    applicable_law: Optional[str] = Field(None, max_length=4000)
    analysis: Optional[str] = Field(None, max_length=8000)
    record_references: List[str] = Field(default_factory=list, max_length=30)

class JudgmentRequest(BaseModel):
    court_name: Optional[str] = None
    case_number: Optional[str] = None
    case_title: Optional[str] = None
    judge_name: Optional[str] = None
    judgment_date: Optional[str] = None
    case_type: str = "Section 138 Negotiable Instruments Act"
    complainant: Optional[str] = None
    accused: Optional[str] = None
    procedural_history: Optional[str] = None
    complainant_case: Optional[str] = None
    defence_case: Optional[str] = None
    issues: List[Issue] = Field(default_factory=list, max_length=20)
    evidence: List[EvidenceItem] = Field(default_factory=list, max_length=100)
    submissions: List[Submission] = Field(default_factory=list, max_length=30)
    verified_legal_authorities: List[str] = Field(default_factory=list, max_length=50)
    proposed_disposition: Optional[str] = None
    proposed_order: Optional[str] = None

def _v(value, placeholder):
    return value.strip() if value and value.strip() else placeholder

def build_draft(req: JudgmentRequest) -> dict:
    missing = []
    for value, label in [
        (req.court_name, "Court name"), (req.case_number, "Case number"),
        (req.case_title, "Case title"), (req.procedural_history, "Procedural history"),
        (req.complainant_case, "Complainant's case"), (req.defence_case, "Defence case"),
        (req.issues, "Points for determination"), (req.evidence, "Evidence"),
        (req.submissions, "Party submissions"), (req.verified_legal_authorities, "Verified authorities"),
        (req.proposed_disposition, "Disposition for judicial determination")]:
        if not value or (isinstance(value, str) and not value.strip()):
            missing.append(label)
    lines = [
        "DRAFT JUDGMENT — NOT A JUDICIAL DECISION",
        "For review and independent determination by the authorised judicial officer", "",
        _v(req.court_name, "[COURT NAME]"), "Case No.: " + _v(req.case_number, "[CASE NUMBER]"),
        _v(req.case_title, "[CASE TITLE AND PARTIES]"), "Case type: " + req.case_type, "",
        "JUDGMENT (DRAFT)", "Date: " + _v(req.judgment_date, "[DATE]"),
        "Presiding officer: " + _v(req.judge_name, "[TO BE COMPLETED]"), "",
        "1. INTRODUCTION", "Verify all particulars against the original court record.", "",
        "2. PARTIES", "Complainant/Petitioner: " + _v(req.complainant, "[TO BE COMPLETED]"),
        "Accused/Respondent: " + _v(req.accused, "[TO BE COMPLETED]"), "",
        "3. PROCEDURAL HISTORY", _v(req.procedural_history, "[NOT SUPPLIED: complete from the record.]"), "",
        "4. COMPLAINANT'S/PETITIONER'S CASE", _v(req.complainant_case, "[NOT SUPPLIED: complete from the record.]"), "",
        "5. ACCUSED'S/RESPONDENT'S CASE", _v(req.defence_case, "[NOT SUPPLIED: state the defence fairly.]"), "",
        "6. EVIDENCE ON RECORD"]
    if req.evidence:
        for i, e in enumerate(req.evidence, 1):
            lines.append(f"6.{i}. {e.reference}: {e.description}")
            if e.record_excerpt:
                lines.append("Record excerpt supplied: " + e.record_excerpt)
    else:
        lines.append("[Evidence not supplied; do not infer exhibits or witnesses.]")
    lines.extend(["", "7. SUBMISSIONS OF THE PARTIES"])
    lines.extend([f"7.{i}. {s.party}: {s.text}" for i, s in enumerate(req.submissions, 1)] or ["[Submissions not supplied.]"])
    lines.extend(["", "8. POINTS FOR DETERMINATION"])
    lines.extend([f"Point No. {i}: {x.question}" for i, x in enumerate(req.issues, 1)] or ["[Points for determination must be framed from the record and law.]"])
    lines.extend(["", "9. APPLICABLE LAW AND VERIFIED AUTHORITIES"])
    lines.extend([f"9.{i}. {a}" for i, a in enumerate(req.verified_legal_authorities, 1)] or ["[No authorities supplied. This tool does not conduct live legal research.]"])
    lines.extend(["", "10. DISCUSSION, ANALYSIS AND FINDINGS"])
    for i, x in enumerate(req.issues, 1):
        lines.extend(["", f"10.{i}. Point No. {i}: {x.question}",
            "Applicable law: " + _v(x.applicable_law, "[LEGAL TEST NOT SUPPLIED — VERIFY]"),
            "Record references: " + (", ".join(x.record_references) or "[NONE LINKED]"),
            "Analysis supplied for review: " + _v(x.analysis, "[ANALYSIS NOT SUPPLIED. Assess supporting and contrary evidence; do not infer a finding.]"),
            "Judicial review required: verify evidence, burden of proof, law and reasoning independently."])
    lines.extend(["", "11. CONCLUSION", _v(req.proposed_disposition, "[NO DISPOSITION SUPPLIED; the court must decide independently.]"),
        "", "12. PROPOSED OPERATIVE ORDER — FOR JUDICIAL DETERMINATION",
        _v(req.proposed_order, "[Insert only directions supported by findings independently reached by the court.]"),
        "", "13. PRE-ISSUE VERIFICATION",
        "Verify the complete record, names, dates, evidence, authorities, calculations, procedure, findings and legal basis for every direction.",
        "", "____________________________", "Signature/designation of authorised judicial officer — court completion only",
        "", "END OF DRAFT — NOT APPROVED, SIGNED OR ISSUED BY A COURT"])
    return {"status": "draft_for_human_review", "draft_label": "DRAFT ONLY — NOT A JUDICIAL DECISION",
        "title": "Draft judgment — " + _v(req.case_number, "case number to be added"),
        "draft": "\n".join(lines), "missing_information": missing,
        "safeguards": ["This is a drafting aid, not an autonomous judgment or outcome prediction.",
        "Missing facts and authorities are not inferred.", "Verify all law and citations against authoritative sources.",
        "A judge or authorised legal reviewer must independently assess the draft.",
        "Use only anonymised or appropriately authorised case data."]}
