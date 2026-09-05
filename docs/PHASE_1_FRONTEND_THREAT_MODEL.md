# Phase 1 — Frontend STRIDE Threat Model Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Threat Model Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & UI Threat Boundary

This specification defines the STRIDE threat model specifically targeting frontend client components, browser storage, user sessions, document rendering, and prompt injection display vectors.

---

## 2. STRIDE Frontend Threat Matrix

| Threat ID | STRIDE Category | Threat Description & Vector | Mitigation Architecture Control | Residual Risk |
|---|---|---|---|---|
| **FE-TH-01** | **Spoofing** | Session hijacking via stolen JWT session cookie | HTTP-Only, SameSite=Strict cookies; mandatory MFA | Low |
| **FE-TH-02** | **Tampering** | Client-side DOM manipulation of compliance status badge | Backend FastAPI enforces all authorizations & determinations | Low |
| **FE-TH-03** | **Repudiation** | Officer claims UI decision was recorded accidentally | Mandatory written justification rationale + re-authentication modal | Low |
| **FE-TH-04** | **Info Disclosure** | Unmasked PII or sensitive bid prices leaked via screenshot | Automatic PII masking, watermarking, explicit classification badges | Medium |
| **FE-TH-05** | **DoS** | Browser crash via rendering 1000-page un-virtualized PDF | PDF canvas virtualization, page rendering limits | Low |
| **FE-TH-06** | **Elevation of Priv** | Hidden UI action buttons executed by un-privileged role | Backend RBAC API validation on every endpoint invocation | Low |
| **FE-TH-07** | **Injection (XSS)** | Untrusted extracted document text executes malicious JS in DOM | DOMPurify HTML sanitization, strict CSP headers (`script-src 'self'`) | Low |
| **FE-TH-08** | **Prompt Injection UI** | Malicious text in PDF tricks user via visual prompt injection | Visual isolation boxes, clear "Untrusted Bidder Text" visual warning | Medium |

---

## 3. Threat Mitigation Principles

1. **Client-Side Untrusted Boundary:** All data rendered from external uploads or LLM extractions is treated as untrusted and sanitized before insertion into the DOM tree.
2. **Zero Client Trust:** Frontend UI state manipulation cannot bypass backend security enforcement.
