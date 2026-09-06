import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Index,
    JSON,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.base import BaseModelMixin

# Cross-dialect JSON column type (JSONB on PostgreSQL, JSON on SQLite)
JSONB_TYPE = JSON().with_variant(JSONB, "postgresql")



class User(BaseModelMixin, Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="ProcurementOfficer")
    is_active = Column(Boolean, default=True, nullable=False)
    organization_id = Column(String(100), default="CPCL", nullable=False)

    officer_decisions = relationship("OfficerDecision", back_populates="reviewer")


class Tender(BaseModelMixin, Base):
    __tablename__ = "tenders"

    tender_number = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    organization = Column(String(255), default="CPCL", nullable=False)
    status = Column(String(50), default="DRAFT", nullable=False)

    versions = relationship("TenderVersion", back_populates="tender", cascade="all, delete-orphan")
    submissions = relationship("BidSubmission", back_populates="tender")


class TenderVersion(BaseModelMixin, Base):
    __tablename__ = "tender_versions"
    __table_args__ = (
        UniqueConstraint("tender_id", "version_number", name="uq_tender_version"),
    )

    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)
    publish_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    is_finalized = Column(Boolean, default=False, nullable=False)

    tender = relationship("Tender", back_populates="versions")
    requirements = relationship("TenderRequirement", back_populates="tender_version", cascade="all, delete-orphan")
    submissions = relationship("BidSubmission", back_populates="tender_version")


class TenderRequirement(BaseModelMixin, Base):
    __tablename__ = "tender_requirements"

    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=False, index=True)
    requirement_code = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    requirement_text = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    metadata_json = Column(JSONB_TYPE, nullable=True)

    tender_version = relationship("TenderVersion", back_populates="requirements")
    rule_maps = relationship("RequirementRuleMap", back_populates="tender_requirement")
    evaluations = relationship("ComplianceEvaluation", back_populates="tender_requirement")


class PolicyVersion(BaseModelMixin, Base):
    __tablename__ = "policy_versions"
    __table_args__ = (
        UniqueConstraint("policy_code", "version", name="uq_policy_code_version"),
    )

    policy_code = Column(String(100), nullable=False, default="POL_GEM_COMPLIANCE_2026", index=True)
    policy_name = Column(String(255), nullable=True, default="GeM Compliance Policy 2026")
    title = Column(String(255), nullable=True)
    version = Column(String(50), nullable=False, default="1.0")
    jurisdiction = Column(String(100), default="INDIA_GEM", nullable=False)
    effective_from = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    effective_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    effective_to = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)
    source_reference = Column(String(500), nullable=True)
    policy_hash = Column(String(64), nullable=True)
    rules_config_json = Column(JSONB_TYPE, nullable=True)

    rules = relationship("ComplianceRule", back_populates="policy_version_rel")


class ComplianceRule(BaseModelMixin, Base):
    __tablename__ = "compliance_rules"

    policy_version_id = Column(String(26), ForeignKey("policy_versions.id"), nullable=True, index=True)
    rule_code = Column(String(100), unique=True, index=True, nullable=False)
    rule_name = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, default="COMPLIANCE")
    rule_type = Column(String(50), default="BOOLEAN_FACT", nullable=False)
    version = Column(String(50), default="1.0", nullable=False)
    policy_code = Column(String(100), default="POL_GEM_COMPLIANCE_2026", nullable=False, index=True)
    policy_version_str = Column(String(50), default="1.0", nullable=False)
    policy_version = Column(String(50), default="1.0", nullable=False)
    effective_from = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    effective_to = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    expression_dsl = Column(Text, nullable=True)
    evaluation_expression_json = Column(JSONB_TYPE, nullable=True)
    required_facts_json = Column(JSONB_TYPE, nullable=True)
    explanation_template = Column(Text, nullable=True)
    severity = Column(String(50), default="MANDATORY", nullable=False)

    policy_version_rel = relationship("PolicyVersion", back_populates="rules")
    rule_maps = relationship("RequirementRuleMap", back_populates="compliance_rule")
    evaluations = relationship("ComplianceEvaluation", back_populates="compliance_rule")



