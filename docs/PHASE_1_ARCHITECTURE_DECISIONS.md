# Phase 1 Architecture Decision Records (ADRs)

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-005  
**Version:** 1.2.0  
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

---

### ADR-001: Modular Monolith Architecture Pattern
* **Context:** The platform requires 23 distinct functional capabilities. We must select an architectural pattern suitable for a student SIH team while maintaining enterprise standards.
* **Decision:** Adopt the **Modular Monolith** pattern.
* **Reason:** Microservices introduce excessive latency and multi-repo complexity for a 36-hour hackathon. A Modular Monolith delivers strict domain boundary separation inside a single deployment unit.
* **Consequences:** Code structure must enforce module encapsulation. Modules cannot directly bypass database boundaries of other modules.

---

### ADR-002: Python (FastAPI) Backend Framework
* **Context:** Backend must orchestrate AI OCR/NLP models, execute deterministic Pydantic validation, and handle async API calls.
* **Decision:** Select **Python (FastAPI)**.
* **Reason:** Provides native Python ecosystem integration (PyMuPDF, PaddleOCR, Pydantic), async request handling, and automatic OpenAPI schema generation.

---

### ADR-003: Next.js Presentation Framework
* **Context:** Workbench requires interactive split-screen document evaluation, side-by-side PDF previewing, and bounding-box overlays.
* **Decision:** Select **Next.js 14+ / React (TypeScript)**.
* **Reason:** Modern SSR capabilities, rapid UI rendering, and robust PDF viewer library integration.

---

### ADR-004: Primary Relational Database Engine (PostgreSQL + JSONB + pgvector)
* **Context:** Transactional domain entities (Tenders, Bidders, Requirements), ACID transaction integrity, and flexible metadata storage.
* **Decision:** Select **PostgreSQL 16+** configured with relational core tables, `JSONB` for controlled flexible metadata, and `pgvector` reserved *only where explicitly justified* for future semantic search on tender clauses. PostGIS is explicitly **excluded**.
* **Reason:** Provides relational integrity for decision auditability combined with native JSONB flexibility while eliminating unnecessary spatial extensions.

---

### ADR-005: S3-Compatible Object Storage for Documents (MinIO)
* **Context:** Multi-megabyte bidder PDF/JPEG document storage separated from the relational database.
* **Decision:** Select **S3-Compatible Object Storage (MinIO)**.
* **Reason:** Separates binary blob storage from PostgreSQL, supports AES-256 encryption, and provides standardized presigned URLs for UI PDF rendering.

---

### ADR-006: Provider-Agnostic AI Abstraction Layer
* **Context:** Preventing single-vendor lock-in for AI OCR text interpretation and explanation generation.
* **Decision:** Adopt a **Unified `AIProviderInterface` Abstraction Layer** supporting Cloud APIs (Gemini/OpenAI) and local offline LLMs (Ollama).

---

