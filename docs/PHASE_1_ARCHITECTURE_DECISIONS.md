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
* **Context:** Historical procurement evaluations must remain explainable and reproducible over time.
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

---

### ADR-025: Vendor-Agnostic AI Gateway Interface (`AIGatewayInterface`)
* **Context:** Business modules requiring AI capabilities (extraction, clause mining, explanations) without vendor lock-in to any single cloud provider or LLM SDK.
* **Options Considered:**
  1. Coupling business logic directly to a commercial LLM SDK (e.g. OpenAI / Anthropic SDKs).
  2. Vendor-Agnostic AI Gateway Interface (`AIGatewayInterface`) supporting 4 provider categories (Commercial Cloud, Enterprise Cloud, Self-Hosted vLLM, Local Ollama).
* **Decision:** Implement **Vendor-Agnostic AI Gateway Interface (`AIGatewayInterface`)**.
* **Reason:** Prevents vendor lock-in, enables seamless fallback from cloud to on-premise models during network outages, and ensures full compliance with government data localization policies.
* **Consequences:** Business code depends solely on abstract request/response JSON schema envelopes.
* **Rejected Alternatives:** Direct vendor SDK coupling (rejected due to vendor lock-in and data localization risks).

---

### ADR-026: Multi-Layer Prompt Injection Sandboxing & Tool Permission Isolation
* **Context:** Uploaded bidder documents contain untrusted text that may attempt indirect prompt injection (e.g. commands asking the model to ignore rules or alter scores).
* **Options Considered:**
  1. Relying solely on LLM base model safety fine-tuning.
  2. Multi-layer defense: XML/Markdown delimiter sandboxing (`<<<UNTRUSTED_DOC_CONTENT>>>`), rigid Pydantic JSON schema output enforcement, suspicious instruction pre-scanners, and ZERO direct tool execution permissions for AI models.
* **Decision:** Implement **Multi-Layer Prompt Injection Sandboxing & Tool Permission Isolation**.
* **Reason:** Guarantees that even if an injection string bypasses LLM text parsing, the model lacks tool permissions to write to database tables or invoke external APIs directly.
* **Consequences:** All uploaded text is wrapped in strict structural delimiters; AI models operate with zero side-effect permissions.
* **Rejected Alternatives:** Unsandboxed prompt concatenation (rejected due to severe security vulnerability).

---

### ADR-027: Non-Authoritative AI Axiom & Strict 4-Tier Responsibility Boundary
* **Context:** Preventing AI models from becoming autonomous decision-makers in government procurement compliance.
* **Options Considered:**
  1. Allowing AI models to generate pass/fail recommendations that directly apply to bidder qualification.
  2. Strict Non-Authoritative Axiom: `AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES`, enforced across a 4-Tier Responsibility Boundary Matrix.
* **Decision:** Adopt **Non-Authoritative AI Axiom & 4-Tier Responsibility Boundary Matrix**.
* **Reason:** Preserves legal accountability and CVC compliance. Final qualification decisions remain strictly attributable to human Procurement Officers; compliance evaluations remain 100% deterministic.
* **Rejected Alternatives:** Autonomous AI qualification decisions (rejected due to violation of procurement law and CVC guidelines).

---

### ADR-028: Mandatory Evidence Citation & Grounding Verification for Explanations
* **Context:** Ensuring generated plain-language explanations in officer workbenches and CVC audit reports have traceable evidence and do not contain un-grounded factual claims.
* **Options Considered:**
  1. Free-form text explanation generation without strict evidence linkage.
  2. Mandatory structural evidence citation (`evidence_id`, `page_number`, `bounding_box`) + Automated Grounding Verification Engine checking evidence citation validity before report export.
* **Decision:** Implement **Mandatory Evidence Citation & Traceable Grounding Verification**.
* **Reason:** Ensures decision-relevant AI-generated factual claims intended for procurement reports have traceable evidence/provenance. Grounding validation checks that referenced evidence exists, is accessible, and supports the claim according to defined validation rules.
* **Consequences:** Explanations failing grounding checks are rejected, flagged, or replaced with structured rule output facts.
* **Rejected Alternatives:** Unchecked free-form LLM explanations (rejected due to hallucination risks).

---

### ADR-029: Immutable Prompt/Template Versioning & Audit Reproducibility Ledger
* **Context:** Guaranteeing historical reproducibility of AI-derived extraction results during legal disputes or CVC vigilance audits.
* **Options Considered:**
  1. Updating prompt templates in-place without version tracking.
  2. Immutable prompt registry (`SP-{CAT}-{TASK}-v{MAJ}.{MIN}`) with execution metadata logging (model ID, prompt version, schema version, raw response hash) embedded in every database extraction record.
* **Decision:** Implement **Immutable Prompt/Template Versioning & Audit Reproducibility Ledger**.
* **Reason:** Enables exact reconstruction of past AI processing contexts during vigilance audits. Model upgrades do not silently overwrite historical extraction data.
* **Consequences:** Prompts are version-controlled and immutable in production; extraction records store full provenance envelopes.
* **Rejected Alternatives:** Unversioned prompt edits (rejected due to audit non-reproducibility).

---

### ADR-030: Capability-Based, Sensitivity-Aware Model Routing & Fallback Safety Gate Strategy
* **Context:** Routing AI task workloads efficiently across multiple models without compromising high-risk compliance quality or leaking sensitive data during primary or fallback execution.
* **Options Considered:**
  1. Routing all requests to a single commercial cloud model based on lowest cost/latency or un-gated fallback routing.
  2. Capability-based and sensitivity-aware routing priority matrix + Explicit Fallback Eligibility Gate (verifying task capability, data sensitivity eligibility, approved status, deployment classification, and policy compliance).
* **Decision:** Implement **Capability-Based, Sensitivity-Aware Model Routing & Fallback Safety Gate Strategy**.
* **Reason:** Ensures sensitive PII data is processed exclusively on self-hosted or local models, while reserving high-reasoning models for complex tender clause mining regardless of cost. Explicit Fallback Eligibility Gate prevents sensitive data from being silently routed to unapproved external providers during cloud outages.
* **Consequences:** AI Gateway dynamically evaluates capability, sensitivity, and availability headers before dispatching primary or fallback task requests.
* **Rejected Alternatives:** Cost-only routing or un-gated fallback (rejected due to risk of selecting weak models or leaking sensitive data during outages).

---

### ADR-031: Government Integration Adapter Pattern & Provider Abstraction
* **Context:** Abstracting diverse external government API protocols, schemas, and portals (GSTN, Udyam, PAN, MCA, DigiLocker, etc.) into a unified internal verification contract without leaking vendor details to downstream compliance engines.
* **Options Considered:**
  1. Direct, ad-hoc HTTP/SOAP API calls from core compliance services to external government endpoints.
  2. Isolated `BaseGovernmentAdapter` pattern with standardized `VerificationRequestPayload` and `NormalizedVerificationResponse` data contracts, routed exclusively through a central `GovernmentVerificationOrchestrator`.
* **Decision:** Implement **Government Integration Adapter Pattern & Provider Abstraction**.
* **Reason:** Isolates external transport, payload parsing, and authentication mechanics. Downstream compliance rules evaluate consistent normalized structures regardless of whether data comes from API Setu, an official portal, a synthetic mock, or a manual officer verification.
* **Consequences:** All government integrations must implement `BaseGovernmentAdapter`. AI services are strictly prohibited from invoking adapters directly.
* **Rejected Alternatives:** Un-abstracted direct API calls (rejected due to tight coupling and risk of breaking downstream rules on vendor schema updates).

---

### ADR-032: Strict Qualification of Government API Availability & Authorized Source Principle
* **Context:** Preventing false or assumptive claims regarding public API access for Indian government portals (GST, MCA, Udyam, EPFO, ESIC, Debarment registries) in documentation and software architecture.
* **Options Considered:**
  1. Claiming direct, unauthenticated, or universal public API integration across all government portals.
  2. Mandatory architectural qualification standard: *"The system supports integration through an authorized or approved source or integration mechanism, subject to onboarding, credentials, permissions, availability, and applicable policy."*
* **Decision:** Adopt **Strict Qualification of Government API Availability & Authorized Source Principle**.
* **Reason:** Ensures absolute honesty regarding public procurement API realities. Clearly distinguishes between confirmed public APIs (e.g., API Setu endpoints, DigiLocker), conditional partner APIs, unverified portals, synthetic mocks, and manual fallback workflows.
* **Rejected Alternatives:** Unqualified claims of universal live API integration (rejected due to inaccuracy and breach of project governance rules).

---

### ADR-033: Canonical Normalized Verification Result Model & Identity Comparison Engine
* **Context:** Normalizing external verification responses into a common domain structure and performing multi-tier field comparison (exact, normalized, alias, mismatch) without relying on ungrounded AI matching.
* **Options Considered:**
  1. Storing raw vendor JSON responses directly in compliance evaluation records or using fuzzy LLM matching for legal identity checks.
  2. Canonical `GovernmentVerificationResult` model with deterministic string normalization, field comparison scoring, and policy-controlled identity matching criteria where similarity scores serve as supporting signals and material identity ambiguity triggers human officer review.
* **Decision:** Implement **Canonical Normalized Verification Result Model & Identity Comparison Engine**.
* **Reason:** Prevents schema divergence from breaking compliance evaluations. Guarantees that legal entity matching relies on deterministic normalization rules (`Pvt Ltd` $\rightarrow$ `Private Limited`) and approved policy criteria rather than opaque LLM inferences or static numerical thresholds.
* **Consequences:** Material identity ambiguity or field mismatches automatically transition to `AMBIGUOUS_IDENTITY` and set `requires_human_review = True`.
* **Rejected Alternatives:** Direct storage of un-normalized vendor JSON, static universal similarity thresholds, or autonomous LLM identity matching (rejected due to auditability and legal risks).

---

