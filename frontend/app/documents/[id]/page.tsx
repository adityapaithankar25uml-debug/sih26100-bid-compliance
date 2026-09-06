'use client';

import React, { useEffect, useState } from 'react';
import { Navbar } from '../../../components/Navbar';
import { Sidebar } from '../../../components/Sidebar';
import { StatusBadge } from '../../../components/StatusBadge';
import { EvidenceViewer } from '../../../components/EvidenceViewer';
import { InconsistencyAlerts } from '../../../components/InconsistencyAlerts';

export default function DocumentDetailPage({ params }: { params: { id: string } }) {
  const documentId = params.id;
  const [docStatus, setDocStatus] = useState<any>(null);
  const [evidenceData, setEvidenceData] = useState<any[]>([]);
  const [inconsistencyData, setInconsistencyData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const token = localStorage.getItem('token') || 'demo-token';
        const headers = { Authorization: `Bearer ${token}` };

        // Fetch doc status
        const resStatus = await fetch(`http://localhost:8000/api/v1/documents/${documentId}/status`, { headers });
        if (resStatus.ok) {
          const dataStatus = await resStatus.json();
          setDocStatus(dataStatus);
        }

        // Fetch evidence
        const resEv = await fetch(`http://localhost:8000/api/v1/documents/${documentId}/evidence`, { headers });
        if (resEv.ok) {
          const dataEv = await resEv.json();
          setEvidenceData(dataEv.evidence_provenance || []);
        }

        // Fetch inconsistency candidates
        const resInc = await fetch(`http://localhost:8000/api/v1/bids/SUB-2026-001/inconsistency-candidates`, { headers });
        if (resInc.ok) {
          const dataInc = await resInc.json();
          setInconsistencyData(dataInc.inconsistency_candidates || []);
        }
      } catch (err) {
        console.error('Failed to fetch document detail:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, [documentId]);

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Document Intelligence Workspace</h1>
              <p className="text-sm font-mono text-slate-500">ID: {documentId}</p>
            </div>
            <span className="px-3 py-1 bg-purple-50 text-purple-900 border border-purple-300 rounded font-semibold text-xs">
              AI PROPOSAL — ADVISORY ONLY
            </span>
          </div>

          {isLoading ? (
            <div className="p-8 text-center text-slate-500 text-sm">Loading document intelligence data...</div>
          ) : (
            <>
              {docStatus && (
                <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
                  <h2 className="text-lg font-semibold text-slate-800">Document Metadata & Security</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <div className="text-slate-500 text-xs uppercase font-semibold">Filename</div>
                      <div className="font-medium text-slate-900">{docStatus.original_filename}</div>
                    </div>
                    <div>
                      <div className="text-slate-500 text-xs uppercase font-semibold">Classification</div>
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-slate-100 text-slate-800 border">
                        {docStatus.security_classification}
                      </span>
                    </div>
                    <div>
                      <div className="text-slate-500 text-xs uppercase font-semibold">Quarantine</div>
                      <StatusBadge status={docStatus.quarantine_status} />
                    </div>
                    <div>
                      <div className="text-slate-500 text-xs uppercase font-semibold">Malware Scan</div>
                      <StatusBadge status={docStatus.malware_scan_result} />
                    </div>
                  </div>
                </div>
              )}

              <InconsistencyAlerts signals={inconsistencyData} />

              <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
                <EvidenceViewer evidenceList={evidenceData} />
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
