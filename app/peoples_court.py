"""Prototype workflow for AI–People's Court.

This module coordinates a *non-binding research demonstration*. It does not
create judicial authority, decide legal outcomes, or persist real case data.
Production use requires institutional authorisation, durable storage, identity
and access management, privacy/security review, and a legally approved process.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CaseCategory(str, Enum):
    CIVIL = "civil"
    CONSUMER = "consumer"
    FAMILY = "family"
    CRIMINAL = "criminal"
    CONSTITUTIONAL = "constitutional"
    SERVICE = "service"
    MOTOR_ACCIDENT = "motor_accident"
    OTHER = "other"


class WorkflowStatus(str, Enum):
    INTAKE = "intake"
    DRAFT_READY = "draft_ready"
    PANEL_REVIEW = "panel_review"
    OBJECTIONS_PENDING = "objections_pending"
    JUDICIAL_REVIEW = "judicial_review"
    DECIDED = "decided"
    RETURNED_FOR_CORRECTION = "returned_for_correction"


class ReviewVerdict(str, Enum):
    AGREE = "agree"
    OBJECT = "object"
    INSUFFICIENT_RECORD = "insufficient_record"


class ObjectionSeverity(str, Enum):
    MINOR = "minor"
    MATERIAL = "material"
    CRITICAL = "critical"


class EvidenceReference(BaseModel):
    reference: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)
    source_document_id: Optional[str] = Field(None, max_length=200)
    page_or_location: Optional[str] = Field(None, max_length=120)
    authenticated_by_court: bool = False


class CaseCreate(BaseModel):
    case_number: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=300)
    category: CaseCategory
    jurisdiction_note: str = Field(min_length=1, max_length=2000)
    party_a_label: str = Field(min_length=1, max_length=160)
    party_b_label: str = Field(min_length=1, max_length=160)
    issue_summary: str = Field(min_length=1, max_length=5000)
    evidence: List[EvidenceReference] = Field(default_factory=list, max_length=100)
    synthetic_data_attestation: bool = Field(
        description="Must be true: this prototype accepts synthetic records only."
    )

    @model_validator(mode="after")
    def require_synthetic(self):
        if not self.synthetic_data_attestation:
            raise ValueError("Prototype accepts synthetic test records only.")
        if self.party_a_label.strip() == self.party_b_label.strip():
            raise ValueError("The two party labels must be distinct.")
        return self


class DraftPackage(BaseModel):
    draft_text: str = Field(min_length=20, max_length=100000)
    issues_considered: List[str] = Field(default_factory=list, max_length=30)
    authorities: List[str] = Field(default_factory=list, max_length=100)
    limitations: List[str] = Field(default_factory=list, max_length=100)
    source_coverage_note: str = Field(min_length=1, max_length=4000)
    human_review_required: bool = True


class DraftSubmission(BaseModel):
    package: DraftPackage
    submitted_by_role: str = Field(min_length=1, max_length=80)


class PanelReviewCreate(BaseModel):
    reviewer_id: str = Field(min_length=1, max_length=120)
    verdict: ReviewVerdict
    fairness_check: bool
    contrary_evidence_check: bool
    source_traceability_check: bool
    comments: str = Field(min_length=1, max_length=5000)
    referenced_evidence: List[str] = Field(default_factory=list, max_length=100)


class ObjectionCreate(BaseModel):
    reviewer_id: str = Field(min_length=1, max_length=120)
    issue: str = Field(min_length=1, max_length=2000)
    explanation: str = Field(min_length=1, max_length=8000)
    severity: ObjectionSeverity
    affected_references: List[str] = Field(default_factory=list, max_length=100)


class ObjectionResponse(BaseModel):
    response: str = Field(min_length=1, max_length=8000)
    disposition: str = Field(min_length=1, max_length=100)
    unresolved: bool


class JudicialDetermination(BaseModel):
    judicial_officer_id: str = Field(min_length=1, max_length=120)
    outcome_reference: str = Field(
        min_length=1,
        max_length=4000,
        description="Reference to the authorised officer's own determination; not an AI-selected outcome.",
    )
    reasons: str = Field(min_length=20, max_length=20000)
    reviewed_original_record: bool
    considered_panel_dissent: bool
    confirms_independent_judgment: bool


class AuditEvent(BaseModel):
    event_id: str
    at: str
    actor_role: str
    event_type: str
    summary: str


class PeoplesCourtCase(BaseModel):
    id: str
    case_number: str
    title: str
    category: CaseCategory
    jurisdiction_note: str
    party_a_label: str
    party_b_label: str
    issue_summary: str
    evidence: List[EvidenceReference]
    status: WorkflowStatus = WorkflowStatus.INTAKE
    created_at: str
    updated_at: str
    draft: Optional[DraftPackage] = None
    draft_submitted_by: Optional[str] = None
    reviews: List[dict] = Field(default_factory=list)
    objections: List[dict] = Field(default_factory=list)
    objection_responses: Dict[str, dict] = Field(default_factory=dict)
    determination: Optional[dict] = None
    audit: List[AuditEvent] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class InMemoryCaseStore:
    """Single-process synthetic demo store. Not durable or production safe."""

    def __init__(self):
        self._items: Dict[str, PeoplesCourtCase] = {}
        self._lock = RLock()

    def _event(self, case: PeoplesCourtCase, role: str, event: str, summary: str):
        case.audit.append(AuditEvent(
            event_id=str(uuid4()), at=utc_now(), actor_role=role,
            event_type=event, summary=summary[:1000]
        ))
        case.updated_at = utc_now()

    def list(self) -> List[dict]:
        with self._lock:
            return [item.model_dump(mode="json") for item in self._items.values()]

    def get(self, case_id: str) -> PeoplesCourtCase:
        with self._lock:
            if case_id not in self._items:
                raise KeyError(case_id)
            return self._items[case_id].model_copy(deep=True)

    def create(self, req: CaseCreate) -> PeoplesCourtCase:
        with self._lock:
            if any(c.case_number == req.case_number for c in self._items.values()):
                raise ValueError("A case with this demo case number already exists.")
            now = utc_now()
            case = PeoplesCourtCase(
                id=str(uuid4()), case_number=req.case_number, title=req.title,
                category=req.category, jurisdiction_note=req.jurisdiction_note,
                party_a_label=req.party_a_label, party_b_label=req.party_b_label,
                issue_summary=req.issue_summary, evidence=req.evidence,
                created_at=now, updated_at=now,
                warnings=[
                    "SYNTHETIC DEMO ONLY — not an official court record.",
                    "No output from this prototype is a judicial order or legally binding decision.",
                    "AI and citizen-panel outputs are advisory; a legally authorised judicial officer must decide independently.",
                ],
            )
            self._items[case.id] = case
            self._event(case, "case_operator", "case_created", "Synthetic case record created.")
            return case.model_copy(deep=True)

    def submit_draft(self, case_id: str, req: DraftSubmission) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status not in (WorkflowStatus.INTAKE, WorkflowStatus.RETURNED_FOR_CORRECTION):
                raise ValueError("Draft can only be submitted at intake or after correction.")
            if not req.package.human_review_required:
                raise ValueError("Every draft must require independent human review.")
            case.draft = req.package
            case.draft_submitted_by = req.submitted_by_role
            case.reviews = []
            case.objections = []
            case.objection_responses = {}
            case.determination = None
            case.status = WorkflowStatus.PANEL_REVIEW
            self._event(case, req.submitted_by_role, "draft_submitted",
                        "Draft submitted for independent advisory panel review.")
            return case.model_copy(deep=True)

    def review(self, case_id: str, req: PanelReviewCreate) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status != WorkflowStatus.PANEL_REVIEW:
                raise ValueError("Panel reviews are accepted only while panel review is open.")
            if any(r["reviewer_id"] == req.reviewer_id for r in case.reviews):
                raise ValueError("This reviewer has already submitted an independent review.")
            review = req.model_dump(mode="json")
            review["submitted_at"] = utc_now()
            case.reviews.append(review)
            self._event(case, "citizen_reviewer", "panel_review_submitted",
                        f"Advisory review submitted: {req.verdict.value}.")
            if req.verdict != ReviewVerdict.AGREE or not (
                req.fairness_check and req.contrary_evidence_check and req.source_traceability_check
            ):
                case.status = WorkflowStatus.OBJECTIONS_PENDING
            return case.model_copy(deep=True)

    def object(self, case_id: str, req: ObjectionCreate) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status not in (WorkflowStatus.PANEL_REVIEW, WorkflowStatus.OBJECTIONS_PENDING):
                raise ValueError("Objections require an open panel review.")
            if any(o["reviewer_id"] == req.reviewer_id and o["issue"] == req.issue for o in case.objections):
                raise ValueError("This reviewer has already raised this objection.")
            item = req.model_dump(mode="json")
            item["objection_id"] = str(uuid4())
            item["submitted_at"] = utc_now()
            case.objections.append(item)
            case.status = WorkflowStatus.OBJECTIONS_PENDING
            self._event(case, "citizen_reviewer", "objection_raised",
                        f"{req.severity.value} objection raised: {req.issue}")
            return case.model_copy(deep=True)

    def respond(self, case_id: str, objection_id: str, req: ObjectionResponse, actor_role: str) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status not in (WorkflowStatus.OBJECTIONS_PENDING, WorkflowStatus.JUDICIAL_REVIEW):
                raise ValueError("No objection-resolution stage is open.")
            objection = next((o for o in case.objections if o["objection_id"] == objection_id), None)
            if objection is None:
                raise KeyError(objection_id)
            case.objection_responses[objection_id] = {
                **req.model_dump(mode="json"), "responded_at": utc_now(), "actor_role": actor_role
            }
            self._event(case, actor_role, "objection_response_recorded",
                        f"Response recorded for objection {objection_id}; unresolved={req.unresolved}.")
            if req.unresolved or objection["severity"] in ("material", "critical"):
                case.status = WorkflowStatus.JUDICIAL_REVIEW
            return case.model_copy(deep=True)

    def request_judicial_review(self, case_id: str, actor_role: str) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status not in (WorkflowStatus.PANEL_REVIEW, WorkflowStatus.OBJECTIONS_PENDING):
                raise ValueError("Case is not awaiting panel review or objection resolution.")
            if not case.reviews:
                raise ValueError("At least one independent review must be recorded.")
            case.status = WorkflowStatus.JUDICIAL_REVIEW
            self._event(case, actor_role, "judicial_review_requested",
                        "Case referred for independent judicial determination.")
            return case.model_copy(deep=True)

    def determine(self, case_id: str, req: JudicialDetermination) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status != WorkflowStatus.JUDICIAL_REVIEW:
                raise ValueError("Judicial review must be open before a determination is recorded.")
            if not (req.reviewed_original_record and req.considered_panel_dissent and req.confirms_independent_judgment):
                raise ValueError("Judicial officer must attest to original-record review, dissent consideration, and independent judgment.")
            unresolved = [
                oid for oid, response in case.objection_responses.items()
                if response.get("unresolved")
            ]
            case.determination = {
                **req.model_dump(mode="json"),
                "recorded_at": utc_now(),
                "advisory_panel_reviews": len(case.reviews),
                "objections_raised": len(case.objections),
                "unresolved_objection_ids": unresolved,
            }
            case.status = WorkflowStatus.DECIDED
            self._event(case, "judicial_officer", "judicial_determination_recorded",
                        "Human judicial officer recorded an independent determination reference.")
            return case.model_copy(deep=True)

    def return_for_correction(self, case_id: str, actor_role: str, reason: str) -> PeoplesCourtCase:
        with self._lock:
            case = self._require(case_id)
            if case.status not in (WorkflowStatus.PANEL_REVIEW, WorkflowStatus.OBJECTIONS_PENDING, WorkflowStatus.JUDICIAL_REVIEW):
                raise ValueError("Only an active review can be returned for correction.")
            case.status = WorkflowStatus.RETURNED_FOR_CORRECTION
            self._event(case, actor_role, "returned_for_correction", reason)
            return case.model_copy(deep=True)

    def _require(self, case_id: str) -> PeoplesCourtCase:
        if case_id not in self._items:
            raise KeyError(case_id)
        return self._items[case_id]


store = InMemoryCaseStore()
