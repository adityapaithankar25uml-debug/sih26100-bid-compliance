# Phase 1 — Environment Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Environment Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the environment architecture, tier isolation rules, data classification boundaries, and integration profile configurations across four discrete system environments: `LOCAL`, `DEVELOPMENT`, `TEST_STAGING`, and `PRODUCTION`. 

The core environment boundary rule is:
> **"Production data MUST NEVER automatically flow into lower environments. Development and testing tiers strictly operate on synthetic or sanitized test data fixtures with mock/sandbox government adapters."**

---

## 2. Four-Tier Environment Matrix

| Architectural Property | `LOCAL` Tier | `DEVELOPMENT` Tier | `TEST_STAGING` Tier | `PRODUCTION` Tier |
|---|---|---|---|---|
| **Primary Objective** | Local developer testing & feature coding | Shared integration testing & continuous build validation | Staging verification, user acceptance testing & pre-release performance bench | Production bid compliance verification operations for CPCL |
| **Hosting Environment** | Developer workstation (Docker Desktop / Compose) | Cloud Dev VPC / Shared Cloud Compute | Isolated Staging VPC | Dedicated Multi-AZ Production VPC |
| **Data Classification** | Synthetic mock fixtures only | Synthetic mock data & anonymized test bids | Synthetic UAT bid submissions | Restricted live procurement bids & government payloads |
| **Govt Adapter Mode** | `MOCK` mode exclusively | `MOCK` / `SANDBOX` modes | `SANDBOX` / `MOCK` modes | `LIVE` / `MANUAL_FALLBACK` modes |
| **AI Gateway Mode** | Local Ollama / Mock Provider | Staging Cloud AI Sandbox | Staging Cloud AI Sandbox | Enterprise Cloud AI / Dedicated On-Prem vLLM |
| **Secrets Management** | Local `.env.example` file (Zero real secrets) | Cloud Dev Secrets Manager | Staging Secrets Manager | Production KMS & Secrets Manager (KMS Envelope) |
| **Network Exposure** | Localhost loopback (`127.0.0.1`) | Private VPC (VPN access only) | Private VPC with restricted UAT Gateway | Isolated VPC with WAF edge protection |
| **Observability Level** | Local console output & debug logs | Centralized Dev APM & debug logs | Full staging metrics, traces & alerts | Production APM, security monitoring & audit chain |
| **Deployment Gate** | Developer local execution | Automated Git push trigger | Automated PR merge gate + QA approval | Dual-control administrative approval |

---

## 3. Data Flow & Sanitization Boundaries

```mermaid
flowchart LR
    ProdDB[(\"Production DB (Restricted Bids & PII)\")] -- "STRICT BARRIER: Zero Direct Sync" --> DevEnv["Lower Environments (Dev / Staging)"]
    
    SynthData[\"Synthetic Data Generator\"] --> DevEnv
    Anonymizer[\"Governed Data Anonymization Engine\"] -->|Explicit Approval & Scrubbing| DevEnv
```

---

## 4. Environment Configuration Isolation Rules

1. **Strict Subnet Separation:** Production VPC subnets share zero routing tables, peering links, or security groups with lower environment VPCs.
2. **Credential Immutability:** Secrets, tokens, and DB passwords generated for production are cryptographically distinct from lower environment credentials.
3. **Database Isolation:** Production PostgreSQL databases reside in dedicated AWS Multi-AZ instances; lower environments use separate isolated database instances.
4. **Government Gateway Isolation:** Production `LIVE` credentials and mTLS certificates are accessible strictly within the production integration adapter subnet.
