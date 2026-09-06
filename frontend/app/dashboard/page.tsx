'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { FileText, FolderCheck, Users, Lock, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';
import { fetchTenders, fetchSubmissions, fetchBidders, verifyAuditChain } from '../../lib/api';
import { Tender, BidSubmission, Bidder, AuditChainVerify } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export default function DashboardPage() {
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [submissions, setSubmissions] = useState<BidSubmission[]>([]);
  const [bidders, setBidders] = useState<Bidder[]>([]);
  const [auditChain, setAuditChain] = useState<AuditChainVerify | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const [tList, sList, bList, aStatus] = await Promise.all([
        fetchTenders(),
        fetchSubmissions(),
        fetchBidders(),
        verifyAuditChain(),
      ]);
      setTenders(tList);
      setSubmissions(sList);
      setBidders(bList);
      setAuditChain(aStatus);
      setLoading(false);
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Title Banner */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">
            Procurement Compliance Verification Workspace
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Ministry of Petroleum & Natural Gas / CPCL GeM Integrated Verification Platform
          </p>
        </div>
        <div className="bg-slate-100 px-3 py-1.5 rounded border border-slate-200 text-xs text-slate-700 font-mono">
          Phase 2 Foundation MVP
        </div>
      </div>

      {/* Axiom Banner */}
      <div className="bg-navy-900 text-white p-4 rounded-lg shadow-sm border border-navy-800 flex items-center justify-between">
        <div className="space-y-1">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Core Architectural Axiom
          </div>
          <div className="text-sm font-medium flex items-center space-x-2 text-slate-200">
            <span className="text-gov-blue font-bold">AI INTERPRETS</span>
            <span>→</span>
            <span className="text-emerald-400 font-bold">AUTHORIZED SOURCES VERIFY</span>
            <span>→</span>
            <span className="font-bold">RULES EVALUATE</span>
            <span>→</span>
            <span className="text-amber-400 font-bold">EVIDENCE PROVES</span>
            <span>→</span>
            <span className="text-white font-bold underline decoration-gov-blue underline-offset-4">HUMAN APPROVES</span>
          </div>
        </div>
        <div className="text-xs text-slate-400 max-w-xs text-right hidden lg:block">
          AI is non-authoritative. Final procurement decisions belong exclusively to authorized human officers.
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-medium uppercase tracking-wider">Active Tenders</span>
            <FileText className="w-5 h-5 text-gov-blue" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">
            {loading ? '...' : tenders.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Cataloged In Procurement Registry</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-medium uppercase tracking-wider">Bid Submissions</span>
            <FolderCheck className="w-5 h-5 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">
            {loading ? '...' : submissions.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Under Compliance Evaluation</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-medium uppercase tracking-wider">Registered Bidders</span>
            <Users className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">
            {loading ? '...' : bidders.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Verified Entity Identifiers</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-medium uppercase tracking-wider">Audit Hash Chain</span>
            <Lock className="w-5 h-5 text-amber-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2 flex items-center gap-2">
            {loading ? '...' : auditChain?.total_blocks || 0}
            {auditChain?.is_valid ? (
              <span className="text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded font-normal flex items-center gap-1 border border-emerald-200">
                <CheckCircle2 className="w-3 h-3" /> Intact
              </span>
            ) : (
              <span className="text-xs text-rose-600 bg-rose-50 px-2 py-0.5 rounded font-normal flex items-center gap-1 border border-rose-200">
                <AlertTriangle className="w-3 h-3" /> Tampered
              </span>
            )}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Tamper-Evident Blocks</div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tenders Table */}
        <div className="lg:col-span-2 bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <FileText className="w-4 h-4 text-gov-blue" />
              Active Procurement Tenders
            </h3>
            <Link
              href="/tenders"
              className="text-xs font-semibold text-gov-blue hover:underline flex items-center gap-1"
            >
              View Catalog <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {tenders.length === 0 ? (
            <div className="text-center py-8 text-slate-400 text-xs">
              No active tenders found. Run seed script or create a new tender.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                    <th className="py-2.5 px-3">Tender Ref</th>
                    <th className="py-2.5 px-3">Title</th>
                    <th className="py-2.5 px-3">Versions</th>
                    <th className="py-2.5 px-3">Status</th>
                    <th className="py-2.5 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {tenders.map((t) => (
                    <tr key={t.id} className="hover:bg-slate-50">
                      <td className="py-3 px-3 font-mono font-semibold text-slate-900">
                        {t.tender_number}
                      </td>
                      <td className="py-3 px-3 text-slate-700 max-w-xs truncate">{t.title}</td>
                      <td className="py-3 px-3 font-mono text-slate-600">
                        v{t.versions?.length || 1}
                      </td>
                      <td className="py-3 px-3">
                        <StatusBadge status={t.status} />
                      </td>
                      <td className="py-3 px-3 text-right">
                        <Link
                          href={`/tenders/${t.id}`}
                          className="text-gov-blue hover:underline font-semibold"
                        >
                          Workspace →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Submissions Sidebar */}
        <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <FolderCheck className="w-4 h-4 text-emerald-600" />
              Recent Submissions
            </h3>
            <Link
              href="/bids"
              className="text-xs font-semibold text-gov-blue hover:underline flex items-center gap-1"
            >
              All Bids <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {submissions.length === 0 ? (
            <div className="text-center py-8 text-slate-400 text-xs">
              No bid submissions logged yet.
            </div>
          ) : (
            <div className="space-y-3">
              {submissions.map((sub) => (
                <div
                  key={sub.id}
                  className="p-3 bg-slate-50 rounded border border-slate-200 hover:border-gov-blue transition-colors space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-slate-900">
                      {sub.submission_reference}
                    </span>
                    <StatusBadge status={sub.status} />
                  </div>
                  <div className="text-[11px] text-slate-500 flex justify-between">
                    <span>Date: {new Date(sub.submission_date).toLocaleDateString()}</span>
                    <Link href={`/bids/${sub.id}`} className="text-gov-blue font-semibold hover:underline">
                      Review Bid
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
