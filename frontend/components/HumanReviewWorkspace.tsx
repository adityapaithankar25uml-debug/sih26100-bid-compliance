'use client';
import React, { useState } from 'react';
import { UserCheck, CheckCircle, Clock, AlertTriangle, MessageSquare, Send } from 'lucide-react';
import { HumanReviewTask } from '../types';

interface HumanReviewWorkspaceProps {
  tasks: HumanReviewTask[];
  onResolveTask: (taskId: string, decision: string, summary: string) => Promise<void>;
  loading?: boolean;
}

export function HumanReviewWorkspace({ tasks, onResolveTask, loading }: HumanReviewWorkspaceProps) {
  const [selectedTask, setSelectedTask] = useState<HumanReviewTask | null>(tasks.length > 0 ? tasks[0] : null);
  const [resolutionSummary, setResolutionSummary] = useState('');
  const [decision, setDecision] = useState('APPROVED');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (loading) {
    return <div className="p-6 text-center text-xs text-slate-400">Loading human review workspace...</div>;
  }

  const handleResolve = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedTask || !resolutionSummary.trim()) return;
    setIsSubmitting(true);
    await onResolveTask(selectedTask.id, decision, resolutionSummary);
    setResolutionSummary('');
    setIsSubmitting(false);
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm space-y-4 p-5">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-gov-blue" />
          Human Review Workspace Queue ({tasks.length})
        </h3>
        <span className="text-xs text-slate-500">Officer Workspace</span>
      </div>

      {tasks.length === 0 ? (
        <div className="p-8 text-center text-xs text-slate-400 bg-slate-50 rounded">
          No human review items pending for this submission. All criteria resolved or verified.
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {/* Task List */}
          <div className="space-y-2 lg:col-span-1 border-r border-slate-100 pr-4">
            {tasks.map((task: HumanReviewTask) => (
              <div
                key={task.id}
                onClick={() => setSelectedTask(task)}
                className={`p-3 rounded border text-xs cursor-pointer transition ${
                  selectedTask?.id === task.id ? 'bg-blue-50 border-blue-400 font-semibold' : 'bg-slate-50 border-slate-200 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[10px] text-slate-500">{task.review_code || task.id.substring(0, 8)}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                    task.status === 'RESOLVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {task.status}
                  </span>
                </div>
                <p className="text-slate-800 text-xs mt-1 line-clamp-2">{task.review_reason}</p>
              </div>
            ))}
          </div>

          {/* Task Detail & Resolution Form */}
          {selectedTask && (
            <div className="lg:col-span-2 space-y-4 text-xs">
              <div className="bg-slate-50 p-4 rounded border border-slate-200 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-slate-900">{selectedTask.review_code || selectedTask.id}</span>
                  <span className="bg-slate-200 text-slate-800 px-2 py-0.5 rounded font-bold">
                    Priority: {selectedTask.priority}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 block font-bold">Review Reason</span>
                  <p className="text-slate-800 font-medium text-sm mt-0.5">{selectedTask.review_reason}</p>
                </div>
                {selectedTask.suggested_action && (
                  <div className="bg-white p-2.5 rounded border border-slate-200 text-slate-700">
                    <strong className="block text-[11px] text-slate-500 uppercase">Suggested Inspection Action</strong>
                    {selectedTask.suggested_action}
                  </div>
                )}
              </div>

              {/* Resolution Form */}
              {selectedTask.status !== 'RESOLVED' ? (
                <form onSubmit={handleResolve} className="space-y-3 bg-white p-4 rounded border border-slate-200">
                  <h4 className="font-bold text-slate-900 text-xs flex items-center gap-1">
                    <MessageSquare className="w-3.5 h-3.5 text-gov-blue" />
                    Record Procurement Officer Task Resolution
                  </h4>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-[11px] font-bold text-slate-600">Resolution Decision</label>
                      <select
                        value={decision}
                        onChange={(e) => setDecision(e.target.value)}
                        className="w-full mt-1 p-2 bg-slate-50 border border-slate-200 rounded text-xs text-slate-900 font-semibold"
                      >
                        <option value="APPROVED">APPROVED — Discrepancy Verified & Cleared</option>
                        <option value="OVERRIDDEN">OVERRIDDEN — Policy Exception Granted</option>
                        <option value="REJECTED">REJECTED — Insufficient Proof</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-slate-600">Officer Resolution Summary & Rationale</label>
                    <textarea
                      value={resolutionSummary}
                      onChange={(e) => setResolutionSummary(e.target.value)}
                      rows={3}
                      required
                      placeholder="Enter detailed procurement officer reasoning..."
                      className="w-full mt-1 p-2 bg-slate-50 border border-slate-200 rounded text-xs text-slate-900"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting || !resolutionSummary.trim()}
                    className="bg-gov-blue text-white px-4 py-2 rounded text-xs font-bold hover:bg-blue-900 flex items-center gap-1.5 disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    {isSubmitting ? 'Submitting...' : 'Submit Task Resolution'}
                  </button>
                </form>
              ) : (
                <div className="p-4 bg-emerald-50 border border-emerald-200 rounded text-emerald-900 space-y-1">
                  <span className="font-bold flex items-center gap-1"><CheckCircle className="w-4 h-4 text-emerald-700" /> Task Resolved</span>
                  <p className="text-xs">Decision: <strong>{selectedTask.decision}</strong></p>
                  <p className="text-xs">Summary: {selectedTask.resolution_summary}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
