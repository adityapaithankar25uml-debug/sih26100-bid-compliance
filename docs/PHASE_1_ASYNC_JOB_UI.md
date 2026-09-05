# Phase 1 — Async Job UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Async Job UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Async Job Tracking

This specification defines the asynchronous job indicator widgets, progress polling controls, retry attempt displays, and Task 7 idempotency feedback UI.

---

## 2. Async Job Floating Indicator Panel

```
+-----------------------------------------------------------------------------------+
| ASYNC TASK MONITOR: Document OCR Batch (#JOB-8812)                                 |
| Status: PROCESSING | Progress: [==========>          ] 50% (6/12 Pages Processed)  |
| TaskAttempt: Attempt 1/3 | Idempotency Key: `job_01J891A901`                      |
+-----------------------------------------------------------------------------------+
```

---

## 3. Polling & TaskAttempt Rules

1. **Smart Exponential Backoff Polling:** Async job progress polls backend `/api/v1/jobs/{job_id}` endpoints starting at 2s intervals, backing off to 10s intervals during long-running background tasks.
2. **TaskAttempt Visualizer:** Displays retry attempts (`TaskAttempt 2/3`) when Celery workers auto-retry transient network failures.
