# Phase 1 — Government Integration Security Architecture

## Overview

The **Government Integration Security Architecture** defines the defense-in-depth framework protecting external government API integrations, cryptographic credentials, bidder PII, and system state within the **SIH26100 Bid Compliance Verification Platform**.

This architecture strictly enforces four isolated security boundaries, zero-trust external payload handling, credential isolation, and pre-AI privacy enforcement.

---

## 1. Four Isolated Security Boundaries

To prevent privilege escalation, token confusion, and unauthorized data access, the platform enforces strict separation across four distinct security zones:

```
+-----------------------------------------------------------------------------------+
| ZONE 1: USER AUTHENTICATION BOUNDARY                                              |
| * JWT tokens issued to Procurement Officers / Admins                              |
| * Identity Provider: Keycloak / OAuth2 / Internal RBAC                            |
+-----------------------------------------------------------------------------------+
                                          │ (Isolated)
                                          ▼
+-----------------------------------------------------------------------------------+
| ZONE 2: BIDDER CONSENT & AUTHORIZATION BOUNDARY                                   |
| * Explicit authorization tokens granted by Bidders for data retrieval             |
| * OAuth2 Scopes / DigiLocker Consent Artefacts / Aadhaar e-KYC consent            |
+-----------------------------------------------------------------------------------+
                                          │ (Isolated)
                                          ▼
+-----------------------------------------------------------------------------------+
| ZONE 3: APPLICATION SYSTEM AUTHORIZATION BOUNDARY                                 |
| * Internal service-to-service mTLS & API Gateway tokens                           |
| * Role-Based & Attribute-Based Access Control (RBAC/ABAC)                         |
+-----------------------------------------------------------------------------------+
                                          │ (Isolated)
                                          ▼
+-----------------------------------------------------------------------------------+
| ZONE 4: GOVERNMENT SOURCE AUTHENTICATION BOUNDARY                                 |
| * G2G & Enterprise API Gateway Credentials (mTLS Certs, OAuth Client Secrets)    |
| * Injected dynamically into adapter runtimes from Secret Management Boundary     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Secret Management & Credential Isolation Boundary

### 2.1 Core Credential Axiom
> **ZERO SECRETS IN CODE, VERSION CONTROL, DATABASE, OR DOCUMENTATION.**
> API keys, OAuth client secrets, mTLS private keys, signing certificates, and gateway credentials must never be committed to Git repositories, saved in PostgreSQL database fields, or embedded in documentation examples.

```
+-----------------------------------------------------------------------------------+
| HARDENED SECRET STORE (AWS Secrets Manager / HashiCorp Vault)                     |
| * Encrypted at rest (AES-256-GCM / KMS)                                          |
| * Dynamic Secret Rotation & Least-Privilege IAM Policies                          |
+-----------------------------------------------------------------------------------+
                                          │
                                          │ (Secure Runtime Environment Injection)
                                          ▼
+-----------------------------------------------------------------------------------+
| ADAPTER RUNTIME ENVIRONMENT                                                       |
| * In-Memory Access Only (Never written to disk or logged)                        |
| * Scoped credentials loaded per verification invocation                           |
+-----------------------------------------------------------------------------------+
```

---

## 3. Defense-in-Depth Technical Controls

### 3.1 Network Transport Security
* **Mandatory TLS 1.3:** All outgoing network connections to government gateways require TLS 1.3 (or minimum TLS 1.2 with standard cipher suites).
* **Strict Certificate Validation:** System HTTP clients validate certificate authority (CA) chains and hostname identity. Self-signed certificates are rejected in production.
* **Mutual TLS (mTLS):** Where required by G2G gateways (e.g., GSTN/API Setu), client certificates and private keys are presented via hardware security modules (HSM) or secure vault integration.

### 3.2 Server-Side Request Forgery (SSRF) Protection
External adapters must be prevented from making arbitrary calls to internal network addresses:

```
[Adapter Dispatch Request]
           │
           ▼
┌────────────────────────────────────────────────────────┐
│ Endpoint Allowlist Validator                           │
├────────────────────────────────────────────────────────┤
│ • Validates target URL against `SourceRegistry`         │
│ • Rejects private IPs (10.0.0.0/8, 172.16.0.0/12, etc.)│
│ • Rejects loopback addresses (127.0.0.1, localhost)     │
│ • Blocks DNS rebind attacks via resolved IP check      │
└────────────────────────────────────────────────────────┘
           │
           ├──────────────────────────┐
           ▼ (Valid External URL)     ▼ (Disallowed / Internal IP)
[Execute External HTTP Call]   [Block & Emit Security Alert]
```

### 3.3 Untrusted External Payload Handling
Government responses are treated as **untrusted external input**:
1. **Schema Validation:** All JSON/XML responses pass through strict Pydantic parsing schemas before internal consumption.
2. **Executable Code Sanitization:** Payload content is stripped of HTML/JavaScript tags to prevent cross-site scripting (XSS) when rendered in officer workbenches.
3. **Configurable Payload Size Limits:** Response payload limits are configurable per source, adapter, endpoint, and documented source constraints (e.g., default 10 MB payload safety threshold for buffer protection).

---

## 4. Privacy Gateway & Pre-AI PII Enclosure

To comply with the Digital Personal Data Protection Act (DPDP Act 2023) and system data security specifications:

```
[Government Response Payload]
              │
              ▼
┌────────────────────────────────────────────────────────┐
│ PRE-AI PRIVACY GATEWAY                                 │
├────────────────────────────────────────────────────────┤
│ • Identifies sensitive PII (Aadhaar, Bank AC, PAN)     │
│ • Applies Deterministic Masking / Tokenization         │
│ • Generates Anonymized Context Payload                 │
└────────────────────────────────────────────────────────┘
              │
              ├──────────────────────────┐
              ▼                          ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│ Deterministic Engine      │  │ External AI Gateway       │
│ Receives FULL Verified    │  │ Receives MASKED Payload   │
│ Data for Rule Evaluation  │  │ for Summarization Only    │
└───────────────────────────┘  └───────────────────────────┘
```

### 4.1 Masking Standards
* **Aadhaar Numbers:** Masked to last 4 digits (`XXXX-XXXX-1234`).
* **Bank Account Numbers:** Masked to last 3 digits (`XXXXXXXXX123`).
* **Personal Phone / Email:** Masked (`j***@domain.com`, `+91-XXXXX-67890`).
* **PAN Identifiers:** Masked in AI prompts (`ABCXX1234X`), fully preserved in encrypted transactional database tables.
