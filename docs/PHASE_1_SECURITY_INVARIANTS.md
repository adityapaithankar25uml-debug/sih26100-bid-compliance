# Phase 1 Mandatory Security & Architectural Invariants

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary & Enforcement Scope

This document codifies the non-negotiable security and architectural invariants established during Phase 1. These invariants define the technical constitution of the SIH26100 platform.

**Mandatory Directive for Phase 2 Implementation:**
These invariants represent design-level constraints. Any Phase 2 implementation code, API router, database migration, AI integration, or frontend component that violates these invariants shall be rejected during code review.

---

## 2. Core Architectural Invariants

### 2.1 INVARIANT-01: Absolute Non-Authoritative AI Boundary
- **Statement:** AI/LLM components are strictly advisory parsing assistants. AI output MUST NEVER directly generate a final compliance determination (`COMPLIANT` / `NON_COMPLIANT`), qualification outcome (`QUALIFIED` / `DISQUALIFIED`), or officer decision.
- **Enforcement Rule:** Every `ExtractedFact` entity output by the AI Gateway MUST carry `is_authoritative = False` and `confidence_score`. Final rule evaluation is performed exclusively by the deterministic AST Compliance Engine (Task 6), and final qualification authority rests exclusively with the Procurement Officer (Task 11).

---

### 2.2 INVARIANT-02: Backend-Authoritative Authorization Boundary
- **Statement:** The frontend user interface (Next.js/React) is an presentation layer and IS NOT a security boundary.
- **Enforcement Rule:** All authorization decisions (RBAC, role scopes, document access checks, override permissions) MUST be evaluated authoritatively on the FastAPI backend on every request. Frontend UI component visibility logic (e.g., hiding action buttons) is strictly cosmetic UX and must never be relied upon for security.

---

### 2.3 INVARIANT-03: Technical Government Failure Isolation
- **Statement:** Technical failure, connection timeout, HTTP `5xx` error, or rate-limiting of external official government APIs (GSTN, MCA21, UDIN, Udyam) MUST NEVER be evaluated as bidder non-compliance or cause automatic bid rejection.
- **Enforcement Rule:** Government API transport failures MUST output `verification_status = TECHNICAL_UNAVAILABLE` or `MANUAL_FALLBACK`. The compliance engine MUST map this to `UNVERIFIED_SOURCE` and flag the requirement for `HUMAN_REVIEW`.

---

### 2.4 INVARIANT-04: Non-Equivalence of Missing Evidence and Non-Compliance
- **Statement:** The absence of evidence (`MISSING_EVIDENCE`) is distinct from proven failure (`NON_COMPLIANT`).
- **Enforcement Rule:** When a required document or fact is missing, the compliance engine MUST emit `rule_status = MISSING_EVIDENCE`. It MUST NOT automatically generate a `NON_COMPLIANT` outcome unless the policy rule explicitly defines missing evidence as an absolute disqualifier after human review notice.

---

### 2.5 INVARIANT-05: Strict Separation of Direct AI and Government API Access
- **Statement:** LLMs, prompt pipelines, and AI agent frameworks MUST NEVER make direct network calls or transmit parameters to external government APIs.
- **Enforcement Rule:** All government verification calls MUST be dispatched through strongly-typed backend Python adapters (Task 5) executing inside controlled, egress-monitored VPC worker nodes. The AI Gateway has zero network egress routes to government endpoints.

---

### 2.6 INVARIANT-06: Absolute Prohibition of Credentials in Frontend & Client Logs
- **Statement:** Government integration credentials, AI provider API keys, DB connection strings, and KMS master keys MUST NEVER be exposed to the browser client or written to frontend telemetry.
- **Enforcement Rule:** Secrets are stored exclusively in AWS Secrets Manager / HashiCorp Vault and injected into backend worker environment variables. The frontend API client consumes backend proxy routes only (`/api/v1/verification/*`).

---

### 2.7 INVARIANT-07: Original vs. Derivative Document Isolation & Provenance
- **Statement:** Original bidder submitted documents must remain immutably isolated from sanitized derivative documents and extracted text blocks.
- **Enforcement Rule:** Original uploaded PDFs are stored in write-once-read-many (WORM) S3 buckets with `classification_level = ORIGINAL_RAW`. Processing pipelines and AI models operate exclusively on `SanitizedDerivative` objects produced after malware scanning and PII scrubbing (Task 8 §6).

---

### 2.8 INVARIANT-08: Cryptographic Tamper-Evident Audit Lineage
- **Statement:** System activities, evidence evaluation updates, officer overrides, and qualification decisions MUST be captured in a tamper-evident audit ledger.
- **Enforcement Rule:** Every `AuditEvent` record MUST calculate a SHA-256 cryptographic hash incorporating the `prev_hash` of the preceding record sequence (Task 8 §7.1). The audit ledger is append-only; update (`UPDATE`) and delete (`DELETE`) operations are strictly revoked on the audit database table.

---

### 2.9 INVARIANT-09: Advisory Multidimensional Risk Boundary
- **Statement:** Composite risk scores, financial ratio flags, and red-flag anomaly alerts generated by the AI/Risk pipeline are strictly advisory metadata.
- **Enforcement Rule:** A high risk score (`risk_score > 80.0`) MUST flag a bid for officer inspection, but MUST NOT independently alter deterministic compliance evaluation results or force bid disqualification.

---

### 2.10 INVARIANT-10: Non-Destructive Human Overrides with Mandatory Justification
- **Statement:** Procurement Officers possess the authority to override deterministic rule outcomes, but overrides MUST NEVER mutate or destroy underlying evidence.
- **Enforcement Rule:** Rule overrides create a new, distinct `RuleOverrideRecord` linking to the original `RuleEvaluationDetail`. Overrides require mandatory justification text ($\ge 50$ characters) and log a dedicated `RULE_OVERRIDDEN` event in the tamper-evident audit ledger.

---

## 3. Summary of Invariant Compliance Mandate

| Invariant ID | Title | Key Architectural Guardrail | Implementation Validation Method |
| :--- | :--- | :--- | :--- |
| **INVARIANT-01** | AI Non-Authoritative | `is_authoritative = False` on all facts | Automated Unit & Integration Tests |
| **INVARIANT-02** | Backend AuthZ | FastAPI JWT & RBAC dependency injection | Security Static Analysis (Bandit/Semgrep) |
| **INVARIANT-03** | Govt Failure Isolation | `TECHNICAL_UNAVAILABLE` $\rightarrow$ `HUMAN_REVIEW` | Mock Government Fault-Injection Tests |
| **INVARIANT-04** | Missing Evidence | `MISSING_EVIDENCE != FAIL` | Rules Engine Boundary Tests |
| **INVARIANT-05** | No Direct AI Egress | AI Gateway network isolation | Container VPC Egress Firewall Rules |
| **INVARIANT-06** | No Secrets in Frontend | Backend proxy architecture | Secret Scanner (GitLeaks/TruffleHog) |
| **INVARIANT-07** | Document Isolation | WORM S3 bucket policies | Object Storage Permission Audits |
| **INVARIANT-08** | Audit Hash Chain | SHA-256 chain calculation per log | Audit Hash Integrity Verification Worker |
| **INVARIANT-09** | Advisory Risk Score | Risk score strictly non-qualifying | Compliance Engine AST Code Review |
| **INVARIANT-10** | Non-Destructive Override | Append-only override record table | Database FK & Revocation Constraint Audits |

Phase 2 implementation must continuously validate compliance with these 10 invariants through automated CI/CD pipeline checks.
