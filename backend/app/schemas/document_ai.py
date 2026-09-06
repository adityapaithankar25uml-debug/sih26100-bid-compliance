from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    original_filename: str
    content_type: str
    file_size_bytes: int
    sha256_hash: str
    storage_ref: str
    quarantine_status: str  # QUARANTINED | VALIDATED | REJECTED
    malware_scan_result: str  # PENDING_SCAN | CLEAN | INFECTED | SCAN_FAILED
    security_classification: str  # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII


class MalwareScanResponse(BaseModel):
    document_id: str
    scan_result: str  # PENDING_SCAN | CLEAN | INFECTED | SCAN_FAILED
    scanner_id: str
    threat_details: Optional[str] = None
    timestamp: str


class DocumentClassificationResponse(BaseModel):
    document_id: str
    predicted_doc_type: str  # CA_TURNOVER_CERTIFICATE | GST_REGISTRATION_CERTIFICATE | etc.
    confidence_score: float
    page_range: Dict[str, int]  # {"start_page": 1, "end_page": 5}
    requires_human_review: bool
    method: str  # HEURISTIC | AI_GATEWAY | MOCK


class PrivacyGatewayResponse(BaseModel):
    document_id: str
    security_classification: str  # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII
    pii_detected: bool
    pii_flags: List[str]
    cloud_eligibility: str  # ELIGIBLE_EXTERNAL_AI | LOCAL_ONLY | SANITIZE_THEN_EXTERNAL_AI | HUMAN_REVIEW_REQUIRED
    sanitized_text_snippet: Optional[str] = None


class BoundingBoxSchema(BaseModel):
    page_number: int = 1
    x0: float
    y0: float
    x1: float
    y1: float


class ExtractedFactSchema(BaseModel):
    field_name: str
    raw_value: Optional[str] = None
    normalized_value: Optional[str] = None
    unit: Optional[str] = None
    confidence_score: float = 1.0
    page_number: int = 1
    bounding_box: Optional[BoundingBoxSchema] = None
    extraction_method: str = "TEXT_PARSER"
    provenance_ref: Optional[str] = None


class ExtractedFieldsEnvelope(BaseModel):
    extraction_id: str
    source_document_id: str
    extraction_method: str
    sensitivity_level: str
    extracted_fields: List[ExtractedFactSchema]


class TenderRequirementCandidateSchema(BaseModel):
    candidate_code: str
    category: str  # FINANCIAL_TURNOVER | PAST_EXPERIENCE | STATUTORY_COMPLIANCE | EMD_REQUIREMENT | LOCAL_CONTENT
    description: str
    threshold_value: Optional[Any] = None
    unit: Optional[str] = None
    is_mandatory: bool = True
    suggested_rule_code: Optional[str] = None
    source_document_id: str
    page_number: int = 1
    source_text_snippet: Optional[str] = None
    extraction_confidence: float = 1.0
    is_authoritative: bool = False  # Strictly non-authoritative candidate proposal


class TenderRequirementCandidateList(BaseModel):
    tender_id: str
    candidate_requirements: List[TenderRequirementCandidateSchema]


class InconsistencyCandidateSchema(BaseModel):
    signal_code: str
    severity: str  # HIGH | MEDIUM | LOW
    description: str
    affected_document_ids: List[str]
    status: str = "REQUIRES_HUMAN_REVIEW"  # CONSISTENT | POTENTIAL_CONFLICT | UNRESOLVED | REQUIRES_HUMAN_REVIEW


class InconsistencyCandidateList(BaseModel):
    bid_submission_id: str
    inconsistency_candidates: List[InconsistencyCandidateSchema]


class AIGatewayRequest(BaseModel):
    task_type: str
    task_id: str
    data_sensitivity_level: str  # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII
    system_prompt_version: str
    prompt_variables: Dict[str, Any]
    input_text_chunk: str


class AIGatewayResponse(BaseModel):
    task_id: str
    status: str  # SUCCEEDED | VALIDATION_FAILED | FAILED | REQUIRES_HUMAN_REVIEW
    provider_id: str
    model_identifier: str
    is_mock: bool = False
    mode: str = "LIVE"  # LIVE | MOCK | DEMO
    structured_output: Dict[str, Any]
    confidence_score: float = 1.0
    raw_response_hash: str
