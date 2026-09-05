# Phase 1 — Notification Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Notification Architecture Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Notification Framework

This specification defines the notification bell popover, toast alert system, task assignment alerts, and event notification preferences.

---

## 2. Notification System Topology

```
+-----------------------------------------------------------------------------------+
| NOTIFICATION POPOVER (Header Bell Icon: 3 Unread)                                  |
| [X] High Priority Only  [Mark All Read]                                           |
|-----------------------------------------------------------------------------------|
| 1. [URGENT] New Human Review Task Assigned: Bidder #BID-102 (Missing GST Cert)    |
|    Tender: #CPCL/2026/01 | 10 minutes ago | [Open Task]                         |
| 2. [INFO] Government GSTN Verification Completed (LIVE Mode)                      |
|    Bidder: #BID-409 | 25 minutes ago | [View Result]                            |
| 3. [ALERT] Stale Verification Flagged on PAN Adapter                              |
|    Tender: #CPCL/2026/04 | 1 hour ago | [Re-verify]                              |
+-----------------------------------------------------------------------------------+
```

---

## 3. Notification Rules & Suppression Controls

1. **Restrained Toast System:** Toast alerts appear in the top-right corner for high-priority operational updates only. Low-priority updates log quietly to the notification popover.
2. **Notification Fatigue Mitigation:** Duplicate alerts for identical background events are suppressed using event deduplication keys.
