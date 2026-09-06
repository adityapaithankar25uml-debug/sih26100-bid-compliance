'use client';
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Shield, FileCheck, HelpCircle, GitCommit, AlertTriangle, UserCheck } from 'lucide-react';
import {
  fetchSubmissions,
  fetchBidComplianceExplanation,
  fetchBidEvidenceTrace,
  fetchBidRiskAssessment,
  fetchHumanReviewTasks,
  resolveHumanReviewTask,
  recordOfficerDecision
} from '../../../lib/api';
import {
  BidSubmission,
  ComplianceExplanationResponse,
  EvidenceTraceGraph,
  RiskAssessmentResponse,
  HumanReviewTask
} from '../../../types';
import { StatusBadge } from '../../../components/StatusBadge';
import { WhyExplanationPanel } from '../../../components/WhyExplanationPanel';
import { EvidenceLineageGraph } from '../../../components/EvidenceLineageGraph';
import { RiskAssessmentPanel } from '../../../components/RiskAssessmentPanel';
import { HumanReviewWorkspace } from '../../../components/HumanReviewWorkspace';
import { OfficerDecisionDialog } from '../../../components/OfficerDecisionDialog';

export default function BidDetailPage() {
  const params = useParams();
  const subId = params?.id as string;
  const [submission, setSubmission] = useState<BidSubmission | null>(null);
  const [explanation, setExplanation] = useState<ComplianceExplanationResponse | null>(null);
  const [evidenceTrace, setEvidenceTrace] = useState<EvidenceTraceGraph | null>(null);
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessmentResponse | null>(null);
  const [reviewTasks, setReviewTasks] = useState<HumanReviewTask[]>([]);
  const [activeTab, setActiveTab] = useState<'explanation' | 'lineage' | 'risk' | 'review' | 'decision'>('explanation');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (subId) {
      Promise.all([
        fetchSubmissions().then((list) => list.find((s) => s.id === subId) || null),
        fetchBidComplianceExplanation(subId),
        fetchBidEvidenceTrace(subId),
        fetchBidRiskAssessment(subId),
        fetchHumanReviewTasks()
      ]).then(([sub, exp, trace, risk, tasks]) => {
        setSubmission(sub);
        setExplanation(exp);
        setEvidenceTrace(trace);
        setRiskAssessment(risk);
        setReviewTasks(tasks.filter((t) => t.bid_submission_id === subId));
        setLoading(false);
      });
    }
  }, [subId]);

  const handleResolveTask = async (taskId: string, decision: string, summary: string) => {
    await resolveHumanReviewTask(taskId, decision, summary);
    const updatedTasks = await fetchHumanReviewTasks();
    setReviewTasks(updatedTasks.filter((t) => t.bid_submission_id === subId));
  };

  const handleOfficerDecision = async (decision: string, rationale: string) => {
    await recordOfficerDecision(subId, decision, rationale);
    if (submission) {
      setSubmission({ ...submission, status: decision });
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-400">Loading Phase 5 Evidence & Review Workspace...</div>;
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

      {/* Proposal Summary Header */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <span className="font-mono text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              {submission.submission_reference}
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-2">
              Phase 5 Evidence, Risk & Human Officer Workspace
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

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('explanation')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === 'explanation' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <HelpCircle className="w-3.5 h-3.5" />
          "Why?" Explanation
        </button>
        <button
          onClick={() => setActiveTab('lineage')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === 'lineage' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <GitCommit className="w-3.5 h-3.5" />
          Evidence Lineage
        </button>
        <button
          onClick={() => setActiveTab('risk')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === 'risk' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <AlertTriangle className="w-3.5 h-3.5" />
          Advisory Risk Engine
        </button>
        <button
          onClick={() => setActiveTab('review')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === 'review' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <UserCheck className="w-3.5 h-3.5" />
          Human Review Tasks ({reviewTasks.length})
        </button>
        <button
          onClick={() => setActiveTab('decision')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === 'decision' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Shield className="w-3.5 h-3.5" />
          Officer Decision & Override
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === 'explanation' && <WhyExplanationPanel explanation={explanation} />}
      {activeTab === 'lineage' && <EvidenceLineageGraph graph={evidenceTrace} />}
      {activeTab === 'risk' && <RiskAssessmentPanel riskAssessment={riskAssessment} />}
      {activeTab === 'review' && (
        <HumanReviewWorkspace
          tasks={reviewTasks}
          onResolveTask={handleResolveTask}
        />
      )}
      {activeTab === 'decision' && (
        <OfficerDecisionDialog
          submissionId={subId}
          onSubmitDecision={handleOfficerDecision}
        />
      )}
    </div>
  );
}
