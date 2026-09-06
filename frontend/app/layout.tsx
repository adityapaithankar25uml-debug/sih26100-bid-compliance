import './globals.css';
import React from 'react';
import { Navbar } from '../components/Navbar';
import { Sidebar } from '../components/Sidebar';

export const metadata = {
  title: 'SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform',
  description: 'Procurement Compliance Verification Platform for GeM Procurement',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 flex flex-col min-h-screen">
        <Navbar />
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1 p-6 overflow-y-auto max-w-7xl">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
