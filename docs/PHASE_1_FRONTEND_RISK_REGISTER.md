# Phase 1 — Frontend Risk Register Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Risk Register Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & UI Risk Register

This specification defines the risk register for frontend user experience, usability, accessibility, and client-side security risks.

No pseudo-claims of "zero risk", "100% secure", or "perfect usability" are permitted.

---

## 2. Frontend Master Risk Register

| Risk ID | Category | Risk Description | Likelihood | Impact | Mitigation Strategy | Owner |
|---|---|---|---|---|---|---|
| **FE-RISK-01** | Usability | Officer misinterprets advisory risk score as automated disqualification | Medium | High | Mandatory disclaimers, distinct color coding, explicit non-disqualification banner | UX Lead |
| **FE-RISK-02** | Security | DOM-based XSS via malicious untrusted PDF OCR text insertion | Low | High | DOMPurify sanitization, CSP headers, strict React text node rendering | Security Lead |
| **FE-RISK-03** | Performance | Browser slowdown during side-by-side display of large PDF documents | Medium | Medium | PDF canvas page virtualization, memory limit controls, dynamic imports | Frontend Lead |
| **FE-RISK-04** | Accessibility | Keyboard navigation blocked in complex multi-column compliance table | Low | Medium | Full WCAG 2.1 AA keyboard testing, sticky columns, explicit ARIA grid roles | Accessibility Lead |
| **FE-RISK-05** | Reliability | Temporary government API timeout visually misinterpreted as bidder failure | Medium | High | Explicit technical failure banner (`MANUAL_FALLBACK_REQUIRED`), clear system notices | Product Owner |
