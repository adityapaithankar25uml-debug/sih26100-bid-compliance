'use client';
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { FileText, ArrowLeft, Layers, CheckSquare, Clock } from 'lucide-react';
import { fetchTenderById } from '../../../lib/api';
import { Tender } from '../../../types';
import { StatusBadge } from '../../../components/StatusBadge';

export default function TenderDetailPage() {
  const params = useParams();
  const tenderId = params?.id as string;
  const [tender, setTender] = useState<Tender | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (tenderId) {
      fetchTenderById(tenderId).then((data) => {
        setTender(data);
        setLoading(false);
      });
    }
  }, [tenderId]);

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-400">Loading tender workspace...</div>;
  }

  if (!tender) {
    return (
      <div className="p-8 text-center text-xs text-slate-500">
        Tender not found or removed. <Link href="/tenders" className="text-gov-blue underline">Back to catalog</Link>
      </div>
    );
  }

  const activeVersion = tender.versions?.[0];
  const requirements = activeVersion?.requirements || [];

  return (
    <div className="space-y-6">
      <Link href="/tenders" className="text-xs font-semibold text-gov-blue hover:underline flex items-center gap-1">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Tender Catalog
      </Link>

      {/* Header Info */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <span className="font-mono text-xs font-bold text-gov-blue bg-gov-light px-2.5 py-1 rounded border border-blue-200">
              {tender.tender_number}
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-2">{tender.title}</h2>
          </div>
          <StatusBadge status={tender.status} />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-3 border-t border-slate-100 text-xs">
          <div>
            <span className="text-slate-500 block">Organization</span>
            <span className="font-semibold text-slate-800">{tender.organization}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Total Versions</span>
            <span className="font-semibold text-slate-800 font-mono">{tender.versions?.length || 1}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Active Version</span>
            <span className="font-semibold text-slate-800 font-mono">v{activeVersion?.version_number || 1}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Created On</span>
            <span className="font-semibold text-slate-800">
              {new Date(tender.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Requirements List */}
        <div className="lg:col-span-2 bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-3">
            <CheckSquare className="w-4 h-4 text-gov-blue" />
            Tender Requirements (Version {activeVersion?.version_number || 1})
          </h3>

          {requirements.length === 0 ? (
            <div className="p-6 text-center text-xs text-slate-400">
              No requirements cataloged for this tender version yet.
            </div>
          ) : (
            <div className="space-y-3">
              {requirements.map((req) => (
                <div key={req.id} className="p-4 bg-slate-50 rounded border border-slate-200 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                      {req.requirement_code}
                    </span>
                    <div className="flex items-center space-x-2 text-xs">
                      <span className="bg-slate-200 text-slate-700 text-[10px] px-2 py-0.5 rounded font-mono">
                        {req.category}
                      </span>
                      {req.is_mandatory ? (
                        <span className="bg-rose-100 text-rose-800 text-[10px] font-bold px-2 py-0.5 rounded">
                          MANDATORY
                        </span>
                      ) : (
                        <span className="bg-slate-100 text-slate-600 text-[10px] px-2 py-0.5 rounded">
                          OPTIONAL
                        </span>
                      )}
                    </div>
                  </div>
                  <p className="text-xs text-slate-700 leading-relaxed font-medium">
                    {req.requirement_text}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Version History Sidebar */}
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-3">
            <Layers className="w-4 h-4 text-indigo-600" />
            Version History
          </h3>

          <div className="space-y-3">
            {tender.versions?.map((ver) => (
              <div
                key={ver.id}
                className="p-3 bg-slate-50 rounded border border-slate-200 text-xs space-y-1"
              >
                <div className="flex items-center justify-between font-semibold text-slate-900">
                  <span>Version {ver.version_number}</span>
                  {ver.is_finalized && (
                    <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded">
                      Finalized
                    </span>
                  )}
                </div>
                <p className="text-slate-600 text-[11px]">{ver.description}</p>
                <div className="text-[10px] text-slate-400 pt-1 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {new Date(ver.publish_date).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
