# Phase 1 — Document Extraction UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Document Extraction UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Extraction Verification Scope

This specification defines the UI components for displaying AI-extracted fields, confidence score indicators, human verification buttons, and field correction input forms.

---

## 2. Document Extraction Verification Panel

```
+-----------------------------------------------------------------------------------+
| EXTRACTION VERIFIER: Audited Balance Sheet FY 2023-24 (#DOC-8812)                  |
+-----------------------------------------------------------------------------------+
| Field Name      | Extracted Value | AI Confidence | Verification Status | Action |
|-----------------+-----------------+---------------+---------------------+--------|
| Annual Turnover | Rs. 62.4 Crores | 96% (High)    | VERIFIED_BY_OFFICER | [Edit] |
| Net Worth       | Rs. 18.2 Crores | 92% (High)    | AI_EXTRACTED        | [Verify|Edit] |
| UDIN Number     | 24089123A8912B  | 74% (Yellow)  | REQUIRES_REVIEW     | [Inspect] |
+-----------------------------------------------------------------------------------+
| FIELD CORRECTION MODAL (Triggered on [Edit])                                     |
| Field: UDIN Number                                                                |
| Original Extracted Value: 24089123A8912B (AI Confidence: 74%)                     |
| Officer Verified Value:  [ 24089123A8912C                   ]                    |
| Reason for Correction:   [ Typo in last character digit     ]                    |
| [ Save & Record Override ]  [ Cancel ]                                            |
+-----------------------------------------------------------------------------------+
```

---

## 3. Human Correction & Audit Logging

1. **Non-Destructive Overrides:** Human corrections **DO NOT** delete the original AI extraction record (`DocumentExtraction`). They create a linked `ManualOverride` record.
2. **Audit Attribution:** Every human edit captures `Officer User ID`, `Timestamp`, `Old Value`, `New Value`, and `Reason`.
