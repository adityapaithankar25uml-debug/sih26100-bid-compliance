'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { FolderCheck, Search } from 'lucide-react';
import { fetchSubmissions, fetchBidders } from '../../lib/api';
import { BidSubmission, Bidder } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export default function BidsPage() {
  const [submissions, setSubmissions] = useState<BidSubmission[]>([]);
  const [bidders, setBidders] = useState<Record<string, Bidder>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [subList, bidderList] = await Promise.all([
        fetchSubmissions(),
        fetchBidders(),
      ]);
      const bidderMap: Record<string, Bidder> = {};
      bidderList.forEach((b) => {
        bidderMap[b.id] = b;
      });
      setSubmissions(subList);
      setBidders(bidderMap);
      setLoading(false);
    }
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <FolderCheck className="w-5 h-5 text-emerald-600" />
            Bid Submissions Registry
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Submitted proposals bound to specific tender versions under evaluation
          </p>
        </div>
      </div>

      {/* Submissions Table */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-400">Loading bid submissions...</div>
        ) : submissions.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">No submissions recorded.</div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                <th className="py-3 px-4">Submission Ref</th>
                <th className="py-3 px-4">Bidder Entity</th>
                <th className="py-3 px-4">Tender Version</th>
                <th className="py-3 px-4">Submission Date</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Review</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {submissions.map((sub) => {
                const bidder = bidders[sub.bidder_id];
                return (
                  <tr key={sub.id} className="hover:bg-slate-50">
                    <td className="py-3.5 px-4 font-mono font-bold text-slate-900">
                      {sub.submission_reference}
                    </td>
                    <td className="py-3.5 px-4 font-medium text-slate-800">
                      {bidder ? bidder.bidder_name : sub.bidder_id}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-600">
                      {sub.tender_version_id.substring(0, 10)}...
                    </td>
                    <td className="py-3.5 px-4 text-slate-600">
                      {new Date(sub.submission_date).toLocaleDateString()}
                    </td>
                    <td className="py-3.5 px-4">
                      <StatusBadge status={sub.status} />
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/bids/${sub.id}`}
                        className="bg-navy-900 hover:bg-gov-blue text-white text-xs font-semibold py-1.5 px-3 rounded transition-colors"
                      >
                        Review Proposal
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
