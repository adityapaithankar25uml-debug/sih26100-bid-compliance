# Phase 1 — Secrets Management Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Secrets Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the secret management architecture, key management system (KMS) integration, secret rotation policies, and secret injection mechanics for the platform.

The non-negotiable secret management rule is:
> **"Zero secrets in code, repositories, container images, or telemetry. All runtime credentials, API tokens, certificates, and database keys are injected dynamically via KMS-encrypted secret vaults."**

---

## 2. Secrets Management Topology

```mermaid
graph TD
    subgraph KMS_Vault ["AWS KMS & Secrets Manager (KMS Envelope Encryption)"]
        KMS_Key["Customer Master Key (CMK)"]
        Secret_DB["`sih26100/prod/postgres` Credentials"]
        Secret_Redis["`sih26100/prod/redis` Auth Token"]
        Secret_AI["`sih26100/prod/ai-providers` API Keys"]
        Secret_Govt["`sih26100/prod/govt-adapters` Certificates"]
    end

    subgraph Runtime_Tasks ["ECS Task Execution Containers"]
        App_Task["FastAPI API Task"]
        Worker_Task["Celery Worker Task"]
    end

    KMS_Key --> Secret_DB
    KMS_Key --> Secret_Redis
    KMS_Key --> Secret_AI
    KMS_Key --> Secret_Govt

    Secret_DB -->|Inject at Container Startup| App_Task
    Secret_Redis -->|Inject at Container Startup| Worker_Task
    Secret_AI -->|Inject at Container Startup| App_Task
    Secret_Govt -->|Inject at Container Startup| Worker_Task
```

---

## 3. Secret Inventory & Governance Matrix

| Secret Identifier | Secret Classification | Rotation Frequency | Access Policy |
|---|---|---|---|
| **`sih26100/prod/postgres`** | Database Credentials | 60 Days (Automated Rotation) | ECS App Task Role & Database Migration Task Role |
| **`sih26100/prod/redis`** | Redis AUTH Token | 90 Days | ECS App Task Role & Celery Worker Task Role |
| **`sih26100/prod/ai-providers`** | Cloud AI API Keys | 30 Days | Pre-AI Privacy Gateway ECS Task Role |
| **`sih26100/prod/govt-adapters`**| Government Adapter mTLS Certs | Annual / On-Demand | Government Adapter Worker ECS Task Role |
| **`sih26100/prod/jwt-signing`**| JWT Signing Key Pair | 90 Days | FastAPI Authentication Task Role |

---

## 4. Secret Protection Rules

1. **Pre-Log Redaction:** The privacy-safe pre-log sanitization pipeline scrubs all secret strings matching key patterns before emitting operational telemetry.
2. **KMS Envelope Encryption:** Secret payloads in AWS Secrets Manager are encrypted using a dedicated AWS KMS Customer Master Key (CMK) with strict key access policies.
3. **Task IAM Scoping:** ECS task execution roles use least-privilege policies; worker containers cannot read administrative database migration credentials.
