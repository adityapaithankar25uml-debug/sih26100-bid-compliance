# Phase 1 Architecture Decision Records (ADRs)

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-005  
**Version:** 1.1.0  
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

---

### ADR-001: Modular Monolith Architecture Pattern

* **Context:** The SIH 26100 platform requires 23 distinct functional capabilities spanning document intelligence, rule evaluation, verification gateways, and audit logging. We must select an architectural pattern suitable for a student SIH team during a 36-hour hackathon while maintaining enterprise software standards for CPCL deployment.
* **Options Considered:**
  1. Microservices Architecture (separate services for OCR, Rule Engine, Verification, Audit, Auth).
  2. Unstructured Monolith (single codebase with shared logic and no boundary enforcement).
  3. Modular Monolith (single deployment unit with strictly encapsulated domain modules and internal service interfaces).
* **Decision:** Adopt the **Modular Monolith** pattern.
* **Reason:** Microservices introduce distributed tracing complexity, inter-service network latency, multi-repo synchronization challenges, and deployment overhead that would overwhelm an SIH hackathon team. An unstructured monolith leads to tight coupling and unmaintainable code. A Modular Monolith delivers strict domain separation, in-memory function call performance, simple deployment (single container/process), and a clear path to extract microservices post-SIH if needed.
* **Consequences:** Code structure must strictly enforce module encapsulation. Modules cannot directly access database tables belonging to other modules.
* **Rejected Alternatives:** Microservices (rejected due to excessive operational overhead for SIH); Unstructured Monolith (rejected due to risk of unmaintainable spaghetti code).

---

### ADR-002: Python (FastAPI) Backend Framework

* **Context:** The backend framework must orchestrate AI OCR/NLP models, execute deterministic Pydantic rule validation, handle async government verification calls, and generate RESTful OpenAPI specifications.
* **Options Considered:**
  1. Node.js (Express / NestJS).
  2. Python (FastAPI).
  3. Java (Spring Boot).
  4. Go (Gin).
* **Decision:** Select **Python (FastAPI)**.
* **Reason:** FastAPI provides native Python ecosystem integration (PyMuPDF, PaddleOCR, LangChain, Pydantic), asynchronous request handling via `async/await`, automatic OpenAPI documentation generation, and high execution speed.
* **Consequences:** Team must enforce clean architecture patterns to prevent large monolithic controller files.
* **Rejected Alternatives:** Node.js (rejected due to weaker native computer vision/OCR library integration); Java/Go (rejected due to slower development velocity for AI pipeline orchestration during SIH).

---

### ADR-003: Next.js Presentation Framework

* **Context:** The procurement workbench requires interactive split-screen document evaluation, real-time status updates, side-by-side PDF previewing with bounding-box highlights, and clean officer workflows.
* **Options Considered:**
  1. Next.js 14+ / React (TypeScript).
  2. Vue.js / Nuxt.
  3. Streamlit / Gradio (Python UI).
* **Decision:** Select **Next.js 14+ / React (TypeScript)**.
* **Reason:** Next.js provides modern component-driven UI capabilities, server-side rendering (SSR), fast client-side navigation, and an ecosystem of robust PDF rendering libraries (`react-pdf`) essential for visual bounding-box overlays.
* **Consequences:** Requires frontend-backend separation via REST API contracts.
* **Rejected Alternatives:** Streamlit (rejected due to lack of customizable split-screen PDF rendering and bounding-box overlay capabilities required for CPCL committee usability).

---

### ADR-004: Primary Relational Database Engine (PostgreSQL + JSONB + pgvector)

* **Context:** The database must store transactional relational domain entities (Tenders, Bidders, Requirements), handle complex relational queries, enforce ACID transaction integrity for officer decisions, store flexible metadata, and support optional vector embeddings for RAG retrieval.
* **Options Considered:**
  1. PostgreSQL 16+ (Relational + JSONB + pgvector).
  2. PostgreSQL with PostGIS extension.
  3. MongoDB.
  4. MySQL.
* **Decision:** Select **PostgreSQL 16+** configured with:
  - **Relational tables** for transactional data integrity (Tenders, Bidders, Officer Decisions, Requirements).
  - **`JSONB`** for controlled flexible metadata, dynamic OCR token coordinates, and rule execution traces.
  - **`pgvector`** extension *only where explicitly justified* for future semantic search or RAG vector retrieval requirements.
  - **Exclusion of PostGIS:** PostGIS is explicitly **removed** from the mandatory MVP architecture because no documented functional requirement mandates spatial or geographic queries.
* **Reason:** PostgreSQL provides ACID compliance for legal decision auditability combined with powerful native `JSONB` document storage. Excluding PostGIS reduces unnecessary database dependency overhead while preserving full relational and vector capability.
* **Consequences:** Database schema must be version-controlled via migrations in Phase 2.
* **Rejected Alternatives:** PostGIS (rejected as unnecessary for MVP functional requirements); MongoDB (rejected due to weaker relational join capabilities for multi-cover tender requirements).

