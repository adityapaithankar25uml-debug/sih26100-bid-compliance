# Phase 1 — Infrastructure Threat Model Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Threat Model Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines infrastructure-specific STRIDE threat vectors, attack surfaces, mitigations, and residual risk evaluations.

---

## 2. Infrastructure STRIDE Threat Matrix

| Threat ID | STRIDE Category | Threat Description & Attack Vector | Mitigation Architecture | Residual Risk |
|---|---|---|---|---|
| **INF-TH-01** | Spoofing | Adversary spoofs DNS or gateway IP to intercept outbound government API requests | TLS 1.2+ server certificate validation + static IP allowlisting | Low |
| **INF-TH-02** | Tampering | Compromised CI/CD runner alters container image binary before ECR push | Cosign OCI image signing + ECR immutability flags | Low |
| **INF-TH-03** | Repudiation | Rogue admin alters PostgreSQL database files directly to hide evidence tampering | KMS encrypted DB storage + SHA-256 external hash-chain audit log | Low |
| **INF-TH-04** | Info Disclosure | Unencrypted S3 bucket leaks raw bidder financial PDFs to public internet | S3 BlockPublicAccess + KMS-SSE bucket policies | Low |
| **INF-TH-05** | Denial of Service | Volumetric HTTP flood overwhelms API gateway load balancers | AWS WAF rate limits + CloudFront edge caching + AWS Shield | Low |
| **INF-TH-06** | Elevation of Priv | Container escape from untrusted PDF parser worker to host OS | ECS Fargate serverless execution, non-root user, read-only FS | Low |
