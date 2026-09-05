# Phase 1 — Exception & Conflict UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Exception UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Conflict Management

This specification defines the UI views for highlighting conflicting document evidence, identity discrepancies, and policy exception requests.

---

## 2. Evidence Conflict Resolver Panel Topology

```
+-----------------------------------------------------------------------------------+
| CONFLICT RESOLUTION WORKBENCH: Discrepancy Flagged on Bidder #BID-409             |
+-----------------------------------------------------------------------------------+
| CONFLICT DETECTED: Annual Turnover Values Disagree                                 |
| Source A (Audited Financial Statement PDF):   Rs. 62.4 Crores                     |
| Source B (GSTN Registry Annual Return API):   Rs. 58.1 Crores                     |
| Variance Discrepancy:                         7.4% Variance                       |
+-----------------------------------------------------------------------------------+
| RESOLUTION WORKFLOW                                                               |
| Officer Resolution Selection:                                                     |
| (o) Accept Audited Financial Statement as Authoritative (Provide Rationale)       |
| ( ) Accept GSTN Registry Figure as Authoritative                                 |
| ( ) Issue Clarification Notice to Bidder via GeM Portal                           |
|                                                                                   |
| Officer Resolution Rationale:                                                     |
| [ Audited financials include non-GST exempt export revenue accounted in FY24. ]   |
| [ Resolve Conflict ]  [ Escalate to Senior Reviewer ]                            |
+-----------------------------------------------------------------------------------+
```

---

## 3. Conflict Resolution Audit Rules

1. **Explicit Provenance Logging:** Conflict resolutions record which evidence source was accepted as authoritative and preserve the rejected source for auditor inspection.
2. **Four-Eyes Trigger on Large Variance:** Variances exceeding 15% automatically flag the resolution for `SENIOR_REVIEWER` supervisory review.
