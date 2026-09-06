'use client';
import React from 'react';
import { GitCommit, FileText, ShieldAlert, CheckCircle, ArrowRight, CornerDownRight } from 'lucide-react';
import { EvidenceTraceGraph, EvidenceTraceNode, EvidenceTraceEdge } from '../types';

interface EvidenceLineageGraphProps {
  graph: EvidenceTraceGraph | null;
  loading?: boolean;
}

export function EvidenceLineageGraph({ graph, loading }: EvidenceLineageGraphProps) {
  if (loading) {
    return <div className="p-6 text-center text-xs text-slate-400">Loading evidence lineage graph...</div>;
  }

  if (!graph || !graph.nodes || graph.nodes.length === 0) {
    return (
      <div className="p-6 bg-slate-50 border border-slate-200 rounded text-center text-xs text-slate-500">
        No evidence lineage graph available for this submission.
      </div>
    );
  }

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'REQUIREMENT':
        return 'bg-purple-50 border-purple-300 text-purple-900';
      case 'RULE':
        return 'bg-blue-50 border-blue-300 text-blue-900';
      case 'FACT':
        return 'bg-emerald-50 border-emerald-300 text-emerald-900';
      case 'EVIDENCE':
        return 'bg-amber-50 border-amber-300 text-amber-900';
      case 'GOVT_RECORD':
        return 'bg-teal-50 border-teal-300 text-teal-900';
      case 'RISK_SIGNAL':
        return 'bg-rose-50 border-rose-300 text-rose-900';
      case 'OFFICER_DECISION':
        return 'bg-slate-900 text-white border-slate-800';
      default:
        return 'bg-slate-100 border-slate-300 text-slate-800';
    }
  };

  return (
    <div className="space-y-4 bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
          <GitCommit className="w-4 h-4 text-gov-blue" />
          Evidence Traceability Lineage Graph
        </h3>
        <span className="text-xs text-slate-500 font-mono">
          Nodes: {graph.nodes.length} | Edges: {graph.edges.length}
        </span>
      </div>

      <div className="space-y-3 pt-2">
        {graph.nodes.map((node: EvidenceTraceNode) => (
          <div key={node.node_id} className={`p-3 rounded border text-xs font-mono flex items-center justify-between ${getNodeColor(node.node_type)}`}>
            <div className="flex items-center gap-2">
              <CornerDownRight className="w-3.5 h-3.5 opacity-60" />
              <span className="font-bold uppercase text-[10px] bg-black/10 px-1.5 py-0.5 rounded">{node.node_type}</span>
              <span className="font-bold font-sans">{node.label}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-white/50 border border-black/10">{node.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
