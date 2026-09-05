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



