# Phase 1 — UI Data Classification Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Data Classification Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Data Display Governance

This specification defines how the UI presents data according to its sensitivity classification level (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, `PII`), enforcing visual security indicators and masking rules.

---

## 2. Classification Level Presentation Matrix

| Data Classification Level | Representative Data Types | UI Visual Indicator | Display & Masking Rules |
|---|---|---|---|
| **PUBLIC** | Tender Title, Tender Number, Closing Date | Blue Badge `[PUBLIC]` | Unrestricted display to authenticated portal users |
| **INTERNAL** | Evaluation Summaries, Aggregate Compliance | Slate Badge `[INTERNAL]` | Accessible to assigned Procurement Officers & Reviewers |
| **CONFIDENTIAL** | Audited Financials, Work Orders, Bid Prices | Amber Badge `[CONFIDENTIAL]`| Accessible to assigned evaluation committee members only |
| **RESTRICTED** | Proprietary IP, Security Clearances | Red Badge `[RESTRICTED]` | Requires explicit high-privilege role & audit log prompt |
| **PII** | Aadhaar Numbers, Personal PAN, Personal Addr | Purple Badge `[PII]` | Automatically masked (`XXXX-XXXX-1234`) with unmask button |

---

## 3. PII Masking & Unmasking Protocol

1. **Default Masked Display:** PII attributes automatically render masked by default across all screens.
2. **Audited Unmask Action:** Clicking "Unmask PII" requires a valid justification entry and logs an `AUDIT_PII_UNMASKED` event capturing `User ID`, `Attribute ID`, and `Justification`.
