'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Shield, UserCheck, KeyRound } from 'lucide-react';
import { loginDemo } from '../../lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState('ProcurementOfficer');
  const [loading, setLoading] = useState(false);

  const roleAccounts = [
    {
      role: 'ProcurementOfficer',
      email: 'officer@cpcl.gov.in',
      name: 'Rajesh Kumar',
      desc: 'Create tenders, review submissions, issue qualification decisions.',
    },
    {
      role: 'SeniorReviewer',
      email: 'senior@cpcl.gov.in',
      name: 'Anita Sharma',
      desc: 'Review high-value compliance evaluations and authorize overrides.',
    },
    {
      role: 'Auditor',
      email: 'auditor@cpcl.gov.in',
      name: 'Vikram Patel',
      desc: 'Verify tamper-evident audit hash chain and review decision lineage.',
    },
    {
      role: 'SystemAdmin',
      email: 'admin@cpcl.gov.in',
      name: 'System Administrator',
      desc: 'Manage policy versions, system parameters, and integrations.',
    },
  ];

  const handleLogin = async (email: string, role: string) => {
    setLoading(true);
    await loginDemo(email, role);
    setLoading(false);
    router.push('/dashboard');
  };

  return (
    <div className="max-w-3xl mx-auto py-10">
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6 space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gov-light text-gov-blue rounded-md">
              <KeyRound className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">
                Development / Demo Authentication Portal
              </h2>
              <p className="text-xs text-slate-500">
                Backend-Authoritative RBAC Role Selector (SIH Submission MVP Baseline)
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {roleAccounts.map((acc) => (
            <div
              key={acc.role}
              onClick={() => handleLogin(acc.email, acc.role)}
              className="border border-slate-200 hover:border-gov-blue rounded-lg p-4 cursor-pointer transition-all hover:shadow-md bg-slate-50 hover:bg-white"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">{acc.name}</h3>
                  <p className="text-xs text-slate-500 font-mono">{acc.email}</p>
                </div>
                <span className="text-[10px] bg-slate-200 font-mono text-slate-700 px-2 py-0.5 rounded">
                  {acc.role}
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-3 leading-snug">{acc.desc}</p>
              <button
                disabled={loading}
                className="mt-4 w-full bg-navy-900 hover:bg-gov-blue text-white text-xs font-semibold py-2 px-3 rounded flex items-center justify-center space-x-2 transition-colors"
              >
                <UserCheck className="w-3.5 h-3.5" />
                <span>Authenticate as {acc.role}</span>
              </button>
            </div>
          ))}
        </div>

        <div className="bg-slate-50 p-4 rounded border border-slate-200 text-xs text-slate-600">
          <div className="font-semibold text-slate-800 flex items-center gap-1.5 mb-1">
            <Shield className="w-4 h-4 text-gov-blue" />
            Security Notice
          </div>
          <p>
            Authentication in this prototype is isolated behind an IdP abstraction layer. All role permissions are strictly authorized by backend middleware. Frontend controls are presentation-only.
          </p>
        </div>
      </div>
    </div>
  );
}
