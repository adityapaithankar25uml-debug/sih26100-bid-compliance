# Phase 1 — Bidder Workspace Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Bidder Workspace Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Bidder Workspace Scope

This specification defines the Bidder Workspace layout, submission summary views, document inventory panels, verification status widgets, and evaluation navigation controls for inspecting individual bidder submissions.

---

## 2. Bidder Workspace Layout Topology

```
+-----------------------------------------------------------------------------------+
| BIDDER WORKSPACE: Alpha Engineering Solutions Pvt Ltd (Bidder ID: #BID-409)       |
| Tender ID: CPCL/2026/894 | Submission Date: 2026-08-25 | GeM ID: GEM/2026/B/8912    |
+-----------------------------------------------------------------------------------+
| SUBSYSTEM STATUS SUMMARY                                                          |
| Compliance: 12/14 PASS | Govt Verifications: 3/4 LIVE | Risk: MEDIUM (Advisory)    |
+-----------------------------------------------------------------------------------+
| TABS: [ Compliance Matrix ] [ Documents (8) ] [ Govt Verifications ] [ Risk ]      |
+-----------------------------------------------------------------------------------+
| TAB CONTENT: Documents Inventory                                                  |
| Doc Name                | Category        | Size   | Malware Scan | SHA-256 Digest|
|-------------------------+-----------------+--------+--------------+---------------|
| Financial_Statements.pdf| Financial Proof | 4.2 MB | PASSED       | a8f9e2...31c  |
| GST_Certificate.pdf     | Legal / Tax     | 1.1 MB | PASSED       | 7b31c9...89f  |
| Past_Work_Orders.pdf    | Tech Experience | 8.9 MB | PASSED       | e291a0...44d  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Interaction Capabilities

1. **Document Viewer Trigger:** Clicking any document launches the Document Viewer UI with extraction overlays.
2. **Re-Run Verification:** Authorized officers can click "Re-Run Verification" to trigger updated government API queries or Celery rule evaluations.