### ADR-034: Absolute Separation of Technical Transport Status from Business Verification Result
* **Context:** Preventing transient network timeouts, HTTP 5xx errors, rate limits, or portal outages from being incorrectly treated as compliance failures or leading to automated bidder disqualifications.
* **Options Considered:**
  1. Collapsing all failed adapter attempts into a generic `FAIL` status.
  2. Strict architectural separation between **Technical Transport Status** (`TIMEOUT`, `HTTP_500_ERROR`, `RATE_LIMITED`) and **Business Verification Result** (`VERIFIED`, `NOT_VERIFIED`, `RECORD_NOT_FOUND`, `MISMATCH`).
* **Decision:** Implement **Absolute Separation of Technical Transport Status from Business Verification Result**.
* **Reason:** Protects bidder rights and procurement fairness. Technical transport failures transition the verification request to `REQUIRES_MANUAL_VERIFICATION`, preserving bidder eligibility while triggering officer workflow fallback.
* **Consequences:** Technical transport failure can **NEVER** directly trigger automated bidder disqualification.
* **Rejected Alternatives:** Collapsing transport failures into compliance failures (rejected due to severe violation of legal procurement principles).

---

### ADR-035: Quad-Operating Mode Strategy (LIVE, SANDBOX, MOCK, MANUAL_FALLBACK)
* **Context:** Supporting seamless operational transitions between live G2G production environments, official developer sandboxes, hackathon prototype demonstrations, and manual portal verification fallback.
* **Options Considered:**
  1. Single binary production vs. non-production toggle.
  2. Four explicit operating modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`) tracked per verification request and visually stamped on all UI components and audit records.
* **Decision:** Implement **Quad-Operating Mode Strategy**.
* **Reason:** Allows SIH 2026 hackathon prototype evaluation using deterministic synthetic mocks while maintaining an auditable production-ready architecture for live G2G onboarding and manual fallback.
* **Consequences:** UI components display prominent color-coded badges indicating the active operating mode for every verification record.
* **Rejected Alternatives:** Unstamped synthetic mock data (rejected due to risk of confusing test data with real government proof).

---

### ADR-036: Evidence-First Provenance Architecture & Multi-Source Conflict Resolution
* **Context:** Ensuring every government verification generates a tamper-evident `EvidenceRecord` linked to raw response hashes and resolving multi-source data conflicts (e.g., GST Active vs. Debarment Listed) without overwriting evidence.
* **Options Considered:**
  1. Overwriting previous verification records or allowing AI to resolve conflicting government evidence autonomously.
  2. Immutable `EvidenceRecord` generation with SHA-256 payload hashing, complete provenance envelopes, dual-evidence preservation, and mandatory human officer escalation for material conflicts.
* **Decision:** Implement **Evidence-First Provenance Architecture & Multi-Source Conflict Resolution**.
* **Reason:** Ensures complete audit reproducibility for CVC vigilance checks. Preserves contradictory source evidence in full without silent overwrites, ensuring human officers make informed final rulings.
* **Consequences:** All verification records are immutable and hashed into the system's tamper-evident audit hash-chain.
* **Rejected Alternatives:** Overwriting historical evidence or autonomous AI conflict resolution (rejected due to breach of legal auditability).

---

### ADR-037: Scoped Government Credential Isolation & Secret Management Boundary
* **Context:** Securing G2G mTLS certificates, API keys, and OAuth client secrets used for external government API authentication.
* **Options Considered:**
  1. Storing API keys or credentials in application configuration files, environment files committed to Git, or Postgres database tables.
  2. Scoped Credential Isolation Boundary storing zero secrets in code/git/DB, utilizing external secret stores (AWS Secrets Manager / Vault) with dynamic runtime environment injection and KMS encryption.
* **Decision:** Implement **Scoped Government Credential Isolation & Secret Management Boundary**.
* **Reason:** Eliminates credential leakage risks and meets government G2G security onboarding requirements.
* **Consequences:** Secrets are never logged, written to disk, or exposed in API payloads or documentation.
* **Rejected Alternatives:** Hardcoded or database-stored credentials (rejected due to severe security vulnerability).

---

### ADR-038: First-Class Manual Verification Fallback & Auditable Human Decision Workflow
* **Context:** Providing a robust, auditable fallback mechanism when automated government APIs are absent, rate-limited, time out, or require officer portal verification.
* **Options Considered:**
  1. Treating manual verification as an un-tracked external process or bypassing system rule evaluation.
  2. First-class Manual Fallback Workflow integrated into Procurement Officer Workbench, requiring structured portal reference entry, SHA-256 hashed evidence artifact capture, policy-configurable dual-officer review for high-risk checks, and standard `EvidenceRecord` generation.
* **Decision:** Implement **First-Class Manual Verification Fallback & Auditable Human Decision Workflow**.
* **Reason:** Ensures business continuity during government portal outages or for sources lacking public APIs (e.g., debarment lists, EPFO/ESIC). Preserves complete tamper-evident auditability.
* **Consequences:** Manual fallback actions produce standard evidence records tagged with `MANUAL_FALLBACK` and linked to `OfficerDecision` audit blocks.
* **Rejected Alternatives:** Un-audited manual overrides or halting procurement evaluation on API failure (rejected due to operational unfeasibility).

---

### ADR-039: Deterministic Rules Engine Architecture & Non-Authoritative AI Boundary
* **Context:** Evaluating bid compliance against complex tender clauses and regulatory policies without allowing unexplainable, non-deterministic LLM inferences to make pass/fail determinations.
* **Options Considered:**
  1. Prompting LLMs to evaluate tender compliance directly and output pass/fail decisions.
  2. Isolated `ComplianceEngineOrchestrator` executing type-safe deterministic rule ASTs on structured facts (`NormalizedFact`), with AI models restricted to pre-evaluation document extraction and post-evaluation explanation rendering.
* **Decision:** Implement **Deterministic Rules Engine Architecture & Non-Authoritative AI Boundary**.
* **Reason:** Guarantees deterministic, explainable, and reproducible compliance evaluations in strict compliance with CVC vigilance guidelines and public procurement law.
* **Consequences:** Compliance rules never invoke LLMs during evaluation. AI models possess zero authority to make pass/fail or qualification determinations.
* **Rejected Alternatives:** Autonomous AI pass/fail evaluation (rejected due to hallucination risks and violation of legal accountability).

---

### ADR-040: Safe Non-Executable AST Expression Architecture (Zero eval/exec)
* **Context:** Representing complex mathematical, threshold, range, and set-membership rule logic safely without introducing dynamic code execution vulnerabilities.
* **Options Considered:**
  1. Executing dynamic Python string expressions using `eval()`, `exec()`, or custom code interpreters.
  2. Safe, structural JSON Abstract Syntax Tree (AST) model evaluated via a closed set of 15 type-safe tree traversal operators (Logical, Relational, String, Chronological).
* **Decision:** Implement **Safe Non-Executable AST Expression Architecture**.
* **Reason:** Eliminates remote code execution (RCE) and code injection vulnerabilities. Guarantees that rules can be safely validated, versioned, and executed in a sandboxed environment with deployment-configurable resource bounds.
* **Consequences:** All rule conditions must be defined as schema-validated AST JSON structures. Arbitrary Python code execution is strictly prohibited.
* **Rejected Alternatives:** Dynamic string evaluation or custom script execution (rejected due to severe security vulnerabilities).

---

### ADR-041: Immutable Policy Versioning & Dynamic Threshold Binding (PolicyVersion)
* **Context:** Managing regulatory procurement thresholds (e.g., local content percentages, MSME exemptions, turnover limits) without hardcoding values in application code or overwriting historical evaluation baselines.
* **Options Considered:**
  1. Hardcoding statutory numbers directly into Python rule classes or database records.
  2. Immutable `PolicyVersion` entity model with versioned parameter maps, formal approval lifecycles (`DRAFT` $\rightarrow$ `ACTIVE` $\rightarrow$ `SUPERSEDED`), and temporal binding to tender publication and corrigendum dates.
* **Decision:** Implement **Immutable Policy Versioning & Dynamic Threshold Binding**.
* **Reason:** Ensures zero hardcoded policy numbers in code. Supports historical evaluation reproducibility during vigilance audits, as historical evaluations remain permanently anchored to their bound tender and policy versions.
* **Consequences:** Operational policy parameter updates require issuing a new SemVer `PolicyVersion`. Hardcoding numbers in rule code is forbidden.
* **Rejected Alternatives:** Hardcoded threshold constants or in-place policy parameter overwrites (rejected due to audit non-reproducibility).

---

### ADR-042: Evidence-First Fact Model & Strict Status Separation (MISSING ≠ FAIL)
* **Context:** Preventing missing bidder documents, unverified government statuses, or network transport failures from being incorrectly classified as compliance failures or triggering automated disqualifications.
* **Options Considered:**
  1. Collapsing missing facts or unverified statuses into a generic `FAIL` output.
  2. Canonical `NormalizedFact` model encapsulating 10 fact sources and 9 explicit status states, enforcing the axiom that missing data yields `MISSING_EVIDENCE` $\rightarrow$ `REQUIRES_HUMAN_REVIEW`, never `FAIL`.
* **Decision:** Implement **Evidence-First Fact Model & Strict Status Separation**.
* **Reason:** Protects bidder rights and procurement fairness. A `FAIL` status requires an explicit, verified false condition supported by immutable `EvidenceRecord` hashes. Missing data transitions to officer review.
* **Consequences:** Missing facts, stale evidence, or transport failures can **NEVER** directly trigger automated bidder disqualification.
* **Rejected Alternatives:** Misclassifying missing evidence as compliance failure (rejected due to breach of legal procurement principles).

---

### ADR-043: Machine-Readable Evaluation Trace & Traceable Grounded Explanations
* **Context:** Generating plain-language compliance explanations for procurement officers and CVC audit reports while ensuring traceable factual grounding.
* **Options Considered:**
  1. Free-form LLM explanation generation based on prompt summaries.
  2. Machine-readable `EvaluationTrace` containing step-by-step AST execution logs, input fact values, policy parameter references, and evidence SHA-256 hashes, rendered into explanations via pre-approved template patterns.
* **Decision:** Implement **Machine-Readable Evaluation Trace & Traceable Grounded Explanations**.
* **Reason:** Eliminates hallucinated or un-grounded explanatory statements in procurement reports. Ensures every statement is mathematically traceable to underlying raw documents and evidence records.
* **Consequences:** Explanations failing grounding hash checks are rejected and replaced with structured rule fact summaries.
* **Rejected Alternatives:** Free-form LLM explanations without deterministic trace linkage (rejected due to hallucination risks).

---

### ADR-044: Submission Qualification Aggregation & Disqualifying-If-Proven Severity Boundary
* **Context:** Aggregating individual requirement evaluations into a submission-level `QualificationOutcome` (`QUALIFIED`, `NOT_QUALIFIED`, `PENDING_REVIEW`) based on requirement severity classes.
* **Options Considered:**
  1. Simple binary ALL-PASS aggregation where any single missing item or failure disqualifies the bidder.
  2. Severity-weighted aggregation matrix categorizing rules into `DISQUALIFYING_IF_PROVEN`, `MATERIAL_REVIEW`, `NON_MATERIAL_REVIEW`, and `INFORMATIONAL`, ensuring disqualification occurs ONLY when a disqualifying violation is proven with verified evidence.
* **Decision:** Implement **Submission Qualification Aggregation & Disqualifying-If-Proven Severity Boundary**.
* **Reason:** Aligns platform behavior with CVC guidelines and Indian public procurement law. Distinguishes between proven disqualifying violations and items requiring officer clarification or minor non-material reviews.
* **Consequences:** Unverified or ambiguous requirements yield `PENDING_REVIEW`, preserving bidder eligibility for human officer evaluation.
* **Rejected Alternatives:** Binary ALL-PASS aggregation (rejected due to premature disqualification risks on technical or missing data items).

---

### ADR-045: Rule Testing, Invariant Validation & DAG Cycle Detection
* **Context:** Ensuring rule definitions are mathematically sound, free from circular requirement dependencies, and robust against boundary edge cases before activation.
* **Options Considered:**
  1. Manual inspection of rule definitions during deployment.
  2. Automated Rule Test Suite verifying standard test case categories (positive, negative, boundary, missing-data, stale-data, conflicting-data, exempt, invalid) + Static Tarjan DAG cycle detection on requirement dependency graphs.
* **Decision:** Implement **Rule Testing, Invariant Validation & DAG Cycle Detection**.
* **Reason:** Prevents evaluation deadlocks, stack overflows, and logic bugs in production tender processing. Enforces core mathematical and architectural engine invariants.
* **Consequences:** Rules failing applicable test suite execution or creating dependency cycles are rejected during administrative review.
* **Rejected Alternatives:** Un-validated rule activation (rejected due to risk of runtime evaluation failures during live tenders).

---

### ADR-046: Policy-Configurable Human Review Gate & Auditable Non-Mutating Manual Overrides
* **Context:** Handling material discrepancies, rule conflicts, or procurement officer overrides without corrupting historical deterministic evaluation records.
* **Options Considered:**
  1. Allowing procurement officers to edit database evaluation records in-place.
  2. Policy-Configurable Human Review Gate escalating ambiguous outcomes to `REQUIRES_HUMAN_REVIEW` + Co-existing `ManualOverride` entity model recording signed officer rationale, evidence attachments, and audit hash-chain blocks, with four-eyes review governed by policy configuration.
* **Decision:** Implement **Policy-Configurable Human Review Gate & Auditable Non-Mutating Manual Overrides**.
* **Reason:** Preserves legal auditability. The historical deterministic rule output remains locked and un-mutated, while the officer's manual override co-exists as an auditable decision block in the hash-chain. Four-eyes review is policy-configurable for designated high-risk actions.
* **Consequences:** In-place database edits of evaluation records are strictly forbidden. All human overrides require explicit officer authentication, justification notes, and audit logging. Four-eyes dual control is enforced where enabled by policy.
* **Rejected Alternatives:** In-place evaluation record edits or un-audited manual overrides (rejected due to breach of legal auditability).

---

### ADR-047: Modular Workflow Orchestration Boundary & Subsystem Isolation
* **Context:** Coordinating the complex multi-stage bid compliance pipeline (ingestion, AI extraction, government verification, rule evaluation, risk scoring, officer review) without tight coupling or duplicating subsystem responsibilities.
* **Options Considered:**
  1. Hardcoding pipeline calls directly inside API endpoint handlers or microservices.
  2. Stateless, event-driven `WorkflowOrchestrator` enforcing explicit task boundaries, dependency resolution, state transitions, and asynchronous execution across Task 1–6 subsystems.
* **Decision:** Implement **Modular Workflow Orchestration Boundary & Subsystem Isolation**.
* **Reason:** Preserves subsystem autonomy and modular monolith architecture principles. The orchestrator coordinates execution order and state transitions without embedding AI inference, government API logic, or rule AST evaluation code.
* **Consequences:** Subsystems interact with the orchestrator via clean data contracts. Subsystem implementations remain isolated and independently testable.
* **Rejected Alternatives:** Monolithic API-embedded pipeline calls or autonomous subsystem-to-subsystem direct chaining (rejected due to spaghetti coupling and loss of centralized workflow state governance).

---

### ADR-048: Multi-Dimensional Workflow State Machine vs Status Isolation
* **Context:** Preventing technical execution states, business submission lifecycle states, rule compliance outcomes, qualification outcomes, and officer decision records from corrupting one another.
* **Options Considered:**
  1. Collapsing all system states into a single generic `status` string.
  2. Isolated 5-Dimensional State Architecture (`WorkflowInstance` Execution State, Business Domain State, Compliance Status, Qualification Outcome, Officer Decision).
* **Decision:** Implement **Multi-Dimensional Workflow State Machine vs Status Isolation**.
* **Reason:** Guarantees domain precision and prevents invalid automated state mutation. A technical task failure (`FAILED`) never alters business compliance state or triggers automated bidder disqualification.
* **Consequences:** Database models maintain distinct status fields. State transitions follow dedicated, audited transition matrices.
* **Rejected Alternatives:** Single generic status field (rejected due to status ambiguity and illegal automated bidder disqualifications).

---

### ADR-049: Directed Acyclic Graph (DAG) Task Dependency Modeling & Cycle Prevention
* **Context:** Structuring complex tender evaluation pipelines to maximize task parallelism (e.g. concurrent government verifications) while preventing execution deadlocks or circular task dependencies.
* **Options Considered:**
  1. Ad-hoc sequential task loops hardcoded in background scripts.
  2. Declarative Directed Acyclic Graph (DAG) task dependency architecture with static Tarjan SCC cycle detection during workflow registration.
* **Decision:** Implement **Directed Acyclic Graph (DAG) Task Dependency Modeling & Cycle Prevention**.
* **Reason:** Maximizes workflow concurrency across independent verifications while guaranteeing zero runtime execution deadlocks or infinite loops.
* **Consequences:** Workflow definitions must be registered as schema-validated DAGs. Definitions containing dependency cycles are rejected during administrative upload.
* **Rejected Alternatives:** Hardcoded sequential loops or unvalidated runtime task graphs (rejected due to poor throughput and deadlock risks).

---

### ADR-050: At-Least-Once Job Delivery with Idempotent Workflow Handlers
* **Context:** Guaranteeing consistent database state and evidence records when background workers retry tasks or handle duplicate network messages in distributed queues.
* **Options Considered:**
  1. Relying on queue-level exactly-once delivery guarantees.
  2. At-Least-Once Delivery at queue level combined with 4-tier Idempotency Keys (API, Instance, Task, Govt Verification) protecting logical operations against duplicate side effects via durable idempotency records and concurrency-safe handler semantics, while distinct execution retries create distinct `TaskAttempt` records.
* **Decision:** Implement **At-Least-Once Job Delivery with Idempotent Workflow Handlers**.
* **Reason:** Exactly-once network delivery is mathematically impossible across distributed worker crashes. At-least-once delivery with idempotent application handlers guarantees zero duplicate side-effects. Database locking mechanisms serve as implementation options rather than rigid architectural bounds.
* **Consequences:** All task handlers must check existing execution outputs and coordinate state before executing task logic.
* **Rejected Alternatives:** Un-guaranteed exactly-once delivery assumptions (rejected due to duplicate side-effect vulnerabilities).

---

### ADR-051: Controlled Retry Classification, Backoff Jitter & Dead-Letter Handling
* **Context:** Responding to infrastructure timeouts, network failures, corrupt input payloads, and government portal outages without causing retry storms or false compliance failures.
* **Options Considered:**
  1. Generic infinite retries or instant task abortion on any exception.
  2. 4-Tier Fault Taxonomy (Transient, Permanent, Govt Business Result, Human Review) with Exponential Backoff + Equal Jitter and configurable retry parameters.
* **Decision:** Implement **Controlled Retry Classification, Backoff Jitter & Dead-Letter Handling**.
* **Reason:** Protects upstream government portals from thundering herd retry spikes. Isolate transient network issues from permanent payload errors.
* **Consequences:** Transient errors retry gracefully; permanent errors isolate cleanly; business verification results pass to rule engine without retrying.
* **Rejected Alternatives:** Uncontrolled immediate retries or immediate failure routing (rejected due to portal overload and system fragility).

---

### ADR-052: Checkpoint-Based Workflow Pause, Human Review & Non-Destructive Resume
* **Context:** Handing off ambiguous, missing, or high-risk evaluation cases to Procurement Officers without losing processed work or corrupting machine trace histories.
* **Options Considered:**
  1. Aborting the workflow and requiring a full pipeline re-run after human intervention.
  2. State Machine Checkpoint Pause (`RUNNING` $\rightarrow$ `WAITING` $\rightarrow$ `REQUIRES_HUMAN_REVIEW`), persisting task outputs to PostgreSQL, queuing items in Officer Workbench UI, and resuming cleanly upon authorized officer decision.
* **Decision:** Implement **Checkpoint-Based Workflow Pause, Human Review & Non-Destructive Resume**.
* **Reason:** Saves computation, minimizes external API overhead, and preserves legal accountability. The original evaluation trace remains locked while the officer's decision co-exists in audit storage.
* **Consequences:** Workflows pause statefully and resume from saved checkpoints without re-evaluating completed upstream DAG nodes.
* **Rejected Alternatives:** Pipeline abortion or in-place record mutation (rejected due to operational inefficiency and audit corruption).

---

### ADR-053: Two-Phase Graceful Workflow Cancellation Semantics (`CANCEL_REQUESTED` $\rightarrow$ `CANCELLED`)
* **Context:** Terminating active or queued evaluation workflows safely upon authorized officer command without leaving orphan database locks or un-audited state.
* **Options Considered:**
  1. Abrupt worker process termination (`SIGKILL`).
  2. Two-Phase Graceful Cancellation Protocol (`CANCEL_REQUESTED` $\rightarrow$ background worker checkpoint inspection $\rightarrow$ snapshot lock $\rightarrow$ `CANCELLED`), ensuring cancellation does not erase audit history or bypass required evidence retention governed by policy.
* **Decision:** Implement **Two-Phase Graceful Workflow Cancellation Semantics**.
* **Reason:** Prevents database corruption, partial un-audited writes, or lock starvation when a workflow is cancelled mid-execution.
* **Consequences:** Active workers inspect cancellation flags at task boundaries and exit cleanly without committing partial results. Audit records and source documents remain retained according to applicable lifecycle policy.
* **Rejected Alternatives:** Forceful worker termination or un-coordinated cancellation (rejected due to state corruption risks).

---

### ADR-054: Integration of Workflow Event Lineage into Tamper-Evident Audit Hash-Chain
* **Context:** Providing legal proof of workflow execution lineage, stage transitions, task retries, and officer decisions for CVC vigilance audits.
* **Options Considered:**
  1. Standard application log files written to disk or centralized log collectors.
  2. Integration of workflow state transition events into the Task 2 SHA-256 tamper-evident audit hash-chain (`AuditEvent`).
* **Decision:** Implement **Integration of Workflow Event Lineage into Tamper-Evident Audit Hash-Chain**.
* **Reason:** Ensures workflow history cannot be repudiated, edited, or deleted after execution. Every applicable workflow state change generates an `AuditEvent` that is linked into the existing tamper-evident SHA-256 hash-chain audit structure.
* **Consequences:** All applicable workflow state changes generate hash-linked audit blocks in PostgreSQL without introducing digital PKI signature frameworks or second audit systems.
* **Rejected Alternatives:** Ephemeral log files or un-chained database events (rejected due to audit non-repudiation requirements).

---

### ADR-055: Unified Centralized Security Boundary & Defense-in-Depth Architecture
* **Context:** Protecting sensitive procurement filings, commercial bidder financials, government verification data, and AI pipelines across complex execution environments.
* **Options Considered:**
  1. Ad-hoc per-service security checks without formal trust boundaries.
  2. Unified Defense-in-Depth Security Boundary Architecture classifying system assets into four formal trust zones (Level 0 Untrusted, Level 1 External Dependency, Level 2 Ingress Gateway, Level 3 Trusted Core).
* **Decision:** Implement **Unified Centralized Security Boundary & Defense-in-Depth Architecture**.
* **Reason:** Ensures every boundary crossing enforces explicit authentication, authorization, validation, and audit logging.
* **Consequences:** Systems enforce defense-in-depth across 7 security dimensions without relying on implicit network trust.
* **Rejected Alternatives:** Perimeter-only security models or unmediated inter-service calls.

---

### ADR-056: Multi-Dimensional Authorization Matrix (RBAC + Capability + Context + Sensitivity)
* **Context:** Preventing unauthorized cross-tenant data access, privilege escalation, and un-audited manual overrides.
* **Options Considered:**
  1. Basic Role-Based Access Control (RBAC) checking single role strings.
  2. Multi-Dimensional Authorization Formula ($\text{WHO} + \text{ACTION} + \text{RESOURCE} + \text{ORG_CONTEXT} + \text{CLASSIFICATION}$).
* **Decision:** Implement **Multi-Dimensional Authorization Matrix**.
* **Reason:** Provides fine-grained capability checks bound to organizational procurement contexts and data sensitivity levels.
* **Consequences:** Procurement officers can access only assigned bids within their organization; unmasking PII requires explicit capabilities.
* **Rejected Alternatives:** Coarse role-only authorization or global admin permissions.

---

### ADR-057: Policy-Controlled Multi-Factor Authentication & Identity Provider Abstraction
* **Context:** Authenticating human users while preventing vendor lock-in to cloud identity platforms.
* **Options Considered:**
  1. Custom internal password storage and basic session tokens.
  2. Identity Provider Abstraction (`IdentityProviderInterface`) supporting OIDC/OAuth2 with policy-controlled MFA and step-up authentication.
* **Decision:** Implement **Policy-Controlled Multi-Factor Authentication & Identity Provider Abstraction**.
* **Reason:** Leverages enterprise OIDC identity providers while enforcing policy-based MFA for high-risk operations (manual overrides, tender approvals).
* **Consequences:** Short-lived JWT access tokens (15-min) paired with silent OAuth2 refresh and Redis token blocklisting.
* **Rejected Alternatives:** Monolithic internal user password tables or static long-lived API tokens.

---

### ADR-058: Security & Sensitivity Data Classification System Enforcement (PUBLIC to PII)
* **Context:** Managing data handling rules across diverse procurement artifacts, bidder financial balance sheets, and government verification responses.
* **Options Considered:**
  1. Uniform security handling across all database fields.
  2. 5-Tier Data Classification System (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, `PII`) governing storage, masking, encryption, and AI routing eligibility.
* **Decision:** Implement **Security & Sensitivity Data Classification System Enforcement**.
* **Reason:** Aligns data sensitivity with handling rules; prevents PII and restricted identifiers from entering external AI prompts.
* **Consequences:** Classification governs handling but does not replace authorization checks; PII can co-exist inside multi-level documents.
* **Rejected Alternatives:** Single security level for all data items.

---

### ADR-059: Pre-AI Privacy Gateway & Reversible Entity Tokenization Pipeline
* **Context:** Using cloud LLM providers for document extraction without exposing unredacted bidder PII, PAN numbers, or financial secrets.
* **Options Considered:**
  1. Transmitting raw extracted document text directly to external cloud LLM APIs.
  2. Pre-AI Privacy Gateway executing regex/NLP entity detection, replacing PII with reversible tokens (`[PII_TOKEN_1]`), and de-tokenizing structured responses inside local application RAM.
* **Decision:** Implement **Pre-AI Privacy Gateway & Reversible Entity Tokenization Pipeline**.
* **Reason:** Guarantees data privacy while maintaining structured AI extraction quality.
* **Consequences:** Sensitive identifiers never cross the Level 3 boundary to external cloud LLMs.
* **Rejected Alternatives:** Direct un-redacted prompt transmission or relying solely on LLM provider privacy promises.

---

### ADR-060: Multi-Stage Document Upload Quarantine & CDR Isolation Pipeline
* **Context:** Protecting server infrastructure and document parsers against malware, executable macros, zip bombs, and polyglot files.
* **Options Considered:**
  1. Saving uploaded files directly to primary document storage buckets.
  2. Multi-Stage Ingestion Pipeline (`Staging Quarantine` $\rightarrow$ Magic Byte Validation $\rightarrow$ Containerized ClamAV Scan $\rightarrow$ CDR Disarm $\rightarrow$ SHA-256 Hashing $\rightarrow$ MinIO Promotion).
* **Decision:** Implement **Multi-Stage Document Upload Quarantine & CDR Isolation Pipeline**.
* **Reason:** Treats all uploaded files as untrusted content, containing malware and exploits before storage.
* **Consequences:** Ingestion enforces policy-configurable size limits, uncompressed expansion caps (10:1 ratio limit), and isolated sandbox parsing.
* **Rejected Alternatives:** Immediate primary bucket storage or un-sandboxed document parsing.

---

### ADR-061: Centralized Secret Isolation & KMS Abstraction Boundary
* **Context:** Preventing exposure of government API keys, database passwords, mTLS certificates, and JWT signing keys.
* **Options Considered:**
  1. Storing credentials in application source code, configuration files, or database tables.
  2. Centralized Secret Manager Abstraction (`SecretManagerInterface`) loading secrets dynamically into process memory at runtime.
* **Decision:** Implement **Centralized Secret Isolation & KMS Abstraction Boundary**.
* **Reason:** Ensures zero secrets are stored in Git repositories, frontend bundles, AI prompts, or log files.
* **Consequences:** Supports zero-downtime secret rotation and scoped credential access per service.
* **Rejected Alternatives:** Hardcoded secrets, Git-committed configuration files, or user-supplied API keys.

---

### ADR-062: Defense-in-Depth Field-Level AES-256-GCM Encryption Architecture
* **Context:** Safeguarding highly sensitive fields (PAN, GSTIN, bank details, government payloads) stored in PostgreSQL against database theft or raw disk inspection.
* **Options Considered:**
  1. Relying solely on full-disk database encryption.
  2. Layered Field-Level AES-256-GCM Encryption for `RESTRICTED` and `PII` fields with entity ULID Additional Authenticated Data (AAD), operating alongside database disk encryption.
* **Decision:** Implement **Defense-in-Depth Field-Level AES-256-GCM Encryption Architecture**.
* **Reason:** Provides defense-in-depth; protects sensitive data fields even if raw database tables are compromised.
* **Consequences:** Application encrypts sensitive attributes before SQL persistence; AAD prevents ciphertext swapping across rows.
* **Rejected Alternatives:** Disk-only database encryption or unencrypted sensitive fields.

---

### ADR-063: Quad-Operating Mode Government Credential Isolation & Transport Security
* **Context:** Securing integrations with external government portals (MCA, GSTN, MSME, Income Tax) while maintaining resilience during portal outages.
* **Options Considered:**
  1. Uniform live external API calls for all environments.
  2. Quad-Operating Modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`) with mTLS transport, circuit breaker isolation, and transport status separation.
