'use client';
import React, { useEffect, useState } from 'react';
import { Lock, ShieldCheck, RefreshCw, CheckCircle2, AlertOctagon } from 'lucide-react';
import { fetchAuditEvents, verifyAuditChain } from '../../lib/api';
import { AuditEvent, AuditChainVerify } from '../../types';

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [chainStatus, setChainStatus] = useState<AuditChainVerify | null>(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    const [eList, verifyRes] = await Promise.all([
      fetchAuditEvents(),
      verifyAuditChain(),
    ]);
    setEvents(eList);
    setChainStatus(verifyRes);
    setLoading(false);
  }

  async function handleVerify() {
    setVerifying(true);
    const res = await verifyAuditChain();
    setChainStatus(res);
    setVerifying(false);
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Lock className="w-5 h-5 text-amber-600" />
            Tamper-Evident Audit Hash Chain
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            SHA-256 canonical event lineage providing tamper-evident historical auditability
          </p>
        </div>
        <button
          onClick={handleVerify}
          disabled={verifying}
          className="bg-navy-900 hover:bg-gov-blue text-white text-xs font-semibold py-2 px-4 rounded flex items-center space-x-2 transition-colors shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${verifying ? 'animate-spin' : ''}`} />
          <span>{verifying ? 'Verifying Chain...' : 'Re-Verify Chain Integrity'}</span>
        </button>
      </div>

      {/* Chain Status Card */}
      {chainStatus && (
        <div
          className={`p-4 rounded-lg border flex items-center justify-between ${
            chainStatus.is_valid
              ? 'bg-emerald-50 border-emerald-300 text-emerald-900'
              : 'bg-rose-50 border-rose-300 text-rose-900'
          }`}
        >
          <div className="flex items-center space-x-3">
            {chainStatus.is_valid ? (
              <CheckCircle2 className="w-6 h-6 text-emerald-600 flex-shrink-0" />
            ) : (
              <AlertOctagon className="w-6 h-6 text-rose-600 flex-shrink-0" />
            )}
            <div>
              <h3 className="font-bold text-sm">
                {chainStatus.is_valid
                  ? 'Audit Hash Chain Verified Intact'
                  : 'TAMPER WARNING: Hash Chain Inconsistency Detected!'}
              </h3>
              <p className="text-xs mt-0.5 opacity-90">{chainStatus.message}</p>
            </div>
          </div>
          <div className="text-right text-xs font-mono font-semibold">
            <div>Verified Blocks: {chainStatus.verified_blocks} / {chainStatus.total_blocks}</div>
          </div>
        </div>
      )}

      {/* Events Table */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-xs uppercase tracking-wider">
            Canonical Audit Events Log ({events.length})
          </h3>
          <span className="text-[11px] text-slate-500 font-mono">
            SHA-256 Hashed Event Lineage
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-400">Verifying audit log...</div>
        ) : events.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">
            No audit events recorded yet. Perform domain actions to generate audit logs.
          </div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 border-b border-slate-200 text-slate-600 font-semibold">
                <th className="py-2.5 px-3">Timestamp</th>
                <th className="py-2.5 px-3">Actor / Role</th>
                <th className="py-2.5 px-3">Action</th>
                <th className="py-2.5 px-3">Resource</th>
                <th className="py-2.5 px-3">Correlation ID</th>
                <th className="py-2.5 px-3">Payload SHA-256</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {events.map((evt) => (
                <tr key={evt.id} className="hover:bg-slate-50">
                  <td className="py-3 px-3 text-slate-600 text-[11px]">
                    {new Date(evt.created_at).toLocaleString()}
                  </td>
                  <td className="py-3 px-3 text-slate-800">
                    <div className="font-bold">{evt.actor_role}</div>
                    <div className="text-[10px] text-slate-500">{evt.actor_id.substring(0, 10)}...</div>
                  </td>
                  <td className="py-3 px-3">
                    <span className="bg-slate-200 text-slate-800 px-2 py-0.5 rounded font-bold text-[10px]">
                      {evt.action}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-700">
                    {evt.resource_type}: {evt.resource_id.substring(0, 8)}...
                  </td>
                  <td className="py-3 px-3 text-slate-500 text-[11px]">
                    {evt.correlation_id}
                  </td>
                  <td className="py-3 px-3 text-gov-blue text-[11px] truncate max-w-[120px]">
                    {evt.payload_hash}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
