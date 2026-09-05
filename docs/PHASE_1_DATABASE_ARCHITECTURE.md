# Phase 1 Database Architecture Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-007  
**Version:** 1.1.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines technical database architecture specifications, indexing policies, transaction isolation models, and identifier strategies. No database creation scripts, SQL migrations, ORM models, or backend/frontend source files are created.

---

## 1. Primary Database Technology Baseline

The single primary database engine selected for the MVP is **PostgreSQL 16+**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL 16+ DATABASE ARCHITECTURE                     │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. RELATIONAL CORE    │ Transactional integrity (ACID) for Tenders, Bidders,│
│                       │ Submissions, Requirements, Decisions, & Audit Logs  │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. CONTROLLED JSONB   │ Flexible storage for raw API payloads, dynamic OCR  │
│                       │ token coordinates, & rule execution traces          │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. PGVECTOR EXTENSION │ Reserved strictly for semantic RAG vector retrieval │
│                       │ of tender clauses (if justified in future)          │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. EXCLUDED EXTENSIONS│ PostGIS is EXCLUDED (no spatial/geographic queries) │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

### 1.1 Relational Core Table Usage Policy
- All core business entities MUST be defined as strict relational tables.
- Foreign keys, `NOT NULL` constraints, unique constraints, and check constraints MUST be declared explicitly to enforce data integrity at the database layer.

### 1.2 Controlled `JSONB` Usage Policy
- `JSONB` data types are permitted ONLY for raw API response payloads, OCR bounding-box token coordinates, dynamic rule execution traces, and system configuration payloads.
- `JSONB` MUST NOT be used to bypass relational normalization for core entities.

### 1.3 `pgvector` Extension Usage Policy
- Reserved *only where explicitly justified* for storing vector embeddings of tender clauses (`tender_clause_embeddings`) to support future semantic search or RAG. Indexed via HNSW algorithms.

### 1.4 Single Primary Database Topology
- PostgreSQL serves as the single source of truth database. PostGIS is explicitly **removed**.

---

## 2. Identifier Strategy for MVP

To balance database index performance, security, and public API exposure, the platform uses a dual-identifier strategy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DUAL IDENTIFIER STRATEGY                            │
├─────────────────────────┬───────────────────────────────────────────────────┤
│ INTERNAL PRIMARY KEY    │ 26-character Crockford Base32 encoded ULIDs       │
│                         │ • Lexicographically sortable, time-ordered ID     │
│                         │ • Generally improves index locality over UUIDv4   │
│                         │ • Zero auto-increment sequence leakage            │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ EXTERNAL PUBLIC KEY     │ UUIDv4 (128-bit Random Unique Identifier)         │
│                         │ • Exposed in REST API endpoints & UI routing URLs │
│                         │ • Reduces predictable enumeration risks           │
│                         │ • Authorization remains strictly MANDATORY        │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ NATURAL IDENTIFIERS     │ PAN, GSTIN, CIN, Udyam Number                     │
│                         │ • Indexed attributes under `bidder_identities`    │
│                         │ • NEVER used as single universal primary key      │
└─────────────────────────┴───────────────────────────────────────────────────┘
```

### Technical ULID & Security Clarifications:
1. **ULID Structure & Index Locality:** Internal primary keys use **26-character Crockford Base32 encoded ULIDs with lexicographically sortable, time-ordered representation**. ULIDs generally improve index locality compared with random UUIDv4 identifiers because their encoded values are time-ordered. They do not guarantee elimination of B-tree fragmentation or page splits.
2. **UUIDv4 Security Scope:** UUIDv4 makes resource identifiers difficult to predict and reduces predictable identifier enumeration risk. It does **NOT** replace authentication, authorization, or object-level access control. Authorization checks remain strictly mandatory for every API request.

---

## 3. Password, Credential, & Secret Handling Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 PASSWORD & CREDENTIAL HANDLING SECURITY                     │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. PLAINTEXT STORAGE  │ STRICTLY PROHIBITED (Passwords never stored unhashed)│
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. REVERSIBLE ENCRYPT │ STRICTLY PROHIBITED (No symmetric encryption for pass)│
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. PASSWORD HASHING   │ Dedicated slow hashing algorithm: Argon2id / bcrypt │
│                       │ with unique per-user cryptographically random salt   │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. API KEYS / SECRETS │ STRICTLY ISOLATED from application database tables  │
│                       │ Managed exclusively via Vault / environment mounts  │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 4. Multi-Rule Mapping & Verification Attempt Schemas

### 4.1 Requirement to Rule Mapping Schema (`requirement_rule_maps`)
Supports binding multiple deterministic rules to a single tender requirement with priority ordering:
- `id`: ULID (`CHAR(26)`) PK
- `tender_requirement_id`: ULID (`CHAR(26)`) FK
- `compliance_rule_id`: ULID (`CHAR(26)`) FK
- `rule_priority_order`: `INTEGER` (Check `> 0`)
- `is_mandatory_for_requirement`: `BOOLEAN` (Default `TRUE`)
- `created_at`: `TIMESTAMPTZ`

### 4.2 Government Verification Retry Schema (`verification_attempts`)
Preserves historical retry records for external API calls without overwriting past attempts:
- `id`: ULID (`CHAR(26)`) PK
- `verification_request_id`: ULID (`CHAR(26)`) FK
- `attempt_number`: `INTEGER` (Check `> 0`)
- `execution_mode`: `VARCHAR(50)` (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`)
- `http_status_code`: `INTEGER`
- `attempted_at`: `TIMESTAMPTZ`
- `error_details`: `TEXT`

---

## 5. Temporal & Versioning Architecture

Guarantees point-in-time historical explainability across five versioning tiers:
1. `tender_versions` — Corrigenda versioning.
2. `compliance_rules` & `policy_versions` — Policy versioning.
3. `document_extractions` — OCR model versioning.
4. `evidence_records` — Append-only evidence versioning.
5. `audit_events` & `audit_hash_chain_blocks` — Cryptographic audit block versioning.

---

## 6. Transaction Boundaries & Concurrency Control

| Operational Transaction Boundary | Affected Entities / Tables | Minimum Isolation Level | Concurrency Control Mechanism |
| :--- | :--- | :--- | :--- |
| **Tender Version Activation** | `tenders`, `tender_versions`, `tender_requirements` | `READ COMMITTED` | Optimistic locking via `version_number` |
| **Bid Submission Ingestion** | `bid_submissions`, `submission_covers`, `documents` | `READ COMMITTED` | Explicit Row-level lock on `bid_submissions` |
| **Verification Attempt & Result** | `verification_requests`, `verification_attempts`, `verification_results` | `READ COMMITTED` | Idempotency key lookup on `request_id` + `attempt_number` |
| **Compliance Evaluation Run** | `compliance_evaluations`, `evidence_records`, `risk_profiles` | `REPEATABLE READ` | Snapshot isolation over requirement criteria |
| **Officer Decision & Sign-Off** | `officer_decisions`, `manual_overrides`, `audit_events`, `hash_blocks` | `SERIALIZABLE` | Strict serialization + Cryptographic block seal |

---

## 7. Connection Pooling & Performance Topology

- **Async Connection Pool:** Backend FastAPI application connects via an asynchronous pool driver (`asyncpg`) managed by PgBouncer.
- **Read-Replica Topology:** Heavy analytical queries (CVC audit exports, dashboards) route to PostgreSQL Read-Replicas, preserving primary master node IOPS for transactional officer decisions.