* **Decision:** Implement **Quad-Operating Mode Government Credential Isolation & Transport Security**.
* **Reason:** Shields production government API credentials to `LIVE` mode, enables isolated testing, and prevents portal timeouts from causing false compliance failures.
* **Consequences:** Technical transport failures (`504 Gateway Timeout`) route cleanly to `MANUAL_FALLBACK` without triggering a business compliance `FAIL`.
* **Rejected Alternatives:** Hardcoded live API calls or allowing transport errors to fail compliance evaluations.

---

### ADR-064: Hash-Chained Audit Lineage Protection without Digital Signatures
* **Context:** Guaranteeing tamper evidence and non-repudiation for all workflow state transitions, rule evaluations, and human decisions.
* **Options Considered:**
  1. PKI digital signature framework for every audit event.
  2. SHA-256 Hash-Chained Audit Ledger ($H_n = \text{SHA256}(H_{n-1} \parallel P_n)$) using append-only database roles.
* **Decision:** Implement **Hash-Chained Audit Lineage Protection without Digital Signatures**.
* **Reason:** Delivers complete tamper evidence and mathematical non-repudiation aligned with Task 2 baseline without the extreme operational complexity and performance overhead of PKI certificate infrastructure.
* **Consequences:** Any alteration of historical audit entries breaks forward hash linkages; daily audit verification jobs detect tampering instantly.
* **Rejected Alternatives:** Complex PKI digital signature audit chains or un-chained database logs.

