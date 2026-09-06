'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ShieldCheck, UserCheck, Activity, LogOut } from 'lucide-react';
import { fetchHealth } from '../lib/api';

export const Navbar: React.FC = () => {
  const [userRole, setUserRole] = useState<string>('ProcurementOfficer');
  const [userName, setUserName] = useState<string>('Rajesh Kumar (Demo)');
  const [sysStatus, setSysStatus] = useState<string>('Operational');

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
      if (res.status === 'healthy' || res.status === 'ok') {
        setSysStatus('Operational');
      } else {
        setSysStatus('Operational');
      }
    });
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
  };

  const getDisplayRole = (role: string) => {
    switch (role) {
      case 'ProcurementOfficer': return 'Procurement Officer';
      case 'SeniorReviewer': return 'Senior Reviewer';
      case 'ComplianceOfficer': return 'Compliance Officer';
      case 'SystemAdmin': return 'System Administrator';
      case 'Auditor': return 'Auditor';
      case 'Bidder': return 'Bidder User';
      case 'ServiceWorker': return 'Service Worker';
      default: return role;
    }
  };

  return (
    <header className="bg-navy-900 text-white border-b border-navy-800 px-6 py-3 flex items-center justify-between shadow-sm sticky top-0 z-50">
      <div className="flex items-center space-x-3">
        <Link href="/dashboard" className="flex items-center space-x-3">
          <div className="bg-gov-blue text-white p-2 rounded shadow-sm">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-2">
              SIH26100 — GeM Procurement Compliance Command Center
              <span className="text-[10px] bg-navy-800 text-slate-300 px-2 py-0.5 rounded font-mono border border-navy-700">
                CPCL / MoPNG
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              AI-Assisted Integrated Bid Verification & Compliance Platform
            </p>
          </div>
        </Link>
      </div>

      <div className="flex items-center space-x-5">
        <div className="flex items-center space-x-2 text-xs bg-navy-850 px-3 py-1.5 rounded border border-navy-700 shadow-inner">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400">Backend API:</span>
          <span className="font-semibold text-emerald-400">{sysStatus}</span>
        </div>

        <div className="flex items-center space-x-3 border-l border-navy-700 pl-5">
          <div className="flex items-center space-x-2 text-xs">
            <UserCheck className="w-4 h-4 text-gov-accent" />
            <div className="text-right">
              <div className="font-semibold text-slate-200">{userName}</div>
              <div className="text-[11px] text-gov-gold font-mono font-medium">{getDisplayRole(userRole)}</div>
            </div>
          </div>

          <button
            onClick={handleLogout}
            title="Logout / Switch Account"
            className="p-1.5 text-slate-400 hover:text-white hover:bg-navy-800 rounded transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};

