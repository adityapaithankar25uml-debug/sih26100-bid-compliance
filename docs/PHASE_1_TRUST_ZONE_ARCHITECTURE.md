# Phase 1 — Infrastructure Trust Zone Architecture

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Trust Zone Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the infrastructure trust zones, security boundaries, and subsystem placement rules aligned with the Task 8 Security Architecture.

The core trust zone principle is:
> **"Data flow across trust zone boundaries requires explicit authentication, capability-based authorization, payload validation, and pre-log privacy scrubbing."**

---

## 2. Four-Tier Infrastructure Trust Zone Mapping

```mermaid
graph TD
    subgraph Zone_0 ["Zone 0: Public / Untrusted Internet Boundary"]
        PublicUsers["Bidder Browsers & Public Traffic"]
        ExtAPIs["External Govt Gateways & Cloud AI Providers"]
    end

    subgraph Zone_1 ["Zone 1: Controlled Ingress & Edge Buffer"]
        WAF_CF["AWS WAF / CloudFront Edge"]
        ALB_DMZ["Application Load Balancer (Public DMZ)"]
    end

    subgraph Zone_2 ["Zone 2: Trusted Application Core"]
        FastAPI_App["FastAPI Backend & Pre-AI Privacy Gateway"]
        Nextjs_App["Next.js Frontend SSR Server"]
        Celery_App["Celery Async DAG Orchestrator Workers"]
    end

    subgraph Zone_3 ["Zone 3: Restricted Data & Audit Sanctuary"]
        PostgreSQL_DB[(\"PostgreSQL Primary (pgvector + Audit Chain)\")]
        Redis_Store[(\"Redis Cache & Celery Broker\")]
        S3_Encrypted[(\"S3 Encrypted Evidence & Document Bucket\")]
        KMS_Vault["KMS & Secrets Manager Vault"]
    end

    Zone_0 -->|HTTPS / WAF Rules| Zone_1
    Zone_1 -->|mTLS / App SG| Zone_2
    Zone_2 -->|IAM / DB App Account| Zone_3
```

---

## 3. Subsystem Placement & Trust Boundaries

| Subsystem Component | Trust Zone Placement | Allowed Ingress Callers | Allowed Outbound Targets | Security Control |
|---|---|---|---|---|
| **Next.js Frontend** | Zone 2 (App Core) | Zone 1 (ALB Ingress) | Zone 2 (FastAPI API) | Static asset CDN, CSP headers, zero server secrets |
| **FastAPI Backend** | Zone 2 (App Core) | Zone 1 (ALB Ingress) | Zone 3 (DB, Redis, S3, KMS), Zone 0 (Govt/AI APIs via NAT) | OAuth2/JWT auth, 5D authorization matrix, rate limits |
| **Document Processing Workers** | Zone 2 (Sandbox) | Zone 2 (Celery Broker) | Zone 3 (S3 Scratch Bucket) | Restricted sandbox, no network egress, read-only FS |
| **AI Extraction Gateway** | Zone 2 (App Core) | Zone 2 (FastAPI) | Zone 0 (External LLM Providers) | PII tokenization, prompt injection scanner |
| **Government Integration Adapters** | Zone 2 (App Core) | Zone 2 (FastAPI) | Zone 0 (Authoritative Govt Portals) | Outbound static IP NAT, TLS 1.2+, mTLS certificates |
| **PostgreSQL Database** | Zone 3 (Sanctuary) | Zone 2 (FastAPI, Celery) | None | Append-only audit user, pgvector, AES-256 storage enc |
| **Redis Broker / Cache** | Zone 3 (Sanctuary) | Zone 2 (FastAPI, Celery) | None | TLS in-transit, AUTH token required, isolated subnets |
| **MinIO / S3 Object Storage** | Zone 3 (Sanctuary) | Zone 2 (FastAPI, Celery) | None | KMS-SSE encryption, bucket versioning, legal hold |
