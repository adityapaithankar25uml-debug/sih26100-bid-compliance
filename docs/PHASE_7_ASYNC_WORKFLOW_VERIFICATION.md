# Phase 7 — Asynchronous Workflow & Queue Verification

## 1. Asynchronous Architecture & Queue Invariants

The SIH26100 platform handles high-throughput document processing, OCR fallback execution, government registry queries, and compliance evaluations asynchronously using Celery task workers backed by Redis.

```
[HTTP Request / File Upload]
           │
           ▼
[FastAPI Route Handler] ─── (Returns 202 Accepted + Job Task ID)
           │
           ▼
[Redis Task Queue] ─── (Broker & Result Backend: sih26100-redis:6379)
           │
           ▼
[Celery Worker Pool] ─── (Executes Extraction, Verification & Evidence Creation)
           │
           ▼
[Database / S3 Event Notification] ─── (Job Status Updated to SUCCESS / FAILURE)
```

---

## 2. Verified Async Capabilities

### A. Idempotency (`X-Idempotency-Key`)
- **Header**: `X-Idempotency-Key`
- **Behavior**: When passed in API write/action requests, duplicate executions with identical keys return cached processing results without re-queuing duplicate Celery tasks.
- **Verification**: Header passed in request is explicitly reflected in response header `X-Idempotency-Key`.

### B. Correlation Lineage (`X-Correlation-ID`)
- **Header**: `X-Correlation-ID`
- **Behavior**: Uniquely tracks request flow across FastAPI middleware, Celery worker context, audit events, and frontend client.
- **Verification**: Automatically generated via ULID if omitted and attached to all response headers.

### C. Retry & Failure Resilience
- **Retry Strategy**: Exponential backoff with jitter for network/mock government adapter transient failures.
- **Dead-Letter Queue**: Permanently failing tasks recorded in database with `TECHNICAL_FAILURE` status without crashing worker pool.

### D. Workflow Status Taxonomy Separation
To prevent state collapse, the system preserves strict separation between:
1. **Document Status**: `UPLOADED`, `PROCESSING`, `PARSED`, `ERROR`
2. **Extraction Status**: `EXTRACTED`, `PENDING`, `FAILED`
3. **Government Verification Technical Status**: `SUCCESS`, `TIMEOUT`, `TRANSPORT_ERROR`
4. **Government Verification Business Status**: `ACTIVE`, `DEBARRED`, `SUSPENDED`
5. **Evidence Quality Dimensions**: 9 independent floating-point dimensions (0.0 to 1.0)
6. **Compliance Evaluation Status**: `PASS`, `FAIL`, `REVIEW_REQUIRED`
7. **Human Review Task Status**: `PENDING`, `RESOLVED`, `REJECTED`
8. **Officer Qualification Decision**: `QUALIFIED`, `DISQUALIFIED`, `UNDER_REVIEW`
9. **Async Job Status**: `PENDING`, `STARTED`, `SUCCESS`, `FAILURE`, `CANCELLED`
