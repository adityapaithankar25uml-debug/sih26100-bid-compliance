# Phase 1 Architecture Decision Records (ADRs)

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-005  
**Version:** 1.3.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## ADR Index

- [ADR-001: Modular Monolith Architecture Pattern](#adr-001-modular-monolith-architecture-pattern)
- [ADR-002: Python (FastAPI) Backend Framework](#adr-002-python-fastapi-backend-framework)
- [ADR-003: Next.js Presentation Framework](#adr-003-nextjs-presentation-framework)
- [ADR-004: Primary Relational Database Engine (PostgreSQL + JSONB + pgvector)](#adr-004-primary-relational-database-engine-postgresql--jsonb--pgvector)
- [ADR-005: S3-Compatible Object Storage for Documents (MinIO)](#adr-005-s3-compatible-object-storage-for-documents-minio)
- [ADR-006: Provider-Agnostic AI Abstraction Layer](#adr-006-provider-agnostic-ai-abstraction-layer)
- [ADR-007: Government Integration Adapter Pattern (4 Runtime Modes)](#adr-007-government-integration-adapter-pattern-4-runtime-modes)
- [ADR-008: Deterministic Python / Pydantic Rule Engine](#adr-008-deterministic-python--pydantic-rule-engine)
- [ADR-009: Tamper-Evident SHA-256 Hash-Chained Audit Ledger](#adr-009-tamper-evident-sha-256-hash-chained-audit-ledger)
- [ADR-010: Separation of Compliance Status, Qualification Outcome, Evidence Confidence, and Risk Scoring](#adr-010-separation-of-compliance-status-qualification-outcome-evidence-confidence-and-risk-scoring)
- [ADR-011: Mandatory Human-in-the-Loop Procurement Officer Decision Authority](#adr-011-mandatory-human-in-the-loop-procurement-officer-decision-authority)
- [ADR-012: Background Task Execution & Queue Technology (Celery + Redis)](#adr-012-background-task-execution--queue-technology-celery--redis)
- [ADR-013: Dual Identifier Strategy (Internal ULID + External UUIDv4)](#adr-013-dual-identifier-strategy-internal-ulid--external-uuidv4)
- [ADR-014: Relational Core Schema with Controlled JSONB and Optional pgvector](#adr-014-relational-core-schema-with-controlled-jsonb-and-optional-pgvector)
- [ADR-015: First-Class Immutable Evidence Ledger Model](#adr-015-first-class-immutable-evidence-ledger-model)
- [ADR-016: Tender, Rule, and Policy Temporal Versioning Architecture](#adr-016-tender-rule-and-policy-temporal-versioning-architecture)
- [ADR-017: Isolation of Tamper-Evident Audit Events from Application Domain Models](#adr-017-isolation-of-tamper-evident-audit-events-from-application-domain-models)
- [ADR-018: Strict Separation of Source Documents, Extracted Field Data, and Government Verification Payloads](#adr-018-strict-separation-of-source-documents-extracted-field-data-and-government-verification-payloads)
- [ADR-019: REST API Conventions and Resource Path Versioning (`/api/v1`)](#adr-019-rest-api-conventions-and-resource-path-versioning-apiv1)
- [ADR-020: Asynchronous Job Polling Pattern (`202 Accepted` + Celery Status Endpoint)](#adr-020-asynchronous-job-polling-pattern-202-accepted--celery-status-endpoint)
- [ADR-021: RFC 7807 Problem Details Error Payload Standard](#adr-021-rfc-7807-problem-details-error-payload-standard)
- [ADR-022: Dual Cursor and Page/Limit Pagination Strategy](#adr-022-dual-cursor-and-pagelimit-pagination-strategy)
- [ADR-023: Idempotency Key Enforcement via Redis for Mutative Jobs (`X-Idempotency-Key`)](#adr-023-idempotency-key-enforcement-via-redis-for-mutative-jobs-x-idempotency-key)
- [ADR-024: Pre-AI Privacy Gateway and Structured Schema Output Enforcement](#adr-024-pre-ai-privacy-gateway-and-structured-schema-output-enforcement)

---

### ADR-001: Modular Monolith Architecture Pattern
* **Context:** Platform requires 23 distinct functional capabilities. Microservices introduce excessive operational overhead for a hackathon team.
* **Decision:** Adopt the **Modular Monolith** pattern.
* **Reason:** Strict domain boundary separation inside a single deployment unit.

---

### ADR-002: Python (FastAPI) Backend Framework
* **Context:** Orchestrating AI OCR/NLP models and deterministic Pydantic validation.
* **Decision:** Select **Python (FastAPI)**.

---

### ADR-003: Next.js Presentation Framework
* **Context:** Workbench requires interactive split-screen document evaluation and PDF previewing.
* **Decision:** Select **Next.js 14+ / React (TypeScript)**.

---

### ADR-004: Primary Relational Database Engine (PostgreSQL + JSONB + pgvector)
* **Context:** Transactional domain entities and flexible metadata. PostGIS is explicitly excluded.
* **Decision:** Select **PostgreSQL 16+** (Relational core + JSONB + optional pgvector).

---

### ADR-005: S3-Compatible Object Storage for Documents (MinIO)
* **Context:** Encrypted PDF storage separated from PostgreSQL.
* **Decision:** Select **S3-Compatible Object Storage (MinIO)**.

---

### ADR-006: Provider-Agnostic AI Abstraction Layer
* **Context:** Preventing vendor lock-in for AI OCR and explanation generation.
* **Decision:** Adopt a **Unified `AIProviderInterface` Abstraction Layer**.

---

### ADR-007: Government Integration Adapter Pattern (4 Runtime Modes)
* **Context:** Supporting LIVE, SANDBOX, MOCK, and MANUAL verification modes with visual UI tagging.
* **Decision:** Adopt **Government Integration Adapter Pattern**.

---

### ADR-008: Deterministic Python / Pydantic Rule Engine
* **Context:** Compliance rules must be evaluated reproducibly without AI hallucination.
* **Decision:** Build a **Custom Deterministic Python / Pydantic Rule Engine**.

---

### ADR-009: Tamper-Evident SHA-256 Hash-Chained Audit Ledger
* **Context:** Legal and vigilance auditability.
* **Decision:** Implement a **Tamper-Evident SHA-256 Hash-Chained Audit Ledger**.

---

### ADR-010: Separation of Compliance Status, Qualification Outcome, Evidence Confidence, and Risk Scoring
* **Context:** Standardizing bidder evaluation results across four separate analytical dimensions.
* **Decision:** Adopt **Strict Four-Dimensional Separation**.

---

### ADR-011: Mandatory Human-in-the-Loop Procurement Officer Decision Authority
* **Context:** Legal accountability under Indian procurement law.
* **Decision:** Mandate **Human-in-the-Loop Decision Authority**.

---

### ADR-012: Background Task Execution & Queue Technology (Celery + Redis)
* **Context:** Heavy async operations (OCR extraction, document parsing, API calls).
* **Decision:** Select **Celery + Redis** as the single background task execution stack.

---

### ADR-013: Dual Identifier Strategy (Internal ULID + External UUIDv4)
* **Context:** High B-tree index insertion locality and security against enumeration attacks on public API routes.
* **Decision:** Adopt **Dual Identifier Strategy (Internal ULID + External UUIDv4)**.
* **Reason:** Internal primary keys use **26-character Crockford Base32 encoded ULIDs with lexicographically sortable, time-ordered representation**. ULIDs generally improve index locality compared with random UUIDv4 identifiers because their encoded values are time-ordered. They do not guarantee elimination of B-tree fragmentation or page splits. External UUIDv4 makes resource identifiers difficult to predict and reduces predictable identifier enumeration risk; it does NOT replace authentication, authorization, or object-level access control, which remain strictly mandatory.
* **Consequences:** All primary key columns use ULID; external public routes reference `external_id` (UUIDv4). Mandatory authorization checks remain enforced on all API endpoints.

---

### ADR-014: Relational Core Schema with Controlled JSONB and Optional pgvector
* **Context:** Designing PostgreSQL database schema structure across 11 Bounded Contexts.
* **Decision:** Adopt **Relational Core Schema with Controlled JSONB and Optional pgvector**.

---

### ADR-015: First-Class Immutable Evidence Ledger Model
* **Context:** Procurement decisions require explicit proof answering "What proves this compliance evaluation result?".
* **Decision:** Implement **First-Class Immutable Evidence Ledger Model**.

---

### ADR-016: Tender, Rule, and Policy Temporal Versioning Architecture
* **Context:** Historical procurement evaluations must remain 100% explainable and reproducible over time.
* **Decision:** Adopt **Five-Tier Temporal Versioning Architecture**.

---

### ADR-017: Isolation of Tamper-Evident Audit Events from Application Domain Models
* **Context:** Preventing corruption of audit logs and distinguishing infrastructure events from business domain entities.
* **Decision:** Implement **Isolation of Tamper-Evident Audit Events from Domain Models**.

---

### ADR-018: Strict Separation of Source Documents, Extracted Field Data, and Government Verification Payloads
* **Context:** Preventing confusion between raw uploaded files, AI/OCR interpretations, and authoritative government responses.
* **Decision:** Adopt **Strict Three-Layer Entity Separation**.

---

### ADR-019: REST API Conventions and Resource Path Versioning (`/api/v1`)
* **Context:** Designing standardized RESTful API endpoints for interaction between Next.js frontend, FastAPI domain modules, and audit services.
* **Options Considered:**
  1. GraphQL API interface.
  2. gRPC Protobuf interface.
  3. RESTful JSON API over HTTPS with major version in URI path (`/api/v1`).
* **Decision:** Adopt **RESTful JSON API over HTTPS with major URI versioning (`/api/v1`)**.
* **Reason:** REST provides clear HTTP verb semantics (`GET`, `POST`, `PUT`, `DELETE`), simple browser compatibility, easy OpenAPI specification generation, and clear cacheability for static resource lookups.
* **Consequences:** All client requests pass through `/api/v1` and use standard JSON request/response envelopes.
* **Rejected Alternatives:** GraphQL (rejected due to complex caching and security auditability overhead); gRPC (rejected due to browser client proxy overhead for Next.js frontend).

---

### ADR-020: Asynchronous Job Polling Pattern (`202 Accepted` + Celery Status Endpoint)
* **Context:** Heavy document OCR parsing, AI extraction, government verification API lookups, and report generation exceed HTTP request timeout thresholds (typically 10–30s).
* **Options Considered:**
  1. Synchronous long-polling HTTP requests holding open connections for 60+ seconds.
  2. WebSockets for all backend processing events.
  3. Asynchronous Job Polling Pattern: Return `202 Accepted` with `Location: /api/v1/jobs/{job_id}`, polling Redis job state asynchronously.
* **Decision:** Implement **Asynchronous Job Polling Pattern (`202 Accepted` + Status Endpoint)**.
* **Reason:** Completely eliminates HTTP request timeout crashes during multi-page PDF processing or external government gateway latency. Simple to implement over standard REST without WebSocket connection drop issues during network switches.
* **Consequences:** Long-running endpoints return `202 Accepted` immediately and dispatch background Celery tasks. Client polls status until `COMPLETED`.
* **Rejected Alternatives:** 60-second synchronous HTTP holding (rejected due to gateway timeouts); WebSockets (rejected due to firewall and connection drop fragility in government networks).

---

### ADR-021: RFC 7807 Problem Details Error Payload Standard
* **Context:** Standardizing machine-readable error responses across all API endpoints.
* **Options Considered:**
  1. Custom ad-hoc JSON error structures (`{"error": "message"}`).
  2. Standard RFC 7807 Problem Details payloads (`type`, `title`, `status`, `detail`, `instance`, `code`, `correlation_id`, `invalid_params`).
* **Decision:** Adopt **RFC 7807 Problem Details Standard**.
* **Reason:** Provides an internationally recognized, consistent error format. Automatically includes request correlation IDs for end-to-end log tracing and structured field-level validation errors.
* **Consequences:** All HTTP 4xx and 5xx error responses conform strictly to the `ProblemDetails` JSON schema.
* **Rejected Alternatives:** Ad-hoc JSON error formats (rejected due to inconsistent client error parsing).

---

### ADR-022: Dual Cursor and Page/Limit Pagination Strategy
* **Context:** Efficiently fetching large datasets (audit events, bidder submissions, tender lists) without database performance bottlenecks.
* **Options Considered:**
  1. OFFSET/LIMIT pagination for all endpoints.
  2. Dual Pagination Strategy: **Cursor-based pagination** (using ULID cursor keys) for append-heavy log streams; **Page/Limit pagination** for UI table views.
* **Decision:** Adopt **Dual Cursor and Page/Limit Pagination Strategy**.
* **Reason:** OFFSET pagination degrades to $O(N)$ performance on deep audit log tables because PostgreSQL must scan and discard $N$ rows. Cursor-based pagination over sequential ULID primary keys provides constant $O(1)$ B-tree index traversal. Page/Limit pagination is retained for small UI table lists (e.g. Tenders list).
* **Consequences:** Audit events, evidence records, and verification attempt streams require `cursor` parameters.
* **Rejected Alternatives:** Universal OFFSET pagination (rejected due to $O(N)$ database query degradation on deep audit logs).

---

### ADR-023: Idempotency Key Enforcement via Redis for Mutative Jobs (`X-Idempotency-Key`)
* **Context:** Preventing duplicate job execution or double submission when network retries occur on mutative endpoints (`POST /api/v1/verifications/request`, `POST /api/v1/tenders`).
* **Options Considered:**
  1. No idempotency checking; allow duplicate backend job execution.
  2. Client-supplied `X-Idempotency-Key` header cached in Redis with 24-hour TTL.
* **Decision:** Enforce **Idempotency Key Header (`X-Idempotency-Key`) for Mutative Endpoints**.
* **Reason:** Prevents duplicate external API calls to government portals (which may incur cost or rate limit penalties) and duplicate document OCR jobs when network reconnections trigger browser retries.
* **Consequences:** Backend intercepts mutative requests, checks Redis for existing key, and returns cached response if key exists.
* **Rejected Alternatives:** No idempotency protection (rejected due to risk of duplicate government API billing/rate limit exhaustion).

---

### ADR-024: Pre-AI Privacy Gateway and Structured Schema Output Enforcement
* **Context:** Protecting personal data (DPDP Act 2023) and guaranteeing that AI outputs do not produce unparseable free text or hallucinatory rule decisions.
* **Options Considered:**
  1. Direct unvalidated text streams to external AI models.
  2. Local Pre-AI Privacy Gateway (sensitivity classification, deterministic redaction, cloud eligibility check) + Strict Pydantic JSON Schema Output Enforcement.
* **Decision:** Implement **Pre-AI Privacy Gateway + Pydantic JSON Schema Output Enforcement**.
* **Reason:** Ensures sensitive personal PII is redacted prior to external AI transit while restricting AI output strictly to validated JSON schemas. Extracted values pass to deterministic Python code for rule evaluation — AI is NEVER allowed to compute pass/fail flags directly.
* **Consequences:** All AI responses must pass schema validation before ingestion into database domain models.
* **Rejected Alternatives:** Unsanitized AI streaming (rejected due to legal DPDP Act non-compliance and hallucination risks).