class RequirementRuleMap(BaseModelMixin, Base):
    __tablename__ = "requirement_rule_maps"

    tender_requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=False, index=True)
    compliance_rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=False, index=True)
    mapping_type = Column(String(50), default="DIRECT", nullable=False)
    weight = Column(Float, default=1.0, nullable=False)

    tender_requirement = relationship("TenderRequirement", back_populates="rule_maps")
    compliance_rule = relationship("ComplianceRule", back_populates="rule_maps")


class Bidder(BaseModelMixin, Base):
    __tablename__ = "bidders"

    bidder_name = Column(String(255), nullable=False, index=True)
    registration_number = Column(String(100), unique=True, index=True, nullable=False)
    entity_type = Column(String(100), default="PRIVATE_LIMITED", nullable=False)
    organization_type = Column(String(100), default="MSE", nullable=False)

    identities = relationship("BidderIdentity", back_populates="bidder", cascade="all, delete-orphan")
    submissions = relationship("BidSubmission", back_populates="bidder")
    verification_requests = relationship("GovernmentVerificationRequest", back_populates="bidder")


class BidderIdentity(BaseModelMixin, Base):
    __tablename__ = "bidder_identities"

    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=False, index=True)
    pan_hash = Column(String(64), nullable=True, index=True)
    gstin_hash = Column(String(64), nullable=True, index=True)
    udyam_hash = Column(String(64), nullable=True, index=True)
    verification_status = Column(String(50), default="UNVERIFIED", nullable=False)

    bidder = relationship("Bidder", back_populates="identities")


class BidSubmission(BaseModelMixin, Base):
    __tablename__ = "bid_submissions"

    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=False, index=True)
    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=False, index=True)
    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=False, index=True)
    submission_reference = Column(String(100), unique=True, index=True, nullable=False)
    submission_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String(50), default="SUBMITTED", nullable=False)

    bidder = relationship("Bidder", back_populates="submissions")
    tender = relationship("Tender", back_populates="submissions")
    tender_version = relationship("TenderVersion", back_populates="submissions")
    covers = relationship("SubmissionCover", back_populates="submission", cascade="all, delete-orphan")
    documents = relationship("SourceDocument", back_populates="submission", cascade="all, delete-orphan")
    evaluations = relationship("ComplianceEvaluation", back_populates="submission", cascade="all, delete-orphan")
    risk_profiles = relationship("RiskAssessmentProfile", back_populates="submission", cascade="all, delete-orphan")
    officer_decisions = relationship("OfficerDecision", back_populates="submission", cascade="all, delete-orphan")


class SubmissionCover(BaseModelMixin, Base):
    __tablename__ = "submission_covers"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    cover_type = Column(String(100), nullable=False) # e.g. TECHNICAL, FINANCIAL, FEE
    document_count = Column(Integer, default=0, nullable=False)
    remarks = Column(Text, nullable=True)

    submission = relationship("BidSubmission", back_populates="covers")
    documents = relationship("SourceDocument", back_populates="submission_cover")


class SourceDocument(BaseModelMixin, Base):
    __tablename__ = "source_documents"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    submission_cover_id = Column(String(26), ForeignKey("submission_covers.id"), nullable=True, index=True)
    original_filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    sha256_hash = Column(String(64), nullable=False, index=True)
    storage_ref = Column(String(500), nullable=False)
    upload_status = Column(String(50), default="UPLOADED", nullable=False)
    security_classification = Column(String(50), default="INTERNAL", nullable=False) # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII
    quarantine_status = Column(String(50), default="QUARANTINED", nullable=False) # QUARANTINED | VALIDATED | REJECTED
    malware_scan_result = Column(String(50), default="PENDING_SCAN", nullable=False) # PENDING_SCAN | CLEAN | INFECTED | SCAN_FAILED
    parent_document_id = Column(String(26), ForeignKey("source_documents.id"), nullable=True, index=True)
    metadata_json = Column(JSONB_TYPE, nullable=True)

    submission = relationship("BidSubmission", back_populates="documents")
    submission_cover = relationship("SubmissionCover", back_populates="documents")
    extractions = relationship("DocumentExtraction", back_populates="source_document", cascade="all, delete-orphan")
    evidences = relationship("EvidenceRecord", back_populates="source_document")
    parent_document = relationship("SourceDocument", remote_side="SourceDocument.id", backref="derivatives")


