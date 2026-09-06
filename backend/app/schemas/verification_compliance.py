from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GovernmentSourceResponse(BaseModel):
    source_code: str
    display_name: str
    authority_type: str
    verification_scope: str
    integration_mode: str
    readiness_status: str
    freshness_policy_days: int
    enabled: bool
    requires_consent: bool
    manual_fallback_allowed: bool
    documentation_reference: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VerificationRequest(BaseModel):
    bid_submission_id: str
    source_code: str
    identifier_type: str
    identifier_value: str
    force_fresh: bool = False


class VerificationRecordResponse(BaseModel):
    id: str
    bid_submission_id: Optional[str] = None
    bidder_id: Optional[str] = None
    source_code: str
    adapter_name: str
    integration_mode: str
    requested_at: datetime
    responded_at: datetime
    technical_status: str
    business_status: str
    source_authority_type: str
    freshness_status: str
    identity_match_status: str
    normalized_facts_json: Dict[str, Any]
    raw_response_hash: Optional[str] = None
    error_category: Optional[str] = None
    is_manual_fallback: bool
    manual_officer_id: Optional[str] = None
    manual_notes: Optional[str] = None
    manual_evidence_ref: Optional[str] = None
    correlation_id: str

    model_config = ConfigDict(from_attributes=True)


class ManualVerificationRequest(BaseModel):
    bid_submission_id: str
    source_code: str
    business_status: str  # VERIFIED, NOT_FOUND, INACTIVE, DEBARRED, etc.
    manual_notes: str
    manual_evidence_ref: Optional[str] = None
    normalized_facts: Dict[str, Any] = Field(default_factory=dict)


class ComplianceRuleResponse(BaseModel):
    id: str
    rule_code: str
    name: str
    description: Optional[str] = None
    rule_type: str
    version: str
    policy_code: str
    policy_version: str
    severity: str
    evaluation_expression_json: Dict[str, Any]
    required_facts_json: List[str]
    explanation_template: str

    model_config = ConfigDict(from_attributes=True)


class PolicyVersionResponse(BaseModel):
    id: str
    policy_code: str
    version: str
    title: str
    jurisdiction: str
    effective_from: datetime
    effective_to: Optional[datetime] = None
    status: str
    policy_hash: str

    model_config = ConfigDict(from_attributes=True)


class RuleResultResponse(BaseModel):
    id: str
    rule_id: str
    rule_code: str
    requirement_id: Optional[str] = None
    result_status: str  # PASS, FAIL, MISSING_EVIDENCE, UNKNOWN, REVIEW_REQUIRED
    explanation_text: str
    evaluation_trace: Dict[str, Any] = Field(alias="evaluation_trace_json")
    fact_values: Dict[str, Any] = Field(alias="fact_values_json")
    evidence_refs: List[str] = Field(alias="evidence_refs_json")

    model_config = ConfigDict(from_attributes=True)


class ComplianceEvaluationResponse(BaseModel):
    id: str
    bid_submission_id: str
    tender_id: str
    tender_version_id: str
    policy_version_id: Optional[str] = None
    evaluation_status: str  # COMPLIANT, NON_COMPLIANT, REQUIRES_REVIEW, INCOMPLETE
    overall_qualification_recommendation: str
    evaluation_trace_json: Dict[str, Any]
    evaluated_at: datetime
    evaluator_id: str
    rule_results: List[RuleResultResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ComplianceMatrixItem(BaseModel):
    requirement_id: str
    requirement_code: str
    requirement_title: str
    category: str
    rule_code: Optional[str] = None
    rule_name: Optional[str] = None
    fact_code: Optional[str] = None
    fact_value: Optional[Any] = None
    fact_status: Optional[str] = None
    source_code: Optional[str] = None
    verification_status: Optional[str] = None
    compliance_status: str  # PASS, FAIL, MISSING, REVIEW, UNKNOWN
    evidence_ref: Optional[str] = None
    explanation: str


class ComplianceMatrixResponse(BaseModel):
    bid_submission_id: str
    tender_id: str
    overall_status: str
    qualification_recommendation: str
    matrix_items: List[ComplianceMatrixItem]


class HumanReviewTaskResponse(BaseModel):
    id: str
    bid_submission_id: str
    document_id: Optional[str] = None
    verification_record_id: Optional[str] = None
    evaluation_id: Optional[str] = None
    review_reason: str
    severity: str
    status: str
    assigned_officer_id: Optional[str] = None
    decision: Optional[str] = None
    comments: Optional[str] = None
    decided_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class HumanReviewDecisionRequest(BaseModel):
    decision: str  # APPROVED, REJECTED, OVERRIDDEN
    comments: str
