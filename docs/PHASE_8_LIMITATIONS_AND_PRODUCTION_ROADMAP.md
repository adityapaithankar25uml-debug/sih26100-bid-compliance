# Phase 8 — Limitations & Production Onboarding Roadmap

## Executive Statement

In accordance with strict architectural governance, this document provides an honest separation between the **Current Demonstration Prototype** and the **Production Deployment Roadmap**.

---

## 1. Current Demonstration Prototype Capabilities vs. Production Roadmap

| Architectural Domain | Current Demonstration Prototype | Production Target Roadmap | Production Onboarding Path |
|---|---|---|---|
| **Government Portal Integration** | 12 Statutory Registries integrated using normalized `GovernmentSourceAdapter` interfaces running `MOCK / DEMO` sandbox payloads | Production REST API / Web Service calls to GST, Udyam, EPFO, ESIC, MCA, etc. | Authorized onboarding and integration with required government sources and identity/consent systems |
| **Authentication & Identity** | JWT Authentication with seeded demo accounts (`officer@cpcl.gov.in`, etc.) | Enterprise Single Sign-On / identity provider integration | Integration with single sign-on / identity providers |
| **Digital Decision Sign-Off** | Backend decision recording in database with SHA-256 event audit logging | Digital certificate (e-Sign) signing for final award decisions | Integration with authorized digital certificate signing services |
| **AI LLM Gateway** | Schema-enforced structured JSON parser connected to cloud / mock gateway | Enterprise LLM engines running within private infrastructure | Cloud / local enterprise AI infrastructure provisioning |
| **Audit Log Persistence** | PostgreSQL canonical table with prev_hash SHA-256 linked block lineage | Read-only / append-only audit storage anchoring | Read-only / append-only audit storage integration |
| **Infrastructure Deployment** | Docker Compose stack running locally (PostgreSQL, Redis, MinIO, FastAPI, Next.js) | High-availability cluster deployment | Deployment on an authorized government-approved cloud/infrastructure environment with appropriate WAF/network controls |

---

## 2. Four-Stage Production Roadmap

```
[STAGE 1: Authorized Onboarding & Integration]
  ├── Authorized onboarding and integration with required government sources and identity/consent systems
  ├── Configure mTLS authentication, IP whitelisting, and API keys
  └── Integrate single sign-on / identity providers for officer authentication

[STAGE 2: Security Assessment & Compliance Review]
  ├── Independent security assessment, penetration testing, and applicable government security/compliance review
  ├── Conduct OWASP Top 10 penetration testing on APIs and Next.js frontend
  └── Validate data privacy compliance for configured data categories

[STAGE 3: Cloud Infrastructure & High-Availability Deployment]
  ├── Deployment on an authorized government-approved cloud/infrastructure environment with appropriate WAF/network controls
  ├── Setup PostgreSQL multi-AZ replication, Redis cluster, and distributed object storage
  └── Configure WAF, network controls, and rate-limiting gateways

[STAGE 4: Future Authorized Pilot & GeM System Integration]
  ├── Retain CPCL / GeM pilot as a future authorized pilot objective
  ├── Train procurement officers and senior reviewers on platform operation
  └── Execute integration alignment with relevant procurement portal technical teams
```

---

## 3. Honest Limitations Summary

1. **Mock Data Scope:** For this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype.
2. **Digital Signature Status:** The audit mechanism verifies hash-chain integrity but does not itself constitute a PKI digital signature or legal non-repudiation mechanism.
3. **OCR Scale Limits:** The prototype PDF parser is optimized for standard bid documents (< 50 pages). Production deployment requires distributed worker queues for 500+ page tenders.