class DocumentExtraction(BaseModelMixin, Base):
    __tablename__ = "document_extractions"

    source_document_id = Column(String(26), ForeignKey("source_documents.id"), nullable=False, index=True)
    extraction_status = Column(String(50), default="COMPLETED", nullable=False)
    extraction_method = Column(String(50), default="TEXT_PARSER", nullable=False) # TEXT_PARSER | OCR_PADDLE | OCR_TESSERACT | MOCK_OCR | AI_GATEWAY
    confidence_score = Column(Float, default=1.0, nullable=False)
    extractor_version = Column(String(50), default="v1.0", nullable=False)
    sensitivity_level = Column(String(50), default="INTERNAL", nullable=False)
    pii_detected_json = Column(JSONB_TYPE, nullable=True)
    metadata_json = Column(JSONB_TYPE, nullable=True)

    source_document = relationship("SourceDocument", back_populates="extractions")
    extracted_fields = relationship("ExtractedField", back_populates="document_extraction", cascade="all, delete-orphan")


class ExtractedField(BaseModelMixin, Base):
    __tablename__ = "extracted_fields"

    document_extraction_id = Column(String(26), ForeignKey("document_extractions.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False, index=True)
    field_value = Column(Text, nullable=True)
    normalized_value = Column(Text, nullable=True)
    source_text_snippet = Column(Text, nullable=True)
    field_type = Column(String(50), default="STRING", nullable=False)
    confidence = Column(Float, default=1.0, nullable=False)

    document_extraction = relationship("DocumentExtraction", back_populates="extracted_fields")
    bounding_boxes = relationship("BoundingBox", back_populates="extracted_field", cascade="all, delete-orphan")


class BoundingBox(BaseModelMixin, Base):
    __tablename__ = "bounding_boxes"

    extracted_field_id = Column(String(26), ForeignKey("extracted_fields.id"), nullable=False, index=True)
    page_number = Column(Integer, default=1, nullable=False)
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    x_max = Column(Float, nullable=False)
    y_max = Column(Float, nullable=False)

    extracted_field = relationship("ExtractedField", back_populates="bounding_boxes")


class GovernmentVerificationRequest(BaseModelMixin, Base):
    __tablename__ = "government_verification_requests"

    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=False, index=True)
    verification_type = Column(String(100), nullable=False) # e.g. PAN, GSTIN, UDYAM
    target_identifier = Column(String(100), nullable=False)
    request_status = Column(String(50), default="PENDING", nullable=False)

    bidder = relationship("Bidder", back_populates="verification_requests")
    attempts = relationship("GovernmentVerificationAttempt", back_populates="verification_request", cascade="all, delete-orphan")


class GovernmentVerificationAttempt(BaseModelMixin, Base):
    __tablename__ = "government_verification_attempts"

    verification_request_id = Column(String(26), ForeignKey("government_verification_requests.id"), nullable=False, index=True)
    attempt_number = Column(Integer, default=1, nullable=False)
    source_system = Column(String(100), nullable=False) # e.g. MOCK_GSTIN_PORTAL, MOCK_PAN_PORTAL
    mode = Column(String(50), default="MOCK", nullable=False) # LIVE | SANDBOX | MOCK | MANUAL_FALLBACK
    http_status = Column(Integer, default=200, nullable=False)
    response_summary = Column(Text, nullable=True)

    verification_request = relationship("GovernmentVerificationRequest", back_populates="attempts")
    results = relationship("GovernmentVerificationResult", back_populates="verification_attempt", cascade="all, delete-orphan")


class GovernmentVerificationResult(BaseModelMixin, Base):
    __tablename__ = "government_verification_results"

    verification_attempt_id = Column(String(26), ForeignKey("government_verification_attempts.id"), nullable=False, index=True)
    verification_status = Column(String(50), default="VERIFIED", nullable=False)
    verified_data_json = Column(JSONB_TYPE, nullable=True)
    match_confidence = Column(Float, default=1.0, nullable=False)

    verification_attempt = relationship("GovernmentVerificationAttempt", back_populates="results")
    evidences = relationship("EvidenceRecord", back_populates="verification_result")


class ComplianceEvaluation(BaseModelMixin, Base):
    __tablename__ = "compliance_evaluations"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    tender_requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=True, index=True)
    compliance_rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=True, index=True)
    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=True, index=True)
    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=True, index=True)
    policy_version_id = Column(String(26), ForeignKey("policy_versions.id"), nullable=True, index=True)
    status = Column(String(50), default="REQUIRES_HUMAN_REVIEW", nullable=False) # VERIFIED | UNVERIFIED | MISSING_EVIDENCE | REQUIRES_HUMAN_REVIEW
    evaluation_status = Column(String(50), default="REQUIRES_REVIEW", nullable=False)
    overall_qualification_recommendation = Column(String(50), default="HUMAN_OFFICER_REVIEW_REQUIRED", nullable=False)
    evaluation_result_json = Column(JSONB_TYPE, nullable=True)
    evaluation_trace_json = Column(JSONB_TYPE, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    evaluator_id = Column(String(26), nullable=False, default="SYSTEM")

    submission = relationship("BidSubmission", back_populates="evaluations")
    tender_requirement = relationship("TenderRequirement", back_populates="evaluations")
    compliance_rule = relationship("ComplianceRule", back_populates="evaluations")
    evidences = relationship("EvidenceRecord", back_populates="compliance_evaluation", cascade="all, delete-orphan")
    rule_results = relationship("ComplianceRuleResult", back_populates="evaluation", cascade="all, delete-orphan")


class EvidenceRecord(BaseModelMixin, Base):
    __tablename__ = "evidence_records"

    compliance_evaluation_id = Column(String(26), ForeignKey("compliance_evaluations.id"), nullable=True, index=True)
    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=True, index=True)
    requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=True, index=True)
    rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=True, index=True)
    policy_version_id = Column(String(26), ForeignKey("policy_versions.id"), nullable=True, index=True)
    source_document_id = Column(String(26), ForeignKey("source_documents.id"), nullable=True, index=True)
    verification_result_id = Column(String(26), ForeignKey("government_verification_results.id"), nullable=True, index=True)
    verification_record_id = Column(String(26), ForeignKey("government_verification_records.id"), nullable=True, index=True)
    evidence_type = Column(String(100), nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    extraction_method = Column(String(50), default="TEXT_PARSER", nullable=True)
    page_number = Column(Integer, nullable=True)
    source_text_snippet = Column(Text, nullable=True)
    bounding_box_json = Column(JSONB_TYPE, nullable=True)
    evidence_payload = Column(JSONB_TYPE, nullable=True)
    evidence_quality_json = Column(JSONB_TYPE, nullable=True)
    status = Column(String(50), default="VALID", nullable=False)
    security_classification = Column(String(50), default="INTERNAL", nullable=False)
    provenance_metadata_json = Column(JSONB_TYPE, nullable=True)

    compliance_evaluation = relationship("ComplianceEvaluation", back_populates="evidences")
    source_document = relationship("SourceDocument", back_populates="evidences")
    verification_result = relationship("GovernmentVerificationResult", back_populates="evidences")


class RiskAssessmentProfile(BaseModelMixin, Base):
    __tablename__ = "risk_assessment_profiles"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    overall_risk_level = Column(String(50), default="LOW", nullable=False) # LOW | MEDIUM | HIGH | CRITICAL
    risk_score = Column(Float, default=0.0, nullable=False)
    profile_version = Column(String(50), default="1.0.0", nullable=False)
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    submission = relationship("BidSubmission", back_populates="risk_profiles")
    signals = relationship("RiskFactorSignal", back_populates="risk_assessment_profile", cascade="all, delete-orphan")


class RiskFactorSignal(BaseModelMixin, Base):
    __tablename__ = "risk_factor_signals"

    risk_assessment_profile_id = Column(String(26), ForeignKey("risk_assessment_profiles.id"), nullable=False, index=True)
    factor_code = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    severity = Column(String(50), default="LOW", nullable=False)
    description = Column(Text, nullable=False)
    signal_payload = Column(JSONB_TYPE, nullable=True)

    risk_assessment_profile = relationship("RiskAssessmentProfile", back_populates="signals")


class OfficerDecision(BaseModelMixin, Base):
    __tablename__ = "officer_decisions"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    reviewer_id = Column(String(26), ForeignKey("users.id"), nullable=False, index=True)
    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=True, index=True)
    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=True, index=True)
    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=True, index=True)
    decision = Column(String(50), nullable=False) # QUALIFIED | DISQUALIFIED | REQUIRES_CLARIFICATION | EVIDENCE_REQUESTED
    rationale = Column(Text, nullable=False)
    evaluation_snapshot_id = Column(String(26), nullable=True, index=True)
    risk_profile_id = Column(String(26), ForeignKey("risk_assessment_profiles.id"), nullable=True, index=True)
    audit_event_id = Column(String(26), ForeignKey("audit_events.id"), nullable=True, index=True)
    decision_timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    submission = relationship("BidSubmission", back_populates="officer_decisions")
    reviewer = relationship("User", back_populates="officer_decisions")
    overrides = relationship("ManualOverride", back_populates="officer_decision", cascade="all, delete-orphan")


