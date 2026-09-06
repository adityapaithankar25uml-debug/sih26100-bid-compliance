'use client';
import React, { useEffect, useState, useCallback } from 'react';
import { UserCheck, CheckCircle, Clock, AlertTriangle, ShieldCheck, Filter } from 'lucide-react';
import { fetchHumanReviewTasks, resolveHumanReviewTask } from '../../lib/api';
import { HumanReviewTask } from '../../types';
import { HumanReviewWorkspace } from '../../components/HumanReviewWorkspace';

export default function HumanReviewPage() {
  const [tasks, setTasks] = useState<HumanReviewTask[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [loading, setLoading] = useState(true);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    const data = await fetchHumanReviewTasks(statusFilter || undefined);
    setTasks(data);
    setLoading(false);
  }, [statusFilter]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleResolveTask = async (taskId: string, decision: string, summary: string) => {
    await resolveHumanReviewTask(taskId, decision, summary);
    await loadTasks();
  };

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <UserCheck className="w-5.5 h-5.5 text-gov-blue" />
            Procurement Officer Human Review Queue
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Prioritized Discrepancies, Ambiguities & Evidence Request Tasks Awaiting Officer Action
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="p-2 bg-slate-50 border border-slate-200 rounded text-xs text-slate-800 font-bold"
          >
            <option value="">All Review Statuses</option>
            <option value="PENDING">PENDING — Action Required</option>
            <option value="IN_REVIEW">IN REVIEW — Assigned</option>
            <option value="RESOLVED">RESOLVED — Decision Recorded</option>
          </select>
        </div>
      </div>

      {/* Human Review Component */}
      <HumanReviewWorkspace
        tasks={tasks}
        onResolveTask={handleResolveTask}
        loading={loading}
      />
    </div>
  );
}
