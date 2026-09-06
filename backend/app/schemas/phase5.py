import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EvidenceQuality(BaseModel):
    source_authority: str = Field(default="AUTHORITATIVE_GOVT", description="AUTHORITATIVE_GOVT | BIDDER_DOCUMENT | AI_EXTRACTED | MANUAL_OFFICER")
    source_freshness: str = Field(default="FRESH", description="FRESH | ACCEPTABLE | STALE | UNKNOWN")
    completeness: str = Field(default="COMPLETE", description="COMPLETE | PARTIAL | MISSING")
    integrity_hash_validity: str = Field(default="VERIFIED", description="VERIFIED | UNCHECKED | FAILED")
    identity_linkage: str = Field(default="MATCHED", description="MATCHED | PARTIAL_MATCH | MISMATCH | UNVERIFIED")
    document_authenticity: str = Field(default="SCAN_CLEAN", description="SCAN_CLEAN | OCR_VERIFIED | SUSPECT | UNVERIFIED")
    temporal_applicability: str = Field(default="VALID_WINDOW", description="VALID_WINDOW | EXPIRED | FUTURE_EFFECTIVE | UNKNOWN")
    extraction_provenance: str = Field(default="DIRECT", description="DIRECT | OCR | AI_PARSED | MANUAL")
    consistency: str = Field(default="CONSISTENT", description="CONSISTENT | CONFLICTING | UNKNOWN")
    quality_assessment_summary: str = Field(default="STRONG", description="STRONG | MODERATE | NEEDS_REVIEW | INSUFFICIENT — Presentation-level decision support summary derived from explicit policy rules")


class EvidenceRecordResponse(BaseModel):
    id: str
    compliance_evaluation_id: Optional[str] = None
    bid_submission_id: Optional[str] = None
    requirement_id: Optional[str] = None
    rule_id: Optional[str] = None
    policy_version_id: Optional[str] = None
    source_document_id: Optional[str] = None
    verification_result_id: Optional[str] = None
    verification_record_id: Optional[str] = None
    evidence_type: str
    confidence_score: float = 1.0
    extraction_method: Optional[str] = None
    page_number: Optional[int] = None
    source_text_snippet: Optional[str] = None
    bounding_box_json: Optional[Dict[str, Any]] = None
    evidence_payload: Optional[Dict[str, Any]] = None
    evidence_quality_json: Optional[Dict[str, Any]] = None
    status: str = "VALID"
    security_classification: str = "INTERNAL" # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII
    provenance_metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class EvidenceTraceNode(BaseModel):
    node_id: str
    node_type: str # REQUIREMENT | RULE | FACT | EVIDENCE | SOURCE_DOC | GOVT_RECORD | RISK_SIGNAL | HUMAN_REVIEW | OFFICER_DECISION | AUDIT_BLOCK
    label: str
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)


class EvidenceTraceEdge(BaseModel):
    source_node_id: str
    target_node_id: str
    relationship: str


class EvidenceTraceGraphResponse(BaseModel):
    submission_id: str
    requirement_id: Optional[str] = None
    nodes: List[EvidenceTraceNode]
    edges: List[EvidenceTraceEdge]


class WhyExplanationItem(BaseModel):
    requirement_id: str
    requirement_code: str
    requirement_title: str
    rule_code: str
    policy_version: str
    tender_version: str
    status: str # PASS, FAIL, MISSING_EVIDENCE, REQUIRES_REVIEW, UNKNOWN, STALE, CONFLICTING
    facts_used: Dict[str, Any]
    evidence_summary: List[Dict[str, Any]]
    calculation_trace: Dict[str, Any]
    explanation_text: str
    ai_advisory_summary: Optional[str] = None


class ComplianceExplanationResponse(BaseModel):
    bid_submission_id: str
    overall_status: str
    qualification_recommendation: str
    evaluated_at: datetime.datetime
    explanations: List[WhyExplanationItem]


