# Phase 1 — Bid Submission UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Bid Submission UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Ingestion UI Scope

This specification defines the UI views for tracking bid submission ingestion status, package extraction progress, file manifest validation, and ingestion error recovery.

---

## 2. Bid Submission Ingestion Monitor

```
+-----------------------------------------------------------------------------------+
| INGESTION TRACKER: Bid Submission #SUB-9021 (Bidder: Beta Controls Inc)          |
| Ingestion Mode: AUTOMATED_GEM_FEED | Ingestion Timestamp: 2026-08-26 14:22:10 IST  |
+-----------------------------------------------------------------------------------+
| PACKAGE INGESTION PIPELINE PROGRESS                                              |
| [1. Ingestion Check] -> [2. Virus Scan] -> [3. CDR Disarm] -> [4. OCR/Extract] -> [5. Ready]
|      COMPLETE                COMPLETE          COMPLETE           IN_PROGRESS         PENDING
+-----------------------------------------------------------------------------------+
| MANIFEST FILE EXTRACTOR STATUS                                                   |
| File Path in Package            | Format | Status      | Extracted Fields Count |
|---------------------------------+--------+-------------+------------------------|
| /docs/turnover_cert.pdf         | PDF    | COMPLETED   | 6 Fields Extracted     |
| /docs/past_performance_po.pdf   | PDF    | IN_PROGRESS | Processing Page 4/12   |
| /docs/corrupt_file.docx         | DOCX   | CONVERTED   | Sanitized & Disarmed   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Ingestion Error Handling UI

1. **Malware Quarantine Alert:** If a file fails virus scanning, the UI displays a high-visibility security alert: `"Malware virus signature detected in upload. File permanently quarantined."`
2. **Sanitization Derivative Indicator:** Clarifies whether a document viewer displays the raw original file or the disarmed sanitized derivative.