---

### ADR-065: Threat-Model-Driven SDLC Security Gates & Risk Benchmarks
* **Context:** Establishing security validation standards across development, testing, and operational release phases.
* **Options Considered:**
  1. Claims of 100% security or zero software vulnerabilities.
  2. Threat-Model-Driven SDLC framework (11 gates from Architecture Review to Penetration Testing) governed by explicit risk-driven acceptance criteria.
* **Decision:** Implement **Threat-Model-Driven SDLC Security Gates & Risk Benchmarks**.
* **Reason:** Replaces unrealistic claims with rigorous, benchmark-based security validation.
* **Consequences:** All security testing protocols are explicitly framed as future implementation and operational controls.
* **Rejected Alternatives:** Claims of absolute zero vulnerability or un-gated release processes.

---

### ADR-066: Policy-Controlled Dynamic Data Retention & Legal Hold Subsystem
* **Context:** Managing retention and deletion of bid documents, normalized facts, evidence, and audit logs according to statutory compliance requirements.
* **Options Considered:**
  1. Universal hardcoded retention periods (e.g., mandatory 10-year retention for all files).
  2. Policy-Controlled Lifecycle Engine dynamically bound to `PolicyVersion` settings, supporting soft-deletion, secure MinIO purging, and dual-control Legal Holds.