class EvaluationSnapshotResponse(BaseModel):
    id: str
    bid_submission_id: str
    tender_version_id: Optional[str] = None
    policy_version_id: Optional[str] = None
    evaluation_id: Optional[str] = None
    snapshot_data_json: Dict[str, Any]
    snapshot_hash: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class RiskFactorSignalResponse(BaseModel):
    id: str
    factor_code: str
    category: str
    severity: str
    description: str
    signal_payload: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class RiskAssessmentResponse(BaseModel):
    id: str
    bid_submission_id: str
    overall_risk_level: str # LOW | MEDIUM | HIGH | CRITICAL
    risk_score: float
    profile_version: str = "1.0.0"
    calculated_at: datetime.datetime
    is_advisory_only: bool = True
    signals: List[RiskFactorSignalResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class HumanReviewTaskResponse(BaseModel):
    id: str
    bid_submission_id: str
    tender_id: Optional[str] = None
    tender_requirement_id: Optional[str] = None
    bidder_id: Optional[str] = None
    policy_version_id: Optional[str] = None
    document_id: Optional[str] = None
    verification_record_id: Optional[str] = None
    evaluation_id: Optional[str] = None
    review_code: Optional[str] = None
    review_reason: str
    severity: str
    priority: str = "MEDIUM"
    status: str # PENDING | IN_REVIEW | RESOLVED | REJECTED | ESCALATED
    assigned_officer_id: Optional[str] = None
    suggested_action: Optional[str] = None
    resolution_summary: Optional[str] = None
    evidence_refs_json: Optional[List[str]] = None
    review_history_json: Optional[List[Dict[str, Any]]] = None
    decision: Optional[str] = None
    comments: Optional[str] = None
    created_at: datetime.datetime
    decided_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class HumanReviewAssignRequest(BaseModel):
    officer_id: str


class HumanReviewResolveRequest(BaseModel):
    decision: str # RESOLVED | OVERRIDDEN | ESCALATED | REJECTED
    resolution_summary: str
    comments: Optional[str] = None


class ManualOverrideCreateRequest(BaseModel):
    requirement_id: str
    rule_id: Optional[str] = None
    previous_status: str
    new_status: str
    override_reason_code: str = "OFFICER_REVIEW" # NEW_EVIDENCE, SOURCE_CORRECTION, IDENTITY_CLARIFICATION, POLICY_EXCEPTION, DATA_CORRECTION, OFFICER_REVIEW, OTHER
    override_reason: str
    supporting_evidence_refs: Optional[List[str]] = None
    requires_four_eyes: bool = False


class ManualOverrideApproveRequest(BaseModel):
    approved: bool
    comments: Optional[str] = None


class ManualOverrideResponse(BaseModel):
    id: str
    officer_decision_id: str
    bid_submission_id: Optional[str] = None
    requirement_id: str
    rule_id: Optional[str] = None
    previous_status: str
    new_status: str
    override_reason_code: Optional[str] = None
    override_reason: str
    supporting_evidence_refs_json: Optional[List[str]] = None
    requires_four_eyes: bool = False
    approved_by_officer_id: Optional[str] = None
    four_eyes_status: str = "APPROVED"
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class OfficerDecisionRequest(BaseModel):
    decision: str # QUALIFIED | DISQUALIFIED | REQUIRES_CLARIFICATION | EVIDENCE_REQUESTED
    rationale: str
    overrides: Optional[List[ManualOverrideCreateRequest]] = None


class OfficerDecisionResponse(BaseModel):
    id: str
    bid_submission_id: str
    tender_id: Optional[str] = None
    tender_version_id: Optional[str] = None
    bidder_id: Optional[str] = None
    reviewer_id: str
    decision: str
    rationale: str
    evaluation_snapshot_id: Optional[str] = None
    risk_profile_id: Optional[str] = None
    audit_event_id: Optional[str] = None
    decision_timestamp: datetime.datetime
    overrides: List[ManualOverrideResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
