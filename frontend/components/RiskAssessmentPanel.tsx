'use client';
import React from 'react';
import { AlertOctagon, ShieldAlert, Info, AlertTriangle, CheckCircle } from 'lucide-react';
import { RiskAssessmentResponse, RiskFactorSignal } from '../types';

interface RiskAssessmentPanelProps {
  riskAssessment: RiskAssessmentResponse | null;
  loading?: boolean;
}

export function RiskAssessmentPanel({ riskAssessment, loading }: RiskAssessmentPanelProps) {
  if (loading) {
    return <div className="p-6 text-center text-xs text-slate-400">Evaluating advisory risk profile...</div>;
  }

  if (!riskAssessment) {
    return (
      <div className="p-6 bg-slate-50 border border-slate-200 rounded text-center text-xs text-slate-500">
        No advisory risk profile available.
      </div>
    );
  }

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return <span className="bg-rose-600 text-white font-bold px-3 py-1 rounded text-xs uppercase tracking-wider flex items-center gap-1"><AlertOctagon className="w-3.5 h-3.5" /> CRITICAL RISK</span>;
      case 'HIGH':
        return <span className="bg-amber-600 text-white font-bold px-3 py-1 rounded text-xs uppercase tracking-wider flex items-center gap-1"><ShieldAlert className="w-3.5 h-3.5" /> HIGH RISK</span>;
      case 'MEDIUM':
        return <span className="bg-blue-600 text-white font-bold px-3 py-1 rounded text-xs uppercase tracking-wider flex items-center gap-1"><Info className="w-3.5 h-3.5" /> MEDIUM RISK</span>;
      case 'LOW':
      default:
        return <span className="bg-emerald-600 text-white font-bold px-3 py-1 rounded text-xs uppercase tracking-wider flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> LOW RISK</span>;
    }
  };

  return (
    <div className="space-y-4 bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
      {/* Header & Risk Score */}
      <div className="flex items-start justify-between border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="font-bold text-slate-900 text-sm">Advisory Risk Engine Profile</h3>
            {getRiskBadge(riskAssessment.overall_risk_level)}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Calculated at: {new Date(riskAssessment.calculated_at).toLocaleString()} | Profile Version: {riskAssessment.profile_version}
          </p>
        </div>

        <div className="text-right bg-slate-50 px-4 py-2 rounded border border-slate-200">
          <span className="text-[10px] text-slate-500 uppercase block font-bold">Non-Linear Risk Score</span>
          <span className="text-2xl font-black font-mono text-slate-900">{riskAssessment.risk_score}</span>
          <span className="text-[10px] text-slate-400 block font-mono">/ 100.0</span>
        </div>
      </div>

      {/* Mandatory Advisory Notice */}
      <div className="p-3 bg-blue-50 border border-blue-200 rounded text-xs text-blue-900 flex items-start gap-2">
        <Info className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
        <div>
          <strong className="block font-bold">MANDATORY ADVISORY NOTICE:</strong>
          <span className="text-[11px] leading-relaxed">
            Risk scores exist strictly to assist procurement officers in prioritizing review attention. Risk scores do <strong>NOT</strong> directly determine bidder qualification or disqualification. Final decision authority rests exclusively with the human procurement officer.
          </span>
        </div>
      </div>

      {/* Risk Signals List */}
      <div className="space-y-2 pt-2">
        <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wide">
          Detected Risk Factor Signals ({riskAssessment.signals.length})
        </h4>

        {riskAssessment.signals.length === 0 ? (
          <div className="p-4 text-center text-xs text-slate-400 bg-slate-50 rounded">
            No risk factor signals detected for this submission.
          </div>
        ) : (
          riskAssessment.signals.map((sig: RiskFactorSignal) => (
            <div key={sig.id} className="p-3 rounded border border-slate-200 bg-slate-50 flex items-start justify-between text-xs space-y-1">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-slate-900">{sig.factor_code}</span>
                  <span className="bg-slate-200 text-slate-800 text-[10px] px-1.5 py-0.5 rounded font-bold uppercase">{sig.category}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                    sig.severity === 'CRITICAL' ? 'bg-red-100 text-red-800 border border-red-300' :
                    sig.severity === 'HIGH' ? 'bg-amber-100 text-amber-800 border border-amber-300' :
                    'bg-slate-200 text-slate-700'
                  }`}>
                    {sig.severity}
                  </span>
                </div>
                <p className="text-slate-700 text-xs mt-1">{sig.description}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
