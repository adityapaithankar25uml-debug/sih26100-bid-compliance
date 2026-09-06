'use client';
import React, { useState } from 'react';
import { UserCheck, ShieldCheck, AlertCircle, FileCheck, Send } from 'lucide-react';

interface OfficerDecisionDialogProps {
  submissionId: string;
  onSubmitDecision: (decision: string, rationale: string) => Promise<void>;
}

export function OfficerDecisionDialog({ submissionId, onSubmitDecision }: OfficerDecisionDialogProps) {
  const [decision, setDecision] = useState('QUALIFIED');
  const [rationale, setRationale] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submittedDecision, setSubmittedDecision] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rationale.trim()) return;
    setIsSubmitting(true);
    await onSubmitDecision(decision, rationale);
    setSubmittedDecision(decision);
    setIsSubmitting(false);
  };

  if (submittedDecision) {
    return (
      <div className="bg-emerald-50 border border-emerald-300 p-5 rounded-lg text-emerald-900 space-y-2">
        <h4 className="font-bold text-sm flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-700" />
          Official Procurement Officer Decision Recorded & Point-in-Time Snapshot Stored
        </h4>
        <p className="text-xs">
          Decision: <span className="font-bold font-mono text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">{submittedDecision}</span>
        </p>
        <p className="text-xs text-slate-700">Rationale: {rationale}</p>
        <p className="text-[11px] text-emerald-700 font-mono">
          Domain event appended to Tamper-Evident SHA-256 Audit Hash Chain.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-gov-blue" />
          Human Procurement Officer Final Qualification Decision
        </h3>
        <span className="text-[10px] font-bold uppercase bg-amber-100 text-amber-800 px-2 py-0.5 rounded border border-amber-300">
          Sole Decision Authority
        </span>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 text-xs">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block font-bold text-slate-700">Final Qualification Outcome</label>
            <select
              value={decision}
              onChange={(e) => setDecision(e.target.value)}
              className="w-full mt-1 p-2 bg-slate-50 border border-slate-200 rounded font-bold text-slate-900 text-xs"
            >
              <option value="QUALIFIED">QUALIFIED — Bidder Satisfies All Procurement Criteria</option>
              <option value="DISQUALIFIED">DISQUALIFIED — Mandatory Requirement Criteria Unmet</option>
              <option value="REQUIRES_CLARIFICATION">REQUIRES CLARIFICATION — Issue Form 7 Clarification Request</option>
              <option value="EVIDENCE_REQUESTED">EVIDENCE REQUESTED — Request Additional Documents</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block font-bold text-slate-700">Officer Decision Rationale & Justification</label>
          <textarea
            value={rationale}
            onChange={(e) => setRationale(e.target.value)}
            rows={3}
            required
            placeholder="Enter authoritative procurement officer justification for audit record..."
            className="w-full mt-1 p-2 bg-slate-50 border border-slate-200 rounded text-slate-900 text-xs"
          />
        </div>

        <button
          type="submit"
          disabled={isSubmitting || !rationale.trim()}
          className="bg-gov-blue text-white font-bold px-5 py-2 rounded hover:bg-blue-900 flex items-center gap-2 text-xs disabled:opacity-50"
        >
          <Send className="w-3.5 h-3.5" />
          {isSubmitting ? 'Recording Decision...' : 'Record Officer Qualification Decision'}
        </button>
      </form>
    </div>
  );
}
