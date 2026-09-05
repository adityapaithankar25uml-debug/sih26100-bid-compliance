# Phase 1 — Procurement Officer Dashboard Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Dashboard Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Dashboard Mission

This specification defines the information layout, key performance indicators (KPIs), summary cards, work queues, and multidimensional status widgets for the Procurement Officer Dashboard.

The dashboard serves as the central operational hub for officers, providing real-time visibility into assigned tender evaluation progress without reducing compliance to a single, oversimplified score.

---

## 2. Dashboard Wireframe Layout Topology

```
+-----------------------------------------------------------------------------------+
| HEADER: Procurement Officer Dashboard | User: P. Officer (CPCL-89) | Date: 2026-09-06 |
+-----------------------------------------------------------------------------------+
| SUMMARY METRIC CARDS                                                              |
| [ Assigned Tenders: 4 ] [ Active Bids: 18 ] [ Pending Reviews: 5 ] [ Stale: 2 ]    |
+-----------------------------------------------------------------------------------+
| WORKLOAD QUEUES (Tabbed View: Assigned Tenders | Pending Actions | Recent Activity)|
|                                                                                   |
| Tender ID    | Title             | Closing Date | Bids | Progress | Status Badge  |
|--------------+-------------------+--------------+------+----------+---------------|
| CPCL/2026/01 | High-Pressure V/V | 2026-09-12   |  5   |  80%     | IN_EVALUATION |
| CPCL/2026/04 | Catalyst Supply   | 2026-09-18   |  3   |  40%     | PENDING_GOVT  |
+-----------------------------------------------------------------------------------+
| DUAL WIDGET SECTION                                                               |
| +-----------------------------------------+-------------------------------------+ |
| | PENDING HUMAN REVIEWS QUEUE             | ADVISORY RISK INDICATORS            | |
| | - Bidder #B-04: Missing GST Certificate | - Bidder #B-09: Financial Surge     | |
| | - Bidder #B-12: Ambiguous Identity      | - Bidder #B-02: Recent Incorporation| |
| +-----------------------------------------+-------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 3. Dashboard Information Widgets & Metrics

1. **Assigned Tenders Summary:** Active tenders assigned to officer with evaluation progress bars.
2. **Pending Actions Queue:** Immediate tasks requiring officer intervention (missing evidence, low-confidence extraction, stale verification).
3. **Multi-Dimensional Status Badges:** Displays compliance progress across separate indicators (`Evaluation Progress %`, `Pending Human Review Count`, `Government Verification Readiness`).
4. **Advisory Risk Indicator Widget:** Highlights bids flagged with high-risk advisory signals for officer investigation.
