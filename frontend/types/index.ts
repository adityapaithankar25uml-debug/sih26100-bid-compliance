export type UserRole = 
  | 'ProcurementOfficer'
  | 'SeniorReviewer'
  | 'Auditor'
  | 'SystemAdmin'
  | 'ServiceWorker'
  | 'Bidder';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  organization_id: string;
  created_at: string;
}

export interface TenderRequirement {
  id: string;
  tender_version_id: string;
  requirement_code: string;
  category: string;
  requirement_text: string;
  is_mandatory: boolean;
  created_at: string;
}

export interface TenderVersion {
  id: string;
  tender_id: string;
  version_number: number;
  description?: string;
  publish_date: string;
  is_finalized: boolean;
  requirements: TenderRequirement[];
  created_at: string;
}

export interface Tender {
  id: string;
  tender_number: string;
  title: string;
  organization: string;
  status: string;
  versions: TenderVersion[];
  created_at: string;
  updated_at: string;
}

export interface Bidder {
  id: string;
  bidder_name: string;
  registration_number: string;
  entity_type: string;
  organization_type: string;
  created_at: string;
}

export interface BidSubmission {
  id: string;
  bidder_id: string;
  tender_id: string;
  tender_version_id: string;
  submission_reference: string;
  submission_date: string;
  status: string;
  created_at: string;
}

export interface AuditEvent {
  id: string;
  actor_id: string;
  actor_role: string;
  action: string;
  resource_type: string;
  resource_id: string;
  correlation_id: string;
  payload_hash: string;
  event_payload: Record<string, any>;
  created_at: string;
}

export interface AuditChainVerify {
  is_valid: boolean;
  total_blocks: number;
  verified_blocks: number;
  first_corrupted_block?: number;
  message: string;
}

// ============================================================
// PHASE 5: EVIDENCE, RISK & HUMAN REVIEW WORKSPACE TYPES
// ============================================================

export interface EvidenceQuality {
  source_authority: string;
  source_freshness: string;
  completeness: string;
  integrity_hash_validity: string;
  identity_linkage: string;
  document_authenticity?: string;
  temporal_applicability?: string;
  extraction_provenance: string;
  consistency: string;
  quality_assessment_summary?: string;
}

export interface EvidenceRecord {
  id: string;
  compliance_evaluation_id?: string;
  bid_submission_id?: string;
  requirement_id?: string;
  rule_id?: string;
  policy_version_id?: string;
  source_document_id?: string;
  verification_result_id?: string;
  verification_record_id?: string;
  evidence_type: string;
  confidence_score: number;
  extraction_method?: string;
  page_number?: number;
  source_text_snippet?: string;
  bounding_box_json?: Record<string, any>;
  evidence_payload?: Record<string, any>;
  evidence_quality_json?: EvidenceQuality;
  status: string;
  security_classification: string;
  provenance_metadata_json?: Record<string, any>;
  created_at: string;
}

export interface EvidenceTraceNode {
  node_id: string;
  node_type: string;
  label: string;
  status: string;
  details: Record<string, any>;
}

export interface EvidenceTraceEdge {
  source_node_id: string;
  target_node_id: string;
  relationship: string;
}

export interface EvidenceTraceGraph {
  submission_id: string;
  requirement_id?: string;
  nodes: EvidenceTraceNode[];
  edges: EvidenceTraceEdge[];
}

export interface WhyExplanationItem {
  requirement_id: string;
  requirement_code: string;
  requirement_title: string;
  rule_code: string;
  policy_version: string;
  tender_version: string;
  status: string;
  facts_used: Record<string, any>;
  evidence_summary: Record<string, any>[];
  calculation_trace: Record<string, any>;
  explanation_text: string;
  ai_advisory_summary?: string;
}

export interface ComplianceExplanationResponse {
  bid_submission_id: string;
  overall_status: string;
  qualification_recommendation: string;
  evaluated_at: string;
  explanations: WhyExplanationItem[];
}

export interface RiskFactorSignal {
  id: string;
  factor_code: string;
  category: string;
  severity: string;
  description: string;
  signal_payload?: Record<string, any>;
}

export interface RiskAssessmentResponse {
  id: string;
  bid_submission_id: string;
  overall_risk_level: string;
  risk_score: number;
  profile_version: string;
  calculated_at: string;
  is_advisory_only: boolean;
  signals: RiskFactorSignal[];
}

export interface HumanReviewTask {
  id: string;
  bid_submission_id: string;
  tender_id?: string;
  tender_requirement_id?: string;
  bidder_id?: string;
  policy_version_id?: string;
  document_id?: string;
  verification_record_id?: string;
  evaluation_id?: string;
  review_code?: string;
  review_reason: string;
  severity: string;
  priority: string;
  status: string;
  assigned_officer_id?: string;
  suggested_action?: string;
  resolution_summary?: string;
  evidence_refs_json?: string[];
  review_history_json?: Record<string, any>[];
  decision?: string;
  comments?: string;
  created_at: string;
  decided_at?: string;
}

export interface ManualOverrideResponse {
  id: string;
  officer_decision_id: string;
  bid_submission_id?: string;
  requirement_id: string;
  rule_id?: string;
  previous_status: string;
  new_status: string;
  override_reason_code?: string;
  override_reason: string;
  supporting_evidence_refs_json?: string[];
  requires_four_eyes: boolean;
  approved_by_officer_id?: string;
  four_eyes_status: string;
  created_at: string;
}

export interface OfficerDecisionResponse {
  id: string;
  bid_submission_id: string;
  tender_id?: string;
  tender_version_id?: string;
  bidder_id?: string;
  reviewer_id: string;
  decision: string;
  rationale: string;
  evaluation_snapshot_id?: string;
  risk_profile_id?: string;
  audit_event_id?: string;
  decision_timestamp: string;
  overrides: ManualOverrideResponse[];
}

export interface EvaluationSnapshot {
  id: string;
  bid_submission_id: string;
  tender_version_id?: string;
  policy_version_id?: string;
  evaluation_id?: string;
  snapshot_data_json: Record<string, any>;
  snapshot_hash: string;
  created_at: string;
}
