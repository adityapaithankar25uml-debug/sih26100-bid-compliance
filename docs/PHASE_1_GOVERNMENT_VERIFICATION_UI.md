# Phase 1 — Government Verification UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Government Verification UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Integration Status Scope

This specification defines the UI components for presenting authorized government integration verification results (PAN, GSTN, MCA21, Udyam MSME, CPPP) and managing technical failure states without misrepresenting them as bidder non-compliance.

---

## 2. Government Verification Matrix Topology

```
+-----------------------------------------------------------------------------------+
| GOVERNMENT REGISTRY VERIFICATION WORKBENCH (Bidder: Alpha Engineering Pvt Ltd)     |
+-----------------------------------------------------------------------------------+
| Registry Source | Endpoint Mode | Verification Status | Source Freshness | Action |
|-----------------+---------------+---------------------+------------------+--------|
| **Income Tax**  | LIVE Adapter  | VERIFIED (Matched)  | 2026-09-01 10:00 | [View] |
| **GSTN Portal** | LIVE Adapter  | VERIFIED (Active)   | 2026-09-01 10:02 | [View] |
| **MCA21 Corporate** | LIVE Gateway| VERIFIED (Active)   | 2026-09-01 10:05 | [View] |
| **Udyam MSME**  | MANUAL_FALLBACK| MANUAL_VERIFICATION | Pending Officer  | [Verify] |
| **EPFO Portal** | SANDBOX Mode  | MOCK_VERIFIED       | Sandbox Fixture  | [Info] |
+-----------------------------------------------------------------------------------+
| TECHNICAL FAILURE DISPLAY STANDARD (Example: MCA21 504 Timeout)                   |
| Status Badge: [ MANUAL_FALLBACK_REQUIRED (Grey Banner) ]                          |
| System Notice: "The MCA21 government registry API was temporarily unavailable      |
| (504 Gateway Timeout). This technical failure DOES NOT indicate bidder failure.   |
| Officer manual verification fallback workflow initiated."                         |
+-----------------------------------------------------------------------------------+
```

---

## 3. Critical UI Representation Rules

1. **Separation of Technical Failures:** A technical connection timeout (`502`/`503`/`504`) or source unavailability is **STRICTLY PROHIBITED** from rendering as "GST FAILED" or "BIDDER NON-COMPLIANT".
2. **Operating Mode Badges:** Every verification entry renders a clear mode badge (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`).