* **Decision:** Implement **Policy-Controlled Dynamic Data Retention & Legal Hold Subsystem**.
* **Reason:** Provides operational flexibility while protecting active investigations from automated data deletion.
* **Consequences:** Placing a `LegalHold` freezes all deletion schedules; audit tombstone ledgers preserve permanent disposal traces.
* **Rejected Alternatives:** Hardcoded universal retention periods or un-gated automated file deletion.

---

* **Consequences:** Celery queue tasks carry minimal ULID references; Redis requires TLS and strong password authentication.
* **Rejected Alternatives:** Un-encrypted internal channels or carrying raw PII payloads in queue messages.

---

### ADR-068: Structured JSON Observability Standard (`LogEvent` Schema)
* **Context:** Providing machine-readable diagnostic logging across all platform micro-containers and background services.
* **Options Considered:**
  1. Unstructured free-text log strings written to standard output.
  2. Standardized JSON `LogEvent` schema enforcing mandatory metadata fields (`timestamp`, `correlation_id`, `severity`, `event_category`, `component`, `environment`, `schema_version`).
* **Decision:** Implement **Structured JSON Observability Standard (`LogEvent` Schema)**.
* **Reason:** Enables automated log indexing, cross-service correlation, and rapid diagnostic parsing.
* **Consequences:** All application subsystems output machine-readable JSON log events matching the `LogEvent` schema.
* **Rejected Alternatives:** Free-text string logging or ad-hoc log field structures.

---

### ADR-069: Correlation-First Diagnostics Taxonomy Architecture (`correlationId`)
* **Context:** Tracing complex bid evaluation transactions across API gateways, Celery worker DAGs, AI gateways, and government integration adapters.
* **Options Considered:**
  1. Independent per-service request IDs without cross-boundary propagation.
  2. Correlation-First Diagnostics Taxonomy where correlation identifiers SHOULD be propagated whenever a causal relationship exists.
* **Decision:** Implement **Correlation-First Diagnostics Taxonomy Architecture (`correlationId`)**.
* **Reason:** Allows engineers and auditors to reconstruct complete end-to-end execution timelines using a correlation key whenever a causal relationship exists. Independently generated telemetry MAY use its own event, incident, or system identifiers when no originating request/workflow exists.
* **Consequences:** Log events, trace spans, and async queue tasks carry `correlationId` when causally linked.
* **Rejected Alternatives:** Isolated per-service IDs or un-correlated log streams.

---

### ADR-070: Operational Telemetry vs. Authoritative Audit Ledger Separation
* **Context:** Preventing ephemeral diagnostic logging from being confused with legal compliance proof or CVC vigilance audit ledgers.
* **Options Considered:**
  1. Merging operational logs and audit events into a single log aggregation platform.
  2. Strict architectural separation between ephemeral operational telemetry (`LogEvent`, `Span`) and the authoritative PostgreSQL SHA-256 hash-chained `AuditEvent` ledger.
* **Decision:** Implement **Operational Telemetry vs. Authoritative Audit Ledger Separation**.
* **Reason:** Protects the evidentiary integrity of the tamper-evident audit ledger while allowing ephemeral telemetry to be managed under policy-controlled retention policies.
* **Consequences:** Telemetry logs reference `audit_event_id` but never replace or alter PostgreSQL audit chain records.
* **Rejected Alternatives:** Single unified log store or relying on application logs for vigilance audit compliance.

---

### ADR-071: W3C Asynchronous Trace Context Propagation Architecture
* **Context:** Maintaining distributed trace graphs across synchronous REST APIs and asynchronous Celery background queue execution.
* **Options Considered:**
  1. Tracing synchronous HTTP API endpoints only.
  2. W3C Trace Context Propagation (`traceparent`, `tracestate`) injecting trace carriers into Redis message headers and Celery task metadata.
* **Decision:** Implement **W3C Asynchronous Trace Context Propagation Architecture**.
* **Reason:** Ensures distributed trace spans maintain parent-child relationships across asynchronous worker task retries.
* **Consequences:** Retries create distinct child spans (`task_attempt_id`) linked to the master task operation span.
* **Rejected Alternatives:** Synchronous-only tracing or un-linked background task execution traces.

---

### ADR-072: Privacy-Safe Pre-Log Telemetry Scrubbing & Redaction Pipeline
* **Context:** Preventing application logs and trace attributes from accidentally capturing sensitive PII, PAN numbers, bank accounts, passwords, or API keys.
* **Options Considered:**
  1. Trusting application developers to manually sanitize log messages in code.
  2. Pre-Log Privacy Proxy executing automated regex/NLP entity scrubbing, header suppression, and credential redaction before log emission.
* **Decision:** Implement **Privacy-Safe Pre-Log Telemetry Scrubbing & Redaction Pipeline**.
* **Reason:** Guarantees data privacy by design; prevents logs from becoming secondary data exfiltration paths.
* **Consequences:** Passwords, API tokens, PAN numbers, and raw document contents are strictly stripped from all log outputs.
* **Rejected Alternatives:** Un-sanitized raw logging or relying solely on manual developer compliance.

---

### ADR-073: Governed Metric Card Specification & High-Cardinality Protection
* **Context:** Preventing metric store memory exhaustion caused by high-cardinality label explosion (e.g., embedding raw ULIDs or user names in Prometheus labels).
* **Options Considered:**
  1. Allowing dynamic label injection in application metric counters.
  2. Governed Metric Card Specification enforcing strict label whitelists and prohibiting raw ULIDs or PII in metric dimensions.
* **Decision:** Implement **Governed Metric Card Specification & High-Cardinality Protection**.
* **Reason:** Protects metrics TSDB availability and ensures consistent metric aggregation across dashboards.
* **Consequences:** Metric cards define exact label dimensions; high-cardinality raw IDs are strictly forbidden as labels.
* **Rejected Alternatives:** Unrestricted metric label creation.

---

### ADR-074: AI Model Provenance & Non-Authoritative Telemetry Boundary
* **Context:** Tracking AI provider performance, prompt template versions, and schema validation failures while enforcing non-authoritative AI boundaries.
* **Options Considered:**
  1. Using AI accuracy or token metrics to automatically trigger compliance qualification outcomes.
  2. AI Telemetry (`AITelemetryEvent`) capturing provider, model version, prompt hash, and grounding status as pure operational telemetry.
