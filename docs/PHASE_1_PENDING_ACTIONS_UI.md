# Phase 1 — Pending Actions UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Pending Actions Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Action Queue Scope

This specification defines the Pending Actions UI panel, organizing officer tasks by urgency, deadline proximity, and review category.

---

## 2. Pending Actions Queue Topology

```
+-----------------------------------------------------------------------------------+
| PENDING OFFICER ACTIONS (Filter: All Assigned Tenders | Total Actionable Items: 7) |
+-----------------------------------------------------------------------------------+
| Priority | Category    | Tender ID    | Bidder ID  | Required Action Description  |
|----------+-------------+--------------+------------+------------------------------|
| URGENT   | Shortfall   | CPCL/2026/01 | BID-102    | Issue 48hr Shortfall Notice  |
| HIGH     | Low AI UDIN | CPCL/2026/01 | BID-103    | Verify UDIN Extracted Digits |
| MEDIUM   | Stale Govt  | CPCL/2026/04 | BID-201    | Re-run GSTN Adapter Query    |
| NORMAL   | Override    | CPCL/2026/04 | BID-205    | Review Officer Exemption     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Action Categorization & Prioritization

1. **Urgency Sorting:** Action items automatically sort by evaluation closing deadline and review urgency (e.g., Shortfall notices expiring soon).
2. **Direct Workspace Linking:** Clicking any action item directly opens the relevant workspace tab with the target element highlighted.
