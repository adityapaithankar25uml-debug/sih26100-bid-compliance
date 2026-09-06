'use client';
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { FolderCheck, ArrowLeft, Shield, CheckCircle, FileCheck } from 'lucide-react';
import { fetchSubmissions } from '../../../lib/api';
import { BidSubmission } from '../../../types';
import { StatusBadge } from '../../../components/StatusBadge';

export default function BidDetailPage() {
  const params = useParams();
  const subId = params?.id as string;
  const [submission, setSubmission] = useState<BidSubmission | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (subId) {
      fetchSubmissions().then((list) => {
        const found = list.find((s) => s.id === subId);
        setSubmission(found || null);
        setLoading(false);
      });
    }
  }, [subId]);

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-400">Loading bid submission...</div>;
  }

  if (!submission) {
    return (
      <div className="p-8 text-center text-xs text-slate-500">
        Submission not found. <Link href="/bids" className="text-gov-blue underline">Back to registry</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link href="/bids" className="text-xs font-semibold text-gov-blue hover:underline flex items-center gap-1">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Submissions Registry
      </Link>

      {/* Proposal Summary Card */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <span className="font-mono text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              {submission.submission_reference}
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-2">
              Bid Submission Review Workspace
            </h2>
          </div>
          <StatusBadge status={submission.status} />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-3 border-t border-slate-100 text-xs">
          <div>
            <span className="text-slate-500 block">Bidder Identifier</span>
            <span className="font-mono font-semibold text-slate-800">{submission.bidder_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Bound Tender ID</span>
            <span className="font-mono font-semibold text-slate-800">{submission.tender_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Tender Version</span>
            <span className="font-mono font-semibold text-slate-800">{submission.tender_version_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Submission Date</span>
            <span className="font-semibold text-slate-800">
              {new Date(submission.submission_date).toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Document Covers Card */}
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-3">
            <FileCheck className="w-4 h-4 text-gov-blue" />
            Registered Document Covers
          </h3>

          <div className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold">
              <span className="text-slate-900">TECHNICAL & EXPERIMENTAL COVER</span>
              <span className="bg-blue-100 text-blue-800 text-[10px] px-2 py-0.5 rounded">REGISTERED</span>
            </div>
            <p className="text-xs text-slate-600">
              Contains technical proposals, experience certificates, and ISO quality documentation.
            </p>
          </div>
        </div>

        {/* Verification Status Card */}
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-3">
            <Shield className="w-4 h-4 text-emerald-600" />
            Compliance Status Framework
          </h3>

          <div className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">Evaluation Phase:</span>
              <span className="font-mono text-gov-blue font-bold">FOUNDATION PERSISTENCE</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              In Phase 2, submission persistence and domain relationships are established. Deterministic compliance rule evaluation runs in later pipeline phases.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