class ManualOverride(BaseModelMixin, Base):
    __tablename__ = "manual_overrides"

    officer_decision_id = Column(String(26), ForeignKey("officer_decisions.id"), nullable=False, index=True)
    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=True, index=True)
    requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=False, index=True)
    rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=True, index=True)
    previous_status = Column(String(50), nullable=False)
    new_status = Column(String(50), nullable=False)
    override_reason_code = Column(String(100), nullable=True, default="OFFICER_REVIEW")
    override_reason = Column(Text, nullable=False)
    supporting_evidence_refs_json = Column(JSONB_TYPE, nullable=True)
    requires_four_eyes = Column(Boolean, default=False, nullable=False)
    approved_by_officer_id = Column(String(26), ForeignKey("users.id"), nullable=True, index=True)
    four_eyes_status = Column(String(50), default="APPROVED", nullable=False)

    officer_decision = relationship("OfficerDecision", back_populates="overrides")


class EvaluationSnapshot(BaseModelMixin, Base):
    __tablename__ = "evaluation_snapshots"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=True, index=True)
    policy_version_id = Column(String(26), ForeignKey("policy_versions.id"), nullable=True, index=True)
    evaluation_id = Column(String(26), ForeignKey("compliance_evaluations.id"), nullable=True, index=True)
    snapshot_data_json = Column(JSONB_TYPE, nullable=False)
    snapshot_hash = Column(String(64), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class AuditEvent(BaseModelMixin, Base):
    __tablename__ = "audit_events"

    actor_id = Column(String(26), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(26), nullable=False, index=True)
    correlation_id = Column(String(100), nullable=False, index=True)
    payload_hash = Column(String(64), nullable=False)
    event_payload = Column(JSONB_TYPE, nullable=False)

    blocks = relationship("AuditHashChainBlock", back_populates="audit_event")


class AuditHashChainBlock(BaseModelMixin, Base):
    __tablename__ = "audit_hash_chain_blocks"

    block_index = Column(Integer, unique=True, index=True, nullable=False)
    audit_event_id = Column(String(26), ForeignKey("audit_events.id"), nullable=False, index=True)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    audit_event = relationship("AuditHashChainBlock", remote_side="AuditHashChainBlock.id", backref="chain_block") if False else relationship("AuditEvent", back_populates="blocks")


class GovernmentSourceRegistry(BaseModelMixin, Base):
    __tablename__ = "government_source_registries"

    source_code = Column(String(50), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    authority_type = Column(String(100), nullable=False)
    verification_scope = Column(String(255), nullable=False)
    integration_mode = Column(String(50), default="MOCK", nullable=False)  # LIVE, SANDBOX, MOCK, MANUAL_FALLBACK
    readiness_status = Column(String(100), default="MOCK_ONLY", nullable=False)
    freshness_policy_days = Column(Integer, default=30, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    requires_consent = Column(Boolean, default=False, nullable=False)
    manual_fallback_allowed = Column(Boolean, default=True, nullable=False)
    documentation_reference = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)


class GovernmentVerificationRecord(BaseModelMixin, Base):
    __tablename__ = "government_verification_records"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=True, index=True)
    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=True, index=True)
    source_code = Column(String(50), nullable=False, index=True)
    adapter_name = Column(String(100), nullable=False)
    integration_mode = Column(String(50), nullable=False)
    requested_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    responded_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    technical_status = Column(String(50), nullable=False)  # SUCCESS, TIMEOUT, RATE_LIMITED, UNAVAILABLE, AUTH_FAILED
    business_status = Column(String(50), nullable=False)   # VERIFIED, NOT_VERIFIED, NOT_FOUND, INACTIVE, DEBARRED, CONFLICTING
    source_authority_type = Column(String(100), nullable=False)
    freshness_status = Column(String(50), default="FRESH", nullable=False)
    identity_match_status = Column(String(50), default="NOT_VERIFIED", nullable=False)  # MATCHED, PARTIAL_MATCH, MISMATCH, AMBIGUOUS
    normalized_facts_json = Column(JSONB_TYPE, nullable=False, default=dict)
    raw_response_hash = Column(String(64), nullable=True)
    error_category = Column(String(100), nullable=True)
    is_manual_fallback = Column(Boolean, default=False, nullable=False)
    manual_officer_id = Column(String(26), nullable=True)
    manual_notes = Column(Text, nullable=True)
    manual_evidence_ref = Column(String(255), nullable=True)
    correlation_id = Column(String(100), nullable=False, index=True)

    facts = relationship("ComplianceFact", back_populates="verification_record")


