# Phase 1 — UI Security Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 UI Security Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & UI Security Boundary

This specification defines client-side security controls, Content Security Policy (CSP) headers, anti-clickjacking headers, sanitization of untrusted extracted text, and secret isolation boundaries.

---

## 2. Client-Side Security Safeguards

1. **Content Security Policy (CSP):** Strict CSP directives (`default-src 'self'`, `script-src 'self'`, `object-src 'none'`, `frame-ancestors 'none'`) preventing cross-site scripting (XSS) and clickjacking attacks.
2. **Untrusted Text HTML Sanitization:** Extracted document text, OCR outputs, and prompt responses pass through strict DOMPurify sanitization before rendering in DOM, preventing XSS injection through untrusted bidder file uploads.
3. **Zero Secrets in Frontend:** API keys, database credentials, government portal passwords, and private signing keys are **STRICTLY PROHIBITED** from appearing in frontend JavaScript bundles, HTML source, or client console logs.
4. **Re-Authentication for Consequential Actions:** Recording final qualification decisions (`QUALIFIED`/`NOT_QUALIFIED`) or executing manual overrides requires explicit password re-authentication modal confirmation.
