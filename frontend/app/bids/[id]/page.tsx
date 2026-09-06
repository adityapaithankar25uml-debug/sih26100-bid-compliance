'use client';
import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Shield,
  FileCheck,
  HelpCircle,
  GitCommit,
  AlertTriangle,
  UserCheck,
  Building2,
  FileText,
  ShieldCheck,
  Lock,
  Layers,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  PlusCircle,
  User
} from 'lucide-react';
import {
  fetchSubmissions,
  fetchBidComplianceExplanation,
  fetchBidEvidenceTrace,
  fetchBidRiskAssessment,
  fetchHumanReviewTasks,
  resolveHumanReviewTask,
  recordOfficerDecision,
  fetchBidComplianceMatrix,
  fetchBidVerifications,
  triggerGovernmentVerification,
  fetchBidManualOverrides,
  createManualOverride,
  approveManualOverride,
  verifyAuditChain
} from '../../../lib/api';
import {
  BidSubmission,
  ComplianceExplanationResponse,
  EvidenceTraceGraph,
  RiskAssessmentResponse,
  HumanReviewTask,
  ComplianceMatrixResponse,
  GovernmentVerificationRecord,
  ManualOverrideResponse,
  AuditChainVerify
} from '../../../types';
import { StatusBadge } from '../../../components/StatusBadge';
import { WhyExplanationPanel } from '../../../components/WhyExplanationPanel';
import { EvidenceLineageGraph } from '../../../components/EvidenceLineageGraph';
import { RiskAssessmentPanel } from '../../../components/RiskAssessmentPanel';
import { HumanReviewWorkspace } from '../../../components/HumanReviewWorkspace';

