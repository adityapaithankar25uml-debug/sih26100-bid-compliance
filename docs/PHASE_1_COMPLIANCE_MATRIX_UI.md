# Phase 1 — Compliance Matrix UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Compliance Matrix Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Compliance Matrix Scope

This specification defines the multi-column, requirement-by-requirement Compliance Evaluation Matrix UI, supporting detailed evidence inspection, rule status badges, and multidimensional determination displays.

---

## 2. Compliance Matrix Layout Topology

```
+--------------------------------------------------------------------------------------------------------------------+
| COMPLIANCE MATRIX: Bidder #BID-409 (Alpha Engineering Pvt Ltd) | Tender #CPCL/2026/894 | Version: v2.1              |
+--------------------------------------------------------------------------------------------------------------------+
| Req ID   | Category    | Requirement Criteria | Evaluated Fact  | Rule Status  | Source & Evidence  | Action Trace |
|----------+-------------+----------------------+-----------------+--------------+--------------------+--------------|
| TR-FIN-01| Financial   | Min Turnover Rs 50Cr | Rs 62.4 Crores  | [ VERIFIED ] | Fin Statements.pdf | [Inspect Trace]|
| TR-TEC-02| Technical   | Similar Work Orders  | 3 Orders Found  | [ VERIFIED ] | Work_Orders.pdf    | [Inspect Trace]|
| TR-LEG-03| Commercial  | GST Active Status    | GSTIN Active    | [ VERIFIED ] | GSTN API (LIVE)    | [Inspect Trace]|
| TR-MSE-04| MSE Prefer. | Valid Udyam Cert     | Missing Cert    | [ MISSING ]  | Pending Submission | [Human Review]|
+--------------------------------------------------------------------------------------------------------------------+
```

---

## 3. Multidimensional Status Taxonomy Rules

The UI explicitly avoids collapsing evaluation statuses into binary PASS/FAIL. The matrix renders 10 distinct status badges:
1. `VERIFIED`: Deterministic rule satisfied with verified facts and valid evidence.
2. `UNVERIFIED`: Fact extracted but awaiting verification or officer confirmation.
3. `MISSING`: Required proof document or field not present.
4. `STALE`: Government verification data exceeds freshness threshold.
5. `CONFLICTING`: Document evidence conflicts with external registry fact.
6. `INVALID`: Verification failed valid format check.
7. `UNKNOWN`: Insufficient evidence to evaluate rule.
8. `NOT_APPLICABLE`: Requirement not applicable to bidder classification (e.g. MSE exemption).
9. `MISSING_EVIDENCE`: Missing document requirement (Routes to Human Review; **NEVER** auto-disqualifies).
10. `HUMAN_REVIEW`: Item flagged for officer manual inspection and decision.
