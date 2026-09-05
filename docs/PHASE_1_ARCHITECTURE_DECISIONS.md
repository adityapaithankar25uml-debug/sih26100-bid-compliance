# Phase 1 Architecture Decision Records (ADRs)

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-005  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## ADR Index

- [ADR-001: Modular Monolith Architecture Pattern](#adr-001-modular-monolith-architecture-pattern)
- [ADR-002: Python (FastAPI) Application Backend](#adr-002-python-fastapi-application-backend)
- [ADR-003: Next.js / React Web Presentation Framework](#adr-003-nextjs--react-web-presentation-framework)
- [ADR-004: PostgreSQL Primary Relational Database](#adr-004-postgresql-primary-relational-database)
- [ADR-005: Redis Caching & Async Job Coordination](#adr-005-redis-caching--async-job-coordination)
- [ADR-006: S3-Compatible Object Storage for Documents](#adr-006-s3-compatible-object-storage-for-documents)
- [ADR-007: Provider-Agnostic AI Abstraction Layer](#adr-007-provider-agnostic-ai-abstraction-layer)
- [ADR-008: Government Integration Adapter Pattern](#adr-008-government-integration-adapter-pattern)
- [ADR-009: Deterministic Python / Pydantic Rule Engine](#adr-009-deterministic-python--pydantic-rule-engine)
- [ADR-010: Evidence-First Compliance & Provenance Architecture](#adr-010-evidence-first-compliance--provenance-architecture)
- [ADR-011: Mandatory Human-in-the-Loop Decision Authority](#adr-011-mandatory-human-in-the-loop-decision-authority)
- [ADR-012: Configurable LIVE / SANDBOX / MOCK / MANUAL Modes](#adr-012-configurable-live--sandbox--mock--manual-modes)

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

### ADR-002: Python (FastAPI) Application Backend

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

### ADR-003: Next.js / React Web Presentation Framework

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

### ADR-004: PostgreSQL Primary Relational Database

* **Context:** The database must handle structured domain entities (Tenders, Bidders, Requirements), support complex relational queries, enforce ACID transaction integrity for officer decisions, and store semi-structured JSON payloads.
* **Options Considered:**
  1. PostgreSQL.
  2. MongoDB.
  3. MySQL.
* **Decision:** Select **PostgreSQL 16**.
* **Reason:** PostgreSQL provides ACID compliance for legal decision auditability combined with powerful native `JSONB` document storage for OCR token coordinates and raw government API response payloads.
* **Consequences:** Database schema must be version-controlled via migrations (in Phase 2).
* **Rejected Alternatives:** MongoDB (rejected due to weaker relational join capabilities for multi-cover tender requirements and compliance matrices).

---

### ADR-005: Redis Caching & Async Job Coordination

* **Context:** Government verification calls (where active) and AI OCR extraction tasks can be time-consuming. We require caching and asynchronous task queue management.
* **Options Considered:**
  1. Redis (Cache + ARQ / Celery Queue).
  2. RabbitMQ + Memcached.
  3. In-memory Python Dict.
* **Decision:** Select **Redis 7**.
* **Reason:** Redis serves dual roles as a high-speed verification result cache with configurable TTL and a lightweight message broker for asynchronous background document processing jobs.
* **Consequences:** Requires Redis container in deployment stack.
* **Rejected Alternatives:** In-memory Python dict (rejected due to process restart data loss and lack of multi-worker shared state).

---

### ADR-006: S3-Compatible Object Storage for Documents

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

### ADR-007: Provider-Agnostic AI Abstraction Layer

* **Context:** The platform relies on LLM capabilities for document classification, OCR field extraction, and natural language explanation generation. We must prevent vendor lock-in to a single AI provider.
* **Options Considered:**
  1. Direct integration with Google Gemini API only.
  2. Direct integration with OpenAI API only.
  3. Unified `AIProviderInterface` wrapper supporting Gemini, OpenAI, and Local Ollama.
* **Decision:** Adopt a **Unified `AIProviderInterface` Abstraction Layer**.
* **Reason:** Enables switching between cloud APIs (Gemini/OpenAI) and local offline LLMs (Ollama Qwen 2.5 3B) based on pricing, network availability during the hackathon, or CPCL data privacy mandates.
* **Consequences:** Prompts must be designed in a provider-agnostic manner and enforced via Pydantic output schemas.
* **Rejected Alternatives:** Single vendor lock-in (rejected due to risk of API downtime or network loss during hackathon demo).

---

### ADR-008: Government Integration Adapter Pattern

* **Context:** Government portals (GST, MCA, Udyam, EPFO, ESIC, etc.) have varying API availability, authentication rules, and access restrictions.
* **Options Considered:**
  1. Direct API calls scattered throughout backend business logic.
  2. Centralized Adapter Pattern enforcing `BaseGovernmentAdapter` interface.
  3. Web Scraping scripts for non-API portals.
* **Decision:** Adopt the **Government Integration Adapter Pattern**.
* **Reason:** Encapsulates external integration quirks behind a uniform contract. Completely isolates application logic from changes in government endpoints or third-party KYB APIs.
* **Consequences:** Every government integration must be wrapped in an adapter class implementing standard response methods.
* **Rejected Alternatives:** Web Scraping (rejected due to WAFs, CAPTCHAs, legal ToS violations, and extreme fragility).

---

### ADR-009: Deterministic Python / Pydantic Rule Engine

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

### ADR-010: Evidence-First Compliance & Provenance Architecture

* **Context:** Procurement officers and CVC/CAG auditors require defensible proof for every evaluation result. Checkbox compliance without evidence is unacceptable.
* **Options Considered:**
  1. Store evaluation result flags only (`PASS` / `FAIL`).
  2. Store evaluation result flags with text summary notes.
  3. Evidence-First Architecture: Bind every result to an immutable evidence record citing exact PDF page, bounding box, API payload, and hash.
* **Decision:** Adopt **Evidence-First Architecture**.
* **Reason:** Creates complete provenance transparency. Clicking any compliance flag in the UI immediately renders the highlighted source document bounding box or raw API payload, eliminating black-box distrust.
* **Consequences:** Requires bounding-box coordinate extraction during OCR processing and evidence link storage in database.
* **Rejected Alternatives:** Result-only flags (rejected due to audit vulnerability and inability to defend decisions during appeals).

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

### ADR-012: Configurable LIVE / SANDBOX / MOCK / MANUAL Modes

* **Context:** Live government APIs require formal government authorization, MoUs, and GSP partnerships that cannot be completed within an SIH hackathon timeline.
* **Options Considered:**
  1. Refuse to demonstrate features where live APIs are unavailable.
  2. Fake live API calls by hardcoding responses inside UI components.
  3. Implement 4 runtime modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`) in backend adapters with explicit visual UI tags.
* **Decision:** Implement **Configurable 4-Runtime Adapter Modes (`LIVE` / `SANDBOX` / `MOCK` / `MANUAL`)**.
* **Reason:** Demonstrates production-grade engineering while maintaining 100% technical honesty during hackathon presentations.
* **Consequences:** UI must render clear visual indicators (`[LIVE_VERIFIED]`, `[MOCK_SIMULATED]`, `[MANUAL_VERIFIED]`) on all data elements.
* **Rejected Alternatives:** Hardcoded UI faking (rejected as dishonest and unarchitected).
