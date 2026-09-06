'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, FileText, FolderCheck, ShieldCheck, UserCheck, ShieldAlert, FileSearch, UploadCloud, Lock, UserCog } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  const navGroups = [
    {
      title: 'CORE PLATFORM',
      items: [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Tenders Catalog', href: '/tenders', icon: FileText },
        { name: 'Bid Submissions', href: '/bids', icon: FolderCheck },
      ]
    },
    {
      title: 'VERIFICATION & REVIEW',
      items: [
        { name: 'Government Verification', href: '/verification', icon: ShieldCheck },
        { name: 'Human Review Queue', href: '/human-review', icon: UserCheck },
        { name: 'Advisory Risk Engine', href: '/risk', icon: ShieldAlert },
      ]
    },
    {
      title: 'EVIDENCE & AUDIT',
      items: [
        { name: 'Evidence Explorer', href: '/evidence', icon: FileSearch },
        { name: 'Document Ingestion', href: '/documents/upload', icon: UploadCloud },
        { name: 'Tamper-Evident Audit', href: '/audit', icon: Lock },
      ]
    },
    {
      title: 'ACCOUNT & AUTH',
      items: [
        { name: 'Demo Account Login', href: '/login', icon: UserCog },
      ]
    }
  ];

  return (
    <aside className="w-64 bg-navy-900 text-slate-300 min-h-[calc(100vh-57px)] border-r border-navy-800 p-4 flex flex-col justify-between shrink-0">
      <div className="space-y-4">
        {navGroups.map((group) => (
          <div key={group.title} className="space-y-1">
            <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-1 font-mono">
              {group.title}
            </div>
            {group.items.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(`${item.href}`));
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-gov-blue text-white shadow-sm font-bold'
                      : 'text-slate-300 hover:bg-navy-800 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        ))}
      </div>

      <div className="bg-navy-850 rounded p-3 text-xs border border-navy-700 space-y-1 text-slate-400 mt-4">
        <div className="font-semibold text-slate-200 text-[11px] uppercase tracking-wider">System Axiom</div>
        <p className="text-[10px] leading-relaxed text-slate-400">
          <span className="text-gov-accent font-semibold">AI INTERPRETS</span> →{' '}
          <span className="text-emerald-400 font-semibold">SOURCES VERIFY</span> →{' '}
          RULES EVALUATE → EVIDENCE PROVES → RISK PRIORITIZES → <span className="text-white font-semibold">HUMAN DECIDES</span> → AUDIT REMEMBERS
        </p>
      </div>
    </aside>
  );
};