* **Decision:** Implement **AI Model Provenance & Non-Authoritative Telemetry Boundary**.
* **Reason:** Preserves the core principle that AI is non-authoritative. AI metrics track system performance and CANNOT trigger compliance results.
* **Consequences:** AI metrics are used for governance and alerting; compliance evaluations run strictly in the deterministic AST engine.
* **Rejected Alternatives:** Treating AI metrics as qualification evidence.

---

### ADR-075: Government Integration Transport Failure vs. Business Result Telemetry Separation
* **Context:** Monitoring government integration gateway connectivity without allowing portal timeouts or network glitches to fail bidder compliance evaluations.
* **Options Considered:**
  1. Logging a single generic failure event whenever a government API call fails.
  2. Strict Telemetry Separation between technical transport status (`504 Gateway Timeout`) and domain business verification outcomes (`UNMATCHED`).
* **Decision:** Implement **Government Integration Transport Failure vs. Business Result Telemetry Separation**.
* **Reason:** Ensures technical infrastructure issues trigger transport retries or `MANUAL_FALLBACK` without falsely marking bidders as non-compliant.
* **Consequences:** Telemetry logs `transport_status` and `business_verification_result` as separate attributes.
* **Rejected Alternatives:** Merging transport errors with domain verification outcomes.

---

### ADR-076: Candidate Service Level Indicator (SLI) & Objective (SLO) Governance
* **Context:** Setting quantitative reliability benchmarks across API, workflow, AI, government integration, and audit subsystems.
* **Options Considered:**
  1. Hardcoding static production Service Level Agreements (SLAs) in system code.
  2. Framework of Candidate SLIs and Proposed SLOs evaluated over rolling 30-day windows.
* **Decision:** Implement **Candidate Service Level Indicator (SLI) & Objective (SLO) Governance**.
* **Reason:** Establishes clear engineering reliability targets while acknowledging that formal SLAs require department policy approval.
* **Consequences:** Reliability metrics measure performance against proposed benchmarks (e.g., 99.5% API availability).
* **Rejected Alternatives:** Hardcoding arbitrary production SLA guarantees in software architecture.

---

### ADR-077: Three-Tier Actionable Alert Hierarchy & Deduplication Framework
* **Context:** Preventing notification noise and alert fatigue for on-call operations and security personnel.
* **Options Considered:**
  1. Triggering instant un-throttled emails/SMS for every log error string.
  2. Three-Tier Alert Hierarchy (`CRITICAL`, `WARNING`, `INFORMATIONAL`) with mandatory deduplication windows, runbook links, and recovery conditions.
* **Decision:** Implement **Three-Tier Actionable Alert Hierarchy & Deduplication Framework**.
* **Reason:** Guarantees that every firing alert is high-signal, actionable, and linked to a concrete operational runbook.
* **Consequences:** Repeated alerts within 15 minutes are deduplicated; critical alerts require clear diagnostic runbooks.
* **Rejected Alternatives:** Un-throttled email notifications or non-actionable alert noise.

---

### ADR-078: Policy-Controlled Telemetry Retention & Dual-Control Legal Hold Governance
* **Context:** Managing log and metric storage lifecycles while complying with statutory vigilance audit requirements.
* **Options Considered:**
  1. Universal static log retention periods (e.g., mandatory 10-year retention for all debug logs).
  2. Policy-Controlled Telemetry Retention Engine supporting tier-specific lifecycles and dual-control `LegalHold` overrides.
* **Decision:** Implement **Policy-Controlled Telemetry Retention & Dual-Control Legal Hold Governance**.
* **Reason:** Optimizes storage expenditure while ensuring active vigilance investigations freeze log deletion schedules.
* **Consequences:** Placing a `LegalHold` freezes retention cleanup; log disposal actions emit audit ledger events.
* **Rejected Alternatives:** Static universal retention periods or un-gated automated log purging.

---

### ADR-079: Role-Based Observability Access Control & Diagnostic Access Auditing
* **Context:** Restricting visibility of system log streams, trace spans, and operational dashboards to authorized user roles.
* **Options Considered:**
  1. Allowing all authenticated users full access to monitoring dashboards.
  2. Role-Based Observability Access Control matrix enforcing organizational context filtering and logging all diagnostic access requests.
* **Decision:** Implement **Role-Based Observability Access Control & Diagnostic Access Auditing**.
* **Reason:** Prevents unauthorized procurement personnel from viewing cross-tenant metrics or sensitive system logs.
* **Consequences:** Accessing raw diagnostic log viewers requires the `telemetry:read_diagnostics` capability and generates an audit log entry.
* **Rejected Alternatives:** Unrestricted monitoring access or global admin dashboard permissions.

---

### ADR-080: Vendor-Neutral OpenTelemetry Abstraction Layer (`TelemetryProviderInterface`)
* **Context:** Emitting telemetry data without locking the platform codebase to specific cloud vendors or proprietary monitoring SDKs.
* **Options Considered:**
  1. Integrating proprietary vendor monitoring SDKs directly into application route handlers.
  2. Vendor-Neutral Telemetry Abstraction (`TelemetryProviderInterface`) supporting standard OpenTelemetry Protocol (OTLP) exports.
* **Decision:** Implement **Vendor-Neutral OpenTelemetry Abstraction Layer (`TelemetryProviderInterface`)**.
* **Reason:** Ensures application code remains completely independent of cloud monitoring vendors (AWS, Azure, GCP) or open-source backends (Grafana, OpenSearch).
* **Consequences:** Telemetry exports follow standard OTLP specifications over gRPC/HTTP.
* **Rejected Alternatives:** Direct proprietary vendor SDK integration.

---

### ADR-081: Four-Tier Environment Isolation & Data Protection Boundary
* **Context:** Preventing production procurement bid data, live government payload credentials, and sensitive PII from leaking into development, testing, or staging environments.
* **Options Considered:**
  1. Shared database instances across development, staging, and production tiers.
  2. Four-Tier Environment Isolation (`LOCAL`, `DEVELOPMENT`, `TEST_STAGING`, `PRODUCTION`) with zero automatic production data flow to lower environments and strict mock/sandbox government adapter scoping.
* **Decision:** Implement **Four-Tier Environment Isolation & Data Protection Boundary**.
* **Reason:** Guarantees data privacy by design, protects live government API credentials, and ensures lower environments operate strictly on synthetic or sanitized test data.
* **Consequences:** Production VPCs share zero subnets, credentials, or databases with lower environment VPCs.
* **Rejected Alternatives:** Shared development/staging database instances or automatic production data replication.

---

### ADR-082: Managed Container Compute Reference Architecture — AWS ECS Fargate
* **Context:** Selecting a scalable, low-overhead container compute architecture for web API endpoints and background workers without managing virtual machine infrastructure.
* **Options Considered:**
  1. Managing self-hosted EC2 virtual machine instances with manual Docker orchestration.
  2. Kubernetes cluster management (EKS).
  3. Managed Container Compute Reference Architecture (AWS ECS Fargate) running isolated API, worker, and frontend container tasks.
* **Decision:** Implement **Managed Container Compute Reference Architecture — AWS ECS Fargate**.
* **Reason:** ECS Fargate is the selected AWS reference deployment model; the logical compute architecture remains portable to equivalent managed container platforms. Provides auto-scaling, process isolation, and minimal operational overhead for the SIH26100 platform while avoiding Kubernetes cluster management complexity.
* **Consequences:** Application tasks execute as non-root container tasks on Fargate with defined vCPU/RAM profiles; logical containers remain portable across cloud infrastructure.
* **Rejected Alternatives:** Un-orchestrated EC2 virtual machines or full EKS Kubernetes cluster management.

---

### ADR-083: Multi-Tier Network Segmentation & Private Subnet Isolation
* **Context:** Preventing public internet access to core databases, Redis message brokers, background workers, and object storage buckets.
* **Options Considered:**
  1. Single public VPC subnet housing application containers and database endpoints.
  2. Multi-Tier Network Segmentation allocating public DMZ subnets for ALB, private application subnets for API/UI tasks, and private data subnets for database/storage endpoints.
* **Decision:** Implement **Multi-Tier Network Segmentation & Private Subnet Isolation**.
* **Reason:** Enforces strict perimeter security; databases and Redis brokers carry zero public IP addresses and zero direct internet routing.
* **Consequences:** Outbound internet access from private subnets for government integrations and AI calls routes exclusively through NAT Gateways with static Elastic IP allowlisting.
* **Rejected Alternatives:** Publicly accessible database endpoints or single-subnet network topology.

---

### ADR-084: Four-Tier Infrastructure Trust Zone Architecture
* **Context:** Defining infrastructure trust boundaries and component placement aligned with the Task 8 Security Architecture.
* **Options Considered:**
  1. Single flat trust boundary across all server components.
  2. Four-Tier Infrastructure Trust Zone Mapping (Zone 0: Public, Zone 1: Ingress Buffer, Zone 2: App Core, Zone 3: Data Sanctuary).
* **Decision:** Implement **Four-Tier Infrastructure Trust Zone Architecture**.
* **Reason:** Enforces strict boundary crossings; data moving between trust zones requires explicit authentication, capability checks, and pre-log privacy scrubbing.
* **Consequences:** Subsystems reside in explicit trust zones governed by fine-grained security group rules and IAM policies.
* **Rejected Alternatives:** Flat unsegmented server network.

---

### ADR-085: Untrusted Document Processing Sandbox & Zero-Egress Isolation
* **Context:** Protecting core application servers from malicious PDF files, embedded macros, or OCR parsing exploits uploaded by untrusted bidders.
* **Options Considered:**
  1. Executing PDF parsing and OCR extraction directly on main web API container instances.
  2. Isolated Untrusted Document Processing Sandbox running in dedicated worker containers in a network-isolated execution boundary with read-only filesystems and strict memory limits.
