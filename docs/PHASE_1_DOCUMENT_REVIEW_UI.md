# Phase 1 — Document Review UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Document Review UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Document Review Scope

This specification defines the document review workflow, metadata inspector, document security status banners, and PII masking controls.

---

## 2. Document Review Split Panel Topology

```
+-----------------------------------------------------------------------------------+
| DOCUMENT REVIEW: Financial_Statements_FY24.pdf (Document ID: #DOC-8812)            |
| Classification: CONFIDENTIAL | Security: SANITIZED DERIVATIVE | Hash: 8a9f2...c01  |
+--------------------------------------------------+--------------------------------+
| LEFT PANEL: Document PDF Viewer Canvas          | RIGHT PANEL: Metadata & Fields |
| +----------------------------------------------+ | Document Category: Financial   |
| | Page 3 of 18                                 | | Upload Date: 2026-08-25        |
| |                                              | | OCR Status: HIGH_ACCURACY    |
| |  INCOME STATEMENT FY 2023-24                 | |                              |
| |  Total Revenue: [ Rs. 62.4 Crores ] <------| | EXTRACTED FIELDS (AI Assistant)|
| |  Net Profit:    [ Rs.  8.1 Crores ]          | | - Turnover: Rs. 62.4 Cr       |
| |                                              | |   Confidence: 96% | [Verify] |
| +----------------------------------------------+ | - Net Profit: Rs. 8.1 Cr       |
|                                                  |   Confidence: 94% | [Verify] |
+--------------------------------------------------+--------------------------------+
```

---

## 3. Security & Provenance Controls

1. **Original vs Derivative Distinction:** The UI displays explicit badges indicating whether the viewer is displaying the original raw file or a sanitized derivative.
2. **PII Masking Toggle:** Authorized officers can toggle PII masking to view or redact sensitive personal data (Aadhaar numbers, PAN holder personal addresses) per Task 8 privacy rules.
