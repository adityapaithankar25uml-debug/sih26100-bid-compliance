# Phase 1 — Error, Empty & Loading States Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Error/Empty/Loading States Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & State Representation

This specification defines the explicit UI designs for loading skeletons, empty data states, RFC 7807 machine-readable API error displays, and technical integration fallback notices.

---

## 2. UI State Component Specifications

### 2.1 Loading State Standard (Skeleton Screen)
- **Visual Design:** Low-contrast pulse animations (`#E2E8F0` shimmer) matching exact table and card geometries. Avoids jarring spinner layout shifts.

### 2.2 Empty State Standard
- **Visual Design:** Neutral icon, clear heading (`"No Pending Human Review Tasks"`), explanatory text, and primary call-to-action button (`"Return to Dashboard"`).

### 2.3 RFC 7807 Error Presentation Standard
- **Visual Design:** Clear error banner displaying RFC 7807 fields:
  - Title: `"Government Integration Gateway Unavailable"`
  - Status Code: `504 Gateway Timeout`
  - Detail: `"The external GSTN portal did not respond within the 10.0s timeout window."`
  - Correlation ID: `req_01J891A901`
  - Action Option: `[ Initiate Manual Verification Fallback ]`

### 2.4 Technical Fallback Representation Rule
- **CRITICAL RULE:** Unavailability of an external backend service is **NEVER** displayed as bidder non-compliance or qualification failure.

```
BAD:  [ GST VERIFICATION FAILED (Red Banner) ]
GOOD: [ MANUAL_FALLBACK_REQUIRED (Grey Neutral Banner - System Timeout) ]
```