---

### ADR-005: S3-Compatible Object Storage for Documents (MinIO)

* **Context:** Bidders upload multi-megabyte PDF, JPEG, and TIFF documents. We require scalable, secure document storage separated from the relational database.
* **Options Considered:**
  1. Local Server File System.
  2. S3-Compatible Object Storage (MinIO for dev/demo, AWS S3 / MinIO for production).
  3. Database BLOB storage.
* **Decision:** Select **S3-Compatible Object Storage (MinIO)**.
* **Reason:** Separates blob storage from relational database, supports file-level AES-256 encryption, and provides standardized presigned URL access for frontend document rendering.
* **Consequences:** Requires object storage client configuration.
* **Rejected Alternatives:** Database BLOB storage (rejected due to database bloat and slow backup/restore cycles).

---

### ADR-006: Provider-Agnostic AI Abstraction Layer

* **Context:** The platform relies on LLM capabilities for document classification, OCR field extraction assistance, and natural language explanation generation. We must prevent vendor lock-in to a single AI provider.
* **Options Considered:**
  1. Direct integration with Google Gemini API only.
  2. Direct integration with OpenAI API only.
  3. Unified `AIProviderInterface` wrapper supporting Gemini, OpenAI, and Local Ollama.
* **Decision:** Adopt a **Unified `AIProviderInterface` Abstraction Layer**.
* **Reason:** Enables switching between cloud APIs (Gemini/OpenAI) and local offline LLMs (Ollama Qwen 2.5 3B) based on pricing, network availability during the hackathon, or CPCL data privacy mandates.
* **Consequences:** Prompts must be designed in a provider-agnostic manner and enforced via Pydantic output schemas.
* **Rejected Alternatives:** Single vendor lock-in (rejected due to risk of API downtime or network loss during hackathon demo).

---

### ADR-007: Government Integration Adapter Pattern (4 Runtime Modes)

* **Context:** Government portals (GST, MCA, Udyam, EPFO, ESIC, etc.) have varying API availability, authentication rules, and access restrictions.
* **Options Considered:**
  1. Direct API calls scattered throughout backend business logic.
  2. Centralized Adapter Pattern enforcing `BaseGovernmentAdapter` interface with 4 modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`).
  3. Web Scraping scripts for non-API portals.
* **Decision:** Adopt the **Government Integration Adapter Pattern** supporting four runtime modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`).
* **Reason:** Encapsulates external integration quirks behind a uniform contract. Completely isolates application logic from changes in government endpoints or third-party KYB APIs while visually tagging provenance on UI cards (`[LIVE_VERIFIED]`, `[MOCK_SIMULATED]`, etc.).
* **Consequences:** Every government integration must be wrapped in an adapter class implementing standard response methods.
* **Rejected Alternatives:** Web Scraping (rejected due to WAFs, CAPTCHAs, legal ToS violations, and extreme fragility).

---

### ADR-008: Deterministic Python / Pydantic Rule Engine

* **Context:** Compliance rules (turnover thresholds, experience years, Make in India local content percentages, MSE EMD waivers) must be evaluated accurately and reproducibly.
* **Options Considered:**
  1. AI LLM evaluates pass/fail rules directly from document text.
  2. External Business Rule Management System (Drools / Camunda).
  3. Custom Deterministic Python Engine utilizing Pydantic schemas.
* **Decision:** Build a **Custom Deterministic Python / Pydantic Rule Engine**.
* **Reason:** AI evaluation is non-deterministic and subject to hallucination. Pydantic/Python logic ensures 100% mathematical reproducibility, version control, unit testability, and zero hallucination risk, conforming strictly to CVC audit requirements.
* **Consequences:** Rule evaluation parameters must be explicitly typed and normalized.
* **Rejected Alternatives:** AI-based rule evaluation (rejected due to legal and CVC non-reproducibility risks).

---

### ADR-009: Tamper-Evident SHA-256 Hash-Chained Audit Ledger

* **Context:** Procurement decisions, AI extraction events, verification calls, and human officer overrides require legally defensible and vigilance-compliant auditability.
* **Options Considered:**
  1. Standard relational database audit log table with timestamps.
  2. Tamper-evident append-only ledger using SHA-256 cryptographic hash chaining (`Hash_n = SHA256(Hash_{n-1} + Timestamp + Actor + Payload)`).
  3. Claims of absolute "tamper-proof" database storage.