### ADR-007: Government Integration Adapter Pattern (4 Runtime Modes)
* **Context:** External government endpoints (GSTN, PAN, MCA, Udyam) have varying availability and authorization requirements.
* **Decision:** Implement **Government Adapter Pattern** supporting 4 runtime modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`) with mandatory provenance UI tagging (`[LIVE_VERIFIED]`, `[MOCK_SIMULATED]`, etc.).

---

### ADR-008: Deterministic Python / Pydantic Rule Engine
* **Context:** Compliance rules must be evaluated with 100% mathematical reproducibility under CVC audit guidelines.
* **Decision:** Build a **Custom Deterministic Python / Pydantic Rule Engine**.
* **Reason:** AI evaluation is non-deterministic and subject to hallucination. Python/Pydantic rules ensure zero hallucination risk.

---

### ADR-009: Tamper-Evident SHA-256 Hash-Chained Audit Ledger
* **Context:** Legal and vigilance auditability for procurement decisions.
* **Decision:** Implement a **Tamper-Evident SHA-256 Hash-Chained Audit Ledger**.
* **Terminology Rationale:** Uses technically accurate term **"tamper-evident audit trail"**. Hash chaining (`Hash_n = SHA256(Hash_{n-1} + Timestamp + Actor + Payload)`) provides immediate mathematical proof if any past log entry is altered, but does not prevent a root DB admin from rewriting the entire database without external WORM backing.

---

### ADR-010: Separation of Compliance Status, Qualification Outcome, Evidence Confidence, and Risk Scoring
* **Context:** Standardizing bidder evaluation results without conflating pass/fail rules with risk scores.
* **Decision:** Adopt **Strict Four-Dimensional Separation**:
  1. **Compliance Status:** Requirement-level status (`PASS`, `FAIL`, `REVIEW`, etc.).
  2. **Qualification Outcome:** Overall bidder status (`COMPLIANT`, `NOT COMPLIANT`, `PROVISIONAL`).
  3. **Evidence Confidence:** Metric (0.0 to 1.0) rating document clarity and API source authority.
  4. **Risk Score:** Independent analytical score (0.0 to 100.0) measuring anomalies, data conflicts, verification failures, and document irregularities.
* **Non-Interference Rule:** Risk score does NOT automatically force `Risk Score = 100` on a mandatory failure, nor can Risk Score independently qualify/disqualify a bidder.

---

### ADR-011: Mandatory Human-in-the-Loop Procurement Officer Decision Authority
* **Context:** Public procurement law dictates named human officer accountability.
* **Decision:** Mandate **Human-in-the-Loop Decision Authority**. The platform is strictly a Decision Support Workbench; the Procurement Officer must record final decisions with mandatory justification text.

---

### ADR-012: Background Task Execution & Queue Technology (Celery + Redis)
* **Context:** Heavy async operations (OCR extraction, document parsing, background verification calls).
* **Decision:** Select **Celery + Redis** as the single background task execution stack. Redis serves as central broker, task queue, and transient result/session cache with TTL.

---

### ADR-013: Dual Identifier Strategy (Internal ULID + External UUIDv4)
* **Context:** High B-tree index insertion locality and security against enumeration attacks on public API routes.
* **Options Considered:**
  1. Auto-increment Integer IDs (`1, 2, 3`).
  2. Standard random UUIDv4 for all primary keys.
  3. Dual Strategy: Internal ULID (`CHAR(26)`) + External UUIDv4.
* **Decision:** Adopt **Dual Identifier Strategy (Internal ULID + External UUIDv4)**.
* **Reason:** Internal primary keys use **26-character Crockford Base32 encoded ULIDs with lexicographically sortable, time-ordered representation**. ULIDs generally improve index locality compared with random UUIDv4 identifiers because their encoded values are time-ordered. They do not guarantee elimination of B-tree fragmentation or page splits. External UUIDv4 makes resource identifiers difficult to predict and reduces predictable identifier enumeration risk; it does NOT replace authentication, authorization, or object-level access control, which remain strictly mandatory.
* **Consequences:** All primary key columns use ULID; external public routes reference `external_id` (UUIDv4). Mandatory authorization checks remain enforced on all API endpoints.
* **Rejected Alternatives:** Integer IDs (rejected due to sequence leakage); UUIDv4 primary keys (rejected due to random B-tree page split performance degradation).

---

### ADR-014: Relational Core Schema with Controlled JSONB and Optional pgvector
* **Context:** Designing PostgreSQL database schema structure across 11 Bounded Contexts.
* **Options Considered:**
  1. Single giant JSON document table (MongoDB-style in Postgres).
  2. Strict relational normalization for core domain entities with controlled JSONB for metadata and pgvector for semantic clause retrieval.
  3. Multi-database hybrid (PostgreSQL + MongoDB).
* **Decision:** Adopt **Relational Core Schema with Controlled JSONB and Optional pgvector**.
* **Reason:** Relational tables enforce foreign key integrity for tenders, bidders, evidence, and officer decisions. JSONB is restricted to raw API payloads, OCR bounding boxes, and execution traces. `pgvector` is reserved strictly for future semantic clause search.
* **Consequences:** Prevents unnormalized data bloat while preserving metadata flexibility.
* **Rejected Alternatives:** NoSQL/MongoDB (rejected due to lack of cross-entity relational joins for multi-cover tenders).

---

### ADR-015: First-Class Immutable Evidence Ledger Model
* **Context:** Procurement decisions require explicit proof answering "What proves this compliance evaluation result?".
* **Options Considered:**
  1. Pass/Fail boolean flags stored on bidder submission record.
  2. Text summary notes attached to evaluation rows.
  3. First-Class Immutable `EvidenceRecord` entity linking requirements to document page bounding boxes or API verification payloads.
* **Decision:** Implement **First-Class Immutable Evidence Ledger Model**.
* **Reason:** Creates complete provenance transparency. Every evaluation result references a dedicated `EvidenceRecord` with SHA-256 payload hash, bounding box `[x0, y0, x1, y1]`, and provenance mode tag. Evidence is append-only; corrections create new evidence version records.
* **Consequences:** Requires evidence assembly step in execution pipeline.
* **Rejected Alternatives:** Result-only flags (rejected due to audit vulnerability and inability to defend decisions in legal appeals).

---

### ADR-016: Tender, Rule, and Policy Temporal Versioning Architecture
* **Context:** Historical procurement evaluations must remain 100% explainable and reproducible even if tender clauses, government rules, or regulatory policies change over time.
* **Options Considered:**
  1. Mutating tender and rule rows directly when corrigenda or policy updates occur.
  2. Soft-deleting old rules and inserting new rows.
  3. Five-Tier Temporal Versioning Architecture (`TenderVersion`, `PolicyVersion`, `ComplianceRule`, `DocumentExtraction`, `EvidenceRecord`).
* **Decision:** Adopt **Five-Tier Temporal Versioning Architecture**.
* **Reason:** Corrigenda create new immutable `TenderVersion` rows. Rules link to immutable `PolicyVersion` definitions (e.g. MII Order 2017 vs 2024). Historical evaluation runs lock their version context permanently.
* **Consequences:** Requirements and evaluation results MUST link to a specific `TenderVersion` ID.
* **Rejected Alternatives:** In-place row mutation (rejected because historical evaluation explainability would be destroyed).

---

### ADR-017: Isolation of Tamper-Evident Audit Events from Application Domain Models
* **Context:** Preventing corruption of audit logs and distinguishing application infrastructure events from business domain entities.
* **Options Considered:**
  1. Storing audit metadata columns directly inside domain tables (`tenders`, `bidders`).
  2. Dedicated append-only `audit_events` and `audit_hash_chain_blocks` tables separate from business domain models.
* **Decision:** Implement **Isolation of Tamper-Evident Audit Events from Domain Models**.
* **Reason:** Isolates audit trail hash chaining from business logic transactions. Database RBAC grants `INSERT, SELECT` ONLY on audit tables to backend applications, preventing `UPDATE` or `DELETE` operations.
* **Consequences:** Audit logger module manages hash-chain block sealing asynchronously.
* **Rejected Alternatives:** Embedded audit columns (rejected due to lack of cryptographic chaining and tamper evidence).

---

### ADR-018: Strict Separation of Source Documents, Extracted Field Data, and Government Verification Payloads
* **Context:** Preventing confusion between raw uploaded files, AI/OCR interpretations, and authoritative government responses.
* **Options Considered:**
  1. Storing extracted text and API responses inside document metadata JSON fields.
  2. Three-layer entity separation: `SourceDocument` (raw file blob) → `DocumentExtraction` (OCR interpretation) → `GovernmentVerificationResult` (external authority API response).
* **Decision:** Adopt **Strict Three-Layer Entity Separation**.
* **Reason:** Preserves data provenance. Extracted document text is unverified bidder claim data; government verification represents authoritative external data. Combining them destroys audit clarity.
* **Consequences:** Explicit entity relationships connecting OCR extractions and API payloads to evidence records.
* **Rejected Alternatives:** Single generic document table (rejected due to provenance loss).
