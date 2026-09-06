'use client';
import React from 'react';
import { HelpCircle, CheckCircle, AlertTriangle, XCircle, Info, ShieldCheck } from 'lucide-react';
import { ComplianceExplanationResponse, WhyExplanationItem } from '../types';

interface WhyExplanationPanelProps {
  explanation: ComplianceExplanationResponse | null;
  loading?: boolean;
}

export function WhyExplanationPanel({ explanation, loading }: WhyExplanationPanelProps) {
  if (loading) {
    return <div className="p-6 text-center text-xs text-slate-400">Loading compliance explanation...</div>;
  }

  if (!explanation || !explanation.explanations || explanation.explanations.length === 0) {
    return (
      <div className="p-6 bg-slate-50 border border-slate-200 rounded text-center text-xs text-slate-500">
        No deterministic compliance explanation available yet. Execute compliance evaluation first.
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'PASS':
        return <span className="bg-emerald-100 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1"><CheckCircle className="w-3 h-3" /> PASS</span>;
      case 'FAIL':
        return <span className="bg-red-100 text-red-800 border border-red-300 px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1"><XCircle className="w-3 h-3" /> FAIL</span>;
      case 'MISSING_EVIDENCE':
        return <span className="bg-amber-100 text-amber-800 border border-amber-300 px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1"><AlertTriangle className="w-3 h-3" /> MISSING EVIDENCE</span>;
      case 'REQUIRES_REVIEW':
      default:
        return <span className="bg-blue-100 text-blue-800 border border-blue-300 px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1"><Info className="w-3 h-3" /> REVIEW REQUIRED</span>;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between bg-slate-900 text-white p-4 rounded-t-lg">
        <div className="flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-amber-400" />
          <h3 className="font-bold text-sm">Deterministic Compliance Explanation (&quot;Why?&quot; View)</h3>
        </div>
        <div className="text-right text-xs">
          <span className="text-slate-400 block">Overall Status</span>
          <span className="font-mono font-bold text-emerald-400">{explanation.overall_status}</span>
        </div>
      </div>

      <div className="space-y-3">
        {explanation.explanations.map((item: WhyExplanationItem, idx: number) => (
          <div key={idx} className="bg-white p-4 rounded border border-slate-200 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <span className="font-mono text-xs text-gov-blue font-bold">{item.requirement_code}</span>
                <h4 className="text-sm font-semibold text-slate-900 mt-1">{item.requirement_title}</h4>
              </div>
              {getStatusBadge(item.status)}
            </div>

            {/* Authoritative Calculation Trace & Facts */}
            <div className="bg-slate-50 p-3 rounded border border-slate-200 text-xs space-y-2 font-mono">
              <div className="flex items-center justify-between text-slate-500 text-[11px]">
                <span>Rule Code: <strong>{item.rule_code}</strong></span>
                <span>Policy Version: <strong>{item.policy_version}</strong></span>
                <span>Tender Version: <strong>{item.tender_version}</strong></span>
              </div>
              <p className="text-slate-800 font-sans text-xs pt-1 border-t border-slate-200">
                <strong>Authoritative Explanation:</strong> {item.explanation_text}
              </p>
              {Object.keys(item.facts_used).length > 0 && (
                <div className="pt-2 text-[11px] text-slate-600">
                  <span className="font-bold text-slate-700">Verified Facts Used:</span>
                  <pre className="bg-slate-100 p-2 rounded mt-1 overflow-x-auto text-slate-900">
                    {JSON.stringify(item.facts_used, null, 2)}
                  </pre>
                </div>
              )}
            </div>

            {/* Advisory AI Summary (Clearly Labeled Non-Authoritative) */}
            {item.ai_advisory_summary && (
              <div className="bg-amber-50 p-2.5 rounded border border-amber-200 text-xs flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-amber-900 text-[10px] uppercase tracking-wide block">
                    AI ADVISORY — NON-AUTHORITATIVE
                  </span>
                  <p className="text-amber-800 text-[11px] mt-0.5 leading-relaxed">
                    {item.ai_advisory_summary}
                  </p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
