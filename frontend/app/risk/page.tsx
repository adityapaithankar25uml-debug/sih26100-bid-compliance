'use client';
import React, { useEffect, useState } from 'react';
import { ShieldAlert, Info, FolderCheck, AlertTriangle, AlertOctagon } from 'lucide-react';
import { fetchSubmissions, fetchBidRiskAssessment } from '../../lib/api';
import { BidSubmission, RiskAssessmentResponse } from '../../types';
import { RiskAssessmentPanel } from '../../components/RiskAssessmentPanel';

export default function RiskPage() {
  const [submissions, setSubmissions] = useState<BidSubmission[]>([]);
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<string>('');
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessmentResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSubmissions() {
      setLoading(true);
      const sList = await fetchSubmissions();
      setSubmissions(sList);
      if (sList.length > 0) {
        setSelectedSubmissionId(sList[0].id);
      } else {
        setLoading(false);
      }
    }
    loadSubmissions();
  }, []);

  useEffect(() => {
    if (!selectedSubmissionId) return;
    async function loadRisk() {
      setLoading(true);
      const riskData = await fetchBidRiskAssessment(selectedSubmissionId);
      setRiskAssessment(riskData);
      setLoading(false);
    }
    loadRisk();
  }, [selectedSubmissionId]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <ShieldAlert className="w-5.5 h-5.5 text-amber-600" />
            Advisory Risk Engine Management
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Non-Linear Risk Profiling to Prioritize Officer Review Attention
          </p>
        </div>

        {submissions.length > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 font-bold">Select Submission:</span>
            <select
              value={selectedSubmissionId}
              onChange={(e) => setSelectedSubmissionId(e.target.value)}
              className="p-2 bg-slate-50 border border-slate-200 rounded text-xs font-mono font-bold text-slate-900"
            >
              {submissions.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.submission_reference} ({s.status})
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Mandatory Risk Control Notice */}
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900 space-y-1.5">
        <strong className="font-bold flex items-center gap-1.5 text-sm">
          <Info className="w-4 h-4 text-amber-700" />
          RISK ENGINE ADVISORY CONTROL RULE
        </strong>
        <p className="text-slate-700 text-[11px] leading-relaxed">
          The risk assessment score is calculated strictly to assist procurement officers in triaging and prioritizing attention. <strong>High or critical risk scores NEVER determine bidder qualification or disqualification automatically</strong>. Final decision authority rests exclusively with the authorized human officer.
        </p>
      </div>

      {/* Risk Panel Component */}
      <RiskAssessmentPanel riskAssessment={riskAssessment} loading={loading} />
    </div>
  );
}
