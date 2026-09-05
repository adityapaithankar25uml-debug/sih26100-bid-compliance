# Phase 1 — Master Security Risk Register

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 8 Security Risk Register)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This document establishes the official Task 8 Security Risk Register for the SIH26100 platform. Deploying an AI-assisted bid compliance system within government procurement demands systematic identification and tracking of technical, operational, and architectural security risks.

The core risk management axiom is:
> **"Zero risk does not exist in software architecture. Security risk management requires transparent identification, rigorous controls, continuous detection, explicit ownership, and realistic residual risk evaluation."**

---

## 2. Risk Severity & Likelihood Evaluation Matrix

Risks are evaluated using a 5x5 Risk Rating Matrix mapping **Impact** (Critical, High, Medium, Low, Negligible) against **Likelihood** (Almost Certain, Likely, Possible, Unlikely, Rare):

$$\text{Risk Score} = \text{Likelihood Rating (1--5)} \times \text{Impact Rating (1--5)}$$

---

## 3. Exhaustive 18-Risk Security Register

| Risk ID | Risk Title & Description | Initial Impact | Likelihood Rationale | Architectural Controls (Tasks 1–7) | Mitigation Strategy (Task 8 Security) | Detection Mechanism | Residual Risk Level | Assigned Owner |
|---|---|---|---|---|---|---|---|---|
| **SR-01** | **Authentication Compromise**<br>Attacker compromises Procurement Officer session via token theft or phishing. | High | Possible (Phishing & social engineering targets human users) | OIDC/OAuth2 integration, short-lived JWT tokens (15-min lifetime). | Policy-controlled MFA, step-up auth for mutative actions, IP velocity checks. | Suspicious login alerts, IP location jump detection. | **Low** (Window limited to token expiration) | SecOps / Identity Team |
| **SR-02** | **Authorization Bypass**<br>User invokes restricted API endpoint or accesses bid outside assigned organization. | High | Unlikely (Modular monolith enforces authorization middleware) | 5-Dimensional authorization formula (`WHO`, `ACTION`, `RESOURCE`, `ORG`, `CLASSIFICATION`). | Mandatory capability checks on every API route handler; explicit default-deny policies. | API Gateway 403 Forbidden audit event alerts. | **Low** (Controlled by automated tests) | AppSec Engineering |
| **SR-03** | **Privilege Escalation**<br>Standard user escalates privileges to administrative or senior reviewer role. | High | Rare (Strict role separation in JWT claims) | Isolated role taxonomies (`ProcurementOfficer`, `SeniorReviewer`, `Auditor`). | Role hierarchy validation; JWT signature verification via public keys. | Audit event logging for privilege modification endpoints. | **Low** (Hardened by token signing) | Security Architect |
| **SR-04** | **Insider Threat**<br>Authorized Procurement Officer colludes with bidder to falsely pass non-compliant bid. | Critical | Possible (Human dishonesty in high-value procurement) | Mandatory `OfficerDecision` recording, evidence citation requirement, non-mutating overrides. | Policy-controlled four-eyes dual review for high-value bids; tamper-evident audit ledger tracking. | Anomaly detection on manual override frequency per officer. | **Medium** (Collusion between dual reviewers requires vigilance monitoring) | CPCL Vigilance Dept |
| **SR-05** | **Malicious File Upload**<br>Bidder uploads malware, executable macro, zip bomb, or polyglot file. | High | Likely (Untrusted external bidders submit thousands of files) | Untrusted file isolation, temporary quarantine bucket. | ClamAV malware scanning, MIME magic byte checks, CDR sanitization, sandboxed parsing. | Virus detection alerts, quarantine file rejection logs. | **Low** (Contained inside sandbox) | Infrastructure Team |
| **SR-06** | **Indirect Prompt Injection**<br>Hidden text in PDF instructions tricks LLM into outputting false facts. | High | Likely (Exploit vectors widely documented in AI applications) | Pre-AI Privacy Gateway, structured JSON schema output validation. | Document text tagged with `untrusted_content_source`; prompt injection regex scrubbers. | AI output schema failure logs, evidence grounding mismatch alerts. | **Medium** (Evolving LLM injection techniques require prompt updating) | AI Security Lead |
| **SR-07** | **AI Data Exfiltration**<br>Sensitive bidder PII or PAN numbers leaked to external LLM provider. | High | Possible (Standard LLM prompts pass full document text if unscrubbed) | Pre-AI Privacy Gateway, vendor-agnostic AI provider abstraction. | PII detection and tokenization before prompt assembly; zero data retention contracts. | Pre-AI scrubber audit metrics, redacted entity counts. | **Low** (Tokenization replaces raw values) | Data Privacy Officer |
| **SR-08** | **Government Credential Leak**<br>API keys or private mTLS certificates for MCA/GSTN exposed. | Critical | Unlikely (Secrets managed in environment / vault) | Government Integration Adapter isolation, Quad-Operating Modes. | `SecretManagerInterface` abstraction, zero secrets in Git/logs, secret rotation support. | Secret scanner tools in CI/CD pipeline, KMS access logs. | **Low** (Protected by secret vault) | SecOps / DevOps |
| **SR-09** | **API Abuse & DoS**<br>Attacker floods REST API endpoints with automated mutative requests. | Medium | Likely (Automated web bots scan public procurement portals) | REST `/api/v1` architecture, RFC 7807 error responses. | API Gateway leaky bucket rate limiting, IP throttling, `X-Idempotency-Key` headers. | API Gateway 429 Too Many Requests log spikes. | **Low** (Rate limiters throttle traffic) | Infrastructure Team |
| **SR-10** | **Database Compromise**<br>Attacker executes SQL injection or gains unauthorized DB connection. | Critical | Unlikely (SQLAlchemy ORM uses parameterized queries exclusively) | Relational core schema, ULID primary keys, separate audit roles. | Parameterized ORM queries only, least-privilege DB user accounts, AES-256 field encryption. | DB firewall alert logs, unexpected query pattern detection. | **Low** (Raw SQL prohibited) | Database Admin |
| **SR-11** | **Object Storage Exposure**<br>MinIO storage bucket configured with public read access. | High | Unlikely (MinIO S3 architecture defaults to private buckets) | MinIO S3-compatible document storage architecture. | Private bucket policy enforcement (`BucketAccessPolicy = PRIVATE`), short-lived pre-signed URLs. | Automated bucket policy compliance scanners. | **Low** (Public read access disabled) | Infrastructure Team |
| **SR-12** | **Redis Queue Poisoning**<br>Attacker injects malicious payloads into Celery Redis job queues. | Medium | Unlikely (Redis isolated in internal container network) | Background task execution using Celery + Redis. | Redis TLS 1.3 encryption, password authentication (`AUTH`), minimal task payload ULIDs. | Redis authentication failure alerts, DLQ depth spikes. | **Low** (Redis network isolated) | Systems Engineer |
| **SR-13** | **Audit Tampering Attempt**<br>Attacker or corrupt admin attempts to edit historical audit records. | Critical | Unlikely (SHA-256 hash chain links blocks sequentially) | Tamper-evident SHA-256 hash-chained audit ledger architecture. | Sequential hash linking ($H_n = \text{SHA256}(H_{n-1} \parallel P_n)$), append-only DB permissions. | Daily automated SHA-256 hash-chain verification job. | **Low** (Hash chain reveals alteration) | Lead Auditor / Vigilance |
| **SR-14** | **Supply Chain Vulnerability**<br>Malicious third-party Python package or container image dependency. | High | Possible (Modern applications rely on open-source packages) | Modular monolith package architecture. | Dependency vulnerability scanning, Software Bill of Materials (SBOM), base image pinning. | Automated dependency vulnerability alerts. | **Medium** (Requires regular patch governance) | DevOps Lead |
| **SR-15** | **Backup Compromise / Loss**<br>Database backups stolen or corrupted during disaster recovery storage. | High | Unlikely (Encrypted backups managed by infrastructure ops) | Encrypted storage architecture. | Encrypted backups (AES-256), access-controlled backup buckets, periodic restore testing. | Backup integrity verification job alerts. | **Low** (Backups encrypted at rest) | Infrastructure Team |
| **SR-16** | **Denial of Resource Exhaustion**<br>Large evaluation jobs exhaust server memory or CPU resources. | Medium | Possible (Multiple complex bids processed concurrently) | Celery task queue isolation, async worker architecture. | Worker container memory/CPU limits, task timeout enforcement, concurrency throttling. | Celery worker OOM alerts, resource utilization metrics. | **Low** (Workers isolated with RAM caps) | Operations Lead |
| **SR-17** | **Security Configuration Error**<br>Misconfigured environment settings (e.g., debug mode enabled in prod). | Medium | Possible (Human error during deployment configuration) | Configurable system parameter architecture. | Strict environment variable schema validation on startup; automated configuration audits. | App startup validation failure logs. | **Low** (Startup checks block invalid config) | SecOps Lead |
| **SR-18** | **Human Error in Overrides**<br>Procurement Officer misreads document and approves incorrect override. | Medium | Likely (Human operators make occasional mistakes) | Officer decision recording with mandatory rationale. | Human review workflow checkpoints; audit logging; senior reviewer signoff for high-risk overrides. | Audit trace reviews, officer decision discrepancy reports. | **Medium** (Inherent to human decision processes) | Department Management |

---

## 4. Residual Risk Mitigation Summary

The 18 identified security risks are actively managed through technical, architectural, and operational controls. Residual risk levels post-mitigation are summarized below:

- **Critical Residual Risks:** 0
- **Medium Residual Risks:** 4 (SR-04 Insider Collusion, SR-06 Indirect Prompt Injection, SR-14 Supply Chain Vulnerabilities, SR-18 Human Error in Overrides)
- **Low Residual Risks:** 14

All medium residual risks are assigned to explicit department leads for continuous operational monitoring, periodic vigilance audits, and prompt engineering updates.
