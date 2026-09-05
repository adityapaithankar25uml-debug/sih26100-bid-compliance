# Phase 1 — Infrastructure Data Classification & Placement Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Data Classification Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification maps system data classifications to infrastructure storage tiers, encryption controls, and access boundaries aligned with Task 8.

---

## 2. Infrastructure Data Placement Matrix

| Data Classification Tier | Infrastructure Target Asset | Encryption Standard | Access Restriction |
|---|---|---|---|
| **PUBLIC** | CloudFront Edge CDN / Static S3 | None (Public Assets) | Read-only public HTTP access |
| **INTERNAL** | App Config / Non-Sensitive Metrics | In-transit TLS 1.2+ | Authenticated application containers |
| **CONFIDENTIAL** | Normalized Facts, Evaluation Snapshots | PostgreSQL Storage AES-256 | App service accounts via connection pooler |
| **RESTRICTED** | Raw Bid Documents, Financials | KMS-SSE S3 Encrypted Buckets | Disarmed sandbox workers & authorized officers |
| **PII** | Tax PAN, GSTIN Details, Officer ULIDs | Field-Level AES-256-GCM + KMS | Pre-AI Privacy Gateway & Officer Workbench |

---

## 3. Data Exposure Prevention Controls

1. **Zero PII in Infrastructure Logs:** Telemetry pipelines scrub raw document contents and PII before log emission.
2. **Zero Secrets in Public Buckets:** S3 bucket policies enforce `BlockPublicAccess = TRUE` across all non-public buckets.
