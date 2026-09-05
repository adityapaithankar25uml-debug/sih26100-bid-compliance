# Phase 1 — Tender Requirement UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Tender Requirement UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Requirement Layout

This specification defines the UI view for inspecting individual tender requirements, bound rule definitions, required document types, and fact mapping criteria.

---

## 2. Tender Requirement Item View

```
+-----------------------------------------------------------------------------------+
| REQUIREMENT: TR-FIN-01 — Average Annual Financial Turnover                         |
| Category: Financial Qualification | Mandate: MANDATORY | Status: ACTIVE           |
+-----------------------------------------------------------------------------------+
| DESCRIPTION & RULE CRITERIA                                                        |
| Requirement Text: "The bidder must have an average annual turnover of at least     |
| Rs. 50 Crores during the last 3 financial years (FY 2022-23, 2023-24, 2024-25)."  |
|                                                                                   |
| BOUND DETERMINISTIC RULE DEFINITION (Policy Version: POL-2026-v1.4)                |
| Rule ID: RULE_FIN_TURNOVER_01                                                     |
| AST Expression: `avg(fact.turnover_fy23, fact.turnover_fy24, fact.turnover_fy25) >= policy.min_turnover_threshold` |
| Threshold Value: Rs. 500,000,000 (Rs. 50 Cr)                                      |
|                                                                                   |
| REQUIRED PROOF & SOURCE DOCUMENTS                                                 |
| 1. Audited Financial Statements (Balance Sheet & P&L) for FY 22-23, 23-24, 24-25. |
| 2. Chartered Accountant Certificate with valid UDIN number.                       |
+-----------------------------------------------------------------------------------+
```

---

## 3. Requirement Interaction Rules

1. **Rule AST Inspector Modal:** Officers can click "Inspect AST Rule" to view the underlying deterministic logic expression and bound policy parameter values.
2. **Category Grouping:** Requirements are grouped by category (Technical Capability, Financial Capacity, Commercial/Legal, Local Content MSE/MII, EMD Exemption).