class RequirementRuleMapping(BaseModelMixin, Base):
    __tablename__ = "requirement_rule_mappings"

    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=False, index=True)
    tender_version_id = Column(String(26), ForeignKey("tender_versions.id"), nullable=False, index=True)
    requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=False, index=True)
    rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)


class ComplianceFact(BaseModelMixin, Base):
    __tablename__ = "compliance_facts"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    fact_code = Column(String(100), nullable=False, index=True)
    fact_value = Column(JSONB_TYPE, nullable=False)
    fact_status = Column(String(50), nullable=False)  # VERIFIED, UNVERIFIED, MISSING, STALE, CONFLICTING
    provenance_ref = Column(String(500), nullable=False)
    verification_record_id = Column(String(26), ForeignKey("government_verification_records.id"), nullable=True, index=True)
    extracted_field_id = Column(String(26), ForeignKey("extracted_fields.id"), nullable=True, index=True)
    retrieved_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    verification_record = relationship("GovernmentVerificationRecord", back_populates="facts")


class ComplianceRuleResult(BaseModelMixin, Base):
    __tablename__ = "compliance_rule_results"

    evaluation_id = Column(String(26), ForeignKey("compliance_evaluations.id"), nullable=False, index=True)
    rule_id = Column(String(26), ForeignKey("compliance_rules.id"), nullable=False, index=True)
    rule_code = Column(String(100), nullable=False, index=True)
    requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=True, index=True)
    result_status = Column(String(50), nullable=False)  # PASS, FAIL, MISSING_EVIDENCE, UNKNOWN, REVIEW_REQUIRED
    evaluation_trace_json = Column(JSONB_TYPE, nullable=False, default=dict)
    explanation_text = Column(Text, nullable=False)
    fact_values_json = Column(JSONB_TYPE, nullable=False, default=dict)
    evidence_refs_json = Column(JSONB_TYPE, nullable=False, default=list)

    evaluation = relationship("ComplianceEvaluation", back_populates="rule_results")


