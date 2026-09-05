# Phase 1 — Government Integration Risk Register

## Overview

The **Government Integration Risk Register** details technical, operational, legal, and security risks associated with connecting external government data sources and document verification pipelines to the **SIH26100 Bid Compliance Verification Platform**.

Each identified risk is paired with pre-architected mitigation strategies and continuous operational monitoring controls.

---

## 1. Master Integration Risk Matrix

| Risk ID | Risk Category | Risk Title & Description | Likelihood | Impact | Architectural Mitigation Strategy | Monitoring & Control Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-GOVT-01** | Technical | **Unannounced API Schema Revisions**<br>Government portal updates JSON/XML payload structures without notification, causing adapter parse failures. | High | Medium | Enforce strict Pydantic schema validation layers. Quarantine malformed payloads and fast-fail gracefully to `REQUIRES_MANUAL_VERIFICATION`. | Automated schema validation exception alerts dispatched to engineering team. |
| **RISK-GOVT-02** | Resilience | **Government Gateway Downtime / Outages**<br>Target portal (e.g., GSTN / MCA) experiences extended downtime or HTTP 503 maintenance spikes during tender closing. | High | High | Implement stateful Circuit Breakers, exponential backoff retries with full jitter, and automatic fallback to `MANUAL_FALLBACK` mode. | Prometheus latency metrics & circuit breaker open/close alerts. |
| **RISK-GOVT-03** | Operations | **API Rate Limit Exhaustion**<br>High-volume tender processing exhausts commercial GSP or API Setu rate quotas (HTTP 429). | Medium | Medium | Token Bucket rate limiters per adapter, request deduplication, and Celery worker queue throttling. | Redis token bucket fill-level telemetry & 429 error counters. |
| **RISK-GOVT-04** | Security | **Credential / Certificate Compromise**<br>mTLS client private keys or GSP OAuth client secrets expire or are exposed. | Low | High | Zero-secrets-in-code policy. Hardened secret store (AWS Secrets Manager / Vault) with automated rotation and KMS encryption. | Automated certificate expiry alerts (30-day notice) & audit logs. |
| **RISK-GOVT-05** | Data Integrity | **Stale Government Records**<br>Government database records are outdated (e.g., GST portal hasn't reflected recent cancellation). | Medium | High | Multi-tiered freshness policies (`POL_FRESHNESS`). Force live re-verification when evidence age exceeds policy window. | Evidence timestamp validation prior to rule evaluation. |
| **RISK-GOVT-06** | Compliance | **Fragmented Debarment Databases**<br>No single authoritative national debarment API exists, leading to missed blacklisting checks. | High | High | Multi-source debarment check scanning GeM, CPPP, and departmental registries + mandatory officer verification fallback. | Vigilance audit hash-chain logs tracking multi-registry checks. |
| **RISK-GOVT-07** | Privacy | **PII Exposure to External AI Models**<br>Unmasked bidder PII (Aadhaar, Bank AC, PAN) transmitted to cloud LLMs. | Medium | High | Enforce Pre-AI Privacy Gateway. Scrub, tokenize, or hash PII before forwarding context to external AI providers. | Automated privacy gateway pre-commit checks & payload scanners. |
| **RISK-GOVT-08** | Security | **Autonomous AI Boundary Violation**<br>AI LLM attempts to execute external API calls directly or modify verification outcomes. | Low | High | Enforce Non-Authoritative AI Axiom & zero direct tool execution permissions for LLMs. AI models lack adapter invocation rights. | AI Gateway permission isolation audit logging. |
| **RISK-GOVT-09** | Governance | **Misrepresentation of Mock Data**<br>Development or synthetic mock data represented as live government verification during evaluation. | Low | High | Quad-Operating Mode Strategy (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`). Prominent, un-bypassable visual badges on UI components. | Frontend render validation tests & audit mode logging. |
| **RISK-GOVT-10** | Integrity | **Officer Collusion in Manual Fallback**<br>Procurement Officer enters false manual verification details or attaches fraudulent evidence artifacts. | Low | High | Policy-configurable dual-verification (Four-Eyes Principle) for high-risk manual checks + mandatory SHA-256 evidence hashing and audit hash-chain logging. | Dual-officer sign-off verification & CVC vigilance audit trails. |
| **RISK-GOVT-11** | Security | **Server-Side Request Forgery (SSRF)**<br>Compromised adapter attempts external HTTP requests to internal network endpoints. | Low | High | Strict Endpoint Allowlisting in `SourceRegistry` + blocking private IP ranges (10.0.0.0/8, 127.0.0.1) at network client layer. | Outbound proxy access logs & egress firewall monitoring. |
| **RISK-GOVT-12** | Performance | **Payload Storage Exhaustion**<br>Large PDF response payloads from gateways exhaust database storage. | Medium | Low | Configurable payload size limits per source/adapter (e.g., default 10 MB payload safety threshold). Storing raw binary payloads in MinIO object storage; saving SHA-256 references in Postgres. | MinIO bucket storage quotas & alert metrics. |

---

## 2. Risk Governance & Escalation Framework

### 2.1 Escalation Matrix
1. **Low Technical Risk (e.g., transient timeout):** Handled automatically by retry algorithm / backoff.
2. **Medium Risk (e.g., rate limit, schema mismatch):** Routed to `REQUIRES_MANUAL_VERIFICATION`; alert dispatched to System Admin.
3. **High Security / Governance Risk (e.g., credential leak, debarment conflict):** Halts request execution, locks relevant tender requirement evaluation, and escalates immediately to **CPCL Vigilance Officer** and **Lead System Architect**.