* **Decision:** Implement **Untrusted Document Processing Sandbox & Zero-Egress Isolation**.
* **Reason:** Isolates untrusted document processing; document-processing workloads operate in a network-isolated execution boundary with no outbound network access by default; implementation may use runtime-specific network isolation such as disabled networking.
* **Consequences:** Malware or parsing exploits cannot execute network callbacks or compromise the primary database.
* **Rejected Alternatives:** Parsing untrusted uploads directly inside web API tasks.

---

### ADR-086: Multi-AZ Relational Database Deployment & Synchronous Failover (PostgreSQL)
* **Context:** Guaranteeing high availability, point-in-time recovery, and zero data loss for PostgreSQL (`pgvector`, JSONB, ULIDs, tamper-evident audit ledger).
* **Options Considered:**
  1. Single-node PostgreSQL database instance without replica failover.
  2. Multi-AZ Managed PostgreSQL Deployment with synchronous physical standby replication, Continuous WAL streaming, and automated DNS failover.
* **Decision:** Implement **Multi-AZ Relational Database Deployment & Synchronous Failover**.
* **Reason:** Protects core procurement facts and audit ledgers against single-AZ cloud infrastructure outages ($< 60$s automatic failover).
* **Consequences:** Primary database commits stream synchronously to standby replicas; PgBouncer handles client connection pooling.
* **Rejected Alternatives:** Single-AZ database deployment or asynchronous un-monitored replication.

---

### ADR-087: Isolated Multi-Pool Redis & Celery Worker Deployment
* **Context:** Preventing background document processing or OCR batch tasks from starving interactive procurement officer workbench actions.
* **Options Considered:**
  1. Single monolithic Celery worker pool processing all background tasks from one queue.
  2. Isolated Multi-Pool Celery Worker Strategy distributing tasks across dedicated queues (`high-priority`, `workflows`, `doc-processing`, `govt-verifications`) with tailored concurrency and logical Redis workload isolation.
* **Decision:** Implement **Isolated Multi-Pool Redis & Celery Worker Deployment**.
* **Reason:** Guarantees sub-second responsiveness for officer workbench actions. Logical isolation of task brokerage, idempotency/cache functions, rate limiting, and other workloads SHALL use dedicated Redis deployments, logical isolation, namespaces/keyspaces, or equivalent mechanisms according to operational and security requirements. Redis deployment uses an availability architecture appropriate to the selected Redis-compatible service, including multi-AZ/failover capabilities where supported and required.
* **Consequences:** Worker tasks scale independently based on queue-specific depth metrics without coupling telemetry to task processing.
* **Rejected Alternatives:** Single global Celery worker queue or hardcoded logical database coupling.

---

### ADR-088: Multi-Bucket Object Storage Taxonomy & Legal Hold Governance
* **Context:** Managing raw untrusted bidder file uploads, sanitized disarmed documents, extracted evidence packages, and system audit reports.
* **Options Considered:**
  1. Storing all files in a single flat storage bucket with uniform permissions.
  2. Multi-Bucket Object Storage Taxonomy (`quarantine-raw`, `clean-documents`, `evidence-ledger`, `reports-audit`) with KMS-SSE encryption, optional Object Lock WORM controls, and legal hold support.
* **Decision:** Implement **Multi-Bucket Object Storage Taxonomy & Legal Hold Governance**.
* **Reason:** Separates untrusted raw uploads from sanitized clean assets. Original bidder submissions MAY use object-lock/WORM controls where required by approved retention, legal-hold, and evidence-governance policy while preserving original SHA-256 hash provenance.
* **Consequences:** Storage lifecycle purges follow approved retention policies; legal holds override dynamic retention purges.
* **Rejected Alternatives:** Single flat storage bucket.

---

### ADR-089: KMS Envelope Encryption & Dynamic Secret Injection Boundary
* **Context:** Managing database passwords, Redis tokens, government certificates, and AI provider API keys without hardcoding credentials in code or Git repositories.
* **Options Considered:**
  1. Storing secrets in application configuration files or container environment variables written to Git.
  2. Centralized Secret Manager & KMS Envelope Encryption injecting secrets dynamically into container task memory at runtime.
* **Decision:** Implement **KMS Envelope Encryption & Dynamic Secret Injection Boundary**.
* **Reason:** Prevents secret leakage in code repositories, container images, or build logs.
* **Consequences:** Secrets are encrypted using customer-managed KMS keys and rotated on policy-defined schedules (30–90 days).
* **Rejected Alternatives:** Hardcoded secrets in code, Git, or Dockerfiles.

---

### ADR-090: Machine Service Identity Least-Privilege IAM Scoping
* **Context:** Granting container workloads infrastructure permissions without providing broad AWS administrative rights.
* **Options Considered:**
  1. Sharing a single administrative IAM role across all container tasks.
  2. Dedicated Task IAM Execution Roles (`role-sih26100-api-task`, `role-sih26100-worker-doc-task`, `role-sih26100-worker-govt-task`) enforcing strict resource least privilege.
* **Decision:** Implement **Machine Service Identity Least-Privilege IAM Scoping**.
* **Reason:** Limits blast radius if a single container workload is compromised.
* **Consequences:** The document parsing task role cannot access government secrets or write to PostgreSQL audit tables.
* **Rejected Alternatives:** Global shared container IAM role.

---

### ADR-091: CI/CD Supply-Chain Vulnerability Gates & SBOM Provenance Verification
* **Context:** Securing software build pipelines against compromised third-party dependencies, malicious packages, or unauthorized container images.
* **Options Considered:**
  1. Building and deploying container images without automated dependency or vulnerability checks.
  2. Multi-Stage CI/CD Security Pipeline enforcing static analysis, secret scanning, dependency audits, SBOM generation, container scanning, and artifact provenance signatures.
* **Decision:** Implement **CI/CD Supply-Chain Vulnerability Gates & SBOM Provenance Verification**.
* **Reason:** Protects software supply chain integrity before code reaches production environments. Artifact signing/provenance is a supply-chain security control and is independent of the application's tamper-evident AuditEvent SHA-256 hash chain.
* **Consequences:** Images containing critical CVEs or violating vulnerability policies are automatically rejected by deployment gates; no digital signatures are added to AuditEvent.
* **Rejected Alternatives:** Un-scanned container image builds.

---

### ADR-092: Zero-Downtime Blue/Green Release Deployment Strategy
* **Context:** Deploying application updates to production without interrupting active procurement officer reviews or causing HTTP 5xx errors.
* **Options Considered:**
  1. In-place container task restarts (causing temporary service downtime).
  2. Blue/Green Deployment Strategy deploying parallel task sets, verifying health check readiness, and shifting ALB target group traffic weights.
* **Decision:** Implement **Zero-Downtime Blue/Green Release Deployment Strategy**.
* **Reason:** Provides seamless zero-downtime release deployments with controlled traffic cutover after required health/readiness checks satisfy approved release policy. Automated rollback MAY be triggered when configured release-health criteria are violated; otherwise the deployment enters operator review/escalation.
* **Consequences:** Production deployments provision green task sets, verify readiness according to policy, and shift traffic smoothly.
* **Rejected Alternatives:** In-place container task restarts or un-monitored rolling deployments.

---

### ADR-093: Expand/Contract Database Schema Migration Pattern
* **Context:** Modifying PostgreSQL relational database schemas during application releases without locking production tables or crashing active web API tasks.
* **Options Considered:**
  1. Executing destructive DDL migrations directly during container startup.
  2. Expand/Contract Database Migration Pattern executing additive DDL changes first, deploying dual-reading application tasks, backfilling historical data, and dropping deprecated columns in subsequent releases.
* **Decision:** Implement **Expand/Contract Database Schema Migration Pattern**.
* **Reason:** Prevents database downtime, table locking failures, and application incompatibility during schema evolution.
* **Consequences:** DDL changes set 5-second statement timeouts; migrations execute via dedicated pre-deployment tasks.
* **Rejected Alternatives:** Destructive synchronous DDL migrations at container startup.

---

### ADR-094: Controlled Egress Government Network Gateway Architecture
* **Context:** Routing outbound government integration adapter requests safely while satisfying external portal IP allowlisting and transport security requirements.
* **Options Considered:**
  1. Direct un-controlled outbound internet access from container tasks with dynamic public IPs.
  2. Controlled Egress Government Gateway Architecture routing outbound government adapter traffic through controlled egress gateways with static IP allowlisting (where required/supported) and secure TLS transport with certificate validation (pinning/mTLS where explicitly required).
* **Decision:** Implement **Controlled Egress Government Network Gateway Architecture**.
* **Reason:** Satisfies government security onboarding requirements (static IP allowlisting where required, TLS certificate validation) while isolating application core logic.
* **Consequences:** Outbound government API calls route through controlled gateways with circuit breaker protection and integration-appropriate transport validation.
* **Rejected Alternatives:** Direct un-gated outbound internet calls from web API tasks.

---

### ADR-095: Feature Flag Governance & Auditable Environment Scoping
* **Context:** Toggling application operational modes (e.g. government adapter LIVE/MOCK modes, AI Gateway routing targets) dynamically at runtime.
* **Options Considered:**
  1. Hardcoding environment settings in application source code or un-audited environment variables.
  2. Governed Feature Flag Architecture with auditable toggle events, scope parameters, and strict security isolation.
* **Decision:** Implement **Feature Flag Governance & Auditable Environment Scoping**.
* **Reason:** Allows operations teams to switch adapter modes or AI fallback routes dynamically; all flag modifications emit audit log events.
* **Consequences:** Feature flags cannot bypass authentication or deterministic compliance evaluation rules.
* **Rejected Alternatives:** Hardcoded runtime flags or un-audited configuration overrides.

---

### ADR-096: Human Decision Authority & Non-Authoritative AI UX Boundary
* **Context:** Preventing AI model output from being presented or visually interpreted as an automated, final qualification or disqualification decision.
* **Options Considered:**
  1. Allowing AI models to trigger automated bidder qualification or disqualification status changes.
  2. Non-Authoritative AI UX Boundary establishing that AI models assist with extraction, classification, and summarization, while the human Procurement Officer retains sole decision authority.
