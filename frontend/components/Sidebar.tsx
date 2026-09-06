'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, FileText, FolderCheck, Lock, LogIn } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Tenders Catalog', href: '/tenders', icon: FileText },
    { name: 'Bid Submissions', href: '/bids', icon: FolderCheck },
    { name: 'Document Ingestion', href: '/documents/upload', icon: FileText },
    { name: 'Audit Hash Chain', href: '/audit', icon: Lock },
    { name: 'Role Switch / Auth', href: '/login', icon: LogIn },
  ];

  return (
    <aside className="w-64 bg-navy-900 text-slate-300 min-h-[calc(100vh-57px)] border-r border-navy-800 p-4 flex flex-col justify-between">
      <div className="space-y-1">
        <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-2">
          Procurement Workspace
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-gov-blue text-white shadow-sm'
                  : 'text-slate-300 hover:bg-navy-800 hover:text-white'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </div>

      <div className="bg-navy-800 rounded p-3 text-xs border border-navy-700 space-y-1 text-slate-400">
        <div className="font-semibold text-slate-300">Compliance Axiom</div>
        <p className="text-[11px] leading-relaxed text-slate-400">
          <span className="text-gov-blue font-semibold">AI INTERPRETS</span> →{' '}
          <span className="text-emerald-400 font-semibold">SOURCES VERIFY</span> →{' '}
          RULES EVALUATE → EVIDENCE PROVES → <span className="text-white font-semibold">HUMAN APPROVES</span>
        </p>
      </div>
    </aside>
  );
};
