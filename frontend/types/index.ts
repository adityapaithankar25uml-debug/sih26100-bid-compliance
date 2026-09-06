export type UserRole = 
  | 'ProcurementOfficer'
  | 'SeniorReviewer'
  | 'Auditor'
  | 'SystemAdmin'
  | 'ServiceWorker';

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
