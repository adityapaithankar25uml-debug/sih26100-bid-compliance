'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Shield, UserCheck, KeyRound, Lock, Info } from 'lucide-react';
import { loginDemo } from '../../lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const roleAccounts = [
    {
      role: 'ProcurementOfficer',
      email: 'officer@cpcl.gov.in',
      name: 'Rajesh Kumar',
      title: 'Procurement Officer',
      desc: 'Create tenders, evaluate bids, resolve review items, issue final decisions.',
    },
    {
      role: 'SeniorReviewer',
      email: 'senior@cpcl.gov.in',
      name: 'Anita Sharma',
      title: 'Senior Reviewer',
      desc: 'Review high-value compliance evaluations and authorize four-eyes overrides.',
    },
    {
      role: 'ComplianceOfficer',
      email: 'compliance@cpcl.gov.in',
      name: 'Dr. S. Ranganathan',
      title: 'Compliance Officer',
      desc: 'Oversee rule mapping, policy versioning, and compliance matrix verification.',
    },
    {
      role: 'Auditor',
      email: 'auditor@cpcl.gov.in',
      name: 'Vikram Patel',
      title: 'Auditor',
      desc: 'Verify Tamper-Evident SHA-256 Audit Hash Chain and decision provenance.',
    },
    {
      role: 'Bidder',
      email: 'bidder@abcengineering.com',
      name: 'ABC Engineering Representative',
      title: 'Bidder User',
      desc: 'Submit bid documents, track verification status, respond to clarifications.',
    },
    {
      role: 'SystemAdmin',
      email: 'admin@cpcl.gov.in',
      name: 'System Administrator',
      title: 'System Admin',
      desc: 'Configure government adapters, security parameters, and system registries.',
    },
  ];

  const handleLogin = async (email: string, role: string) => {
    setLoading(true);
    await loginDemo(email, role);
    setLoading(false);
    router.push('/dashboard');
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-6">
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6 space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-gov-blue text-white rounded-md shadow-sm">
              <KeyRound className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Government Procurement Demo Identity Authentication Portal
              </h2>
              <p className="text-xs text-slate-500">
                Backend-Authoritative RBAC Seeded Demo User Authenticator (SIH 2026 Submission)
              </p>
            </div>
          </div>
        </div>

        <div className="p-3.5 bg-amber-50 border border-amber-200 rounded text-xs text-amber-900 flex items-start gap-2">
          <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
          <div>
            <strong className="block font-bold">MANDATORY RBAC CONTROL NOTICE:</strong>
            Frontend role-switching dropdowns are strictly prohibited. Selecting a demo account authenticates directly via the backend API (`/api/v1/auth/login`) to receive a cryptographically signed backend JWT token with explicit backend-authoritative scopes.
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {roleAccounts.map((acc) => (
            <div
              key={acc.role}
              onClick={() => handleLogin(acc.email, acc.role)}
              className="border border-slate-200 hover:border-gov-blue rounded-lg p-4 cursor-pointer transition-all hover:shadow-md bg-slate-50 hover:bg-white flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-bold text-slate-900 text-sm">{acc.name}</h3>
                    <span className="text-[11px] text-gov-blue font-medium">{acc.title}</span>
                  </div>
                  <span className="text-[10px] bg-slate-200 font-mono text-slate-700 px-1.5 py-0.5 rounded font-semibold">
                    {acc.role}
                  </span>
                </div>
                <p className="text-xs text-slate-500 font-mono mt-1">{acc.email}</p>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">{acc.desc}</p>
              </div>

              <button
                disabled={loading}
                className="mt-4 w-full bg-navy-900 hover:bg-gov-blue text-white text-xs font-bold py-2 px-3 rounded flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
              >
                <UserCheck className="w-3.5 h-3.5" />
                <span>Authenticate as {acc.role}</span>
              </button>
            </div>
          ))}
        </div>

        <div className="bg-slate-50 p-4 rounded border border-slate-200 text-xs text-slate-600 space-y-1">
          <div className="font-semibold text-slate-800 flex items-center gap-1.5">
            <Shield className="w-4 h-4 text-gov-blue" />
            Backend Authorization & Audit Traceability
          </div>
          <p className="text-slate-500 text-[11px]">
            Every authenticated action generates a correlation ID (`X-Correlation-ID`) and records an immutable event entry into the <strong>Tamper-Evident SHA-256 Audit Hash Chain</strong>. Un-authenticated or unauthorized actions are immediately denied by backend security guards.
          </p>
        </div>
      </div>
    </div>
  );
}

