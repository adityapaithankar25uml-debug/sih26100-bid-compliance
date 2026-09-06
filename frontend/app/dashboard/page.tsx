'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { FileText, FolderCheck, Users, Lock, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, UserCheck, ShieldAlert, FileSearch } from 'lucide-react';
import { fetchTenders, fetchSubmissions, fetchBidders, verifyAuditChain, fetchHumanReviewTasks } from '../../lib/api';
import { Tender, BidSubmission, Bidder, AuditChainVerify, HumanReviewTask } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export default function DashboardPage() {
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [submissions, setSubmissions] = useState<BidSubmission[]>([]);
  const [bidders, setBidders] = useState<Bidder[]>([]);
  const [reviewTasks, setReviewTasks] = useState<HumanReviewTask[]>([]);
  const [auditChain, setAuditChain] = useState<AuditChainVerify | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const [tList, sList, bList, rList, aStatus] = await Promise.all([
        fetchTenders(),
        fetchSubmissions(),
        fetchBidders(),
        fetchHumanReviewTasks(),
        verifyAuditChain(),
      ]);
      setTenders(tList);
      setSubmissions(sList);
      setBidders(bList);
      setReviewTasks(rList);
      setAuditChain(aStatus);
      setLoading(false);
    }
    loadData();
  }, []);

  const pendingReviews = reviewTasks.filter((t) => t.status !== 'RESOLVED' && t.status !== 'REJECTED');

  return (
    <div className="space-y-6">
      {/* Top Title Banner */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-gov-blue" />
            Procurement Compliance Verification Command Center
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Ministry of Petroleum & Natural Gas / CPCL Integrated Bid Compliance Verification Platform
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/bids"
            className="bg-gov-blue hover:bg-blue-900 text-white px-3.5 py-2 rounded text-xs font-bold transition shadow-sm"
          >
            Review Active Bids
          </Link>
          <Link
            href="/human-review"
            className="bg-amber-600 hover:bg-amber-700 text-white px-3.5 py-2 rounded text-xs font-bold transition shadow-sm flex items-center gap-1.5"
          >
            <UserCheck className="w-3.5 h-3.5" />
            Pending Reviews ({pendingReviews.length})
          </Link>
        </div>
      </div>

      {/* System Axiom Banner */}
      <div className="bg-navy-900 text-white p-4 rounded-lg shadow-sm border border-navy-800 flex items-center justify-between">
        <div className="space-y-1">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider font-mono">
            Core System Principle
          </div>
          <div className="text-xs md:text-sm font-medium flex flex-wrap items-center gap-1.5 text-slate-200">
            <span className="text-gov-accent font-bold">AI INTERPRETS</span>
            <span>→</span>
            <span className="text-emerald-400 font-bold">SOURCES VERIFY</span>
            <span>→</span>
            <span className="font-bold">RULES EVALUATE</span>
            <span>→</span>
            <span className="text-amber-400 font-bold">EVIDENCE PROVES</span>
            <span>→</span>
            <span className="text-rose-300 font-bold">RISK PRIORITIZES</span>
            <span>→</span>
            <span className="text-white font-bold underline decoration-gov-accent underline-offset-4">HUMAN DECIDES</span>
            <span>→</span>
            <span className="text-slate-300 font-bold">AUDIT REMEMBERS</span>
          </div>
        </div>
        <div className="text-xs text-slate-400 max-w-xs text-right hidden xl:block">
          AI extractions are advisory. Statutory procurement decisions rest exclusively with authorized officers.
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Active Tenders</span>
            <FileText className="w-5 h-5 text-gov-blue" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            {loading ? '...' : tenders.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Cataloged Procurement Specs</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Bid Submissions</span>
            <FolderCheck className="w-5 h-5 text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            {loading ? '...' : submissions.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Under Active Verification</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Pending Officer Tasks</span>
            <UserCheck className="w-5 h-5 text-amber-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            {loading ? '...' : pendingReviews.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Human Review Queue Items</div>
        </div>

        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Audit Chain Integrity</span>
            <Lock className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2 flex items-center gap-2">
            {loading ? '...' : auditChain?.total_blocks || 0}
            {auditChain?.is_valid ? (
              <span className="text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-bold flex items-center gap-1 border border-emerald-200">
                <CheckCircle2 className="w-3 h-3" /> Intact Chain
              </span>
            ) : (
              <span className="text-[10px] text-rose-700 bg-rose-50 px-2 py-0.5 rounded font-bold flex items-center gap-1 border border-rose-200">
                <AlertTriangle className="w-3 h-3" /> Integrity Check Failed
              </span>
            )}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Tamper-Evident SHA-256 Blocks</div>
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
              className="text-xs font-bold text-gov-blue hover:underline flex items-center gap-1"
            >
              View Catalog <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {tenders.length === 0 ? (
            <div className="text-center py-8 text-slate-400 text-xs">
              No active tenders found.
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
                          className="text-gov-blue hover:underline font-bold"
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

        {/* Submissions & Pending Reviews Sidebar */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <FolderCheck className="w-4 h-4 text-emerald-600" />
                Active Bid Submissions
              </h3>
              <Link
                href="/bids"
                className="text-xs font-bold text-gov-blue hover:underline flex items-center gap-1"
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
                      <Link href={`/bids/${sub.id}`} className="text-gov-blue font-bold hover:underline">
                        Review Workspace →
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

