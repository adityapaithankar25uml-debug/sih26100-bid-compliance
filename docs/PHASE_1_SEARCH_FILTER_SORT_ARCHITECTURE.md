# Phase 1 — Search, Filter & Sort Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Search/Filter Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Filter Architecture

This specification defines the enterprise search bar, faceted filtering drawer, multi-column sorting controls, and query parameter URL synchronization standards.

---

## 2. Faceted Search & Filter Panel Topology

```
+-----------------------------------------------------------------------------------+
| SEARCH & FILTER BAR                                                               |
| [ Search Bidders / Documents / Requirements...                      ] [ Search ]  |
+-----------------------------------------------------------------------------------+
| FACETED FILTERS (Active: Category = Financial | Status = REQUIRES_HUMAN_REVIEW)   |
| Category: [ All | Technical | Financial(X) | Legal | MSE ]                       |
| Status:   [ All | Verified | Unverified | Missing Evidence(X) | Stale ]           |
| Risk:     [ All | High Advisory | Medium Advisory | Low Advisory ]                |
| Tender Version: [ All | v2.1 (Active)(X) | v2.0 | v1.0 ]                            |
+-----------------------------------------------------------------------------------+
```

---

## 3. URL Synchronization & Security Safeguards

1. **Deep-Linkable Query Parameters:** Filter states synchronize with URL query parameters (e.g. `?category=FINANCIAL&status=REQUIRES_HUMAN_REVIEW`), enabling shareable deep links for authorized reviewers.
2. **RBAC Scope Enforcement:** Search results automatically enforce server-side RBAC scoping; unauthorized bids or sensitive documents are omitted from results.
