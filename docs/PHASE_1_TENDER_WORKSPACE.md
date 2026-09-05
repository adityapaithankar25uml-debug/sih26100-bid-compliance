# Phase 1 — Tender Workspace Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Tender Workspace Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Workspace Scope

This specification defines the Tender Workspace layout, version switching UI, corrigendum history tracking, requirement configuration tabs, and submitted bidder list displays.

---

## 2. Tender Workspace Layout Topology

```
+-----------------------------------------------------------------------------------+
| TENDER HEADER: Tender #CPCL/2026/894 — High-Pressure Valves Supply                 |
| Version Active: TenderVersion v2.1 (Corrigendum 2) | PolicyVersion: POL-2026-v1.4    |
+-----------------------------------------------------------------------------------+
| TABS: [ Overview & Amendments ] [ Requirements (14) ] [ Bidders (6) ] [ Matrix ]   |
+-----------------------------------------------------------------------------------+
| TAB CONTENT: Overview & Corrigenda History                                         |
| - Original Tender Published: 2026-08-01 (TenderVersion v1.0)                      |
| - Corrigendum 1 Issued: 2026-08-15 (TenderVersion v2.0 - Extended Submission Date)|
| - Corrigendum 2 Issued: 2026-08-20 (TenderVersion v2.1 - Revised Turnover Rule)  |
|                                                                                   |
| BIDDERS EVALUATION PROGRESS                                                       |
| Bidder ID   | Company Name       | Submission Date | Progress | Status Badge      |
|-------------+--------------------+-----------------+----------+-------------------|
| BID-101     | Alpha Valves Ltd   | 2026-08-25      | 100%     | EVALUATED         |
| BID-102     | Beta Controls Inc  | 2026-08-26      |  75%     | PENDING_GOVT_GSTN |
| BID-103     | Gamma Heavy Engg   | 2026-08-27      |  50%     | REQUIRES_HUMAN    |
+-----------------------------------------------------------------------------------+
```

---

## 3. Version Transparency Rules

1. **Explicit Version Displays:** Every tab displays the active `TenderVersion` and `PolicyVersion` bound to the evaluation.
2. **Corrigenda Change Diff Visualizer:** When a tender corrigendum is selected, changed requirements are highlighted in amber with a side-by-side diff showing previous vs updated rule criteria.
