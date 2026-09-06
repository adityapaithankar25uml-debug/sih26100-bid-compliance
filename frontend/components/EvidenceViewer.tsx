import React from 'react';
import { StatusBadge } from './StatusBadge';

export interface EvidenceItemProps {
  fieldName: string;
  extractedValue: string;
  sourceDocumentName: string;
  sourceDocumentHash?: string;
  pageNumber: number;
  boundingBox?: {
    x0: number;
    y0: number;
    x1: number;
    y1: number;
  };
  extractionMethod: string;
  provenanceRef?: string;
}

export const EvidenceViewer: React.FC<{ evidenceList: EvidenceItemProps[] }> = ({ evidenceList }) => {
  if (!evidenceList || evidenceList.length === 0) {
    return (
      <div className="p-4 bg-slate-50 border border-slate-200 rounded text-slate-500 text-sm">
        No evidence items available for this document.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-slate-800 uppercase tracking-wider">
        Traceable Evidence Provenance ({evidenceList.length} Extracted Fields)
      </h3>
      <div className="overflow-x-auto border border-slate-200 rounded-lg">
        <table className="min-w-full divide-y divide-slate-200 bg-white text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Field</th>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Extracted Value</th>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Source File</th>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Page</th>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Bounding Box</th>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-600 uppercase">Method</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {evidenceList.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium text-slate-900">{item.fieldName}</td>
                <td className="px-4 py-3 font-mono text-slate-800 bg-slate-50/50 rounded">{item.extractedValue}</td>
                <td className="px-4 py-3 text-slate-600 font-mono text-xs">{item.sourceDocumentName}</td>
                <td className="px-4 py-3 text-slate-700">Page {item.pageNumber}</td>
                <td className="px-4 py-3 text-xs font-mono text-slate-500">
                  {item.boundingBox
                    ? `[${item.boundingBox.x0.toFixed(0)}, ${item.boundingBox.y0.toFixed(0)}, ${item.boundingBox.x1.toFixed(0)}, ${item.boundingBox.y1.toFixed(0)}]`
                    : 'N/A'}
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={item.extractionMethod === 'AI_GATEWAY' ? 'AI_EXTRACTED' : 'DETERMINISTIC'} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