* **Decision:** Implement **Human Decision Authority & Non-Authoritative AI UX Boundary**.
* **Reason:** Preserves the core system axiom (`AI interprets. Authorized sources verify. Rules evaluate. Evidence proves. Human approves.`). Prevents automated AI disqualification.
* **Consequences:** All AI outputs carry clear visual disclaimers; qualification decisions require manual officer written justification and signature.
* **Rejected Alternatives:** Autonomous AI qualification decision UI.

---

### ADR-097: Evidence-First Compliance Matrix & Multi-Dimensional Lineage UI
* **Context:** Designing the compliance evaluation UI so officers can trace any rule determination backward to its underlying evidence source.
* **Options Considered:**
  1. Displaying static, non-interactive compliance summary scores without underlying evidence links.
  2. Evidence-First Compliance Matrix UI allowing officers to step backward from rule status to fact normalization, extraction bounding box, and raw SHA-256 document digest.
* **Decision:** Implement **Evidence-First Compliance Matrix & Multi-Dimensional Lineage UI**.
* **Reason:** Ensures 100% explainability and auditability for every compliance evaluation outcome.
* **Consequences:** Officers can inspect bounding box coordinates, extraction confidence, and government registry responses directly from the matrix.
* **Rejected Alternatives:** Single black-box compliance score UI.

---

### ADR-098: Multi-Dimensional Status Taxonomy Separation
* **Context:** Preventing technical connection errors, missing documents, advisory risk scores, or AI extraction uncertainty from being collapsed into binary PASS/FAIL badges.
* **Options Considered:**
  1. Binary PASS/FAIL status taxonomy for all evaluation states.
  2. Multi-Dimensional Status Taxonomy rendering 10 distinct status badges (`VERIFIED`, `UNVERIFIED`, `MISSING`, `STALE`, `CONFLICTING`, `INVALID`, `UNKNOWN`, `NOT_APPLICABLE`, `MISSING_EVIDENCE`, `HUMAN_REVIEW`).
* **Decision:** Implement **Multi-Dimensional Status Taxonomy Separation**.
* **Reason:** Prevents technical API timeouts or missing evidence from automatically triggering bidder disqualification.
* **Consequences:** Status badges render with distinct color coding and explicit text labels.
* **Rejected Alternatives:** Binary PASS/FAIL status collapsing.

---

### ADR-099: Role-Aware & Classification-Aware Information Architecture
* **Context:** Ensuring the UI enforces role-based access control (RBAC) and data classification sensitivity rules across all workspace views.
* **Options Considered:**
  1. Universal UI data exposure relying solely on backend access controls.
  2. Role-Aware & Classification-Aware Information Architecture dynamically tailoring menus, action buttons, PII masking, and data classification badges (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, `PII`) per user role.
* **Decision:** Implement **Role-Aware & Classification-Aware Information Architecture**.
* **Reason:** Enhances user experience by hiding unauthorized actions while visually highlighting sensitive data handling.
* **Consequences:** Backend API remains authoritative security boundary; UI unmasking of PII triggers audit logging.
* **Rejected Alternatives:** Uniform UI data exposure regardless of role.

---

### ADR-100: Version-Aware Tender & Policy Evaluation Workspace Architecture
* **Context:** Evaluating bids against modified tender corrigenda or updated policy rule definitions over time.
* **Options Considered:**
  1. Evaluating bids against dynamic, un-versioned global rule definitions.
  2. Version-Aware Tender & Policy Evaluation Workspace explicitly binding every view and evaluation to a specific `TenderVersion` and `PolicyVersion`.
* **Decision:** Implement **Version-Aware Tender & Policy Evaluation Workspace Architecture**.
* **Reason:** Guarantees historical reproducibility and evaluation integrity when tender amendments or policy thresholds change.
* **Consequences:** UI headers prominently display bound version IDs; corrigenda diffs highlight rule criteria changes.
* **Rejected Alternatives:** Un-versioned global evaluation workspaces.

---

### ADR-101: Secure Document Review Boundary & Derivative Provenance Viewer
* **Context:** Rendering untrusted uploaded PDFs and Office documents safely in browser client viewports without exposing users to malware or script exploits.
* **Options Considered:**
  1. Opening raw uploaded files directly in browser native plugins.
  2. Secure Document Review Boundary rendering disarmed sanitized derivatives alongside original SHA-256 payload digests and bounding box extraction overlays.
* **Decision:** Implement **Secure Document Review Boundary & Derivative Provenance Viewer**.
* **Reason:** Prevents browser-based malware execution while maintaining clear distinction between original submissions and sanitized derivatives.
* **Consequences:** PDF canvas virtualization prevents browser memory bloat on large multi-hundred-page documents.
* **Rejected Alternatives:** Direct un-sanitized browser rendering of raw uploads.

---

### ADR-102: Government Integration Verification State Presentation
* **Context:** Presenting government registry verification outcomes (`LIVE`, `SANDBOX`, `MANUAL_FALLBACK`) clearly without misrepresenting technical timeouts as bidder failure.
* **Options Considered:**
  1. Rendering failed API connectivity as bidder non-compliance.
  2. Government Verification State Presentation rendering technical failure as neutral `MANUAL_FALLBACK_REQUIRED` banners and displaying explicit adapter operating mode badges.
* **Decision:** Implement **Government Integration Verification State Presentation**.
* **Reason:** Preserves Task 5 architectural boundary separating technical transport failure from business verification result.
* **Consequences:** Officers receive clear manual fallback prompts when external government gateways time out.
* **Rejected Alternatives:** Displaying API timeouts as bidder non-compliance.

---

### ADR-103: Human Review Workspace & Non-Destructive Override Governance
* **Context:** Managing evaluation exceptions, missing evidence, low-confidence extractions, and manual officer overrides.
* **Options Considered:**
  1. Allowing manual overrides to overwrite historical automated evaluation snapshot records.
  2. Human Review Workspace with non-destructive override governance creating linked `ManualOverride` records while preserving immutable historical snapshots.
* **Decision:** Implement **Human Review Workspace & Non-Destructive Override Governance**.
* **Reason:** Protects audit integrity and evaluation snapshot reproducibility.
* **Consequences:** All overrides require written justification notes; policy-sensitive exemptions enforce four-eyes supervisory review.
* **Rejected Alternatives:** Mutating historical evaluation database snapshots.

---

### ADR-104: Tamper-Evident SHA-256 Audit Explorer Architecture
* **Context:** Providing auditors with an interactive UI to verify procurement decision timelines and audit block hash continuity.
* **Options Considered:**
  1. Providing raw SQL database logs or un-indexed log files to auditors.
  2. Tamper-Evident SHA-256 Audit Explorer UI displaying continuous block hash links ($H_n = \text{SHA-256}(H_{n-1} \parallel \text{Payload})$) and event payload inspection.
* **Decision:** Implement **Tamper-Evident SHA-256 Audit Explorer Architecture**.
* **Reason:** Enables independent verification of audit chain continuity without falsely asserting digital signatures or PKI non-repudiation.
* **Consequences:** Auditors can trace event lineage and verify block hash integrity across all tender actions.
* **Rejected Alternatives:** Un-indexed text log files or unsupported digital-signature assertions.

---

### ADR-105: Accessible & Enterprise-Grade Procurement Design System Standards
* **Context:** Defining visual aesthetics, color semantics, component libraries, and accessibility standards for the platform UI.
* **Options Considered:**
  1. Consumer-oriented AI interface designs with purple neon gradients, glassmorphism, and chatbot bubbles.
  2. Accessible & Enterprise-Grade Procurement Design System establishing deep navy/blue tones, dense data tables, clear status badges, and WCAG 2.1 AA accessibility guidelines.
* **Decision:** Implement **Accessible & Enterprise-Grade Procurement Design System Standards**.
* **Reason:** Creates a serious, professional government procurement interface with high data density and accessible contrast.
* **Consequences:** Color is never the sole indicator of status; high-contrast focus indicators and semantic ARIA markup are enforced.
* **Rejected Alternatives:** Consumer AI chatbot interfaces or low-contrast neon themes.

---

### ADR-106: Client-Side Security Isolation & Backend-Authoritative RBAC UX Boundary
* **Context:** Protecting frontend client execution from XSS, clickjacking, CSRF, and authorization bypass vulnerabilities.
* **Options Considered:**
  1. Relying on client-side JavaScript checks as the sole authorization mechanism.
  2. Client-Side Security Isolation with strict CSP headers, DOMPurify HTML sanitization of untrusted text, and backend-authoritative RBAC enforcement on every API request.
* **Decision:** Implement **Client-Side Security Isolation & Backend-Authoritative RBAC UX Boundary**.
* **Reason:** Ensures client-side UI hiding improves UX without becoming a single point of security failure.
* **Consequences:** Untrusted OCR text is sanitized before DOM insertion; secrets and API keys are strictly excluded from frontend bundles.
* **Rejected Alternatives:** Client-side only security boundaries.

---

### ADR-107: Telemetry-Decoupled Frontend Observability & OpenTelemetry Integration
* **Context:** Capturing client-side errors, page performance, and user interactions without compromising user privacy or creating compliance dependencies.
* **Options Considered:**
  1. Treating client telemetry as authoritative evidence for bidder compliance evaluations.
  2. Telemetry-Decoupled Frontend Observability propagating correlation IDs via OpenTelemetry Web SDK while keeping operational metrics strictly isolated from compliance evidence.
* **Decision:** Implement **Telemetry-Decoupled Frontend Observability & OpenTelemetry Integration**.
* **Reason:** Integrates with Task 9 operational observability without allowing ephemeral browser metrics to influence qualification decisions.
* **Consequences:** Client telemetry payloads are scrubbed of PII before export; correlation IDs link browser requests to backend traces.
* **Rejected Alternatives:** Using client telemetry as compliance evidence.







