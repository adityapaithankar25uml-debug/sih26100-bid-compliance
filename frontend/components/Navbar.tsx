'use client';
import React, { useEffect, useState } from 'react';
import { ShieldCheck, UserCheck, Activity } from 'lucide-react';
import { fetchHealth } from '../lib/api';

export const Navbar: React.FC = () => {
  const [userRole, setUserRole] = useState<string>('ProcurementOfficer');
  const [userName, setUserName] = useState<string>('Rajesh Kumar (Demo)');
  const [sysStatus, setSysStatus] = useState<string>('Healthy');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('user');
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          if (parsed.role) setUserRole(parsed.role);
          if (parsed.full_name) setUserName(parsed.full_name);
        } catch (e) {}
      }
    }

    fetchHealth().then((res) => {
      if (res.status === 'healthy') {
        setSysStatus('Operational');
      } else {
        setSysStatus('Degraded');
      }
    });
  }, []);

  return (
    <header className="bg-navy-900 text-white border-b border-navy-800 px-6 py-3 flex items-center justify-between shadow-sm">
      <div className="flex items-center space-x-3">
        <div className="bg-gov-blue text-white p-2 rounded">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-2">
            SIH26100 — GeM Procurement Compliance Platform
            <span className="text-[10px] bg-navy-800 text-slate-300 px-2 py-0.5 rounded font-mono border border-navy-700">
              CPCL / MoPNG
            </span>
          </h1>
          <p className="text-xs text-slate-400">
            AI-Assisted Integrated Compliance & Audit Verification System
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2 text-xs bg-navy-800 px-3 py-1.5 rounded border border-navy-700">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-300">Backend System:</span>
          <span className="font-semibold text-emerald-400">{sysStatus}</span>
        </div>

        <div className="flex items-center space-x-2 text-xs border-l border-navy-700 pl-6">
          <UserCheck className="w-4 h-4 text-gov-blue" />
          <div className="text-right">
            <div className="font-semibold text-slate-200">{userName}</div>
            <div className="text-[11px] text-slate-400 font-mono">{userRole}</div>
          </div>
        </div>
      </div>
    </header>
  );
};
