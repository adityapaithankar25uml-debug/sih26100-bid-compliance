# Phase 1 — Navigation Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Navigation Architecture Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Shell Layout Framework

This specification defines the global navigation structure, breadcrumb trail rules, persistent shell headers/footers, and context-preserving workspace transitions for the platform UI.

---

## 2. Global Application Shell Topology

```
+-----------------------------------------------------------------------------------+
| GLOBAL HEADER BAR: Logo | Portal Identity | Global Search | Role Badge | User Profile |
+-----------------------------------------------------------------------------------+
| BREADCRUMB BAR: Home > Tenders > Tender #CPCL/2026/894 > Bidder #BID-409 > Matrix |
+------------------+----------------------------------------------------------------+
| SIDE NAVIGATION  | MAIN WORKSPACE CONTENT AREA                                    |
| (Role-Filtered)  |                                                                |
| - Dashboard      | [Tender Header: Version v2.1 | Policy v1.4 | Security: INTERNAL]|
| - Tenders        |                                                                |
| - Bidders        | (Primary Dynamic View / Compliance Matrix / Document Viewer)   |
| - Reviews (3)    |                                                                |
| - Risk Matrix    |                                                                |
| - Audit Explorer |                                                                |
| - System Admin   |                                                                |
+------------------+----------------------------------------------------------------+
| SYSTEM FOOTER: Environment: PRODUCTION | System Version: 1.0.0 | Security Baseline  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Navigation Rules & Deep-Linking Standards

1. **Persistent Context Header:** Every evaluation view displays a fixed metadata bar containing `Tender ID`, `TenderVersion`, `PolicyVersion`, `Bidder ID`, and `Security Classification`.
2. **Breadcrumb Trail Lineage:** Breadcrumbs dynamically reflect workspace hierarchy (e.g., `Home` $\rightarrow$ `Tenders` $\rightarrow$ `Tender #104` $\rightarrow$ `Bidder #88` $\rightarrow$ `Requirement #TR-04` $\rightarrow$ `Evidence Trace`).
3. **Role-Filtered Side Navigation:** Sidebar options render based on backend authenticated JWT roles (`PROCUREMENT_OFFICER`, `SENIOR_REVIEWER`, `AUDITOR`, `SYSTEM_ADMIN`).
4. **State Preservation Across Transitions:** Navigating between document viewers and compliance matrices preserves scroll position, filter parameters, and active tab states.
