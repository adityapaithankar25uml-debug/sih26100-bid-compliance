# Phase 1 Database Architecture Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-007  
**Version:** 1.0.0  
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
- All core business entities (Tenders, Tender Versions, Requirements, Rules, Bidders, Submissions, Verifications, Evidence, Decisions, Audit Logs) MUST be defined as strict relational tables.
- Foreign keys, `NOT NULL` constraints, unique constraints, and check constraints MUST be declared explicitly to enforce data integrity at the database layer.

### 1.2 Controlled `JSONB` Usage Policy
- `JSONB` data types are permitted ONLY for:
  1. Raw external government API response payloads (`verification_results.raw_payload`).
  2. OCR bounding-box token coordinates (`extracted_fields.token_coordinates`).
  3. Dynamic rule execution evaluation trace trees (`compliance_evaluations.execution_trace`).
  4. System configuration parameters (`system_configurations.config_payload`).
- `JSONB` MUST NOT be used to bypass relational normalization for core entities (e.g., storing all requirements inside a `JSONB` array in the tender table is strictly forbidden).

### 1.3 `pgvector` Extension Usage Policy
- The `pgvector` extension is included in the database design *only where explicitly justified* for storing vector embeddings of tender clause text to support future semantic search or Retrieval-Augmented Generation (RAG).
- Vector embeddings MUST be stored in dedicated child tables (`tender_clause_embeddings`) and indexed using HNSW (Hierarchical Navigable Small World) index algorithms.

### 1.4 Single Primary Database Topology
- The architecture uses PostgreSQL as the single source of truth database.
- MongoDB, NoSQL document databases, and graph databases are explicitly rejected to prevent distributed transaction failures during officer decision sign-offs.
- PostGIS is explicitly **removed** because no spatial queries are required for CPCL bid compliance workflows.

---

## 2. Identifier Strategy for MVP

To balance database index performance, security, and public API exposure, the platform uses a dual-identifier strategy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DUAL IDENTIFIER STRATEGY                            │
├─────────────────────────┬───────────────────────────────────────────────────┤
│ INTERNAL PRIMARY KEY    │ ULID (128-bit Lexicographically Sortable Identifier)│
│                         │ • Chronologically sortable (millisecond precision)│
│                         │ • High B-tree index insertion locality            │
│                         │ • Zero auto-increment sequence leakage            │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ EXTERNAL PUBLIC KEY     │ UUIDv4 (128-bit Random Unique Identifier)         │
│                         │ • Exposed in REST API endpoints & UI routing URLs │
│                         │ • Prevents resource enumeration attacks           │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ NATURAL IDENTIFIERS     │ PAN, GSTIN, CIN, Udyam Number                     │
│                         │ • Indexed attributes under `bidder_identities`    │
│                         │ • NEVER used as single universal primary key      │
└─────────────────────────┴───────────────────────────────────────────────────┘
```

### Rationale for ULID as Internal Primary Key:
1. **Index Locality:** Standard UUIDv4 creates random B-tree insertions, causing frequent page splits and buffer pool churn on large tables. ULID starts with a 48-bit timestamp, ensuring sequential, append-friendly B-tree index performance similar to auto-increment IDs.
2. **Security:** Unlike integer auto-increment IDs (`1, 2, 3`), ULIDs do not reveal resource counts or allow simple parameter tampering enumeration attacks.
3. **Sortability:** ULIDs can be sorted chronologically without needing a separate `created_at` timestamp index scan.

---

## 3. Temporal & Versioning Architecture

The database architecture guarantees historical explainability across five versioning tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FIVE-TIER TEMPORAL VERSIONING ARCHITECTURE               │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. TENDER VERSIONING  │ `tenders` (parent container) ──► `tender_versions`  │
│                       │ Corrigenda create new version rows (v1, v2, v3).    │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. RULE VERSIONING    │ `compliance_rules` link to `policy_versions`        │
│                       │ (e.g. MII Order 2017 vs 2024 amendment).            │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. EXTRACTION VERSION │ `document_extractions` lock OCR model version       │
│                       │ and prompt schema version.                          │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. EVIDENCE VERSION   │ `evidence_records` are append-only. Corrections     │
│                       │ create new evidence version linked to parent ID.    │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 5. AUDIT VERSION      │ `audit_events` are append-only SHA-256 blocks.      │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 4. Transaction Boundaries & Isolation Levels

To ensure consistency during complex multi-step operations, explicit transaction boundaries and PostgreSQL isolation levels are defined:

| Operational Transaction Boundary | Affected Entities / Tables | Minimum Isolation Level | Concurrency Control Mechanism |
| :--- | :--- | :--- | :--- |
| **Tender Version Activation** | `tenders`, `tender_versions`, `tender_requirements` | `READ COMMITTED` | Optimistic locking via `version_number` |
| **Bid Submission Ingestion** | `bid_submissions`, `submission_covers`, `documents` | `READ COMMITTED` | Explicit Row-level lock on `bid_submissions` |
| **Verification Response Ingestion**| `verification_requests`, `verification_results`, `redis_cache` | `READ COMMITTED` | Idempotency key lookup on `request_id` |
| **Compliance Evaluation Run** | `compliance_evaluations`, `evidence_records`, `risk_profiles` | `REPEATABLE READ` | Snapshot isolation over requirement criteria |
| **Officer Decision & Sign-Off** | `officer_decisions`, `manual_overrides`, `audit_events`, `hash_blocks` | `SERIALIZABLE` | Strict serialization + Cryptographic block seal |

---

## 5. Connection Pooling & Performance Topology

- **Async Pool Management:** Backend FastAPI application connects via an asynchronous pool driver (`asyncpg`) managed by PgBouncer.
- **Connection Pool Sizing:** Configured with max 50 active connections per worker, preventing connection starvation during spike background OCR processing.
- **Read-Replica Topology:** Heavy analytical queries (e.g., CVC audit exports and reporting dashboards) are routed to PostgreSQL Read-Replicas, preserving primary master node IOPS for transactional officer decisions and document ingestion.