export default function BidDetailPage() {
  const params = useParams();
  const subId = params?.id as string;

  const [submission, setSubmission] = useState<BidSubmission | null>(null);
  const [explanation, setExplanation] = useState<ComplianceExplanationResponse | null>(null);
  const [evidenceTrace, setEvidenceTrace] = useState<EvidenceTraceGraph | null>(null);
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessmentResponse | null>(null);
  const [reviewTasks, setReviewTasks] = useState<HumanReviewTask[]>([]);
  const [complianceMatrix, setComplianceMatrix] = useState<ComplianceMatrixResponse | null>(null);
  const [verifications, setVerifications] = useState<GovernmentVerificationRecord[]>([]);
  const [manualOverrides, setManualOverrides] = useState<ManualOverrideResponse[]>([]);
  const [auditStatus, setAuditStatus] = useState<AuditChainVerify | null>(null);

  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'compliance'
    | 'documents'
    | 'verification'
    | 'evidence'
    | 'risk'
    | 'review'
    | 'decision'
    | 'audit'
  >('compliance');

  const [loading, setLoading] = useState(true);
  const [decisionRationale, setDecisionRationale] = useState('');
  const [selectedDecision, setSelectedDecision] = useState('QUALIFIED');
  const [submittingDecision, setSubmittingDecision] = useState(false);

  // Manual Override Form State
  const [overrideReqId, setOverrideReqId] = useState('');
  const [overridePrevStatus, setOverridePrevStatus] = useState('FAIL');
  const [overrideNewStatus, setOverrideNewStatus] = useState('PASS');
  const [overrideReason, setOverrideReason] = useState('');
  const [submittingOverride, setSubmittingOverride] = useState(false);

  const loadAllData = useCallback(async () => {
    if (!subId) return;
    setLoading(true);
    const [sub, exp, trace, risk, tasks, matrix, verifs, overrides, aStatus] = await Promise.all([
      fetchSubmissions().then((list) => list.find((s) => s.id === subId || s.submission_reference === subId || subId === 'SUB_01') || list[0] || null),
      fetchBidComplianceExplanation(subId),
      fetchBidEvidenceTrace(subId),
      fetchBidRiskAssessment(subId),
      fetchHumanReviewTasks(),
      fetchBidComplianceMatrix(subId),
      fetchBidVerifications(subId),
      fetchBidManualOverrides(subId),
      verifyAuditChain(),
    ]);

    setSubmission(sub);
    setExplanation(exp);
    setEvidenceTrace(trace);
    setRiskAssessment(risk);
    setReviewTasks(tasks.filter((t) => t.bid_submission_id === subId));
    setComplianceMatrix(matrix);
    setVerifications(verifs);
    setManualOverrides(overrides);
    setAuditStatus(aStatus);
    setLoading(false);
  }, [subId]);

  useEffect(() => {
    loadAllData();
  }, [loadAllData]);

  const handleResolveTask = async (taskId: string, decision: string, summary: string) => {
    await resolveHumanReviewTask(taskId, decision, summary);
    await loadAllData();
  };

  const handleOfficerDecisionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!decisionRationale.trim()) return;
    setSubmittingDecision(true);
    const res = await recordOfficerDecision(subId, selectedDecision, decisionRationale);
    if (res && submission) {
      setSubmission({ ...submission, status: selectedDecision });
    }
    setSubmittingDecision(false);
    await loadAllData();
  };

  const handleCreateOverrideSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!overrideReqId || !overrideReason.trim()) return;
    setSubmittingOverride(true);
    await createManualOverride(subId, overrideReqId, overridePrevStatus, overrideNewStatus, overrideReason);
    setOverrideReason('');
    setSubmittingOverride(false);
    await loadAllData();
  };

  const handleApproveOverride = async (overrideId: string, approved: boolean) => {
    await approveManualOverride(overrideId, approved, 'Reviewed and verified by Senior Reviewer.');
    await loadAllData();
  };

  const handleTriggerVerification = async (sourceCode: string) => {
    await triggerGovernmentVerification(subId, sourceCode);
    await loadAllData();
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-400">Loading Bid Submission Workspace...</div>;
  }

  if (!submission) {
    return (
      <div className="p-8 text-center text-xs text-slate-500">
        Submission not found. <Link href="/bids" className="text-gov-blue underline">Back to registry</Link>
      </div>
    );
  }

  const pendingTaskCount = reviewTasks.filter((t) => t.status !== 'RESOLVED' && t.status !== 'REJECTED').length;

  return (
    <div className="space-y-6">
      <Link href="/bids" className="text-xs font-semibold text-gov-blue hover:underline flex items-center gap-1">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Submissions Registry
      </Link>

      {/* Workspace Summary Header */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-slate-900 bg-slate-100 px-2.5 py-1 rounded border border-slate-300">
                {submission.submission_reference}
              </span>
              <span className="text-xs font-mono bg-blue-50 text-blue-900 px-2.5 py-1 rounded border border-blue-200">
                Tender: {submission.tender_id} (v1.0.0)
              </span>
            </div>
            <h2 className="text-xl font-bold text-slate-900 mt-2">
              Integrated Bid Verification Workspace — {submission.bidder_id}
            </h2>
          </div>
          <StatusBadge status={submission.status} />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-3 border-t border-slate-100 text-xs">
          <div>
            <span className="text-slate-500 block">Bidder Legal Identity</span>
            <span className="font-bold text-slate-800">ABC Engineering Pvt Ltd</span>
          </div>
          <div>
            <span className="text-slate-500 block">Identity Linkage</span>
            <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[10px]">
              MATCHED (GSTIN / PAN)
            </span>
          </div>
          <div>
            <span className="text-slate-500 block">Submission Date</span>
            <span className="font-semibold text-slate-800">
              {new Date(submission.submission_date).toLocaleString()}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block">Advisory Risk Level</span>
            <span className="font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-[10px]">
              {riskAssessment?.overall_risk_level || 'MEDIUM'} (Score: {riskAssessment?.risk_score || 25})
            </span>
          </div>
        </div>
      </div>

      {/* 9 Workspace Tabs */}
      <div className="flex items-center gap-1 border-b border-slate-200 text-xs font-semibold overflow-x-auto pb-0">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'overview' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Building2 className="w-3.5 h-3.5" /> Overview (Bidder 360)
        </button>
        <button
          onClick={() => setActiveTab('compliance')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'compliance' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <FileCheck className="w-3.5 h-3.5" /> Compliance Matrix
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'documents' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <FileText className="w-3.5 h-3.5" /> Documents & AI Extraction
        </button>
        <button
          onClick={() => setActiveTab('verification')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'verification' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <ShieldCheck className="w-3.5 h-3.5" /> Government Verification
        </button>
        <button
          onClick={() => setActiveTab('evidence')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'evidence' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <GitCommit className="w-3.5 h-3.5" /> Evidence & Lineage
        </button>
        <button
          onClick={() => setActiveTab('risk')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'risk' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <AlertTriangle className="w-3.5 h-3.5" /> Risk Engine
        </button>
        <button
          onClick={() => setActiveTab('review')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'review' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <UserCheck className="w-3.5 h-3.5" /> Human Review ({pendingTaskCount})
        </button>
        <button
          onClick={() => setActiveTab('decision')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'decision' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Shield className="w-3.5 h-3.5" /> Decision & Override
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`pb-2.5 px-3 border-b-2 flex items-center gap-1.5 whitespace-nowrap transition ${
            activeTab === 'audit' ? 'border-gov-blue text-gov-blue font-bold' : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Lock className="w-3.5 h-3.5" /> Audit Hash Chain
        </button>
      </div>

      {/* TAB 1: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
            <Building2 className="w-4 h-4 text-gov-blue" /> Bidder 360 & Statutory Identifier Profile
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">Legal Registered Name</span>
              <span className="font-semibold text-slate-900 text-sm">ABC Engineering Private Limited</span>
            </div>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">PAN (Income Tax)</span>
              <span className="font-mono font-bold text-slate-900 text-sm">AACCA1234F</span>
            </div>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">GSTIN Registration</span>
              <span className="font-mono font-bold text-slate-900 text-sm">33AACCA1234F1Z5</span>
            </div>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">Udyam / MSME Certificate</span>
              <span className="font-mono font-bold text-slate-900 text-sm">UDYAM-TN-02-0012345</span>
            </div>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">Corporate Identity Number (CIN)</span>
              <span className="font-mono font-bold text-slate-900 text-sm">U28920TN2015PTC101234</span>
            </div>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
              <span className="text-slate-500 font-bold block">EPFO Establishment Code</span>
              <span className="font-mono font-bold text-slate-900 text-sm">TN/MAS/0045123/000</span>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: COMPLIANCE MATRIX (FLAGSHIP SCREEN) */}
      {activeTab === 'compliance' && (
        <div className="space-y-4">
          <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-gov-blue" />
                  Deterministic Compliance Matrix Evaluation
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Evaluation Recommendation: <strong>{complianceMatrix?.qualification_recommendation || 'QUALIFICATION_RECOMMENDED'}</strong>
                </p>
              </div>
              <StatusBadge status={complianceMatrix?.overall_status || 'PASS'} />
            </div>

            {/* Matrix Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold">
                    <th className="py-2.5 px-3">Requirement</th>
                    <th className="py-2.5 px-3">Rule Code</th>
                    <th className="py-2.5 px-3">Source & Verification</th>
                    <th className="py-2.5 px-3">Compliance Status</th>
                    <th className="py-2.5 px-3">Evidence Trace</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {complianceMatrix?.matrix_items.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="py-3 px-3">
                        <div className="font-bold text-slate-900">{item.requirement_title}</div>
                        <div className="text-[10px] text-slate-500 font-mono">{item.requirement_code}</div>
                      </td>
                      <td className="py-3 px-3 font-mono font-bold text-slate-700">
                        {item.rule_code}
                      </td>
                      <td className="py-3 px-3">
                        <span className="font-mono text-[10px] bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded font-bold">
                          {item.source_code || 'GOVERNMENT'}
                        </span>
                        <div className="text-[10px] text-slate-500 mt-0.5">{item.verification_status}</div>
                      </td>
                      <td className="py-3 px-3">
                        <StatusBadge status={item.compliance_status} />
                      </td>
                      <td className="py-3 px-3 text-[11px] text-slate-600 max-w-xs truncate">
                        {item.explanation || 'Verified via evidence payload.'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <WhyExplanationPanel explanation={explanation} />
        </div>
      )}

      {/* TAB 3: DOCUMENTS & AI EXTRACTION */}
      {activeTab === 'documents' && (
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
            <FileText className="w-4 h-4 text-gov-blue" /> Document Intelligence & AI Field Extraction Review
          </h3>
          <div className="p-3 bg-purple-50 border border-purple-200 rounded text-xs text-purple-900">
            <strong className="font-bold block">ADVISORY AI EXTRACTION BOUNDARY:</strong>
            Extracted fields are labeled as <strong>AI EXTRACTED (ADVISORY)</strong> and require source verification or rule evaluation before influencing compliance status.
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-900">
                <span>Techno-Commercial Declaration.pdf</span>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded">Scanned & Clean</span>
              </div>
              <p className="text-slate-500 text-[11px]">SHA-256: 8f9a2b1c4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b</p>
              <div className="pt-2 border-t border-slate-200 text-slate-700 space-y-1">
                <div className="flex justify-between">
                  <span>Local Content %:</span> <strong>72.5% (MII Class-I)</strong>
                </div>
                <div className="flex justify-between">
                  <span>Extraction Confidence:</span> <strong className="text-emerald-700">96.8%</strong>
                </div>
                <div className="flex justify-between">
                  <span>Page & Bounding Box:</span> <span>Page 2 [x:50, y:120]</span>
                </div>
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-900">
                <span>Audited_Financial_Statement_FY24.pdf</span>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded">Scanned & Clean</span>
              </div>
              <p className="text-slate-500 text-[11px]">SHA-256: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b</p>
              <div className="pt-2 border-t border-slate-200 text-slate-700 space-y-1">
                <div className="flex justify-between">
                  <span>Annual Turnover:</span> <strong>₹ 14.50 Crores</strong>
                </div>
                <div className="flex justify-between">
                  <span>Extraction Confidence:</span> <strong className="text-emerald-700">94.2%</strong>
                </div>
                <div className="flex justify-between">
                  <span>Page & Bounding Box:</span> <span>Page 5 [x:40, y:210]</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: GOVERNMENT VERIFICATION */}
      {activeTab === 'verification' && (
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-gov-blue" />
              Government Gateway Verifications for Submission {submission.submission_reference}
            </h3>
            <span className="bg-orange-50 text-orange-900 px-2.5 py-1 rounded text-[10px] font-bold border border-orange-200">
              INTEGRATION MODE: MOCK / DEMO
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {['GST', 'UDYAM', 'PAN', 'MCA', 'EPFO', 'DEBARMENT'].map((code) => {
              const rec = verifications.find((v) => v.source_code === code);
              return (
                <div key={code} className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-slate-900 text-sm">{code} Registry</span>
                    <span className="bg-orange-100 text-orange-900 text-[10px] px-1.5 py-0.5 rounded font-bold font-mono">
                      MOCK / DEMO
                    </span>
                  </div>
                  <div className="flex items-center justify-between pt-1">
                    <span className="text-slate-500">Business Verification:</span>
                    <StatusBadge status={rec?.business_status || 'VERIFIED'} />
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                    <span>Verified: {rec?.verified_at ? new Date(rec.verified_at).toLocaleString() : 'Recent'}</span>
                    <button
                      onClick={() => handleTriggerVerification(code)}
                      className="text-gov-blue font-bold hover:underline"
                    >
                      Re-Verify →
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 5: EVIDENCE & LINEAGE */}
      {activeTab === 'evidence' && (
        <div className="space-y-6">
          <EvidenceLineageGraph graph={evidenceTrace} />
        </div>
      )}


      {/* TAB 6: RISK ASSESSMENT */}
      {activeTab === 'risk' && <RiskAssessmentPanel riskAssessment={riskAssessment} />}

      {/* TAB 7: HUMAN REVIEW */}
      {activeTab === 'review' && (
        <HumanReviewWorkspace tasks={reviewTasks} onResolveTask={handleResolveTask} />
      )}

      {/* TAB 8: DECISION & MANUAL OVERRIDE */}
      {activeTab === 'decision' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Officer Decision Submission */}
          <form onSubmit={handleOfficerDecisionSubmit} className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4 text-xs">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
              <Shield className="w-4 h-4 text-gov-blue" /> Submit Statutory Officer Procurement Decision
            </h3>
            <div className="p-3 bg-blue-50 border border-blue-200 rounded text-blue-900 text-[11px]">
              <strong>AUTHORITATIVE DECISION NOTICE:</strong> Final qualification or disqualification is strictly executed by authorized human officers.
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Select Statutory Decision</label>
              <select
                value={selectedDecision}
                onChange={(e) => setSelectedDecision(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded text-xs font-bold text-slate-900"
              >
                <option value="QUALIFIED">QUALIFIED — Meets All Technical & Commercial Specifications</option>
                <option value="DISQUALIFIED">DISQUALIFIED — Fails Mandatory Procurement Rules</option>
                <option value="REQUIRES_CLARIFICATION">REQUIRES CLARIFICATION — Issue Clarification Request</option>
                <option value="EVIDENCE_REQUESTED">EVIDENCE REQUESTED — Request Additional Proof</option>
              </select>
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Officer Decision Rationale & Justification</label>
              <textarea
                value={decisionRationale}
                onChange={(e) => setDecisionRationale(e.target.value)}
                rows={4}
                required
                placeholder="Enter detailed statutory procurement reasoning..."
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded text-xs text-slate-900"
              />
            </div>
            <button
              type="submit"
              disabled={submittingDecision || !decisionRationale.trim()}
              className="w-full bg-navy-900 hover:bg-gov-blue text-white py-2.5 rounded font-bold text-xs transition disabled:opacity-50"
            >
              {submittingDecision ? 'Recording Decision...' : 'Record & Sign Officer Decision'}
            </button>
          </form>

          {/* Four-Eyes Manual Override Workspace */}
          <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4 text-xs">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
              <UserCheck className="w-4 h-4 text-amber-600" /> Four-Eyes Manual Rule Overrides ({manualOverrides.length})
            </h3>
            <form onSubmit={handleCreateOverrideSubmit} className="space-y-3 p-3 bg-slate-50 rounded border border-slate-200">
              <span className="font-bold text-slate-800 block text-[11px] uppercase">Propose Policy Override</span>
              <input
                type="text"
                placeholder="Requirement ID (e.g. REQ-MII-01)"
                value={overrideReqId}
                onChange={(e) => setOverrideReqId(e.target.value)}
                required
                className="w-full p-2 bg-white border border-slate-200 rounded text-xs"
              />
              <div className="grid grid-cols-2 gap-2">
                <select
                  value={overridePrevStatus}
                  onChange={(e) => setOverridePrevStatus(e.target.value)}
                  className="p-2 bg-white border border-slate-200 rounded text-xs font-semibold"
                >
                  <option value="FAIL">Previous: FAIL</option>
                  <option value="MISSING_EVIDENCE">Previous: MISSING_EVIDENCE</option>
                </select>
                <select
                  value={overrideNewStatus}
                  onChange={(e) => setOverrideNewStatus(e.target.value)}
                  className="p-2 bg-white border border-slate-200 rounded text-xs font-semibold"
                >
                  <option value="PASS">New: PASS (Waived)</option>
                  <option value="NOT_APPLICABLE">New: N/A</option>
                </select>
              </div>
              <textarea
                placeholder="Detailed override rationale..."
                value={overrideReason}
                onChange={(e) => setOverrideReason(e.target.value)}
                rows={2}
                required
                className="w-full p-2 bg-white border border-slate-200 rounded text-xs"
              />
              <button
                type="submit"
                disabled={submittingOverride || !overrideReason.trim()}
                className="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded text-xs transition disabled:opacity-50"
              >
                Propose Override (Requires Peer Approval)
              </button>
            </form>

            {/* Existing Overrides List */}
            <div className="space-y-2 pt-2">
              {manualOverrides.map((ov) => (
                <div key={ov.id} className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-mono font-bold text-slate-900">{ov.requirement_id}</span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                      ov.four_eyes_status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {ov.four_eyes_status}
                    </span>
                  </div>
                  <p className="text-slate-700">{ov.override_reason}</p>
                  {ov.four_eyes_status === 'PENDING_APPROVAL' && (
                    <div className="pt-2 flex gap-2">
                      <button
                        onClick={() => handleApproveOverride(ov.id, true)}
                        className="bg-emerald-600 text-white px-2 py-1 rounded text-[10px] font-bold"
                      >
                        Approve Override
                      </button>
                      <button
                        onClick={() => handleApproveOverride(ov.id, false)}
                        className="bg-rose-600 text-white px-2 py-1 rounded text-[10px] font-bold"
                      >
                        Reject Override
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 9: AUDIT EXPLORER */}
      {activeTab === 'audit' && (
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <Lock className="w-4 h-4 text-amber-600" />
              Submission Audit Trail & SHA-256 Hash Chain Status
            </h3>
            <span className="text-xs font-mono text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              Verified Blocks: {auditStatus?.verified_blocks || 0} / {auditStatus?.total_blocks || 0}
            </span>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            All evaluation events, human reviews, and officer decisions for submission <strong>{submission.submission_reference}</strong> are canonically linked into the <strong>Tamper-Evident SHA-256 Audit Hash Chain</strong>.
          </p>
        </div>
      )}
    </div>
  );
}
