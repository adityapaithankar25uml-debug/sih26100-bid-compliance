'use client';
import React, { useEffect, useState } from 'react';
import { FileSearch, Layers, ShieldCheck, Link2, Info } from 'lucide-react';
import { fetchSubmissions, fetchBidEvidenceTrace } from '../../lib/api';
import { BidSubmission, EvidenceTraceGraph } from '../../types';
import { EvidenceViewer } from '../../components/EvidenceViewer';
import { EvidenceLineageGraph } from '../../components/EvidenceLineageGraph';

export default function EvidencePage() {
  const [submissions, setSubmissions] = useState<BidSubmission[]>([]);
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<string>('');
  const [traceGraph, setTraceGraph] = useState<EvidenceTraceGraph | null>(null);
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
    async function loadTrace() {
      setLoading(true);
      const data = await fetchBidEvidenceTrace(selectedSubmissionId);
      setTraceGraph(data);
      setLoading(false);
    }
    loadTrace();
  }, [selectedSubmissionId]);

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <FileSearch className="w-5.5 h-5.5 text-gov-blue" />
            Evidence & Provenance Explorer
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Traceability Ledger & 9 Independent Evidence Quality Dimensions
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

      {/* 9 Quality Dimensions Guidance Banner */}
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 space-y-2">
        <strong className="font-bold flex items-center gap-1.5 text-slate-900">
          <Info className="w-4 h-4 text-gov-blue" />
          9 INDEPENDENT EVIDENCE QUALITY DIMENSIONS
        </strong>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-[11px]">
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">1. source_authority</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">2. source_freshness</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">3. completeness</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">4. integrity_hash_validity</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">5. identity_linkage</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">6. document_authenticity</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">7. temporal_applicability</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">8. extraction_provenance</div>
          <div className="bg-white p-2 rounded border border-slate-200 font-mono">9. consistency</div>
        </div>
      </div>

      {/* Evidence Trace Graph & Viewer */}
      {traceGraph ? (
        <div className="space-y-6">
          <EvidenceLineageGraph graph={traceGraph} />
        </div>
      ) : (

        <div className="p-8 text-center text-xs text-slate-400 bg-slate-50 rounded border border-slate-200">
          {loading ? 'Loading evidence trace graph...' : 'No evidence trace graph available for selected submission.'}
        </div>
      )}
    </div>
  );
}
