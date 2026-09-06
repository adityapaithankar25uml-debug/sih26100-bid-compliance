# Phase 7 — Integration Architecture & System Integration Specification

## 1. Overview & Architectural Boundaries

Phase 7 connects the complete modular-monolith backend and Next.js frontend into a unified, end-to-end procurement compliance verification platform for GeM procurement (CPCL / Ministry of Petroleum & Natural Gas).

### Core Architectural Axiom
`AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → RISK PRIORITIZES → HUMAN DECIDES → AUDIT REMEMBERS`

- **AI is Advisory / Non-Authoritative**: LLMs and extraction pipelines interpret raw document artifacts into normalized structured facts. AI NEVER makes qualification, disqualification, or authoritative verification decisions.
- **Authorized Government Adapters**: All 12 platform government registries (`GST`, `UDYAM`, `PAN`, `MCA`, `EPFO`, `ESIC`, `STARTUP_INDIA`, `NSIC`, `OEM_AUTH`, `DEBARMENT`, `GEM_PROFILE`, `DIGILOCKER`) operate in explicit `MOCK/DEMO` mode for SIH demo resilience.
- **Deterministic Rules Evaluation**: Compliance evaluation is executed by the rule engine based on verified facts and evidence quality.
- **9 Evidence Quality Dimensions**: Every evidence item preserves 9 independent quality dimensions (`source_authority`, `source_freshness`, `completeness`, `integrity_hash_validity`, `identity_linkage`, `document_authenticity`, `temporal_applicability`, `extraction_provenance`, `consistency`).
- **Human Officer Authority & Four-Eyes Approval**: Qualification/disqualification rests strictly with authorized procurement officers. Manual overrides exceeding threshold policies require four-eyes approval by Senior Reviewers.
- **Tamper-Evident SHA-256 Audit Hash Chain**: Every state mutation, decision, override, and verification generates a cryptographic SHA-256 audit block chained sequentially to preserve audit integrity.

---

## 2. Integrated Procurement Compliance Workflow

```
[Procurement Officer Login]
            │
            ▼
[Procurement Dashboard] ─── (Metrics, Active Tenders, Pending Tasks)
            │
            ▼
[Tender Catalog] ─── (Open TEN_01 Specs & Requirements)
            │
            ▼
[Bid Submissions Registry] ─── (Open Bid SUB_01 Workspace)
            │
            ▼
[Document Ingestion & Extraction] ─── (OCR, Fact Extraction, Normalization)
            │
            ▼
[Government Verification Center] ─── (12 Government Registries, MOCK/DEMO Badges)
            │
            ▼
[Evidence Explorer] ─── (9 Quality Dimensions, Lineage Graph)
            │
            ▼
[Deterministic Compliance Matrix] ─── (Rule Evaluation, Pass/Fail Criteria)
            │
            ▼
[Advisory Risk Engine] ─── (Risk Scoring, Priority Signals)
            │
            ▼
[Human Review Queue] ─── (Task Resolution, Discrepancy Reconciliation)
            │
            ▼
[Officer Decision & Manual Override] ─── (Policy Thresholds, Four-Eyes Approval)
            │
            ▼
[Tamper-Evident SHA-256 Audit Chain] ─── (Hash Chain Verification)
```

---

## 3. Core Component Integration Contracts

### A. Frontend to Backend Contract
- **Protocol**: REST over HTTPS/HTTP with JSON payload definitions.
- **API Base URL**: `http://localhost:8000/api/v1` (configured via `NEXT_PUBLIC_API_URL`).
- **Correlation Propagation**: Every request accepts `X-Correlation-ID` header, generated via ULID if omitted, and returned in all response headers.
- **Idempotency Propagation**: Every write/action endpoint accepts optional `X-Idempotency-Key` header, echoed back in response headers for duplicate request suppression.

### B. Async Workflow & Queue Contract
- **Task Broker**: Redis 7 Alpine (`sih26100-redis:6379`).
- **Worker**: Celery Async Workers with dead-letter queue and retry capabilities.
- **Job Status Tracking**: Polling via status endpoints with progress percentages and failure handling.

### C. Object Storage Contract
- **Storage Service**: MinIO S3-compatible storage (`sih26100-minio:9000`).
- **Bucket**: `sih26100-documents`.
- **Integrity**: SHA-256 hash computed upon upload and stored in evidence records.

---

## 4. Government Integration Classification Taxonomy

1. **LIVE**: Direct production API access with valid credentials (Not used in SIH demo).
2. **SANDBOX**: Developer sandbox environment with staging endpoints.
3. **MOCK/DEMO**: Deterministic simulated government registry responses with clear visual badges.
4. **MANUAL_FALLBACK**: Officer document upload fallback when service is offline.
5. **NOT_VERIFIED**: Source not queried or response pending.
6. **TECHNICAL_FAILURE**: Transport error or network timeout (Distinct from business failure).
