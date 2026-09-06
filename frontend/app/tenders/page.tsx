'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { FileText, Plus, Search } from 'lucide-react';
import { fetchTenders } from '../../lib/api';
import { Tender } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export default function TendersPage() {
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchTenders().then((data) => {
      setTenders(data);
      setLoading(false);
    });
  }, []);

  const filtered = tenders.filter(
    (t) =>
      t.tender_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-5 h-5 text-gov-blue" />
            Procurement Tender Catalog
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Registry of active procurement tenders and version amendments
          </p>
        </div>
      </div>

      {/* Filter and Actions */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search tender number or title..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:border-gov-blue"
          />
        </div>
      </div>

      {/* Tenders Table */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-400">Loading tender catalog...</div>
        ) : filtered.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">No tenders match search criteria.</div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                <th className="py-3 px-4">Tender Number</th>
                <th className="py-3 px-4">Title</th>
                <th className="py-3 px-4">Organization</th>
                <th className="py-3 px-4">Active Version</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Workspace</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((t) => (
                <tr key={t.id} className="hover:bg-slate-50">
                  <td className="py-3.5 px-4 font-mono font-bold text-slate-900">
                    {t.tender_number}
                  </td>
                  <td className="py-3.5 px-4 font-medium text-slate-800 max-w-md">{t.title}</td>
                  <td className="py-3.5 px-4 text-slate-600 font-mono">{t.organization}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-700">
                    Version {t.versions?.length || 1}
                  </td>
                  <td className="py-3.5 px-4">
                    <StatusBadge status={t.status} />
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <Link
                      href={`/tenders/${t.id}`}
                      className="bg-navy-900 hover:bg-gov-blue text-white text-xs font-semibold py-1.5 px-3 rounded transition-colors"
                    >
                      Open Workspace
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