* **Decision:** Implement a **Tamper-Evident SHA-256 Hash-Chained Audit Ledger**.
* **Terminology & Technical Rationale:** We explicitly adopt the technically accurate term **"tamper-evident audit trail"** (rather than "tamper-proof"). Cryptographic hash chaining ensures that any modification, insertion, or deletion of past audit records immediately invalidates all subsequent block hashes, providing undeniable mathematical evidence of tampering to auditors. However, hash chaining alone does not mathematically guarantee that a privileged database administrator with full write access cannot rewrite the entire historical ledger from scratch; true tamper-resistance requires backing the chain with external write-once-read-many (WORM) storage or external timestamping services.
* **Consequences:** Every audit event must calculate and store its cryptographic hash based on the preceding record hash.
* **Rejected Alternatives:** Absolute "tamper-proof" claims (rejected as technically inaccurate for single-database deployments); unchained audit logs (rejected due to lack of tamper detection).

---

### ADR-010: Separation of Compliance Status, Qualification Outcome, Evidence Confidence, and Risk Scoring

* **Context:** Evaluating bidders requires distinct analytical metrics without conflating binary pass/fail compliance, overall qualification, evidence quality, and risk indicators.
* **Options Considered:**
  1. Single percentage score combining compliance and risk.
  2. Mandatory rule: "Any mandatory requirement FAIL forces Risk Score = 100".
  3. Four strictly separated analytical dimensions: (A) Compliance Status, (B) Compliance/Qualification Outcome, (C) Evidence Confidence, (D) Risk Score.
* **Decision:** Adopt **Strict Four-Dimensional Separation**:
  - **A. Compliance Status:** Itemized status for individual requirements (`PASS`, `FAIL`, `REVIEW`, `MISSING`, `EXPIRED`, `CONFLICT`, `NOT_VERIFIED`, `NOT_APPLICABLE`).
  - **B. Compliance / Qualification Outcome:** Overall bidder evaluation outcome (`COMPLIANT`, `NOT COMPLIANT`, `PROVISIONAL`). A mandatory requirement failure produces `Compliance Status = FAIL` and/or `Qualification Outcome = NOT COMPLIANT`.
  - **C. Evidence Confidence:** Metric (0.0–1.0 or `HIGH`/`MEDIUM`/`LOW`/`UNVERIFIED`) rating document OCR quality and API verification source authority.
  - **D. Risk Score:** Independent analytical score (0.0–100.0) measuring anomaly indicators, conflicting information across sources, verification failures, suspicious document patterns, document irregularities, and historical/vendor risk indicators.
* **Non-Interference Mandate:** Risk Score is a separate analytical dimension. A mandatory requirement failure sets `Compliance Status = FAIL` and `Qualification Outcome = NOT COMPLIANT`, but DOES NOT automatically force `Risk Score = 100`. Risk score itself CANNOT independently qualify or disqualify a bidder.
* **Decision Authority:** The Human Procurement Officer remains the final decision authority.
* **Consequences:** Data structures and UI dashboards must render these four dimensions independently.
* **Rejected Alternatives:** Automatic disqualification by risk score (rejected because qualification must be rule-driven and human-approved); conflating risk score with compliance pass/fail (rejected as structurally flawed).

---

### ADR-011: Mandatory Human-in-the-Loop Decision Authority

* **Context:** Public procurement rules dictate legal accountability for qualification decisions.
* **Options Considered:**
  1. Fully automated AI qualification/disqualification.
  2. System qualifies bidders automatically unless an officer vetoes within 24 hours.
  3. Mandatory Human-in-the-Loop: System generates evaluation workbench; Procurement Officer must explicitly record final decision with mandatory rationale.
* **Decision:** Mandate **Human-in-the-Loop Decision Authority**.
* **Reason:** CVC guidelines and Indian law hold named government procurement officers legally accountable. The platform is designed strictly as a Decision Support Workbench.
* **Consequences:** UI must force officers to provide non-empty justification text for manual overrides and final decision recordings.
* **Rejected Alternatives:** Autonomous AI decision making (rejected due to legal liability and non-compliance with procurement regulations).

---

### ADR-012: Background Task Execution & Queue Technology (Celery + Redis)

* **Context:** Asynchronous background processing is required for heavy tasks such as multi-page PDF OCR extraction, document layout parsing, background API verification calls, and async notification delivery.
* **Options Considered:**
  1. Celery + Redis.
  2. ARQ + Redis.
  3. Synchronous request-response processing inside FastAPI handlers.
* **Decision:** Select **Celery + Redis** as the single background task execution stack for the MVP.
* **Role of Redis:** Redis 7+ serves as the central message broker, task queue, background-job coordinator, and ephemeral result/session cache with configurable TTL.
* **Role of Celery:** Celery manages background worker processes, task routing, retries with exponential backoff, and task monitoring.
* **Consequences:** Celery worker processes must be managed alongside the main FastAPI application.
* **Rejected Alternatives:** ARQ (rejected as a secondary alternative to maintain a single, mature background processing stack); synchronous in-request processing (rejected due to HTTP request timeout risks during multi-page PDF processing).
