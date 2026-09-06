import { Tender, Bidder, BidSubmission, AuditEvent, AuditChainVerify, User, ComplianceExplanationResponse, EvidenceTraceGraph, RiskAssessmentResponse, HumanReviewTask, OfficerDecisionResponse, ManualOverrideResponse, GovernmentSource, GovernmentVerificationRecord, ComplianceMatrixResponse } from '../types';


const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Correlation-ID': `FE-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
  };
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return headers;
}

export async function fetchHealth(): Promise<{ status: string }> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    return await res.json();
  } catch (err) {
    return { status: 'error' };
  }
}

export async function fetchReadiness(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/readiness`);
    return await res.json();
  } catch (err) {
    return { status: 'unreachable' };
  }
}

export async function loginDemo(email: string, role: string): Promise<User | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: 'DemoPass123!' }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data));
    }
    return {
      id: data.user_id,
      email: data.email,
      full_name: data.full_name,
      role: data.role,
      is_active: true,
      organization_id: 'CPCL',
      created_at: new Date().toISOString(),
    };
  } catch (err) {
    return null;
  }
}

export async function fetchTenders(): Promise<Tender[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/tenders`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchTenderById(id: string): Promise<Tender | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/tenders/${id}`, { headers: getAuthHeaders() });
    if (res.ok) return await res.json();
  } catch (err) {}

  const tenders = await fetchTenders();
  if (tenders.length > 0) {
    const found = tenders.find((t) => t.id === id || t.tender_number === id || id === 'TEN_01');
    return found || tenders[0];
  }
  return null;
}

export async function fetchBidders(): Promise<Bidder[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/bidders`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchSubmissions(): Promise<BidSubmission[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/submissions`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchAuditEvents(): Promise<AuditEvent[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/audit/events`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function verifyAuditChain(): Promise<AuditChainVerify | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/audit/verify-chain`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchDocumentStatus(documentId: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/documents/${documentId}/status`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchDocumentEvidence(documentId: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/documents/${documentId}/evidence`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchTenderRequirementCandidates(tenderId: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/tenders/${tenderId}/requirement-candidates`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchBidInconsistencyCandidates(submissionId: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/inconsistency-candidates`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

// ============================================================
// PHASE 5 API FUNCTIONS
// ============================================================

export async function fetchBidComplianceExplanation(submissionId: string): Promise<ComplianceExplanationResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/explanation`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchBidEvidenceTrace(submissionId: string): Promise<EvidenceTraceGraph | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/evidence-trace`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchBidRiskAssessment(submissionId: string): Promise<RiskAssessmentResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/risk-assessment`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchHumanReviewTasks(statusFilter?: string): Promise<HumanReviewTask[]> {
  try {
    const url = statusFilter ? `${API_BASE_URL}/human-reviews?status_filter=${statusFilter}` : `${API_BASE_URL}/human-reviews`;
    const res = await fetch(url, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function resolveHumanReviewTask(taskId: string, decision: string, summary: string): Promise<HumanReviewTask | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/human-reviews/${taskId}/resolve`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ decision, resolution_summary: summary }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function recordOfficerDecision(
  submissionId: string,
  decision: string,
  rationale: string,
  overrides?: any[]
): Promise<OfficerDecisionResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/officer-decisions`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ decision, rationale, overrides }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchBidManualOverrides(submissionId: string): Promise<ManualOverrideResponse[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/manual-overrides`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function approveManualOverride(overrideId: string, approved: boolean, comments?: string): Promise<ManualOverrideResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/manual-overrides/${overrideId}/approve`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ approved, comments }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchGovernmentSources(): Promise<GovernmentSource[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/government-sources`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchBidVerifications(submissionId: string): Promise<GovernmentVerificationRecord[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/verifications`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function triggerGovernmentVerification(submissionId: string, sourceCode: string, identifierValue?: string): Promise<GovernmentVerificationRecord | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/government-verifications`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ bid_submission_id: submissionId, source_code: sourceCode, identifier_value: identifierValue }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function recordManualVerification(submissionId: string, sourceCode: string, businessStatus: string, manualNotes: string): Promise<GovernmentVerificationRecord | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/government-verifications/manual`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        bid_submission_id: submissionId,
        source_code: sourceCode,
        business_status: businessStatus,
        manual_notes: manualNotes,
      }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchBidComplianceMatrix(submissionId: string): Promise<ComplianceMatrixResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/compliance-matrix`, { headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function evaluateBidCompliance(submissionId: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/evaluate-compliance`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function createManualOverride(
  submissionId: string,
  requirementId: string,
  previousStatus: string,
  newStatus: string,
  overrideReason: string
): Promise<ManualOverrideResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/bids/${submissionId}/manual-overrides`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        requirement_id: requirementId,
        previous_status: previousStatus,
        new_status: newStatus,
        override_reason: overrideReason,
        requires_four_eyes: true,
      }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

