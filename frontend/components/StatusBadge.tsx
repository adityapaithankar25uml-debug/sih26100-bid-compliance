import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const normalized = (status || '').toUpperCase();

  let style = 'bg-slate-100 text-slate-800 border-slate-300';
  let label = normalized;

  switch (normalized) {
    case 'AI_EXTRACTED':
    case 'AI PROPOSAL':
      style = 'bg-purple-50 text-purple-900 border-purple-300 font-medium';
      label = 'AI EXTRACTED (ADVISORY)';
      break;
    case 'AI_GENERATED':
      style = 'bg-violet-50 text-violet-900 border-violet-300 font-medium';
      label = 'AI GENERATED (ADVISORY)';
      break;
    case 'DETERMINISTIC':
    case 'DETERMINISTICALLY_EXTRACTED':
      style = 'bg-cyan-50 text-cyan-900 border-cyan-300 font-medium';
      label = 'DETERMINISTIC EXTRACTION';
      break;
    case 'GOVERNMENT_VERIFIED':
      style = 'bg-emerald-100 text-emerald-900 border-emerald-400 font-bold';
      label = 'GOVERNMENT VERIFIED';
      break;
    case 'MOCK':
    case 'DEMO':
    case 'MOCK / DEMO':
      style = 'bg-orange-50 text-orange-900 border-orange-300 font-medium';
      label = 'MOCK / DEMO';
      break;
    case 'VERIFIED':
    case 'QUALIFIED':
    case 'ACTIVE':
      style = 'bg-emerald-50 text-emerald-800 border-emerald-300 font-semibold';
      break;
    case 'UNVERIFIED':
    case 'PENDING':
    case 'SUBMITTED':
      style = 'bg-blue-50 text-blue-800 border-blue-300 font-medium';
      break;
    case 'MISSING_EVIDENCE':
      style = 'bg-amber-50 text-amber-900 border-amber-300 font-medium';
      label = 'MISSING EVIDENCE (NON-FATAL)';
      break;
    case 'REQUIRES_HUMAN_REVIEW':
      style = 'bg-indigo-50 text-indigo-900 border-indigo-300 font-medium';
      label = 'HUMAN REVIEW REQUIRED';
      break;
    case 'CONFLICTING':
    case 'INVALID':
    case 'DISQUALIFIED':
      style = 'bg-rose-50 text-rose-800 border-rose-300 font-semibold';
      break;
    case 'NOT_APPLICABLE':
      style = 'bg-slate-100 text-slate-600 border-slate-200';
      label = 'N/A';
      break;
    default:
      style = 'bg-slate-100 text-slate-800 border-slate-300';
  }

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs border ${style}`}
      aria-label={`Status: ${label}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 opacity-75" />
      {label}
    </span>
  );
};
