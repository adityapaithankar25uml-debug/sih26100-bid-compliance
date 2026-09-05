# Phase 1 API Architecture Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-012  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines API architecture principles, REST conventions, asynchronous job specifications, header standards, and rate limiting policies. No FastAPI controllers, routes, API clients, or backend code files are created.

---

## 1. API Architectural Style & Philosophy

The SIH 26100 platform API is designed as a **RESTful JSON API over HTTPS** serving a **Modular Monolith** backend framework (FastAPI). 

### 1.1 Non-Negotiable Core API Axiom
```
AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES
```

The API design preserves this operational pipeline across all endpoints:
- AI extractions are returned as *proposals* or *unconfirmed data*.
- External verifications return *provenance tags* (`[LIVE_VERIFIED]`, `[SANDBOX_VERIFIED]`, `[MOCK_SIMULATED]`, `[MANUAL_VERIFIED]`).
- Rule engine evaluations return *deterministic itemized statuses* (`PASS`, `FAIL`, `REVIEW`, etc.).
- Officer decision endpoints enforce *mandatory justification rationale strings* and *cryptographic decision sign-off*.
- Risk scores are returned as *independent analytical metrics* (0.0 to 100.0) that CANNOT auto-qualify or auto-disqualify a bidder.

---

## 2. Base Path & Versioning Strategy

- **API Base Path:** `/api/v1`
- **Versioning Policy:** Major versioning is embedded directly in the URI path (`/api/v1/`). Non-breaking additions (new response fields, optional query parameters) do not alter the version path. Breaking schema modifications trigger a version increment to `/api/v2/`.

---

## 3. Request & Response Conventions

### 3.1 HTTP Method Usage Matrix

| HTTP Method | Usage Scope | Idempotent | Success Code |
| :--- | :--- | :--- | :--- |
| `GET` | Read resources, list collections, check job status | Yes | `200 OK` |
| `POST` | Create new resources, trigger job execution | No | `201 Created` / `202 Accepted` |
| `PUT` | Complete replacement of a mutable resource | Yes | `200 OK` |
| `PATCH` | Partial update of specific mutable attributes | No | `200 OK` |
| `DELETE` | Soft-delete non-auditable master entities | Yes | `200 OK` / `204 No Content` |

### 3.2 Standard Request & Response Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer <JWT_ACCESS_TOKEN>
X-Correlation-ID: <UUIDv4_TRACE_ID>
X-Idempotency-Key: <ULID_IDEMPOTENCY_KEY>  (Required for POST job triggers)
```

### 3.3 Identifier & Timestamp Standards
- **Public URL Parameters:** `external_id` (UUIDv4) is used for all public API path parameters (e.g., `/api/v1/tenders/f47ac10b-58cc-4372-a567-0e02b2c3d479`).
- **Timestamps:** ISO-8601 UTC strings with millisecond precision (`YYYY-MM-DDTHH:MM:SS.sssZ`).
- **Enums:** Upper-case string literals matching domain dictionary taxonomies (e.g. `PASS`, `FAIL`, `LIVE`, `MOCK`, `COMPLIANT`).

---

## 4. Synchronous vs. Asynchronous Job API Pattern

To prevent HTTP request timeouts during long-running tasks, APIs are strictly categorized into **Synchronous** and **Asynchronous Job** endpoints.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYNCHRONOUS VS. ASYNCHRONOUS JOBS                        │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ SYNCHRONOUS (Direct)  │ Fast read/write operations (< 500ms):              │
│                       │ • User auth, tender reads, requirement confirmation,│
│                       │   officer decision submission, audit log query      │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ ASYNCHRONOUS (Job)    │ Long-running background operations (> 1000ms):      │
│                       │ • Document PDF upload parsing & magic-byte check    │
│                       │ • OCR field extraction & bounding box rendering     │
│                       │ • AI tender requirement extraction                 │
│                       │ • External government API verification calls        │
│                       │ • Deterministic compliance evaluation runs          │
│                       │ • CVC audit PDF report compilation                  │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

### 4.1 Asynchronous Job Execution Pattern (`202 Accepted`)
When an asynchronous endpoint is invoked (e.g. `POST /api/v1/documents/{doc_id}/extract`):
1. The server validates headers, returns `202 Accepted`, and dispatches a Celery task queue job.
2. Response includes a `Location` header pointing to the status polling endpoint: `/api/v1/jobs/{job_id}`.
3. Client polls `GET /api/v1/jobs/{job_id}` until `status == "COMPLETED"`, then fetches the resulting resource.

```json
// Response Payload from 202 Accepted Job Trigger
{
  "status": "ACCEPTED",
  "job_id": "01HZX89J4K2P00000000000001",
  "job_type": "DOCUMENT_OCR_EXTRACTION",
  "status_endpoint": "/api/v1/jobs/01HZX89J4K2P00000000000001",
  "created_at": "2026-09-05T23:30:00.000Z"
}
```

---

## 5. Pagination, Filtering, & Sorting Conventions

### 5.1 Dual Pagination Strategy
1. **Cursor-Based Pagination (Append-Heavy Streams):** Used for `audit_events`, `evidence_records`, and `verification_attempts`. Requests pass `cursor=<ULID>` and `limit=50`. Returns `next_cursor` for deterministic $O(1)$ B-tree index traversal.
2. **Page/Limit Pagination (UI Dashboards):** Used for `tenders` list and `bidders` list. Requests pass `page=1` and `limit=20`.

```json
// Standard Paginated Response Envelope
{
  "data": [ ... ],
  "pagination": {
    "total_count": 142,
    "limit": 20,
    "page": 1,
    "total_pages": 8,
    "next_cursor": "01HZX89J4K2P00000000000099"
  }
}
```

---

## 6. Correlation IDs, Idempotency, & Concurrency Control

### 6.1 Request Correlation Tracking (`X-Correlation-ID`)
Every incoming HTTP request MUST contain or be assigned an `X-Correlation-ID` (UUIDv4). This ID is injected into audit events, Celery background jobs, and error response envelopes for end-to-end log tracing.

### 6.2 Idempotency Key Enforcement (`X-Idempotency-Key`)
Mutative operations that trigger background jobs or external verification requests require an `X-Idempotency-Key` header. 
- The key is cached in Redis with a 24-hour TTL.
- If a duplicate request arrives with the same key, the server immediately returns the cached response without re-executing the job.

### 6.3 Optimistic Concurrency Control (`ETag` / `If-Match`)
Concurrent updates to mutable resources (e.g. modifying tender version deadlines) require passing an `If-Match: "<version_number>"` header. If the entity version has changed, the server returns `409 Conflict`.

---

## 7. Rate Limiting & Circuit Breaker Policies

- **Rate Limits:** Enforced per user IP and JWT user ID via Redis sliding window middleware:
  - Standard API Endpoints: 100 requests / minute.
  - Verification & AI Job Endpoints: 20 requests / minute.
- **Circuit Breaker:** External government adapters trip to `OPEN` after 5 consecutive timeouts or 5xx server errors, fast-failing subsequent verification calls to `MANUAL_FALLBACK` mode.
