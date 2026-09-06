'use client';

import React, { useState } from 'react';
import { Navbar } from '../../../components/Navbar';
import { Sidebar } from '../../../components/Sidebar';
import { StatusBadge } from '../../../components/StatusBadge';

export default function DocumentUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [submissionId, setSubmissionId] = useState('SUB-2026-001');
  const [statusMsg, setStatusMsg] = useState('');
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setStatusMsg('Please select a procurement document file to upload.');
      return;
    }

    setIsProcessing(true);
    setStatusMsg('Uploading and performing quarantine malware scan...');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('bid_submission_id', submissionId);

      const token = localStorage.getItem('token') || 'demo-token';
      const res = await fetch('http://localhost:8000/api/v1/documents/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Upload failed');
      }

      const data = await res.json();
      setUploadResult(data);
      setStatusMsg('File uploaded, quarantine scan completed cleanly, and metadata persisted.');
    } catch (err: any) {
      setStatusMsg(`Upload Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Procurement Document Ingestion</h1>
        <p className="text-xs text-slate-500 mt-1">
          Securely upload tender or bidder documents for validation, malware scanning, classification, and AI extraction.
        </p>
      </div>

      <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg text-xs text-amber-900">
        <span className="font-bold">System Notice:</span> Extracted document facts and AI proposals are advisory candidates only. Final qualification decisions remain exclusively human-driven by the Procurement Officer.
      </div>


          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
              <h2 className="text-lg font-semibold text-slate-800">Upload Procurement File</h2>
              <form onSubmit={handleUpload} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">
                    Bid Submission ID
                  </label>
                  <input
                    type="text"
                    value={submissionId}
                    onChange={(e) => setSubmissionId(e.target.value)}
                    className="w-full px-3 py-2 border rounded border-slate-300 text-sm"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">
                    Select Document (PDF, DOCX, XLSX, Images)
                  </label>
                  <input
                    type="file"
                    onChange={handleFileChange}
                    accept=".pdf,.docx,.xlsx,.png,.jpg,.jpeg"
                    className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={isProcessing}
                  className="w-full py-2 px-4 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded text-sm disabled:opacity-50"
                >
                  {isProcessing ? 'Processing Ingestion...' : 'Upload & Scan Document'}
                </button>
              </form>

              {statusMsg && (
                <div className="p-3 rounded bg-slate-100 border border-slate-200 text-xs font-mono text-slate-700">
                  {statusMsg}
                </div>
              )}
            </div>

            {uploadResult && (
              <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
                <h2 className="text-lg font-semibold text-slate-800">Ingestion Result & Metadata</h2>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-slate-500">Document ID:</span>
                    <span className="font-mono text-xs font-bold text-slate-900">{uploadResult.document_id}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-slate-500">Original Filename:</span>
                    <span className="font-medium text-slate-900">{uploadResult.original_filename}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-slate-500">File Size:</span>
                    <span className="text-slate-900">{(uploadResult.file_size_bytes / 1024).toFixed(1)} KB</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-slate-500">SHA-256 Hash:</span>
                    <span className="font-mono text-xs text-slate-700">{uploadResult.sha256_hash.substring(0, 16)}...</span>
                  </div>
                  <div className="flex justify-between border-b pb-2 items-center">
                    <span className="text-slate-500">Quarantine Status:</span>
                    <StatusBadge status={uploadResult.quarantine_status} />
                  </div>
                  <div className="flex justify-between border-b pb-2 items-center">
                    <span className="text-slate-500">Malware Scan:</span>
                    <StatusBadge status={uploadResult.malware_scan_result} />
                  </div>
                  <div className="flex justify-between items-center pt-2">
                    <span className="text-slate-500">Security Classification:</span>
                    <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-slate-100 text-slate-800 border">
                      {uploadResult.security_classification}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
    </div>
  );
}