class HumanReviewTask(BaseModelMixin, Base):
    __tablename__ = "human_review_tasks"

    bid_submission_id = Column(String(26), ForeignKey("bid_submissions.id"), nullable=False, index=True)
    tender_id = Column(String(26), ForeignKey("tenders.id"), nullable=True, index=True)
    tender_requirement_id = Column(String(26), ForeignKey("tender_requirements.id"), nullable=True, index=True)
    bidder_id = Column(String(26), ForeignKey("bidders.id"), nullable=True, index=True)
    policy_version_id = Column(String(26), ForeignKey("policy_versions.id"), nullable=True, index=True)
    document_id = Column(String(26), ForeignKey("source_documents.id"), nullable=True, index=True)
    verification_record_id = Column(String(26), ForeignKey("government_verification_records.id"), nullable=True, index=True)
    evaluation_id = Column(String(26), ForeignKey("compliance_evaluations.id"), nullable=True, index=True)
    review_code = Column(String(100), nullable=True, index=True)
    review_reason = Column(String(255), nullable=False)
    severity = Column(String(50), default="MEDIUM", nullable=False)  # HIGH, MEDIUM, LOW, CRITICAL
    priority = Column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, IN_REVIEW, RESOLVED, REJECTED, ESCALATED
    assigned_officer_id = Column(String(26), nullable=True, index=True)
    suggested_action = Column(Text, nullable=True)
    resolution_summary = Column(Text, nullable=True)
    evidence_refs_json = Column(JSONB_TYPE, nullable=True)
    review_history_json = Column(JSONB_TYPE, nullable=True)
    decision = Column(String(50), nullable=True)
    comments = Column(Text, nullable=True)
    decided_at = Column(DateTime, nullable=True)


