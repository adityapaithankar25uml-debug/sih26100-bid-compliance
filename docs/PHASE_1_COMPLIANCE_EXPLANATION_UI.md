# Phase 1 — Compliance Explanation UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Compliance Explanation UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Explainability Scope

This specification defines the compliance explainability panel, AST calculation trace visualizer, and step-by-step evaluation breakdown UI.

---

## 2. Compliance Explanation Modal Topology

```
+-----------------------------------------------------------------------------------+
| COMPLIANCE EXPLANATION: Requirement #TR-FIN-01 (Turnover Evaluation)              |
+-----------------------------------------------------------------------------------+
| 1. REQUIREMENT TEXT & THRESHOLD                                                   |
| Min Average Annual Turnover Required: Rs. 500,000,000 (Rs. 50 Crores)              |
|                                                                                   |
| 2. EVALUATED FACT VALUES (Extracted & Verified)                                    |
| - FY 2021-22 Turnover: Rs. 58.0 Crores (Source: Financial_Statements.pdf p.4)     |
| - FY 2022-23 Turnover: Rs. 61.2 Crores (Source: Financial_Statements.pdf p.4)     |
| - FY 2023-24 Turnover: Rs. 68.0 Crores (Source: Financial_Statements.pdf p.4)     |
|                                                                                   |
| 3. AST RULE CALCULATION TRACE                                                     |
| Calculated Average Turnover = (58.0 + 61.2 + 68.0) / 3 = Rs. 62.4 Crores         |
| Evaluation Comparison: Rs. 62.4 Crores >= Rs. 50.0 Crores -> TRUE                 |
| Rule AST Result: VERIFIED / COMPLIANT                                             |
+-----------------------------------------------------------------------------------+
```

---

## 3. Explainability Rules

1. **Deterministic Traceability:** Every rule determination explains the exact math, formula inputs, and comparison operators used.
2. **No Black-Box Output:** Explanations are generated from AST calculation execution traces, **NOT** LLM hallucinations.
