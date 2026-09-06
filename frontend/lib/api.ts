import { Tender, Bidder, BidSubmission, AuditEvent, AuditChainVerify, User } from '../types';

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
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
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
