'use client';
import React, { useEffect, useState } from 'react';
import { ShieldCheck, RefreshCw, AlertCircle, CheckCircle, Info, ExternalLink } from 'lucide-react';
import { fetchGovernmentSources } from '../../lib/api';
import { GovernmentSource } from '../../types';

export default function VerificationCenterPage() {
  const [sources, setSources] = useState<GovernmentSource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSources() {
      setLoading(true);
      const data = await fetchGovernmentSources();
      setSources(data);
      setLoading(false);
    }
    loadSources();
  }, []);

  const domains = [
    { code: 'GST', name: 'GSTIN / GST Portal Registry', desc: 'Active registration, return filing status, and turnover bracket verification.' },
    { code: 'UDYAM', name: 'Udyam / MSME Certificate Registry', desc: 'Micro, Small & Medium Enterprise classification and registration validity.' },
    { code: 'PAN', name: 'Income Tax PAN Database', desc: 'Taxpayer identity verification, entity name matching, and PAN status.' },
    { code: 'MCA', name: 'Ministry of Corporate Affairs (CIN/DIN)', desc: 'Corporate identity number, active company status, and director identification.' },
    { code: 'EPFO', name: 'Employees Provident Fund Organisation', desc: 'EPF establishment code registration, active remittance status, and headcount.' },
    { code: 'ESIC', name: 'Employees State Insurance Corporation', desc: 'ESIC establishment code and monthly contribution compliance.' },
    { code: 'STARTUP_INDIA', name: 'DPIIT Startup India Portal', desc: 'DPIIT recognition number, tax exemption status, and eligibility.' },
    { code: 'NSIC', name: 'National Small Industries Corporation', desc: 'Single point registration scheme and competency certificate verification.' },
    { code: 'OEM_AUTH', name: 'Original Equipment Manufacturer Registry', desc: 'MAAF / OEM authorization code, validity period, and product mapping.' },
    { code: 'DIGILOCKER', name: 'DigiLocker Verification Gateway', desc: 'Consent-based document retrieval and digital credential verification.' },
    { code: 'DEBARMENT', name: 'GeM / Central Procurement Debarment List', desc: 'Check blacklisting, debarment, and holiday-listing status.' },
    { code: 'GEM_PROFILE', name: 'GeM Seller Profile & Rating', desc: 'Vendor assessment score, incident history, and seller category.' },
  ];

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="w-5.5 h-5.5 text-gov-blue" />
            Government Verification Center
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Authoritative Government Gateway Adapter Registry & Integration Status
          </p>
        </div>
        <div className="bg-orange-50 text-orange-900 px-3 py-1.5 rounded border border-orange-200 text-xs font-bold font-mono flex items-center gap-1.5">
          <Info className="w-4 h-4 text-orange-700" />
          INTEGRATION MODE: MOCK / DEMO
        </div>
      </div>

      {/* Integration Notice */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-900 space-y-1.5">
        <strong className="font-bold flex items-center gap-1.5 text-sm">
          <Info className="w-4 h-4 text-blue-700" />
          AUTHORITATIVE SOURCE VERIFICATION PRINCIPLE
        </strong>
        <p className="text-slate-700 text-[11px] leading-relaxed">
          The platform integrates with official government registries to verify bidder identity, financial standing, statutory compliance, and debarment status. In accordance with strict audit safeguards, <strong>mock adapters explicitly state their demo integration mode</strong>. Technical transport failures or API timeouts never result in an automatic qualification failure; instead, they trigger human review and manual verification fallback workflows.
        </p>
      </div>

      {/* Registry Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {domains.map((dom) => {
          const registered = sources.find((s) => s.source_code === dom.code || s.name.toUpperCase().includes(dom.code));
          const mode = registered?.integration_mode || 'MOCK';
          return (
            <div
              key={dom.code}
              className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex flex-col justify-between space-y-3 hover:border-gov-blue transition"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <span className="font-mono font-bold text-xs bg-slate-100 text-slate-800 px-2 py-0.5 rounded border border-slate-200">
                    {dom.code}
                  </span>
                  <span className="bg-orange-50 text-orange-800 border border-orange-300 px-2 py-0.5 rounded font-mono text-[10px] font-bold">
                    {mode} MODE
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-sm mt-2">{dom.name}</h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">{dom.desc}</p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-emerald-700 font-semibold flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600" /> Adapter Ready
                </span>
                <span className="text-slate-400 text-[10px] font-mono">Sandbox Endpoint</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
