import React from 'react';
import { StatusBadge } from './StatusBadge';

export interface InconsistencySignal {
  signal_code: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  affected_document_ids: string[];
  status: string;
}

export const InconsistencyAlerts: React.FC<{ signals: InconsistencySignal[] }> = ({ signals }) => {
  if (!signals || signals.length === 0) {
    return (
      <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded text-sm font-medium">
        ✓ No document inconsistency candidates detected.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-800 uppercase tracking-wider">
        Candidate Discrepancy Alerts ({signals.length} Signals)
      </h3>
      <div className="space-y-2">
        {signals.map((sig, idx) => (
          <div key={idx} className="p-4 border rounded-lg border-amber-200 bg-amber-50/40 flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs font-bold text-amber-900 bg-amber-100 px-2 py-0.5 rounded">
                  {sig.signal_code}
                </span>
                <span className="text-xs font-semibold text-slate-600">Severity: {sig.severity}</span>
              </div>
              <p className="text-sm text-slate-800">{sig.description}</p>
              <p className="text-xs text-slate-500 font-mono">
                Affected Document IDs: {sig.affected_document_ids.join(', ')}
              </p>
            </div>
            <StatusBadge status="REQUIRES_HUMAN_REVIEW" />
          </div>
        ))}
      </div>
    </div>
  );
};
